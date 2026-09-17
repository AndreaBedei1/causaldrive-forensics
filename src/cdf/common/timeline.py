"""Intervals and matching within an explicitly chosen time domain.

The retained nearest-neighbour cadence helper is only a low-confidence grid
diagnostic. Periodic timestamps cannot identify physical correspondence; fusion
uses radar evidence in ``cdf.fusion.clock_alignment`` instead.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

__all__ = [
    "Interval",
    "TimeGrid",
    "estimate_clock_offset",
    "overlap",
    "temporal_relation",
    "within_tolerance",
    "build_common_grid",
]


@dataclass(frozen=True)
class Interval:
    """A closed interval in seconds of the caller's chosen clock."""

    start: float
    end: float

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise ValueError("Interval end {0} precedes start {1}".format(self.end, self.start))

    @property
    def duration(self) -> float:
        return float(self.end) - float(self.start)

    def contains(self, t: float) -> bool:
        return float(self.start) <= float(t) <= float(self.end)

    def intersects(self, other: "Interval") -> bool:
        return not (self.end < other.start or other.end < self.start)

    def intersection(self, other: "Interval") -> Optional["Interval"]:
        if not self.intersects(other):
            return None
        return Interval(max(self.start, other.start), min(self.end, other.end))

    def union_hull(self, other: "Interval") -> "Interval":
        return Interval(min(self.start, other.start), max(self.end, other.end))

    def expanded(self, pad: float) -> "Interval":
        return Interval(self.start - float(pad), self.end + float(pad))


def overlap(a: Interval, b: Interval) -> float:
    """Overlap duration of two intervals in seconds (``0.0`` when disjoint)."""
    inter = a.intersection(b)
    return 0.0 if inter is None else inter.duration


def jaccard(a: Interval, b: Interval) -> float:
    """Temporal Jaccard index of two intervals, in ``[0, 1]``.

    Degenerate (zero-length) intervals fall back to a tolerance-free equality
    test so that instantaneous events still match themselves.
    """
    inter = overlap(a, b)
    hull = a.union_hull(b).duration
    if hull <= 1e-9:
        return 1.0 if abs(a.start - b.start) <= 1e-9 else 0.0
    return float(inter) / float(hull)


def within_tolerance(t_a: float, t_b: float, tol: float) -> bool:
    """Whether two timestamps agree within ``tol`` seconds."""
    return abs(float(t_a) - float(t_b)) <= float(tol)


def temporal_relation(a: Interval, b: Interval, tol: float = 0.05) -> str:
    """Qualitative relation of ``a`` to ``b``.

    Returns one of ``"before"``, ``"after"``, ``"overlaps"``, ``"contains"``,
    ``"during"``, ``"equals"``. Used to annotate graph edges with an inspectable
    temporal justification instead of an opaque number.
    """
    if abs(a.start - b.start) <= tol and abs(a.end - b.end) <= tol:
        return "equals"
    if a.end < b.start - tol:
        return "before"
    if b.end < a.start - tol:
        return "after"
    if a.start <= b.start + tol and a.end >= b.end - tol:
        return "contains"
    if b.start <= a.start + tol and b.end >= a.end - tol:
        return "during"
    return "overlaps"


@dataclass
class TimeGrid:
    """A uniform grid in a clock domain already established by the caller."""

    t0: float
    t1: float
    dt: float

    def __post_init__(self) -> None:
        if self.dt <= 0.0:
            raise ValueError("TimeGrid dt must be positive")
        if self.t1 < self.t0:
            raise ValueError("TimeGrid t1 precedes t0")

    def times(self) -> List[float]:
        """The grid points, inclusive of both ends up to rounding."""
        n = int(math.floor((self.t1 - self.t0) / self.dt + 1e-9)) + 1
        return [self.t0 + k * self.dt for k in range(max(1, n))]

    def __len__(self) -> int:
        return len(self.times())


def build_common_grid(
    spans: Sequence[Tuple[float, float]], dt: float
) -> Optional[TimeGrid]:
    """Grid covering the *intersection* of all participant time spans.

    Returns ``None`` when the spans do not overlap, which fusion reports as a
    diagnostic instead of guessing an alignment.
    """
    if not spans:
        return None
    t0 = max(float(s[0]) for s in spans)
    t1 = min(float(s[1]) for s in spans)
    if t1 < t0:
        return None
    return TimeGrid(t0=t0, t1=t1, dt=float(dt))


@dataclass
class ClockOffsetEstimate:
    """Result of aligning one participant's clock to the reference participant."""

    participant_id: str
    reference_id: str
    offset_s: float
    """Estimated additive offset: ``t_reference ~= t_participant + offset_s``."""
    residual_s: float
    """Median absolute residual after applying the offset."""
    n_samples: int
    method: str
    confidence: float
    notes: List[str] = field(default_factory=list)


def estimate_clock_offset(
    ref_times: Sequence[float],
    other_times: Sequence[float],
    participant_id: str,
    reference_id: str,
    max_offset_s: float = 1.0,
) -> ClockOffsetEstimate:
    """Diagnose cadence phase, NOT physical clock alignment.

    Equal periodic grids can conceal arbitrarily many sample periods of offset.
    Confidence is capped at 0.05 even with zero residual. Empty results use a
    numerical zero placeholder with zero confidence, never a resolved clock.
    """
    ref = sorted(float(t) for t in ref_times)
    oth = sorted(float(t) for t in other_times)
    notes: List[str] = []

    if not ref or not oth:
        return ClockOffsetEstimate(
            participant_id=participant_id,
            reference_id=reference_id,
            offset_s=0.0,
            residual_s=float("inf"),
            n_samples=0,
            method="nearest-neighbour-median",
            confidence=0.0,
            notes=["empty series; unresolved cadence diagnostic"],
        )

    import bisect

    diffs: List[float] = []
    for t in oth:
        i = bisect.bisect_left(ref, t)
        cands = []
        if i < len(ref):
            cands.append(ref[i])
        if i > 0:
            cands.append(ref[i - 1])
        if not cands:
            continue
        nearest = min(cands, key=lambda r: abs(r - t))
        d = nearest - t
        if abs(d) <= max_offset_s:
            diffs.append(d)

    if not diffs:
        notes.append(
            "no sample pair within max_offset_s={0}s; streams may not overlap".format(
                max_offset_s
            )
        )
        return ClockOffsetEstimate(
            participant_id=participant_id,
            reference_id=reference_id,
            offset_s=0.0,
            residual_s=float("inf"),
            n_samples=0,
            method="nearest-neighbour-median",
            confidence=0.0,
            notes=notes,
        )

    diffs.sort()
    mid = len(diffs) // 2
    offset = diffs[mid] if len(diffs) % 2 == 1 else 0.5 * (diffs[mid - 1] + diffs[mid])
    residuals = sorted(abs(d - offset) for d in diffs)
    rmid = len(residuals) // 2
    residual = (
        residuals[rmid]
        if len(residuals) % 2 == 1
        else 0.5 * (residuals[rmid - 1] + residuals[rmid])
    )

    notes.append("cadence only; physical correspondence is unidentifiable")
    confidence = 0.05 / (1.0 + 50.0 * float(residual))
    if abs(offset) > 1e-6:
        notes.append(
            "non-zero cadence phase ({0:.6f}s); not a physical offset estimate".format(
                offset
            )
        )
    return ClockOffsetEstimate(
        participant_id=participant_id,
        reference_id=reference_id,
        offset_s=float(offset),
        residual_s=float(residual),
        n_samples=len(diffs),
        method="nearest-neighbour-median",
        confidence=float(confidence),
        notes=notes,
    )


def series_span(times: Sequence[float]) -> Optional[Tuple[float, float]]:
    """``(min, max)`` of a time series, or ``None`` when empty."""
    if not times:
        return None
    return (float(min(times)), float(max(times)))


def nearest_index(times: Sequence[float], t: float) -> Optional[int]:
    """Index of the sample nearest to ``t``, or ``None`` for an empty series."""
    if not times:
        return None
    best_i, best_d = 0, abs(float(times[0]) - float(t))
    for i in range(1, len(times)):
        d = abs(float(times[i]) - float(t))
        if d < best_d:
            best_i, best_d = i, d
    return best_i


def resolve_offsets(
    streams: Dict[str, Sequence[float]], reference_id: Optional[str] = None
) -> Dict[str, ClockOffsetEstimate]:
    """Estimate every participant's offset relative to a reference participant.

    The reference defaults to the participant with the most samples, which is the
    most stable anchor when one recorder produced a shorter window.
    """
    if not streams:
        return {}
    if reference_id is None:
        reference_id = max(streams.items(), key=lambda kv: len(kv[1]))[0]
    ref_times = streams[reference_id]
    out: Dict[str, ClockOffsetEstimate] = {}
    for pid, times in streams.items():
        if pid == reference_id:
            out[pid] = ClockOffsetEstimate(
                participant_id=pid,
                reference_id=reference_id,
                offset_s=0.0,
                residual_s=0.0,
                n_samples=len(times),
                method="reference",
                confidence=1.0,
            )
        else:
            out[pid] = estimate_clock_offset(ref_times, times, pid, reference_id)
    return out
