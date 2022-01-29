'''
ArpMethod用来根据root_note和up_note_cnt来生成下一个音符
注意，ArpMethod生成的音符不一定在MIDI协议规定的范围内，有可能超出，具体的处理请外部根据情况进行抉择
可能是放弃该音符，或使用MIDI规定范围内最近的一个音符替代


有一些代码写的时候没有好好思考，比如时有时无的 - 1，很丑，让人摸不清头脑
可以参考arp_velocity_automation里面的代码，其实算法都差不多
'''


OCTAVE_INTERVAL = 12

class ArpMethod:
    def __init__(self, root_note, up_note_cnt):
        # self.root_note代表琶音器起始音符
        self.root_note = root_note
        # self.up_note_cnt代表琶音器能够往上上升几次
        self.up_note_cnt = up_note_cnt

    def next_note(self):
        # 默认琶音器直接返回root_note，也就是不琶音
        return self.root_note

class UpMethod(ArpMethod):
    def __init__(self, root_note, up_note_cnt):
        ArpMethod.__init__(self, root_note, up_note_cnt)
        self._next_note = self.root_note

    def next_note(self):
        result = self._next_note
        # 这里检测还是否能继续向上上升八度，如果不能，那么下一个音符就应该回到初始音符
        if ((self._next_note - self.root_note) // OCTAVE_INTERVAL) >= self.up_note_cnt - 1:
            self._next_note = self.root_note
        # 否则上升八度
        else:
            self._next_note += OCTAVE_INTERVAL
        return result

class DownMethod(ArpMethod):
    def __init__(self, root_note, up_note_cnt):
        ArpMethod.__init__(self, root_note, up_note_cnt)
        self._next_note = self.root_note


    def next_note(self):
        result = self._next_note
        # 这里检测还是否能继续向下降八度，如果不能，那么下一个音符就应该回到初始音符
        if (self.root_note - self._next_note) // OCTAVE_INTERVAL >= self.up_note_cnt - 1:
            self._next_note = self.root_note
        # 否则上升八度
        else:
            self._next_note -= OCTAVE_INTERVAL
        return result

class UpDownMethod(ArpMethod):
    def __init__(self, root_note, up_note_cnt):
        ArpMethod.__init__(self, root_note, up_note_cnt)
        self._next_note = self.root_note
        self.uping = True


    def next_note(self):
        result = self._next_note
        # 如果是上行模式，那么加八度，如果不是那么减八度
        print(self.uping)
        if self.uping:
            self._next_note += OCTAVE_INTERVAL
        else:
            self._next_note -= OCTAVE_INTERVAL

        # 如果当前音符距离初始音符距离已经超过指定距离了，那么转换模式
        dist = abs(self._next_note - self.root_note)
        if dist == 0 or dist // OCTAVE_INTERVAL > self.up_note_cnt:
            if self.uping:
                self._next_note -= OCTAVE_INTERVAL
            else:
                self._next_note += OCTAVE_INTERVAL
            self.uping = not self.uping

        return result


class DownUpMethod(UpDownMethod):
    def __init__(self, root_note, up_note_cnt):
        UpDownMethod.__init__(self, root_note, up_note_cnt)
        self.uping = False

# 这个按照大三和弦进行琶音，根音到3音距离为4，3音到5音距离为3，5音到下一个八度的根音距离为5
# 也就是根据[4,3,5]进行叠加
class ThreeChordMethod(ArpMethod):
    def __init__(self, root_note, up_note_cnt):
        ArpMethod.__init__(self, root_note, up_note_cnt)
        self._next_note = self.root_note
        # 距离列表
        self.steps = [4, 3, 5]
        # 当前是第几步，self.steps[self.nth_step % 3]即下一步需要跨越多少距离
        self.nth_step = 0

    def next_note(self):
        result = self._next_note

        self._next_note += self.steps[self.nth_step % 3]
        self.nth_step += 1

        if self.nth_step >= self.up_note_cnt:
            self._next_note = self.root_note
            self.nth_step = 0

        return result


# 七和弦不过是根据[4,3,4,1]进行叠加
class SevenChordMethod(ThreeChordMethod):
    def __init__(self, root_note, up_note_cnt):
        ThreeChordMethod.__init__(self, root_note, up_note_cnt)
        self.steps = [4, 3, 4, 1]

