#!/usr/bin/env bash
# One-command setup for gta6-mcp. Run: ./setup.sh
set -euo pipefail
cd "$(dirname "$0")"

say() { printf '\n\033[1;35m%s\033[0m\n' "$*"; }

if ! command -v python3 >/dev/null; then
  echo "python3 not found — install Python 3.10+ first (https://python.org)"; exit 1
fi

PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
say "🐍 Python $PYVER detected"

if [ ! -d .venv ]; then
  say "📦 Creating virtualenv (.venv)…"
  python3 -m venv .venv
fi

say "⬇️  Installing gta6-mcp + dependencies…"
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -e .

say "🧪 Sanity check…"
.venv/bin/python -W ignore -c "import gta6_mcp; print('   gta6-mcp', gta6_mcp.__version__, 'OK')"

cat <<'NEXT'

✅ Installed. Three steps left (one-time):

  1. On the PS5:  Settings → System → Remote Play → turn it ON
                  then "Link Device" to get the 8-digit PIN.

  2. Link your PSN account (interactive — browser login + that PIN):

       .venv/bin/pyremoteplay <PS5_IP> --register

  3. Add the server to Claude Code:

       claude mcp add gta6 -- "$(pwd)/.venv/bin/gta6-mcp"

Then tell Claude:  "Connect to the PS5 at <PS5_IP> and take a screenshot."

Guía completa en español: docs/instalacion.md
NEXT
