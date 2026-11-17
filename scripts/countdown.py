"""Rewrite the README countdown banner based on days until GTA 6 launch.

Run daily by .github/workflows/countdown.yml. Exits 0 always; prints
"changed" when the README was modified so the workflow knows to commit.
"""

import re
from datetime import date, datetime, timezone
from pathlib import Path

LAUNCH = date(2026, 11, 19)
README = Path(__file__).resolve().parent.parent / "README.md"
BANNER = re.compile(r"^### (⏳|🔴|🏁).*$", flags=re.MULTILINE)


def banner_for(today: date) -> str:
    days = (LAUNCH - today).days
    if days > 1:
        return f"### ⏳ T-MINUS {days} DAYS"
    if days == 1:
        return "### ⏳ T-MINUS 1 DAY"
    if days == 0:
        return "### 🔴 IT'S HAPPENING"
    return "### 🏁 IT HAPPENED — scroll down for the clips"


def main() -> None:
    today = datetime.now(timezone.utc).date()
    text = README.read_text(encoding="utf-8")
    updated = BANNER.sub(banner_for(today), text, count=1)
    if updated != text:
        README.write_text(updated, encoding="utf-8")
        print("changed")
    else:
        print("unchanged")


if __name__ == "__main__":
    main()
