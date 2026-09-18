"""A rolling window of camera frames, bounded in memory rather than in intent.

The premise of this project is that a vehicle keeps a short window of onboard
data and nothing more -- the same premise a dashcam or an event data recorder
works on. A camera makes that premise expensive: at 20 Hz, a 25 s window of
800x600 RGB is about 1.1 GB raw, per vehicle. So the buffer holds *compressed*
frames and drops the oldest as it goes, and the whole point of the class is that
it cannot grow past the window whatever the run does.

Two windows, not one
--------------------

The brief asks for 20 seconds before the event and 5 after, which is not a single
sliding window. Before any trigger, the buffer keeps the most recent 20 s and
discards behind that. When a trigger arrives, it stops discarding and keeps
collecting for 5 s more, then stops accepting frames entirely. That way the 20 s
before the impact survive -- which a plain 25 s sliding window would have thrown
away by the time the run ended.

The encoding decision
---------------------

Encoding to a video file while the simulator ticks would put an encoder on the
critical path of a synchronous run, and a slow tick changes the physics being
recorded. So frames are compressed individually as they arrive -- cheap, bounded,
parallel to nothing -- and muxed into a file after the run, by
:func:`encode_buffer`. If no encoder is available the frames are written as
individual images with the same index beside them, and the viewer reads either.
A missing video is a degraded artifact, never a failed run.

Timestamps are the recorder's own, like everything else local. The frame index is
what lets the viewer seek to an event: given an event at t = 8.42 on this
vehicle's clock, it names the frame to show.
"""

from __future__ import annotations

import logging
from collections import deque
from typing import Any, Deque, Dict, List, Mapping, Optional, Sequence, Tuple

LOGGER = logging.getLogger(__name__)

__all__ = ["VideoBuffer", "FrameRecord"]


class FrameRecord:
    """One compressed frame, with the recorder-local time it was taken."""

    __slots__ = ("t", "frame", "payload", "encoding", "width", "height")

    def __init__(
        self,
        t: float,
        frame: int,
        payload: bytes,
        encoding: str,
        width: int,
        height: int,
    ) -> None:
        self.t = float(t)
        self.frame = int(frame)
        self.payload = payload
        self.encoding = str(encoding)
        self.width = int(width)
        self.height = int(height)

    @property
    def nbytes(self) -> int:
        return len(self.payload)

    def index_entry(self, position: int) -> Dict[str, Any]:
        return {
            "i": position,
            "t_local": round(self.t, 4),
            "frame": self.frame,
            "bytes": self.nbytes,
            "encoding": self.encoding,
        }


class VideoBuffer:
    """Bounded pre-event / post-event frame storage for one camera.

    The bound is enforced two ways, deliberately. The time window is the intended
    limit; the frame count is a backstop, because a caller that feeds frames with
    a broken clock would otherwise defeat the window and exhaust memory. Whichever
    binds first wins.
    """

    def __init__(
        self,
        pre_event_s: float = 20.0,
        post_event_s: float = 5.0,
        max_frames: int = 1200,
        participant_id: str = "",
        sensor_id: str = "front",
    ) -> None:
        self.pre_event_s = float(pre_event_s)
        self.post_event_s = float(post_event_s)
        self.max_frames = int(max_frames)
        self.participant_id = str(participant_id)
        self.sensor_id = str(sensor_id)

        self._frames: Deque[FrameRecord] = deque()
        self._trigger_t: Optional[float] = None
        self._closed = False
        self._n_accepted = 0
        self._n_evicted = 0
        self._n_rejected_after_close = 0

    # -- state ------------------------------------------------------------

    @property
    def triggered(self) -> bool:
        return self._trigger_t is not None

    @property
    def closed(self) -> bool:
        """Whether the post-event window has elapsed and no more will be taken."""
        return self._closed

    @property
    def frames(self) -> List[FrameRecord]:
        return list(self._frames)

    def __len__(self) -> int:
        return len(self._frames)

    @property
    def nbytes(self) -> int:
        return sum(f.nbytes for f in self._frames)

    def span(self) -> Optional[Tuple[float, float]]:
        if not self._frames:
            return None
        return (self._frames[0].t, self._frames[-1].t)

    # -- filling ----------------------------------------------------------

    def mark_event(self, t: float) -> None:
        """Note that the event happened, so the pre-event window stops rolling.

        Only the first call counts. A chain collision fires several triggers, and
        re-arming on the second would extend the post-event window each time,
        turning a bounded tail into an unbounded one.
        """
        if self._trigger_t is None:
            self._trigger_t = float(t)
            LOGGER.debug(
                "%s/%s: video buffer latched at t=%.3f with %d frames held",
                self.participant_id, self.sensor_id, float(t), len(self._frames),
            )

    def add(
        self,
        t: float,
        frame: int,
        payload: bytes,
        encoding: str = "jpeg",
        width: int = 0,
        height: int = 0,
    ) -> bool:
        """Offer a frame. Returns whether it was kept.

        Frames offered after the post-event window has closed are refused and
        counted. Refusing is the point: a camera that kept recording to the end
        of the run would be recording something the premise of the experiment
        says the vehicle does not keep.
        """
        if self._closed:
            self._n_rejected_after_close += 1
            return False

        t = float(t)
        if self._trigger_t is not None and t - self._trigger_t > self.post_event_s:
            self._closed = True
            self._n_rejected_after_close += 1
            return False

        self._frames.append(FrameRecord(t, frame, payload, encoding, width, height))
        self._n_accepted += 1
        self._evict()
        return True

    def _evict(self) -> None:
        """Drop what is outside the window, and never exceed the frame backstop."""
        if self._trigger_t is None:
            # Still rolling: keep only the most recent pre-event seconds.
            cutoff = self._frames[-1].t - self.pre_event_s
            while len(self._frames) > 1 and self._frames[0].t < cutoff:
                self._frames.popleft()
                self._n_evicted += 1
        else:
            # Latched: keep the pre-event window measured from the event itself,
            # not from the newest frame, or the tail would push out the head it
            # was latched to preserve.
            cutoff = self._trigger_t - self.pre_event_s
            while len(self._frames) > 1 and self._frames[0].t < cutoff:
                self._frames.popleft()
                self._n_evicted += 1

        while len(self._frames) > self.max_frames:
            self._frames.popleft()
            self._n_evicted += 1

    # -- output -----------------------------------------------------------

    def index(self) -> Dict[str, Any]:
        """The frame index, which is what makes the video seekable by event time."""
        span = self.span()
        return {
            "participant_id": self.participant_id,
            "sensor_id": self.sensor_id,
            "clock": "participant-local",
            "pre_event_s": self.pre_event_s,
            "post_event_s": self.post_event_s,
            "event_t_local": (
                None if self._trigger_t is None else round(self._trigger_t, 4)
            ),
            "n_frames": len(self._frames),
            "t_first": None if span is None else round(span[0], 4),
            "t_last": None if span is None else round(span[1], 4),
            "duration_s": None if span is None else round(span[1] - span[0], 4),
            "bytes": self.nbytes,
            "n_accepted": self._n_accepted,
            "n_evicted_by_window": self._n_evicted,
            "n_refused_after_window_closed": self._n_rejected_after_close,
            "width": self._frames[0].width if self._frames else 0,
            "height": self._frames[0].height if self._frames else 0,
            "frames": [
                f.index_entry(i) for i, f in enumerate(self._frames)
            ],
            "note": (
                "recorder-local timestamps. The index is how a viewer seeks to "
                "an event: an event at t on this vehicle's clock maps to the "
                "frame with the nearest t_local"
            ),
        }

    def frame_at(self, t: float) -> Optional[int]:
        """Index of the frame nearest a local time, for seeking."""
        if not self._frames:
            return None
        best, best_gap = 0, abs(self._frames[0].t - float(t))
        for i, frame in enumerate(self._frames):
            gap = abs(frame.t - float(t))
            if gap < best_gap:
                best, best_gap = i, gap
        return best
