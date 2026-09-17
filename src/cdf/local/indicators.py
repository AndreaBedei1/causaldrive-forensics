"""Derived local indicators: what one vehicle can compute from its own evidence.

Every quantity produced here is a function of a *single* participant's own
localisation, own actuator commands and own radar tracks. Nothing in this module
reads another actor's true state, a map, a lane graph or a signal phase -- which
is precisely why the indicators are admissible as local forensic evidence.

Two families are produced:

``OwnIndicators``
    Ego behaviour: speed, body-frame accelerations, yaw rate, how much heading the
    vehicle accumulated over a short window, and how far it drifted sideways from
    the straight path implied by its own heading at the start of a window. The
    last two are the map-free substitutes for "turned at the junction" and
    "changed lane": both are inferred from the vehicle's own pose history alone.

``TrackIndicators``
    Interaction geometry for each locally maintained radar track: range and range
    rate (radar sign convention -- **negative range rate means closing**),
    time-to-collision, the target's lateral position and lateral rate in the
    observer's body frame, the constant-velocity closest point of approach, the
    target's acceleration inferred from the range-rate history, and a *predicted
    path conflict* score.

The conflict score deserves a note, because it is the one place where the project
would be tempted to consult a map. :func:`infer_conflict` does not: it propagates
both parties' currently observed constant-velocity motion, intersects the two
predicted polylines, and asks whether both would arrive at the crossing at
roughly the same time. A conflict region is therefore a *hypothesis derived from
observed motion*, falsifiable from the same evidence, rather than a lookup in
privileged road topology.

Robustness note
---------------
Several recorded fields (``vx``/``vy``, ``accel_long``, ``rel_vx``/``rel_vy``,
``gvx``/``gvy``) are optional in the schema and default to ``0.0``. When a whole
series is identically zero we fall back to a finite-difference estimate from the
positions that *are* recorded, controlled by ``indicators.derived_fallback``.
This keeps the indicator layer honest (it never invents data) while remaining
usable with recorders that persist only poses.
"""

from __future__ import annotations

import bisect
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import ParticipantEvidence
from ..common.geometry import (
    angle_diff_deg,
    closest_approach,
    deg2rad,
    distance,
    global_to_body,
    polyline_intersection,
    predict_constant_velocity,
    time_to_collision_1d,
)

__all__ = [
    "OwnIndicators",
    "TrackIndicators",
    "compute_own_indicators",
    "compute_track_indicators",
    "infer_conflict",
    "cumulative_heading_change",
    "net_heading_change",
    "lateral_path_offset",
]


# ---------------------------------------------------------------------------
# Public records
# ---------------------------------------------------------------------------


@dataclass
class OwnIndicators:
    """Ego-behaviour indicators for one telemetry sample.

    One instance is produced per telemetry sample, in the same order, so callers
    may index ``OwnIndicators`` and ``ParticipantEvidence.telemetry`` in lockstep.
    """

    t: float
    frame: int
    speed: float
    """Ground speed, m/s."""
    accel_long: float
    """Longitudinal (body ``+x``) acceleration, m/s^2. Negative means braking."""
    accel_lat: float
    """Lateral (body ``+y``, i.e. rightwards) acceleration, m/s^2."""
    yaw_rate: float
    """Heading rate, deg/s."""
    heading_change_deg: float
    """Cumulative |heading change| over ``events.heading_change.window_s``.

    Accumulating the *absolute* per-step increments (rather than the net change)
    makes the quantity monotone in manoeuvre effort: a sustained turn and an
    out-and-back steering excursion both register, which is what the lane-change
    versus turn discrimination needs.
    """
    lateral_offset_m: float
    """Signed sideways displacement from the heading-aligned path, metres.

    The reference is the pose the vehicle held ``events.lane_change_like.window_s``
    seconds ago: the current position is expressed in that pose's body frame and
    the ``+y`` (rightwards) component is reported. Positive means the vehicle has
    moved to the right of the path it was following. No map lane is consulted.
    """
    throttle: float
    brake: float
    steer: float


@dataclass
class TrackIndicators:
    """Interaction indicators for one sample of one local radar track."""

    t: float
    frame: int
    track_id: str

    range_m: float
    range_rate: float
    """Radar sign convention: negative means closing."""
    ttc: Optional[float]
    """Range-rate time-to-collision, ``None`` when not closing or beyond
    ``indicators.ttc.max_reportable_s`` (no evidence, *not* "safe")."""

    lateral_offset_m: float
    """Target's lateral position in the observer body frame (``rel_y``)."""
    lateral_rate_mps: float
    """``d(rel_y)/dt``, estimated by central differences of the recorded offset."""
    longitudinal_m: float
    """Target's longitudinal position in the observer body frame (``rel_x``)."""

    t_cpa: Optional[float]
    """Time of closest approach under constant relative velocity, or ``None``."""
    d_cpa: float
    """Distance at closest approach, metres."""

    target_accel_long: float
    """Target acceleration along the line of sight, inferred from the range-rate
    history plus the observer's own acceleration (see
    :func:`compute_track_indicators`). Negative means the target is slowing."""

    conflict_score: float
    """Predicted-path conflict score in ``[0, 1]`` (see :func:`infer_conflict`)."""
    conflict_x: Optional[float]
    """Inferred conflict point, global frame. ``None`` when no conflict."""
    conflict_y: Optional[float]


# ---------------------------------------------------------------------------
# Small numeric helpers
# ---------------------------------------------------------------------------


def _central_difference(times: Sequence[float], values: Sequence[float]) -> List[float]:
    """Central-difference derivative, one-sided at the ends.

    Central differences are used rather than backward differences because event
    onsets are timestamped from these series: a backward difference would bias
    every onset half a sample late.
    """
    n = len(values)
    out = [0.0] * n
    if n < 2:
        return out
    for i in range(n):
        lo = max(0, i - 1)
        hi = min(n - 1, i + 1)
        dt = float(times[hi]) - float(times[lo])
        if abs(dt) <= 1e-9:
            out[i] = 0.0
        else:
            out[i] = (float(values[hi]) - float(values[lo])) / dt
    return out


def _central_difference_angle_deg(
    times: Sequence[float], angles_deg: Sequence[float]
) -> List[float]:
    """Central-difference derivative of an angle series, wrap-aware (deg/s)."""
    n = len(angles_deg)
    out = [0.0] * n
    if n < 2:
        return out
    for i in range(n):
        lo = max(0, i - 1)
        hi = min(n - 1, i + 1)
        dt = float(times[hi]) - float(times[lo])
        if abs(dt) <= 1e-9:
            out[i] = 0.0
        else:
            out[i] = angle_diff_deg(angles_deg[hi], angles_deg[lo]) / dt
    return out


def _effective(
    recorded: Sequence[float], derived: Sequence[float], enabled: bool
) -> List[float]:
    """Prefer the recorded series; fall back to ``derived`` when it is all zero.

    A recorder that persists only poses leaves the velocity/acceleration fields at
    their schema defaults. Rather than silently reporting zero motion we
    reconstruct the quantity from the positions that *were* recorded, and say so
    in the module docstring. Fallback can be disabled to audit a recorder.
    """
    if not enabled:
        return [float(v) for v in recorded]
    for v in recorded:
        if abs(float(v)) > 1e-9:
            return [float(x) for x in recorded]
    return [float(x) for x in derived]


def _window_start_index(times: Sequence[float], i: int, window_s: float) -> int:
    """Index of the first sample no older than ``window_s`` before ``times[i]``."""
    return bisect.bisect_left(times, float(times[i]) - float(window_s))


def _nearest_index(
    times: Sequence[float], t: float, max_gap: float
) -> Optional[int]:
    """Index of the sample nearest ``t``, or ``None`` when none is within ``max_gap``."""
    if not times:
        return None
    i = bisect.bisect_left(times, float(t))
    best: Optional[int] = None
    best_d = float("inf")
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(times):
            d = abs(float(times[j]) - float(t))
            if d < best_d:
                best, best_d = j, d
    if best is None or best_d > float(max_gap):
        return None
    return best


# ---------------------------------------------------------------------------
# Public window helpers (shared with the event extractor)
# ---------------------------------------------------------------------------


def cumulative_heading_change(
    times: Sequence[float], yaw_deg: Sequence[float], window_s: float
) -> List[float]:
    """Cumulative absolute heading change over a trailing window, per sample.

    Exposed publicly because the event extractor needs the same quantity over a
    *different* window (the lane-change window) than the one stored on
    :class:`OwnIndicators`; duplicating the computation would risk the two
    drifting apart.
    """
    n = len(times)
    if n == 0:
        return []
    prefix = [0.0] * n
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + abs(angle_diff_deg(yaw_deg[i], yaw_deg[i - 1]))
    out: List[float] = []
    for i in range(n):
        j = _window_start_index(times, i, window_s)
        out.append(prefix[i] - prefix[j])
    return out


def net_heading_change(
    times: Sequence[float], yaw_deg: Sequence[float], window_s: float
) -> List[float]:
    """Absolute *net* heading change over a trailing window, per sample.

    Together with :func:`cumulative_heading_change` this separates the two ways a
    vehicle can accumulate heading: a turn spends all of its cumulative change on
    a net change, whereas a lane change spends it on an out-and-back excursion
    that nets out to roughly zero. That contrast is the map-free replacement for
    "did it change lane or take the junction?".
    """
    out: List[float] = []
    for i in range(len(times)):
        j = _window_start_index(times, i, window_s)
        out.append(abs(angle_diff_deg(yaw_deg[i], yaw_deg[j])))
    return out


def lateral_path_offset(
    times: Sequence[float],
    xs: Sequence[float],
    ys: Sequence[float],
    yaw_deg: Sequence[float],
    window_s: float,
) -> List[float]:
    """Signed lateral drift from the heading-aligned path, per sample.

    For each sample the pose held ``window_s`` seconds earlier defines a frame;
    the current position expressed in that frame has a ``+y`` (rightwards)
    component which is exactly "how far sideways the vehicle has moved relative
    to where it was pointing". This is the map-free lane-change observable.
    """
    n = len(times)
    out: List[float] = []
    for i in range(n):
        j = _window_start_index(times, i, window_s)
        _fwd, lat = global_to_body(xs[i], ys[i], xs[j], ys[j], yaw_deg[j])
        out.append(float(lat))
    return out


# ---------------------------------------------------------------------------
# Ego state assembly
# ---------------------------------------------------------------------------


@dataclass
class _OwnState:
    """Column-oriented view of a participant's own telemetry, gaps filled in.

    Kept private: it exists so that :func:`compute_own_indicators` and
    :func:`compute_track_indicators` derive the ego kinematics exactly once and
    in exactly the same way.
    """

    times: List[float]
    frames: List[int]
    x: List[float]
    y: List[float]
    yaw: List[float]
    speed: List[float]
    vx: List[float]
    vy: List[float]
    accel_long: List[float]
    accel_lat: List[float]
    yaw_rate: List[float]


def _build_own_state(ev: ParticipantEvidence, cfg: Config) -> _OwnState:
    """Assemble the ego kinematic columns, reconstructing unrecorded derivatives."""
    fallback = bool(cfg.get("indicators.derived_fallback", True))

    times = [float(s.t) for s in ev.telemetry]
    frames = [int(s.frame) for s in ev.telemetry]
    xs = [float(s.x) for s in ev.telemetry]
    ys = [float(s.y) for s in ev.telemetry]
    yaw = [float(s.yaw) for s in ev.telemetry]

    vx = _effective(
        [float(s.vx) for s in ev.telemetry], _central_difference(times, xs), fallback
    )
    vy = _effective(
        [float(s.vy) for s in ev.telemetry], _central_difference(times, ys), fallback
    )
    speed = _effective(
        [float(s.speed) for s in ev.telemetry],
        [math.hypot(vx[i], vy[i]) for i in range(len(times))],
        fallback,
    )
    yaw_rate = _effective(
        [float(s.yaw_rate) for s in ev.telemetry],
        _central_difference_angle_deg(times, yaw),
        fallback,
    )
    accel_long = _effective(
        [float(s.accel_long) for s in ev.telemetry],
        _central_difference(times, speed),
        fallback,
    )
    # Lateral acceleration of a planar rigid body in steady turning is v * omega;
    # that is the best estimate available when the recorder stored no IMU value.
    accel_lat = _effective(
        [float(s.accel_lat) for s in ev.telemetry],
        [speed[i] * deg2rad(yaw_rate[i]) for i in range(len(times))],
        fallback,
    )

    return _OwnState(
        times=times,
        frames=frames,
        x=xs,
        y=ys,
        yaw=yaw,
        speed=speed,
        vx=vx,
        vy=vy,
        accel_long=accel_long,
        accel_lat=accel_lat,
        yaw_rate=yaw_rate,
    )


# ---------------------------------------------------------------------------
# Own indicators
# ---------------------------------------------------------------------------


def compute_own_indicators(ev: ParticipantEvidence, cfg: Config) -> List[OwnIndicators]:
    """Derive ego-behaviour indicators, one per telemetry sample.

    Controls are joined by CARLA frame number when available (an exact join) and
    by nearest timestamp otherwise. A sample with no matching control record
    reports zero commands: that is what the recorder observed, and inventing a
    command would fabricate evidence.
    """
    st = _build_own_state(ev, cfg)
    if not st.times:
        return []

    hc_window = float(cfg.get("events.heading_change.window_s", 1.5))
    lc_window = float(cfg.get("events.lane_change_like.window_s", 3.0))
    max_gap = float(cfg.get("indicators.max_sync_gap_s", 0.15))

    heading_change = cumulative_heading_change(st.times, st.yaw, hc_window)
    lateral = lateral_path_offset(st.times, st.x, st.y, st.yaw, lc_window)

    by_frame = ev.controls_by_frame()

    out: List[OwnIndicators] = []
    for i, t in enumerate(st.times):
        ctrl = by_frame.get(st.frames[i])
        if ctrl is None:
            ctrl = ev.control_at(t, max_gap)
        out.append(
            OwnIndicators(
                t=float(t),
                frame=st.frames[i],
                speed=float(st.speed[i]),
                accel_long=float(st.accel_long[i]),
                accel_lat=float(st.accel_lat[i]),
                yaw_rate=float(st.yaw_rate[i]),
                heading_change_deg=float(heading_change[i]),
                lateral_offset_m=float(lateral[i]),
                throttle=float(ctrl.throttle) if ctrl is not None else 0.0,
                brake=float(ctrl.brake) if ctrl is not None else 0.0,
                steer=float(ctrl.steer) if ctrl is not None else 0.0,
            )
        )
    return out


# ---------------------------------------------------------------------------
# Predicted-path conflict inference (map-free)
# ---------------------------------------------------------------------------


def infer_conflict(
    own_x: float,
    own_y: float,
    own_vx: float,
    own_vy: float,
    tgt_x: float,
    tgt_y: float,
    tgt_vx: float,
    tgt_vy: float,
    cfg: Config,
) -> Tuple[float, Optional[Tuple[float, float]], Optional[float], Optional[float]]:
    """Infer a latent conflict between two observed motions, without any map.

    Both parties' current planar motion is extrapolated at constant velocity over
    ``indicators.conflict.prediction_horizon_s`` (sampled every
    ``indicators.conflict.prediction_step_s``) and the two predicted polylines are
    intersected. A crossing alone is not a conflict -- two vehicles may cross the
    same point minutes apart -- so the score is driven by the *arrival-time gap*:
    it is 1.0 for simultaneous arrival and decays linearly to 0 at
    ``indicators.conflict.max_arrival_gap_s``.

    A stationary party has no meaningful predicted path, so speeds below
    ``min_own_speed_mps`` / ``min_target_speed_mps`` yield a zero score rather
    than a spurious conflict.

    Returns
    -------
    ``(conflict_score, conflict_point_or_None, t_own_arrival, t_target_arrival)``
    with the score in ``[0, 1]`` and the point in the global frame.
    """
    horizon = float(cfg.get("indicators.conflict.prediction_horizon_s", 4.0))
    step = float(cfg.get("indicators.conflict.prediction_step_s", 0.2))
    min_own = float(cfg.get("indicators.conflict.min_own_speed_mps", 1.5))
    min_tgt = float(cfg.get("indicators.conflict.min_target_speed_mps", 1.5))
    max_gap = float(cfg.get("indicators.conflict.max_arrival_gap_s", 2.5))
    if step <= 0.0 or horizon <= 0.0:
        raise ValueError(
            "indicators.conflict prediction horizon/step must be positive "
            "(got horizon={0}, step={1})".format(horizon, step)
        )
    if max_gap <= 0.0:
        raise ValueError(
            "indicators.conflict.max_arrival_gap_s must be positive (got {0})".format(
                max_gap
            )
        )

    own_speed = math.hypot(float(own_vx), float(own_vy))
    tgt_speed = math.hypot(float(tgt_vx), float(tgt_vy))
    if own_speed < min_own or tgt_speed < min_tgt:
        return (0.0, None, None, None)

    path_own = predict_constant_velocity(own_x, own_y, own_vx, own_vy, horizon, step)
    path_tgt = predict_constant_velocity(tgt_x, tgt_y, tgt_vx, tgt_vy, horizon, step)

    # Both predictions are straight, so their endpoints bound them exactly: a
    # cheap rejection test keeps the O(n*m) polyline intersection off the hot path.
    if not _bbox_overlap(path_own[0], path_own[-1], path_tgt[0], path_tgt[-1]):
        return (0.0, None, None, None)

    hits = polyline_intersection(path_own, path_tgt)
    if not hits:
        return (0.0, None, None, None)

    best_key: Optional[Tuple[float, float]] = None
    best: Optional[Tuple[float, float, float, float]] = None
    for hx, hy, _i, _j in hits:
        t_own = distance(own_x, own_y, hx, hy) / own_speed
        t_tgt = distance(tgt_x, tgt_y, hx, hy) / tgt_speed
        gap = abs(t_own - t_tgt)
        # Deterministic pick: the conflict that materialises first, ties broken by
        # the tighter arrival gap.
        key = (max(t_own, t_tgt), gap)
        if best_key is None or key < best_key:
            best_key = key
            best = (float(hx), float(hy), float(t_own), float(t_tgt))

    if best is None:
        return (0.0, None, None, None)

    hx, hy, t_own, t_tgt = best
    score = 1.0 - abs(t_own - t_tgt) / max_gap
    score = max(0.0, min(1.0, score))
    return (float(score), (hx, hy), t_own, t_tgt)


def _bbox_overlap(
    a0: Sequence[float],
    a1: Sequence[float],
    b0: Sequence[float],
    b1: Sequence[float],
) -> bool:
    """Whether the axis-aligned bounds of segments ``a0a1`` and ``b0b1`` overlap."""
    if max(a0[0], a1[0]) < min(b0[0], b1[0]):
        return False
    if max(b0[0], b1[0]) < min(a0[0], a1[0]):
        return False
    if max(a0[1], a1[1]) < min(b0[1], b1[1]):
        return False
    if max(b0[1], b1[1]) < min(a0[1], a1[1]):
        return False
    return True


# ---------------------------------------------------------------------------
# Track indicators
# ---------------------------------------------------------------------------


def compute_track_indicators(
    ev: ParticipantEvidence, cfg: Config
) -> Dict[str, List[TrackIndicators]]:
    """Derive interaction indicators for every local radar track.

    Target acceleration is inferred rather than measured. Differentiating the
    range rate yields ``(a_target - a_own) . los``; adding back the observer's own
    acceleration projected on the line of sight recovers the target's own
    acceleration along that line. The approximation neglects rotation of the line
    of sight, which is second order for the short episodes the extractor cares
    about, and it uses only quantities the observer measured itself.

    Returns a mapping ``track_id -> indicators sorted by time``; track ids are
    visited in sorted order so the result is deterministic.
    """
    st = _build_own_state(ev, cfg)
    fallback = bool(cfg.get("indicators.derived_fallback", True))
    max_ttc = float(cfg.get("indicators.ttc.max_reportable_s", 12.0))
    max_gap = float(cfg.get("indicators.max_sync_gap_s", 0.15))

    out: Dict[str, List[TrackIndicators]] = {}
    for track_id, samples in sorted(ev.tracks_by_id().items()):
        times = [float(s.t) for s in samples]
        rel_x = [float(s.rel_x) for s in samples]
        rel_y = [float(s.rel_y) for s in samples]
        gx = [float(s.gx) for s in samples]
        gy = [float(s.gy) for s in samples]
        range_m = [float(s.range_m) for s in samples]
        range_rate = [float(s.range_rate) for s in samples]

        rel_vx = _effective(
            [float(s.rel_vx) for s in samples], _central_difference(times, rel_x), fallback
        )
        rel_vy = _effective(
            [float(s.rel_vy) for s in samples], _central_difference(times, rel_y), fallback
        )
        gvx = _effective(
            [float(s.gvx) for s in samples], _central_difference(times, gx), fallback
        )
        gvy = _effective(
            [float(s.gvy) for s in samples], _central_difference(times, gy), fallback
        )

        # The lateral rate is deliberately differentiated from the *recorded*
        # offset rather than read from the tracker's smoothed rel_vy: it is the
        # quantity an auditor can recompute from the persisted track file.
        lateral_rate = _central_difference(times, rel_y)
        d_range_rate = _central_difference(times, range_rate)

        series: List[TrackIndicators] = []
        for i, sample in enumerate(samples):
            j = _nearest_index(st.times, times[i], max_gap)

            bearing = math.atan2(rel_y[i], rel_x[i])
            if j is None:
                own_los_accel = 0.0
            else:
                own_los_accel = st.accel_long[j] * math.cos(bearing) + st.accel_lat[
                    j
                ] * math.sin(bearing)
            target_accel_long = d_range_rate[i] + own_los_accel

            ttc = time_to_collision_1d(range_m[i], range_rate[i])
            if ttc is not None and ttc > max_ttc:
                ttc = None

            t_cpa, d_cpa = closest_approach(rel_x[i], rel_y[i], rel_vx[i], rel_vy[i])

            if j is None:
                score, point = 0.0, None
            else:
                score, point, _t_own, _t_tgt = infer_conflict(
                    st.x[j],
                    st.y[j],
                    st.vx[j],
                    st.vy[j],
                    gx[i],
                    gy[i],
                    gvx[i],
                    gvy[i],
                    cfg,
                )

            series.append(
                TrackIndicators(
                    t=float(times[i]),
                    frame=int(sample.frame),
                    track_id=track_id,
                    range_m=float(range_m[i]),
                    range_rate=float(range_rate[i]),
                    ttc=ttc,
                    lateral_offset_m=float(rel_y[i]),
                    lateral_rate_mps=float(lateral_rate[i]),
                    longitudinal_m=float(rel_x[i]),
                    t_cpa=t_cpa,
                    d_cpa=float(d_cpa),
                    target_accel_long=float(target_accel_long),
                    conflict_score=float(score),
                    conflict_x=None if point is None else float(point[0]),
                    conflict_y=None if point is None else float(point[1]),
                )
            )
        out[track_id] = series
    return out
