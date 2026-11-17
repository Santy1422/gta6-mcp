"""Tests for the README countdown banner script."""

import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import countdown  # noqa: E402


@pytest.mark.parametrize(
    ("today", "expected"),
    [
        (date(2026, 11, 10), "### ⏳ T-MINUS 9 DAYS"),
        (date(2026, 11, 17), "### ⏳ T-MINUS 2 DAYS"),
        (date(2026, 11, 18), "### ⏳ T-MINUS 1 DAY"),
        (date(2026, 11, 19), "### 🔴 IT'S HAPPENING"),
        (date(2026, 11, 20), "### 🏁 IT HAPPENED — scroll down for the clips"),
        (date(2027, 1, 1), "### 🏁 IT HAPPENED — scroll down for the clips"),
    ],
)
def test_banner_for(today, expected):
    assert countdown.banner_for(today) == expected


@pytest.fixture
def fake_readme(tmp_path, monkeypatch):
    readme = tmp_path / "README.md"
    readme.write_text("# Title\n\n### ⏳ T-MINUS 9 DAYS\n\nbody\n", encoding="utf-8")
    monkeypatch.setattr(countdown, "README", readme)

    class FixedDatetime:
        @staticmethod
        def now(tz=None):
            return datetime(2026, 11, 19, 12, 0, tzinfo=timezone.utc)

    monkeypatch.setattr(countdown, "datetime", FixedDatetime)
    return readme


def test_main_updates_banner(fake_readme, capsys):
    countdown.main()
    assert capsys.readouterr().out.strip() == "changed"
    assert "### 🔴 IT'S HAPPENING" in fake_readme.read_text(encoding="utf-8")


def test_main_is_idempotent(fake_readme, capsys):
    countdown.main()
    countdown.main()
    assert capsys.readouterr().out.strip().splitlines() == ["changed", "unchanged"]
    assert fake_readme.read_text(encoding="utf-8").count("🔴") == 1
