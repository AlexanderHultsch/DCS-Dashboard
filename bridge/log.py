import logging
import logging.handlers
import sys
from pathlib import Path

logger = logging.getLogger("dcs-dashboard")


def setup(log_cfg: dict) -> None:
    Path(log_cfg["file"]).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        log_cfg["file"],
        maxBytes=log_cfg["max_mb"] * 1024 * 1024,
        backupCount=log_cfg["backups"],
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03d | %(message)s", "%Y-%m-%d %H:%M:%S"))
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s.%(msecs)03d | %(message)s", "%H:%M:%S"))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False


def line(source: str, name: str, value) -> None:
    logger.info(f"{source:<7} | {name:<20} | {value}")
