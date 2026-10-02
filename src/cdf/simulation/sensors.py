"""Raw CARLA sensor adapters with frame-matched queues."""

from __future__ import annotations

import math
import queue
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, List, Optional

import numpy as np

from ..common.config import Config
from ..recording.depth_velocity import (
    DepthRadialVelocityConfig,
    depth_radial_velocity_config_from_mapping,
)
from .carla_client import import_carla


@dataclass
class RadarSpec:
    """One LOGICAL radar of a vehicle.

    CARLA's ``sensor.other.radar`` traces its rays inside a cone around its x
    axis whose lateral half-width is ``tan(horizontal_fov / 2) x range``: a
    horizontal FOV of 180 degrees or more folds back (measured on 0.9.15: 200 ->
    +-80 deg, 270 -> +-45 deg, 360 -> a vertical slice at 0 deg, 180 -> no
    return).  A wider logical sensor is therefore made of ``physical_radars``
    co-located CARLA radars at yaws ``360 k / N`` (each
    ``physical_horizontal_fov_deg`` wide, ``points_per_second / N`` rays) whose
    returns are merged into this one sensor frame (``LogicalRadar``).  The
    mount height is absolute (``mount_z``) or, with ``mount_z_above_roof_m``,
    that much above the top of the vehicle's own bounding box.
    """

    sensor_id: str = "surround"
    blueprint: str = "sensor.other.radar"
    horizontal_fov_deg: float = 360.0
    vertical_fov_deg: float = 30.0
    range_m: float = 90.0
    points_per_second: int = 21600
    sensor_tick_s: float = 0.05
    mount_x: float = 0.0
    mount_y: float = 0.0
    mount_z: float = 0.0
    mount_z_above_roof_m: Optional[float] = None
    mount_yaw_deg: float = 0.0
    mount_pitch_deg: float = 0.0
    physical_radars: int = 1
    physical_horizontal_fov_deg: Optional[float] = None

    def physical_layout(self) -> List[Dict[str, float]]:
        """Yaw (relative to the logical sensor), horizontal FOV and ray rate of each physical radar."""
        count = int(self.physical_radars)
        if count < 1:
            raise ValueError("a radar needs at least one physical sensor")
        each_fov = float(self.physical_horizontal_fov_deg or self.horizontal_fov_deg)
        if each_fov >= 180.0:
            raise ValueError("CARLA radars cannot exceed a 180 degree horizontal FOV ({0} requested); use "
                             "physical_radars with physical_horizontal_fov_deg < 180".format(each_fov))
        if count > 1 and count * each_fov < self.horizontal_fov_deg - 1e-6:
            raise ValueError("{0} physical radars of {1} deg cannot cover {2} deg".format(
                count, each_fov, self.horizontal_fov_deg))
        if count > 1 and self.horizontal_fov_deg < 360.0 - 1e-6:
            raise ValueError("several physical radars are spread over 360 degrees only")
        return [{"yaw_deg": 360.0 * k / count if count > 1 else 0.0, "horizontal_fov_deg": each_fov,
                 "points_per_second": int(round(self.points_per_second / count))} for k in range(count)]

    def mount_height(self, vehicle: Any = None) -> float:
        if self.mount_z_above_roof_m is None:
            return float(self.mount_z)
        box = vehicle.bounding_box
        return float(box.location.z + box.extent.z + self.mount_z_above_roof_m)


def radar_specs_from_config(cfg: Config) -> List[RadarSpec]:
    entries = cfg.get("radar.sensors", []) or []
    if not entries:
        raise ValueError("active sensor profile defines no radar sensors")
    out = []
    for e in entries:
        m = e.get("mount", {}) or {}
        above_roof = m.get("z_above_roof_m")
        spec = RadarSpec(sensor_id=str(e.get("sensor_id", "surround")), blueprint=str(e.get("blueprint", "sensor.other.radar")),
            horizontal_fov_deg=float(e.get("horizontal_fov_deg", 360)), vertical_fov_deg=float(e.get("vertical_fov_deg", 30)),
            range_m=float(e.get("range_m", 90)), points_per_second=int(e.get("points_per_second", 21600)),
            sensor_tick_s=float(e.get("sensor_tick_s", 0.05)), mount_x=float(m.get("x", 0.0)), mount_y=float(m.get("y", 0)),
            mount_z=float(m.get("z", 0.0)), mount_z_above_roof_m=None if above_roof is None else float(above_roof),
            mount_yaw_deg=float(m.get("yaw_deg", 0)), mount_pitch_deg=float(m.get("pitch_deg", 0)),
            physical_radars=int(e.get("physical_radars", 1)),
            physical_horizontal_fov_deg=None if e.get("physical_horizontal_fov_deg") is None
            else float(e["physical_horizontal_fov_deg"]))
        spec.physical_layout()  # validate before anything is spawned
        out.append(spec)
    return out


def rotate_detections(rows: np.ndarray, yaw_deg: float, pitch_deg: float = 0.0) -> np.ndarray:
    """Express detections of a physical radar (yaw, pitch relative to the logical sensor) in the logical frame.

    ``rows`` are [depth, azimuth, altitude, radial velocity] (CARLA: x forward,
    y right, z up; azimuth positive to the right).  Depth and the radial velocity
    lie along the line of sight and do not change; only its direction does.
    """
    if not len(rows) or (abs(yaw_deg) < 1e-12 and abs(pitch_deg) < 1e-12):
        return rows
    out = np.array(rows, dtype=np.float64, copy=True)
    az, alt = out[:, 1], out[:, 2]
    x, y, z = np.cos(alt) * np.cos(az), np.cos(alt) * np.sin(az), np.sin(alt)
    p, q = math.radians(pitch_deg), math.radians(yaw_deg)
    x, z = x * math.cos(p) - z * math.sin(p), x * math.sin(p) + z * math.cos(p)  # nose-up pitch
    x, y = x * math.cos(q) - y * math.sin(q), x * math.sin(q) + y * math.cos(q)  # yaw toward +y (right)
    out[:, 1] = np.arctan2(y, x)
    out[:, 2] = np.arcsin(np.clip(z, -1.0, 1.0))
    return out


class _PhysicalRadar:
    """One CARLA radar actor with its frame-matched queue."""

    def __init__(self, scenario_world: Any, vehicle: Any, spec: RadarSpec, layout: Dict[str, float], mount_z: float,
                 max_queue: int) -> None:
        carla = import_carla()
        self.layout = layout
        self._queue = queue.Queue(maxsize=max_queue)
        self._pending: Optional[Any] = None  # a measurement of a later frame, kept for its own poll
        self.dropped = self.received = self.delivered = 0
        transform = carla.Transform(carla.Location(x=spec.mount_x, y=spec.mount_y, z=mount_z),
                                    carla.Rotation(pitch=spec.mount_pitch_deg,
                                                   yaw=spec.mount_yaw_deg + layout["yaw_deg"], roll=0))
        attributes = {"horizontal_fov": layout["horizontal_fov_deg"], "vertical_fov": spec.vertical_fov_deg,
                      "range": spec.range_m, "points_per_second": layout["points_per_second"],
                      "sensor_tick": spec.sensor_tick_s}
        self.sensor = scenario_world.spawn_sensor(spec.blueprint, transform, attach_to=vehicle, attributes=attributes)
        self.sensor.listen(self._on_measurement)

    def _on_measurement(self, measurement: Any) -> None:
        self.received += 1
        try:
            self._queue.put_nowait(measurement)
        except queue.Full:
            self.dropped += 1

    def take(self, frame: int, timeout_s: float) -> Optional[Any]:
        """This radar's measurement of exactly ``frame`` (None if it has none)."""
        if self._pending is not None:
            if int(self._pending.frame) > int(frame):
                return None
            m, self._pending = self._pending, None
            if int(m.frame) == int(frame):
                self.delivered += 1
                return m
        for _ in range(256):
            try:
                m = self._queue.get(timeout=timeout_s)
            except queue.Empty:
                return None
            if int(m.frame) < int(frame):
                continue
            if int(m.frame) > int(frame):
                self._pending = m
                return None
            self.delivered += 1
            return m
        return None

    def stop(self) -> None:
        try:
            if self.sensor.is_listening:
                self.sensor.stop()
        except RuntimeError:
            pass


def measurement_rows(measurement: Any) -> np.ndarray:
    """CARLA radar measurement -> float array [depth, azimuth, altitude, radial velocity].

    The raw buffer holds four float32 per detection: velocity, azimuth,
    altitude, depth.  The velocity is kept native: the range rate, negative
    while the target approaches.
    """
    raw = np.frombuffer(measurement.raw_data, dtype=np.float32).reshape(-1, 4)
    return raw[:, [3, 1, 2, 0]].astype(np.float64)


class RadarSensor:
    """One logical radar: its physical CARLA radars merged into one sensor frame per tick."""

    def __init__(self, scenario_world: Any, vehicle: Any, spec: RadarSpec, max_queue: int = 64) -> None:
        self.spec = spec
        self.mount_z = spec.mount_height(vehicle)
        self.layout = spec.physical_layout()
        self.physical = [_PhysicalRadar(scenario_world, vehicle, spec, layout, self.mount_z, max_queue)
                         for layout in self.layout]
        self._delivered = self._incomplete = self._beyond_range = 0

    @property
    def dropped(self) -> int:
        return sum(radar.dropped for radar in self.physical)

    def metadata(self) -> Dict[str, Any]:
        """What the vehicle logger records about this sensor (logical frame, physical make-up)."""
        out = dict(self.spec.__dict__)
        out.update(mount_z=round(self.mount_z, 4), physical_layout=[dict(item) for item in self.layout])
        return out

    def poll(self, frame: int, timeout_s: float = 2.0) -> Optional[Dict[str, Any]]:
        parts, timestamp = [], None
        for radar in self.physical:
            m = radar.take(frame, timeout_s)
            if m is None:
                continue
            timestamp = float(m.timestamp) if timestamp is None else timestamp
            rows = rotate_detections(measurement_rows(m), radar.layout["yaw_deg"])
            parts.append((int(m.frame), rows))
        if not parts:
            return None
        if len(parts) < len(self.physical):
            self._incomplete += 1
        rows = np.concatenate([r for _, r in parts]) if parts else np.empty((0, 4))
        # Off its axis a CARLA radar reaches beyond its range (the range bounds the
        # forward component only): the logical sensor keeps a radial range.
        keep = rows[:, 0] <= self.spec.range_m
        self._beyond_range += int((~keep).sum())
        self._delivered += 1
        return {"frame": parts[0][0], "timestamp": timestamp, "sensor_id": self.spec.sensor_id, "source": "radar",
                "sensor_transform": {"x": self.spec.mount_x, "y": self.spec.mount_y, "z": round(self.mount_z, 4),
                                     "yaw_deg": self.spec.mount_yaw_deg, "pitch_deg": self.spec.mount_pitch_deg},
                "detections": rows[keep].astype(np.float32)}

    @property
    def stats(self) -> Dict[str, Any]:
        return {"callbacks_received": sum(r.received for r in self.physical),
                "queue_drops": self.dropped,
                "frames_delivered": self._delivered,
                "incomplete_frames": self._incomplete,
                "returns_beyond_range_dropped": self._beyond_range,
                "physical": [{"yaw_deg": r.layout["yaw_deg"], "callbacks_received": r.received,
                              "queue_drops": r.dropped, "frames_delivered": r.delivered} for r in self.physical]}

    def stop(self) -> None:
        for radar in self.physical:
            radar.stop()


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
    suppress_ground: bool = True
    min_relative_height_m: float = -0.9

    @property
    def max_bins(self) -> int:
        # After sparsification there is at most one return per azimuth bin.
        return int(math.ceil(self.horizontal_fov_deg / self.azimuth_bin_deg))


def depth_observation_spec_from_config(cfg: Config) -> DepthObservationSpec:
    d = cfg.get("depth_observations", {}) or {}
    return DepthObservationSpec(
        max_range_m=float(d.get("max_range_m", 90.0)),
        horizontal_fov_deg=float(d.get("horizontal_fov_deg", 90.0)),
        vertical_fov_deg=float(d.get("vertical_fov_deg", 10.0)),
        azimuth_bin_deg=float(d.get("azimuth_bin_deg", 2.0)),
        altitude_bin_deg=float(d.get("altitude_bin_deg", 2.0)),
        suppress_ground=bool(d.get("suppress_ground", True)),
        min_relative_height_m=float(d.get("min_relative_height_m", -0.9)),
    )


def depth_radial_velocity_config_from_config(cfg: Config) -> DepthRadialVelocityConfig:
    """Load the optional temporal depth velocity estimator configuration."""
    return depth_radial_velocity_config_from_mapping(cfg.get("depth_radial_velocity", {}) or {})


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


def sparsify_depth_observations(detections: List[Dict[str, Any]],
                                spec: DepthObservationSpec) -> List[Dict[str, Any]]:
    """Keep one nearest non-ground return per horizontal azimuth bin.

    The input is deliberately the existing 2-degree-by-2-degree extraction;
    this second stage removes vertical duplicates without introducing semantic
    object assumptions.  Ground rejection uses only camera-local geometry.
    """
    n_az = int(math.ceil(spec.horizontal_fov_deg / spec.azimuth_bin_deg))
    half_h = math.radians(spec.horizontal_fov_deg / 2.0)
    selected: Dict[int, Dict[str, Any]] = {}
    for detection in detections:
        depth = float(detection.get("depth", float("nan")))
        azimuth = float(detection.get("azimuth", float("nan")))
        altitude = float(detection.get("altitude", float("nan")))
        if not (math.isfinite(depth) and math.isfinite(azimuth) and math.isfinite(altitude)):
            continue
        if depth <= 0.0 or depth > spec.max_range_m:
            continue
        z_relative = depth * math.sin(altitude)
        if spec.suppress_ground and z_relative < spec.min_relative_height_m:
            continue
        bin_index = int(math.floor((azimuth + half_h) / math.radians(spec.azimuth_bin_deg)))
        bin_index = max(0, min(n_az - 1, bin_index))
        previous = selected.get(bin_index)
        # Stable tie-breaks make the output reproducible for equal surfaces.
        key = (depth, abs(altitude), altitude)
        if previous is None or key < previous["_selection_key"]:
            kept = dict(detection)
            kept.pop("_selection_key", None)
            kept["_selection_key"] = key
            selected[bin_index] = kept
    out = []
    for index in sorted(selected):
        item = dict(selected[index])
        item.pop("_selection_key", None)
        out.append(item)
    return out


def depth_observations_from_depth(depth_m: np.ndarray, spec: DepthObservationSpec,
                                  horizontal_fov_deg: float) -> List[Dict[str, Any]]:
    """Create sparse nearest-surface detections from the existing 2-D extraction."""
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
    return sparsify_depth_observations(detections, spec)


def depth_observations_from_bgra(raw_data: bytes, width: int, height: int,
                                 camera_fov_deg: float, spec: DepthObservationSpec) -> List[Dict[str, Any]]:
    return depth_observations_from_depth(
        decode_carla_depth(raw_data, width, height), spec, camera_fov_deg
    )


class CameraSensor:
    def __init__(self, scenario_world: Any, vehicle: Any, spec: CameraSpec, max_queue: int = 64,
                 report_frame_gaps: bool = False) -> None:
        carla = import_carla(); self.spec = spec; self._queue = queue.Queue(maxsize=max_queue); self._dropped = 0; self._received = 0; self._duplicates = 0; self._pre_timeline = 0
        self._minimum_frame: Optional[int] = None
        self._report_frame_gaps = bool(report_frame_gaps)
        self._seen_frames = set()
        transform = carla.Transform(carla.Location(x=spec.mount_x, y=spec.mount_y, z=spec.mount_z), carla.Rotation(pitch=spec.mount_pitch_deg, yaw=spec.mount_yaw_deg, roll=spec.mount_roll_deg))
        self.sensor = scenario_world.spawn_sensor(spec.blueprint, transform, attach_to=vehicle, attributes=spec.attributes()); self.sensor.listen(self._on_image)
    def _on_image(self, image: Any) -> None:
        self._received += 1
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
                    self._pre_timeline += 1
                    continue
                if int(image.frame) in self._seen_frames:
                    self._duplicates += 1
                    continue
                self._seen_frames.add(int(image.frame))
                out.append(self._record(image))
            except queue.Empty:
                return out
    @property
    def stats(self) -> Dict[str, Any]:
        frames = sorted(self._seen_frames)
        gaps = sum(max(0, later - earlier - 1) for earlier, later in zip(frames, frames[1:]))
        stats = {
            "callbacks_received": self._received,
            "queue_drops": self._dropped,
            "duplicate_callbacks": self._duplicates,
            "pre_timeline_callbacks": self._pre_timeline,
            "frames_written": len(frames),
            "first_frame": frames[0] if frames else None,
            "last_frame": frames[-1] if frames else None,
        }
        if self._report_frame_gaps:
            stats["missing_frame_count"] = int(gaps)
        return stats
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
