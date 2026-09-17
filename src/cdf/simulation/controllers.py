"""Deterministic scripted controllers used to *generate* scenarios.

These controllers are test-generation code. They legitimately know the scripted
world -- the route, the timing, the intended manoeuvre -- because they create it.
The forensic algorithm never sees any of this: it only observes the resulting
motion through onboard sensors. Keeping generation and inference in separate
modules is what makes that separation checkable rather than merely claimed.

Design
------
A participant's behaviour is fully described by

* a :class:`RoutePlan` -- a fixed polyline the vehicle follows,
* a base target speed, and
* an ordered list of :class:`ScriptedAction` items, each with an explicit
  ``action_id``, start time and duration.

That last piece is what makes the counterfactual layer possible: an intervention
is simply "remove, delay, or weaken the action with this id", replayed from the
same seed and spawn state. There is no hidden behaviour to intervene on.

Control is deliberately simple and deterministic: pure-pursuit lateral steering
plus a PI longitudinal controller. No randomness, no wall-clock, no Traffic
Manager in the safety-critical path.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.geometry import angle_diff_deg, distance

__all__ = [
    "ControlCommand",
    "VehicleState",
    "RoutePlan",
    "ScriptedAction",
    "ScriptedController",
    "PIDLongitudinal",
]


@dataclass
class ControlCommand:
    """A vehicle actuation command, mirroring ``carla.VehicleControl``."""

    throttle: float = 0.0
    brake: float = 0.0
    steer: float = 0.0
    hand_brake: bool = False
    reverse: bool = False

    def clamped(self) -> "ControlCommand":
        """Clamp every channel into its physical range."""
        return ControlCommand(
            throttle=min(1.0, max(0.0, float(self.throttle))),
            brake=min(1.0, max(0.0, float(self.brake))),
            steer=min(1.0, max(-1.0, float(self.steer))),
            hand_brake=bool(self.hand_brake),
            reverse=bool(self.reverse),
        )


@dataclass
class VehicleState:
    """The controller's view of its own vehicle (own state only)."""

    t: float
    x: float
    y: float
    yaw: float
    """Heading in degrees."""
    speed: float
    """Ground speed in m/s."""
    vx: float = 0.0
    vy: float = 0.0


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------


@dataclass
class RoutePlan:
    """A fixed polyline route with a lateral offset channel.

    The lateral offset is how lane-change and cut-in manoeuvres are produced: the
    pursuit target is displaced sideways from the nominal route, so the vehicle
    smoothly leaves its lane without any map-level lane-change command.
    """

    points: List[Tuple[float, float]] = field(default_factory=list)
    headings: List[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.points and not self.headings:
            self.headings = self._derive_headings()

    def _derive_headings(self) -> List[float]:
        out: List[float] = []
        for i in range(len(self.points)):
            j = min(i + 1, len(self.points) - 1)
            k = max(i - 1, 0)
            dx = self.points[j][0] - self.points[k][0]
            dy = self.points[j][1] - self.points[k][1]
            out.append(math.degrees(math.atan2(dy, dx)) if (dx or dy) else 0.0)
        return out

    def __len__(self) -> int:
        return len(self.points)

    def nearest_index(self, x: float, y: float, hint: int = 0) -> int:
        """Index of the closest route point, searching forward from ``hint``.

        Searching forward keeps the controller from snapping back to an earlier
        part of a route that crosses itself (roundabouts, loops).
        """
        if not self.points:
            raise ValueError("route is empty")
        best_i = max(0, min(int(hint), len(self.points) - 1))
        best_d = distance(x, y, *self.points[best_i])
        for i in range(best_i, len(self.points)):
            d = distance(x, y, *self.points[i])
            if d < best_d:
                best_i, best_d = i, d
            elif d > best_d + 12.0:
                # Moving away for a while: the minimum is behind us.
                break
        return best_i

    def lookahead(
        self, x: float, y: float, distance_m: float, hint: int = 0
    ) -> Tuple[float, float, int]:
        """The point ``distance_m`` further along the route, and its index."""
        i = self.nearest_index(x, y, hint)
        travelled = 0.0
        j = i
        while j + 1 < len(self.points) and travelled < float(distance_m):
            travelled += distance(*self.points[j], *self.points[j + 1])
            j += 1
        return (self.points[j][0], self.points[j][1], i)

    def offset_point(self, index: int, lateral_m: float) -> Tuple[float, float]:
        """A route point displaced ``lateral_m`` to its right (positive = right)."""
        idx = max(0, min(int(index), len(self.points) - 1))
        px, py = self.points[idx]
        heading = self.headings[idx]
        # +y is to the right of the heading in CARLA's left-handed planar frame.
        rx = -math.sin(math.radians(heading)) * float(lateral_m)
        ry = math.cos(math.radians(heading)) * float(lateral_m)
        return (px + rx, py + ry)

    def remaining_distance(self, index: int) -> float:
        """Route length remaining from ``index`` to the end."""
        total = 0.0
        for i in range(max(0, int(index)), len(self.points) - 1):
            total += distance(*self.points[i], *self.points[i + 1])
        return total


# ---------------------------------------------------------------------------
# Scripted actions (the intervention handles)
# ---------------------------------------------------------------------------


@dataclass
class ScriptedAction:
    """One named, timed behaviour modification.

    ``action_id`` is the handle the counterfactual layer intervenes on. Keep ids
    stable and descriptive (``"B_emergency_brake"``, ``"B_cut_in"``), because they
    appear in counterfactual manifests and in the causal-contribution report.

    Supported kinds
    ---------------
    ``brake``        params: ``intensity`` (0..1)
    ``set_speed``    params: ``target_speed`` (m/s)
    ``lane_shift``   params: ``lateral_m`` (signed, positive = right), applied
                     progressively over ``duration``
    ``hold``         params: ``target_speed``; simply maintains a speed
    ``stop``         full brake and hand brake
    """

    action_id: str
    kind: str
    t_start: float
    duration: float = 1.0
    params: Dict[str, float] = field(default_factory=dict)
    enabled: bool = True

    def active_at(self, t: float) -> bool:
        return self.enabled and (self.t_start <= float(t) < self.t_start + self.duration)

    def elapsed_fraction(self, t: float) -> float:
        """Progress through the action in ``[0, 1]``."""
        if self.duration <= 0.0:
            return 1.0
        return max(0.0, min(1.0, (float(t) - self.t_start) / self.duration))

    def started(self, t: float) -> bool:
        return self.enabled and float(t) >= self.t_start

    def describe(self) -> Dict[str, Any]:
        """Serialisable description for the run manifest."""
        return {
            "action_id": self.action_id,
            "kind": self.kind,
            "t_start": self.t_start,
            "duration": self.duration,
            "params": dict(self.params),
            "enabled": self.enabled,
        }


# ---------------------------------------------------------------------------
# Longitudinal control
# ---------------------------------------------------------------------------


class PIDLongitudinal:
    """A small PI speed controller with anti-windup.

    Derivative action is omitted on purpose: with a fixed 0.05 s step and a noise
    free own-speed signal it adds nothing but sensitivity to step changes in the
    target, which scripted actions produce constantly.
    """

    def __init__(self, kp: float = 0.55, ki: float = 0.12, integral_limit: float = 4.0) -> None:
        self.kp = float(kp)
        self.ki = float(ki)
        self.integral_limit = float(integral_limit)
        self._integral = 0.0

    def reset(self) -> None:
        self._integral = 0.0

    def step(self, target_speed: float, current_speed: float, dt: float) -> Tuple[float, float]:
        """Return ``(throttle, brake)`` for the given speed error."""
        error = float(target_speed) - float(current_speed)
        self._integral += error * float(dt)
        self._integral = max(-self.integral_limit, min(self.integral_limit, self._integral))
        command = self.kp * error + self.ki * self._integral

        if command >= 0.0:
            return (min(1.0, command), 0.0)
        # Release the integral when braking so it does not fight the next accel.
        self._integral = min(self._integral, 0.0)
        return (0.0, min(1.0, -command * 0.6))


# ---------------------------------------------------------------------------
# The scripted controller
# ---------------------------------------------------------------------------


class ScriptedController:
    """Deterministic route-following controller driven by scripted actions.

    Lateral control is pure pursuit against a lookahead point on the route,
    displaced by whatever lateral offset the active ``lane_shift`` actions
    request. Longitudinal control is a PI loop on the current target speed,
    overridden while a ``brake`` or ``stop`` action is active.
    """

    def __init__(
        self,
        participant_id: str,
        route: RoutePlan,
        target_speed: float,
        actions: Optional[Sequence[ScriptedAction]] = None,
        lookahead_base_m: float = 5.0,
        lookahead_time_s: float = 0.6,
        max_steer: float = 0.8,
        steer_gain: float = 0.9,
        steer_rate_limit: float = 0.14,
        post_impact_stop: bool = True,
    ) -> None:
        self.participant_id = participant_id
        self.route = route
        self.base_target_speed = float(target_speed)
        self.actions: List[ScriptedAction] = list(actions or [])
        self.lookahead_base_m = float(lookahead_base_m)
        self.lookahead_time_s = float(lookahead_time_s)
        self.max_steer = float(max_steer)
        self.steer_gain = float(steer_gain)
        self.steer_rate_limit = float(steer_rate_limit)
        self.post_impact_stop = bool(post_impact_stop)

        self._pid = PIDLongitudinal()
        self._route_hint = 0
        self._last_steer = 0.0
        self._lateral_offset = 0.0
        self._current_target_speed = float(target_speed)
        self._impacted = False

    # -- state ------------------------------------------------------------

    def reset(self) -> None:
        """Return the controller to its initial state (for a clean replay)."""
        self._pid.reset()
        self._route_hint = 0
        self._last_steer = 0.0
        self._lateral_offset = 0.0
        self._current_target_speed = self.base_target_speed
        self._impacted = False

    def notify_impact(self) -> None:
        """Tell the controller its vehicle was hit.

        Post-impact behaviour must be scripted rather than left to physics, so
        that POST_IMPACT_STOP is a reproducible part of the scenario.
        """
        self._impacted = True

    def action(self, action_id: str) -> Optional[ScriptedAction]:
        for a in self.actions:
            if a.action_id == action_id:
                return a
        return None

    def describe(self) -> Dict[str, Any]:
        """Serialisable controller description for the run manifest."""
        return {
            "type": "ScriptedController",
            "participant_id": self.participant_id,
            "target_speed": self.base_target_speed,
            "route_points": len(self.route),
            "lookahead_base_m": self.lookahead_base_m,
            "lookahead_time_s": self.lookahead_time_s,
            "actions": [a.describe() for a in self.actions],
        }

    # -- control ----------------------------------------------------------

    def step(self, state: VehicleState, dt: float) -> ControlCommand:
        """Compute the actuation command for this tick."""
        if self._impacted and self.post_impact_stop:
            return ControlCommand(throttle=0.0, brake=1.0, steer=0.0).clamped()

        target_speed = self._resolve_target_speed(state.t)
        lateral = self._resolve_lateral_offset(state.t)
        brake_override = self._resolve_brake_override(state.t)

        steer = self._steer(state, lateral)

        if brake_override is not None:
            throttle, brake = 0.0, brake_override
            self._pid.reset()
        else:
            throttle, brake = self._pid.step(target_speed, state.speed, dt)

        return ControlCommand(
            throttle=throttle, brake=brake, steer=steer, hand_brake=False
        ).clamped()

    def _resolve_target_speed(self, t: float) -> float:
        """Latest ``set_speed``/``hold`` action that has started wins."""
        speed = self.base_target_speed
        for a in self.actions:
            if a.kind in ("set_speed", "hold") and a.started(t):
                speed = float(a.params.get("target_speed", speed))
        self._current_target_speed = speed
        return speed

    def _resolve_brake_override(self, t: float) -> Optional[float]:
        """Strongest active braking command, if any."""
        best: Optional[float] = None
        for a in self.actions:
            if a.kind == "brake" and a.active_at(t):
                intensity = float(a.params.get("intensity", 1.0))
                best = intensity if best is None else max(best, intensity)
            elif a.kind == "stop" and a.started(t):
                best = 1.0
        return best

    def _resolve_lateral_offset(self, t: float) -> float:
        """Accumulated lateral displacement requested by ``lane_shift`` actions.

        The offset ramps in smoothly with a raised-cosine profile, which produces
        a realistic cut-in trajectory instead of a step that the pursuit
        controller would chase with a violent steer.
        """
        offset = 0.0
        for a in self.actions:
            if a.kind != "lane_shift" or not a.enabled:
                continue
            if float(t) < a.t_start:
                continue
            target = float(a.params.get("lateral_m", 0.0))
            frac = a.elapsed_fraction(t)
            smooth = 0.5 * (1.0 - math.cos(math.pi * frac))
            offset += target * smooth
        self._lateral_offset = offset
        return offset

    def _steer(self, state: VehicleState, lateral_offset: float) -> float:
        """Pure-pursuit steering toward a laterally displaced lookahead point."""
        if len(self.route) < 2:
            return 0.0
        lookahead_m = self.lookahead_base_m + self.lookahead_time_s * max(0.0, state.speed)
        tx, ty, idx = self.route.lookahead(state.x, state.y, lookahead_m, self._route_hint)
        self._route_hint = idx

        if abs(lateral_offset) > 1e-6:
            # Displace the pursuit target sideways relative to the route heading.
            look_idx = min(len(self.route) - 1, idx + self._points_ahead(idx, lookahead_m))
            tx, ty = self.route.offset_point(look_idx, lateral_offset)

        desired_heading = math.degrees(math.atan2(ty - state.y, tx - state.x))
        error = angle_diff_deg(desired_heading, state.yaw)
        steer = self.steer_gain * (error / 45.0)
        steer = max(-self.max_steer, min(self.max_steer, steer))

        # Rate limiting keeps the trajectory smooth and reproducible.
        delta = max(-self.steer_rate_limit, min(self.steer_rate_limit, steer - self._last_steer))
        steer = self._last_steer + delta
        self._last_steer = steer
        return steer

    def _points_ahead(self, index: int, lookahead_m: float) -> int:
        """How many route points ``lookahead_m`` corresponds to from ``index``."""
        travelled = 0.0
        j = index
        while j + 1 < len(self.route) and travelled < lookahead_m:
            travelled += distance(*self.route.points[j], *self.route.points[j + 1])
            j += 1
        return j - index

    # -- introspection used by scenario validation ------------------------

    @property
    def lateral_offset(self) -> float:
        """The lateral displacement currently commanded (metres, + = right)."""
        return self._lateral_offset

    @property
    def target_speed(self) -> float:
        """The speed the controller is currently aiming for (m/s)."""
        return self._current_target_speed

    @property
    def impacted(self) -> bool:
        return self._impacted
