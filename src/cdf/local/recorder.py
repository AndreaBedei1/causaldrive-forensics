"""Memory-bounded rolling forensic recorder (an event-data-recorder analogue).

Each participant runs one :class:`RollingRecorder`. It behaves like an automotive
EDR: the vehicle continuously overwrites a short rolling history of its *own*
onboard signals, and only when something happens (an impact, a near miss, an
emergency brake) is that history frozen and a further stretch of post-event data
appended. Everything older than the window is gone -- it was never kept.

Why a rolling buffer rather than "log everything"
-------------------------------------------------
Two reasons, one practical and one scientific.

*Practical*: raw CARLA radar produces roughly 145 detections per frame per
sensor. At 20 Hz over a 45 s run that is ~130k detections per vehicle, and the
recorder must run inside the simulation loop without unbounded growth. The
buffers here are sized once, from ``recorder.pre_event_s * recorder.sample_rate_hz``,
and provably cannot exceed that size before a trigger (see
:class:`RingBuffer`, whose backing store is a ``deque`` with a hard ``maxlen``).

*Scientific*: the central claim of this project is that a useful causal
reconstruction can be built from what a vehicle could *plausibly* have retained,
not from an omniscient recording of the whole world. Bounding the evidence is
therefore part of the experiment, not an optimisation.

Memory bound after the trigger
------------------------------
Freezing the window must not turn the buffers into an unbounded log either. Once
a trigger fires the pre-event ring buffers stop receiving appends (so nothing
they hold can be evicted) and later samples go into post-event lists that accept
data only inside ``[t_trigger, t_trigger + post_event_s]`` *and* only up to a
fixed post-event capacity. The total retention is thus hard-capped at
``(pre_event_s + post_event_s) * sample_rate_hz * records_per_step`` records per
stream, whatever the caller does afterwards -- a time bound alone would not do,
because a sensor callback that fires faster than the nominal rate (or twice for
the same timestamp) would otherwise grow the post-event lists without limit.

Records per step
----------------
Not every stream produces one record per simulation step. The tracker emits up
to ``radar_processing.tracking.max_tracks`` :class:`TrackSample` per step and a
vehicle may carry several radars, each contributing its own
:class:`RadarFrame`. Sizing those buffers at ``pre_event_s * sample_rate_hz``
*records* would therefore silently shorten their history -- with 16 tracks per
step the retained track window would cover 1.25 s instead of 20 s, and the track
stream is precisely the interaction evidence the downstream event extraction
depends on. Each stream is consequently sized at
``pre_event_s * sample_rate_hz * records_per_step`` (the multiplicity is read
from the same configuration keys the producers use), so every stream really does
retain ``pre_event_s`` of history. The bound stays structural: the multiplicities
are fixed at construction time, never grown in response to traffic.

Layer discipline
----------------
The recorder stores records exactly as its owner produced them; it never
inspects, enriches or correlates them, and it has no access to any other
participant. Event extraction is a separate stage, which is why
:meth:`RollingRecorder.to_evidence` returns a bundle with an empty ``events``
list.
"""

from __future__ import annotations

import dataclasses
from collections import deque
from typing import Any, Deque, Dict, Generic, List, Optional, Sequence, Tuple, TypeVar

from ..common.config import Config
from ..common.evidence import ParticipantEvidence, save_participant
from ..common.layout import RunLayout
from ..common.schemas import (
    ControlSample,
    LocalTriggerRecord,
    RadarFrame,
    TelemetrySample,
    TrackSample,
)
from ..common.timeline import Interval

__all__ = ["RingBuffer", "RollingRecorder"]


_T = TypeVar("_T")

#: Tolerance used for "has enough simulation time elapsed" comparisons. It only
#: absorbs float accumulation noise in timestamps; it is not a grace period.
_TIME_EPS = 1e-9


class RingBuffer(Generic[_T]):
    """A bounded FIFO of timestamped records.

    The capacity is a *hard* bound: the backing ``deque`` is constructed with
    ``maxlen``, so appending to a full buffer evicts the oldest item in O(1) and
    ``len(buffer) <= capacity`` holds by construction rather than by convention.
    That property is what makes the recorder's memory footprint provable instead
    of merely intended.

    Items are expected to carry a ``t`` attribute (simulation seconds), which
    :meth:`drop_before` uses to additionally bound the buffer *in time*.
    """

    __slots__ = ("_items", "_capacity")

    def __init__(self, max_samples: int) -> None:
        capacity = int(max_samples)
        if capacity < 1:
            raise ValueError(
                "RingBuffer capacity must be at least 1, got {0!r}".format(max_samples)
            )
        self._capacity = capacity
        self._items: Deque[_T] = deque(maxlen=capacity)

    # -- introspection ----------------------------------------------------

    @property
    def capacity(self) -> int:
        """Maximum number of retained items; never exceeded."""
        return self._capacity

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def items(self) -> List[_T]:
        """A snapshot list of the retained items, oldest first."""
        return list(self._items)

    @property
    def oldest(self) -> Optional[_T]:
        """The oldest retained item, or ``None`` when empty."""
        return self._items[0] if self._items else None

    @property
    def newest(self) -> Optional[_T]:
        """The most recently appended item, or ``None`` when empty."""
        return self._items[-1] if self._items else None

    # -- mutation ---------------------------------------------------------

    def append(self, item: _T) -> None:
        """Append one item, evicting the oldest when the buffer is full."""
        self._items.append(item)

    def extend(self, items: Sequence[_T]) -> None:
        """Append several items in order."""
        for item in items:
            self._items.append(item)

    def clear(self) -> None:
        """Discard every retained item."""
        self._items.clear()

    def drop_before(self, t: float) -> int:
        """Evict leading items whose timestamp is strictly before ``t``.

        Returns the number of evicted items. Eviction stops at the first item
        that is new enough, which is correct for the non-decreasing timestamp
        order the recorder feeds in and keeps the cost proportional to the number
        actually removed.
        """
        cutoff = float(t)
        removed = 0
        while self._items:
            head = self._items[0]
            head_t = getattr(head, "t", None)
            if head_t is None:
                raise TypeError(
                    "RingBuffer.drop_before requires items with a 't' attribute, "
                    "got {0!r}".format(type(head).__name__)
                )
            if float(head_t) < cutoff:
                self._items.popleft()
                removed += 1
            else:
                break
        return removed

    def __repr__(self) -> str:
        return "RingBuffer(len={0}, capacity={1})".format(len(self._items), self._capacity)


class _Stream:
    """One recorded signal: rolling pre-event buffer plus post-event storage.

    Both halves are bounded. ``buffer`` is a :class:`RingBuffer` (evicts the
    oldest, which is the point of a rolling window) and ``post`` is a plain list
    that *refuses* records once ``post_capacity`` is reached. Refusing rather
    than evicting is deliberate: after an impact the earliest post-event records
    are the valuable ones, so an over-fast stream must lose its tail, never the
    moment of the incident.
    """

    __slots__ = ("name", "buffer", "post", "post_capacity", "records_per_step")

    def __init__(self, name: str, capacity: int, post_capacity: int, records_per_step: int) -> None:
        self.name = str(name)
        self.buffer: RingBuffer = RingBuffer(capacity)
        self.post: List[Any] = []
        self.post_capacity = int(post_capacity)
        self.records_per_step = int(records_per_step)

    def __len__(self) -> int:
        return len(self.buffer) + len(self.post)


class RollingRecorder:
    """Per-participant rolling recorder with a one-shot freeze on trigger.

    Lifecycle
    ---------
    1. *Rolling* -- every ``record_*`` call appends to a ring buffer, and
       anything older than ``recorder.pre_event_s`` before the newest observed
       simulation time is evicted. Memory is flat.
    2. *Frozen* -- the first :meth:`trigger` pins the window to
       ``[t_trigger - pre_event_s, t_trigger + post_event_s]``. The pre-event
       buffers are trimmed once to that start time and then never touched again,
       so no evidence recorded before the incident can be lost. Subsequent
       samples are appended to post-event lists while they fall inside the
       window, and ignored once the window closes.
    3. *Finished* -- :attr:`finished` turns ``True`` as soon as the observed
       simulation time reaches ``t_trigger + post_event_s``. The driving loop
       polls it to decide when the run may stop.

    Later triggers are recorded as evidence (a near miss followed by a collision
    is exactly the sequence we want to see) but never restart the window: an EDR
    that re-armed on every subsequent event would drop the pre-incident history
    that makes the reconstruction possible.
    """

    def __init__(self, cfg: Config, participant_id: str) -> None:
        self.cfg = cfg
        self.participant_id = str(participant_id)

        self.pre_event_s = float(cfg.get("recorder.pre_event_s", 20.0))
        self.post_event_s = float(cfg.get("recorder.post_event_s", 5.0))
        self.sample_rate_hz = float(cfg.get("recorder.sample_rate_hz", 20.0))
        self.max_radar_points_per_frame = int(
            cfg.get("recorder.max_radar_points_per_frame", 400)
        )

        if self.pre_event_s <= 0.0:
            raise ValueError(
                "recorder.pre_event_s must be positive, got {0!r}".format(self.pre_event_s)
            )
        if self.post_event_s < 0.0:
            raise ValueError(
                "recorder.post_event_s must not be negative, got {0!r}".format(
                    self.post_event_s
                )
            )
        if self.sample_rate_hz <= 0.0:
            raise ValueError(
                "recorder.sample_rate_hz must be positive, got {0!r}".format(
                    self.sample_rate_hz
                )
            )
        if self.max_radar_points_per_frame < 1:
            raise ValueError(
                "recorder.max_radar_points_per_frame must be at least 1, got {0!r}".format(
                    self.max_radar_points_per_frame
                )
            )

        self._sample_period_s = 1.0 / self.sample_rate_hz
        # Boundary slack of half a nominal sampling period, to absorb float
        # accumulation in timestamps. It is not a grace period.
        self._edge_slack_s = 0.5 * self._sample_period_s
        # Time-bound of the rolling window. ``pre_event_s * sample_rate_hz``
        # samples at the nominal rate span ``pre_event_s - sample_period`` of
        # simulation time (N samples bracket N-1 intervals), so the time cutoff
        # is placed half a period inside the nominal edge: the count bound and
        # the time bound then agree exactly at the nominal rate, whatever a
        # stream's per-step multiplicity is, instead of one clipping the other.
        self._retention_span_s = self.pre_event_s - self._edge_slack_s

        self._capacity = max(1, int(round(self.pre_event_s * self.sample_rate_hz)))
        # One extra step of headroom so the sample landing exactly on the window
        # edge is never the one refused.
        self._post_capacity = max(1, int(round(self.post_event_s * self.sample_rate_hz)) + 1)

        # How many records each stream produces per simulation step. Read from
        # the very configuration keys the producers use, so the recorder cannot
        # drift out of step with the tracker or the sensor profile.
        sensors = cfg.get("radar.sensors", []) or []
        radar_per_step = max(1, len(sensors) if isinstance(sensors, (list, tuple)) else 1)
        tracks_per_step = max(1, int(cfg.get("radar_processing.tracking.max_tracks", 16)))

        self._streams: Dict[str, _Stream] = {}
        for name, per_step in (
            ("telemetry", 1),
            ("controls", 1),
            ("radar", radar_per_step),
            ("tracks", tracks_per_step),
        ):
            self._streams[name] = _Stream(
                name,
                capacity=self._capacity * per_step,
                post_capacity=self._post_capacity * per_step,
                records_per_step=per_step,
            )

        self._triggers: List[LocalTriggerRecord] = []
        # Triggers are caller-driven too, so they get a bound of their own: an
        # over-eager near-miss detector must not turn the trigger list into the
        # unbounded log the rest of this class is built to avoid. The *earliest*
        # triggers are kept, the first of which anchors the window.
        self._max_triggers = self._capacity + self._post_capacity
        self._triggers_discarded = 0
        self._frozen = False
        self._t_trigger: Optional[float] = None
        self._t_last: Optional[float] = None

        self._radar_points_discarded = 0
        self._samples_outside_window = 0
        self._samples_over_capacity = 0

    # -- state ------------------------------------------------------------

    @property
    def capacity(self) -> int:
        """Pre-event capacity in simulation *steps* (``pre_event_s * rate``).

        A stream that produces several records per step (radar with more than one
        sensor, tracks) is sized at this many steps times its multiplicity; see
        :meth:`stream_capacities`.
        """
        return self._capacity

    def stream_capacities(self) -> Dict[str, int]:
        """Hard per-stream record capacity of the rolling pre-event buffers."""
        return {name: s.buffer.capacity for name, s in sorted(self._streams.items())}

    def records_per_step(self) -> Dict[str, int]:
        """How many records per simulation step each stream is sized for."""
        return {name: s.records_per_step for name, s in sorted(self._streams.items())}

    @property
    def triggered(self) -> bool:
        """Whether a trigger has fired and the window is frozen."""
        return self._frozen

    @property
    def trigger_time(self) -> Optional[float]:
        """Simulation time of the *first* trigger, or ``None``."""
        return self._t_trigger

    @property
    def last_time(self) -> Optional[float]:
        """Newest simulation time observed by any stream."""
        return self._t_last

    @property
    def triggers(self) -> List[LocalTriggerRecord]:
        """All recorded triggers, in arrival order."""
        return list(self._triggers)

    @property
    def finished(self) -> bool:
        """Whether a trigger fired and ``post_event_s`` of sim time has elapsed."""
        if not self._frozen or self._t_trigger is None or self._t_last is None:
            return False
        return self._t_last + _TIME_EPS >= self._t_trigger + self.post_event_s

    @property
    def window(self) -> Optional[Interval]:
        """The retained window.

        After a trigger this is the pinned ``[t_trigger - pre_event_s,
        t_trigger + post_event_s]``; while still rolling it is the span actually
        retained, which is the honest answer to "what would survive right now".
        ``None`` before anything has been recorded.
        """
        if self._frozen and self._t_trigger is not None:
            return Interval(
                self._t_trigger - self.pre_event_s, self._t_trigger + self.post_event_s
            )
        span = self._retained_span()
        if span is None:
            return None
        return Interval(span[0], span[1])

    def counts(self) -> Dict[str, int]:
        """Retained record counts per stream (diagnostics and tests)."""
        out: Dict[str, int] = {name: len(s) for name, s in self._streams.items()}
        out["triggers"] = len(self._triggers)
        return out

    # -- recording --------------------------------------------------------

    def record_telemetry(self, s: TelemetrySample) -> None:
        """Retain one own-telemetry sample."""
        self._check_owner(s.participant_id, "telemetry")
        self._store("telemetry", s)

    def record_control(self, s: ControlSample) -> None:
        """Retain one own-control sample."""
        self._check_owner(s.participant_id, "control")
        self._store("controls", s)

    def record_radar(self, f: RadarFrame) -> None:
        """Retain one radar frame, capped at ``max_radar_points_per_frame``.

        Raw CARLA frames are dominated by road-surface clutter, so an uncapped
        recorder would spend almost all of its memory on returns the processing
        stage discards anyway. The cap keeps the *nearest* detections, which are
        the ones that carry interaction evidence.
        """
        self._check_owner(f.participant_id, "radar")
        self._store("radar", self._cap_detections(f))

    def record_tracks(self, samples: Sequence[TrackSample]) -> None:
        """Retain a batch of local track samples (one tracker output step).

        Ownership is validated over the whole batch *before* anything is stored,
        so a mis-wired tracker cannot leave half a step behind in the buffers.
        """
        batch = list(samples)
        for s in batch:
            self._check_owner(s.participant_id, "track")
        for s in batch:
            self._store("tracks", s)

    def trigger(self, rec: LocalTriggerRecord) -> None:
        """Record a trigger; the first one freezes the pre-event window."""
        self._check_owner(rec.participant_id, "trigger")
        self._note_time(float(rec.t))
        if len(self._triggers) < self._max_triggers:
            self._triggers.append(rec)
        else:
            self._triggers_discarded += 1
        if self._frozen:
            # Deliberate no-op on the window: a re-arming EDR would throw away
            # the pre-incident history the whole method depends on.
            return
        self._frozen = True
        self._t_trigger = float(rec.t)
        self._freeze_window()

    # -- output -----------------------------------------------------------

    def to_evidence(self) -> ParticipantEvidence:
        """Bundle everything retained into a :class:`ParticipantEvidence`.

        ``events`` is intentionally left empty: extraction is a separate stage
        that consumes this bundle, and mixing the two would make the recorder
        untestable in isolation.
        """
        return ParticipantEvidence(
            participant_id=self.participant_id,
            telemetry=self._merged("telemetry"),
            controls=self._merged("controls"),
            radar=self._merged("radar"),
            tracks=self._merged("tracks"),
            triggers=sorted(self._triggers, key=lambda r: float(r.t)),
            events=[],
            meta=self.meta(),
        )

    def persist(self, layout: RunLayout) -> ParticipantEvidence:
        """Write the retained evidence into the canonical run layout."""
        evidence = self.to_evidence()
        save_participant(layout, evidence)
        return evidence

    def meta(self) -> Dict[str, Any]:
        """Serialisable description of how this bundle was retained.

        Persisted alongside the evidence so that a later reader can tell what the
        recorder could and could not have kept -- an "absence of evidence" claim
        is only defensible if the retention policy is on record.
        """
        window = self.window
        return {
            "recorder": {
                "participant_id": self.participant_id,
                "pre_event_s": self.pre_event_s,
                "post_event_s": self.post_event_s,
                "sample_rate_hz": self.sample_rate_hz,
                "buffer_capacity_samples": self._capacity,
                "post_capacity_samples": self._post_capacity,
                "stream_capacity_samples": self.stream_capacities(),
                "records_per_step": self.records_per_step(),
                "max_radar_points_per_frame": self.max_radar_points_per_frame,
                "radar_points_discarded": self._radar_points_discarded,
                "samples_outside_window_discarded": self._samples_outside_window,
                "samples_over_capacity_discarded": self._samples_over_capacity,
                "triggers_discarded": self._triggers_discarded,
                "triggered": self._frozen,
                "finished": self.finished,
                "trigger_t": self._t_trigger,
                "n_triggers": len(self._triggers),
                "window_start": None if window is None else window.start,
                "window_end": None if window is None else window.end,
                "counts": self.counts(),
            }
        }

    # -- internals --------------------------------------------------------

    def _check_owner(self, participant_id: str, stream: str) -> None:
        """Reject a record belonging to another participant.

        A recorder is strictly single-owner; a foreign record reaching it means
        the sensor callbacks were mis-wired, which would fabricate cross-vehicle
        evidence. That must fail loudly rather than be silently stored.
        """
        if str(participant_id) != self.participant_id:
            raise ValueError(
                "recorder for participant {0!r} received a {1} record owned by "
                "{2!r}".format(self.participant_id, stream, participant_id)
            )

    def _note_time(self, t: float) -> None:
        """Advance the observed simulation clock (monotone, never regresses)."""
        value = float(t)
        self._t_last = value if self._t_last is None else max(self._t_last, value)

    def _store(self, stream_name: str, item: Any) -> bool:
        """Retain ``item``, respecting the rolling or frozen retention policy.

        Returns whether the item was retained.
        """
        stream = self._streams[stream_name]
        t = float(item.t)
        self._note_time(t)

        if self._frozen:
            if not self._in_frozen_window(t):
                self._samples_outside_window += 1
                return False
            if len(stream.post) >= stream.post_capacity:
                # The window is frozen, not unbounded: a callback firing faster
                # than the configured rate loses its tail here rather than
                # growing the post-event list without limit.
                self._samples_over_capacity += 1
                return False
            stream.post.append(item)
            return True

        buffer = stream.buffer
        buffer.append(item)
        # Time-bound the rolling window as well as count-bounding it: when a
        # stream ticks faster than the nominal rate the capacity alone would
        # retain less than pre_event_s, and when it ticks slower it would retain
        # more than the policy allows.
        buffer.drop_before(self._t_last - self._retention_span_s)
        return True

    def _in_frozen_window(self, t: float) -> bool:
        """Whether ``t`` falls inside the pinned window (with edge slack)."""
        if self._t_trigger is None:
            return True
        start = self._t_trigger - self.pre_event_s - self._edge_slack_s
        end = self._t_trigger + self.post_event_s + self._edge_slack_s
        return start <= float(t) <= end

    def _freeze_window(self) -> None:
        """Trim every pre-event buffer once, to the pinned window start."""
        if self._t_trigger is None:
            raise RuntimeError("_freeze_window called before a trigger was recorded")
        cutoff = self._t_trigger - self._retention_span_s
        for stream in self._streams.values():
            stream.buffer.drop_before(cutoff)

    def _cap_detections(self, frame: RadarFrame) -> RadarFrame:
        """Return ``frame`` with at most ``max_radar_points_per_frame`` returns.

        The nearest detections are kept. A copy is made only when the cap
        actually bites, so the common case costs nothing and the caller's frame
        object is never mutated.
        """
        n = len(frame.detections)
        if n <= self.max_radar_points_per_frame:
            return frame
        # Stable sort: detections at equal range keep their original order, so
        # the truncation is deterministic.
        kept = sorted(frame.detections, key=lambda d: float(d.depth))[
            : self.max_radar_points_per_frame
        ]
        self._radar_points_discarded += n - len(kept)
        return dataclasses.replace(frame, detections=kept)

    def _merged(self, stream_name: str) -> List[Any]:
        """Pre-event buffer followed by post-event records, sorted by time."""
        stream = self._streams[stream_name]
        out: List[Any] = stream.buffer.items()
        out.extend(stream.post)
        out.sort(key=lambda s: float(s.t))
        return out

    def _retained_span(self) -> Optional[Tuple[float, float]]:
        """``(t_first, t_last)`` over everything currently retained."""
        lo: Optional[float] = None
        hi: Optional[float] = None
        for stream in self._streams.values():
            buffer = stream.buffer
            post = stream.post
            candidates: List[float] = []
            if len(buffer) > 0:
                candidates.append(float(buffer.oldest.t))
                candidates.append(float(buffer.newest.t))
            if post:
                candidates.append(float(post[0].t))
                candidates.append(float(post[-1].t))
            for value in candidates:
                lo = value if lo is None else min(lo, value)
                hi = value if hi is None else max(hi, value)
        if lo is None or hi is None:
            return None
        return (lo, hi)

    def __repr__(self) -> str:
        return (
            "RollingRecorder(participant={0!r}, capacity={1}, triggered={2}, "
            "counts={3})".format(
                self.participant_id, self._capacity, self._frozen, self.counts()
            )
        )
