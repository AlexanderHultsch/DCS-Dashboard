# DCS-Dashboard

A simple tablet dashboard for the **AH-64D Apache** in DCS World. A small Python bridge connects to DCS via [DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios) and serves an HTML page you open on an iPad or any tablet. Big touch buttons replace keyboard combinations for cockpit commands and George, the AI copilot.

**Status:** early exploration. Nothing is usable yet.

## Plan

1. **Read** – test which data we can read from DCS (both seats, in flight).
2. **Control** – test which cockpit controls we can set from outside.
3. **Dashboard** – HTML page with preset views: Startup, Navigation, Fighting, George.

Details: [docs/SPEC.md](docs/SPEC.md)

## Requirements

- Windows, DCS World with the AH-64D module
- Python 3.12+
- Single player (multiplayer servers may block exports)

## Setup

Coming with Stage 1. Machine-specific settings go into `config.toml`, copied from `config.example.toml` (not tracked by git).
