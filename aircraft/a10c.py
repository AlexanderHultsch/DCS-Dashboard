DCSBIOS_MODULE = "A-10C"
NAME = "A-10C"
DCS_NAMES = ["A-10C_2"]

KEYS = {}

MASTER_LAMPS = [
    {"id": "MASTER_CAUTION", "label": "MASTER CAUTION", "color": "amber", "button": "UFC_MASTER_CAUTION"},
]

VIEWS = [
    {"name": "COCKPIT", "seats": [0], "layout": "map", "lamps": MASTER_LAMPS, "controls": [], "links": []},
]

CONTROL_NAMES = []

MPD_INDICATIONS = ()
MPD_SEATS = {}

TRIM_RELEASED = None

SEATS = [{"prefix": "", "label": "A-10C"}]
SEAT_OUTPUT = None
TRIM_SWITCH = None
