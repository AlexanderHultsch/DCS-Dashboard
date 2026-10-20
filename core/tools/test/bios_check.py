#!/usr/bin/env python3
"""List every control of a DCS-BIOS module with the dashboard control it should become.

  python3 bios_check.py MODULE [--json DIR] [--lua FILE] [--summary]     e.g. python3 bios_check.py F-16C_50 --lua .../aircraft_modules/F-16C_50.lua

Reads MODULE.json from the DCS-BIOS JSON folder (<saved_games>/Scripts/DCS-BIOS/doc/json from the dashboard config, or DIR when --json
is given). With --lua the DCS-BIOS module file is read too, to get the define function of every id (defineToggleSwitch, definePushButton,
defineSpringloaded_3PosTumb, ...). Prints a tab-separated table, one row per control:
  id, category, description, control_type, inputs, outputs, readback, define, position order, build
  inputs    set_state max / fixed_step / variable_step suggested_step / action argument
  outputs   name+suffix: type and max_value (integer) or max_length (string)
  readback  "yes" if an output has exactly the id as its name (the bridge reads a control by its own id), else the suffixed names
  position order  from the JSON positions list, else from the description ("OFF - ON"); empty if neither lists them
  build     the dashboard control: button, selector (N) [spring], knob, step rocker (fixed), step rocker (N), lamp, display,
            bar or gauge, none; "NO READBACK" is appended to a button, selector or knob without an output named like its id
--summary prints the counts per build type, the NO READBACK ids and the 3+ position selectors without a position order instead of the table.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "core"))
import config

SPRING_DEFINES = ("defineSpringloaded", "defineRockerSwitch")
DEFINE_RE = re.compile(r':(define\w+)\(\s*"([^"]+)"')


def json_dir(args: list[str]) -> Path:
    if "--json" in args:
        i = args.index("--json")
        path = Path(args[i + 1])
        del args[i:i + 2]
        return path
    return Path(config.load()["dcs"]["saved_games"]) / "Scripts" / "DCS-BIOS" / "doc" / "json"


def lua_option(args: list[str]) -> Path | None:
    if "--lua" not in args:
        return None
    i = args.index("--lua")
    path = Path(args[i + 1])
    del args[i:i + 2]
    return path


def load_defines(path: Path | None) -> dict:
    if path is None:
        return {}
    defines = {}
    for name, identifier in DEFINE_RE.findall(path.read_text(encoding="utf-8")):
        defines.setdefault(identifier, name)
    return defines


def load_controls(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [control for category in data.values() for control in category.values()]


def input_of(control: dict, interface: str) -> dict | None:
    return next((i for i in control["inputs"] if i["interface"] == interface), None)


def inputs_text(control: dict) -> str:
    parts = []
    for i in control["inputs"]:
        if i["interface"] == "set_state":
            parts.append(f"set_state {i['max_value']}")
        elif i["interface"] == "variable_step":
            parts.append(f"variable_step {i.get('suggested_step', '')}".strip())
        elif i["interface"] == "action":
            parts.append(f"action {i.get('argument', '')}".strip())
        else:
            parts.append(i["interface"])
    return "; ".join(parts)


def outputs_text(control: dict) -> str:
    parts = []
    for o in control["outputs"]:
        size = o["max_value"] if o["type"] == "integer" else o["max_length"]
        parts.append(f"{control['identifier']}{o['suffix']}: {o['type']} {size}")
    return "; ".join(parts)


def readback_text(control: dict) -> str:
    names = [control["identifier"] + o["suffix"] for o in control["outputs"]]
    if control["identifier"] in names:
        return "yes"
    return " ".join(names)


def has_readback(control: dict) -> bool:
    return any(o["suffix"] == "" for o in control["outputs"])


def positions_text(control: dict) -> str:
    if control.get("positions"):
        return " - ".join(control["positions"])
    set_state = input_of(control, "set_state")
    parts = control["description"].split(" - ")
    if not set_state or len(parts) != set_state["max_value"] + 1:
        return ""
    words = parts[0].split(":")[-1].split()
    keep = []
    for word in reversed(words):
        if not (word.isupper() or word.isdigit()):
            break
        keep.insert(0, word)
    parts[0] = " ".join(keep or words[-1:])
    parts[-1] = re.sub(r"\s*\(A-10C( II)?\)$", "", parts[-1])
    return " - ".join(parts)


def is_button(control: dict, define: str) -> bool:
    return define == "definePushButton" or "button" in control["description"].lower() or "button" in define.lower()


def build_of(control: dict, define: str) -> str:
    set_state = input_of(control, "set_state")
    fixed = input_of(control, "fixed_step")
    variable = input_of(control, "variable_step")
    if set_state:
        top = set_state["max_value"]
        if top == 65535 or variable:
            build = "knob"
        elif top == 1:
            build = "button" if is_button(control, define) else "selector (2)"
        else:
            build = f"selector ({top + 1})"
            if define.startswith(SPRING_DEFINES):
                build += " spring"
    elif variable:
        build = f"step rocker ({variable.get('suggested_step', '')})"
    elif fixed:
        build = "step rocker (fixed)"
    elif control["control_type"] == "led" or define == "defineIndicatorLight":
        build = "lamp"
    elif any(o["type"] == "string" for o in control["outputs"]):
        build = "display"
    elif control["control_type"] == "analog_gauge" or define in ("defineFloat", "define8BitFloat"):
        build = "bar or gauge"
    else:
        build = "none"
    if build.split()[0] in ("button", "selector", "knob") and not has_readback(control):
        build += " NO READBACK"
    return build


def row_of(control: dict, defines: dict) -> list[str]:
    define = defines.get(control["identifier"], "")
    build = build_of(control, define)
    positions = "" if build.startswith("button") else positions_text(control)
    fields = [control["identifier"], control["category"], control["description"], control["control_type"],
              inputs_text(control), outputs_text(control), readback_text(control), define, positions, build]
    return [field.replace("\t", " ").replace("\n", " ") for field in fields]


def print_summary(rows: list[list[str]]) -> None:
    builds = Counter(row[9].replace(" NO READBACK", "") for row in rows)
    print(f"{len(rows)} controls")
    for build, count in builds.most_common():
        print(f"{count:5d}  {build}")
    no_readback = [row[0] for row in rows if row[9].endswith("NO READBACK")]
    print(f"NO READBACK ({len(no_readback)}): {' '.join(no_readback)}")
    guesses = [row[0] for row in rows if not row[8] and (m := re.match(r"selector \((\d+)\)", row[9])) and int(m[1]) >= 3]
    print(f"3+ position selectors without position order ({len(guesses)}): {' '.join(guesses)}")


def main(argv: list[str]) -> int:
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2
    summary = "--summary" in args
    if summary:
        args.remove("--summary")
    lua = lua_option(args)
    directory = json_dir(args)
    if len(args) != 1:
        print(__doc__)
        return 2
    path = directory / f"{args[0]}.json"
    if not path.exists():
        print(f"not found: {path}", file=sys.stderr)
        return 2
    defines = load_defines(lua)
    rows = [row_of(control, defines) for control in load_controls(path)]
    if summary:
        print_summary(rows)
        return 0
    print("\t".join(["id", "category", "description", "control_type", "inputs", "outputs", "readback", "define", "position order", "build"]))
    for row in rows:
        print("\t".join(row))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
