"""Raw CARLA sensor adapters with frame-matched queues."""

from __future__ import annotations

import math
import queue
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..common.config import Config
from .carla_client import import_carla


@dataclass
class RadarSpec:
    sensor_id: str = "front"
    blueprint: str = "sensor.other.radar"
    horizontal_fov_deg: float = 120.0
    vertical_fov_deg: float = 10.0
    range_m: float = 90.0
    points_per_second: int = 6000
    sensor_tick_s: float = 0.05
    mount_x: float = 2.2
    mount_y: float = 0.0
    mount_z: float = 1.0
    mount_yaw_deg: float = 0.0
    mount_pitch_deg: float = 0.0

    def attributes(self) -> Dict[str, Any]:
        return {"horizontal_fov": self.horizontal_fov_deg, "vertical_fov": self.vertical_fov_deg,
                "range": self.range_m, "points_per_second": self.points_per_second,
                "sensor_tick": self.sensor_tick_s}


def radar_specs_from_config(cfg: Config) -> List[RadarSpec]:
    entries = cfg.get("radar.sensors", []) or []
    if not entries:
        raise ValueError("active sensor profile defines no radar sensors")
    out = []
    for e in entries:
        m = e.get("mount", {}) or {}
        out.append(RadarSpec(sensor_id=str(e.get("sensor_id", "front")), blueprint=str(e.get("blueprint", "sensor.other.radar")),
            horizontal_fov_deg=float(e.get("horizontal_fov_deg", 120)), vertical_fov_deg=float(e.get("vertical_fov_deg", 10)),
            range_m=float(e.get("range_m", 90)), points_per_second=int(e.get("points_per_second", 6000)),
            sensor_tick_s=float(e.get("sensor_tick_s", 0.05)), mount_x=float(m.get("x", 2.2)), mount_y=float(m.get("y", 0)),
            mount_z=float(m.get("z", 1)), mount_yaw_deg=float(m.get("yaw_deg", 0)), mount_pitch_deg=float(m.get("pitch_deg", 0))))
    return out


class RadarSensor:
    def __init__(self, scenario_world: Any, vehicle: Any, spec: RadarSpec, max_queue: int = 64) -> None:
        carla = import_carla(); self.spec = spec; self._queue = queue.Queue(maxsize=max_queue); self._dropped = 0
        transform = carla.Transform(carla.Location(x=spec.mount_x, y=spec.mount_y, z=spec.mount_z), carla.Rotation(pitch=spec.mount_pitch_deg, yaw=spec.mount_yaw_deg, roll=0))
        self.sensor = scenario_world.spawn_sensor(spec.blueprint, transform, attach_to=vehicle, attributes=spec.attributes())
        self.sensor.listen(self._on_measurement)
    def _on_measurement(self, measurement: Any) -> None:
        try: self._queue.put_nowait(measurement)
        except queue.Full: self._dropped += 1
    @property
    def dropped(self) -> int: return self._dropped
    def poll(self, frame: int, timeout_s: float = 2.0) -> Optional[Dict[str, Any]]:
        for _ in range(256):
            try: m = self._queue.get(timeout=timeout_s)
            except queue.Empty: return None
            if int(m.frame) < int(frame): continue
            return {"frame": int(m.frame), "timestamp": float(m.timestamp), "sensor_id": self.spec.sensor_id,
                    "sensor_transform": {"x": self.spec.mount_x, "y": self.spec.mount_y, "z": self.spec.mount_z,
                                          "yaw_deg": self.spec.mount_yaw_deg, "pitch_deg": self.spec.mount_pitch_deg},
                    "detections": [{"depth": float(d.depth), "azimuth": float(d.azimuth), "altitude": float(d.altitude), "radial_velocity": float(d.velocity)} for d in m]}
        return None
    def stop(self) -> None:
        try:
            if self.sensor.is_listening: self.sensor.stop()
        except RuntimeError: pass


@dataclass
class CameraSpec:
    sensor_id: str = "front"; blueprint: str = "sensor.camera.rgb"; width: int = 800; height: int = 600; fov_deg: float = 90.0
    mount_x: float = 1.4; mount_y: float = 0.0; mount_z: float = 1.4; mount_pitch_deg: float = 0.0
    def attributes(self) -> Dict[str, Any]:
        return {"image_size_x": str(self.width), "image_size_y": str(self.height), "fov": str(self.fov_deg)}


def camera_spec_from_config(cfg: Config) -> Optional[CameraSpec]:
    b = cfg.get("sensors.camera", None)
    if b is None or not bool(b.get("enabled", True)): return None
    return CameraSpec(sensor_id=str(b.get("sensor_id", "front")), blueprint=str(b.get("blueprint", "sensor.camera.rgb")),
        width=int(b.get("width", 800)), height=int(b.get("height", 600)), fov_deg=float(b.get("fov_deg", 90)),
        mount_x=float(b.get("mount_x", 1.4)), mount_y=float(b.get("mount_y", 0)), mount_z=float(b.get("mount_z", 1.4)), mount_pitch_deg=float(b.get("mount_pitch_deg", 0)))


class CameraSensor:
    def __init__(self, scenario_world: Any, vehicle: Any, spec: CameraSpec, max_queue: int = 8) -> None:
        carla = import_carla(); self.spec = spec; self._queue = queue.Queue(maxsize=max_queue); self._dropped = 0
        transform = carla.Transform(carla.Location(x=spec.mount_x, y=spec.mount_y, z=spec.mount_z), carla.Rotation(pitch=spec.mount_pitch_deg, yaw=0, roll=0))
        self.sensor = scenario_world.spawn_sensor(spec.blueprint, transform, attach_to=vehicle, attributes=spec.attributes()); self.sensor.listen(self._on_image)
    def _on_image(self, image: Any) -> None:
        try: self._queue.put_nowait(image)
        except queue.Full: self._dropped += 1
    @property
    def dropped(self) -> int: return self._dropped
    def poll(self, frame: int, timeout_s: float = 2.0) -> Optional[Dict[str, Any]]:
        for _ in range(64):
            try: image = self._queue.get(timeout=timeout_s)
            except queue.Empty: return None
            if int(image.frame) < int(frame): continue
            return {"frame": int(image.frame), "timestamp": float(image.timestamp), "width": int(image.width), "height": int(image.height), "data": bytes(image.raw_data),
                    "sensor_id": self.spec.sensor_id, "sensor_transform": {"x": self.spec.mount_x, "y": self.spec.mount_y, "z": self.spec.mount_z, "pitch_deg": self.spec.mount_pitch_deg}}
        return None
    def stop(self) -> None:
        try:
            if self.sensor.is_listening: self.sensor.stop()
        except RuntimeError: pass


class CollisionSensor:
    def __init__(self, scenario_world: Any, vehicle: Any) -> None:
        carla = import_carla(); self._events: List[Dict[str, Any]] = []; self._vehicle_cursor = 0; self._gt_cursor = 0
        self.sensor = scenario_world.spawn_sensor("sensor.other.collision", carla.Transform(), attach_to=vehicle); self.sensor.listen(self._on_event)
    def _on_event(self, event: Any) -> None:
        i = event.normal_impulse
        other = getattr(event, "other_actor", None)
        self._events.append({"timestamp": float(event.timestamp), "frame": int(event.frame), "impulse": math.sqrt(float(i.x)**2 + float(i.y)**2 + float(i.z)**2),
                             "other_actor_id": int(getattr(other, "id", -1)) if other is not None else -1,
                             "other_type_id": str(getattr(other, "type_id", "")) if other is not None else ""})
    def drain_vehicle(self) -> List[Dict[str, Any]]:
        out = [{"timestamp": e["timestamp"], "frame": e["frame"], "impulse": e["impulse"]} for e in self._events[self._vehicle_cursor:]]
        self._vehicle_cursor = len(self._events); return out
    def drain_ground_truth(self) -> List[Dict[str, Any]]:
        out = list(self._events[self._gt_cursor:]); self._gt_cursor = len(self._events); return out
    def stop(self) -> None:
        try:
            if self.sensor.is_listening: self.sensor.stop()
        except RuntimeError: pass
