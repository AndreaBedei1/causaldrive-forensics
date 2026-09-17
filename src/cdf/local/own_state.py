"""Derivation of a participant's own motion state from its own raw readings.

Everything in this module is computed from quantities a single vehicle can read
about *itself*: its pose, its velocity vector and (when the simulator exposes it)
its IMU acceleration. Nothing here consults another actor, the map, or any
privileged channel -- which is what makes the resulting
:class:`~cdf.common.schemas.TelemetrySample` admissible local evidence.

Why finite differences at all
-----------------------------
CARLA reports a vehicle's velocity directly but not, in general, a trustworthy
body-frame acceleration: ``Vehicle.get_acceleration()`` is noisy and an IMU
sensor is an optional attachment. The local pipeline nevertheless needs
``accel_long`` (braking/acceleration events) and ``yaw_rate`` (heading-change
events), so :func:`derive_motion` reconstructs them from the velocity and yaw
history when they are not supplied. The reconstruction is a *pure function* of
``(previous sample, current reading, dt)``: no hidden state, no wall clock, and
therefore bit-identical across reruns of the same seed.

Frames
------
World-frame accelerations ``(ax, ay)`` follow CARLA's left-handed planar
convention (see :mod:`cdf.common.geometry`). The body frame has ``+x`` forward
and ``+y`` to the right of the driver, so ``accel_long > 0`` means speeding up
along the current heading and ``accel_lat > 0`` means accelerating to the right.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple

from ..common.geometry import angle_diff_deg, rotate2d
from ..common.schemas import TelemetrySample

__all__ = [
    "derive_motion",
    "body_frame_acceleration",
    "ground_speed",
    "make_telemetry",
]


# ---------------------------------------------------------------------------
# Frame conversion
# ---------------------------------------------------------------------------


def body_frame_acceleration(ax: float, ay: float, yaw_deg: float) -> Tuple[float, float]:
    """Rotate a world-frame planar acceleration into the vehicle body frame.

    Parameters
    ----------
    ax, ay:
        World-frame acceleration components in m/s^2.
    yaw_deg:
        Vehicle heading in degrees, CARLA convention.

    Returns
    -------
    ``(accel_long, accel_lat)`` in m/s^2: longitudinal (positive forward) and
    lateral (positive to the driver's right).

    The transform is the inverse of :func:`cdf.common.geometry.rotate2d`, i.e. a
    rotation by ``-yaw``; expressing it through the shared geometry helper keeps
    the sign convention defined in exactly one place.
    """
    return rotate2d(float(ax), float(ay), -float(yaw_deg))


# ---------------------------------------------------------------------------
# Motion derivation
# ---------------------------------------------------------------------------


def derive_motion(
    prev: Optional[TelemetrySample], cur_raw: Dict[str, float], dt: float
) -> Dict[str, float]:
    """Complete a raw pose/velocity reading into a full motion state.

    Parameters
    ----------
    prev:
        The previously recorded telemetry sample of the *same* participant, or
        ``None`` for the first sample of a run.
    cur_raw:
        Current raw reading. ``"yaw"`` is mandatory; ``"vx"``, ``"vy"``, ``"vz"``
        default to zero. ``"ax"``, ``"ay"``, ``"az"`` and ``"yaw_rate"`` are
        optional: when present (and not ``None``) they are trusted as measured,
        otherwise they are reconstructed by finite differences against ``prev``.
    dt:
        Simulation time elapsed since ``prev``, in seconds. Must not be negative;
        a value of ``0.0`` (or a missing ``prev``) simply means no finite
        difference is available and the unsupplied derivatives stay at zero.

    Returns
    -------
    A mapping with the keys ``ax``, ``ay``, ``az``, ``accel_long``,
    ``accel_lat``, ``yaw_rate`` and ``speed``, ready to be handed to
    :func:`make_telemetry`.

    Raises
    ------
    ValueError
        If ``dt`` is negative (samples supplied out of order) or ``"yaw"`` is
        missing. Both are wiring bugs that must not be papered over: a silently
        zeroed yaw rate would suppress every heading-change event downstream.
    """
    if float(dt) < 0.0:
        raise ValueError(
            "derive_motion received a negative dt ({0!r}); telemetry samples must "
            "be supplied in non-decreasing simulation-time order".format(dt)
        )
    if "yaw" not in cur_raw or cur_raw["yaw"] is None:
        raise ValueError("derive_motion requires a 'yaw' reading in cur_raw")

    step = float(dt)
    can_difference = prev is not None and step > 0.0

    yaw = float(cur_raw["yaw"])
    vx = _as_float(cur_raw.get("vx"), 0.0)
    vy = _as_float(cur_raw.get("vy"), 0.0)
    vz = _as_float(cur_raw.get("vz"), 0.0)

    ax = _supplied_or_difference(
        cur_raw.get("ax"), vx, prev.vx if prev is not None else 0.0, step, can_difference
    )
    ay = _supplied_or_difference(
        cur_raw.get("ay"), vy, prev.vy if prev is not None else 0.0, step, can_difference
    )
    az = _supplied_or_difference(
        cur_raw.get("az"), vz, prev.vz if prev is not None else 0.0, step, can_difference
    )

    supplied_rate = cur_raw.get("yaw_rate")
    if supplied_rate is not None:
        yaw_rate = float(supplied_rate)
    elif can_difference:
        # Wrap the difference: a heading crossing +/-180 deg must not read as a
        # ~360 deg/s spike, which would fire a spurious heading-change event.
        yaw_rate = angle_diff_deg(yaw, float(prev.yaw)) / step  # type: ignore[union-attr]
    else:
        yaw_rate = 0.0

    accel_long, accel_lat = body_frame_acceleration(ax, ay, yaw)

    return {
        "ax": ax,
        "ay": ay,
        "az": az,
        "accel_long": accel_long,
        "accel_lat": accel_lat,
        "yaw_rate": yaw_rate,
        "speed": ground_speed(vx, vy),
    }


def ground_speed(vx: float, vy: float) -> float:
    """Planar speed magnitude in m/s.

    The vertical component is deliberately excluded: ``TelemetrySample.speed`` is
    defined as *ground* speed, and on a slope or during the settle-in after spawn
    ``vz`` is a suspension artifact rather than travel.
    """
    return math.hypot(float(vx), float(vy))


def make_telemetry(
    participant_id: str,
    t: float,
    frame: int,
    x: float,
    y: float,
    z: float = 0.0,
    yaw: float = 0.0,
    pitch: float = 0.0,
    roll: float = 0.0,
    vx: float = 0.0,
    vy: float = 0.0,
    vz: float = 0.0,
    ax: float = 0.0,
    ay: float = 0.0,
    az: float = 0.0,
    yaw_rate: float = 0.0,
) -> TelemetrySample:
    """Build a :class:`TelemetrySample` with the derived quantities filled in.

    ``speed``, ``accel_long`` and ``accel_lat`` are computed here rather than at
    the call sites so that every producer of telemetry -- the live recorder, the
    replay tooling and the test fixtures -- agrees on the definitions.

    The accelerations are taken as already-known world-frame values; callers that
    must reconstruct them from a velocity history run :func:`derive_motion`
    first and splat its result into this constructor.
    """
    accel_long, accel_lat = body_frame_acceleration(ax, ay, yaw)
    return TelemetrySample(
        t=float(t),
        frame=int(frame),
        participant_id=str(participant_id),
        x=float(x),
        y=float(y),
        z=float(z),
        yaw=float(yaw),
        pitch=float(pitch),
        roll=float(roll),
        vx=float(vx),
        vy=float(vy),
        vz=float(vz),
        speed=ground_speed(vx, vy),
        ax=float(ax),
        ay=float(ay),
        az=float(az),
        accel_long=accel_long,
        accel_lat=accel_lat,
        yaw_rate=float(yaw_rate),
    )


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _as_float(value: Any, default: float) -> float:
    """``float(value)`` with ``None`` mapped to ``default``."""
    return default if value is None else float(value)


def _supplied_or_difference(
    supplied: Any, cur_v: float, prev_v: float, dt: float, can_difference: bool
) -> float:
    """Trust a measured derivative, else finite-difference the velocity."""
    if supplied is not None:
        return float(supplied)
    if can_difference:
        return (float(cur_v) - float(prev_v)) / float(dt)
    return 0.0
