"""Coordinate transforms and planar geometry used by the local pipeline.

Everything here operates on plain floats and NumPy arrays: there is no CARLA
import, so the whole module is unit-testable without a simulator.

Frames and conventions
----------------------
* **Global (map) frame** -- CARLA's left-handed world frame. We use only the
  planar components ``(x, y)`` and the heading ``yaw`` in degrees. CARLA yaw
  grows clockwise when viewed from above with ``+x`` at yaw ``0``.
* **Body frame** -- attached to a participant: ``+x`` forward, ``+y`` to the
  right of the driver, origin at the vehicle reference point.
* **Sensor frame** -- attached to a radar: ``+x`` along boresight, ``+y`` right.
  Radar detections arrive in spherical coordinates ``(depth, azimuth, altitude)``
  with azimuth positive to the right and altitude positive upwards.

The global transform of a radar return therefore composes *only* the observer's
own localisation with the sensor's known mounting extrinsics. No property of the
observed object is ever queried -- this is what makes the estimate legitimate
local evidence.
"""

from __future__ import annotations

import math
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np

__all__ = [
    "normalize_angle_deg",
    "angle_diff_deg",
    "wrap_pi",
    "deg2rad",
    "rad2deg",
    "polar_to_body",
    "body_to_global",
    "global_to_body",
    "radar_detection_to_global",
    "rotate2d",
    "distance",
    "closest_point_on_segment",
    "segment_intersection",
    "polyline_intersection",
    "time_to_collision_1d",
    "closest_approach",
    "trajectory_rmse",
    "resample_trajectory",
    "heading_from_velocity",
    "predict_constant_velocity",
    "point_in_circle",
]


# ---------------------------------------------------------------------------
# Angles
# ---------------------------------------------------------------------------


def deg2rad(deg: float) -> float:
    """Degrees to radians."""
    return float(deg) * math.pi / 180.0


def rad2deg(rad: float) -> float:
    """Radians to degrees."""
    return float(rad) * 180.0 / math.pi


def normalize_angle_deg(deg: float) -> float:
    """Wrap an angle in degrees to ``(-180, 180]``."""
    a = (float(deg) + 180.0) % 360.0 - 180.0
    return 180.0 if a == -180.0 else a


def angle_diff_deg(a: float, b: float) -> float:
    """Signed smallest difference ``a - b`` in degrees, wrapped to ``(-180, 180]``."""
    return normalize_angle_deg(float(a) - float(b))


def wrap_pi(rad: float) -> float:
    """Wrap an angle in radians to ``(-pi, pi]``."""
    a = (float(rad) + math.pi) % (2.0 * math.pi) - math.pi
    return math.pi if a == -math.pi else a


# ---------------------------------------------------------------------------
# Frame transforms
# ---------------------------------------------------------------------------


def rotate2d(x: float, y: float, yaw_deg: float) -> Tuple[float, float]:
    """Rotate ``(x, y)`` by ``yaw_deg`` in CARLA's left-handed planar convention.

    With ``+x`` forward and ``+y`` to the right, a positive yaw rotates the body
    axes clockwise when seen from above, which is the same sign convention CARLA
    uses for ``Rotation.yaw``.
    """
    c = math.cos(deg2rad(yaw_deg))
    s = math.sin(deg2rad(yaw_deg))
    return (c * float(x) - s * float(y), s * float(x) + c * float(y))


def polar_to_body(
    depth: float,
    azimuth: float,
    altitude: float,
    sensor_x: float = 0.0,
    sensor_y: float = 0.0,
    sensor_z: float = 0.0,
    sensor_yaw_deg: float = 0.0,
) -> Tuple[float, float, float]:
    """Convert one radar return to the observer's body frame.

    Parameters
    ----------
    depth, azimuth, altitude:
        Radar measurement: range in metres, azimuth and altitude in **radians**.
        Azimuth is positive to the right of boresight, altitude positive upwards.
    sensor_x, sensor_y, sensor_z:
        Mounting translation of the sensor in the body frame, metres.
    sensor_yaw_deg:
        Mounting yaw of the sensor relative to the body frame, degrees.

    Returns
    -------
    ``(x, y, z)`` in the body frame, metres.
    """
    d = float(depth)
    az = float(azimuth)
    alt = float(altitude)

    horiz = d * math.cos(alt)
    sx = horiz * math.cos(az)
    sy = horiz * math.sin(az)
    sz = d * math.sin(alt)

    bx, by = rotate2d(sx, sy, sensor_yaw_deg)
    return (bx + float(sensor_x), by + float(sensor_y), sz + float(sensor_z))


def body_to_global(
    bx: float, by: float, origin_x: float, origin_y: float, origin_yaw_deg: float
) -> Tuple[float, float]:
    """Map a body-frame point to the global frame using the observer's own pose."""
    rx, ry = rotate2d(bx, by, origin_yaw_deg)
    return (rx + float(origin_x), ry + float(origin_y))


def global_to_body(
    gx: float, gy: float, origin_x: float, origin_y: float, origin_yaw_deg: float
) -> Tuple[float, float]:
    """Inverse of :func:`body_to_global`."""
    dx = float(gx) - float(origin_x)
    dy = float(gy) - float(origin_y)
    return rotate2d(dx, dy, -float(origin_yaw_deg))


def radar_detection_to_global(
    depth: float,
    azimuth: float,
    altitude: float,
    own_x: float,
    own_y: float,
    own_yaw_deg: float,
    sensor_x: float = 0.0,
    sensor_y: float = 0.0,
    sensor_z: float = 0.0,
    sensor_yaw_deg: float = 0.0,
) -> Tuple[float, float]:
    """Full radar-return-to-global-frame transform.

    Composes the sensor extrinsics with the observer's own localisation only.
    This is the single place where a local track acquires global coordinates, and
    it demonstrably needs nothing about the observed object.
    """
    bx, by, _bz = polar_to_body(
        depth, azimuth, altitude, sensor_x, sensor_y, sensor_z, sensor_yaw_deg
    )
    return body_to_global(bx, by, own_x, own_y, own_yaw_deg)


# ---------------------------------------------------------------------------
# Planar geometry
# ---------------------------------------------------------------------------


def distance(ax: float, ay: float, bx: float, by: float) -> float:
    """Euclidean distance between two planar points."""
    return math.hypot(float(bx) - float(ax), float(by) - float(ay))


def point_in_circle(
    px: float, py: float, cx: float, cy: float, radius: float
) -> bool:
    """Whether ``(px, py)`` lies within ``radius`` of ``(cx, cy)``."""
    return distance(px, py, cx, cy) <= float(radius)


def closest_point_on_segment(
    px: float, py: float, ax: float, ay: float, bx: float, by: float
) -> Tuple[float, float, float]:
    """Closest point on segment ``AB`` to ``P``.

    Returns ``(x, y, t)`` where ``t`` in ``[0, 1]`` is the normalised position
    along the segment.
    """
    vx, vy = float(bx) - float(ax), float(by) - float(ay)
    denom = vx * vx + vy * vy
    if denom <= 1e-12:
        return (float(ax), float(ay), 0.0)
    t = ((float(px) - float(ax)) * vx + (float(py) - float(ay)) * vy) / denom
    t = max(0.0, min(1.0, t))
    return (float(ax) + t * vx, float(ay) + t * vy, t)


def segment_intersection(
    p1: Sequence[float],
    p2: Sequence[float],
    p3: Sequence[float],
    p4: Sequence[float],
) -> Optional[Tuple[float, float, float, float]]:
    """Intersection of segments ``p1p2`` and ``p3p4``.

    Returns ``(x, y, t, u)`` with ``t``/``u`` the normalised positions along the
    first and second segment, or ``None`` when the segments do not cross.
    """
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])
    x3, y3 = float(p3[0]), float(p3[1])
    x4, y4 = float(p4[0]), float(p4[1])

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom
    if not (0.0 <= t <= 1.0 and 0.0 <= u <= 1.0):
        return None
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1), t, u)


def polyline_intersection(
    poly_a: Sequence[Sequence[float]], poly_b: Sequence[Sequence[float]]
) -> List[Tuple[float, float, int, int]]:
    """All crossings between two polylines.

    Returns a list of ``(x, y, i, j)`` where ``i``/``j`` index the crossing
    segment in ``poly_a``/``poly_b``. Used to infer a latent conflict region from
    two predicted trajectories without consulting any map.
    """
    out: List[Tuple[float, float, int, int]] = []
    for i in range(len(poly_a) - 1):
        for j in range(len(poly_b) - 1):
            hit = segment_intersection(poly_a[i], poly_a[i + 1], poly_b[j], poly_b[j + 1])
            if hit is not None:
                out.append((hit[0], hit[1], i, j))
    return out


# ---------------------------------------------------------------------------
# Kinematic indicators
# ---------------------------------------------------------------------------


def time_to_collision_1d(range_m: float, range_rate: float) -> Optional[float]:
    """Range-rate time-to-collision.

    ``range_rate`` follows the radar convention: **negative means closing**.
    Returns ``None`` when the target is not closing (TTC is undefined), which the
    event extractor treats as "no evidence" rather than "safe".
    """
    rr = float(range_rate)
    if rr >= -1e-3:
        return None
    return max(0.0, float(range_m) / (-rr))


def closest_approach(
    rel_x: float,
    rel_y: float,
    rel_vx: float,
    rel_vy: float,
) -> Tuple[Optional[float], float]:
    """Constant-velocity closest point of approach.

    Parameters are the target's relative position and relative velocity in any
    consistent planar frame.

    Returns ``(t_cpa, d_cpa)``: the time of closest approach in seconds
    (``None`` when the relative motion is not converging) and the distance at
    that moment in metres.
    """
    vx, vy = float(rel_vx), float(rel_vy)
    px, py = float(rel_x), float(rel_y)
    v2 = vx * vx + vy * vy
    if v2 <= 1e-9:
        return (None, math.hypot(px, py))
    t = -(px * vx + py * vy) / v2
    if t < 0.0:
        return (None, math.hypot(px, py))
    dx = px + vx * t
    dy = py + vy * t
    return (t, math.hypot(dx, dy))


def heading_from_velocity(vx: float, vy: float, fallback: float = 0.0) -> float:
    """Heading in degrees implied by a planar velocity, or ``fallback`` if still."""
    if math.hypot(float(vx), float(vy)) < 1e-3:
        return float(fallback)
    return rad2deg(math.atan2(float(vy), float(vx)))


def predict_constant_velocity(
    x: float, y: float, vx: float, vy: float, horizon_s: float, step_s: float = 0.2
) -> List[Tuple[float, float]]:
    """Sample a constant-velocity prediction of a planar trajectory.

    Used to derive *predicted* path conflicts from observable motion, which is
    how conflict regions are inferred without any map topology.
    """
    n = max(1, int(round(float(horizon_s) / float(step_s))))
    return [
        (float(x) + float(vx) * step_s * k, float(y) + float(vy) * step_s * k)
        for k in range(n + 1)
    ]


# ---------------------------------------------------------------------------
# Trajectory comparison (used by fusion track association)
# ---------------------------------------------------------------------------


def resample_trajectory(
    times: Sequence[float],
    xs: Sequence[float],
    ys: Sequence[float],
    query_times: Sequence[float],
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Linearly resample a planar trajectory onto ``query_times``.

    Returns ``(x, y, valid)`` where ``valid`` is a boolean mask that is ``False``
    outside the source time support -- extrapolation is never silently invented.
    """
    t = np.asarray(times, dtype=float)
    qx = np.asarray(query_times, dtype=float)
    if t.size == 0:
        nan = np.full(qx.shape, np.nan)
        return nan, nan.copy(), np.zeros(qx.shape, dtype=bool)

    order = np.argsort(t)
    t = t[order]
    x = np.asarray(xs, dtype=float)[order]
    y = np.asarray(ys, dtype=float)[order]

    valid = (qx >= t[0] - 1e-9) & (qx <= t[-1] + 1e-9)
    rx = np.interp(qx, t, x)
    ry = np.interp(qx, t, y)
    rx = np.where(valid, rx, np.nan)
    ry = np.where(valid, ry, np.nan)
    return rx, ry, valid


def trajectory_rmse(
    ax: Iterable[float], ay: Iterable[float], bx: Iterable[float], by: Iterable[float]
) -> Optional[float]:
    """Planar RMSE between two already time-aligned trajectories.

    ``NaN`` samples (produced by :func:`resample_trajectory` outside the time
    support) are excluded. Returns ``None`` when nothing overlaps.
    """
    axx = np.asarray(list(ax), dtype=float)
    ayy = np.asarray(list(ay), dtype=float)
    bxx = np.asarray(list(bx), dtype=float)
    byy = np.asarray(list(by), dtype=float)
    n = min(axx.size, ayy.size, bxx.size, byy.size)
    if n == 0:
        return None
    axx, ayy, bxx, byy = axx[:n], ayy[:n], bxx[:n], byy[:n]
    mask = ~(np.isnan(axx) | np.isnan(ayy) | np.isnan(bxx) | np.isnan(byy))
    if not np.any(mask):
        return None
    d2 = (axx[mask] - bxx[mask]) ** 2 + (ayy[mask] - byy[mask]) ** 2
    return float(math.sqrt(float(np.mean(d2))))
