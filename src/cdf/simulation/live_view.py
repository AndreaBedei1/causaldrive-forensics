"""External-only spectator view for a running CARLA scenario.

This module is deliberately outside every forensic stage.  It reads only the
privileged actor transforms needed to position CARLA's native spectator and to
draw short-lived operator labels.  It does not return measurements, write
artifacts, or participate in the scenario controllers, sensors, oracle, or
analysis pipeline.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping, Optional, Sequence, Tuple

from .carla_client import import_carla

LOGGER = logging.getLogger(__name__)

Point = Tuple[float, float, float]

__all__ = [
    "LiveScenarioView",
    "LiveViewOptions",
    "RealtimePacer",
    "vehicle_center",
]


def vehicle_center(locations: Sequence[Point]) -> Point:
    """Return the arithmetic XYZ center of one or more vehicle locations."""
    if not locations:
        raise ValueError("at least one vehicle location is required")
    n = float(len(locations))
    return (
        sum(float(point[0]) for point in locations) / n,
        sum(float(point[1]) for point in locations) / n,
        sum(float(point[2]) for point in locations) / n,
    )


@dataclass(frozen=True)
class LiveViewOptions:
    """Operator-only controls for :class:`LiveScenarioView`."""

    mode: str = "overhead"
    follow_vehicle: str = "A"
    spectator_height: float = 35.0
    show_labels: bool = True
    realtime: bool = False
    playback_speed: float = 1.0
    smoothing: float = 0.35

    def __post_init__(self) -> None:
        mode = str(self.mode).lower()
        follow_vehicle = str(self.follow_vehicle).upper()
        if mode not in {"overhead", "follow"}:
            raise ValueError("spectator mode must be 'overhead' or 'follow'")
        if not follow_vehicle:
            raise ValueError("follow vehicle must not be empty")
        if float(self.spectator_height) <= 0.0:
            raise ValueError("spectator height must be greater than zero")
        if float(self.playback_speed) <= 0.0:
            raise ValueError("playback speed must be greater than zero")
        if not 0.0 < float(self.smoothing) <= 1.0:
            raise ValueError("spectator smoothing must be in the interval (0, 1]")
        object.__setattr__(self, "mode", mode)
        object.__setattr__(self, "follow_vehicle", follow_vehicle)


class RealtimePacer:
    """Pace wall-clock playback without changing the simulation tick."""

    def __init__(
        self,
        playback_speed: float = 1.0,
        clock: Callable[[], float] = time.perf_counter,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if float(playback_speed) <= 0.0:
            raise ValueError("playback speed must be greater than zero")
        self.playback_speed = float(playback_speed)
        self._clock = clock
        self._sleep = sleep
        self._wall_start: Optional[float] = None
        self._sim_start: float = 0.0

    def start(self, simulated_time: float = 0.0) -> None:
        """Start a playback epoch anchored to a simulation timestamp."""
        self._wall_start = float(self._clock())
        self._sim_start = float(simulated_time)

    def pace(self, simulated_time: float) -> float:
        """Sleep until the requested simulated time should be visible.

        Returns the sleep duration, or ``0.0`` when the loop is already behind.
        The caller invokes this only after all work for the current tick is done.
        """
        if self._wall_start is None:
            self.start(simulated_time)
        assert self._wall_start is not None
        simulated_elapsed = max(0.0, float(simulated_time) - self._sim_start)
        target_wall_elapsed = simulated_elapsed / self.playback_speed
        actual_wall_elapsed = float(self._clock()) - self._wall_start
        remaining = target_wall_elapsed - actual_wall_elapsed
        if remaining <= 0.0:
            return 0.0
        self._sleep(remaining)
        return remaining


class LiveScenarioView:
    """Move CARLA's native spectator and draw transient participant labels."""

    label_height_m = 2.5
    label_lifetime_s = 0.15

    def __init__(
        self,
        world: Any,
        vehicles: Mapping[str, Any],
        options: Optional[LiveViewOptions] = None,
        clock: Callable[[], float] = time.perf_counter,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.world = world
        self.vehicles: Dict[str, Any] = {
            str(pid).upper(): actor for pid, actor in vehicles.items()
        }
        if not self.vehicles:
            raise ValueError("live spectator view requires at least one vehicle")
        self.options = options or LiveViewOptions()
        if self.options.mode == "follow" and self.options.follow_vehicle not in self.vehicles:
            available = ", ".join(sorted(self.vehicles))
            raise ValueError(
                "live spectator follow target {0!r} is not present; available vehicles: {1}".format(
                    self.options.follow_vehicle, available
                )
            )

        self._previous_position: Optional[Point] = None
        self._pacer = (
            RealtimePacer(self.options.playback_speed, clock=clock, sleep=sleep)
            if self.options.realtime
            else None
        )
        self._spectator: Any = None
        self._available = True

        settings = None
        get_settings = getattr(self.world, "get_settings", None)
        if get_settings is not None:
            settings = get_settings()
        if bool(getattr(settings, "no_rendering_mode", False)):
            self._available = False
            LOGGER.warning(
                "live spectator requested, but CARLA is in no_rendering_mode; "
                "the scenario will run without a visible window"
            )
            return

        try:
            self._spectator = self.world.get_spectator()
        except Exception as exc:  # CARLA can raise several native exception types.
            raise RuntimeError(
                "live spectator mode could not access CARLA's native spectator: {0}".format(exc)
            ) from exc

    @property
    def available(self) -> bool:
        """Whether the connected world can display the external view."""
        return self._available

    def start(self, simulated_time: float = 0.0) -> None:
        """Start realtime pacing after scenario initialization is complete."""
        if self._pacer is not None:
            self._pacer.start(simulated_time)

    def pace(self, simulated_time: float) -> float:
        """Pace after the current tick's scientific work has completed."""
        if self._pacer is None:
            return 0.0
        return self._pacer.pace(simulated_time)

    def smooth_position(self, desired: Point) -> Point:
        """Apply the configured camera-position smoothing."""
        desired = tuple(float(value) for value in desired)  # type: ignore[assignment]
        if self._previous_position is None:
            self._previous_position = desired
            return desired
        alpha = float(self.options.smoothing)
        previous = self._previous_position
        smoothed = tuple(
            alpha * desired[index] + (1.0 - alpha) * previous[index]
            for index in range(3)
        )
        self._previous_position = smoothed  # type: ignore[assignment]
        return smoothed  # type: ignore[return-value]

    def update(self, simulated_time: float = 0.0) -> bool:
        """Update the spectator and labels for the current simulation tick."""
        if not self._available:
            return False

        points = self._vehicle_points()
        if not points:
            return False

        if self.options.mode == "follow":
            desired_position, target = self._follow_camera()
        else:
            desired_position, target = self._overhead_camera(points)
        camera_position = self.smooth_position(desired_position)
        self._spectator.set_transform(self._look_at(camera_position, target))

        if self.options.show_labels:
            self._draw_labels(points)
        return True

    def _vehicle_points(self) -> Dict[str, Point]:
        points: Dict[str, Point] = {}
        for pid, vehicle in self.vehicles.items():
            tf = vehicle.get_transform()
            loc = tf.location
            points[pid] = (float(loc.x), float(loc.y), float(loc.z))
        return points

    def _overhead_camera(self, points: Mapping[str, Point]) -> Tuple[Point, Point]:
        center = vehicle_center(list(points.values()))
        spread = max(
            math.hypot(point[0] - center[0], point[1] - center[1])
            for point in points.values()
        )
        height = max(float(self.options.spectator_height), 8.0 + 1.25 * spread)
        offset = max(8.0, min(0.45 * height, 0.35 * max(spread, 1.0)))
        camera = (center[0] - offset, center[1], center[2] + height)
        return camera, center

    def _follow_camera(self) -> Tuple[Point, Point]:
        vehicle = self.vehicles[self.options.follow_vehicle]
        tf = vehicle.get_transform()
        loc = tf.location
        yaw = math.radians(float(tf.rotation.yaw))
        forward = getattr(vehicle, "get_forward_vector", None)
        if forward is not None:
            vector = forward()
            fx, fy = float(vector.x), float(vector.y)
        else:
            fx, fy = math.cos(yaw), math.sin(yaw)
        distance = max(8.0, 0.28 * float(self.options.spectator_height))
        height = max(4.0, min(8.0, 0.2 * float(self.options.spectator_height)))
        camera = (float(loc.x) - fx * distance, float(loc.y) - fy * distance, float(loc.z) + height)
        target = (float(loc.x) + fx * 8.0, float(loc.y) + fy * 8.0, float(loc.z) + 1.5)
        return camera, target

    def _look_at(self, camera: Point, target: Point) -> Any:
        carla = import_carla()
        dx = target[0] - camera[0]
        dy = target[1] - camera[1]
        dz = target[2] - camera[2]
        horizontal = math.hypot(dx, dy)
        yaw = math.degrees(math.atan2(dy, dx)) if horizontal else 0.0
        pitch = math.degrees(math.atan2(dz, horizontal))
        return carla.Transform(
            carla.Location(x=camera[0], y=camera[1], z=camera[2]),
            carla.Rotation(pitch=pitch, yaw=yaw, roll=0.0),
        )

    def _draw_labels(self, points: Mapping[str, Point]) -> None:
        debug = getattr(self.world, "debug", None)
        if debug is None:
            LOGGER.warning("live spectator labels unavailable: CARLA debug API is missing")
            return
        carla = import_carla()
        colors = {"A": (255, 40, 40), "B": (40, 220, 60), "C": (60, 120, 255)}
        color_type = getattr(carla, "Color", None)
        for pid, point in points.items():
            kwargs: Dict[str, Any] = {
                "draw_shadow": True,
                "life_time": self.label_lifetime_s,
                "persistent_lines": False,
            }
            color_values = colors.get(pid)
            if color_values is not None and color_type is not None:
                kwargs["color"] = color_type(*color_values)
            debug.draw_string(
                carla.Location(
                    x=point[0], y=point[1], z=point[2] + self.label_height_m
                ),
                pid,
                **kwargs
            )
