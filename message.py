import byte_utils


MSG_HANDSHAKE = 1
MSG_MIDI = 2
MSG_ARP = 3
MSG_CHORD = 4
MSG_PITCH_WHEEL = 5
MSG_MODULATION_WHEEL = 6
MSG_CC = 7
MSG_CONTROL = 8
MSG_TRACK = 9


class Message:
    def __init__(self, op):
        self.op = op

    def fromBytes(self, bytes):
        raise Exception("Not implemented yet!")

    def toBytes(self):
        raise Exception("Not implemented yet!")

class HandShakeMessage(Message):
    def __init__(self, name = None, platform = None):
        Message.__init__(self, MSG_HANDSHAKE)
        self.name = name
        self.platform = platform

    def fromBytes(self, bytes):
        offset = 1
        self.name, n = byte_utils.read_string(bytes, offset)
        offset += n
        self.platform, n = byte_utils.read_string(bytes, offset)
        offset += n
        return self

    def toBytes(self):
        return bytes(byte_utils.message([
            byte_utils.int1(self.op),
            byte_utils.string(self.name),
            byte_utils.string(self.platform)
        ]))

class MidiMessage(Message):
    def __init__(self):
        Message.__init__(self, MSG_MIDI)

    def setup(self, note, velocity, state):
        self.note = note
        self.velocity = velocity
        self.state = state
        return self

    def fromBytes(self, bytes):
        offset = 1
        self.note, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.velocity, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.state, n = byte_utils.read_int1(bytes, offset)
        offset += n
        return self


class ArpMessage(Message):
    def __init__(self):
        Message.__init__(self, MSG_ARP)

    def setup(self, note, velocity, state, method, rate, swing_pct, up_note_cnt, velocity_automation, dynamic_pct, bpm):
        self.note = note
        self.velocity = velocity
        self.state = state
        self.method = method
        self.rate = rate
        self.swing_pct = swing_pct
        self.up_note_cnt = up_note_cnt
        self.velocity_automation = velocity_automation
        self.dynamic_pct = dynamic_pct
        self.bpm = bpm
        return self

    def toBytes(self):
        return bytes(byte_utils.message([
            byte_utils.int1(self.op),
            byte_utils.int1(self.note),
            byte_utils.int1(self.velocity),
            byte_utils.int1(self.state),
            byte_utils.int1(self.method),
            byte_utils.int1(self.rate),
            byte_utils.int1(self.swing_pct),
            byte_utils.int1(self.up_note_cnt),
            byte_utils.int1(self.velocity_automation),
            byte_utils.int2(self.dynamic_pct),
            byte_utils.int2(self.bpm)
        ]))


    def fromBytes(self, bytes):
        offset = 1
        def read_by_method_and_skip(read_method):
            nonlocal offset
            result, n = read_method(bytes, offset)
            offset+=n
            return result

        self.note = read_by_method_and_skip(byte_utils.read_int1)
        self.velocity = read_by_method_and_skip(byte_utils.read_int1)
        self.state = read_by_method_and_skip(byte_utils.read_int1)
        self.method = read_by_method_and_skip(byte_utils.read_int1)
        self.rate = read_by_method_and_skip(byte_utils.read_int1)
        self.swing_pct = read_by_method_and_skip(byte_utils.read_int1)
        self.up_note_cnt = read_by_method_and_skip(byte_utils.read_int1)
        self.velocity_automation = read_by_method_and_skip(byte_utils.read_int1)
        self.dynamic_pct = read_by_method_and_skip(byte_utils.read_int2)
        self.bpm = read_by_method_and_skip(byte_utils.read_int2)
        return self


class PitchWheelMessage(Message):
    def __init__(self):
        Message.__init__(self, MSG_PITCH_WHEEL)

    def setup(self, pos, prev_pos):
        self.pos = pos
        self.prev_pos = prev_pos
        return self

    def toBytes(self):
        return bytes(byte_utils.message([
            byte_utils.int1(self.op),
            byte_utils.int1(self.pos),
            byte_utils.int1(self.prev_pos)
        ]))

    def fromBytes(self, bytes):
        offset = 1
        self.pos, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.prev_pos, n = byte_utils.read_int1(bytes, offset)
        return self


class ModulationWheelMessage(PitchWheelMessage):
    def __init__(self):
        Message.__init__(self, MSG_MODULATION_WHEEL)


class ControlMessage(MidiMessage):
    def __init__(self):
        Message.__init__(self, MSG_CONTROL)

    def setup(self, operation, state, auto_close):
        self.operation = operation
        self.state = state
        self.auto_close = auto_close
        return self

    def fromBytes(self, bytes):
        offset = 1
        self.operation, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.state, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.auto_close, n = byte_utils.read_int1(bytes, offset)
        offset += n
        return self

    def toBytes(self):
        return bytes(byte_utils.message([
            byte_utils.int1(self.op),
            byte_utils.int1(self.operation),
            byte_utils.int1(self.state),
            byte_utils.int1(self.auto_close)
        ]))

class TrackMessage(MidiMessage):
    def __init__(self):
        Message.__init__(self, MSG_TRACK)


    def setup(self, nth, state, value):
        self.nth = nth
        self.state = state
        self.value = value
        return self


    def fromBytes(self, bytes):
        offset = 1
        self.nth, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.state, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.value, n = byte_utils.read_int1(bytes, offset)
        offset += n
        return self

    def toBytes(self):
        return bytes(byte_utils.message([
            byte_utils.int1(self.op),
            byte_utils.int1(self.nth),
            byte_utils.int1(self.state),
            byte_utils.int1(self.value)
        ]))

class CCMessage(MidiMessage):
    def __init__(self):
        Message.__init__(self, MSG_CC)

    def setup(self, channel, value):
        self.channel = channel
        self.value = value
        return self

    def fromBytes(self, bytes):
        offset = 1
        self.channel, n = byte_utils.read_int1(bytes, offset)
        offset += n
        self.value, n = byte_utils.read_int1(bytes, offset)
        offset += n
        return self

    def toBytes(self):
        return bytes(byte_utils.message([
            byte_utils.int1(self.op),
            byte_utils.int1(self.nth),
            byte_utils.int1(self.value)
        ]))

