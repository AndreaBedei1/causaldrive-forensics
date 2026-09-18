"""Whether the property verdicts the reconstruction reached were the right ones.

The properties are checked twice, over two traces, with the *same* formulae.

Once over the merged reconstruction: what the vehicles could establish between
them. Once over the observable ground truth: what was true. The second is the
reference, and running the identical checker over it is what makes the
comparison about the reconstruction rather than about two different definitions
of "stopped".

Four numbers come out of that, and two of them matter more than the headline.

**False violation rate** — the reconstruction said FAIL where the truth says
PASS. This is the expensive error: a vehicle accused of running a stop sign it
stopped at.

**Missed violation rate** — the reconstruction said PASS where the truth says
FAIL. Cheaper, and usually the one a conservative detector buys.

An UNKNOWN is neither. It is counted separately and never folded into either
rate, because a property the reconstruction could not decide has not made a
mistake -- it has declined to guess, which is the behaviour the three-valued
semantics exist to produce. Folding UNKNOWN into PASS would make a run that
observed nothing look perfectly accurate.

Vacuous properties are excluded from every rate on both sides. A property whose
trigger never fired has not been got right.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.io import read_json
from ..common.layout import RunLayout
from ..common.schemas import (
    SCHEMA_VERSIONS, CheckStatus, Provenance, events_from_payload,
)

LOGGER = logging.getLogger(__name__)

__all__ = ["aggregate_formal", "measure_formal", "reference_verdicts"]

PASS = CheckStatus.PASS.value
FAIL = CheckStatus.FAIL.value
UNKNOWN = CheckStatus.UNKNOWN.value


def reference_verdicts(
    layout: RunLayout,
    cfg: Optional[Config] = None,
) -> Optional[Dict[str, Any]]:
    """Run the same properties over the observable ground truth.

    The reference trace is privileged and complete, so it has no coverage model
    and no unaligned recorders: every participant is on simulator time by
    construction. That is the point -- an UNKNOWN on this side would mean the
    *property* could not be decided even with perfect information, which is a
    statement about the property rather than about the reconstruction.
    """
    if not layout.observable_events.exists():
        return None
    from ..formal import EventTrace, check_all

    payload = read_json(layout.observable_events)
    events = events_from_payload(payload.get("events", []) or [])
    if not events:
        return None
    participants = sorted({str(e.participant_id) for e in events})
    trace = EventTrace.from_events(
        events,
        coverage=None,
        time_axis="common",
        aligned_participants=participants,
    )
    return check_all(trace, cfg, scope=Provenance.ORACLE)


def _by_id(report: Optional[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    if not report:
        return {}
    return {
        str(r["property_id"]): r for r in report.get("results", []) or []
    }


def _witness(result: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
    """One concrete instance behind a verdict, for the report to quote.

    A rate without an example is a number nobody can check. The brief asks for
    witnesses by name and this is where they come from.
    """
    instances = result.get("counterexamples") or result.get("instances") or []
    if not instances:
        return None
    first = instances[0]
    return {
        "trigger_event_id": first.get("trigger_event_id"),
        "participant": first.get("participant"),
        "subject": first.get("subject"),
        "t": first.get("t"),
        "interval": first.get("interval"),
        "witness_event_ids": first.get("witness"),
        "reason": first.get("reason"),
    }


def measure_formal(
    run_dir: Any,
    cfg: Optional[Config] = None,
) -> Dict[str, Any]:
    """Score the reconstruction's property verdicts against the reference."""
    cfg = cfg if cfg is not None else Config({})
    layout = (
        run_dir if isinstance(run_dir, RunLayout) else RunLayout.from_run_dir(run_dir)
    )
    if not layout.formal_results.exists():
        return {
            "scored": False,
            "reason": "no formal/results.json; the property checker has not run",
        }

    inferred = read_json(layout.formal_results)
    reference = reference_verdicts(layout, cfg)
    inferred_by_id = _by_id(inferred)

    if reference is None:
        # Still report what the reconstruction said. A run with no observable
        # ground truth cannot be scored, but "the checker produced these
        # verdicts" is a different and still useful statement.
        return {
            "scored": False,
            "reason": (
                "no observable ground truth for this run, so the verdicts "
                "cannot be checked against anything"
            ),
            "verdict_counts": _counts(inferred_by_id.values()),
            "per_property": {
                pid: {
                    "inferred": r["status"],
                    "vacuous": bool(r.get("vacuous")),
                    "witness": _witness(r),
                }
                for pid, r in sorted(inferred_by_id.items())
            },
        }

    reference_by_id = _by_id(reference)
    per_property: Dict[str, Any] = {}
    agree = disagree = 0
    false_violations: List[str] = []
    missed_violations: List[str] = []
    undecided: List[str] = []

    for pid in sorted(set(inferred_by_id) | set(reference_by_id)):
        mine = inferred_by_id.get(pid)
        theirs = reference_by_id.get(pid)
        entry: Dict[str, Any] = {
            "inferred": mine["status"] if mine else None,
            "reference": theirs["status"] if theirs else None,
            "inferred_vacuous": bool(mine.get("vacuous")) if mine else None,
            "reference_vacuous": bool(theirs.get("vacuous")) if theirs else None,
            "witness": _witness(mine) if mine else None,
            "reference_witness": _witness(theirs) if theirs else None,
        }

        # Either side vacuous means the obligation did not arise there, and a
        # verdict about an obligation that never arose is not a verdict to score.
        if (mine is None or theirs is None
                or mine.get("vacuous") or theirs.get("vacuous")):
            entry["comparison"] = "not_comparable"
            entry["why"] = (
                "the trigger fired on at most one side, so there is no shared "
                "obligation to agree or disagree about"
            )
        elif theirs["status"] == UNKNOWN:
            # Checked before the reconstruction's own UNKNOWN: if the property
            # could not be decided even with exact state, nothing about the
            # reconstruction follows from its verdict either way. Reporting that
            # as "the reconstruction declined" would blame it for a limit of the
            # property.
            entry["comparison"] = "reference_undecided"
            entry["why"] = (
                "even with exact state the property could not be decided -- "
                "usually because its window ran past the end of the recording "
                "-- so there is nothing to score the reconstruction against"
            )
        elif mine["status"] == UNKNOWN:
            entry["comparison"] = "undecided"
            entry["why"] = (
                "the reference decided this and the reconstruction could not. "
                "Not an error: a property it could not establish has not been "
                "got wrong, and this is the gap between what was true and what "
                "the vehicles could show"
            )
            undecided.append(pid)
        elif mine["status"] == theirs["status"]:
            entry["comparison"] = "agree"
            agree += 1
        elif mine["status"] == FAIL and theirs["status"] == PASS:
            entry["comparison"] = "false_violation"
            entry["why"] = "claimed a violation the ground truth does not support"
            false_violations.append(pid)
            disagree += 1
        elif mine["status"] == PASS and theirs["status"] == FAIL:
            entry["comparison"] = "missed_violation"
            entry["why"] = "missed a violation the ground truth shows"
            missed_violations.append(pid)
            disagree += 1
        else:  # pragma: no cover - every combination above is exhaustive
            entry["comparison"] = "not_comparable"
            entry["why"] = "an unexpected combination of verdicts"
        per_property[pid] = entry

    n_comparable = agree + disagree
    return {
        "scored": True,
        "schema_version": SCHEMA_VERSIONS["evaluation"],
        "verdict_counts": _counts(inferred_by_id.values()),
        "reference_verdict_counts": _counts(reference_by_id.values()),
        "n_comparable": n_comparable,
        "n_agree": agree,
        "n_disagree": disagree,
        "agreement": round(agree / n_comparable, 4) if n_comparable else None,
        "false_violations": false_violations,
        "missed_violations": missed_violations,
        "false_violation_rate": (
            round(len(false_violations) / n_comparable, 4) if n_comparable else None
        ),
        "missed_violation_rate": (
            round(len(missed_violations) / n_comparable, 4) if n_comparable else None
        ),
        "undecided_by_reconstruction": undecided,
        "per_property": per_property,
        "note": (
            "the same formulae are evaluated over the merged reconstruction and "
            "over the observable ground truth, so the comparison is about the "
            "reconstruction rather than about two definitions of the same word. "
            "UNKNOWN is never folded into PASS: declining to decide is not an "
            "error, and counting it as agreement would make a run that observed "
            "nothing look perfectly accurate"
        ),
    }


def aggregate_formal(per_run: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """Campaign totals over the property verdicts.

    Counts are summed and divided once. Averaging per-run rates would let a run
    with one comparable property outweigh a run with eight, and the question is
    about properties rather than about runs.

    Which properties produced the false violations is listed rather than only
    counted: one property failing everywhere and eight failing once each are the
    same rate and completely different problems.
    """
    scored = [r for r in per_run if r.get("scored")]
    if not scored:
        return {"scored": False, "reason": "no run could be scored", "n_runs": 0}

    comparable = agree = 0
    false_by_property: Dict[str, int] = {}
    missed_by_property: Dict[str, int] = {}
    undecided_by_property: Dict[str, int] = {}
    for run in scored:
        comparable += int(run.get("n_comparable") or 0)
        agree += int(run.get("n_agree") or 0)
        for pid in run.get("false_violations") or []:
            false_by_property[pid] = false_by_property.get(pid, 0) + 1
        for pid in run.get("missed_violations") or []:
            missed_by_property[pid] = missed_by_property.get(pid, 0) + 1
        for pid in run.get("undecided_by_reconstruction") or []:
            undecided_by_property[pid] = undecided_by_property.get(pid, 0) + 1

    n_false = sum(false_by_property.values())
    n_missed = sum(missed_by_property.values())
    return {
        "scored": True,
        "n_runs": len(scored),
        "n_comparable": comparable,
        "n_agree": agree,
        "agreement": round(agree / comparable, 4) if comparable else None,
        "n_false_violations": n_false,
        "n_missed_violations": n_missed,
        "false_violation_rate": (
            round(n_false / comparable, 4) if comparable else None
        ),
        "missed_violation_rate": (
            round(n_missed / comparable, 4) if comparable else None
        ),
        "false_violations_by_property": dict(sorted(false_by_property.items())),
        "missed_violations_by_property": dict(sorted(missed_by_property.items())),
        "undecided_by_property": dict(sorted(undecided_by_property.items())),
        "note": (
            "counts summed across runs and divided once, so every comparable "
            "property weighs the same. Broken down by property because one "
            "property failing everywhere and eight failing once each give the "
            "same rate and are different problems"
        ),
    }


def _counts(results: Any) -> Dict[str, int]:
    out = {PASS: 0, FAIL: 0, UNKNOWN: 0, "vacuous": 0}
    for result in results or []:
        if result.get("vacuous"):
            out["vacuous"] += 1
            continue
        out[str(result.get("status"))] = out.get(str(result.get("status")), 0) + 1
    return out
