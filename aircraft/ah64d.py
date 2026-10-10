DCSBIOS_MODULE = "AH-64D"

POWER_POSITIONS = [
    {"value": 0, "label": "OFF"},
    {"value": 16383, "label": "IDLE"},
    {"value": 58981, "label": "FLY"},
    {"value": 65535, "label": "LOCKOUT", "disabled": True},
]
ENGINE_START_POSITIONS = [
    {"value": 2, "label": "START", "momentary": True},
    {"value": 1, "label": "OFF"},
    {"value": 0, "label": "IGN ORIDE", "momentary": True},
]
MODE_POSITIONS = [
    {"value": 2, "label": "DAY"},
    {"value": 1, "label": "NT"},
    {"value": 0, "label": "MONO"},
]
TEDAC_MODE_POSITIONS = [
    {"value": 2, "label": "DAY"},
    {"value": 1, "label": "NT"},
    {"value": 0, "label": "OFF"},
]
KNOB_STEP = 3200
MPD_BUTTON_HOLD = 0.3
MPD_LABELS = {"B1": "M", "AC": "A/C", "AST": "*"}
KU_LABELS = {
    "DOT": ".", "SIGN": "+/-", "SLASH": "/", "DIV": "\u00f7", "MULTI": "*", "PLUS": "+",
    "MINUS": "\u2212", "BKS": "BKS", "SPC": "SPC", "CLR": "CLR", "ENT": "ENTER", "LEFT": "\u2190", "RIGHT": "\u2192",
}


def mpd_controls(side: str) -> list[dict]:
    slots = [f"{row}{n}" for row in "TLRB" for n in range(1, 7)] + ["FCR", "WPN", "TSD", "VID", "COM", "AC", "AST"]
    controls = [
        {"id": f"{{seat}}_MPD_{side}_{slot}", "label": MPD_LABELS.get(slot, slot), "type": "button", "hold": MPD_BUTTON_HOLD, "side": side, "slot": slot}
        for slot in slots
    ]
    controls += [
        {"id": f"{{seat}}_MPD_{side}_BRT", "label": "BRT", "type": "knob", "step": KNOB_STEP, "side": side, "slot": "BRT"},
        {"id": f"{{seat}}_MPD_{side}_VIDEO", "label": "VID", "type": "knob", "step": KNOB_STEP, "side": side, "slot": "VIDEO"},
        {"id": f"{{seat}}_MPD_{side}_MODE", "label": "MODE", "type": "selector", "step_fallback": True, "positions": MODE_POSITIONS, "side": side, "slot": "MODE"},
    ]
    return controls


def ku_controls() -> list[dict]:
    slots = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + list(KU_LABELS)
    controls = [{"id": "{seat}_KU_DISPLAY", "label": "SCRATCHPAD", "type": "display", "slot": "DISPLAY"}]
    controls += [
        {"id": f"{{seat}}_KU_{slot}", "label": KU_LABELS.get(slot, slot), "type": "button", "hold": MPD_BUTTON_HOLD, "slot": slot}
        for slot in slots
    ]
    controls.append({"id": "{seat}_KU_BRT", "label": "BRT", "type": "knob", "step": KNOB_STEP, "slot": "BRT"})
    return controls


def cursor_controls() -> list[dict]:
    return [
        {"id": "{seat}_CURSOR", "label": "CURSOR", "type": "stick", "x": "{seat}_COLLECTIVE_CURSOR_LR", "y": "{seat}_COLLECTIVE_CURSOR_UD", "slot": "CURSOR"},
        {"id": "{seat}_COLLECTIVE_CURSOR_DISPLAY", "label": "CURSOR SWITCH DISPLAY", "type": "button", "hold": MPD_BUTTON_HOLD, "slot": "CURSOR_DISPLAY"},
        {"id": "{seat}_COLLECTIVE_CURSOR_ENTER", "label": "ENTER", "type": "button", "hold": MPD_BUTTON_HOLD, "slot": "CURSOR_ENTER"},
    ]


def tedac_controls() -> list[dict]:
    buttons = [
        ("TAD_SEL", "TAD", "TAD"), ("FCR_SEL", "FCR", "FCR"), ("PNV_SEL", "PNV", "PNV"), ("GS_SEL", "G/S", "GS"),
        ("MULTI", "*", "AST"), ("BORESIGHT", "AZ/EL", "B1"), ("ACM", "ACM", "B2"), ("FREEZE", "FREEZE", "B3"), ("FILTER", "FILTER", "B4"),
    ]
    controls = [
        {"id": f"CPG_TEDAC_{name}", "label": label, "type": "button", "hold": MPD_BUTTON_HOLD, "side": "T", "seats": [1], "slot": slot}
        for name, label, slot in buttons
    ]
    controls.append({"id": "CPG_TEDAC_DISP_MODE", "label": "MODE", "type": "selector", "step_fallback": True, "positions": TEDAC_MODE_POSITIONS, "side": "T", "seats": [1], "slot": "MODE"})
    controls += [
        {"id": f"CPG_TEDAC_{name}", "label": label, "type": "knob", "step": KNOB_STEP, "side": "T", "seats": [1], "slot": label}
        for name, label in (("FLIR_LEV", "LEV"), ("FLIR_GAIN", "GAIN"))
    ]
    controls += [
        {"id": f"CPG_TEDAC_{name}", "label": label, "type": "hat", "ud": f"CPG_TEDAC_{name}", "hold": MPD_BUTTON_HOLD, "positions": {"up": "\u25b2", "down": "\u25bc"}, "side": "T", "seats": [1], "slot": name}
        for name, label in (("RF", "R/F"), ("EL", "EL"), ("SYM", "SYM"), ("BRT", "BRT"), ("CON", "CON"))
    ]
    controls.append({"id": "CPG_TEDAC_AZ", "label": "AZ", "type": "hat", "lr": "CPG_TEDAC_AZ", "hold": MPD_BUTTON_HOLD, "positions": {"left": "\u25c0", "right": "\u25b6"}, "side": "T", "seats": [1], "slot": "AZ"})
    return controls


MASTER_LAMPS = [
    {"id": "{seat}_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "{seat}_INTL_MWARN_BTN"},
    {"id": "{seat}_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "{seat}_INTL_MCAUTION_BTN"},
]


def panel_pages(name: str, cells: dict, box: list, placard: list, art: list, controls: list) -> list[dict]:
    return [
        {
            "name": name, "seats": [seat], "panel": True, "layout": "panel", "map": cell, "box": box,
            "lamps": MASTER_LAMPS, "print": placard, "art": art, "controls": controls,
        }
        for seat, cell in cells.items()
    ]


def tail_wheel_pages() -> list[dict]:
    controls = [
        {"id": "{seat}_T_WHEEL_UNLOCK_BTN", "label": "TAIL WHEEL", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_T_WHEEL_UNLOCK_L", "legend": "UNLOCK", "color": "amber", "at": [130, 71, 88, 90]},
        {"id": "{seat}_NVS_MODE", "label": "NVS MODE", "type": "selector", "positions": [{"value": 2, "label": "FIXED"}, {"value": 1, "label": "NORM"}, {"value": 0, "label": "OFF"}], "at": [410, 52, 80, 126]},
    ]
    placard = [
        ["TAIL WHEEL", 177.5, 38, 30, 153], ["+", 83, 51, 16], ["NVS MODE", 456, 43, 30, 134],
        ["FIXED", 449, 68.5, 21, 52], ["NORM", 497.5, 115, 21, 67, 90], ["OFF", 447, 165, 20, 36],
    ]
    art = [
        {"shape": "plate", "at": [10, 6, 600, 196]},
        {"shape": "bracket", "at": [9, 4, 44, 80]},
        {"shape": "bracket", "at": [572, 128, 50, 74]},
        {"shape": "screw", "at": [31, 60, 18]}, {"shape": "screw", "at": [61, 143, 14]},
        {"shape": "screw", "at": [551, 68, 14]}, {"shape": "screw", "at": [594, 158, 18]},
        {"shape": "outline", "at": [121, 63, 100, 101]},
    ]
    return panel_pages("TAIL WHEEL / NVS", {0: [2, 1, 1, 3], 1: [5, 1, 1, 3]}, [622, 216], placard, art, controls)


def emergency_pages() -> list[dict]:
    controls = [
        {"id": "{seat}_EMERG_GUARD_BTN", "label": "GUARD", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_EMERG_GUARD_L", "color": "green", "at": [103, 99, 84, 86]},
        {"id": "{seat}_EMERG_XPNDR_BTN", "label": "XPNDR", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_EMERG_XPNDR_L", "color": "green", "at": [213, 99, 86, 87]},
        {"id": "{seat}_EMERG_ZERO_SW", "label": "ZEROIZE", "type": "selector", "guard": True, "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}], "at": [326, 96, 80, 88]},
        {"id": "{seat}_EMERG_HYD_BTN", "label": "EMERG HYD", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_EMERG_HYD_L", "color": "green", "at": [449, 115, 90, 89]},
    ]
    placard = [
        ["EMERGENCY", 302.5, 32, 28, 188], ["+", 131, 51, 16], ["GUARD", 146.5, 80, 25, 83], ["XPNDR", 255.5, 81.5, 25, 81],
        ["ZEROIZE", 364.5, 84, 25, 105], ["EMERG", 497, 60, 25, 84], ["HYD", 496.5, 84.5, 25, 49],
    ]
    art = [
        {"shape": "plate", "at": [9, 4, 601, 228]},
        {"shape": "bracket", "at": [9, 4, 44, 82]},
        {"shape": "bracket", "at": [574, 166, 51, 66]},
        {"shape": "screw", "at": [32, 60, 19]}, {"shape": "screw", "at": [72, 179, 15]},
        {"shape": "screw", "at": [561, 72, 15]}, {"shape": "screw", "at": [598, 188, 18]},
        {"shape": "outline", "at": [96, 90, 100, 98]}, {"shape": "outline", "at": [205, 91, 100, 101]},
        {"shape": "hazard", "at": [427, 93, 139, 133], "hole": [445, 111, 98, 97]},
    ]
    return panel_pages("EMERGENCY", {0: [3, 1, 1, 3], 1: [2, 1, 1, 3]}, [625, 251], placard, art, controls)


VIEWS = [
    {
        "name": "COCKPIT",
        "seats": [0, 1],
        "layout": "map",
        "lamps": MASTER_LAMPS,
        "controls": [
            {"id": "canopy", "label": "CANOPY", "type": "key", "key": "canopy", "readback": "PLT_CANOPY", "states": {"0": "CLOSED", "1": "OPEN"}, "seats": [0], "map": [2, 7, 1, 3]},
        ],
        "links": [
            {"label": "KU", "view": "KU", "seats": [0, 1], "map": [1, 1, 1, 3]},
            {"label": "MPD L", "view": "MPD", "side": "L", "seats": [0], "map": [3, 4, 3, 3]},
            {"label": "MPD R", "view": "MPD", "side": "R", "seats": [0], "map": [3, 7, 3, 3]},
            {"label": "MPD L", "view": "MPD", "side": "L", "seats": [1], "map": [2, 4, 3, 2]},
            {"label": "TEDAC", "view": "MPD", "side": "T", "seats": [1], "map": [2, 6, 3, 2]},
            {"label": "MPD R", "view": "MPD", "side": "R", "seats": [1], "map": [2, 8, 3, 3]},
        ],
    },
    *tail_wheel_pages(),
    *emergency_pages(),
    {
        "name": "Startup",
        "seats": [0],
        "lamps": [
            {"id": "PLT_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "PLT_INTL_MWARN_BTN"},
            {"id": "PLT_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "PLT_INTL_MCAUTION_BTN"},
            {"id": "PLT_ENG_1_FIRE_L", "label": "ENG 1 FIRE", "color": "red"},
            {"id": "PLT_APU_FIRE_L", "label": "APU FIRE", "color": "red"},
            {"id": "PLT_ENG_2_FIRE_L", "label": "ENG 2 FIRE", "color": "red"},
            {"id": "PLT_APU_L", "label": "APU ON", "color": "green"},
        ],
        "controls": [
            {"id": "PLT_MASTER_IGN_SW", "label": "MSTR IGN", "type": "selector", "positions": [{"value": 0, "label": "OFF"}, {"value": 1, "label": "BATT"}, {"value": 2, "label": "EXT PWR", "disabled": True}], "grid": [1, 1, 1, 1]},
            {"id": "PLT_APU_BTN_CVR", "label": "APU COVER", "type": "selector", "positions": [{"value": 0, "label": "CLOSED"}, {"value": 1, "label": "OPEN"}], "grid": [1, 2, 1, 1]},
            {"id": "PLT_APU_BTN", "label": "APU", "type": "button", "hold": 0.3, "requires": {"id": "PLT_APU_BTN_CVR", "value": 1}, "grid": [1, 3, 1, 1]},
            {"id": "PLT_ENG1_START", "label": "ENG 1 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS, "grid": [1, 4, 1, 1]},
            {"id": "PLT_ENG2_START", "label": "ENG 2 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS, "grid": [1, 5, 1, 1]},
            {"id": "power_left", "label": "PWR LVR 1", "type": "lever", "readback": "PLT_ENG_L_PW_LVR", "side": "left", "positions": POWER_POSITIONS, "grid": [1, 6, 3, 1]},
            {"id": "power_right", "label": "PWR LVR 2", "type": "lever", "readback": "PLT_ENG_R_PW_LVR", "side": "right", "positions": POWER_POSITIONS, "grid": [1, 7, 3, 1]},
            {"id": "PLT_ROTOR_BRK", "label": "RTR BRK", "type": "selector", "positions": [{"value": 2, "label": "OFF"}, {"value": 1, "label": "BRK", "disabled": True}, {"value": 0, "label": "LOCK"}], "grid": [2, 1, 1, 1]},
            {"id": "PLT_PARK_BRAKE", "label": "PARK BRAKE", "type": "selector", "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "PULLED"}], "grid": [2, 2, 1, 1]},
            {"id": "PLT_T_WHEEL_UNLOCK_BTN", "label": "TAIL WHEEL", "type": "button", "hold": 0.3, "lamp": "PLT_T_WHEEL_UNLOCK_L", "legend": "UNLOCK", "seats": [0], "grid": [2, 5, 1, 1]},
            {"id": "PLT_EXTL_NAV_L_SW", "label": "NAV", "type": "selector", "positions": [{"value": 2, "label": "BRT"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "DIM"}], "grid": [2, 3, 1, 1]},
            {"id": "PLT_EXTL_ACOL_L_SW", "label": "ANTI COL", "type": "selector", "positions": [{"value": 2, "label": "WHT"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "RED"}], "grid": [2, 4, 1, 1]},
            {"id": "PLT_MPD_L_MODE", "label": "MPD L", "type": "selector", "step_fallback": True, "positions": MODE_POSITIONS, "grid": [3, 1, 1, 1]},
            {"id": "PLT_MPD_R_MODE", "label": "MPD R", "type": "selector", "step_fallback": True, "positions": MODE_POSITIONS, "grid": [3, 2, 1, 1]},
            {"id": "canopy", "label": "CANOPY", "type": "key", "key": "canopy", "readback": "PLT_CANOPY", "states": {"0": "CLOSED", "1": "OPEN"}, "grid": [3, 3, 1, 1]},
        ],
    },
    {
        "name": "Flight",
        "seats": [0, 1],
        "lamps": [
            {"id": "{seat}_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "{seat}_INTL_MWARN_BTN"},
            {"id": "{seat}_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "{seat}_INTL_MCAUTION_BTN"},
            {"id": "PLT_ENG_1_FIRE_L", "label": "ENG 1 FIRE", "color": "red"},
            {"id": "PLT_APU_FIRE_L", "label": "APU FIRE", "color": "red"},
            {"id": "PLT_ENG_2_FIRE_L", "label": "ENG 2 FIRE", "color": "red"},
            {"id": "PLT_APU_L", "label": "APU ON", "color": "green"},
        ],
        "controls": [
            {"id": "controls", "label": "CONTROLS", "type": "controls", "trim_switch": "{seat}_CYCLIC_TRIM_UD", "grid": [1, 1, 2, 2]},
            {"id": "controls_overlay", "label": "CTRL IND", "type": "key", "key": "controls_overlay", "grid": [3, 1, 1, 1]},
            {"id": "{seat}_CYCLIC_SYMBOLOGY", "label": "SYMBOLOGY", "type": "hat", "ud": "{seat}_CYCLIC_SYMBOLOGY", "hold": 0.3, "positions": {"up": "T/C", "down": "H/B"}, "grid": [1, 4, 2, 1]},
            {"id": "monocle", "label": "MONOCLE", "type": "key", "key": "monocle", "grid": [1, 5, 1, 1]},
            {"id": "PLT_T_WHEEL_UNLOCK_BTN", "label": "TAIL WHEEL", "type": "button", "hold": 0.3, "lamp": "PLT_T_WHEEL_UNLOCK_L", "legend": "UNLOCK", "seats": [0], "grid": [2, 5, 1, 1]},
            {"id": "flight_power_left", "label": "PWR LVR 1", "type": "lever", "readback": "{seat}_ENG_L_PW_LVR", "side": "left", "positions": POWER_POSITIONS, "grid": [1, 6, 3, 1]},
            {"id": "flight_power_right", "label": "PWR LVR 2", "type": "lever", "readback": "{seat}_ENG_R_PW_LVR", "side": "right", "positions": POWER_POSITIONS, "grid": [1, 7, 3, 1]},
        ],
    },
    {
        "name": "Fight",
        "seats": [0, 1],
        "lamps": [
            {"id": "{seat}_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "{seat}_INTL_MWARN_BTN"},
            {"id": "{seat}_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "{seat}_INTL_MCAUTION_BTN"},
            {"id": "{seat}_MASTER_ARM_ARM_L", "label": "ARM", "color": "amber"},
            {"id": "{seat}_MASTER_ARM_SAFE_L", "label": "SAFE", "color": "green"},
            {"id": "{seat}_GROUND_OVERRIDE_L", "label": "GND ORIDE", "color": "amber"},
        ],
        "controls": [
            {"id": "{seat}_MASTER_ARM_BTN", "label": "A/S", "type": "button", "hold": 0.3, "grid": [1, 1, 1, 1]},
            {"id": "{seat}_GROUND_OVERRIDE_BTN", "label": "GND ORIDE", "type": "button", "hold": 0.3, "grid": [1, 2, 1, 1]},
            {"id": "{seat}_WAS", "label": "WAS", "type": "hat", "ud": "{seat}_CYCLIC_WEAPON_UD", "lr": "{seat}_CYCLIC_WEAPON_LR", "hold": 0.3, "positions": {"up": "G", "down": "A", "left": "R", "right": "M"}, "grid": [1, 3, 1, 2]},
            {"id": "{seat}_SIGHT_SEL", "label": "SIGHT SEL", "type": "hat", "ud": "{seat}_COLLECTIVE_SIGHT_SELECT_UD", "lr": "{seat}_COLLECTIVE_SIGHT_SELECT_LR", "hold": 0.3, "positions": {"up": "HMD", "down": "LINK", "left": "FCR", "right": "TADS"}, "grid": [2, 3, 1, 2]},
            {"id": "{seat}_CYCLIC_FLARE", "label": "FLARE", "type": "button", "hold": 0.3, "grid": [2, 1, 1, 1]},
            {"id": "{seat}_CYCLIC_CHAFF", "label": "CHAFF", "type": "button", "hold": 0.3, "grid": [2, 2, 1, 1]},
            {"id": "PLT_CMWS_FLARE_COUNT", "label": "FLARE COUNT", "type": "display", "grid": [3, 1, 1, 1]},
            {"id": "PLT_CMWS_CHAFF_COUNT", "label": "CHAFF COUNT", "type": "display", "grid": [3, 2, 1, 1]},
            {"id": "PLT_CMWS_PW", "label": "CMWS PWR", "type": "selector", "rest": 1, "hold": 0.5, "positions": [{"value": 2, "label": "TEST", "momentary": True}, {"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}], "seats": [0], "grid": [1, 5, 1, 1]},
            {"id": "PLT_CMWS_ARM", "label": "FLARE SQUIBS", "type": "selector", "positions": [{"value": 1, "label": "ARM"}, {"value": 0, "label": "SAFE"}], "seats": [0], "grid": [1, 6, 1, 1]},
            {"id": "PLT_CMWS_MODE", "label": "CMWS MODE", "type": "selector", "positions": [{"value": 1, "label": "CMWS"}, {"value": 0, "label": "NAV"}], "seats": [0], "grid": [2, 5, 1, 1]},
            {"id": "PLT_CMWS_BYPASS", "label": "CMWS OPER", "type": "selector", "positions": [{"value": 1, "label": "BYPASS"}, {"value": 0, "label": "AUTO"}], "seats": [0], "grid": [2, 6, 1, 1]},
        ],
    },
    {"name": "MPD", "seats": [0, 1], "layout": "mpd", "lamps": [], "controls": mpd_controls("L") + mpd_controls("R") + cursor_controls() + tedac_controls()},
    {"name": "KU", "seats": [0, 1], "layout": "ku", "lamps": [], "controls": ku_controls()},
]

CONTROL_NAMES = [f"{seat}_{axis}" for seat in ("plt", "cpg") for axis in ("cyc_pitch", "cyc_roll", "coll", "pedals")]

MPD_INDICATIONS = (7, 9, 11, 13)
MPD_SEATS = {0: (7, 9), 1: (11, 13)}

TRIM_RELEASED = 2

SEAT_NAMES = {0: "PLT", 1: "CPG"}
