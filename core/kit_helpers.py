"""Constants and builders shared by the aircraft files that use the panel kit."""

from panel_kit import REF

BUTTON_HOLD = 0.3
KNOB_STEP = 3200
UP_DOWN = {"up": "tri-up", "down": "tri-down"}

# arrow heads of the emergency trim hat, in glyph units (width, height, paths)
ARROW_UP = (10, 9, [("M0.5 8.5L5 0.5L9.5 8.5Z", 1, True)])
ARROW_DOWN = (10, 9, [("M0.5 0.5L5 8.5L9.5 0.5Z", 1, True)])
ARROW_LEFT = (9, 10, [("M8.5 0.5L0.5 5L8.5 9.5Z", 1, True)])
ARROW_RIGHT = (9, 10, [("M0.5 0.5L8.5 5L0.5 9.5Z", 1, True)])


def kit_page(name: str, cell: list | None, page: dict, lamps: list, seat: int = 0) -> dict:
    return {
        "name": name, "seats": [seat], **({"panel": True, "map": cell} if cell is not None else {}), "layout": "panel", "box": page["box"],
        "lamps": lamps, "print": page["print"], "art": page["art"], "controls": page["controls"],
        **({"indicators": page["indicators"]} if page["indicators"] else {}),
        **({"scroll": True} if page.get("scroll") else {}),
        "kit": True, "ref": list(REF),
    }


def step_rocker(bios: str, label: str) -> dict:
    return {"id": bios, "label": label, "type": "hat", "ud": bios, "steps": "fixed", "positions": {"up": "tri-up", "down": "tri-down"}}


def readout(bios: str, label: str, cols: int) -> dict:
    return {"id": bios, "label": label, "type": "display", "cols": cols, "ids": [bios]}
