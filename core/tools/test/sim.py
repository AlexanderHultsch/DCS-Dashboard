#!/usr/bin/env python3
"""Send ONE DCS-BIOS export packet that sets the named outputs.

  python3 sim.py [--json DIR] NAME=VALUE ...    e.g. SEAT_POSITION=1 PLT_KU_DISPLAY="HELLO"
  python3 sim.py --reset                        clear the remembered 64 KB memory (logs/test/sim_state.bin)

The control list is read from the DCS-BIOS JSON folder: <saved_games>/Scripts/DCS-BIOS/doc/json, with saved_games
from the dashboard config, or DIR when --json is given. Only MetadataStart.json, CommonData.json and the DCSBIOS_MODULE
file of every aircraft file in aircraft/ are read. Text for string outputs, numbers for integer outputs.
"""
import importlib
import json
import socket
import struct
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "core"))
import config

STATE = REPO / "logs" / "test" / "sim_state.bin"
GROUP, PORT = "239.255.50.10", 5010
SYNC = b"\x55\x55\x55\x55"


def json_dir(args: list[str]) -> Path:
    if "--json" in args:
        i = args.index("--json")
        path = Path(args[i + 1])
        del args[i:i + 2]
        return path
    return Path(config.load()["dcs"]["saved_games"]) / "Scripts" / "DCS-BIOS" / "doc" / "json"


def json_files(directory: Path) -> list[Path]:
    sys.path.insert(0, str(REPO / "aircraft"))
    modules = [importlib.import_module(path.stem).DCSBIOS_MODULE for path in sorted((REPO / "aircraft").glob("*.py"))]
    return [directory / f"{name}.json" for name in ["MetadataStart", "CommonData", *modules]]


def load_all_outputs(directory: Path) -> dict:
    outputs = {}
    for path in json_files(directory):
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for category in data.values():
            for control in category.values():
                for output in control["outputs"]:
                    outputs.setdefault(control["identifier"] + output["suffix"], []).append((path.stem, output))
    return outputs


def load_memory() -> bytearray:
    if STATE.exists():
        data = STATE.read_bytes()
        if len(data) == 65536:
            return bytearray(data)
    return bytearray(65536)


def main(argv: list[str]) -> int:
    args = argv[1:]
    STATE.parent.mkdir(parents=True, exist_ok=True)
    if "--reset" in args:
        STATE.write_bytes(bytes(65536))
        args.remove("--reset")
        if not args:
            return 0
    if not args:
        print(__doc__)
        return 2
    outputs = load_all_outputs(json_dir(args))
    memory = load_memory()
    blocks = b""
    for arg in args:
        name, sep, value = arg.partition("=")
        if not sep:
            print(f"expected NAME=VALUE, got {arg!r}", file=sys.stderr)
            return 2
        found = outputs.get(name)
        if not found:
            print(f"unknown output {name!r}", file=sys.stderr)
            return 2
        if len(found) > 1 and len({json.dumps(o, sort_keys=True) for _, o in found}) > 1:
            print(f"{name!r} is ambiguous: {', '.join(m for m, _ in found)}", file=sys.stderr)
            return 2
        output = found[0][1]
        address = output["address"]
        if output["type"] == "integer":
            number = int(value, 0)
            if not 0 <= number <= output["max_value"]:
                print(f"{name}: {number} outside 0..{output['max_value']}", file=sys.stderr)
                return 2
            word = int.from_bytes(memory[address:address + 2], "little")
            word = (word & ~output["mask"] & 0xFFFF) | ((number << output["shift_by"]) & output["mask"])
            data = word.to_bytes(2, "little")
        else:
            text = value.encode("latin-1")
            if len(text) > output["max_length"]:
                print(f"{name}: text longer than {output['max_length']}", file=sys.stderr)
                return 2
            data = text.ljust(output["max_length"], b"\x00")
        memory[address:address + len(data)] = data
        blocks += struct.pack("<HH", address, len(data)) + data
    STATE.write_bytes(bytes(memory))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    sock.sendto(SYNC + blocks, (GROUP, PORT))
    sock.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
