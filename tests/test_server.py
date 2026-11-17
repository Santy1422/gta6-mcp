"""Tests for the MCP tool surface, with the session faked out."""

import asyncio

import pytest

from gta6_mcp import server
from gta6_mcp.session import RemotePlaySession


class FakeSession:
    def __init__(self):
        self.calls = []

    def connect(self, host, user=None, resolution="720p"):
        self.calls.append(("connect", host, user, resolution))
        return {"host": host, "user": user or "tester", "resolution": resolution}

    def disconnect(self):
        self.calls.append(("disconnect",))

    def screenshot(self):
        self.calls.append(("screenshot",))
        return b"\x89PNG fake"

    def tap(self, button, ms=100):
        self.calls.append(("tap", button, ms))

    def stick(self, side, x, y, ms=500):
        self.calls.append(("stick", side, x, y, ms))

    def drive(self, throttle, steer, seconds):
        self.calls.append(("drive", throttle, steer, seconds))
        return {
            "throttle": throttle,
            "steer": steer,
            "seconds": min(seconds, 5.0),
            "pedal": "R2" if throttle >= 0 else "L2",
        }

    def combo(self, buttons, interval_ms=80):
        self.calls.append(("combo", tuple(buttons), interval_ms))
        return {
            "buttons": [b.upper() for b in buttons],
            "count": len(buttons),
            "interval_ms": interval_ms,
        }

    def action_log(self, limit=20):
        self.calls.append(("action_log", limit))
        return [{"action": "press"}]


@pytest.fixture
def fake_session(monkeypatch):
    fake = FakeSession()
    monkeypatch.setattr(server, "_session", fake)
    return fake


def test_search_delegates(monkeypatch):
    monkeypatch.setattr(
        RemotePlaySession, "search", staticmethod(lambda: [{"host": "10.0.0.9"}])
    )
    assert server.search() == [{"host": "10.0.0.9"}]


def test_status_delegates(monkeypatch):
    monkeypatch.setattr(
        RemotePlaySession, "status", staticmethod(lambda host: {"host": host})
    )
    assert server.status("10.0.0.5") == {"host": "10.0.0.5"}


def test_wake_delegates(monkeypatch):
    monkeypatch.setattr(
        RemotePlaySession, "wake", staticmethod(lambda host, user=None: f"woke {host}")
    )
    assert server.wake("10.0.0.5") == "woke 10.0.0.5"


def test_connect_and_disconnect(fake_session):
    assert server.connect("10.0.0.5")["host"] == "10.0.0.5"
    assert server.disconnect() == "Disconnected."
    assert ("disconnect",) in fake_session.calls


def test_screenshot_wraps_png(fake_session):
    image = server.screenshot()
    assert image.data.startswith(b"\x89PNG")


def test_press_and_stick(fake_session):
    assert "CROSS" in server.press("cross", ms=50)
    assert ("tap", "cross", 50) in fake_session.calls
    assert "left" in server.stick("left", 1.0, -1.0, ms=200)
    assert ("stick", "left", 1.0, -1.0, 200) in fake_session.calls


def test_drive_formats_result(fake_session):
    message = server.drive(throttle=-1.0, steer=0.5, seconds=2.0)
    assert "L2" in message and "+0.50" in message
    assert ("drive", -1.0, 0.5, 2.0) in fake_session.calls


def test_cheat_parses_sequence(fake_session):
    message = server.cheat("R1, R2 L1,CROSS")
    assert "4-button sequence" in message
    assert ("combo", ("R1", "R2", "L1", "CROSS"), 80) in fake_session.calls


def test_macros(fake_session):
    server.enter_vehicle()
    server.open_phone()
    assert ("tap", "TRIANGLE", 400) in fake_session.calls
    assert ("tap", "UP", 100) in fake_session.calls


def test_action_log(fake_session):
    assert server.action_log(5) == [{"action": "press"}]
    assert ("action_log", 5) in fake_session.calls


def test_main_runs_server(monkeypatch):
    ran = []
    monkeypatch.setattr(server.mcp, "run", lambda: ran.append(True))
    server.main()
    assert ran == [True]


def test_all_tools_registered():
    tools = {t.name for t in asyncio.run(server.mcp.list_tools())}
    assert tools == {
        "search",
        "status",
        "wake",
        "connect",
        "disconnect",
        "screenshot",
        "press",
        "stick",
        "drive",
        "cheat",
        "enter_vehicle",
        "open_phone",
        "action_log",
    }
