"""Unit tests for RemotePlaySession with a faked pyremoteplay device.

No PS5 required: RPDevice and QueueReceiver are replaced with fakes that
record every controller call, so we can assert exactly what would hit the
console.
"""

import asyncio
import io

import pytest
from PIL import Image

import gta6_mcp.session as session_module
from gta6_mcp.session import RemotePlaySession, SessionError


class FakeController:
    def __init__(self):
        self.calls = []
        self.started = False

    def start(self):
        self.started = True

    def button(self, name, action="tap"):
        self.calls.append(("button", name, action))

    def stick(self, side, axis=None, value=None, point=None):
        self.calls.append(("stick", side, point))


class FakeFrame:
    def to_image(self):
        return Image.new("RGB", (64, 36), "hotpink")


class FakeReceiver:
    def __init__(self):
        self.video_frames = [FakeFrame()]

    def get_latest_video_frame(self):
        return self.video_frames[-1]


class FakeDevice:
    registered_users = ["tester"]
    reachable = True

    def __init__(self, host):
        self.host = host
        self.controller = FakeController()
        self.connected = False
        self.session_kwargs = None

    def get_status(self):
        return {"host-name": "FAKE-PS5"} if self.reachable else None

    def get_users(self):
        return list(self.registered_users)

    def create_session(self, user, **kwargs):
        self.session_kwargs = {"user": user, **kwargs}

    async def connect(self):
        self.connected = True
        return True

    def disconnect(self):
        self.connected = False


@pytest.fixture
def fake_env(monkeypatch):
    FakeDevice.registered_users = ["tester"]
    FakeDevice.reachable = True
    monkeypatch.setattr(session_module, "RPDevice", FakeDevice)
    monkeypatch.setattr(session_module, "QueueReceiver", FakeReceiver)
    monkeypatch.setattr(session_module, "FRAME_TIMEOUT", 1.0)
    monkeypatch.setattr(session_module.time, "sleep", lambda s: None)


@pytest.fixture
def connected(fake_env):
    s = RemotePlaySession()
    s.connect("10.0.0.5")
    yield s
    s.disconnect()


def test_connect_reports_session_details(connected):
    assert connected.connected
    device = connected._device
    assert device.controller.started
    assert device.session_kwargs["user"] == "tester"


def test_connect_rejects_unknown_user(fake_env):
    with pytest.raises(SessionError, match="not registered"):
        RemotePlaySession().connect("10.0.0.5", user="stranger")


def test_connect_requires_registration(fake_env):
    FakeDevice.registered_users = []
    with pytest.raises(SessionError, match="--register"):
        RemotePlaySession().connect("10.0.0.5")


def test_tools_require_connection():
    s = RemotePlaySession()
    for call in (s.screenshot, lambda: s.tap("CROSS"), lambda: s.stick("left", 1, 0)):
        with pytest.raises(SessionError, match="Not connected"):
            call()


def test_screenshot_returns_png(connected):
    png = connected.screenshot()
    assert Image.open(io.BytesIO(png)).size == (64, 36)


def test_tap_presses_then_releases(connected):
    connected.tap("cross", ms=50)
    calls = connected._device.controller.calls
    assert ("button", "CROSS", "press") in calls
    assert ("button", "CROSS", "release") in calls
    assert calls.index(("button", "CROSS", "press")) < calls.index(
        ("button", "CROSS", "release")
    )


def test_stick_clamps_and_recenters(connected):
    connected.stick("left", 5.0, -5.0, ms=50)
    calls = [c for c in connected._device.controller.calls if c[0] == "stick"]
    assert calls[0] == ("stick", "left", (1.0, -1.0))
    assert calls[-1] == ("stick", "left", (0.0, 0.0))


def test_stick_rejects_unknown_side(connected):
    with pytest.raises(SessionError, match="Unknown stick"):
        connected.stick("middle", 0, 0)


def test_drive_uses_r2_and_steers(connected):
    result = connected.drive(throttle=1.0, steer=-0.5, seconds=2.0)
    assert result["pedal"] == "R2"
    calls = connected._device.controller.calls
    assert ("stick", "left", (-0.5, 0.0)) in calls
    assert ("button", "R2", "press") in calls
    assert ("button", "R2", "release") in calls


def test_drive_brakes_with_l2_and_caps_duration(connected):
    result = connected.drive(throttle=-1.0, steer=0.0, seconds=60.0)
    assert result["pedal"] == "L2"
    assert result["seconds"] == session_module.MAX_DRIVE_SECONDS


def test_action_log_records_inputs(connected):
    connected.tap("CROSS", ms=50)
    connected.drive(1.0, 0.0, 1.0)
    actions = [entry["action"] for entry in connected.action_log()]
    assert actions[0] == "connect"
    assert "press" in actions and "drive" in actions
    assert all("at" in entry for entry in connected.action_log())


def test_disconnect_resets_state(connected):
    connected.disconnect()
    assert not connected.connected
    with pytest.raises(SessionError):
        connected.screenshot()


def test_server_registers_all_tools():
    from gta6_mcp.server import mcp

    tools = {t.name for t in asyncio.run(mcp.list_tools())}
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
        "enter_vehicle",
        "open_phone",
        "action_log",
    }
