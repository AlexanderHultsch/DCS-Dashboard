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


def lever(name: str, label: str, side: str, marks: list, at: list, handle: list) -> dict:
    return {
        "id": name, "label": label, "type": "lever", "readback": f"{{seat}}_ENG_{side[0].upper()}_PW_LVR", "side": side,
        "positions": [{**p, "y": y} for p, y in zip(POWER_POSITIONS, marks)], "handle": handle, "at": at,
    }


def power_pages() -> list[dict]:
    pilot_levers = [628, 497, 188, 128]
    cpg_levers = [214, 166, 43, 20]
    controls = [
        {"id": "PLT_ROTOR_BRK", "label": "RTR BRK", "type": "selector", "positions": [{"value": 2, "label": "OFF", "y": 99}, {"value": 1, "label": "BRK", "disabled": True, "y": 128}, {"value": 0, "label": "LOCK", "y": 160}], "at": [128, 60, 64, 136]},
        {
            "id": "PLT_MASTER_IGN_SW", "label": "MSTR IGN", "type": "selector", "style": "rotary", "knob": [160, 274, 72],
            "positions": [{"value": 0, "label": "OFF", "angle": 66, "y": 235}, {"value": 1, "label": "BATT", "angle": 90, "y": 272}, {"value": 2, "label": "EXT PWR", "disabled": True, "angle": 118, "y": 345}],
            "at": [70, 196, 235, 160],
        },
        {"id": "PLT_APU_BTN", "label": "APU", "type": "button", "hold": 0.3, "requires": {"id": "PLT_APU_BTN_CVR", "value": 1}, "lamp": "PLT_APU_L", "legend": "ON", "color": "green", "at": [132, 438, 50, 66]},
        {"id": "PLT_APU_BTN_CVR", "label": "APU COVER", "type": "selector", "style": "cover", "positions": [{"value": 0, "label": "CLOSED"}, {"value": 1, "label": "OPEN"}], "at": [104, 405, 119, 128]},
        {"id": "PLT_ENG1_START", "label": "ENG 1 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS, "at": [60, 535, 64, 150]},
        {"id": "PLT_ENG2_START", "label": "ENG 2 START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS, "at": [186, 535, 64, 150]},
        lever("power_left", "PWR LVR NO 1", "left", pilot_levers, [300, 98, 87, 596], [358, 54, 40]),
        lever("power_right", "PWR LVR NO 2", "right", pilot_levers, [387, 98, 160, 596], [424, 54, 40]),
        {"id": "PLT_PW_LVR_FRIC", "label": "FRICT", "type": "knob", "style": "slider", "step": KNOB_STEP, "at": [425, 235, 115, 260]},
    ]
    placard = [
        ["POWER", 397, 40, 30, 100], ["RTR BRK", 164, 70, 24, 105],
        ["OFF", 224, 99, 19, 36], ["BRK", 228, 128, 19, 38], ["LOCK", 237, 160, 19, 52],
        ["MSTR IGN", 157, 184, 26, 117],
        ["OFF", 262, 229, 19, 36], ["BATT", 279, 272, 19, 48], ["EXT", 254, 316, 19, 33], ["PWR", 254, 336, 19, 38], ["+", 231, 363, 16],
        ["APU", 162, 390, 26, 50],
        ["ENG START", 157, 548, 26, 146], ["START", 158, 568, 17, 62], ["OFF", 155, 607, 19, 37], ["IGN ORIDE", 158, 660, 17, 94],
        ["NO 1", 84, 691, 20, 52], ["NO 2", 210, 691, 20, 56],
        ["LOCK", 509, 122, 19, 50], ["OUT", 505, 139, 19, 38], ["FLY", 497, 188, 19, 36], ["IDLE", 495, 497, 19, 44], ["OFF", 487, 628, 19, 33],
        ["NO 1", 358, 694, 20, 52], ["NO 2", 423, 694, 20, 58],
        ["INC", 556, 236, 18, 36], ["F", 553, 318, 20], ["R", 553, 341, 20], ["I", 553, 364, 20], ["C", 553, 388, 20], ["T", 553, 411, 20], ["DECR", 560, 489, 19, 56],
    ]
    art = [
        {"shape": "plate", "at": [4, 4, 612, 706]},
        {"shape": "screw", "at": [45, 60, 18]}, {"shape": "screw", "at": [603, 68, 17]}, {"shape": "screw", "at": [539, 70, 11]},
        {"shape": "screw", "at": [73, 158, 11]}, {"shape": "screw", "at": [36, 337, 19]}, {"shape": "screw", "at": [601, 348, 17]},
        {"shape": "screw", "at": [62, 541, 11]}, {"shape": "screw", "at": [25, 648, 17]}, {"shape": "screw", "at": [595, 655, 17]},
        {"shape": "screw", "at": [520, 658, 11]},
        {"shape": "slot", "at": [327, 80, 131, 598]}, {"shape": "slot", "at": [105, 407, 118, 125]},
        *[{"shape": "line", "at": [310, y, 16, 0]} for y in (128, 187, 495, 625)],
        *[{"shape": "line", "at": [458, y, 12, 0]} for y in (128, 188, 497, 628)],
        {"shape": "arrow", "at": [545, 250, 16, 52], "up": True}, {"shape": "arrow", "at": [545, 420, 16, 52]},
    ]
    cpg_controls = [
        lever("power_left", "PWR LVR NO 1", "left", cpg_levers, [96, 4, 35, 243], [122, 18, 14]),
        lever("power_right", "PWR LVR NO 2", "right", cpg_levers, [131, 4, 49, 243], [140, 18, 14]),
    ]
    cpg_placard = [
        ["LOCK", 76, 20, 8, 15], ["FLY", 75, 43, 8, 11], ["IDLE", 76, 165, 8, 14],
        ["LOCK", 167, 20, 8, 15], ["OUT", 167, 29, 8, 12], ["FLY", 166, 44, 8, 11], ["IDLE", 166, 166, 8, 14], ["OFF", 166, 214, 8, 12],
        ["NO. 1", 111, 242, 7, 16], ["NO. 2", 145, 242, 7, 16],
    ]
    cpg_art = [
        {"shape": "plate", "at": [1, 2, 224, 246]},
        {"shape": "screw", "at": [213, 6, 8]}, {"shape": "screw", "at": [213, 106, 8]}, {"shape": "screw", "at": [213, 228, 8]},
        {"shape": "slot", "at": [112, 10, 38, 230]},
        *[{"shape": "line", "at": [102, y, 8, 0]} for y in (43, 166, 214)],
        *[{"shape": "line", "at": [150, y, 8, 0]} for y in (20, 43, 166, 214)],
    ]
    return (
        panel_pages("POWER", {0: [4, 1, 2, 3]}, [621, 712], placard, art, controls)
        + panel_pages("POWER", {1: [3, 1, 2, 3]}, [226, 250], cpg_placard, cpg_art, cpg_controls)
    )


def intr_lt_controls(spots: dict) -> list[dict]:
    controls = [
        {"id": f"{{seat}}_INTL_{name}_L_KNB", "label": name, "type": "knob", "step": KNOB_STEP, "sweep": sweep, "at": spots[name]}
        for name, sweep in (("SIGNAL", [-129, 124]), ("PRIMARY", [-125, 125]), ("FLOOD", [-125, 125]))
    ]
    controls.append({"id": "{seat}_INTL_TEST_BTN", "label": "PRESS TO TEST", "type": "button", "shape": "round", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_INTL_TEST_BTN", "color": "amber", "at": spots["TEST"]})
    return controls


def light_pages() -> list[dict]:
    controls = [
        {"id": "PLT_EXTL_NAV_L_SW", "label": "NAV", "type": "selector", "positions": [{"value": 2, "label": "BRT", "y": 57}, {"value": 1, "label": "OFF", "y": 102}, {"value": 0, "label": "DIM", "y": 147}], "at": [85, 34, 73, 136]},
        {"id": "PLT_EXTL_FROMATION_L_KNB", "label": "FORM", "type": "knob", "step": KNOB_STEP, "sweep": [-125, 125], "at": [90, 210, 100, 100]},
        {"id": "PLT_EXTL_ACOL_L_SW", "label": "ANTI COL", "type": "selector", "positions": [{"value": 2, "label": "WHT", "y": 340}, {"value": 1, "label": "OFF", "y": 385}, {"value": 0, "label": "RED", "y": 430}], "at": [122, 317, 73, 136]},
        {"id": "PLT_INTL_STBYINST_L_KNB", "label": "STBY INST", "type": "knob", "step": KNOB_STEP, "sweep": [-125, 125], "at": [459, 262, 92, 92]},
        *intr_lt_controls({"SIGNAL": [254, 92, 92, 92], "PRIMARY": [446, 93, 92, 92], "FLOOD": [274, 258, 92, 92], "TEST": [388, 377, 68, 68]}),
    ]
    placard = [
        ["EXT LT", 111, 37, 26, 102], ["INTR LT", 402, 35, 26, 118],
        ["BRT", 115, 59, 18, 35], ["OFF", 60, 104, 18, 35], ["DIM", 125, 149, 18, 32],
        ["N", 179, 83, 20], ["A", 182, 102, 20], ["V", 182, 122, 20],
        ["FORM", 133, 192, 22, 66], ["OFF", 88, 303, 17, 30], ["BRT", 200, 304, 17, 37],
        ["WHT", 151, 342, 17, 38], ["OFF", 98, 379, 18, 35], ["RED", 163, 426, 18, 35],
        ["A", 206, 355, 20], ["N", 208, 373, 20], ["T", 210, 391, 20], ["I", 213, 409, 20],
        ["C", 238, 368, 20], ["O", 240, 385, 20], ["L", 243, 404, 20],
        ["SIGNAL", 293, 67, 22, 90], ["DIM", 255, 176, 17, 36], ["RST", 359, 178, 17, 37], ["BRT", 380, 158, 17, 40],
        ["PRIMARY", 487, 66, 22, 116], ["OFF", 437, 178, 17, 28], ["BRT", 554, 179, 17, 38],
        ["FLOOD", 313, 238, 22, 83], ["OFF", 266, 343, 17, 30], ["BRT", 376, 343, 17, 38],
        ["+", 403, 255, 16], ["STBY INST", 502, 240, 22, 131], ["OFF", 452, 347, 17, 28], ["BRT", 565, 347, 17, 38],
        ["PRESS", 352, 389, 19, 64], ["TO", 355, 404, 19, 22], ["TEST", 355, 418, 19, 49],
    ]
    art = [
        {"shape": "plate", "at": [26, 4, 566, 449]},
        {"shape": "bracket", "at": [0, 36, 46, 62]}, {"shape": "bracket", "at": [558, 20, 61, 70]},
        {"shape": "bracket", "at": [570, 390, 49, 66]}, {"shape": "bracket", "at": [34, 380, 52, 56]},
        {"shape": "screw", "at": [12, 62, 16]}, {"shape": "screw", "at": [577, 57, 18]},
        {"shape": "screw", "at": [598, 421, 17]}, {"shape": "screw", "at": [58, 405, 17]},
        {"shape": "screw", "at": [55, 140, 9]}, {"shape": "screw", "at": [87, 345, 9]},
        {"shape": "screw", "at": [547, 373, 9]}, {"shape": "screw", "at": [535, 209, 10]},
        {"shape": "line", "at": [203, 68, 33, 272]},
    ]
    cpg_placard = [
        ["INTR LT", 99, 19.5, 9.5, 45], ["SIGNAL", 57, 32, 8, 36], ["PRIMARY", 145, 32, 8, 45], ["FLOOD", 57, 97, 8, 33],
        ["DIM", 35, 79.5, 6.5, 15], ["RST", 77, 78.5, 6.5, 16], ["BRT", 84, 68.5, 6.5, 16],
        ["OFF", 123, 79.5, 6.5, 14], ["BRT", 165, 79.5, 6.5, 17], ["OFF", 33, 148.5, 6.5, 14], ["BRT", 76, 148.5, 6.5, 16],
        ["PRESS", 127, 116, 7, 27], ["TO", 127, 122.5, 7, 9], ["TEST", 127, 129, 7, 21],
    ]
    cpg_art = [
        {"shape": "plate", "at": [4, 4, 200, 166]},
        {"shape": "screw", "at": [5, 49, 4.5]}, {"shape": "screw", "at": [192, 49, 4.5]},
        {"shape": "screw", "at": [4, 122, 4.5]}, {"shape": "screw", "at": [191, 123, 4.5]},
    ]
    cpg_controls = intr_lt_controls({"SIGNAL": [35, 42, 40, 40], "PRIMARY": [123, 42, 40, 40], "FLOOD": [35, 111, 40, 40], "TEST": [140, 109, 28, 28]})
    return (
        panel_pages("EXT / INTR LT", {0: [7, 1, 1, 3]}, [619, 457], placard, art, controls)
        + panel_pages("INTR LT", {1: [6, 1, 1, 3]}, [208, 174], cpg_placard, cpg_art, cpg_controls)
    )


def fire_button(label: str, name: str, lamp: str, at: list) -> dict:
    return {
        "id": f"{{seat}}_FIRE_{name}_BTN", "label": label, "type": "button", "guard": True, "hold": MPD_BUTTON_HOLD,
        "lamps": [
            {"id": f"{{seat}}_{lamp}_FIRE_L", "color": "amber", "legend": "FIRE"},
            {"id": f"{{seat}}_{lamp}_READY_L", "color": "green", "legend": "RDY"},
        ],
        "at": at,
    }


def fire_pages() -> list[dict]:
    controls = [
        fire_button("ENG 1", "ENG1", "ENG_1", [55, 52, 35, 40]),
        fire_button("APU", "APU", "APU", [138, 52, 35, 40]),
        fire_button("ENG 2", "ENG2", "ENG_2", [221, 52, 35, 40]),
        {"id": "{seat}_FIRE_PRIME_EXT", "label": "PRI", "type": "button", "guard": True, "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_FIRE_EXT_DISCH_PRI_L", "legend": "DISCH", "color": "amber", "at": [66, 117, 38, 38]},
        {"id": "{seat}_FIRE_RES_EXT", "label": "RES", "type": "button", "guard": True, "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_FIRE_EXT_DISCH_RES_L", "legend": "DISCH", "color": "amber", "at": [211, 117, 38, 38]},
        {
            "id": "{seat}_FIRE_DETECT_TEST", "label": "TEST", "type": "selector", "orient": "h", "rest": 1, "hold": 0.5,
            "positions": [{"value": 0, "label": "1", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "2", "momentary": True}],
            "at": [124, 118, 65, 37],
        },
    ]
    placard = [
        ["ENG 1", 70.5, 27, 11, 31], ["APU", 153.5, 27, 11, 21], ["ENG 2", 237.5, 27, 11, 33],
        ["+", 113, 74, 8], ["PRI", 83, 106, 11, 17], ["TEST", 156, 113, 11, 26], ["RES", 228.5, 106.5, 11, 21],
        ["1", 129, 136, 7], ["2", 183, 136, 7], ["FIRE DET/EXTG", 157, 168.5, 13, 108],
    ]
    art = [
        {"shape": "plate", "at": [2, 2, 315, 177]},
        {"shape": "slot", "at": [45, 41, 55, 59]}, {"shape": "slot", "at": [129, 41, 54, 59]}, {"shape": "slot", "at": [212, 41, 53, 59]},
        {"shape": "hazard", "at": [37, 50, 8, 47], "period": 17}, {"shape": "hazard", "at": [101, 50, 26, 47], "period": 17},
        {"shape": "hazard", "at": [185, 50, 26, 47], "period": 17}, {"shape": "hazard", "at": [268, 50, 10, 47], "period": 17},
        {"shape": "outline", "at": [61, 113, 47, 45]}, {"shape": "outline", "at": [205, 113, 49, 45]},
    ]
    return panel_pages("FIRE DET/EXTG", {0: [1, 4, 1, 3], 1: [1, 4, 1, 2]}, [319, 181], placard, art, controls)


def jettison_pages() -> list[dict]:
    stations = [
        ("L OUTBD", "LO", "L_OUTBOARD", [121, 70, 81, 83]), ("L INBD", "LI", "L_INBOARD", [219, 70, 81, 83]),
        ("R INBD", "RI", "R_INBOARD", [317, 70, 81, 83]), ("R OUTBD", "RO", "R_OUTBOARD", [414, 70, 81, 83]),
        ("L TIP", "LW", "L_TIP", [70, 209, 85, 83]), ("R TIP", "RW", "R_TIP", [450, 209, 85, 83]),
    ]
    controls = [
        {"id": f"{{seat}}_JETT_STORE_{name}", "label": label, "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": f"{{seat}}_JETT_{lamp}_L", "color": "amber", "at": at}
        for label, name, lamp, at in stations
    ]
    controls.append({"id": "{seat}_JETT_BTN", "label": "JETT", "type": "button", "shape": "round", "style": "plunger", "guard": True, "hold": MPD_BUTTON_HOLD, "at": [237, 208, 124, 124]})
    placard = [
        ["STORES JETTISON", 307, 24, 28, 274], ["L OUTBD", 151, 53.5, 24, 90], ["L INBD", 258.5, 53, 23, 73],
        ["R INBD", 357.5, 52.5, 24, 75], ["R OUTBD", 465, 52.5, 24, 92], ["L TIP", 113.5, 192, 24, 63], ["R TIP", 489.5, 191.5, 24, 65],
        ["JETT", 397, 265, 24, 56],
    ]
    art = [
        {"shape": "plate", "at": [3, 2, 615, 355]},
        {"shape": "bracket", "at": [8, 2, 44, 82]}, {"shape": "bracket", "at": [570, 2, 45, 80]},
        {"shape": "bracket", "at": [3, 276, 52, 80]}, {"shape": "bracket", "at": [566, 276, 52, 80]},
        {"shape": "screw", "at": [24, 59, 17]}, {"shape": "screw", "at": [594, 59, 17]},
        {"shape": "screw", "at": [22, 298, 17]}, {"shape": "screw", "at": [592, 298, 17]},
        {"shape": "screw", "at": [66, 115, 14]}, {"shape": "screw", "at": [546, 115, 14]},
        {"shape": "screw", "at": [108, 332, 14]}, {"shape": "screw", "at": [500, 331, 14]},
        {"shape": "hazard", "at": [185, 198, 242, 136]},
        {"shape": "slot", "at": [367, 252, 62, 26]},
    ]
    return panel_pages("STORES JETT", {0: [6, 1, 1, 3], 1: [7, 1, 1, 3]}, [621, 370], placard, art, controls)


def video_knob(name: str, label: str, at: list, group: str | None = None, mark: list | None = None, dot: list | None = None) -> dict:
    knob = {"id": f"PLT_VIDEO_{name}", "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-130, 130], "at": at}
    if group:
        knob.update({"group": group, "mark": mark, "dot": dot})
    return knob


def armament_pages() -> list[dict]:
    controls = [
        {
            "id": "{seat}_MASTER_ARM_BTN", "label": "A/S", "type": "button", "hold": MPD_BUTTON_HOLD,
            "lamps": [
                {"id": "{seat}_MASTER_ARM_ARM_L", "color": "amber", "legend": "ARM"},
                {"id": "{seat}_MASTER_ARM_SAFE_L", "color": "green", "legend": "SAFE"},
            ],
            "at": [81, 63, 60, 60],
        },
        {"id": "{seat}_GROUND_OVERRIDE_BTN", "label": "GND ORIDE", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_GROUND_OVERRIDE_L", "color": "amber", "at": [175.5, 63, 60, 60]},
        {"id": "{seat}_INST_MZERO_SW", "label": "MASTER ZEROIZE", "type": "selector", "guard": True, "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}], "at": [376, 74, 60, 76]},
    ]
    placard = [
        ["ARMAMENT", 156.4, 25.5, 20, 111], ["A/S", 111.5, 53, 16, 34], ["GND ORIDE", 203, 53.2, 16, 91], ["+", 158.7, 130.5, 11],
        ["MASTER", 406, 30, 16, 64], ["ZEROIZE", 406, 50, 16, 76], ["ON", 459, 96, 12, 18], ["OFF", 460, 128, 12, 26],
    ]
    art = [
        {"shape": "plate", "at": [10, 2, 302, 162]}, {"shape": "plate", "at": [331, 2, 150, 163]},
        {"shape": "screw", "at": [32, 30, 9]}, {"shape": "screw", "at": [284, 31, 9]},
        {"shape": "screw", "at": [66, 89, 8]}, {"shape": "screw", "at": [251, 89, 8]},
        {"shape": "screw", "at": [34, 140, 9]}, {"shape": "screw", "at": [284, 140, 9]},
        {"shape": "screw", "at": [345, 152, 6]}, {"shape": "screw", "at": [467, 152, 6]},
        {"shape": "line", "at": [77.5, 63, 0, 63]}, {"shape": "line", "at": [77.5, 126, 67, 0]}, {"shape": "line", "at": [144.5, 63, 0, 63]},
        {"shape": "line", "at": [172, 63, 0, 63]}, {"shape": "line", "at": [172, 126, 66, 0]}, {"shape": "line", "at": [238, 63, 0, 63]},
    ]
    video_controls = [
        video_knob("IHADSS_BRT", "IHADSS BRT", [65, 212, 60, 60], "IHADSS", [24, 213, 38, 36], [57.2, 242.5, 10]),
        video_knob("IHADSS_CON", "IHADSS CON", [65, 212, 60, 60], "IHADSS", [24, 249, 38, 36], [57.2, 255.5, 10]),
        video_knob("SYM_BRT", "SYM BRT", [237.5, 223, 44, 44]),
        {"id": "PLT_VIDEO_AUTO_CON", "label": "ACM", "type": "selector", "style": "cap", "positions": [{"value": 0, "label": "OFF"}, {"value": 1, "label": "ACM"}], "at": [132.5, 307.5, 47, 47]},
        video_knob("FLIR_LVL", "FLIR LVL", [228.5, 315.5, 60, 60], "FLIR", [185.2, 313, 38, 35], [221.2, 344, 10]),
        video_knob("FLIR_GAIN", "FLIR GAIN", [228.5, 315.5, 60, 60], "FLIR", [185.2, 348, 38, 36], [221.2, 356.3, 10]),
    ]
    video_placard = [
        ["VIDEO", 160, 184.5, 18, 55], ["IHADSS", 111.3, 204.7, 16.5, 58], ["BRT", 35, 243.3, 11, 21], ["CON", 36.6, 255.7, 11, 24],
        ["MIN", 68.5, 273, 11.5, 20.5], ["MAX", 122.4, 273, 11.5, 25], ["+", 155.3, 265.5, 11],
        ["SYM BRT", 263.5, 210.8, 16, 69], ["MIN", 239.6, 268.8, 11.5, 20], ["MAX", 279.7, 268.3, 11.5, 24],
        ["ACM", 154.3, 301, 16, 34], ["FLIR", 259, 301, 16, 34], ["LVL", 201.5, 344.5, 11, 20], ["GAIN", 200.2, 356.4, 11, 27],
        ["MIN", 232, 374, 11.5, 20], ["MAX", 285, 374, 11.5, 24],
    ]
    video_art = [
        {"shape": "plate", "at": [12, 168, 300, 213]},
        {"shape": "screw", "at": [64, 187, 8]}, {"shape": "screw", "at": [249, 187, 8]},
        {"shape": "screw", "at": [60, 292, 8]}, {"shape": "screw", "at": [292, 291, 8]},
    ]
    return (
        panel_pages("ARMAMENT", {0: [2, 4, 1, 3]}, [481, 384], placard + video_placard, art + video_art, controls + video_controls)
        + panel_pages("ARMAMENT", {1: [1, 6, 1, 2]}, [481, 168], placard, art, controls)
    )


def eufd_rocker(name: str, at: list) -> dict:
    return {"id": f"{{seat}}_EUFD_{name}", "label": name, "type": "hat", "ud": f"{{seat}}_EUFD_{name}", "hold": MPD_BUTTON_HOLD, "positions": {"up": "▲", "down": "▼"}, "at": at}


def eufd_button(name: str, label: str, at: list) -> dict:
    return {"id": f"{{seat}}_EUFD_{name}", "label": label, "type": "button", "style": "flat", "hold": MPD_BUTTON_HOLD, "at": at}


def eufd_pages() -> list[dict]:
    controls = [
        {"id": "{seat}_EUFD_DISPLAY", "label": "EUFD", "type": "display", "ids": [f"{{seat}}_EUFD_LINE{n}" for n in range(1, 15)], "at": [104, 14.5, 325, 169.5]},
        eufd_rocker("WCA", [61, 27, 18.5, 63]),
        eufd_rocker("IDM", [15, 71.5, 19, 63]),
        eufd_rocker("RTS", [63, 114.5, 19, 63]),
        {"id": "{seat}_EUFD_BRT", "label": "BRT", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135], "at": [455, 45, 47, 47]},
        eufd_button("PRESET", "P", [451.5, 116.5, 19.5, 20]),
        eufd_button("ENT", "ENTER", [501, 116.5, 22, 20.5]),
        eufd_button("STOPWATCH", "STOPWATCH", [451, 168, 20, 18.5]),
        eufd_button("SWAP", "SWAP", [501, 168, 20.5, 18.5]),
    ]
    placard = [
        ["WCA", 70, 58.5, 13.5, 16.5], ["IDM", 24.5, 103, 13.5, 15], ["RTS", 72, 146, 13.5, 17],
        ["BRT", 475, 42, 10, 17], ["P", 462.5, 127.8, 16.5, 7.5],
    ]
    art = [
        {"shape": "plate", "at": [2, 2, 552, 193]},
        {"shape": "slot", "at": [100, 13, 332, 173]},
        {"shape": "bracket", "at": [61, 32, 18.5, 53]}, {"shape": "bracket", "at": [15, 76.5, 19, 53]}, {"shape": "bracket", "at": [63, 119.5, 19, 53]},
        {"shape": "bracket", "at": [451.5, 116.5, 19.5, 20]}, {"shape": "bracket", "at": [501, 116.5, 22, 20.5]},
        {"shape": "bracket", "at": [451, 168, 20, 18.5]}, {"shape": "bracket", "at": [501, 168, 20.5, 18.5]},
        {"shape": "path", "at": [504.5, 124, 16, 8], "d": "M15 0V4.2H4", "width": 1.6},
        {"shape": "path", "at": [504.5, 124, 16, 8], "d": "M5.5 1.2L1 4.2L5.5 7.2Z", "width": 1, "fill": True},
        {"shape": "path", "at": [455, 169.5, 12.4, 16.2], "d": "M0.4 10a5.8 5.8 0 1 0 11.6 0a5.8 5.8 0 1 0-11.6 0M3.4 0.5H9M6.2 0.5V4.2M6.2 10L4.3 12.6", "width": 1.6},
        {"shape": "path", "at": [503.5, 170.3, 14, 14], "d": "M0.9 5.9A6.2 6.2 0 0 1 11.75 3M13.1 8.1A6.2 6.2 0 0 1 2.25 11", "width": 1.6},
        {"shape": "path", "at": [503.5, 170.3, 14, 14], "d": "M12.5 3.9L12.9 1L9.5 3.8ZM1.5 10.1L1.1 13L4.45 10.2Z", "width": 0.8, "fill": True},
    ]
    return panel_pages("EUFD", {0: [1, 7, 1, 3], 1: [1, 8, 1, 3]}, [556, 197], placard, art, controls)


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
    *power_pages(),
    *light_pages(),
    *fire_pages(),
    *jettison_pages(),
    *armament_pages(),
    *eufd_pages(),
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
