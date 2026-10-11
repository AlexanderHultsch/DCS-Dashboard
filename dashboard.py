import importlib
import json
import math
import re
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from bridge import config, dcsbios, export, keys, log

LEVER_KEYS = {(0, 1): "idle", (1, 2): "up", (2, 1): "down", (1, 0): "off"}
LEVER_WAIT = 1.0
STEP_WAIT = 0.5
STEP_TRIES = 2
PRESS_MIN = 0.3
PRESS_MAX = 1.0
CONFIRM_WAIT = 0.5
CONFIRM_POLL = 0.02
GUARD_WINDOW = 5.0
COVER_CLOSE_DELAY = 1.0
COVER_POLL = 0.05

MPD_SEPARATOR = "-" * 41
MPD_BUTTON = re.compile(r"^PB(\d+)_(?:bold_)?(\d+)$")
MPD_SKIP_LINES = ("children are {", "}")

STICK_CENTRE = 0.02

CONTROLS_STALE = 3
TRIM_POLL = 0.05

SEAT = "SEAT_POSITION"
INDEX = Path(__file__).resolve().parent / "web" / "index.html"
ICON = Path(__file__).resolve().parent / "web" / "apple-touch-icon.png"
SETTINGS_FILE = Path(__file__).resolve().parent / "settings.json"

ac = None
cfg = {}
settings = {}
outputs = {}
state = dcsbios.new_state()
lock = threading.Lock()
command_lock = threading.Lock()
last_packet = None
control_values = {}
control_packet = None
mpd_labels = {}
mpd_times = {}
stick_lock = threading.Lock()
stick_last = {}
trim = {}
trim_switch = {}
guard_open = {}
real_cover = {}
cmd_sock = None


def expand(name: str, seat: int) -> str:
    return name.replace("{seat}", ac.SEAT_NAMES[seat])


def expand_all(name: str) -> list[str]:
    if "{seat}" in name:
        return [expand(name, seat) for seat in ac.SEAT_NAMES]
    return [name]


def read_names() -> list[str]:
    names = [SEAT]
    for view in ac.VIEWS:
        for lamp in view["lamps"]:
            names += expand_all(lamp["id"])
            if "button" in lamp:
                names += expand_all(lamp["button"])
        for lamp in view.get("indicators", []):
            names += expand_all(lamp["bright"]) + expand_all(lamp["dim"])
        for control in view["controls"]:
            if control["type"] == "lever":
                names += expand_all(control["readback"])
            elif control["type"] == "key":
                if "readback" in control:
                    names += expand_all(control["readback"])
            elif control["type"] == "hat":
                if "ud" in control:
                    names += expand_all(control["ud"])
                if "lr" in control:
                    names += expand_all(control["lr"])
            elif control["type"] == "controls":
                if "trim_switch" in control:
                    names += expand_all(control["trim_switch"])
            elif control["type"] == "stick":
                names += expand_all(control["x"]) + expand_all(control["y"])
            elif control["type"] == "display" and "ids" in control:
                for identifier in control["ids"]:
                    names += expand_all(identifier)
            else:
                names += expand_all(control["id"])
            if "lamp" in control:
                names += expand_all(control["lamp"])
            for lamp in control.get("lamps", []):
                names += expand_all(lamp["id"])
            if "cover" in control:
                names += expand_all(control["cover"])
            if "requires" in control:
                names += expand_all(control["requires"]["id"])
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
            track_trim()


def track_trim() -> None:
    now = time.monotonic()
    fresh = control_packet is not None and now - control_packet <= CONTROLS_STALE
    for prefix in ac.SEAT_NAMES.values():
        current = read(f"{prefix}_CYCLIC_TRIM_UD")
        if current is None:
            continue
        before = trim_switch.get(prefix)
        trim_switch[prefix] = current
        if before != ac.TRIM_RELEASED or current == ac.TRIM_RELEASED:
            continue
        axes = [control_values.get(f"{prefix.lower()}_{axis}") for axis in ("cyc_pitch", "cyc_roll", "pedals")]
        if not fresh or None in axes:
            log.line("dash", "trim", f"{prefix} set, no control data")
            continue
        trim[prefix] = {"pitch": axes[0], "roll": axes[1], "pedals": axes[2], "reset": False, "time": now}
        log.line("dash", "trim", f"{prefix} set P {axes[0]:+.2f} R {axes[1]:+.2f} Y {axes[2]:+.2f}")


def trim_reset_watcher() -> None:
    combo = cfg["keys"]["trim_reset"]
    title = cfg["dcs"]["window_title"]
    was_pressed = False
    while True:
        time.sleep(TRIM_POLL)
        pressed = keys.is_pressed(combo) and title in keys.foreground_title()
        if pressed and not was_pressed:
            with lock:
                seat = read(SEAT)
                if seat in ac.SEAT_NAMES:
                    prefix = ac.SEAT_NAMES[seat]
                    trim[prefix] = {"pitch": 0.0, "roll": 0.0, "pedals": 0.0, "reset": True, "time": time.monotonic()}
                    log.line("dash", "trim", f"{prefix} reset")
        was_pressed = pressed


def parse_mpd_labels(text: str) -> dict[str, str]:
    blocks = [[]]
    for line in text.replace("\\n", "\n").split("\n"):
        line = line.strip()
        if line == MPD_SEPARATOR:
            blocks.append([])
        elif line:
            blocks[-1].append(line)
    found = {}
    for lines in blocks:
        if not lines:
            continue
        match = MPD_BUTTON.match(lines[0])
        body = [line for line in lines[1:] if line not in MPD_SKIP_LINES]
        if not match or not body:
            continue
        found.setdefault(match.group(1), []).append((int(match.group(2)), "\n".join(body)))
    labels = {}
    for button, parts in found.items():
        texts = []
        for _, part in sorted(parts, key=lambda p: p[0]):
            if part not in texts:
                texts.append(part)
        labels[button] = "\n".join(texts)
    return labels


def export_reader(sock: socket.socket) -> None:
    global control_packet
    while True:
        data = sock.recv(65536)
        try:
            values = export.parse(data)
        except ValueError:
            continue
        with lock:
            now = time.monotonic()
            for name in ac.CONTROL_NAMES:
                try:
                    number = float(values[name])
                except (KeyError, ValueError):
                    continue
                if math.isfinite(number):
                    control_values[name] = number
            for number in ac.MPD_INDICATIONS:
                text = values.get(f"ind{number}")
                if text is not None:
                    mpd_labels[number] = parse_mpd_labels(text)
                    mpd_times[number] = now
            control_packet = now


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
        seat = read(SEAT)
        left, right = ac.MPD_SEATS.get(seat, (None, None))
        received = [mpd_times[n] for n in (left, right) if n in mpd_times]
        return {
            "seat": seat,
            "age": age,
            "values": {name: read(name) for name in outputs if name != SEAT},
            "controls": dict(control_values),
            "controls_age": controls_age,
            "mpd_labels": {
                "L": dict(mpd_labels.get(left, {})),
                "R": dict(mpd_labels.get(right, {})),
                "age": round(now - max(received), 1) if received else None,
            },
            "trim": {
                prefix.lower(): {
                    "pitch": point["pitch"], "roll": point["roll"], "pedals": point["pedals"],
                    "reset": point["reset"], "age": round(now - point["time"], 1),
                }
                for prefix, point in trim.items()
            },
        }


def find_control(identifier, seat=None):
    fallback = None
    for view in ac.VIEWS:
        for control in view["controls"]:
            if control["id"] == identifier:
                if seat is None or (seat in view["seats"] and ("seats" not in control or seat in control["seats"])):
                    return control, view
                if fallback is None:
                    fallback = (control, view)
        for lamp in view["lamps"]:
            if lamp.get("button") == identifier:
                if seat is None or seat in view["seats"]:
                    return {"id": identifier, "type": "button", "hold": 0.3}, view
                if fallback is None:
                    fallback = ({"id": identifier, "type": "button", "hold": 0.3}, view)
    return fallback or (None, None)


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


def is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def move_stick(control: dict, name: str, value, seat: int) -> tuple[bool, str]:
    if not isinstance(value, dict) or not is_number(value.get("x")) or not is_number(value.get("y")):
        return False, "position not available"
    position = (max(-1.0, min(1.0, value["x"])), max(-1.0, min(1.0, value["y"])))
    with stick_lock:
        last = stick_last.setdefault(name, {"position": (0.0, 0.0), "raw": {}})
        for axis, v in zip(("x", "y"), position):
            raw = round(32767.5 + v * 32767.5)
            axis_name = expand(control[axis], seat)
            if last["raw"].get(axis_name) != raw:
                send(axis_name, raw)
                last["raw"][axis_name] = raw
        was_centre = all(abs(v) < STICK_CENTRE for v in last["position"])
        is_centre = all(abs(v) < STICK_CENTRE for v in position)
        last["position"] = position
    if was_centre and not is_centre:
        log.line("dash", name, "moving")
    elif is_centre and not was_centre:
        log.line("dash", name, "centre")
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


def hold_until(name: str, level, hold: float, limit: float) -> bool:
    start = time.monotonic()
    seen = False
    while True:
        with lock:
            seen = seen or read(name) == level
        elapsed = time.monotonic() - start
        if seen and elapsed >= hold or elapsed >= limit:
            return seen
        time.sleep(CONFIRM_POLL)


def open_real_cover(name: str) -> bool:
    with command_lock:
        send(name, 1)
        opened = hold_until(name, 1, 0, CONFIRM_WAIT)
        if not opened:
            send(name, 0)
    if opened:
        with lock:
            real_cover[name] = time.monotonic() + GUARD_WINDOW
        log.line("dash", name, "cover open")
    return opened


def close_real_cover(due_only: bool = False) -> None:
    now = time.monotonic()
    with lock:
        names = [name for name, close_at in real_cover.items() if not due_only or now >= close_at]
        for name in names:
            del real_cover[name]
    for name in names:
        with command_lock:
            send(name, 0)
        log.line("dash", name, "cover closed")


def cover_watcher() -> None:
    while True:
        time.sleep(COVER_POLL)
        close_real_cover(True)


def command(body: dict) -> tuple[bool, str, bool | None]:
    identifier = body.get("id")
    value = body.get("value", "")
    ok, message, confirmed = check_and_send(identifier, value, body)
    if not ok:
        log.line("dash", identifier, f"{value} refused: {message}")
    return ok, message, confirmed


def check_and_send(identifier, value, body: dict) -> tuple[bool, str, bool | None]:
    with lock:
        seat = read(SEAT)
    control, view = find_control(identifier, seat)
    if control is None:
        return False, "unknown control", None
    if seat is None:
        return False, "no DCS data", None
    if seat not in view["seats"]:
        return False, "CP/G seat: read only" if seat == 1 else "pilot seat: read only", None
    if "seats" in control and seat not in control["seats"]:
        return False, "CP/G seat: read only" if seat == 1 else "pilot seat: read only", None
    if body.get("guard") == "open":
        if not control.get("guard"):
            return False, "not guarded", None
        with lock:
            guard_open.clear()
        close_real_cover()
        if "cover" in control and not open_real_cover(expand(control["cover"], seat)):
            return False, "cover did not open", None
        with lock:
            guard_open[identifier] = time.monotonic()
        log.line("dash", expand(identifier, seat), "guard open")
        return True, "", None
    if control.get("guard"):
        with lock:
            opened = guard_open.pop(identifier, None)
        if opened is None or time.monotonic() - opened > GUARD_WINDOW:
            return False, "guard closed", None
        with lock:
            for cover in real_cover:
                real_cover[cover] = time.monotonic() + COVER_CLOSE_DELAY
    name = expand(identifier, seat)
    if control["type"] in ("display", "controls"):
        return False, "display only", None
    if control["type"] == "lever":
        target = next((p for p in control["positions"] if p["label"] == value), None)
        if target is None or target.get("disabled"):
            return False, "position not available", None
        ok, message = move_lever(control, value, target, seat)
        return ok, message, True if ok else None
    if control["type"] == "button":
        requires = control.get("requires")
        if requires:
            with lock:
                current = read(expand(requires["id"], seat))
            if current != requires["value"]:
                return False, "locked: open the cover first", None
        with command_lock:
            send(name, 1)
            confirmed = hold_until(name, 1, max(control.get("hold", 0.3), PRESS_MIN), PRESS_MAX)
            send(name, 0)
        log.line("dash", name, "pressed" if confirmed else "pressed, not confirmed")
        return True, "", confirmed
    if control["type"] == "knob":
        if is_number(value) and 0 <= value <= 65535:
            level = round(value)
            with command_lock:
                send(name, level)
            log.line("dash", name, f"set {level}")
            return True, "", None
        if value not in ("up", "down"):
            return False, "position not available", None
        with command_lock:
            send(name, f"+{control['step']}" if value == "up" else f"-{control['step']}")
        log.line("dash", name, f"{value} sent")
        return True, "", None
    if control["type"] == "stick":
        ok, message = move_stick(control, name, value, seat)
        return ok, message, None
    if control["type"] == "key":
        with command_lock:
            if not keys.focus(cfg["dcs"]["window_title"]):
                return False, "DCS not in front", None
            keys.press(cfg["keys"][control["key"]], 0.1)
        log.line("dash", name, "pressed")
        return True, "", None
    if control["type"] == "hat":
        axes = {"up": ("ud", 2), "down": ("ud", 0), "left": ("lr", 0), "right": ("lr", 2)}
        if not isinstance(value, str) or value not in control["positions"]:
            return False, "position not available", None
        axis, level = axes[value]
        target = expand(control[axis], seat)
        with command_lock:
            send(target, level)
            confirmed = hold_until(target, level, max(control.get("hold", 0.3), PRESS_MIN), PRESS_MAX)
            send(target, 1)
        log.line("dash", name, f"{value} ({control['positions'][value]}) sent" + ("" if confirmed else ", not confirmed"))
        return True, "", confirmed
    position = next((p for p in control["positions"] if p["value"] == value and not isinstance(value, bool)), None)
    if position is None or position.get("disabled"):
        return False, "position not available", None
    how = "sent"
    confirmed = None
    with command_lock:
        send(name, value)
        if position.get("momentary"):
            confirmed = hold_until(name, value, control["hold"], max(control["hold"], CONFIRM_WAIT))
            send(name, control["rest"])
        elif not control.get("step_fallback"):
            confirmed = hold_until(name, value, 0, CONFIRM_WAIT)
        if control.get("step_fallback"):
            reached, by_steps = reach_by_steps(name, value)
            if not reached:
                return False, "position not reached", None
            confirmed = True
            if by_steps:
                how = "sent by steps"
    if confirmed is False:
        how += ", not confirmed"
    log.line("dash", name, f"{value} {how}")
    return True, "", confirmed


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
            self.reply_json(200, {"views": ac.VIEWS})
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
        ok, message, confirmed = command(body)
        if ok:
            self.reply_json(200, {"ok": True, "confirmed": confirmed})
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


def load_aircraft(value: str):
    name = re.sub(r"[^a-z0-9]", "", str(value).lower())
    try:
        return importlib.import_module("aircraft." + name)
    except ImportError:
        raise SystemExit(f"Unknown aircraft: {value}")


def main() -> None:
    global ac, cfg, settings, outputs, cmd_sock
    cfg = config.load()
    ac = load_aircraft(cfg["dcs"].get("aircraft", "AH-64D"))
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
    try:
        keys.parse(key_map["trim_reset"])
    except (KeyError, ValueError):
        raise SystemExit("config.toml needs [keys] trim_reset, see config.example.toml.")
    for view in ac.VIEWS:
        for control in view["controls"]:
            if control["type"] == "key":
                try:
                    keys.parse(key_map[control["key"]])
                except (KeyError, ValueError):
                    raise SystemExit(f"config.toml needs [keys] {control['key']}, see config.example.toml.")
    names = read_names()
    outputs, missing = dcsbios.load_outputs(dcsbios.json_path(cfg["dcs"]["saved_games"], ac.DCSBIOS_MODULE), names)
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
    threading.Thread(target=trim_reset_watcher, daemon=True).start()
    threading.Thread(target=cover_watcher, daemon=True).start()
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
