import csv
import select
import socket
import sys
import time
from pathlib import Path

from bridge import config, dcsbios, keys, log

BLOCK = ["JETT", "FIRE_ENG", "FIRE_APU", "FIRE_PRIME", "FIRE_RES", "ZERO", "CHOP", "BUCS", "TRIGGER"]
TIMEOUT = 0.5


def integer_output(control: dict):
    return next((o for o in control["outputs"] if o["type"] == "integer"), None)


def get_input(control: dict, interface: str):
    return next((i for i in control["inputs"] if i["interface"] == interface), None)


def positions(control: dict):
    set_state = get_input(control, "set_state")
    if set_state is None:
        return None
    m = set_state["max_value"]
    return list(range(m + 1)) if m <= 20 else [0, m // 2, m]


def pump(sock: socket.socket, state: dict, timeout: float) -> None:
    ready, _, _ = select.select([sock], [], [], max(timeout, 0))
    if ready:
        try:
            dcsbios.apply_packet(state, sock.recv(65536))
        except ValueError as e:
            log.line("bridge", "dcsbios packet skipped", e)


def wait_until(sock: socket.socket, state: dict, output: dict, check, timeout: float = TIMEOUT):
    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        pump(sock, state, remaining)
        v = dcsbios.read_value(state, output)
        if v is not None and check(v):
            return v
    return dcsbios.read_value(state, output)


def send(cmd_sock: socket.socket, cmd_port: int, identifier: str, value) -> None:
    log.line("stage2", identifier, f"sent {value}")
    dcsbios.send(cmd_sock, cmd_port, identifier, value)


def sweep(sock: socket.socket, cmd_sock: socket.socket, cmd_port: int, state: dict, control: dict) -> tuple[str, str]:
    identifier = control["identifier"]
    if any(word in identifier for word in BLOCK):
        return "skipped", "blocklist"
    output = integer_output(control)
    steps = positions(control)
    if output is None:
        if steps is not None:
            for value in steps + [0]:
                send(cmd_sock, cmd_port, identifier, value)
        elif get_input(control, "action") is not None:
            send(cmd_sock, cmd_port, identifier, "TOGGLE")
        return "sent-unverified", ""
    original = dcsbios.read_value(state, output)
    if original is None:
        return "fail", "no readback"

    if steps is not None:
        m = get_input(control, "set_state")["max_value"]
        tol = m // 100 if m > 20 else 0
        failed = []
        try:
            for p in steps:
                send(cmd_sock, cmd_port, identifier, p)
                v = wait_until(sock, state, output, lambda v: abs(v - p) <= tol)
                log.line("stage2", identifier, f"read {v}")
                if v is None or abs(v - p) > tol:
                    failed.append(str(p))
        finally:
            send(cmd_sock, cmd_port, identifier, original)
            v = wait_until(sock, state, output, lambda v: abs(v - original) <= tol)
            log.line("stage2", identifier, f"read {v}")
            if v is None or abs(v - original) > tol:
                failed.append("restore")
        return ("pass", "") if not failed else ("fail", " ".join(failed))

    variable_step = get_input(control, "variable_step")
    if variable_step is not None:
        step = variable_step["suggested_step"]
        tol = output["max_value"] // 100
        send(cmd_sock, cmd_port, identifier, f"+{step}")
        v = wait_until(sock, state, output, lambda v: v != original)
        log.line("stage2", identifier, f"read {v}")
        if v is None or v == original:
            return "fail", "no change"
        send(cmd_sock, cmd_port, identifier, f"-{step}")
        v = wait_until(sock, state, output, lambda v: abs(v - original) <= tol)
        log.line("stage2", identifier, f"read {v}")
        if v is None or abs(v - original) > tol:
            return "fail", "no return"
        return "pass", ""
    if get_input(control, "action") is not None:
        send(cmd_sock, cmd_port, identifier, "TOGGLE")
        v = wait_until(sock, state, output, lambda v: v != original)
        log.line("stage2", identifier, f"read {v}")
        if v is None or v == original:
            return "fail", "no change"
        send(cmd_sock, cmd_port, identifier, "TOGGLE")
        v = wait_until(sock, state, output, lambda v: v == original)
        log.line("stage2", identifier, f"read {v}")
        if v != original:
            return "fail", "no return"
        return "pass", ""
    return "sent-unverified", ""


def wait_for_seat(sock: socket.socket, state: dict, seat_output: dict) -> int:
    deadline = time.monotonic() + 30
    while dcsbios.read_value(state, seat_output) is None and time.monotonic() < deadline:
        pump(sock, state, deadline - time.monotonic())
    seat = dcsbios.read_value(state, seat_output)
    if seat is None:
        raise SystemExit("No DCS-BIOS data. Is DCS running with a mission loaded?")
    return seat


def write_results(cfg: dict, rows: list) -> Path:
    results_file = Path(cfg["log"]["file"]).parent / "stage2_results.csv"
    is_new = not results_file.exists()
    with open(results_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["control", "seat", "route", "result", "note"])
        writer.writerows(rows)
    return results_file


def sweep_test(bios_sock: socket.socket, cmd_sock: socket.socket, cmd_port: int, state: dict, controls: list, name: str, text: str) -> tuple[list, dict, int]:
    prefix = name + "_"
    selected = [c for c in controls if c["identifier"].startswith(prefix) and text in c["identifier"]]
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if all(dcsbios.read_value(state, integer_output(c)) is not None for c in selected if integer_output(c)):
            break
        pump(bios_sock, state, deadline - time.monotonic())

    seconds = TIMEOUT * sum(
        len(positions(c)) + 1
        for c in selected
        if not any(word in c["identifier"] for word in BLOCK) and integer_output(c) and positions(c)
    )
    log.line("bridge", "ready", f"seat {name}, {len(selected)} controls, about {seconds / 60:.0f} min at most")

    rows = []
    counts = {}
    try:
        input("Press Enter to start, Ctrl+C to stop. ")
        for i, control in enumerate(selected, 1):
            result, note = sweep(bios_sock, cmd_sock, cmd_port, state, control)
            log.line("stage2", control["identifier"], f"[{i}/{len(selected)}] {result} {note}".strip())
            rows.append((control["identifier"], name, "dcsbios", result, note))
            counts[result] = counts.get(result, 0) + 1
    except KeyboardInterrupt:
        pass
    return rows, counts, len(selected)


def key_tests(cfg: dict) -> tuple[list, str]:
    entries = cfg.get("keys")
    title = cfg.get("dcs", {}).get("window_title")
    if entries is None or title is None:
        raise SystemExit("config.toml needs [keys] and [dcs] window_title, see config.example.toml.")
    for key_name, combo in entries.items():
        try:
            keys.parse(combo)
        except ValueError as e:
            raise SystemExit(f"[keys] {key_name} = '{combo}': {e}")
    tests = []
    for key_name, combo in entries.items():
        if key_name.startswith("george_") and key_name != "george_show_hide":
            tests.append((f"{key_name} short", combo, 0.1))
            tests.append((f"{key_name} long", combo, 1.0))
        else:
            tests.append((key_name, combo, 0.1))
    return tests, title


def keys_test(tests: list, title: str, name: str) -> tuple[list, dict, int]:
    log.line("bridge", "ready", f"seat {name}, {len(tests)} key tests, window '{title}'")
    rows = []
    counts = {}
    try:
        for i, (label, combo, hold) in enumerate(tests, 1):
            answer = input(f"{label} ({combo}): Enter to send, s to skip: ").strip().lower()
            note = ""
            if answer == "s":
                result = "skipped"
            else:
                ok = keys.focus(title)
                log.line("stage2", label, "focus ok" if ok else "focus failed")
                if not ok:
                    result, note = "fail", "no focus"
                else:
                    time.sleep(0.3)
                    log.line("stage2", label, f"sent {combo} hold {hold}")
                    keys.press(combo, hold)
                    answer = ""
                    while answer not in ("y", "n", "s"):
                        answer = input("Did it work? y / n / s: ").strip().lower()
                    result = {"y": "pass", "n": "fail", "s": "skipped"}[answer]
            log.line("stage2", label, f"[{i}/{len(tests)}] {result} {note}".strip())
            rows.append((label, name, "keys", result, note))
            counts[result] = counts.get(result, 0) + 1
    except KeyboardInterrupt:
        pass
    return rows, counts, len(tests)


def main() -> None:
    keys_mode = sys.argv[1:] == ["keys"]
    text = sys.argv[1] if len(sys.argv) > 1 else ""

    cfg = config.load()
    log.setup(cfg["log"])
    tests, title = key_tests(cfg) if keys_mode else ([], "")
    path = dcsbios.json_path(cfg["dcs"]["saved_games"])
    controls = [] if keys_mode else dcsbios.load_controls(path)
    seat_output = dcsbios.load_outputs(path, ["SEAT_POSITION"])[0]["SEAT_POSITION"]
    group, port = cfg["dcs_bios"]["export_multicast"], cfg["dcs_bios"]["export_port"]
    cmd_port = cfg["dcs_bios"]["command_port"]
    bios_sock = dcsbios.open_socket(group, port)
    cmd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    log.line("bridge", "start", f"stage 2 {'keys' if keys_mode else 'sweep'}, DCS-BIOS {group}:{port}, commands to port {cmd_port}")

    state = dcsbios.new_state()
    seat = wait_for_seat(bios_sock, state, seat_output)
    name = "PLT" if seat == 0 else "CPG"

    if keys_mode:
        rows, counts, total = keys_test(tests, title, name)
        unit = "key tests"
    else:
        rows, counts, total = sweep_test(bios_sock, cmd_sock, cmd_port, state, controls, name, text)
        unit = "controls"

    results_file = write_results(cfg, rows)
    log.line("bridge", "summary", ", ".join(f"{k} {v}" for k, v in counts.items()))
    log.line("bridge", "stop", f"{len(rows)} of {total} {unit}, results in {results_file.name}")
    bios_sock.close()
    cmd_sock.close()


if __name__ == "__main__":
    main()
