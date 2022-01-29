import mido

devices = mido.get_output_names()
index = 0
for device in devices:
    print(index, ".", device)
    index = index + 1

choic = int(input("input order: "))

midi_conn = mido.open_output(devices[choic])

midi_conn.send(mido.Message('note_on', note = 94, velocity = 127, channel = 1))
midi_conn.send(mido.Message('note_on', note = 94, velocity = 0, channel = 1))
