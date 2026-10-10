import json
import math
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from bridge import config, dcsbios, export, keys, log

POWER_POSITIONS = [
    {"value": 0, "label": "OFF"},
    {"value": 16383, "label": "IDLE"},
    {"value": 58981, "label": "FLY"},
    {"value": 65535, "label": "LOCKOUT", "disabled": True},
]
ENGINE_START_POSITIONS = [
    {"value": 2, "label": "START", "momentary": True},
    {"value": 1, "label": "OFF"},
    {"value": 0, "label": "IGN ORIDE", "momentary": True},
]
MODE_POSITIONS = [
    {"value": 2, "label": "DAY"},
    {"value": 1, "label": "NT"},
    {"value": 0, "label": "MONO"},
]
KNOB_STEP = 3200
MPD_BUTTON_HOLD = 0.15
MPD_LABELS = {"B1": "M", "AC": "A/C", "AST": "*"}
KU_LABELS = {
    "DOT": ".", "SIGN": "+/-", "SLASH": "/", "DIV": "\u00f7", "MULTI": "*", "PLUS": "+",
    "MINUS": "\u2212", "BKS": "BKS", "SPC": "SPC", "CLR": "CLR", "ENT": "ENTER", "LEFT": "\u2190", "RIGHT": "\u2192",
}


def mpd_controls(side: str) -> list[dict]:
    slots = [f"{row}{n}" for row in "TLRB" for n in range(1, 7)] + ["FCR", "WPN", "TSD", "VID", "COM", "AC", "AST"]
    controls = [
        {"id": f"{{seat}}_MPD_{side}_{slot}", "label": MPD_LABELS.get(slot, slot), "type": "button", "hold": MPD_BUTTON_HOLD, "side": side, "slot": slot}
        for slot in slots
    ]
    controls += [
        {"id": f"{{seat}}_MPD_{side}_BRT", "label": "BRT", "type": "knob", "step": KNOB_STEP, "side": side, "slot": "BRT"},
        {"id": f"{{seat}}_MPD_{side}_VIDEO", "label": "VID", "type": "knob", "step": KNOB_STEP, "side": side, "slot": "VIDEO"},
        {"id": f"{{seat}}_MPD_{side}_MODE", "label": "MODE", "type": "selector", "step_fallback": True, "positions": MODE_POSITIONS, "side": side, "slot": "MODE"},
    ]
    return controls


def ku_controls() -> list[dict]:
    slots = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + list(KU_LABELS)
    controls = [{"id": "{seat}_KU_DISPLAY", "label": "SCRATCHPAD", "type": "display", "slot": "DISPLAY"}]
    controls += [
        {"id": f"{{seat}}_KU_{slot}", "label": KU_LABELS.get(slot, slot), "type": "button", "hold": MPD_BUTTON_HOLD, "slot": slot}
        for slot in slots
    ]
    controls.append({"id": "{seat}_KU_BRT", "label": "BRT", "type": "knob", "step": KNOB_STEP, "slot": "BRT"})
    return controls


VIEWS = [
    {
        "name": "Startup",
        "seats": [0],
        "lamps": [
            {"id": "PLT_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "PLT_INTL_MWARN_BTN"},
            {"id": "PLT_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "PLT_INTL_MCAUTION_BTN"},
            {"id": "PLT_ENG_1_FIRE_L", "label": "ENG 1 FIRE", "color": "red"},
            {"id": "PLT_APU_FIRE_L", "label": "APU FIRE", "color": "red"},
            {"id": "PLT_ENG_2_FIRE_L", "label": "ENG 2 FIRE", "color": "red"},
            {"id": "PLT_APU_L", "label": "APU ON", "color": "green"},
        ],
        "controls": [
            {"id": "PLT_MASTER_IGN_SW", "label": "MSTR IGN", "type": "selector", "positions": [{"value": 0, "label": "OFF"}, {"value": 1, "label": "BATT"}, {"value": 2, "label": "EXT PWR", "disabled": True}], "grid": [1, 1, 1, 1]},
            {"id": "PLT_APU_BTN_CVR", "label": "APU COVER", "type": "selector", "positions": [{"value": 0, "label": "CLOSED"}, {"value": 1, "label": "OPEN"}], "grid": [1, 2, 1, 1]},
            {"id": "PLT_APU_BTN", "label": "APU", "type": "button", "hold": 0.3, "requires": {"id": "PLT_APU_BTN_CVR", "value": 1}, "grid": [1, 3, 1, 1]},
            {"id": "PLT_ENG1_START", "label": "ENG 1 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS, "grid": [1, 4, 1, 1]},
            {"id": "PLT_ENG2_START", "label": "ENG 2 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS, "grid": [1, 5, 1, 1]},
            {"id": "power_left", "label": "PWR LVR 1", "type": "lever", "readback": "PLT_ENG_L_PW_LVR", "side": "left", "positions": POWER_POSITIONS, "grid": [1, 6, 3, 1]},
            {"id": "power_right", "label": "PWR LVR 2", "type": "lever", "readback": "PLT_ENG_R_PW_LVR", "side": "right", "positions": POWER_POSITIONS, "grid": [1, 7, 3, 1]},
            {"id": "PLT_ROTOR_BRK", "label": "RTR BRK", "type": "selector", "positions": [{"value": 2, "label": "OFF"}, {"value": 1, "label": "BRK", "disabled": True}, {"value": 0, "label": "LOCK"}], "grid": [2, 1, 1, 1]},
            {"id": "PLT_PARK_BRAKE", "label": "PARK BRAKE", "type": "selector", "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "PULLED"}], "grid": [2, 2, 1, 1]},
            {"id": "PLT_T_WHEEL_UNLOCK_BTN", "label": "TAIL WHEEL", "type": "button", "hold": 0.3, "lamp": "PLT_T_WHEEL_UNLOCK_L", "legend": "UNLOCK", "seats": [0], "grid": [2, 5, 1, 1]},
            {"id": "PLT_EXTL_NAV_L_SW", "label": "NAV", "type": "selector", "positions": [{"value": 2, "label": "BRT"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "DIM"}], "grid": [2, 3, 1, 1]},
            {"id": "PLT_EXTL_ACOL_L_SW", "label": "ANTI COL", "type": "selector", "positions": [{"value": 2, "label": "WHT"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "RED"}], "grid": [2, 4, 1, 1]},
            {"id": "PLT_MPD_L_MODE", "label": "MPD L", "type": "selector", "step_fallback": True, "positions": MODE_POSITIONS, "grid": [3, 1, 1, 1]},
            {"id": "PLT_MPD_R_MODE", "label": "MPD R", "type": "selector", "step_fallback": True, "positions": MODE_POSITIONS, "grid": [3, 2, 1, 1]},
            {"id": "canopy", "label": "CANOPY", "type": "key", "key": "canopy", "readback": "PLT_CANOPY", "states": {"0": "CLOSED", "1": "OPEN"}, "grid": [3, 3, 1, 3]},
        ],
    },
    {
        "name": "Flight",
        "seats": [0, 1],
        "lamps": [
            {"id": "{seat}_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "{seat}_INTL_MWARN_BTN"},
            {"id": "{seat}_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "{seat}_INTL_MCAUTION_BTN"},
            {"id": "PLT_ENG_1_FIRE_L", "label": "ENG 1 FIRE", "color": "red"},
            {"id": "PLT_APU_FIRE_L", "label": "APU FIRE", "color": "red"},
            {"id": "PLT_ENG_2_FIRE_L", "label": "ENG 2 FIRE", "color": "red"},
            {"id": "PLT_APU_L", "label": "APU ON", "color": "green"},
        ],
        "controls": [
            {"id": "controls", "label": "CONTROLS", "type": "controls", "grid": [1, 1, 3, 3]},
            {"id": "{seat}_CYCLIC_SYMBOLOGY", "label": "SYMBOLOGY", "type": "hat", "ud": "{seat}_CYCLIC_SYMBOLOGY", "hold": 0.3, "positions": {"up": "T/C", "down": "H/B"}, "grid": [1, 4, 2, 1]},
            {"id": "monocle", "label": "MONOCLE", "type": "key", "key": "monocle", "grid": [1, 5, 1, 1]},
            {"id": "PLT_T_WHEEL_UNLOCK_BTN", "label": "TAIL WHEEL", "type": "button", "hold": 0.3, "lamp": "PLT_T_WHEEL_UNLOCK_L", "legend": "UNLOCK", "seats": [0], "grid": [2, 5, 1, 1]},
            {"id": "flight_power_left", "label": "PWR LVR 1", "type": "lever", "readback": "{seat}_ENG_L_PW_LVR", "side": "left", "positions": POWER_POSITIONS, "grid": [1, 6, 3, 1]},
            {"id": "flight_power_right", "label": "PWR LVR 2", "type": "lever", "readback": "{seat}_ENG_R_PW_LVR", "side": "right", "positions": POWER_POSITIONS, "grid": [1, 7, 3, 1]},
        ],
    },
    {
        "name": "Fight",
        "seats": [0, 1],
        "lamps": [
            {"id": "{seat}_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "{seat}_INTL_MWARN_BTN"},
            {"id": "{seat}_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "{seat}_INTL_MCAUTION_BTN"},
            {"id": "{seat}_MASTER_ARM_ARM_L", "label": "ARM", "color": "amber"},
            {"id": "{seat}_MASTER_ARM_SAFE_L", "label": "SAFE", "color": "green"},
            {"id": "{seat}_GROUND_OVERRIDE_L", "label": "GND ORIDE", "color": "amber"},
        ],
        "controls": [
            {"id": "{seat}_MASTER_ARM_BTN", "label": "A/S", "type": "button", "hold": 0.3},
            {"id": "{seat}_GROUND_OVERRIDE_BTN", "label": "GND ORIDE", "type": "button", "hold": 0.3},
            {"id": "{seat}_WAS", "label": "WAS", "type": "hat", "ud": "{seat}_CYCLIC_WEAPON_UD", "lr": "{seat}_CYCLIC_WEAPON_LR", "hold": 0.3, "positions": {"up": "G", "down": "A", "left": "R", "right": "M"}},
            {"id": "{seat}_SIGHT_SEL", "label": "SIGHT SEL", "type": "hat", "ud": "{seat}_COLLECTIVE_SIGHT_SELECT_UD", "lr": "{seat}_COLLECTIVE_SIGHT_SELECT_LR", "hold": 0.3, "positions": {"up": "HMD", "down": "LINK", "left": "FCR", "right": "TADS"}},
            {"id": "{seat}_CYCLIC_FLARE", "label": "FLARE", "type": "button", "hold": 0.3},
            {"id": "{seat}_CYCLIC_CHAFF", "label": "CHAFF", "type": "button", "hold": 0.3},
            {"id": "PLT_CMWS_FLARE_COUNT", "label": "FLARE COUNT", "type": "display"},
            {"id": "PLT_CMWS_CHAFF_COUNT", "label": "CHAFF COUNT", "type": "display"},
        ],
    },
    {"name": "MPD", "seats": [0, 1], "layout": "mpd", "lamps": [], "controls": mpd_controls("L") + mpd_controls("R")},
    {"name": "KU", "seats": [0, 1], "layout": "ku", "lamps": [], "controls": ku_controls()},
]

LEVER_KEYS = {(0, 1): "idle", (1, 2): "up", (2, 1): "down", (1, 0): "off"}
LEVER_WAIT = 1.0
STEP_WAIT = 0.5
STEP_TRIES = 2

CONTROL_NAMES = [f"{seat}_{axis}" for seat in ("plt", "cpg") for axis in ("cyc_pitch", "cyc_roll", "coll", "pedals")]

SEAT = "SEAT_POSITION"
SEAT_NAMES = {0: "PLT", 1: "CPG"}
INDEX = Path(__file__).resolve().parent / "web" / "index.html"
ICON = Path(__file__).resolve().parent / "web" / "apple-touch-icon.png"
SETTINGS_FILE = Path(__file__).resolve().parent / "settings.json"

cfg = {}
settings = {}
outputs = {}
state = dcsbios.new_state()
lock = threading.Lock()
command_lock = threading.Lock()
last_packet = None
control_values = {}
control_packet = None
cmd_sock = None


def expand(name: str, seat: int) -> str:
    return name.replace("{seat}", SEAT_NAMES[seat])


def expand_all(name: str) -> list[str]:
    if "{seat}" in name:
        return [expand(name, seat) for seat in SEAT_NAMES]
    return [name]


def read_names() -> list[str]:
    names = [SEAT]
    for view in VIEWS:
        for lamp in view["lamps"]:
            names += expand_all(lamp["id"])
        for control in view["controls"]:
            if control["type"] == "lever":
                names += expand_all(control["readback"])
            elif control["type"] == "key":
                if "readback" in control:
                    names += expand_all(control["readback"])
            elif control["type"] == "hat":
                names += expand_all(control["ud"])
                if "lr" in control:
                    names += expand_all(control["lr"])
            elif control["type"] != "controls":
                names += expand_all(control["id"])
            if "lamp" in control:
                names += expand_all(control["lamp"])
    return list(dict.fromkeys(names))


def reader(sock: socket.socket) -> None:
    global last_packet
    while True:
        data = sock.recv(65536)
        with lock:
            try:
                dcsbios.apply_packet(state, data)
            except ValueError as e:
                log.line("bridge", "dcsbios packet skipped", e)
                continue
            last_packet = time.monotonic()


def export_reader(sock: socket.socket) -> None:
    global control_packet
    while True:
        data = sock.recv(65536)
        try:
            values = export.parse(data)
        except ValueError:
            continue
        with lock:
            for name in CONTROL_NAMES:
                try:
                    number = float(values[name])
                except (KeyError, ValueError):
                    continue
                if math.isfinite(number):
                    control_values[name] = number
            control_packet = time.monotonic()


def read(name: str):
    return dcsbios.read_value(state, outputs[name])


def load_settings() -> dict:
    result = {"logging": True}
    try:
        with open(SETTINGS_FILE, encoding="utf-8") as f:
            saved = json.load(f)
    except (OSError, ValueError):
        return result
    if isinstance(saved, dict):
        result.update(saved)
    return result


def save_settings(data: dict) -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def settings_reply() -> dict:
    return {
        "logging": settings["logging"],
        "saved_games": cfg["dcs"]["saved_games"],
        "address": f"http://{lan_ip()}:{cfg['dashboard']['port']}",
    }


def change_settings(body: dict) -> bool:
    enabled = body.get("logging")
    if not isinstance(enabled, bool):
        return False
    if enabled:
        log.set_file_logging(True)
        log.line("bridge", "settings", "file logging on")
    else:
        log.line("bridge", "settings", "file logging off")
        log.set_file_logging(False)
    settings["logging"] = enabled
    save_settings(settings)
    return True


def snapshot() -> dict:
    with lock:
        now = time.monotonic()
        age = None if last_packet is None else round(now - last_packet, 1)
        controls_age = None if control_packet is None else round(now - control_packet, 1)
        return {
            "seat": read(SEAT),
            "age": age,
            "values": {name: read(name) for name in outputs if name != SEAT},
            "controls": dict(control_values),
            "controls_age": controls_age,
        }


def find_control(identifier):
    for view in VIEWS:
        for control in view["controls"]:
            if control["id"] == identifier:
                return control, view
        for lamp in view["lamps"]:
            if lamp.get("button") == identifier:
                return {"id": identifier, "type": "button", "hold": 0.3}, view
    return None, None


def send(identifier: str, value) -> None:
    dcsbios.send(cmd_sock, cfg["dcs_bios"]["command_port"], identifier, value)


def lever_index(control: dict, raw: int) -> int:
    positions = control["positions"]
    return min(range(len(positions)), key=lambda i: abs(positions[i]["value"] - raw))


def move_lever(control: dict, value, target: dict, seat: int) -> tuple[bool, str]:
    readback = expand(control["readback"], seat)
    with lock:
        raw = read(readback)
    if raw is None:
        return False, "no readback"
    current = lever_index(control, raw)
    goal = control["positions"].index(target)
    if current == goal:
        log.line("dash", control["id"], f"{value}: already there")
        return True, ""
    if current == 3:
        return False, "position not available"
    direction = 1 if goal > current else -1
    steps = [(i, i + direction) for i in range(current, goal, direction)]
    names = [LEVER_KEYS[step] for step in steps]
    with command_lock:
        for (a, b), name in zip(steps, names):
            if not keys.focus(cfg["dcs"]["window_title"]):
                return False, "DCS not in front"
            keys.press(cfg["keys"][f"power_{control['side']}_{name}"], 0.1)
            deadline = time.monotonic() + LEVER_WAIT
            while True:
                with lock:
                    raw = read(readback)
                if raw is not None and lever_index(control, raw) == b:
                    break
                if time.monotonic() >= deadline:
                    return False, f"no readback after {name}"
                time.sleep(0.05)
    log.line("dash", control["id"], f"{value}: keys {', '.join(names)}")
    return True, ""


def wait_readback(name: str, done) -> tuple[object, bool]:
    deadline = time.monotonic() + STEP_WAIT
    while True:
        with lock:
            current = read(name)
        if done(current):
            return current, True
        if time.monotonic() >= deadline:
            return current, False
        time.sleep(0.05)


def reach_by_steps(name: str, value: int) -> tuple[bool, bool]:
    current, reached = wait_readback(name, lambda c: c == value)
    if reached:
        return True, False
    for _ in range(STEP_TRIES):
        if current is None:
            return False, False
        before = current
        send(name, "INC" if value > before else "DEC")
        current, _ = wait_readback(name, lambda c: c is not None and c != before)
        if current == value:
            return True, True
    return False, False


def command(body: dict) -> tuple[bool, str]:
    identifier = body.get("id")
    value = body.get("value", "")
    ok, message = check_and_send(identifier, value, body)
    if not ok:
        log.line("dash", identifier, f"{value} refused: {message}")
    return ok, message


def check_and_send(identifier, value, body: dict) -> tuple[bool, str]:
    control, view = find_control(identifier)
    if control is None:
        return False, "unknown control"
    with lock:
        seat = read(SEAT)
    if seat is None:
        return False, "no DCS data"
    if seat not in view["seats"]:
        return False, "CP/G seat: read only" if seat == 1 else "pilot seat: read only"
    if "seats" in control and seat not in control["seats"]:
        return False, "CP/G seat: read only" if seat == 1 else "pilot seat: read only"
    name = expand(identifier, seat)
    if control["type"] in ("display", "controls"):
        return False, "display only"
    if control["type"] == "lever":
        target = next((p for p in control["positions"] if p["label"] == value), None)
        if target is None or target.get("disabled"):
            return False, "position not available"
        return move_lever(control, value, target, seat)
    if control["type"] == "button":
        requires = control.get("requires")
        if requires:
            with lock:
                current = read(expand(requires["id"], seat))
            if current != requires["value"]:
                return False, "locked: open the cover first"
        with command_lock:
            send(name, 1)
            time.sleep(control.get("hold", 0.3))
            send(name, 0)
        log.line("dash", name, "pressed")
        return True, ""
    if control["type"] == "knob":
        if value not in ("up", "down"):
            return False, "position not available"
        with command_lock:
            send(name, f"+{control['step']}" if value == "up" else f"-{control['step']}")
        log.line("dash", name, f"{value} sent")
        return True, ""
    if control["type"] == "key":
        with command_lock:
            if not keys.focus(cfg["dcs"]["window_title"]):
                return False, "DCS not in front"
            keys.press(cfg["keys"][control["key"]], 0.1)
        log.line("dash", name, "pressed")
        return True, ""
    if control["type"] == "hat":
        axes = {"up": ("ud", 2), "down": ("ud", 0), "left": ("lr", 0), "right": ("lr", 2)}
        if not isinstance(value, str) or value not in control["positions"]:
            return False, "position not available"
        axis, level = axes[value]
        target = expand(control[axis], seat)
        with command_lock:
            send(target, level)
            time.sleep(control.get("hold", 0.3))
            send(target, 1)
        log.line("dash", name, f"{value} ({control['positions'][value]}) sent")
        return True, ""
    position = next((p for p in control["positions"] if p["value"] == value and not isinstance(value, bool)), None)
    if position is None or position.get("disabled"):
        return False, "position not available"
    how = "sent"
    with command_lock:
        send(name, value)
        if position.get("momentary"):
            time.sleep(control["hold"])
            send(name, control["rest"])
        if control.get("step_fallback"):
            reached, by_steps = reach_by_steps(name, value)
            if not reached:
                return False, "position not reached"
            if by_steps:
                how = "sent by steps"
    log.line("dash", name, f"{value} {how}")
    return True, ""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def reply(self, status: int, content_type: str, body: bytes, no_store: bool = False) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        if no_store:
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def reply_json(self, status: int, data: dict) -> None:
        self.reply(status, "application/json", json.dumps(data).encode("utf-8"), no_store=True)

    def do_GET(self) -> None:
        if self.path == "/":
            if not INDEX.exists():
                self.reply(404, "text/plain; charset=utf-8", b"web/index.html is missing")
            else:
                self.reply(200, "text/html; charset=utf-8", INDEX.read_bytes())
        elif self.path == "/apple-touch-icon.png":
            if not ICON.exists():
                self.reply(404, "text/plain; charset=utf-8", b"web/apple-touch-icon.png is missing")
            else:
                self.reply(200, "image/png", ICON.read_bytes())
        elif self.path == "/layout":
            self.reply_json(200, {"views": VIEWS})
        elif self.path == "/state":
            self.reply_json(200, snapshot())
        elif self.path == "/settings":
            self.reply_json(200, settings_reply())
        else:
            self.reply(404, "text/plain; charset=utf-8", b"not found")

    def do_POST(self) -> None:
        if self.path not in ("/command", "/settings"):
            self.reply(404, "text/plain; charset=utf-8", b"not found")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))
        except ValueError:
            body = None
        if not isinstance(body, dict):
            self.reply_json(400, {"error": "bad request"})
            return
        if self.path == "/settings":
            if change_settings(body):
                self.reply_json(200, settings_reply())
            else:
                self.reply_json(400, {"error": "bad request"})
            return
        ok, message = command(body)
        if ok:
            self.reply_json(200, {"ok": True})
        else:
            self.reply_json(409, {"error": message})


def lan_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("10.255.255.255", 1))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def main() -> None:
    global cfg, settings, outputs, cmd_sock
    cfg = config.load()
    log.setup(cfg["log"])
    settings = load_settings()
    log.set_file_logging(settings["logging"])
    key_map = cfg.get("keys", {})
    try:
        for side in ("left", "right"):
            for step in LEVER_KEYS.values():
                keys.parse(key_map[f"power_{side}_{step}"])
        cfg["dcs"]["window_title"]
    except (KeyError, ValueError):
        raise SystemExit("config.toml needs [dcs] window_title and the power_* keys, see config.example.toml.")
    for view in VIEWS:
        for control in view["controls"]:
            if control["type"] == "key":
                try:
                    keys.parse(key_map[control["key"]])
                except (KeyError, ValueError):
                    raise SystemExit(f"config.toml needs [keys] {control['key']}, see config.example.toml.")
    names = read_names()
    outputs, missing = dcsbios.load_outputs(dcsbios.json_path(cfg["dcs"]["saved_games"]), names)
    if missing:
        raise SystemExit("Not in DCS-BIOS: " + ", ".join(missing))
    group, export_port = cfg["dcs_bios"]["export_multicast"], cfg["dcs_bios"]["export_port"]
    command_port = cfg["dcs_bios"]["command_port"]
    host, port = cfg["dashboard"]["host"], cfg["dashboard"]["port"]
    bios_sock = dcsbios.open_socket(group, export_port)
    cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        export_sock = export.open_socket(cfg["export"]["port"])
    except OSError:
        export_sock = None
        log.line("bridge", "export port busy", "no control positions")
    server = ThreadingHTTPServer((host, port), Handler)
    threading.Thread(target=reader, args=(bios_sock,), daemon=True).start()
    if export_sock:
        threading.Thread(target=export_reader, args=(export_sock,), daemon=True).start()
    log.line("bridge", "start", f"dashboard on port {port}, DCS-BIOS {group}:{export_port}, commands to port {command_port}")
    print(f"Open http://{lan_ip()}:{port} on the tablet")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.line("bridge", "stop", "Ctrl+C")
    finally:
        server.server_close()
        bios_sock.close()
        if export_sock:
            export_sock.close()
        cmd_sock.close()


if __name__ == "__main__":
    main()
