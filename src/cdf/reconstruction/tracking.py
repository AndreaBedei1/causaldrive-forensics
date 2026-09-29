"""Anonymous local radar tracks: association, Kalman filter and RTS smoother.

raw radar detections
  -> returns placed in the recorder's own local odometric frame
  -> each active track claims the returns inside its gate (gated association)
  -> left-over *moving* returns are clustered and start tentative tracks
  -> a tentative track that keeps receiving moving returns is confirmed and
     gets an anonymous id: track_001, track_002, ...
  -> each confirmed track is filtered forward (Kalman, constant velocity) and
     smoothed backward (Rauch-Tung-Striebel) into a local trajectory.

A confirmed track keeps claiming returns even when they look static, so a
vehicle that stops (a braking lead car) is not dropped.

Local odometric frame: origin at the recorder's first ego position, x along
its first heading, y to its right (CARLA's convention).  Every recorder has its
own frame; frames of different recorders are never compared.

Radar velocity convention, verified on the recordings: the CARLA detection
velocity is the range rate, negative while the range shrinks (static scenery
ahead of a recorder at speed v returns about -v*cos(azimuth)).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .config import TrackingConfig

# Velocity uncertainty of a newly started track (its tangential speed is unknown).
INITIAL_VELOCITY_STD_MPS = 10.0
# Below this closing speed a time-to-contact is not meaningful.
MIN_CLOSING_FOR_TTC_MPS = 0.1


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
                         for name in ("x", "y", "heading", "vx", "vy")}

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
    states = []
    for record, heading in zip(ego_records, headings):
        dx = float(record["x"]) - float(first["x"])
        dy = float(record["y"]) - float(first["y"])
        world_vx = float(record["velocity"]["x"])
        world_vy = float(record["velocity"]["y"])
        states.append(EgoState(
            t_local=round(float(record["timestamp"]) - clock_origin, 4),
            x=c0 * dx + s0 * dy, y=-s0 * dx + c0 * dy, heading=float(heading),
            vx=c0 * world_vx + s0 * world_vy, vy=-s0 * world_vx + c0 * world_vy))
    return EgoTrajectory(states)


@dataclass
class RadarMount:
    """Radar position on the vehicle (x forward, y right, z up; metres)."""

    x: float = 2.2
    y: float = 0.0
    z: float = 1.0
    yaw: float = 0.0  # radians

    @classmethod
    def from_metadata(cls, metadata: Mapping[str, Any]) -> "RadarMount":
        transform = metadata.get("sensor_transform") or {}
        return cls(x=float(transform.get("x", 2.2)), y=float(transform.get("y", 0.0)),
                   z=float(transform.get("z", 1.0)),
                   yaw=math.radians(float(transform.get("yaw_deg", 0.0))))


def sensor_position(ego: EgoState, mount: RadarMount) -> np.ndarray:
    c, s = math.cos(ego.heading), math.sin(ego.heading)
    return np.array([ego.x + c * mount.x - s * mount.y, ego.y + s * mount.x + c * mount.y])


# --------------------------------------------------------------------------
# Radar sweeps in the local frame
# --------------------------------------------------------------------------

@dataclass
class RadarSweep:
    """Object-height returns of one radar sweep, in the local frame."""

    t_local: float
    sensor_xy: np.ndarray  # (2,)
    points: np.ndarray  # (N, 2)
    radial_speed: np.ndarray  # (N,) the target's own speed along the line of sight, + = away


def radar_sweeps(observations: Any, ego: EgoTrajectory, mount: RadarMount,
                 clock_origin: float, cfg: TrackingConfig) -> List[RadarSweep]:
    """Place every radar return in the local frame and remove ego motion."""
    sweeps = []
    for index, timestamp in enumerate(observations.timestamps):
        t_local = round(float(timestamp) - clock_origin, 4)
        pose = ego.at(t_local)
        rows = np.asarray(observations.frame_detections(index), dtype=float).reshape(-1, 4)
        depth, altitude, range_rate = rows[:, 0], rows[:, 2], rows[:, 3]
        azimuth = rows[:, 1] + mount.yaw
        # Height in the sensor frame on purpose: a vehicle ahead shares the road
        # grade (S01 climbs a 7 degree slope), so world pitch would mislead.
        height = mount.z + depth * np.sin(altitude)
        valid = (np.isfinite(rows).all(axis=1) & (depth > 0.0)
                 & (height >= cfg.min_height_m) & (height <= cfg.max_height_m))
        # Unit line of sight in the vehicle frame.
        forward = np.cos(altitude) * np.cos(azimuth)
        right = np.cos(altitude) * np.sin(azimuth)
        c, s = math.cos(pose.heading), math.sin(pose.heading)
        own_forward = c * pose.vx + s * pose.vy
        own_right = -s * pose.vx + c * pose.vy
        # range_rate = (target velocity - own velocity) . line of sight, so adding
        # the own velocity leaves the target's own speed along the line of sight.
        radial_speed = range_rate + own_forward * forward + own_right * right
        vehicle_x = mount.x + depth * forward
        vehicle_y = mount.y + depth * right
        points = np.column_stack([pose.x + c * vehicle_x - s * vehicle_y,
                                  pose.y + s * vehicle_x + c * vehicle_y])
        sweeps.append(RadarSweep(t_local=t_local, sensor_xy=sensor_position(pose, mount),
                                 points=points[valid], radial_speed=radial_speed[valid]))
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
    """What a track received in one sweep (``xy`` is None for a missed sweep)."""

    t_local: float
    sensor_xy: np.ndarray
    xy: Optional[np.ndarray] = None
    radial_speed: Optional[float] = None
    line_of_sight: Optional[np.ndarray] = None
    n_returns: int = 0


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
    """Position rows, plus a Doppler row: radial speed = line_of_sight . velocity."""
    position_var = cfg.measurement_std_m ** 2
    if measurement.radial_speed is None or measurement.line_of_sight is None:
        H = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0]])
        return H, measurement.xy, np.eye(2) * position_var
    ux, uy = measurement.line_of_sight
    H = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, ux, uy]])
    z = np.array([measurement.xy[0], measurement.xy[1], measurement.radial_speed])
    return H, z, np.diag([position_var, position_var, cfg.radial_speed_std_mps ** 2])


def _initial_state(measurement: TrackMeasurement, cfg: TrackingConfig) -> Tuple[np.ndarray, np.ndarray]:
    velocity = np.zeros(2)
    if measurement.radial_speed is not None and measurement.line_of_sight is not None:
        velocity = measurement.radial_speed * measurement.line_of_sight
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
        self.measurements.append(TrackMeasurement(t_local=sweep.t_local, sensor_xy=sweep.sensor_xy))


def _measurement_from_returns(sweep: RadarSweep, mask: np.ndarray) -> TrackMeasurement:
    """Median position and median line-of-sight speed of the claimed returns."""
    xy = np.median(sweep.points[mask], axis=0)
    line_of_sight = xy - sweep.sensor_xy
    line_of_sight = line_of_sight / max(float(np.linalg.norm(line_of_sight)), 1e-6)
    return TrackMeasurement(t_local=sweep.t_local, sensor_xy=sweep.sensor_xy, xy=xy,
                            radial_speed=float(np.median(sweep.radial_speed[mask])),
                            line_of_sight=line_of_sight, n_returns=int(mask.sum()))


def _gate(track: _ActiveTrack, sweep: RadarSweep, free: np.ndarray, cfg: TrackingConfig) -> np.ndarray:
    """Free returns near the predicted position with a consistent Doppler speed."""
    if not len(sweep.points):
        return np.zeros(0, dtype=bool)
    offsets = sweep.points - track.x[:2]
    distance = np.hypot(offsets[:, 0], offsets[:, 1])
    lines = sweep.points - sweep.sensor_xy
    lines = lines / np.maximum(np.hypot(lines[:, 0], lines[:, 1]), 1e-6)[:, None]
    predicted_radial = lines @ track.x[2:]
    mask = (free & (distance <= cfg.max_association_distance_m)
            & (np.abs(sweep.radial_speed - predicted_radial) <= cfg.max_velocity_mismatch_mps))
    if track.track_id is None:
        # Tentative tracks may only grow on moving returns (never on scenery).
        mask &= np.abs(sweep.radial_speed) >= cfg.moving_speed_mps
    return mask


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
            mask = _gate(track, sweep, free, cfg)
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
    """One smoothed track state, plus its geometry relative to the recorder."""

    t_local: float
    x_m: float
    y_m: float
    vx_mps: float
    vy_mps: float
    speed_mps: float
    pos_std_m: float
    vel_std_mps: float
    range_m: float
    bearing_deg: float  # positive = to the recorder's right
    longitudinal_m: float  # ahead of the radar along the current heading
    lateral_m: float  # positive = to the right of the current heading
    closing_speed_mps: float  # positive = range shrinking
    ttc_s: Optional[float]
    measured: bool
    n_returns: int
    meas_x_m: Optional[float] = None
    meas_y_m: Optional[float] = None

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
        return {"track_id": self.track_id,
                "first_seen_t_local": self.first_t, "last_seen_t_local": self.last_t,
                "duration_s": round(self.last_t - self.first_t, 3),
                "measured_sweeps": len(measured),
                "radar_returns": sum(sample.n_returns for sample in self.samples),
                "min_range_m": round(closest.range_m, 2),
                "min_range_t_local": closest.t_local,
                "max_speed_mps": round(max(sample.speed_mps for sample in self.samples), 2),
                "first_range_m": round(self.samples[0].range_m, 2),
                "first_bearing_deg": round(self.samples[0].bearing_deg, 1),
                "last_range_m": round(self.samples[-1].range_m, 2),
                "last_bearing_deg": round(self.samples[-1].bearing_deg, 1)}


def _relative_sample(t_local: float, state: np.ndarray, covariance: np.ndarray,
                     measurement: TrackMeasurement, ego: EgoTrajectory, mount: RadarMount) -> TrackSample:
    own = ego.at(t_local)
    relative = state[:2] - sensor_position(own, mount)
    relative_velocity = state[2:] - np.array([own.vx, own.vy])
    range_m = float(np.hypot(*relative))
    c, s = math.cos(own.heading), math.sin(own.heading)
    longitudinal = c * relative[0] + s * relative[1]
    lateral = -s * relative[0] + c * relative[1]
    closing = -float(relative @ relative_velocity) / max(range_m, 1e-6)
    ttc = range_m / closing if closing > MIN_CLOSING_FOR_TTC_MPS else None
    return TrackSample(
        t_local=t_local, x_m=float(state[0]), y_m=float(state[1]),
        vx_mps=float(state[2]), vy_mps=float(state[3]), speed_mps=float(np.hypot(*state[2:])),
        pos_std_m=float(math.sqrt(max(covariance[0, 0] + covariance[1, 1], 0.0) / 2.0)),
        vel_std_mps=float(math.sqrt(max(covariance[2, 2] + covariance[3, 3], 0.0) / 2.0)),
        range_m=range_m, bearing_deg=math.degrees(math.atan2(lateral, longitudinal)),
        longitudinal_m=longitudinal, lateral_m=lateral, closing_speed_mps=closing,
        ttc_s=None if ttc is None else round(ttc, 3),
        measured=measurement.xy is not None, n_returns=measurement.n_returns,
        meas_x_m=None if measurement.xy is None else round(float(measurement.xy[0]), 3),
        meas_y_m=None if measurement.xy is None else round(float(measurement.xy[1]), 3))


def build_local_tracks(observations: Any, ego: EgoTrajectory, mount: RadarMount,
                       clock_origin: float, cfg: TrackingConfig) -> List[LocalTrack]:
    """Raw radar observations of one recorder -> smoothed anonymous tracks."""
    tracks = []
    for raw in associate_returns(radar_sweeps(observations, ego, mount, clock_origin, cfg), cfg):
        measurements = list(raw.measurements)
        while measurements[-1].xy is None:  # drop the prediction-only tail
            measurements.pop()
        states, covariances, _ = filter_and_smooth(measurements, cfg)
        samples = [_relative_sample(m.t_local, state, covariance, m, ego, mount)
                   for m, state, covariance in zip(measurements, states, covariances)]
        tracks.append(LocalTrack(track_id=raw.track_id, samples=samples))
    return tracks
