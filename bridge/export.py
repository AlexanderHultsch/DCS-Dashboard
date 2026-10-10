import socket

NAMES = [
    "lat", "lon", "alt", "hdg", "pitch", "bank", "ias", "tas", "ralt", "vs", "g",
    "eng_rpm_l", "eng_rpm_r", "eng_temp_l", "eng_temp_r",
    "fuel_int", "fuel_ext", "fuel_flow_l", "fuel_flow_r",
]


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


def changes(values: dict[str, str], last: dict) -> list[tuple[str, str]]:
    result = []
    for name, value in values.items():
        if name not in last or last[name] != value:
            last[name] = value
            result.append((name, value))
    return result
