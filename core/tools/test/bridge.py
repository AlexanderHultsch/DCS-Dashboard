#!/usr/bin/env python3
"""Run core/dashboard.py in the foreground with a fake keys module (Ctrl+C stops it).

The fake module never presses a real key. Every call is appended to logs/test/keys.log,
e.g. `press ('LCtrl+LAlt+G', 0.1, 0.0)` (key combination, hold time in seconds, gap).
"""
import sys
import types
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KEYS_LOG = REPO / "logs" / "test" / "keys.log"
KEYS_LOG.parent.mkdir(parents=True, exist_ok=True)

source = (REPO / "core" / "keys.py").read_text(encoding="utf-8")
scan_ns = {}
exec(source[:source.index("class KEYBDINPUT")], scan_ns)
SCAN = scan_ns["SCAN"]


def log_call(name, *args):
    with open(KEYS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{name} {args!r}\n")


def parse(combo):
    names = [part.strip() for part in combo.split("+")]
    for name in names:
        if name not in SCAN:
            raise ValueError(f"unknown key: {name}")
    return names


fake = types.ModuleType("keys")
fake.SCAN = SCAN
fake.parse = parse
fake.is_pressed = lambda combo: parse(combo) and False
fake.foreground_title = lambda: ""
fake.find_window = lambda title: None
fake.send_key = lambda name, up: log_call("send_key", name, up)
fake.focus = lambda title: log_call("focus", title) or True
fake.press = lambda combo, hold, gap=0.0: log_call("press", combo, hold, gap)
sys.modules["keys"] = fake

sys.path.insert(0, str(REPO / "core"))
import dashboard

dashboard.main()
