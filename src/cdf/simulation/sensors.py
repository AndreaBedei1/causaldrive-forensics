"""Raw CARLA sensor adapters with frame-matched queues."""

from __future__ import annotations

import math
import queue
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Optional

import numpy as np

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
                    "source": "radar",
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
    sensor_tick_s: float = 0.0; mount_x: float = 1.4; mount_y: float = 0.0; mount_z: float = 1.4; mount_pitch_deg: float = 0.0; mount_yaw_deg: float = 0.0; mount_roll_deg: float = 0.0
    def attributes(self) -> Dict[str, Any]:
        attrs = {"image_size_x": str(self.width), "image_size_y": str(self.height), "fov": str(self.fov_deg)}
        if self.sensor_tick_s > 0.0:
            attrs["sensor_tick"] = str(self.sensor_tick_s)
        return attrs


def camera_spec_from_config(cfg: Config) -> Optional[CameraSpec]:
    b = cfg.get("sensors.camera", None)
    if b is None or not bool(b.get("enabled", True)): return None
    return CameraSpec(sensor_id=str(b.get("sensor_id", "front")), blueprint=str(b.get("blueprint", "sensor.camera.rgb")),
        width=int(b.get("width", 800)), height=int(b.get("height", 600)), fov_deg=float(b.get("fov_deg", 90)),
        sensor_tick_s=float(b.get("sensor_tick_s", 0.0)),
        mount_x=float(b.get("mount_x", 1.4)), mount_y=float(b.get("mount_y", 0)), mount_z=float(b.get("mount_z", 1.4)), mount_pitch_deg=float(b.get("mount_pitch_deg", 0)),
        mount_yaw_deg=float(b.get("mount_yaw_deg", 0)), mount_roll_deg=float(b.get("mount_roll_deg", 0)))


def depth_camera_spec_from_config(cfg: Config) -> Optional[CameraSpec]:
    """Load the raw depth-camera installation, if enabled."""
    b = cfg.get("sensors.depth_camera", None)
    if b is None or not bool(b.get("enabled", True)): return None
    return CameraSpec(sensor_id=str(b.get("sensor_id", "front_depth")), blueprint=str(b.get("blueprint", "sensor.camera.depth")),
        width=int(b.get("width", 800)), height=int(b.get("height", 600)), fov_deg=float(b.get("fov_deg", 90)),
        sensor_tick_s=float(b.get("sensor_tick_s", 0.0)),
        mount_x=float(b.get("mount_x", 1.4)), mount_y=float(b.get("mount_y", 0)), mount_z=float(b.get("mount_z", 1.4)), mount_pitch_deg=float(b.get("mount_pitch_deg", 0)),
        mount_yaw_deg=float(b.get("mount_yaw_deg", 0)), mount_roll_deg=float(b.get("mount_roll_deg", 0)))


@dataclass
class DepthObservationSpec:
    max_range_m: float = 90.0
    horizontal_fov_deg: float = 90.0
    vertical_fov_deg: float = 10.0
    azimuth_bin_deg: float = 2.0
    altitude_bin_deg: float = 2.0

    @property
    def max_bins(self) -> int:
        horizontal = int(math.ceil(self.horizontal_fov_deg / self.azimuth_bin_deg))
        vertical = int(math.ceil(self.vertical_fov_deg / self.altitude_bin_deg))
        return horizontal * vertical


def depth_observation_spec_from_config(cfg: Config) -> DepthObservationSpec:
    d = cfg.get("depth_observations", {}) or {}
    return DepthObservationSpec(
        max_range_m=float(d.get("max_range_m", 90.0)),
        horizontal_fov_deg=float(d.get("horizontal_fov_deg", 90.0)),
        vertical_fov_deg=float(d.get("vertical_fov_deg", 10.0)),
        azimuth_bin_deg=float(d.get("azimuth_bin_deg", 2.0)),
        altitude_bin_deg=float(d.get("altitude_bin_deg", 2.0)),
    )


def decode_carla_depth(raw_data: bytes, width: int, height: int) -> np.ndarray:
    """Decode CARLA's BGRA 24-bit depth image to metres."""
    array = np.frombuffer(raw_data, dtype=np.uint8).reshape((int(height), int(width), 4))
    blue = array[..., 0].astype(np.float32)
    green = array[..., 1].astype(np.float32)
    red = array[..., 2].astype(np.float32)
    encoded = red + 256.0 * green + 65536.0 * blue
    return 1000.0 * encoded / float(256 ** 3 - 1)


def camera_intrinsics(width: int, height: int, horizontal_fov_deg: float) -> tuple:
    """Return pinhole ``fx, fy, cx, cy`` for CARLA's horizontal FOV."""
    fx = float(width) / (2.0 * math.tan(math.radians(float(horizontal_fov_deg)) / 2.0))
    return fx, fx, float(width) / 2.0, float(height) / 2.0


def unproject_pixel(u: float, v: float, depth_m: float, width: int, height: int,
                    horizontal_fov_deg: float) -> tuple:
    """Unproject a CARLA depth ray (x forward, y right, z up).

    CARLA's raw depth converter yields camera-to-surface ray distance. The
    normalized pinhole ray is therefore scaled so its Euclidean length remains
    ``depth_m``.
    """
    fx, fy, cx, cy = camera_intrinsics(width, height, horizontal_fov_deg)
    nx = (float(u) - cx) / fx
    ny = (cy - float(v)) / fy
    scale = float(depth_m) / math.sqrt(1.0 + nx * nx + ny * ny)
    x = scale
    y = nx * scale
    z = ny * scale
    return x, y, z


@lru_cache(maxsize=8)
def _camera_geometry(width: int, height: int, horizontal_fov_deg: float,
                     observation_horizontal_fov_deg: float,
                     observation_vertical_fov_deg: float,
                     azimuth_bin_deg: float, altitude_bin_deg: float) -> tuple:
    """Cache static per-pixel angles and bin membership for repeated frames."""
    fx, fy, cx, cy = camera_intrinsics(width, height, horizontal_fov_deg)
    u, v = np.meshgrid(np.arange(width, dtype=np.float32), np.arange(height, dtype=np.float32))
    nx = (u - cx) / fx
    ny = (cy - v) / fy
    azimuth = np.arctan2(nx, np.ones_like(nx))
    altitude = np.arctan2(ny, np.sqrt(1.0 + nx * nx))
    half_h = math.radians(float(observation_horizontal_fov_deg) / 2.0)
    half_v = math.radians(float(observation_vertical_fov_deg) / 2.0)
    angular_valid = (np.abs(azimuth) <= half_h) & (np.abs(altitude) <= half_v)
    n_az = int(math.ceil(float(observation_horizontal_fov_deg) / float(azimuth_bin_deg)))
    n_al = int(math.ceil(float(observation_vertical_fov_deg) / float(altitude_bin_deg)))
    az_bins = np.clip(
        np.floor((azimuth + half_h) / math.radians(float(azimuth_bin_deg))).astype(np.int32),
        0, n_az - 1,
    )
    al_bins = np.clip(
        np.floor((altitude + half_v) / math.radians(float(altitude_bin_deg))).astype(np.int32),
        0, n_al - 1,
    )
    bin_ids = al_bins * n_az + az_bins
    flat_valid = angular_valid.ravel()
    flat_bins = bin_ids.ravel()
    groups = tuple(np.flatnonzero(flat_valid & (flat_bins == i)) for i in range(n_az * n_al))
    return azimuth.ravel(), altitude.ravel(), groups


def depth_observations_from_depth(depth_m: np.ndarray, spec: DepthObservationSpec,
                                  horizontal_fov_deg: float) -> List[Dict[str, Any]]:
    """Create one nearest-surface detection per deterministic angular bin."""
    if depth_m.ndim != 2:
        raise ValueError("depth array must be two-dimensional")
    height, width = depth_m.shape
    azimuth, altitude, groups = _camera_geometry(
        int(width), int(height), float(horizontal_fov_deg),
        float(spec.horizontal_fov_deg), float(spec.vertical_fov_deg),
        float(spec.azimuth_bin_deg), float(spec.altitude_bin_deg),
    )
    half_h = math.radians(spec.horizontal_fov_deg / 2.0)
    half_v = math.radians(spec.vertical_fov_deg / 2.0)
    detections: List[Dict[str, Any]] = []
    flat_depth = depth_m.ravel()
    for pixel_indices in groups:
        if not len(pixel_indices):
            continue
        values = flat_depth[pixel_indices]
        valid = np.isfinite(values) & (values > 0.0) & (values <= spec.max_range_m)
        if not np.any(valid):
            continue
        indices = pixel_indices[valid]
        values = values[valid]
        nearest_count = max(1, int(math.ceil(len(values) * 0.1)))
        nearest = np.partition(values, nearest_count - 1)[:nearest_count]
        representative = float(np.median(nearest))
        selected = indices[int(np.argmin(np.abs(values - representative)))]
        # Convert before clipping so float32 input cannot round a boundary
        # just outside the configured field of view.
        azimuth_value = min(max(float(azimuth[selected]), -half_h), half_h)
        altitude_value = min(max(float(altitude[selected]), -half_v), half_v)
        detections.append({
            "depth": float(flat_depth[selected]),
            "azimuth": azimuth_value,
            "altitude": altitude_value,
            # Reserved for depth-derived temporal radial velocity estimation.
            # It is deliberately not computed in this acquisition step.
            "radial_velocity": None,
        })
    return detections


def depth_observations_from_bgra(raw_data: bytes, width: int, height: int,
                                 camera_fov_deg: float, spec: DepthObservationSpec) -> List[Dict[str, Any]]:
    return depth_observations_from_depth(
        decode_carla_depth(raw_data, width, height), spec, camera_fov_deg
    )


class CameraSensor:
    def __init__(self, scenario_world: Any, vehicle: Any, spec: CameraSpec, max_queue: int = 64) -> None:
        carla = import_carla(); self.spec = spec; self._queue = queue.Queue(maxsize=max_queue); self._dropped = 0
        self._minimum_frame: Optional[int] = None
        self._seen_frames = set()
        transform = carla.Transform(carla.Location(x=spec.mount_x, y=spec.mount_y, z=spec.mount_z), carla.Rotation(pitch=spec.mount_pitch_deg, yaw=spec.mount_yaw_deg, roll=spec.mount_roll_deg))
        self.sensor = scenario_world.spawn_sensor(spec.blueprint, transform, attach_to=vehicle, attributes=spec.attributes()); self.sensor.listen(self._on_image)
    def _on_image(self, image: Any) -> None:
        try: self._queue.put_nowait(image)
        except queue.Full: self._dropped += 1
    @property
    def dropped(self) -> int: return self._dropped

    def set_minimum_frame(self, frame: int) -> None:
        """Ignore callback images produced before the recorded timeline."""
        self._minimum_frame = int(frame)
    def _record(self, image: Any) -> Dict[str, Any]:
        return {"frame": int(image.frame), "timestamp": float(image.timestamp), "width": int(image.width), "height": int(image.height), "data": bytes(image.raw_data),
                "sensor_id": self.spec.sensor_id, "sensor_blueprint": self.spec.blueprint, "fov_deg": self.spec.fov_deg, "sensor_tick_s": self.spec.sensor_tick_s,
                "sensor_transform": {"x": self.spec.mount_x, "y": self.spec.mount_y, "z": self.spec.mount_z,
                "pitch_deg": self.spec.mount_pitch_deg, "yaw_deg": self.spec.mount_yaw_deg, "roll_deg": self.spec.mount_roll_deg}}

    def drain_available(self) -> List[Dict[str, Any]]:
        """Return all currently queued images without waiting for a future frame."""
        out = []
        while True:
            try:
                image = self._queue.get_nowait()
                if self._minimum_frame is not None and int(image.frame) < self._minimum_frame:
                    continue
                if int(image.frame) in self._seen_frames:
                    continue
                self._seen_frames.add(int(image.frame))
                out.append(self._record(image))
            except queue.Empty:
                return out
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
