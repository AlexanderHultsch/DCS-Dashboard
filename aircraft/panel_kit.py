"""Panel kit: the layout compiler of the cockpit panel pages (docs/COCKPIT_FIXES.md, sections 2 to 4 and 8).

Every size is in design units (du) and defined once, below. A page makes one Panel (plate width and height in
du, even numbers), places parts by their centre on the 1 du grid and attaches labels to them; it never gives a
size, except for a display (a glass screen with live text), whose size the content decides, and the travel of the
power levers (within limits). The plate brings four identical corner ears with a SCREW_L in the centre of each. Further screws are
placed only by naming an x line and a y line from the line table:

    x lines: L R (plate edges), CX (middle), SL SR (corner screws), NAME.cx (every placed part)
    y lines: T B (plate edges), CY (middle), ST SB (corner screws), NAME.cy (every placed part)

Panel.build() checks the layout (LayoutError on a collision) and returns the page data in the format
web/index.html draws: box [w, h], controls (the given control data plus "at", "kit" and, for a guarded part,
"cover_at"; a dual-function knob also "mark" and "dot"; a rotary also "knob"; a power lever or the slider also
"handle", a lever the "y" of every position; the flap of a button is a control of its own), indicators (the lamps and
letters of a dial), print ([text, x, y, size, width] or with a rotation) and art.
A page with several physical panels is a PanelGroup: one Panel per plate at a page offset, 16 du apart.

    p = Panel("EMERGENCY", 580, 276)
    p.mark("EMERGENCY", "TITLE", "CX", 52, "panel title")
    p.push("GUARD", 114, 166, guard_button, frame=True)
    p.label("GUARD", "NAME", "GUARD", "above")
    p.screw("S", "GUARD.cx", "SB")
    page = p.build()
"""

import math

REF = (640, 600)
GAP = 8
MARGIN = 36
EAR_CLEAR = 12

PARTS = {
    # face: the lamp face inside the bezel; frame: the white frame variant; legend: font size of the face legend
    "PUSH": {"w": 84, "h": 84, "face": 60, "frame": 100, "frame_stroke": 4, "legend": 12},
    "PUSH_SMALL": {"w": 56, "h": 56},
    "ROUND": {"w": 64, "h": 64},
    "PLUNGER": {"w": 100, "h": 100},
    # w / h: the ring; band: the touch square (a guarded switch has one band per position instead)
    "TOGGLE": {"w": 56, "h": 56, "lever": 40, "band": 60},
    # w / h: the tick ring; knob: the knob diameter; tick: inner and outer radius of the ticks
    "ROTARY": {"w": 100, "h": 100, "knob": 72, "tick": (42, 50)},
    "KNOB_L": {"w": 96, "h": 96},
    "KNOB_M": {"w": 72, "h": 72},
    "KNOB_S": {"w": 56, "h": 56},
    # two halves of 60 du are 57 px at the scale of a 1024 x 768 screen: the touch minimum is 56 px
    "ROCKER": {"w": 52, "h": 120},
    "CHIP": {"w": 64, "h": 22},
    "DIAL": {"w": 112, "h": 112},
    # w / h: the grip of a power lever and of the slider; it slides in a slot (the grip plus SLOT pad on every side)
    "LEVER": {"w": 40, "h": 40},
    # w / h: the slot of the slider; its grip is a LEVER grip
    "SLIDER": {"w": 56, "h": 240},
    # selector dot of a dual-function knob; touch: square beside the knob (clear: its distance to the knob),
    # pitch: centre distance of two marks, gap: dot centre to the knob edge
    "MARK": {"w": 10, "h": 10, "touch": 56, "clear": 6, "pitch": 64, "gap": 14},
}
KNOBS = ("KNOB_L", "KNOB_M", "KNOB_S")
# DISPLAY has no size here: the page gives it; inset: glass border and padding between the glass and its text
DISPLAY = {"inset": 6, "border": 3}
# slot of a lever or the slider: pad around the grip, border, tick beside a lever mark; reach: how far the touch area of the
# levers goes past the end marks; travel: limits of the page's choice of the grip travel from LOCKOUT to OFF;
# arrow: width of the arrow heads in the slider legend
SLOT = {"pad": 8, "border": 3, "tick": 8, "reach": 44, "travel": (360, 440), "arrow": 16}
# the plain cover of a button (a hinged flap, not a guard cover): the button plus this margin on every side
FLAP = {"margin": 8}
GUARD_COVER = {"margin": 12, "frame": 14, "lock": 24}
HAZARD_PAD = {"margin": 20, "period": 34, "border": 2}
# dark housing around a part (and its cover); hazard strip: fixed width, as tall as the housing less the inset
HOUSING = {"margin": 12, "border": 3}
HAZARD_STRIP = {"w": 32, "inset": 8}
PLATE = {"radius": 6, "border": 3}
EAR = {"w": 52, "h": 52, "border": 2}
SCREWS = {"L": 26, "M": 18, "S": 12}
SLOT_ANGLES = (15, 100, 65, 140)
# label style: font size and estimated glyph width; the page draws the text at exactly that width
STYLES = {"TITLE": (32, 19), "NAME": (24, 14), "POS": (20, 12), "SMALL": (16, 10)}
# a face legend is plain text, not stretched to a width: estimated in em per glyph for a wide sans font
LEGEND_GLYPH = 0.74
# position labels of a toggle, one (side, rotation) per position in the order of the positions (None: not printed);
# along shifts a label along its side of the part and keeps it from pushing further labels out
TOGGLE_LABELS = {
    "above_side_below": (("above", 0), ("right", 90), ("below", 0)),
    "above_left_below": (("above", 0), ("left", 0), ("below", 0)),
    "above_below": (("above", 0), ("below", 0)),
    "left_right": (("left", 0), None, ("right", 0)),
    "right_pair": (("right", 0, -24), ("right", 0, 24)),
    "right_triple": (("right", 0, -28), ("right", 0, 0), ("right", 0, 28)),
}
# position labels of a rotary, each (circle radius, two words on two lines): ticks: level with the end of the tick;
# fan: on a wider circle so that the labels stay clear of each other
ROTARY_LABELS = {"ticks": (PARTS["ROTARY"]["tick"][1], False), "fan": (78, True)}
# printed scale marks of a knob, one (side, along) per mark; along is a fraction of the knob half size (down or right is positive)
KNOB_LABELS = {
    "lower_sides": (("left", 0.7), ("right", 0.7)),
    "below_sides": (("below", -0.6), ("below", 0.6)),
    "signal": (("left", 0.7), ("right", -0.1), ("right", 0.7)),
}
# symbols of a small key are given in their own units and drawn at this scale
GLYPH_SCALE = 2
# the dial face: stroke, a tick every 10 degrees, every third one longer
DIAL_FACE = {"stroke": 2, "long": 9, "short": 5}
GROUP_GAP = 16
RULE_STROKE = 3


class LayoutError(ValueError):
    pass


def centred(cx, cy, w, h):
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def grow(box, d):
    return (box[0] - d, box[1] - d, box[2] + d, box[3] + d)


def union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def within(a, b):
    return b[0] <= a[0] and b[1] <= a[1] and a[2] <= b[2] and a[3] <= b[3]


def num(v):
    return int(v) if float(v).is_integer() else v


def xywh(box):
    return [num(box[0]), num(box[1]), num(box[2] - box[0]), num(box[3] - box[1])]


def legend(text, style, cx, cy):
    """Text drawn by a part itself (a rocker name, a key letter), centred on the part."""
    size, glyph = STYLES[style]
    return {"shape": "text", "at": [cx, cy], "text": text, "size": size, **({"width": len(text) * glyph} if len(text) > 1 else {})}


def text_size(text, style, rotate):
    size, glyph = STYLES[style]
    lines = text.split("\n")
    w, h = max(len(t) for t in lines) * glyph, size * len(lines)
    return (h, w) if rotate % 180 else (w, h)


class Panel:
    def __init__(self, name: str, w: int, h: int):
        if w % 2 or h % 2 or not (0 < w <= REF[0] and 0 < h <= REF[1]):
            raise LayoutError(f"{name}: plate {w} x {h} du must be even and at most {REF[0]} x {REF[1]}")
        self.name, self.w, self.h = name, w, h
        ex, ey = EAR["w"] // 2, EAR["h"] // 2
        self.xs = {"L": 0, "R": w, "CX": w // 2, "SL": ex, "SR": w - ex}
        self.ys = {"T": 0, "B": h, "CY": h // 2, "ST": ey, "SB": h - ey}
        self.ears = [(x, y, x + EAR["w"], y + EAR["h"]) for y in (0, h - EAR["h"]) for x in (0, w - EAR["w"])]
        self.parts = {}
        self.labels = []
        self.decor = []
        self.indicators = []
        self.screws = []
        for y in ("ST", "SB"):
            for x in ("SL", "SR"):
                self._screw("L", x, y)

    def fail(self, message: str):
        raise LayoutError(f"{self.name}: {message}")

    def _part(self, name: str, kind: str, cx: int, cy: int, control: dict, size: tuple | None = None) -> dict:
        if name in self.parts or "." in name:
            self.fail(f"part name {name!r} is taken or has a dot")
        if not (isinstance(cx, int) and isinstance(cy, int)):
            self.fail(f"part {name} must sit on the 1 du grid, got ({cx}, {cy})")
        if "at" in control:
            self.fail(f"part {name}: the kit sizes and places the control, remove its 'at'")
        body = centred(cx, cy, *(size or (PARTS[kind]["w"], PARTS[kind]["h"])))
        part = {
            "name": name, "kind": kind, "cx": cx, "cy": cy, "control": control, "kit": {"part": kind},
            "body": body, "outer": body, "inner": body, "touch": body, "cover": None, "pad": None, "housing": None, "round": False,
            "art": [], "edges": {}, "members": [control], "marks": [], "knob": None, "extras": [],
        }
        if control.get("guard"):
            part["cover"] = part["outer"] = part["inner"] = grow(body, GUARD_COVER["margin"])
            part["kit"].update(cover_frame=GUARD_COVER["frame"], cover_lock=GUARD_COVER["lock"])
        self.parts[name] = part
        self.xs[name + ".cx"] = cx
        self.ys[name + ".cy"] = cy
        return part

    def push(self, name: str, cx: int, cy: int, control: dict, frame: bool = False, flap: dict | None = None) -> dict:
        """Square pushbutton (bezel and face, optional lamp legend), with the white frame centred on it. A flap is the control
        of a plain hinged cover: the button plus the FLAP margin on every side, centred on the button."""
        spec = PARTS["PUSH"]
        part = self._part(name, "PUSH", cx, cy, control)
        part["kit"].update(face=spec["face"], legend_size=spec["legend"])
        for text in [control.get("legend")] + [lamp["legend"] for lamp in control.get("lamps", [])]:
            if text and len(text) * spec["legend"] * LEGEND_GLYPH > spec["face"]:
                self.fail(f"legend {text!r} of {name} is wider than the {spec['face']} du face")
        if frame:
            box = centred(cx, cy, spec["frame"], spec["frame"])
            part["outer"] = part["inner"] = union(part["body"], box)
            if part["cover"]:
                part["cover"] = part["outer"] = part["inner"] = grow(part["outer"], GUARD_COVER["margin"])
            stroke = spec["frame_stroke"]
            part["art"].append({"shape": "outline", "at": xywh(grow(box, -stroke / 2)), "stroke": stroke, "for": control["id"]})
        if flap:
            part["outer"] = part["inner"] = grow(part["outer"], FLAP["margin"])
            part["extras"].append((flap, part["outer"]))
        return part

    def plunger(self, name: str, cx: int, cy: int, control: dict) -> dict:
        """Round plunger pushbutton; a guarded one gets a round cover."""
        part = self._part(name, "PLUNGER", cx, cy, control)
        part["round"] = True
        return part

    def toggle(self, name: str, cx: int, cy: int, control: dict, labels: str | None = None) -> dict:
        """Toggle switch (ring and lever): one touch square, or one band per position when guarded; optional position label preset."""
        spec = PARTS["TOGGLE"]
        part = self._part(name, "TOGGLE", cx, cy, control)
        part["kit"].update(ring=spec["w"], lever=spec["lever"])
        n = len(control["positions"])
        band = spec["band"]
        if control.get("guard"):
            part["touch"] = centred(cx, cy, *((band * n, band) if control.get("orient") == "h" else (band, band * n)))
        else:
            part["touch"] = centred(cx, cy, band, band)
        if labels:
            preset = TOGGLE_LABELS[labels]
            if len(preset) != n:
                self.fail(f"label preset {labels} is for {len(preset)} positions, {name} has {n}")
            for position, spot in zip(control["positions"], preset):
                if spot:
                    self.label(position["label"], "POS", name, *spot)
        return part

    def round(self, name: str, cx: int, cy: int, control: dict) -> dict:
        """Round pushbutton or cap."""
        return self._part(name, "ROUND", cx, cy, control)

    def push_small(self, name: str, cx: int, cy: int, control: dict, glyph) -> dict:
        """Small flat key. The glyph is a letter or a symbol (width, height, [(path, stroke, filled)]) in its own units."""
        part = self._part(name, "PUSH_SMALL", cx, cy, control)
        part["art"].append({"shape": "bracket", "at": xywh(part["body"])})
        if isinstance(glyph, str):
            part["art"].append(legend(glyph, "TITLE", cx, cy))
        else:
            w, h, paths = glyph
            at = xywh(centred(cx, cy, w * GLYPH_SCALE, h * GLYPH_SCALE))
            part["art"] += [{"shape": "path", "at": at, "d": d, "width": stroke, "scale": GLYPH_SCALE, **({"fill": True} if filled else {})} for d, stroke, filled in paths]
        return part

    def rocker(self, name: str, cx: int, cy: int, control: dict) -> dict:
        """Vertical rocker with an up and a down half; its name (the control label) is printed between the two arrows."""
        part = self._part(name, "ROCKER", cx, cy, control)
        part["art"] += [{"shape": "bracket", "at": xywh(part["body"])}, legend(control["label"], "POS", cx, cy)]
        return part

    def rotary(self, name: str, cx: int, cy: int, control: dict, turned: tuple = (), labels: str = "ticks") -> dict:
        """Rotary selector: a dark knob inside a ring of ticks, one tick per position angle. The position labels sit outside
        the ring on the side the angle points to, placed by the ROTARY_LABELS preset; the texts in turned are rotated."""
        spec = PARTS["ROTARY"]
        part = self._part(name, "ROTARY", cx, cy, control)
        part["knob"] = [cx, cy, spec["knob"] // 2]
        inner, outer = spec["tick"]
        reach, split = ROTARY_LABELS[labels]
        for position in control["positions"]:
            angle = math.radians(position["angle"])
            dx, dy = math.sin(angle), -math.cos(angle)
            part["art"].append({"shape": "line", "at": [round(cx + inner * dx, 1), round(cy + inner * dy, 1), round((outer - inner) * dx, 1), round((outer - inner) * dy, 1)]})
            if abs(dx) >= abs(dy):
                side, along = ("right" if dx > 0 else "left"), round(reach * dy)
            else:
                side, along = ("below" if dy > 0 else "above"), round(reach * dx)
            text = position["label"].replace(" ", "\n") if split else position["label"]
            self.label(text, "POS", name, side, 90 if position["label"] in turned else 0, along)
        return part

    def display(self, name: str, cx: int, cy: int, w: int, h: int, control: dict) -> dict:
        """Glass screen with live text: the only part whose size (even du) the page chooses. The control is the text area, the glass less its inset."""
        if w % 2 or h % 2:
            self.fail(f"display {name}: {w} x {h} du must be even")
        part = self._part(name, "DISPLAY", cx, cy, control, (w, h))
        part["touch"] = grow(part["body"], -DISPLAY["inset"])
        part["art"].append({"shape": "glass", "at": xywh(grow(part["body"], -DISPLAY["border"] / 2)), "for": control["id"]})
        return part

    def dial(self, name: str, cx: int, cy: int) -> dict:
        """Round indicator face with a ring of ticks. Its lamps and letters are added with indicator()."""
        part = self._part(name, "DIAL", cx, cy, {})
        r, face = PARTS["DIAL"]["w"] // 2, DIAL_FACE
        ticks = ""
        for i in range(36):
            a = math.radians(i * 10)
            inner = r - (face["long"] if i % 3 == 0 else face["short"])
            ticks += f"M{round(r + inner * math.sin(a), 1)} {round(r - inner * math.cos(a), 1)}L{round(r + r * math.sin(a), 1)} {round(r - r * math.cos(a), 1)}"
        d = f"M0 {r}a{r} {r} 0 1 0 {r * 2} 0a{r} {r} 0 1 0 {-r * 2} 0" + ticks
        part["art"].append({"shape": "path", "at": xywh(part["body"]), "d": d, "width": face["stroke"], "part": "DIAL", "name": name})
        return part

    def indicator(self, name: str, indicator: dict):
        """Lamp or letter of a dial: its box ('at') must lie inside the dial."""
        x, y, w, h = indicator["at"]
        if not within((x, y, x + w, y + h), self.parts[name]["body"]):
            self.fail(f"indicator {indicator['label']!r} is not inside {name}")
        self.indicators.append(indicator)

    def knob(self, name: str, kind: str, cx: int, cy: int, control: dict | list, marks: tuple = ()) -> dict:
        """Knob. A dual-function knob takes a list of controls (the first is shown) and one selector mark text each;
        the marks are stacked beside the knob on its left and choose the control."""
        if kind not in KNOBS:
            self.fail(f"knob {name}: {kind} is not one of {', '.join(KNOBS)}")
        members = control if isinstance(control, list) else [control]
        wanted = len(members) if len(members) > 1 else 0
        if len(marks) != wanted:
            self.fail(f"knob {name}: {len(members)} control(s) take {wanted} selector marks, got {len(marks)}")
        part = self._part(name, kind, cx, cy, members[0])
        part["members"] = members
        spec = PARTS["MARK"]
        left = int(part["body"][0])
        for i, text in enumerate(marks):
            y = cy + round((i - (len(marks) - 1) / 2) * spec["pitch"])
            dot = self._part(f"{name}_{i}", "MARK", left - spec["gap"], y, {})
            dot["touch"] = (left - spec["clear"] - spec["touch"], y - spec["touch"] / 2, left - spec["clear"], y + spec["touch"] / 2)
            part["marks"].append(dot)
            self.label(text, "POS", f"{name}_{i}", "left")
        return part

    def knob_labels(self, name: str, preset: str, *texts: str):
        """Printed scale marks of a knob (OFF, BRT, MIN, MAX ...) from the preset of their arrangement on the photos."""
        part = self.parts[name]
        if part["kind"] not in KNOBS:
            self.fail(f"knob labels: {name} is not a knob")
        spots = KNOB_LABELS[preset]
        if len(spots) != len(texts):
            self.fail(f"knob label preset {preset} is for {len(spots)} marks, {name} got {len(texts)}")
        half = PARTS[part["kind"]]["w"] // 2
        for text, (side, along) in zip(texts, spots):
            self.label(text, "POS", name, side, 0, round(along * half))

    def levers(self, name: str, cx: int, cy: int, travel: int, controls: tuple, marks: tuple, names: tuple, left_marks: tuple = ()):
        """The two power levers: one slot each, side by side with cx between them, a LEVER grip in each. The grips travel
        travel du (the page's choice within the SLOT limits) from the top mark (the last position) to the bottom mark (the
        first), a mark at every position at a distance that follows the position value, so the grip stands level with the
        mark text of its position. A tick sits on the outer side of each slot at every mark, the mark texts (one per position,
        None: not printed) right of the right slot and, if given, left of the left slot, the lever names below the slots
        (moved apart if wider than the slots). A lever touches in one band per mark, from its slot to the end of its mark
        texts. Parts: NAME_1 (left), NAME_2. The lever geometry is in page coordinates: use it on a Panel, not in a PanelGroup."""
        lo, hi = SLOT["travel"]
        positions = controls[0]["positions"]
        if travel % 2 or not lo <= travel <= hi:
            self.fail(f"levers {name}: travel {travel} must be even and within {lo} to {hi} du")
        if controls[1]["positions"] != positions or len(marks) != len(positions) or (left_marks and len(left_marks) != len(positions)):
            self.fail(f"levers {name}: both levers and all mark texts need the same positions")
        grip, pad, tick = PARTS["LEVER"], SLOT["pad"], SLOT["tick"]
        w, h = grip["w"] + 2 * pad, travel + grip["h"] + 2 * pad
        top, bottom = cy - travel // 2, cy + travel // 2
        ys = [bottom - round(travel * p["value"] / positions[-1]["value"]) for p in positions]
        for side, (control, texts) in enumerate(zip(controls, (left_marks, marks))):
            x = cx + (2 * side - 1) * (w // 2)
            lever = {**control, "positions": [{**p, "y": y} for p, y in zip(positions, ys)], "handle": [x, grip["w"], grip["h"]]}
            part = self._part(f"{name}_{side + 1}", "LEVER", x, cy, lever, (w, h))
            x0, y0, x1, y1 = part["body"]
            part["kit"].update(slot=xywh(grow(part["body"], -SLOT["border"] / 2)))
            part["outer"] = (x0 - tick * (1 - side), y0, x1 + tick * side, y1)
            part["art"] += [{"shape": "line", "at": [x1 if side else x0 - tick, y, tick, 0]} for y in ys]
            widest = max((text_size(t, "POS", 0)[0] for t in texts if t), default=0)
            reach = tick + (GAP + widest if widest else 0)
            part["touch"] = (x0 - reach if side == 0 else x0, top - SLOT["reach"], x1 if side == 0 else x1 + reach, bottom + SLOT["reach"])
            for text, y in zip(texts, ys):
                if text:
                    self.label(text, "POS", part["name"], "right" if side else "left", 0, y - cy)
            self.label(names[side], "POS", part["name"], "below", 0, (2 * side - 1) * max(0, (text_size(names[side], "POS", 0)[0] - (w - GAP)) // 2))

    def slider(self, name: str, cx: int, cy: int, control: dict, top: str, bottom: str, word: str) -> dict:
        """Slider: a LEVER grip in a slot, the value from 0 at the bottom to the maximum at the top. The legend sits right of the
        slot in one centred column, GAP du between its items: the top text level with the top of the slot, an arrow up, the
        word spelled downwards, an arrow down and the bottom text level with the bottom of the slot."""
        spec, grip = PARTS["SLIDER"], PARTS["LEVER"]
        part = self._part(name, "SLIDER", cx, cy, {**control, "handle": [cx, grip["w"], grip["h"]]})
        x0, y0, x1, y1 = part["body"]
        reach = SLOT["pad"] + grip["h"] / 2
        part["kit"].update(slot=xywh(grow(part["body"], -SLOT["border"] / 2)), track=[num(y0 + reach), num(y1 - reach)])
        letters = "\n".join(word)
        (tw, th), (lw, lh), (bw, bh) = (text_size(t, "POS", 0) for t in (top, letters, bottom))
        mid = x1 + GAP + max(tw, lw, bw) / 2
        arrow = (spec["h"] - th - bh - lh - 4 * GAP) / 2
        self._add_label(top, "POS", centred(mid, y0 + th / 2, tw, th), 0)
        self._add_label(letters, "POS", centred(mid, cy, lw, lh), 0)
        self._add_label(bottom, "POS", centred(mid, y1 - bh / 2, bw, bh), 0)
        head = SLOT["arrow"]
        part["art"].append({"shape": "arrow", "at": [num(mid - head / 2), num(y0 + th + GAP), head, num(arrow)], "up": True})
        part["art"].append({"shape": "arrow", "at": [num(mid - head / 2), num(cy + lh / 2 + GAP), head, num(arrow)]})
        return part

    def hazard(self, name: str, label: str | None = None, style: str = "NAME", side: str = "right") -> dict:
        """Striped pad around a part (or its cover), the part centred in it; optionally a label on a slot inside."""
        part = self.parts[name]
        if part["pad"] or part["edges"]:
            self.fail(f"the hazard pad of {name} comes once and before its labels")
        inner = part["outer"]
        mx = my = HAZARD_PAD["margin"]
        slot = None
        if label:
            w, h = text_size(label, style, 0)
            w, h = w + GAP + w % 2, h + GAP
            if side in ("left", "right"):
                mx = max(mx, w + 2 * GAP)
                x = inner[2] + GAP if side == "right" else inner[0] - GAP - w
                slot = (x, part["cy"] - h / 2, x + w, part["cy"] + h / 2)
            elif side in ("above", "below"):
                my = max(my, h + 2 * GAP)
                y = inner[3] + GAP if side == "below" else inner[1] - GAP - h
                slot = (part["cx"] - w / 2, y, part["cx"] + w / 2, y + h)
            else:
                self.fail(f"pad label side {side!r} is not above, below, left or right")
        pad = (inner[0] - mx, inner[1] - my, inner[2] + mx, inner[3] + my)
        part["pad"] = part["outer"] = pad
        border = HAZARD_PAD["border"]
        art = [{"shape": "hazard", "at": xywh(grow(pad, -border / 2)), "hole": xywh(inner), "border": border, "period": HAZARD_PAD["period"], "for": part["control"]["id"]}]
        if part["round"]:
            art[0]["round"] = True
        if slot:
            art.append({"shape": "slot", "at": xywh(slot)})
            self._add_label(label, style, grow(slot, -GAP / 2), 0, inside=name)
        part["art"][:0] = art
        return part

    def housing(self, name: str) -> dict:
        """Dark housing around a part (and its cover), the part centred in it; labels attach outside it."""
        part = self.parts[name]
        if part["pad"] or part["edges"]:
            self.fail(f"the housing of {name} comes once, without a hazard pad and before its labels")
        box = grow(part["outer"], HOUSING["margin"])
        part["housing"] = part["pad"] = part["outer"] = box
        part["art"].append({"shape": "slot", "at": xywh(grow(box, -HOUSING["border"] / 2)), "for": part["control"]["id"]})
        return part

    def strip(self, name: str, side: str):
        """Decorative hazard strip against the left or right side of a housing, as tall as the housing less the inset."""
        part = self.parts[name]
        if not part["housing"]:
            self.fail(f"hazard strip: {name} has no housing")
        x0, y0, x1, y1 = part["housing"]
        w, inset = HAZARD_STRIP["w"], HAZARD_STRIP["inset"]
        if side == "left":
            box = (x0 - w, y0 + inset, x0, y1 - inset)
        elif side == "right":
            box = (x1, y0 + inset, x1 + w, y1 - inset)
        else:
            self.fail(f"strip side {side!r} is not left or right")
        border = HAZARD_PAD["border"]
        art = {"shape": "hazard", "at": xywh(grow(box, -border / 2)), "border": border, "period": HAZARD_PAD["period"]}
        self.decor.append({"name": f"strip {side} of {name}", "box": box, "art": art})

    def label(self, text: str, style: str, part: str, side: str, rotate: int = 0, along: int = 0):
        """Label attached to a part, GAP du outside the part (and outside the labels already on that side). A label
        with 'along' is shifted that many du along the side, sits on the part's own edge and pushes no other label out."""
        p = self.parts[part]
        if rotate and "\n" in text:
            self.fail(f"label {text!r}: only a single line can be rotated")
        w, h = text_size(text, style, rotate)
        x0, y0, x1, y1 = p["outer"]
        edge = None if along else p["edges"].get(side)
        odd_w, odd_h = w % 2 / 2, h % 2 / 2
        if side == "above":
            bottom = (y0 if edge is None else edge) - GAP - odd_h
            box = (p["cx"] + along - w / 2, bottom - h, p["cx"] + along + w / 2, bottom)
            edge = box[1]
        elif side == "below":
            top = (y1 if edge is None else edge) + GAP + odd_h
            box = (p["cx"] + along - w / 2, top, p["cx"] + along + w / 2, top + h)
            edge = box[3]
        elif side == "left":
            right = (x0 if edge is None else edge) - GAP - odd_w
            box = (right - w, p["cy"] + along - h / 2, right, p["cy"] + along + h / 2)
            edge = box[0]
        elif side == "right":
            left = (x1 if edge is None else edge) + GAP + odd_w
            box = (left, p["cy"] + along - h / 2, left + w, p["cy"] + along + h / 2)
            edge = box[2]
        else:
            self.fail(f"label side {side!r} is not above, below, left or right")
        if not along:
            p["edges"][side] = edge
        self._add_label(text, style, box, rotate)

    def mark(self, text: str, style: str, x, y, reason: str, rotate: int = 0):
        """Free label (title, bracket text, mark) centred on the grid or on a named line; needs a reason."""
        if not reason:
            self.fail(f"the free label {text!r} needs a reason")
        try:
            cx = self.xs[x] if isinstance(x, str) else x
            cy = self.ys[y] if isinstance(y, str) else y
        except KeyError as e:
            self.fail(f"free label {text!r}: no line {e.args[0]!r}")
        if not (isinstance(cx, int) and isinstance(cy, int)):
            self.fail(f"free label {text!r} must sit on the 1 du grid, got ({cx}, {cy})")
        self._add_label(text, style, centred(cx, cy, *text_size(text, style, rotate)), rotate)

    def rule(self, name: str, x: int, y0: int, y1: int):
        """Printed vertical dividing line on the grid."""
        if not all(isinstance(v, int) for v in (x, y0, y1)):
            self.fail(f"rule {name} must sit on the 1 du grid, got x {x}, y {y0} to {y1}")
        box = (x - RULE_STROKE / 2, y0, x + RULE_STROKE / 2, y1)
        self.decor.append({"name": name, "box": box, "art": {"shape": "line", "at": [x, y0, 0, y1 - y0]}})

    def _add_label(self, text: str, style: str, box: tuple, rotate: int, inside: str | None = None):
        self.labels.append({"text": text, "style": style, "box": box, "rotate": rotate, "inside": inside})

    def screw(self, size: str, x: str, y: str):
        """Edge (M) or inner (S) screw on an x line and a y line of the line table."""
        if size not in ("M", "S"):
            self.fail("the page places edge (M) and inner (S) screws, the corner screws (L) come with the ears")
        self._screw(size, x, y)

    def edge_screws(self, sides: bool = False):
        self.screw("M", "CX", "ST")
        self.screw("M", "CX", "SB")
        if sides:
            self.screw("M", "SL", "CY")
            self.screw("M", "SR", "CY")

    def _screw(self, size: str, x: str, y: str):
        for value, table, axis in ((x, self.xs, "x"), (y, self.ys, "y")):
            if not isinstance(value, str) or value not in table:
                self.fail(f"a screw is placed by naming an {axis} line ({', '.join(table)}), not by {value!r}")
        cx, cy, d = self.xs[x], self.ys[y], SCREWS[size]
        rot = SLOT_ANGLES[len(self.screws) % len(SLOT_ANGLES)]
        self.screws.append({"size": size, "cx": cx, "cy": cy, "box": centred(cx, cy, d, d), "rot": rot})

    def check(self):
        problems = []
        plate = (0, 0, self.w, self.h)
        content = grow(plate, -MARGIN)
        near_ears = [grow(e, EAR_CLEAR) for e in self.ears]
        parts = list(self.parts.values())
        for i, p in enumerate(parts):
            if not within(p["outer"], content):
                problems.append(f"part {p['name']} in the {MARGIN} du plate margin")
            if any(overlaps(p["outer"], e) for e in near_ears):
                problems.append(f"part {p['name']} closer than {EAR_CLEAR} du to an ear")
            if not within(p["touch"], plate):
                problems.append(f"touch area of {p['name']} outside the plate")
            for q in parts[i + 1:]:
                if overlaps(p["outer"], q["outer"]):
                    problems.append(f"parts {p['name']} and {q['name']} overlap")
                if overlaps(p["touch"], q["touch"]):
                    problems.append(f"touch areas of {p['name']} and {q['name']} overlap")
        for i, lab in enumerate(self.labels):
            box, what = lab["box"], f"label {lab['text']!r}"
            if not within(box, content):
                problems.append(f"{what} in the {MARGIN} du plate margin")
            if any(overlaps(box, e) for e in near_ears):
                problems.append(f"{what} closer than {EAR_CLEAR} du to an ear")
            for p in parts:
                if lab["inside"] == p["name"]:
                    if overlaps(box, p["inner"]) or not within(box, p["pad"]):
                        problems.append(f"{what} not inside the pad of {p['name']}")
                elif overlaps(box, p["outer"]):
                    problems.append(f"{what} overlaps part {p['name']}")
            for other in self.labels[i + 1:]:
                if overlaps(box, other["box"]):
                    problems.append(f"{what} overlaps label {other['text']!r}")
            if any(overlaps(box, s["box"]) for s in self.screws):
                problems.append(f"{what} overlaps a screw")
            problems += [f"{what} overlaps {d['name']}" for d in self.decor if overlaps(box, d["box"])]
        for i, d in enumerate(self.decor):
            if not within(d["box"], content):
                problems.append(f"{d['name']} in the {MARGIN} du plate margin")
            if any(overlaps(d["box"], e) for e in near_ears):
                problems.append(f"{d['name']} closer than {EAR_CLEAR} du to an ear")
            problems += [f"{d['name']} overlaps part {p['name']}" for p in parts if overlaps(d["box"], p["outer"])]
            problems += [f"{d['name']} overlaps {o['name']}" for o in self.decor[i + 1:] if overlaps(d["box"], o["box"])]
        for s in self.screws[4:]:
            what = f"screw {s['size']} at ({s['cx']}, {s['cy']})"
            if not within(s["box"], plate):
                problems.append(f"{what} outside the plate")
            if any(overlaps(s["box"], e) for e in self.ears):
                problems.append(f"{what} on an ear")
            problems += [f"{what} overlaps part {p['name']}" for p in parts if overlaps(s["box"], p["outer"])]
            problems += [f"{what} overlaps another screw" for t in self.screws if t is not s and overlaps(s["box"], t["box"])]
        if problems:
            self.fail("; ".join(problems))

    def build(self) -> dict:
        self.check()
        art = [{"shape": "plate", "at": xywh(grow((0, 0, self.w, self.h), -PLATE["border"] / 2)), "r": PLATE["radius"], "border": PLATE["border"]}]
        art += [{"shape": "ear", "at": xywh(grow(e, -EAR["border"] / 2)), "r": PLATE["radius"], "border": EAR["border"]} for e in self.ears]
        art += [{"shape": "screw", "at": [num(s["cx"]), num(s["cy"]), num(SCREWS[s["size"]] / 2)], "size": s["size"], "rot": s["rot"]} for s in self.screws]
        controls = []
        for p in self.parts.values():
            art += p["art"]
            for i, member in enumerate(p["members"] if p["control"] else []):
                control = {**member, "at": xywh(p["touch"]), "kit": p["kit"]}
                if p["cover"]:
                    control["cover_at"] = xywh(p["cover"])
                if p["knob"]:
                    control["knob"] = p["knob"]
                if p["marks"]:
                    mark = p["marks"][i]
                    control["mark"], control["dot"] = xywh(mark["touch"]), [num(mark["cx"]), num(mark["cy"]), PARTS["MARK"]["w"]]
                controls.append(control)
            controls += [{**extra, "at": xywh(box), "kit": {"part": "FLAP"}} for extra, box in p["extras"]]
        art += [d["art"] for d in self.decor]
        printed = []
        for lab in self.labels:
            size, glyph = STYLES[lab["style"]]
            x0, y0, x1, y1 = lab["box"]
            cx = num((x0 + x1) / 2)
            if lab["rotate"]:
                printed.append([lab["text"], cx, num((y0 + y1) / 2), size, len(lab["text"]) * glyph, lab["rotate"]])
                continue
            for i, line in enumerate(lab["text"].split("\n")):
                printed.append([line, cx, num(y0 + size * i + size / 2), size] + ([len(line) * glyph] if len(line) > 1 else []))
        return {"box": [self.w, self.h], "controls": controls, "indicators": self.indicators, "print": printed, "art": art}


def shifted(item, dx: int, dy: int, keys: tuple) -> dict:
    out = dict(item)
    for key in keys:
        if key in out:
            out[key] = [num(out[key][0] + dx), num(out[key][1] + dy), *out[key][2:]]
    return out


class PanelGroup:
    """A page of several physical panels: one Panel (plate with its own ears and screws) per panel at a page offset.
    Plates next to each other are exactly GROUP_GAP du apart and share an edge line; the page is at most REF."""

    def __init__(self, name: str):
        self.name = name
        self.plates = []

    def panel(self, name: str, w: int, h: int, x: int, y: int) -> Panel:
        if not (isinstance(x, int) and isinstance(y, int)):
            raise LayoutError(f"{self.name}: plate {name} must sit on the 1 du grid, got ({x}, {y})")
        panel = Panel(f"{self.name} / {name}", w, h)
        self.plates.append((panel, x, y))
        return panel

    def check(self):
        problems = []
        boxes = [(p.name, (x, y, x + p.w, y + p.h)) for p, x, y in self.plates]
        for i, (name, a) in enumerate(boxes):
            for other, b in boxes[i + 1:]:
                dx, dy = max(b[0] - a[2], a[0] - b[2]), max(b[1] - a[3], a[1] - b[3])
                if dx < 0 and dy < 0:
                    problems.append(f"plates {name} and {other} overlap")
                elif dx < 0 and (dy != GROUP_GAP or not (a[0] == b[0] or a[2] == b[2])):
                    problems.append(f"plates {name} and {other} must be {GROUP_GAP} du apart and share a left or right edge line (gap {dy})")
                elif dy < 0 and (dx != GROUP_GAP or not (a[1] == b[1] or a[3] == b[3])):
                    problems.append(f"plates {name} and {other} must be {GROUP_GAP} du apart and share a top or bottom edge line (gap {dx})")
        width, height = max(b[2] for _, b in boxes), max(b[3] for _, b in boxes)
        if min(b[0] for _, b in boxes) or min(b[1] for _, b in boxes):
            problems.append("the plates must start at 0, 0")
        if width > REF[0] or height > REF[1]:
            problems.append(f"page {width} x {height} du is bigger than {REF[0]} x {REF[1]}")
        if problems:
            raise LayoutError(f"{self.name}: " + "; ".join(problems))
        return width, height

    def build(self) -> dict:
        width, height = self.check()
        page = {"box": [width, height], "controls": [], "indicators": [], "print": [], "art": []}
        for panel, x, y in self.plates:
            built = panel.build()
            page["controls"] += [shifted(c, x, y, ("at", "cover_at", "mark", "dot", "knob")) for c in built["controls"]]
            page["indicators"] += [shifted(i, x, y, ("at",)) for i in built["indicators"]]
            page["print"] += [[t, num(px + x), num(py + y), *rest] for t, px, py, *rest in built["print"]]
            page["art"] += [shifted(a, x, y, ("at", "hole")) for a in built["art"]]
        return page
