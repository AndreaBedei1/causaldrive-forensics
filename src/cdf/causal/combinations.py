"""Multi-action counterfactuals: when no single change would have prevented it.

Removing one action at a time answers one question: *was this action necessary?*
It cannot answer the question a multi-vehicle incident usually poses, which is
whether any single change would have been enough at all. Two vehicles can each
contribute without either being individually decisive -- remove A's behaviour and
the crash still happens, remove B's and it still happens, remove both and it does
not. Single-action replay reports that case as ``insufficient_evidence``, which
is true but uninformative.

This module adds the bounded search that settles it, and the vocabulary to say
what it found:

``single_initiator``
    exactly one action, removed alone, prevents the collision;
``shared_contribution``
    two or more actions each prevent it *on their own* -- either would have been
    enough;
``joint_contribution``
    no single action prevents it, but some minimal set of two or more does;
``contributing_but_not_necessary``
    no tested set prevents the collision, but removing an action measurably
    reduces its severity;
``insufficient_evidence``
    nothing tested changed the outcome, or there was nothing testable.

A **minimal prevention set** is an inclusion-minimal tested set whose joint
removal prevents the collision. Minimality is asserted only over what was
actually replayed: a set whose subsets were never tested is reported as
``minimal_within_tested`` rather than as minimal, because an untested subset
might have been enough and claiming otherwise would be an unsupported negative.

None of this is a fault percentage. A score here is a statement about what
changed when the simulator re-ran the encounter, and the artifacts say so.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Sequence, Tuple

from ..common.config import Config

__all__ = [
    "ATTRIBUTION_CLASSES",
    "SetOutcome",
    "minimal_prevention_sets",
    "classify_from_set_outcomes",
    "plan_combinations",
]


ATTRIBUTION_CLASSES: Tuple[str, ...] = (
    "single_initiator",
    "shared_contribution",
    "joint_contribution",
    "contributing_but_not_necessary",
    "insufficient_evidence",
)


@dataclass
class SetOutcome:
    """What happened when this set of actions was removed together."""

    actions: FrozenSet[str]
    prevented: bool
    severity_reduction: Optional[float] = None
    intervention_id: str = ""
    collision: Optional[bool] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "actions": sorted(self.actions),
            "size": len(self.actions),
            "prevented": bool(self.prevented),
            "collision": self.collision,
            "severity_reduction": (
                None if self.severity_reduction is None
                else round(float(self.severity_reduction), 6)
            ),
            "intervention_id": self.intervention_id,
            "notes": list(self.notes),
        }


def minimal_prevention_sets(
    outcomes: Sequence[SetOutcome],
) -> List[Dict[str, Any]]:
    """Inclusion-minimal tested sets whose joint removal prevented the collision.

    Minimality is judged against the sets that were *actually replayed*. A set
    all of whose proper subsets were tested and none of which prevented is
    minimal outright; a set with an untested proper subset is reported as
    minimal only within what was tested, because the untested subset might have
    sufficed and asserting otherwise would be a claim about a replay nobody ran.
    """
    preventing = [o for o in outcomes if o.prevented]
    tested = {o.actions for o in outcomes}
    results: List[Dict[str, Any]] = []
    for outcome in preventing:
        smaller_preventing = [
            other for other in preventing
            if other.actions < outcome.actions
        ]
        if smaller_preventing:
            continue  # a tested subset already prevented it: not minimal
        untested_subsets = [
            subset
            for size in range(1, len(outcome.actions))
            for subset in itertools.combinations(sorted(outcome.actions), size)
            if frozenset(subset) not in tested
        ]
        results.append(
            {
                "actions": sorted(outcome.actions),
                "size": len(outcome.actions),
                "intervention_id": outcome.intervention_id,
                "minimality": (
                    "minimal" if not untested_subsets else "minimal_within_tested"
                ),
                "untested_subsets": [sorted(s) for s in untested_subsets],
                "note": (
                    "every proper subset was replayed and none prevented the "
                    "collision" if not untested_subsets else
                    "{0} proper subset(s) were never replayed; a smaller set may "
                    "also have been enough".format(len(untested_subsets))
                ),
            }
        )
    results.sort(key=lambda r: (r["size"], r["actions"]))
    return results


def classify_from_set_outcomes(
    factual_collision: bool,
    outcomes: Sequence[SetOutcome],
    cfg: Optional[Config] = None,
) -> Dict[str, Any]:
    """Name what the replays established, without overstating any of it."""
    min_severity = 0.05
    if cfg is not None:
        min_severity = float(
            cfg.get("counterfactual.contribution.min_severity_reduction", 0.05)
        )

    if not outcomes:
        return {
            "attribution_class": "insufficient_evidence",
            "rationale": "no counterfactual replay completed for this outcome",
            "necessary_actions": [],
            "sufficient_single_actions": [],
            "minimal_prevention_sets": [],
            "contributing_actions": [],
            "mitigating_actions": [],
            "n_replays": 0,
            "disclaimer": _DISCLAIMER,
        }
    if not factual_collision:
        return {
            "attribution_class": "insufficient_evidence",
            "rationale": (
                "the factual run produced no collision, so there is no outcome to "
                "attribute; any preventive behaviour is reported separately"
            ),
            "necessary_actions": [],
            "sufficient_single_actions": [],
            "minimal_prevention_sets": [],
            "contributing_actions": [],
            "mitigating_actions": [],
            "n_replays": len(outcomes),
            "disclaimer": _DISCLAIMER,
        }

    singles = {
        next(iter(o.actions)): o for o in outcomes if len(o.actions) == 1
    }
    sufficient_singles = sorted(a for a, o in singles.items() if o.prevented)
    minimal_sets = minimal_prevention_sets(outcomes)
    severity_contributors = sorted(
        a
        for a, o in singles.items()
        if not o.prevented
        and o.severity_reduction is not None
        and float(o.severity_reduction) >= min_severity
    )
    # An action whose *removal* makes the impact worse did not contribute to the
    # collision -- it reduced it. Reporting that as "nothing changed" would
    # discard a real and opposite finding: these are the behaviours that
    # mitigated an outcome they did not cause.
    mitigating = sorted(
        a
        for a, o in singles.items()
        if not o.prevented
        and o.severity_reduction is not None
        and float(o.severity_reduction) <= -min_severity
    )

    if len(sufficient_singles) == 1:
        return {
            "attribution_class": "single_initiator",
            "rationale": (
                "removing {0} alone prevented the collision in replay and no "
                "other single action did".format(sufficient_singles[0])
            ),
            "necessary_actions": list(sufficient_singles),
            "sufficient_single_actions": list(sufficient_singles),
            "minimal_prevention_sets": minimal_sets,
            "contributing_actions": severity_contributors,
            "mitigating_actions": mitigating,
            "n_replays": len(outcomes),
            "disclaimer": _DISCLAIMER,
        }
    if len(sufficient_singles) >= 2:
        return {
            "attribution_class": "shared_contribution",
            "rationale": (
                "{0} actions each prevented the collision on their own; either "
                "change alone would have been enough".format(len(sufficient_singles))
            ),
            "necessary_actions": list(sufficient_singles),
            "sufficient_single_actions": list(sufficient_singles),
            "minimal_prevention_sets": minimal_sets,
            "contributing_actions": severity_contributors,
            "mitigating_actions": mitigating,
            "n_replays": len(outcomes),
            "disclaimer": _DISCLAIMER,
        }
    joint = [s for s in minimal_sets if s["size"] >= 2]
    if joint:
        return {
            "attribution_class": "joint_contribution",
            "rationale": (
                "no single action prevented the collision, but removing {0} "
                "together did; the contribution is joint".format(
                    " and ".join(joint[0]["actions"])
                )
            ),
            "necessary_actions": [],
            "sufficient_single_actions": [],
            "minimal_prevention_sets": minimal_sets,
            "contributing_actions": severity_contributors,
            "mitigating_actions": mitigating,
            "n_replays": len(outcomes),
            "disclaimer": _DISCLAIMER,
        }
    if severity_contributors:
        return {
            "attribution_class": "contributing_but_not_necessary",
            "rationale": (
                "no tested change prevented the collision; {0} measurably reduced "
                "its severity".format(", ".join(severity_contributors))
            ),
            "necessary_actions": [],
            "sufficient_single_actions": [],
            "minimal_prevention_sets": [],
            "contributing_actions": severity_contributors,
            "mitigating_actions": mitigating,
            "n_replays": len(outcomes),
            "disclaimer": _DISCLAIMER,
        }
    if mitigating:
        return {
            "attribution_class": "insufficient_evidence",
            "rationale": (
                "no tested change prevented the collision, and removing {0} made "
                "the impact measurably more severe: on this evidence {1} "
                "mitigated an outcome {1} did not cause, and no initiator is "
                "attributed".format(
                    ", ".join(mitigating),
                    "they" if len(mitigating) > 1 else "it",
                )
            ),
            "necessary_actions": [],
            "sufficient_single_actions": [],
            "minimal_prevention_sets": [],
            "contributing_actions": [],
            "mitigating_actions": mitigating,
            "n_replays": len(outcomes),
            "disclaimer": _DISCLAIMER,
        }
    return {
        "attribution_class": "insufficient_evidence",
        "rationale": (
            "none of the {0} replayed changes altered the outcome or its "
            "severity".format(len(outcomes))
        ),
        "necessary_actions": [],
        "sufficient_single_actions": [],
        "minimal_prevention_sets": [],
        "contributing_actions": [],
        "mitigating_actions": [],
        "n_replays": len(outcomes),
        "disclaimer": _DISCLAIMER,
    }


_DISCLAIMER = (
    "Causal contribution under controlled replay semantics. NOT legal fault and "
    "NOT a fault percentage."
)


def plan_combinations(
    candidates: Sequence[str],
    tested: Sequence[FrozenSet[str]],
    size: int,
    max_replays: int,
) -> List[FrozenSet[str]]:
    """Which sets of ``size`` actions to replay next, deterministically.

    Only combinations drawn from actions that did *not* individually prevent the
    collision are worth testing: if removing one alone was already enough,
    removing it together with something else tells us nothing new. Ordering is
    lexicographic so a campaign is reproducible, and the count is capped.
    """
    if size < 2 or len(candidates) < size:
        return []
    already = {frozenset(s) for s in tested}
    out: List[FrozenSet[str]] = []
    for combo in itertools.combinations(sorted(set(candidates)), size):
        key = frozenset(combo)
        if key in already:
            continue
        out.append(key)
        if len(out) >= max_replays:
            break
    return out
