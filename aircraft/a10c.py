from panel_kit import REF, Panel, PanelGroup

DCSBIOS_MODULE = "A-10C"
NAME = "A-10C"
DCS_NAMES = ["A-10C_2"]

KEYS = {}

KNOB_STEP = 3200
BUTTON_HOLD = 0.3

MASTER_LAMPS = [
    {"id": "MASTER_CAUTION", "label": "MASTER CAUTION", "color": "amber", "button": "UFC_MASTER_CAUTION"},
]


def kit_page(name: str, cell: list, page: dict) -> dict:
    return {
        "name": name, "seats": [0], "panel": True, "layout": "panel", "map": cell, "box": page["box"],
        "lamps": MASTER_LAMPS, "print": page["print"], "art": page["art"], "controls": page["controls"],
        **({"indicators": page["indicators"]} if page["indicators"] else {}),
        **({"scroll": True} if page.get("scroll") else {}),
        "kit": True, "ref": list(REF),
    }


def brake_plate(g: PanelGroup):
    p = g.panel("EMER BRAKE", 340, 240, 0, 0)
    p.toggle("SEAT", 90, 148, {
        "id": "SEAT_ADJUST", "label": "SEAT ADJUST", "type": "selector", "rest": 1, "hold": 0.5,
        "positions": [{"value": 2, "label": "UP", "momentary": True}, {"value": 1, "label": "HOLD"}, {"value": 0, "label": "DOWN", "momentary": True}],
    }, "above_side_below")
    p.toggle("BRAKE", 250, 148, {
        "id": "EMER_BRAKE", "label": "EMER BRAKE", "type": "selector",
        "positions": [{"value": 1, "label": "PULLED"}, {"value": 0, "label": "IN"}],
    }, "above_below")
    p.label("EMER\nBRAKE", "NAME", "BRAKE", "above")


def aux_plate(g: PanelGroup):
    p = g.panel("AUX LTG", 340, 568, 0, 256)
    p.knob("RSIL", "KNOB_M", 170, 128, {"id": "ALCP_RSIL", "label": "REFUEL STATUS & INDEXER LTS", "type": "knob", "step": KNOB_STEP, "sweep": [-130, 130]})
    p.label("REFUEL STATUS\n& INDEXER LTS", "NAME", "RSIL", "above")
    p.knob_labels("RSIL", "lower_sides", "DIM", "BRT")
    p.toggle("NVIS", 100, 280, {
        "id": "ALCP_NVIS_LTS", "label": "NVIS LTS", "type": "selector",
        "positions": [{"value": 2, "label": "TOP"}, {"value": 1, "label": "ALL"}, {"value": 0, "label": "OFF"}],
    }, "right_triple")
    p.label("NVIS\nLTS", "NAME", "NVIS", "above")
    p.toggle("HARS", 240, 280, {
        "id": "ALCP_HARSSAS", "label": "HARS/SAS OVERRIDE", "type": "selector",
        "positions": [{"value": 1, "label": "OVERRIDE"}, {"value": 0, "label": "NORM"}],
    }, "above_below")
    p.label("HARS/SAS", "NAME", "HARS", "above")
    p.push("LAMP", 100, 488, {"id": "LAMP_TEST_BTN", "label": "SIGNAL LIGHTS LAMP TEST", "type": "button", "hold": BUTTON_HOLD})
    p.label("SIGNAL\nLIGHTS\nLAMP\nTEST", "NAME", "LAMP", "above")
    p.push("FDBA", 226, 488, {"id": "ALCP_FDBA_TEST", "label": "FIRE DETECT BLEED AIR LEAK TEST", "type": "button", "hold": BUTTON_HOLD})
    p.label("FIRE\nDETECT\nBLEED AIR\nLEAK TEST", "NAME", "FDBA", "above")


def sas_pair(p: Panel, title: str, key: str, y: int):
    p.mark(title, "NAME", "CX", y, "title of the two switches")
    for side, x in (("L", 92), ("R", 188)):
        p.toggle(f"{key}_{side}", x, y + 72, {
            "id": f"SASP_{key}_SAS_{side}", "label": f"{title} {side}", "type": "selector",
            "positions": [{"value": 1, "label": "ENGAGE"}, {"value": 0, "label": "OFF"}],
        }, "above_below")
        p.label(side, "POS", f"{key}_{side}", "left" if side == "L" else "right")


def sas_plate(g: PanelGroup):
    p = g.panel("SAS", 284, 824, 356, 0)
    sas_pair(p, "YAW SAS", "YAW", 52)
    sas_pair(p, "PITCH SAS", "PITCH", 232)
    p.knob("TRIM", "KNOB_M", 92, 480, {"id": "SASP_YAW_TRIM", "label": "YAW TRIM", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("YAW TRIM", "NAME", "TRIM", "above")
    p.knob_labels("TRIM", "lower_sides", "L", "R")
    p.toggle("MON", 196, 480, {
        "id": "SASP_MONITOR_TEST", "label": "MONITOR TEST", "type": "selector", "orient": "h", "rest": 1, "hold": 0.5,
        "positions": [{"value": 0, "label": "L", "momentary": True}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "R", "momentary": True}],
    }, "left_right")
    p.label("MONITOR\nTEST", "POS", "MON", "above")
    p.push("TRIM_BTN", 142, 660, {"id": "SASP_TO_TRIM", "label": "T/O TRIM", "type": "button", "hold": BUTTON_HOLD, "lamp": "TAKE_OFF_TRIM", "color": "green"})
    p.label("T/O TRIM", "NAME", "TRIM_BTN", "above")


def brake_pages() -> list[dict]:
    g = PanelGroup("BRAKE / AUX LT / SAS", "a10c", scroll=True)
    brake_plate(g)
    aux_plate(g)
    sas_plate(g)
    return [kit_page("BRAKE / AUX LT / SAS", [1, 1, 2, 2], g.build())]


# arrow heads of the emergency trim hat, in glyph units (width, height, paths)
ARROW_UP = (10, 9, [("M0.5 8.5L5 0.5L9.5 8.5Z", 1, True)])
ARROW_DOWN = (10, 9, [("M0.5 0.5L5 8.5L9.5 0.5Z", 1, True)])
ARROW_LEFT = (9, 10, [("M8.5 0.5L0.5 5L8.5 9.5Z", 1, True)])
ARROW_RIGHT = (9, 10, [("M0.5 0.5L8.5 5L0.5 9.5Z", 1, True)])


def emer_hat_button(name: str, label: str, value: int) -> dict:
    return {"id": f"EMER_TRIM_{name}", "label": label, "type": "button", "style": "flat", "bios": "EFCP_EMER_TRIM", "value": value, "rest": 0, "hold": BUTTON_HOLD}


def emer_disengage(p: Panel, name: str, label: str, bios: str, x: int, y: int, left: tuple, right: tuple):
    p.toggle(name, x, y, {
        "id": bios, "label": label, "type": "selector", "orient": "h",
        "positions": [{"value": 0, "label": "L"}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "R"}],
    }, "left_right")
    p.label(label.replace(" EMER ", " EMER\n"), "NAME", name, "above")
    for side, (lamp, legend), dx in (("L", left, -92), ("R", right, 92)):
        p.lamp(f"{name}_{side}", x + dx, y, {"id": lamp, "legend": legend, "color": "amber"})


def emer_pages() -> list[dict]:
    p = Panel("EMER FLT CTRL", 640, 544, "a10c")
    p.toggle("TRIM", 150, 148, {
        "id": "EFCP_TRIM_OVERRIDE", "label": "PITCH/ROLL TRIM", "type": "selector",
        "positions": [{"value": 1, "label": "NORM"}, {"value": 0, "label": "EMER OVERRIDE"}],
    }, "above_below")
    p.label("PITCH/ROLL\nTRIM", "NAME", "TRIM", "above")
    p.push_small("NOSE_DN", 436, 64, emer_hat_button("NOSE_DN", "NOSE DN", 1), ARROW_UP)
    p.push_small("L_WING", 376, 124, emer_hat_button("L_WING_DN", "L WING DN", 4), ARROW_LEFT)
    p.push_small("R_WING", 496, 124, emer_hat_button("R_WING_DN", "R WING DN", 2), ARROW_RIGHT)
    p.push_small("NOSE_UP", 436, 184, emer_hat_button("NOSE_UP", "NOSE UP", 3), ARROW_DOWN)
    p.label("NOSE DN", "POS", "NOSE_DN", "right")
    p.label("L WING\nDN", "POS", "L_WING", "left")
    p.label("R WING\nDN", "POS", "R_WING", "right")
    p.label("NOSE UP", "POS", "NOSE_UP", "right")
    emer_disengage(p, "AIL", "AILERON EMER DISENGAGE", "EFCP_AILERON_EMER_DISENGAGE", 164, 324, ("L_AILERON_EMER_DISENGAGE", "L-AIL"), ("R_AILERON_EMER_DISENGAGE", "R-AIL"))
    emer_disengage(p, "ELEV", "ELEVATOR EMER DISENGAGE", "EFCP_ELEVATOR_EMER_DISENGAGE", 476, 324, ("L_ELEVATOR_EMER_DISENGAGE", "L-ELEV"), ("R_ELEVATOR_EMER_DISENGAGE", "R-ELEV"))
    for name, label, bios, x in (("SPDBK", "SPD BK EMER RETR", "EFCP_SPDBK_EMER_RETR", 110), ("FLAP", "FLAP EMER RETR", "EFCP_FLAPS_EMER_RETR", 300)):
        p.toggle(name, x, 452, {"id": bios, "label": label, "type": "selector", "positions": [{"value": 1, "label": "UP"}, {"value": 0, "label": "DOWN"}]})
        p.label(label.replace(" EMER", "\nEMER"), "NAME", name, "above")
    p.toggle("MRFCS", 490, 452, {
        "id": "EFCP_MRFCS", "label": "FLT CONT", "type": "selector",
        "positions": [{"value": 1, "label": "NORM"}, {"value": 0, "label": "MAN REVERSION"}],
    }, "above_below")
    p.label("FLT CONT", "NAME", "MRFCS", "above")
    return [kit_page("EMER FLT CTRL", [5, 1, 1, 2], p.build())]


WHEEL_ANGLES = {8: [-40, -13, 13, 40, 140, 167, 193, 220], 4: [-40, -13, 13, 40]}


def iff_wheel(p: Panel, name: str, label: str, x: int, y: int, digits: int):
    positions = [{"value": n, "label": str(n), "angle": angle} for n, angle in enumerate(WHEEL_ANGLES[digits])]
    p.rotary(name, x, y, {"id": f"IFF_{name}", "label": label, "type": "selector", "style": "rotary", "positions": positions})


def iff_lamp_button(p: Panel, name: str, label: str, bios: str, x: int):
    p.push(name, x, 130, {"id": f"IFF_{bios}_TEST", "label": label, "type": "button", "hold": BUTTON_HOLD, "lamp": f"IFF_{bios}", "color": "green"})
    p.label(label, "NAME", name, "above")
    p.knob(f"{name}_DIM", "KNOB_S", x + 90, 130, {"id": f"IFF_{bios}_DIM", "label": f"{label} DIM", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("DIM", "NAME", f"{name}_DIM", "above")


def iff_pages() -> list[dict]:
    p = Panel("IFF", 640, 854, "a10c", scroll=True)
    iff_lamp_button(p, "REPLY", "REPLY", "REPLY", 90)
    iff_lamp_button(p, "TEST", "TEST", "TEST", 270)
    p.rotary("MASTER", 496, 150, {
        "id": "IFF_MASTER", "label": "MASTER", "type": "selector", "style": "rotary",
        "positions": [
            {"value": 0, "label": "OFF", "angle": 0}, {"value": 1, "label": "STBY", "angle": -52}, {"value": 2, "label": "LOW", "angle": -90},
            {"value": 3, "label": "NORM", "angle": -125}, {"value": 4, "label": "EMER", "angle": 125, "disabled": True},
        ],
    })
    p.label("MASTER", "NAME", "MASTER", "above")
    p.toggle("AUDIO", 112, 344, {
        "id": "IFF_OUT_AUDIO_LIGHT", "label": "AUDIO LIGHT", "type": "selector",
        "positions": [{"value": 2, "label": "AUDIO"}, {"value": 1, "label": "OUT"}, {"value": 0, "label": "LIGHT"}],
    }, "above_left_below")
    for key, label, x in (("M1", "M-1", 232), ("M2", "M-2", 340), ("M3", "M-3/A", 448), ("M4", "M-C", 556)):
        p.toggle(key, x, 344, {
            "id": f"IFF_TEST_{key}", "label": label, "type": "selector",
            "positions": [{"value": 2, "label": "TEST"}, {"value": 1, "label": "ON"}, {"value": 0, "label": "OUT"}],
        })
        p.label(label, "NAME", key, "above")
        p.label("ON", "POS", key, "left")
        p.label("OUT", "POS", key, "below")
    p.bracket("TEST", "TEST", 232, 556, 248)
    p.toggle("MODE4", 112, 536, {
        "id": "IFF_ON_OUT", "label": "MODE 4", "type": "selector",
        "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OUT"}],
    }, "above_below")
    p.label("MODE 4", "NAME", "MODE4", "above")
    p.mark("MODE 1", "NAME", 320, 438, "title of the two wheels")
    iff_wheel(p, "MODE1_WHEEL1", "MODE 1 WHEEL 1", 264, 536, 8)
    iff_wheel(p, "MODE1_WHEEL2", "MODE 1 WHEEL 2", 376, 536, 4)
    p.mark("MODE 3/A", "NAME", 320, 642, "title of the four wheels")
    for n, x in enumerate((152, 264, 376, 488), 1):
        iff_wheel(p, f"MODE3A_WHEEL{n}", f"MODE 3/A WHEEL {n}", x, 740, 8)
    return [kit_page("IFF", [3, 1, 2, 2], p.build())]


def int_knob(p: Panel, key: str, label: str, x: int, y: int):
    p.knob(key, "KNOB_S", x, y, {"id": f"INT_{key}_VOL", "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-150, 150]})
    p.label(label, "NAME", key, "above")
    p.chip(f"{key}_PULL", key, {
        "id": f"INT_{key}_UNMUTE", "label": f"{label} PULL", "type": "selector", "style": "chip", "legend": "PULL",
        "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "OUT"}],
    })


def intercom_pages() -> list[dict]:
    g = PanelGroup("INTERCOM / STALL", "a10c", scroll=True)
    p = g.panel("INTERCOM", 640, 468, 0, 0)
    rows = ((("INT", "INT"), ("FM", "FM"), ("UHF", "UHF"), ("VHF", "VHF")), (("AIM", "AIM"), ("IFF", "IFF"), ("ILS", "ILS"), ("TCN", "TCH")))
    for row, y in zip(rows, (96, 230)):
        for (key, label), x in zip(row, (106, 246, 386, 526)):
            int_knob(p, key, label, x, y)
    p.push("HM", 106, 382, {"id": "INT_HM", "label": "HM", "type": "button", "hold": BUTTON_HOLD})
    p.label("HM", "NAME", "HM", "above")
    p.rotary("MODE", 320, 382, {
        "id": "INT_MODE", "label": "INTERCOM SELECTOR", "type": "selector", "style": "rotary",
        "positions": [
            {"value": 0, "label": "INT", "angle": -60}, {"value": 1, "label": "FM", "angle": -25}, {"value": 2, "label": "VHF", "angle": 25},
            {"value": 3, "label": "HF", "angle": 65}, {"value": 4, "label": "BLANK", "angle": 100},
        ],
    })
    p.knob("VOL", "KNOB_M", 526, 382, {"id": "INT_VOL", "label": "VOL", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("VOL", "NAME", "VOL", "above")
    s = g.panel("STALL", 640, 176, 0, 484)
    s.mark("VOL", "NAME", "CX", 48, "placard text between the two names")
    for key, label, bios, x in (("STALL", "STALL", "STALL_VOL", 200), ("PEAK", "PEAK PRFM", "STALL_PEAK_VOL", 440)):
        s.knob(key, "KNOB_M", x, 104, {"id": bios, "label": f"{label} VOL", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
        s.label(label, "NAME", key, "above")
    return [kit_page("INTERCOM / STALL", [6, 1, 2, 2], g.build())]


VIEWS = [
    {"name": "COCKPIT", "seats": [0], "layout": "map", "lamps": MASTER_LAMPS, "controls": [], "links": []},
    *brake_pages(),
    *iff_pages(),
    *emer_pages(),
    *intercom_pages(),
]

CONTROL_NAMES = []

MPD_INDICATIONS = ()
MPD_SEATS = {}

TRIM_RELEASED = None

SEATS = [{"prefix": "", "label": "A-10C"}]
SEAT_OUTPUT = None
TRIM_SWITCH = None
