# GTA 6 MCP — Claude Plays GTA 6 🌴

> **An AI is about to drive through Vice City on a real PS5. No jailbreak. No mods. No PC port. Launch day.**

[![CI](https://github.com/Santy1422/gta6-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Santy1422/gta6-mcp/actions/workflows/ci.yml)
[![MCP](https://img.shields.io/badge/Protocol-MCP-blueviolet)](https://modelcontextprotocol.io)
[![Platform](https://img.shields.io/badge/Platform-PS5%20(stock)-003791)](https://www.playstation.com)
[![Game](https://img.shields.io/badge/Game-GTA%206-ff2d78)](https://www.rockstargames.com/VI)
[![Status](https://img.shields.io/badge/Status-T--minus%20launch%20day-orange)]()
[![Day One](https://img.shields.io/badge/Day%20One-Nov%2019%2C%202026-success)]()

**GTA 6 launches Thursday, November 19, 2026.** The same day, Claude — Anthropic's AI — will be behind the wheel. Not in an emulator. Not in a modded PC build. On a **stock PlayStation 5**, through an MCP server that streams the console's video to the model and sends controller input back.

You'll be able to watch every decision it makes, tool call by tool call.

---

## Why this hasn't been done before

"AI plays a game" is a known genre — *Claude Plays Pokémon* went viral on Twitch. "AI plays GTA" exists too… **on PC only**. Every single prior project needed a computer, a mod, or a jailbreak:

| Project | Game | Platform | Console? |
|---|---|---|---|
| Claude plays GTA 4 (covered by XDA) | GTA 4 | PC | ❌ |
| GTAV-CLAUDE-MCP | GTA V | PC + mod | ❌ |
| gta-sa-mcp / sa-mcp | San Andreas | PC | ❌ |
| local-game-mcp | Any Windows game | PC | ❌ |
| Claude/Gemini Plays Pokémon | Pokémon | Emulator | ❌ |
| ps5-mcp (prior art) | — | PS5 **jailbroken** | ⚠️ |
| **GTA 6 MCP (this project)** | **GTA 6, day one** | **Stock PS5** | ✅ |

The empty square on that board is **a real, untouched console playing the biggest game launch in history** — and that's the square this project sits on.

## How it works

No hardware hacks. Sony ships the door: **PS5 Remote Play**, which Rockstar has confirmed GTA 6 supports. We stream the console's screen out, let Claude look at it, and inject controller input back in — a full perception-action loop over the official remote play protocol.

```
            ┌──────────────────────────────────────────────┐
            │                                              │
   ┌────────▼────────┐   video stream    ┌─────────────────┴──┐
   │      PS5        │ ────────────────► │   GTA 6 MCP server │
   │  (stock, GTA 6) │                   │  (Remote Play link) │
   └────────▲────────┘                   └─────────┬──────────┘
            │                                      │ screenshot()
            │ virtual DualSense                    ▼
            │ input                      ┌────────────────────┐
            └─────────────────────────── │       Claude       │
                      press() / stick()  │  sees → thinks →   │
                      drive() / macros   │       acts         │
                                         └────────────────────┘
```

### The toolbox Claude gets

| Tool | What it does |
|---|---|
| `screenshot()` | Grab the current frame from the Remote Play stream |
| `press(button, ms)` | Tap or hold any DualSense button |
| `stick(side, x, y, ms)` | Analog stick control — steering, camera |
| `drive(throttle, steer, seconds)` | High-level driving macro |
| `enter_vehicle()` | Find and enter the nearest car |
| `open_phone()` | Open the in-game phone |

Every action Claude takes shows up as a **visible tool call in the log**, side by side with the gameplay. That log is the receipt: no scripted footage, no human on the sticks.

## What Claude can actually do (the honest part)

The perception-action loop takes seconds per cycle — Claude looks at a frame, reasons, then acts. That means:

- ✅ **Driving** through Vice City, cruising, exploring, sightseeing
- ✅ **Navigating** menus, the map, the in-game phone
- ✅ **Simple objectives** via macros: get a car, reach a location, follow a road
- ❌ Real-time combat, precision stunts, or "beating the game" — the latency makes twitch gameplay physically impossible, and we're not going to pretend otherwise

An AI tourist in Vice City on day one is the whole point — and it's wild enough on its own.

## Quickstart

Requirements: Python 3.10+, a PS5 with Remote Play enabled, and your PSN account — all on the same network.

```bash
git clone https://github.com/Santy1422/gta6-mcp.git
cd gta6-mcp
python3 -m venv .venv && .venv/bin/pip install -e .

# One-time: link your PSN account to this machine (interactive)
.venv/bin/pyremoteplay <PS5_IP> --register
```

Then add it to Claude (Claude Code shown; any MCP client works):

```bash
claude mcp add gta6 -- /path/to/gta6-mcp/.venv/bin/gta6-mcp
```

And tell Claude something like:

> Connect to the PS5 at 192.168.1.42, take a screenshot, and go for a drive.

Every input the server sends to the console is recorded — ask Claude for `action_log()` and you get the timestamped receipt of everything it did.

## Development

```bash
pip install -e ".[dev]"
ruff check src tests   # lint
pytest                 # 13 tests, no PS5 required (pyremoteplay is faked)
```

The codebase is two modules: `session.py` (Remote Play session on a background
event loop, exposed as blocking calls) and `server.py` (the MCP tool surface).

## Roadmap

- [x] Research: map every prior "AI plays GTA" project, confirm the PS5 + GTA 6 gap
- [ ] **Phase 0** — Pre-launch: PS5 Remote Play link established, first frame captured
- [ ] **Phase 1** — Minimal MCP (`screenshot`, `press`, `stick`) — server built ✅, console validation pending
- [ ] **Phase 2** — 🚨 **Launch day (Nov 19)**: Claude's first drive through Vice City, recorded
- [ ] **Phase 3** — Week one: high-level macros, longer autonomous sessions, full video
- [ ] **Phase 4** — Long-horizon goals, live streaming, and beyond

Full phase breakdown with exit criteria and risks: **[ROADMAP.md](ROADMAP.md)**. The research that started it all: **[docs/research.md](docs/research.md)**.

## Follow the launch

⭐ **Star the repo** — launch-day footage, the tool-call logs, and the MCP server code land here first. If Claude stalls a car at a red light in Vice City on November 19, you'll want to have seen it live.

## Disclaimer

This is an unofficial, independent experiment. Not affiliated with, endorsed by, or connected to Rockstar Games, Take-Two Interactive, Sony Interactive Entertainment, or Anthropic. It uses a personal PSN account and a personally owned console and copy of the game. Remote Play automation is unofficial; use at your own risk.

## License

[MIT](LICENSE)
