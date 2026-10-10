import select

from bridge import config, dcsbios, export, log

DCSBIOS_NAMES = [
    # Seat
    "SEAT_POSITION",
    # Master caution and warning
    "PLT_MASTER_CAUTION_L", "CPG_MASTER_CAUTION_L", "PLT_MASTER_WARNING_L", "CPG_MASTER_WARNING_L",
    # Engine and APU lamps
    "PLT_ENG_1_READY_L", "CPG_ENG_1_READY_L", "PLT_ENG_2_READY_L", "CPG_ENG_2_READY_L",
    "PLT_APU_READY_L", "CPG_APU_READY_L", "PLT_ENG_1_FIRE_L", "CPG_ENG_1_FIRE_L",
    "PLT_ENG_2_FIRE_L", "CPG_ENG_2_FIRE_L", "PLT_APU_FIRE_L", "CPG_APU_FIRE_L", "PLT_APU_L",
    # Startup switches
    "PLT_MASTER_IGN_SW", "PLT_APU_BTN_CVR", "PLT_APU_BTN", "PLT_ENG1_START", "PLT_ENG2_START",
    "PLT_ROTOR_BRK", "PLT_PARK_BRAKE",
    # Power levers
    "PLT_ENG_L_PW_LVR", "PLT_ENG_R_PW_LVR", "CPG_ENG_L_PW_LVR", "CPG_ENG_R_PW_LVR",
    # Armament
    "PLT_MASTER_ARM_BTN", "CPG_MASTER_ARM_BTN", "PLT_GROUND_OVERRIDE_BTN", "CPG_GROUND_OVERRIDE_BTN",
    "PLT_MASTER_ARM_ARM_L", "CPG_MASTER_ARM_ARM_L", "PLT_MASTER_ARM_SAFE_L", "CPG_MASTER_ARM_SAFE_L",
    "PLT_GROUND_OVERRIDE_L", "CPG_GROUND_OVERRIDE_L",
    # Weapons action switch
    "PLT_CYCLIC_WEAPON_UD", "CPG_CYCLIC_WEAPON_UD", "PLT_CYCLIC_WEAPON_LR", "CPG_CYCLIC_WEAPON_LR",
    "CPG_LHG_WPN_UP_DN", "CPG_LHG_WPN_L_R",
    # Sight select
    "PLT_COLLECTIVE_SIGHT_SELECT_UD", "CPG_COLLECTIVE_SIGHT_SELECT_UD",
    "PLT_COLLECTIVE_SIGHT_SELECT_LR", "CPG_COLLECTIVE_SIGHT_SELECT_LR",
    # Flare and chaff
    "PLT_CYCLIC_FLARE", "CPG_CYCLIC_FLARE", "PLT_CYCLIC_CHAFF", "CPG_CYCLIC_CHAFF",
    "PLT_CMWS_FLARE_COUNT", "PLT_CMWS_CHAFF_COUNT",
    # Force trim / hold
    "PLT_CYCLIC_TRIM_UD", "CPG_CYCLIC_TRIM_UD", "PLT_CYCLIC_TRIM_LR", "CPG_CYCLIC_TRIM_LR",
    # KU scratchpad
    "PLT_KU_DISPLAY", "CPG_KU_DISPLAY",
    # Radios
    "UHF_RADIO", "VHF_AM_RADIO", "FM1_RADIO", "FM2_RADIO", "HF_RADIO",
    # Standby instruments
    "PLT_IAS_NEEDLE", "PLT_ALT_NEEDLE",
]
# EUFD
DCSBIOS_NAMES += [f"PLT_EUFD_LINE{i}" for i in range(1, 15)] + [f"CPG_EUFD_LINE{i}" for i in range(1, 15)]


def main() -> None:
    cfg = config.load()
    log.setup(cfg["log"])
    outputs, missing = dcsbios.load_outputs(dcsbios.json_path(cfg["dcs"]["saved_games"]), DCSBIOS_NAMES)
    for name in missing:
        log.line("bridge", "not in DCS-BIOS", name)
    group, port = cfg["dcs_bios"]["export_multicast"], cfg["dcs_bios"]["export_port"]
    bios_sock = dcsbios.open_socket(group, port)
    export_sock = export.open_socket(cfg["export"]["port"])
    log.line("bridge", "start", f"DCS-BIOS {group}:{port}, export port {cfg['export']['port']}")

    state = dcsbios.new_state()
    bios_last = {}
    export_last = {}
    counts = {"dcsbios": {}, "export": {}}
    first_packet = set()
    try:
        while True:
            ready, _, _ = select.select([bios_sock, export_sock], [], [], 1.0)
            for sock in ready:
                data = sock.recv(65536)
                if sock is bios_sock:
                    source = "dcsbios"
                    try:
                        dcsbios.apply_packet(state, data)
                    except ValueError as e:
                        log.line("bridge", "dcsbios packet skipped", e)
                    changes = dcsbios.changes(state, outputs, bios_last)
                else:
                    source = "export"
                    try:
                        values = export.parse(data)
                    except ValueError as e:
                        log.line("bridge", "export packet skipped", e)
                        continue
                    changes = export.changes(values, export_last)
                if source not in first_packet:
                    first_packet.add(source)
                    log.line("bridge", "first packet", source)
                for name, value in changes:
                    log.line(source, name, value)
                    counts[source][name] = counts[source].get(name, 0) + 1
    except KeyboardInterrupt:
        pass
    log.line("bridge", "stop", "Ctrl+C")
    summary(counts, outputs, missing)
    bios_sock.close()
    export_sock.close()


def summary(counts: dict, outputs: dict, missing: list[str]) -> None:
    expected = {
        "dcsbios": list(outputs),
        "export": export.NAMES + [n for n in counts["export"] if n not in export.NAMES],
    }
    for source, names in expected.items():
        seen = counts[source]
        changed = [n for n in names if seen.get(n, 0) >= 2]
        groups = {
            "constant": [n for n in names if seen.get(n, 0) == 1],
            "never seen": [n for n in names if n not in seen],
        }
        text = f"{source}: {len(changed)} changed, {len(groups['constant'])} constant, {len(groups['never seen'])} never seen"
        if source == "dcsbios":
            text += f", {len(missing)} not in DCS-BIOS"
            groups["not in DCS-BIOS"] = missing
        log.line("bridge", "summary", text)
        for group, group_names in groups.items():
            if group_names:
                log.line("bridge", f"{source} {group}", ", ".join(sorted(group_names)))


if __name__ == "__main__":
    main()
