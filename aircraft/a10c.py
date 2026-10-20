from panel_kit import REF, Panel, PanelGroup

DCSBIOS_MODULE = "A-10C"
NAME = "A-10C"
DCS_NAMES = ["A-10C_2"]

KEYS = {}

KNOB_STEP = 3200
BUTTON_HOLD = 0.3
PWR_POSITIONS = [
    {"value": 2, "label": "DAY"},
    {"value": 1, "label": "NT"},
    {"value": 0, "label": "OFF"},
]

MASTER_LAMPS = [
    {"id": "MASTER_CAUTION", "label": "MASTER CAUTION", "color": "amber", "button": "UFC_MASTER_CAUTION"},
]
GUN_READY_LAMP = {"id": "GUN_READY", "label": "GUN READY", "color": "green"}
CANOPY_LAMP = {"id": "CANOPY_UNLOCKED", "label": "CANOPY UNLOCKED", "color": "red"}


def kit_page(name: str, cell: list, page: dict) -> dict:
    return {
        "name": name, "seats": [0], "panel": True, "layout": "panel", "map": cell, "box": page["box"],
        "lamps": MASTER_LAMPS, "print": page["print"], "art": page["art"], "controls": page["controls"],
        **({"indicators": page["indicators"]} if page["indicators"] else {}),
        **({"scroll": True} if page.get("scroll") else {}),
        "kit": True, "ref": list(REF),
    }


EMER_BRAKE = {
    "id": "EMER_BRAKE", "label": "EMER BRAKE", "type": "selector",
    "positions": [{"value": 1, "label": "PULLED"}, {"value": 0, "label": "IN"}],
}


def brake_plate(g: PanelGroup):
    p = g.panel("EMER BRAKE", 340, 240, 0, 0)
    p.toggle("SEAT", 90, 148, {
        "id": "SEAT_ADJUST", "label": "SEAT ADJUST", "type": "selector", "rest": 1, "hold": 0.5,
        "positions": [{"value": 2, "label": "UP", "momentary": True}, {"value": 1, "label": "HOLD"}, {"value": 0, "label": "DOWN", "momentary": True}],
    }, "above_side_below")
    p.toggle("BRAKE", 250, 148, EMER_BRAKE, "above_below")
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


def pump_pair(p: Panel, name: str, bios: str, title: str, word: str, mid: int, y: int):
    p.mark("BOOST PUMPS", "NAME", mid, y - 48, "title of the two switches")
    for side, dx in (("L", -56), ("R", 56)):
        p.toggle(f"{name}_{side}", mid + dx, y, {
            "id": f"FSCP_BOOST_{bios}_{side}", "label": f"{title} BOOST PUMP {side}", "type": "selector",
            "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}],
        })
        p.label(side, "POS", f"{name}_{side}", "left" if side == "L" else "right")
    p.mark(word, "POS", mid, y, "printed between the two switches")
    p.mark("OFF", "POS", mid, y + 46, "printed once below the two switches")


def fill_disable_pair(p: Panel, name: str, bios: str, title: str, word: str, mid: int, y: int):
    p.mark("FILL DISABLE", "NAME", mid, y - 52, "title of the two buttons")
    for side, dx in (("L", -58), ("R", 58)):
        p.round(f"{name}_{side}", mid + dx, y, {
            "id": f"FSCP_FD_{bios}_{side}", "label": f"{title} FILL DISABLE {side}", "type": "selector", "style": "cap",
            "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "OUT"}],
        })
        p.label(side, "POS", f"{name}_{side}", "left" if side == "L" else "right")
    p.mark(word, "POS", mid, y, "printed between the two buttons")


def fuel_plate(g: PanelGroup):
    p = g.panel("FUEL", 640, 472, 0, 0)
    p.toggle("EXT_WING", 64, 124, {
        "id": "FSCP_EXT_TANKS_WING", "label": "EXT TKS WING", "type": "selector",
        "positions": [{"value": 1, "label": "WING"}, {"value": 0, "label": "OFF"}],
    })
    p.toggle("EXT_FUS", 128, 124, {
        "id": "FSCP_EXT_TANKS_FUS", "label": "EXT TKS FUS", "type": "selector",
        "positions": [{"value": 1, "label": "FUS"}, {"value": 0, "label": "OFF"}],
    })
    p.label("WING", "POS", "EXT_WING", "above")
    p.label("FUS", "POS", "EXT_FUS", "above")
    p.mark("EXT TKS", "NAME", 96, 48, "title of the two switches")
    p.mark("OFF", "POS", 96, 170, "printed once below the two switches")
    p.toggle("GATE", 222, 124, {
        "id": "FSCP_TK_GATE", "label": "TK GATE", "type": "selector",
        "positions": [{"value": 1, "label": "OPEN"}, {"value": 0, "label": "CLOSE"}],
    }, "above_below")
    p.label("TK GATE", "NAME", "GATE", "above")
    p.toggle("CROSS", 324, 124, {
        "id": "FSCP_CROSSFEED", "label": "CROSS FEED", "type": "selector",
        "positions": [{"value": 1, "label": "CROSS FEED"}, {"value": 0, "label": "OFF"}],
    })
    p.label("CROSS\nFEED", "NAME", "CROSS", "above")
    p.label("OFF", "POS", "CROSS", "below")
    p.knob("RCVR_LT", "KNOB_M", 500, 124, {"id": "ALCP_RCVR_LTS", "label": "RCVR LT", "type": "knob", "step": KNOB_STEP, "sweep": [-130, 130]})
    p.label("RCVR LT", "NAME", "RCVR_LT", "above")
    p.knob_labels("RCVR_LT", "below_sides", "OFF", "BRT")
    pump_pair(p, "WING_PUMP", "WING", "WING", "WING", 140, 252)
    fill_disable_pair(p, "WING_FD", "WING", "WING", "WING", 378, 252)
    pump_pair(p, "MAIN_PUMP", "MAIN", "MAIN", "MAIN", 140, 380)
    fill_disable_pair(p, "MAIN_FD", "MAIN", "MAIN", "MAIN", 378, 380)
    p.toggle("RCVR", 560, 316, {
        "id": "FSCP_RCVR_LEVER", "label": "RCVR", "type": "selector",
        "positions": [{"value": 1, "label": "CLOSE"}, {"value": 0, "label": "OPEN"}],
    }, "above_below")
    p.label("RCVR", "NAME", "RCVR", "above")


def refuel_lights_plate(g: PanelGroup):
    p = g.panel("AIR REFUEL", 496, 112, 0, 488)
    for text, x in (("READY", 104), ("LATCHED", 248), ("DISCONNECT", 392)):
        p.lamp(text, x, 56, {"id": f"AIR_REFUEL_{text}", "legend": text, "color": "green"}, "LAMP_WIDE")


def fuel_pages() -> list[dict]:
    g = PanelGroup("FUEL SYSTEM", "a10c")
    fuel_plate(g)
    refuel_lights_plate(g)
    return [kit_page("FUEL SYSTEM", [1, 3, 1, 2], g.build())]


FLAPS_SWITCH = {
    "id": "FLAPS_SWITCH", "label": "FLAP LEVER", "type": "selector",
    "positions": [{"value": 2, "label": "UP"}, {"value": 1, "label": "MVR"}, {"value": 0, "label": "DN"}],
}


def flap_plate(g: PanelGroup):
    p = g.panel("FLAP LEVER", 176, 150, 0, 0)
    p.toggle("FLAP", 64, 76, FLAPS_SWITCH, "right_triple")


def throttle_toggle_pair(p: Panel, name: str, bios: str, label: str, positions: list, y: int, extra: dict):
    for side, x in (("L", 324), ("R", 384)):
        p.toggle(f"{name}_{side}", x, y, {"id": f"{bios}_{side}", "label": f"{label} {side}", "type": "selector", "positions": positions, **extra})
        p.label(side, "POS", f"{name}_{side}", "above")


ENG_THROTTLE = {side: {"id": f"ENG_THROTTLE_{side}", "label": f"{side} THROTTLE", "type": "bar", "max": 65535} for side in ("L", "R")}


def throttles_plate(g: PanelGroup):
    p = g.panel("THROTTLES", 448, 600, 192, 0)
    for side, x in (("L", 60), ("R", 116)):
        p.bar(f"THR_{side}", x, 170, ENG_THROTTLE[side])
        p.label(side, "POS", f"THR_{side}", "above")
    p.knob("FRICT", "KNOB_M", 190, 346, {"id": "ENGINE_THROTTLE_FRICTION", "label": "FRICTION", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("FRICTION", "NAME", "FRICT", "above")
    p.knob_labels("FRICT", "lower_sides", "DECR", "INCR")
    p.mark("ENG FUEL\nFLOW", "NAME", 354, 60, "title of the two switches")
    throttle_toggle_pair(p, "FLOW", "ENGINE_FUEL_FLOW", "ENG FUEL FLOW", [{"value": 1, "label": "NORM"}, {"value": 0, "label": "OVERRIDE"}], 166, {})
    p.mark("NORM", "POS", 354, 96, "printed once between the two switches")
    p.mark("OVERRIDE", "POS", 354, 212, "printed once below the two switches")
    p.mark("ENG OPER", "NAME", 354, 248, "title of the two switches")
    oper = [{"value": 2, "label": "IGN", "momentary": True}, {"value": 1, "label": "NORM"}, {"value": 0, "label": "MOTOR"}]
    throttle_toggle_pair(p, "OPER", "ENGINE_OPER", "ENG OPER", oper, 354, {"rest": 1, "hold": 0.5})
    p.mark("IGN", "POS", 354, 284, "printed once between the two switches")
    p.mark("MOTOR", "POS", 354, 400, "printed once below the two switches")
    p.toggle("APU", 354, 508, {
        "id": "ENGINE_APU_START", "label": "APU START", "type": "selector",
        "positions": [{"value": 1, "label": "START"}, {"value": 0, "label": "OFF"}],
    }, "above_below")
    p.label("APU", "NAME", "APU", "above")
    p.push("SILENCE", 110, 484, {"id": "GEAR_HORN_SILENCE", "label": "LDG WARN SILENCE", "type": "button", "hold": BUTTON_HOLD})
    p.label("LDG WARN\nSILENCE", "NAME", "SILENCE", "above")


def throttle_pages() -> list[dict]:
    g = PanelGroup("THROTTLE", "a10c")
    flap_plate(g)
    throttles_plate(g)
    return [kit_page("THROTTLE", [2, 3, 2, 2], g.build())]


def laste_plate(g: PanelGroup):
    p = g.panel("LASTE", 640, 284, 0, 0)
    p.toggle("EAC", 72, 150, {
        "id": "LASTE_EAC", "label": "EAC", "type": "selector",
        "positions": [{"value": 1, "label": "ARM"}, {"value": 0, "label": "OFF"}],
    }, "right_pair")
    p.toggle("ALTM", 176, 150, {
        "id": "LASTE_RDR_ALTM", "label": "RDR ALTM", "type": "selector",
        "positions": [{"value": 1, "label": "NRM"}, {"value": 0, "label": "DIS"}],
    }, "right_pair")
    p.push("ENGAGE", 320, 150, {"id": "LASTE_AP_TOGGLE", "label": "AUTOPILOT ENGAGE / DISENGAGE", "type": "button", "hold": BUTTON_HOLD})
    p.label("ENGAGE/\nDISENGAGE", "NAME", "ENGAGE", "below")
    p.toggle("AP", 450, 150, {
        "id": "LASTE_AP_MODE", "label": "AUTOPILOT SELECT", "type": "selector",
        "positions": [{"value": 2, "label": "PATH"}, {"value": 1, "label": "ALT/HDG"}, {"value": 0, "label": "ALT"}],
    }, "right_triple")
    p.bracket("AUTOPILOT", "AUTOPILOT", 270, 490, 64)
    p.mark("LASTE", "TITLE", 556, 64, "panel title")


def seat_plate(g: PanelGroup):
    p = g.panel("SEAT ARM", 184, 216, 0, 300)
    p.toggle("SEAT", 92, 124, {
        "id": "SEAT_ARM", "label": "SEAT ARM", "type": "selector",
        "positions": [{"value": 1, "label": "DISARM"}, {"value": 0, "label": "ARM"}],
    }, "above_below")
    p.label("SEAT ARM", "NAME", "SEAT", "above")


def laste_pages() -> list[dict]:
    g = PanelGroup("LASTE", "a10c")
    laste_plate(g)
    seat_plate(g)
    return [kit_page("LASTE", [4, 3, 1, 2], g.build())]


def step_rocker(bios: str, label: str) -> dict:
    return {"id": bios, "label": label, "type": "hat", "ud": bios, "steps": "fixed", "positions": {"up": "tri-up", "down": "tri-down"}}


def readout(bios: str, label: str, cols: int) -> dict:
    return {"id": bios, "label": label, "type": "display", "cols": cols, "ids": [bios]}


def uhf_pages() -> list[dict]:
    p = Panel("UHF", 640, 584, "a10c")
    p.push("TEST", 84, 96, {"id": "UHF_TEST", "label": "TEST DISPLAY", "type": "button", "hold": BUTTON_HOLD})
    p.label("TEST\nDISPLAY", "POS", "TEST", "below")
    p.push("LOAD", 218, 96, {"id": "UHF_LOAD", "label": "LOAD", "type": "button", "guard": True, "cover": "UHF_COVER", "hold": BUTTON_HOLD})
    p.label("LOAD", "NAME", "LOAD", "below")
    p.display("CHAN", 372, 96, 72, 56, readout("UHF_PRESET", "CHAN", 2))
    p.label("CHAN", "NAME", "CHAN", "above")
    p.rocker("PRESET", 450, 96, step_rocker("UHF_PRESET_SEL", "CHAN"))
    p.push("STATUS", 556, 96, {"id": "UHF_STATUS", "label": "STATUS", "type": "button", "hold": BUTTON_HOLD})
    p.label("STATUS", "POS", "STATUS", "below")
    p.display("FREQ", 320, 230, 288, 64, readout("UHF_FREQUENCY", "FREQUENCY", 7))
    for bios, label, x in (("100MHZ_SEL", "100", 104), ("10MHZ_SEL", "10", 212), ("1MHZ_SEL", "1", 320), ("POINT1MHZ_SEL", ".1", 428), ("POINT25_SEL", ".025", 536)):
        p.rocker(bios, x, 338, step_rocker(f"UHF_{bios}", label))
    p.rotary("FUNC", 140, 488, {
        "id": "UHF_FUNCTION", "label": "FUNCTION", "type": "selector", "style": "rotary",
        "positions": [
            {"value": 0, "label": "OFF", "angle": -75}, {"value": 1, "label": "MAIN", "angle": -40},
            {"value": 2, "label": "BOTH", "angle": 40}, {"value": 3, "label": "ADF", "angle": 75, "disabled": True},
        ],
    })
    p.rotary("MODE", 500, 488, {
        "id": "UHF_MODE", "label": "MODE", "type": "selector", "style": "rotary",
        "positions": [{"value": 0, "label": "MNL", "angle": -70}, {"value": 1, "label": "PRESET", "angle": 0}, {"value": 2, "label": "GRD", "angle": 70}],
    })
    p.knob("VOL", "KNOB_S", 290, 490, {"id": "UHF_VOL", "label": "VOL", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("VOL", "NAME", "VOL", "above")
    p.toggle("SQL", 370, 490, {
        "id": "UHF_SQUELCH", "label": "SQUELCH", "type": "selector",
        "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}],
    }, "above_below")
    p.label("SQUELCH", "NAME", "SQL", "above")
    return [kit_page("UHF", [6, 3, 1, 2], p.build())]


def vhf_pages() -> list[dict]:
    p = Panel("VHF FM", 640, 582, "a10c")
    p.knob("VOL", "KNOB_S", 100, 100, {"id": "VHFFM_VOL", "label": "VOL", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("VOL", "NAME", "VOL", "above")
    p.toggle("SQL", 100, 216, {
        "id": "VHFFM_SQUELCH", "label": "SQUELCH", "type": "selector",
        "positions": [{"value": 2, "label": "SQ DIS"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "TONE"}],
    })
    p.label("SQ DIS", "POS", "SQL", "above")
    p.label("TONE", "POS", "SQL", "below")
    p.display("FREQ", 330, 84, 336, 64, readout("VHF_FM_FREQUENCY_S", "FREQUENCY", 7))
    for bios, label, x in (("FREQ1", "10", 222), ("FREQ2", "1", 302), ("FREQ3", ".1", 382), ("FREQ4", ".025", 462)):
        p.rocker(bios, x, 190, step_rocker(f"VHFFM_{bios}", label))
    p.rotary("SEL", 170, 380, {
        "id": "VHFFM_FREQEMER", "label": "FREQUENCY SELECTION", "type": "selector", "style": "rotary",
        "positions": [
            {"value": 0, "label": "EMER FM", "angle": -75}, {"value": 1, "label": "EMER AM", "angle": -25},
            {"value": 2, "label": "MAN", "angle": 25}, {"value": 3, "label": "PRE", "angle": 75},
        ],
    }, labels="fan")
    p.display("PRESET", 300, 380, 72, 56, readout("VHFFM_PRESET_STR", "PRESET", 2))
    p.label("PRESET", "NAME", "PRESET", "above")
    p.rocker("WHEEL", 380, 380, step_rocker("VHFFM_PRESET", "PRE"))
    p.rotary("MODE", 510, 380, {
        "id": "VHFFM_MODE", "label": "MODE", "type": "selector", "style": "rotary",
        "positions": [{"value": 0, "label": "OFF", "angle": -70}, {"value": 1, "label": "TR", "angle": 0}, {"value": 2, "label": "DF", "angle": 70, "disabled": True}],
    })
    p.push("LOAD", 300, 472, {"id": "VHFFM_LOAD", "label": "LOAD", "type": "button", "hold": BUTTON_HOLD})
    p.label("LOAD", "NAME", "LOAD", "below")
    return [kit_page("VHF FM", [7, 3, 1, 2], p.build())]


ARC_SCREEN = (
    "FREQUENCY", "MODULATION", "PREV_MANUAL_FREQ", "SELECTED_RT", "XMIT_RECV", "ACTIVE_CHANNEL", "ACTIVE_ECCM_CHANNEL", "COMSEC_MODE", "COMSEC_SUBMODE",
    "COMSEC_MENU_MODE", "KY_SUBMODE", "SG_TIME", "LOAD_TIME", "PREV", "MORE", "EXIT_SEND", "EXIT_RECV", "EXIT_LOAD",
)


def arc_button(p: Panel, name: str, label: str, x: int, y: int):
    p.round(name, x, y, {"id": f"ARC210_{name}", "label": label, "type": "button", "shape": "round", "hold": BUTTON_HOLD})


def arc_dial(p: Panel, name: str, label: str, x: int, y: int, words: tuple):
    p.rotary(name, x, y, {
        "id": f"ARC210_{name}", "label": label, "type": "selector", "style": "rotary",
        "positions": [{"value": n, "label": word, "angle": angle} for n, (word, angle) in enumerate(zip(words, (-135, -90, -45, 0, 45, 90, 135)))],
    }, labels="fan")


def radio_pages() -> list[dict]:
    p = Panel("RADIO 1", 640, 1040, "a10c", scroll=True)
    for name, label, x in (("TOD_SEND", "TOD SND", 100), ("TOD_REC", "TOD RCV", 240), ("GPS", "GPS", 380), ("TRANS_REC_SEL", "RT SELECT", 520)):
        p.push(name, x, 84, {"id": f"ARC210_{name}", "label": label, "type": "button", "hold": BUTTON_HOLD})
        p.label(label, "POS", name, "below")
    p.mark("EMER\nTOD", "POS", 170, 84, "printed between TOD SND and TOD RCV")
    p.display("SCREEN", 260, 334, 300, 340, {"id": "ARC210_SCREEN", "label": "ARC-210", "type": "display", "cols": 20, "ids": [f"ARC210_{field}" for field in ARC_SCREEN]})
    for name, label, y in (("FSK_UP", "LINE 1", 224), ("FSK_MID", "LINE 2", 334), ("FSK_LOW", "LINE 3", 444)):
        p.push_small(name, 64, y, {"id": f"ARC210_{name}", "label": label, "type": "button", "style": "flat", "hold": BUTTON_HOLD}, ARROW_RIGHT)
    p.push_small("BRIGHT_INC", 64, 560, {"id": "ARC210_BRIGHT_INC", "label": "BRIGHTNESS UP", "type": "button", "style": "flat", "hold": BUTTON_HOLD}, ARROW_UP)
    p.push_small("BRIGHT_DEC", 64, 624, {"id": "ARC210_BRIGHT_DEC", "label": "BRIGHTNESS DOWN", "type": "button", "style": "flat", "hold": BUTTON_HOLD}, ARROW_DOWN)
    arc_button(p, "SQUELCH", "SQL", 526, 200)
    p.label("SQL", "NAME", "SQUELCH", "left")
    arc_button(p, "MENU", "MENU / TIME", 470, 320)
    p.label("MENU", "POS", "MENU", "above")
    p.label("TIME", "POS", "MENU", "below")
    arc_button(p, "AMP_FREQ_MODUL", "AM/FM", 566, 320)
    p.label("AM/FM", "POS", "AMP_FREQ_MODUL", "above")
    arc_button(p, "TRANS_REC_FUNC", "XMT/RCV / SEND", 470, 450)
    p.label("XMT/RCV", "POS", "TRANS_REC_FUNC", "above")
    p.label("SEND", "POS", "TRANS_REC_FUNC", "below")
    arc_button(p, "OFF_FREQ", "OFFSET / RCV", 566, 450)
    p.label("OFFSET", "POS", "OFF_FREQ", "above")
    p.label("RCV", "POS", "OFF_FREQ", "below")
    arc_button(p, "ENTER", "ENTER", 566, 570)
    p.label("ENTER", "POS", "ENTER", "left")
    for bios, label, x in (("100MHZ_SEL", "100", 130), ("10MHZ_SEL", "10", 230), ("1MHZ_SEL", "1", 330), ("100KHZ_SEL", ".1", 430), ("25KHZ_SEL", ".025", 530)):
        p.rocker(bios, x, 700, step_rocker(f"ARC210_{bios}", label))
    arc_dial(p, "MASTER", "LEFT MODE", 150, 880, ("OFF", "TR\u00a0G", "TR", "ADF", "CHG PRST", "TEST", "ZERO (PULL)"))
    p.rocker("CHN_KNB", 310, 880, {**step_rocker("ARC210_CHN_KNB", "CHAN"), "steps": KNOB_STEP})
    arc_dial(p, "SEC_SW", "RIGHT MODE", 470, 880, ("ECCM MASTER", "ECCM", "PRST", "MAN", "MAR", "243", "121 (PULL)"))
    return [kit_page("RADIO 1", [5, 3, 1, 2], p.build())]


def fire_pages() -> list[dict]:
    p = Panel("FIRE / JETT", 640, 540, "a10c")
    for title, name, bios, lamp, x in (
        ("FIRE L ENG", "LENG", "FIRE_LENG_PULL", "L_ENG_FIRE", 100),
        ("FIRE APU", "APU", "FIRE_APU_PULL", "APU_FIRE", 290),
        ("FIRE R ENG", "RENG", "FIRE_RENG_PULL", "R_ENG_FIRE", 480),
    ):
        p.toggle(name, x, 152, {
            "id": bios, "label": title, "type": "selector", "guard": True,
            "positions": [{"value": 1, "label": "PULL"}, {"value": 0, "label": "IN"}],
        }, "above_below")
        p.label(title, "POS", name, "above")
        p.lamp(f"{name}_FIRE", x + 84, 152, {"id": lamp, "legend": "FIRE", "color": "red"})
    p.rule("RULE_LENG_APU", 225, 36, 250)
    p.rule("RULE_APU_RENG", 415, 36, 250)
    p.plunger("JETT", 160, 400, {"id": "EXT_STORES_JETTISON", "label": "EXT STORES JETT", "type": "button", "shape": "round", "style": "plunger", "guard": True, "hold": BUTTON_HOLD})
    p.label("EXT STORES\nJETT", "POS", "JETT", "above")
    p.toggle("DISCH", 480, 400, {
        "id": "FIRE_EXT_DISCH", "label": "FIRE EXTING DISCH", "type": "selector", "orient": "h", "guard": True,
        "positions": [{"value": 0, "label": "L"}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "R"}],
    }, "left_right")
    p.label("FIRE\nEXTING\nDISCH", "POS", "DISCH", "above")
    p.rule("RULE_JETT_DISCH", 320, 290, 504)
    return [kit_page("FIRE / JETT", [2, 5, 1, 4], p.build())]


def cmsc_arrow(name: str, label: str) -> dict:
    return {"id": f"CMSC_{name}", "label": label, "type": "button", "style": "flat", "hold": BUTTON_HOLD}


def cmsc_pages() -> list[dict]:
    p = Panel("CMSC", 640, 484, "a10c")
    p.push_small("JMR_BTN", 64, 110, cmsc_arrow("JMR", "JMR"), ARROW_RIGHT)
    p.push_small("MWS_BTN", 64, 230, cmsc_arrow("MWS", "MWS"), ARROW_RIGHT)
    p.display("JMR", 222, 110, 220, 60, readout("CMSC_TXT_JMR", "JMR", 8))
    p.label("JMR", "NAME", "JMR", "above")
    p.display("MWS", 222, 230, 220, 60, readout("CMSC_TXT_MWS", "MWS", 8))
    p.label("MWS", "NAME", "MWS", "above")
    p.display("CHAFF_FLARE", 486, 110, 220, 60, readout("CMSC_TXT_CHAFF_FLARE", "CHAFF / FLARE", 8))
    p.mark("CHAFF", "NAME", 432, 62, "title of the left half of the window")
    p.mark("FLARE", "NAME", 540, 62, "title of the right half of the window")
    p.lamp("PRIO", 412, 186, {"id": "CMSC_PRIO", "legend": "", "color": "green"})
    p.lamp("UNKN", 560, 186, {"id": "CMSC_UNKN", "legend": "", "color": "green"})
    p.bracket("RWR", "RWR", 384, 536, 236)
    p.push("PRI", 412, 320, {"id": "CMSC_PRI", "label": "RWR PRI", "type": "button", "legend": "PRI", "hold": BUTTON_HOLD})
    p.push("SEP", 508, 320, {"id": "CMSC_SEP", "label": "RWR SEP", "type": "button", "legend": "SEP", "hold": BUTTON_HOLD})
    for name, label, bios, x in (("BRT", "BRT", "CMSC_BRT", 120), ("AUD", "AUD", "CMSC_RWR_VOL", 240)):
        p.knob(name, "KNOB_S", x, 420, {"id": bios, "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
        p.label(label, "NAME", name, "above")
    p.lamp("ML", 360, 420, {"id": "CMSC_LAUNCH", "legend": "ML", "color": "red"})
    return [kit_page("CMSC", [3, 6, 1, 2], p.build())]


ANTI_SKID_SWITCH = {
    "id": "ANTI_SKID_SWITCH", "label": "ANTI-SKID", "type": "selector",
    "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}],
}
LANDING_LIGHTS = {
    "id": "LANDING_LIGHTS", "label": "LIGHTS LAND", "type": "selector",
    "positions": [{"value": 2, "label": "LAND"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "TAXI"}],
}
GEAR_LEVER = {
    "id": "GEAR_LEVER", "label": "LANDING GEAR", "type": "selector",
    "positions": [{"value": 1, "label": "UP"}, {"value": 0, "label": "DOWN"}],
}


def gear_plate(g: PanelGroup):
    p = g.panel("LANDING GEAR", 436, 600, 0, 0)
    p.toggle("SKID", 100, 156, ANTI_SKID_SWITCH)
    p.label("ANTI-\nSKID", "NAME", "SKID", "above")
    p.label("OFF", "POS", "SKID", "below")
    p.toggle("LAND", 336, 156, LANDING_LIGHTS, "above_side_below")
    p.label("LIGHTS\nLAND", "NAME", "LAND", "above")
    for side, x in (("L", 80), ("N", 160), ("R", 240)):
        p.lamp(f"{side}_SAFE", x, 262, {"id": f"GEAR_{side}_SAFE", "legend": f"{side} SAFE", "color": "green"})
    p.bar("FLAPS", 90, 450, {"id": "FLAP_POS", "label": "FLAPS DEGREES", "type": "bar", "max": 65535})
    p.label("FLAPS\nDEGREES", "POS", "FLAPS", "above")
    p.push("SILENCE", 215, 400, {"id": "GEAR_HORN_SILENCE", "label": "LDG WARN SILENCE", "type": "button", "hold": BUTTON_HOLD})
    p.label("LDG WARN\nSILENCE", "NAME", "SILENCE", "above")
    p.lamp("HANDLE", 215, 500, {"id": "HANDLE_GEAR_WARNING", "legend": "LGD GEAR DOWN", "color": "red"}, "LAMP_WIDE")
    p.round("DOWNLOCK", 336, 316, {"id": "DOWNLOCK_OVERRIDE", "label": "DOWNLOCK OVERRIDE", "type": "button", "shape": "round", "hold": BUTTON_HOLD})
    p.hazard("DOWNLOCK", "DOWNLOCK\nOVERRIDE", "POS", "above")
    p.toggle("GEAR", 336, 490, GEAR_LEVER, "above_below")


def aux_gear_plate(g: PanelGroup):
    p = g.panel("AUX GEAR", 188, 600, 452, 0)
    p.toggle("AUX", 94, 200, {
        "id": "AUX_GEAR", "label": "AUX GEAR", "type": "selector",
        "positions": [{"value": 1, "label": "PULLED"}, {"value": 0, "label": "IN"}],
    }, "above_below")
    p.label("AUX\nGEAR", "NAME", "AUX", "above")
    p.push("LOCK", 94, 400, {"id": "AUX_GEAR_LOCK", "label": "AUX GEAR LOCK", "type": "button", "hold": BUTTON_HOLD})
    p.label("LOCK", "NAME", "LOCK", "above")


def gear_pages() -> list[dict]:
    g = PanelGroup("LANDING GEAR", "a10c")
    gear_plate(g)
    aux_gear_plate(g)
    return [kit_page("LANDING GEAR", [5, 5, 2, 1], g.build())]


def ahcp_switch(label: str, bios: str, positions: tuple) -> dict:
    return {"id": bios, "label": label, "type": "selector", "positions": [{"value": value, "label": text} for value, text in positions]}


def ahcp_toggle(p: Panel, name: str, x: int, y: int, control: dict):
    p.toggle(name, x, y, control, "right_triple" if len(control["positions"]) == 3 else "right_pair")


AHCP_ARM = ((2, "ARM"), (1, "SAFE"), (0, "TRAIN"))
AHCP_ON_OFF = ((1, "ON"), (0, "OFF"))
AHCP_MASTER_ARM = ahcp_switch("MASTER ARM", "AHCP_MASTER_ARM", AHCP_ARM)
AHCP_GUNPAC = ahcp_switch("GUN/PAC ARM", "AHCP_GUNPAC", ((2, "ARM"), (1, "SAFE"), (0, "GUNARM")))
AHCP_LASER_ARM = ahcp_switch("LASER ARM", "AHCP_LASER_ARM", AHCP_ARM)
AHCP_TGP = ahcp_switch("TGP", "AHCP_TGP", AHCP_ON_OFF)
HARS_FAST_ERECT = {"id": "HARS_FAST_ERECT", "label": "HARS FAST ERECT", "type": "button", "hold": BUTTON_HOLD}


def ahcp_pages() -> list[dict]:
    g = PanelGroup("AHCP", "a10c", scroll=True)
    p = g.panel("AHCP", 640, 510, 0, 0)
    for name, title, x, y, control in (
        ("MASTER", "MASTER ARM", 190, 100, AHCP_MASTER_ARM),
        ("GUNPAC", "GUN/PAC ARM", 450, 100, AHCP_GUNPAC),
        ("LASER", "LASER ARM", 190, 212, AHCP_LASER_ARM),
        ("TGP", "TGP", 450, 212, AHCP_TGP),
        ("ALT", "ALT SCE", 110, 324, ahcp_switch("ALT SCE", "AHCP_ALT_SCE", ((2, "BARO"), (1, "DELTA"), (0, "RADAR")))),
        ("DAYNIGHT", None, 300, 324, ahcp_switch("HUD MODE DAY/NIGHT", "AHCP_HUD_DAYNIGHT", ((1, "DAY"), (0, "NIGHT")))),
        ("HUDMODE", None, 500, 324, ahcp_switch("HUD MODE NORM/STBY", "AHCP_HUD_MODE", ((1, "NORM"), (0, "STBY")))),
        ("CICU", "CICU", 110, 436, ahcp_switch("CICU", "AHCP_CICU", AHCP_ON_OFF)),
        ("JTRS", "JTRS", 300, 436, ahcp_switch("JTRS", "AHCP_JTRS", AHCP_ON_OFF)),
        ("IFFCC", "IFFCC", 500, 436, ahcp_switch("IFFCC", "AHCP_IFFCC", ((2, "ON"), (1, "TEST"), (0, "OFF")))),
    ):
        ahcp_toggle(p, name, x, y, control)
        if title:
            p.mark(title, "NAME", x, y - 52, "title above the position labels of the switch")
    p.mark("HUD MODE", "NAME", 400, 272, "title of the two switches")
    h = g.panel("HARS FAST ERECT", 320, 188, 0, 526)
    h.push("ERECT", 160, 110, HARS_FAST_ERECT)
    h.label("HARS FAST ERECT", "NAME", "ERECT", "above")
    return [kit_page("AHCP", [5, 6, 2, 1], g.build())]


def nmsp_button(p: Panel, name: str, label: str, bios: str, x: int, y: int):
    p.push(name, x, y, {"id": f"NMSP_{bios}_BTN", "label": label, "type": "button", "hold": BUTTON_HOLD, "lamp": f"NMSP_{bios}_LED", "legend": label, "color": "green"})


def nmsp_pages() -> list[dict]:
    p = Panel("NMSP", 640, 318, "a10c")
    nmsp_button(p, "HARS", "HARS", "HARS", 96, 120)
    p.toggle("PTR", 232, 120, {
        "id": "NMSP_ABLE_STOW", "label": "PTR", "type": "selector", "orient": "h",
        "positions": [{"value": 0, "label": "ABLE"}, {"value": 1, "label": "STOW"}],
    }, "left_right_pair")
    p.label("PTR", "NAME", "PTR", "above")
    nmsp_button(p, "EGI", "EGI", "EGI", 400, 120)
    for name, label, bios, x in (("STRPT", "STR PT", "STEERPT", 96), ("ANCHR", "ANCHR", "ANCHR", 212), ("TCN", "TCN", "TCN", 328), ("ILS", "ILS", "ILS", 444)):
        nmsp_button(p, name, label, bios, x, 240)
    p.mark("HOMING", "NAME", 552, 60, "title of the two lamps")
    p.lamp("UHF", 552, 112, {"id": "NMSP_UHF_LED", "legend": "UHF", "color": "amber"})
    p.lamp("FM", 552, 168, {"id": "NMSP_FM_LED", "legend": "FM", "color": "amber"})
    return [kit_page("NMSP", [5, 7, 2, 1], p.build())]


def cmsp_toggle(p: Panel, name: str, label: str, x: int, disabled: bool):
    p.toggle(name, x, 370, {
        "id": f"CMSP_{name}", "label": label, "type": "selector", "rest": 1, "hold": 0.5,
        "positions": [{"value": 2, "label": "MENU", "momentary": True, **({"disabled": True} if disabled else {})}, {"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}],
    })
    p.label(name, "NAME", name, "above")


CMSP_DISPLAY = {"id": "CMSP1", "label": "CMSP", "type": "display", "cols": 19, "ids": ["CMSP1", "CMSP2"]}


def cmsp_pages() -> list[dict]:
    p = Panel("CMSP", 640, 488, "a10c")
    p.display("DISPLAY", 236, 80, 400, 88, CMSP_DISPLAY)
    p.rocker("NXT", 486, 96, {"id": "CMSP_UPDN", "label": "NXT", "type": "hat", "ud": "CMSP_UPDN", "hold": BUTTON_HOLD, "positions": {"up": "tri-up", "down": "tri-down"}})
    p.push("RTN", 560, 96, {"id": "CMSP_RTN", "label": "RTN", "type": "button", "legend": "RTN", "hold": BUTTON_HOLD})
    for n, x in enumerate((86, 186, 286, 386), 1):
        p.push_small(f"SET{n}", x, 172, {"id": f"CMSP_ARW{n}", "label": f"SET {n}", "type": "button", "style": "flat", "hold": BUTTON_HOLD}, ARROW_UP)
    p.mark("SET", "POS", 236, 172, "printed between the second and third SET button")
    p.toggle("JTSN", 486, 232, {
        "id": "CMSP_JTSN", "label": "JTSN", "type": "selector", "guard": True,
        "positions": [{"value": 1, "label": "JTSN"}, {"value": 0, "label": "OFF"}],
    })
    p.label("JTSN", "NAME", "JTSN", "above")
    p.knob("BRT", "KNOB_S", 566, 232, {"id": "CMSP_BRT", "label": "BRT", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("BRT", "NAME", "BRT", "above")
    p.bracket("SYSTEM", "SYSTEM", 42, 378, 272)
    for name, label, x, disabled in (("MWS", "MWS", 70, True), ("JMR", "JMR", 158, True), ("RWR", "RWR", 262, False), ("DISP", "DISP", 350, False)):
        cmsp_toggle(p, name, label, x, disabled)
    for text, y in (("MENU", 342), ("ON", 370), ("OFF", 398)):
        p.mark(text, "POS", 210, y, "printed once between the JMR and RWR switches")
    p.rotary("MODE", 496, 370, {
        "id": "CMSP_MODE", "label": "MODE", "type": "selector", "style": "rotary",
        "positions": [
            {"value": 0, "label": "OFF", "angle": -130}, {"value": 1, "label": "STBY", "angle": -85}, {"value": 2, "label": "MAN", "angle": -40},
            {"value": 3, "label": "SEMI", "angle": 5}, {"value": 4, "label": "AUTO", "angle": 50},
        ],
    }, labels="fan")
    p.label("MODE", "NAME", "MODE", "below")
    return [kit_page("CMSP", [1, 9, 1, 2], p.build())]


CAUTION_LAMPS = (
    ("CL_A1", "ENG START\nCYCLE"), ("CL_A2", "L-HYD\nPRESS"), ("CL_A3", "R-HYD\nPRESS"), ("CL_A4", "GUN\nUNSAFE"),
    ("CL_B1", "ANTI-\nSKID"), ("CL_B2", "L-HYD\nRES"), ("CL_B3", "R-HYD\nRES"), ("CL_B4", "OXY\nLOW"),
    ("CL_C1", "ELEV\nDISENG"), ("CL_C2", ""), ("CL_C3", "SEAT NOT\nARMED"), ("CL_C4", "BLEED AIR\nLEAK"),
    ("CL_D1", "AIL\nDISENG"), ("CL_D2", "L-AIL\nTAB"), ("CL_D3", "R-AIL\nTAB"), ("CL_D4", "SERVICE AIR\nHOT"),
    ("CL_E1", "PITCH\nSAS"), ("CL_E2", "L-ENG\nHOT"), ("CL_E3", "R-ENG\nHOT"), ("CL_E4", "WINDSHIELD\nHOT"),
    ("CL_F1", "YAW\nSAS"), ("CL_F2", "L-ENG\nOIL PRESS"), ("CL_F3", "R-ENG\nOIL PRESS"), ("CL_F4", "CICU"),
    ("CL_G1", "GCAS"), ("CL_G2", "L-MAIN\nPUMP"), ("CL_G3", "R-MAIN\nPUMP"), ("CL_G4", ""),
    ("CL_H1", "LASTE"), ("CL_H2", "L-WING\nPUMP"), ("CL_H3", "R-WING\nPUMP"), ("CL_H4", "HARS"),
    ("CL_I1", "IFF\nMODE-4"), ("CL_I2", "L-MAIN\nFUEL LOW"), ("CL_I3", "R-MAIN\nFUEL LOW"), ("CL_I4", "L-R TKS\nUNEQUAL"),
    ("CL_J1", "EAC"), ("CL_J2", "L-FUEL\nPRESS"), ("CL_J3", "R-FUEL\nPRESS"), ("CL_J4", "NAV"),
    ("CL_K1", "STALL\nSYS"), ("CL_K2", "L-CONV"), ("CL_K3", "R-CONV"), ("CL_K4", "CADC"),
    ("CL_L1", "APU\nGEN"), ("CL_L2", "L-GEN"), ("CL_L3", "R-GEN"), ("CL_L4", "INST\nINV"),
)


def caution_pages() -> list[dict]:
    p = Panel("CAUTION", 640, 640, "a10c", scroll=True)
    for n, (bios, legend) in enumerate(CAUTION_LAMPS):
        row, column = divmod(n, 4)
        p.lamp(bios, 104 + 144 * column, 56 + 48 * row, {"id": bios, "legend": legend, "color": "amber"}, "LAMP_WIDE")
    return [kit_page("CAUTION", [2, 9, 2, 2], p.build())]


def aap_toggle(p: Panel, name: str, label: str, bios: str, x: int):
    p.toggle(name, x, 100, {
        "id": bios, "label": label, "type": "selector",
        "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}],
    }, "right_pair")
    p.label(name, "NAME", name, "above")


AAP_STEERPT = {
    "id": "AAP_STEERPT", "label": "STEER PT", "type": "selector", "style": "rotary",
    "positions": [{"value": 0, "label": "FLT PLAN", "angle": -90}, {"value": 1, "label": "MARK", "angle": -50}, {"value": 2, "label": "MISSION", "angle": 0}],
}
AAP_PAGE = {
    "id": "AAP_PAGE", "label": "PAGE", "type": "selector", "style": "rotary",
    "positions": [
        {"value": 0, "label": "OTHER", "angle": -90}, {"value": 1, "label": "POSITION", "angle": -50},
        {"value": 2, "label": "STEER", "angle": 0}, {"value": 3, "label": "WAYPT", "angle": 50},
    ],
}


def aap_plate(g: PanelGroup):
    p = g.panel("AAP", 640, 360, 0, 0)
    aap_toggle(p, "CDU", "CDU POWER", "AAP_CDUPWR", 200)
    aap_toggle(p, "EGI", "EGI POWER", "AAP_EGIPWR", 440)
    p.rotary("STEERPT", 190, 240, AAP_STEERPT)
    p.label("STEER PT", "NAME", "STEERPT", "below")
    p.rotary("PAGE", 480, 240, AAP_PAGE)
    p.label("PAGE", "NAME", "PAGE", "below")
    p.toggle("STEER", 283, 240, {
        "id": "AAP_STEER", "label": "STEER", "type": "selector", "rest": 1, "hold": 0.5,
        "positions": [{"value": 2, "label": "UP", "momentary": True}, {"value": 1, "label": "CENTER"}, {"value": 0, "label": "DOWN", "momentary": True}],
    })
    p.label("STEER", "NAME", "STEER", "below")


def ils_plate(g: PanelGroup):
    p = g.panel("ILS", 640, 348, 0, 376)
    p.mark("ILS", "TITLE", "CX", 58, "panel title")
    p.rotary("PWR", 140, 118, {
        "id": "ILS_PWR", "label": "POWER", "type": "selector", "style": "rotary",
        "positions": [{"value": 0, "label": "OFF", "angle": -50}, {"value": 1, "label": "PWR", "angle": 0}],
    })
    p.knob("VOL", "KNOB_M", 500, 118, {"id": "ILS_VOL", "label": "VOL", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("VOL", "NAME", "VOL", "above")
    p.display("FREQ", 320, 170, 200, 64, readout("ILS_FREQUENCY_S", "ILS FREQUENCY", 6))
    p.rocker("MHZ", 140, 252, step_rocker("ILS_MHZ", "MHZ"))
    p.rocker("KHZ", 500, 252, step_rocker("ILS_KHZ", "KHZ"))


def aap_pages() -> list[dict]:
    g = PanelGroup("AAP / ILS", "a10c", scroll=True)
    aap_plate(g)
    ils_plate(g)
    return [kit_page("AAP / ILS", [5, 9, 1, 2], g.build())]


def tacan_pages() -> list[dict]:
    p = Panel("TACAN", 640, 500, "a10c")
    p.display("CHAN", 190, 112, 176, 64, readout("TACAN_CHANNEL", "CHANNEL", 4))
    p.label("CHANNEL", "NAME", "CHAN", "above")
    p.knob("VOL", "KNOB_S", 520, 112, {"id": "TACAN_VOL", "label": "VOL", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("VOL", "NAME", "VOL", "above")
    p.rocker("TENS", 96, 270, step_rocker("TACAN_10", "10"))
    p.push("TEST", 196, 270, {"id": "TACAN_TEST_BTN", "label": "TEST", "type": "button", "hold": BUTTON_HOLD})
    p.label("TEST", "NAME", "TEST", "above")
    p.lamp("TEST_LAMP", 196, 350, {"id": "TACAN_TEST", "legend": "", "color": "red"})
    p.rocker("UNITS", 296, 270, step_rocker("TACAN_1", "1"))
    p.toggle("XY", 392, 270, {
        "id": "TACAN_XY", "label": "X/Y", "type": "selector",
        "positions": [{"value": 1, "label": "Y"}, {"value": 0, "label": "X"}],
    }, "above_below")
    p.rotary("MODE", 500, 400, {
        "id": "TACAN_MODE", "label": "MODE", "type": "selector", "style": "rotary",
        "positions": [
            {"value": 0, "label": "OFF", "angle": -80}, {"value": 1, "label": "REC", "angle": -40}, {"value": 2, "label": "T/R", "angle": 0},
            {"value": 3, "label": "A/A REC", "angle": 40}, {"value": 4, "label": "A/A T/R", "angle": 80},
        ],
    }, labels="fan")
    return [kit_page("TACAN", [6, 9, 1, 2], p.build())]


def hars_pages() -> list[dict]:
    g = PanelGroup("HARS / HMCS", "a10c")
    h = g.panel("HMCS", 640, 176, 0, 0)
    h.toggle("PWR", 320, 98, {
        "id": "A102_HMCS_PW", "label": "HMCS POWER", "type": "selector",
        "positions": [{"value": 2, "label": "ON"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "BAT"}],
    }, "right_triple")
    h.label("HMCS", "NAME", "PWR", "above")
    p = g.panel("HARS", 640, 380, 0, 192)
    p.toggle("MODE", 110, 108, {
        "id": "HARS_SLAVE_DG", "label": "SLAVE / DG", "type": "selector",
        "positions": [{"value": 1, "label": "SLAVE"}, {"value": 0, "label": "DG"}],
    }, "above_below")
    p.knob("LAT", "KNOB_M", 280, 108, {"id": "HARS_LATITUDE", "label": "LAT", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("LAT", "NAME", "LAT", "above")
    p.knob_labels("LAT", "lower_sides", "0", "90")
    p.toggle("NS", 430, 108, {
        "id": "HARS_NS", "label": "N / S", "type": "selector",
        "positions": [{"value": 1, "label": "N"}, {"value": 0, "label": "S"}],
    }, "above_below")
    p.round("PTS", 110, 256, {"id": "HARS_PTS", "label": "PUSH TO SYNC", "type": "button", "shape": "round", "hold": BUTTON_HOLD})
    p.label("PUSH TO\nSYNC", "NAME", "PTS", "below")
    p.knob("HDG", "KNOB_M", 280, 256, {"id": "HARS_HDG", "label": "HDG", "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label("HDG", "NAME", "HDG", "above")
    p.knob_labels("HDG", "lower_sides", "-", "+")
    p.toggle("MAGVAR", 430, 256, {
        "id": "HARS_MAGVAR", "label": "MAG VAR", "type": "selector",
        "positions": [{"value": 2, "label": "+15"}, {"value": 1, "label": "0"}, {"value": 0, "label": "-15"}],
    }, "right_triple")
    p.label("MAG\nVAR", "NAME", "MAGVAR", "above")
    p.bar("SYNC", 550, 190, {"id": "HARS_SYNC", "label": "SYN-IND", "type": "bar", "max": 65535})
    p.label("SYN-IND", "NAME", "SYNC", "above")
    return [kit_page("HARS / HMCS", [7, 9, 1, 2], g.build())]


def canopy_plate(g: PanelGroup):
    p = g.panel("CANOPY", 640, 444, 0, 0)
    p.toggle("CANOPY", 130, 160, {
        "id": "CANOPY_OPEN", "label": "CANOPY", "type": "selector", "rest": 1, "hold": 0.5,
        "positions": [{"value": 2, "label": "OPEN", "momentary": True}, {"value": 1, "label": "HOLD"}, {"value": 0, "label": "CLOSE", "momentary": True}],
    }, "right_triple")
    p.label("CANOPY", "NAME", "CANOPY", "above", 0, -40)
    p.push("LADDER", 290, 160, {"id": "LADDER_EXTEND", "label": "EXTEND BOARDING LADDER", "type": "button", "guard": True, "cover": "LADDER_EXTEND_COVER", "hold": BUTTON_HOLD})
    p.label("EXTEND\nBOARDING\nLADDER", "POS", "LADDER", "below")
    p.toggle("JTSN", 400, 160, {
        "id": "CANOPY_JTSN", "label": "CANOPY JETTISON", "type": "selector", "guard": True,
        "positions": [{"value": 1, "label": "PULL"}, {"value": 0, "label": "IN"}],
    }, "above_below")
    p.label("CANOPY\nJTSN", "NAME", "JTSN", "above")
    p.toggle("UNLOCK", 490, 160, {
        "id": "CANOPY_JTSN_UNLOCK", "label": "JTSN UNLOCK", "type": "selector",
        "positions": [{"value": 1, "label": "UNLOCK"}, {"value": 0, "label": "LOCK"}],
    }, "above_below")
    p.label("JTSN\nUNLOCK", "NAME", "UNLOCK", "above")
    p.bar("POS", 560, 160, {"id": "CANOPY_POS", "label": "CANOPY POSITION", "type": "bar", "max": 65535})
    p.label("CANOPY\nPOS", "POS", "POS", "below")
    p.toggle("DISENGAGE", 110, 350, {
        "id": "CANOPY_DISENGAGE", "label": "ACTUATOR DISENGAGE", "type": "selector",
        "positions": [{"value": 1, "label": "DISENGAGE"}, {"value": 0, "label": "ENGAGE"}],
    }, "above_below")
    p.label("ACTUATOR", "NAME", "DISENGAGE", "above")
    p.lamp("UNLOCKED", 380, 350, {"id": "CANOPY_UNLOCKED", "legend": "CANOPY\nUNLOCKED", "color": "red"}, "LAMP_WIDE")


def elec_plate(g: PanelGroup):
    p = g.panel("ELECTRICAL POWER", 640, 384, 0, 460)
    p.toggle("APU", 130, 124, {
        "id": "EPP_APU_GEN_PWR", "label": "APU GEN PWR", "type": "selector",
        "positions": [{"value": 1, "label": "PWR"}, {"value": 0, "label": "OFF/RESET"}],
    })
    p.label("APU GEN\nPWR", "NAME", "APU", "above")
    p.label("OFF/RESET", "POS", "APU", "below")
    p.toggle("INV", 320, 124, {
        "id": "EPP_INVERTER", "label": "INVERTER", "type": "selector", "rest": 1, "hold": 0.5,
        "positions": [{"value": 2, "label": "STBY"}, {"value": 1, "label": "OFF"}, {"value": 0, "label": "TEST", "momentary": True}],
    })
    p.label("INVERTER\nSTBY", "NAME", "INV", "above")
    p.label("OFF", "POS", "INV", "right")
    p.label("TEST", "POS", "INV", "below")
    p.toggle("FLOOD", 510, 124, {
        "id": "EPP_EMER_FLOOD", "label": "EMER FLOOD", "type": "selector",
        "positions": [{"value": 1, "label": "EMER FLOOD"}, {"value": 0, "label": "OFF"}],
    })
    p.label("EMER\nFLOOD", "NAME", "FLOOD", "above")
    p.label("OFF", "POS", "FLOOD", "below")
    for side, bios, x in (("L", "EPP_AC_GEN_PWR_L", 130), ("R", "EPP_AC_GEN_PWR_R", 320)):
        p.toggle(f"AC_{side}", x, 290, {
            "id": bios, "label": f"AC GEN PWR {side}", "type": "selector",
            "positions": [{"value": 1, "label": "PWR"}, {"value": 0, "label": "OFF/RESET"}],
        })
        p.label(side, "POS", f"AC_{side}", "left" if side == "L" else "right")
        p.label("OFF/RESET", "POS", f"AC_{side}", "below")
    p.mark("AC GEN PWR", "POS", 225, 290, "title between the two AC GEN switches")
    p.toggle("BAT", 510, 290, {
        "id": "EPP_BATTERY_PWR", "label": "BATTERY PWR", "type": "selector",
        "positions": [{"value": 1, "label": "PWR"}, {"value": 0, "label": "OFF"}],
    })
    p.label("BATTERY\nPWR", "NAME", "BAT", "above")
    p.label("OFF", "POS", "BAT", "below")


def canopy_pages() -> list[dict]:
    g = PanelGroup("CANOPY / ELEC", "a10c", scroll=True)
    canopy_plate(g)
    elec_plate(g)
    return [kit_page("CANOPY / ELEC", [1, 11, 2, 2], g.build())]


def env_toggle(p: Panel, name: str, label: str, bios: str, x: int, y: int, title: str):
    p.toggle(name, x, y, {"id": bios, "label": label, "type": "selector", "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}]})
    p.label(title, "NAME", name, "above")
    p.label("OFF", "POS", name, "below")


def env_knob(p: Panel, name: str, label: str, bios: str, x: int, y: int, marks: tuple):
    p.knob(name, "KNOB_M", x, y, {"id": bios, "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label(label, "NAME", name, "above")
    p.knob_labels(name, "lower_sides", *marks)


def env_pages() -> list[dict]:
    p = Panel("ENVIRONMENT", 640, 1280, "a10c", scroll=True)
    p.lamp("FLOW", 110, 190, {"id": "OXY_FLOW", "legend": "FLOW", "color": "white"})
    p.bar("PRESS", 330, 190, {"id": "OXY_PRESS", "label": "OXYGEN SUPPLY PRESSURE", "type": "bar", "max": 65535})
    p.label("OXYGEN\nSUPPLY\nPRESSURE", "POS", "PRESS", "below")
    p.bar("QTY", 520, 190, {"id": "OXY_VOLUME", "label": "LIQUID OXYGEN LITERS", "type": "bar", "max": 65535})
    p.label("LIQUID OXYGEN\nLITERS", "POS", "QTY", "below")
    p.toggle("EMER", 80, 470, {
        "id": "OXY_EMERGENCY", "label": "OXYGEN EMERGENCY", "type": "selector", "rest": 1, "hold": 0.5,
        "positions": [
            {"value": 0, "label": "EMERGENCY", "momentary": True, "disabled": True}, {"value": 1, "label": "NORMAL"},
            {"value": 2, "label": "TEST MARK", "momentary": True, "disabled": True},
        ],
    }, "right_triple")
    p.toggle("DILUTER", 310, 470, {
        "id": "OXY_DILUTER", "label": "OXYGEN DILUTION", "type": "selector",
        "positions": [{"value": 1, "label": "100% OXYGEN"}, {"value": 0, "label": "NORMAL OXYGEN"}],
    }, "above_below")
    p.toggle("SUPPLY", 450, 470, {
        "id": "OXY_SUPPLY", "label": "OXYGEN SUPPLY", "type": "selector",
        "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}],
    }, "above_below")
    p.label("SUPPLY", "NAME", "SUPPLY", "above")
    p.push("OXY_TEST", 548, 470, {"id": "ENVCP_OXY_TEST", "label": "OXY IND TEST", "type": "button", "hold": BUTTON_HOLD})
    p.label("OXY IND\nTEST", "NAME", "OXY_TEST", "above")
    env_toggle(p, "DEFOG", "WINDSHIELD DEFOG/DEICE", "ENVCP_WINDSHIELD_DEFOG", 150, 640, "WINDSHIELD\nDEFOG/DEICE")
    env_knob(p, "CANOPY_DEFOG", "CANOPY DEFOG", "ENVCP_CANOPY_DEFOG", 420, 640, ("OFF", "MAX"))
    env_toggle(p, "PITOT", "PITOT HEAT", "ENVCP_PITOT_HEAT", 150, 800, "PITOT\nHEAT")
    env_toggle(p, "BLEED", "BLEED AIR", "ENVCP_BLEED_AIR", 510, 800, "BLEED\nAIR")
    p.bar("CABIN", 330, 880, {"id": "CABIN_PRESS_ALT", "label": "CABIN PRESS ALT", "type": "bar", "max": 65535})
    p.label("CABIN\nPRESS ALT\nx 1000", "POS", "CABIN", "below")
    p.toggle("TEMP_PRESS", 150, 960, {
        "id": "ENVCP_TEMP_PRESS", "label": "TEMP/PRESS", "type": "selector",
        "positions": [{"value": 2, "label": "NORM"}, {"value": 1, "label": "DUMP"}, {"value": 0, "label": "RAM"}],
    }, "above_side_below")
    p.label("TEMP/PRESS", "NAME", "TEMP_PRESS", "above")
    env_toggle(p, "AIR_SUPPLY", "MAIN AIR SUPPLY", "ENVCP_AIR_SUPPLY", 510, 960, "MAIN AIR\nSUPPLY")
    env_knob(p, "FLOW_LEVEL", "FLOW LEVEL", "ENVCP_FLOW_LEVEL", 150, 1160, ("LO", "HI"))
    p.rotary("AC", 470, 1160, {
        "id": "ENVCP_AC_OPER", "label": "CABIN AIR COND", "type": "selector", "style": "rotary",
        "positions": [
            {"value": 2, "label": "COLD", "angle": -90}, {"value": 1, "label": "OPER AUTO", "angle": 0},
            {"value": 3, "label": "HOT", "angle": 90}, {"value": 0, "label": "MAN", "angle": 180},
        ],
    })
    p.label("CABIN AIR\nCOND", "NAME", "AC", "above")
    return [kit_page("ENVIRONMENT", [3, 11, 3, 2], p.build())]


def lcp_knob(p: Panel, name: str, label: str, bios: str, x: int, y: int, preset: str = "lower_sides", marks: tuple = ("OFF", "BRT")):
    p.knob(name, "KNOB_M", x, y, {"id": bios, "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]})
    p.label(label, "NAME", name, "above")
    p.knob_labels(name, preset, *marks)


def lcp_toggle(p: Panel, name: str, label: str, bios: str, x: int, y: int, title: str):
    p.toggle(name, x, y, {"id": bios, "label": label, "type": "selector", "positions": [{"value": 1, "label": "ON"}, {"value": 0, "label": "OFF"}]})
    p.label(title, "NAME", name, "above")
    p.label("OFF", "POS", name, "below")


def lighting_pages() -> list[dict]:
    p = Panel("LIGHTING", 640, 592, "a10c")
    p.toggle("POSITION", 100, 124, {
        "id": "LCP_POSITION", "label": "POSITION", "type": "selector",
        "positions": [{"value": 0, "label": "FLASH"}, {"value": 1, "label": "OFF"}, {"value": 2, "label": "STEADY"}],
    }, "above_side_below")
    p.label("POSITION", "NAME", "POSITION", "above")
    lcp_knob(p, "FORMATION", "FORMATION", "LCP_FORMATION", 320, 124)
    lcp_toggle(p, "ANTICOLL", "ANTI-COLLISION", "LCP_ANTICOLLISION", 540, 124, "ANTI-\nCOLLISION")
    lcp_knob(p, "ENG_INST", "ENG INST", "LCP_ENG_INST", 120, 256)
    lcp_toggle(p, "NOSE", "NOSE ILLUM", "LCP_NOSE_ILLUM", 320, 256, "NOSE ILLUM")
    lcp_knob(p, "AUX_INST", "AUX INST", "LCP_AUX_INST", 520, 256)
    p.toggle("SIGNAL", 120, 388, {
        "id": "LCP_SIGNAL_LIGHTS", "label": "SIGNAL LTS", "type": "selector",
        "positions": [{"value": 1, "label": "BRT"}, {"value": 0, "label": "DIM"}],
    }, "above_below")
    p.label("SIGNAL LTS", "NAME", "SIGNAL", "above")
    lcp_knob(p, "FLT_INST", "FLT INST", "LCP_FLIGHT_INST", 320, 388)
    lcp_toggle(p, "ACCEL", "ACCEL & COMP", "LCP_ACCEL_COMP", 530, 388, "ACCEL &\nCOMP")
    lcp_knob(p, "FLOOD", "FLOOD", "LCP_FLOOD", 170, 520, "signal", ("OFF", "BRT", "TSTORM"))
    lcp_knob(p, "CONSOLE", "CONSOLE", "LCP_CONSOLE", 470, 520)
    return [kit_page("LIGHTING", [6, 11, 2, 2], p.build())]


def mfcd_controls(side: str) -> list[dict]:
    prefix = f"{side}MFD"
    controls = [
        {"id": f"{prefix}_{n:02d}", "label": str(n), "type": "button", "hold": BUTTON_HOLD, "side": side, "slot": str(n)}
        for n in range(1, 21)
    ]
    controls += [
        {"id": f"{prefix}_{name}", "label": name, "type": "hat", "ud": f"{prefix}_{name}", "hold": BUTTON_HOLD, "positions": {"up": "tri-up", "down": "tri-down"}, "side": side, "slot": name}
        for name in ("ADJ", "BRT")
    ]
    controls.append({"id": f"{prefix}_PWR", "label": "PWR", "type": "selector", "positions": PWR_POSITIONS, "side": side, "slot": "PWR"})
    return controls


CDU_LABELS = {"POINT": ".", "SLASH": "/"}
UP_DOWN = {"up": "tri-up", "down": "tri-down"}
LEFT_RIGHT = {"left": "tri-left", "right": "tri-right"}


def hat_rocker(prefix: str, name: str, label: str, side: str, positions: dict) -> dict:
    axis = "ud" if "up" in positions else "lr"
    return {"id": f"{prefix}_{name}", "label": label, "type": "hat", axis: f"{prefix}_{name}", "hold": BUTTON_HOLD, "positions": positions, "side": side, "slot": name}


def cdu_controls() -> list[dict]:
    keys = ["SYS", "NAV", "WP", "OSET", "FPM", "PREV"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + ["POINT", "SLASH", "CLR", "BCK", "SPC", "FA", "MK"]
    controls = [{"id": "CDU_SCREEN", "label": "CDU", "type": "display", "cols": 24, "ids": [f"CDU_LINE{n}" for n in range(10)], "side": "C", "slot": "DISPLAY"}]
    controls += [
        {"id": f"CDU_LSK_{slot}", "label": f"LSK {slot}", "type": "button", "hold": BUTTON_HOLD, "side": "C", "slot": slot}
        for slot in ("3L", "5L", "7L", "9L", "3R", "5R", "7R", "9R")
    ]
    controls += [
        {"id": f"CDU_{key}", "label": CDU_LABELS.get(key, key), "type": "button", "hold": BUTTON_HOLD, "side": "C", "slot": key}
        for key in keys
    ]
    controls += [
        hat_rocker("CDU", "BRT", "BRT / DIM", "C", {"left": "DIM", "right": "BRT"}),
        hat_rocker("CDU", "PG", "PG", "C", UP_DOWN),
        hat_rocker("CDU", "SCROLL", "SCROLL", "C", LEFT_RIGHT),
        hat_rocker("CDU", "DATA", "+ / \u2212", "C", UP_DOWN),
        {**AAP_PAGE, "side": "C", "slot": "PAGE"},
        {**AAP_STEERPT, "side": "C", "slot": "STEERPT"},
    ]
    return controls


def ufc_controls() -> list[dict]:
    keys = [(f"UFC_{n}", str(n % 10)) for n in (*range(1, 10), 10)]
    keys += [("UFC_SPC", "SPC"), ("UFC_HACK", "HACK"), ("UFC_FUNC", "FUNC"), ("UFC_LTR", "LTR"), ("UFC_CLR", "CLR"), ("UFC_ENT", "ENT"), ("UFC_MK", "MK"), ("UFC_ALT_ALRT", "ALT ALRT")]
    keys += [("UFC_COM1", "COM 1"), ("UFC_COM_SEC", "COM SEC"), ("UFC_IFF", "IFF"), ("UFC_COM2", "COM 2"), ("UFC_ECCM", "ECCM"), ("UFC_IDM", "IDM")]
    controls = [
        {"id": bios, "label": label, "type": "button", "hold": BUTTON_HOLD, "side": "U", "slot": bios[4:]}
        for bios, label in keys
    ]
    controls.append({"id": "UFC_MASTER_CAUTION", "label": "MASTER CAUTION", "type": "button", "hold": BUTTON_HOLD, "lamp": "MASTER_CAUTION", "side": "U", "slot": "MASTER_CAUTION"})
    controls += [hat_rocker("UFC", name, name, "U", UP_DOWN) for name in ("STEER", "DATA", "SEL", "DEPR")]
    controls.append(hat_rocker("UFC", "INTEN", "INTEN", "U", LEFT_RIGHT))
    return controls


VIEWS = [
    {
        "name": "COCKPIT", "seats": [0], "layout": "map", "controls": [],
        "lamps": MASTER_LAMPS + [
            GUN_READY_LAMP,
            {"id": "NOSEWHEEL_STEERING", "label": "NWS", "color": "green"},
            {"id": "MARKER_BEACON", "label": "MARKER", "color": "green"},
            CANOPY_LAMP,
        ],
        "links": [
            {"label": "MFCD L", "view": "MFCD", "side": "L", "seats": [0], "map": [3, 5, 2, 1]},
            {"label": "MFCD R", "view": "MFCD", "side": "R", "seats": [0], "map": [3, 8, 2, 1]},
            {"label": "CDU", "view": "CDU", "side": "C", "seats": [0], "map": [4, 9, 1, 2]},
            {"label": "UFC", "view": "CDU", "side": "U", "seats": [0], "map": [1, 5, 1, 4]},
        ],
    },
    *brake_pages(),
    *iff_pages(),
    *emer_pages(),
    *intercom_pages(),
    *fuel_pages(),
    *throttle_pages(),
    *laste_pages(),
    *radio_pages(),
    *uhf_pages(),
    *vhf_pages(),
    *fire_pages(),
    *cmsc_pages(),
    *gear_pages(),
    *ahcp_pages(),
    *nmsp_pages(),
    *cmsp_pages(),
    *caution_pages(),
    *aap_pages(),
    *tacan_pages(),
    *hars_pages(),
    *canopy_pages(),
    *env_pages(),
    *lighting_pages(),
    {
        "name": "Flight", "seats": [0],
        "lamps": MASTER_LAMPS + [
            {"id": "GEAR_L_SAFE", "label": "L SAFE", "color": "green"},
            {"id": "GEAR_N_SAFE", "label": "N SAFE", "color": "green"},
            {"id": "GEAR_R_SAFE", "label": "R SAFE", "color": "green"},
            {"id": "HANDLE_GEAR_WARNING", "label": "GEAR", "color": "red"},
            {"id": "L_ENG_FIRE", "label": "L ENG FIRE", "color": "red"},
            {"id": "APU_FIRE", "label": "APU FIRE", "color": "red"},
            {"id": "R_ENG_FIRE", "label": "R ENG FIRE", "color": "red"},
            CANOPY_LAMP,
        ],
        "controls": [
            {"id": "EXT_SPEED_BRAKE_LEFT", "label": "SPD BRK", "type": "bar", "max": 65535, "grid": [1, 1, 1, 1]},
            {**GEAR_LEVER, "grid": [1, 3, 2, 1]},
            {**FLAPS_SWITCH, "grid": [1, 4, 2, 1]},
            {"id": "FLAP_POS", "label": "FLAPS POS", "type": "bar", "max": 65535, "grid": [3, 5, 1, 1]},
            {**LANDING_LIGHTS, "grid": [1, 5, 1, 1]},
            {**ANTI_SKID_SWITCH, "grid": [2, 5, 1, 1]},
            {**ENG_THROTTLE["L"], "grid": [1, 6, 3, 1]},
            {**ENG_THROTTLE["R"], "grid": [1, 7, 3, 1]},
            {"id": "FUEL_QTY_L", "label": "FUEL L", "type": "bar", "max": 65535, "grid": [3, 1, 1, 1]},
            {"id": "FUEL_QTY_R", "label": "FUEL R", "type": "bar", "max": 65535, "grid": [3, 2, 1, 1]},
            {**EMER_BRAKE, "grid": [3, 3, 1, 1]},
            {**HARS_FAST_ERECT, "grid": [3, 4, 1, 1]},
        ],
    },
    {
        "name": "Fight", "seats": [0],
        "lamps": MASTER_LAMPS + [GUN_READY_LAMP, {"id": "CMSC_LAUNCH", "label": "LAUNCH", "color": "red"}],
        "controls": [
            {**AHCP_MASTER_ARM, "grid": [2, 1, 1, 1]},
            {**AHCP_GUNPAC, "grid": [2, 2, 1, 1]},
            {**AHCP_LASER_ARM, "grid": [2, 3, 1, 1]},
            {**AHCP_TGP, "grid": [2, 4, 1, 1]},
            {**readout("CMSC_TXT_CHAFF_FLARE", "CHAFF / FLARE", 8), "grid": [2, 5, 1, 2]},
            {"id": "CMSP1", "label": "CMSP 1", "type": "display", "grid": [3, 1, 1, 3]},
            {"id": "CMSP2", "label": "CMSP 2", "type": "display", "grid": [3, 4, 1, 3]},
        ],
    },
    {
        "name": "MFCD", "seats": [0], "layout": "mfcd", "lamps": [], "controls": mfcd_controls("L") + mfcd_controls("R"),
        "titles": {"L": "LEFT MFCD", "R": "RIGHT MFCD"}, "inert": ["DSP", "CON", "SYM"],
    },
    {"name": "CDU", "seats": [0], "layout": "cdu", "lamps": [], "controls": cdu_controls() + ufc_controls()},
]

CONTROL_NAMES = []

MPD_INDICATIONS = ()
MPD_SEATS = {}

TRIM_RELEASED = None

SEATS = [{"prefix": "", "label": "A-10C"}]
SEAT_OUTPUT = None
TRIM_SWITCH = None
