"""Remote Play session wrapper: one PS5, one background event loop.

pyremoteplay's Session is asyncio-based; the MCP server's tools are
synchronous calls. This module bridges the two by running the Remote Play
session on a dedicated event loop in a daemon thread and exposing blocking
methods on top of it.

Every input sent to the console is recorded in an action log — the public
"receipt" that proves the AI is the one on the sticks.
"""

from __future__ import annotations

import asyncio
import io
import threading
import time
import warnings
from collections import deque
from datetime import datetime, timezone
from typing import Any

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pyee")

from pyremoteplay import RPDevice
from pyremoteplay.receiver import QueueReceiver

CONNECT_TIMEOUT = 30.0
FRAME_TIMEOUT = 10.0
ACTION_LOG_SIZE = 200
MAX_DRIVE_SECONDS = 5.0

STICKS = ("left", "right")


class SessionError(RuntimeError):
    """Raised when the Remote Play session cannot do what was asked."""


def _clamp(value: float) -> float:
    return max(-1.0, min(1.0, value))


class RemotePlaySession:
    """Owns the connection to a single PS5 over Remote Play."""

    def __init__(self) -> None:
        self._device: RPDevice | None = None
        self._receiver: QueueReceiver | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._actions: deque[dict[str, Any]] = deque(maxlen=ACTION_LOG_SIZE)

    # ------------------------------------------------------------------ state

    @property
    def connected(self) -> bool:
        return bool(self._device and self._device.connected)

    def _require_connection(self) -> RPDevice:
        if not self.connected:
            raise SessionError("Not connected to a PS5. Call connect(host) first.")
        return self._device

    def _record(self, action: str, **details: Any) -> None:
        self._actions.append(
            {
                "at": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                "action": action,
                **details,
            }
        )

    def action_log(self, limit: int = 20) -> list[dict[str, Any]]:
        return list(self._actions)[-max(1, limit):]

    # ------------------------------------------------------------- discovery

    @staticmethod
    def search() -> list[dict[str, Any]]:
        devices = RPDevice.search()
        return [
            {
                "host": device.host,
                "name": device.host_name,
                "type": device.host_type,
                "status": device.status_name,
            }
            for device in devices
        ]

    @staticmethod
    def status(host: str) -> dict[str, Any]:
        device = RPDevice(host)
        status = device.get_status()
        if not status:
            raise SessionError(
                f"No response from {host}. Is the PS5 on (or in rest mode with "
                "Remote Play enabled) and on the same network?"
            )
        return dict(status)

    @staticmethod
    def wake(host: str, user: str | None = None) -> str:
        device = RPDevice(host)
        users = device.get_users()
        if not users:
            raise SessionError(
                f"No registered PSN users for {host}. Register once with: "
                f"pyremoteplay {host} --register"
            )
        device.wakeup(user or users[0])
        return f"Wake signal sent to {host}. The console may take ~20s to come up."

    # ------------------------------------------------------------ connection

    def connect(
        self,
        host: str,
        user: str | None = None,
        resolution: str = "720p",
        fps: int = 30,
    ) -> dict[str, Any]:
        if self.connected:
            raise SessionError("Already connected. Call disconnect() first.")

        device = RPDevice(host)
        if not device.get_status():
            raise SessionError(
                f"No response from {host}. Is the PS5 reachable on this network?"
            )
        users = device.get_users()
        if not users:
            raise SessionError(
                f"No registered PSN users for {host}. Register once with: "
                f"pyremoteplay {host} --register"
            )
        if user is None:
            user = users[0]
        elif user not in users:
            raise SessionError(f"User {user!r} not registered. Known users: {users}")

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever, name="remoteplay-loop", daemon=True
        )
        self._thread.start()

        self._receiver = QueueReceiver()
        device.create_session(
            user,
            loop=self._loop,
            receiver=self._receiver,
            resolution=resolution,
            fps=fps,
            quality="default",
            codec="h264",
        )
        try:
            ok = asyncio.run_coroutine_threadsafe(
                device.connect(), self._loop
            ).result(CONNECT_TIMEOUT)
            if not ok:
                raise SessionError(
                    "Remote Play session refused. Check that this user is "
                    "registered and no other Remote Play client is connected."
                )
            device.controller.start()
            self._device = device
            self._wait_first_frame()
        except Exception:
            self._device = None
            self._teardown(device)
            raise
        self._record("connect", host=host, user=user, resolution=resolution, fps=fps)
        return {"host": host, "user": user, "resolution": resolution, "fps": fps}

    def disconnect(self) -> None:
        device, self._device = self._device, None
        self._teardown(device)
        if device is not None:
            self._record("disconnect")

    def _teardown(self, device: RPDevice | None) -> None:
        if device is not None:
            try:
                device.disconnect()
            except Exception:
                pass
        if self._loop is not None:
            self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread is not None:
                self._thread.join(timeout=5)
        self._loop = None
        self._thread = None
        self._receiver = None

    def _wait_first_frame(self) -> None:
        deadline = time.monotonic() + FRAME_TIMEOUT
        while time.monotonic() < deadline:
            if self._receiver.video_frames:
                return
            time.sleep(0.2)
        raise SessionError(
            "Connected, but no video frame arrived. The stream may be blocked "
            "or the codec unsupported; try resolution='540p'."
        )

    # ---------------------------------------------------------------- vision

    def screenshot(self) -> bytes:
        self._require_connection()
        frame = self._receiver.get_latest_video_frame()
        if frame is None:
            raise SessionError("No video frame available yet.")
        image = frame.to_image()
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        self._record("screenshot", size=f"{image.width}x{image.height}")
        return buf.getvalue()

    # ----------------------------------------------------------------- input

    def tap(self, button: str, ms: int = 100) -> None:
        device = self._require_connection()
        button = button.upper()
        ms = max(10, ms)
        device.controller.button(button, "press")
        time.sleep(ms / 1000)
        device.controller.button(button, "release")
        self._record("press", button=button, ms=ms)

    def stick(self, side: str, x: float, y: float, ms: int = 500) -> None:
        device = self._require_connection()
        if side not in STICKS:
            raise SessionError(f"Unknown stick {side!r}; use one of {STICKS}.")
        x, y = _clamp(x), _clamp(y)
        ms = max(10, ms)
        device.controller.stick(side, point=(x, y))
        time.sleep(ms / 1000)
        device.controller.stick(side, point=(0.0, 0.0))
        self._record("stick", side=side, x=x, y=y, ms=ms)

    def walk(
        self, x: float, y: float, seconds: float, sprint: bool = False
    ) -> dict[str, Any]:
        """Move on foot: hold the left stick (and CROSS to sprint) for a burst."""
        device = self._require_connection()
        x, y = _clamp(x), _clamp(y)
        if x == 0 and y == 0:
            raise SessionError("walk needs a direction; x and y are both 0.")
        seconds = max(0.2, min(seconds, MAX_DRIVE_SECONDS))
        device.controller.stick("left", point=(x, y))
        if sprint:
            device.controller.button("CROSS", "press")
        try:
            time.sleep(seconds)
        finally:
            if sprint:
                device.controller.button("CROSS", "release")
            self.release_sticks()
        self._record("walk", x=x, y=y, seconds=seconds, sprint=sprint)
        return {"x": x, "y": y, "seconds": seconds, "sprint": sprint}

    def combo(self, buttons: list[str], interval_ms: int = 80) -> dict[str, Any]:
        """Execute a button sequence at machine speed — the cheat-code primitive."""
        device = self._require_connection()
        if not buttons:
            raise SessionError("Empty button sequence.")
        sequence = [b.upper() for b in buttons]
        unknown = [b for b in sequence if b not in device.controller.buttons()]
        if unknown:
            raise SessionError(
                f"Unknown buttons {unknown}; valid: {device.controller.buttons()}"
            )
        interval = max(30, interval_ms) / 1000
        for button in sequence:
            device.controller.button(button, "press")
            time.sleep(interval / 2)
            device.controller.button(button, "release")
            time.sleep(interval / 2)
        self._record("combo", buttons=sequence, interval_ms=interval_ms)
        return {"buttons": sequence, "count": len(sequence), "interval_ms": interval_ms}

    def drive(self, throttle: float, steer: float, seconds: float) -> dict[str, Any]:
        device = self._require_connection()
        throttle, steer = _clamp(throttle), _clamp(steer)
        seconds = max(0.2, min(seconds, MAX_DRIVE_SECONDS))
        pedal = "R2" if throttle >= 0 else "L2"
        pressing = abs(throttle) > 0.05

        if steer:
            device.controller.stick("left", point=(steer, 0.0))
        if pressing:
            device.controller.button(pedal, "press")
        try:
            time.sleep(seconds)
        finally:
            if pressing:
                device.controller.button(pedal, "release")
            self.release_sticks()
        self._record("drive", throttle=throttle, steer=steer, seconds=seconds, pedal=pedal)
        return {"throttle": throttle, "steer": steer, "seconds": seconds, "pedal": pedal}

    def release_sticks(self) -> None:
        device = self._require_connection()
        for side in STICKS:
            device.controller.stick(side, point=(0.0, 0.0))
