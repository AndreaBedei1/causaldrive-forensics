"""Causal reasoning over the *fused* event set, after identities are resolved.

Why this stage exists
---------------------

Local causal edges are proposed inside one vehicle's log, so a rule can only fire
when one vehicle saw **both** the cause and the effect. That is the wrong shape
for a multi-vehicle incident. The common case is:

    B brakes hard      -- recorded by B, in B's own telemetry
    the gap to B closes -- recorded by A, on A's radar
    A's time-to-collision collapses
    A and B collide

Node merging already puts B's deceleration and A's observation of it into one
fused node (``cdf.fusion.event_alignment`` places ``TARGET_DECELERATION`` in the
same family as ``DECELERATION``). But the *edge* "B's braking closed the gap"
belongs to no single log: A never saw the brake command and B never measured the
closing range. Merging nodes cannot invent it, and
:func:`cdf.fusion.graph_fusion.fuse_graphs` deliberately does not -- it only
remaps and unions the participants' own claims.

This module is the missing step. It reasons over the fused node set *once the
identities are known*, and proposes the causal edges that only become available
after fusion.

What it is allowed to use
-------------------------

Fused nodes, their resolved subjects, the common timeline, the track-association
confidences and the clock-alignment confidences. Nothing else. No oracle, no
scenario, no scripted action, no map, no actor id. The rules are stated over
event semantics (families and the vehicles an event makes a claim about) and are
identical for every scenario -- there is no branch anywhere on a scenario id, a
variant or an action name.

The three disciplines
---------------------

1. **Observation is not causation.** A radar track appearing is evidence that a
   vehicle is there, not a cause of anything. ``RADAR_TRACK_APPEARED`` and
   ``RADAR_TRACK_LOST`` may never be an endpoint of a causal edge
   (:data:`FORBIDDEN_CAUSAL_TYPES`), exactly as in the local rule table.

2. **A cause precedes its effect, on the common clock.** Every proposal is
   checked against ``t_peak`` in common time, with an explicit allowance for
   clock-alignment error that is *derived from the alignment itself* rather than
   guessed: a pair of participants whose clocks were aligned poorly gets a wider
   tolerance, and the allowance used is written onto the edge.

3. **Nothing is overwritten.** If the participants already claim a relation
   between two fused nodes, their claim stands and no inferred edge is added for
   that ordered pair. An inferred edge is only ever *new* structure, and it is
   labelled ``origin="post_fusion_inference"`` so a reader can always separate
   what the vehicles said from what fusion concluded.

The vehicles an event is about
------------------------------

After fusion every node carries a resolved subject, which makes this well
defined (:func:`node_subjects`):

* a **unary** event (a deceleration, a brake command, a lane change) is about one
  vehicle -- the one it describes, whoever observed it;
* a **relational** event (a closing range, a low TTC, a collision) is about an
  unordered **pair**.

Rules are then stated as set relations between the cause's vehicles and the
effect's vehicles -- ``same_actor``, ``actor_in_pair``, ``pair_to_actor``,
``same_pair``, ``shared_member`` -- which is what makes them general.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    Evidence,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from ..common.timeline import Interval, temporal_relation
from .event_alignment import family_of
from .track_association import TrackAssignment

__all__ = [
    "GlobalCausalRule",
    "DEFAULT_GLOBAL_RULES",
    "FORBIDDEN_CAUSAL_TYPES",
    "ORIGIN_LOCAL",
    "ORIGIN_INFERRED",
    "node_subjects",
    "infer_global_causal_edges",
]


#: Marker written into ``GraphEdge.detail["origin"]``.
ORIGIN_LOCAL = "local"
ORIGIN_INFERRED = "post_fusion_inference"

#: Track lifecycle events are evidence that something was observed, never a
#: physical cause. Keeping them out of causal edges is the single most important
#: discipline in this module: without it, "the radar acquired a track" would
#: appear to cause every collision that follows it.
FORBIDDEN_CAUSAL_TYPES: FrozenSet[str] = frozenset(
    {
        EventType.RADAR_TRACK_APPEARED.value,
        EventType.RADAR_TRACK_LOST.value,
    }
)

# --- semantic groups, stated once -----------------------------------------
_BRAKE_COMMAND = (EventType.BRAKE_ONSET.value, EventType.HARD_BRAKE.value)
_DECELERATION = (
    EventType.DECELERATION.value,
    EventType.HARD_DECELERATION.value,
    EventType.TARGET_DECELERATION.value,
)
_SPEED_UP = (EventType.ACCELERATION.value, EventType.VEHICLE_STARTED.value)
_THROTTLE = (EventType.THROTTLE_ONSET.value,)
_LATERAL_OWN = (
    EventType.LANE_CHANGE_LIKE_MANEUVER.value,
    EventType.CUT_IN_LIKE_MOTION.value,
    EventType.SIGNIFICANT_HEADING_CHANGE.value,
    EventType.STEER_ONSET.value,
)
_CLOSING = (EventType.RANGE_DECREASING.value, EventType.RAPID_CLOSING.value)
_TTC_RISK = (EventType.LOW_TTC.value, EventType.CRITICAL_TTC.value)
_CONFLICT = (
    EventType.PREDICTED_PATH_CONFLICT.value,
    EventType.CONFLICT_REGION_ENTRY.value,
)
_LATERAL_REL = (EventType.LATERAL_CROSSING.value,)
_COLLISION = (EventType.COLLISION.value,)
_NEAR_MISS = (EventType.NEAR_MISS.value,)
_POST_IMPACT = (EventType.POST_IMPACT_STOP.value,)


@dataclass(frozen=True)
class GlobalCausalRule:
    """One general causal rule over the fused event set.

    ``relation`` states how the vehicles the cause is about must relate to the
    vehicles the effect is about. It is what makes a rule cross-participant
    without naming any participant:

    ``same_actor``
        both sides describe the same single vehicle (B's brake command and B's
        deceleration);
    ``actor_in_pair``
        the cause describes one vehicle, the effect a pair containing it (B's
        deceleration and the closing gap between A and B);
    ``pair_to_actor``
        the cause describes a pair, the effect one of its members (the A-B
        time-to-collision and A's braking);
    ``same_pair``
        both describe the same pair (A-B closing and A-B low TTC);
    ``shared_member``
        both describe pairs sharing exactly one vehicle (the A-B impact and the
        B-C impact that follows it).
    """

    name: str
    cause_types: Tuple[str, ...]
    effect_types: Tuple[str, ...]
    edge_type: CausalEdgeType
    relation: str
    prior: float
    max_lag_s: float
    description: str
    #: When true the rule only fires if the cause and the effect are not backed
    #: by the same single participant -- i.e. the edge is genuinely knowledge
    #: that fusion created rather than a restatement of one vehicle's account.
    require_cross_participant: bool = False
    #: When true the cause must precede the effect by *more than the clock
    #: uncertainty*. Needed wherever the claim is about ordering itself: two
    #: impacts that cannot be ordered beyond the alignment residual are not
    #: evidence of a chain in either direction, and asserting one would also
    #: create a two-cycle for the DAG stage to break arbitrarily.
    require_strict_order: bool = False

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("a global causal rule needs a name")
        if self.relation not in _RELATIONS:
            raise ValueError(
                "rule {0!r} uses unknown relation {1!r}; expected one of {2}".format(
                    self.name, self.relation, ", ".join(sorted(_RELATIONS))
                )
            )
        if not 0.0 < float(self.prior) <= 1.0:
            raise ValueError(
                "rule {0!r} prior must be in (0, 1], got {1!r}".format(
                    self.name, self.prior
                )
            )
        if float(self.max_lag_s) <= 0.0:
            raise ValueError(
                "rule {0!r} max_lag_s must be positive, got {1!r}".format(
                    self.name, self.max_lag_s
                )
            )
        overlap = set(self.cause_types) & set(self.effect_types)
        if overlap and self.relation != "shared_member":
            # A type on both sides is only sound when the relation itself
            # guarantees the two endpoints describe *different* vehicles --
            # which is exactly what ``shared_member`` does (two impacts sharing
            # one vehicle). Everywhere else it would let an event cause itself.
            raise ValueError(
                "rule {0!r} has {1} on both sides under relation {2!r}; a type "
                "may only repeat when the relation separates the vehicles".format(
                    self.name, ", ".join(sorted(overlap)), self.relation
                )
            )
        banned = (set(self.cause_types) | set(self.effect_types)) & FORBIDDEN_CAUSAL_TYPES
        if banned:
            raise ValueError(
                "rule {0!r} uses observation-only type(s) {1} as a causal "
                "endpoint".format(self.name, ", ".join(sorted(banned)))
            )


_RELATIONS = ("same_actor", "actor_in_pair", "pair_to_actor", "same_pair", "shared_member")


#: The rule table. Every entry is a statement about physics and geometry that
#: holds in any scenario; none of them mentions a scenario, a variant, a role or
#: a scripted action. Priors are ordered by how directly the relation follows
#: from the measurement, not tuned against any reference graph.
DEFAULT_GLOBAL_RULES: Tuple[GlobalCausalRule, ...] = (
    # -- one vehicle's behaviour, reconstructed across logs -----------------
    GlobalCausalRule(
        name="global_brake_command_decelerates_vehicle",
        cause_types=_BRAKE_COMMAND,
        effect_types=_DECELERATION,
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="same_actor",
        prior=0.85,
        max_lag_s=1.5,
        description=(
            "A brake command is recorded by the braking vehicle; the resulting "
            "deceleration may be measured by that vehicle, by a vehicle watching "
            "it on radar, or by both."
        ),
    ),
    GlobalCausalRule(
        name="global_throttle_accelerates_vehicle",
        cause_types=_THROTTLE,
        effect_types=_SPEED_UP,
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="same_actor",
        prior=0.85,
        max_lag_s=2.0,
        description="A throttle command is followed by that vehicle's acceleration.",
    ),
    # -- one vehicle's behaviour changing a pairwise relation ---------------
    GlobalCausalRule(
        name="remote_deceleration_closes_gap",
        cause_types=_DECELERATION,
        effect_types=_CLOSING,
        edge_type=CausalEdgeType.TRIGGERS,
        relation="actor_in_pair",
        prior=0.80,
        max_lag_s=2.5,
        description=(
            "A vehicle slowing shortens the gap to anything following it. The "
            "deceleration and the closing range are routinely measured by "
            "different vehicles, which is why this edge cannot be proposed "
            "before fusion."
        ),
    ),
    GlobalCausalRule(
        name="remote_braking_contributes_to_closing",
        cause_types=_BRAKE_COMMAND,
        effect_types=_CLOSING,
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="actor_in_pair",
        prior=0.70,
        max_lag_s=3.0,
        description=(
            "The braking command itself is only ever in the braking vehicle's "
            "own log; the gap it closes is only ever in the follower's. Linking "
            "them is the clearest example of a claim that needs both accounts."
        ),
        require_cross_participant=True,
    ),
    GlobalCausalRule(
        name="remote_acceleration_closes_gap",
        cause_types=_SPEED_UP,
        effect_types=_CLOSING,
        edge_type=CausalEdgeType.INCREASES_RISK_OF,
        relation="actor_in_pair",
        prior=0.40,
        max_lag_s=3.0,
        description=(
            "Closure is relative: a vehicle speeding up shortens the gap to "
            "whatever is ahead of it just as the vehicle ahead braking does. "
            "Stated so the reconstruction stays symmetric."
        ),
    ),
    GlobalCausalRule(
        name="remote_lateral_manoeuvre_creates_conflict",
        cause_types=_LATERAL_OWN,
        effect_types=_CONFLICT,
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="actor_in_pair",
        prior=0.55,
        max_lag_s=3.0,
        description=(
            "A vehicle changing lane or heading puts itself on a path that "
            "conflicts with another's. The manoeuvre is in that vehicle's own "
            "telemetry; the conflict is inferred by the vehicle it threatens."
        ),
    ),
    # -- escalation within one pair ----------------------------------------
    GlobalCausalRule(
        name="global_closing_increases_ttc_risk",
        cause_types=_CLOSING,
        effect_types=(EventType.LOW_TTC.value,),
        edge_type=CausalEdgeType.INCREASES_RISK_OF,
        relation="same_pair",
        prior=0.50,
        max_lag_s=4.0,
        description="A gap that keeps shortening drives the time-to-collision down.",
    ),
    GlobalCausalRule(
        name="global_ttc_escalates_to_critical",
        cause_types=(EventType.LOW_TTC.value,) + _CLOSING,
        effect_types=(EventType.CRITICAL_TTC.value,),
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="same_pair",
        prior=0.80,
        max_lag_s=3.0,
        description="A low time-to-collision that is not resolved becomes critical.",
    ),
    GlobalCausalRule(
        name="global_lateral_crossing_predicts_conflict",
        cause_types=_LATERAL_REL,
        effect_types=_CONFLICT,
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="same_pair",
        prior=0.60,
        max_lag_s=3.0,
        description="A target crossing our heading is what makes a path conflict credible.",
    ),
    GlobalCausalRule(
        name="global_conflict_shortens_ttc",
        cause_types=_CONFLICT,
        effect_types=_TTC_RISK,
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="same_pair",
        prior=0.70,
        max_lag_s=3.0,
        description="Converging paths collapse the margin between the two vehicles.",
    ),
    # -- pairwise risk provoking one vehicle's response --------------------
    GlobalCausalRule(
        name="global_risk_triggers_braking",
        cause_types=_TTC_RISK,
        effect_types=_BRAKE_COMMAND + (EventType.HARD_DECELERATION.value,),
        edge_type=CausalEdgeType.TRIGGERS,
        relation="pair_to_actor",
        prior=0.70,
        max_lag_s=2.5,
        description=(
            "A vehicle that sees the margin collapse brakes. After fusion the "
            "risk may have been measured by the other vehicle in the pair."
        ),
    ),
    GlobalCausalRule(
        name="global_conflict_triggers_evasive_manoeuvre",
        cause_types=_CONFLICT + _LATERAL_REL,
        effect_types=(
            EventType.STEER_ONSET.value,
            EventType.SIGNIFICANT_HEADING_CHANGE.value,
            EventType.LANE_CHANGE_LIKE_MANEUVER.value,
        ),
        edge_type=CausalEdgeType.TRIGGERS,
        relation="pair_to_actor",
        prior=0.45,
        max_lag_s=3.0,
        description="A credible path conflict provokes steering away from it.",
    ),
    # -- outcomes ----------------------------------------------------------
    GlobalCausalRule(
        name="global_critical_ttc_causes_collision",
        cause_types=(EventType.CRITICAL_TTC.value,),
        effect_types=_COLLISION,
        edge_type=CausalEdgeType.CAUSES_OUTCOME,
        relation="same_pair",
        prior=0.90,
        max_lag_s=3.0,
        description="A critical margin that is never recovered ends in contact.",
    ),
    GlobalCausalRule(
        name="global_unmitigated_conflict_causes_collision",
        cause_types=_CONFLICT + (EventType.RAPID_CLOSING.value,),
        effect_types=_COLLISION,
        edge_type=CausalEdgeType.CAUSES_OUTCOME,
        relation="same_pair",
        prior=0.55,
        max_lag_s=4.0,
        description="Converging paths or a fast closure, unresolved, end in contact.",
    ),
    GlobalCausalRule(
        name="global_conflict_causes_near_miss",
        cause_types=_TTC_RISK + _CONFLICT,
        effect_types=_NEAR_MISS,
        edge_type=CausalEdgeType.CAUSES_OUTCOME,
        relation="same_pair",
        prior=0.65,
        max_lag_s=3.0,
        description="The same escalation, resolved without contact, is a near miss.",
    ),
    GlobalCausalRule(
        name="global_braking_prevents_collision",
        cause_types=_BRAKE_COMMAND + (EventType.HARD_DECELERATION.value,),
        effect_types=_NEAR_MISS,
        edge_type=CausalEdgeType.PREVENTS,
        relation="actor_in_pair",
        prior=0.65,
        max_lag_s=3.0,
        description=(
            "Braking hard enough that the encounter ends without contact is "
            "preventive behaviour, and is reported as such rather than as a "
            "contribution to an outcome that did not happen."
        ),
    ),
    GlobalCausalRule(
        name="global_evasive_steering_prevents_collision",
        cause_types=(
            EventType.STEER_ONSET.value,
            EventType.SIGNIFICANT_HEADING_CHANGE.value,
            EventType.LANE_CHANGE_LIKE_MANEUVER.value,
        ),
        effect_types=_NEAR_MISS,
        edge_type=CausalEdgeType.PREVENTS,
        relation="actor_in_pair",
        prior=0.45,
        max_lag_s=3.0,
        description="Steering out of a conflict that then resolves without contact.",
    ),
    # -- mechanics after an impact, including the chain --------------------
    GlobalCausalRule(
        name="global_impact_forces_stop",
        cause_types=_COLLISION,
        effect_types=_POST_IMPACT,
        edge_type=CausalEdgeType.TRIGGERS,
        relation="pair_to_actor",
        prior=0.85,
        max_lag_s=4.0,
        description="An impact brings the vehicles involved to a stop.",
    ),
    GlobalCausalRule(
        name="global_impact_forces_deceleration",
        cause_types=_COLLISION,
        effect_types=(EventType.HARD_DECELERATION.value, EventType.DECELERATION.value),
        edge_type=CausalEdgeType.TRIGGERS,
        relation="pair_to_actor",
        prior=0.85,
        max_lag_s=2.0,
        description="The impact itself decelerates the vehicles that were struck.",
    ),
    GlobalCausalRule(
        name="global_impact_propagates_to_next_impact",
        cause_types=_COLLISION,
        effect_types=_COLLISION,
        edge_type=CausalEdgeType.CONTRIBUTES_TO,
        relation="shared_member",
        prior=0.60,
        max_lag_s=3.0,
        description=(
            "Two impacts that share exactly one vehicle, close together in time, "
            "are a chain: the first changed the shared vehicle's motion and the "
            "second followed. Stated over any three vehicles; no scenario is "
            "named anywhere."
        ),
        require_cross_participant=False,
        require_strict_order=True,
    ),
)


# ---------------------------------------------------------------------------
# The vehicles an event makes a claim about
# ---------------------------------------------------------------------------


def node_subjects(
    node: Event, cfg: Config, participants: Sequence[str]
) -> Tuple[FrozenSet[str], bool, bool]:
    """``(vehicles, relational, resolved)`` for one fused node.

    ``vehicles`` is the set of participants the event makes a claim about: one
    for a unary event, two for a relational one. ``resolved`` is False when the
    node still carries an unresolved local track label instead of a participant
    id -- such a node is excluded from every rule, because a claim about "some
    track" cannot be related to a claim about a named vehicle.
    """
    known = set(participants)
    _family, relational = family_of(node.event_type, cfg)
    observer = str(node.participant_id)
    subject = node.subject

    if subject in (None, "", "self"):
        if relational:
            # A relational event whose counterpart was never named: the pair is
            # unknown, so nothing may be concluded about it.
            return frozenset({observer}), True, False
        return frozenset({observer}), False, observer in known

    subject_s = str(subject)
    if subject_s not in known:
        # Still a raw local track label such as "A::T007".
        return frozenset({observer}), relational, False

    if relational:
        return frozenset({observer, subject_s}), True, observer in known
    # A unary event about another vehicle: the subject is the vehicle described.
    return frozenset({subject_s}), False, True


def _relation_holds(relation: str, cause: FrozenSet[str], effect: FrozenSet[str]) -> bool:
    if relation == "same_actor":
        return len(cause) == 1 and cause == effect
    if relation == "actor_in_pair":
        return len(cause) == 1 and len(effect) == 2 and cause < effect
    if relation == "pair_to_actor":
        return len(cause) == 2 and len(effect) == 1 and effect < cause
    if relation == "same_pair":
        return len(cause) == 2 and cause == effect
    if relation == "shared_member":
        return len(cause) == 2 and len(effect) == 2 and len(cause & effect) == 1
    raise ValueError("unknown relation {0!r}".format(relation))


# ---------------------------------------------------------------------------
# Supporting confidences
# ---------------------------------------------------------------------------


def _identity_confidence(
    node: Event, assignments: Mapping[str, TrackAssignment]
) -> float:
    """How sure the association stage was about the identities this node rests on.

    A fused node that names another vehicle does so because a radar track was
    resolved to it. If that resolution was shaky, every causal claim built on the
    node inherits the doubt; this returns the weakest such confidence, or 1.0 for
    a node that rests only on a vehicle's own telemetry.
    """
    confidences: List[float] = []
    for ev in node.evidence or []:
        if ev.kind != "event":
            continue
        label = str((ev.detail or {}).get("local_subject") or "")
        if not label:
            continue
        assignment = assignments.get(label)
        if assignment is not None:
            confidences.append(float(assignment.confidence))
    if not confidences:
        return 1.0
    return max(0.0, min(1.0, min(confidences)))


def _clock_terms(
    alignment: Optional[Mapping[str, Any]], participants: Iterable[str]
) -> Tuple[float, float]:
    """``(confidence, slack_s)`` of the clock alignment behind a set of vehicles.

    The slack is the alignment's own residual, so a pair of recorders that were
    reconciled badly is given a correspondingly wider temporal tolerance instead
    of a constant fudge factor.
    """
    offsets = dict((alignment or {}).get("offsets") or {})
    confidences: List[float] = []
    residuals: List[float] = []
    for pid in participants:
        block = offsets.get(pid)
        if not isinstance(block, Mapping):
            continue
        try:
            confidences.append(float(block.get("confidence", 1.0)))
        except (TypeError, ValueError):
            pass
        try:
            residual = block.get("residual")
            if residual is not None:
                residuals.append(abs(float(residual)))
        except (TypeError, ValueError):
            pass
    confidence = min(confidences) if confidences else 1.0
    slack = max(residuals) if residuals else 0.0
    return max(0.0, min(1.0, confidence)), max(0.0, slack)


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------


@dataclass
class _NodeFacts:
    """Everything a rule needs to know about one fused node."""

    node: Event
    type_value: str
    vehicles: FrozenSet[str]
    relational: bool
    resolved: bool
    owners: FrozenSet[str]
    identity_confidence: float


def _rule_table(cfg: Config) -> List[GlobalCausalRule]:
    """The active rules, after ``fusion.post_fusion.overrides``.

    Overrides may disable a rule or adjust its prior and lag window; they may not
    invent cause/effect type lists, because that is how a scenario-specific rule
    would sneak in through configuration.
    """
    overrides = cfg.get("fusion.post_fusion.overrides", {}) or {}
    if not isinstance(overrides, Mapping):
        raise TypeError(
            "fusion.post_fusion.overrides must be a mapping rule -> {field: value}"
        )
    known = {rule.name for rule in DEFAULT_GLOBAL_RULES}
    unknown = sorted(set(map(str, overrides.keys())) - known)
    if unknown:
        raise KeyError(
            "fusion.post_fusion.overrides names unknown rule(s): {0}".format(
                ", ".join(unknown)
            )
        )

    active: List[GlobalCausalRule] = []
    for rule in DEFAULT_GLOBAL_RULES:
        patch = overrides.get(rule.name) or {}
        if not isinstance(patch, Mapping):
            raise TypeError(
                "override for rule {0!r} must be a mapping".format(rule.name)
            )
        forbidden = sorted(set(map(str, patch.keys())) - {"enabled", "prior", "max_lag_s"})
        if forbidden:
            raise KeyError(
                "override for rule {0!r} may only set enabled/prior/max_lag_s, "
                "got {1}".format(rule.name, ", ".join(forbidden))
            )
        if not bool(patch.get("enabled", True)):
            continue
        if "prior" in patch or "max_lag_s" in patch:
            rule = GlobalCausalRule(
                name=rule.name,
                cause_types=rule.cause_types,
                effect_types=rule.effect_types,
                edge_type=rule.edge_type,
                relation=rule.relation,
                prior=float(patch.get("prior", rule.prior)),
                max_lag_s=float(patch.get("max_lag_s", rule.max_lag_s)),
                description=rule.description,
                require_cross_participant=rule.require_cross_participant,
                require_strict_order=rule.require_strict_order,
            )
        active.append(rule)
    return active


def infer_global_causal_edges(
    fused: GraphDocument,
    existing_edges: Sequence[GraphEdge],
    assignments: Mapping[str, TrackAssignment],
    alignment: Optional[Mapping[str, Any]],
    cfg: Config,
    participants: Sequence[str],
) -> Tuple[List[GraphEdge], Dict[str, Any]]:
    """Propose the causal edges that only exist once the logs are merged.

    Returns ``(new_edges, diagnostics)``. ``new_edges`` never duplicates an
    ordered pair that ``existing_edges`` already connects in either direction:
    the participants' own claims are authoritative and an inferred edge is only
    ever new structure.
    """
    enabled = bool(cfg.get("fusion.post_fusion.enabled", True))
    diagnostics: Dict[str, Any] = {
        "enabled": enabled,
        "n_candidate_pairs": 0,
        "n_proposed": 0,
        "n_added": 0,
        "rules": {},
        "rejected": [],
        "notes": [],
    }
    if not enabled:
        diagnostics["notes"].append(
            "post-fusion causal reasoning disabled (fusion.post_fusion.enabled=false); "
            "the fused causal graph is the union of the participants' own claims"
        )
        return [], diagnostics
    if fused.graph_kind != "causal":
        diagnostics["notes"].append(
            "post-fusion causal reasoning applies to causal graphs only; "
            "{0!r} left unchanged".format(fused.graph_kind)
        )
        return [], diagnostics

    rules = _rule_table(cfg)
    min_conf = float(cfg.get("fusion.post_fusion.min_edge_confidence", 0.20))
    base_min_lag = float(cfg.get("fusion.post_fusion.min_lag_s", -0.15))
    max_slack = float(cfg.get("fusion.post_fusion.max_clock_slack_s", 0.35))
    node_weight = float(cfg.get("fusion.post_fusion.confidence.node_weight", 0.6))
    tau = float(cfg.get("fusion.post_fusion.confidence.temporal_decay_s", 3.0))
    single_obs = float(
        cfg.get("fusion.post_fusion.confidence.single_observer_factor", 0.85)
    )
    max_new = int(cfg.get("fusion.post_fusion.max_new_edges", 4000))
    if tau <= 0.0:
        raise ValueError("fusion.post_fusion.confidence.temporal_decay_s must be > 0")
    if not 0.0 <= node_weight <= 1.0:
        raise ValueError("fusion.post_fusion.confidence.node_weight must be in [0, 1]")

    known_participants = sorted(set(map(str, participants)))
    facts: Dict[str, _NodeFacts] = {}
    for node in fused.nodes:
        type_value = (
            node.event_type.value
            if isinstance(node.event_type, EventType)
            else str(node.event_type)
        )
        if type_value in FORBIDDEN_CAUSAL_TYPES:
            continue
        vehicles, relational, resolved = node_subjects(node, cfg, known_participants)
        facts[node.event_id] = _NodeFacts(
            node=node,
            type_value=type_value,
            vehicles=vehicles,
            relational=relational,
            resolved=resolved,
            owners=frozenset(node.owners or [node.participant_id]),
            identity_confidence=_identity_confidence(node, assignments),
        )

    # Ordered pairs already claimed by a participant, in either direction: the
    # vehicles' own account is never displaced by an inference.
    claimed = set()
    for edge in existing_edges:
        claimed.add((edge.source, edge.target))
        claimed.add((edge.target, edge.source))

    by_type: Dict[str, List[_NodeFacts]] = {}
    for fact in facts.values():
        by_type.setdefault(fact.type_value, []).append(fact)
    for bucket in by_type.values():
        bucket.sort(key=lambda f: (f.node.t_peak, f.node.event_id))

    proposals: Dict[Tuple[str, str], Tuple[float, GraphEdge, str]] = {}
    rejected: List[Dict[str, Any]] = []

    for rule in rules:
        rule_stats = {"n_pairs": 0, "n_proposed": 0, "n_added": 0}
        diagnostics["rules"][rule.name] = rule_stats
        causes = [f for t in rule.cause_types for f in by_type.get(t, ())]
        effects = [f for t in rule.effect_types for f in by_type.get(t, ())]
        if not causes or not effects:
            continue
        causes.sort(key=lambda f: (f.node.t_peak, f.node.event_id))
        effects.sort(key=lambda f: (f.node.t_peak, f.node.event_id))

        for cause in causes:
            if not cause.resolved:
                continue
            for effect in effects:
                if effect.node.event_id == cause.node.event_id or not effect.resolved:
                    continue
                if not _relation_holds(rule.relation, cause.vehicles, effect.vehicles):
                    continue
                rule_stats["n_pairs"] += 1
                diagnostics["n_candidate_pairs"] += 1

                pair_participants = sorted(cause.vehicles | effect.vehicles)
                clock_confidence, residual = _clock_terms(alignment, pair_participants)
                slack = min(max_slack, residual)
                lag = float(effect.node.t_peak) - float(cause.node.t_peak)
                if lag > rule.max_lag_s or lag < (base_min_lag - slack):
                    continue
                if rule.require_strict_order and lag <= slack:
                    rejected.append(
                        {
                            "reason": "order_not_resolved_beyond_clock_uncertainty",
                            "rule": rule.name,
                            "source": cause.node.event_id,
                            "target": effect.node.event_id,
                            "delta_t_s": round(lag, 6),
                            "clock_slack_s": round(slack, 6),
                            "message": (
                                "the two events are {0:.3f}s apart but the clock "
                                "alignment is only good to {1:.3f}s; their order is "
                                "not established, so no chain is asserted".format(
                                    lag, slack
                                )
                            ),
                        }
                    )
                    continue

                if rule.require_cross_participant:
                    single_owner = (
                        len(cause.owners) == 1
                        and cause.owners == effect.owners
                    )
                    if single_owner:
                        continue

                key = (cause.node.event_id, effect.node.event_id)
                if key in claimed:
                    rejected.append(
                        {
                            "reason": "already_claimed_by_participants",
                            "rule": rule.name,
                            "source": key[0],
                            "target": key[1],
                            "message": (
                                "the participants already relate these two fused "
                                "events; their own claim stands"
                            ),
                        }
                    )
                    continue

                observers = cause.owners | effect.owners
                corroborated = len(observers) > 1
                node_factor = node_weight * 0.5 * (
                    float(cause.node.confidence) + float(effect.node.confidence)
                ) + (1.0 - node_weight)
                temporal_factor = math.exp(-abs(lag) / tau)
                identity_factor = min(
                    cause.identity_confidence, effect.identity_confidence
                )
                support_factor = 1.0 if corroborated else single_obs
                confidence = (
                    float(rule.prior)
                    * node_factor
                    * temporal_factor
                    * identity_factor
                    * clock_confidence
                    * support_factor
                )
                confidence = max(0.0, min(1.0, confidence))
                if confidence < min_conf:
                    continue

                rule_stats["n_proposed"] += 1
                diagnostics["n_proposed"] += 1

                previous = proposals.get(key)
                if previous is not None and previous[0] >= confidence:
                    continue

                edge = _build_edge(
                    rule=rule,
                    cause=cause,
                    effect=effect,
                    lag=lag,
                    confidence=confidence,
                    terms={
                        "rule_prior": round(float(rule.prior), 6),
                        "node_factor": round(node_factor, 6),
                        "temporal_factor": round(temporal_factor, 6),
                        "identity_factor": round(identity_factor, 6),
                        "clock_factor": round(clock_confidence, 6),
                        "support_factor": round(support_factor, 6),
                        "node_weight": node_weight,
                        "temporal_decay_s": tau,
                    },
                    slack=slack,
                    corroborated=corroborated,
                    observers=sorted(observers),
                    pair_participants=pair_participants,
                    cfg=cfg,
                )
                proposals[key] = (confidence, edge, rule.name)

    ordered = sorted(
        proposals.items(),
        key=lambda item: (-item[1][0], item[0][0], item[0][1], item[1][2]),
    )
    if len(ordered) > max_new:
        rejected.append(
            {
                "reason": "max_new_edges",
                "message": (
                    "{0} inferred edge(s) proposed, keeping the {1} strongest "
                    "(fusion.post_fusion.max_new_edges)".format(len(ordered), max_new)
                ),
            }
        )
        ordered = ordered[:max_new]

    new_edges = [edge for _key, (_conf, edge, _rule) in ordered]
    for _key, (_conf, _edge, rule_name) in ordered:
        diagnostics["rules"][rule_name]["n_added"] += 1
    new_edges.sort(key=lambda e: (e.source, e.target, e.edge_type))
    diagnostics["n_added"] = len(new_edges)
    diagnostics["rejected"] = rejected
    diagnostics["parameters"] = {
        "min_edge_confidence": min_conf,
        "min_lag_s": base_min_lag,
        "max_clock_slack_s": max_slack,
        "node_weight": node_weight,
        "temporal_decay_s": tau,
        "single_observer_factor": single_obs,
        "max_new_edges": max_new,
        "n_rules_active": len(rules),
    }
    return new_edges, diagnostics


def _interval(node: Event) -> Interval:
    """The closed interval a fused event occupies on the common clock."""
    start = min(float(node.t_start), float(node.t_peak))
    end = max(float(node.t_end if node.t_end is not None else node.t_peak), float(node.t_peak))
    return Interval(start=start, end=end)


def _build_edge(
    rule: GlobalCausalRule,
    cause: _NodeFacts,
    effect: _NodeFacts,
    lag: float,
    confidence: float,
    terms: Mapping[str, float],
    slack: float,
    corroborated: bool,
    observers: Sequence[str],
    pair_participants: Sequence[str],
    cfg: Config,
) -> GraphEdge:
    """One inferred edge, carrying everything needed to audit it."""
    tolerance = float(cfg.get("simulation.fixed_delta_seconds", 0.05))
    relation = temporal_relation(
        _interval(cause.node), _interval(effect.node), tol=tolerance
    )
    evidence = [
        Evidence(
            kind="event",
            ref=cause.node.event_id,
            t_start=float(cause.node.t_start),
            t_end=float(cause.node.t_end) if cause.node.t_end is not None else None,
            detail={
                "part": "cause",
                "event_type": cause.type_value,
                "vehicles": sorted(cause.vehicles),
                "owners": sorted(cause.owners),
                "time_domain": "common",
            },
        ),
        Evidence(
            kind="event",
            ref=effect.node.event_id,
            t_start=float(effect.node.t_start),
            t_end=float(effect.node.t_end) if effect.node.t_end is not None else None,
            detail={
                "part": "effect",
                "event_type": effect.type_value,
                "vehicles": sorted(effect.vehicles),
                "owners": sorted(effect.owners),
                "time_domain": "common",
            },
        ),
    ]
    return GraphEdge(
        source=cause.node.event_id,
        target=effect.node.event_id,
        edge_type=rule.edge_type.value,
        confidence=round(float(confidence), 6),
        provenance=Provenance.FUSED,
        rule=rule.name,
        temporal_relation=relation,
        evidence=evidence,
        owners=sorted(observers),
        merged_from=[],
        detail={
            "origin": ORIGIN_INFERRED,
            "rule": rule.name,
            "rule_description": rule.description,
            "relation": rule.relation,
            "cause_vehicles": sorted(cause.vehicles),
            "effect_vehicles": sorted(effect.vehicles),
            "subject_participants": list(pair_participants),
            "cross_participant": bool(corroborated),
            "supporting_events": [cause.node.event_id, effect.node.event_id],
            "supporting_participants": list(observers),
            "n_independent_observers": len(observers),
            "time_domain": "common",
            "source_t_common": round(float(cause.node.t_peak), 6),
            "target_t_common": round(float(effect.node.t_peak), 6),
            "delta_t_s": round(float(lag), 6),
            "max_lag_s": float(rule.max_lag_s),
            "clock_slack_s": round(float(slack), 6),
            "confidence_terms": dict(terms),
        },
    )
