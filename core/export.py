import socket
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lua" / "DCS-Dashboard-Export.lua"


def open_socket(port: int) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))
    return sock


def parse(data: bytes) -> dict[str, str]:
    values = {}
    for line in data.decode("utf-8", errors="replace").splitlines():
        if not line:
            continue
        name, sep, value = line.partition("=")
        if not sep:
            raise ValueError(f"line without '=': {line[:40]}")
        values[name] = value
    return values


def install_problems(saved_games: str) -> list[str]:
    scripts = Path(saved_games) / "Scripts"
    installed = scripts / SCRIPT.name
    problems = []
    if not installed.exists():
        problems.append("not installed: copy core\\lua\\DCS-Dashboard-Export.lua to <Saved Games>\\Scripts")
    elif installed.read_bytes().replace(b"\r\n", b"\n") != SCRIPT.read_bytes().replace(b"\r\n", b"\n"):
        problems.append("outdated: copy core\\lua\\DCS-Dashboard-Export.lua to <Saved Games>\\Scripts again, then restart the mission")
    export_lua = scripts / "Export.lua"
    if not export_lua.exists() or SCRIPT.name not in export_lua.read_text(encoding="utf-8", errors="replace"):
        problems.append("not loaded: add the dofile line to <Saved Games>\\Scripts\\Export.lua, see README step 4")
    return problems
