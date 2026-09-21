"""Execute one fixed scenario and write raw CARLA acquisitions."""

from __future__ import annotations

import json
import logging
import math
import platform
import sys
import time
from pathlib import Path
from typing import Any, List

from ..common.config import Config
from ..common.geometry import distance
from ..recording.ground_truth_logger import GroundTruthLogger
from .carla_client import import_carla
from .scenario_base import ScenarioSpec, build_route, make_controller, resolve_spawn_waypoint
from .vehicle_agent import RawVehicleAgent
from .world import ScenarioWorld

LOGGER = logging.getLogger(__name__)


def _state(actor: Any, frame: int, timestamp: float) -> dict:
    tf = actor.get_transform(); v = actor.get_velocity(); a = actor.get_acceleration(); w = actor.get_angular_velocity()
    return {"frame": int(frame), "timestamp": float(timestamp), "actor_id": int(actor.id), "type_id": str(actor.type_id),
            "transform": {"x": float(tf.location.x), "y": float(tf.location.y), "z": float(tf.location.z), "roll_deg": float(tf.rotation.roll), "pitch_deg": float(tf.rotation.pitch), "yaw_deg": float(tf.rotation.yaw)},
            "velocity": {"x": float(v.x), "y": float(v.y), "z": float(v.z)}, "acceleration": {"x": float(a.x), "y": float(a.y), "z": float(a.z)},
            "angular_velocity": {"x": float(w.x), "y": float(w.y), "z": float(w.z)}}


def run_scenario(client: Any, cfg: Config, spec: ScenarioSpec, seed: int, output_root: str = "traces") -> Path:
    """Run one scenario variant and return its trace directory."""
    carla = import_carla()
    run_name = f"run_{int(seed)}" if spec.variant == "default" else f"run_{int(seed)}_{spec.variant}"
    run_root = Path(output_root) / spec.scenario_id / run_name
    run_root.mkdir(parents=True, exist_ok=True)
    gt = GroundTruthLogger(run_root, {"scenario_id": spec.scenario_id, "variant": spec.variant, "seed": int(seed), "map": spec.map_name})
    agents: List[RawVehicleAgent] = []
    try:
        with ScenarioWorld(client, cfg, spec.map_name, seed=seed) as sworld:
            placements = []
            for pspec in spec.participants:
                wp = resolve_spawn_waypoint(sworld.map, sworld.spawn_points(), pspec.spawn)
                placements.append((pspec, wp, build_route(sworld.map, wp, pspec.route)))
            for i, (_, wp, _) in enumerate(placements):
                for _, prior, _ in placements[:i]:
                    if distance(wp.transform.location.x, wp.transform.location.y, prior.transform.location.x, prior.transform.location.y) < float(cfg.get("simulation.min_spawn_gap_m", 5.0)):
                        raise ValueError("scenario spawn points are too close")
            for pspec, wp, route in placements:
                tf = wp.transform
                transform = carla.Transform(carla.Location(x=tf.location.x, y=tf.location.y, z=tf.location.z + float(cfg.get("simulation.spawn_z_offset", 0.3))), carla.Rotation(pitch=0, yaw=tf.rotation.yaw, roll=0))
                agent = RawVehicleAgent(sworld, cfg, pspec, make_controller(pspec, route), transform, run_root)
                agents.append(agent)
            sworld.warmup()
            for agent in agents:
                speed = float(agent.spec.initial_speed)
                if speed:
                    yaw = math.radians(agent.vehicle.get_transform().rotation.yaw)
                    agent.vehicle.set_target_velocity(carla.Vector3D(x=math.cos(yaw) * speed, y=math.sin(yaw) * speed, z=0))
            for _ in range(4): sworld.tick()
            dt = sworld.delta_seconds
            limit = min(float(spec.max_duration_s), float(cfg.get("simulation.max_duration_s", spec.max_duration_s)))
            while sworld.elapsed_seconds <= limit + 1e-9:
                snapshot = sworld.tick(); frame = int(snapshot.frame); timestamp = float(snapshot.timestamp.elapsed_seconds)
                controls = {agent.spec.participant_id: agent.step(timestamp, frame, dt) for agent in agents}
                for agent in agents:
                    gt.state({"participant_id": agent.spec.participant_id, **_state(agent.vehicle, frame, timestamp)})
                    gt.control({"participant_id": agent.spec.participant_id, **controls[agent.spec.participant_id]})
                    for collision in agent.ground_truth_collisions():
                        gt.collision({"participant_id": agent.spec.participant_id, **collision})
    finally:
        for agent in agents: agent.close()
        gt.close()
    metadata = {"scenario_id": spec.scenario_id, "variant": spec.variant, "seed": int(seed), "participants": [p.participant_id for p in spec.participants], "python": sys.version, "platform": platform.platform(), "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    (run_root / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    return run_root
