"""Unit tests for the radar front-end (:mod:`cdf.local.radar`).

The tests are built from *inverted* ground truth: a target is placed at a known
body-frame or global position, the corresponding polar returns are synthesised by
inverting :func:`cdf.common.geometry.polar_to_body`, and the front-end is then
required to recover the original quantity. That makes every assertion a numeric
statement about the transform chain rather than a smoke test.
"""

from __future__ import annotations

import math
import random
from typing import List, Sequence, Tuple

import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.geometry import body_to_global, rotate2d
from cdf.common.schemas import RadarDetection, RadarFrame, TelemetrySample
from cdf.local.radar import (
    RadarFrontEnd,
    apply_degradation,
    cluster_points,
    filter_detections,
)

PARTICIPANT = "A"
MOUNT_X = 2.2
MOUNT_Z = 1.0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _config() -> Config:
    """The real resolved configuration (default.yaml + baseline radar profile)."""
    return load_run_config(sensor_profile="radar_baseline")


def _empty_frame(t: float = 0.0, frame: int = 10, sensor_yaw: float = 0.0) -> RadarFrame:
    return RadarFrame(
        t=t,
        frame=frame,
        participant_id=PARTICIPANT,
        sensor_id="front",
        detections=[],
        sensor_yaw=sensor_yaw,
        sensor_x=MOUNT_X,
        sensor_y=0.0,
        sensor_z=MOUNT_Z,
    )


def _telemetry(
    x: float, y: float, yaw: float, t: float = 0.0, frame: int = 10
) -> TelemetrySample:
    return TelemetrySample(
        t=t, frame=frame, participant_id=PARTICIPANT, x=x, y=y, z=0.0, yaw=yaw
    )


def _detection_from_body(
    bx: float, by: float, bz: float, velocity: float, frame: RadarFrame
) -> RadarDetection:
    """Invert :func:`polar_to_body`: body-frame point -> polar radar return."""
    sx, sy = rotate2d(bx - frame.sensor_x, by - frame.sensor_y, -frame.sensor_yaw)
    sz = bz - frame.sensor_z
    depth = math.sqrt(sx * sx + sy * sy + sz * sz)
    return RadarDetection(
        depth=depth,
        azimuth=math.atan2(sy, sx),
        altitude=math.asin(sz / depth) if depth > 0.0 else 0.0,
        velocity=velocity,
    )


#: Symmetric blob whose centroid is exactly the nominal target position, so that
#: an exact transform chain must reproduce the target position exactly.
_BLOB: Sequence[Tuple[float, float]] = (
    (0.0, 0.0),
    (0.4, 0.0),
    (-0.4, 0.0),
    (0.0, 0.4),
    (0.0, -0.4),
)


def _blob_detections(
    bx: float, by: float, frame: RadarFrame, velocity: float = -8.0
) -> List[RadarDetection]:
    return [
        _detection_from_body(bx + dx, by + dy, MOUNT_Z, velocity, frame)
        for dx, dy in _BLOB
    ]


# ---------------------------------------------------------------------------
# polar -> body -> global round trip
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("yaw", [0.0, 90.0, 180.0, -90.0])
def test_polar_to_global_round_trip_recovers_target_position(yaw: float) -> None:
    """A target at a known global position is recovered to well under 0.1 m."""
    cfg = _config()
    own = _telemetry(x=12.0, y=-7.5, yaw=yaw)
    front_end = RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0))

    true_rel = (30.0, 3.0)  # 30 m ahead, 3 m to the right of the observer
    true_gx, true_gy = body_to_global(
        true_rel[0], true_rel[1], own.x, own.y, own.yaw
    )

    frame = _empty_frame()
    frame.detections = _blob_detections(true_rel[0], true_rel[1], frame)

    clusters = front_end.process(frame, own)

    assert len(clusters) == 1
    cluster = clusters[0]
    # The pipeline requirement is 0.1 m; the transform chain is in fact exact up
    # to floating point, so anything above 1e-6 indicates a real defect.
    assert math.hypot(cluster.gx - true_gx, cluster.gy - true_gy) < 1e-6
    assert abs(cluster.rel_x - true_rel[0]) < 1e-6
    assert abs(cluster.rel_y - true_rel[1]) < 1e-6
    # range/azimuth must agree with the body-frame centroid they describe.
    assert cluster.range_m == pytest.approx(math.hypot(*true_rel), abs=1e-6)
    assert cluster.azimuth_rad == pytest.approx(
        math.atan2(true_rel[1], true_rel[0]), abs=1e-9
    )
    assert cluster.range_rate == pytest.approx(-8.0, abs=1e-9)
    assert cluster.n_points == len(_BLOB)


def test_round_trip_is_actually_yaw_dependent() -> None:
    """Guard against a transform that ignores the observer heading entirely."""
    cfg = _config()
    positions = []
    for yaw in (0.0, 90.0, 180.0, -90.0):
        own = _telemetry(x=12.0, y=-7.5, yaw=yaw)
        front_end = RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0))
        frame = _empty_frame()
        frame.detections = _blob_detections(30.0, 3.0, frame)
        cluster = front_end.process(frame, own)[0]
        positions.append((round(cluster.gx, 3), round(cluster.gy, 3)))
    assert len(set(positions)) == 4


def test_sensor_yaw_extrinsic_is_applied() -> None:
    """A yawed sensor mounting must not shift the recovered global position."""
    cfg = _config()
    own = _telemetry(x=0.0, y=0.0, yaw=0.0)
    true_rel = (20.0, -6.0)

    seen = []
    for sensor_yaw in (0.0, -20.0, 25.0):
        frame = _empty_frame(sensor_yaw=sensor_yaw)
        frame.detections = _blob_detections(true_rel[0], true_rel[1], frame)
        front_end = RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0))
        cluster = front_end.process(frame, own)[0]
        seen.append((cluster.gx, cluster.gy))

    for gx, gy in seen:
        assert math.hypot(gx - true_rel[0], gy - true_rel[1]) < 1e-6


# ---------------------------------------------------------------------------
# Plausibility filtering
# ---------------------------------------------------------------------------


def test_filter_detections_rejects_implausible_returns() -> None:
    """The three real-world artifacts are removed and the valid return survives."""
    cfg = _config()
    valid = RadarDetection(depth=30.0, azimuth=0.10, altitude=0.0, velocity=-8.0)
    first_frame_artifact = RadarDetection(
        depth=5.0, azimuth=0.0, altitude=0.0, velocity=-100.0
    )
    too_far = RadarDetection(depth=140.0, azimuth=0.0, altitude=0.0, velocity=-8.0)
    too_near = RadarDetection(depth=0.4, azimuth=0.0, altitude=0.0, velocity=-1.0)
    road_surface = RadarDetection(depth=12.0, azimuth=0.0, altitude=-0.5, velocity=-8.0)
    above_band = RadarDetection(depth=12.0, azimuth=0.0, altitude=0.9, velocity=-8.0)
    out_of_fov = RadarDetection(depth=12.0, azimuth=1.5, altitude=0.0, velocity=-8.0)

    kept = filter_detections(
        [
            first_frame_artifact,
            too_far,
            valid,
            too_near,
            road_surface,
            above_band,
            out_of_fov,
        ],
        cfg,
    )

    assert kept == [valid]


def test_filter_detections_keeps_a_realistic_clutter_free_subset() -> None:
    """On a clutter-heavy frame only the above-road, plausible returns survive."""
    cfg = _config()
    rng = random.Random(11)
    detections: List[RadarDetection] = []
    # 140 road-surface returns (below the sensor plane) plus 5 vehicle returns.
    for _ in range(140):
        detections.append(
            RadarDetection(
                depth=rng.uniform(4.0, 60.0),
                azimuth=rng.uniform(-1.0, 1.0),
                altitude=rng.uniform(-0.40, -0.08),
                velocity=rng.uniform(-12.0, -6.0),
            )
        )
    for _ in range(5):
        detections.append(
            RadarDetection(
                depth=rng.uniform(25.0, 27.0),
                azimuth=rng.uniform(-0.05, 0.05),
                altitude=rng.uniform(-0.01, 0.02),
                velocity=-9.0,
            )
        )

    kept = filter_detections(detections, cfg)
    assert len(kept) == 5
    assert all(d.altitude > -0.05 for d in kept)


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------


def test_cluster_points_separates_groups_and_drops_noise() -> None:
    """Two separated blobs -> two clusters; isolated returns -> dropped."""
    points: List[Tuple[float, float, float]] = [
        # group A (indices 0..3)
        (10.0, 0.0, -5.0),
        (10.5, 0.3, -5.1),
        (9.7, -0.4, -4.9),
        (10.2, 0.1, -5.0),
        # noise (index 4)
        (20.0, 0.0, -5.0),
        # group B (indices 5..8)
        (30.0, 1.0, -5.0),
        (30.4, 1.2, -5.1),
        (29.6, 0.8, -4.9),
        (30.2, 1.1, -5.0),
        # noise (index 9)
        (45.0, 12.0, -5.0),
    ]

    groups = cluster_points(points, eps=2.2, min_points=3, velocity_weight=0.6)

    assert [sorted(g) for g in groups] == [[0, 1, 2, 3], [5, 6, 7, 8]]
    flat = {i for g in groups for i in g}
    assert 4 not in flat and 9 not in flat


def test_cluster_points_merges_a_tight_group_into_one_cluster() -> None:
    """A dense blob of returns from one object must not fragment."""
    rng = random.Random(3)
    points = [
        (25.0 + rng.uniform(-0.6, 0.6), -1.0 + rng.uniform(-0.6, 0.6), -7.0)
        for _ in range(12)
    ]
    groups = cluster_points(points, eps=2.2, min_points=3, velocity_weight=0.6)
    assert len(groups) == 1
    assert sorted(groups[0]) == list(range(12))


def test_cluster_points_chains_through_a_bridging_core_point() -> None:
    """Density reachability is transitive: a chain longer than eps stays one cluster."""
    points = [(0.0, 0.0, 0.0), (1.5, 0.0, 0.0), (3.0, 0.0, 0.0)]
    groups = cluster_points(points, eps=2.0, min_points=3, velocity_weight=0.0)
    assert len(groups) == 1
    assert sorted(groups[0]) == [0, 1, 2]


def test_cluster_points_uses_range_rate_to_split_co_located_objects() -> None:
    """Same place, opposite radial motion => different objects when weighted."""
    points: List[Tuple[float, float, float]] = []
    for k in range(4):
        points.append((20.0 + 0.2 * k, 0.1 * k, -12.0))
    for k in range(4):
        points.append((20.0 + 0.2 * k, 0.1 * k, 2.0))

    split = cluster_points(points, eps=2.2, min_points=3, velocity_weight=0.6)
    merged = cluster_points(points, eps=2.2, min_points=3, velocity_weight=0.0)

    assert [sorted(g) for g in split] == [[0, 1, 2, 3], [4, 5, 6, 7]]
    assert len(merged) == 1


def test_cluster_points_edge_cases() -> None:
    assert cluster_points([], eps=2.2, min_points=3, velocity_weight=0.6) == []
    assert (
        cluster_points([(1.0, 1.0, 0.0)], eps=2.2, min_points=3, velocity_weight=0.6)
        == []
    )
    with pytest.raises(ValueError):
        cluster_points([(1.0, 1.0, 0.0)], eps=0.0, min_points=3, velocity_weight=0.6)


# ---------------------------------------------------------------------------
# Degradation
# ---------------------------------------------------------------------------


def _noisy_config(**degradation: float) -> Config:
    base = {
        "enabled": True,
        "dropout_prob": 0.0,
        "point_dropout_prob": 0.0,
        "range_noise_sigma_m": 0.0,
        "azimuth_noise_sigma_rad": 0.0,
        "velocity_noise_sigma_mps": 0.0,
    }
    base.update(degradation)
    return _config().with_overrides({"radar": {"degradation": base}})


def _uniform_frame(n: int) -> RadarFrame:
    frame = _empty_frame()
    frame.detections = [
        RadarDetection(depth=30.0, azimuth=0.05, altitude=0.0, velocity=-10.0)
        for _ in range(n)
    ]
    return frame


def test_apply_degradation_is_pure_and_reproducible() -> None:
    frame = _uniform_frame(200)
    cfg = _noisy_config(
        range_noise_sigma_m=0.5,
        azimuth_noise_sigma_rad=0.02,
        velocity_noise_sigma_mps=0.5,
    )

    a = apply_degradation(frame, cfg, random.Random(7))
    b = apply_degradation(frame, cfg, random.Random(7))
    c = apply_degradation(frame, cfg, random.Random(8))

    assert a is not frame
    assert [d.depth for d in a.detections] == [d.depth for d in b.detections]
    assert [d.depth for d in a.detections] != [d.depth for d in c.detections]
    # the input is untouched
    assert len(frame.detections) == 200
    assert all(d.depth == 30.0 and d.velocity == -10.0 for d in frame.detections)
    # extrinsics are carried through unchanged
    assert (a.sensor_x, a.sensor_z, a.sensor_id) == (MOUNT_X, MOUNT_Z, "front")


def test_apply_degradation_injects_the_requested_noise_magnitude() -> None:
    frame = _uniform_frame(400)
    cfg = _noisy_config(range_noise_sigma_m=0.5, velocity_noise_sigma_mps=0.8)
    out = apply_degradation(frame, cfg, random.Random(19))

    depths = [d.depth for d in out.detections]
    mean = sum(depths) / len(depths)
    std = math.sqrt(sum((d - mean) ** 2 for d in depths) / (len(depths) - 1))
    assert abs(mean - 30.0) < 0.15
    assert 0.40 < std < 0.62

    vels = [d.velocity for d in out.detections]
    vmean = sum(vels) / len(vels)
    vstd = math.sqrt(sum((v - vmean) ** 2 for v in vels) / (len(vels) - 1))
    assert abs(vmean + 10.0) < 0.25
    assert 0.65 < vstd < 0.98
    # altitude carries no noise model
    assert all(d.altitude == 0.0 for d in out.detections)


def test_apply_degradation_dropout_semantics() -> None:
    frame = _uniform_frame(400)

    whole_frame = apply_degradation(
        frame, _noisy_config(dropout_prob=1.0), random.Random(1)
    )
    assert whole_frame.detections == []
    assert whole_frame.frame == frame.frame  # the frame itself is still recorded

    all_points = apply_degradation(
        frame, _noisy_config(point_dropout_prob=1.0), random.Random(1)
    )
    assert all_points.detections == []

    half = apply_degradation(
        frame, _noisy_config(point_dropout_prob=0.5), random.Random(5)
    )
    assert 160 < len(half.detections) < 240


def test_apply_degradation_disabled_is_an_untouched_copy() -> None:
    frame = _uniform_frame(5)
    cfg = _config()  # baseline profile: degradation disabled
    rng = random.Random(4)
    out = apply_degradation(frame, cfg, rng)

    assert len(out.detections) == 5
    assert all(d.depth == 30.0 for d in out.detections)
    assert out.detections[0] is not frame.detections[0]
    # a disabled profile must not consume the random stream
    assert rng.random() == random.Random(4).random()


# ---------------------------------------------------------------------------
# Front-end behaviour
# ---------------------------------------------------------------------------


def test_front_end_caps_clusters_and_keeps_the_closest() -> None:
    cfg = _config().with_overrides(
        {"radar_processing": {"cluster": {"max_clusters": 2}}}
    )
    own = _telemetry(x=0.0, y=0.0, yaw=0.0)
    frame = _empty_frame()
    detections: List[RadarDetection] = []
    for rng_m in (40.0, 10.0, 30.0, 20.0):
        detections.extend(_blob_detections(rng_m, 0.0, frame))
    frame.detections = detections

    clusters = RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0)).process(frame, own)

    assert len(clusters) == 2
    assert [round(c.range_m) for c in clusters] == [10, 20]


def test_front_end_returns_nothing_when_everything_is_clutter() -> None:
    cfg = _config()
    own = _telemetry(x=0.0, y=0.0, yaw=0.0)
    frame = _empty_frame()
    frame.detections = [
        RadarDetection(depth=20.0, azimuth=0.0, altitude=-0.4, velocity=-3.0)
        for _ in range(50)
    ]
    assert RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0)).process(frame, own) == []


def test_front_end_quality_rewards_dense_compact_clusters() -> None:
    cfg = _config()
    own = _telemetry(x=0.0, y=0.0, yaw=0.0)
    frame = _empty_frame()

    dense = [
        _detection_from_body(20.0 + 0.1 * k, 0.1 * (k % 3), MOUNT_Z, -6.0, frame)
        for k in range(8)
    ]
    sparse = [
        _detection_from_body(40.0 + 1.6 * k, 0.0, MOUNT_Z, -6.0, frame) for k in range(3)
    ]
    frame.detections = dense + sparse

    clusters = RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0)).process(frame, own)
    assert len(clusters) == 2
    near, far = clusters[0], clusters[1]
    assert near.n_points == 8 and far.n_points == 3
    assert near.quality > 0.8
    assert far.quality < 0.5
    assert near.quality > far.quality
    assert far.extent_x == pytest.approx(3.2, abs=1e-6)


def test_front_end_rejects_another_participants_evidence() -> None:
    """Mixing participants would fabricate evidence, so it must fail loudly."""
    cfg = _config()
    front_end = RadarFrontEnd(cfg, PARTICIPANT, rng=random.Random(0))
    own = _telemetry(x=0.0, y=0.0, yaw=0.0)

    foreign_frame = _empty_frame()
    foreign_frame.participant_id = "B"
    with pytest.raises(ValueError):
        front_end.process(foreign_frame, own)

    frame = _empty_frame()
    foreign_telemetry = _telemetry(x=0.0, y=0.0, yaw=0.0)
    foreign_telemetry.participant_id = "B"
    with pytest.raises(ValueError):
        front_end.process(frame, foreign_telemetry)
