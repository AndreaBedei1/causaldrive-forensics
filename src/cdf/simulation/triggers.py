"""Privileged triggers for scripted actions (scenario construction only).

A triggered action has no fixed start time.  It is armed when the run starts
and fires when a condition on the simulator's true state becomes true; it then
starts ``reaction_s`` later and plays exactly like a timed action.  This is how
a scenario makes one vehicle *react* to another (an evasive manoeuvre that
happens because a car cut in, and does not happen when it does not) instead of
replaying a schedule that coincides with it.

The condition reads true poses of other actors, which no recorder has.  That is
legitimate for building a scenario and for nothing else: firings are written to
``ground_truth/triggers.jsonl`` only, never to ``vehicles/``, and the
reconstruction never sees them.  A trigger whose target is not in the run (a
counterfactual without that vehicle) can never fire.

Only one kind exists so far:

``envelope_entry``
    Fires the first time any part of the target's true bounding box lies in a
    corridor ahead of the owner's front face: ``ahead_m`` long, as wide as the
    owner plus ``lateral_margin_m`` on each side, in the owner's own frame.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

__all__ = ["ActionTrigger", "Pose", "TRIGGER_KINDS", "envelope_entry", "box_outline"]

TRIGGER_KINDS = ("envelope_entry",)


@dataclass(frozen=True)
class Pose:
    """A vehicle's true planar pose and bounding box (centre, yaw, half extents)."""

    x: float
    y: float
    yaw_deg: float
    half_length: float
    half_width: float


@dataclass
class ActionTrigger:
    """When an armed action fires.  See the module docstring."""

    kind: str
    target: str
    ahead_m: float = 15.0
    lateral_margin_m: float = 0.3
    reaction_s: float = 0.5
    window_start_s: float = 0.0
    window_end_s: float = math.inf

    def __post_init__(self) -> None:
        if self.kind not in TRIGGER_KINDS:
            raise ValueError("unknown trigger kind {0!r} (known: {1})".format(self.kind, ", ".join(TRIGGER_KINDS)))
        if not self.target:
            raise ValueError("a trigger needs a target participant")
        if self.ahead_m <= 0.0 or self.reaction_s < 0.0 or self.lateral_margin_m < 0.0:
            raise ValueError("trigger distances and delays must be non-negative (ahead_m > 0)")
        if self.window_end_s < self.window_start_s:
            raise ValueError("trigger window ends before it starts")

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ActionTrigger":
        window = d.get("window_s") or [0.0, math.inf]
        return ActionTrigger(
            kind=str(d.get("kind", "")),
            target=str(d.get("target", "")),
            ahead_m=float(d.get("ahead_m", 15.0)),
            lateral_margin_m=float(d.get("lateral_margin_m", 0.3)),
            reaction_s=float(d.get("reaction_s", 0.5)),
            window_start_s=float(window[0]),
            window_end_s=float(window[1]),
        )

    def in_window(self, t: float) -> bool:
        return self.window_start_s <= float(t) <= self.window_end_s

    def condition(self, owner: Pose, target: Pose) -> bool:
        if self.kind == "envelope_entry":
            return envelope_entry(owner, target, self.ahead_m, self.lateral_margin_m)
        raise ValueError(self.kind)

    def describe(self) -> Dict[str, Any]:
        return {"kind": self.kind, "target": self.target, "ahead_m": self.ahead_m,
                "lateral_margin_m": self.lateral_margin_m, "reaction_s": self.reaction_s,
                "window_s": [self.window_start_s, None if math.isinf(self.window_end_s) else self.window_end_s]}


def box_outline(pose: Pose, step: float = 0.25) -> List[Tuple[float, float]]:
    """Points every ``step`` metres along a box's outline, world frame."""
    c, s = math.cos(math.radians(pose.yaw_deg)), math.sin(math.radians(pose.yaw_deg))
    ex, ey = pose.half_length, pose.half_width

    def ticks(extent: float) -> Iterable[float]:
        n = max(1, int(math.ceil(2.0 * extent / step)))
        return [-extent + 2.0 * extent * i / n for i in range(n + 1)]

    local = [(x, side * ey) for x in ticks(ex) for side in (-1.0, 1.0)]
    local += [(side * ex, y) for y in ticks(ey) for side in (-1.0, 1.0)]
    return [(pose.x + c * x - s * y, pose.y + s * x + c * y) for x, y in local]


def envelope_entry(owner: Pose, target: Pose, ahead_m: float, lateral_margin_m: float) -> bool:
    """Is any part of ``target``'s box inside the corridor ahead of ``owner``'s front face?

    Owner frame: x forward, y to the right (CARLA's left-handed convention);
    the corridor is ``half_length < x <= half_length + ahead_m`` and
    ``|y| <= half_width + lateral_margin_m``.
    """
    c, s = math.cos(math.radians(owner.yaw_deg)), math.sin(math.radians(owner.yaw_deg))
    front = owner.half_length
    half = owner.half_width + lateral_margin_m
    for px, py in box_outline(target):
        dx, dy = px - owner.x, py - owner.y
        along = c * dx + s * dy
        across = -s * dx + c * dy
        if front < along <= front + ahead_m and abs(across) <= half:
            return True
    return False


def fire_due_triggers(t: float, poses: Dict[str, Pose], armed: Iterable[Tuple[str, Any]]) -> List[Dict[str, Any]]:
    """Fire every armed action whose condition holds at scenario time ``t``.

    ``armed`` yields ``(owner_id, action)`` for actions with a trigger that has
    not fired yet; ``poses`` holds every participant actually in the run.
    Returns one privileged record per firing.
    """
    fired = []
    for owner_id, action in armed:
        trigger: Optional[ActionTrigger] = action.trigger
        if trigger is None or action.fired_at is not None or not trigger.in_window(t):
            continue
        owner, target = poses.get(owner_id), poses.get(trigger.target)
        if owner is None or target is None:
            continue  # the target is not in this run: the action can never fire
        if trigger.condition(owner, target):
            action.fire(t)
            fired.append({"t_scenario": round(float(t), 4), "participant_id": owner_id,
                          "action_id": action.action_id, "trigger": trigger.describe(),
                          "action_t_start": round(float(action.t_start), 4)})
    return fired
