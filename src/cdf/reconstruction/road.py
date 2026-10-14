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
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

import numpy as np

from ..common.opendrive import LaneSample, best_map

OPENDRIVE_DIR = Path("CarlaUE4") / "Content" / "Carla" / "Maps" / "OpenDrive"
MAP_MIN_FIT = 0.8  # share of the recorder's positions inside the map's driving lanes
LANE_SEARCH_M = 4.0  # lane stretches within this distance of a point are candidates
MIN_SPEED_MPS = 1.0  # below, a target has no direction of travel


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
