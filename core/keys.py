import ctypes
import time
from ctypes import wintypes

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
MAPVK_VSC_TO_VK_EX = 3
INPUT_KEYBOARD = 1

SCAN = {
    "LCtrl": (0x1D, False), "RCtrl": (0x1D, True),
    "LShift": (0x2A, False), "RShift": (0x36, False),
    "LAlt": (0x38, False), "RAlt": (0x38, True),
    "LWin": (0x5B, True),
    "Home": (0x47, True), "End": (0x4F, True),
    "PageUp": (0x49, True), "PageDown": (0x51, True),
    "Insert": (0x52, True), "Delete": (0x53, True),
    "Up": (0x48, True), "Down": (0x50, True), "Left": (0x4B, True), "Right": (0x4D, True),
    "Space": (0x39, False), "Enter": (0x1C, False),
}
for _name, _code in zip("QWERTYUIOP", range(0x10, 0x1A)):
    SCAN[_name] = (_code, False)
for _name, _code in zip("ASDFGHJKL", range(0x1E, 0x27)):
    SCAN[_name] = (_code, False)
for _name, _code in zip("ZXCVBNM", range(0x2C, 0x33)):
    SCAN[_name] = (_code, False)
for _name, _code in zip("1234567890", range(0x02, 0x0C)):
    SCAN[_name] = (_code, False)
for _number, _code in zip(range(1, 13), list(range(0x3B, 0x45)) + [0x57, 0x58]):
    SCAN[f"F{_number}"] = (_code, False)


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [("type", wintypes.DWORD), ("u", INPUT_UNION)]


user32 = ctypes.windll.user32
user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
user32.SendInput.restype = wintypes.UINT
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.IsWindowVisible.argtypes = [wintypes.HWND]
user32.SetForegroundWindow.argtypes = [wintypes.HWND]
user32.GetForegroundWindow.restype = wintypes.HWND
user32.MapVirtualKeyW.argtypes = [wintypes.UINT, wintypes.UINT]
user32.MapVirtualKeyW.restype = wintypes.UINT
user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = ctypes.c_short

ENUM_PROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def parse(combo: str) -> list[str]:
    names = [part.strip() for part in combo.split("+")]
    for name in names:
        if name not in SCAN:
            raise ValueError(f"unknown key: {name}")
    return names


def send_key(name: str, up: bool) -> None:
    code, extended = SCAN[name]
    flags = KEYEVENTF_SCANCODE
    if extended:
        flags |= KEYEVENTF_EXTENDEDKEY
    if up:
        flags |= KEYEVENTF_KEYUP
    event = INPUT(type=INPUT_KEYBOARD)
    event.ki = KEYBDINPUT(0, code, flags, 0, 0)
    user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT))


def is_pressed(combo: str) -> bool:
    for name in parse(combo):
        code, extended = SCAN[name]
        vk = user32.MapVirtualKeyW(code | (0xE000 if extended else 0), MAPVK_VSC_TO_VK_EX)
        if vk == 0 or not user32.GetAsyncKeyState(vk) & 0x8000:
            return False
    return True


def foreground_title() -> str:
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return ""
    buffer = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(hwnd, buffer, 256)
    return buffer.value


def find_window(title: str):
    found = []

    def check(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            buffer = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(hwnd, buffer, 256)
            if title in buffer.value:
                found.append(hwnd)
                return False
        return True

    user32.EnumWindows(ENUM_PROC(check), 0)
    return found[0] if found else None


def focus(title: str) -> bool:
    hwnd = find_window(title)
    if hwnd is None:
        return False
    send_key("LShift", False)
    send_key("LShift", True)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    return user32.GetForegroundWindow() == hwnd


def press(combo: str, hold: float, gap: float = 0.0) -> None:
    names = parse(combo)
    if gap > 0:
        for name in names[:-1]:
            send_key(name, False)
        time.sleep(gap)
        send_key(names[-1], False)
        time.sleep(hold)
        send_key(names[-1], True)
        time.sleep(gap)
        for name in reversed(names[:-1]):
            send_key(name, True)
        return
    for name in names:
        send_key(name, False)
    time.sleep(hold)
    for name in reversed(names):
        send_key(name, True)
