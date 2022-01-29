import message

class MessageHandler:
    def handle(self, bytes, conn, client_address):
        raise Exception("Method has not implemented yet")

class HandShakeMessageHandler(MessageHandler):
    def handle(self, bytes, conn, client_address):
        client_message = message.HandShakeMessage()
        client_message.fromBytes(bytes)
        print("Got an message from: ", client_message.name, "platform: ", client_message.platform)
        conn.send(message.HandShakeMessage("LILPIG_LAPTOP", "VPadServer(python)").toBytes())



class MidiMessageHandler(MessageHandler):
    def __init__(self, midi_connection):
        self.midi_connection = midi_connection

    def handle(self, bytes, conn, client_address):
        client_message = message.MidiMessage()
        client_message.fromBytes(bytes)
        print("Midi Message Handler Receive an message: ", client_message.note, client_message.velocity, client_message.state)
        self.midi_connection.sendMidiMessage(client_message)

STATE_ON = 1
STATE_OFF = 0
import arp_thread
class ArpMessageHandler(MessageHandler):

    def __init__(self, midi_connection):
        self.midi_connection = midi_connection
        # note@ip:port    ->      arp thread
        self.arp_note_list = {}

    @staticmethod
    def computed_signed_id(client_ip, client_port, message):
        return str(message.note) + "@" + client_ip + ":" + str(client_port)

    def set_node_arp_on(self, client_ip, client_port, message):
        new_arp_thread = arp_thread.ArpThread(message, self.midi_connection)
        self.arp_note_list[
            ArpMessageHandler.computed_signed_id(client_ip, client_port, message)
        ] = new_arp_thread
        new_arp_thread.startArp()


    def set_node_arp_off(self, client_ip, client_port, message):
        try:
            arp_thread_to_delete = self.arp_note_list.pop(
                ArpMessageHandler.computed_signed_id(client_ip, client_port, message)
            )
            arp_thread_to_delete.stopArp()
        except :
            # 如果要关闭的arp不在列表中，直接放弃
            pass

    def handle(self, bytes, conn, client_address):
        client_message = message.ArpMessage()
        client_message.fromBytes(bytes)
        print("Arp Message Handler Receive an message: ", client_message.note, client_message.velocity, client_message.state, client_message.rate, client_message.method, client_message.swing_pct , client_message.bpm)
        client_ip = client_address[0]
        client_port = client_address[1]
        if client_message.state == STATE_ON:
            self.set_node_arp_on(client_ip, client_port, client_message)
        else:
            self.set_node_arp_off(client_ip, client_port, client_message)


class PitchWheelMessageHandler(MessageHandler):

    def __init__(self, midi_connection):
        self.midi_connection = midi_connection

    def handle(self, bytes, conn, client_address):
         pitch_wheel_message = message.PitchWheelMessage().fromBytes(bytes)
         print("PitchWheel Message Handler Receive an message: ", pitch_wheel_message.pos, pitch_wheel_message.prev_pos)
         self.midi_connection.sendPitchMessage(pitch_wheel_message)

class ControlMessageHandler(MessageHandler):
    def __init__(self, controller_connection):
        self.controller_connection = controller_connection

    def handle(self, bytes, conn, client_address):
        control_msg = message.ControlMessage().fromBytes(bytes)
        print("Control Message Handler Receive an message: ", control_msg.operation, control_msg.state, control_msg.auto_close)
        self.controller_connection.sendControlMessage(control_msg)


class CCMessageHandler(MessageHandler):
    def __init__(self, midi_conn):
        self.midi_conn = midi_conn

    def handle(self, bytes, conn, client_address):
        cc_message = message.CCMessage().fromBytes(bytes)
        print("CC Message Handler Receive an message: ", cc_message.channel, cc_message.value)
        self.midi_conn.sendCCMessage(cc_message)

class TrackMessageHandler(MessageHandler):
    def __init__(self, controller_connection):
        self.controller_connection = controller_connection

    def handle(self, bytes, conn, client_address):
        track_message = message.TrackMessage().fromBytes(bytes)
        print("Track Message Handler Receive an message: ", track_message.nth, track_message.state, track_message.value)
        self.controller_connection.sendTrackMessage(track_message)

