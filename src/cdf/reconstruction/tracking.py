"""Anonymous local radar tracks: association, Kalman filter and RTS smoother.

raw detections of every radar of the recorder (front, left, right)
  -> each return placed in the recorder's own local odometric frame from ITS radar's mount
  -> each active track claims the returns inside its gate (gated association)
  -> left-over *moving* returns are clustered and start tentative tracks
  -> a tentative track that keeps receiving moving returns is confirmed and
     gets an anonymous id: track_001, track_002, ...
  -> each confirmed track is filtered forward (Kalman, constant velocity) and
     smoothed backward (Rauch-Tung-Striebel) into a local trajectory.

A confirmed track keeps claiming returns even when they look static, so a
vehicle that stops (a braking lead car) is not dropped.  A target that stops
abruptly (it crashes) changes its Doppler speed beyond the gate in one sweep:
a confirmed track whose surroundings were free of foreign returns may then
take the returns around it whose speed lies between standstill and the
predicted one (see ``_slowdown_gate``), and follows the target through the
crash.

Local odometric frame: origin at the recorder's first ego position, x along
its first heading, y to its right (CARLA's convention).  Every recorder has its
own frame; frames of different recorders are never compared.

Radar velocity convention, verified on the recordings: the CARLA detection
velocity is the range rate, negative while the range shrinks (static scenery
ahead of a recorder at speed v returns about -v*cos(azimuth)).

Geometry.  The recorder carries several radars at different places on its
body (``RadarMount``: position and orientation in the vehicle frame, read from
each radar's own metadata).  A return is placed from the position of the radar
that produced it, along that radar's line of sight, and its Doppler speed is
corrected by that radar's own velocity: the displacement of its mount point over
the last sweep, which carries the lever arm of a turning, pitching body.  Nothing
assumes a common origin for the returns of different radars.  The CLEARANCE of a
return is its distance to the recorder's own footprint (its bounding box,
``EgoFootprint``, vehicle frame); returns inside the footprint are the
recorder's own body and are dropped.  A track's clearance is that of its NEAR
surface: its returns are spread over the target's visible body, so the median
point that the Kalman filter follows lies deeper than the surface that will
touch first.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .config import TrackingConfig

# Velocity uncertainty of a newly started track (its tangential speed is unknown).
INITIAL_VELOCITY_STD_MPS = 10.0
# Below this closing speed a time-to-contact is not meaningful.
MIN_CLOSING_FOR_TTC_MPS = 0.1
# Returns whose ground point lies at least this far inside the recorder's own
# footprint come from its own body and are dropped.
OWN_BODY_MARGIN_M = 0.05
# A track's near surface in one sweep: this percentile of its returns' clearances
# (robust to one stray return, about the nearest one for few returns).
NEAR_SURFACE_PERCENTILE = 10.0
# The depth of the median point behind the near surface is smoothed over this
# many measured sweeps on each side (running median).
SURFACE_OFFSET_HALF_WINDOW = 2
# A target's acceleration along its own velocity: central difference of the
# smoothed velocity over this half window (s).
ACCELERATION_HALF_WINDOW_S = 0.15


# --------------------------------------------------------------------------
# The recorder's own motion in its local frame (self-localisation only)
# --------------------------------------------------------------------------

@dataclass
class EgoState:
    t_local: float
    x: float
    y: float
    heading: float  # radians; 0 = the recorder's first heading
    vx: float
    vy: float
    yaw_rate: float = 0.0  # rad/s, + = turning right (clockwise seen from above)
    z: float = 0.0  # height above the first pose
    pitch: float = 0.0  # radians, + = nose up (CARLA)
    roll: float = 0.0  # radians (CARLA)

    @property
    def speed(self) -> float:
        return math.hypot(self.vx, self.vy)


class EgoTrajectory:
    """The recorder's poses in its local frame, linearly interpolated in time."""

    def __init__(self, states: Sequence[EgoState]) -> None:
        if not states:
            raise ValueError("an ego trajectory needs at least one state")
        self.states = list(states)
        self.times = np.array([state.t_local for state in self.states], dtype=float)
        self._columns = {name: np.array([getattr(state, name) for state in self.states], dtype=float)
                         for name in ("x", "y", "heading", "vx", "vy", "z", "pitch", "roll")}
        # The yaw rate from the unwrapped heading (central differences).
        self._columns["yaw_rate"] = (np.gradient(self._columns["heading"], self.times)
                                     if len(self.times) > 1 else np.zeros(len(self.times)))

    def at(self, t_local: float) -> EgoState:
        values = {name: float(np.interp(t_local, self.times, column))
                  for name, column in self._columns.items()}
        return EgoState(t_local=float(t_local), **values)

    @property
    def start(self) -> float:
        return float(self.times[0])

    @property
    def end(self) -> float:
        return float(self.times[-1])


def ego_trajectory(ego_records: Sequence[Mapping[str, Any]], clock_origin: float) -> EgoTrajectory:
    """Express ego.jsonl poses in the frame anchored at the first pose."""
    first = ego_records[0]
    yaw0 = math.radians(float(first["yaw_deg"]))
    c0, s0 = math.cos(yaw0), math.sin(yaw0)
    headings = np.unwrap([math.radians(float(record["yaw_deg"])) - yaw0 for record in ego_records])
    pitches = np.unwrap([math.radians(float(record.get("pitch_deg", 0.0))) for record in ego_records])
    rolls = np.unwrap([math.radians(float(record.get("roll_deg", 0.0))) for record in ego_records])
    states = []
    for record, heading, pitch, roll in zip(ego_records, headings, pitches, rolls):
        dx = float(record["x"]) - float(first["x"])
        dy = float(record["y"]) - float(first["y"])
        world_vx = float(record["velocity"]["x"])
        world_vy = float(record["velocity"]["y"])
        states.append(EgoState(
            t_local=round(float(record["timestamp"]) - clock_origin, 4),
            x=c0 * dx + s0 * dy, y=-s0 * dx + c0 * dy, heading=float(heading),
            vx=c0 * world_vx + s0 * world_vy, vy=-s0 * world_vx + c0 * world_vy,
            z=float(record.get("z", 0.0)) - float(first.get("z", 0.0)), pitch=float(pitch), roll=float(roll)))
    return EgoTrajectory(states)


# --------------------------------------------------------------------------
# Radars on the body, the recorder's own footprint
# --------------------------------------------------------------------------

@dataclass
class RadarMount:
    """One radar on the vehicle: position (x forward, y right, z up from the vehicle
    origin on the ground; metres) and orientation (radians: yaw + = to the right,
    pitch + = nose up), as recorded in the radar's own metadata."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.6
    yaw: float = 0.0
    pitch: float = 0.0
    sensor_id: str = "radar"

    @classmethod
    def from_metadata(cls, metadata: Mapping[str, Any]) -> "RadarMount":
        transform = metadata.get("sensor_transform") or {}
        return cls(x=float(transform.get("x", 0.0)), y=float(transform.get("y", 0.0)),
                   z=float(transform.get("z", 0.6)), yaw=math.radians(float(transform.get("yaw_deg", 0.0))),
                   pitch=math.radians(float(transform.get("pitch_deg", 0.0))),
                   sensor_id=str(metadata.get("sensor_id", "radar")))

    def directions(self, azimuth: np.ndarray, altitude: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Unit lines of sight of detections (sensor azimuth/altitude) in the vehicle frame."""
        x, y, z = np.cos(altitude) * np.cos(azimuth), np.cos(altitude) * np.sin(azimuth), np.sin(altitude)
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        x, z = x * cp - z * sp, x * sp + z * cp
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        return x * cy - y * sy, x * sy + y * cy, z


@dataclass
class RadarStream:
    """The raw sweeps of one radar (compact observations) and where it sits on the body."""

    mount: RadarMount
    observations: Any

    @property
    def sensor_id(self) -> str:
        return self.mount.sensor_id


def sensor_position(ego: EgoState, mount: RadarMount) -> np.ndarray:
    c, s = math.cos(ego.heading), math.sin(ego.heading)
    return np.array([ego.x + c * mount.x - s * mount.y, ego.y + s * mount.x + c * mount.y])


def sensor_velocity(ego: EgoState, mount: RadarMount) -> Tuple[float, float]:
    """The radar's instantaneous velocity in the vehicle frame (forward, right).

    The vehicle's velocity plus its rotation about the vehicle origin: a mount
    at (x, y) moves at yaw_rate * (-y, x) more (a front radar 2.4 m ahead turning
    at 20 deg/s moves 0.84 m/s sideways; a side radar 1.1 m out moves 0.38 m/s
    along the heading).
    """
    c, s = math.cos(ego.heading), math.sin(ego.heading)
    forward = c * ego.vx + s * ego.vy - ego.yaw_rate * mount.y
    right = -s * ego.vx + c * ego.vy + ego.yaw_rate * mount.x
    return forward, right


def sensor_point(ego: EgoState, mount: RadarMount) -> np.ndarray:
    """The radar's position in the local frame, 3-D: the mount turned by the vehicle's heading, pitch and roll."""
    cy, sy = math.cos(ego.heading), math.sin(ego.heading)
    cp, sp = math.cos(ego.pitch), math.sin(ego.pitch)
    cr, sr = math.cos(ego.roll), math.sin(ego.roll)
    # Columns: the vehicle's forward, right and up axes (CARLA's rotation convention).
    rotation = np.array([[cp * cy, cy * sp * sr - sy * cr, -(cy * sp * cr + sy * sr)],
                         [cp * sy, sy * sp * sr + cy * cr, cy * sr - sy * sp * cr],
                         [sp, -cp * sr, cp * cr]])
    return np.array([ego.x, ego.y, ego.z]) + rotation @ np.array([mount.x, mount.y, mount.z])


def radar_velocity(ego: EgoTrajectory, mount: RadarMount, t_local: float, t_previous: float) -> np.ndarray:
    """One radar's own velocity over the last sweep interval: its displacement / time (local frame, 3-D).

    This is how CARLA's radar measures its own motion (current minus previous
    location of THAT radar over the tick), so the range rates it reports for
    static scenery are exactly cancelled.  It includes the rotation about the
    vehicle origin (lever arm) and the swing of the mount when the vehicle
    pitches and rolls (braking, impact).  The instantaneous velocity of the
    vehicle differs from it whenever the speed changes within a tick: by about
    3 m/s at an impact.
    """
    if t_local - t_previous <= 1e-6:
        own = ego.at(t_local)
        forward, right = sensor_velocity(own, mount)
        c, s = math.cos(own.heading), math.sin(own.heading)
        return np.array([c * forward - s * right, s * forward + c * right, 0.0])
    return (sensor_point(ego.at(t_local), mount) - sensor_point(ego.at(t_previous), mount)) / (t_local - t_previous)


@dataclass(frozen=True)
class EgoFootprint:
    """The recorder's own rectangle in its vehicle frame (x forward, y right, origin = vehicle origin; metres)."""

    x_min: float
    x_max: float
    y_min: float
    y_max: float

    @classmethod
    def from_metadata(cls, footprint: Optional[Mapping[str, Any]]) -> Optional["EgoFootprint"]:
        """From the vehicle metadata's ``ego_footprint``; None if absent."""
        if not footprint:
            return None
        try:
            return cls(x_min=float(footprint["x_min_m"]), x_max=float(footprint["x_max_m"]),
                       y_min=float(footprint["y_min_m"]), y_max=float(footprint["y_max_m"]))
        except (KeyError, TypeError, ValueError):
            return None

    @property
    def centre(self) -> Tuple[float, float]:
        return (self.x_min + self.x_max) / 2.0, (self.y_min + self.y_max) / 2.0

    def nearest(self, x: Any, y: Any) -> Tuple[Any, Any]:
        """The footprint point nearest to each point (the point itself inside)."""
        return np.clip(x, self.x_min, self.x_max), np.clip(y, self.y_min, self.y_max)

    def distance(self, x: Any, y: Any) -> Any:
        """Distance of points (vehicle frame) to the footprint: the clearance of a surface point (0 inside)."""
        qx, qy = self.nearest(x, y)
        return np.hypot(np.asarray(x) - qx, np.asarray(y) - qy)

    def contains(self, x: np.ndarray, y: np.ndarray, margin: float = 0.0) -> np.ndarray:
        """Points (vehicle frame) at least ``margin`` inside the rectangle."""
        return ((x > self.x_min + margin) & (x < self.x_max - margin)
                & (y > self.y_min + margin) & (y < self.y_max - margin))

    def outward(self, x: float, y: float) -> Tuple[float, float]:
        """Unit direction from the nearest footprint point to (x, y); from the centre for a point inside."""
        qx, qy = self.nearest(x, y)
        dx, dy = x - float(qx), y - float(qy)
        norm = math.hypot(dx, dy)
        if norm < 1e-6:
            cx, cy = self.centre
            dx, dy = x - cx, y - cy
            norm = max(math.hypot(dx, dy), 1e-6)
        return dx / norm, dy / norm

    def segment_distance(self, p0: Tuple[float, float], p1: Tuple[float, float]) -> Tuple[float, float]:
        """(minimum distance, fraction along the segment where it occurs) from the segment p0-p1 to the footprint."""
        x0, y0 = p0
        x1, y1 = p1
        dx, dy = x1 - x0, y1 - y0
        # Clipped parametric intersection with the rectangle (Liang-Barsky).
        lo, hi = 0.0, 1.0
        inside = True
        for p, q in ((-dx, x0 - self.x_min), (dx, self.x_max - x0), (-dy, y0 - self.y_min), (dy, self.y_max - y0)):
            if abs(p) < 1e-12:
                if q < 0:
                    inside = False
                    break
                continue
            r = q / p
            if p < 0:
                lo = max(lo, r)
            else:
                hi = min(hi, r)
            if lo > hi:
                inside = False
                break
        if inside:
            return 0.0, lo
        # No intersection: the minimum lies at an endpoint or at the projection of a corner.
        candidates = [0.0, 1.0]
        length2 = dx * dx + dy * dy
        if length2 > 1e-12:
            for cx in (self.x_min, self.x_max):
                for cy in (self.y_min, self.y_max):
                    candidates.append(min(max(((cx - x0) * dx + (cy - y0) * dy) / length2, 0.0), 1.0))
        best = min(candidates, key=lambda f: float(self.distance(x0 + f * dx, y0 + f * dy)))
        return float(self.distance(x0 + best * dx, y0 + best * dy)), best


# --------------------------------------------------------------------------
# Radar sweeps in the local frame
# --------------------------------------------------------------------------

@dataclass
class RadarSweep:
    """Object-height returns of all radars at one instant, in the local frame."""

    t_local: float
    points: np.ndarray  # (N, 2)
    origins: np.ndarray  # (N, 2) position of the radar that produced each return
    radar: np.ndarray  # (N,) index of that radar in the stream list
    radial_speed: np.ndarray  # (N,) the target's own horizontal speed along the line of sight, + = away
    clearance: np.ndarray  # (N,) distance from the recorder's footprint (planar range without footprint)
    depth: np.ndarray  # (N,) raw range from that radar
    own_body: int = 0  # returns dropped because they lie inside the recorder's own footprint
    radars: Tuple[str, ...] = ()  # sensor ids by index


def _stream_times(stream: RadarStream, clock_origin: float) -> List[float]:
    return [round(float(timestamp) - clock_origin, 4) for timestamp in stream.observations.timestamps]


def radar_sweeps(streams: Sequence[RadarStream], ego: EgoTrajectory, clock_origin: float, cfg: TrackingConfig,
                 footprint: Optional[EgoFootprint] = None) -> List[RadarSweep]:
    """Place every return of every radar in the local frame and remove that radar's own motion.

    All radars tick together; the returns of one instant form one sweep.  Each
    radar's own motion is the displacement of ITS mount over its last sweep
    interval (``radar_velocity``, as CARLA measures it), so scenery stays
    static in a turn, under braking and through an impact.  The Doppler speed
    is projected onto the horizontal plane (targets move horizontally).
    Returns from inside the recorder's own footprint are its own body and are
    dropped; the others carry their clearance.
    """
    names = tuple(stream.sensor_id for stream in streams)
    times = [_stream_times(stream, clock_origin) for stream in streams]
    lookup = [{t: index for index, t in enumerate(stream_times)} for stream_times in times]
    instants = sorted(set().union(*times)) if times else []
    interval = float(np.median(np.diff(instants))) if len(instants) > 1 else 0.0
    sweeps = []
    for t_local in instants:
        pose = ego.at(t_local)
        c, s = math.cos(pose.heading), math.sin(pose.heading)
        parts: Dict[str, List[np.ndarray]] = {key: [] for key in
                                              ("points", "origins", "radar", "radial", "clearance", "depth")}
        own_body = 0
        for k, stream in enumerate(streams):
            index = lookup[k].get(t_local)
            if index is None:
                continue
            mount = stream.mount
            rows = np.asarray(stream.observations.frame_detections(index), dtype=float).reshape(-1, 4)
            depth, azimuth, altitude, range_rate = rows[:, 0], rows[:, 1], rows[:, 2], rows[:, 3]
            ux, uy, uz = mount.directions(azimuth, altitude)
            vehicle_x, vehicle_y = mount.x + depth * ux, mount.y + depth * uy
            # Height in the vehicle frame on purpose: a vehicle ahead shares the road
            # grade (S01 climbs a 7 degree slope), so world pitch would mislead.
            height = mount.z + depth * uz
            valid = (np.isfinite(rows).all(axis=1) & (depth > 0.0)
                     & (height >= cfg.min_height_m) & (height <= cfg.max_height_m))
            previous = times[k][index - 1] if index > 0 else t_local - interval
            if previous < ego.start - 1e-6:  # no earlier pose: the next interval instead
                velocity = radar_velocity(ego, mount, min(t_local + interval, ego.end), t_local)
            else:
                velocity = radar_velocity(ego, mount, t_local, previous)
            # Line of sight in the local frame (the vehicle's heading; its small pitch and
            # roll only matter for the radar's own displacement, already in ``velocity``).
            line_x, line_y = c * ux - s * uy, s * ux + c * uy
            # range_rate = (target velocity - radar velocity) . line of sight, so adding
            # the radar's velocity leaves the target's own speed along the line of sight.
            horizontal = np.maximum(np.hypot(ux, uy), 0.2)
            radial_speed = (range_rate + velocity[0] * line_x + velocity[1] * line_y + velocity[2] * uz) / horizontal
            if footprint is not None:
                inside = valid & footprint.contains(vehicle_x, vehicle_y, OWN_BODY_MARGIN_M)
                own_body += int(inside.sum())
                valid &= ~inside
                clearance = footprint.distance(vehicle_x, vehicle_y)
            else:
                clearance = np.hypot(vehicle_x, vehicle_y)
            origin = sensor_position(pose, mount)
            points = np.column_stack([pose.x + c * vehicle_x - s * vehicle_y, pose.y + s * vehicle_x + c * vehicle_y])
            count = int(valid.sum())
            parts["points"].append(points[valid])
            parts["origins"].append(np.tile(origin, (count, 1)))
            parts["radar"].append(np.full(count, k, dtype=int))
            parts["radial"].append(radial_speed[valid])
            parts["clearance"].append(np.asarray(clearance)[valid])
            parts["depth"].append(depth[valid])

        def joined(key: str, width: Optional[int] = None) -> np.ndarray:
            if parts[key]:
                return np.concatenate(parts[key])
            return np.empty((0, width)) if width else np.empty(0, dtype=int if key == "radar" else float)

        sweeps.append(RadarSweep(t_local=t_local, points=joined("points", 2), origins=joined("origins", 2),
                                 radar=joined("radar"), radial_speed=joined("radial"),
                                 clearance=np.maximum(joined("clearance"), 0.0), depth=joined("depth"),
                                 own_body=own_body, radars=names))
    return sweeps


def cluster_points(points: np.ndarray, max_gap_m: float) -> List[List[int]]:
    """Single-linkage clusters: points closer than ``max_gap_m`` are one object."""
    remaining = list(range(len(points)))
    clusters = []
    while remaining:
        members = [remaining.pop(0)]
        frontier = list(members)
        while frontier:
            current = frontier.pop()
            close = [i for i in remaining
                     if math.hypot(*(points[i] - points[current])) < max_gap_m]
            for i in close:
                remaining.remove(i)
            members.extend(close)
            frontier.extend(close)
        clusters.append(sorted(members))
    return clusters


# --------------------------------------------------------------------------
# Kalman filter (constant velocity, state [px, py, vx, vy]) and RTS smoother
# --------------------------------------------------------------------------

@dataclass
class TrackMeasurement:
    """What a track received in one sweep (``xy`` is None for a missed sweep).

    ``dopplers`` holds one (unit line of sight from that radar to its returns,
    median radial speed) per radar that saw the track in this sweep: radars at
    different places see the target along different lines of sight.
    """

    t_local: float
    xy: Optional[np.ndarray] = None
    dopplers: List[Tuple[np.ndarray, float]] = field(default_factory=list)
    n_returns: int = 0
    near_clearance: Optional[float] = None  # clearance of the track's near surface in this sweep
    surface_offset: Optional[float] = None  # median clearance of its returns minus the near one
    radar: Optional[str] = None  # the radar with most of the track's returns in this sweep
    radars: Tuple[str, ...] = ()  # every radar that saw it in this sweep


def _transition(dt: float) -> np.ndarray:
    matrix = np.eye(4)
    matrix[0, 2] = matrix[1, 3] = dt
    return matrix


def kf_predict(x: np.ndarray, P: np.ndarray, dt: float, acceleration_std: float) -> Tuple[np.ndarray, np.ndarray]:
    F = _transition(dt)
    # Piecewise-constant white acceleration.
    G = np.array([[0.5 * dt * dt, 0.0], [0.0, 0.5 * dt * dt], [dt, 0.0], [0.0, dt]])
    Q = (acceleration_std ** 2) * (G @ G.T)
    return F @ x, F @ P @ F.T + Q


def kf_update(x: np.ndarray, P: np.ndarray, z: np.ndarray, H: np.ndarray, R: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    x_new = x + K @ (z - H @ x)
    I_KH = np.eye(len(x)) - K @ H
    return x_new, I_KH @ P @ I_KH.T + K @ R @ K.T  # Joseph form stays symmetric


def _measurement_model(measurement: TrackMeasurement, cfg: TrackingConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Position rows, plus one Doppler row per radar: radial speed = line_of_sight . velocity."""
    rows = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
    values = [measurement.xy[0], measurement.xy[1]]
    variances = [cfg.measurement_std_m ** 2] * 2
    for line, radial in measurement.dopplers:
        rows.append([0.0, 0.0, float(line[0]), float(line[1])])
        values.append(radial)
        variances.append(cfg.radial_speed_std_mps ** 2)
    return np.array(rows), np.array(values, dtype=float), np.diag(variances)


def _initial_state(measurement: TrackMeasurement, cfg: TrackingConfig) -> Tuple[np.ndarray, np.ndarray]:
    velocity = np.zeros(2)
    if measurement.dopplers:
        line, radial = measurement.dopplers[0]
        velocity = radial * np.asarray(line, dtype=float)
    x = np.array([measurement.xy[0], measurement.xy[1], velocity[0], velocity[1]])
    P = np.diag([cfg.measurement_std_m ** 2] * 2 + [INITIAL_VELOCITY_STD_MPS ** 2] * 2)
    return x, P


def filter_and_smooth(measurements: Sequence[TrackMeasurement], cfg: TrackingConfig) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Forward Kalman filter, then backward Rauch-Tung-Striebel smoother.

    Returns (smoothed states, smoothed covariances, filtered states), one row
    per measurement record; missed sweeps are prediction-only steps.
    """
    x, P = _initial_state(measurements[0], cfg)
    predicted_x, predicted_P, filtered_x, filtered_P = [x], [P], [x], [P]
    for previous, current in zip(measurements, measurements[1:]):
        x, P = kf_predict(x, P, current.t_local - previous.t_local, cfg.acceleration_std_mps2)
        predicted_x.append(x)
        predicted_P.append(P)
        if current.xy is not None:
            H, z, R = _measurement_model(current, cfg)
            x, P = kf_update(x, P, z, H, R)
        filtered_x.append(x)
        filtered_P.append(P)

    smoothed_x = list(filtered_x)
    smoothed_P = list(filtered_P)
    for k in range(len(measurements) - 2, -1, -1):
        F = _transition(measurements[k + 1].t_local - measurements[k].t_local)
        gain = filtered_P[k] @ F.T @ np.linalg.inv(predicted_P[k + 1])
        smoothed_x[k] = filtered_x[k] + gain @ (smoothed_x[k + 1] - predicted_x[k + 1])
        smoothed_P[k] = filtered_P[k] + gain @ (smoothed_P[k + 1] - predicted_P[k + 1]) @ gain.T
    return np.array(smoothed_x), np.array(smoothed_P), np.array(filtered_x)


# --------------------------------------------------------------------------
# Gated association of returns to tracks
# --------------------------------------------------------------------------

class _ActiveTrack:
    """A track during association: current filter state and its sweeps so far."""

    def __init__(self, birth_order: int, first: TrackMeasurement, cfg: TrackingConfig) -> None:
        self.birth_order = birth_order
        self.track_id: Optional[str] = None
        # Its last sweep had returns of its own and no foreign return around it.
        self.clean = False
        self.x, self.P = _initial_state(first, cfg)
        self.t_local = first.t_local
        self.measurements = [first]
        self.n_updates = 1
        self.last_update_t = first.t_local

    def predict(self, t_local: float, cfg: TrackingConfig) -> None:
        self.x, self.P = kf_predict(self.x, self.P, t_local - self.t_local, cfg.acceleration_std_mps2)
        self.t_local = t_local

    def update(self, measurement: TrackMeasurement, cfg: TrackingConfig) -> None:
        H, z, R = _measurement_model(measurement, cfg)
        self.x, self.P = kf_update(self.x, self.P, z, H, R)
        self.measurements.append(measurement)
        self.n_updates += 1
        self.last_update_t = measurement.t_local

    def miss(self, sweep: RadarSweep) -> None:
        self.measurements.append(TrackMeasurement(t_local=sweep.t_local))


def _unit_lines(points: np.ndarray, origins: np.ndarray) -> np.ndarray:
    lines = points - origins
    return lines / np.maximum(np.hypot(lines[:, 0], lines[:, 1]), 1e-6)[:, None]


def _measurement_from_returns(sweep: RadarSweep, mask: np.ndarray) -> TrackMeasurement:
    """Median position of the claimed returns, and per radar the median line-of-sight speed."""
    xy = np.median(sweep.points[mask], axis=0)
    dopplers = []
    counts = []
    for k in sorted(set(sweep.radar[mask].tolist())):
        own = mask & (sweep.radar == k)
        line = np.median(sweep.points[own], axis=0) - sweep.origins[own][0]
        line = line / max(float(np.linalg.norm(line)), 1e-6)
        counts.append((int(own.sum()), k))
        dopplers.append((int(own.sum()), line, float(np.median(sweep.radial_speed[own]))))
    dopplers.sort(key=lambda item: -item[0])  # the radar with most returns first
    clearances = sweep.clearance[mask]
    near = float(np.percentile(clearances, NEAR_SURFACE_PERCENTILE))
    offset = max(float(np.median(clearances)) - near, 0.0)
    main = max(counts)[1]
    return TrackMeasurement(t_local=sweep.t_local, xy=xy, dopplers=[(line, radial) for _, line, radial in dopplers],
                            n_returns=int(mask.sum()), near_clearance=near, surface_offset=offset,
                            radar=sweep.radars[main] if sweep.radars else str(main),
                            radars=tuple(sorted(sweep.radars[k] if sweep.radars else str(k) for _, k in counts)))


def _gate(track: _ActiveTrack, sweep: RadarSweep, free: np.ndarray, cfg: TrackingConfig) -> np.ndarray:
    """Free returns near the predicted position with a consistent Doppler speed (each along its own radar's line of sight)."""
    if not len(sweep.points):
        return np.zeros(0, dtype=bool)
    offsets = sweep.points - track.x[:2]
    distance = np.hypot(offsets[:, 0], offsets[:, 1])
    predicted_radial = _unit_lines(sweep.points, sweep.origins) @ track.x[2:]
    mask = (free & (distance <= cfg.max_association_distance_m)
            & (np.abs(sweep.radial_speed - predicted_radial) <= cfg.max_velocity_mismatch_mps))
    if track.track_id is None:
        # Tentative tracks may only grow on moving returns (never on scenery).
        mask &= np.abs(sweep.radial_speed) >= cfg.moving_speed_mps
    return mask


def _slowdown_gate(track: _ActiveTrack, sweep: RadarSweep, free: np.ndarray, own: np.ndarray,
                   cfg: TrackingConfig) -> np.ndarray:
    """A confirmed track's returns after an abrupt slowdown of its target (a crash).

    Only when the ordinary gate gave it nothing in this sweep and its previous
    sweep was clean (its own returns, no foreign one around it: a road crest or
    a guardrail next to the target is foreign clutter in every sweep, so it never
    qualifies): the free returns within the position gate whose line-of-sight
    speed lies between standstill and the predicted one (Doppler gate width at
    both ends), at least ``min_slowdown_returns`` of them.
    """
    offsets = sweep.points - track.x[:2]
    near = free & (np.hypot(offsets[:, 0], offsets[:, 1]) <= cfg.max_association_distance_m)
    was_clean = track.clean
    track.clean = bool(own.any()) and not (near & ~own).any()
    if track.track_id is None or own.any() or not was_clean:
        return own
    predicted = _unit_lines(sweep.points, sweep.origins) @ track.x[2:]
    tolerance = cfg.max_velocity_mismatch_mps
    slowed = (near & (sweep.radial_speed >= np.minimum(predicted, 0.0) - tolerance)
              & (sweep.radial_speed <= np.maximum(predicted, 0.0) + tolerance))
    if int(slowed.sum()) < cfg.min_slowdown_returns:
        return own
    track.clean = True
    return slowed


def associate_returns(sweeps: Sequence[RadarSweep], cfg: TrackingConfig) -> List[_ActiveTrack]:
    """Deterministic gated association; returns the confirmed tracks."""
    active: List[_ActiveTrack] = []
    finished: List[_ActiveTrack] = []
    births = 0
    confirmed = 0
    for sweep in sweeps:
        free = np.ones(len(sweep.points), dtype=bool)
        # 1. Existing tracks claim returns: confirmed tracks first, older first.
        for track in sorted(active, key=lambda item: (item.track_id is None, item.birth_order)):
            track.predict(sweep.t_local, cfg)
            mask = _slowdown_gate(track, sweep, free, _gate(track, sweep, free, cfg), cfg)
            if mask.any():
                track.update(_measurement_from_returns(sweep, mask), cfg)
                free &= ~mask
            else:
                track.miss(sweep)
        # 2. End tracks that have been silent for too long.
        survivors = []
        for track in active:
            if sweep.t_local - track.last_update_t > cfg.max_track_gap_s:
                if track.track_id is not None:
                    finished.append(track)
            else:
                survivors.append(track)
        active = survivors
        # 3. Left-over moving returns away from every track start tentative tracks.
        candidates = free & (np.abs(sweep.radial_speed) >= cfg.moving_speed_mps)
        suppression_m = cfg.max_association_distance_m + cfg.cluster_distance_m
        for track in active:
            offsets = sweep.points - track.x[:2]
            candidates &= np.hypot(offsets[:, 0], offsets[:, 1]) > suppression_m
        indices = np.flatnonzero(candidates)
        for cluster in cluster_points(sweep.points[indices], cfg.cluster_distance_m):
            mask = np.zeros(len(sweep.points), dtype=bool)
            mask[indices[cluster]] = True
            births += 1
            active.append(_ActiveTrack(births, _measurement_from_returns(sweep, mask), cfg))
        # 4. Confirm tentative tracks that kept receiving moving returns.
        for track in active:
            if track.track_id is None and track.n_updates >= cfg.min_track_frames:
                confirmed += 1
                track.track_id = "track_{0:03d}".format(confirmed)
    finished.extend(track for track in active if track.track_id is not None)
    return sorted(finished, key=lambda item: item.track_id)


# --------------------------------------------------------------------------
# Smoothed local tracks
# --------------------------------------------------------------------------

@dataclass
class TrackSample:
    """One smoothed track state, plus its geometry relative to the recorder.

    Relative geometry is in the recorder's vehicle frame at that instant
    (origin = vehicle origin, x forward, y right), independent of where the
    radars sit.
    """

    t_local: float
    x_m: float
    y_m: float
    vx_mps: float
    vy_mps: float
    speed_mps: float
    pos_std_m: float
    vel_std_mps: float
    range_m: float  # raw: from the radar that observed it to the tracked (median) point, horizontal
    bearing_deg: float  # from the vehicle origin, positive = to the recorder's right
    longitudinal_m: float  # of the tracked point, along the current heading from the vehicle origin
    lateral_m: float  # positive = to the right of the current heading
    closing_speed_mps: float  # rate at which the clearance shrinks (+ = approaching the footprint)
    closing_ttc_s: Optional[float]  # clearance / closing speed (line-of-sight time to contact)
    measured: bool
    n_returns: int
    meas_x_m: Optional[float] = None
    meas_y_m: Optional[float] = None
    # Free distance from the recorder's footprint to the target's near surface
    # (the distance from the vehicle origin when the footprint is unknown).
    clearance_m: Optional[float] = None
    # How far the tracked point lies ahead of the recorder's front edge (the
    # longitudinal distance when the footprint is unknown).
    ahead_m: Optional[float] = None
    surface_offset_m: float = 0.0  # depth of the tracked point behind the near surface
    radar: Optional[str] = None  # the radar that observed the track (latest measured sweep)
    acceleration_mps2: float = 0.0  # the target's own acceleration along its velocity (smoothed)
    relative_vx_mps: float = 0.0  # target minus recorder velocity, along the recorder's heading
    relative_vy_mps: float = 0.0  # ... and to its right (non-rotating)
    # Seen past another track of the same recorder (set by the local reconstruction,
    # conflict.occluded_by): its returns may be hidden by or mixed with that vehicle's.
    occluded: bool = False

    def __post_init__(self) -> None:
        if self.clearance_m is None:
            self.clearance_m = self.range_m
        if self.ahead_m is None:
            self.ahead_m = self.longitudinal_m

    def to_dict(self, track_id: str) -> Dict[str, Any]:
        out: Dict[str, Any] = {"track_id": track_id}
        for name, value in self.__dict__.items():
            out[name] = round(value, 3) if isinstance(value, float) else value
        return out


@dataclass
class LocalTrack:
    track_id: str
    samples: List[TrackSample]

    @property
    def first_t(self) -> float:
        return self.samples[0].t_local

    @property
    def last_t(self) -> float:
        return self.samples[-1].t_local

    def sample_near(self, t_local: float, tolerance_s: float = 0.026) -> Optional[TrackSample]:
        best = min(self.samples, key=lambda sample: abs(sample.t_local - t_local))
        return best if abs(best.t_local - t_local) <= tolerance_s else None

    def summary(self) -> Dict[str, Any]:
        measured = [sample for sample in self.samples if sample.measured]
        closest = min(self.samples, key=lambda sample: sample.range_m)
        nearest = min(self.samples, key=lambda sample: sample.clearance_m)
        return {"track_id": self.track_id,
                "first_seen_t_local": self.first_t, "last_seen_t_local": self.last_t,
                "duration_s": round(self.last_t - self.first_t, 3),
                "measured_sweeps": len(measured),
                "radar_returns": sum(sample.n_returns for sample in self.samples),
                "radars": sorted({sample.radar for sample in measured if sample.radar}),
                "min_range_m": round(closest.range_m, 2),
                "min_range_t_local": closest.t_local,
                "min_clearance_m": round(nearest.clearance_m, 2),
                "min_clearance_t_local": nearest.t_local,
                "max_speed_mps": round(max(sample.speed_mps for sample in self.samples), 2),
                "first_range_m": round(self.samples[0].range_m, 2),
                "first_bearing_deg": round(self.samples[0].bearing_deg, 1),
                "last_range_m": round(self.samples[-1].range_m, 2),
                "last_bearing_deg": round(self.samples[-1].bearing_deg, 1)}


def _relative_sample(t_local: float, state: np.ndarray, covariance: np.ndarray,
                     measurement: TrackMeasurement, ego: EgoTrajectory, radar_mount: Optional[RadarMount],
                     footprint: Optional[EgoFootprint] = None, surface_offset: float = 0.0,
                     acceleration: float = 0.0) -> TrackSample:
    own = ego.at(t_local)
    c, s = math.cos(own.heading), math.sin(own.heading)
    dx, dy = float(state[0]) - own.x, float(state[1]) - own.y
    x_v, y_v = c * dx + s * dy, -s * dx + c * dy
    dvx, dvy = float(state[2]) - own.vx, float(state[3]) - own.vy
    rel_x, rel_y = c * dvx + s * dvy, -s * dvx + c * dvy
    # Apparent velocity in the recorder's rotating frame: a turning recorder sweeps its
    # footprint past still objects (yaw rate + = turning right).
    frame_vx, frame_vy = rel_x + own.yaw_rate * y_v, rel_y - own.yaw_rate * x_v
    if footprint is not None:
        distance = float(footprint.distance(x_v, y_v))
        nx, ny = footprint.outward(x_v, y_v)
        ahead = x_v - footprint.x_max
    else:
        distance = math.hypot(x_v, y_v)
        nx, ny = x_v / max(distance, 1e-6), y_v / max(distance, 1e-6)
        ahead = x_v
    closing = -(nx * frame_vx + ny * frame_vy)
    clearance = max(distance - surface_offset, 0.0)
    ttc = clearance / closing if closing > MIN_CLOSING_FOR_TTC_MPS else None
    if radar_mount is not None:
        origin = sensor_position(own, radar_mount)
        range_m = float(np.hypot(float(state[0]) - origin[0], float(state[1]) - origin[1]))
    else:
        range_m = math.hypot(x_v, y_v)
    return TrackSample(
        t_local=t_local, x_m=float(state[0]), y_m=float(state[1]),
        vx_mps=float(state[2]), vy_mps=float(state[3]), speed_mps=float(np.hypot(*state[2:])),
        pos_std_m=float(math.sqrt(max(covariance[0, 0] + covariance[1, 1], 0.0) / 2.0)),
        vel_std_mps=float(math.sqrt(max(covariance[2, 2] + covariance[3, 3], 0.0) / 2.0)),
        range_m=range_m, bearing_deg=math.degrees(math.atan2(y_v, x_v)),
        longitudinal_m=x_v, lateral_m=y_v, closing_speed_mps=closing,
        closing_ttc_s=None if ttc is None else round(ttc, 3),
        measured=measurement.xy is not None, n_returns=measurement.n_returns,
        meas_x_m=None if measurement.xy is None else round(float(measurement.xy[0]), 3),
        meas_y_m=None if measurement.xy is None else round(float(measurement.xy[1]), 3),
        clearance_m=clearance, ahead_m=ahead, surface_offset_m=surface_offset,
        radar=None if radar_mount is None else radar_mount.sensor_id, acceleration_mps2=acceleration,
        relative_vx_mps=rel_x, relative_vy_mps=rel_y)


def surface_offsets(measurements: Sequence[TrackMeasurement]) -> List[float]:
    """Per measurement record, the smoothed depth of the tracked point behind the near surface.

    Running median over ``SURFACE_OFFSET_HALF_WINDOW`` measured sweeps on each
    side; a missed sweep takes the value of the nearest measured one.
    """
    measured = [index for index, m in enumerate(measurements) if m.surface_offset is not None]
    if not measured:
        return [0.0] * len(measurements)
    raw = [measurements[index].surface_offset for index in measured]
    smooth = [float(np.median(raw[max(k - SURFACE_OFFSET_HALF_WINDOW, 0):k + SURFACE_OFFSET_HALF_WINDOW + 1]))
              for k in range(len(raw))]
    out = []
    for index in range(len(measurements)):
        nearest = min(range(len(measured)), key=lambda k: abs(measured[k] - index))
        out.append(smooth[nearest])
    return out


def _along_velocity(times: np.ndarray, states: np.ndarray, index: int, lo: int, hi: int) -> float:
    """Velocity change from ``lo`` to ``hi`` per second, along the velocity at ``index``."""
    velocity = states[index, 2:]
    speed = float(np.linalg.norm(velocity))
    if speed < 0.5:
        # Below walking pace the direction is unreliable: the change of speed.
        return float((np.linalg.norm(states[hi, 2:]) - np.linalg.norm(states[lo, 2:])) / (times[hi] - times[lo]))
    return float((states[hi, 2:] - states[lo, 2:]) @ (velocity / speed) / (times[hi] - times[lo]))


def accelerations(times: Sequence[float], states: np.ndarray, filtered: Optional[np.ndarray] = None) -> List[float]:
    """The target's acceleration along its own velocity at each smoothed state (central difference).

    With the forward-filtered states, the estimate claims no more than the
    evidence up to that instant shows (the backward difference of the filtered
    velocity over the same span): the smoother spreads an abrupt stop, a crash,
    up to 0.2 s into the past, where it would announce a braking target before
    it braked.  Of the two the one closer to zero is kept, zero if they disagree.
    """
    times = np.asarray(times, dtype=float)
    out = []
    for index, t in enumerate(times):
        lo = int(np.searchsorted(times, t - ACCELERATION_HALF_WINDOW_S - 1e-6))
        hi = int(np.searchsorted(times, t + ACCELERATION_HALF_WINDOW_S + 1e-6)) - 1
        if hi <= lo or times[hi] - times[lo] < 1e-6:
            out.append(0.0)
            continue
        smoothed = _along_velocity(times, states, index, lo, hi)
        if filtered is None:
            out.append(smoothed)
            continue
        past = int(np.searchsorted(times, t - 2.0 * ACCELERATION_HALF_WINDOW_S - 1e-6))
        if index <= past or times[index] - times[past] < 1e-6:
            out.append(0.0)
            continue
        causal = _along_velocity(times, filtered, index, past, index)
        out.append(0.0 if smoothed * causal <= 0.0 else
                   (smoothed if abs(smoothed) < abs(causal) else causal))
    return out


def build_local_tracks(streams: Sequence[RadarStream], ego: EgoTrajectory, clock_origin: float,
                       cfg: TrackingConfig, footprint: Optional[EgoFootprint] = None,
                       stats: Optional[Dict[str, Any]] = None) -> List[LocalTrack]:
    """Raw radar observations of one recorder (every radar) -> smoothed anonymous tracks.

    ``footprint`` (the recorder's own bounding box, vehicle frame) turns
    positions into clearances and drops returns from the recorder's own body;
    ``stats`` (optional) receives how many such returns were dropped.
    """
    mounts = {stream.sensor_id: stream.mount for stream in streams}
    sweeps = radar_sweeps(streams, ego, clock_origin, cfg, footprint)
    if stats is not None:
        stats["own_body_returns_dropped"] = sum(sweep.own_body for sweep in sweeps)
    tracks = []
    for raw in associate_returns(sweeps, cfg):
        measurements = list(raw.measurements)
        while measurements[-1].xy is None:  # drop the prediction-only tail
            measurements.pop()
        states, covariances, filtered = filter_and_smooth(measurements, cfg)
        offsets = surface_offsets(measurements) if footprint is not None else [0.0] * len(measurements)
        acceleration = accelerations([m.t_local for m in measurements], states, filtered)
        samples = []
        radar = None
        for m, state, covariance, offset, accel in zip(measurements, states, covariances, offsets, acceleration):
            radar = m.radar or radar
            samples.append(_relative_sample(m.t_local, state, covariance, m, ego, mounts.get(radar), footprint,
                                            offset, accel))
        tracks.append(LocalTrack(track_id=raw.track_id, samples=samples))
    return tracks
