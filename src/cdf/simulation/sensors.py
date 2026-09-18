"""Sensor attachment and synchronous measurement retrieval.

CARLA delivers sensor data through callbacks on a separate thread, which does not
by itself line up with synchronous ticking. Each sensor here therefore pushes its
measurements into a thread-safe queue, and the run loop pulls the measurement
*belonging to the tick it just executed* by matching frame numbers. Stale frames
are discarded rather than silently attributed to the wrong tick.

Boundary note
-------------
A CARLA collision event exposes ``other_actor``, which is privileged information
an onboard unit could not possibly have. :meth:`CollisionSensor.drain_local`
strips it and returns a :class:`LocalTriggerRecord` carrying only what a real
vehicle would know -- that an impact happened, when, and how hard. The identity
of the other party is available exclusively through
:meth:`CollisionSensor.drain_privileged`, which only the oracle logger calls.
"""

from __future__ import annotations

import logging
import math
import queue
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from ..common.config import Config
from ..common.schemas import (
    LocalTriggerRecord,
    RadarDetection,
    RadarFrame,
    TriggerKind,
)
from .carla_client import import_carla

LOGGER = logging.getLogger(__name__)

__all__ = [
    "RadarSpec",
    "radar_specs_from_config",
    "RadarSensor",
    "CollisionSensor",
    "CameraSpec",
    "camera_spec_from_config",
    "CameraSensor",
    "LaneInvasionSensor",
]


# ---------------------------------------------------------------------------
# Radar
# ---------------------------------------------------------------------------


@dataclass
class RadarSpec:
    """Declarative description of one radar installation."""

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
        """Blueprint attributes for this specification."""
        return {
            "horizontal_fov": self.horizontal_fov_deg,
            "vertical_fov": self.vertical_fov_deg,
            "range": self.range_m,
            "points_per_second": int(self.points_per_second),
            "sensor_tick": self.sensor_tick_s,
        }


def radar_specs_from_config(cfg: Config) -> List[RadarSpec]:
    """Build radar specifications from the active ``radar`` profile."""
    entries = cfg.get("radar.sensors", []) or []
    if not entries:
        raise ValueError(
            "the active sensor profile defines no radar sensors "
            "(expected radar.sensors in configs/sensors/*.yaml)"
        )
    specs: List[RadarSpec] = []
    for entry in entries:
        mount = entry.get("mount", {}) or {}
        specs.append(
            RadarSpec(
                sensor_id=entry.get("sensor_id", "front"),
                blueprint=entry.get("blueprint", "sensor.other.radar"),
                horizontal_fov_deg=float(entry.get("horizontal_fov_deg", 120.0)),
                vertical_fov_deg=float(entry.get("vertical_fov_deg", 10.0)),
                range_m=float(entry.get("range_m", 90.0)),
                points_per_second=int(entry.get("points_per_second", 6000)),
                sensor_tick_s=float(entry.get("sensor_tick_s", 0.05)),
                mount_x=float(mount.get("x", 2.2)),
                mount_y=float(mount.get("y", 0.0)),
                mount_z=float(mount.get("z", 1.0)),
                mount_yaw_deg=float(mount.get("yaw_deg", 0.0)),
                mount_pitch_deg=float(mount.get("pitch_deg", 0.0)),
            )
        )
    return specs


class RadarSensor:
    """A radar attached to one participant, delivering frame-matched measurements."""

    def __init__(
        self,
        scenario_world: Any,
        vehicle: Any,
        spec: RadarSpec,
        participant_id: str,
        max_queue: int = 64,
    ) -> None:
        carla = import_carla()
        self.spec = spec
        self.participant_id = participant_id
        self._queue: "queue.Queue[Any]" = queue.Queue(maxsize=max_queue)
        self._dropped = 0

        transform = carla.Transform(
            carla.Location(x=spec.mount_x, y=spec.mount_y, z=spec.mount_z),
            carla.Rotation(pitch=spec.mount_pitch_deg, yaw=spec.mount_yaw_deg, roll=0.0),
        )
        self.sensor = scenario_world.spawn_sensor(
            spec.blueprint, transform, attach_to=vehicle, attributes=spec.attributes()
        )
        self.sensor.listen(self._on_measurement)

    def _on_measurement(self, measurement: Any) -> None:
        """Sensor-thread callback: enqueue without ever blocking the simulator."""
        try:
            self._queue.put_nowait(measurement)
        except queue.Full:
            self._dropped += 1

    @property
    def dropped(self) -> int:
        """Measurements discarded because the queue was full (should stay 0)."""
        return self._dropped

    def poll(self, frame: int, timeout_s: float = 2.0) -> Optional[RadarFrame]:
        """Return the measurement produced for ``frame``, or ``None``.

        Measurements older than ``frame`` are dropped: attributing a stale radar
        return to the current tick would corrupt the range-rate history that TTC
        and tracking depend on.
        """
        deadline_iterations = 0
        while True:
            try:
                measurement = self._queue.get(timeout=float(timeout_s))
            except queue.Empty:
                return None
            if int(measurement.frame) < int(frame):
                deadline_iterations += 1
                if deadline_iterations > 256:
                    LOGGER.warning(
                        "radar %s: discarded %d stale frames while waiting for %d",
                        self.spec.sensor_id,
                        deadline_iterations,
                        frame,
                    )
                    return None
                continue
            return self._to_record(measurement)

    def _to_record(self, measurement: Any) -> RadarFrame:
        """Convert a CARLA radar measurement into our schema record."""
        detections = [
            RadarDetection(
                depth=float(d.depth),
                azimuth=float(d.azimuth),
                altitude=float(d.altitude),
                velocity=float(d.velocity),
            )
            for d in measurement
        ]
        return RadarFrame(
            t=float(measurement.timestamp),
            frame=int(measurement.frame),
            participant_id=self.participant_id,
            sensor_id=self.spec.sensor_id,
            detections=detections,
            sensor_yaw=self.spec.mount_yaw_deg,
            sensor_x=self.spec.mount_x,
            sensor_y=self.spec.mount_y,
            sensor_z=self.spec.mount_z,
        )

    def stop(self) -> None:
        """Stop listening (cleanup is still owned by :class:`ScenarioWorld`)."""
        try:
            if self.sensor.is_listening:
                self.sensor.stop()
        except RuntimeError as exc:
            LOGGER.warning("could not stop radar %s: %s", self.spec.sensor_id, exc)


# ---------------------------------------------------------------------------
# Collision
# ---------------------------------------------------------------------------


@dataclass
class _RawCollision:
    """A collision event as CARLA reported it, including privileged fields.

    Instances never leave this module except through the two explicit drain
    methods, which decide what each layer is allowed to see.
    """

    t: float
    frame: int
    impulse: float
    other_actor_id: int
    other_type_id: str


class CollisionSensor:
    """Onboard collision sensor with a strict local/privileged split."""

    def __init__(self, scenario_world: Any, vehicle: Any, participant_id: str) -> None:
        carla = import_carla()
        self.participant_id = participant_id
        self._events: List[_RawCollision] = []
        self._local_cursor = 0
        self._privileged_cursor = 0

        self.sensor = scenario_world.spawn_sensor(
            "sensor.other.collision", carla.Transform(), attach_to=vehicle
        )
        self.sensor.listen(self._on_event)

    def _on_event(self, event: Any) -> None:
        impulse = event.normal_impulse
        magnitude = math.sqrt(
            float(impulse.x) ** 2 + float(impulse.y) ** 2 + float(impulse.z) ** 2
        )
        other = getattr(event, "other_actor", None)
        self._events.append(
            _RawCollision(
                t=float(event.timestamp),
                frame=int(event.frame),
                impulse=magnitude,
                other_actor_id=int(getattr(other, "id", -1)) if other is not None else -1,
                other_type_id=str(getattr(other, "type_id", "")) if other is not None else "",
            )
        )

    @property
    def any_collision(self) -> bool:
        return bool(self._events)

    def drain_local(self, min_impulse: float = 0.0) -> List[LocalTriggerRecord]:
        """New collisions as ONBOARD-observable trigger records.

        The privileged ``other_actor`` identity is deliberately dropped here: a
        real vehicle's collision sensor reports that an impact occurred and how
        hard, not who it was.
        """
        out: List[LocalTriggerRecord] = []
        while self._local_cursor < len(self._events):
            raw = self._events[self._local_cursor]
            self._local_cursor += 1
            if raw.impulse < float(min_impulse):
                continue
            out.append(
                LocalTriggerRecord(
                    t=raw.t,
                    frame=raw.frame,
                    participant_id=self.participant_id,
                    kind=TriggerKind.COLLISION,
                    collision_detected=True,
                    impulse=raw.impulse,
                    detail={"source": "onboard_collision_sensor"},
                )
            )
        return out

    def drain_privileged(self) -> List[Dict[str, Any]]:
        """New collisions INCLUDING the other party's identity.

        PRIVILEGED. Only :mod:`cdf.oracle` may call this; the result is ground
        truth used for evaluation and must never reach local or fused inference.
        """
        out: List[Dict[str, Any]] = []
        while self._privileged_cursor < len(self._events):
            raw = self._events[self._privileged_cursor]
            self._privileged_cursor += 1
            out.append(
                {
                    "t": raw.t,
                    "frame": raw.frame,
                    "participant_id": self.participant_id,
                    "impulse": raw.impulse,
                    "other_actor_id": raw.other_actor_id,
                    "other_type_id": raw.other_type_id,
                }
            )
        return out

    def stop(self) -> None:
        try:
            if self.sensor.is_listening:
                self.sensor.stop()
        except RuntimeError as exc:
            LOGGER.warning("could not stop collision sensor: %s", exc)


# ---------------------------------------------------------------------------
# Front camera
# ---------------------------------------------------------------------------


@dataclass
class CameraSpec:
    """Declarative description of the forward-facing RGB camera.

    Modest by default. The camera exists so that signs and road markings are
    *perceived* rather than looked up, and a 1080p feed would cost a great deal of
    encoding time to answer the same question no better. The resolution is
    reported with the perception metrics, because a detector's precision means
    little without knowing the image it worked from.
    """

    sensor_id: str = "front"
    blueprint: str = "sensor.camera.rgb"
    width: int = 800
    height: int = 600
    fov_deg: float = 90.0
    mount_x: float = 1.4
    mount_y: float = 0.0
    mount_z: float = 1.4
    mount_pitch_deg: float = 0.0
    jpeg_quality: int = 70

    def attributes(self) -> Dict[str, Any]:
        return {
            "image_size_x": str(int(self.width)),
            "image_size_y": str(int(self.height)),
            "fov": str(float(self.fov_deg)),
        }


def camera_spec_from_config(cfg: Config) -> Optional[CameraSpec]:
    """The configured camera, or ``None`` when the camera is switched off.

    Off is a supported configuration rather than a degraded one: the V1 scenarios
    were recorded without a camera and have to stay runnable without one, so
    every consumer of camera artifacts must cope with their absence anyway.
    """
    block = cfg.get("sensors.camera", None)
    if block is None or not bool(block.get("enabled", True)):
        return None
    return CameraSpec(
        sensor_id=str(block.get("sensor_id", "front")),
        blueprint=str(block.get("blueprint", "sensor.camera.rgb")),
        width=int(block.get("width", 800)),
        height=int(block.get("height", 600)),
        fov_deg=float(block.get("fov_deg", 90.0)),
        mount_x=float(block.get("mount_x", 1.4)),
        mount_y=float(block.get("mount_y", 0.0)),
        mount_z=float(block.get("mount_z", 1.4)),
        mount_pitch_deg=float(block.get("mount_pitch_deg", 0.0)),
        jpeg_quality=int(block.get("jpeg_quality", 70)),
    )


class CameraSensor:
    """A forward camera whose frames are compressed on arrival, not stored raw.

    A 25 s window of 800x600 RGB at 20 Hz is about 700 MB per vehicle, which is
    why nothing here holds a raw frame longer than it takes to encode it. JPEG at
    the configured quality brings that under 20 MB, and the compression runs on
    the sensor thread where it costs the simulator nothing.

    The frame is also handed to the caller as an array, once, for perception, so
    the detector sees full fidelity and only the stored copy is lossy.
    """

    def __init__(
        self,
        scenario_world: Any,
        vehicle: Any,
        spec: CameraSpec,
        participant_id: str,
        max_queue: int = 8,
    ) -> None:
        carla = import_carla()
        self.spec = spec
        self.participant_id = participant_id
        self._queue: "queue.Queue[Any]" = queue.Queue(maxsize=max_queue)
        self._dropped = 0

        transform = carla.Transform(
            carla.Location(x=spec.mount_x, y=spec.mount_y, z=spec.mount_z),
            carla.Rotation(pitch=spec.mount_pitch_deg, yaw=0.0, roll=0.0),
        )
        self.sensor = scenario_world.spawn_sensor(
            spec.blueprint, transform, attach_to=vehicle,
            attributes=spec.attributes(),
        )
        self.sensor.listen(self._on_image)

    def _on_image(self, image: Any) -> None:
        try:
            self._queue.put_nowait(image)
        except queue.Full:
            # Dropping a frame beats blocking the sensor thread, which would
            # stall the tick and change the physics being recorded.
            self._dropped += 1

    @property
    def dropped(self) -> int:
        return self._dropped

    def poll(self, frame: int, timeout_s: float = 2.0) -> Optional[Dict[str, Any]]:
        """The image produced for ``frame``, as ``{t, frame, array, jpeg}``.

        Stale images are discarded rather than attributed to the wrong tick, for
        the same reason radar frames are: a sign seen one tick late would be
        timestamped against the wrong vehicle state.
        """
        discarded = 0
        while True:
            try:
                image = self._queue.get(timeout=float(timeout_s))
            except queue.Empty:
                return None
            if int(image.frame) < int(frame):
                discarded += 1
                if discarded > 64:
                    LOGGER.warning(
                        "camera %s: discarded %d stale frames waiting for %d",
                        self.spec.sensor_id, discarded, frame,
                    )
                    return None
                continue
            return self._to_record(image)

    def _to_record(self, image: Any) -> Dict[str, Any]:
        import numpy as np

        raw = np.frombuffer(image.raw_data, dtype=np.uint8)
        bgra = raw.reshape((int(image.height), int(image.width), 4))
        bgr = np.ascontiguousarray(bgra[:, :, :3])
        rgb = np.ascontiguousarray(bgr[:, :, ::-1])
        return {
            "t": float(image.timestamp),
            "frame": int(image.frame),
            "width": int(image.width),
            "height": int(image.height),
            "array": rgb,
            "jpeg": self._encode(bgr),
        }

    def _encode(self, bgr: Any) -> bytes:
        """JPEG bytes, or the raw buffer when no encoder is available.

        Falling back rather than failing: a run whose frames could not be
        compressed is a larger artifact, not a lost one.
        """
        try:
            import cv2

            ok, buffer = cv2.imencode(
                ".jpg", bgr,
                [int(cv2.IMWRITE_JPEG_QUALITY), int(self.spec.jpeg_quality)],
            )
            if ok:
                return bytes(buffer.tobytes())
        except ImportError:
            LOGGER.warning(
                "no image encoder available; camera frames will be stored raw"
            )
        return bytes(bgr.tobytes())

    def stop(self) -> None:
        try:
            if self.sensor.is_listening:
                self.sensor.stop()
        except RuntimeError as exc:
            LOGGER.warning("could not stop camera %s: %s", self.spec.sensor_id, exc)


# ---------------------------------------------------------------------------
# Lane invasion
# ---------------------------------------------------------------------------


class LaneInvasionSensor:
    """Reports when the vehicle crosses a road marking.

    Treated as a simulated onboard ADAS signal, which is what the brief permits
    and what a production lane-departure warning is. It reports *that* a marking
    was crossed and what sort; it does not report which lane the vehicle is in,
    where that lane goes, or what else is on it. Those would be map knowledge.

    Unlike radar and the camera this sensor is event-driven rather than per-tick,
    so there is nothing to frame-match: reports are drained when asked for.
    """

    def __init__(
        self,
        scenario_world: Any,
        vehicle: Any,
        participant_id: str,
    ) -> None:
        carla = import_carla()
        self.participant_id = participant_id
        self._records: List[Dict[str, Any]] = []
        self.sensor = scenario_world.spawn_sensor(
            "sensor.other.lane_invasion", carla.Transform(), attach_to=vehicle
        )
        self.sensor.listen(self._on_event)

    def _on_event(self, event: Any) -> None:
        try:
            types = [
                str(getattr(marking, "type", "")) for marking in
                (getattr(event, "crossed_lane_markings", None) or [])
            ]
        except (AttributeError, TypeError):  # pragma: no cover - defensive
            types = []
        self._records.append({
            "t": float(getattr(event, "timestamp", 0.0)),
            "frame": int(getattr(event, "frame", 0)),
            "participant_id": self.participant_id,
            "marking_types": types,
        })

    def drain(self) -> List[Dict[str, Any]]:
        """Every report so far, oldest first, clearing the buffer."""
        out = sorted(self._records, key=lambda r: r["t"])
        self._records = []
        return out

    def stop(self) -> None:
        try:
            if self.sensor.is_listening:
                self.sensor.stop()
        except RuntimeError as exc:
            LOGGER.warning("could not stop lane sensor: %s", exc)
