"""The gta6-mcp server: the toolbox Claude uses to play GTA 6 on a PS5.

Low-level tools (screenshot/press/stick) form the perception-action loop;
the macros (drive/enter_vehicle/open_phone) are GTA-shaped shortcuts so a
single tool call covers seconds of gameplay despite model latency.
"""

from __future__ import annotations

import time

from mcp.server.mcpserver import Image, MCPServer

from .session import RemotePlaySession

mcp = MCPServer(
    "gta6-mcp",
    instructions=(
        "Control a PS5 running GTA 6 over Remote Play. Workflow: status(host) "
        "to find the console, connect(host) to start the session, then loop "
        "screenshot() -> decide -> press()/stick()/drive(). The action loop "
        "has seconds of latency: prefer short macro bursts (1-3 s), re-observe "
        "after every action, and avoid anything needing real-time reactions."
    ),
)

_session = RemotePlaySession()


@mcp.tool()
def status(host: str) -> dict:
    """Check whether a PS5 at this IP/hostname is reachable and what it's running."""
    return RemotePlaySession.status(host)


@mcp.tool()
def connect(host: str, user: str | None = None, resolution: str = "720p") -> dict:
    """Start a Remote Play session with the PS5 at `host`.

    The PSN user must already be registered on this machine
    (one-time: `pyremoteplay <host> --register`). Defaults to the first
    registered user. Resolutions: 360p, 540p, 720p, 1080p.
    """
    return _session.connect(host, user=user, resolution=resolution)


@mcp.tool()
def disconnect() -> str:
    """End the Remote Play session."""
    _session.disconnect()
    return "Disconnected."


@mcp.tool()
def screenshot() -> Image:
    """Grab the current frame of the game as a PNG. Call after every action."""
    return Image(data=_session.screenshot(), format="png")


@mcp.tool()
def press(button: str, ms: int = 100) -> str:
    """Tap or hold a DualSense button for `ms` milliseconds.

    Buttons: CROSS, CIRCLE, SQUARE, TRIANGLE, UP, DOWN, LEFT, RIGHT,
    L1, R1, L2, R2, L3, R3, OPTIONS, SHARE, PS, TOUCHPAD.
    """
    _session.tap(button, ms)
    return f"Pressed {button.upper()} for {ms} ms."


@mcp.tool()
def stick(side: str, x: float, y: float, ms: int = 500) -> str:
    """Move the 'left' or 'right' analog stick to (x, y) for `ms` milliseconds.

    x: -1.0 (left) to 1.0 (right). y: -1.0 (up) to 1.0 (down).
    Left stick moves/steers; right stick controls the camera.
    The stick returns to center afterwards.
    """
    _session.stick(side, x, y, ms)
    return f"Stick {side} at ({x:.2f}, {y:.2f}) for {ms} ms."


@mcp.tool()
def drive(throttle: float = 1.0, steer: float = 0.0, seconds: float = 2.0) -> str:
    """Drive the current vehicle for `seconds` (capped at 5).

    throttle: 1.0 accelerate (R2), -1.0 brake/reverse (L2), 0 coast.
    steer: -1.0 full left to 1.0 full right.
    Short bursts (1-3 s) then screenshot() to see where you ended up.
    """
    seconds = max(0.2, min(seconds, 5.0))
    pedal = "R2" if throttle >= 0 else "L2"
    if steer:
        _session._require_connection().controller.stick(
            "left", point=(max(-1.0, min(1.0, steer)), 0.0)
        )
    if abs(throttle) > 0.05:
        _session.hold(pedal)
    time.sleep(seconds)
    if abs(throttle) > 0.05:
        _session.release(pedal)
    _session.release_sticks()
    return f"Drove {seconds:.1f}s (throttle={throttle:+.2f} via {pedal}, steer={steer:+.2f})."


@mcp.tool()
def enter_vehicle() -> str:
    """Enter the nearest vehicle (holds TRIANGLE). Then screenshot() to confirm."""
    _session.tap("TRIANGLE", ms=400)
    return "Sent enter-vehicle (TRIANGLE held 400 ms)."


@mcp.tool()
def open_phone() -> str:
    """Open the in-game phone (D-pad UP)."""
    _session.tap("UP", ms=100)
    return "Sent open-phone (UP)."


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
