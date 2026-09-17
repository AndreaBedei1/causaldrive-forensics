"""Unit tests for the radar tracker (:mod:`cdf.local.tracking`).

Every scenario here is driven by an analytically known target trajectory, so the
assertions are numeric statements about the estimator (does the range converge to
the truth? does TTC fall as the gap closes?) and structural statements about
identity (one object -> one id; crossing objects -> no swap; a lost object ->
a *new* id, never a recycled one).

The head-on case is driven end to end through :class:`cdf.local.radar.RadarFrontEnd`
from synthesised polar returns, so the transform chain and the tracker are
exercised together exactly as they are in the pipeline.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Sequence, Tuple

import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.geometry import global_to_body, rotate2d
from cdf.common.schemas import RadarDetection, RadarFrame, TelemetrySample
from cdf.local.radar import RadarCluster, RadarFrontEnd
from cdf.local.tracking import RadarTracker

PARTICIPANT = "A"
DT = 0.05
MOUNT_X = 2.2
MOUNT_Z = 1.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _config() -> Config:
    return load_run_config(sensor_profile="radar_baseline")


def _telemetry(
    t: float,
    frame: int,
    x: float,
    y: float,
    yaw: float = 0.0,
    vx: float = 0.0,
    vy: float = 0.0,
) -> TelemetrySample:
    return TelemetrySample(
        t=t,
        frame=frame,
        participant_id=PARTICIPANT,
        x=x,
        y=y,
        z=0.0,
        yaw=yaw,
        vx=vx,
        vy=vy,
        speed=math.hypot(vx, vy),
    )


def _cluster_from_truth(
    t: float,
    frame: int,
    own: TelemetrySample,
    target_xy: Tuple[float, float],
    target_v: Tuple[float, float],
    n_points: int = 6,
) -> RadarCluster:
    """A noise-free cluster measurement of a target with known state.

    Only quantities an onboard radar could produce are filled in; they are
    derived from the observer's own pose/velocity and the target's position, the
    same composition the real front-end performs.
    """
    rel_x, rel_y = global_to_body(
        target_xy[0], target_xy[1], own.x, own.y, own.yaw
    )
    range_m = math.hypot(rel_x, rel_y)
    rel_vx, rel_vy = rotate2d(
        target_v[0] - own.vx, target_v[1] - own.vy, -own.yaw
    )
    range_rate = (rel_x * rel_vx + rel_y * rel_vy) / range_m
    return RadarCluster(
        t=t,
        frame=frame,
        participant_id=PARTICIPANT,
        sensor_id="front",
        rel_x=rel_x,
        rel_y=rel_y,
        gx=target_xy[0],
        gy=target_xy[1],
        range_m=range_m,
        azimuth_rad=math.atan2(rel_y, rel_x),
        range_rate=range_rate,
        n_points=n_points,
        extent_x=1.8,
        extent_y=1.6,
        quality=0.9,
    )


#: Six returns from the corners and flanks of a car-sized body. The pattern is
#: symmetric, so its centroid is exactly the nominal target position.
_CAR_RETURNS: Sequence[Tuple[float, float]] = (
    (-1.8, -0.8),
    (-1.8, 0.8),
    (0.0, -0.9),
    (0.0, 0.9),
    (1.8, -0.8),
    (1.8, 0.8),
)


def _radar_frame_for_target(
    t: float,
    frame_no: int,
    own: TelemetrySample,
    target_xy: Tuple[float, float],
    target_v: Tuple[float, float],
    rng: random.Random,
    jitter: float = 0.10,
) -> RadarFrame:
    """Synthesise the polar returns a front radar would report for one target."""
    frame = RadarFrame(
        t=t,
        frame=frame_no,
        participant_id=PARTICIPANT,
        sensor_id="front",
        detections=[],
        sensor_yaw=0.0,
        sensor_x=MOUNT_X,
        sensor_y=0.0,
        sensor_z=MOUNT_Z,
    )
    base_x, base_y = global_to_body(
        target_xy[0], target_xy[1], own.x, own.y, own.yaw
    )
    vrel_x, vrel_y = rotate2d(
        target_v[0] - own.vx, target_v[1] - own.vy, -own.yaw
    )

    detections: List[RadarDetection] = []
    for dx, dy in _CAR_RETURNS:
        bx = base_x + dx + rng.uniform(-jitter, jitter)
        by = base_y + dy + rng.uniform(-jitter, jitter)
        bz = MOUNT_Z + rng.uniform(-0.15, 0.15)
        sx = bx - frame.sensor_x
        sy = by - frame.sensor_y
        sz = bz - frame.sensor_z
        depth = math.sqrt(sx * sx + sy * sy + sz * sz)
        radial = (sx * vrel_x + sy * vrel_y) / depth
        detections.append(
            RadarDetection(
                depth=depth,
                azimuth=math.atan2(sy, sx),
                altitude=math.asin(sz / depth),
                velocity=radial,
            )
        )
    frame.detections = detections
    return frame


# ---------------------------------------------------------------------------
# Head-on approach: one stable track, converging range, falling TTC
# ---------------------------------------------------------------------------


def test_head_on_approach_yields_one_stable_track_with_falling_ttc() -> None:
    """A 14 m/s closing geometry must produce exactly one confirmed track."""
    cfg = _config()
    front_end = RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0))
    tracker = RadarTracker(cfg, PARTICIPANT)
    synth_rng = random.Random(1234)

    own_speed = 6.0
    target_speed = 8.0
    closing = own_speed + target_speed

    all_samples: List = []
    for k in range(1, 41):
        t = DT * k
        own = _telemetry(
            t=t, frame=k, x=own_speed * t, y=0.0, yaw=0.0, vx=own_speed, vy=0.0
        )
        target_xy = (60.0 - target_speed * t, 0.3)
        frame = _radar_frame_for_target(
            t, k, own, target_xy, (-target_speed, 0.0), synth_rng
        )
        clusters = front_end.process(frame, own)
        assert len(clusters) == 1, "the car body must yield exactly one cluster"
        all_samples.extend(tracker.update(t, k, clusters, own))

    ids = {s.track_id for s in all_samples}
    assert ids == {"A::T001"}
    # confirmation needs 3 hits, so 38 of the 40 frames must report.
    assert len(all_samples) == 38
    assert len(tracker.active_tracks) == 1
    assert tracker.active_tracks[0].confirmed

    # Truth: range starts at 60 m and shrinks by 14 m/s for 2 s. The estimate
    # must track it, not merely trend in the right direction.
    final_truth = 60.0 - closing * (DT * 40)
    assert all_samples[-1].range_m == pytest.approx(final_truth, abs=0.25)
    worst_error = max(abs(s.range_m - (60.0 - closing * s.t)) for s in all_samples)
    assert worst_error < 0.35

    ranges = [s.range_m for s in all_samples]
    assert ranges[0] > ranges[-1]
    decreasing = sum(1 for a, b in zip(ranges, ranges[1:]) if b < a)
    assert decreasing >= len(ranges) - 2

    # Measured range rate is the closing speed, negative by radar convention.
    assert all(s.range_rate < 0.0 for s in all_samples)
    assert all_samples[-1].range_rate == pytest.approx(-closing, abs=0.2)

    ttcs = [s.ttc for s in all_samples]
    assert all(v is not None and math.isfinite(v) and v > 0.0 for v in ttcs)
    assert ttcs[0] > ttcs[-1]
    assert ttcs[-1] == pytest.approx(final_truth / closing, abs=0.05)
    falling = sum(1 for a, b in zip(ttcs, ttcs[1:]) if b < a)
    assert falling >= len(ttcs) - 3

    # The estimated global velocity must converge to the true target velocity.
    assert all_samples[-1].gvx == pytest.approx(-target_speed, abs=0.5)
    assert abs(all_samples[-1].gvy) < 0.5


def test_receding_target_has_no_ttc_and_positive_range_rate() -> None:
    """The sign convention must survive the whole chain: receding => no TTC."""
    cfg = _config()
    tracker = RadarTracker(cfg, PARTICIPANT)
    samples: List = []
    for k in range(1, 21):
        t = DT * k
        own = _telemetry(t=t, frame=k, x=0.0, y=0.0, yaw=0.0)
        target_xy = (25.0 + 7.0 * t, 0.0)
        cluster = _cluster_from_truth(t, k, own, target_xy, (7.0, 0.0))
        samples.extend(tracker.update(t, k, [cluster], own))

    assert samples
    assert all(s.range_rate > 0.0 for s in samples)
    assert all(s.ttc is None for s in samples)


# ---------------------------------------------------------------------------
# Identity under crossing traffic
# ---------------------------------------------------------------------------


def test_crossing_targets_do_not_swap_track_ids() -> None:
    """Two objects whose paths cross within the gate must keep their identities.

    The first target's returns are additionally dropped for the two frames around
    the crossing. That is the case a per-track greedy nearest-neighbour gets
    wrong: the surviving cluster is inside the *other* track's gate, so a greedy
    matcher steals it and permanently swaps the two identities.
    """
    cfg = _config()
    tracker = RadarTracker(cfg, PARTICIPANT)

    def target_a(t: float) -> Tuple[float, float]:
        return (10.0 + 10.0 * t, 0.0)

    def target_b(t: float) -> Tuple[float, float]:
        return (22.0, -12.0 + 12.0 * t)

    occluded_frames = (20, 21)
    per_track: Dict[str, List] = {}
    min_separation = 1e9
    for k in range(1, 41):
        t = DT * k
        own = _telemetry(t=t, frame=k, x=0.0, y=0.0, yaw=0.0)
        a_xy, b_xy = target_a(t), target_b(t)
        min_separation = min(
            min_separation, math.hypot(a_xy[0] - b_xy[0], a_xy[1] - b_xy[1])
        )
        clusters = []
        if k not in occluded_frames:
            # First in the list, therefore the older track: a greedy matcher
            # iterating tracks in order is the one that would steal here.
            clusters.append(_cluster_from_truth(t, k, own, a_xy, (10.0, 0.0)))
        clusters.append(_cluster_from_truth(t, k, own, b_xy, (0.0, 12.0)))
        if k % 2 == 0:  # the tracker must not depend on cluster ordering
            clusters.reverse()
        for sample in tracker.update(t, k, clusters, own):
            per_track.setdefault(sample.track_id, []).append(sample)

    # The scenario really is ambiguous: the two objects pass within the gate.
    assert min_separation < float(cfg.get("radar_processing.tracking.gate_m"))
    assert len(per_track) == 2
    assert len(tracker.active_tracks) == 2

    for samples in per_track.values():
        first, last = samples[0], samples[-1]
        if abs(first.gy) < 1.0:  # the along-x traveller
            assert last.gx > first.gx + 10.0
            assert abs(last.gy - 0.0) < 1.0
            assert last.gx == pytest.approx(target_a(DT * 40)[0], abs=0.6)
        else:  # the along-y traveller, which entered from y < 0
            assert first.gy < -9.0
            assert last.gy > 9.0
            assert abs(last.gx - 22.0) < 1.0
            assert last.gy == pytest.approx(target_b(DT * 40)[1], abs=0.6)

        # A swap would appear as a discontinuity far larger than the fastest
        # motion either object can achieve between two reported samples.
        for prev, cur in zip(samples, samples[1:]):
            step = math.hypot(cur.gx - prev.gx, cur.gy - prev.gy)
            assert step < 12.0 * (cur.t - prev.t) + 0.3


# ---------------------------------------------------------------------------
# Loss, drop and re-acquisition
# ---------------------------------------------------------------------------


def test_lost_track_is_dropped_after_max_misses_and_reacquired_with_a_new_id() -> None:
    """Ids are never recycled: a re-acquired object is a new hypothesis."""
    cfg = _config()
    max_misses = int(cfg.get("radar_processing.tracking.max_misses"))
    tracker = RadarTracker(cfg, PARTICIPANT)

    def target_xy(t: float) -> Tuple[float, float]:
        return (50.0 - 10.0 * t, 0.5)

    frame_no = 0
    first_ids = set()
    for _ in range(6):
        frame_no += 1
        t = DT * frame_no
        own = _telemetry(t=t, frame=frame_no, x=0.0, y=0.0, yaw=0.0)
        cluster = _cluster_from_truth(t, frame_no, own, target_xy(t), (-10.0, 0.0))
        for s in tracker.update(t, frame_no, [cluster], own):
            first_ids.add(s.track_id)

    assert first_ids == {"A::T001"}
    assert tracker.active_tracks[0].confirmed

    # One miss short of the drop threshold the hypothesis must still be alive.
    for _ in range(max_misses - 1):
        frame_no += 1
        t = DT * frame_no
        own = _telemetry(t=t, frame=frame_no, x=0.0, y=0.0, yaw=0.0)
        assert tracker.update(t, frame_no, [], own) == []
    assert len(tracker.active_tracks) == 1
    assert tracker.active_tracks[0].misses == max_misses - 1

    # The next miss drops it.
    frame_no += 1
    t = DT * frame_no
    own = _telemetry(t=t, frame=frame_no, x=0.0, y=0.0, yaw=0.0)
    assert tracker.update(t, frame_no, [], own) == []
    assert tracker.active_tracks == []

    # Re-acquisition: a brand new id, and the old one is never reused.
    second_ids = set()
    for _ in range(5):
        frame_no += 1
        t = DT * frame_no
        own = _telemetry(t=t, frame=frame_no, x=0.0, y=0.0, yaw=0.0)
        cluster = _cluster_from_truth(t, frame_no, own, target_xy(t), (-10.0, 0.0))
        for s in tracker.update(t, frame_no, [cluster], own):
            second_ids.add(s.track_id)

    assert second_ids == {"A::T002"}
    assert not (first_ids & second_ids)


def test_single_dropped_frame_does_not_break_a_track() -> None:
    """Coasting is the point of max_misses > 1: one dropout must be survivable."""
    cfg = _config()
    tracker = RadarTracker(cfg, PARTICIPANT)
    ids = set()
    for k in range(1, 21):
        t = DT * k
        own = _telemetry(t=t, frame=k, x=0.0, y=0.0, yaw=0.0)
        target = (45.0 - 10.0 * t, 0.0)
        clusters = (
            []
            if k in (8, 14)
            else [_cluster_from_truth(t, k, own, target, (-10.0, 0.0))]
        )
        for s in tracker.update(t, k, clusters, own):
            ids.add(s.track_id)

    assert ids == {"A::T001"}
    assert len(tracker.active_tracks) == 1
    # The coasted frames still advanced the state to the right place.
    assert tracker.active_tracks[0].range_m == pytest.approx(45.0 - 10.0, abs=0.8)


# ---------------------------------------------------------------------------
# Confirmation, capacity and relative velocity
# ---------------------------------------------------------------------------


def test_confirmation_requires_min_hits_and_confidence() -> None:
    cfg = _config()
    min_hits = int(cfg.get("radar_processing.tracking.min_hits_to_confirm"))
    hit_gain = float(cfg.get("radar_processing.tracking.confidence.hit_gain"))
    tracker = RadarTracker(cfg, PARTICIPANT)

    emitted: List[int] = []
    for k in range(1, min_hits + 3):
        t = DT * k
        own = _telemetry(t=t, frame=k, x=0.0, y=0.0, yaw=0.0)
        cluster = _cluster_from_truth(
            t, k, own, (30.0 - 5.0 * t, 0.0), (-5.0, 0.0)
        )
        emitted.append(len(tracker.update(t, k, [cluster], own)))

    assert emitted[: min_hits - 1] == [0] * (min_hits - 1)
    assert all(n == 1 for n in emitted[min_hits - 1 :])
    track = tracker.active_tracks[0]
    assert track.confirmed
    assert track.hits == min_hits + 2
    assert track.confidence == pytest.approx(min(1.0, hit_gain * (min_hits + 2)))


def test_capacity_cap_evicts_the_least_confident_tracks() -> None:
    cfg = _config().with_overrides({"radar_processing": {"tracking": {"max_tracks": 3}}})
    tracker = RadarTracker(cfg, PARTICIPANT)

    established = [(30.0, -8.0), (30.0, 8.0)]
    newcomers = [(45.0, -6.0), (45.0, 0.0), (45.0, 6.0)]

    for k in range(1, 4):
        t = DT * k
        own = _telemetry(t=t, frame=k, x=0.0, y=0.0, yaw=0.0)
        clusters = [
            _cluster_from_truth(t, k, own, xy, (0.0, 0.0)) for xy in established
        ]
        tracker.update(t, k, clusters, own)
    assert len(tracker.active_tracks) == 2

    t = DT * 4
    own = _telemetry(t=t, frame=4, x=0.0, y=0.0, yaw=0.0)
    clusters = [
        _cluster_from_truth(t, 4, own, xy, (0.0, 0.0))
        for xy in established + newcomers
    ]
    tracker.update(t, 4, clusters, own)

    alive = tracker.active_tracks
    assert len(alive) == 3
    # The two established (high-confidence) tracks survive; of the three equal
    # newcomers the oldest wins the tie.
    assert [tr.track_id for tr in alive] == ["A::T001", "A::T002", "A::T003"]
    assert alive[0].confidence > alive[2].confidence


def test_relative_velocity_is_expressed_in_the_observer_body_frame() -> None:
    """A yawed, moving observer must report rel_v in its own body axes."""
    cfg = _config()
    tracker = RadarTracker(cfg, PARTICIPANT)

    own_vy = 5.0
    target_vy = 9.0
    samples: List = []
    for k in range(1, 61):
        t = DT * k
        own = _telemetry(
            t=t,
            frame=k,
            x=10.0,
            y=20.0 + own_vy * t,
            yaw=90.0,  # heading along +y in CARLA's left-handed frame
            vx=0.0,
            vy=own_vy,
        )
        target_xy = (10.0, 60.0 + target_vy * t)
        cluster = _cluster_from_truth(t, k, own, target_xy, (0.0, target_vy))
        samples.extend(tracker.update(t, k, [cluster], own))

    last = samples[-1]
    # Global relative velocity (0, +4) rotated into a body frame heading +y is
    # purely longitudinal: the target pulls away straight ahead.
    assert last.gvx == pytest.approx(0.0, abs=0.3)
    assert last.gvy == pytest.approx(target_vy, abs=0.3)
    assert last.rel_vx == pytest.approx(target_vy - own_vy, abs=0.3)
    assert last.rel_vy == pytest.approx(0.0, abs=0.3)
    assert last.rel_y == pytest.approx(0.0, abs=0.2)
    assert last.rel_x > 0.0
    assert last.range_rate == pytest.approx(target_vy - own_vy, abs=0.3)
    assert last.ttc is None


def test_tracker_rejects_another_participants_evidence() -> None:
    cfg = _config()
    tracker = RadarTracker(cfg, PARTICIPANT)
    own = _telemetry(t=DT, frame=1, x=0.0, y=0.0, yaw=0.0)
    cluster = _cluster_from_truth(DT, 1, own, (20.0, 0.0), (0.0, 0.0))

    foreign_own = _telemetry(t=DT, frame=1, x=0.0, y=0.0, yaw=0.0)
    foreign_own.participant_id = "B"
    with pytest.raises(ValueError):
        tracker.update(DT, 1, [cluster], foreign_own)

    foreign_cluster = _cluster_from_truth(DT, 1, own, (20.0, 0.0), (0.0, 0.0))
    foreign_cluster.participant_id = "B"
    with pytest.raises(ValueError):
        tracker.update(DT, 1, [foreign_cluster], own)


def test_tracker_rejects_time_going_backwards() -> None:
    """A non-monotone timestamp is a wiring bug and must not be smoothed over."""
    cfg = _config()
    tracker = RadarTracker(cfg, PARTICIPANT)
    own = _telemetry(t=1.0, frame=20, x=0.0, y=0.0, yaw=0.0)
    tracker.update(1.0, 20, [_cluster_from_truth(1.0, 20, own, (20.0, 0.0), (0.0, 0.0))], own)
    earlier = _telemetry(t=0.5, frame=10, x=0.0, y=0.0, yaw=0.0)
    with pytest.raises(ValueError):
        tracker.update(0.5, 10, [], earlier)


def test_time_monotonicity_survives_an_empty_track_list() -> None:
    """Out-of-order frames must be rejected even when no hypothesis is alive.

    Adversarial case for the obvious implementation of the monotonicity guard:
    deriving ``dt`` per track and raising there means the guard is only armed
    while at least one track exists. After every hypothesis has been dropped --
    which is exactly what a long occlusion or a sensor outage produces -- an
    out-of-order frame would then be swallowed silently and would spawn tracks
    stamped with a time earlier than samples already emitted, corrupting the
    ordering of the evidence the whole causal layer is built on.

    The assertions also pin down that the rejection happens *before* any state
    change: no track is created and, decisively, the id counter is not consumed,
    so the next legitimate frame still gets the id it was owed.
    """
    cfg = _config()
    max_misses = int(cfg.get("radar_processing.tracking.max_misses"))
    tracker = RadarTracker(cfg, PARTICIPANT)

    def observe(t: float, frame: int, target: Tuple[float, float]) -> List:
        own = _telemetry(t=t, frame=frame, x=0.0, y=0.0, yaw=0.0)
        cluster = _cluster_from_truth(t, frame, own, target, (0.0, 0.0))
        return tracker.update(t, frame, [cluster], own)

    # Establish and confirm one track.
    ids = set()
    for k in range(1, 6):
        for sample in observe(1.0 + DT * k, k, (25.0, 0.0)):
            ids.add(sample.track_id)
    assert ids == {"A::T001"}

    # Starve it until the tracker holds nothing at all.
    frame_no = 5
    for _ in range(max_misses):
        frame_no += 1
        t = 1.0 + DT * frame_no
        tracker.update(t, frame_no, [], _telemetry(t=t, frame=frame_no, x=0.0, y=0.0))
    assert tracker.active_tracks == []
    last_good_t = 1.0 + DT * frame_no

    # An earlier timestamp is a wiring bug and must fail loudly even now.
    with pytest.raises(ValueError):
        observe(last_good_t - 0.5, 1, (25.0, 0.0))
    # ...and must have changed nothing on the way out.
    assert tracker.active_tracks == []

    # A repeated timestamp is legitimate (two sensors on the same tick) and must
    # still be accepted -- the guard must not have been over-tightened into a
    # strict-increase rule.
    frame_no += 1
    observe(last_good_t, frame_no, (25.0, 0.0))
    assert [tr.track_id for tr in tracker.active_tracks] == ["A::T002"]
