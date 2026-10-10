import ctypes
import os
import tomllib
import uuid
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDERID_SAVED_GAMES = "{4C5C32FF-BB9D-43b0-B5B4-2D72E54EAAA4}"
DCS_FOLDERS = ("DCS", "DCS.openbeta")


def saved_games_base() -> Path:
    try:
        guid = (ctypes.c_ubyte * 16).from_buffer_copy(uuid.UUID(FOLDERID_SAVED_GAMES).bytes_le)
        shell32, ole32 = ctypes.windll.shell32, ctypes.windll.ole32
        shell32.SHGetKnownFolderPath.argtypes = [ctypes.c_void_p, wintypes.DWORD, wintypes.HANDLE, ctypes.POINTER(ctypes.c_void_p)]
        shell32.SHGetKnownFolderPath.restype = ctypes.HRESULT
        ole32.CoTaskMemFree.argtypes = [ctypes.c_void_p]
        pointer = ctypes.c_void_p()
        shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(pointer))
        try:
            return Path(ctypes.wstring_at(pointer.value))
        finally:
            ole32.CoTaskMemFree(pointer)
    except (OSError, AttributeError, ValueError, TypeError):
        return Path.home() / "Saved Games"


def detect_saved_games() -> str | None:
    base = saved_games_base()
    for name in DCS_FOLDERS:
        if (base / name / "Scripts" / "DCS-BIOS").is_dir():
            return str(base / name)
    return None


def load(path=ROOT / "config.toml") -> dict:
    if not Path(path).exists():
        raise SystemExit("config.toml not found. Copy config.example.toml to config.toml and adjust it.")
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    saved_games = cfg["dcs"]["saved_games"]
    if saved_games.strip().lower() in ("", "auto"):
        saved_games = detect_saved_games()
        if saved_games is None:
            raise SystemExit("DCS Saved Games folder not found. Set saved_games in config.toml.")
    cfg["dcs"]["saved_games"] = os.path.expandvars(saved_games)
    cfg["log"]["file"] = str(ROOT / cfg["log"]["file"])
    return cfg
