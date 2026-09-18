"""The inspectable causal rule table used by the local causal-DAG builder.

Why a rule table at all
-----------------------
The scientific claim of this project is that a causal reconstruction produced
onboard a single vehicle can be *audited*. An opaque scoring function would make
that impossible, so every causal hypothesis this pipeline is allowed to state is
declared here, in one table, as a :class:`CausalRule`: which event types may act
as a cause, which may act as an effect, what kind of causal claim the edge
encodes, how strong the prior on that claim is, how long the cause may precede
the effect, and -- in prose -- *why* the relation is physically plausible. A
reviewer can read this module and know exactly which edges the system is capable
of drawing, before looking at a single run.

Two invariants keep the table honest
------------------------------------
1. **Rules are generic over event types.** Nothing here (or anywhere downstream)
   may be keyed on a scenario id, a participant id or a track id. The same table
   is applied to every run; scenario-specific behaviour would make the evaluation
   circular.
2. **An observation is not a cause.** ``RADAR_TRACK_APPEARED`` and
   ``RADAR_TRACK_LOST`` record when our own sensor started or stopped seeing an
   object. They are facts about the *observer*, not about the world, so they may
   never appear on either side of a causal edge; they carry the ``OBSERVED_FROM``
   relation in the event graph instead. :func:`validate_rules` enforces this.

Tuning
------
Each field of each rule is overridable from configuration under
``causal_rules.overrides.<rule name>.<field>`` (see :func:`load_rules`), so the
literal numbers below are *documented defaults*, not hidden magic: they can be
changed without touching code, and the table actually used by a run is recorded
in the produced graph's ``meta``.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import CausalEdgeType, EventType, OUTCOME_EVENT_TYPES

__all__ = [
    "CausalRule",
    "DEFAULT_RULES",
    "OWN_BEHAVIOUR_EVENT_TYPES",
    "INTERACTION_EVENT_TYPES",
    "OBSERVATION_EVENT_TYPES",
    "ROAD_CONTROL_EVENT_TYPES",
    "NON_ACTION_EVENT_TYPES",
    "SUBJECT_FREE_EVENT_TYPES",
    "OVERRIDABLE_FIELDS",
    "load_rules",
    "validate_rules",
    "rule_by_name",
]


# ---------------------------------------------------------------------------
# Event-type taxonomy groups used by the rule table and its validator
# ---------------------------------------------------------------------------

#: Events derived from a participant's *own* telemetry and controls. They
#: describe what this vehicle did, so they never carry a radar track subject.
OWN_BEHAVIOUR_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.VEHICLE_STARTED,
    EventType.ACCELERATION,
    EventType.DECELERATION,
    EventType.HARD_DECELERATION,
    EventType.BRAKE_ONSET,
    EventType.HARD_BRAKE,
    EventType.THROTTLE_ONSET,
    EventType.STEER_ONSET,
    EventType.SIGNIFICANT_HEADING_CHANGE,
    EventType.LANE_CHANGE_LIKE_MANEUVER,
    EventType.FULL_STOP,
)

#: What this vehicle saw of the road: signs from its camera, marking crossings
#: from its lane sensor. Own-vehicle events too -- the other party is the road
#: rather than a tracked object -- so they carry no subject either.
ROAD_CONTROL_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.STOP_SIGN_DETECTED,
    EventType.YIELD_SIGN_DETECTED,
    EventType.STOP_LINE_DETECTED,
    EventType.STOP_LINE_CROSSED,
    EventType.LANE_MARKING_CROSSED,
    EventType.SOLID_LINE_CROSSED,
    EventType.ROAD_BOUNDARY_CROSSED,
)

#: Derived assertions that a required response was absent. Most carry the
#: subject they failed to respond to, so they are not subject-free; the two
#: arising from traffic control rather than from another vehicle do not, which
#: is why the group is listed separately from either side.
NON_ACTION_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.NO_STOP_AFTER_STOP_SIGN,
    EventType.NO_BRAKING_RESPONSE,
    EventType.NO_YIELD_RESPONSE,
    EventType.NO_EVASIVE_RESPONSE,
    EventType.CONFLICT_ENTRY_WITHOUT_DECELERATION,
    EventType.CONTINUED_ACCELERATION_DURING_CONFLICT,
)

#: Events derived from a participant's own radar tracks. Each concerns one
#: locally tracked object and therefore always carries a ``subject`` track id.
INTERACTION_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.RANGE_DECREASING,
    EventType.RAPID_CLOSING,
    EventType.LOW_TTC,
    EventType.CRITICAL_TTC,
    EventType.LATERAL_CROSSING,
    EventType.CUT_IN_LIKE_MOTION,
    EventType.PREDICTED_PATH_CONFLICT,
    EventType.CONFLICT_REGION_ENTRY,
    EventType.TARGET_DECELERATION,
)

#: Purely observational events: they say when our sensor acquired or dropped a
#: track, which is a property of the sensing process rather than of the world.
#: Banned from the causal table (see the module docstring).
OBSERVATION_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.RADAR_TRACK_APPEARED,
    EventType.RADAR_TRACK_LOST,
)

#: Event types that describe the ego vehicle itself and therefore have no radar
#: track subject: its own behaviour plus the terminal outcome events. Used to
#: validate ``require_self_effect`` rules.
SUBJECT_FREE_EVENT_TYPES: Tuple[EventType, ...] = tuple(
    list(OWN_BEHAVIOUR_EVENT_TYPES) + list(ROAD_CONTROL_EVENT_TYPES)
    + list(OUTCOME_EVENT_TYPES)
)

#: Per-rule fields that ``causal_rules.overrides.<name>`` may set. Cause/effect
#: type lists are deliberately *not* overridable: changing which event types a
#: rule relates changes the scientific claim and belongs in code review, not in
#: a configuration file.
OVERRIDABLE_FIELDS: Tuple[str, ...] = (
    "enabled",
    "prior",
    "max_lag_s",
    "edge_type",
    "require_same_subject",
    "require_self_effect",
)


# ---------------------------------------------------------------------------
# Rule record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CausalRule:
    """One declarative causal hypothesis template.

    Frozen because the table is a constant registry: :func:`load_rules` produces
    *new* rules via :func:`dataclasses.replace` when configuration overrides a
    field, so a mutated global can never leak between runs.

    Attributes
    ----------
    name:
        Stable identifier. It is written onto every edge the rule produces
        (``GraphEdge.rule``) and is the key under which configuration overrides
        are looked up, so renaming one is a breaking change.
    cause_types / effect_types:
        The rule fires for every ordered pair of events whose types fall in these
        sets and whose timing and subject constraints hold.
    edge_type:
        A :class:`~cdf.common.schemas.CausalEdgeType` *value*. ``CAUSES_OUTCOME``
        is reserved, by convention, for edges whose effect is the forensic
        outcome itself (``COLLISION`` / ``NEAR_MISS``); ``PREVENTS`` states that
        the cause is what stopped a worse outcome from materialising.
    prior:
        Strength of the rule in ``[0, 1]`` before any evidence is considered. It
        is a *modelling assumption*, not a measured probability.
    max_lag_s:
        Longest cause->effect delay the rule accepts. Short for mechanical
        couplings (a brake command decelerating the vehicle), longer for
        developing traffic conflicts.
    require_same_subject:
        Both events must concern the *same* local radar track. Used for chains
        that describe one object's behaviour; meaningless (and therefore false)
        when the effect is the ego vehicle's own reaction.
    require_self_effect:
        The effect must be an own-behaviour event, i.e. one with no radar track
        subject. Used for perception->reaction rules, where the effect is
        something *we* did.
    description:
        Why the relation is physically plausible. Read by humans auditing the
        produced graph; also copied into the graph ``meta``.
    """

    name: str
    cause_types: Tuple[EventType, ...]
    effect_types: Tuple[EventType, ...]
    edge_type: str
    prior: float
    max_lag_s: float
    require_same_subject: bool
    require_self_effect: bool
    description: str

    def matches_cause(self, event_type: EventType) -> bool:
        """Whether ``event_type`` may act as this rule's cause."""
        return event_type in self.cause_types

    def matches_effect(self, event_type: EventType) -> bool:
        """Whether ``event_type`` may act as this rule's effect."""
        return event_type in self.effect_types


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------

_TRIGGERS = CausalEdgeType.TRIGGERS.value
_CONTRIBUTES_TO = CausalEdgeType.CONTRIBUTES_TO.value
_INCREASES_RISK_OF = CausalEdgeType.INCREASES_RISK_OF.value
_PREVENTS = CausalEdgeType.PREVENTS.value
_CAUSES_OUTCOME = CausalEdgeType.CAUSES_OUTCOME.value


DEFAULT_RULES: Tuple[CausalRule, ...] = (
    # -- how a conflict develops around one tracked object --------------------
    CausalRule(
        name="target_deceleration_closes_gap",
        cause_types=(EventType.TARGET_DECELERATION,),
        effect_types=(EventType.RANGE_DECREASING, EventType.RAPID_CLOSING),
        edge_type=_TRIGGERS,
        prior=0.80,
        max_lag_s=2.5,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "A tracked object slowing down while we hold speed mechanically "
            "shortens the gap: the observed range starts falling and the "
            "range-rate turns strongly negative."
        ),
    ),
    CausalRule(
        name="closing_range_increases_ttc_risk",
        cause_types=(EventType.RANGE_DECREASING,),
        effect_types=(EventType.LOW_TTC,),
        edge_type=_INCREASES_RISK_OF,
        prior=0.50,
        max_lag_s=4.0,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "A steadily shrinking range does not by itself imply an imminent "
            "impact -- the closure may be slow -- but it is the precondition "
            "under which a low time-to-collision can arise, so the relation is "
            "risk-raising rather than triggering."
        ),
    ),
    CausalRule(
        name="rapid_closing_shortens_ttc",
        cause_types=(EventType.RAPID_CLOSING,),
        effect_types=(EventType.LOW_TTC,),
        edge_type=_CONTRIBUTES_TO,
        prior=0.75,
        max_lag_s=3.0,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "Time-to-collision is range divided by closing speed, so a high "
            "closing speed on a track is a direct numerical contributor to that "
            "same track's TTC falling below the warning threshold."
        ),
    ),
    CausalRule(
        name="ttc_escalates_to_critical",
        cause_types=(EventType.LOW_TTC, EventType.RAPID_CLOSING),
        effect_types=(EventType.CRITICAL_TTC,),
        edge_type=_CONTRIBUTES_TO,
        prior=0.80,
        max_lag_s=3.0,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "Without an intervening correction, an already-low TTC on a track "
            "keeps decreasing into the critical band; the earlier threshold "
            "crossing is the same physical process one stage earlier."
        ),
    ),
    CausalRule(
        name="cut_in_closes_gap",
        cause_types=(EventType.CUT_IN_LIKE_MOTION,),
        effect_types=(
            EventType.RANGE_DECREASING,
            EventType.RAPID_CLOSING,
            EventType.LOW_TTC,
        ),
        edge_type=_TRIGGERS,
        prior=0.75,
        max_lag_s=2.5,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "An object moving laterally into our path takes over the headway we "
            "had reserved for empty road, which abruptly converts lateral "
            "separation into longitudinal closure on that track."
        ),
    ),
    CausalRule(
        name="lateral_crossing_predicts_conflict",
        cause_types=(EventType.LATERAL_CROSSING,),
        effect_types=(EventType.PREDICTED_PATH_CONFLICT,),
        edge_type=_CONTRIBUTES_TO,
        prior=0.60,
        max_lag_s=3.0,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "Sustained lateral motion across our heading is what makes the "
            "constant-velocity extrapolation of the two paths intersect; the "
            "predicted conflict is that observation carried forward in time."
        ),
    ),
    CausalRule(
        name="predicted_conflict_becomes_region_entry",
        cause_types=(EventType.PREDICTED_PATH_CONFLICT, EventType.LATERAL_CROSSING),
        effect_types=(EventType.CONFLICT_REGION_ENTRY,),
        edge_type=_TRIGGERS,
        prior=0.70,
        max_lag_s=4.0,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "A predicted crossing point that neither party alters is reached: "
            "entry into the inferred conflict region is the prediction coming "
            "true for that same track."
        ),
    ),
    CausalRule(
        name="conflict_region_entry_shortens_ttc",
        cause_types=(EventType.CONFLICT_REGION_ENTRY,),
        effect_types=(EventType.LOW_TTC, EventType.CRITICAL_TTC),
        edge_type=_CONTRIBUTES_TO,
        prior=0.70,
        max_lag_s=3.0,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "Once both parties occupy the same small region the remaining "
            "separation is metres rather than tens of metres, which is exactly "
            "the condition under which TTC collapses."
        ),
    ),
    CausalRule(
        name="predicted_conflict_increases_ttc_risk",
        cause_types=(EventType.PREDICTED_PATH_CONFLICT,),
        effect_types=(EventType.LOW_TTC,),
        edge_type=_INCREASES_RISK_OF,
        prior=0.55,
        max_lag_s=4.0,
        require_same_subject=True,
        require_self_effect=False,
        description=(
            "A path conflict predicted from extrapolated motion raises the "
            "probability of a low-TTC encounter with that track, but the "
            "prediction can be falsified by either party, so the claim is "
            "risk-raising rather than deterministic."
        ),
    ),
    # -- how the ego vehicle reacts to what it perceives -----------------------
    CausalRule(
        name="critical_ttc_triggers_hard_braking",
        cause_types=(EventType.CRITICAL_TTC,),
        effect_types=(EventType.HARD_BRAKE, EventType.HARD_DECELERATION),
        edge_type=_TRIGGERS,
        prior=0.85,
        max_lag_s=2.0,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "A critical time-to-collision is the canonical stimulus for an "
            "emergency stop, whether commanded by a driver model or an "
            "autonomous-emergency-braking function. The subjects need not match "
            "because the ego brakes once, for whichever threat is worst."
        ),
    ),
    CausalRule(
        name="low_ttc_triggers_braking",
        cause_types=(EventType.LOW_TTC,),
        effect_types=(EventType.BRAKE_ONSET, EventType.DECELERATION),
        edge_type=_TRIGGERS,
        prior=0.60,
        max_lag_s=2.5,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "A TTC below the comfort threshold typically produces ordinary "
            "service braking rather than an emergency stop; the weaker prior "
            "reflects that the driver may instead simply lift off."
        ),
    ),
    CausalRule(
        name="rapid_closing_triggers_braking",
        cause_types=(EventType.RAPID_CLOSING,),
        effect_types=(EventType.BRAKE_ONSET, EventType.HARD_BRAKE),
        edge_type=_TRIGGERS,
        prior=0.55,
        max_lag_s=2.5,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "Fast closure is perceptible before any TTC threshold is crossed "
            "(looming), so it can explain a brake application that precedes the "
            "TTC events."
        ),
    ),
    CausalRule(
        name="lateral_threat_triggers_evasive_steering",
        cause_types=(
            EventType.CUT_IN_LIKE_MOTION,
            EventType.LATERAL_CROSSING,
            EventType.PREDICTED_PATH_CONFLICT,
            EventType.CONFLICT_REGION_ENTRY,
        ),
        effect_types=(
            EventType.STEER_ONSET,
            EventType.SIGNIFICANT_HEADING_CHANGE,
            EventType.LANE_CHANGE_LIKE_MANEUVER,
        ),
        edge_type=_TRIGGERS,
        prior=0.50,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "A threat that is lateral rather than straight ahead is commonly "
            "answered by steering away from it; the modest prior reflects that "
            "braking is the more frequent response."
        ),
    ),
    # -- own actuation -> own motion (mechanical, short lag) -------------------
    CausalRule(
        name="brake_command_decelerates_vehicle",
        cause_types=(EventType.BRAKE_ONSET, EventType.HARD_BRAKE),
        effect_types=(EventType.DECELERATION, EventType.HARD_DECELERATION),
        edge_type=_CONTRIBUTES_TO,
        prior=0.85,
        max_lag_s=1.5,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "The brake command is the actuation and the measured longitudinal "
            "deceleration is its mechanical consequence, delayed only by "
            "hydraulic build-up and tyre response."
        ),
    ),
    CausalRule(
        name="throttle_command_accelerates_vehicle",
        cause_types=(EventType.THROTTLE_ONSET,),
        effect_types=(EventType.ACCELERATION, EventType.VEHICLE_STARTED),
        edge_type=_CONTRIBUTES_TO,
        prior=0.85,
        max_lag_s=2.0,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "Symmetrically to braking: applying throttle is what makes our own "
            "speed rise, and is what moves a standing vehicle off."
        ),
    ),
    # -- own behaviour raising the risk we then observe ------------------------
    CausalRule(
        name="own_acceleration_closes_gap",
        cause_types=(EventType.ACCELERATION, EventType.VEHICLE_STARTED),
        effect_types=(
            EventType.RANGE_DECREASING,
            EventType.RAPID_CLOSING,
            EventType.LOW_TTC,
        ),
        edge_type=_INCREASES_RISK_OF,
        prior=0.40,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Closure is relative: our own acceleration shortens the gap to "
            "anything ahead just as the target's braking does. Stating it keeps "
            "the reconstruction symmetric instead of always blaming the other "
            "party."
        ),
    ),
    CausalRule(
        name="own_lateral_manoeuvre_creates_conflict",
        cause_types=(
            EventType.STEER_ONSET,
            EventType.SIGNIFICANT_HEADING_CHANGE,
            EventType.LANE_CHANGE_LIKE_MANEUVER,
        ),
        effect_types=(
            EventType.PREDICTED_PATH_CONFLICT,
            EventType.CONFLICT_REGION_ENTRY,
            EventType.LATERAL_CROSSING,
        ),
        edge_type=_INCREASES_RISK_OF,
        prior=0.40,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Our own steering changes our predicted path, so a conflict that "
            "appears just afterwards may have been created by us rather than by "
            "the other party. This rule is the deliberate mirror image of "
            "'lateral_threat_triggers_evasive_steering'; which of the two "
            "survives in a given run is decided by the observed ordering, and "
            "by cycle rejection when the ordering is ambiguous."
        ),
    ),
    # -- outcomes -------------------------------------------------------------
    CausalRule(
        name="critical_ttc_causes_collision",
        cause_types=(EventType.CRITICAL_TTC,),
        effect_types=(EventType.COLLISION,),
        edge_type=_CAUSES_OUTCOME,
        prior=0.90,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "A time-to-collision inside the critical band that is followed by an "
            "impact is the strongest onboard explanation of that impact: the "
            "collision is the TTC running out."
        ),
    ),
    CausalRule(
        name="unmitigated_conflict_causes_collision",
        cause_types=(
            EventType.RAPID_CLOSING,
            EventType.CONFLICT_REGION_ENTRY,
            EventType.CUT_IN_LIKE_MOTION,
        ),
        effect_types=(EventType.COLLISION,),
        edge_type=_CAUSES_OUTCOME,
        prior=0.50,
        max_lag_s=4.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Fallback explanation for impacts the TTC estimator never flagged -- "
            "a short-range cut-in or an intersection conflict can produce a "
            "collision before any TTC sample is confirmed."
        ),
    ),
    CausalRule(
        name="conflict_causes_near_miss",
        cause_types=(
            EventType.CRITICAL_TTC,
            EventType.LOW_TTC,
            EventType.CONFLICT_REGION_ENTRY,
        ),
        effect_types=(EventType.NEAR_MISS,),
        edge_type=_CAUSES_OUTCOME,
        prior=0.65,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "A near miss is a conflict that materialised without contact; the "
            "conflict indicators are what make the encounter a near miss rather "
            "than ordinary traffic."
        ),
    ),
    CausalRule(
        name="braking_prevents_collision",
        cause_types=(
            EventType.HARD_BRAKE,
            EventType.HARD_DECELERATION,
            EventType.BRAKE_ONSET,
        ),
        effect_types=(EventType.NEAR_MISS,),
        edge_type=_PREVENTS,
        prior=0.70,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "A near miss is a collision that did not happen. When our own "
            "braking precedes it, the braking is the averting action -- hence "
            "PREVENTS rather than CAUSES_OUTCOME: the edge claims the cause "
            "removed a worse outcome, not that it produced this one."
        ),
    ),
    CausalRule(
        name="steering_prevents_collision",
        cause_types=(
            EventType.STEER_ONSET,
            EventType.SIGNIFICANT_HEADING_CHANGE,
            EventType.LANE_CHANGE_LIKE_MANEUVER,
        ),
        effect_types=(EventType.NEAR_MISS,),
        edge_type=_PREVENTS,
        prior=0.45,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "The evasive-steering counterpart of 'braking_prevents_collision'; "
            "weaker because a steering input close to an encounter is also "
            "consistent with ordinary path following."
        ),
    ),
    CausalRule(
        name="collision_forces_stop",
        cause_types=(EventType.COLLISION,),
        effect_types=(EventType.POST_IMPACT_STOP, EventType.HARD_DECELERATION),
        edge_type=_TRIGGERS,
        prior=0.85,
        max_lag_s=4.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "The impact itself, plus the post-impact braking it provokes, is "
            "what brings the vehicle to rest. TRIGGERS rather than "
            "CAUSES_OUTCOME because the standstill is a consequence of the "
            "outcome, not the forensic outcome under investigation."
        ),
    ),
    # -- coming to rest -------------------------------------------------------
    CausalRule(
        name="braking_brings_vehicle_to_rest",
        cause_types=(
            EventType.BRAKE_ONSET, EventType.HARD_BRAKE,
            EventType.DECELERATION, EventType.HARD_DECELERATION,
        ),
        effect_types=(EventType.FULL_STOP,),
        edge_type=_TRIGGERS,
        prior=0.85,
        max_lag_s=6.0,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "Sustained braking ends in a standstill. The lag is generous "
            "because how long it takes depends on the speed the braking began "
            "at, which the rule does not know."
        ),
    ),
    # -- traffic control, as seen rather than as known ------------------------
    CausalRule(
        name="traffic_control_prompts_slowing",
        cause_types=(
            EventType.STOP_SIGN_DETECTED, EventType.YIELD_SIGN_DETECTED,
            EventType.STOP_LINE_DETECTED,
        ),
        effect_types=(
            EventType.BRAKE_ONSET, EventType.DECELERATION,
            EventType.HARD_DECELERATION, EventType.FULL_STOP,
        ),
        edge_type=_TRIGGERS,
        prior=0.60,
        max_lag_s=8.0,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "Seeing a sign or a stop line is what prompts a driver to slow. A "
            "perception-to-reaction coupling, so the effect must be the "
            "vehicle's own behaviour; the prior is moderate because plenty of "
            "braking has nothing to do with a sign."
        ),
    ),
    CausalRule(
        name="crossing_a_stop_line_enters_the_conflict",
        cause_types=(EventType.STOP_LINE_CROSSED,),
        effect_types=(
            EventType.CONFLICT_REGION_ENTRY, EventType.PREDICTED_PATH_CONFLICT,
        ),
        edge_type=_CONTRIBUTES_TO,
        prior=0.70,
        max_lag_s=5.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "A stop line marks the boundary of the area where paths meet, so "
            "crossing it is how a vehicle comes to be in a conflict. "
            "Geometrically true regardless of whether crossing it was allowed, "
            "which is a separate question for the responsibility layer."
        ),
    ),
    # -- steering and road markings ------------------------------------------
    CausalRule(
        name="steering_crosses_a_marking",
        cause_types=(
            EventType.STEER_ONSET, EventType.SIGNIFICANT_HEADING_CHANGE,
            EventType.LANE_CHANGE_LIKE_MANEUVER,
        ),
        effect_types=(
            EventType.LANE_MARKING_CROSSED, EventType.SOLID_LINE_CROSSED,
            EventType.ROAD_BOUNDARY_CROSSED,
        ),
        edge_type=_TRIGGERS,
        prior=0.80,
        max_lag_s=3.0,
        require_same_subject=False,
        require_self_effect=True,
        description=(
            "Lateral movement is what takes a vehicle across a line. The "
            "mechanical direction of the coupling: the steering comes first and "
            "the crossing follows from it."
        ),
    ),
    CausalRule(
        name="leaving_the_lane_creates_a_path_conflict",
        cause_types=(
            EventType.LANE_MARKING_CROSSED, EventType.SOLID_LINE_CROSSED,
            EventType.ROAD_BOUNDARY_CROSSED,
        ),
        effect_types=(
            EventType.CUT_IN_LIKE_MOTION, EventType.PREDICTED_PATH_CONFLICT,
            EventType.CONFLICT_REGION_ENTRY,
        ),
        edge_type=_INCREASES_RISK_OF,
        prior=0.55,
        max_lag_s=4.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Crossing into another lane puts a vehicle where other traffic is "
            "entitled to be. Risk-raising rather than triggering: most lane "
            "changes conflict with nothing, and whether this one did depends on "
            "what was there."
        ),
    ),
    # -- non-actions ----------------------------------------------------------
    CausalRule(
        name="undischarged_obligation_puts_vehicle_in_conflict",
        cause_types=(
            EventType.NO_STOP_AFTER_STOP_SIGN, EventType.NO_YIELD_RESPONSE,
        ),
        effect_types=(
            EventType.CONFLICT_REGION_ENTRY, EventType.PREDICTED_PATH_CONFLICT,
            EventType.LOW_TTC, EventType.CRITICAL_TTC,
        ),
        edge_type=_CONTRIBUTES_TO,
        prior=0.70,
        max_lag_s=6.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Not stopping where stopping was required is what leaves a vehicle "
            "moving into the area where paths cross. The edge states a physical "
            "consequence of the absent deceleration; whether the obligation was "
            "binding is not asserted here."
        ),
    ),
    CausalRule(
        name="unresponsiveness_lets_the_conflict_run_out",
        cause_types=(
            EventType.NO_BRAKING_RESPONSE, EventType.NO_EVASIVE_RESPONSE,
        ),
        effect_types=(EventType.COLLISION,),
        edge_type=_CAUSES_OUTCOME,
        prior=0.75,
        max_lag_s=4.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Once a time-to-collision is critical, an impact follows unless "
            "something changes. The absence of any response is therefore part "
            "of the explanation of the impact rather than merely coincident "
            "with it -- which is exactly the claim a non-action node makes, and "
            "why it is only emitted where the interval was really watched."
        ),
    ),
    CausalRule(
        name="pressing_on_into_a_conflict_raises_the_risk",
        cause_types=(
            EventType.CONFLICT_ENTRY_WITHOUT_DECELERATION,
            EventType.CONTINUED_ACCELERATION_DURING_CONFLICT,
        ),
        effect_types=(
            EventType.LOW_TTC, EventType.CRITICAL_TTC, EventType.COLLISION,
        ),
        edge_type=_INCREASES_RISK_OF,
        prior=0.65,
        max_lag_s=4.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Arriving at a conflict without having slowed, or accelerating once "
            "inside one, leaves less time and more energy for whatever follows. "
            "Risk-raising rather than causing: it worsens the situation without "
            "being sufficient for an impact on its own."
        ),
    ),
    CausalRule(
        name="stopping_prevents_the_collision",
        cause_types=(EventType.FULL_STOP,),
        effect_types=(EventType.NEAR_MISS,),
        edge_type=_PREVENTS,
        prior=0.70,
        max_lag_s=6.0,
        require_same_subject=False,
        require_self_effect=False,
        description=(
            "Coming to a complete stop and then having a near miss rather than "
            "an impact is the clearest case of a behaviour acting against the "
            "outcome. PREVENTS, in the same sense as the braking and steering "
            "rules: it worked against what was developing."
        ),
    ),
)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_rules(rules: Sequence[CausalRule]) -> None:
    """Raise :class:`ValueError` if a rule table violates the table invariants.

    Run on :data:`DEFAULT_RULES` at import time and again on every table produced
    by :func:`load_rules`, so a bad override fails at construction time rather
    than producing a subtly wrong graph.
    """
    seen: Dict[str, int] = {}
    for index, rule in enumerate(rules):
        where = "rule {0!r} (#{1})".format(rule.name, index)
        if not rule.name:
            raise ValueError("{0}: rule name must not be empty".format(where))
        if rule.name in seen:
            raise ValueError(
                "duplicate rule name {0!r} (positions {1} and {2}); rule names are "
                "the key for configuration overrides and must be unique".format(
                    rule.name, seen[rule.name], index
                )
            )
        seen[rule.name] = index

        if not rule.cause_types:
            raise ValueError("{0}: cause_types must not be empty".format(where))
        if not rule.effect_types:
            raise ValueError("{0}: effect_types must not be empty".format(where))

        valid_edge_types = tuple(e.value for e in CausalEdgeType)
        if rule.edge_type not in valid_edge_types:
            raise ValueError(
                "{0}: edge_type {1!r} is not a CausalEdgeType value (expected one "
                "of {2})".format(where, rule.edge_type, ", ".join(valid_edge_types))
            )
        if not 0.0 < float(rule.prior) <= 1.0:
            raise ValueError(
                "{0}: prior must lie in (0, 1], got {1!r}".format(where, rule.prior)
            )
        if float(rule.max_lag_s) <= 0.0:
            raise ValueError(
                "{0}: max_lag_s must be positive, got {1!r}".format(where, rule.max_lag_s)
            )
        if not rule.description.strip():
            raise ValueError(
                "{0}: description must explain why the relation is plausible".format(where)
            )

        for event_type in tuple(rule.cause_types) + tuple(rule.effect_types):
            if not isinstance(event_type, EventType):
                raise ValueError(
                    "{0}: {1!r} is not an EventType member".format(where, event_type)
                )
            if event_type in OBSERVATION_EVENT_TYPES:
                raise ValueError(
                    "{0}: {1} is an observation event and may never take part in a "
                    "causal edge; observation relations belong in the event graph "
                    "(OBSERVED_FROM)".format(where, event_type.value)
                )

        overlap = set(rule.cause_types) & set(rule.effect_types)
        if overlap:
            raise ValueError(
                "{0}: event type(s) {1} appear as both cause and effect, which "
                "would let the rule build a cycle out of a single event "
                "type".format(where, sorted(t.value for t in overlap))
            )

        if rule.require_self_effect:
            bad = [
                t.value for t in rule.effect_types if t not in SUBJECT_FREE_EVENT_TYPES
            ]
            if bad:
                raise ValueError(
                    "{0}: require_self_effect is set but effect type(s) {1} concern a "
                    "tracked object and therefore always carry a subject".format(
                        where, sorted(bad)
                    )
                )
        if rule.require_same_subject:
            bad_pair = [
                t.value
                for t in tuple(rule.cause_types) + tuple(rule.effect_types)
                if t not in INTERACTION_EVENT_TYPES
            ]
            if bad_pair:
                raise ValueError(
                    "{0}: require_same_subject is set but type(s) {1} are not "
                    "track-scoped, so the constraint could never be "
                    "satisfied".format(where, sorted(bad_pair))
                )
        if rule.require_same_subject and rule.require_self_effect:
            raise ValueError(
                "{0}: require_same_subject and require_self_effect are mutually "
                "exclusive (an own-behaviour effect has no track subject to "
                "match)".format(where)
            )


validate_rules(DEFAULT_RULES)


def rule_by_name(rules: Sequence[CausalRule], name: str) -> CausalRule:
    """Look up one rule by name, failing loudly when it is absent."""
    for rule in rules:
        if rule.name == name:
            return rule
    raise KeyError(
        "no causal rule named {0!r} (known: {1})".format(
            name, ", ".join(sorted(r.name for r in rules))
        )
    )


# ---------------------------------------------------------------------------
# Configuration binding
# ---------------------------------------------------------------------------


def load_rules(cfg: Config) -> List[CausalRule]:
    """Return :data:`DEFAULT_RULES` with configuration overrides applied.

    Two configuration mechanisms act on the table:

    * ``causal_rules.default_max_lag_s`` is a *global ceiling*. A rule whose
      declared window is longer is clipped to it, so one configuration value can
      tighten the whole table; rules that already declare a shorter, mechanically
      motivated window keep it.
    * ``causal_rules.overrides.<rule name>.<field>`` adjusts a single rule. The
      fields in :data:`OVERRIDABLE_FIELDS` may be set; ``enabled: false`` removes
      the rule entirely. An explicit ``max_lag_s`` override is honoured as given
      and is *not* clipped by the ceiling -- otherwise asking for a longer window
      would silently do nothing.

    Unknown rule names and unknown field names raise, because a silently ignored
    override would make a published configuration a lie about what was run.
    """
    ceiling = _positive_float(
        cfg.get("causal_rules.default_max_lag_s", 4.0), "causal_rules.default_max_lag_s"
    )
    raw_overrides = cfg.get("causal_rules.overrides", {}) or {}
    if not isinstance(raw_overrides, Mapping):
        raise TypeError(
            "causal_rules.overrides must be a mapping of rule name -> settings, "
            "got {0!r}".format(type(raw_overrides).__name__)
        )

    known_names = set(r.name for r in DEFAULT_RULES)
    unknown = sorted(set(str(k) for k in raw_overrides.keys()) - known_names)
    if unknown:
        raise KeyError(
            "causal_rules.overrides names {0} which are not rules in DEFAULT_RULES "
            "(known: {1})".format(unknown, ", ".join(sorted(known_names)))
        )

    out: List[CausalRule] = []
    for rule in DEFAULT_RULES:
        override = raw_overrides.get(rule.name, {}) or {}
        if not isinstance(override, Mapping):
            raise TypeError(
                "causal_rules.overrides.{0} must be a mapping, got {1!r}".format(
                    rule.name, type(override).__name__
                )
            )
        bad_fields = sorted(set(str(k) for k in override.keys()) - set(OVERRIDABLE_FIELDS))
        if bad_fields:
            raise KeyError(
                "causal_rules.overrides.{0} sets unsupported field(s) {1} "
                "(supported: {2})".format(
                    rule.name, bad_fields, ", ".join(OVERRIDABLE_FIELDS)
                )
            )
        if not bool(override.get("enabled", True)):
            continue

        changes: Dict[str, Any] = {}
        if "prior" in override:
            prior = float(override["prior"])
            if not 0.0 < prior <= 1.0:
                raise ValueError(
                    "causal_rules.overrides.{0}.prior must lie in (0, 1], got "
                    "{1!r}".format(rule.name, override["prior"])
                )
            changes["prior"] = prior
        if "max_lag_s" in override:
            changes["max_lag_s"] = _positive_float(
                override["max_lag_s"], "causal_rules.overrides.{0}.max_lag_s".format(rule.name)
            )
        else:
            changes["max_lag_s"] = min(float(rule.max_lag_s), ceiling)
        if "edge_type" in override:
            edge_type = str(override["edge_type"])
            valid = tuple(e.value for e in CausalEdgeType)
            if edge_type not in valid:
                raise ValueError(
                    "causal_rules.overrides.{0}.edge_type must be a CausalEdgeType "
                    "value (one of {1}), got {2!r}".format(
                        rule.name, ", ".join(valid), override["edge_type"]
                    )
                )
            changes["edge_type"] = edge_type
        for flag in ("require_same_subject", "require_self_effect"):
            if flag in override:
                changes[flag] = bool(override[flag])

        out.append(dataclasses.replace(rule, **changes))

    if not out:
        raise ValueError(
            "every causal rule was disabled by causal_rules.overrides; the causal "
            "graph would be empty by construction"
        )
    validate_rules(tuple(out))
    return out


def _positive_float(value: Any, dotted: str) -> float:
    """Coerce a configuration value to a strictly positive float, or fail loudly."""
    try:
        out = float(value)
    except (TypeError, ValueError):
        raise TypeError("{0} must be a number, got {1!r}".format(dotted, value))
    if out <= 0.0:
        raise ValueError("{0} must be positive, got {1!r}".format(dotted, value))
    return out
