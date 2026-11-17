# Roadmap

The realistic plan. Dates are anchored to the GTA 6 launch on **Thursday, November 19, 2026**. Each phase has an exit gate — we don't move on until it's met, and we say so publicly when something slips.

## Phase 0 — Pre-launch plumbing (Nov 17–18)

**Goal:** prove we can see and touch the console before the game exists.

- [ ] Confirm PS5 firmware version and enable Remote Play
- [ ] Register the console with [pyremoteplay](https://pyremoteplay.readthedocs.io/) and establish a session
- [ ] Receive a video frame from the stream programmatically
- [ ] Send a button press and see it land on the console

**Exit gate:** one frame captured + one input delivered, end to end.

**Contingency:** if pyremoteplay fails against current PS5 firmware (14.x), fall back to [chiaki-ng](https://github.com/streetpea/chiaki-ng) as the Remote Play client, with window capture + virtual gamepad input pointed at its window. Slower to brag about, equally real.

## Phase 1 — Minimal MCP server (Nov 18)

**Goal:** the smallest tool surface Claude needs, validated on a game we already own.

- [x] MCP server exposing `screenshot()`, `press(button, ms)`, `stick(side, x, y, ms)` — plus `drive()`, `enter_vehicle()`, `open_phone()` macros
- [ ] Claude completes a trivial task in another PS5 game (navigate a menu, move a character)
- [ ] Tool-call log capture working alongside screen recording

**Exit gate:** Claude performs a multi-step action on the PS5 unassisted, with the log to prove it.

## Phase 2 — Launch day 🚨 (Nov 19)

**Goal:** Claude's first drive through Vice City, recorded, the day the game comes out.

- [ ] Boot GTA 6, get past intro/menus (human-assisted is fine here — we say so)
- [ ] Start Claude with the character in a car on an open street
- [ ] Short-burst macros (1–3 s): throttle, steer, brake, look around
- [ ] Record gameplay + live tool-call log side by side
- [ ] Publish the first clip

**Exit gate:** a published, unedited clip of Claude driving in GTA 6 on a stock PS5.

## Phase 3 — Week one (Nov 20–26)

**Goal:** from "it moves" to "it does things".

- [ ] High-level macros: `drive(throttle, steer, seconds)`, `enter_vehicle()`, `open_phone()`, `navigate_to(landmark)`
- [ ] Longer autonomous sessions (15–30 min) with a stated objective
- [ ] A full-length video with real footage; update the README with it
- [ ] Clean up and publish the MCP server code with setup instructions

**Exit gate:** someone else can clone the repo and reproduce the setup with their own PS5.

## Phase 4 — Later / ideas

No dates. These happen if the foundation holds and people care:

- Long-horizon goals ("cross the whole map", "earn $X in-game")
- Live streaming sessions (the Claude Plays Pokémon format)
- Xbox Series support via cloud gaming
- Smarter perception: minimap reading, objective-text OCR

## Known risks (and how we handle them)

| Risk | Reality | Mitigation |
|---|---|---|
| **Latency** | The screenshot → model → action loop takes seconds; GTA 6 runs at 30 FPS plus Remote Play compression | Design for driving/exploring, not combat. Short macro bursts. Never promise twitch gameplay |
| **Firmware** | Sony ships firmware often (14.x in Sept/Oct 2026); unofficial libraries can break | Phase 0 tests this first; chiaki-ng fallback ready |
| **Capture limits** | Unknown whether Rockstar/Sony restricts Remote Play or capture in the first hours | Test before promising anything publicly on day one |
| **Competition** | The GTA 4 experiment already made news; others will try on launch day | Speed (Phases 0–2 inside 48 h) and the console-not-PC angle |
| **PSN account** | This is unofficial automation | Personal account, personal console, personal risk |

## Out of scope / non-goals

Things this project will **not** claim, so nobody has to walk anything back:

- ❌ Real-time combat or anything requiring sub-second reactions
- ❌ Speedruns
- ❌ "Claude beats GTA 6" — it won't, and saying otherwise would break the moment anyone looks closely
- ❌ Anything requiring a jailbreak, mods, or TOS-breaking console tampering
