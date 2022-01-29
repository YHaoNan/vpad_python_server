import mido
import time

devices = mido.get_output_names()
index = 0
for device in devices:
    print(index, ".", device)
    index = index + 1

choic = int(input("input order: "))

midi_conn = mido.open_output(devices[choic])

midi_conn.send(mido.Message('pitchwheel', pitch = 7000))
time.sleep(2)

midi_conn.send(mido.Message('pitchwheel', pitch = 5000))
time.sleep(2)
