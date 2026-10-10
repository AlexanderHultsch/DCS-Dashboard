import json
import socket
import struct
from pathlib import Path

SYNC = b"\x55\x55\x55\x55"


def json_path(saved_games: str) -> Path:
    return Path(saved_games) / "Scripts" / "DCS-BIOS" / "doc" / "json" / "AH-64D.json"


def load_json(path) -> dict:
    if not Path(path).exists():
        raise SystemExit(f"DCS-BIOS control list not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_outputs(path, names: list[str]) -> tuple[dict, list[str]]:
    data = load_json(path)
    all_outputs = {}
    for category in data.values():
        for control in category.values():
            for output in control["outputs"]:
                all_outputs[control["identifier"] + output["suffix"]] = output
    found = {name: all_outputs[name] for name in names if name in all_outputs}
    missing = [name for name in names if name not in all_outputs]
    return found, missing


def load_controls(path) -> list[dict]:
    data = load_json(path)
    return [
        control
        for category in data.values()
        for control in category.values()
        if control["inputs"]
    ]


def open_socket(group: str, port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port))
    mreq = struct.pack("4s4s", socket.inet_aton(group), socket.inet_aton("0.0.0.0"))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


def send(sock: socket.socket, port: int, identifier: str, value) -> None:
    sock.sendto(f"{identifier} {value}\n".encode("ascii"), ("127.0.0.1", port))


def new_state() -> dict:
    return {"memory": bytearray(65536), "seen": bytearray(65536)}


def apply_packet(state: dict, data: bytes) -> None:
    pos = 4 if data.startswith(SYNC) else 0
    while pos < len(data):
        if pos + 4 > len(data):
            raise ValueError("truncated block header")
        address, length = struct.unpack_from("<HH", data, pos)
        pos += 4
        if pos + length > len(data):
            raise ValueError("truncated block data")
        if address + length > 65536:
            raise ValueError("block beyond 64 KB memory")
        state["memory"][address:address + length] = data[pos:pos + length]
        state["seen"][address:address + length] = b"\x01" * length
        pos += length


def read_value(state: dict, output: dict):
    address = output["address"]
    if state["seen"][address] == 0:
        return None
    memory = state["memory"]
    if output["type"] == "integer":
        word = int.from_bytes(memory[address:address + 2], "little")
        return (word & output["mask"]) >> output["shift_by"]
    raw = memory[address:address + output["max_length"]]
    return raw.decode("latin-1").rstrip("\x00")


def changes(state: dict, outputs: dict, last: dict) -> list[tuple[str, object]]:
    result = []
    for name, output in outputs.items():
        value = read_value(state, output)
        if value is None:
            continue
        if name not in last or last[name] != value:
            last[name] = value
            result.append((name, value))
    return result
