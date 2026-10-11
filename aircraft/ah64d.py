import math

from aircraft.panel_kit import PARTS, REF, Panel, PanelGroup

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
    return panel_pages(name, cells, page["box"], page["print"], page["art"], page["controls"], page["indicators"], ref=REF)


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


def lever(name: str, label: str, side: str) -> dict:
    return {"id": name, "label": label, "type": "lever", "readback": f"{{seat}}_ENG_{side[0].upper()}_PW_LVR", "side": side, "positions": POWER_POSITIONS}


def power_levers() -> tuple:
    return lever("power_left", "PWR LVR NO 1", "left"), lever("power_right", "PWR LVR NO 2", "right")


# printed marks of the power levers in the order of POWER_POSITIONS
LEVER_MARKS = ("OFF", "IDLE", "FLY", "LOCK\nOUT")
LEVER_NAMES = ("NO. 1", "NO. 2")


def power_pages() -> list[dict]:
    p = Panel("POWER", 640, 600)
    p.toggle("RTR", 154, 96, {
        "id": "PLT_ROTOR_BRK", "label": "RTR BRK", "type": "selector",
        "positions": [{"value": 2, "label": "OFF"}, {"value": 1, "label": "BRK", "disabled": True}, {"value": 0, "label": "LOCK"}],
    }, "right_triple")
    p.label("RTR BRK", "NAME", "RTR", "above", 0, -20)
    p.rotary("MSTR", 154, 224, {
        "id": "PLT_MASTER_IGN_SW", "label": "MSTR IGN", "type": "selector", "style": "rotary",
        "positions": [{"value": 0, "label": "OFF", "angle": 66}, {"value": 1, "label": "BATT", "angle": 90}, {"value": 2, "label": "EXT PWR", "disabled": True, "angle": 118}],
    }, labels="fan")
    p.label("MSTR IGN", "NAME", "MSTR", "above")
    p.push("APU", 154, 364, {
        "id": "PLT_APU_BTN", "label": "APU", "type": "button", "hold": MPD_BUTTON_HOLD, "requires": {"id": "PLT_APU_BTN_CVR", "value": 1},
        "lamp": "PLT_APU_L", "legend": "ON", "color": "green",
    }, flap={
        "id": "PLT_APU_BTN_CVR", "label": "APU COVER", "type": "selector", "style": "cover", "positions": [{"value": 0, "label": "CLOSED"}, {"value": 1, "label": "OPEN"}],
    })
    p.label("APU", "NAME", "APU", "above")
    p.mark("ENG START", "NAME", 154, 434, "title of the two switches")
    for n, x in ((1, 88), (2, 220)):
        p.toggle(f"ENG{n}", x, 490, {"id": f"PLT_ENG{n}_START", "label": f"ENG {n} START", "type": "selector", "rest": 1, "hold": 0.5, "positions": ENGINE_START_POSITIONS})
        p.label(f"NO {n}", "POS", f"ENG{n}", "below")
    for text, y in (("START", 462), ("OFF", 490), ("IGN\nORIDE", 528)):
        p.mark(text, "POS", 154, y, "printed once between the two switches, as on the photo")
    p.mark("+", "SMALL", 230, 300, "panel mark as on the photo")
    p.levers("LEVERS", 340, 304, 400, power_levers(), LEVER_MARKS, LEVER_NAMES)
    p.label("POWER", "TITLE", "LEVERS_1", "above", 0, 28)
    p.slider("FRICT", 504, 304, {"id": "PLT_PW_LVR_FRIC", "label": "FRICT", "type": "knob", "style": "slider", "step": KNOB_STEP}, "INC", "DECR", "FRICT")
    c = Panel("POWER", 312, 576)
    c.levers("LEVERS", 156, 284, 400, power_levers(), LEVER_MARKS, LEVER_NAMES, (None, "IDLE", "FLY", "LOCK"))
    return kit_pages("POWER", {0: [4, 1, 2, 3]}, p) + kit_pages("POWER", {1: [3, 1, 2, 3]}, c)


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


# symbols of the EUFD keys: width, height and the paths (path, stroke, filled) in their own units
EUFD_ENTER = (16, 8, [("M15 0V4.2H4", 1.6, False), ("M5.5 1.2L1 4.2L5.5 7.2Z", 1, True)])
EUFD_STOPWATCH = (12, 16, [("M0.4 10a5.8 5.8 0 1 0 11.6 0a5.8 5.8 0 1 0-11.6 0M3.4 0.5H9M6.2 0.5V4.2M6.2 10L4.3 12.6", 1.6, False)])
EUFD_SWAP = (14, 14, [("M0.9 5.9A6.2 6.2 0 0 1 11.75 3M13.1 8.1A6.2 6.2 0 0 1 2.25 11", 1.6, False), ("M12.5 3.9L12.9 1L9.5 3.8ZM1.5 10.1L1.1 13L4.45 10.2Z", 0.8, True)])


def eufd_rocker(name: str) -> dict:
    return {"id": f"{{seat}}_EUFD_{name}", "label": name, "type": "hat", "ud": f"{{seat}}_EUFD_{name}", "hold": MPD_BUTTON_HOLD, "positions": {"up": "tri-up", "down": "tri-down"}}


def eufd_button(name: str, label: str) -> dict:
    return {"id": f"{{seat}}_EUFD_{name}", "label": label, "type": "button", "style": "flat", "hold": MPD_BUTTON_HOLD}


def eufd_pages() -> list[dict]:
    p = Panel("EUFD", 640, 524)
    p.display("DISPLAY", 320, 204, 568, 280, {"id": "{seat}_EUFD_DISPLAY", "label": "EUFD", "type": "display", "ids": [f"{{seat}}_EUFD_LINE{n}" for n in range(1, 15)]})
    for name, x in (("WCA", 90), ("IDM", 154), ("RTS", 218)):
        p.rocker(name, x, 428, eufd_rocker(name))
    p.knob("BRT", "KNOB_L", 350, 440, {"id": "{seat}_EUFD_BRT", "label": "BRT", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("BRT", "NAME", "BRT", "above")
    p.push_small("PRESET", 484, 396, eufd_button("PRESET", "P"), "P")
    p.push_small("ENT", 548, 396, eufd_button("ENT", "ENTER"), EUFD_ENTER)
    p.push_small("STOPWATCH", 484, 460, eufd_button("STOPWATCH", "STOPWATCH"), EUFD_STOPWATCH)
    p.push_small("SWAP", 548, 460, eufd_button("SWAP", "SWAP"), EUFD_SWAP)
    return kit_pages("EUFD", {0: [1, 7, 1, 3], 1: [1, 8, 1, 3]}, p)


def dial_point(cx: int, cy: int, radius: float, angle: float) -> tuple[float, float]:
    rad = math.radians(angle)
    return cx + radius * math.sin(rad), cy - radius * math.cos(rad)


def threat_sector(name: str, label: str, angle: float, cx: int, cy: int) -> dict:
    r = PARTS["DIAL"]["w"] // 2
    inner, outer, half = r // 2, r - 4, 20
    pts = [dial_point(cx, cy, inner, angle - half), dial_point(cx, cy, outer, angle - half), dial_point(cx, cy, outer, angle + half), dial_point(cx, cy, inner, angle + half)]
    x, y = min(p[0] for p in pts), min(p[1] for p in pts)
    (ax, ay), (bx, by), (qx, qy), (dx, dy) = [(round(p[0] - x, 1), round(p[1] - y, 1)) for p in pts]
    d = f"M{ax} {ay}L{bx} {by}A{outer} {outer} 0 0 1 {qx} {qy}L{dx} {dy}A{inner} {inner} 0 0 0 {ax} {ay}Z"
    return {
        "bright": f"PLT_CMWS_{name}_BRT_L", "dim": f"PLT_CMWS_{name}_DIM_L", "label": label, "shape": "sector", "d": d,
        "at": [round(x, 1), round(y, 1), round(max(p[0] for p in pts) - x, 1), round(max(p[1] for p in pts) - y, 1)],
    }


def threat_letter(name: str, cx: int, cy: int) -> dict:
    return {
        "bright": f"PLT_CMWS_{name}_BRT_L", "dim": f"PLT_CMWS_{name}_DIM_L", "label": name, "shape": "letter", "text": name, "size": 17,
        "at": [cx - 9, cy - 9, 18, 18],
    }


def threat_dial(p: Panel, name: str, cx: int, cy: int):
    p.dial(name, cx, cy)
    for sector, label, angle in (("FWD_LEFT", "FWD LEFT", -45), ("FWD_RIGHT", "FWD RIGHT", 45), ("AFT_RIGHT", "AFT RIGHT", 135), ("AFT_LEFT", "AFT LEFT", -135)):
        p.indicator(name, threat_sector(sector, label, angle, cx, cy))
    for letter, dy in (("D", -25), ("R", 25)):
        p.indicator(name, threat_letter(letter, cx, cy + dy))


def cmws_toggle(name: str, label: str, top: str, bottom: str, guard: bool = False) -> dict:
    return {
        "id": f"PLT_CMWS_{name}", "label": label, "type": "selector", "positions": [{"value": 1, "label": top}, {"value": 0, "label": bottom}],
        **({"guard": True, "cover": f"PLT_CMWS_{name}_CVR"} if guard else {}),
    }


def cmws_pages() -> list[dict]:
    g = PanelGroup("CMWS")
    u = g.panel("INDICATOR", 616, 288, 0, 0)
    u.rotary("PWR", 114, 170, {
        "id": "PLT_CMWS_PW", "label": "PWR", "type": "selector", "style": "rotary", "rest": 1, "hold": 0.5,
        "positions": [
            {"value": 0, "label": "OFF", "angle": 50}, {"value": 1, "label": "ON", "angle": 92},
            {"value": 2, "label": "TEST", "momentary": True, "angle": 128},
        ],
    }, turned=("ON",))
    u.label("PWR", "NAME", "PWR", "below")
    u.display("STATUS", 284, 172, 104, 96, {
        "id": "PLT_CMWS_STATUS", "label": "STATUS", "type": "display", "cols": 4, "page": "PLT_CMWS_PAGE",
        "ids": [
            "PLT_CMWS_PAGE", "PLT_CMWS_FLARE_LETTER", "PLT_CMWS_FLARE_COUNT", "PLT_CMWS_CHAFF_LETTER", "PLT_CMWS_CHAFF_COUNT",
            "PLT_CMWS_BIT_LINE_1", "PLT_CMWS_BIT_LINE_2",
        ],
        "pages": {
            "MAIN": [["PLT_CMWS_FLARE_LETTER", "PLT_CMWS_FLARE_COUNT"], ["PLT_CMWS_CHAFF_LETTER", "PLT_CMWS_CHAFF_COUNT"]],
            "TEST": [["PLT_CMWS_BIT_LINE_1"], ["PLT_CMWS_BIT_LINE_2"]],
        },
    })
    u.label("STATUS", "NAME", "STATUS", "below")
    threat_dial(u, "THREAT", 406, 164)
    u.label("THREAT", "NAME", "THREAT", "below")
    u.knob("AUDIO", "KNOB_M", 516, 72, {"id": "PLT_CMWS_VOL", "label": "AUDIO", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    u.label("AUDIO", "NAME", "AUDIO", "below")
    u.knob("LAMP", "KNOB_M", 516, 184, {"id": "PLT_CMWS_LAMP", "label": "LAMP", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    u.label("LAMP", "NAME", "LAMP", "below")
    u.mark("+", "SMALL", 572, 120, "panel mark as on the photo")
    c = g.panel("CONTROL PANEL", 616, 248, 0, 304)
    c.mark("CMWS CONTROL PANEL", "TITLE", 240, 52, "panel title")
    c.mark("+", "SMALL", 184, 100, "panel mark as on the photo")
    for name, label, top, bottom, x in (("ARM", "ARM / SAFE", "ARM", "SAFE", 128), ("MODE", "CMWS / NAV", "CMWS", "NAV", 240), ("BYPASS", "BYPASS / AUTO", "BYPASS", "AUTO", 352)):
        c.toggle(name, x, 140, cmws_toggle(name, label, top, bottom), "above_below")
    c.toggle("JETT", 460, 150, cmws_toggle("JETT", "JETTISON", "ON", "OFF", True))
    c.hazard("JETT")
    c.label("JETTISON", "NAME", "JETT", "right", 90)
    return kit_pages("CMWS", {0: [1, 10, 2, 3]}, g)


def wiper_panel(p: Panel, seat: str):
    p.mark("WINDSHIELD WIPER", "TITLE", "CX", 80, "panel title")
    p.mark("+", "SMALL", 145, 122, "panel mark as on the photo")
    p.round("DEFOG", 84, 174, {"id": f"{seat}_DEFOG_BTN", "label": "DEFOG", "type": "button", "shape": "round", "hold": MPD_BUTTON_HOLD})
    p.label("DEFOG", "NAME", "DEFOG", "above")
    p.rotary("WIPER", 246, 190, {
        "id": f"{seat}_WIPER_SW", "label": "WINDSHIELD WIPER", "type": "selector", "style": "rotary", "orient": "h",
        "positions": [
            {"value": 0, "label": "PARK", "angle": -42}, {"value": 1, "label": "OFF", "angle": 0},
            {"value": 2, "label": "LO", "angle": 37}, {"value": 3, "label": "HI", "angle": 74},
        ],
    }, labels="fan")


def center_pages() -> list[dict]:
    g = PanelGroup("CENTER")
    a = g.panel("CHK OVSP TEST", 640, 210, 0, 0)
    a.mark("CHK OVSP TEST", "TITLE", 250, 52, "panel title")
    a.mark("GEN RST", "TITLE", 500, 52, "panel title")
    for name, x in (("A", 170), ("B", 330)):
        a.toggle(f"CKT_{name}", x, 114, {
            "id": f"PLT_CHK_OSPD_ENG_{name}", "label": f"CKT {name}", "type": "selector", "rest": 1, "hold": 0.5,
            "positions": [{"value": 2, "label": "ENG 1", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "ENG 2", "momentary": True}],
        })
        a.label(f"CKT {name}", "NAME", f"CKT_{name}", "below")
    for text, y in (("ENG 1", 86), ("OFF", 114), ("ENG 2", 142)):
        a.mark(text, "POS", 250, y, "printed once between the two switches, as on the photo")
    a.toggle("GEN", 500, 114, {
        "id": "PLT_GEN_RESET", "label": "GEN RST", "type": "selector", "orient": "h", "rest": 1, "hold": 0.5,
        "positions": [{"value": 0, "label": "GEN 1", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "GEN 2", "momentary": True}],
    }, "left_right")
    a.mark("+", "SMALL", 420, 86, "panel mark as on the photo")
    wiper_panel(g.panel("WINDSHIELD WIPER", 376, 304, 0, 226), "PLT")
    c = g.panel("PARK BRAKE / ALT SET", 248, 304, 392, 226)
    c.toggle("PARK", 100, 120, {
        "id": "PLT_PARK_BRAKE", "label": "PARK BRAKE", "type": "selector", "orient": "h",
        "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "PULLED"}],
    }, "left_right_pair")
    c.label("PARK\nBRAKE", "NAME", "PARK", "above")
    c.knob("ALT", "KNOB_M", 124, 232, {"id": "PLT_ALT_SET_KNB", "label": "ALT SET", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    c.label("ALT SET", "NAME", "ALT", "above")
    return kit_pages("CENTER", {0: [6, 5, 2, 4]}, g)


def comm_knob(p: Panel, key: str, label: str, x: int, y: int, pull: bool):
    p.knob(key, "KNOB_S", x, y, {"id": f"{{seat}}_COM_{key}_VOL", "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-150, 150]})
    p.label(label, "NAME", key, "above")
    if pull:
        p.chip(f"{key}_PULL", key, {
            "id": f"{{seat}}_COM_{key}_PW", "label": f"{label} PULL", "type": "selector", "style": "chip", "legend": "PULL",
            "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "OUT"}],
        })


def comm_pages() -> list[dict]:
    p = Panel("COMM", 640, 600)
    p.mark("COMM", "TITLE", "CX", 52, "panel title")
    p.bracket("SOL", "SOL", 52, 588, 208)
    for key, label, x in (("VHF", "VHF", 88), ("UHF", "UHF", 204), ("FM1", "FM 1", 320), ("FM2", "FM 2", 436), ("HF", "HF", 552)):
        comm_knob(p, key, label, x, 130, True)
        p.toggle(f"{key}_SQL", x, 256, {
            "id": f"{{seat}}_COM_{key}_SQL", "label": f"{label} SQL", "type": "selector", "rest": 1, "hold": 0.5,
            "positions": [{"value": 2, "label": "ENABLE", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "DISABLE", "momentary": True}],
        })
    p.knob("MASTER", "KNOB_L", 128, 372, {"id": "{seat}_COM_MASTER_VOL", "label": "MASTER", "type": "knob", "step": KNOB_STEP, "sweep": [-150, 150]})
    p.label("MASTER", "NAME", "MASTER", "above")
    p.knob_labels("MASTER", "lower_sides", "MIN", "MAX")
    p.knob("SENS", "KNOB_M", 262, 360, {"id": "{seat}_COM_SENS_KNB", "label": "SENS", "type": "knob", "step": KNOB_STEP, "sweep": [-150, 150]})
    p.label("SENS", "NAME", "SENS", "above")
    p.toggle("ICS", 378, 320, {
        "id": "{seat}_COM_ICS_MODE", "label": "ICS", "type": "selector",
        "positions": [{"value": 2, "label": "PTT"}, {"value": 1, "label": "VOX"}, {"value": 0, "label": "HOT MIC"}],
    }, "above_left_below")
    p.label("ICS", "NAME", "ICS", "above")
    p.round("IDENT", 520, 356, {"id": "{seat}_COM_IDENT_BTN", "label": "IDENT", "type": "button", "shape": "round", "hold": MPD_BUTTON_HOLD})
    p.label("IDENT", "NAME", "IDENT", "above")
    p.bracket("AUX", "AUX", 52, 588, 428)
    p.mark("+", "SMALL", 488, 454, "panel mark as on the photo")
    for key, label, x, pull in (("IFF", "IFF", 96, False), ("RLWR", "RLWR", 208, False), ("ATA", "ATA", 320, False), ("VCR", "VCR", 432, True), ("ADF", "ADF", 544, True)):
        comm_knob(p, key, label, x, 502, pull)
    return kit_pages("COMM", {0: [3, 10, 3, 3], 1: [2, 11, 2, 2]}, p)


def wiper_pages() -> list[dict]:
    p = Panel("WIPER / DEFOG", 376, 304)
    wiper_panel(p, "CPG")
    return kit_pages("WIPER / DEFOG", {1: [4, 11, 1, 2]}, p)


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
