#!/usr/bin/env python3
"""Coverage of the A-10C panel pages against docs/A10C (SPEC.md section 2 and 11, BIOS.md).

  python3 coverage.py [PAGE ...]               per page: expected / used / missing / extra DCS-BIOS ids
  python3 coverage.py --expected [PAGE ...]    print the expected ids of the pages instead

No page name = all 23 pages. Exit code is always 0. A-10C.json comes from the DCS-BIOS JSON folder of the dashboard config.
"""
import fnmatch
import importlib
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BIOS_MD = REPO / "docs" / "A10C" / "BIOS.md"
SPEC_MD = REPO / "docs" / "A10C" / "SPEC.md"

# page name (SPEC.md "#### NAME") -> exact BIOS.md "### " headings of its panels.
# A (heading, [ids]) entry takes only those ids of that section.
# The "Plus" ids come from the Controls line of the page in SPEC.md.
PAGE_SECTIONS = {
    "BRAKE / AUX LT / SAS": [
        "Emergency Brake System (p. 174)",
        "Auxiliary Lighting Control Panel (p. 175)",
        "Stability Augmentation System (SAS) Panel (p. 176)",
    ],
    "IFF": ["Identify Friend or Foe (IFF) Panel (p. 178)"],
    "EMER FLT CTRL": ["Emergency Flight Control Panel (p. 180)"],
    "INTERCOM / STALL": [
        "Intercom Control Panel (p. 182)",
        "Stall Warning Control Panel (p. 183)",
    ],
    "FUEL SYSTEM": [
        "Fuel System Control Panel (p. 158)",
        "Air Refuel Status Lights (p. 153)",
    ],
    "THROTTLE": [
        "Throttles Panel (p. 160)",
        "Flap lever, left of the throttles (p. 156)",
    ],
    "LASTE": ["LASTE Control Panel (p. 163)"],
    "RADIO 1": ["AN/ARC-186(V) Radio Control Panel (p. 167)"],
    "UHF": ["AN/ARC-164 UHF Radio Control Panel (p. 168)"],
    "VHF FM": ["AN/ARC-186(V) VHF FM Radio 2 Control Panel (p. 171)"],
    "FIRE / JETT": [
        'Left Engine "T-Handle" Fire Extinguisher Discharge Select (p. 114)',
        'APU "T Handle" Fire Extinguisher Discharge Select (p. 136)',
        'RIGHT Engine "T Handle" Fire Extinguisher Discharge Select (p. 147)',
        "Fire Extinguisher Discharge (p. 144)",
        "Emergency Jettison Button (p. 120)",
    ],
    "LANDING GEAR": ["Landing Gear and Flap Control Panel (p. 125)"],
    "AHCP": [
        "Armament HUD Control Panel (AHCP) (p. 129)",
        "Heading Attitude Reference (HARS) Fast Erect Button (p. 133)",
    ],
    "CMSC": ["Countermeasures Set Control (CMSC) (p. 136)"],
    "NMSP": ["Navigation Mode Select Panel (NMSP) (p. 140)"],
    "CMSP": ["Countermeasure Signal Processor (CMSP) Panel (p. 491)"],
    "CAUTION": ["Caution Light Panel (p. 195)"],
    "AAP / ILS": [
        "Auxiliary Avionics Panel (AAP) (p. 203)",
        "ILS Control Panel and ILS Operation (p. 199)",
    ],
    "TACAN": ["TACAN Operation and Control Panel (p. 198)"],
    "HARS / HMCS": [
        "Heading and Attitude Reference Systems (HARS) Control Panel (p. 200)",
        "Helmet Mounted Cueing System (HMCS) Control Panel (p. 201)",
    ],
    "CANOPY / ELEC": [
        "Cockpit Canopy Switch and Canopy Ejection Handle (p. 186)",
        "Electrical Power Panel (p. 187)",
        ("Marker and Canopy Lights (p. 148)", ["CANOPY_UNLOCKED"]),
    ],
    "ENVIRONMENT": ["Environment System Panel (p. 189)"],
    "LIGHTING": ["Lighting Control Panel (p. 191)"],
}

# ids (or patterns) a page section says are not shown, besides SPEC.md section 11
NOT_SHOWN = {
    "LIGHTING": ["INT_*_L_BRIGHT"],
}

ID_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def load_json_ids() -> set:
    sys.path.insert(0, str(REPO / "core"))
    import config
    json_dir = Path(config.load()["dcs"]["saved_games"]) / "Scripts" / "DCS-BIOS" / "doc" / "json"
    with open(json_dir / "A-10C.json", encoding="utf-8") as f:
        data = json.load(f)
    return {c["identifier"] for category in data.values() for c in category.values()}


def split_sections(path: Path, level: str) -> dict:
    sections, name = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            name = line[len(level) + 1:].strip() if line.startswith(level + " ") else None
            if name is not None:
                sections.setdefault(name, [])
            continue
        if name is not None:
            sections[name].append(line)
    return sections


def expand_range(first: str, last: str, json_ids: set) -> list:
    prefix = ""
    for a, b in zip(first, last):
        if a != b:
            break
        prefix += a
    found = sorted(i for i in json_ids if i.startswith(prefix) and len(i) == len(first) and first <= i <= last)
    return found or [first, last]


def cell_ids(cell: str, json_ids: set) -> list:
    ids = []
    for token in re.split(r",| / ", cell):
        token = token.strip().strip("`").strip()
        if not token or token == "—":
            continue
        if "…" in token:
            first, _, last = token.partition("…")
            ids += expand_range(first.strip(), last.strip(), json_ids)
        else:
            ids.append(token)
    return ids


def section_ids(lines: list, json_ids: set) -> list:
    ids = []
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] == "Control" or set(cells[0]) <= set("- "):
            continue
        ids += cell_ids(cells[1], json_ids)
    return ids


def section11_ids() -> list:
    lines, inside = [], False
    for line in SPEC_MD.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.startswith("## 11.")
            continue
        if inside:
            lines.append(line)
    return [t for t in re.findall(r"`([^`]+)`", "\n".join(lines)) if re.match(r"^[A-Z][A-Z0-9_*]*$", t)]


def plus_ids(page: str, spec_pages: dict) -> list:
    for line in spec_pages.get(page, []):
        if line.startswith("- **Controls:**") and "Plus:" in line:
            tail = line.split("Plus:", 1)[1]
            return [t for t in re.findall(r"`([^`]+)`", tail) if ID_RE.match(t)]
    return []


def matches(id_: str, patterns: list) -> bool:
    return any(fnmatch.fnmatchcase(id_, p) for p in patterns)


def expected(page: str, json_ids: set, bios: dict, spec_pages: dict, excluded: list, warnings: list) -> list:
    candidates = []
    for entry in PAGE_SECTIONS[page]:
        heading, only = entry if isinstance(entry, tuple) else (entry, None)
        if heading not in bios:
            warnings.append(f"WARNING {page}: BIOS.md has no section '{heading}'")
            continue
        found = section_ids(bios[heading], json_ids)
        candidates += [i for i in found if only is None or i in only]
    candidates += plus_ids(page, spec_pages)
    result = []
    for id_ in candidates:
        if id_ in result:
            continue
        if id_ not in json_ids:
            warnings.append(f"WARNING {page}: expected id is not in A-10C.json: {id_}")
            continue
        if matches(id_, excluded) or matches(id_, NOT_SHOWN.get(page, [])):
            continue
        result.append(id_)
    return result


def walk(node, out: set) -> None:
    if isinstance(node, str):
        out.add(node)
    elif isinstance(node, dict):
        for k, v in node.items():
            out.add(k)
            walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def load_views():
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(REPO / "core"))
    sys.path.insert(0, str(REPO / "aircraft"))
    return importlib.import_module("a10c").VIEWS


def main(argv: list) -> int:
    args = argv[1:]
    show_expected = "--expected" in args
    pages = [a for a in args if a != "--expected"] or list(PAGE_SECTIONS)
    json_ids = load_json_ids()
    bios = split_sections(BIOS_MD, "###")
    spec_pages = split_sections(SPEC_MD, "####")
    excluded = section11_ids()
    warnings = []
    for page in PAGE_SECTIONS:
        if page not in spec_pages:
            warnings.append(f"WARNING SPEC.md has no page section '#### {page}'")
    for page in spec_pages:
        if page not in PAGE_SECTIONS:
            warnings.append(f"WARNING SPEC.md page section '#### {page}' is not in PAGE_SECTIONS")
    views = []
    if not show_expected:
        try:
            views = load_views()
        except Exception as e:
            print(f"WARNING cannot import aircraft/a10c.py: {e!r}")
    total = 0
    for page in pages:
        if page not in PAGE_SECTIONS:
            print(f"{page}: unknown page")
            continue
        exp = expected(page, json_ids, bios, spec_pages, excluded, warnings)
        if show_expected:
            print(f"{page}: expected {len(exp)}")
            print("  " + ", ".join(exp))
            continue
        built = [v for v in views if v.get("name") == page]
        if not built:
            print(f"{page}: not built")
            continue
        strings = set()
        for v in built:
            walk(v, strings)
        used = {s for s in strings if s in json_ids}
        missing = [i for i in exp if i not in used]
        extra = sorted(used - set(exp))
        total += len(missing)
        print(f"{page}: expected {len(exp)}, used {len(used)}, missing [{', '.join(missing)}], extra [{', '.join(extra)}]")
    for w in dict.fromkeys(warnings):
        print(w)
    if not show_expected:
        print(f"TOTAL missing {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
