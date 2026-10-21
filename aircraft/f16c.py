from panel_kit import REF, Panel, PanelGroup

DCSBIOS_MODULE = "F-16C_50"
NAME = "F-16C"
DCS_NAMES = ["F-16C_50"]

KEYS = {}

KNOB_STEP = 3200
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


def kit_page(name: str, cell: list, page: dict) -> dict:
    return {
        "name": name, "seats": [0], "panel": True, "layout": "panel", "map": cell, "box": page["box"],
        "lamps": MASTER_LAMPS, "print": page["print"], "art": page["art"], "controls": page["controls"],
        **({"indicators": page["indicators"]} if page["indicators"] else {}),
        **({"scroll": True} if page.get("scroll") else {}),
        "kit": True, "ref": list(REF),
    }


def selector(bios: str, label: str, positions: tuple, **extra) -> dict:
    return {"id": bios, "label": label, "type": "selector", **extra, "positions": [{"value": value, "label": text} for value, text in positions]}


def spring(bios: str, label: str, positions: tuple, rest: int, **extra) -> dict:
    return {
        "id": bios, "label": label, "type": "selector", **extra, "rest": rest, "hold": 0.5,
        "positions": [{"value": value, "label": text, **({} if value == rest else {"momentary": True})} for value, text in positions],
    }


def push_button(bios: str, label: str) -> dict:
    return {"id": bios, "label": label, "type": "button", "hold": BUTTON_HOLD}


def knob(bios: str, label: str) -> dict:
    return {"id": bios, "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]}


def lamp(bios: str, legend: str, color: str) -> dict:
    return {"id": bios, "legend": legend, "color": color}


def step_rocker(bios: str, label: str) -> dict:
    return {"id": bios, "label": label, "type": "hat", "ud": bios, "steps": "fixed", "positions": {"up": "tri-up", "down": "tri-down"}}


def readout(bios: str, label: str, cols: int) -> dict:
    return {"id": bios, "label": label, "type": "display", "cols": cols, "ids": [bios]}


def canopy_plate(g: PanelGroup):
    p = g.panel("CANOPY", 420, 332, 0, 0)
    p.toggle("SWITCH", 80, 148, spring("CANOPY_SW", "CANOPY SWITCH", ((0, "OPEN"), (1, "HOLD"), (2, "CLOSE")), 1), "right_triple")
    p.mark("CANOPY\nSWITCH", "NAME", 80, 84, "name above the position labels of the switch")
    p.toggle("LEVER", 238, 148, selector("CANOPY_HANDLE", "CANOPY LEVER", ((1, "UNLOCKED"), (0, "LOCKED"))), "above_below")
    p.label("CANOPY\nLEVER", "NAME", "LEVER", "above")
    p.bar("POS", 344, 148, {"id": "CANOPY_POS", "label": "CANOPY POSITION", "type": "bar", "max": 65535})
    p.label("CANOPY\nPOS", "POS", "POS", "below")


def defog_plate(g: PanelGroup):
    p = g.panel("DEFOG", 144, 332, 436, 0)
    levels = [(value, "MIN" if value == 0 else "MAX" if value == 20 else str(value)) for value in range(0, 21, 5)]
    p.toggle("LEVER", 72, 166, selector("DEFOG_LEVER", "DEFOG", levels))
    p.label("MIN", "POS", "LEVER", "above")
    p.label("DEFOG", "NAME", "LEVER", "above")
    p.label("MAX", "POS", "LEVER", "below")


def jettison_plate(g: PanelGroup):
    p = g.panel("CANOPY JETTISON", 264, 264, 0, 348)
    p.toggle("THANDLE", 132, 160, selector("CANOPY_JETT_THANDLE", "CANOPY JETTISON", ((1, "PULL"), (0, "STOW")), guard=True), "above_below")
    p.label("CANOPY\nJETTISON", "NAME", "THANDLE", "above")


def canopy_pages() -> list[dict]:
    g = PanelGroup("CANOPY / DEFOG", "f16c", scroll=True)
    canopy_plate(g)
    defog_plate(g)
    jettison_plate(g)
    return [kit_page("CANOPY / DEFOG", [1, 1, 1, 2], g.build())]


def fuel_plate(g: PanelGroup):
    p = g.panel("FUEL", 640, 252, 0, 0)
    p.mark("FUEL", "TITLE", 52, 126, "panel name turned along the left edge", 90)
    p.toggle("MASTER", 116, 148, selector("FUEL_MASTER_SW", "FUEL MASTER", ((1, "MASTER"), (0, "OFF")), guard=True, cover="FUEL_MASTER_CV"), "above_below")
    p.toggle("INERT", 240, 148, selector("TANK_INTERTING_SW", "TANK INERTING", ((1, "TANK INERTING"), (0, "OFF")), guard=True))
    p.label("TANK\nINERTING", "NAME", "INERT", "above")
    p.label("OFF", "POS", "INERT", "below")
    p.rotary("FEED", 412, 148, {
        "id": "ENGINE_FEED_KNB", "label": "ENG FEED", "type": "selector", "style": "rotary",
        "positions": [{"value": 0, "label": "OFF", "angle": -90}, {"value": 1, "label": "NORM", "angle": -50}, {"value": 2, "label": "AFT", "angle": 0}, {"value": 3, "label": "FWD", "angle": 50}],
    })
    p.label("ENG FEED", "NAME", "FEED", "above")
    p.toggle("REFUEL", 560, 148, selector("AIR_REFUEL_SW", "AIR REFUEL", ((1, "OPEN"), (0, "CLOSE"))), "above_below")
    p.label("AIR\nREFUEL", "NAME", "REFUEL", "above")


def epu_plate(g: PanelGroup):
    p = g.panel("EPU", 288, 264, 0, 268)
    p.toggle("EPU", 76, 160, selector("EPU_SW", "EPU", ((2, "OFF"), (1, "NORM"), (0, "ON")), guard=True), "right_triple")
    p.label("EPU", "NAME", "EPU", "above")
    p.lamp("HYDRAZN", 216, 112, lamp("LIGHT_HYDRAZN", "HYDRAZN", "amber"))
    p.lamp("AIR", 216, 160, lamp("LIGHT_AIR", "AIR", "amber"))
    p.lamp("RUN", 216, 208, lamp("LIGHT_EPU", "EPU", "green"))


def start_plate(g: PanelGroup):
    p = g.panel("ENG & JET START", 336, 264, 304, 268)
    p.lamp("RUN", 76, 160, lamp("LIGHT_JFS_RUN", "RUN", "green"))
    p.toggle("JFS", 156, 160, spring("JFS_SW", "JFS", ((0, "START 1"), (1, "OFF"), (2, "START 2")), 1), "above_side_below")
    p.label("JFS", "NAME", "JFS", "above")
    p.toggle("CONT", 254, 160, selector("ENG_CONT_SW", "ENG CONT", ((1, "PRI"), (0, "SEC")), guard=True, cover="ENG_CONT_SW_COVER"), "above_below")
    p.label("ENG\nCONT", "NAME", "CONT", "above")


def fuel_pages() -> list[dict]:
    g = PanelGroup("FUEL / EPU / START", "f16c")
    fuel_plate(g)
    epu_plate(g)
    start_plate(g)
    return [kit_page("FUEL / EPU / START", [2, 1, 1, 2], g.build())]


def flcs_plate(g: PanelGroup):
    p = g.panel("FLT CONTROL", 626, 282, 0, 0)
    p.mark("FLT CONTROL", "TITLE", 52, 141, "panel name turned along the left edge", 90)
    p.toggle("DIGITAL", 130, 148, selector("DIGI_BAK_SW", "DIGITAL BACKUP", ((1, "BACKUP"), (0, "OFF"))), "above_below")
    p.label("DIGITAL\nBACKUP", "NAME", "DIGITAL", "above")
    p.toggle("FLAPS", 252, 148, selector("ALT_FLAPS_SW", "ALT FLAPS", ((1, "EXTEND"), (0, "NORM"))), "above_below")
    p.label("ALT\nFLAPS", "NAME", "FLAPS", "above")
    p.toggle("RESET", 372, 148, selector("FLCS_RESET_SW", "FLCS RESET", ((1, "RESET"), (0, "OFF"))), "above_below")
    p.label("FLCS\nRESET", "NAME", "RESET", "above")
    p.toggle("BIT", 460, 148, spring("BIT_SW", "FLCS BIT", ((1, "BIT"), (0, "OFF")), 0), "above_below")
    p.label("FLCS", "NAME", "BIT", "above")
    p.lamp("RUN", 548, 124, lamp("LIGHT_FL_RUN", "RUN", "green"))
    p.lamp("FAIL", 548, 172, lamp("LIGHT_FL_FAIL", "FAIL", "red"))


def trim_plate(g: PanelGroup):
    p = g.panel("MANUAL TRIM", 454, 366, 0, 298)
    p.mark("MANUAL TRIM", "TITLE", 52, 183, "panel name turned along the left edge", 90)
    p.knob("ROLL", "KNOB_M", 192, 104, knob("ROLL_TRIM", "ROLL TRIM"))
    p.label("ROLL TRIM", "NAME", "ROLL", "above")
    p.knob_labels("ROLL", "lower_sides", "L WING\nDN", "R WING\nDN")
    p.toggle("DISC", 368, 148, selector("TRIM_AP_DISC_SW", "TRIM/AP DISC", ((1, "NORM"), (0, "DISC"))), "above_below")
    p.label("TRIM/AP\nDISC", "NAME", "DISC", "above")
    p.knob("YAW", "KNOB_M", 132, 284, knob("YAW_TRIM", "YAW TRIM"))
    p.label("YAW TRIM", "NAME", "YAW", "above")
    p.knob_labels("YAW", "lower_sides", "L", "R")
    p.knob("PITCH", "KNOB_M", 288, 284, knob("PITCH_TRIM", "PITCH TRIM"))
    p.label("PITCH TRIM", "NAME", "PITCH", "above")
    p.knob_labels("PITCH", "lower_sides", "NOSE\nUP", "NOSE\nDN")


def override_plate(g: PanelGroup):
    p = g.panel("MANUAL PITCH", 156, 240, 470, 298)
    p.toggle("OVRD", 78, 148, spring("MANUAL_PITCH_SW", "MANUAL PITCH", ((1, "OVRD"), (0, "NORM")), 0), "above_below")
    p.label("MANUAL\nPITCH", "NAME", "OVRD", "above")


def flcs_pages() -> list[dict]:
    g = PanelGroup("FLT CONTROL / TRIM", "f16c", scroll=True)
    flcs_plate(g)
    trim_plate(g)
    override_plate(g)
    return [kit_page("FLT CONTROL / TRIM", [3, 1, 1, 2], g.build())]


def elec_plate(g: PanelGroup):
    p = g.panel("ELEC", 344, 430, 0, 0)
    p.mark("ELEC", "TITLE", 52, 76, "panel name turned along the left edge", 90)
    p.toggle("MAIN", 124, 100, selector("MAIN_PWR_SW", "MAIN PWR", ((0, "MAIN PWR"), (1, "BATT"), (2, "OFF"))), "above_side_below")
    p.push("RESET", 124, 262, push_button("ELEC_CAUTION", "ELEC CAUTION RESET"))
    p.label("CAUTION\nRESET", "NAME", "RESET", "above")
    for n, (bios, legend) in enumerate((("LIGHT_FLCS_PMG", "FLCS\nPMG"), ("LIGHT_MAIN_GEN", "MAIN\nGEN"), ("LIGHT_STBY_GEN", "STBY\nGEN"), ("LIGHT_EPU_GEN", "EPU\nGEN"), ("LIGHT_EPU_PMG", "EPU\nPMG"))):
        p.lamp(f"L{n}", 248, 100 + 48 * n, lamp(bios, legend, "amber"))
    p.bracket("BATT", "ACFT BATT", 44, 300, 336)
    for n, (bios, legend) in enumerate((("LIGHT_TO_FLCS", "TO\nFLCS"), ("LIGHT_FLCS_RLY", "FLCS\nRLY"), ("LIGHT_ACFT_BATT_FAIL", "FAIL"))):
        p.lamp(f"B{n}", 88 + 80 * n, 374, lamp(bios, legend, "amber"))


def test_plate(g: PanelGroup):
    p = g.panel("TEST", 592, 370, 0, 446)
    p.mark("TEST", "TITLE", 52, 76, "panel name turned along the left edge", 90)
    p.push("FIRE", 125, 158, push_button("FIRE_OHEAT_DETECT_BTN", "FIRE & OHEAT DETECT"))
    p.label("FIRE &\nOHEAT\nDETECT", "NAME", "FIRE", "above")
    p.toggle("OBOGS", 217, 158, spring("OBOGS_SW", "OBOGS BIT", ((1, "BIT"), (0, "OFF")), 0), "above_below")
    p.label("OBOGS", "NAME", "OBOGS", "above")
    p.push("MAL", 309, 158, push_button("MAL_IND_LTS_TEST", "MAL & IND LTS"))
    p.label("MAL &\nIND LTS", "NAME", "MAL", "above")
    p.toggle("PROBE", 136, 278, spring("PROBE_HEAT_SW", "PROBE HEAT", ((0, "PROBE HEAT"), (1, "OFF"), (2, "TEST")), 1), "above_side_below")
    p.toggle("EPUGEN", 246, 278, spring("EPU_GEN_TEST_SW", "EPU/GEN", ((1, "EPU/GEN"), (0, "OFF")), 0), "above_below")
    p.mark("FLCS PWR", "NAME", 372, 222, "title of the four lamps")
    for name, bios, x, y in (("C", "LIGHT_FLCS_PWR_C", 332, 262), ("A", "LIGHT_FLCS_PWR_A", 412, 262), ("D", "LIGHT_FLCS_PWR_D", 332, 310), ("B", "LIGHT_FLCS_PWR_B", 412, 310)):
        p.lamp(name, x, y, lamp(bios, name, "green"))
    p.toggle("PWR", 500, 278, spring("FLCS_PWR_TEST_SW", "FLCS PWR TEST", ((2, "TEST"), (1, "NORM"), (0, "MAINT")), 1), "above_side_below")
    p.label("FLCS PWR\nTEST", "NAME", "PWR", "above")


def elec_pages() -> list[dict]:
    g = PanelGroup("ELEC / TEST", "f16c", scroll=True)
    elec_plate(g)
    test_plate(g)
    return [kit_page("ELEC / TEST", [4, 1, 1, 2], g.build())]


def rotary_positions(items: tuple) -> list[dict]:
    return [{"value": value, "label": text, "angle": angle, **({"disabled": True} if rest else {})} for value, text, angle, *rest in items]


def ext_lighting_plate(g: PanelGroup):
    p = g.panel("EXT LIGHTING", 620, 460, 0, 0)
    p.mark("EXT LIGHTING", "TITLE", 52, 230, "panel name turned along the left edge", 90)
    p.rotary("ANTI", 140, 190, {
        "id": "ANTI_COLL_LIGHT_KNB", "label": "ANTI-COLL", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "OFF", -140), (1, "1", -105), (2, "2", -70), (3, "3", -35), (4, "4", 0), (5, "A", 35), (6, "B", 70), (7, "C", 105))),
    })
    p.label("ANTI-COLL", "NAME", "ANTI", "above")
    p.toggle("FLASH", 290, 190, selector("POS_FLASH_LIGHT_SW", "POSITION FLASH / STEADY", ((1, "FLASH"), (0, "STEADY"))), "above_below")
    p.toggle("WING", 390, 190, selector("POS_WING_TAIL_LIGHT_SW", "POSITION WING / TAIL", ((0, "BRT"), (1, "OFF"), (2, "DIM"))), "above_side_below")
    p.label("WING/\nTAIL", "NAME", "WING", "above")
    p.toggle("FUSE", 500, 190, selector("POS_FUSELAGE_LIGHT_SW", "FUSELAGE", ((0, "BRT"), (1, "OFF"), (2, "DIM"))), "above_side_below")
    p.label("FUSELAGE", "NAME", "FUSE", "above")
    p.knob("FORM", "KNOB_M", 140, 360, knob("FORM_LIGHT_KNB", "FORM"))
    p.label("FORM", "NAME", "FORM", "above")
    p.label("BRT", "POS", "FORM", "right")
    p.rotary("MASTER", 336, 360, {
        "id": "MASTER_LIGHT_SW", "label": "MASTER", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "OFF", -90), (1, "ALL", -50), (2, "A-C", 0), (3, "FORM", 50), (4, "NORM", 90))),
    })
    p.label("MASTER", "NAME", "MASTER", "above")
    p.knob("AERIAL", "KNOB_M", 520, 360, knob("AIR_REFUEL_LIGHT_KNB", "AERIAL REFUELING"))
    p.label("AERIAL\nREFUELING", "NAME", "AERIAL", "above")
    p.label("BRT", "POS", "AERIAL", "below")


def ext_lighting_pages() -> list[dict]:
    g = PanelGroup("EXT LIGHTING", "f16c")
    ext_lighting_plate(g)
    return [kit_page("EXT LIGHTING", [5, 1, 1, 2], g.build())]


def ecm_plate(g: PanelGroup):
    p = g.panel("ECM", 626, 520, 0, 0)
    p.mark("ECM", "TITLE", 52, 260, "panel name turned along the left edge", 90)
    p.toggle("PWR", 116, 112, selector("ECM_PW_SW", "ECM POWER", ((2, "OPR"), (1, "STBY"), (0, "OFF"))), "right_triple")
    p.toggle("XMIT", 270, 112, selector("ECM_XMIT_SW", "XMIT", ((2, "1"), (1, "2"), (0, "3"))), "right_triple")
    p.label("XMIT", "NAME", "XMIT", "above")
    p.knob("DIM", "KNOB_M", 420, 112, knob("ECM_DIM_KNB", "DIM"))
    p.label("DIM", "NAME", "DIM", "above")
    modules = (("1", "ECM_1_BTN", "LIGHT_ECM_1_"), ("2", "ECM_2_BTN", "LIGHT_ECM_2_"), ("3", "ECM_3_BTN", "LIGHT_ECM_3_"),
               ("4", "ECM_4_BTN", "LIGHT_ECM_4_"), ("5", "ECM_5_BTN", "LIGHT_ECM_5_"), ("6", "ECM_6_BTN", "LIGHT_ECM_"))
    for n, (number, bios, lights) in enumerate(modules):
        x, y = 118 + 268 * (n % 2), 230 + 104 * (n // 2)
        key = {**push_button(bios, f"ECM {number}"), **({"legend": number} if number != "6" else {})}
        p.push(f"M{number}", x, y, key)
        for m, (letter, color) in enumerate((("S", "amber"), ("A", "green"), ("F", "red"), ("T", "white"))):
            p.lamp(f"M{number}{letter}", x + 88 + 80 * (m % 2), y - 24 + 48 * (m // 2), lamp(lights + letter, letter, color))


def ecm_pages() -> list[dict]:
    g = PanelGroup("ECM", "f16c")
    ecm_plate(g)
    return [kit_page("ECM", [6, 1, 1, 2], g.build())]


def audio1_plate(g: PanelGroup):
    p = g.panel("AUDIO 1", 616, 324, 0, 0)
    p.mark("AUDIO 1", "TITLE", 52, 162, "panel name turned along the left edge", 90)
    for name, x, bios, mode in (("COMM1", 170, "COMM1_PWR_KNB", "COMM1_MODE_KNB"), ("COMM2", 372, "COMM2_PWR_KNB", "COMM2_MODE_KNB")):
        title = f"COMM {name[-1]}"
        p.knob(name, "KNOB_M", x, 112, knob(bios, title))
        p.label(title, "NAME", name, "above")
        p.knob_labels(name, "lower_sides", "OFF", "INC")
        p.rotary(f"{name}_MODE", x, 236, {
            "id": mode, "label": f"{title} MODE", "type": "selector", "style": "rotary",
            "positions": rotary_positions(((0, "OFF", -50), (1, "SQL", 0), (2, "GD", 50))),
        })
    p.knob("MSL", "KNOB_S", 508, 112, knob("MSL_KNB", "MSL"))
    p.label("MSL", "NAME", "MSL", "above")
    p.label("INC", "POS", "MSL", "right")
    p.knob("THREAT", "KNOB_S", 508, 236, knob("THREAT_KNB", "THREAT"))
    p.label("THREAT", "NAME", "THREAT", "above")
    p.label("INC", "POS", "THREAT", "right")


def audio2_plate(g: PanelGroup):
    p = g.panel("AUDIO 2", 616, 206, 0, 340)
    p.mark("AUDIO 2", "TITLE", 52, 103, "panel name turned along the left edge", 90)
    p.knob("TACAN", "KNOB_S", 170, 118, knob("TACAN_KNB", "TACAN"))
    p.label("TACAN", "NAME", "TACAN", "above")
    p.label("INC", "POS", "TACAN", "right")
    p.knob("ILS", "KNOB_S", 372, 118, knob("ILS_PWR_KNB", "ILS"))
    p.label("ILS", "NAME", "ILS", "above")
    p.knob_labels("ILS", "lower_sides", "OFF", "INC")


def audio_pages() -> list[dict]:
    g = PanelGroup("AUDIO", "f16c")
    audio1_plate(g)
    audio2_plate(g)
    return [kit_page("AUDIO", [7, 1, 1, 2], g.build())]


def gear_plate(g: PanelGroup):
    p = g.panel("LANDING GEAR", 640, 642, 0, 0)
    p.push("JETT", 110, 158, {**push_button("EMERG_STORE_JETT", "EMER STORES JETTISON"), "guard": True, "hold": 1.0})
    p.hazard("JETT")
    p.label("EMER STORES\nJETTISON", "POS", "JETT", "above")
    p.mark("WHEELS", "NAME", 240, 64, "title of the three gear lamps")
    for n, (bios, legend) in enumerate((("LIGHT_GEAR_N", "NOSE"), ("LIGHT_GEAR_L", "LEFT"), ("LIGHT_GEAR_R", "RIGHT"))):
        p.lamp(f"W{n}", 240, 110 + 48 * n, lamp(bios, legend, "green"))
    p.toggle("HOOK", 330, 158, selector("HOOK_SW", "HOOK", ((1, "UP"), (0, "DN")), guard=True), "above_below")
    p.label("HOOK", "NAME", "HOOK", "above")
    p.toggle("GEAR", 420, 158, selector("GEAR_HANDLE", "LG HANDLE", ((1, "UP"), (0, "DOWN"))), "above_below")
    p.label("LG\nHANDLE", "NAME", "GEAR", "above")
    p.lamp("WARN", 492, 158, lamp("LIGHT_GEAR_WARN", "GEAR\nWARN", "red"))
    p.bar("SPEED", 564, 194, {"id": "SPEEDBRAKE_INDICATOR", "label": "SPEED BRAKE", "type": "bar", "max": 65535})
    p.label("SPEED\nBRAKE", "NAME", "SPEED", "above")
    p.toggle("GND", 94, 360, selector("GND_JETT_ENABLE_SW", "GND JETT ENABLE", ((1, "ENABLE"), (0, "OFF"))), "above_below")
    p.label("GND\nJETT", "NAME", "GND", "above")
    p.toggle("BRAKES", 206, 360, selector("BRAKE_CHAN_SW", "BRAKES", ((1, "CHAN 1"), (0, "CHAN 2"))), "above_below")
    p.label("BRAKES", "NAME", "BRAKES", "above")
    p.toggle("PARK", 340, 360, selector("ANTI_SKID_SW", "PARKING BRAKE / ANTI-SKID", ((0, "PARKING BRAKE"), (1, "ANTI-SKID"), (2, "OFF"))))
    p.label("PARKING BRAKE", "POS", "PARK", "above")
    p.label("ANTI-SKID", "POS", "PARK", "right")
    p.label("OFF", "POS", "PARK", "below")
    p.toggle("STORES", 94, 544, selector("STORES_CONFIG_SW", "STORES CONFIG", ((1, "CAT I"), (0, "CAT III"))), "above_below")
    p.label("STORES\nCONFIG", "NAME", "STORES", "above")
    p.push("HORN", 206, 544, push_button("HORN_SILENCE_BTN", "HORN SILENCER"))
    p.label("HORN\nSILENCER", "NAME", "HORN", "above")
    p.toggle("LAND", 330, 544, selector("LAND_TAXI_LIGHT_SW", "LANDING / TAXI LIGHTS", ((0, "LANDING"), (1, "OFF"), (2, "TAXI"))), "above_side_below")
    p.push("DNLOCK", 470, 544, push_button("DN_LOCK_BTN", "DN LOCK REL"))
    p.hazard("DNLOCK")
    p.label("DN LOCK\nREL", "POS", "DNLOCK", "above")


def alt_gear_plate(g: PanelGroup):
    p = g.panel("ALT GEAR", 300, 240, 0, 658)
    p.toggle("HANDLE", 100, 136, selector("GEAR_ALT_HANDLE", "ALT GEAR", ((1, "PULL"), (0, "STOW")), guard=True), "above_below")
    p.label("ALT GEAR", "NAME", "HANDLE", "above")
    p.push("RESET", 220, 136, push_button("GEAR_ALT_BTN", "ALT GEAR RESET"))
    p.label("RESET", "NAME", "RESET", "above")


def hmcs_plate(g: PanelGroup):
    p = g.panel("HMCS", 324, 200, 316, 658)
    p.mark("HMCS", "TITLE", 52, 100, "panel name turned along the left edge", 90)
    p.knob("INT", "KNOB_M", 190, 128, knob("HMCS_INT_KNB", "HMCS SYMBOLOGY INT"))
    p.label("SYMBOLOGY\nINT", "NAME", "INT", "above")
    p.knob_labels("INT", "lower_sides", "OFF", "INC")


def gear_pages() -> list[dict]:
    g = PanelGroup("LANDING GEAR / HMCS", "f16c", scroll=True)
    gear_plate(g)
    alt_gear_plate(g)
    hmcs_plate(g)
    return [kit_page("LANDING GEAR / HMCS", [1, 3, 1, 2], g.build())]


def cmds_plate(g: PanelGroup):
    p = g.panel("CMDS", 600, 448, 0, 0)
    for n, (bios, legend) in enumerate((("LIGHT_CMDS_NO_GO", "NO GO"), ("LIGHT_CMDS_GO", "GO"), ("LIGHT_CMDS_DISP", "DISP"), ("LIGHT_CMDS_RDY", "RDY"))):
        p.lamp(f"S{n}", 72 + 76 * n, 64, lamp(bios, legend, "green"))
    p.display("CH", 404, 64, 96, 56, readout("CMDS_CH_AMOUNT", "CH", 4))
    p.display("FL", 516, 64, 96, 56, readout("CMDS_FL_AMOUNT", "FL", 4))
    p.toggle("RWR", 100, 188, selector("CMDS_PWR_SOURCHE_SW", "RWR", ((1, "ON"), (0, "OFF"))), "above_below")
    p.label("RWR", "NAME", "RWR", "above")
    p.toggle("CHSW", 404, 188, selector("CMDS_CH_EXP_CAT_SW", "CH", ((1, "ON"), (0, "OFF"))), "above_below")
    p.label("CH", "NAME", "CHSW", "above")
    p.toggle("FLSW", 516, 188, selector("CMDS_FL_EXP_CAT_SW", "FL", ((1, "ON"), (0, "OFF"))), "above_below")
    p.label("FL", "NAME", "FLSW", "above")
    p.toggle("JETT", 100, 330, selector("CMDS_JETT_SW", "JETT", ((1, "JETT"), (0, "OFF")), guard=True), "above_below")
    p.rotary("PRGM", 280, 330, {
        "id": "CMDS_PROG_KNB", "label": "PRGM", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "BIT", -105, True), (1, "1", -70), (2, "2", -20), (3, "3", 20), (4, "4", 70))),
    })
    p.label("PRGM", "NAME", "PRGM", "below")
    p.rotary("MODE", 462, 330, {
        "id": "CMDS_MODE_KNB", "label": "MODE", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "OFF", -135), (1, "STBY", -105), (2, "MAN", -75), (3, "SEMI", -35), (4, "AUTO", 35), (5, "BYP", 75))),
    })
    p.label("MODE", "NAME", "MODE", "below")


def dispense_plate(g: PanelGroup):
    p = g.panel("CHAFF/FLARE", 204, 204, 0, 464)
    p.push("BTN", 102, 126, push_button("CMDS_DISPENSE_BTN", "CHAFF/FLARE DISPENSE"))
    p.label("CHAFF/\nFLARE", "POS", "BTN", "above")


def cmds_pages() -> list[dict]:
    g = PanelGroup("CMDS", "f16c", scroll=True)
    cmds_plate(g)
    dispense_plate(g)
    return [kit_page("CMDS", [2, 3, 1, 2], g.build())]


def rwr_button(p: Panel, name: str, bios: str, label: str, x: int, y: int, *lamps: tuple, hold: float = BUTTON_HOLD):
    control = {**push_button(bios, label), "hold": hold}
    if len(lamps) == 1:
        control.update(lamp=lamps[0][0], legend=lamps[0][1], color=lamps[0][2])
    else:
        control["lamps"] = [lamp(*item) for item in lamps]
    p.push(name, x, y, control)
    p.label(label, "POS", name, "above")


def rwr_prime_plate(g: PanelGroup):
    p = g.panel("PRIME", 364, 304, 0, 0)
    rwr_button(p, "LAUNCH", "RWR_LAUNCH_BTN", "LAUNCH", 78, 106, ("LIGHT_RWR_MSL_LAUNCH", "MSL", "red"))
    rwr_button(p, "MODE", "RWR_MODE_BTN", "MODE", 182, 106, ("LIGHT_RWR_MODE_PRI", "PRI", "green"), ("LIGHT_RWR_MODE_OPEN", "OPEN", "green"))
    rwr_button(p, "HANDOFF", "RWR_HANDOFF_BTN", "HANDOFF", 286, 106, ("LIGHT_RWR_HANDOFF_UP", "UP", "green"), ("LIGHT_RWR_HANDOFF_H", "H", "green"))
    rwr_button(p, "UNKNOWN", "RWR_UNKNOWN_SHIP_BTN", "UNKNOWN", 78, 226, ("LIGHT_RWR_SHIP_U", "U", "green"), ("LIGHT_RWR_SHIP_UNK", "UNK", "green"))
    rwr_button(p, "SYSTEST", "RWR_SYS_TEST_BTN", "SYS TEST", 182, 226, ("LIGHT_RWR_SYSTEST_ON", "ON", "green"), ("LIGHT_RWR_SYSTEST", "TEST", "green"), hold=1.0)
    rwr_button(p, "TGTSEP", "RWR_T_BTN", "TGT SEP", 286, 226, ("LIGHT_RWR_TGTSEP_UP", "TGT", "green"), ("LIGHT_RWR_TGTSEP_DN", "SEP", "green"))


def rwr_azimuth_plate(g: PanelGroup):
    p = g.panel("AZIMUTH", 220, 304, 380, 0)
    p.mark("AZIMUTH\nINDICATOR", "NAME", 110, 84, "title of the plate, the scope itself is not drawn")
    p.knob("BRT", "KNOB_M", 110, 196, knob("RWR_INTENS_KNB", "AZIMUTH INDICATOR BRIGHTNESS"))
    p.label("BRT", "NAME", "BRT", "above")


def rwr_aux_plate(g: PanelGroup):
    p = g.panel("AUX", 600, 184, 0, 320)
    rwr_button(p, "SEARCH", "RWR_SEARCH_BTN", "SEARCH", 90, 106, ("LIGHT_RWR_SEARCH", "S", "green"))
    rwr_button(p, "ACTPWR", "RWR_ACT_PWR_BTN", "ACT/PWR", 198, 106, ("LIGHT_RWR_ACTIVITY", "ACT", "amber"), ("LIGHT_RWR_ACT_POWER", "POWER", "green"))
    rwr_button(p, "ALT", "RWR_ALT_BTN", "ALTITUDE", 306, 106, ("LIGHT_RWR_ALT_LOW", "LOW", "amber"), ("LIGHT_RWR_ALT", "ALT", "green"))
    rwr_button(p, "POWER", "RWR_PWR_BTN", "POWER", 414, 106, ("LIGHT_RWR_POWER", "PWR", "green"))
    p.knob("DIM", "KNOB_M", 522, 106, knob("RWR_IND_DIM_KNB", "DIM"))
    p.label("DIM", "NAME", "DIM", "above")


def threat_pages() -> list[dict]:
    g = PanelGroup("THREAT WARNING", "f16c")
    rwr_prime_plate(g)
    rwr_azimuth_plate(g)
    rwr_aux_plate(g)
    return [kit_page("THREAT WARNING", [3, 3, 1, 2], g.build())]


def iff_plate(g: PanelGroup):
    p = g.panel("IFF", 264, 232, 0, 0)
    p.mark("IFF", "TITLE", 52, 116, "panel name turned along the left edge", 90)
    p.rotary("CI", 130, 114, {
        "id": "IFF_C_I_KNB", "label": "C & I", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((1, "BACK UP", -35), (0, "UFC", 50))),
    })
    p.label("C & I", "NAME", "CI", "below")


def uhf_plate(g: PanelGroup):
    p = g.panel("UHF BACKUP", 600, 592, 0, 248)
    p.push("TEST", 90, 96, push_button("UHF_TEST_BTN", "TEST DISPLAY"))
    p.label("TEST\nDISPLAY", "POS", "TEST", "below")
    p.display("CHAN", 300, 96, 72, 56, readout("UHF_CHAN_DISP", "CHAN", 2))
    p.label("CHAN", "NAME", "CHAN", "above")
    p.rocker("CHAN_KNB", 378, 96, step_rocker("UHF_CHAN_KNB", "CHAN"))
    p.push("STATUS", 510, 96, push_button("UHF_STATUS_BTN", "STATUS"))
    p.label("STATUS", "POS", "STATUS", "below")
    p.display("FREQ", 300, 230, 288, 64, readout("UHF_FREQ_DISP", "FREQUENCY", 7))
    p.rotary("A32", 106, 346, {
        "id": "UHF_FREQ_100_KNB", "label": "A-3-2", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "A", -50, True), (1, "3", -80), (2, "2", -110))),
    })
    for bios, label, x in (("10", "10", 190), ("1", "1", 276), ("01", ".1", 362)):
        p.rocker(f"F{bios}", x, 346, step_rocker(f"UHF_FREQ_{bios}_KNB", label))
    p.rotary("F0025", 482, 346, {
        "id": "UHF_FREQ_0025_KNB", "label": "0.025 MHZ", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "00", -75), (1, "25", -25), (2, "50", 25), (3, "75", 75))),
    })
    p.rotary("FUNC", 140, 500, {
        "id": "UHF_FUNC_KNB", "label": "FUNCTION", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "OFF", -75), (1, "MAIN", -40), (2, "BOTH", 40), (3, "ADF", 75, True))),
    })
    p.toggle("SQL", 300, 500, selector("UHF_SQUELCH_SW", "SQUELCH", ((1, "ON"), (0, "OFF"))), "above_below")
    p.label("SQUELCH", "NAME", "SQL", "above")
    p.rotary("MODE", 460, 500, {
        "id": "UHF_MODE_KNB", "label": "MODE", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "MNL", -70), (1, "PRESET", 0), (2, "GRD", 70))),
    })


def uhf_pages() -> list[dict]:
    g = PanelGroup("UHF / IFF BACKUP", "f16c", scroll=True)
    iff_plate(g)
    uhf_plate(g)
    return [kit_page("UHF / IFF BACKUP", [4, 3, 2, 2], g.build())]


def left_eyebrow_plate(g: PanelGroup):
    p = g.panel("LEFT EYEBROW", 364, 284, 0, 0)
    p.push("MC", 170, 78, {**push_button("MASTER_CAUTION", "MASTER CAUTION"), "lamp": "LIGHT_MASTER_CAUTION", "color": "amber"})
    p.label("MASTER\nCAUTION", "POS", "MC", "left")
    p.lamp("TF", 264, 78, lamp("LIGHT_TF_FAIL", "TF-FAIL", "red"))
    p.push("ACK", 170, 178, push_button("F_ACK_BTN", "F-ACK"))
    p.label("F-ACK", "POS", "ACK", "below")
    p.push("IDENT", 270, 178, push_button("IFF_ID_BTN", "IFF IDENT"))
    p.label("IFF IDENT", "POS", "IDENT", "below")


def right_eyebrow_plate(g: PanelGroup):
    p = g.panel("RIGHT EYEBROW", 364, 208, 0, 300)
    lamps = (("LIGHT_ENG_FIRE", "ENG\nFIRE"), ("LIGHT_ENGINE", "ENGINE"), ("LIGHT_HYD_OIL_PRESS", "HYD/OIL\nPRESS"),
             ("LIGHT_FLCS", "FLCS"), ("LIGHT_DBU_ON", "DBU ON"), ("LIGHT_TO_LDG_CONFIG", "TO/LDG\nCONFIG"),
             ("LIGHT_CANOPY", "CANOPY"), ("LIGHT_OXY_LOW", "OXY\nLOW"))
    for n, (bios, legend) in enumerate(lamps):
        p.lamp(f"L{n}", 94 + 88 * (n % 3), 56 + 48 * (n // 3), lamp(bios, legend, "red"))


def aoa_plate(g: PanelGroup):
    p = g.panel("AOA INDEXER", 244, 284, 380, 0)
    p.knob("DIM", "KNOB_S", 84, 142, knob("AOA_INDEX_BRT_KNB", "AOA INDEXER DIMMING"))
    p.label("DIM", "NAME", "DIM", "above")
    for n, (bios, legend, color) in enumerate((("LIGHT_AOA_UP", "HIGH", "red"), ("LIGHT_AOA_MID", "OPT", "green"), ("LIGHT_AOA_DN", "LOW", "amber"))):
        p.lamp(f"L{n}", 170, 86 + 56 * n, lamp(bios, legend, color))


def ar_plate(g: PanelGroup):
    p = g.panel("AR / NWS", 244, 208, 380, 300)
    p.knob("DIM", "KNOB_S", 84, 104, knob("AR_STATUS_BRT_KNB", "AR STATUS DIMMING"))
    p.label("DIM", "NAME", "DIM", "above")
    for n, (bios, legend, color) in enumerate((("LIGHT_RDY", "RDY", "white"), ("LIGHT_AR_NWS", "AR\nNWS", "green"), ("LIGHT_DISC", "DISC", "red"))):
        p.lamp(f"L{n}", 170, 56 + 48 * n, lamp(bios, legend, color))


def eyebrow_pages() -> list[dict]:
    g = PanelGroup("EYEBROWS / INDEXERS", "f16c")
    left_eyebrow_plate(g)
    right_eyebrow_plate(g)
    aoa_plate(g)
    ar_plate(g)
    return [kit_page("EYEBROWS / INDEXERS", [1, 5, 1, 4], g.build())]


def misc_plate(g: PanelGroup):
    p = g.panel("MISC", 522, 412, 0, 0)
    p.mark("MISC", "TITLE", 52, 206, "panel name turned along the left edge", 90)
    p.toggle("RF", 130, 96, selector("RF_SW", "RF", ((2, "NORM"), (1, "QUIET"), (0, "SILENT"))), "right_triple")
    p.label("RF", "NAME", "RF", "above")
    p.lamp("ECM", 330, 96, lamp("LIGHT_ECM", "ECM", "green"))
    p.toggle("LASER", 130, 206, selector("LASER_ARM_SW", "LASER ARM", ((1, "LASER ARM"), (0, "OFF"))), "above_below")
    p.toggle("MASTER", 330, 206, selector("MASTER_ARM_SW", "MASTER ARM", ((0, "MASTER ARM"), (1, "OFF"), (2, "SIMULATE"))), "right_triple")
    p.toggle("ROLL", 130, 338, selector("AP_ROLL_SW", "AUTOPILOT ROLL", ((2, "HDG SEL"), (1, "ATT HOLD"), (0, "STRG SEL"))), "right_triple")
    p.label("ROLL", "NAME", "ROLL", "above")
    p.toggle("PITCH", 330, 338, selector("AP_PITCH_SW", "AUTOPILOT PITCH", ((2, "ALT HOLD"), (1, "A/P OFF"), (0, "ATT HOLD"))), "right_triple")
    p.label("PITCH", "NAME", "PITCH", "above")


def misc_pages() -> list[dict]:
    g = PanelGroup("MISC", "f16c")
    misc_plate(g)
    return [kit_page("MISC", [2, 5, 3, 1], g.build())]


def var_rocker(bios: str, label: str) -> dict:
    return {**step_rocker(bios, label), "steps": KNOB_STEP}


def air_data_plate(g: PanelGroup):
    p = g.panel("AIR DATA / SAI / ADI", 380, 468, 0, 0)
    p.rocker("IAS", 82, 152, var_rocker("AIRSPEED_SET_KNB", "IAS"))
    p.label("SET\nINDEX", "NAME", "IAS", "above")
    p.rocker("ALT", 178, 152, var_rocker("ALT_BARO_SET_KNB", "ALT"))
    p.label("BARO\nSET", "NAME", "ALT", "above")
    p.toggle("MODE", 274, 152, spring("ALT_MODE_LV", "ALTIMETER MODE", ((2, "PNEU"), (1, "OFF"), (0, "ELEC")), 1), "above_side_below")
    p.label("ALT\nMODE", "NAME", "MODE", "above")
    p.knob("ADI", "KNOB_M", 120, 340, knob("ADI_PITCH_TRIM", "ADI PITCH TRIM"))
    p.label("ADI\nTRIM", "NAME", "ADI", "above")
    p.knob("SAI", "KNOB_S", 264, 340, knob("SAI_PITCH_TRIM", "SAI PITCH TRIM"))
    p.label("SAI", "NAME", "SAI", "above")
    p.chip("SAI_PULL", "SAI", {
        "id": "SAI_CAGE", "label": "SAI PULL TO CAGE", "type": "selector", "style": "chip", "legend": "PULL",
        "positions": [{"value": 0, "label": "IN"}, {"value": 1, "label": "OUT"}],
    })


def fuel_qty_plate(g: PanelGroup):
    p = g.panel("FUEL QTY SEL", 244, 468, 396, 0)
    p.mark("FUEL QTY SEL", "NAME", 122, 52, "panel name above the knob")
    p.rotary("SEL", 100, 160, {
        "id": "FUEL_QTY_SEL_KNB", "label": "FUEL QTY SEL", "type": "selector", "style": "rotary",
        "positions": rotary_positions(((0, "NORM", 25), (1, "RSVR", 60), (2, "INT WING", 95), (3, "EXT WING", 150), (4, "EXT CTR", -150))),
    }, labels="fan")
    p.toggle("TRANS", 122, 374, selector("EXT_FUEL_TRANS_SW", "EXT FUEL TRANS", ((1, "NORM"), (0, "WING FIRST"))), "above_below")
    p.label("EXT FUEL\nTRANS", "NAME", "TRANS", "above")


def ehsi_plate(g: PanelGroup):
    p = g.panel("EHSI", 380, 468, 0, 484)
    p.mark("EHSI", "NAME", 190, 52, "title of the plate, the instrument itself is not drawn")
    p.display("RANGE", 130, 130, 96, 56, readout("EHSI_RANGE", "RANGE", 4))
    p.label("NM", "POS", "RANGE", "above")
    p.display("COURSE", 258, 130, 72, 56, readout("EHSI_COURSE", "COURSE", 3))
    p.label("CRS", "POS", "COURSE", "above")
    p.display("LEFT", 90, 240, 72, 56, readout("EHSI_MODE_LEFT", "MODE", 3))
    p.display("RIGHT", 170, 240, 72, 56, readout("EHSI_MODE_RIGHT", "MODE", 3))
    p.mark("MODE", "POS", 130, 196, "title of the two mode windows")
    p.push("M", 294, 240, {**push_button("EHSI_MODE", "EHSI MODE"), "legend": "M"})
    p.rocker("HDG", 62, 356, var_rocker("EHSI_HDG_SET_KNB", "HDG"))
    p.push("HDG_PUSH", 142, 356, push_button("EHSI_HDG_SET_BTN", "HDG SET PUSH"))
    p.label("ADJ HDG", "POS", "HDG_PUSH", "below")
    p.rocker("CRS", 222, 356, var_rocker("EHSI_CRS_SET_KNB", "CRS"))
    p.push("CRS_PUSH", 302, 356, push_button("EHSI_CRS_SET", "CRS SET PUSH"))
    p.label("BRT", "POS", "CRS_PUSH", "below")


def clock_plate(g: PanelGroup):
    p = g.panel("CLOCK", 244, 266, 396, 484)
    p.mark("CLOCK", "NAME", 122, 52, "title of the plate, the instrument itself is not drawn")
    p.rocker("WIND", 74, 140, var_rocker("CLOCK_WIND", "WIND"))
    p.push("SET", 154, 140, push_button("CLOCK_SET", "CLOCK SET PULL"))
    p.label("PULL\nSET", "POS", "SET", "below")


def instruments_pages() -> list[dict]:
    g = PanelGroup("INSTRUMENTS", "f16c", scroll=True)
    air_data_plate(g)
    fuel_qty_plate(g)
    ehsi_plate(g)
    clock_plate(g)
    return [kit_page("INSTRUMENTS", [4, 6, 2, 3], g.build())]


def seat_arming_plate(g: PanelGroup):
    p = g.panel("SEAT ARMING", 160, 240, 0, 0)
    p.toggle("ARM", 80, 148, selector("SEAT_EJECT_SAFE", "SEAT ARMING LEVER", ((1, "LOCKED"), (0, "ARMED"))), "above_below")
    p.label("SEAT\nARMING", "NAME", "ARM", "above")


def seat_adj_plate(g: PanelGroup):
    p = g.panel("SEAT ADJ", 288, 336, 176, 0)
    p.toggle("ADJ", 96, 192, spring("SEAT_ADJ", "SEAT ADJ", ((0, "UP"), (1, "OFF"), (2, "DOWN")), 1), "above_side_below")
    p.label("SEAT ADJ", "NAME", "ADJ", "above")
    p.bar("HEIGHT", 210, 192, {"id": "SEAT_HEIGHT", "label": "SEAT HEIGHT", "type": "bar", "max": 65535})
    p.label("SEAT\nHEIGHT", "NAME", "HEIGHT", "above")


def seat_pages() -> list[dict]:
    g = PanelGroup("SEAT", "f16c")
    seat_arming_plate(g)
    seat_adj_plate(g)
    return [kit_page("SEAT", [6, 6, 2, 3], g.build())]


CAUTION_LAMPS = (
    ("LIGHT_FLCS_FAULT", "FLCS\nFAULT"), ("LIGHT_ENGINE_FAULT", "ENGINE\nFAULT"), ("LIGHT_AVIONICS_FAULT", "AVIONICS\nFAULT"), ("LIGHT_SEAT_NOT", "SEAT NOT\nARMED"),
    ("LIGHT_ELEC_SYS", "ELEC SYS"), ("LIGHT_SEC", "SEC"), ("LIGHT_EQUIP_HOT", "EQUIP\nHOT"), ("LIGHT_NWS_FAIL", "NWS\nFAIL"),
    ("LIGHT_PROBE_HEAT", "PROBE HEAT"), ("LIGHT_FUEL_OIL_HOT", "FUEL/OIL\nHOT"), ("LIGHT_RADAR_ALT", "RADAR\nALT"), ("LIGHT_ANTI_SKID", "ANTI\nSKID"),
    ("LIGHT_CADC", "CADC"), ("LIGHT_INLET_ICING", "INLET\nICING"), ("LIGHT_IFF", "IFF"), ("LIGHT_HOOK", "HOOK"),
    ("LIGHT_STORES_CONFIG", "STORES\nCONFIG"), ("LIGHT_OVERHEAT", "OVERHEAT"), ("LIGHT_NUCLEAR", "NUCLEAR"), ("LIGHT_OBOGS", "OBOGS"),
    ("LIGHT_ATF_NOT", "ATF NOT\nENGAGED"), ("LIGHT_EEC", "EEC"), None, ("LIGHT_CABIN_PRESS", "CABIN\nPRESS"),
    ("LIGHT_FWD_FUEL_LOW", "FWD\nFUEL LOW"), ("LIGHT_BUC", "BUC"), None, None,
    ("LIGHT_AFT_FUEL_LOW", "AFT\nFUEL LOW"), None, None, None,
)


def caution_plate(g: PanelGroup):
    p = g.panel("CAUTION", 640, 448, 0, 0)
    for n, cell in enumerate(CAUTION_LAMPS):
        if cell:
            p.lamp(f"L{n}", 104 + 144 * (n % 4), 56 + 48 * (n // 4), lamp(cell[0], cell[1], "amber"), "LAMP_WIDE")


def caution_pages() -> list[dict]:
    g = PanelGroup("CAUTION", "f16c")
    caution_plate(g)
    return [kit_page("CAUTION", [1, 9, 2, 2], g.build())]


def hud_plate(g: PanelGroup):
    p = g.panel("HUD CONTROL", 462, 312, 0, 0)
    p.mark("HUD", "TITLE", 52, 156, "panel name turned along the left edge", 90)
    brightness = selector("HUD_BRT_SW", "HUD BRIGHTNESS", ((0, "DAY"), (1, "AUTO BRT"), (2, "NIGHT")))
    brightness["positions"][1]["disabled"] = True
    switches = (
        ("SCALES", selector("HUD_SCALES_SW", "HUD SCALES", ((0, "VV/VAH"), (1, "VAH"), (2, "OFF")))),
        ("FPM", selector("HUD_FP_MARKER_SW", "HUD FLIGHTPATH MARKER", ((0, "ATT/FPM"), (1, "FPM"), (2, "OFF")))),
        ("DED", selector("HUD_DED_DATA_SW", "HUD DED/PFLD", ((0, "DED DATA"), (1, "PFL"), (2, "OFF")))),
        ("RETICLE", selector("HUD_DEPRESS_RET_SW", "HUD DEPRESSIBLE RETICLE", ((0, "STBY"), (1, "PRI"), (2, "OFF")))),
        ("SPEED", selector("HUD_SPEED_SW", "HUD VELOCITY", ((0, "CAS"), (1, "TAS"), (2, "GND SPD")))),
        ("BRT", brightness),
    )
    for n, (name, control) in enumerate(switches):
        p.toggle(name, 130 + 120 * (n % 3), 92 + 128 * (n // 3), control, "above_side_below")


def hud_pages() -> list[dict]:
    g = PanelGroup("HUD CONTROL", "f16c")
    hud_plate(g)
    return [kit_page("HUD CONTROL", [3, 9, 1, 2], g.build())]


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
    *canopy_pages(),
    *fuel_pages(),
    *flcs_pages(),
    *elec_pages(),
    *ext_lighting_pages(),
    *ecm_pages(),
    *audio_pages(),
    *gear_pages(),
    *cmds_pages(),
    *threat_pages(),
    *uhf_pages(),
    *eyebrow_pages(),
    *misc_pages(),
    *instruments_pages(),
    *seat_pages(),
    *caution_pages(),
    *hud_pages(),
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
