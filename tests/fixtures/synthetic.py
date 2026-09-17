"""Complete, simulator-free runs for the integration test-suite.

Why this module exists
----------------------
The whole inference stack -- local event extraction, local causal graphs, fusion,
model checking, evaluation -- reads *persisted artifacts*, never a live
simulator. That separation is only worth something if it is exercised: this
module therefore synthesises physically plausible encounters and writes them into
a real :class:`~cdf.common.layout.RunLayout`, so the entire downstream pipeline
can be driven end to end with no CARLA server anywhere in the loop.

What "physically plausible" means here
-------------------------------------
* **One kinematic model, integrated once.** Every participant is a point mass
  following a straight line with an optional lateral manoeuvre and an optional
  braking phase. Position, velocity and acceleration are produced by a single
  Euler integration, so ``p[k] - p[k-1] == v[k] * dt`` holds *exactly* and the
  recorded telemetry cannot disagree with itself.
* **Radar returns are derived from the true relative geometry**, by inverting
  :func:`cdf.common.geometry.polar_to_body`: reflection points are placed on the
  face of the target vehicle that actually faces the observing radar, expressed
  in the observer's body frame, and then converted back into the sensor-polar
  ``(depth, azimuth, altitude)`` triple the recorder would have stored. The
  range-rate channel is the radial component of the true relative velocity, so
  its sign obeys the radar convention used everywhere in this project:
  **negative means closing**.
* **The real perception chain runs on those returns.** The synthetic frames are
  pushed through :class:`cdf.local.radar.RadarFrontEnd` and
  :class:`cdf.local.tracking.RadarTracker` -- the production code -- so the
  tracks on disk are produced by the same clustering, gating and smoothing a
  recorded run uses. Nothing writes a track by hand.

Documented simplifications
--------------------------
These are approximations, not hidden ones; a test that depends on any of them
should say so.

* Reflection points are placed at the radar's own mounting height, so the
  ``altitude`` channel is exactly zero and the elevation gate of
  ``radar_processing.filter`` is not exercised by these fixtures.
* The lever-arm term ``omega x r`` between the vehicle origin and the radar
  mounting point is neglected in the range-rate computation; it is of the order
  of ``yaw_rate * 2.2 m`` and is negligible for the near-straight motion used
  here.
* Contact between two vehicles is tested with the oriented bounding boxes'
  support radii along the line joining their centres, which is exact for the
  aligned (rear-end) case and slightly conservative for an oblique impact.
* The post-impact phase applies a hard deceleration to *both* vehicles. A real
  impact accelerates the struck vehicle forward; what the local layer reads from
  it is only "an impact happened, then I came to rest", which this reproduces.
* :func:`synthetic_partial_view` emulates occlusion by *not generating* the
  returns that the middle vehicle would block. This is a TEST FIXTURE
  convenience: the real S07 measurement (``configs/scenarios/s07_partial_view``)
  obtains the same missing evidence from genuine sensor occlusion plus a
  narrow-field-of-view radar in CARLA, and no graph element is ever deleted
  after inference in either case.

Layers
------
This module sits on the *privileged* side of the data boundary: it is the
generator of ground truth, so it may write the oracle trace (including actor ids
and lane labels) exactly as :mod:`cdf.oracle.logger` would. The per-participant
artifacts it writes contain only what that participant's own sensors could have
produced, which is what
``tests/test_no_privileged_leakage.py`` independently verifies.

Determinism
-----------
The only randomness is a seeded :class:`random.Random` handed to the radar
front-end (it draws nothing at all unless a degraded sensor profile is
selected). No wall-clock value is written to any artifact.
"""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from cdf.common.config import Config, load_run_config
from cdf.common.evidence import ParticipantEvidence, save_participant
from cdf.common.geometry import (
    angle_diff_deg,
    deg2rad,
    global_to_body,
    heading_from_velocity,
    polar_to_body,
    rotate2d,
)
from cdf.common.io import write_json, write_jsonl_gz
from cdf.common.layout import RunLayout
from cdf.common.schemas import (
    ControlSample,
    LocalTriggerRecord,
    OutcomeClass,
    ParticipantManifest,
    RadarDetection,
    RadarFrame,
    RunManifest,
    TelemetrySample,
    TrackSample,
    TriggerKind,
    to_jsonable,
)
from cdf.local.radar import RadarFrontEnd
from cdf.local.tracking import RadarTracker
from cdf.oracle.logger import ORACLE_TRACE_SCHEMA_VERSION, OracleActorState

__all__ = [
    "SyntheticVehicle",
    "SyntheticScene",
    "body_point_to_polar",
    "build_run",
    "oracle_check_input",
    "oracle_trace_rows",
    "synthetic_rear_end",
    "synthetic_cut_in",
    "synthetic_crossing",
    "synthetic_partial_view",
]


# ---------------------------------------------------------------------------
# Vehicle model parameters
# ---------------------------------------------------------------------------
# These describe the synthetic *scene*, in the same way a scenario YAML file
# describes a CARLA scene. They are deliberately not pipeline thresholds: every
# threshold the pipeline applies is read from the :class:`Config` handed in.

#: Bounding-box length and width of every synthetic vehicle, metres. Close to a
#: mid-size saloon (the CARLA ``vehicle.tesla.model3`` is 4.79 x 2.16 m).
VEHICLE_LENGTH_M = 4.70
VEHICLE_WIDTH_M = 1.90

#: Mass used to turn an impact speed into a collision impulse, kilograms.
VEHICLE_MASS_KG = 1500.0

#: Deceleration produced by a full (1.0) brake command, m/s^2. Roughly the
#: 0.8 g a passenger car reaches on dry asphalt.
FULL_BRAKE_DECEL_MPS2 = 8.0

#: Deceleration applied to both vehicles after an impact, m/s^2.
POST_IMPACT_DECEL_MPS2 = 9.0

#: Throttle command reported while cruising at the target speed. The synthetic
#: vehicles hold speed exactly, so this is a plausible recorded command rather
#: than a quantity the model consumes.
CRUISE_THROTTLE = 0.30

#: Yaw rate (deg/s) that corresponds to a full steering command, used to turn
#: the model's yaw rate into a plausible recorded steer command.
FULL_STEER_YAW_RATE_DEG_S = 30.0

#: Reflection points generated along the illuminated face of a target. Five
#: points spaced over a 4.7 m face sit 1.175 m apart, which is inside the
#: ``radar_processing.cluster.eps_m`` neighbourhood, so the front-end sees one
#: coherent object rather than a shattered one.
N_REFLECTION_POINTS = 5

#: Frame number of the first recorded step. CARLA frame counters never start at
#: zero; using a non-zero base keeps the fixtures honest about that.
FIRST_FRAME = 1000

#: Tolerance of the polar/body round-trip self-check, metres.
_ROUNDTRIP_TOL_M = 1e-6


# ---------------------------------------------------------------------------
# Scene description
# ---------------------------------------------------------------------------


@dataclass
class SyntheticVehicle:
    """One participant of a synthetic encounter.

    The trajectory is a straight line along ``heading_deg`` from ``(x0, y0)``,
    optionally displaced sideways by ``lateral_offset_m`` over a smooth window
    (the cut-in manoeuvre) and optionally braked from ``brake_start_s``.
    """

    participant_id: str
    x0: float
    y0: float
    heading_deg: float
    speed_mps: float

    brake_start_s: Optional[float] = None
    brake_intensity: float = 0.0
    brake_duration_s: float = 10.0

    lateral_offset_m: float = 0.0
    lateral_start_s: Optional[float] = None
    lateral_duration_s: float = 2.5

    blind_to: Tuple[str, ...] = ()
    """Participants whose returns this vehicle's radar never receives.

    TEST FIXTURE ONLY -- see the module docstring: this emulates occlusion by
    omission, where the real S07 scenario obtains it from genuine geometry."""

    # --- privileged scene labels: written to the oracle trace only ---
    actor_id: int = 0
    lane_id: int = -2
    road_id: int = 37

    def forward(self) -> Tuple[float, float]:
        """Unit vector along the vehicle's nominal heading, global frame."""
        return rotate2d(1.0, 0.0, self.heading_deg)

    def right(self) -> Tuple[float, float]:
        """Unit vector 90 degrees to the right of the nominal heading."""
        return rotate2d(0.0, 1.0, self.heading_deg)


@dataclass
class SyntheticScene:
    """A complete synthetic run: participants, duration and labelling."""

    scenario_id: str
    name: str
    variant: str
    duration_s: float
    vehicles: List[SyntheticVehicle]
    notes: List[str] = field(default_factory=list)

    def ids(self) -> List[str]:
        return [v.participant_id for v in self.vehicles]


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------


def body_point_to_polar(
    bx: float,
    by: float,
    bz: float,
    sensor_x: float = 0.0,
    sensor_y: float = 0.0,
    sensor_z: float = 0.0,
    sensor_yaw_deg: float = 0.0,
) -> Tuple[float, float, float]:
    """Exact inverse of :func:`cdf.common.geometry.polar_to_body`.

    Turns a point expressed in the observer's body frame into the
    ``(depth, azimuth, altitude)`` triple a radar mounted with the given
    extrinsics would have reported for it. Generating detections this way -- and
    round-tripping them back through the production transform -- is what makes
    the synthetic returns physically consistent with the scene instead of merely
    plausible-looking.
    """
    px = float(bx) - float(sensor_x)
    py = float(by) - float(sensor_y)
    pz = float(bz) - float(sensor_z)
    qx, qy = rotate2d(px, py, -float(sensor_yaw_deg))
    horiz = math.hypot(qx, qy)
    depth = math.hypot(horiz, pz)
    if depth <= 1e-9:
        raise ValueError(
            "cannot build a radar return for a point at the sensor origin "
            "(body point {0!r})".format((bx, by, bz))
        )
    return (depth, math.atan2(qy, qx), math.asin(pz / depth))


def _rect_corners(
    cx: float, cy: float, yaw_deg: float, length: float, width: float
) -> List[Tuple[float, float]]:
    """The four corners of a vehicle's oriented bounding box, global frame."""
    half_l, half_w = 0.5 * float(length), 0.5 * float(width)
    local = [
        (half_l, -half_w),
        (half_l, half_w),
        (-half_l, half_w),
        (-half_l, -half_w),
    ]
    out: List[Tuple[float, float]] = []
    for lx, ly in local:
        gx, gy = rotate2d(lx, ly, yaw_deg)
        out.append((float(cx) + gx, float(cy) + gy))
    return out


def _support_radius(yaw_deg: float, direction_deg: float, length: float, width: float) -> float:
    """Half-extent of an oriented box along ``direction_deg``.

    This is the box's support function, i.e. the exact distance from the centre
    to the box boundary measured along that direction for an axis-aligned
    approach and a conservative over-estimate for an oblique one.
    """
    phi = deg2rad(angle_diff_deg(direction_deg, yaw_deg))
    return 0.5 * (float(length) * abs(math.cos(phi)) + float(width) * abs(math.sin(phi)))


def _illuminated_face(
    cx: float,
    cy: float,
    yaw_deg: float,
    observer_x: float,
    observer_y: float,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """The two corners of the target face that points back at the observer.

    A radar illuminates the face it faces: for a vehicle being followed that is
    its rear face, for one crossing in front it is a flank. Picking the face by
    the outward normal most opposed to the observer's line of sight reproduces
    that without any special-casing per scenario.
    """
    corners = _rect_corners(cx, cy, yaw_deg, VEHICLE_LENGTH_M, VEHICLE_WIDTH_M)
    # Faces as (corner_a, corner_b, outward normal heading in degrees).
    faces = (
        (corners[0], corners[1], yaw_deg),           # front
        (corners[2], corners[3], yaw_deg + 180.0),   # rear
        (corners[1], corners[2], yaw_deg + 90.0),    # right flank
        (corners[3], corners[0], yaw_deg - 90.0),    # left flank
    )
    los = math.atan2(float(cy) - float(observer_y), float(cx) - float(observer_x))
    los_deg = los * 180.0 / math.pi

    best = None
    best_score = None
    for a, b, normal_deg in faces:
        # cos of the angle between the face normal and the line of sight: -1
        # means the face stares straight back at the observer.
        score = math.cos(deg2rad(angle_diff_deg(normal_deg, los_deg)))
        if best_score is None or score < best_score:
            best_score = score
            best = (a, b)
    if best is None:  # pragma: no cover - the face list is never empty
        raise RuntimeError("no illuminated face found")
    return best


# ---------------------------------------------------------------------------
# Kinematic simulation
# ---------------------------------------------------------------------------


@dataclass
class _State:
    """Exact state of one vehicle at one simulation step."""

    t: float
    frame: int
    x: float
    y: float
    yaw: float
    vx: float
    vy: float
    speed: float
    ax: float
    ay: float
    accel_long: float
    accel_lat: float
    yaw_rate: float
    throttle: float
    brake: float
    steer: float


@dataclass
class _Contact:
    """A true contact between two participants. PRIVILEGED."""

    t: float
    frame: int
    a: str
    b: str
    impulse: float


def _lateral_offset(vehicle: SyntheticVehicle, t: float) -> float:
    """Smooth (raised-cosine) lateral displacement profile, metres.

    A raised cosine has zero slope at both ends, so the manoeuvre starts and
    finishes without a step in lateral velocity -- which is what keeps the
    derived yaw rate and steer command physically reasonable.
    """
    if vehicle.lateral_start_s is None or vehicle.lateral_offset_m == 0.0:
        return 0.0
    u = (float(t) - float(vehicle.lateral_start_s)) / float(vehicle.lateral_duration_s)
    u = max(0.0, min(1.0, u))
    return float(vehicle.lateral_offset_m) * 0.5 * (1.0 - math.cos(math.pi * u))


def _commanded_accel(
    vehicle: SyntheticVehicle, t: float, impact_t: Optional[float]
) -> Tuple[float, float, float]:
    """``(accel, throttle, brake)`` commanded at time ``t``."""
    if impact_t is not None and t >= impact_t:
        return (-POST_IMPACT_DECEL_MPS2, 0.0, 1.0)
    start = vehicle.brake_start_s
    if start is not None and start <= t < start + vehicle.brake_duration_s:
        intensity = float(vehicle.brake_intensity)
        return (-intensity * FULL_BRAKE_DECEL_MPS2, 0.0, intensity)
    return (0.0, CRUISE_THROTTLE, 0.0)


def _simulate(
    scene: SyntheticScene, dt: float
) -> Tuple[Dict[str, List[_State]], List[_Contact]]:
    """Integrate the whole scene, detecting true contacts as they happen.

    All vehicles advance together because contact couples them: the struck and
    striking vehicles both switch to their post-impact deceleration at the same
    instant.
    """
    n_steps = int(round(float(scene.duration_s) / float(dt)))
    if n_steps < 2:
        raise ValueError(
            "a synthetic scene needs at least two steps; duration={0} dt={1}".format(
                scene.duration_s, dt
            )
        )

    speed = {v.participant_id: float(v.speed_mps) for v in scene.vehicles}
    pos = {v.participant_id: (float(v.x0), float(v.y0)) for v in scene.vehicles}
    prev_vel: Dict[str, Tuple[float, float]] = {}
    prev_yaw = {v.participant_id: float(v.heading_deg) for v in scene.vehicles}
    impact_t: Dict[str, Optional[float]] = {v.participant_id: None for v in scene.vehicles}

    states: Dict[str, List[_State]] = {v.participant_id: [] for v in scene.vehicles}
    contacts: List[_Contact] = []
    collided: set = set()

    for k in range(n_steps):
        t = round((k + 1) * float(dt), 9)
        frame = FIRST_FRAME + k

        for vehicle in scene.vehicles:
            pid = vehicle.participant_id
            accel, throttle, brake = _commanded_accel(vehicle, t, impact_t[pid])
            speed[pid] = max(0.0, speed[pid] + accel * dt)

            lat = _lateral_offset(vehicle, t)
            lat_prev = _lateral_offset(vehicle, t - dt)
            lat_rate = (lat - lat_prev) / float(dt)

            fx, fy = vehicle.forward()
            rx, ry = vehicle.right()
            vx = fx * speed[pid] + rx * lat_rate
            vy = fy * speed[pid] + ry * lat_rate

            px, py = pos[pid]
            pos[pid] = (px + vx * dt, py + vy * dt)

            pvx, pvy = prev_vel.get(pid, (vx, vy))
            ax = (vx - pvx) / float(dt)
            ay = (vy - pvy) / float(dt)
            prev_vel[pid] = (vx, vy)

            yaw = heading_from_velocity(vx, vy, fallback=prev_yaw[pid])
            yaw_rate = angle_diff_deg(yaw, prev_yaw[pid]) / float(dt)
            prev_yaw[pid] = yaw

            along, lateral_accel = rotate2d(ax, ay, -yaw)
            steer = max(-1.0, min(1.0, yaw_rate / FULL_STEER_YAW_RATE_DEG_S))

            states[pid].append(
                _State(
                    t=t,
                    frame=frame,
                    x=pos[pid][0],
                    y=pos[pid][1],
                    yaw=yaw,
                    vx=vx,
                    vy=vy,
                    speed=math.hypot(vx, vy),
                    ax=ax,
                    ay=ay,
                    accel_long=along,
                    accel_lat=lateral_accel,
                    yaw_rate=yaw_rate,
                    throttle=throttle,
                    brake=brake,
                    steer=steer,
                )
            )

        for i in range(len(scene.vehicles)):
            for j in range(i + 1, len(scene.vehicles)):
                va, vb = scene.vehicles[i], scene.vehicles[j]
                key = (va.participant_id, vb.participant_id)
                if key in collided:
                    continue
                sa, sb = states[va.participant_id][-1], states[vb.participant_id][-1]
                dx, dy = sb.x - sa.x, sb.y - sa.y
                gap = math.hypot(dx, dy)
                line_deg = math.atan2(dy, dx) * 180.0 / math.pi
                touch = _support_radius(
                    sa.yaw, line_deg, VEHICLE_LENGTH_M, VEHICLE_WIDTH_M
                ) + _support_radius(
                    sb.yaw, line_deg + 180.0, VEHICLE_LENGTH_M, VEHICLE_WIDTH_M
                )
                if gap > touch:
                    continue
                rel_speed = math.hypot(sb.vx - sa.vx, sb.vy - sa.vy)
                collided.add(key)
                impact_t[va.participant_id] = t
                impact_t[vb.participant_id] = t
                contacts.append(
                    _Contact(
                        t=t,
                        frame=frame,
                        a=va.participant_id,
                        b=vb.participant_id,
                        impulse=VEHICLE_MASS_KG * rel_speed,
                    )
                )

    return states, contacts


# ---------------------------------------------------------------------------
# Sensor synthesis
# ---------------------------------------------------------------------------


@dataclass
class _SensorSpec:
    """The radar mounting and field of view taken from the resolved config."""

    sensor_id: str
    mount_x: float
    mount_y: float
    mount_z: float
    mount_yaw_deg: float
    half_fov_rad: float
    range_m: float


def _sensor_spec(cfg: Config) -> _SensorSpec:
    """Read the first radar of the active sensor profile.

    Reading it from the configuration rather than hard-coding it is what keeps
    the synthetic returns consistent with whatever profile a test selects.
    """
    sensors = cfg.get("radar.sensors", []) or []
    if not sensors:
        raise KeyError(
            "the resolved configuration defines no radar under 'radar.sensors'; "
            "a synthetic run cannot generate returns without a sensor definition"
        )
    entry = sensors[0]
    mount = entry.get("mount", {}) or {}
    return _SensorSpec(
        sensor_id=str(entry.get("sensor_id", "front")),
        mount_x=float(mount.get("x", 2.2)),
        mount_y=float(mount.get("y", 0.0)),
        mount_z=float(mount.get("z", 1.0)),
        mount_yaw_deg=float(mount.get("yaw_deg", 0.0)),
        half_fov_rad=0.5 * deg2rad(float(entry.get("horizontal_fov_deg", 120.0))),
        range_m=float(entry.get("range_m", 90.0)),
    )


def _radar_frame(
    observer: SyntheticVehicle,
    own: _State,
    others: Sequence[Tuple[SyntheticVehicle, _State]],
    spec: _SensorSpec,
) -> RadarFrame:
    """Build one radar frame from the true geometry of the scene.

    For every visible target the illuminated face is sampled at
    :data:`N_REFLECTION_POINTS` points; each point is transformed into the
    observer's body frame, inverted into sensor-polar coordinates and paired with
    the radial component of the true relative velocity. No property of the target
    other than its shape and motion enters -- and none of it survives into the
    recorded frame, which carries only ``(depth, azimuth, altitude, velocity)``.
    """
    detections: List[RadarDetection] = []

    sensor_off_x, sensor_off_y = rotate2d(spec.mount_x, spec.mount_y, own.yaw)
    sensor_gx = own.x + sensor_off_x
    sensor_gy = own.y + sensor_off_y

    for target, tstate in others:
        if target.participant_id in observer.blind_to:
            # TEST FIXTURE emulation of occlusion -- see the module docstring.
            continue
        corner_a, corner_b = _illuminated_face(
            tstate.x, tstate.y, tstate.yaw, sensor_gx, sensor_gy
        )
        for idx in range(N_REFLECTION_POINTS):
            u = idx / float(N_REFLECTION_POINTS - 1)
            gx = corner_a[0] + u * (corner_b[0] - corner_a[0])
            gy = corner_a[1] + u * (corner_b[1] - corner_a[1])

            bx, by = global_to_body(gx, gy, own.x, own.y, own.yaw)
            depth, azimuth, altitude = body_point_to_polar(
                bx,
                by,
                spec.mount_z,  # reflection at the radar's own height => altitude 0
                spec.mount_x,
                spec.mount_y,
                spec.mount_z,
                spec.mount_yaw_deg,
            )
            if depth > spec.range_m or abs(azimuth) > spec.half_fov_rad:
                continue

            # Self-check: the production transform must recover the body point we
            # started from. A silent disagreement here would mean the fixture is
            # feeding the pipeline geometry that cannot exist.
            rx, ry, _rz = polar_to_body(
                depth,
                azimuth,
                altitude,
                spec.mount_x,
                spec.mount_y,
                spec.mount_z,
                spec.mount_yaw_deg,
            )
            if abs(rx - bx) > _ROUNDTRIP_TOL_M or abs(ry - by) > _ROUNDTRIP_TOL_M:
                raise AssertionError(
                    "radar polar/body round-trip disagrees by more than {0} m: "
                    "body=({1}, {2}) recovered=({3}, {4})".format(
                        _ROUNDTRIP_TOL_M, bx, by, rx, ry
                    )
                )

            los_x = gx - sensor_gx
            los_y = gy - sensor_gy
            norm = math.hypot(los_x, los_y)
            if norm <= 1e-9:  # pragma: no cover - guarded by the depth gate above
                continue
            # Radar convention: velocity is d(depth)/dt, so a target that is
            # being approached reports a NEGATIVE value.
            range_rate = (
                (tstate.vx - own.vx) * (los_x / norm)
                + (tstate.vy - own.vy) * (los_y / norm)
            )
            detections.append(
                RadarDetection(
                    depth=depth,
                    azimuth=azimuth,
                    altitude=altitude,
                    velocity=range_rate,
                )
            )

    return RadarFrame(
        t=own.t,
        frame=own.frame,
        participant_id=observer.participant_id,
        sensor_id=spec.sensor_id,
        detections=detections,
        sensor_yaw=spec.mount_yaw_deg,
        sensor_x=spec.mount_x,
        sensor_y=spec.mount_y,
        sensor_z=spec.mount_z,
    )


# ---------------------------------------------------------------------------
# Per-participant evidence
# ---------------------------------------------------------------------------


def _triggers(
    cfg: Config,
    pid: str,
    telemetry: Sequence[TelemetrySample],
    controls: Sequence[ControlSample],
    tracks_by_step: Sequence[Sequence[TrackSample]],
    contacts: Sequence[_Contact],
) -> List[LocalTriggerRecord]:
    """Evaluate the recorder triggers from ONBOARD evidence only.

    This mirrors :meth:`cdf.simulation.vehicle_agent.ParticipantAgent._handle_triggers`
    exactly, including the "armed once" behaviour, so the synthetic triggers are
    the ones a recorded run would have produced. The collision trigger is the
    only one derived from the privileged contact list -- and it carries only what
    an onboard collision sensor reports: that an impact happened, when, and how
    hard. The identity of the other party is not recorded.
    """
    out: List[LocalTriggerRecord] = []

    min_impulse = float(cfg.get("recorder.triggers.collision.min_impulse", 1.0))
    for contact in contacts:
        if pid not in (contact.a, contact.b):
            continue
        if contact.impulse < min_impulse:
            continue
        out.append(
            LocalTriggerRecord(
                t=float(contact.t),
                frame=int(contact.frame),
                participant_id=pid,
                kind=TriggerKind.COLLISION,
                collision_detected=True,
                impulse=float(contact.impulse),
                detail={"source": "onboard_collision_sensor"},
            )
        )

    near_miss_armed = bool(cfg.get("recorder.triggers.near_miss.enabled", True))
    ttc_thr = float(cfg.get("recorder.triggers.near_miss.ttc_s", 0.9))
    range_thr = float(cfg.get("recorder.triggers.near_miss.min_range_m", 12.0))
    brake_armed = bool(cfg.get("recorder.triggers.emergency_brake.enabled", True))
    brake_thr = float(cfg.get("recorder.triggers.emergency_brake.brake_cmd", 0.85))
    decel_thr = float(cfg.get("recorder.triggers.emergency_brake.decel_mps2", 5.5))

    for idx, samples in enumerate(tracks_by_step):
        tel = telemetry[idx]
        ctl = controls[idx]
        if near_miss_armed:
            for s in samples:
                if s.ttc is not None and s.ttc <= ttc_thr and s.range_m <= range_thr:
                    out.append(
                        LocalTriggerRecord(
                            t=float(tel.t),
                            frame=int(tel.frame),
                            participant_id=pid,
                            kind=TriggerKind.NEAR_MISS,
                            collision_detected=False,
                            impulse=0.0,
                            detail={
                                "ttc": float(s.ttc),
                                "range_m": float(s.range_m),
                                "track_id": s.track_id,
                                "source": "local_ttc",
                            },
                        )
                    )
                    near_miss_armed = False
                    break
        if brake_armed and ctl.brake >= brake_thr and tel.accel_long <= -decel_thr:
            out.append(
                LocalTriggerRecord(
                    t=float(tel.t),
                    frame=int(tel.frame),
                    participant_id=pid,
                    kind=TriggerKind.EMERGENCY_BRAKE,
                    collision_detected=False,
                    impulse=0.0,
                    detail={
                        "brake": float(ctl.brake),
                        "accel_long": float(tel.accel_long),
                        "source": "local_control",
                    },
                )
            )
            brake_armed = False

    out.sort(key=lambda r: (float(r.t), r.kind.value))
    return out


def _build_participant(
    scene: SyntheticScene,
    vehicle: SyntheticVehicle,
    states: Dict[str, List[_State]],
    contacts: Sequence[_Contact],
    cfg: Config,
    spec: _SensorSpec,
    seed: int,
) -> Tuple[ParticipantEvidence, List[RadarFrame]]:
    """Run one participant's onboard stack over the synthetic scene."""
    pid = vehicle.participant_id
    others = [v for v in scene.vehicles if v.participant_id != pid]

    front_end = RadarFrontEnd(cfg, pid, rng=random.Random(seed))
    tracker = RadarTracker(cfg, pid)

    telemetry: List[TelemetrySample] = []
    controls: List[ControlSample] = []
    radar: List[RadarFrame] = []
    tracks: List[TrackSample] = []
    tracks_by_step: List[List[TrackSample]] = []

    for idx, own in enumerate(states[pid]):
        sample = TelemetrySample(
            t=own.t,
            frame=own.frame,
            participant_id=pid,
            x=own.x,
            y=own.y,
            z=0.0,
            yaw=own.yaw,
            vx=own.vx,
            vy=own.vy,
            vz=0.0,
            speed=own.speed,
            ax=own.ax,
            ay=own.ay,
            az=0.0,
            accel_long=own.accel_long,
            accel_lat=own.accel_lat,
            yaw_rate=own.yaw_rate,
        )
        control = ControlSample(
            t=own.t,
            frame=own.frame,
            participant_id=pid,
            throttle=own.throttle,
            brake=own.brake,
            steer=own.steer,
        )

        frame = _radar_frame(
            vehicle,
            own,
            [(other, states[other.participant_id][idx]) for other in others],
            spec,
        )
        clusters = front_end.process(frame, sample)
        step_tracks = tracker.update(own.t, own.frame, clusters, sample)

        telemetry.append(sample)
        controls.append(control)
        radar.append(frame)
        tracks.extend(step_tracks)
        tracks_by_step.append(list(step_tracks))

    triggers = _triggers(cfg, pid, telemetry, controls, tracks_by_step, contacts)

    evidence = ParticipantEvidence(
        participant_id=pid,
        telemetry=telemetry,
        controls=controls,
        radar=radar,
        tracks=tracks,
        triggers=triggers,
        events=[],
        meta={
            "source": "synthetic_fixture",
            "sensor_profile": str(cfg.get("sensors.profile", "radar_baseline")),
            "n_radar_frames": len(radar),
            "n_track_samples": len(tracks),
        },
    )
    return evidence, radar


# ---------------------------------------------------------------------------
# Oracle trace (privileged)
# ---------------------------------------------------------------------------


def _oracle_rows(
    scene: SyntheticScene, states: Dict[str, List[_State]]
) -> List[Dict[str, Any]]:
    """Per-frame privileged trace, in the shape :mod:`cdf.oracle.logger` writes."""
    rows: List[Dict[str, Any]] = []
    by_id = {v.participant_id: v for v in scene.vehicles}
    n = len(states[scene.vehicles[0].participant_id])
    for idx in range(n):
        actors: List[Dict[str, Any]] = []
        for pid in sorted(states):
            st = states[pid][idx]
            vehicle = by_id[pid]
            actors.append(
                asdict(
                    OracleActorState(
                        participant_id=pid,
                        actor_id=vehicle.actor_id,
                        x=st.x,
                        y=st.y,
                        z=0.0,
                        yaw=st.yaw,
                        pitch=0.0,
                        roll=0.0,
                        vx=st.vx,
                        vy=st.vy,
                        vz=0.0,
                        speed=st.speed,
                        ax=st.ax,
                        ay=st.ay,
                        az=0.0,
                        yaw_rate=st.yaw_rate,
                        throttle=st.throttle,
                        brake=st.brake,
                        steer=st.steer,
                        lane_id=vehicle.lane_id,
                        road_id=vehicle.road_id,
                        section_id=0,
                        is_junction=False,
                        junction_id=None,
                        traffic_light_state=None,
                        traffic_light_id=None,
                        is_at_traffic_light=False,
                    )
                )
            )
        first = states[sorted(states)[0]][idx]
        rows.append(
            {
                "t": first.t,
                "frame": first.frame,
                "actors": actors,
                "traffic_lights": [],
            }
        )
    return rows


def _oracle_summary(
    scene: SyntheticScene,
    run_id: str,
    seed: int,
    states: Dict[str, List[_State]],
    contacts: Sequence[_Contact],
) -> Dict[str, Any]:
    """Privileged run summary, including the true identity of both parties."""
    by_id = {v.participant_id: v for v in scene.vehicles}
    collisions: List[Dict[str, Any]] = []
    for contact in contacts:
        # CARLA reports an impact once per involved actor; mirror that here.
        for pid, other in ((contact.a, contact.b), (contact.b, contact.a)):
            collisions.append(
                {
                    "t": float(contact.t),
                    "frame": int(contact.frame),
                    "participant_id": pid,
                    "other_participant_id": other,
                    "other_actor_id": by_id[other].actor_id,
                    "other_type_id": "synthetic.kinematic.vehicle",
                    "impulse": float(contact.impulse),
                    "is_participant_pair": True,
                }
            )
    return {
        "schema_version": ORACLE_TRACE_SCHEMA_VERSION,
        "provenance": "oracle",
        "scenario_id": scene.scenario_id,
        "run_id": run_id,
        "seed": int(seed),
        "variant": scene.variant,
        "map_name": "synthetic",
        "participants": sorted(states),
        "n_frames": len(states[scene.vehicles[0].participant_id]),
        "collisions": collisions,
        "collision_pairs": [
            {"a": c.a, "b": c.b, "t": float(c.t)} for c in sorted(contacts, key=lambda c: c.t)
        ],
        "interventions": {},
        "notes": list(scene.notes),
    }


def oracle_trace_rows(layout: RunLayout) -> List[Dict[str, Any]]:
    """Read back the persisted privileged trace. PRIVILEGED -- evaluation only."""
    from cdf.common.io import read_jsonl_gz

    if not layout.oracle_trace.exists():
        raise FileNotFoundError(
            "no privileged trace at {0}; the run was not built by this "
            "fixture".format(layout.oracle_trace)
        )
    return read_jsonl_gz(layout.oracle_trace)


def oracle_check_input(layout: RunLayout) -> Dict[str, Any]:
    """The privileged trace in the shape :mod:`cdf.checking.properties` expects.

    The two oracle representations in the package have not been reconciled:
    :meth:`cdf.oracle.logger.OracleLogger.frame_rows` writes each instant as
    ``{"t", "frame", "actors": [ {..., "participant_id": pid} ]}`` -- a *list* --
    whereas ``cdf.checking.properties._oracle_samples`` reads ``{"samples":
    [{"t", "actors": {pid: {...}}}]}`` -- a *mapping* -- and silently reports
    ``UNKNOWN`` when it does not find it. Converting here, in one documented
    place, keeps every test honest about which shape it is feeding the checker
    instead of each one quietly inventing its own.

    The per-actor states are passed through unchanged, so the privileged fields
    the oracle properties need (``in_junction``, ``signal_state``) are absent
    exactly when the scene has no junction or signal -- which is what makes an
    ``UNKNOWN`` verdict the correct one rather than a masked failure.
    """
    from cdf.common.io import read_json

    samples: List[Dict[str, Any]] = []
    for row in oracle_trace_rows(layout):
        actors = {
            str(a["participant_id"]): dict(a) for a in row.get("actors", []) if "participant_id" in a
        }
        samples.append({"t": float(row["t"]), "frame": row.get("frame"), "actors": actors})

    summary_path = layout.oracle_dir / "oracle_summary.json"
    summary = read_json(summary_path) if summary_path.exists() else {}
    out = dict(summary)
    out["samples"] = samples
    return out


# ---------------------------------------------------------------------------
# Run assembly
# ---------------------------------------------------------------------------


def build_run(
    scene: SyntheticScene,
    tmp_root: Union[str, Path],
    cfg: Optional[Config] = None,
    seed: int = 0,
) -> RunLayout:
    """Simulate ``scene`` and persist it as a complete run directory.

    Returns the :class:`~cdf.common.layout.RunLayout` of the run, ready for
    :func:`cdf.local.pipeline.analyse_run` and :func:`cdf.fusion.pipeline.fuse_run`.
    """
    cfg = cfg if cfg is not None else load_run_config()
    dt = float(cfg.get("simulation.fixed_delta_seconds", 0.05))
    spec = _sensor_spec(cfg)

    states, contacts = _simulate(scene, dt)

    layout = RunLayout.create(tmp_root, scene.scenario_id, scene.name, seed, scene.variant)
    run_id = "{0}-{1}-seed{2:03d}-{3}".format(
        scene.scenario_id, scene.variant, int(seed), cfg.hash[:8]
    )

    participants: List[ParticipantManifest] = []
    for vehicle in scene.vehicles:
        evidence, radar = _build_participant(
            scene, vehicle, states, contacts, cfg, spec, seed
        )
        save_participant(layout, evidence)
        summary = evidence.summary()
        participants.append(
            ParticipantManifest(
                participant_id=vehicle.participant_id,
                blueprint="synthetic.kinematic.vehicle",
                spawn={"x": float(vehicle.x0), "y": float(vehicle.y0), "yaw": float(vehicle.heading_deg)},
                controller="SyntheticKinematicController",
                controller_params={
                    "initial_speed": float(vehicle.speed_mps),
                    "brake_start_s": vehicle.brake_start_s,
                    "brake_intensity": float(vehicle.brake_intensity),
                    "lateral_offset_m": float(vehicle.lateral_offset_m),
                },
                sensor_profile=str(cfg.get("sensors.profile", "radar_baseline")),
                radar_sensors=[{"sensor_id": spec.sensor_id, "range_m": spec.range_m}],
                n_telemetry=int(summary["n_telemetry"]),
                n_radar_frames=int(summary["n_radar_frames"]),
                n_track_samples=int(summary["n_track_samples"]),
                n_events=0,
                triggers=[to_jsonable(t) for t in evidence.triggers],
            )
        )

    outcome = OutcomeClass.COLLISION if contacts else OutcomeClass.NO_EVENT
    manifest = RunManifest(
        run_id=run_id,
        scenario_id=scene.scenario_id,
        variant=scene.variant,
        seed=int(seed),
        map_name="synthetic",
        fixed_delta_seconds=dt,
        synchronous_mode=True,
        config_hash=cfg.hash,
        config=cfg.data,
        participants=participants,
        # started_at/finished_at stay empty on purpose: a wall-clock stamp would
        # make the artifacts non-reproducible.
        duration_sim_s=float(scene.duration_s),
        n_frames=len(states[scene.vehicles[0].participant_id]),
        outcome=outcome,
        outcome_detail={
            "collision_pairs": [
                {"a": c.a, "b": c.b, "t": float(c.t)} for c in contacts
            ],
            "collided_participants": sorted({p for c in contacts for p in (c.a, c.b)}),
        },
        python_version="",
        carla_version="not-installed",
        platform="synthetic",
        package_version="",
        notes=["synthetic fixture run: no simulator was involved"] + list(scene.notes),
    )
    write_json(layout.manifest, manifest)

    layout.oracle_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl_gz(layout.oracle_trace, _oracle_rows(scene, states))
    write_json(
        layout.oracle_dir / "oracle_summary.json",
        _oracle_summary(scene, run_id, seed, states, contacts),
    )
    return layout


# ---------------------------------------------------------------------------
# The scenes
# ---------------------------------------------------------------------------


def synthetic_rear_end(
    tmp_root: Union[str, Path],
    seed: int = 0,
    collide: bool = True,
    cfg: Optional[Config] = None,
) -> RunLayout:
    """Two vehicles in one lane: A closes on the slower B and brakes late.

    With ``collide=True`` A brakes too late and strikes B, so the run carries a
    collision trigger, a critical-TTC episode before it and a post-impact stop.
    With ``collide=False`` A brakes early enough to stop short: the critical-TTC
    episode still occurs but resolves without contact, which is exactly the
    near-miss case the outcome layer must distinguish.

    B is the lead vehicle and its forward radar therefore holds no track at all,
    which reproduces the asymmetry of the recorded S01 run.
    """
    brake_start = 4.9 if collide else 4.3
    intensity = 0.85 if collide else 1.0
    scene = SyntheticScene(
        scenario_id="SYN01",
        name="rear_end",
        variant="crash" if collide else "avoided",
        duration_s=8.0,
        vehicles=[
            SyntheticVehicle(
                participant_id="A",
                x0=0.0,
                y0=0.0,
                heading_deg=0.0,
                speed_mps=14.0,
                brake_start_s=brake_start,
                brake_intensity=intensity,
                actor_id=101,
            ),
            SyntheticVehicle(
                participant_id="B",
                x0=30.0,
                y0=0.0,
                heading_deg=0.0,
                speed_mps=9.0,
                actor_id=102,
            ),
        ],
        notes=[
            "A follows B in the same lane at a 5 m/s speed differential",
            "A brakes at t={0:.2f}s with intensity {1:.2f}".format(brake_start, intensity),
        ],
    )
    return build_run(scene, tmp_root, cfg=cfg, seed=seed)


def synthetic_cut_in(
    tmp_root: Union[str, Path], seed: int = 0, cfg: Optional[Config] = None
) -> RunLayout:
    """B leaves the adjacent lane and settles into A's path ahead of it.

    The manoeuvre is a genuine lateral trajectory, not a labelled "lane change":
    A can only observe that the tracked object's lateral offset collapses towards
    its own longitudinal axis while it stays ahead -- which is precisely what
    ``CUT_IN_LIKE_MOTION`` is defined to mean.
    """
    scene = SyntheticScene(
        scenario_id="SYN02",
        name="cut_in",
        variant="crash",
        duration_s=8.0,
        vehicles=[
            SyntheticVehicle(
                participant_id="A",
                x0=0.0,
                y0=0.0,
                heading_deg=0.0,
                speed_mps=14.0,
                brake_start_s=4.6,
                brake_intensity=0.85,
                actor_id=201,
            ),
            SyntheticVehicle(
                participant_id="B",
                x0=32.0,
                y0=-3.5,
                heading_deg=0.0,
                speed_mps=9.0,
                lateral_offset_m=3.5,
                lateral_start_s=1.0,
                lateral_duration_s=2.5,
                actor_id=202,
                lane_id=-3,
            ),
        ],
        notes=[
            "B shifts 3.5 m laterally into A's path between t=1.0s and t=3.5s",
            "A is 5 m/s faster and reacts only at t=4.6s",
        ],
    )
    return build_run(scene, tmp_root, cfg=cfg, seed=seed)


def synthetic_crossing(
    tmp_root: Union[str, Path], seed: int = 0, cfg: Optional[Config] = None
) -> RunLayout:
    """Two vehicles on perpendicular straight paths that meet at the crossing.

    Neither participant is told that a junction exists: the conflict has to be
    inferred from the constant-bearing, decreasing-range geometry alone, by
    propagating both observed motions and intersecting the predictions. The
    encounter is arranged so that both arrive at the crossing point at the same
    instant, which is what makes the arrival-time gap -- and therefore the
    conflict score -- large.
    """
    scene = SyntheticScene(
        scenario_id="SYN03",
        name="crossing",
        variant="crash",
        duration_s=6.0,
        vehicles=[
            SyntheticVehicle(
                participant_id="A",
                x0=-45.0,
                y0=0.0,
                heading_deg=0.0,
                speed_mps=12.0,
                actor_id=301,
                road_id=41,
            ),
            SyntheticVehicle(
                participant_id="B",
                x0=0.0,
                y0=-45.0,
                heading_deg=90.0,
                speed_mps=12.0,
                actor_id=302,
                road_id=42,
                lane_id=-1,
            ),
        ],
        notes=[
            "A travels +x, B travels +y, both at 12 m/s from 45 m out",
            "constant bearing: the paths intersect at the origin at t=3.75s",
        ],
    )
    return build_run(scene, tmp_root, cfg=cfg, seed=seed)


def synthetic_partial_view(
    tmp_root: Union[str, Path], seed: int = 0, cfg: Optional[Config] = None
) -> RunLayout:
    """Three vehicles in one lane, where A cannot observe the lead vehicle C.

    C brakes hard first, B reacts and stops short of it, and A -- which never saw
    C at all -- closes on the now-stationary B and strikes it. A's local
    reconstruction is therefore missing the event that initiated the whole chain,
    while B's contains it; whether fusion recovers it is the measurement
    ``tests/integration/test_fusion_improvement.py`` performs.

    TEST FIXTURE NOTE -- the occlusion is emulated: A's radar frames simply omit
    every return that would have come from C, because B sits squarely between
    them for the whole run. The real S07 measurement obtains the same missing
    evidence from genuine sensor occlusion in CARLA (plus a narrow-field-of-view
    radar profile on A), and in neither case is anything removed from a graph
    after inference.
    """
    scene = SyntheticScene(
        scenario_id="SYN07",
        name="partial_view",
        variant="occluded",
        duration_s=10.0,
        vehicles=[
            SyntheticVehicle(
                participant_id="A",
                x0=0.0,
                y0=0.0,
                heading_deg=0.0,
                speed_mps=14.0,
                brake_start_s=5.4,
                brake_intensity=0.8,
                blind_to=("C",),
                actor_id=701,
            ),
            SyntheticVehicle(
                participant_id="B",
                x0=24.0,
                y0=0.0,
                heading_deg=0.0,
                speed_mps=14.0,
                brake_start_s=3.7,
                brake_intensity=1.0,
                actor_id=702,
            ),
            SyntheticVehicle(
                participant_id="C",
                x0=50.0,
                y0=0.0,
                heading_deg=0.0,
                speed_mps=14.0,
                brake_start_s=3.0,
                brake_intensity=1.0,
                actor_id=703,
            ),
        ],
        notes=[
            "C brakes first at t=3.0s; B reacts at t=3.7s; A reacts only at t=5.4s",
            "A's radar returns from C are suppressed: emulated occlusion by B",
        ],
    )
    return build_run(scene, tmp_root, cfg=cfg, seed=seed)
