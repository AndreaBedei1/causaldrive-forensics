"""Road geometry for road-relative semantics (no run, scenario or ground-truth data).

The driving lanes of the map the recorder drove on, from the public OpenDRIVE file shipped with the CARLA
installation (``cdf.common.opendrive``): the map is the one whose driving lanes contain the recorder's own
recorded positions (``ego.jsonl``, its GNSS-like pose).  Without a local installation, or when no map fits,
there is no road model and the semantics fall back to the recorder-relative kinematics alone.

``RoadFrame.lane_toward_speed``: a target's velocity across ITS OWN lane, signed toward the recorder (positive
= moving toward the recorder's side of the road).  Two cars following one curved road keep their lanes: this
speed stays near zero while their positions drift sideways in any fixed frame.  A car crossing into the
recorder's lane has it positive, on a straight road or on a curve.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

import numpy as np

from ..common.opendrive import LaneSample, best_map

OPENDRIVE_DIR = Path("CarlaUE4") / "Content" / "Carla" / "Maps" / "OpenDrive"
MAP_MIN_FIT = 0.8  # share of the recorder's positions inside the map's driving lanes
LANE_SEARCH_M = 4.0  # lane stretches within this distance of a point are candidates
MIN_SPEED_MPS = 1.0  # below, a target has no direction of travel
LANE_TRAVEL_DEG = 30.0  # a vehicle within this of its lane's direction travels along it (else it crosses or turns)


class RoadLanes:
    """Driving-lane stretches of one map with a spatial index."""

    def __init__(self, name: str, lanes: Sequence[LaneSample]) -> None:
        from scipy.spatial import cKDTree
        self.name = name
        self.lanes = list(lanes)
        self.tree = cKDTree(np.array([(lane.x, lane.y) for lane in self.lanes]))

    def direction(self, x: float, y: float) -> Optional[float]:
        """Heading [rad, world frame] of the driving lane containing (x, y), None off the driving lanes."""
        best: Optional[Tuple[float, float]] = None
        for index in self.tree.query_ball_point((x, y), LANE_SEARCH_M):
            lane = self.lanes[index]
            yaw = math.radians(lane.yaw)
            dx, dy = x - lane.x, y - lane.y
            along, across = dx * math.cos(yaw) + dy * math.sin(yaw), -dx * math.sin(yaw) + dy * math.cos(yaw)
            if abs(along) <= lane.length / 2.0 and abs(across) <= lane.width / 2.0:
                if best is None or abs(across) < best[0]:
                    best = (abs(across), yaw)
        return None if best is None else best[1]


_SOURCES: Optional[Dict[str, str]] = None
_ROADS: Dict[str, RoadLanes] = {}


def _opendrive_sources() -> Dict[str, str]:
    global _SOURCES
    if _SOURCES is None:
        _SOURCES = {}
        try:
            from ..common.config import load_run_config
            from ..common.installation import find_carla_root as find_root
            root = find_root(load_run_config().get("simulation.carla_root"))
        except Exception:  # no configuration or installation: no road model
            root = None
        if root is not None:
            _SOURCES = {path.stem: path.read_text(encoding="utf-8", errors="replace")
                        for path in sorted((Path(root) / OPENDRIVE_DIR).glob("*.xodr"))}
    return _SOURCES


def road_for_positions(points: Sequence[Tuple[float, float]]) -> Optional[RoadLanes]:
    """The driving lanes of the map that contains the recorder's own positions, None without one."""
    sources = _opendrive_sources()
    if not sources or not points:
        return None
    name, lanes = best_map(sources, points, MAP_MIN_FIT)
    if name is None or not lanes:
        return None
    if name not in _ROADS:
        _ROADS[name] = RoadLanes(name, lanes)
    return _ROADS[name]


@dataclass
class RoadFrame:
    """The road model with the transform of the recorder's local frame (anchored at its first pose) to the
    world frame of the map."""

    road: RoadLanes
    x0: float
    y0: float
    yaw0: float
    _paths: Dict[float, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_ego_records(cls, records: Sequence[Mapping[str, Any]], step: int = 10) -> Optional["RoadFrame"]:
        if not records:
            return None
        road = road_for_positions([(float(r["x"]), float(r["y"])) for r in records[::step]])
        if road is None:
            return None
        first = records[0]
        return cls(road, float(first["x"]), float(first["y"]), math.radians(float(first["yaw_deg"])))

    def to_world(self, x: float, y: float) -> Tuple[float, float]:
        c, s = math.cos(self.yaw0), math.sin(self.yaw0)
        return self.x0 + c * x - s * y, self.y0 + s * x + c * y

    def vector_to_world(self, vx: float, vy: float) -> Tuple[float, float]:
        c, s = math.cos(self.yaw0), math.sin(self.yaw0)
        return c * vx - s * vy, s * vx + c * vy

    def path_at(self, ego: Any, t: float) -> Optional[Tuple["LanePath", float, float]]:
        """(the recorder's lane path at ``t``, its own arc length and lateral offset on it), None off the lanes.
        ``ego``: its trajectory in the local frame; its later positions choose the branch at a junction."""
        key = round(t, 3)
        if key not in self._paths:
            own = ego.at(t)
            wx, wy = self.to_world(own.x, own.y)
            future, travelled, last = [], 0.0, (wx, wy)
            step = 0.1
            k = 1
            while t + k * step <= ego.end + 1e-9 and travelled < 90.0:
                o = ego.at(t + k * step)
                fx, fy = self.to_world(o.x, o.y)
                travelled += math.hypot(fx - last[0], fy - last[1])
                future.append((fx, fy, travelled))
                last, k = (fx, fy), k + 1
            path = lane_path(self.road, wx, wy, self.yaw0 + own.heading, future)
            if path is None:
                self._paths[key] = None
            else:
                s0, l0, _ = path.project(np.array([[wx, wy]]))[0]
                self._paths[key] = (path, float(s0), float(l0))
        return self._paths[key]

    def to_path(self, ego: Any, t: float, local_xy: np.ndarray) -> Optional[np.ndarray]:
        """Points of the recorder's local frame in its path frame at ``t``: (arc length ahead of the recorder,
        lateral offset from its own line, + = right; path heading [rad, world])."""
        state = self.path_at(ego, t)
        if state is None:
            return None
        path, s0, l0 = state
        world = np.array([self.to_world(float(x), float(y)) for x, y in np.atleast_2d(local_xy)])
        out = path.project(world)
        out[:, 0] -= s0
        out[:, 1] -= l0
        return out

    def along_lane(self, x: float, y: float, vx: float, vy: float) -> Optional[Tuple[float, float]]:
        """The target's (local position x, y and velocity vx, vy) velocity without its component across its own
        lane, in the local frame: the null hypothesis that a car keeps its lane.  None off the map's driving
        lanes, without a direction of travel, or more than ``LANE_TRAVEL_DEG`` off its lane's direction (a car
        crossing or turning: no lane to keep)."""
        wx, wy = self.to_world(x, y)
        wvx, wvy = self.vector_to_world(vx, vy)
        speed = math.hypot(wvx, wvy)
        if speed < MIN_SPEED_MPS:
            return None
        heading = self.road.direction(wx, wy)
        if heading is None:
            return None
        dx, dy = math.cos(heading), math.sin(heading)
        along = wvx * dx + wvy * dy
        if abs(along) < speed * math.cos(math.radians(LANE_TRAVEL_DEG)):
            return None
        c, s = math.cos(self.yaw0), math.sin(self.yaw0)
        lvx, lvy = along * dx, along * dy
        return c * lvx + s * lvy, -s * lvx + c * lvy

    def lane_toward_speed(self, x: float, y: float, vx: float, vy: float,
                          ego_x: float, ego_y: float) -> Optional[float]:
        """The target's (local position x, y and velocity vx, vy) velocity across its own lane, signed toward
        the recorder at (ego_x, ego_y) (all in the recorder's local frame); None off the map's driving lanes
        or without a direction of travel."""
        wx, wy = self.to_world(x, y)
        wvx, wvy = self.vector_to_world(vx, vy)
        if math.hypot(wvx, wvy) < MIN_SPEED_MPS:
            return None
        heading = self.road.direction(wx, wy)
        if heading is None:
            return None
        dx, dy = math.cos(heading), math.sin(heading)
        if wvx * dx + wvy * dy < 0.0:  # the lane's direction of travel is the target's
            dx, dy = -dx, -dy
        nx, ny = -dy, dx
        ex, ey = self.to_world(ego_x, ego_y)
        side = (ex - wx) * nx + (ey - wy) * ny
        if abs(side) < 1e-6:
            return None
        return (wvx * nx + wvy * ny) * (1.0 if side > 0 else -1.0)


# --------------------------------------------------------------------------
# The recorder's path along its lane (road-relative ego path)
# --------------------------------------------------------------------------

PATH_STEP_M = 2.0  # spacing of the path polyline (the lane stretches are ~2 m long)
PATH_AHEAD_M = 80.0  # how far ahead the path is traced
PATH_BEHIND_M = 10.0  # straight continuation behind the recorder (bodies level with it)
CONTINUATION_M = 3.0  # the next lane stretch lies within this of the extrapolated point: no lane change
CONTINUATION_DEG = 35.0  # ... and turns by less than this per step


def _wrap(angle: float) -> float:
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


class LanePath:
    """A polyline in the world frame with arc length: the recorder's path along its lane."""

    def __init__(self, points: Sequence[Tuple[float, float]]) -> None:
        self.points = np.asarray(points, dtype=float)
        seg = np.diff(self.points, axis=0)
        self.lengths = np.hypot(seg[:, 0], seg[:, 1])
        self.headings = np.arctan2(seg[:, 1], seg[:, 0])
        self.cumulative = np.concatenate([[0.0], np.cumsum(self.lengths)])

    def project(self, xy: np.ndarray) -> np.ndarray:
        """(N, 3): arc length, signed lateral offset (+ = right of the path, as the vehicle frame) and the path
        heading [rad] at the foot of every point."""
        xy = np.atleast_2d(np.asarray(xy, dtype=float))
        a = self.points[:-1][None, :, :]
        d = (self.points[1:] - self.points[:-1])[None, :, :]
        rel = xy[:, None, :] - a
        length2 = np.maximum(np.sum(d * d, axis=2), 1e-9)
        f = np.clip(np.sum(rel * d, axis=2) / length2, 0.0, 1.0)
        foot = a + f[:, :, None] * d
        dist = np.hypot(*(xy[:, None, :] - foot).transpose(2, 0, 1))
        k = np.argmin(dist, axis=1)
        idx = np.arange(len(xy))
        h = self.headings[k]
        off = xy - foot[idx, k]
        lateral = -np.sin(h) * off[:, 0] + np.cos(h) * off[:, 1]
        s = self.cumulative[k] + f[idx, k] * self.lengths[k]
        return np.column_stack([s, lateral, h])


def lane_path(road: RoadLanes, x: float, y: float, heading: float,
              future: Optional[Sequence[Tuple[float, float, float]]] = None) -> Optional[LanePath]:
    """The recorder's path along the driving lane it is in: from its position, traced forward lane stretch by
    lane stretch (the stretch continuing the lane: within ``CONTINUATION_M`` of the extrapolated point and
    ``CONTINUATION_DEG`` of its heading).  Where several continue it (a junction), the one nearest the
    recorder's own later position at that distance (``future``: (x, y, arc length) of its recorded path).  A
    lane change or a swerve does not move the path: it follows the lane, not the recorder.  None off the lanes or
    when no lane there runs within ``LANE_TRAVEL_DEG`` of the recorder's heading (the corridor is then straight)."""
    best = None
    for index in road.tree.query_ball_point((x, y), LANE_SEARCH_M):
        lane = road.lanes[index]
        yaw = math.radians(lane.yaw)
        if abs(_wrap(yaw - heading)) > math.radians(LANE_TRAVEL_DEG):
            continue  # the recorder does not travel along this lane (a junction stretch of another direction)
        dx, dy = x - lane.x, y - lane.y
        along, across = dx * math.cos(yaw) + dy * math.sin(yaw), -dx * math.sin(yaw) + dy * math.cos(yaw)
        if abs(along) <= lane.length / 2.0 + 1.0 and abs(across) <= lane.width / 2.0 + 0.5:
            if best is None or abs(across) < best[0]:
                best = (abs(across), lane, along)
    if best is None:
        return None
    _, lane, along = best
    psi = math.radians(lane.yaw)
    px, py = lane.x + along * math.cos(psi), lane.y + along * math.sin(psi)
    points = [(px - PATH_BEHIND_M * math.cos(psi), py - PATH_BEHIND_M * math.sin(psi)), (px, py)]
    travelled = 0.0
    future_xy = None if not future else np.array([(f[0], f[1]) for f in future])
    future_s = None if not future else np.array([f[2] for f in future])
    while travelled < PATH_AHEAD_M:
        tx, ty = px + PATH_STEP_M * math.cos(psi), py + PATH_STEP_M * math.sin(psi)
        candidates = []
        for index in road.tree.query_ball_point((tx, ty), CONTINUATION_M):
            c = road.lanes[index]
            cyaw = math.radians(c.yaw)
            if abs(_wrap(cyaw - psi)) <= math.radians(CONTINUATION_DEG):
                candidates.append(c)
        travelled += PATH_STEP_M
        if candidates:
            goal = (tx, ty)
            if future_s is not None and future_s[-1] >= travelled:
                k = int(np.searchsorted(future_s, travelled))
                goal = (float(future_xy[k, 0]), float(future_xy[k, 1]))
            c = min(candidates, key=lambda c: math.hypot(c.x - goal[0], c.y - goal[1]))
            cyaw = math.radians(c.yaw)
            along = (tx - c.x) * math.cos(cyaw) + (ty - c.y) * math.sin(cyaw)
            px, py, psi = c.x + along * math.cos(cyaw), c.y + along * math.sin(cyaw), cyaw
        else:
            px, py = tx, ty
        points.append((px, py))
    return LanePath(points)
