# Contributing

Launch week is the fun part — here's how to get in on it.

## The rules of the house

- **100% test coverage is enforced.** `pytest` fails under 100%. If you add a line, you test it. No PS5 needed: the whole suite runs against a faked pyremoteplay (see `tests/test_session.py`).
- **Lint:** `ruff check src tests scripts` must pass.
- **Honesty policy:** no PR gets merged that makes the README promise something the code can't do. The hype survives because it's checkable.

## Setup

```bash
git clone https://github.com/Santy1422/gta6-mcp.git
cd gta6-mcp
python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## What we want

- **Cheat codes** — the moment GTA 6 codes drop, PR them into [docs/cheats.md](docs/cheats.md). Fastest verified contribution gets credited.
- **Macros** — high-level moves that survive seconds of latency: `navigate_to`, lane-keeping bursts, menu flows.
- **Launch-day runs** — got a PS5 and this repo? Run the experiment yourself Thursday and open an issue with your clip and action log.
- **Predictions** — [place your bets](https://github.com/Santy1422/gta6-mcp/issues/new?template=prediction.yml) before the first clip drops.

## What we don't want

Jailbreaks, mods, anything that touches the console beyond Sony's official Remote Play protocol. That constraint *is* the project.
