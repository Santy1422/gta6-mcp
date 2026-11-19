# GTA 6 MCP — Claude Plays GTA 6 🌴

> **An AI is about to drive through Vice City on a real PS5. No jailbreak. No mods. No PC port. Launch day.**

<div align="center">

### 🔴 IT'S HAPPENING

**GTA 6 drops Thursday, Nov 19, 2026. The first AI gameplay clip lands in this repo the same day.**

**⭐ Star now · 👀 Watch releases — or find out about it a week later on someone else's feed**

</div>

[![CI](https://github.com/Santy1422/gta6-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/Santy1422/gta6-mcp/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/Santy1422/gta6-mcp/actions/workflows/ci.yml)
[![MCP](https://img.shields.io/badge/Protocol-MCP-blueviolet)](https://modelcontextprotocol.io)
[![Platform](https://img.shields.io/badge/Platform-PS5%20(stock)-003791)](https://www.playstation.com)
[![Game](https://img.shields.io/badge/Game-GTA%206-ff2d78)](https://www.rockstargames.com/VI)
[![Status](https://img.shields.io/badge/Status-T--minus%20launch%20day-orange)]()
[![Release](https://img.shields.io/github/v/release/Santy1422/gta6-mcp?label=release&color=blue)](https://github.com/Santy1422/gta6-mcp/releases)
[![Day One](https://img.shields.io/badge/Day%20One-Nov%2019%2C%202026-success)]()
[![Stars](https://img.shields.io/github/stars/Santy1422/gta6-mcp?style=social)](https://github.com/Santy1422/gta6-mcp/stargazers)

**GTA 6 launches Thursday, November 19, 2026.** The same day, Claude — Anthropic's AI — will be behind the wheel. Not in an emulator. Not in a modded PC build. On a **stock PlayStation 5**, through an MCP server that streams the console's video to the model and sends controller input back.

You'll be able to watch every decision it makes, tool call by tool call.

```text
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                                                            │
│              📼  FIRST DRIVE — RESERVED                    │
│                                                            │
│         This space intentionally left blank                │
│         until Thursday, Nov 19 2026, ~9:00 AM.             │
│                                                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

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
| `walk(x, y, seconds, sprint)` | On-foot movement bursts, with sprint |
| `enter_vehicle()` | Find and enter the nearest car |
| `open_phone()` | Open the in-game phone |
| `cheat(sequence)` | Execute a cheat-code button sequence at machine speed |

Every action Claude takes shows up as a **visible tool call in the log**, side by side with the gameplay. That log is the receipt: no scripted footage, no human on the sticks.

## What Claude can actually do (the honest part)

The perception-action loop takes seconds per cycle — Claude looks at a frame, reasons, then acts. That means:

- ✅ **Driving** through Vice City, cruising, exploring, sightseeing
- ✅ **Navigating** menus, the map, the in-game phone
- ✅ **Simple objectives** via macros: get a car, reach a location, follow a road
- ❌ Real-time combat, precision stunts, or "beating the game" — the latency makes twitch gameplay physically impossible, and we're not going to pretend otherwise

An AI tourist in Vice City on day one is the whole point — and it's wild enough on its own.

## 🎮 Cheat codes at machine speed

GTA cheats have always been button sequences — `R1, R2, L1, R2, LEFT, DOWN, RIGHT, UP…` — and humans have always fumbled them. Claude doesn't. The `cheat()` tool fires any sequence with millisecond timing, zero mistakes, every press receipted in the action log.

Nobody knows GTA 6's cheat codes yet. The moment the community finds the first one, it goes into **[docs/cheats.md](docs/cheats.md)** and Claude can execute it on stream — probably before most players have finished writing it down. Watch that file.

## Quickstart

Requirements: Python 3.10+, a PS5 with Remote Play enabled, and your PSN account — all on the same network.

```bash
git clone https://github.com/Santy1422/gta6-mcp.git
cd gta6-mcp
./setup.sh
```

That's it — the script installs everything and prints the two one-time steps left: linking your PSN account (`pyremoteplay <PS5_IP> --register`, browser login + the 8-digit PIN from the console's Remote Play settings) and adding the server to Claude.

📖 Guía detallada en español, incluyendo los ajustes de la PS5 y problemas típicos: **[docs/instalacion.md](docs/instalacion.md)**

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
ruff check src tests scripts   # lint
pytest                         # 54 tests, 100% coverage enforced, no PS5 required
```

The codebase is two modules: `session.py` (Remote Play session on a background
event loop, exposed as blocking calls) and `server.py` (the MCP tool surface — 14 tools).

Want in before Thursday? See **[CONTRIBUTING.md](CONTRIBUTING.md)**. What shipped so far: **[CHANGELOG.md](CHANGELOG.md)** · **[v0.1.0 — "The server is ready. The game isn't."](https://github.com/Santy1422/gta6-mcp/releases/tag/v0.1.0)**

## Roadmap

*Updated live through launch week — watch the checkboxes flip.*

- [x] Research: map every prior "AI plays GTA" project, confirm the PS5 + GTA 6 gap
- [ ] **Phase 0** — Pre-launch: PS5 Remote Play link established, first frame captured
- [ ] **Phase 1** — Minimal MCP (`screenshot`, `press`, `stick`) — server built ✅, console validation pending
- [ ] **Phase 2** — 🚨 **Launch day (Nov 19)**: Claude's first drive through Vice City, recorded
- [ ] **Phase 3** — Week one: high-level macros, longer autonomous sessions, full video
- [ ] **Phase 4** — Long-horizon goals, live streaming, and beyond

Full phase breakdown with exit criteria and risks: **[ROADMAP.md](ROADMAP.md)**. The research that started it all: **[docs/research.md](docs/research.md)**.

## The moment

Thursday morning, three things happen at once: GTA 6 unlocks, a stock PS5 boots it, and an AI picks up the controller. Whatever happens next — Claude cruising down Ocean Drive or stalling at its first red light — **the unedited clip and the full tool-call log get committed to this repo within hours**.

There are two kinds of people on November 19: the ones watching the first AI drive through Vice City as it happens, and the ones reading the recap. 

**How to be in the first group:**

- ⭐ **Star the repo** — this is the scoreboard that decides how far launch-day clips travel
- 👀 **Watch → Custom → Releases** — GitHub pings you the second the first clip drops
- 🔁 Got a PS5 and this repo cloned? You can run the exact same experiment Thursday — race us to the first clip

Everything ships here first. The write-ups, threads, and videos come after.

## 🔮 Place your bets

The betting window is open until the first clip drops. [**File a Prediction issue**](https://github.com/Santy1422/gta6-mcp/issues/new?template=prediction.yml) and call it:

- Seconds until the first crash
- Does Claude pick up a wanted star?
- Does it ever reach the beach?

Winners get immortalized in this README. Losers **also** get immortalized in this README. The house (the AI) always loses.

## ⭐ Star milestones

Every milestone unlocks a challenge Claude has to attempt, on camera:

| Stars | Claude must attempt… |
|---|---|
| 100 ⭐ | Parallel parking |
| 250 ⭐ | Obey **every** traffic law for 10 straight minutes |
| 500 ⭐ | Drive the full coastline without touching water |
| 1,000 ⭐ | A 24-hour autonomous session, streamed |
| 5,000 ⭐ | Pass the (self-imposed) Vice City driving test, examiner voice included |

The counter is at the top of this page. You know what to do.

## Most wanted

```text
        ╔══════════════════════════════════════════╗
        ║                 WANTED                   ║
        ║               ★ ★ ★ ★ ★                  ║
        ║                                          ║
        ║                "CLAUDE"                  ║
        ║                                          ║
        ║   Last seen : Ocean Drive, northbound    ║
        ║   Vehicle   : whatever was unlocked      ║
        ║   Charges   : driving at 2 tool calls    ║
        ║               per second, impersonating  ║
        ║               a licensed driver,         ║
        ║               excessive politeness       ║
        ║               at four-way stops          ║
        ║                                          ║
        ║   DO NOT APPROACH — IT WILL APOLOGIZE    ║
        ╚══════════════════════════════════════════╝
```

## FAQ

**Will it beat the game?**
No.

**Will it obey traffic laws?**
Also no. But unlike other Vice City residents, it will feel bad about it.

**Why is it driving so slowly?**
Each decision is a screenshot → reasoning → controller input round-trip measured in seconds. It's not slow, it's *deliberate*.

**Is this legal?**
It's my PS5, my copy of the game, and an AI with too much free time. Remote Play is an official Sony feature; the automation on top is unofficial — see the disclaimer.

**Can I run this?**
Yes — [Quickstart](#quickstart). All you need is a PS5 and the conviction that this is a good use of it.

**Is this whole repo just hype?**
The hype is real. So are the [54 passing tests](tests/) — at 100% coverage, which is more than the hype can say.

## 📰 Press

Writing about AI playing GTA 6 on launch day? The one-paragraph version:

> *On November 19, 2026, an open-source MCP server let Anthropic's Claude play Grand Theft Auto VI on an unmodified PlayStation 5 over Sony's official Remote Play protocol — screenshot in, controller input out, with a public log of every decision the AI made.*

Clips, logs, and technical details: everything in this repo is quotable with a link back.

## Disclaimer

This is an unofficial, independent experiment. Not affiliated with, endorsed by, or connected to Rockstar Games, Take-Two Interactive, Sony Interactive Entertainment, or Anthropic. It uses a personal PSN account and a personally owned console and copy of the game. Remote Play automation is unofficial; use at your own risk.

## License

[MIT](LICENSE)
