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
POST_IMPACT_RECORDING_S = 5.0


def _state(actor: Any, frame: int, timestamp: float) -> dict:
    tf = actor.get_transform(); v = actor.get_velocity(); a = actor.get_acceleration(); w = actor.get_angular_velocity()
    return {"frame": int(frame), "timestamp": float(timestamp), "actor_id": int(actor.id), "type_id": str(actor.type_id),
            "transform": {"x": float(tf.location.x), "y": float(tf.location.y), "z": float(tf.location.z), "roll_deg": float(tf.rotation.roll), "pitch_deg": float(tf.rotation.pitch), "yaw_deg": float(tf.rotation.yaw)},
            "velocity": {"x": float(v.x), "y": float(v.y), "z": float(v.z)}, "acceleration": {"x": float(a.x), "y": float(a.y), "z": float(a.z)},
            "angular_velocity": {"x": float(w.x), "y": float(w.y), "z": float(w.z)}}


def _position_spectator(world: Any, vehicles: List[Any], carla: Any) -> None:
    """Keep CARLA's spectator on a read-only overhead view of the run."""
    if not vehicles:
        return
    transforms = [vehicle.get_transform() for vehicle in vehicles]
    locations = [transform.location for transform in transforms]
    center_x = sum(float(location.x) for location in locations) / len(locations)
    center_y = sum(float(location.y) for location in locations) / len(locations)
    center_z = sum(float(location.z) for location in locations) / len(locations)
    span = max(
        max(float(location.x) for location in locations) - min(float(location.x) for location in locations),
        max(float(location.y) for location in locations) - min(float(location.y) for location in locations),
        1.0,
    )
    offset = min(12.0, max(6.0, span * 0.2))
    altitude = max(35.0, min(45.0, 35.0 + span * 0.15))
    camera_location = carla.Location(
        x=center_x + offset,
        y=center_y - offset,
        z=center_z + altitude,
    )
    look_x = center_x - float(camera_location.x)
    look_y = center_y - float(camera_location.y)
    look_z = center_z - float(camera_location.z)
    horizontal = math.hypot(look_x, look_y)
    spectator = world.get_spectator()
    spectator.set_transform(
        carla.Transform(
            camera_location,
            carla.Rotation(
                pitch=math.degrees(math.atan2(look_z, horizontal)),
                yaw=math.degrees(math.atan2(look_y, look_x)),
                roll=0.0,
            ),
        )
    )


def run_scenario(client: Any, cfg: Config, spec: ScenarioSpec, seed: int, output_root: str = "traces") -> Path:
    """Run one scenario variant and return its trace directory."""
    carla = import_carla()
    run_name = f"run_{int(seed)}" if spec.variant == "default" else f"run_{int(seed)}_{spec.variant}"
    run_root = Path(output_root) / spec.scenario_id / run_name
    run_root.mkdir(parents=True, exist_ok=True)
    gt = GroundTruthLogger(run_root, {"scenario_id": spec.scenario_id, "variant": spec.variant, "seed": int(seed), "map": spec.map_name})
    agents: List[RawVehicleAgent] = []
    simulation_start_timestamp = None
    simulation_end_timestamp = None
    fixed_delta_seconds = None
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
            # CARLA's elapsed clock is not reset when the requested map is
            # already loaded. The scripted timeline begins after physics has
            # settled and the configured initial velocity has taken effect,
            # exactly as the scenario definitions expect.
            simulation_start = sworld.elapsed_seconds
            dt = sworld.delta_seconds
            simulation_start_timestamp = float(simulation_start)
            fixed_delta_seconds = float(dt)
            _position_spectator(sworld.world, [agent.vehicle for agent in agents], carla)
            for agent in agents:
                agent.set_sensor_start_frame(sworld.frame + 1)
            limit = min(float(spec.max_duration_s), float(cfg.get("simulation.max_duration_s", spec.max_duration_s)))
            scheduled_end = max(
                [float(action.t_start) + float(action.duration)
                 for participant in spec.participants for action in participant.actions],
                default=0.0,
            )
            last_collision_t = None
            wall_clock_start = time.monotonic()
            while sworld.elapsed_seconds - simulation_start <= limit + 1e-9:
                snapshot = sworld.tick(); frame = int(snapshot.frame); timestamp = float(snapshot.timestamp.elapsed_seconds)
                simulation_end_timestamp = timestamp
                scenario_timestamp = timestamp - simulation_start
                _position_spectator(sworld.world, [agent.vehicle for agent in agents], carla)
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
                        last_collision_t = scenario_timestamp
                # The reference runner ended a non-contact recording once every
                # declared manoeuvre had completed.  When a contact occurs, it
                # instead retains a fixed post-impact window, anchored to the
                # latest physical collision so a chain's secondary impact is
                # never truncated.  This is execution/capture control only;
                # it does not inspect expected outcomes or alter vehicle inputs.
                if scheduled_end > 0.0:
                    if last_collision_t is None and scenario_timestamp >= scheduled_end:
                        break
                    if (last_collision_t is not None
                            and scenario_timestamp >= scheduled_end
                            and scenario_timestamp >= last_collision_t + POST_IMPACT_RECORDING_S):
                        break
                remaining_wall_time = wall_clock_start + scenario_timestamp - time.monotonic()
                if remaining_wall_time > 0.0:
                    time.sleep(remaining_wall_time)
            for agent in agents:
                agent.flush_sensor_queues()
    finally:
        for agent in agents: agent.close()
        gt.close()
    metadata = {"scenario_id": spec.scenario_id, "variant": spec.variant, "seed": int(seed), "participants": [p.participant_id for p in spec.participants], "python": sys.version, "platform": platform.platform(), "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if simulation_start_timestamp is not None:
        metadata["simulation_start_timestamp"] = simulation_start_timestamp
    if fixed_delta_seconds is not None:
        metadata["fixed_delta_seconds"] = fixed_delta_seconds
    if simulation_end_timestamp is not None and simulation_start_timestamp is not None:
        metadata["simulation_end_timestamp"] = simulation_end_timestamp
        metadata["recorded_duration_s"] = simulation_end_timestamp - simulation_start_timestamp
    (run_root / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    return run_root
