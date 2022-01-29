import threading
import time
import time_utils
import arpmessage_constants
import message

STATE_ON = 1
STATE_OFF = 0

# 如下两个常量代表ArpThread内部轮询时钟采用的休眠模式
# SLEEP_MODE_POSITIVE代表主动抢占式，这个模式会让内部时钟更加精确且不依赖具体平台，但一般会增加一些资源消耗
# SLEEP_MODE_NEGATIVE代表被动式，它使用time.sleep函数，在我的电脑下它最低延时是(1~1.5ms)，据说有的系统会达到16ms
# 被动式会让内部时钟不稳定，但由于原理是线程放弃执行，等待CPU再次分配时间片，所以它的资源消耗更小
SLEEP_MODE_POSITIVE = 1
SLEEP_MODE_NEGATIVE = 2

NOTE_DLY_BUFSIZE = 1024
class ArpThread:

    def __init__(self, arp_message, midi_connection):
        # sleep_mode是当前arp_thread时钟选择的延时策略，分为积极型和消极型，积极性占用资源更多但更精确，消极型占用资源更少，但不可控
        # 如果你的系统在消极型延时策略运行的很不错的话，那么应该启用消极型策略
        self.sleep_mode = SLEEP_MODE_POSITIVE
        # delay_ms是延时函数，通过`self.sleep_mode`确定到底使用哪个函数
        self.delay_ms = time_utils.delayMSPositive if self.sleep_mode == SLEEP_MODE_POSITIVE else time_utils.delayMSNegative
        # 用户发来的琶音消息
        self.arp_message = arp_message
        # midi连接
        self.midi_connection = midi_connection
        # 琶音线程是否已经开始
        self.is_started = False
        # 琶音线程是否已经中断
        self.is_terminated = False


    def send_message_async(self, note, velocity, lengthMS):
        def send_message():
            self.midi_connection.sendMidiMessage(
                message.MidiMessage().setup(note, velocity, STATE_ON)
            )
            self.delay_ms(lengthMS)
            self.midi_connection.sendMidiMessage(
                message.MidiMessage().setup(note, velocity, STATE_OFF)
            )

        threading.Thread(target=send_message).start()


    def run(self):
        self.is_started = True
        # 根据BPM算出每拍间隔多少秒
        print(self.arp_message.rate)
        beat_interval = 60.0 / self.arp_message.bpm
        # 根据rate算出每个音符间隔多少秒
        note_interval = beat_interval * arpmessage_constants.RATE_SCALE[self.arp_message.rate]
        note_interval_ms = note_interval * 1000
        # swing_time，如果音符从零开始，swing_time就是奇数音符的延迟时间，通过延迟奇数音符制造摇摆效果
        swing_dly_time = note_interval_ms * (self.arp_message.swing_pct / 100)

        # note_delay_ms代表琶音音符的延时，形如[0, 100, 200, 300]， 即第一个音符在第0毫秒响，第二个在第100毫秒
        # NOTE_DLY_BUFSIZE代表这个延时数组的长度，当其中最后一个元素也被消耗了，那么下面的算法会重新填充演示数组
        note_delay_ms = [(note_interval_ms * i) + (swing_dly_time if i % 2 == 1 else 0) for i in range(NOTE_DLY_BUFSIZE)]
        # 当前读取的延时数组下标位置
        note_idx = 0

        # 解析琶音方式
        arp_method = arpmessage_constants.METHOD_CLASSES[self.arp_message.method](self.arp_message.note, self.arp_message.up_note_cnt)
        # 解析力度自动化方式
        arp_velocity_automation = arpmessage_constants.VELOCITY_AUTOMATION_CLASSES[self.arp_message.velocity_automation](self.arp_message.velocity, self.arp_message.dynamic_pct, self.arp_message.up_note_cnt)


        # 琶音主循环，每次间隔1ms（实际上大概是1~1.5ms），在循环中会不断地将当前时间与琶音起始时间相减
        # 如果时间间隔大于等于某个音符了，那么它就该被消费了（意思就是触发该音符并移动note_idx）
        # 这个模型的好处在于，琶音音符之间的延时互不影响
        #   即使在C语言中，每一个语句也都需要消耗时间，更别说一个循环中的所有语句，我们假设下面的循环语句消耗的总时间为D（在我的机器上实测为1~1.5ms）
        #   我们再假设当前每一个音符之间的间隔为I
        #   如果单纯在循环中使用time.sleep(I)去等待下一次循环触发，然后播放下一个音符的话
        #   那么不得不承认实际上下一个音符会在I+D之后触发（因为循环中的每条语句都消耗了时间）
        #   那么第三个音符会在I+D+I+D后触发，你也看到了，D会越叠越多
        #   即使D只为短短的1ms（在大部分乐曲中这个延时并不起眼），但堆叠起来，可能也会变得非常多
        #   造成的效果就是，琶音器一开始还挺准确的，越来越不准。。。
        #   而我们把控制反转了，我们从被动等待到主动查询该音符是否该被触发了，这样D就独立了，不是说它被消解了，只是它不会堆叠了
        #   如：第一个音符在I+D时触发，第二个音符在I+I+D时触发，始终只有一个D
        start_time = time.perf_counter_ns()
        while not self.is_terminated:
            time_interval = (time.perf_counter_ns() - start_time)
            if time_interval >= note_delay_ms[note_idx] * 1000000:
                note_length_ms = (note_interval_ms if note_idx % 2 == 0 else note_interval_ms - swing_dly_time) / 2
                self.send_message_async(arp_method.next_note(), arp_velocity_automation.next_velocity(), note_length_ms)
                note_idx += 1
            self.delay_ms(1)
            # 如果note_delay_ms缓冲区全部被消费，那么重新填充
            if note_idx == NOTE_DLY_BUFSIZE:
                last = note_delay_ms[NOTE_DLY_BUFSIZE - 1]
                print(note_idx, NOTE_DLY_BUFSIZE, last)
                note_delay_ms = [(last + note_interval_ms * (i+1)) + (swing_dly_time if i % 2 == 1 else 0) for i in range(0, NOTE_DLY_BUFSIZE)]
                print(note_delay_ms)
                note_idx = 0






    def startArp(self):
        threading.Thread(target = ArpThread.run, args = (self,)).start()

    def stopArp(self):
        self.is_terminated = True
