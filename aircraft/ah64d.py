import math

from aircraft.panel_kit import REF, Panel, PanelGroup

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
        {"id": f"CPG_TEDAC_{name}", "label": label, "type": "hat", "ud": f"CPG_TEDAC_{name}", "hold": MPD_BUTTON_HOLD, "positions": {"up": "tri-up", "down": "tri-down"}, "side": "T", "seats": [1], "slot": name}
        for name, label in (("RF", "R/F"), ("EL", "EL"), ("SYM", "SYM"), ("BRT", "BRT"), ("CON", "CON"))
    ]
    controls.append({"id": "CPG_TEDAC_AZ", "label": "AZ", "type": "hat", "lr": "CPG_TEDAC_AZ", "hold": MPD_BUTTON_HOLD, "positions": {"left": "tri-left", "right": "tri-right"}, "side": "T", "seats": [1], "slot": "AZ"})
    return controls


MASTER_LAMPS = [
    {"id": "{seat}_MASTER_WARNING_L", "label": "MASTER WARNING", "color": "red", "button": "{seat}_INTL_MWARN_BTN"},
    {"id": "{seat}_MASTER_CAUTION_L", "label": "MASTER CAUTION", "color": "amber", "button": "{seat}_INTL_MCAUTION_BTN"},
]


def panel_pages(name: str, cells: dict, box: list, placard: list, art: list, controls: list, indicators: list | None = None, ref: tuple | None = None) -> list[dict]:
    return [
        {
            "name": name, "seats": [seat], "panel": True, "layout": "panel", "map": cell, "box": box,
            "lamps": MASTER_LAMPS, "print": placard, "art": art, "controls": controls,
            **({"indicators": indicators} if indicators else {}),
            **({"kit": True, "ref": list(ref)} if ref else {}),
        }
        for seat, cell in cells.items()
    ]


def kit_pages(name: str, cells: dict, panel: Panel) -> list[dict]:
    page = panel.build()
    return panel_pages(name, cells, page["box"], page["print"], page["art"], page["controls"], ref=REF)


def tail_wheel_pages() -> list[dict]:
    p = Panel("TAIL WHEEL / NVS", 600, 224)
    p.mark("+", "SMALL", 69, 64, "panel mark as on the photo")
    p.push("WHEEL", 177, 126, {"id": "{seat}_T_WHEEL_UNLOCK_BTN", "label": "TAIL WHEEL", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_T_WHEEL_UNLOCK_L", "legend": "UNLOCK", "color": "amber"}, frame=True)
    p.label("TAIL WHEEL", "TITLE", "WHEEL", "above")
    p.toggle("NVS", 460, 132, {"id": "{seat}_NVS_MODE", "label": "NVS MODE", "type": "selector", "positions": [{"value": 2, "label": "FIXED"}, {"value": 1, "label": "NORM"}, {"value": 0, "label": "OFF"}]}, "above_side_below")
    p.label("NVS MODE", "TITLE", "NVS", "above")
    return kit_pages("TAIL WHEEL / NVS", {0: [2, 1, 1, 3], 1: [5, 1, 1, 3]}, p)


def emergency_pages() -> list[dict]:
    p = Panel("EMERGENCY", 580, 276)
    p.mark("EMERGENCY", "TITLE", "CX", 52, "panel title")
    p.mark("+", "SMALL", 86, 68, "panel mark as on the photo")
    p.push("GUARD", 114, 166,{"id": "{seat}_EMERG_GUARD_BTN", "label": "GUARD", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_EMERG_GUARD_L", "color": "green"}, frame=True)
    p.label("GUARD", "NAME", "GUARD", "above")
    p.push("XPNDR", 230, 166,{"id": "{seat}_EMERG_XPNDR_BTN", "label": "XPNDR", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_EMERG_XPNDR_L", "color": "green"}, frame=True)
    p.label("XPNDR", "NAME", "XPNDR", "above")
    p.toggle("ZEROIZE", 336, 156,{"id": "{seat}_EMERG_ZERO_SW", "label": "ZEROIZE", "type": "selector", "guard": True, "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}]})
    p.label("ZEROIZE", "NAME", "ZEROIZE", "above")
    p.push("HYD", 454, 178,{"id": "{seat}_EMERG_HYD_BTN", "label": "EMERG HYD", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_EMERG_HYD_L", "color": "green"})
    p.hazard("HYD")
    p.label("EMERG\nHYD", "NAME", "HYD", "above")
    return kit_pages("EMERGENCY", {0: [3, 1, 1, 3], 1: [2, 1, 1, 3]}, p)


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


def intr_lt_knob(p: Panel, name: str, sweep: list, cx: int, cy: int, preset: str, marks: tuple):
    p.knob(name, "KNOB_M", cx, cy, {"id": f"{{seat}}_INTL_{name}_L_KNB", "label": name, "type": "knob", "step": KNOB_STEP, "sweep": sweep})
    p.label(name, "NAME", name, "above")
    p.knob_labels(name, preset, *marks)


def intr_lt_test(p: Panel, cx: int, cy: int):
    p.round("TEST", cx, cy, {"id": "{seat}_INTL_TEST_BTN", "label": "PRESS TO TEST", "type": "button", "shape": "round", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_INTL_TEST_BTN", "color": "amber"})
    p.label("PRESS TO\nTEST", "NAME", "TEST", "left")


def light_pages() -> list[dict]:
    p = Panel("EXT / INTR LT", 612, 456)
    p.mark("EXT LT", "TITLE", 124, 52, "panel title")
    p.mark("INTR LT", "TITLE", 410, 52, "panel title")
    p.rule("EXT / INTR divider", 224, 72, 420)
    p.toggle("NAV", 124, 132, {"id": "PLT_EXTL_NAV_L_SW", "label": "NAV", "type": "selector", "positions": [{"value": 2, "label": "BRT"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "DIM"}]}, "above_left_below")
    p.label("N\nA\nV", "POS", "NAV", "right")
    p.knob("FORM", "KNOB_M", 124, 264, {"id": "PLT_EXTL_FROMATION_L_KNB", "label": "FORM", "type": "knob", "step": KNOB_STEP, "sweep": [-125, 125]})
    p.label("FORM", "NAME", "FORM", "above")
    p.knob_labels("FORM", "lower_sides", "OFF", "BRT")
    p.toggle("ACOL", 124, 364, {"id": "PLT_EXTL_ACOL_L_SW", "label": "ANTI COL", "type": "selector", "positions": [{"value": 2, "label": "WHT"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "RED"}]}, "above_left_below")
    p.label("A\nN\nT\nI", "POS", "ACOL", "right")
    p.label("C\nO\nL", "POS", "ACOL", "right")
    p.knob("STBY INST", "KNOB_M", 496, 256, {"id": "PLT_INTL_STBYINST_L_KNB", "label": "STBY INST", "type": "knob", "step": KNOB_STEP, "sweep": [-125, 125]})
    p.label("STBY INST", "NAME", "STBY INST", "above")
    p.knob_labels("STBY INST", "lower_sides", "OFF", "BRT")
    intr_lt_knob(p, "SIGNAL", [-129, 124], 324, 144, "signal", ("DIM", "BRT", "RST"))
    intr_lt_knob(p, "PRIMARY", [-125, 125], 496, 144, "lower_sides", ("OFF", "BRT"))
    intr_lt_knob(p, "FLOOD", [-125, 125], 324, 256, "lower_sides", ("OFF", "BRT"))
    p.mark("+", "SMALL", 410, 252, "panel mark as on the photo")
    intr_lt_test(p, 440, 364)
    c = Panel("INTR LT", 428, 360)
    c.mark("INTR LT", "TITLE", "CX", 52, "panel title")
    intr_lt_knob(c, "SIGNAL", [-129, 124], 116, 144, "signal", ("DIM", "BRT", "RST"))
    intr_lt_knob(c, "PRIMARY", [-125, 125], 288, 144, "lower_sides", ("OFF", "BRT"))
    intr_lt_knob(c, "FLOOD", [-125, 125], 116, 256, "lower_sides", ("OFF", "BRT"))
    intr_lt_test(c, 360, 256)
    return kit_pages("EXT / INTR LT", {0: [7, 1, 1, 3]}, p) + kit_pages("INTR LT", {1: [6, 1, 1, 3]}, c)


def fire_button(label: str, name: str, lamp: str) -> dict:
    return {
        "id": f"{{seat}}_FIRE_{name}_BTN", "label": label, "type": "button", "guard": True, "cover": f"{{seat}}_FIRE_{name}_CVR", "hold": MPD_BUTTON_HOLD,
        "lamps": [
            {"id": f"{{seat}}_{lamp}_FIRE_L", "color": "amber", "legend": "FIRE"},
            {"id": f"{{seat}}_{lamp}_READY_L", "color": "green", "legend": "RDY"},
        ],
    }


def fire_pages() -> list[dict]:
    p = Panel("FIRE DET/EXTG", 600, 456)
    for label, name, lamp, x in (("ENG 1", "ENG1", "ENG_1", 136), ("APU", "APU", "APU", 300), ("ENG 2", "ENG2", "ENG_2", 464)):
        p.push(name, x, 134, fire_button(label, name, lamp))
        p.housing(name)
        p.label(label, "NAME", name, "above")
    p.strip("ENG1", "left")
    p.strip("ENG1", "right")
    p.strip("APU", "right")
    p.strip("ENG2", "right")
    for label, name, x in (("PRI", "PRIME", 168), ("RES", "RES", 432)):
        p.push(label, x, 310, {"id": f"{{seat}}_FIRE_{name}_EXT", "label": label, "type": "button", "guard": True, "hold": MPD_BUTTON_HOLD, "lamp": f"{{seat}}_FIRE_EXT_DISCH_{label}_L", "legend": "DISCH", "color": "amber"}, frame=True)
        p.label(label, "NAME", label, "above")
    p.toggle("TEST", 300, 310, {
        "id": "{seat}_FIRE_DETECT_TEST", "label": "TEST", "type": "selector", "orient": "h", "rest": 1, "hold": 0.5,
        "positions": [{"value": 0, "label": "1", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "2", "momentary": True}],
    }, "left_right")
    p.label("TEST", "NAME", "TEST", "above")
    p.mark("FIRE DET/EXTG", "TITLE", "CX", 404, "panel title")
    return kit_pages("FIRE DET/EXTG", {0: [1, 4, 1, 3], 1: [1, 4, 1, 2]}, p)


def jettison_pages() -> list[dict]:
    p = Panel("STORES JETT", 556, 408)
    p.mark("STORES JETTISON", "TITLE", "CX", 52, "panel title")
    stations = [
        ("L OUTBD", "LO", "L_OUTBOARD", 110, 150), ("L INBD", "LI", "L_INBOARD", 222, 150),
        ("R INBD", "RI", "R_INBOARD", 334, 150), ("R OUTBD", "RO", "R_OUTBOARD", 446, 150),
        ("L TIP", "LW", "L_TIP", 78, 290), ("R TIP", "RW", "R_TIP", 478, 290),
    ]
    for label, name, lamp, x, y in stations:
        p.push(name, x, y, {"id": f"{{seat}}_JETT_STORE_{name}", "label": label, "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": f"{{seat}}_JETT_{lamp}_L", "color": "amber"})
        p.label(label, "NAME", name, "above")
    p.plunger("JETT", 278, 290, {"id": "{seat}_JETT_BTN", "label": "JETT", "type": "button", "shape": "round", "style": "plunger", "guard": True, "hold": MPD_BUTTON_HOLD})
    p.hazard("JETT", "JETT")
    return kit_pages("STORES JETT", {0: [6, 1, 1, 3], 1: [7, 1, 1, 3]}, p)


def video_knob(name: str, label: str, group: str | None = None) -> dict:
    knob = {"id": f"PLT_VIDEO_{name}", "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-130, 130]}
    return {**knob, "group": group} if group else knob


def armament_plate(g: PanelGroup):
    p = g.panel("ARMAMENT", 352, 244, 0, 0)
    p.mark("ARMAMENT", "TITLE", "CX", 52, "panel title")
    p.push("AS", 114, 158, {
        "id": "{seat}_MASTER_ARM_BTN", "label": "A/S", "type": "button", "hold": MPD_BUTTON_HOLD,
        "lamps": [
            {"id": "{seat}_MASTER_ARM_ARM_L", "color": "amber", "legend": "ARM"},
            {"id": "{seat}_MASTER_ARM_SAFE_L", "color": "green", "legend": "SAFE"},
        ],
    }, frame=True)
    p.label("A/S", "NAME", "AS", "above")
    p.push("GND", 238, 158, {"id": "{seat}_GROUND_OVERRIDE_BTN", "label": "GND ORIDE", "type": "button", "hold": MPD_BUTTON_HOLD, "lamp": "{seat}_GROUND_OVERRIDE_L", "color": "amber"}, frame=True)
    p.label("GND ORIDE", "NAME", "GND", "above")
    p.mark("+", "SMALL", "CX", 198, "panel mark as on the photo")


def zeroize_plate(g: PanelGroup):
    p = g.panel("MASTER ZEROIZE", 240, 244, 368, 0)
    p.toggle("ZEROIZE", 120, 138, {
        "id": "{seat}_INST_MZERO_SW", "label": "MASTER ZEROIZE", "type": "selector", "guard": True, "cover": "{seat}_INST_MZERO_CVR",
        "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}],
    }, "right_pair")
    p.label("MASTER\nZEROIZE", "NAME", "ZEROIZE", "above")


def video_plate(g: PanelGroup):
    p = g.panel("VIDEO", 608, 340, 0, 260)
    p.mark("VIDEO", "TITLE", "CX", 52, "panel title")
    p.mark("+", "SMALL", 239, 138, "panel mark as on the photo")
    p.knob("IHADSS", "KNOB_L", 174, 116, [video_knob("IHADSS_BRT", "IHADSS BRT", "IHADSS"), video_knob("IHADSS_CON", "IHADSS CON", "IHADSS")], ("BRT", "CON"))
    p.label("IHADSS", "NAME", "IHADSS", "above")
    p.knob_labels("IHADSS", "below_sides", "MIN", "MAX")
    p.knob("SYM", "KNOB_M", 464, 104, video_knob("SYM_BRT", "SYM BRT"))
    p.label("SYM BRT", "NAME", "SYM", "above")
    p.knob_labels("SYM", "lower_sides", "MIN", "MAX")
    p.round("ACM", 284, 220, {"id": "PLT_VIDEO_AUTO_CON", "label": "ACM", "type": "selector", "style": "cap", "positions": [{"value": 0, "label": "OFF"}, {"value": 1, "label": "ACM"}]})
    p.label("ACM", "NAME", "ACM", "above")
    p.knob("FLIR", "KNOB_L", 464, 228, [video_knob("FLIR_LVL", "FLIR LVL", "FLIR"), video_knob("FLIR_GAIN", "FLIR GAIN", "FLIR")], ("LVL", "GAIN"))
    p.label("FLIR", "NAME", "FLIR", "above")
    p.knob_labels("FLIR", "below_sides", "MIN", "MAX")


def armament_pages() -> list[dict]:
    pilot = PanelGroup("ARMAMENT")
    armament_plate(pilot)
    zeroize_plate(pilot)
    video_plate(pilot)
    cpg = PanelGroup("ARMAMENT")
    armament_plate(cpg)
    zeroize_plate(cpg)
    return kit_pages("ARMAMENT", {0: [2, 4, 1, 3]}, pilot) + kit_pages("ARMAMENT", {1: [1, 6, 1, 2]}, cpg)


def eufd_rocker(name: str, at: list) -> dict:
    return {"id": f"{{seat}}_EUFD_{name}", "label": name, "type": "hat", "ud": f"{{seat}}_EUFD_{name}", "hold": MPD_BUTTON_HOLD, "positions": {"up": "tri-up", "down": "tri-down"}, "at": at}


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


THREAT_CENTER = (376, 95)


def dial_point(radius: float, angle: float) -> tuple[float, float]:
    rad = math.radians(angle)
    return THREAT_CENTER[0] + radius * math.sin(rad), THREAT_CENTER[1] - radius * math.cos(rad)


def threat_sector(name: str, label: str, angle: float) -> dict:
    inner, outer, half = 28, 52, 20
    pts = [dial_point(inner, angle - half), dial_point(outer, angle - half), dial_point(outer, angle + half), dial_point(inner, angle + half)]
    x, y = min(p[0] for p in pts), min(p[1] for p in pts)
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = [(round(p[0] - x, 1), round(p[1] - y, 1)) for p in pts]
    d = f"M{ax} {ay}L{bx} {by}A{outer} {outer} 0 0 1 {cx} {cy}L{dx} {dy}A{inner} {inner} 0 0 0 {ax} {ay}Z"
    return {
        "bright": f"PLT_CMWS_{name}_BRT_L", "dim": f"PLT_CMWS_{name}_DIM_L", "label": label, "shape": "sector", "d": d,
        "at": [round(x, 1), round(y, 1), round(max(p[0] for p in pts) - x, 1), round(max(p[1] for p in pts) - y, 1)],
    }


def threat_letter(name: str, y: float) -> dict:
    return {
        "bright": f"PLT_CMWS_{name}_BRT_L", "dim": f"PLT_CMWS_{name}_DIM_L", "label": name, "shape": "letter", "text": name, "size": 17,
        "at": [THREAT_CENTER[0] - 9, y - 9, 18, 18],
    }


def threat_dial_art() -> list[dict]:
    r = 56
    ticks = ""
    for i in range(36):
        a = math.radians(i * 10)
        inner = r - (9 if i % 3 == 0 else 5)
        ticks += f"M{round(r + inner * math.sin(a), 1)} {round(r - inner * math.cos(a), 1)}L{round(r + r * math.sin(a), 1)} {round(r - r * math.cos(a), 1)}"
    at = [THREAT_CENTER[0] - r, THREAT_CENTER[1] - r, r * 2, r * 2]
    return [
        {"shape": "path", "at": at, "d": f"M0 {r}a{r} {r} 0 1 0 {r * 2} 0a{r} {r} 0 1 0 {-r * 2} 0", "width": 1.2},
        {"shape": "path", "at": at, "d": ticks, "width": 1.2},
    ]


def cmws_toggle(name: str, label: str, top: str, bottom: str, x: float, guard: bool = False) -> dict:
    return {
        "id": f"PLT_CMWS_{name}", "label": label, "type": "selector", "positions": [{"value": 1, "label": top}, {"value": 0, "label": bottom}],
        "at": [x - 33, 344, 66, 96], **({"guard": True, "cover": f"PLT_CMWS_{name}_CVR"} if guard else {}),
    }


def cmws_pages() -> list[dict]:
    controls = [
        {
            "id": "PLT_CMWS_PW", "label": "PWR", "type": "selector", "style": "rotary", "rest": 1, "hold": 0.5, "knob": [124, 122, 36],
            "positions": [
                {"value": 0, "label": "OFF", "angle": 50, "y": 62}, {"value": 1, "label": "ON", "angle": 92, "y": 116},
                {"value": 2, "label": "TEST", "momentary": True, "angle": 128, "y": 170},
            ],
            "at": [60, 34, 150, 170],
        },
        {
            "id": "PLT_CMWS_STATUS", "label": "STATUS", "type": "display", "cols": 4, "at": [215, 58, 100, 96], "page": "PLT_CMWS_PAGE",
            "ids": [
                "PLT_CMWS_PAGE", "PLT_CMWS_FLARE_LETTER", "PLT_CMWS_FLARE_COUNT", "PLT_CMWS_CHAFF_LETTER", "PLT_CMWS_CHAFF_COUNT",
                "PLT_CMWS_BIT_LINE_1", "PLT_CMWS_BIT_LINE_2",
            ],
            "pages": {
                "MAIN": [["PLT_CMWS_FLARE_LETTER", "PLT_CMWS_FLARE_COUNT"], ["PLT_CMWS_CHAFF_LETTER", "PLT_CMWS_CHAFF_COUNT"]],
                "TEST": [["PLT_CMWS_BIT_LINE_1"], ["PLT_CMWS_BIT_LINE_2"]],
            },
        },
        {"id": "PLT_CMWS_VOL", "label": "AUDIO", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135], "at": [454, 30, 60, 60]},
        {"id": "PLT_CMWS_LAMP", "label": "LAMP", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135], "at": [457, 110, 60, 60]},
        cmws_toggle("ARM", "ARM / SAFE", "ARM", "SAFE", 163),
        cmws_toggle("MODE", "CMWS / NAV", "CMWS", "NAV", 275),
        cmws_toggle("BYPASS", "BYPASS / AUTO", "BYPASS", "AUTO", 387),
        cmws_toggle("JETT", "JETTISON", "ON", "OFF", 514, True),
    ]
    placard = [
        ["OFF", 176, 77, 19, 38], ["ON", 190, 116, 19, 26, 90], ["TEST", 184, 161, 19, 44],
        ["PWR", 181, 192, 21, 40], ["STATUS", 274, 190, 21, 64], ["THREAT", 385, 190, 21, 66],
        ["AUDIO", 484, 100, 21, 48], ["LAMP", 487, 190, 21, 44], ["+", 534, 100, 14],
        ["CMWS CONTROL PANEL", 263, 266, 25, 245], ["+", 225, 303, 16],
        ["ARM", 163, 346, 20, 36], ["CMWS", 275, 342, 20, 50], ["BYPASS", 387, 342, 20, 66],
        ["SAFE", 163, 444, 20, 40], ["NAV", 275, 444, 20, 30], ["AUTO", 387, 444, 20, 38],
        ["JETTISON", 574, 380, 22, 118, 90],
    ]
    art = [
        {"shape": "plate", "at": [4, 4, 620, 228]}, {"shape": "plate", "at": [4, 244, 620, 238]},
        {"shape": "screw", "at": [32, 122, 13]}, {"shape": "screw", "at": [528, 52, 13]}, {"shape": "screw", "at": [604, 108, 14]},
        {"shape": "screw", "at": [542, 176, 12]}, {"shape": "screw", "at": [132, 192, 11]},
        {"shape": "screw", "at": [36, 332, 14]}, {"shape": "screw", "at": [44, 414, 14]},
        {"shape": "screw", "at": [598, 302, 14]}, {"shape": "screw", "at": [606, 386, 14]},
        {"shape": "glass", "at": [210, 22, 238, 146]},
        *threat_dial_art(),
        {"shape": "line", "at": [156.2, 95, 9.2, -7.7]}, {"shape": "line", "at": [166, 120.5, 12, -0.6]}, {"shape": "line", "at": [157.1, 147.9, 9.5, 7.3]},
        {"shape": "hazard", "at": [432, 252, 56, 216], "period": 22},
    ]
    indicators = [
        threat_sector("FWD_LEFT", "FWD LEFT", -45), threat_sector("FWD_RIGHT", "FWD RIGHT", 45),
        threat_sector("AFT_RIGHT", "AFT RIGHT", 135), threat_sector("AFT_LEFT", "AFT LEFT", -135),
        threat_letter("D", 70), threat_letter("R", 120),
    ]
    return panel_pages("CMWS", {0: [1, 10, 2, 3]}, [628, 486], placard, art, controls, indicators)


def wiper_plate(seat: str, dx: int = 0, dy: int = 0) -> tuple[list, list, list]:
    def move(at: list) -> list:
        return [round(at[0] + dx, 1), round(at[1] + dy, 1), *at[2:]]

    controls = [
        {"id": f"{seat}_DEFOG_BTN", "label": "DEFOG", "type": "button", "shape": "round", "hold": MPD_BUTTON_HOLD, "at": move([147.7, 301.4, 70, 70])},
        {
            "id": f"{seat}_WIPER_SW", "label": "WINDSHIELD WIPER", "type": "selector", "style": "rotary", "orient": "h", "knob": move([420, 358, 52]),
            "positions": [
                {"value": 0, "label": "PARK", "angle": -42, "x": 335 + dx}, {"value": 1, "label": "OFF", "angle": 0, "x": 397 + dx},
                {"value": 2, "label": "LO", "angle": 37, "x": 451 + dx}, {"value": 3, "label": "HI", "angle": 74, "x": 519 + dx},
            ],
            "at": move([305, 250, 240, 165]),
        },
    ]
    placard = [
        ["WINDSHIELD WIPER", 317.9, 243, 28, 295], ["+", 104.6, 267, 14], ["DEFOG", 181.2, 285.7, 22, 76],
        ["PARK", 350.5, 281, 15, 46], ["OFF", 420.7, 264.7, 15, 28], ["LO", 479.3, 281, 15, 20], ["HI", 501, 335, 15, 18],
    ]
    art = [
        {"shape": "plate", "at": [4, 217, 620, 265]},
        {"shape": "screw", "at": [31.5, 271.3, 20]}, {"shape": "screw", "at": [555.3, 282.1, 13]},
        {"shape": "screw", "at": [73.4, 390.6, 14]}, {"shape": "screw", "at": [595.8, 389.2, 18]},
        {"shape": "screw", "at": [35.5, 463, 17]}, {"shape": "screw", "at": [593.6, 463, 17]},
        {"shape": "line", "at": [369.2, 301.6, -6.7, -7.6]}, {"shape": "line", "at": [465.8, 297.3, 6.6, -8]}, {"shape": "line", "at": [477.7, 341.4, 9.6, -2.7]},
    ]
    return (
        controls,
        [[t, round(x + dx, 1), round(y + dy, 1), *rest] for t, x, y, *rest in placard],
        [{**a, "at": move(a["at"])} for a in art],
    )


def center_pages() -> list[dict]:
    def ckt(name: str, label: str, x: float) -> dict:
        return {
            "id": f"PLT_CHK_OSPD_ENG_{name}", "label": label, "type": "selector", "rest": 1, "hold": 0.5, "at": [x - 40, 24.5, 80, 180],
            "positions": [
                {"value": 2, "label": "ENG 1", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "ENG 2", "momentary": True},
            ],
        }

    wiper_controls, wiper_placard, wiper_art = wiper_plate("PLT")
    controls = [
        ckt("A", "CKT A", 146.5), ckt("B", "CKT B", 291.9),
        {
            "id": "PLT_GEN_RESET", "label": "GEN RST", "type": "selector", "orient": "h", "rest": 1, "hold": 0.5, "at": [373.4, 76.7, 180, 80],
            "positions": [
                {"value": 0, "label": "GEN 1", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "GEN 2", "momentary": True},
            ],
        },
        *wiper_controls,
        {
            "id": "PLT_PARK_BRAKE", "label": "PARK BRAKE", "type": "selector", "orient": "h", "at": [170, 505, 150, 66],
            "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "PULLED"}],
        },
        {"id": "PLT_ALT_SET_KNB", "label": "ALT SET", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135], "at": [462, 506, 64, 64]},
    ]
    placard = [
        ["CHK OVSP TEST", 193.7, 41.8, 30, 256], ["GEN RST", 466.4, 41.8, 30, 128],
        ["ENG 1", 219.2, 81.8, 16, 57], ["OFF", 219.2, 113, 16, 29], ["ENG 2", 219.2, 142, 16, 57],
        ["CKT A", 146.5, 175.6, 21, 74], ["CKT B", 291.9, 175.6, 21, 74],
        ["+", 381.3, 89.8, 14], ["GEN 1", 390.8, 113.8, 17, 52], ["GEN 2", 538, 113.8, 17, 58],
        *wiper_placard,
        ["PARK BRAKE", 92, 538, 22, 108], ["IN", 196, 538, 18, 18], ["PULLED", 309, 538, 18, 56], ["ALT SET", 402, 538, 22, 80],
    ]
    art = [
        {"shape": "plate", "at": [4, 4, 620, 207]}, *wiper_art, {"shape": "plate", "at": [4, 488, 620, 100]},
        {"shape": "screw", "at": [34.5, 68, 17]}, {"shape": "screw", "at": [550, 76.7, 11]},
        {"shape": "screw", "at": [75.2, 149.4, 13]}, {"shape": "screw", "at": [591.4, 149.4, 17]},
        {"shape": "screw", "at": [24, 500, 9]}, {"shape": "screw", "at": [604, 576, 9]},
    ]
    return panel_pages("CENTER", {0: [6, 5, 2, 4]}, [628, 592], placard, art, controls)


def comm_knob(key: str, label: str, at: list, chip_at: list | None = None) -> list[dict]:
    knob = {"id": f"{{seat}}_COM_{key}_VOL", "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-150, 150], "at": at}
    if chip_at is None:
        return [knob]
    chip = {
        "id": f"{{seat}}_COM_{key}_PW", "label": f"{label} PULL", "type": "selector", "style": "chip", "legend": "PULL",
        "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "OUT"}], "at": chip_at,
    }
    return [{**knob, "pull": chip["id"]}, chip]


def comm_pages() -> list[dict]:
    radios = [("VHF", "VHF", 97, 101), ("UHF", "UHF", 206, 210), ("FM1", "FM 1", 316, 321), ("FM2", "FM 2", 427, 436), ("HF", "HF", 537, 550)]
    aux = [("IFF", "IFF", 99, None), ("RLWR", "RLWR", 213, None), ("ATA", "ATA", 331, None), ("VCR", "VCR", 446, [411, 574, 70, 17]), ("ADF", "ADF", 549, [496, 574, 70, 17])]
    controls = []
    for key, label, x, knob_x in radios:
        controls += comm_knob(key, label, [knob_x - 35, 69, 70, 70], [knob_x - 35, 141, 70, 17])
        controls.append({
            "id": f"{{seat}}_COM_{key}_SQL", "label": f"{label} SQL", "type": "selector", "rest": 1, "hold": 0.5, "at": [x - 39, 168, 78, 126],
            "positions": [
                {"value": 2, "label": "ENABLE", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "DISABLE", "momentary": True},
            ],
        })
    controls += [
        {"id": "{seat}_COM_MASTER_VOL", "label": "MASTER", "type": "knob", "step": KNOB_STEP, "sweep": [-150, 150], "at": [79, 294, 104, 104]},
        {"id": "{seat}_COM_SENS_KNB", "label": "SENS", "type": "knob", "step": KNOB_STEP, "sweep": [-150, 150], "at": [225, 309, 72, 72]},
        {
            "id": "{seat}_COM_ICS_MODE", "label": "ICS", "type": "selector", "at": [350, 289, 80, 119],
            "positions": [{"value": 2, "label": "PTT"}, {"value": 1, "label": "VOX"}, {"value": 0, "label": "HOT MIC"}],
        },
        {"id": "{seat}_COM_IDENT_BTN", "label": "IDENT", "type": "button", "shape": "round", "hold": MPD_BUTTON_HOLD, "at": [487, 316, 68, 68]},
    ]
    for key, label, x, chip_at in aux:
        controls += comm_knob(key, label, [x - 35, 483, 70, 70], chip_at)
    placard = [
        ["COMM", 314, 25.5, 27, 88],
        ["VHF", 97, 62.5, 22, 46], ["UHF", 204, 62.5, 22, 46], ["FM 1", 316, 62.5, 22, 56], ["FM 2", 427, 63, 22, 57], ["HF", 535, 62.5, 22, 30],
        ["SOL", 318.5, 170.5, 25, 46],
        ["MASTER", 124, 280, 26, 102], ["SENS", 255, 283.5, 26, 62], ["MIN", 86.5, 411, 19, 33], ["MAX", 162, 411, 19, 42],
        ["ICS", 390, 274.5, 24, 40], ["PTT", 388, 300.5, 18.5, 34], ["VOX", 331, 349, 19, 38], ["HOT MIC", 391.5, 398, 20, 82],
        ["IDENT", 522.5, 295.5, 25, 71],
        ["AUX", 325, 436, 26, 49], ["+", 490, 446, 16],
        ["IFF", 99, 465.5, 25, 36], ["RLWR", 211, 465.5, 25, 72], ["ATA", 325, 465.5, 25, 51], ["VCR", 437, 465.5, 25, 49], ["ADF", 545.5, 465.5, 25, 49],
    ]
    art = [
        {"shape": "plate", "at": [3, 4, 620, 592]},
        {"shape": "bracket", "at": [3, 4, 52, 78]}, {"shape": "bracket", "at": [570, 4, 53, 80]},
        {"shape": "bracket", "at": [3, 500, 52, 96]}, {"shape": "bracket", "at": [570, 500, 53, 96]},
        {"shape": "screw", "at": [27, 57, 18]}, {"shape": "screw", "at": [150, 52, 14]}, {"shape": "screw", "at": [475.5, 54.5, 14]}, {"shape": "screw", "at": [599, 58, 19]},
        {"shape": "screw", "at": [32, 540, 20]}, {"shape": "screw", "at": [156, 541, 15]}, {"shape": "screw", "at": [492, 537, 15]}, {"shape": "screw", "at": [607.5, 541, 19]},
        {"shape": "line", "at": [58.5, 171, 220.5, 0]}, {"shape": "line", "at": [58.5, 171, 0, 30]},
        {"shape": "line", "at": [358.5, 171, 222.5, 0]}, {"shape": "line", "at": [581, 171, 0, 30]},
        {"shape": "line", "at": [58.5, 435, 220.5, 0]}, {"shape": "line", "at": [58.5, 435, 0, 29]},
        {"shape": "line", "at": [365, 435, 224, 0]}, {"shape": "line", "at": [589, 435, 0, 31]},
    ]
    return panel_pages("COMM", {0: [3, 10, 3, 3], 1: [2, 11, 2, 2]}, [627, 600], placard, art, controls)


def wiper_pages() -> list[dict]:
    controls, placard, art = wiper_plate("CPG", 0, -213)
    return panel_pages("WIPER / DEFOG", {1: [4, 11, 1, 2]}, [628, 273], placard, art, controls)


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
    *cmws_pages(),
    *center_pages(),
    *comm_pages(),
    *wiper_pages(),
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
