"""Causal attribution from controlled counterfactual replays.

What this module computes, precisely
------------------------------------
For every replayed intervention it answers two questions with numbers that came
out of the simulator:

*Did removing (or weakening) this action prevent the crash?* -- the **but-for**
test, :func:`but_for`.

*If the crash still happened, was it less severe?* -- the **severity reduction**,
:func:`severity_reduction`.

Those two are combined into one transparent, normalised
:func:`contribution_score`, and :func:`classify_attribution` turns the set of
per-action results into one of three verdicts: a single initiator, a shared
contribution, or insufficient evidence.

What this module does NOT compute
---------------------------------
Fault. Liability. Blame. A but-for result is a statement about *this* physical
system under *these* interventions: "in the replayed world where B never braked,
no collision occurred". Legal fault additionally involves duty, foreseeability,
right of way, and rules of the road, none of which this system models and none of
which are recoverable from onboard evidence. Every public function here repeats
that caveat, because a number labelled "contribution" is exactly the kind of
number that gets quoted out of context.

Two honesty rules are structural rather than advisory:

* Where no replay succeeded, or no replay prevented the collision, the verdict is
  ``insufficient_evidence``. A culprit is never forced.
* A counterfactual's ``validation_passed`` being ``False`` is *not* an error
  here. Scenario validation asserts that the designed encounter happened; a
  replay that successfully prevents the crash is expected to fail it. Prevention
  is read from the outcome, never from the validation flag.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.schemas import SCHEMA_VERSIONS
from .counterfactuals import CounterfactualOutcome
from .interventions import InterventionSpec

LOGGER = logging.getLogger(__name__)

__all__ = [
    "ATTRIBUTION_CLASSES",
    "CausalContribution",
    "but_for",
    "severity_reduction",
    "contribution_score",
    "contribution_of",
    "classify_attribution",
    "attribution_report",
]

#: The only verdicts this module can reach.
ATTRIBUTION_CLASSES = (
    "single_initiator",
    "shared_contribution",
    "insufficient_evidence",
)

#: Severity metrics a configuration may select through
#: ``counterfactual.severity_metric``.
_SEVERITY_METRICS = ("relative_impact_speed", "impact_speed")


@dataclass
class CausalContribution:
    """One intervention's measured contribution, with the raw outcome kept.

    The score is never stored without the evidence that produced it: ``outcome``
    (and, for the baseline, ``factual``) stay attached so a reader can always ask
    "what actually happened in that replay?".
    """

    intervention_id: str
    action_id: str
    op: str
    targets_participant: str
    but_for: int
    """1 when the factual run collided and this replay did not, else 0."""
    severity_reduction: Optional[float]
    """Fractional reduction of the severity metric; ``None`` when undefined."""
    score: float
    outcome: CounterfactualOutcome
    prevented_collision: bool = False
    #: Whether this replay is the *kind* that can establish causation at all --
    #: a removal or a weakening, rather than the same action performed sooner.
    #: A replay that prevented the collision without establishing causation is a
    #: prevention opportunity, and the difference matters: counting the second
    #: as the first makes the method name whoever could most easily have avoided
    #: the outcome, which is usually the vehicle that was hit.
    establishes_causation: bool = True
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Serialisable record, raw outcome included."""
        return {
            "intervention_id": self.intervention_id,
            "action_id": self.action_id,
            "op": self.op,
            "targets_participant": self.targets_participant,
            "but_for": int(self.but_for),
            "severity_reduction": self.severity_reduction,
            "contribution_score": round(float(self.score), 6),
            "prevented_collision": bool(self.prevented_collision),
            "establishes_causation": bool(self.establishes_causation),
            "outcome": self.outcome.to_dict(),
            "notes": list(self.notes),
        }


# ---------------------------------------------------------------------------
# Elementary measures
# ---------------------------------------------------------------------------


#: Operations that make an action *less* than it was -- absent, weaker, or later.
#: Only these bear on but-for causation, because only these approximate the
#: question "what if this had not been done?".
COUNTERFACTUAL_REMOVALS: Tuple[str, ...] = ("disable", "scale", "delay", "set")

#: Operations that make an action *more* than it was: earlier, or stronger.
#: A replay of this kind answers "would more of this have helped?", which is
#: useful prevention advice and is not evidence that the action caused anything.
COUNTERFACTUAL_IMPROVEMENTS: Tuple[str, ...] = ("advance",)

#: The one operation that supplies a behaviour which did not occur at all.
#:
#: Whether it can establish causation depends on *what* it supplies. Inserting
#: the stop a vehicle was required to make, where the evidence supports that it
#: did not, tests the causal relevance of the omission -- which is a real
#: but-for question and the only way to ask it, since there is no factual action
#: to remove. Inserting a brake for a vehicle under no obligation to brake asks
#: "could someone have avoided this?", which is prevention advice wearing the
#: same clothes.
#:
#: The two are told apart by whether the replay names the non-action it repairs.
COUNTERFACTUAL_INSERTION: str = "insert_action"


def establishes_but_for(cf: CounterfactualOutcome) -> bool:
    """Whether this replay is the kind that can establish but-for causation.

    Removing an action, weakening it, or delaying it all approximate its absence.
    *Advancing* it does not: it is a stronger version of the same behaviour, and
    a collision avoided by doing something sooner says the driver could have done
    better, not that what they did caused the crash.

    The distinction is load-bearing. In the rear-end scenario, disabling the
    following driver's late brake changes nothing and weakening it changes
    nothing -- but braking a second earlier avoids the collision entirely. Count
    that as but-for causation and the system names the vehicle that was hit,
    which is precisely what the oracle's own attribution rules exclude and
    exactly the wrong answer.

    Insertion is the third case and needs care, because it looks like the second
    and behaves like the first. A vehicle that ran a stop sign performed no
    action to weaken: the only way to ask whether the omission mattered is to
    supply the stop and see. That is a genuine but-for test *of the omission* --
    but only where the omission is itself supported, which is why an insertion
    counts only when it names the non-action it repairs. An insertion that names
    none is adding safe behaviour to a run, and if that established causation
    then every vehicle would have caused every collision it could have avoided.
    """
    op = str(getattr(cf, "op", "") or "").lower()
    if op == COUNTERFACTUAL_INSERTION:
        # An insertion establishes causation only when it repairs an omission
        # the evidence supports. Without that, adding safe behaviour to any run
        # would "establish" that every vehicle caused every collision it could
        # have prevented -- which is the same error as counting an advanced
        # brake, arriving by a different route.
        return bool(str(getattr(cf, "repairs_non_action", "") or ""))
    if op in COUNTERFACTUAL_IMPROVEMENTS:
        return False
    if op == "scale":
        # Scaling up intensifies; only scaling down weakens.
        factor = None
        params = getattr(cf, "params", None) or {}
        if isinstance(params, Mapping):
            factor = params.get("factor")
        if factor is not None:
            try:
                return float(factor) < 1.0
            except (TypeError, ValueError):
                return True
    return True


def but_for(factual: CounterfactualOutcome, cf: CounterfactualOutcome) -> int:
    """The but-for test: 1 when *removing* the action prevented the collision.

    Returns 1 exactly when the factual run collided, the replay -- identical in
    every respect except the single intervened action -- did not, **and** the
    intervention was one that removes, weakens or delays the action rather than
    strengthening it. Otherwise 0.

    That last condition is not a technicality. But-for causation asks what would
    have happened had the action not occurred; a replay in which the driver acts
    *sooner* answers a different question, and treating its answer as causation
    makes the method name whoever could most easily have avoided the outcome --
    usually the victim. See :func:`establishes_but_for`.

    This is a **causal contribution under the stated intervention semantics**:
    "had this scripted action not been performed as it was, no collision would
    have occurred in this replay". It is explicitly **not** a finding of legal
    fault: duty of care, right of way and foreseeability are outside this model
    and cannot be derived from onboard evidence.
    """
    _require_outcome(factual, "factual")
    _require_outcome(cf, "counterfactual")
    if not (factual.collision and not cf.collision):
        return 0
    return 1 if establishes_but_for(cf) else 0


def severity_reduction(
    factual: CounterfactualOutcome,
    cf: CounterfactualOutcome,
    cfg: Optional[Config] = None,
) -> Optional[float]:
    """Fractional reduction of impact severity, or ``None`` when undefined.

    The metric is chosen by ``counterfactual.severity_metric`` and defaults to
    ``relative_impact_speed`` -- the magnitude of the relative velocity at
    impact, which is the quantity that governs how bad a collision is, rather
    than how fast either vehicle happened to be travelling.

    Returns ``(factual - counterfactual) / factual``: positive when the replay
    was less severe, negative when it was worse, ``None`` when either run has no
    measured value (no impact, or no persisted oracle trace) or when the factual
    severity is zero and the ratio would be meaningless. ``None`` means *not
    measured* and must not be read as zero.
    """
    _require_outcome(factual, "factual")
    _require_outcome(cf, "counterfactual")

    metric = (
        str(cfg.get("counterfactual.severity_metric", _SEVERITY_METRICS[0]))
        if cfg
        else _SEVERITY_METRICS[0]
    )
    if metric not in _SEVERITY_METRICS:
        raise ValueError(
            "counterfactual.severity_metric is {0!r}; expected one of {1}".format(
                metric, list(_SEVERITY_METRICS)
            )
        )

    base = getattr(factual, metric)
    replayed = getattr(cf, metric)
    if base is None or replayed is None:
        return None
    base = float(base)
    if base <= 0.0:
        return None
    return (base - float(replayed)) / base


def contribution_score(
    factual: CounterfactualOutcome,
    cf: CounterfactualOutcome,
    cfg: Optional[Config] = None,
) -> float:
    """Normalised causal-contribution score in ``[0, 1]``.

    The formula, in full::

        score = (w_prevent * but_for + w_severity * clamp(severity_reduction, 0, 1))
                / (w_prevent + w_severity)

    with ``w_prevent = counterfactual.contribution.prevention_weight`` (default
    1.0) and ``w_severity = counterfactual.contribution.severity_weight``
    (default 0.5). Prevention therefore dominates, and a replay that only made
    the impact softer still scores above one that changed nothing.

    When the replay prevented the collision *by removing the action* the severity
    term is 1.0 by definition (there was no impact left to be severe), even
    though :func:`severity_reduction` returns ``None`` because the counterfactual
    has no impact speed to compare. When severity is undefined for any other
    reason the term is 0.0: an unmeasured reduction is not evidence of a
    reduction.

    A replay that prevented the collision by performing the action *sooner*
    scores zero on both terms, which is correct and deliberate: it establishes
    that the outcome was avoidable, not that the action caused it, and a score
    is a ranking of candidate *causes*. The prevention itself is not discarded --
    it is recorded on the contribution as ``prevented_collision`` with
    ``establishes_causation`` false, so a reader can see both facts.

    **This is not a fault percentage.** It is a monotone summary of two
    measurements from controlled replays, on an arbitrary but fixed scale, and it
    is meaningless outside the intervention set that produced it. The raw
    outcomes are kept alongside it in :class:`CausalContribution` precisely so
    that the score never has to be trusted on its own.
    """
    prevention_weight = (
        float(cfg.get("counterfactual.contribution.prevention_weight", 1.0)) if cfg else 1.0
    )
    severity_weight = (
        float(cfg.get("counterfactual.contribution.severity_weight", 0.5)) if cfg else 0.5
    )
    total = prevention_weight + severity_weight
    if total <= 0.0:
        raise ValueError(
            "counterfactual.contribution weights sum to {0}; they must be "
            "positive for the score to be normalisable".format(total)
        )

    prevented = but_for(factual, cf)
    reduction = severity_reduction(factual, cf, cfg)
    if reduction is None:
        # Prevention is the strongest possible severity reduction; anything else
        # unmeasured contributes nothing.
        reduction = 1.0 if prevented else 0.0

    severity_term = min(1.0, max(0.0, float(reduction)))
    return (prevention_weight * prevented + severity_weight * severity_term) / total


def contribution_of(
    factual: CounterfactualOutcome,
    cf: CounterfactualOutcome,
    cfg: Optional[Config] = None,
) -> CausalContribution:
    """Package one replay into the record :func:`classify_attribution` consumes."""
    notes: List[str] = []
    if not factual.collision:
        notes.append(
            "the factual run did not collide, so the but-for test is vacuous here"
        )
    if cf.collision and cf.relative_impact_speed is None:
        notes.append("replay collided but its impact severity was not measurable")
    if not cf.collision and cf.near_miss:
        notes.append(
            "collision prevented, but the replay still produced a near miss"
        )
    prevented = bool(factual.collision and not cf.collision)
    if prevented and not establishes_but_for(cf):
        notes.append(
            "this replay prevented the collision by performing the action "
            "*sooner*, not by removing it. That shows the outcome was "
            "avoidable, not that the action caused it, so it does not count "
            "towards but-for causation"
        )
    return CausalContribution(
        intervention_id=cf.intervention_id,
        action_id=cf.action_id,
        op=cf.op,
        targets_participant=cf.targets_participant,
        but_for=but_for(factual, cf),
        severity_reduction=severity_reduction(factual, cf, cfg),
        score=contribution_score(factual, cf, cfg),
        outcome=cf,
        prevented_collision=prevented,
        establishes_causation=establishes_but_for(cf),
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------


def classify_attribution(
    results: Sequence[CausalContribution],
    cfg: Optional[Config] = None,
    factual_collision: bool = True,
) -> Dict[str, Any]:
    """Turn per-replay contributions into an attribution verdict.

    Results are aggregated **per scripted action**, not per intervention: an
    action is replayed several ways (disabled, weakened, re-timed) and each way
    is a separate test of the same hypothesis. An action counts as *necessary*
    when at least one of its replays prevented the collision; its score is the
    strongest one it achieved.

    The verdict follows mechanically from how many actions are necessary:

    * exactly one  -> ``single_initiator``, and that action is the primary
      initiator;
    * two or more  -> ``shared_contribution`` (the S05 shape: intervening on
      *either* participant prevents the crash, so neither is "the" cause), with
      no primary initiator, because naming one would be a choice the evidence
      does not support;
    * none, or no replay at all -> ``insufficient_evidence``.

    The last case is a real result, not a failure to try. It is what an honest
    system returns when the crash survived every intervention it was able to
    make, and it must never be rewritten into a culprit.

    ``factual_collision`` says whether the run being attributed collided at all.
    It does not change the verdict -- a run with no outcome has nothing to
    attribute and reaches ``insufficient_evidence`` either way -- but it does
    change the *reason given*, and a reason is not a decoration. The viewer
    prints this sentence to a reader, and telling them "the collision still
    occurred in all six replays" about a run that never collided is a plain
    falsehood, even though the class beside it is right.
    """
    for item in results:
        if not isinstance(item, CausalContribution):
            raise TypeError(
                "classify_attribution expects CausalContribution records (build "
                "them with contribution_of), got {0!r}".format(type(item))
            )

    min_score = (
        float(cfg.get("counterfactual.contribution.min_reportable_score", 0.0))
        if cfg
        else 0.0
    )

    scores: Dict[str, float] = {}
    necessary: List[str] = []
    per_action: Dict[str, List[CausalContribution]] = {}
    for item in results:
        per_action.setdefault(item.action_id, []).append(item)

    for action_id in sorted(per_action):
        items = per_action[action_id]
        scores[action_id] = round(max(float(i.score) for i in items), 6)
        if any(int(i.but_for) == 1 for i in items):
            necessary.append(action_id)

    contributing = [
        action_id
        for action_id in sorted(scores)
        if action_id not in necessary and scores[action_id] > min_score
    ]

    if not results:
        attribution_class = "insufficient_evidence"
        primary: Optional[str] = None
        rationale = (
            "no counterfactual replay produced a usable outcome, so no causal "
            "contribution could be measured"
        )
    elif not factual_collision:
        attribution_class = "insufficient_evidence"
        primary = None
        rationale = (
            "the factual run produced no collision, so there is no outcome to "
            "attribute; the {0} replay(s) are reported for what they show about "
            "the encounter, not as evidence against anybody".format(len(results))
        )
    elif len(necessary) == 1:
        attribution_class = "single_initiator"
        primary = necessary[0]
        rationale = (
            "removing or weakening {0} prevented the collision in replay, and no "
            "other replayed action did; the collision is attributed to that "
            "action under the stated intervention semantics (not a finding of "
            "legal fault)".format(primary)
        )
    elif len(necessary) >= 2:
        attribution_class = "shared_contribution"
        primary = None
        rationale = (
            "intervening on any of {0} independently prevented the collision, so "
            "no single action is necessary on its own; the contribution is "
            "shared and no primary initiator is named".format(", ".join(necessary))
        )
    else:
        attribution_class = "insufficient_evidence"
        primary = None
        rationale = (
            "the collision still occurred in all {0} replay(s); none of the "
            "interventions available was sufficient to prevent it, so no "
            "initiator is attributed".format(len(results))
        )

    return {
        "necessary_actions": list(necessary),
        "contributing_actions": contributing,
        "attribution_class": attribution_class,
        "primary_initiator": primary,
        "scores": scores,
        "rationale": rationale,
        "n_replays": len(results),
        "disclaimer": (
            "Causal contribution under controlled replay semantics. NOT legal "
            "fault and NOT a fault percentage."
        ),
    }


def attribution_report(
    factual: Optional[CounterfactualOutcome],
    counterfactuals: Sequence[CounterfactualOutcome],
    cfg: Optional[Config] = None,
    interventions: Optional[Sequence[InterventionSpec]] = None,
    failures: Optional[Sequence[Mapping[str, Any]]] = None,
    scenario_id: str = "",
    variant: str = "",
    seed: int = 0,
) -> Dict[str, Any]:
    """The full causal-contribution document written to ``causal_contribution.json``.

    Carries the factual outcome, every replay's raw outcome and score, the
    verdict, and -- importantly -- what could *not* be replayed: a replay that
    crashed is listed with its error so that a reader can tell a hypothesis that
    was tested and rejected from one that was never tested at all.
    """
    failures = list(failures or [])
    contributions: List[CausalContribution] = []

    if factual is None:
        classification = {
            "necessary_actions": [],
            "contributing_actions": [],
            "attribution_class": "insufficient_evidence",
            "primary_initiator": None,
            "scores": {},
            "rationale": (
                "the factual outcome is unknown, so no counterfactual comparison "
                "is possible"
            ),
            "n_replays": len(counterfactuals),
            "disclaimer": (
                "Causal contribution under controlled replay semantics. NOT legal "
                "fault and NOT a fault percentage."
            ),
        }
    else:
        contributions = [contribution_of(factual, cf, cfg) for cf in counterfactuals]
        classification = classify_attribution(
            contributions, cfg, factual_collision=bool(factual.collision)
        )

    notes: List[str] = []
    if failures:
        notes.append(
            "{0} replay(s) failed and were not evaluated: {1}".format(
                len(failures),
                ", ".join(str(f.get("intervention_id", "?")) for f in failures),
            )
        )
    if factual is not None and not factual.collision:
        notes.append(
            "the factual run did not collide; but-for prevention is undefined for "
            "this run and every score reflects severity only"
        )

    set_analysis = set_analysis_from(factual, counterfactuals, cfg)
    if set_analysis.get("n_composite_replays"):
        # Only a multi-action replay can tell a joint contribution from an
        # absence of evidence, so when one was run its verdict is the verdict.
        classification = dict(classification)
        classification["attribution_class"] = set_analysis["attribution_class"]
        classification["rationale"] = set_analysis["rationale"]
        classification["minimal_prevention_sets"] = set_analysis[
            "minimal_prevention_sets"
        ]
        classification["source"] = "multi_action_replay"

    return {
        "schema_version": SCHEMA_VERSIONS["counterfactual"],
        "scenario_id": scenario_id,
        "variant": variant,
        "seed": int(seed),
        "severity_metric": (
            str(cfg.get("counterfactual.severity_metric", _SEVERITY_METRICS[0]))
            if cfg
            else _SEVERITY_METRICS[0]
        ),
        "weights": {
            "prevention": (
                float(cfg.get("counterfactual.contribution.prevention_weight", 1.0))
                if cfg
                else 1.0
            ),
            "severity": (
                float(cfg.get("counterfactual.contribution.severity_weight", 0.5))
                if cfg
                else 0.5
            ),
        },
        "factual": factual.to_dict() if factual is not None else None,
        "interventions": [iv.to_dict() for iv in (interventions or [])],
        "contributions": [c.to_dict() for c in contributions],
        "classification": classification,
        "set_analysis": set_analysis,
        "n_requested": len(interventions or []),
        "n_completed": len(counterfactuals),
        "n_failed": len(failures),
        "failures": [dict(f) for f in failures],
        "notes": notes,
    }


def set_analysis_from(
    factual: Optional[CounterfactualOutcome],
    counterfactuals: Sequence[CounterfactualOutcome],
    cfg: Optional[Config],
) -> Dict[str, Any]:
    """Classify the replays as *sets* of removed actions.

    This is the analysis that can distinguish a joint contribution -- neither
    change is enough alone, both together are -- from a genuine absence of
    evidence. It subsumes the single-action verdicts, so it is reported for
    every suite; when only single actions were replayed it simply finds no
    multi-action prevention set, which is itself worth recording.
    """
    from .combinations import SetOutcome, classify_from_set_outcomes

    outcomes = []
    for cf in counterfactuals:
        actions = getattr(cf, "action_ids", None) or (
            [cf.action_id] if cf.action_id else []
        )
        if not actions:
            continue
        outcomes.append(
            SetOutcome(
                actions=frozenset(str(a) for a in actions),
                prevented=bool(
                    factual is not None and factual.collision and not cf.collision
                ),
                severity_reduction=severity_reduction(factual, cf, cfg)
                if factual is not None
                else None,
                intervention_id=cf.intervention_id,
                collision=cf.collision,
            )
        )
    result = classify_from_set_outcomes(
        bool(factual is not None and factual.collision), outcomes, cfg
    )
    result["set_outcomes"] = [o.to_dict() for o in sorted(
        outcomes, key=lambda o: (len(o.actions), sorted(o.actions))
    )]
    result["n_composite_replays"] = sum(1 for o in outcomes if len(o.actions) > 1)
    return result


def _require_outcome(value: Any, role: str) -> None:
    """Fail loudly rather than silently comparing the wrong kind of object."""
    if not isinstance(value, CounterfactualOutcome):
        raise TypeError(
            "the {0} argument must be a CounterfactualOutcome, got {1!r}".format(
                role, type(value)
            )
        )
