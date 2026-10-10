import os
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(path=ROOT / "config.toml") -> dict:
    if not Path(path).exists():
        raise SystemExit("config.toml not found. Copy config.example.toml to config.toml and adjust it.")
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    cfg["dcs"]["saved_games"] = os.path.expandvars(cfg["dcs"]["saved_games"])
    cfg["log"]["file"] = str(ROOT / cfg["log"]["file"])
    return cfg
