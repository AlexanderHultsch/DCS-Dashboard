# DCS-Dashboard – Spec

## Purpose and open outcome

This is an exploratory open-source hobby project: a self-made helper dashboard on a tablet (iPad) for the AH-64D in DCS World. It replaces keyboard combinations for cockpit commands and the George AI copilot, and shows a few relevant values. The end result is deliberately open; each stage ends with a go / no-go decision for the next.

Principles:

- Keep it simple: the smallest code that works, few dependencies, no extra layers.
- Not every edge case is handled: a crash or a lost packet is fine, a restart fixes it.
- One interface: the Python bridge is the only way the dashboard talks to DCS.
- Debuggable: a size-limited rolling log makes problems traceable from the log files alone.

Public repo rules:

- No personal data in code, docs, logs or commits: no names, emails, IP addresses, user paths or machine names.
- Everything machine-specific (DCS Saved Games folder, ports, keybinds) lives in a local `config.toml`; the repo ships only `config.example.toml`.
- Logs and local config are in `.gitignore` and never committed.
- Commits use the GitHub no-reply address.

## Fixed decisions

| Topic | Decision |
| --- | --- |
| Aircraft | AH-64D only, pilot and CPG seat |
| Game mode | Single player only |
| Platform | DCS World on Windows (Steam or standalone) |
| Language | Python for the bridge; plain HTML, CSS and JavaScript for the dashboard; Lua only for the small DCS-side export script |
| Code | Public GitHub repo `DCS-Dashboard`, only the main branch; usable by anyone |
| Dashboard | HTML page served by the bridge, used in a tablet browser over the local network |
| Debug log | Rolling log file with a size limit: events and value changes |
| AI | Not part of the product; see future development |
| Test scripts | One for reading (Stage 1), one for controlling (Stage 2) |

## Architecture

```
DCS World · AH-64D (gaming PC)
 ├─ DCS-BIOS (Lua) ............ switches, lamps, display text, radios; accepts commands
 └─ Custom export script (Lua)  position, attitude, speeds, engine and fuel values
        │ UDP (states, commands, flight data)      ▲ keypresses (George, key combos)
        ▼                                          │
Python bridge · the only interface
 ├─ State store ......... live values from all sources, every change to the log
 ├─ Command sender ...... DCS-BIOS commands, keypresses
 └─ Web server .......... serves the HTML page, live updates via WebSocket
        ▲ USB                   │ writes               ▲▼ WebSocket
 Your controls            Rolling log             Tablet dashboard
 (stick, collective,      (size-limited files)    (4 preset views, HTML,
  pedals)                                          follows current seat)
```

DCS-BIOS and a small export script deliver the data. The bridge holds it, sends every command and serves the dashboard page. Everything that happens lands in the rolling log.

## Stage 1 – Read all data

Goal: prove which values we can read live, for both seats and in flight.

Detailed spec, value list and build steps: [STAGE1.md](STAGE1.md). It takes precedence over this section; USB controls (source 4) are deferred there.

Sources:

1. DCS-BIOS ([DCS-Skunkworks fork](https://github.com/DCS-Skunkworks/dcs-bios), AH-64D module): switch positions, lamps, EUFD and KU text, radio frequencies, standby instruments, current seat.
2. Custom export script (Lua, runs next to DCS-BIOS): position, heading, pitch, bank, airspeed, radar altitude, vertical speed, G, engine and fuel values from DCS's built-in export functions.
3. Try only: MPD page text through DCS's display parsing. May not work for the Apache.
4. Your controls: cyclic, collective, pedals and their buttons, read directly in Python via USB.

Test script `stage1_read.py`:

- Listens to all four sources at once.
- Prints only changed values to the console.
- Writes every change to the rolling log `logs/dcs-dashboard.log`: time, source, name, value.
- On exit prints a summary: which values changed at least once, which never did.

Test run:

1. Cold and dark on the ramp, pilot seat: flip a few switches, start APU and engines.
2. Switch to the CPG seat, flip a few switches there.
3. Short hover and a small circuit, land.

Done when: the log covers both seats and the flight, and each value group is marked readable, not readable or implausible. The Apache engine values get extra attention.

## Stage 2 – Check what is controllable

Goal: a pass / fail list of every control we can set from outside, for both seats.

Detailed spec, routes and build steps: [STAGE2.md](STAGE2.md). It takes precedence over this section.

Routes:

- DCS-BIOS commands for all cockpit controls; preferred wherever an entry exists.
- Simulated keypresses to the DCS window for George and for keyboard combinations without a DCS-BIOS entry. Needs the keybinds set in DCS and the DCS window in focus.
- Fallback only if keypresses prove unreliable: commands sent through the custom export script.

Test script `stage2_sweep.py`:

- Reads the AH-64D control list from DCS-BIOS and works through the controls of the current seat.
- Sets each switch or knob to each position, waits about 0.5 s, checks the readback, then restores the original position.
- Push buttons without a readback are marked "sent, not verifiable".
- Blocklist, never sent: jettison controls, fire buttons and extinguishers, zeroize switches, CHOP, BUCS, weapons trigger, M4 trigger.
- George commands and keyboard combinations are sent one by one; the user confirms the result, since they have no readback.
- Writes `logs/stage2_results.csv`: control, seat, route, result (pass, fail, sent-unverified, skipped). Details go to the rolling log.

Test run: cold and dark on the ramp, once per seat.

Done when: every control of both seats has a result and the failures are reviewed.

## Stage 3 – Tablet dashboard

Goal: replace the keyboard combinations for cockpit commands and George with buttons on a tablet, plus a few relevant displays. Flying itself stays on stick, collective and pedals.

Detailed spec, view list and build steps: [STAGE3.md](STAGE3.md). It takes precedence over this section; it uses polling (GET /state five times per second) instead of a WebSocket.

How it works:

- The bridge serves a plain HTML page (HTML, CSS, JavaScript, no framework), opened in the tablet's browser and added to the home screen for fullscreen.
- Live values and button presses run over one WebSocket between page and bridge.
- Local network only, no login.
- Shows pilot or CPG controls automatically, depending on the current seat.
- Mainly large touch buttons and a few displays per view; the design stays plain now and gets polished later.
- Only controls that passed Stage 2 go on the dashboard.

Preset views, switched by tabs at the top:

| View | Buttons | Displays |
| --- | --- | --- |
| Startup | Master ignition, APU cover and button, engine 1 and 2 start, power levers, rotor brake, parking brake | APU and engine ready and fire lamps, master caution and warning |
| Navigation | MPD bezel buttons incl. TSD, KU keyboard, force trim and hold mode switch | KU scratchpad, EUFD lines, radar altitude, airspeed, heading, vertical speed |
| Fighting | Master arm / safe, ground override, weapons action switch, sight select, flare, chaff | Arm / safe lamps, flare and chaff counts, master caution and warning |
| George | George command buttons | None planned |

Keyboard combinations for cockpit commands each get a button on the view where they belong. The MPD buttons are a plain grid without page labels; the MPD itself is read in the game.

Done when: one session from cold start to a short flight works without the keyboard for every listed command.

## Future development: AI integration

Not part of this plan, and nothing in Stages 1 to 3 depends on it. If the dashboard works well, an AI assistant (e.g. Claude) could later connect to the bridge through an MCP server.

Ideas collected so far:

- Status advisor: reads cautions, lamps and flight and engine data, explains them and suggests next steps.
- Auto startup: runs a routine from cold and dark to ready for takeoff.
- Waypoint entry: enters a coordinate list into the TSD via the KU.
- George control on request.
- Each capability would be a use case with its own on / off toggle on the dashboard.

## Assumptions, open questions, out of scope

Assumptions:

- The gaming PC runs Windows with Python 3.12 or newer; tablet and PC share the local network.
- The DCS Saved Games folder is set in `config.toml`.
- The George commands and the keyboard combinations are bound to keys in the DCS control settings.
- Rolling log: 5 MB per file, the last 3 files kept, about 15 MB in total.

Open questions:

- [ ] Radios on the dashboard in version 1, or later?
- [x] Are the generic engine values plausible for the Apache? Partly: RPM is NG %, temperature is always 0. TGT, torque, NP and NR come from the MPD page text. See [STAGE1.md](STAGE1.md#results).
- [x] Can the MPD page text be read? Yes, for the displays of the occupied seat. See [STAGE1.md](STAGE1.md#results).
- [x] Keypresses need the DCS window in focus. Is that fine when triggered from the tablet? Yes: the bridge brings DCS to the front before each key, which worked every time. See [STAGE2.md](STAGE2.md#results).
- [ ] Which keyboard combinations for cockpit commands are used today? Each one becomes a dashboard button.

Out of scope: AI integration (see future development), multiplayer, automatic flying (stick, collective, pedals), cockpit-replica graphics, hardware panels, security beyond the local network.
