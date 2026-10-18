# A-10C II – DCS-BIOS mapping

Maps every control in [PANELS.md](PANELS.md) to its DCS-BIOS identifier. Source: the DCS-Skunkworks DCS-BIOS module `A-10C` (`Scripts/DCS-BIOS/lib/modules/aircraft_modules/A-10C.lua`, commit 11c6209 of 2026-10-08), which serves both the A-10C and the A-10C II (`A-10C_2`). The module has 749 controls.

Sections and control names follow PANELS.md. Columns:

- **DCS-BIOS identifier**: the name used to read and command the control; `—` if there is none.
- **Access**: `read + command` (an output and an input exist), `read only` (lamps, gauges, text: `defineIndicatorLight`, `defineFloat`, `defineString`, `define8BitFloat`, `defineBitFromDrawArgument`, `defineFloatFromDrawArgument`, `defineIntegerFromGetter`), or `—`.
- **Note**: the DCS-BIOS description or positions where they differ from PANELS.md, `likely` when the match is by meaning rather than by name, and for controls without an identifier the gap: `keybind` (needs a DCS key), `export` (needs the export script), `no function in DCS`, or `not exported`.
