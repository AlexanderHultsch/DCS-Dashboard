#!/usr/bin/env python3
"""Command smoke test of the panel pages against the running test bridge (python3 bridge.py).

  python3 smoke.py [--acft NAME] [--seat 0|1] PAGE ...      e.g. python3 smoke.py IFF "EMER FLT CTRL"   (NAME: the _ACFT_NAME to send, default A-10C_2)
  AH-64D: python3 smoke.py --acft AH-64D_BLK_II --seat 1 MPD KU George ...   (--seat is sent as SEAT_POSITION every second; {seat} ids are expanded
  with PLT / CPG; a page name with two seats (FIGHT, COCKPIT, ...) is taken for the given seat; the master lamp buttons of the lamp row are tested too;
  controls of the other seat (own "seats", or a page of the other seat) are SKIPped; key, macro and key hat controls and the power levers are checked in
  logs/test/keys.log (the fake keys module of bridge.py) instead of UDP: the combo of the control's key(s) must be pressed in order; a lever is moved by one step and the
  readback is set by this script after the key arrived; a stick gets a deflection and the centre; display and controls are SKIPped)

Posts one valid command per control of each page to <DASHBOARD_URL>/command (default http://127.0.0.1:8080) and checks that a DCS-BIOS command
line starting with the control's DCS-BIOS id ("bios", else "id"; for a hat the axis id) arrives on UDP 127.0.0.1:7778.
  button    {"id"}
  selector  the first position that is not disabled
  knob      value 32768
  hat       the first direction; with "steps" the sent line must be `<id> INC` (steps "fixed") or `<id> +N` (steps N)
  guarded   first {"id", "guard": "open"} (a real cover id is set to 1 with sim.py so the bridge sees it open), then the command
  others    SKIP (display, bar)
A "not confirmed" reply is fine (the simulator does not move switches). _ACFT_NAME=A-10C_2 is re-sent every second.
Prints PASS / FAIL / SKIP per control; exit code 1 if any control fails.
"""
import ast
import importlib
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BRIDGE = os.environ.get("DASHBOARD_URL", "http://127.0.0.1:8080")
PORT = 7778
SETTLE = 0.2
ACFT = "A-10C_2"
SEAT = None
KEYS_LOG = REPO / "logs" / "test" / "keys.log"
PREFIX = {0: "PLT", 1: "CPG"}


SIM_LOCK = threading.Lock()


def sim(*args: str) -> None:
    with SIM_LOCK:
        subprocess.run([sys.executable, str(HERE / "sim.py"), *args], check=True, capture_output=True)


def keep_fresh(stop: threading.Event) -> None:
    while not stop.is_set():
        sim(f"_ACFT_NAME={ACFT}", *([] if SEAT is None else [f"SEAT_POSITION={SEAT}"]))
        stop.wait(1.0)


def post(body: dict) -> tuple[int, dict]:
    request = urllib.request.Request(BRIDGE + "/command", json.dumps(body).encode(), {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=15) as reply:
            return reply.status, json.loads(reply.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def drain(sock: socket.socket) -> list[str]:
    lines = []
    while True:
        try:
            lines += sock.recv(4096).decode().splitlines()
        except BlockingIOError:
            return lines


def expand(text: str) -> str:
    return text if SEAT is None else text.replace("{seat}", PREFIX[SEAT])


def key_map() -> dict:
    sys.path.insert(0, str(REPO / "aircraft"))
    sys.path.insert(0, str(REPO / "core"))
    module = __import__("ah64d" if ACFT.startswith("AH-64D") else "a10c")
    return module.KEYS


def key_calls() -> list[tuple]:
    if not KEYS_LOG.exists():
        return []
    calls = []
    for line in KEYS_LOG.read_text(encoding="utf-8").splitlines():
        name, _, rest = line.partition(" ")
        calls.append((name, ast.literal_eval(rest)))
    return calls


def key_presses_since(count: int) -> list[str]:
    return [args[0] for name, args in key_calls()[count:] if name == "press"]


def own_seat(control: dict, view: dict) -> bool:
    return SEAT is None or (SEAT in view.get("seats", [SEAT]) and SEAT in control.get("seats", [SEAT]))


def command_for(control: dict) -> tuple[dict, str] | None:
    kind = control["type"]
    bios = expand(control.get("bios", control["id"]))
    if kind == "button":
        return {"id": control["id"]}, bios
    if kind == "selector":
        position = next(p for p in control["positions"] if not p.get("disabled"))
        return {"id": control["id"], "value": position["value"]}, expand(control["id"])
    if kind == "knob":
        return {"id": control["id"], "value": 32768}, expand(control["id"])
    if kind == "hat":
        direction = next(iter(control["positions"]))
        return {"id": control["id"], "value": direction}, expand(control["ud" if direction in ("up", "down") else "lr"])
    return None


def do_post(body: dict, settle: float = SETTLE) -> tuple[int, dict]:
    status, reply = post(body)
    time.sleep(settle)
    return status, reply


def check_keys_control(control: dict, body: dict, expected: list[str]) -> tuple[str, str]:
    before = len(key_calls())
    status, reply = do_post(body, 0.1)
    got = key_presses_since(before)
    if status != 200:
        return "FAIL", f"refused {status}: {reply.get('error')}"
    if got != expected:
        return "FAIL", f"expected keys {expected}, got {got}"
    return "PASS", f"{json.dumps(body)} -> keys.log {got}"


def check_lever(control: dict) -> tuple[str, str]:
    keys = key_map()
    readback = expand(control["readback"])
    target = control["positions"][1]
    expected = [keys[f"power_{control['side']}_idle"]]
    sim(f"{readback}=0")
    time.sleep(0.2)
    before = len(key_calls())
    result = {}
    worker = threading.Thread(target=lambda: result.update(zip(("status", "reply"), post({"id": control["id"], "value": target["label"]}))))
    worker.start()
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline and not key_presses_since(before):
        time.sleep(0.02)
    sim(f"{readback}={target['value']}")
    worker.join()
    got = key_presses_since(before)
    if result.get("status") != 200:
        return "FAIL", f"refused {result.get('status')}: {result.get('reply')}"
    if got != expected:
        return "FAIL", f"expected keys {expected}, got {got}"
    return "PASS", f"{target['label']} from OFF -> keys.log {got}"


def check_stick(sock: socket.socket, control: dict) -> tuple[str, str]:
    x, y = expand(control["x"]), expand(control["y"])
    digital = control.get("digital")
    high, low, centre = ("2", "0", "1") if digital else ("65535", "0", "32768")
    drain(sock)
    status, reply = do_post({"id": control["id"], "value": {"x": 1, "y": -1}})
    sent = drain(sock)
    if status != 200:
        return "FAIL", f"refused {status}: {reply.get('error')}"
    expect_move = [f"{x} {high}", f"{y} {low}"]
    if not all(line in sent for line in expect_move):
        return "FAIL", f"deflection: expected {expect_move}, got {sent}"
    drain(sock)
    status, reply = do_post({"id": control["id"], "value": {"x": 0, "y": 0}})
    sent = drain(sock)
    expect_centre = [f"{x} {centre}", f"{y} {centre}"]
    if status != 200 or not all(line in sent for line in expect_centre):
        return "FAIL", f"centre: expected {expect_centre}, got {sent} ({status})"
    return "PASS", f"{expect_move} then {expect_centre}"


def check(sock: socket.socket, control: dict, view: dict | None = None) -> list[tuple[str, str, str]]:
    """Returns [(result, control label, text)], more than one entry for a hat with two axes."""
    cid = control["id"]
    kind = control["type"]
    if view is not None and not own_seat(control, view):
        return [("SKIP", cid, f"other seat (seats {control.get('seats', view.get('seats'))})")]
    if kind in ("display", "controls", "bar"):
        return [("SKIP", cid, f"type {kind} (display only, the bridge refuses it)")]
    if kind == "lever":
        return [("PASS" if (r := check_lever(control))[0] == "PASS" else "FAIL", cid, r[1])]
    if kind == "stick":
        r = check_stick(sock, control)
        return [(r[0], cid, r[1])]
    keys = key_map() if kind in ("key", "macro") or "keys" in control else None
    if kind == "key":
        r = check_keys_control(control, {"id": cid}, [keys[control["key"]]])
        return [(r[0], cid, r[1])]
    if kind == "macro":
        r = check_keys_control(control, {"id": cid}, [keys[step[0]] for step in control["steps"]])
        return [(r[0], cid, r[1])]
    if kind == "hat" and "keys" in control:
        out = []
        direction = next(iter(control["positions"]))
        r = check_keys_control(control, {"id": cid, "value": direction}, [keys[control["keys"][direction]]])
        out.append((r[0], cid, r[1]))
        for direction in control.get("long", {}):
            r = check_keys_control(control, {"id": cid, "value": direction, "long": True}, [keys[control["keys"][direction]]])
            out.append((r[0], cid + " (long)", r[1]))
        return out
    if kind == "hat" and "steps" not in control:
        out = []
        seen = set()
        for direction in control["positions"]:
            axis = "ud" if direction in ("up", "down") else "lr"
            if axis in seen:
                continue
            seen.add(axis)
            r = check_one(sock, {**control, "positions": {direction: control["positions"][direction]}})
            out.append((r[0], cid + f" ({axis})", r[1]))
        return out
    r = check_one(sock, control)
    return [(r[0], cid, r[1])]


def check_one(sock: socket.socket, control: dict) -> tuple[str, str]:
    planned = command_for(control)
    if planned is None:
        return "SKIP", f"type {control['type']}"
    body, bios = planned
    drain(sock)
    sent = []
    if control.get("requires"):
        sim(f"{expand(control['requires']['id'])}={control['requires']['value']}")
        time.sleep(0.1)
    if control.get("step_fallback"):
        sim(f"{expand(control['id'])}={body['value']}")
        time.sleep(0.1)
    cover = expand(control["cover"]) if "cover" in control else None
    if control.get("guard"):
        if cover:
            sim(f"{cover}=1")
        status, reply = post({"id": control["id"], "guard": "open"})
        time.sleep(SETTLE)
        sent += drain(sock)
        if status != 200:
            return "FAIL", f"guard open refused: {reply}"
    status, reply = post(body)
    time.sleep(SETTLE)
    sent += drain(sock)
    if cover:
        sim(f"{cover}=0")
    if control.get("requires"):
        sim(f"{expand(control['requires']['id'])}=0")
    hit = [line for line in sent if line.split(" ")[0] == bios]
    if "steps" in control and hit:
        expected = f"{bios} " + ("INC" if control["steps"] == "fixed" else f"+{control['steps']}")
        if hit[0] != expected:
            return "FAIL", f"expected {expected!r}, got {hit[0]!r}"
    if control["type"] == "hat" and "steps" not in control and hit:
        level = {"up": 2, "down": 0, "left": 0, "right": 2}[body["value"]]
        expected = [f"{bios} {level}", f"{bios} 1"]
        if hit[:2] != expected:
            return "FAIL", f"expected {expected}, got {hit}"
    if control["type"] == "button" and SEAT is not None and hit:
        expected = [f"{bios} {control.get('value', 1)}", f"{bios} {control.get('rest', 0)}"]
        if hit[:2] != expected:
            return "FAIL", f"expected {expected}, got {hit}"
    if status != 200:
        return "FAIL", f"refused {status}: {reply.get('error')}"
    if not hit:
        return "FAIL", f"no command line for {bios}, got {sent}"
    return "PASS", f"{json.dumps(body)} -> {hit[0]}" + ("" if reply.get("confirmed") else " (not confirmed)")


def aircraft_name(dcs_name: str) -> str | None:
    sys.path.insert(0, str(REPO / "core"))
    sys.path.insert(0, str(REPO / "aircraft"))
    for path in sorted((REPO / "aircraft").glob("*.py")):
        module = importlib.import_module(path.stem)
        if dcs_name in module.DCS_NAMES:
            return module.NAME
    return None


def switch_aircraft() -> bool:
    name = aircraft_name(ACFT)
    if name is None:
        print(f"no file in aircraft/ lists {ACFT} in DCS_NAMES", file=sys.stderr)
        return False
    sim(f"_ACFT_NAME={ACFT}", *([] if SEAT is None else [f"SEAT_POSITION={SEAT}"]))
    deadline = time.monotonic() + 10
    seen = None
    while time.monotonic() < deadline:
        with urllib.request.urlopen(BRIDGE + "/state", timeout=15) as reply:
            seen = json.loads(reply.read())["aircraft"]
        if seen == name:
            return True
        time.sleep(0.2)
    print(f"the bridge does not switch to {ACFT} ({name}) within 10 s, /state shows {seen}", file=sys.stderr)
    return False


def main(names: list[str]) -> int:
    if not names:
        print(__doc__)
        return 2
    if not switch_aircraft():
        return 1
    with urllib.request.urlopen(BRIDGE + "/layout", timeout=15) as reply:
        layout = json.loads(reply.read())
    views = {}
    for view in layout["views"]:
        views.setdefault(view["name"].upper(), []).append(view)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", PORT))
    sock.setblocking(False)
    stop = threading.Event()
    sim("--reset")
    sim(f"_ACFT_NAME={ACFT}", *([] if SEAT is None else [f"SEAT_POSITION={SEAT}"]))
    keeper = threading.Thread(target=keep_fresh, args=(stop,), daemon=True)
    keeper.start()
    time.sleep(0.5)
    failed = 0
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    try:
        for name in names:
            candidates = views.get(name.upper(), [])
            view = next((v for v in candidates if SEAT is None or SEAT in v["seats"]), None)
            if view is None:
                other = [v for v in candidates]
                if other and SEAT is not None:
                    print(f"SKIP  {name}  page exists for seat {other[0]['seats']} only, not for seat {SEAT}")
                    counts["SKIP"] += 1
                    continue
                print(f"{name}: no such page")
                failed += 1
                continue
            entries = list(view["controls"])
            if SEAT is not None:
                entries += [{"id": lamp["button"], "type": "button", "hold": 0.3, "lamp_button": True} for lamp in view.get("lamps", []) if lamp.get("button")]
            for control in entries:
                for result, label, text in check(sock, control, view if SEAT is not None else None):
                    failed += result == "FAIL"
                    counts[result] += 1
                    print(f"{result}  {name}  {label}  {text}", flush=True)
    finally:
        stop.set()
        keeper.join()
        sock.close()
    print(f"{'FAILED' if failed else 'all PASS'}: {failed} failure(s)  (PASS {counts['PASS']}, SKIP {counts['SKIP']})")
    return 1 if failed else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if os.environ.get("SEAT_POSITION") in ("0", "1"):
        SEAT = int(os.environ["SEAT_POSITION"])
    while args[:1] in (["--acft"], ["--seat"]):
        if args[0] == "--acft":
            ACFT = args[1]
        else:
            SEAT = int(args[1])
        args = args[2:]
    if ACFT.startswith("AH-64D") and SEAT is None:
        SEAT = 0
    sys.exit(main(args))
