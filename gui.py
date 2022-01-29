from tkinter import *
import mido
import virtual_midi_device as vmd
from constants import *
import server
import pystray
from PIL import Image

icon = None
# 窗口对象
window = None
# 服务器启动状态的StringVar
state = None
# 选定的乐器MIDI名字（对应mido端口）
inst = None
# 选定的控制MIDI名字
ctrl = None
# 睡眠实现
sleep_impl = None
# 开启或关闭按钮的StringVar
to_start_or_stop = None


# 创建虚拟MIDI设备时返回的Port，用于关闭设备、获取MIDI信号等等等等等等
_tevm_inst_port = None
_tevm_ctrl_port = None

# 调用teVirtualMIDI DLL， 创建虚拟MIDI设备
def _create_virtual_device():
    global _tevm_inst_port, _tevm_ctrl_port
    _tevm_inst_port = vmd.create_virtual_midi_device(INSTRUMENT_DEVICE_NAME)
    _tevm_ctrl_port = vmd.create_virtual_midi_device(CONTROLLER_DEVICE_NAME)

# 关闭虚拟MIDI设备，在应用程序结束时会被自动调用
def _close_virtual_device():
    if _tevm_inst_port != None: vmd.close_virtual_midi_device(_tevm_inst_port)
    if _tevm_ctrl_port != None: vmd.close_virtual_midi_device(_tevm_ctrl_port)

# 辅助方法，获取字符串数组中第一个以某一子字符串开头的列表项，如没有则返回空字符串
def _get_first_item_starts_with_or_empty(list, starts_with):
    r = ""
    for i in list:
        if i.startswith(starts_with):
            r = i
            break
    return r


# 这个方法是真正关闭窗口
def _close_window():
    # 关闭系统托盘图标
    if icon != None: icon.stop()
    # 关闭设备
    _close_virtual_device()
    # 关闭服务器
    if state.get() == "ON":
        server.stop(_stop_server_callback)
    # 销毁窗口
    window.destroy()

# 从系统托盘展示
def _show_window():
    if icon != None: icon.stop()
    window.after(0, window.deiconify)

# 当窗口关闭被点击时，拦截，不关闭窗口，最小化到系统托盘
def _hide_to_system_tray():
    global icon
    window.withdraw()
    image = Image.open("icon.ico")
    menu = (pystray.MenuItem('Quit', _close_window), pystray.MenuItem('Show', _show_window))
    icon = pystray.Icon("VPadServer", image, "VPadServer", menu)
    icon.run()


# 启动或关闭服务器
def _toggle_vpad_server():
    if state.get() == "OFF":
        server.serve(inst.get(), ctrl.get(), sleep_impl.get(), _start_server_callback)
    else:
        server.stop(_stop_server_callback)

# 服务器启动callback
def _start_server_callback(successed):
    if successed:
        state.set("ON")
        to_start_or_stop.set("STOP")

# 服务器关闭callback
def _stop_server_callback(successed):
    if successed:
        state.set("OFF")
        to_start_or_stop.set("START")


def init_ui():

    global window, state, inst, ctrl, sleep_impl, to_start_or_stop

    _create_virtual_device()

    window = Tk()
    window.geometry("260x300")
    window.title("VPadServer")

    Label(window, text="STATE: ").place(x = 10, y = 20)
    Label(window, text="INST: ").place(x = 10, y = 60)
    Label(window, text="CTRL: ").place(x = 10, y = 100)
    Label(window, text="SLEEP: ").place(x = 10, y = 140)

    state = StringVar()
    state.set("OFF")
    Label(window, textvariable=state).place(x = 80, y = 20)

    midi_outputs = mido.get_output_names()
    inst = StringVar()
    inst.set(_get_first_item_starts_with_or_empty(midi_outputs, INSTRUMENT_DEVICE_NAME))
    OptionMenu(window, inst, *midi_outputs).place(x = 80, y = 60)

    ctrl = StringVar()
    ctrl.set(_get_first_item_starts_with_or_empty(midi_outputs, CONTROLLER_DEVICE_NAME))
    OptionMenu(window, ctrl, *midi_outputs).place(x = 80, y = 100)

    sleep_impls = ("POSITIVE", "NEGATIVE")
    sleep_impl = StringVar()
    sleep_impl.set(sleep_impls[0])
    OptionMenu(window, sleep_impl, *sleep_impls).place(x = 80, y = 140)


    to_start_or_stop = StringVar()
    to_start_or_stop.set("START")
    Button(window, textvariable=to_start_or_stop, command = _toggle_vpad_server).place(x = 10, y = 240)

    Button(window, text="QUIT", command = _close_window).place(x = 80, y = 240)

    # 当点击右上角的x时，不退出，隐藏到系统托盘，
    window.protocol("WM_DELETE_WINDOW", _hide_to_system_tray)
    window.mainloop()


init_ui()