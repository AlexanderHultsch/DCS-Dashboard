DCSBIOS_MODULE = "F-16C_50"
NAME = "F-16C"
DCS_NAMES = ["F-16C_50"]

KEYS = {}

BUTTON_HOLD = 0.3
UP_DOWN = {"up": "tri-up", "down": "tri-down"}
MFD_ROCKERS = [("GAIN", "TL"), ("SYM", "TR"), ("BRT", "BL"), ("CON", "BR")]

MASTER_LAMPS = [
    {"id": "LIGHT_MASTER_CAUTION", "label": "MASTER CAUTION", "color": "amber", "button": "MASTER_CAUTION"},
]


def mfd_controls(side: str) -> list[dict]:
    prefix = f"MFD_{side}"
    controls = [
        {"id": f"{prefix}_{n}", "label": str(n), "type": "button", "hold": BUTTON_HOLD, "side": side, "slot": str(n)}
        for n in range(1, 21)
    ]
    controls += [
        {"id": f"{prefix}_{name}_SW", "label": name, "type": "hat", "ud": f"{prefix}_{name}_SW", "hold": BUTTON_HOLD, "positions": UP_DOWN, "side": side, "slot": corner}
        for name, corner in MFD_ROCKERS
    ]
    return controls


VIEWS = [
    {
        "name": "COCKPIT", "seats": [0], "layout": "map", "controls": [],
        "lamps": MASTER_LAMPS + [
            {"id": "LIGHT_AR_NWS", "label": "AR / NWS", "color": "green"},
            {"id": "LIGHT_MARKER_BEACON", "label": "MARKER", "color": "green"},
            {"id": "LIGHT_CANOPY", "label": "CANOPY", "color": "red"},
            {"id": "LIGHT_ENG_FIRE", "label": "ENG FIRE", "color": "red"},
        ],
        "links": [
            {"label": "MFD L", "view": "MFD", "side": "L", "seats": [0], "map": [2, 6, 2, 1]},
            {"label": "MFD R", "view": "MFD", "side": "R", "seats": [0], "map": [2, 8, 2, 1]},
        ],
    },
    {
        "name": "MFD", "seats": [0], "layout": "mfcd", "lamps": [], "controls": mfd_controls("L") + mfd_controls("R"),
        "titles": {"L": "LEFT MFD", "R": "RIGHT MFD"}, "inert": [],
    },
]

CONTROL_NAMES = []

MPD_INDICATIONS = ()
MPD_SEATS = {}

TRIM_RELEASED = None

SEATS = [{"prefix": "", "label": "F-16C"}]
SEAT_OUTPUT = None
TRIM_SWITCH = None
