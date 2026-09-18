"""Running the properties over a trace, and saying what came of each.

An aggregate verdict over many trigger instances needs a rule, and the rule has
to be asymmetric. One instance failing means the property failed, however many
others passed -- a vehicle that stopped at four signs and ran the fifth ran a
sign. One instance undecidable and none failing means the property is undecided,
because a pass claimed while an instance is unknown is a pass over unwatched
time.

Vacuity is reported separately from all three. A property whose trigger never
fired has not passed; there was nothing to pass. Folding those into PASS would
make the pass rate a measure of how few obligations a scenario contained, and the
negative-control runs -- where almost nothing is triggered -- would score best of
all.

The same care applies to properties relating two vehicles. Comparing one
recorder's timestamps with another's is meaningless unless the clocks were
aligned, so on an unaligned trace those properties return UNKNOWN with that as
the reason, rather than quietly comparing numbers from two different clocks.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.schemas import SCHEMA_VERSIONS, CheckStatus, Provenance
from .evaluator import evaluate
from .properties import PROPERTIES, TemporalProperty
from .syntax import SELF, SUBJECT, render
from .trace import EventTrace

LOGGER = logging.getLogger(__name__)

__all__ = ["check_property", "check_all", "describe_properties"]


def describe_properties() -> Dict[str, Any]:
    """The properties as written, for ``formal/properties.json``.

    Published separately from the results so a reader can see what was checked
    without having to read a result to infer it.
    """
    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "logic": "metric temporal logic over a finite trace, three-valued",
        "operators": {
            "F[a,b]": "eventually, within the future interval",
            "G[a,b]": "always, throughout the future interval",
            "O[a,b]": "once, somewhere in the past interval",
            "H[a,b]": "historically, throughout the past interval",
            "phi S[a,b] psi": (
                "since: psi held somewhere in the past interval and phi has "
                "held at every instant after it. The one operator whose window "
                "is set by an event rather than by a constant"
            ),
        },
        "verdicts": {
            "PASS": "the property held at every triggered instance",
            "FAIL": "at least one instance violated it",
            "UNKNOWN": (
                "no instance failed, and at least one could not be decided "
                "because the interval ran outside the recording or across a "
                "gap in the evidence"
            ),
            "vacuous": (
                "the trigger never fired, so there was nothing to check. "
                "Reported separately and excluded from accuracy figures"
            ),
        },
        "note": (
            "each formula here is the object that is evaluated, not a "
            "description of separate code. Missing evidence never becomes PASS"
        ),
        "properties": [p.describe() for p in PROPERTIES],
    }


def check_property(
    prop: TemporalProperty,
    trace: EventTrace,
    cfg: Optional[Config] = None,
    participant_filter: Optional[str] = None,
) -> Dict[str, Any]:
    """Evaluate one property at every instant its trigger fired."""
    cfg = cfg if cfg is not None else Config({})

    if prop.needs_two_vehicles and not trace.is_multi_participant_safe():
        return {
            "property_id": prop.property_id,
            "title": prop.title,
            "formula": render(prop.formula),
            "status": CheckStatus.UNKNOWN.value,
            "vacuous": False,
            "n_instances": 0,
            "instances": [],
            "reason": (
                "this property relates events recorded by different vehicles, "
                "and their clocks were not aligned. Comparing the timestamps "
                "would be comparing two different clocks"
            ),
        }

    triggers = [
        event
        for trigger_type in prop.trigger_types
        for event in trace.of_type(trigger_type.value)
    ]
    # One instant can carry two boundary events -- a lane sensor reports the
    # marking and the solid line together -- and evaluating the same obligation
    # twice at the same time would double-count one violation.
    seen_at = set()
    deduped = []
    for event in sorted(triggers, key=lambda e: (e.t_peak, str(e.participant_id))):
        key = (str(event.participant_id), round(float(event.t_peak), 4))
        if key in seen_at:
            continue
        seen_at.add(key)
        deduped.append(event)
    triggers = deduped
    if participant_filter is not None:
        triggers = [
            e for e in triggers if str(e.participant_id) == str(participant_filter)
        ]

    if not triggers:
        return {
            "property_id": prop.property_id,
            "title": prop.title,
            "formula": render(prop.formula),
            "status": CheckStatus.PASS.value,
            "vacuous": True,
            "n_instances": 0,
            "instances": [],
            "reason": (
                "no {0} occurred, so the obligation never arose. Vacuous rather "
                "than satisfied".format(
                    " or ".join(t.value for t in prop.trigger_types)
                )
            ),
        }

    instances: List[Dict[str, Any]] = []
    for event in triggers:
        binding = {
            SELF: str(event.participant_id),
            SUBJECT: str(event.subject) if event.subject else None,
        }
        anchor = float(
            event.t_start if prop.anchor == "t_start" else event.t_peak
        )
        verdict = evaluate(prop.formula, trace, anchor, binding, cfg)
        instances.append({
            "trigger_event_id": event.event_id,
            "participant": str(event.participant_id),
            "subject": str(event.subject) if event.subject else "",
            "t": round(anchor, 4),
            "anchor": prop.anchor,
            **verdict.as_dict(),
        })

    statuses = [i["status"] for i in instances]
    if CheckStatus.FAIL.value in statuses:
        status = CheckStatus.FAIL
        reason = "{0} of {1} instance(s) violated the property".format(
            statuses.count(CheckStatus.FAIL.value), len(statuses)
        )
    elif CheckStatus.UNKNOWN.value in statuses:
        status = CheckStatus.UNKNOWN
        reason = (
            "{0} of {1} instance(s) could not be decided, and none failed. A "
            "pass here would be a claim about time that was not observed".format(
                statuses.count(CheckStatus.UNKNOWN.value), len(statuses)
            )
        )
    else:
        status = CheckStatus.PASS
        reason = "all {0} instance(s) satisfied the property".format(len(statuses))

    return {
        "property_id": prop.property_id,
        "title": prop.title,
        "formula": render(prop.formula),
        "benchmark_rule": prop.benchmark_rule,
        "status": status.value,
        "vacuous": False,
        "n_instances": len(instances),
        "n_pass": statuses.count(CheckStatus.PASS.value),
        "n_fail": statuses.count(CheckStatus.FAIL.value),
        "n_unknown": statuses.count(CheckStatus.UNKNOWN.value),
        "counterexamples": [
            i for i in instances if i["status"] == CheckStatus.FAIL.value
        ][:8],
        "instances": instances,
        "reason": reason,
    }


def check_all(
    trace: EventTrace,
    cfg: Optional[Config] = None,
    scope: Provenance = Provenance.FUSED,
    properties: Sequence[TemporalProperty] = PROPERTIES,
) -> Dict[str, Any]:
    """Every property over one trace, with a summary that keeps vacuity apart."""
    results = [check_property(p, trace, cfg) for p in properties]

    decided = [r for r in results if not r["vacuous"]]
    summary = {
        "n_properties": len(results),
        "n_vacuous": sum(1 for r in results if r["vacuous"]),
        "n_checked": len(decided),
        "n_pass": sum(1 for r in decided if r["status"] == CheckStatus.PASS.value),
        "n_fail": sum(1 for r in decided if r["status"] == CheckStatus.FAIL.value),
        "n_unknown": sum(
            1 for r in decided if r["status"] == CheckStatus.UNKNOWN.value
        ),
    }
    summary["unknown_rate"] = (
        round(summary["n_unknown"] / summary["n_checked"], 4)
        if summary["n_checked"] else None
    )
    summary["violations"] = sorted(
        r["property_id"] for r in decided if r["status"] == CheckStatus.FAIL.value
    )

    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "scope": scope.value,
        "trace": trace.describe(),
        "summary": summary,
        "results": results,
        "note": (
            "a vacuous property is one whose trigger never fired; it is counted "
            "apart from the pass rate, because otherwise a run containing few "
            "obligations would score better than one that met many and handled "
            "them correctly"
        ),
    }
