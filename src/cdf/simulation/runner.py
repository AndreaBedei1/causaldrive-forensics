"""Execute one fixed scenario and write raw CARLA acquisitions."""

from __future__ import annotations

import json
import logging
import math
import platform
import sys
import time
from pathlib import Path
from typing import Any, List, Optional, Tuple

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


def _spectator_mode(value: Optional[str], participants: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """Return a checked spectator mode without changing scenario configuration."""
    if value is None:
        return None, None
    if value == "overhead":
        return "overhead", None
    if value.startswith("follow:"):
        participant_id = value.split(":", 1)[1]
        if participant_id in participants:
            return "follow", participant_id
        raise ValueError("spectator follow target is not a scenario participant: {0}".format(participant_id))
    raise ValueError("spectator must be 'overhead' or 'follow:<participant>'")


def _update_spectator(sworld: ScenarioWorld, agents: List[RawVehicleAgent], mode: str,
                      participant_id: Optional[str]) -> None:
    """Move CARLA's spectator only; it is not an actor or a recorded sensor."""
    carla = import_carla()
    spectator = sworld.world.get_spectator()
    if mode == "overhead":
        transforms = [agent.vehicle.get_transform() for agent in agents]
        centre_x = sum(tf.location.x for tf in transforms) / len(transforms)
        centre_y = sum(tf.location.y for tf in transforms) / len(transforms)
        centre_z = max(tf.location.z for tf in transforms)
        transform = carla.Transform(
            carla.Location(x=centre_x, y=centre_y, z=centre_z + 45.0),
            carla.Rotation(pitch=-90.0, yaw=0.0, roll=0.0),
        )
    else:
        agent = next(agent for agent in agents if agent.spec.participant_id == participant_id)
        vehicle_transform = agent.vehicle.get_transform()
        yaw_radians = math.radians(vehicle_transform.rotation.yaw)
        transform = carla.Transform(
            carla.Location(
                x=vehicle_transform.location.x - 12.0 * math.cos(yaw_radians),
                y=vehicle_transform.location.y - 12.0 * math.sin(yaw_radians),
                z=vehicle_transform.location.z + 7.0,
            ),
            carla.Rotation(pitch=-20.0, yaw=vehicle_transform.rotation.yaw, roll=0.0),
        )
    spectator.set_transform(transform)


def _pace_realtime(enabled: bool, wall_start: float, simulation_start: float,
                   simulation_timestamp: float) -> None:
    """Wait until wall time reaches a completed synchronous simulation tick."""
    if enabled:
        delay = wall_start + (simulation_timestamp - simulation_start) - time.monotonic()
        if delay > 0.0:
            time.sleep(delay)


def run_scenario(client: Any, cfg: Config, spec: ScenarioSpec, seed: int, output_root: str = "traces",
                 realtime: bool = False, spectator: Optional[str] = None,
                 hold_after_s: float = 0.0) -> Path:
    """Run one scenario variant and return its trace directory."""
    carla = import_carla()
    run_name = f"run_{int(seed)}" if spec.variant == "default" else f"run_{int(seed)}_{spec.variant}"
    run_root = Path(output_root) / spec.scenario_id / run_name
    run_root.mkdir(parents=True, exist_ok=True)
    gt = GroundTruthLogger(run_root, {"scenario_id": spec.scenario_id, "variant": spec.variant, "seed": int(seed), "map": spec.map_name})
    agents: List[RawVehicleAgent] = []
    hold_after_s = float(hold_after_s)
    if hold_after_s < 0.0:
        raise ValueError("hold_after_s must be non-negative")
    spectator_mode, spectator_participant = _spectator_mode(
        spectator, [participant.participant_id for participant in spec.participants]
    )
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
            # CARLA's elapsed clock is not reset when the requested map is
            # already loaded. Scenario limits and scripted action times are
            # defined relative to this run, whereas the recorded timestamps
            # remain CARLA's unmodified clock values.
            simulation_start = sworld.elapsed_seconds
            wall_start = time.monotonic() if realtime else 0.0
            if spectator_mode is None and not realtime:
                sworld.warmup()
            else:
                for _ in range(int(cfg.get("simulation.warmup_ticks", 20))):
                    snapshot = sworld.tick()
                    if spectator_mode is not None:
                        _update_spectator(sworld, agents, spectator_mode, spectator_participant)
                    _pace_realtime(realtime, wall_start, simulation_start, float(snapshot.timestamp.elapsed_seconds))
            for agent in agents:
                speed = float(agent.spec.initial_speed)
                if speed:
                    yaw = math.radians(agent.vehicle.get_transform().rotation.yaw)
                    agent.vehicle.set_target_velocity(carla.Vector3D(x=math.cos(yaw) * speed, y=math.sin(yaw) * speed, z=0))
            for _ in range(4):
                if spectator_mode is None and not realtime:
                    sworld.tick()
                else:
                    snapshot = sworld.tick()
                    if spectator_mode is not None:
                        _update_spectator(sworld, agents, spectator_mode, spectator_participant)
                    _pace_realtime(realtime, wall_start, simulation_start, float(snapshot.timestamp.elapsed_seconds))
            dt = sworld.delta_seconds
            limit = min(float(spec.max_duration_s), float(cfg.get("simulation.max_duration_s", spec.max_duration_s)))
            while sworld.elapsed_seconds - simulation_start <= limit + 1e-9:
                snapshot = sworld.tick(); frame = int(snapshot.frame); timestamp = float(snapshot.timestamp.elapsed_seconds)
                scenario_timestamp = timestamp - simulation_start
                controls = {
                    agent.spec.participant_id: agent.step(
                        scenario_timestamp, frame, dt, recorded_timestamp=timestamp
                    )
                    for agent in agents
                }
                for agent in agents:
                    gt.state({"participant_id": agent.spec.participant_id, **_state(agent.vehicle, frame, timestamp)})
                    gt.control({"participant_id": agent.spec.participant_id, **controls[agent.spec.participant_id]})
                    for collision in agent.ground_truth_collisions():
                        gt.collision({"participant_id": agent.spec.participant_id, **collision})
                if spectator_mode is not None:
                    _update_spectator(sworld, agents, spectator_mode, spectator_participant)
                if realtime:
                    _pace_realtime(True, wall_start, simulation_start, timestamp)
            if hold_after_s > 0.0:
                time.sleep(hold_after_s)
    finally:
        for agent in agents: agent.close()
        gt.close()
    metadata = {"scenario_id": spec.scenario_id, "variant": spec.variant, "seed": int(seed), "participants": [p.participant_id for p in spec.participants], "python": sys.version, "platform": platform.platform(), "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    (run_root / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    return run_root
