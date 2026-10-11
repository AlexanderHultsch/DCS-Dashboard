"""Panel kit: the layout compiler of the cockpit panel pages (docs/COCKPIT_FIXES.md, sections 2 to 4 and 8).

Every size is in design units (du) and defined once, below. A page makes one Panel (plate width and height in
du, even numbers), places parts by their centre on the 1 du grid and attaches labels to them; it never gives a
size. The plate brings four identical corner ears with a SCREW_L in the centre of each. Further screws are
placed only by naming an x line and a y line from the line table:

    x lines: L R (plate edges), CX (middle), SL SR (corner screws), NAME.cx (every placed part)
    y lines: T B (plate edges), CY (middle), ST SB (corner screws), NAME.cy (every placed part)

Panel.build() checks the layout (LayoutError on a collision) and returns the page data in the format
web/index.html draws: box [w, h], controls (the given control data plus "at", "kit" and, for a guarded part,
"cover_at"), print ([text, x, y, size, width] or with a rotation) and art.

    p = Panel("EMERGENCY", 580, 276)
    p.mark("EMERGENCY", "TITLE", "CX", 52, "panel title")
    p.push("GUARD", 114, 166, guard_button, frame=True)
    p.label("GUARD", "NAME", "GUARD", "above")
    p.screw("S", "GUARD.cx", "SB")
    page = p.build()
"""

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
    # w / h: the ring; band: touch height per position until the switch chooser replaces the bands
    "TOGGLE": {"w": 56, "h": 56, "lever": 40, "band": 60},
    "ROTARY": {"w": 100, "h": 100},
    "KNOB_L": {"w": 96, "h": 96},
    "KNOB_M": {"w": 72, "h": 72},
    "KNOB_S": {"w": 56, "h": 56},
    "ROCKER": {"w": 52, "h": 100},
    "CHIP": {"w": 64, "h": 22},
    "SLIDER": {"w": 40, "h": 200},
    "LEVER": {"w": 40, "h": 200},
}
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
# position labels of a toggle, one (side, rotation) per position in the order of the positions (None: not printed)
TOGGLE_LABELS = {
    "above_side_below": (("above", 0), ("right", 90), ("below", 0)),
    "above_below": (("above", 0), ("below", 0)),
    "left_right": (("left", 0), None, ("right", 0)),
}


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
        self.screws = []
        for y in ("ST", "SB"):
            for x in ("SL", "SR"):
                self._screw("L", x, y)

    def fail(self, message: str):
        raise LayoutError(f"{self.name}: {message}")

    def _part(self, name: str, kind: str, cx: int, cy: int, control: dict) -> dict:
        if name in self.parts or "." in name:
            self.fail(f"part name {name!r} is taken or has a dot")
        if not (isinstance(cx, int) and isinstance(cy, int)):
            self.fail(f"part {name} must sit on the 1 du grid, got ({cx}, {cy})")
        if "at" in control:
            self.fail(f"part {name}: the kit sizes and places the control, remove its 'at'")
        body = centred(cx, cy, PARTS[kind]["w"], PARTS[kind]["h"])
        part = {
            "name": name, "kind": kind, "cx": cx, "cy": cy, "control": control, "kit": {"part": kind},
            "body": body, "outer": body, "inner": body, "touch": body, "cover": None, "pad": None, "housing": None, "round": False,
            "art": [], "edges": {},
        }
        if control.get("guard"):
            part["cover"] = part["outer"] = part["inner"] = grow(body, GUARD_COVER["margin"])
            part["kit"].update(cover_frame=GUARD_COVER["frame"], cover_lock=GUARD_COVER["lock"])
        self.parts[name] = part
        self.xs[name + ".cx"] = cx
        self.ys[name + ".cy"] = cy
        return part

    def push(self, name: str, cx: int, cy: int, control: dict, frame: bool = False) -> dict:
        """Square pushbutton (bezel and face, optional lamp legend), with the white frame centred on it."""
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
        return part

    def plunger(self, name: str, cx: int, cy: int, control: dict) -> dict:
        """Round plunger pushbutton; a guarded one gets a round cover."""
        part = self._part(name, "PLUNGER", cx, cy, control)
        part["round"] = True
        return part

    def toggle(self, name: str, cx: int, cy: int, control: dict, labels: str | None = None) -> dict:
        """Toggle switch (ring and lever) with one touch band per position and optional position label preset."""
        spec = PARTS["TOGGLE"]
        part = self._part(name, "TOGGLE", cx, cy, control)
        part["kit"].update(ring=spec["w"], lever=spec["lever"])
        n = len(control["positions"])
        band = spec["band"]
        part["touch"] = centred(cx, cy, *((band * n, band) if control.get("orient") == "h" else (band, band * n)))
        if labels:
            preset = TOGGLE_LABELS[labels]
            if len(preset) != n:
                self.fail(f"label preset {labels} is for {len(preset)} positions, {name} has {n}")
            for position, spot in zip(control["positions"], preset):
                if spot:
                    self.label(position["label"], "POS", name, *spot)
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

    def label(self, text: str, style: str, part: str, side: str, rotate: int = 0):
        """Label attached to a part, GAP du outside the part (and outside the labels already on that side)."""
        p = self.parts[part]
        if rotate and "\n" in text:
            self.fail(f"label {text!r}: only a single line can be rotated")
        w, h = text_size(text, style, rotate)
        x0, y0, x1, y1 = p["outer"]
        edge = p["edges"].get(side)
        odd_w, odd_h = w % 2 / 2, h % 2 / 2
        if side == "above":
            bottom = (y0 if edge is None else edge) - GAP - odd_h
            box = (p["cx"] - w / 2, bottom - h, p["cx"] + w / 2, bottom)
            p["edges"][side] = box[1]
        elif side == "below":
            top = (y1 if edge is None else edge) + GAP + odd_h
            box = (p["cx"] - w / 2, top, p["cx"] + w / 2, top + h)
            p["edges"][side] = box[3]
        elif side == "left":
            right = (x0 if edge is None else edge) - GAP - odd_w
            box = (right - w, p["cy"] - h / 2, right, p["cy"] + h / 2)
            p["edges"][side] = box[0]
        elif side == "right":
            left = (x1 if edge is None else edge) + GAP + odd_w
            box = (left, p["cy"] - h / 2, left + w, p["cy"] + h / 2)
            p["edges"][side] = box[2]
        else:
            self.fail(f"label side {side!r} is not above, below, left or right")
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
            control = {**p["control"], "at": xywh(p["touch"]), "kit": p["kit"]}
            if p["cover"]:
                control["cover_at"] = xywh(p["cover"])
            controls.append(control)
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
                printed.append([line, cx, num(y0 + size * i + size / 2), size, len(line) * glyph])
        return {"box": [self.w, self.h], "controls": controls, "print": printed, "art": art}
