"""Declarative scenario specification and construction.

A scenario is described entirely by data (``configs/scenarios/*.yaml``) and turned
into CARLA actors, routes and scripted controllers by the helpers here. Keeping
scenarios declarative buys three things the experiment protocol depends on:

* **Reproducibility** -- the whole specification is hashed into the run manifest.
* **Interventions** -- every behaviour is a named :class:`ScriptedAction`, so a
  counterfactual replay is "the same spec with one action disabled, delayed or
  weakened", not a separate hand-written variant.
* **Validation** -- the spec states what is supposed to happen (the expected
  outcome, the expected collision pair, minimum separation), so a scenario that
  silently stops producing its intended encounter fails loudly.

Spawn and route construction use the CARLA map API. That is legitimate: this is
test-generation code. The forensic pipeline observes only the resulting motion.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.geometry import angle_diff_deg, distance
from .carla_client import import_carla
from .controllers import RoutePlan, ScriptedAction, ScriptedController

LOGGER = logging.getLogger(__name__)

__all__ = [
    "SpawnSpec",
    "RouteSpec",
    "ParticipantSpec",
    "ScenarioSpec",
    "build_route",
    "resolve_spawn_waypoint",
    "junction_approach_waypoint",
]


# ---------------------------------------------------------------------------
# Specification dataclasses
# ---------------------------------------------------------------------------


@dataclass
class SpawnSpec:
    """How to derive a participant's spawn waypoint from the map.

    Three anchoring modes are supported:

    ``spawn_index``
        Offset from one of the map's recommended spawn points. Stable and
        readable for straight-road scenarios.
    ``location``
        An explicit ``(x, y)`` projected onto the nearest driving lane.
    ``junction_approach``
        The lane that approaches a given junction centre from a given compass
        bearing, backed off ``back_m`` metres. This is what makes crossing
        scenarios expressible without hand-copying coordinates per map.
    """

    anchor: str = "spawn_index"
    index: int = 0
    x: float = 0.0
    y: float = 0.0
    junction_x: float = 0.0
    junction_y: float = 0.0
    bearing_deg: float = 0.0
    back_m: float = 40.0
    forward_m: float = 0.0
    lane_offset: int = 0

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SpawnSpec":
        return SpawnSpec(
            anchor=d.get("anchor", "spawn_index"),
            index=int(d.get("index", 0)),
            x=float(d.get("x", 0.0)),
            y=float(d.get("y", 0.0)),
            junction_x=float(d.get("junction_x", 0.0)),
            junction_y=float(d.get("junction_y", 0.0)),
            bearing_deg=float(d.get("bearing_deg", 0.0)),
            back_m=float(d.get("back_m", 40.0)),
            forward_m=float(d.get("forward_m", 0.0)),
            lane_offset=int(d.get("lane_offset", 0)),
        )


@dataclass
class RouteSpec:
    """How far and through which turns a participant drives."""

    length_m: float = 200.0
    step_m: float = 2.0
    turns: List[str] = field(default_factory=list)
    """Turn decisions consumed in order at successive junctions:
    ``"straight"``, ``"left"`` or ``"right"``. Exhausted decisions default to
    ``"straight"``."""

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "RouteSpec":
        return RouteSpec(
            length_m=float(d.get("length_m", 200.0)),
            step_m=float(d.get("step_m", 2.0)),
            turns=[str(t) for t in d.get("turns", [])],
        )


@dataclass
class ParticipantSpec:
    """Everything needed to instantiate one participant vehicle."""

    participant_id: str
    blueprint: str = "vehicle.tesla.model3"
    spawn: SpawnSpec = field(default_factory=SpawnSpec)
    route: RouteSpec = field(default_factory=RouteSpec)
    initial_speed: float = 0.0
    """Velocity imparted at spawn, m/s, so the encounter does not need a long
    acceleration run-up."""
    target_speed: float = 12.0
    sensor_profile: Optional[str] = None
    """Per-participant radar profile override. This is how scenario S07 creates
    genuine partial observability through sensing rather than by deleting data."""
    actions: List[ScriptedAction] = field(default_factory=list)
    post_impact_stop: bool = True

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ParticipantSpec":
        actions = []
        for a in d.get("actions", []) or []:
            actions.append(
                ScriptedAction(
                    action_id=a["action_id"],
                    kind=a["kind"],
                    t_start=float(a.get("t_start", 0.0)),
                    duration=float(a.get("duration", 1.0)),
                    params={k: float(v) for k, v in (a.get("params", {}) or {}).items()},
                    enabled=bool(a.get("enabled", True)),
                )
            )
        return ParticipantSpec(
            participant_id=str(d["id"]),
            blueprint=d.get("blueprint", "vehicle.tesla.model3"),
            spawn=SpawnSpec.from_dict(d.get("spawn", {}) or {}),
            route=RouteSpec.from_dict(d.get("route", {}) or {}),
            initial_speed=float(d.get("initial_speed", 0.0)),
            target_speed=float(d.get("target_speed", 12.0)),
            sensor_profile=d.get("sensor_profile"),
            actions=actions,
            post_impact_stop=bool(d.get("post_impact_stop", True)),
        )


@dataclass
class ScenarioSpec:
    """A complete, validated scenario definition."""

    scenario_id: str
    name: str
    description: str = ""
    map_name: str = "Town05"
    variant: str = "default"
    participants: List[ParticipantSpec] = field(default_factory=list)

    expected_outcome: str = "collision"
    """``"collision"``, ``"near_miss"`` or ``"no_event"``."""
    expected_collision_pairs: List[List[str]] = field(default_factory=list)
    expected_collision_order: List[List[str]] = field(default_factory=list)
    """For chain collisions: the pairs in the order they must occur."""

    max_duration_s: float = 30.0
    validation: Dict[str, Any] = field(default_factory=dict)
    causal_template: List[Dict[str, Any]] = field(default_factory=list)
    """Designed ground-truth causal structure, consumed by the oracle graph
    builder. Never visible to local or fused inference."""
    intervention_candidates: List[str] = field(default_factory=list)
    """Action ids the counterfactual layer is allowed to intervene on."""
    traffic_control: Dict[str, Any] = field(default_factory=dict)
    """Stop and give-way signs, and where their stop lines are.

    Two jobs, and keeping them apart matters. At construction time it says what
    to place, because CARLA does not put a physical stop sign at every junction a
    scenario might want and an approach with no sign on it cannot be perceived.
    At evaluation time it is the privileged traffic-control ground truth: the true
    class of each sign, its position, its stop line, and which approach it
    governs.

    It is never read by local inference, which sees signs only through the
    camera. That is the whole point of having a camera: the gap between what the
    sign is and what the vehicle made of it is the perception result.

    Shape::

        traffic_control:
          signs:
            - sign_id: "stop_A"
              kind: "stop"              # stop | yield
              governs: "A"              # the approach it faces
              anchor: {...}             # same form as a participant spawn
              spawn_prop: true          # place a prop if the map has none
              stop_line_forward_m: 3.0  # line position relative to the sign
          tie_break: null               # participant id, or null: see below

    ``tie_break`` exists so that a near-simultaneous arrival at an all-way stop
    can be resolved *only* where the scenario says how. Left null -- the default
    -- the priority benchmark reports AMBIGUOUS_PRIORITY rather than applying a
    convention the experiment has not declared.
    """
    traffic_lights: Dict[str, Any] = field(default_factory=dict)
    """Optional signal configuration, e.g. freezing one approach on red.

    Scenario construction may set traffic-light state; the resulting states are
    recorded by the oracle only. Local inference has no way to observe them,
    which is exactly why those facts remain outside local and fused inference."""
    expected_local_unknowns: List[str] = field(default_factory=list)
    """Facts the local and fused layers are expected to be UNABLE to establish.
    The evaluation asserts they are absent locally and present in the oracle."""
    notes: List[str] = field(default_factory=list)

    def participant(self, participant_id: str) -> ParticipantSpec:
        for p in self.participants:
            if p.participant_id == participant_id:
                return p
        raise KeyError("no participant {0!r} in scenario {1}".format(participant_id, self.scenario_id))

    @property
    def participant_ids(self) -> List[str]:
        return [p.participant_id for p in self.participants]

    def validate_static(self) -> List[str]:
        """Structural checks that need no simulator. Returns a list of problems."""
        problems: List[str] = []
        ids = self.participant_ids
        if not 2 <= len(ids) <= 3:
            problems.append(
                "scenario must have 2 or 3 participants, found {0}".format(len(ids))
            )
        if len(set(ids)) != len(ids):
            problems.append("duplicate participant ids: {0}".format(ids))
        for pair in self.expected_collision_pairs:
            for pid in pair:
                if pid not in ids:
                    problems.append(
                        "expected_collision_pairs references unknown participant {0!r}".format(pid)
                    )
        action_ids: List[str] = []
        for p in self.participants:
            for a in p.actions:
                action_ids.append(a.action_id)
        if len(set(action_ids)) != len(action_ids):
            problems.append("duplicate scripted action ids: {0}".format(action_ids))
        signs = (self.traffic_control or {}).get("signs", []) or []
        sign_ids = [str(sign.get("sign_id", "")) for sign in signs]
        if len(set(sign_ids)) != len(sign_ids):
            problems.append("duplicate traffic-control sign ids: {0}".format(sign_ids))
        for sign in signs:
            kind = str(sign.get("kind", "")).lower()
            if kind not in ("stop", "yield"):
                problems.append(
                    "sign {0!r} has kind {1!r}; only 'stop' and 'yield' are "
                    "implemented, and a sign the detector cannot classify is "
                    "worse than one the scenario does not place".format(
                        sign.get("sign_id"), sign.get("kind"))
                )
            governs = str(sign.get("governs", ""))
            if governs and governs not in ids:
                problems.append(
                    "sign {0!r} governs unknown participant {1!r}".format(
                        sign.get("sign_id"), governs)
                )
        tie_break = (self.traffic_control or {}).get("tie_break")
        if tie_break is not None and str(tie_break) not in ids:
            problems.append(
                "traffic_control.tie_break names unknown participant "
                "{0!r}".format(tie_break)
            )

        for cand in self.intervention_candidates:
            if cand not in action_ids:
                problems.append(
                    "intervention candidate {0!r} is not a declared action".format(cand)
                )
        if self.expected_outcome not in ("collision", "near_miss", "no_event"):
            problems.append("unknown expected_outcome {0!r}".format(self.expected_outcome))
        return problems

    @staticmethod
    def from_config(cfg: Config, variant: Optional[str] = None) -> "ScenarioSpec":
        """Build a specification from a resolved run configuration.

        A named variant deep-merges its overrides over the base ``scenario``
        block, which is how S01 expresses both its crash and its avoided variant
        without duplicating the whole definition.
        """
        from ..common.config import deep_merge

        block = cfg.get("scenario", None)
        if block is None:
            raise KeyError(
                "configuration has no 'scenario' section; was a scenario config loaded?"
            )
        chosen = variant or block.get("default_variant", "default")
        variants = block.get("variants", {}) or {}
        if chosen != "default" and chosen not in variants:
            raise KeyError(
                "scenario {0} has no variant {1!r} (available: {2})".format(
                    block.get("scenario_id"), chosen, sorted(variants.keys()) or ["default"]
                )
            )
        merged = dict(block)
        if chosen in variants:
            merged = deep_merge(merged, variants[chosen] or {})
        # Variant participant overrides are keyed by participant id.
        overrides = merged.pop("participant_overrides", {}) or {}
        participants = []
        for pdict in merged.get("participants", []) or []:
            pid = str(pdict["id"])
            if pid in overrides:
                pdict = deep_merge(pdict, overrides[pid] or {})
            participants.append(ParticipantSpec.from_dict(pdict))

        spec = ScenarioSpec(
            scenario_id=str(merged["scenario_id"]),
            name=str(merged.get("name", merged["scenario_id"])),
            description=str(merged.get("description", "")),
            map_name=str(merged.get("map", "Town05")),
            variant=chosen,
            participants=participants,
            expected_outcome=str(merged.get("expected_outcome", "collision")),
            expected_collision_pairs=[list(p) for p in merged.get("expected_collision_pairs", [])],
            expected_collision_order=[list(p) for p in merged.get("expected_collision_order", [])],
            max_duration_s=float(merged.get("max_duration_s", 30.0)),
            validation=merged.get("validation", {}) or {},
            causal_template=merged.get("causal_template", []) or [],
            intervention_candidates=[str(c) for c in merged.get("intervention_candidates", [])],
            traffic_control=merged.get("traffic_control", {}) or {},
            traffic_lights=merged.get("traffic_lights", {}) or {},
            expected_local_unknowns=[
                str(u) for u in merged.get("expected_local_unknowns", []) or []
            ],
            notes=[str(n) for n in merged.get("notes", [])],
        )
        problems = spec.validate_static()
        if problems:
            raise ValueError(
                "scenario {0} variant {1!r} is invalid:\n  - {2}".format(
                    spec.scenario_id, chosen, "\n  - ".join(problems)
                )
            )
        return spec


# ---------------------------------------------------------------------------
# Map-based construction (scenario generation only)
# ---------------------------------------------------------------------------


def junction_approach_waypoint(
    carla_map: Any,
    junction_x: float,
    junction_y: float,
    bearing_deg: float,
    back_m: float,
    search_radius: float = 60.0,
    sample_step: float = 2.0,
) -> Any:
    """Find the lane that approaches a junction from a given compass bearing.

    ``bearing_deg`` is the direction of *travel* of the approaching vehicle, in
    CARLA's yaw convention. The function scans driving waypoints near the
    junction, keeps those whose heading points toward the junction centre and
    matches the requested bearing, and returns the one backed off ``back_m``
    metres along its lane.

    This makes crossing scenarios portable: the YAML names a junction centre and
    two bearings instead of a table of hand-measured spawn coordinates.
    """
    carla = import_carla()
    best = None
    best_score = float("inf")

    for wp in carla_map.generate_waypoints(sample_step):
        if wp.lane_type != carla.LaneType.Driving or wp.is_junction:
            continue
        loc = wp.transform.location
        d = distance(loc.x, loc.y, junction_x, junction_y)
        if d > search_radius or d < 8.0:
            continue
        heading = wp.transform.rotation.yaw
        # Must be travelling roughly toward the junction centre.
        to_junction = math.degrees(math.atan2(junction_y - loc.y, junction_x - loc.x))
        if abs(angle_diff_deg(heading, to_junction)) > 35.0:
            continue
        bearing_err = abs(angle_diff_deg(heading, bearing_deg))
        if bearing_err > 30.0:
            continue
        # Prefer a lane close to the requested stand-off distance and bearing.
        score = abs(d - back_m) + bearing_err * 0.5
        if score < best_score:
            best_score = score
            best = wp

    if best is None:
        raise ValueError(
            "no lane approaches junction ({0:.1f}, {1:.1f}) on bearing {2:.1f} deg "
            "within {3:.0f} m".format(junction_x, junction_y, bearing_deg, search_radius)
        )
    return best


def resolve_spawn_waypoint(carla_map: Any, spawn_points: Sequence[Any], spec: SpawnSpec) -> Any:
    """Turn a :class:`SpawnSpec` into a concrete lane waypoint."""
    carla = import_carla()

    if spec.anchor == "spawn_index":
        if not 0 <= spec.index < len(spawn_points):
            raise IndexError(
                "spawn index {0} out of range (map has {1} spawn points)".format(
                    spec.index, len(spawn_points)
                )
            )
        wp = carla_map.get_waypoint(
            spawn_points[spec.index].location,
            project_to_road=True,
            lane_type=carla.LaneType.Driving,
        )
    elif spec.anchor == "location":
        wp = carla_map.get_waypoint(
            carla.Location(x=spec.x, y=spec.y, z=0.0),
            project_to_road=True,
            lane_type=carla.LaneType.Driving,
        )
    elif spec.anchor == "junction_approach":
        wp = junction_approach_waypoint(
            carla_map,
            spec.junction_x,
            spec.junction_y,
            spec.bearing_deg,
            spec.back_m,
        )
    else:
        raise ValueError("unknown spawn anchor {0!r}".format(spec.anchor))

    if wp is None:
        raise ValueError("spawn spec {0!r} did not resolve to a driving lane".format(spec))

    # Lateral lane offset (positive = to the right of travel).
    for _ in range(abs(spec.lane_offset)):
        nxt = wp.get_right_lane() if spec.lane_offset > 0 else wp.get_left_lane()
        if nxt is None or nxt.lane_type != carla.LaneType.Driving or nxt.lane_id * wp.lane_id < 0:
            raise ValueError(
                "participant requests lane_offset {0} but no same-direction drivable "
                "lane exists there".format(spec.lane_offset)
            )
        wp = nxt

    if abs(spec.forward_m) > 1e-6:
        nxts = wp.next(abs(spec.forward_m)) if spec.forward_m > 0 else wp.previous(abs(spec.forward_m))
        if not nxts:
            raise ValueError(
                "cannot offset spawn by {0} m along the lane".format(spec.forward_m)
            )
        wp = nxts[0]
    return wp


def build_route(carla_map: Any, start_wp: Any, spec: RouteSpec) -> RoutePlan:
    """Sample a driveable route forward from ``start_wp``.

    At each junction the next turn decision is consumed from ``spec.turns``;
    when they run out the route continues straight. Choosing the successor by
    heading difference (rather than by CARLA's arbitrary successor order) is what
    makes crossing and roundabout routes reproducible.
    """
    points: List[Tuple[float, float]] = []
    headings: List[float] = []

    wp = start_wp
    turns = list(spec.turns)
    travelled = 0.0
    step = max(0.5, float(spec.step_m))
    guard = int(spec.length_m / step) * 4 + 100

    while travelled < float(spec.length_m) and guard > 0:
        guard -= 1
        tf = wp.transform
        points.append((float(tf.location.x), float(tf.location.y)))
        headings.append(float(tf.rotation.yaw))

        candidates = wp.next(step)
        if not candidates:
            LOGGER.warning(
                "route ended early after %.1f m of %.1f m requested", travelled, spec.length_m
            )
            break
        if len(candidates) == 1:
            wp = candidates[0]
        else:
            decision = turns.pop(0) if turns else "straight"
            wp = _choose_successor(wp, candidates, decision)
        travelled += step

    if len(points) < 2:
        raise ValueError("route degenerated to fewer than two points")
    return RoutePlan(points=points, headings=headings)


def _choose_successor(current: Any, candidates: Sequence[Any], decision: str) -> Any:
    """Pick the successor matching a turn decision, by relative heading."""
    base = current.transform.rotation.yaw
    scored: List[Tuple[float, Any]] = []
    for c in candidates:
        delta = angle_diff_deg(c.transform.rotation.yaw, base)
        scored.append((delta, c))

    decision = (decision or "straight").lower()
    if decision == "straight":
        return min(scored, key=lambda s: abs(s[0]))[1]
    if decision == "right":
        # In CARLA's left-handed frame a right turn increases yaw.
        rights = [s for s in scored if s[0] > 12.0]
        return max(rights, key=lambda s: s[0])[1] if rights else min(
            scored, key=lambda s: abs(s[0])
        )[1]
    if decision == "left":
        lefts = [s for s in scored if s[0] < -12.0]
        return min(lefts, key=lambda s: s[0])[1] if lefts else min(
            scored, key=lambda s: abs(s[0])
        )[1]
    raise ValueError("unknown turn decision {0!r}".format(decision))


def make_controller(spec: ParticipantSpec, route: RoutePlan) -> ScriptedController:
    """Instantiate the scripted controller for a participant specification."""
    return ScriptedController(
        participant_id=spec.participant_id,
        route=route,
        target_speed=spec.target_speed,
        actions=list(spec.actions),
        post_impact_stop=spec.post_impact_stop,
    )
