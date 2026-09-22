"""One vehicle's controller and raw onboard recording."""

from __future__ import annotations

from collections import deque
from concurrent.futures import ThreadPoolExecutor
import time
from typing import Any

from ..common.config import Config, configs_dir, load_yaml
from ..recording.vehicle_logger import VehicleLogger
from .carla_client import import_carla
from .controllers import ScriptedController, VehicleState
from .sensors import (CameraSensor, CollisionSensor, RadarSensor,
                      camera_spec_from_config, depth_camera_spec_from_config,
                      depth_radial_velocity_config_from_config,
                      depth_observation_spec_from_config,
                      depth_observations_from_bgra, radar_specs_from_config)
from ..recording.depth_velocity import DepthRadialVelocityEstimator



class RawVehicleAgent:
    def __init__(self, scenario_world: Any, cfg: Config, spec: Any, controller: ScriptedController,
                 spawn_transform: Any, output_root: Any) -> None:
        self.world = scenario_world; self.cfg = cfg; self.spec = spec; self.controller = controller
        self.vehicle = scenario_world.spawn_vehicle(spec.blueprint, spawn_transform)
        sensor_cfg = cfg
        if spec.sensor_profile:
            profile_path = configs_dir() / "sensors" / (str(spec.sensor_profile) + ".yaml")
            profile = load_yaml(profile_path)
            sensor_cfg = cfg.with_overrides({"radar": profile.get("radar", {}), "sensors": {"profile": str(spec.sensor_profile)}})
        self.radar = [RadarSensor(scenario_world, self.vehicle, rs) for rs in radar_specs_from_config(sensor_cfg)]
        camera_spec = camera_spec_from_config(cfg)
        depth_camera_spec = depth_camera_spec_from_config(cfg)
        self.depth_observation_spec = depth_observation_spec_from_config(cfg)
        self._depth_executor = ThreadPoolExecutor(max_workers=1) if depth_camera_spec else None
        self._depth_futures = deque()
        self.camera = CameraSensor(scenario_world, self.vehicle, camera_spec) if camera_spec else None
        self.depth_camera = (CameraSensor(scenario_world, self.vehicle, depth_camera_spec,
                                          max_queue=512, report_frame_gaps=True)
                             if depth_camera_spec else None)
        self.depth_velocity_config = depth_radial_velocity_config_from_config(cfg)
        self._depth_estimator = DepthRadialVelocityEstimator(self.depth_velocity_config)
        self.collision_sensor = CollisionSensor(scenario_world, self.vehicle)
        self.logger = VehicleLogger(output_root, spec.participant_id, {
            "participant_id": spec.participant_id, "blueprint": spec.blueprint,
            "sensor_profile": str(spec.sensor_profile or cfg.get("sensors.profile", "")),
            "radar": [r.spec.__dict__ for r in self.radar],
            "camera": camera_spec.__dict__ if camera_spec else None,
            "depth_camera": depth_camera_spec.__dict__ if depth_camera_spec else None,
            "depth_observations": self.depth_observation_spec.__dict__,
            "depth_radial_velocity": self.depth_velocity_config.as_metadata(),
            "vehicle_transform": {"x": spawn_transform.location.x, "y": spawn_transform.location.y, "z": spawn_transform.location.z, "yaw_deg": spawn_transform.rotation.yaw},
        })

    def state_record(self, t: float, frame: int) -> dict:
        tf = self.vehicle.get_transform(); v = self.vehicle.get_velocity(); a = self.vehicle.get_acceleration(); ang = self.vehicle.get_angular_velocity()
        return {"frame": int(frame), "timestamp": float(t), "x": float(tf.location.x), "y": float(tf.location.y), "z": float(tf.location.z),
                "roll_deg": float(tf.rotation.roll), "pitch_deg": float(tf.rotation.pitch), "yaw_deg": float(tf.rotation.yaw),
                "velocity": {"x": float(v.x), "y": float(v.y), "z": float(v.z)}, "acceleration": {"x": float(a.x), "y": float(a.y), "z": float(a.z)},
                "angular_velocity": {"x": float(ang.x), "y": float(ang.y), "z": float(ang.z)}}

    def set_sensor_start_frame(self, frame: int) -> None:
        """Exclude warm-up callbacks while retaining later delayed images."""
        if self.camera is not None:
            self.camera.set_minimum_frame(frame)
        if self.depth_camera is not None:
            self.depth_camera.set_minimum_frame(frame)

    def _submit_depth(self, item: dict) -> None:
        data = item.pop("data")
        item["source"] = "depth"
        future = self._depth_executor.submit(
            depth_observations_from_bgra,
            data, item["width"], item["height"], item["fov_deg"],
            self.depth_observation_spec,
        )
        self._depth_futures.append((item, future))

    def _drain_depth_futures(self, wait: bool = False) -> None:
        ready = []
        while self._depth_futures:
            item, future = self._depth_futures[0]
            if not wait and not future.done():
                break
            item["detections"] = future.result()
            self._depth_futures.popleft()
            ready.append(item)
        # Callbacks can arrive out of order; temporal state is updated only in
        # increasing CARLA timestamp order (frame is a deterministic tie-breaker).
        ready.sort(key=lambda record: (float(record["timestamp"]), int(record["frame"])))
        for item in ready:
            item["detections"] = self._depth_estimator.process(
                int(item["frame"]), float(item["timestamp"]), item["detections"]
            )
            self.logger.log_depth_observations(item)

    def step(self, t: float, frame: int, dt: float, recorded_timestamp: float = None) -> dict:
        """Advance the scripted controller using ``t`` and log CARLA's raw time."""
        timestamp = float(t) if recorded_timestamp is None else float(recorded_timestamp)
        record = self.state_record(timestamp, frame)
        speed = (record["velocity"]["x"] ** 2 + record["velocity"]["y"] ** 2 + record["velocity"]["z"] ** 2) ** 0.5
        state = VehicleState(t=t, x=record["x"], y=record["y"], yaw=record["yaw_deg"], speed=speed,
                             vx=record["velocity"]["x"], vy=record["velocity"]["y"])
        command = self.controller.step(state, dt)
        clamped = command.clamped()
        carla = import_carla()
        self.vehicle.apply_control(carla.VehicleControl(
            throttle=clamped.throttle, brake=clamped.brake, steer=clamped.steer,
            hand_brake=clamped.hand_brake, reverse=clamped.reverse,
        ))
        self.logger.log_state(record)
        self.logger.log_control({"frame": int(frame), "timestamp": timestamp, "throttle": command.throttle, "brake": command.brake,
                                 "steer": command.steer, "hand_brake": command.hand_brake, "reverse": command.reverse})
        for radar in self.radar:
            item = radar.poll(frame)
            if item is not None: self.logger.log_radar(item)
        if self.camera is not None:
            for item in self.camera.drain_available():
                data = item.pop("data")
                item["source"] = "rgb"
                self.logger.log_camera(item, data)
        if self.depth_camera is not None:
            for item in self.depth_camera.drain_available():
                self._submit_depth(item)
            self._drain_depth_futures()
        for collision in self.collision_sensor.drain_vehicle():
            self.logger.log_collision(collision)
            self.controller.notify_impact()
        return {"frame": int(frame), "timestamp": timestamp, "throttle": command.throttle, "brake": command.brake,
                "steer": command.steer, "hand_brake": command.hand_brake, "reverse": command.reverse}

    def flush_sensor_queues(self, timeout_s: float = 2.0) -> None:
        """Process already-delivered callbacks without advancing the world."""
        deadline = time.monotonic() + float(timeout_s)
        while time.monotonic() < deadline:
            drained = False
            if self.camera is not None:
                items = self.camera.drain_available()
                drained = drained or bool(items)
                for item in items:
                    data = item.pop("data")
                    item["source"] = "rgb"
                    self.logger.log_camera(item, data)
            if self.depth_camera is not None:
                items = self.depth_camera.drain_available()
                drained = drained or bool(items)
                for item in items:
                    self._submit_depth(item)
                self._drain_depth_futures()
            time.sleep(0.005)
        self._drain_depth_futures(wait=True)

    def ground_truth_collisions(self):
        return self.collision_sensor.drain_ground_truth()

    def close(self) -> None:
        if self._depth_executor is not None:
            self._depth_executor.shutdown(wait=True)
        if self.camera is not None:
            self.logger.set_camera_stats(self.camera.stats)
        if self.depth_camera is not None:
            depth_stats = dict(self.depth_camera.stats)
            depth_stats["radial_velocity"] = self._depth_estimator.stats.as_dict()
            self.logger.set_depth_stats(depth_stats)
        for radar in self.radar:
            self.logger.set_radar_stats(radar.spec.sensor_id, radar.stats)
        self.logger.close()
