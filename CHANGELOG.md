# Changelog

## v0.1.0 — 2026-11-17 — "The server is ready. The game isn't."

Two days before GTA 6 launches, the MCP server is feature-complete for day one:

### Added
- Remote Play session bridge over pyremoteplay: background event loop, blocking tool surface, hardened teardown
- 14 MCP tools: `search`, `status`, `wake`, `connect`, `disconnect`, `screenshot`, `press`, `stick`, `drive`, `walk`, `cheat`, `enter_vehicle`, `open_phone`, `action_log`
- `cheat()` — button sequences at machine speed, validated against the DualSense map
- `walk()` — on-foot movement bursts with optional sprint, for the pre-car minutes of launch day
- `action_log()` — the timestamped receipt of every input the AI sends
- 54 tests at 100% coverage (enforced in CI), no console required
- Daily self-updating launch countdown in the README
- Prediction betting via issue template; cheat-code registry awaiting day one

### Known unknowns
- pyremoteplay vs. current PS5 firmware: untested against real hardware until Phase 0 completes (fallback: chiaki-ng)
- GTA 6's actual button mapping: assumed GTA-conventional until Thursday
