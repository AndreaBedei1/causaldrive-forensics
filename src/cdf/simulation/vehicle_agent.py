"""One vehicle's controller and raw onboard recording."""

from __future__ import annotations

from typing import Any

from ..common.config import Config
from ..recording.vehicle_logger import VehicleLogger
from .controllers import ScriptedController, VehicleState
from .sensors import CameraSensor, CollisionSensor, RadarSensor, camera_spec_from_config, radar_specs_from_config


class RawVehicleAgent:
    def __init__(self, scenario_world: Any, cfg: Config, spec: Any, controller: ScriptedController,
                 spawn_transform: Any, output_root: Any) -> None:
        self.world = scenario_world; self.cfg = cfg; self.spec = spec; self.controller = controller
        self.vehicle = scenario_world.spawn_vehicle(spec.blueprint, spawn_transform)
        self.radar = [RadarSensor(scenario_world, self.vehicle, rs) for rs in radar_specs_from_config(cfg)]
        camera_spec = camera_spec_from_config(cfg)
        self.camera = CameraSensor(scenario_world, self.vehicle, camera_spec) if camera_spec else None
        self.collision_sensor = CollisionSensor(scenario_world, self.vehicle)
        self.logger = VehicleLogger(output_root, spec.participant_id, {
            "participant_id": spec.participant_id, "blueprint": spec.blueprint,
            "radar": [r.spec.__dict__ for r in self.radar],
            "camera": camera_spec.__dict__ if camera_spec else None,
            "vehicle_transform": {"x": spawn_transform.location.x, "y": spawn_transform.location.y, "z": spawn_transform.location.z, "yaw_deg": spawn_transform.rotation.yaw},
        })

    def state_record(self, t: float, frame: int) -> dict:
        tf = self.vehicle.get_transform(); v = self.vehicle.get_velocity(); a = self.vehicle.get_acceleration(); ang = self.vehicle.get_angular_velocity()
        return {"frame": int(frame), "timestamp": float(t), "x": float(tf.location.x), "y": float(tf.location.y), "z": float(tf.location.z),
                "roll_deg": float(tf.rotation.roll), "pitch_deg": float(tf.rotation.pitch), "yaw_deg": float(tf.rotation.yaw),
                "velocity": {"x": float(v.x), "y": float(v.y), "z": float(v.z)}, "acceleration": {"x": float(a.x), "y": float(a.y), "z": float(a.z)},
                "angular_velocity": {"x": float(ang.x), "y": float(ang.y), "z": float(ang.z)}}

    def step(self, t: float, frame: int, dt: float) -> dict:
        record = self.state_record(t, frame)
        speed = (record["velocity"]["x"] ** 2 + record["velocity"]["y"] ** 2 + record["velocity"]["z"] ** 2) ** 0.5
        state = VehicleState(t=t, x=record["x"], y=record["y"], yaw=record["yaw_deg"], speed=speed,
                             vx=record["velocity"]["x"], vy=record["velocity"]["y"])
        command = self.controller.step(state, dt)
        self.vehicle.apply_control(command.clamped())
        self.logger.log_state(record)
        self.logger.log_control({"frame": int(frame), "timestamp": float(t), "throttle": command.throttle, "brake": command.brake,
                                 "steer": command.steer, "hand_brake": command.hand_brake, "reverse": command.reverse})
        for radar in self.radar:
            item = radar.poll(frame)
            if item is not None: self.logger.log_radar(item)
        if self.camera is not None:
            item = self.camera.poll(frame)
            if item is not None:
                data = item.pop("data"); self.logger.log_camera(item, data)
        for collision in self.collision_sensor.drain_vehicle(): self.logger.log_collision(collision)
        return {"frame": int(frame), "timestamp": float(t), "throttle": command.throttle, "brake": command.brake,
                "steer": command.steer, "hand_brake": command.hand_brake, "reverse": command.reverse}

    def ground_truth_collisions(self):
        return self.collision_sensor.drain_ground_truth()

    def close(self) -> None:
        self.logger.close()
