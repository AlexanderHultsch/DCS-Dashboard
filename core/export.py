import socket


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
