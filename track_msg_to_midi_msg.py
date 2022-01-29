import mido

STATE_FADER_UP = 0
STATE_FADER_DOWN = 1
STATE_FADER_VALUE_CHANGED = 2
STATE_SOLO_ON = 3
STATE_SOLO_OFF = 4
STATE_MUTE_ON = 5
STATE_MUTE_OFF = 6
STATE_REC_ON = 7
STATE_REC_OFF = 8


TRACK_FADER_TOUCH_NOTE_OFFSET = 104
TRACK_SOLO_NOTE_OFFSET = 8
TRACK_MUTE_NOTE_OFFSET = 16
TRACK_REC_NOTE_OFFSET = 0

def _on_and_off_message(note, velocity):
    return [mido.Message('note_on', note = note, velocity = velocity), mido.Message('note_off', note = note, velocity = velocity)]


def _mapToMidoPitchValue(pos):
    return pos * 128 - 8192


def convert_to_sequence(track_msg):
    if track_msg.state == STATE_FADER_DOWN or track_msg.state == STATE_FADER_UP:
        note = TRACK_FADER_TOUCH_NOTE_OFFSET + track_msg.nth - 1
        velocity = 127 if track_msg.state == STATE_FADER_DOWN else 0
        return _on_and_off_message(note, velocity)
    elif track_msg.state == STATE_FADER_VALUE_CHANGED:
        return [mido.Message('pitchwheel', pitch=_mapToMidoPitchValue(track_msg.value), channel= track_msg.nth - 1)]
    else:
        velocity = 127
        offset = 0
        if track_msg.state == STATE_SOLO_ON or track_msg.state == STATE_SOLO_OFF:
            offset = TRACK_SOLO_NOTE_OFFSET
        elif track_msg.state == STATE_MUTE_ON or track_msg.state == STATE_MUTE_OFF:
            offset = TRACK_MUTE_NOTE_OFFSET
        elif track_msg.state == STATE_REC_ON or track_msg.state == STATE_REC_OFF:
            offset = TRACK_REC_NOTE_OFFSET
        note = offset + track_msg.nth - 1
        return _on_and_off_message(note, velocity)

