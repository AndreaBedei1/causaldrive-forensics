"""Time synchronisation of two viewers shown side by side (GROUND TRUTH and RECONSTRUCTION, docs/REPLAY.md).

The leading viewer sends, on a local UDP port, only the instant it shows on the recording clock (``t_recording``:
the clock of the recordings, the simulator's in the canonical runs, where every recorder's clock is the
simulator's), whether it plays, and its speed.  The following viewer maps that instant through its own clock
(``run.replay_time_of``) and takes the play state and speed.  Nothing else crosses: no position, identity or event,
so neither viewer reads anything of the other's data and each keeps its own CARLA server.
"""

from __future__ import annotations

import json
import socket
from typing import Any, Dict, Optional

HOST = "127.0.0.1"


def encode(t_recording: float, playing: bool, speed: float) -> bytes:
    return json.dumps({"t_recording": round(float(t_recording), 6), "playing": bool(playing),
                       "speed": float(speed)}).encode("utf-8")


def decode(data: bytes) -> Dict[str, Any]:
    message = json.loads(data.decode("utf-8"))
    return {"t_recording": float(message["t_recording"]), "playing": bool(message["playing"]),
            "speed": float(message["speed"])}


class SyncSender:
    """The leading viewer: one datagram per frame to the follower's port on this machine."""

    def __init__(self, port: int) -> None:
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, t_recording: float, playing: bool, speed: float) -> None:
        try:
            self.socket.sendto(encode(t_recording, playing, speed), (HOST, self.port))
        except OSError:
            pass  # no follower yet: the leader is never disturbed

    def close(self) -> None:
        self.socket.close()


class SyncReceiver:
    """The following viewer: the latest datagram received since the previous call, if any."""

    def __init__(self, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, int(port)))
        self.socket.setblocking(False)
        self.port = self.socket.getsockname()[1]

    def latest(self) -> Optional[Dict[str, Any]]:
        message = None
        while True:
            try:
                data = self.socket.recv(4096)
            except (BlockingIOError, OSError):
                return message
            try:
                message = decode(data)
            except (ValueError, KeyError):
                continue

    def close(self) -> None:
        self.socket.close()


def apply_sync(clock: Any, run: Any, message: Dict[str, Any]) -> None:
    """Put a follower's PlaybackClock on the leader's instant, play state and speed."""
    clock.seek_to(run.replay_time_of(message["t_recording"]))
    if message["speed"] > 0:
        clock.set_speed(message["speed"])
    clock.playing = bool(message["playing"]) and not clock.at_end
