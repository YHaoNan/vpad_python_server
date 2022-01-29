import math

MIDI_MIN_VELOCITY = 1
MIDI_MAX_VELOCITY = 127

def max_velocity(root_velocity, dynamic_pct):
    return root_velocity + math.ceil((MIDI_MAX_VELOCITY - root_velocity) * (dynamic_pct / 100))

def min_velocity(root_velocity, dynamic_pct):
    return root_velocity - math.ceil((root_velocity - MIDI_MIN_VELOCITY) * (dynamic_pct / 100))

'''
ArpVelocityAutomation
始终返回琶音起始音量
'''
class ArpVelocityAutomation:
    def __init__(self, root_velocity, dynamic_pct, up_note_cnt):
        self.dynamic_pct = dynamic_pct
        self.up_note_cnt = up_note_cnt
        self.root_velocity = root_velocity

    def next_velocity(self):
        return self.root_velocity

'''
UpArpVelocityAutoMation
在指定动态范围内将音量均分成up_note_cnt等份，然后依次升高，当琶音进行了up_note_cnt个音符后，重新依次升高
'''
class UpArpVelocityAutoMation(ArpVelocityAutomation):
    def __init__(self, root_velocity, dynamic_pct, up_note_cnt):
        ArpVelocityAutomation.__init__(self, root_velocity, dynamic_pct, up_note_cnt)
        self.velocity_range = [
            min_velocity(self.root_velocity, self.dynamic_pct),
            max_velocity(self.root_velocity, self.dynamic_pct)
        ]
        self.velocity_step_distence = math.ceil((self.velocity_range[1] - self.velocity_range[0]) / self.up_note_cnt)
        self._next_velocity = self.velocity_range[0]

    def next_velocity(self):
        result = self._next_velocity

        self._next_velocity += self.velocity_step_distence

        if self._next_velocity >= self.velocity_range[1]:
            self._next_velocity = self.velocity_range[0]

        return result

'''
DownArpVelocityAutoMation
在指定动态范围内将音量均分成up_note_cnt等份，然后依次降低，当琶音进行了up_note_cnt个音符后，重新依次降低
'''
class DownArpVelocityAutomation(ArpVelocityAutomation):
    def __init__(self, root_velocity, dynamic_pct, up_note_cnt):
        ArpVelocityAutomation.__init__(self, root_velocity, dynamic_pct, up_note_cnt)
        self.velocity_range = [
            min_velocity(self.root_velocity, self.dynamic_pct),
            max_velocity(self.root_velocity, self.dynamic_pct)
        ]
        self.velocity_step_distence = math.ceil((self.velocity_range[1] - self.velocity_range[0]) / self.up_note_cnt)
        self._next_velocity = self.velocity_range[1]

    def next_velocity(self):
        result = self._next_velocity

        self._next_velocity -= self.velocity_step_distence

        if self._next_velocity <= self.velocity_range[0]:
            self._next_velocity = self.velocity_range[1]

        return result


'''
StepArpVelocityAutomation
指定动态范围内的最大音量为强拍，指定动态范围内的最小音量为弱拍
强弱拍交替进行
'''
class StepArpVelocityAutomation(ArpVelocityAutomation):
    def __init__(self, root_velocity, dynamic_pct, up_note_cnt):
        ArpVelocityAutomation.__init__(self, root_velocity, dynamic_pct, up_note_cnt)
        self.weak_velocity = min_velocity(self.root_velocity, self.dynamic_pct)
        self.strong_velocity = max_velocity(self.root_velocity, self.dynamic_pct)
        self.counter = 0

    def next_velocity(self):
        if self.counter % 2 == 0:
            self.counter = (self.counter + 1) % 2
            return self.strong_velocity
        else:
            self.counter = (self.counter + 1) % 2
            return self.weak_velocity

import random
'''
RandomArpVelocityAutomation
指定动态范围内随机的音量
'''
class RandomArpVelocityAutomation(ArpVelocityAutomation):
    def __init__(self, root_velocity, dynamic_pct, up_note_cnt):
        ArpVelocityAutomation.__init__(self, root_velocity, dynamic_pct, up_note_cnt)
        self.velocity_range = [
            min_velocity(self.root_velocity, self.dynamic_pct),
            max_velocity(self.root_velocity, self.dynamic_pct)
        ]

    def next_velocity(self):
        return random.randint(self.velocity_range[0], self.velocity_range[1])


