
import mido
import mido.backends.rtmidi
import time

STATE_ON = 1
STATE_OFF = 0

class MidiConnection:
    def __init__(self, midi_port):
        self.output = mido.open_output(midi_port)

    def sendCCMessage(self, ccMessage):
        self.output.send(mido.Message('control_change', control = ccMessage.channel, value = ccMessage.value))

    def sendMidiMessage(self, midiMessageFromClient):
        self.output.send(mido.Message(
            'note_on' if midiMessageFromClient.state == STATE_ON else 'note_off',
            note = midiMessageFromClient.note,
            velocity = midiMessageFromClient.velocity
        ))

    def _mapToMidoPitchValue(self, pos):
        return pos * 128 - 8192


    def sendPitchMessage(self, pitch_message):
        # 如果新位置比旧位置大，那么每次前进1步知道新位置。否则每次后退一步
        step = 1 if pitch_message.pos > pitch_message.prev_pos else -1
        current_pos = pitch_message.prev_pos + step

        # 判断当前位置是不是已经超过目标位置一步了，如果超过了就退出循环
        while current_pos != pitch_message.pos + step:
            time.sleep(0.001)
            mido_value = self._mapToMidoPitchValue(current_pos)
            print("CURRENT PITCH ", mido_value, current_pos)
            self.output.send(
                mido.Message(
                    'pitchwheel', pitch = mido_value
                )
            )
            current_pos += step
    def close(self):
        self.output.close()

import control_msg_to_midi_msg
import track_msg_to_midi_msg

class ControllerConnection:
    def __init__(self, midi_port):
        self.output = mido.open_output(midi_port)


    def sendTrackMessage(self, trackMessage):
        midi_msgs = track_msg_to_midi_msg.convert_to_sequence(trackMessage)
        print(midi_msgs)
        for msg in midi_msgs:
            self.output.send(msg)

    def sendControlMessage(self, controlMessage):
        midi_msgs = control_msg_to_midi_msg.convert_to_sequence(controlMessage)
        print(midi_msgs)
        for msg in midi_msgs:
            self.output.send(msg)

    def close(self):
        self.output.close()