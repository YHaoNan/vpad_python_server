import socketserver
import message_handler
import byte_utils
import midi_connection
import constants
import threading

_message_handlers = None


_BUFFER_SIZE = 1024
class VPadRequestHandler(socketserver.BaseRequestHandler):

    def handle(self) -> None:
        while True:
            self.data = self.request.recv(_BUFFER_SIZE)
            print(self.data)
            # 如果没有数据了 跳出循环
            if(len(self.data) == 0): break
            # 开始读取数据 暂时没有考虑数据超出缓冲区的情况
            self.offset = 0
            while self.offset < len(self.data):
                message_bytes = self.read_an_message_bytes()
                message_handler = self.resolve_message_handlers(message_bytes)
                message_handler.handle(message_bytes, self.request, self.client_address)


    def skip_bytes(self, n):
        self.offset += n

    def read_an_message_bytes(self):
        # 读取一个消息的首两个字节，这个字节代表消息的长度
        length, n = byte_utils.read_int2(self.data, self.offset)
        # 跳过读取的字节
        self.skip_bytes(n)

        # 读取消息体，这个消息体已经不包含代表长度两个字节了
        message_bytes = byte_utils.slice(self.data, self.offset, length)
        # 跳过该消息，执行完这行，self.offset应该在下一条消息首部
        self.skip_bytes(length)
        return message_bytes


    def resolve_message_handlers(self, message_bytes):
        print(message_bytes[0])
        return _message_handlers[message_bytes[0]]



_server = None
_server_thread = None
_inst_midi_conn = None
_controller_midi_conn = None

def serve(inst_midi_port, controller_midi_port, sleep_impl, callback):
    global _server, _server_thread, _message_handlers, _inst_midi_conn, _controller_midi_conn

    _inst_midi_conn = midi_connection.MidiConnection(inst_midi_port)
    _controller_midi_conn = midi_connection.ControllerConnection(controller_midi_port)

    _message_handlers = [
        None,
        message_handler.HandShakeMessageHandler(),
        message_handler.MidiMessageHandler(_inst_midi_conn),
        message_handler.ArpMessageHandler(_inst_midi_conn),
        None, # chord
        message_handler.PitchWheelMessageHandler(_inst_midi_conn),
        None, # modulation
        message_handler.CCMessageHandler(_inst_midi_conn), # CC
        message_handler.ControlMessageHandler(_controller_midi_conn),
        message_handler.TrackMessageHandler(_controller_midi_conn)
    ]

    if _server == None:
        _server = socketserver.ThreadingTCPServer(('0.0.0.0', constants.VPAD_SERVER_PORT), VPadRequestHandler)
        _server_thread = threading.Thread(target=_server.serve_forever)
        _server_thread.setName("server thread")
        _server_thread.setDaemon(True)
        _server_thread.start()
        callback(True)
    else:
        callback(False)
        # raise Exception("There is already has a server instance.")

def stop(callback):
    global _server,_server_thread

    if _server != None:
        _server.shutdown()
        _server_thread.join()
        _server.server_close()
        _server_thread = None
        _server = None
        if _inst_midi_conn != None: _inst_midi_conn.close()
        if _controller_midi_conn != None: _controller_midi_conn.close()
        callback(True)
    else:
        callback(False)
