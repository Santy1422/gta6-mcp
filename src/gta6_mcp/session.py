"""Remote Play session wrapper: one PS5, one background event loop.

pyremoteplay's Session is asyncio-based; the MCP server's tools are
synchronous calls. This module bridges the two by running the Remote Play
session on a dedicated event loop in a daemon thread and exposing blocking
methods on top of it.
"""

from __future__ import annotations

import asyncio
import io
import threading
import time
import warnings
from typing import Optional

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pyee")

from pyremoteplay import RPDevice
from pyremoteplay.receiver import QueueReceiver

CONNECT_TIMEOUT = 30.0
FRAME_TIMEOUT = 10.0

STICKS = ("left", "right")


class SessionError(RuntimeError):
    """Raised when the Remote Play session cannot do what was asked."""


class RemotePlaySession:
    """Owns the connection to a single PS5 over Remote Play."""

    def __init__(self) -> None:
        self._device: Optional[RPDevice] = None
        self._receiver: Optional[QueueReceiver] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None

    # ------------------------------------------------------------------ state

    @property
    def connected(self) -> bool:
        return bool(self._device and self._device.connected)

    def _require_connection(self) -> RPDevice:
        if not self.connected:
            raise SessionError(
                "Not connected to a PS5. Call connect(host) first."
            )
        return self._device

    # ------------------------------------------------------------- discovery

    @staticmethod
    def status(host: str) -> dict:
        device = RPDevice(host)
        status = device.get_status()
        if not status:
            raise SessionError(
                f"No response from {host}. Is the PS5 on (or in rest mode with "
                "Remote Play enabled) and on the same network?"
            )
        return dict(status)

    # ------------------------------------------------------------ connection

    def connect(
        self,
        host: str,
        user: Optional[str] = None,
        resolution: str = "720p",
        fps: int = 30,
    ) -> dict:
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
            self._teardown(device)
            raise
        return {"host": host, "user": user, "resolution": resolution, "fps": fps}

    def disconnect(self) -> None:
        device, self._device = self._device, None
        self._teardown(device)

    def _teardown(self, device: Optional[RPDevice]) -> None:
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
        return buf.getvalue()

    # ----------------------------------------------------------------- input

    def tap(self, button: str, ms: int = 100) -> None:
        device = self._require_connection()
        button = button.upper()
        device.controller.button(button, "press")
        time.sleep(max(ms, 10) / 1000)
        device.controller.button(button, "release")

    def hold(self, button: str) -> None:
        self._require_connection().controller.button(button.upper(), "press")

    def release(self, button: str) -> None:
        self._require_connection().controller.button(button.upper(), "release")

    def stick(self, side: str, x: float, y: float, ms: int = 500) -> None:
        device = self._require_connection()
        if side not in STICKS:
            raise SessionError(f"Unknown stick {side!r}; use one of {STICKS}.")
        x = max(-1.0, min(1.0, x))
        y = max(-1.0, min(1.0, y))
        device.controller.stick(side, point=(x, y))
        time.sleep(max(ms, 10) / 1000)
        device.controller.stick(side, point=(0.0, 0.0))

    def release_sticks(self) -> None:
        device = self._require_connection()
        for side in STICKS:
            device.controller.stick(side, point=(0.0, 0.0))
