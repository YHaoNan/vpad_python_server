import ctypes



# TE_VM_FLAGS_PARSE_RX tells the driver to always provide valid preparsed MIDI-commands either via Callback or via virtualMIDIGetData
TE_VM_FLAGS_PARSE_RX = (1)
# TE_VM_FLAGS_PARSE_TX tells the driver to parse all data received via virtualMIDISendData
TE_VM_FLAGS_PARSE_TX = (2)
# TE_VM_FLAGS_INSTANTIATE_RX_ONLY - Only the "midi-out" part of the port is created
TE_VM_FLAGS_INSTANTIATE_RX_ONLY = (4)
# TE_VM_FLAGS_INSTANTIATE_TX_ONLY - Only the "midi-in" part of the port is created
TE_VM_FLAGS_INSTANTIATE_TX_ONLY	= (8)
# TE_VM_FLAGS_INSTANTIATE_BOTH - a bidirectional port is created
TE_VM_FLAGS_INSTANTIATE_BOTH = (12)

# 加载DLL
tvm = ctypes.CDLL("teVirtualMIDI.dll")

# 设置virtualMIDICreatePortEx2的返回值类型，其为int指针类型
tvm.virtualMIDICreatePortEx2.restype = ctypes.POINTER(ctypes.c_int)
@ctypes.CFUNCTYPE(
    None,
    ctypes.POINTER(ctypes.c_int),  # 第一个参数 port int指针类型
    ctypes.POINTER(ctypes.c_char),  # 第二个参数 midiDataBytes
    ctypes.c_ulong,  # 第三个参数 长度
    ctypes.POINTER(ctypes.c_ulong),  # 第四个参数dwCallbackInstance
)
def _on_midi_signal_recevied_callback(port, midiDatabytes, length, dwCallbackInstance):
    tvm.virtualMIDISendData(port, midiDatabytes, length)


def create_virtual_midi_device(name):
    port = tvm.virtualMIDICreatePortEx2(name, _on_midi_signal_recevied_callback, None, None, 2, TE_VM_FLAGS_PARSE_RX)
    return port

def close_virtual_midi_device(port):
    tvm.virtualMIDIClosePort(port)
