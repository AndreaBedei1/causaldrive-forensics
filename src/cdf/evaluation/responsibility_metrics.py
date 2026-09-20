"""Whether the responsibility findings matched what the scenario designed.

This comparison is different in kind from the others and the difference has to
stay visible. The graph comparison scores a reconstruction against *what
happened*; this scores it against *what the experiment intended*, which is a
claim about the scenario rather than about the world.

That makes it the weaker reference, and it is reported separately for exactly
that reason. A scenario can be designed so that B is the contributor and then
fail to make B behave that way -- the design reference checks itself against the
trace for precisely this, and a disagreement here may mean the reconstruction was
wrong or may mean the scenario did not execute as written.

Four things are measured.

**Contributor sets.** Precision and recall over the vehicles named as
responsibility contributors, plus exact-set match, which is the strict question:
did the method name the same vehicles, no more and no fewer.

**Violations.** Whether each designed normative failure was detected.

**Evidence classes.** Whether *supported*, *partial* and *insufficient* were
assigned as designed -- a vehicle correctly identified as involved but graded
partial where the design says supported is a different kind of near-miss from
naming the wrong vehicle, and the two are not averaged together.

**The hard cases.** Ambiguous priority, the pushed vehicle, independent impacts
and secondary collisions are flagged by name, because they are the rows where a
plausible-looking aggregate can hide the answer being exactly backwards.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..common.config import Config
from ..common.io import read_json
from ..common.layout import RunLayout
from ..common.schemas import SCHEMA_VERSIONS

LOGGER = logging.getLogger(__name__)

__all__ = [
    "aggregate_responsibility", "designed_contributors", "measure_responsibility",
]

#: Scenario/variant pairs whose designed answer is subtle enough that an
#: aggregate can hide getting it backwards. Named so the report can call them
#: out individually rather than letting them average away.
HARD_CASES: Dict[Tuple[str, str], str] = {
    ("S12", "near_simultaneous"): (
        "priority must stay ambiguous; a method that always names a winner "
        "scores better on a naive metric while being wrong"
    ),
    ("S14", "c_pushes_b"): (
        "the pushed vehicle must not be an initiating contributor merely "
        "because it physically struck the vehicle ahead"
    ),
    ("S15", "deflected_into_c"): (
        "the deflected vehicle and the bystander are both uninvolved in the "
        "normative account"
    ),
    ("S16", "consequential"): (
        "the second impact is a consequence, so its participant contributes to "
        "the first and not to the second"
    ),
    ("S16", "independent"): (
        "the same pair, the same geometry, and the second impact is that "
        "vehicle's own doing. This is the case S14's retired "
        "independent_impacts variant was written for, on a road situation "
        "rather than on a stopped car creeping into a wreck"
    ),
}


#: Template state names that assert a vehicle failed to do something required.
#: These are what make a designed *normative* claim, as opposed to a designed
#: physical one. Matched against cdf.oracle.events.STATE_EVENT_TYPES.
_NORMATIVE_STATES: Tuple[str, ...] = (
    "no_stop", "no_yield", "no_braking", "unsafe_entry", "solid_line_crossed",
)


def designed_contributors(design: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """What the scenario's causal template designs -- physically and normatively.

    These are two different claims and an earlier version of this module scored
    one against the other, which is the category error the whole V2 refactor was
    about. The template is a *physical* structure: in the chain-collision
    scenario it says the lead vehicle's emergency brake closed the gap and the
    follower's critical TTC caused the impact. Both are causes. Neither is a
    normative failing -- braking hard is not a rule violation, and a vehicle that
    brakes lawfully and is struck from behind has done nothing wrong.

    So the template yields two sets:

    ``physical`` -- every participant owning a cause node, excluding ``PREVENTS``
    edges, which name behaviour designed to act *against* the outcome. Compared
    with the reconstruction's physical contributors.

    ``normative`` -- the subset whose cause is a state that asserts a required
    behaviour was absent. Compared with the responsibility findings. A scenario
    with no traffic control and no designed omission has none, and the normative
    comparison is then **not applicable** rather than zero: a reconstruction that
    finds a real normative failing the scenario never designed has not made a
    false positive against a reference that says nothing on the subject.
    """
    if not design:
        return {
            "known": False, "physical": [], "normative": [],
            "reason": "no design reference",
        }

    template = design.get("causal_template") or []
    physical: Set[str] = set()
    normative: Set[str] = set()
    for edge in template:
        if str(edge.get("edge", "")) == "PREVENTS":
            continue
        cause = edge.get("cause") or {}
        participant = cause.get("participant")
        if not participant:
            continue
        physical.add(str(participant))
        if str(cause.get("name", "")) in _NORMATIVE_STATES:
            normative.add(str(participant))

    return {
        "known": bool(template),
        "physical": sorted(physical),
        "normative": sorted(normative),
        "declares_any_normative_failing": bool(normative),
        "n_template_edges": len(template),
        "reason": "" if template else "the scenario declares no causal template",
        "note": (
            "two sets, because the template makes two kinds of claim. Physical "
            "causes are not normative failings: braking hard closes a gap and "
            "breaks no rule"
        ),
    }


def _prf(matched: int, n_found: int, n_expected: int) -> Dict[str, Any]:
    precision = (matched / n_found) if n_found else None
    recall = (matched / n_expected) if n_expected else None
    f1 = None
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    return {
        "n_expected": n_expected,
        "n_found": n_found,
        "n_matched": matched,
        "precision": None if precision is None else round(precision, 4),
        "recall": None if recall is None else round(recall, 4),
        "f1": None if f1 is None else round(f1, 4),
    }


def measure_responsibility(
    run_dir: Any,
    cfg: Optional[Config] = None,
) -> Dict[str, Any]:
    """Score the responsibility findings against the scenario design."""
    cfg = cfg if cfg is not None else Config({})
    layout = (
        run_dir if isinstance(run_dir, RunLayout) else RunLayout.from_run_dir(run_dir)
    )
    if not layout.responsibility_report.exists():
        return {
            "scored": False,
            "reason": "no responsibility report; the normative layer has not run",
        }

    report = read_json(layout.responsibility_report)
    design = (
        read_json(layout.scenario_design_graph)
        if layout.scenario_design_graph.exists() else None
    )
    findings = report.get("findings") or {}

    supported = sorted(
        pid for pid, f in findings.items()
        if f.get("responsibility_evidence") == "supported"
    )
    partial = sorted(
        pid for pid, f in findings.items()
        if f.get("responsibility_evidence") == "partial"
    )
    physical = sorted(
        pid for pid, f in findings.items()
        if f.get("physical_causal_contributor") == "yes"
    )

    designed = designed_contributors(design)
    if not designed["known"]:
        return {
            "scored": False,
            "reason": (
                "no scenario design reference for this run, so the findings "
                "cannot be compared with what was intended"
            ),
            "supported_contributors": supported,
            "partial_contributors": partial,
            "physical_contributors": physical,
        }

    manifest = read_json(layout.manifest) if layout.manifest.exists() else {}
    key = (str(manifest.get("scenario_id", "")), str(manifest.get("variant", "")))
    mechanism_executed = design.get("mechanism_executed")

    # --- physical: template causes against physical contributors ----------
    expected_physical = set(designed["physical"])
    found_physical = set(physical)

    # --- normative: designed omissions against supported contributions ----
    expected_normative = set(designed["normative"])
    found_supported = set(supported)
    normative_applicable = bool(designed["declares_any_normative_failing"])

    normative: Dict[str, Any] = {
        "applicable": normative_applicable,
        "designed": sorted(expected_normative),
        "supported": supported,
        "partial": partial,
    }
    if normative_applicable:
        normative.update({
            "sets": _prf(
                len(expected_normative & found_supported),
                len(found_supported), len(expected_normative),
            ),
            "exact_set_match": found_supported == expected_normative,
            "named_but_not_designed": sorted(found_supported - expected_normative),
            "designed_but_not_named": sorted(expected_normative - found_supported),
            "designed_but_named_partial": sorted(expected_normative & set(partial)),
        })
    else:
        normative["why_not"] = (
            "this scenario designs no normative failing -- it has no traffic "
            "control and no designed omission -- so there is nothing to score "
            "the responsibility findings against. A finding here is not a false "
            "positive against a reference that says nothing on the subject; it "
            "is a finding the design does not cover"
        )
        normative["findings_the_design_does_not_cover"] = supported

    return {
        "scored": True,
        "schema_version": SCHEMA_VERSIONS["evaluation"],
        # Carried so the campaign aggregate can name the hard cases rather than
        # reporting that some unidentified run got one backwards.
        "scenario": key[0],
        "variant": key[1],
        "physical": {
            "designed": sorted(expected_physical),
            "found": sorted(found_physical),
            "sets": _prf(
                len(expected_physical & found_physical),
                len(found_physical), len(expected_physical),
            ),
            "exact_set_match": found_physical == expected_physical,
            "found_but_not_designed": sorted(found_physical - expected_physical),
            "designed_but_not_found": sorted(expected_physical - found_physical),
        },
        "normative": normative,
        "evidence_classes": {
            pid: findings[pid].get("responsibility_evidence")
            for pid in sorted(findings)
        },
        "scenario_mechanism_executed": mechanism_executed,
        "mechanism_caveat": (
            None if mechanism_executed is not False else
            "the scenario's designed actions left no physical trace, so a "
            "disagreement here may be the scenario rather than the method"
        ),
        "hard_case": HARD_CASES.get(key),
        "note": (
            "scored against what the scenario intended, not against what "
            "happened. The weaker of the two references and reported apart for "
            "that reason. The physical and normative comparisons are separate "
            "because the template makes both kinds of claim and they are not "
            "interchangeable: a vehicle that brakes hard is a designed physical "
            "cause and breaks no rule"
        ),
    }


def aggregate_responsibility(
    per_run: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    """Campaign totals, summed from counts rather than averaged over runs.

    Averaging per-run ratios would weight a two-vehicle scenario the same as a
    three-vehicle one. Summing the counts and dividing once gives every
    participant equal weight, which is the question being asked.
    """
    scored = [r for r in per_run if r.get("scored")]
    if not scored:
        return {"scored": False, "reason": "no run could be scored", "n_runs": 0}

    expected = found = matched = 0
    exact = 0
    n_normative = 0
    for run in scored:
        sets = run["physical"]["sets"]
        expected += int(sets["n_expected"])
        found += int(sets["n_found"])
        matched += int(sets["n_matched"])
        exact += 1 if run["physical"]["exact_set_match"] else 0
        if run["normative"]["applicable"]:
            n_normative += 1

    # One explanation per scenario and variant. Repeating it once per seed makes
    # a three-seed campaign read as three separate findings.
    seen_hard = set()
    hard = [
        {
            "scenario": r.get("scenario"), "variant": r.get("variant"),
            "designed_physical": r["physical"]["designed"],
            "found_physical": r["physical"]["found"],
            "designed_normative": r["normative"]["designed"],
            "supported": r["normative"]["supported"],
            "why_it_is_hard": r["hard_case"],
        }
        for r in scored
        if r.get("hard_case")
        and (r.get("scenario"), r.get("variant")) not in seen_hard
        and not seen_hard.add((r.get("scenario"), r.get("variant")))
    ]

    # Normative totals over only the runs where a normative reference exists.
    n_expected = n_found = n_matched = 0
    for run in scored:
        if not run["normative"]["applicable"]:
            continue
        sets = run["normative"]["sets"]
        n_expected += int(sets["n_expected"])
        n_found += int(sets["n_found"])
        n_matched += int(sets["n_matched"])

    return {
        "scored": True,
        "n_runs": len(scored),
        "physical_contributor_sets": _prf(matched, found, expected),
        "n_exact_physical_match": exact,
        "exact_physical_match_rate": round(exact / len(scored), 4),
        "n_runs_with_a_normative_reference": n_normative,
        "normative_contributor_sets": (
            _prf(n_matched, n_found, n_expected) if n_normative else None
        ),
        "hard_cases": hard,
        "note": (
            "counts are summed across runs and divided once, so every "
            "participant weighs the same. The hard cases are listed "
            "individually because an aggregate can hide getting one backwards"
        ),
    }
