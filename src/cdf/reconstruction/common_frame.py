"""A common coordinate frame for the recorders' observations (reconstruction side, no ground truth).

Every recorder logs its own pose stream (``ego.jsonl``: position and heading in the map frame, the
recorded GNSS/INS pose; in the CARLA campaign it is exact, the robustness study perturbs it).  A
``PoseSource`` gives a recorder's pose at an instant of its own clock.  A radar track sample is measured
relative to the recorder's body (vehicle frame: longitudinal, lateral); it is placed in the common frame
by composing that relative measurement with the recorder's pose at the same instant -- never through
another recorder, the scenario or ground truth.  Times are put on the global clock with the recorder's
``offset_to_global`` (``reconstruction/global/alignment.json``).

What each sample carries (``CommonSample``): the track point (median of its returns), the observed near
surface (the point moved back towards the recorder by its depth, as the CRITICAL_TTC model does), the
ground velocity, its uncertainty, the line of sight from the recorder's body, and -- in memory only -- the
radar returns the track claimed in that sweep, each with the position of the radar that produced it.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np

from .tracking import EgoFootprint, EgoTrajectory, LocalTrack

DEFAULT_BODY = EgoFootprint(-2.3, 2.3, -0.95, 0.95)
HEADING_MIN_SPEED_MPS = 1.0  # below this a target's motion fixes no heading (conflict.HEADING_MIN_SPEED_MPS)


@dataclass(frozen=True)
class WorldPose:
    """A recorder's pose in the common (map) frame: metres, radians, metres per second."""

    x: float
    y: float
    yaw: float
    vx: float = 0.0
    vy: float = 0.0

    def to_world(self, longitudinal: float, lateral: float) -> np.ndarray:
        c, s = math.cos(self.yaw), math.sin(self.yaw)
        return np.array([self.x + c * longitudinal - s * lateral, self.y + s * longitudinal + c * lateral])

    def to_vehicle(self, point: Sequence[float]) -> Tuple[float, float]:
        dx, dy = float(point[0]) - self.x, float(point[1]) - self.y
        c, s = math.cos(self.yaw), math.sin(self.yaw)
        return c * dx + s * dy, -s * dx + c * dy


class PoseSource:
    """Where a recorder was, by its own clock (t_local).  Subclasses: the recorded stream, a perturbed one.

    ``position_std_m`` (per axis) and ``yaw_std_rad`` are the accuracy the source declares, as a GNSS/INS
    receiver reports its own estimate: the association gates widen with them.  0 for an exact stream.
    ``velocity_std_mps`` likewise for the recorded velocity."""

    name = "abstract"
    position_std_m = 0.0
    yaw_std_rad = 0.0
    velocity_std_mps = 0.0

    def pose_at(self, t_local: float) -> WorldPose:  # pragma: no cover - interface
        raise NotImplementedError

    def poses_at(self, times: Sequence[float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """(x, y, yaw) arrays at many instants of the recorder's clock (default: one by one)."""
        poses = [self.pose_at(float(t)) for t in times]
        return (np.array([p.x for p in poses]), np.array([p.y for p in poses]), np.array([p.yaw for p in poses]))

    @property
    def start(self) -> float:  # pragma: no cover - interface
        raise NotImplementedError

    @property
    def end(self) -> float:  # pragma: no cover - interface
        raise NotImplementedError


class RecordedPoseSource(PoseSource):
    """The recorder's own recorded pose stream (``ego.jsonl``), interpolated linearly (heading unwrapped).

    Baseline of the campaign: CARLA writes the exact pose, so this is an ideal GNSS/INS; the robustness
    study replaces it with a perturbed source (``PerturbedPoseSource``)."""

    name = "recorded"

    def __init__(self, records: Sequence[Mapping[str, Any]], clock_origin: float) -> None:
        rows = sorted(records, key=lambda record: float(record["timestamp"]))
        self.times = np.array([float(r["timestamp"]) - clock_origin for r in rows])
        self.x = np.array([float(r["x"]) for r in rows])
        self.y = np.array([float(r["y"]) for r in rows])
        self.yaw = np.unwrap(np.radians([float(r["yaw_deg"]) for r in rows]))
        velocity = [r.get("velocity") or {} for r in rows]
        self.vx = np.array([float(v.get("x", 0.0)) for v in velocity])
        self.vy = np.array([float(v.get("y", 0.0)) for v in velocity])

    @classmethod
    def from_vehicle_dir(cls, vehicle_dir: Path, clock_origin: float) -> "RecordedPoseSource":
        path = Path(vehicle_dir) / "ego.jsonl"
        with path.open(encoding="utf-8") as handle:
            records = [json.loads(line) for line in handle if line.strip()]
        return cls(records, clock_origin)

    @property
    def start(self) -> float:
        return float(self.times[0])

    @property
    def end(self) -> float:
        return float(self.times[-1])

    def pose_at(self, t_local: float) -> WorldPose:
        t = min(max(t_local, self.times[0]), self.times[-1])
        return WorldPose(float(np.interp(t, self.times, self.x)), float(np.interp(t, self.times, self.y)),
                         float(np.interp(t, self.times, self.yaw)), float(np.interp(t, self.times, self.vx)),
                         float(np.interp(t, self.times, self.vy)))

    def poses_at(self, times: Sequence[float]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        t = np.clip(np.asarray(times, dtype=float), self.times[0], self.times[-1])
        return np.interp(t, self.times, self.x), np.interp(t, self.times, self.y), np.interp(t, self.times, self.yaw)


@dataclass
class CommonSample:
    """One radar track sample in the common frame (see the module docstring)."""

    t_local: float
    t_global: float
    point: np.ndarray  # track point (median of its returns)
    near: np.ndarray  # observed near surface
    velocity: np.ndarray  # ground velocity
    pos_std: float
    vel_std: float
    observer: np.ndarray  # the recorder's body point nearest the target (line-of-sight origin)
    measured: bool
    heading: Optional[float] = None  # direction of motion [rad] when the speed fixes it
    # Variance (m^2 per axis) the observer's own pose adds to the sample: the pose source's declared
    # position accuracy and its heading accuracy times the range.
    pose_var: float = 0.0
    returns: Optional[np.ndarray] = field(default=None, repr=False)  # (N, 2) claimed returns, common frame
    origins: Optional[np.ndarray] = field(default=None, repr=False)  # (N, 2) their radars' positions

    @property
    def speed(self) -> float:
        return float(np.hypot(*self.velocity))

    @property
    def line_of_sight(self) -> np.ndarray:
        line = self.near - self.observer
        return line / max(float(np.hypot(*line)), 1e-6)


@dataclass
class CommonTrack:
    """A recorder's radar track in the common frame, on the global clock."""

    recorder: str
    track_id: str
    samples: List[CommonSample]
    status: str = "ANONYMOUS"  # as the collision-based association left it
    entity: Optional[str] = None  # the recorder it was associated with, if any

    @property
    def name(self) -> str:
        return "{0}:{1}".format(self.recorder, self.track_id)

    @property
    def start(self) -> float:
        return self.samples[0].t_global

    @property
    def end(self) -> float:
        return self.samples[-1].t_global

    def at(self, t_global: float, tolerance: float = 0.026) -> Optional[CommonSample]:
        times = np.array([s.t_global for s in self.samples])
        index = int(np.argmin(np.abs(times - t_global)))
        return self.samples[index] if abs(times[index] - t_global) <= tolerance else None

    def state_at(self, t_global: float, tolerance: float = 0.026) -> Optional[CommonSample]:
        """The nearest sample within ``tolerance``, moved to ``t_global`` at its own velocity: two recorders'
        radars need not sample at the same instants."""
        sample = self.at(t_global, tolerance)
        return None if sample is None else shifted(sample, t_global)


def shifted(sample: CommonSample, t_global: float) -> CommonSample:
    """A sample carried to a nearby instant at the target's own velocity (its observer point and the radar
    positions stay: they only orient the lines of sight)."""
    dt = t_global - sample.t_global
    if abs(dt) < 1e-9:
        return sample
    move = sample.velocity * dt
    return replace(sample, t_global=t_global, point=sample.point + move, near=sample.near + move,
                   returns=None if sample.returns is None else sample.returns + move)


@dataclass
class RecorderBody:
    """A recorder's own body in the common frame: its pose source, footprint and clock offset."""

    recorder: str
    poses: PoseSource
    footprint: Optional[EgoFootprint]
    offset_to_global: float
    # The recorder's own collision reports (its collision sensor, first callback): (t_global, the other
    # recorders of the matched contact; empty when no other recorder reported it).
    contacts: Tuple[Tuple[float, Tuple[str, ...]], ...] = ()

    def pose_at_global(self, t_global: float) -> WorldPose:
        return self.poses.pose_at(t_global - self.offset_to_global)

    def covers(self, t_global: float) -> bool:
        t_local = t_global - self.offset_to_global
        return self.poses.start - 1e-6 <= t_local <= self.poses.end + 1e-6

    def polygon(self, t_global: float) -> np.ndarray:
        """(4, 2) corners of the recorder's footprint in the common frame."""
        pose, fp = self.pose_at_global(t_global), self.footprint or DEFAULT_BODY
        return np.array([pose.to_world(x, y) for x, y in ((fp.x_max, fp.y_min), (fp.x_max, fp.y_max),
                                                           (fp.x_min, fp.y_max), (fp.x_min, fp.y_min))])

    def distance(self, t_global: float, point: Sequence[float]) -> float:
        """Distance from a point to the recorder's footprint (0 inside)."""
        pose, fp = self.pose_at_global(t_global), self.footprint or DEFAULT_BODY
        x, y = pose.to_vehicle(point)
        return float(math.hypot(max(fp.x_min - x, 0.0, x - fp.x_max), max(fp.y_min - y, 0.0, y - fp.y_max)))

    def outline_distance(self, t_global: float, point: Sequence[float]) -> float:
        """Distance from a point to the recorder's footprint outline: an observed near surface lies on it,
        so a point inside the body is as far from it as from the nearest edge."""
        pose, fp = self.pose_at_global(t_global), self.footprint or DEFAULT_BODY
        x, y = pose.to_vehicle(point)
        if fp.x_min <= x <= fp.x_max and fp.y_min <= y <= fp.y_max:
            return float(min(x - fp.x_min, fp.x_max - x, y - fp.y_min, fp.y_max - y))
        return float(math.hypot(max(fp.x_min - x, 0.0, x - fp.x_max), max(fp.y_min - y, 0.0, y - fp.y_max)))


def outline_distances(poses: PoseSource, footprint: Optional[EgoFootprint], t_local: Sequence[float],
                      points: np.ndarray, inside_zero: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    """``RecorderBody.outline_distance`` for many (instant of the recorder's clock, point) pairs at once:
    (distances, mask of the instants the pose source covers).  ``inside_zero``: a point inside the body is
    at distance 0 (``RecorderBody.distance``)."""
    t = np.asarray(t_local, dtype=float)
    points = np.asarray(points, dtype=float).reshape(-1, 2)
    valid = (t >= poses.start - 1e-6) & (t <= poses.end + 1e-6)
    x, y, yaw = poses.poses_at(t)
    c, s = np.cos(yaw), np.sin(yaw)
    dx, dy = points[:, 0] - x, points[:, 1] - y
    lx, ly = c * dx + s * dy, -s * dx + c * dy
    fp = footprint or DEFAULT_BODY
    inside = (lx >= fp.x_min) & (lx <= fp.x_max) & (ly >= fp.y_min) & (ly <= fp.y_max)
    edge = np.minimum(np.minimum(lx - fp.x_min, fp.x_max - lx), np.minimum(ly - fp.y_min, fp.y_max - ly))
    zero = np.zeros_like(lx)
    outside = np.hypot(np.maximum(np.maximum(fp.x_min - lx, zero), lx - fp.x_max),
                       np.maximum(np.maximum(fp.y_min - ly, zero), ly - fp.y_max))
    return np.where(inside, 0.0 if inside_zero else edge, outside), valid


def common_track(track: LocalTrack, recorder: str, ego: EgoTrajectory, poses: PoseSource,
                 footprint: Optional[EgoFootprint], offset_to_global: float, status: str = "ANONYMOUS",
                 entity: Optional[str] = None) -> CommonTrack:
    """One local track in the common frame.

    The track's position relative to the recorder's body (longitudinal, lateral) and its ground velocity
    expressed in the recorder's axes (through the recorder's own heading in its local frame) are composed
    with the recorder's pose from ``poses``; so are its claimed returns."""
    fp = footprint or DEFAULT_BODY
    samples = []
    returns = track.returns or [None] * len(track.samples)
    for sample, claimed in zip(track.samples, returns):
        pose = poses.pose_at(sample.t_local)
        local = ego.at(sample.t_local)
        nx, ny = fp.outward(sample.longitudinal_m, sample.lateral_m)
        near_x = sample.longitudinal_m - sample.surface_offset_m * nx
        near_y = sample.lateral_m - sample.surface_offset_m * ny
        bx, by = fp.nearest(near_x, near_y)
        c, s = math.cos(local.heading), math.sin(local.heading)
        rel_vx, rel_vy = c * sample.vx_mps + s * sample.vy_mps, -s * sample.vx_mps + c * sample.vy_mps
        cw, sw = math.cos(pose.yaw), math.sin(pose.yaw)
        velocity = np.array([cw * rel_vx - sw * rel_vy, sw * rel_vx + cw * rel_vy])
        speed = float(np.hypot(*velocity))
        world_returns = world_origins = None
        if claimed is not None:
            points, origins = claimed
            world_returns = _local_to_world(points, local, pose)
            world_origins = _local_to_world(origins, local, pose)
        reach = math.hypot(sample.longitudinal_m, sample.lateral_m)
        samples.append(CommonSample(
            t_local=sample.t_local, t_global=round(sample.t_local + offset_to_global, 4),
            point=pose.to_world(sample.longitudinal_m, sample.lateral_m), near=pose.to_world(near_x, near_y),
            velocity=velocity, pos_std=sample.pos_std_m, vel_std=sample.vel_std_mps,
            observer=pose.to_world(float(bx), float(by)), measured=sample.measured,
            heading=math.atan2(velocity[1], velocity[0]) if speed >= HEADING_MIN_SPEED_MPS else None,
            returns=world_returns, origins=world_origins,
            pose_var=poses.position_std_m ** 2 + (poses.yaw_std_rad * reach) ** 2))
    return CommonTrack(recorder=recorder, track_id=track.track_id, samples=samples, status=status, entity=entity)


def _local_to_world(points: np.ndarray, local: Any, pose: WorldPose) -> np.ndarray:
    """Local-frame points of a recorder -> its vehicle frame (local pose) -> common frame (pose source)."""
    points = np.asarray(points, dtype=float).reshape(-1, 2)
    c, s = math.cos(local.heading), math.sin(local.heading)
    dx, dy = points[:, 0] - local.x, points[:, 1] - local.y
    vx, vy = c * dx + s * dy, -s * dx + c * dy
    cw, sw = math.cos(pose.yaw), math.sin(pose.yaw)
    return np.column_stack([pose.x + cw * vx - sw * vy, pose.y + sw * vx + cw * vy])
