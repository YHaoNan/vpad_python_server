import mido

OP_PLAY = 0
OP_STOP = 1
OP_RECORD = 2
OP_UNDO = 3
OP_REDO = 4
OP_LOOP = 5
OP_SAVE = 6
OP_ZOOM = 7
OP_CURSOR_L = 8
OP_CURSOR_R = 9
OP_CURSOR_U = 10
OP_CURSOR_D = 11
OP_CLICK = 12
OP_TRACK_BANK_LEFT = 13
OP_TRACK_BANK_RIGHT = 14

OPERATION_MAP = {
    OP_PLAY: 94,
    OP_STOP: 93,
    OP_RECORD: 95,
    OP_UNDO: 76,
    OP_REDO: 79,
    OP_LOOP: 86,
    OP_SAVE: 80,
    OP_ZOOM: 99,
    OP_CURSOR_L: 100,
    OP_CURSOR_R: 101,
    OP_CURSOR_U: 96,
    OP_CURSOR_D: 98,
    OP_CLICK: 89,
    OP_TRACK_BANK_LEFT: 46,
    OP_TRACK_BANK_RIGHT: 47
}
"""
98 zoom in
99 zoom out 
"""
OP_STATE_OFF = 0
OP_STATE_ON = 1

def convert_to_sequence(control_msg):
    midi_msgs = []
    try:
        op_note = OPERATION_MAP[control_msg.operation]

        if control_msg.state == OP_STATE_ON:
            midi_msgs.append(mido.Message('note_on', note = op_note, velocity = 127))
            midi_msgs.append(mido.Message('note_off', note = op_note, velocity = 127))

        if control_msg.state == OP_STATE_OFF or control_msg.auto_close == 1:
            midi_msgs.append(mido.Message('note_on', note = op_note, velocity = 0))
            midi_msgs.append(mido.Message('note_off', note = op_note, velocity = 0))

        return midi_msgs
    except Exception as e:
        print(e)
        return []