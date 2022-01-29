import arp_methods
import arp_velocity_automation

METHOD_NO_METHOD = 0
METHOD_UP = 1
METHOD_DOWN = 2
METHOD_UP_DOWN = 3
METHOD_DOWN_UP = 4
METHOD_3CHORD = 5
METHOD_7CHORD = 6
METHOD_CLASSES = [arp_methods.ArpMethod, arp_methods.UpMethod, arp_methods.DownMethod, arp_methods.UpDownMethod, arp_methods.DownUpMethod, arp_methods.ThreeChordMethod, arp_methods.SevenChordMethod]


RATE_1_1 = 0
RATE_1_2_D = 1
RATE_1_1_T = 2
RATE_1_2 = 3
RATE_1_4_D = 4
RATE_1_2_T = 5
RATE_1_4 = 6
RATE_1_8_D = 7
RATE_1_4_T = 8
RATE_1_8 = 9
RATE_1_16_D = 10
RATE_1_8_T = 11
RATE_1_16 = 12
RATE_1_32_D = 13
RATE_1_16_T = 14
RATE_1_32 = 15
RATE_1_64_D = 16
RATE_1_32_T = 17
RATE_1_64 = 18
RATE_1_64_T = 19

# Arp Thread使用一个拍子的长度去按照客户端发来的模式乘以 RATE_SCALE中的数值
# 如BPM是130，那么一个拍子的长度就是60 / 130，这里ArpThread目前只支持4/4拍
RATE_SCALE = [0 for i in range(20)]

# RATE_1_1是全音符，所以系数是4，就是4个拍子的长度
RATE_SCALE[RATE_1_1] = 4
# RATE_1_1_T是全音符的三连音，它比全音符短一些
# 三个全音符三连音正好填满两个拍子(等于2个全音符)，所以这里使用全音符*2/3
RATE_SCALE[RATE_1_1_T] = RATE_SCALE[RATE_1_1] * 2 / 3
RATE_SCALE[RATE_1_2] = 2
# RATE_1_2_D是二分音符加上附点，比二分音符再长二分音符的一半
RATE_SCALE[RATE_1_2_D] = RATE_SCALE[RATE_1_2] * 1.5
RATE_SCALE[RATE_1_2_T] = RATE_SCALE[RATE_1_2] * 2 / 3
RATE_SCALE[RATE_1_4] = 1
RATE_SCALE[RATE_1_4_D] = RATE_SCALE[RATE_1_4] * 1.5
RATE_SCALE[RATE_1_4_T] = RATE_SCALE[RATE_1_4] * 2 / 3
RATE_SCALE[RATE_1_8] = 0.5
RATE_SCALE[RATE_1_8_D] = RATE_SCALE[RATE_1_8] * 1.5
RATE_SCALE[RATE_1_8_T] = RATE_SCALE[RATE_1_8] * 2 / 3
RATE_SCALE[RATE_1_16] = 0.25
RATE_SCALE[RATE_1_16_D] = RATE_SCALE[RATE_1_16] * 1.5
RATE_SCALE[RATE_1_16_T] = RATE_SCALE[RATE_1_16] * 2 / 3
RATE_SCALE[RATE_1_32] = 0.125
RATE_SCALE[RATE_1_32_D] = RATE_SCALE[RATE_1_32] * 1.5
RATE_SCALE[RATE_1_32_T] = RATE_SCALE[RATE_1_32] * 2 / 3
RATE_SCALE[RATE_1_64] = 0.0625
RATE_SCALE[RATE_1_64_D] = RATE_SCALE[RATE_1_64] * 1.5
RATE_SCALE[RATE_1_64_T] = RATE_SCALE[RATE_1_64] * 2 / 3


VELOCITY_NO_AUTOMATION = 0
VELOCITY_UP = 1
VELOCITY_DOWN = 2
VELOCITY_UP_DOWN = 3
VELOCITY_DOWN_UP = 4
VELOCITY_STEP = 5
VELOCITY_RANDOM = 6

VELOCITY_AUTOMATION_CLASSES = [
    arp_velocity_automation.ArpVelocityAutomation,
    arp_velocity_automation.UpArpVelocityAutoMation,
    arp_velocity_automation.DownArpVelocityAutomation,
    arp_velocity_automation.ArpVelocityAutomation,
    arp_velocity_automation.ArpVelocityAutomation,
    arp_velocity_automation.StepArpVelocityAutomation,
    arp_velocity_automation.RandomArpVelocityAutomation
]