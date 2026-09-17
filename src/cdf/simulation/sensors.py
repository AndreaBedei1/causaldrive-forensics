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
