import json
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from bridge import config, dcsbios, keys, log

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

VIEWS = [
    {
        "name": "Startup",
        "lamps": [
            {"id": "PLT_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red"},
            {"id": "PLT_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber"},
            {"id": "PLT_ENG_1_FIRE_L", "label": "ENG 1 FIRE", "color": "red"},
            {"id": "PLT_APU_FIRE_L", "label": "APU FIRE", "color": "red"},
            {"id": "PLT_ENG_2_FIRE_L", "label": "ENG 2 FIRE", "color": "red"},
            {"id": "PLT_APU_L", "label": "APU ON", "color": "green"},
        ],
        "controls": [
            {"id": "PLT_MASTER_IGN_SW", "label": "MSTR IGN", "type": "selector", "positions": [{"value": 0, "label": "OFF"}, {"value": 1, "label": "BATT"}, {"value": 2, "label": "EXT PWR", "disabled": True}]},
            {"id": "PLT_APU_BTN_CVR", "label": "APU COVER", "type": "selector", "positions": [{"value": 0, "label": "CLOSED"}, {"value": 1, "label": "OPEN"}]},
            {"id": "PLT_APU_BTN", "label": "APU", "type": "button", "hold": 0.3, "requires": {"id": "PLT_APU_BTN_CVR", "value": 1}},
            {"id": "PLT_ENG1_START", "label": "ENG 1 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS},
            {"id": "PLT_ENG2_START", "label": "ENG 2 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS},
            {"id": "power_left", "label": "PWR LVR 1", "type": "lever", "readback": "PLT_ENG_L_PW_LVR", "side": "left", "positions": POWER_POSITIONS},
            {"id": "power_right", "label": "PWR LVR 2", "type": "lever", "readback": "PLT_ENG_R_PW_LVR", "side": "right", "positions": POWER_POSITIONS},
            {"id": "PLT_ROTOR_BRK", "label": "RTR BRK", "type": "selector", "positions": [{"value": 2, "label": "OFF"}, {"value": 1, "label": "BRK", "disabled": True}, {"value": 0, "label": "LOCK"}]},
            {"id": "PLT_PARK_BRAKE", "label": "PARK BRAKE", "type": "selector", "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "PULLED"}]},
        ],
    }
]

LEVER_KEYS = {(0, 1): "idle", (1, 2): "up", (2, 1): "down", (1, 0): "off"}
LEVER_WAIT = 1.0

SEAT = "SEAT_POSITION"
INDEX = Path(__file__).resolve().parent / "web" / "index.html"

cfg = {}
outputs = {}
state = dcsbios.new_state()
lock = threading.Lock()
command_lock = threading.Lock()
last_packet = None
cmd_sock = None


def read_names() -> list[str]:
    names = [SEAT]
    for view in VIEWS:
        names += [lamp["id"] for lamp in view["lamps"]]
        for control in view["controls"]:
            names.append(control["readback"] if control["type"] == "lever" else control["id"])
    return names


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


def read(name: str):
    return dcsbios.read_value(state, outputs[name])


def snapshot() -> dict:
    with lock:
        age = None if last_packet is None else round(time.monotonic() - last_packet, 1)
        return {
            "seat": read(SEAT),
            "age": age,
            "values": {name: read(name) for name in outputs if name != SEAT},
        }


def find_control(identifier):
    for view in VIEWS:
        for control in view["controls"]:
            if control["id"] == identifier:
                return control
    return None


def send(identifier: str, value) -> None:
    dcsbios.send(cmd_sock, cfg["dcs_bios"]["command_port"], identifier, value)


def lever_index(control: dict, raw: int) -> int:
    positions = control["positions"]
    return min(range(len(positions)), key=lambda i: abs(positions[i]["value"] - raw))


def move_lever(control: dict, value, target: dict) -> tuple[bool, str]:
    with lock:
        raw = read(control["readback"])
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
                    raw = read(control["readback"])
                if raw is not None and lever_index(control, raw) == b:
                    break
                if time.monotonic() >= deadline:
                    return False, f"no readback after {name}"
                time.sleep(0.05)
    log.line("dash", control["id"], f"{value}: keys {', '.join(names)}")
    return True, ""


def command(body: dict) -> tuple[bool, str]:
    identifier = body.get("id")
    value = body.get("value", "")
    ok, message = check_and_send(identifier, value, body)
    if not ok:
        log.line("dash", identifier, f"{value} refused: {message}")
    return ok, message


def check_and_send(identifier, value, body: dict) -> tuple[bool, str]:
    control = find_control(identifier)
    if control is None:
        return False, "unknown control"
    with lock:
        seat = read(SEAT)
    if seat is None:
        return False, "no DCS data"
    if seat != 0:
        return False, "CP/G seat: read only"
    if control["type"] == "lever":
        target = next((p for p in control["positions"] if p["label"] == value), None)
        if target is None or target.get("disabled"):
            return False, "position not available"
        return move_lever(control, value, target)
    if control["type"] == "button":
        requires = control["requires"]
        with lock:
            current = read(requires["id"])
        if current != requires["value"]:
            return False, "locked: open the cover first"
        with command_lock:
            send(identifier, 1)
            time.sleep(control["hold"])
            send(identifier, 0)
        log.line("dash", identifier, "pressed")
        return True, ""
    position = next((p for p in control["positions"] if p["value"] == value and not isinstance(value, bool)), None)
    if position is None or position.get("disabled"):
        return False, "position not available"
    with command_lock:
        send(identifier, value)
        if position.get("momentary"):
            time.sleep(control["hold"])
            send(identifier, control["rest"])
    log.line("dash", identifier, f"{value} sent")
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
        elif self.path == "/layout":
            self.reply_json(200, {"views": VIEWS})
        elif self.path == "/state":
            self.reply_json(200, snapshot())
        else:
            self.reply(404, "text/plain; charset=utf-8", b"not found")

    def do_POST(self) -> None:
        if self.path != "/command":
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
    global cfg, outputs, cmd_sock
    cfg = config.load()
    log.setup(cfg["log"])
    key_map = cfg.get("keys", {})
    try:
        for side in ("left", "right"):
            for step in LEVER_KEYS.values():
                keys.parse(key_map[f"power_{side}_{step}"])
        cfg["dcs"]["window_title"]
    except (KeyError, ValueError):
        raise SystemExit("config.toml needs [dcs] window_title and the power_* keys, see config.example.toml.")
    names = read_names()
    outputs, missing = dcsbios.load_outputs(dcsbios.json_path(cfg["dcs"]["saved_games"]), names)
    if missing:
        raise SystemExit("Not in DCS-BIOS: " + ", ".join(missing))
    group, export_port = cfg["dcs_bios"]["export_multicast"], cfg["dcs_bios"]["export_port"]
    command_port = cfg["dcs_bios"]["command_port"]
    host, port = cfg["dashboard"]["host"], cfg["dashboard"]["port"]
    bios_sock = dcsbios.open_socket(group, export_port)
    cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ThreadingHTTPServer((host, port), Handler)
    threading.Thread(target=reader, args=(bios_sock,), daemon=True).start()
    log.line("bridge", "start", f"dashboard on port {port}, DCS-BIOS {group}:{export_port}, commands to port {command_port}")
    print(f"Open http://{lan_ip()}:{port} on the tablet")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.line("bridge", "stop", "Ctrl+C")
    finally:
        server.server_close()
        bios_sock.close()
        cmd_sock.close()


if __name__ == "__main__":
    main()
