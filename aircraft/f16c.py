DCSBIOS_MODULE = "F-16C_50"
NAME = "F-16C"
DCS_NAMES = ["F-16C_50"]

KEYS = {}

MASTER_LAMPS = [
    {"id": "LIGHT_MASTER_CAUTION", "label": "MASTER CAUTION", "color": "amber", "button": "MASTER_CAUTION"},
]

VIEWS = [
    {
        "name": "COCKPIT", "seats": [0], "layout": "map", "controls": [],
        "lamps": MASTER_LAMPS + [
            {"id": "LIGHT_AR_NWS", "label": "AR / NWS", "color": "green"},
            {"id": "LIGHT_MARKER_BEACON", "label": "MARKER", "color": "green"},
            {"id": "LIGHT_CANOPY", "label": "CANOPY", "color": "red"},
            {"id": "LIGHT_ENG_FIRE", "label": "ENG FIRE", "color": "red"},
        ],
        "links": [],
    },
]

CONTROL_NAMES = []

MPD_INDICATIONS = ()
MPD_SEATS = {}

TRIM_RELEASED = None

SEATS = [{"prefix": "", "label": "F-16C"}]
SEAT_OUTPUT = None
TRIM_SWITCH = None
