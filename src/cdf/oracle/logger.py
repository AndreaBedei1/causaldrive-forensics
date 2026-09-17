"""Privileged ground-truth logger.

PRIVILEGED LAYER -- EVALUATION ONLY.

This module is the *only* place that reads global simulator state: exact actor
poses and velocities, the true collision pairs, map metadata (lane/road/junction
ids), traffic-light states and the scripted intervention timeline. Everything it
produces is ground truth used to score the local and fused reconstructions, and
it must never be fed back into inference.

Two structural safeguards back that up:

* Oracle artifacts are written under ``oracle/`` and every graph it emits carries
  ``scope=Provenance.ORACLE``; :func:`cdf.graph.export.load_graph` refuses to hand
  such a document to a stage that asked for a local or fused graph.
* ``tests/test_no_privileged_leakage.py`` fails if any module under ``cdf.local``
  or ``cdf.fusion`` imports this package, or if a privileged field name appears in
  a local or fused artifact.

Only :mod:`cdf.oracle.logger` needs the simulator; the rest of the oracle package
works on the persisted trace and imports no CARLA API.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..common.io import write_json, write_jsonl_gz
from ..common.layout import RunLayout
from ..simulation.carla_client import import_carla

LOGGER = logging.getLogger(__name__)

__all__ = ["OracleActorState", "OracleFrame", "OracleLogger", "ORACLE_TRACE_SCHEMA_VERSION"]

ORACLE_TRACE_SCHEMA_VERSION = "1.0.0"


@dataclass
class OracleActorState:
    """Exact state of one participant at one frame. PRIVILEGED."""

    participant_id: str
    actor_id: int
    x: float
    y: float
    z: float
    yaw: float
    pitch: float
    roll: float
    vx: float
    vy: float
    vz: float
    speed: float
    ax: float
    ay: float
    az: float
    yaw_rate: float
    throttle: float
    brake: float
    steer: float
    # --- privileged map context ---
    lane_id: Optional[int] = None
    road_id: Optional[int] = None
    section_id: Optional[int] = None
    is_junction: bool = False
    junction_id: Optional[int] = None
    traffic_light_state: Optional[str] = None
    traffic_light_id: Optional[int] = None
    is_at_traffic_light: bool = False


@dataclass
class OracleFrame:
    """All privileged state at one simulation step."""

    t: float
    frame: int
    actors: List[OracleActorState] = field(default_factory=list)
    traffic_lights: List[Dict[str, Any]] = field(default_factory=list)


class OracleLogger:
    """Records exact simulator state for every participant, every tick.

    The logger also owns the *true* collision record: it drains the privileged
    side of each participant's collision sensor, which is the only path by which
    the identity of a collision partner ever becomes known.
    """

    def __init__(
        self,
        scenario_id: str,
        run_id: str,
        seed: int,
        variant: str = "default",
        map_name: str = "",
        record_traffic_lights: bool = True,
    ) -> None:
        self.scenario_id = scenario_id
        self.run_id = run_id
        self.seed = int(seed)
        self.variant = variant
        self.map_name = map_name
        self.record_traffic_lights = bool(record_traffic_lights)

        self._participants: Dict[str, Any] = {}
        self._collision_sensors: Dict[str, Any] = {}
        self._controllers: Dict[str, Any] = {}
        self._frames: List[OracleFrame] = []
        self._collisions: List[Dict[str, Any]] = []
        self._actor_to_participant: Dict[int, str] = {}
        self._carla_map: Any = None
        self._notes: List[str] = []
        # Collision events arrive stamped with the simulator's absolute clock,
        # while the rest of the run is recorded on scenario time. Without this
        # offset the oracle's collision timestamps would sit on a different clock
        # from the evidence they are meant to score.
        self.time_offset: float = 0.0

    # -- registration -----------------------------------------------------

    def bind_map(self, carla_map: Any) -> None:
        """Provide the CARLA map so lane/road/junction context can be recorded."""
        self._carla_map = carla_map

    def register(
        self,
        participant_id: str,
        actor: Any,
        collision_sensor: Optional[Any] = None,
        controller: Optional[Any] = None,
    ) -> None:
        """Register a participant whose exact state should be recorded."""
        self._participants[participant_id] = actor
        self._actor_to_participant[int(actor.id)] = participant_id
        if collision_sensor is not None:
            self._collision_sensors[participant_id] = collision_sensor
        if controller is not None:
            self._controllers[participant_id] = controller

    def participant_of_actor(self, actor_id: int) -> Optional[str]:
        """Resolve a CARLA actor id to a participant label. PRIVILEGED."""
        return self._actor_to_participant.get(int(actor_id))

    # -- capture ----------------------------------------------------------

    def capture(self, t: float, frame: int, world: Optional[Any] = None) -> OracleFrame:
        """Record exact state for every registered participant at this tick."""
        carla = import_carla()
        states: List[OracleActorState] = []

        for pid, actor in self._participants.items():
            tf = actor.get_transform()
            vel = actor.get_velocity()
            acc = actor.get_acceleration()
            ang = actor.get_angular_velocity()
            ctrl = actor.get_control()

            lane_id = road_id = section_id = junction_id = None
            is_junction = False
            if self._carla_map is not None:
                wp = self._carla_map.get_waypoint(
                    tf.location, project_to_road=True, lane_type=carla.LaneType.Driving
                )
                if wp is not None:
                    lane_id = int(wp.lane_id)
                    road_id = int(wp.road_id)
                    section_id = int(wp.section_id)
                    is_junction = bool(wp.is_junction)
                    if is_junction:
                        junction = wp.get_junction()
                        junction_id = int(junction.id) if junction is not None else None

            tl_state = None
            tl_id = None
            at_light = False
            try:
                at_light = bool(actor.is_at_traffic_light())
                light = actor.get_traffic_light()
                if light is not None:
                    tl_state = str(actor.get_traffic_light_state())
                    tl_id = int(light.id)
            except RuntimeError as exc:
                LOGGER.debug("traffic light query failed for %s: %s", pid, exc)

            speed = float((vel.x ** 2 + vel.y ** 2 + vel.z ** 2) ** 0.5)
            states.append(
                OracleActorState(
                    participant_id=pid,
                    actor_id=int(actor.id),
                    x=float(tf.location.x),
                    y=float(tf.location.y),
                    z=float(tf.location.z),
                    yaw=float(tf.rotation.yaw),
                    pitch=float(tf.rotation.pitch),
                    roll=float(tf.rotation.roll),
                    vx=float(vel.x),
                    vy=float(vel.y),
                    vz=float(vel.z),
                    speed=speed,
                    ax=float(acc.x),
                    ay=float(acc.y),
                    az=float(acc.z),
                    yaw_rate=float(ang.z),
                    throttle=float(ctrl.throttle),
                    brake=float(ctrl.brake),
                    steer=float(ctrl.steer),
                    lane_id=lane_id,
                    road_id=road_id,
                    section_id=section_id,
                    is_junction=is_junction,
                    junction_id=junction_id,
                    traffic_light_state=tl_state,
                    traffic_light_id=tl_id,
                    is_at_traffic_light=at_light,
                )
            )

        lights: List[Dict[str, Any]] = []
        if self.record_traffic_lights and world is not None:
            for light in world.get_actors().filter("traffic.traffic_light"):
                loc = light.get_transform().location
                lights.append(
                    {
                        "traffic_light_id": int(light.id),
                        "state": str(light.get_state()),
                        "x": float(loc.x),
                        "y": float(loc.y),
                    }
                )

        oframe = OracleFrame(t=float(t), frame=int(frame), actors=states, traffic_lights=lights)
        self._frames.append(oframe)
        self._drain_collisions(t)
        return oframe

    def _drain_collisions(self, t: float) -> None:
        """Collect true collision pairs from the privileged sensor channel."""
        for pid, sensor in self._collision_sensors.items():
            for raw in sensor.drain_privileged():
                other_pid = self.participant_of_actor(raw["other_actor_id"])
                self._collisions.append(
                    {
                        "t": float(raw["t"]) - self.time_offset,
                        "frame": raw["frame"],
                        "participant_id": pid,
                        "other_participant_id": other_pid,
                        "other_actor_id": raw["other_actor_id"],
                        "other_type_id": raw["other_type_id"],
                        "impulse": raw["impulse"],
                        "is_participant_pair": other_pid is not None,
                    }
                )

    # -- results ----------------------------------------------------------

    @property
    def collisions(self) -> List[Dict[str, Any]]:
        """True collision records, including the identity of both parties."""
        return list(self._collisions)

    @property
    def frames(self) -> List[OracleFrame]:
        return list(self._frames)

    def participant_ids(self) -> List[str]:
        return sorted(self._participants.keys())

    def add_note(self, note: str) -> None:
        """Attach a diagnostic note to the trace (e.g. a validation warning)."""
        self._notes.append(note)

    def collision_pairs(self) -> List[Tuple[str, str, float]]:
        """Deduplicated ``(a, b, t)`` participant collision pairs, time-ordered.

        CARLA reports an impact once per involved actor, so the raw records
        contain each pair twice; the canonical pair is order-independent.
        """
        seen: Dict[Tuple[str, str], float] = {}
        for c in sorted(self._collisions, key=lambda r: float(r["t"])):
            other = c.get("other_participant_id")
            if other is None:
                continue
            key = tuple(sorted((c["participant_id"], other)))
            if key not in seen:
                seen[key] = float(c["t"])
        return [(k[0], k[1], v) for k, v in sorted(seen.items(), key=lambda kv: kv[1])]

    def trace(self) -> Dict[str, Any]:
        """The full privileged trace as a serialisable mapping."""
        return {
            "schema_version": ORACLE_TRACE_SCHEMA_VERSION,
            "provenance": "oracle",
            "scenario_id": self.scenario_id,
            "run_id": self.run_id,
            "seed": self.seed,
            "variant": self.variant,
            "map_name": self.map_name,
            "participants": self.participant_ids(),
            "n_frames": len(self._frames),
            "collisions": self._collisions,
            "collision_pairs": [
                {"a": a, "b": b, "t": t} for (a, b, t) in self.collision_pairs()
            ],
            "interventions": {
                pid: ctrl.describe() for pid, ctrl in self._controllers.items()
            },
            "notes": list(self._notes),
        }

    def frame_rows(self) -> List[Dict[str, Any]]:
        """The per-frame trace as plain dicts, ready for JSON-lines output."""
        rows: List[Dict[str, Any]] = []
        for f in self._frames:
            rows.append(
                {
                    "t": f.t,
                    "frame": f.frame,
                    "actors": [asdict(a) for a in f.actors],
                    "traffic_lights": f.traffic_lights,
                }
            )
        return rows

    def persist(self, layout: RunLayout) -> Dict[str, Any]:
        """Write the privileged trace under ``oracle/``."""
        layout.oracle_dir.mkdir(parents=True, exist_ok=True)
        write_jsonl_gz(layout.oracle_trace, self.frame_rows())
        summary = self.trace()
        write_json(layout.oracle_dir / "oracle_summary.json", summary)
        LOGGER.info(
            "oracle trace persisted: %d frames, %d collision records",
            len(self._frames),
            len(self._collisions),
        )
        return summary

    # -- convenience for scenario validation ------------------------------

    def state_series(self, participant_id: str) -> List[OracleActorState]:
        """Every recorded state for one participant, in time order."""
        out: List[OracleActorState] = []
        for f in self._frames:
            for a in f.actors:
                if a.participant_id == participant_id:
                    out.append(a)
        return out

    def min_separation(self, a: str, b: str) -> Optional[Tuple[float, float]]:
        """Minimum true centre-to-centre distance between two participants.

        Returns ``(t, distance)``, or ``None`` when either participant has no
        recorded state. Used to validate that an intended encounter happened.
        """
        best: Optional[Tuple[float, float]] = None
        for f in self._frames:
            pa = next((s for s in f.actors if s.participant_id == a), None)
            pb = next((s for s in f.actors if s.participant_id == b), None)
            if pa is None or pb is None:
                continue
            d = float(((pa.x - pb.x) ** 2 + (pa.y - pb.y) ** 2) ** 0.5)
            if best is None or d < best[1]:
                best = (f.t, d)
        return best
