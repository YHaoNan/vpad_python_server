import socket
import message
import arpmessage_constants as AC

DATAPACK = "./data/datapack1"
SERVER = "localhost"
PORT = 1236


# with open(DATAPACK, 'r', encoding="utf-8") as file:
#     bytes_hex = file.readline()[:-1].split(" ")
#     bytes = bytes([int(hex_str, 16) for hex_str in bytes_hex ])
#     s = socket.socket()
#     s.connect((SERVER, PORT))
#     s.send(bytes)
#     print("send ok!")
#     result = s.recv(1024)
#     print("result -> ", result)


import time
RATE = AC.RATE_1_16
BPM = 130
NOTE = 48
METHOD = AC.METHOD_7CHORD
UP_NOTE_CNT = 4
SWING_PCT = 0
VELOCITY_AUTOMATION = AC.VELOCITY_UP
DYNAMIC = 100


TEST_TIME = 10

s = socket.socket()
s.connect((SERVER, PORT))
s.send(message.ArpMessage().setup(NOTE,60,1,METHOD, RATE, SWING_PCT, UP_NOTE_CNT, VELOCITY_AUTOMATION, DYNAMIC, BPM).toBytes())
print("SEND OK")
time.sleep(TEST_TIME)
s.send(message.ArpMessage().setup(NOTE,60,0,METHOD, RATE, SWING_PCT, UP_NOTE_CNT, VELOCITY_AUTOMATION, DYNAMIC, BPM).toBytes())
print("SEND OK")

