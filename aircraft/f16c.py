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


def trim_knob(bios: str, label: str) -> dict:
    return {"id": bios, "label": label, "type": "knob", "step": KNOB_STEP, "sweep": [-135, 135]}


def lamp(bios: str, legend: str, color: str) -> dict:
    return {"id": bios, "legend": legend, "color": color}


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
    p.knob("ROLL", "KNOB_M", 192, 104, trim_knob("ROLL_TRIM", "ROLL TRIM"))
    p.label("ROLL TRIM", "NAME", "ROLL", "above")
    p.knob_labels("ROLL", "lower_sides", "L WING\nDN", "R WING\nDN")
    p.toggle("DISC", 368, 148, selector("TRIM_AP_DISC_SW", "TRIM/AP DISC", ((1, "NORM"), (0, "DISC"))), "above_below")
    p.label("TRIM/AP\nDISC", "NAME", "DISC", "above")
    p.knob("YAW", "KNOB_M", 132, 284, trim_knob("YAW_TRIM", "YAW TRIM"))
    p.label("YAW TRIM", "NAME", "YAW", "above")
    p.knob_labels("YAW", "lower_sides", "L", "R")
    p.knob("PITCH", "KNOB_M", 288, 284, trim_knob("PITCH_TRIM", "PITCH TRIM"))
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
