"""Radar front-end: raw polar returns -> plausible, spatially coherent clusters.

This is the first stage of a participant's *own* perception chain. It consumes
nothing but the participant's own radar frames, its own sensor extrinsics and its
own localisation, which is what makes the resulting clusters admissible local
evidence: no property of the observed object -- its identity, its true pose, its
commanded speed -- is ever queried.

Why each stage exists
---------------------
* **Degradation** (:func:`apply_degradation`) injects the sensor-quality profile
  *after* acquisition rather than asking the simulator for a worse sensor. That
  keeps every profile reproducible from a seed and makes "what would participant
  B have seen with a degraded radar?" a controlled, re-runnable experiment.
* **Plausibility filtering** (:func:`filter_detections`) is mandatory, not
  cosmetic. Measured CARLA output on this machine is ~145 returns per frame, the
  large majority of which are road-surface reflections below the sensor plane,
  and the first frame after spawn routinely contains a ~100 m/s return that is
  physically impossible for a road vehicle. Feeding either into the tracker
  produces confident nonsense.
* **Clustering** (:func:`cluster_points`) turns a cloud of returns into at most
  one measurement per physical object. Range-rate participates in the distance
  metric because two vehicles at the same bearing and range but with opposite
  radial motion are genuinely different objects.

Frames
------
``rel_x``/``rel_y`` are in the observer **body** frame (``+x`` forward, ``+y``
right). ``range_m`` and ``azimuth_rad`` are the polar coordinates *of that same
body-frame centroid*, so ``hypot(rel_x, rel_y) == range_m`` exactly; they are not
the raw sensor-relative range/bearing, which would be offset by the mounting
translation. ``range_rate`` remains the measured radial rate along the sensor
line of sight. Keeping the position quantities in one frame is what lets the
downstream indicators (TTC, closest approach, conflict prediction) compose
without silent frame mismatches; the residual inconsistency between a
body-origin range and a sensor-origin range rate is bounded by the mounting
offset (~2 m) and is documented here rather than hidden.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..common.config import Config
from ..common.geometry import body_to_global, global_to_body, polar_to_body
from ..common.schemas import RadarDetection, RadarFrame, TelemetrySample

__all__ = [
    "RadarCluster",
    "apply_degradation",
    "filter_detections",
    "cluster_points",
    "stationarity_residual",
    "RadarFrontEnd",
]


# ---------------------------------------------------------------------------
# Cluster record
# ---------------------------------------------------------------------------


@dataclass
class RadarCluster:
    """One physical object hypothesis extracted from a single radar frame.

    A cluster is a *measurement*, not a track: it has no identity across frames.
    Identity is established by :mod:`cdf.local.tracking`, which is the only place
    allowed to invent a (still anonymous) label.
    """

    t: float
    frame: int
    participant_id: str
    sensor_id: str

    # Observer body frame (x forward, y right), metres.
    rel_x: float = 0.0
    rel_y: float = 0.0
    # Global (map) frame estimate obtained from the observer's own pose only.
    gx: float = 0.0
    gy: float = 0.0

    range_m: float = 0.0
    """Range of the body-frame centroid, metres (``hypot(rel_x, rel_y)``)."""
    azimuth_rad: float = 0.0
    """Bearing of the body-frame centroid, radians, positive to the right."""
    range_rate: float = 0.0
    """Mean measured radial velocity of the member returns; negative = closing."""

    n_points: int = 0
    extent_x: float = 0.0
    extent_y: float = 0.0
    quality: float = 0.0
    """Heuristic ``0..1`` measurement quality from point count and compactness."""

    is_stationary: bool = False
    """Whether this measurement is consistent with a world-fixed object.

    Derived from own speed and the measured bearing alone (see
    :func:`stationarity_residual`), so it remains purely local evidence."""
    stationarity_residual: float = 0.0
    """``|range_rate + own_speed * cos(azimuth)|`` in m/s: how far the
    measurement departs from what a world-fixed object would produce."""


def stationarity_residual(
    range_rate: float,
    azimuth_rad: float,
    v_forward: float,
    v_lateral: float = 0.0,
) -> float:
    """How inconsistent a return is with being a world-fixed object, in m/s.

    A world-fixed point at bearing ``azimuth`` produces a radial velocity of
    exactly ``-(v_forward*cos(az) + v_lateral*sin(az))`` -- the negated
    projection of the observer's own velocity onto the line of sight. The
    residual against that prediction is near zero for road surface, kerbs, walls,
    poles and parked objects, and close to the *relative* speed for anything
    actually moving.

    ``v_forward``/``v_lateral`` are the observer's own velocity in its body frame
    (``+x`` forward, ``+y`` right). Using the full velocity vector rather than
    scalar speed matters whenever the vehicle is not travelling straight ahead:
    during a post-impact spin the heading and the velocity direction diverge
    sharply, and a forward-only model then mistakes the entire static world for
    moving objects and floods the tracker with spurious tracks.

    This is the classic automotive-radar stationary-target discriminator, and it
    is legitimate local evidence: it needs only the observer's own velocity and
    the bearing and range-rate the sensor itself reported. Nothing about the
    observed object is required.
    """
    az = float(azimuth_rad)
    expected = -(float(v_forward) * math.cos(az) + float(v_lateral) * math.sin(az))
    return abs(float(range_rate) - expected)


# ---------------------------------------------------------------------------
# Sensor degradation
# ---------------------------------------------------------------------------


def _rebuilt_frame(frame: RadarFrame, detections: List[RadarDetection]) -> RadarFrame:
    """A copy of ``frame`` carrying ``detections`` and the same extrinsics."""
    return RadarFrame(
        t=frame.t,
        frame=frame.frame,
        participant_id=frame.participant_id,
        sensor_id=frame.sensor_id,
        detections=detections,
        sensor_yaw=frame.sensor_yaw,
        sensor_x=frame.sensor_x,
        sensor_y=frame.sensor_y,
        sensor_z=frame.sensor_z,
        schema_version=frame.schema_version,
    )


def apply_degradation(frame: RadarFrame, cfg: Config, rng: random.Random) -> RadarFrame:
    """Apply the configured ``radar.degradation`` profile to one radar frame.

    The function is pure with respect to its inputs -- a brand new
    :class:`~cdf.common.schemas.RadarFrame` with brand new detections is
    returned and ``frame`` is never mutated -- and deterministic given ``rng``.
    That combination is what makes a degraded run byte-reproducible from a seed.

    Draw discipline: when degradation is enabled, exactly one uniform draw and
    three Gaussian draws are consumed per detection *regardless of whether the
    detection survives*. Consequently changing ``point_dropout_prob`` or a noise
    sigma re-weights the outcome without reshuffling the whole random stream,
    which keeps profile comparisons interpretable.
    """
    if not bool(cfg.get("radar.degradation.enabled", False)):
        return _rebuilt_frame(
            frame,
            [
                RadarDetection(d.depth, d.azimuth, d.altitude, d.velocity)
                for d in frame.detections
            ],
        )

    frame_dropout = float(cfg.get("radar.degradation.dropout_prob", 0.0))
    point_dropout = float(cfg.get("radar.degradation.point_dropout_prob", 0.0))
    range_sigma = float(cfg.get("radar.degradation.range_noise_sigma_m", 0.0))
    azimuth_sigma = float(cfg.get("radar.degradation.azimuth_noise_sigma_rad", 0.0))
    velocity_sigma = float(cfg.get("radar.degradation.velocity_noise_sigma_mps", 0.0))

    if rng.random() < frame_dropout:
        # A whole-frame dropout models a blinded/aborted sensor cycle: the
        # recorder keeps the frame (so the gap is visible downstream) but it
        # carries no returns.
        return _rebuilt_frame(frame, [])

    kept: List[RadarDetection] = []
    for det in frame.detections:
        drop = rng.random()
        d_noise = rng.gauss(0.0, range_sigma) if range_sigma > 0.0 else 0.0
        a_noise = rng.gauss(0.0, azimuth_sigma) if azimuth_sigma > 0.0 else 0.0
        v_noise = rng.gauss(0.0, velocity_sigma) if velocity_sigma > 0.0 else 0.0
        if drop < point_dropout:
            continue
        kept.append(
            RadarDetection(
                depth=max(0.0, float(det.depth) + d_noise),
                azimuth=float(det.azimuth) + a_noise,
                altitude=float(det.altitude),
                velocity=float(det.velocity) + v_noise,
            )
        )
    return _rebuilt_frame(frame, kept)


# ---------------------------------------------------------------------------
# Plausibility filtering
# ---------------------------------------------------------------------------


def filter_detections(
    detections: Sequence[RadarDetection], cfg: Config
) -> List[RadarDetection]:
    """Drop physically implausible returns before any downstream inference.

    All five gates come from ``radar_processing.filter``. The altitude band is
    the one that removes the road-surface clutter dominating a raw CARLA frame;
    the velocity gate is what removes the ~100 m/s artifact emitted on the first
    frame after spawn. Order of the returns is preserved so that clustering stays
    deterministic.
    """
    min_range = float(cfg.get("radar_processing.filter.min_range_m", 1.5))
    max_range = float(cfg.get("radar_processing.filter.max_range_m", 90.0))
    max_abs_velocity = float(
        cfg.get("radar_processing.filter.max_abs_velocity_mps", 60.0)
    )
    min_altitude = float(cfg.get("radar_processing.filter.min_altitude_rad", -0.05))
    max_altitude = float(cfg.get("radar_processing.filter.max_altitude_rad", 0.25))
    max_abs_azimuth = float(
        cfg.get("radar_processing.filter.max_abs_azimuth_rad", 1.10)
    )

    out: List[RadarDetection] = []
    for det in detections:
        depth = float(det.depth)
        if not (min_range <= depth <= max_range):
            continue
        if abs(float(det.velocity)) > max_abs_velocity:
            continue
        altitude = float(det.altitude)
        if not (min_altitude <= altitude <= max_altitude):
            continue
        if abs(float(det.azimuth)) > max_abs_azimuth:
            continue
        out.append(det)
    return out


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------


def cluster_points(
    points: Sequence[Tuple[float, float, float]],
    eps: float,
    min_points: int,
    velocity_weight: float,
) -> List[List[int]]:
    """Group body-frame returns into object hypotheses (DBSCAN, density based).

    Parameters
    ----------
    points:
        ``(rel_x, rel_y, range_rate)`` triples in the observer body frame.
    eps:
        Neighbourhood radius of the metric
        ``sqrt(dx^2 + dy^2 + (velocity_weight * dv)^2)``.
    min_points:
        Minimum neighbourhood population for a point to be a *core* point. The
        point itself counts, matching the usual DBSCAN ``minPts`` convention.
    velocity_weight:
        Weight (seconds) converting a range-rate difference into a pseudo-metre,
        so that two objects at the same place moving differently do not merge.

    Returns
    -------
    Lists of indices into ``points``. Core points are linked transitively;
    non-core points inside the neighbourhood of a core point join that core
    point's cluster; everything else is noise and is dropped. Iteration is in
    index order throughout, so the output -- both the cluster order and the
    member order -- is a deterministic function of the input.

    This is implemented here rather than pulled from scikit-learn to keep the
    dependency surface small and the behaviour auditable: a forensic pipeline
    must be able to explain exactly why two returns were merged.
    """
    n = len(points)
    if n == 0:
        return []
    if eps <= 0.0:
        raise ValueError("cluster eps must be positive, got {0!r}".format(eps))
    if min_points < 1:
        raise ValueError("min_points must be >= 1, got {0!r}".format(min_points))

    arr = np.asarray(points, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 3:
        raise ValueError(
            "cluster_points expects (rel_x, rel_y, range_rate) triples, got shape {0}".format(
                arr.shape
            )
        )

    dx = arr[:, 0][:, None] - arr[:, 0][None, :]
    dy = arr[:, 1][:, None] - arr[:, 1][None, :]
    dv = float(velocity_weight) * (arr[:, 2][:, None] - arr[:, 2][None, :])
    within = (dx * dx + dy * dy + dv * dv) <= float(eps) * float(eps)

    counts = within.sum(axis=1)
    core = counts >= int(min_points)
    if not bool(core.any()):
        return []

    # Connected components of the core-point graph, grown one seed at a time.
    # Seeds are visited in ascending index order, so a component is always
    # labelled by its lowest member index: the labelling is a pure function of
    # the input, never of traversal luck.
    labels: List[Optional[int]] = [None] * n
    visited = np.zeros(n, dtype=bool)
    for seed in range(n):
        if not core[seed] or visited[seed]:
            continue
        visited[seed] = True
        labels[seed] = seed
        stack = [seed]
        while stack:
            i = stack.pop()
            reachable = np.nonzero(within[i] & core & ~visited)[0]
            for j in reachable.tolist():
                visited[j] = True
                labels[j] = seed
                stack.append(int(j))

    for i in range(n):
        if core[i]:
            continue
        # Border point: attach to the lowest-indexed core point it can reach.
        neighbours = np.nonzero(within[i] & core)[0]
        if neighbours.size:
            labels[i] = labels[int(neighbours[0])]

    order: List[int] = []
    groups: Dict[int, List[int]] = {}
    for i in range(n):
        lab = labels[i]
        if lab is None:
            continue
        if lab not in groups:
            groups[lab] = []
            order.append(lab)
        groups[lab].append(i)
    return [groups[lab] for lab in order]


# ---------------------------------------------------------------------------
# Front-end
# ---------------------------------------------------------------------------


class RadarFrontEnd:
    """Per-participant radar processing chain (degrade -> filter -> cluster).

    One instance belongs to exactly one participant. It holds the degradation
    random stream, which is why it is a class and not a free function: the
    stream must advance monotonically across frames for the degradation profile
    to be reproducible yet non-repeating.
    """

    def __init__(
        self,
        cfg: Config,
        participant_id: str,
        rng: Optional[random.Random] = None,
    ) -> None:
        self._cfg = cfg
        self._participant_id = str(participant_id)
        # A seeded stream is mandatory: an unseeded default would make degraded
        # runs irreproducible, which would invalidate every profile comparison.
        self._rng = rng if rng is not None else random.Random(int(cfg.get("run.seed", 0)))

        self._eps = float(cfg.get("radar_processing.cluster.eps_m", 2.2))
        self._min_points = int(cfg.get("radar_processing.cluster.min_points", 3))
        self._velocity_weight = float(
            cfg.get("radar_processing.cluster.velocity_weight", 0.6)
        )
        self._max_clusters = int(cfg.get("radar_processing.cluster.max_clusters", 24))
        self._stationary_enabled = bool(
            cfg.get("radar_processing.stationary.enabled", True)
        )
        self._stationary_tolerance = float(
            cfg.get("radar_processing.stationary.tolerance_mps", 1.5)
        )
        self._quality_saturation = float(
            cfg.get(
                "radar_processing.cluster.quality_saturation_points",
                2.0 * float(self._min_points),
            )
        )

    # -- accessors --------------------------------------------------------

    @property
    def participant_id(self) -> str:
        """The participant this front-end belongs to."""
        return self._participant_id

    # -- main entry point -------------------------------------------------

    def process(
        self, frame: RadarFrame, telemetry: TelemetrySample
    ) -> List[RadarCluster]:
        """Turn one raw radar frame into at most ``max_clusters`` measurements.

        ``telemetry`` must be the observer's own pose sample nearest in time to
        ``frame``; only ``x``, ``y`` and ``yaw`` are read from it. Mixing another
        participant's frame or pose into this front-end would fabricate evidence,
        so both are checked and a mismatch raises instead of being tolerated.
        """
        if frame.participant_id != self._participant_id:
            raise ValueError(
                "radar frame belongs to participant {0!r} but this front-end serves {1!r}".format(
                    frame.participant_id, self._participant_id
                )
            )
        if telemetry.participant_id != self._participant_id:
            raise ValueError(
                "telemetry belongs to participant {0!r} but this front-end serves {1!r}".format(
                    telemetry.participant_id, self._participant_id
                )
            )

        degraded = apply_degradation(frame, self._cfg, self._rng)
        detections = filter_detections(degraded.detections, self._cfg)
        if not detections:
            return []

        points: List[Tuple[float, float, float]] = []
        residuals: List[float] = []
        sensor_yaw_rad = math.radians(float(frame.sensor_yaw))
        # Own velocity in the body frame; see stationarity_residual for why the
        # full vector rather than scalar speed is required.
        v_forward, v_lateral = global_to_body(
            telemetry.vx, telemetry.vy, 0.0, 0.0, telemetry.yaw
        )
        # Lever-arm term: the radar sits forward of the vehicle origin, so when
        # the vehicle rotates the sensor itself translates at omega x r. During a
        # post-impact spin this reaches several m/s -- comparable to the closing
        # speeds we are trying to detect -- and uncompensated it makes the entire
        # static world look like moving objects. Yaw rate is reported in deg/s.
        omega = math.radians(float(telemetry.yaw_rate))
        v_forward -= omega * float(frame.sensor_y)
        v_lateral += omega * float(frame.sensor_x)
        for det in detections:
            bx, by, _bz = polar_to_body(
                det.depth,
                det.azimuth,
                det.altitude,
                frame.sensor_x,
                frame.sensor_y,
                frame.sensor_z,
                frame.sensor_yaw,
            )
            points.append((bx, by, float(det.velocity)))
            # The stationarity test must pair the measured range rate with the
            # bearing it was measured along -- the SENSOR-frame azimuth, rotated
            # into the body frame by the mounting yaw. Using the body-frame
            # centroid bearing instead introduces a parallax error of the order of
            # the mounting offset, which at short range is large enough to make
            # roadside clutter look like a moving object.
            residuals.append(
                stationarity_residual(
                    det.velocity,
                    float(det.azimuth) + sensor_yaw_rad,
                    v_forward,
                    v_lateral,
                )
            )

        groups = cluster_points(
            points, self._eps, self._min_points, self._velocity_weight
        )

        clusters: List[RadarCluster] = []
        for members in groups:
            clusters.append(
                self._build_cluster(frame, telemetry, points, members, residuals)
            )

        # Cap by keeping the closest hypotheses: a saturated frame is exactly the
        # situation in which the far-field returns matter least.
        clusters.sort(key=lambda c: (c.range_m, c.azimuth_rad))
        if len(clusters) > self._max_clusters:
            clusters = clusters[: self._max_clusters]
        return clusters

    # -- helpers ----------------------------------------------------------

    def _build_cluster(
        self,
        frame: RadarFrame,
        telemetry: TelemetrySample,
        points: Sequence[Tuple[float, float, float]],
        members: Sequence[int],
        residuals: Sequence[float],
    ) -> RadarCluster:
        """Reduce the member returns of one cluster to a single measurement."""
        n = len(members)
        xs = [points[i][0] for i in members]
        ys = [points[i][1] for i in members]
        vs = [points[i][2] for i in members]

        cx = sum(xs) / float(n)
        cy = sum(ys) / float(n)
        range_rate = sum(vs) / float(n)

        gx, gy = body_to_global(cx, cy, telemetry.x, telemetry.y, telemetry.yaw)
        spread = sum(math.hypot(x - cx, y - cy) for x, y in zip(xs, ys)) / float(n)

        azimuth = float(math.atan2(cy, cx))
        # Median rather than mean: a handful of member returns smeared by a
        # neighbouring moving object must not drag a wall's verdict.
        member_residuals = sorted(float(residuals[i]) for i in members)
        mid = len(member_residuals) // 2
        residual = (
            member_residuals[mid]
            if len(member_residuals) % 2 == 1
            else 0.5 * (member_residuals[mid - 1] + member_residuals[mid])
        )
        stationary = bool(
            self._stationary_enabled and residual <= self._stationary_tolerance
        )

        return RadarCluster(
            t=float(frame.t),
            frame=int(frame.frame),
            participant_id=self._participant_id,
            sensor_id=frame.sensor_id,
            rel_x=float(cx),
            rel_y=float(cy),
            gx=float(gx),
            gy=float(gy),
            range_m=float(math.hypot(cx, cy)),
            azimuth_rad=azimuth,
            range_rate=float(range_rate),
            n_points=int(n),
            extent_x=float(max(xs) - min(xs)),
            extent_y=float(max(ys) - min(ys)),
            quality=self._quality(n, spread),
            is_stationary=stationary,
            stationarity_residual=float(residual),
        )

    def _quality(self, n_points: int, spread: float) -> float:
        """Measurement quality in ``0..1`` from point count and compactness.

        A cluster is trustworthy when it is *populated* (many returns agree that
        something is there) and *compact* (the returns really do come from one
        object rather than from a smear across the neighbourhood radius). The two
        factors multiply so that either deficiency alone lowers the score.
        """
        saturation = max(1.0, float(self._quality_saturation))
        count_factor = min(1.0, float(n_points) / saturation)
        compactness = self._eps / (self._eps + max(0.0, float(spread)))
        return max(0.0, min(1.0, count_factor * compactness))
