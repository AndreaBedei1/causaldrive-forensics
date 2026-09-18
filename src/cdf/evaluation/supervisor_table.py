"""One row per scenario, readable without knowing anything about the code.

The brief asks for this table by name and puts it above the aggregate metrics,
which is the right order. An F1 of 0.358 tells a reader how well the method did
on average and nothing about what it found; a row saying "B ran the stop sign, A
had priority, and removing B's roll-through averts the collision in 6 of 6
replays" tells them what the method is *for*.

Every cell is read from an artifact. Nothing is recomputed here, and nothing is
typed in. Where an artifact is missing the cell says so -- "not run" and "found
nothing" look identical in a table that fills gaps with dashes, and they are very
different findings.

## The columns, and what each is allowed to say

| Column | Source |
|---|---|
| what happened | the recorded outcome and the collisions in the merged log |
| reconstructed? | node and edge F1 against the observable ground truth |
| clock aligned? | the alignment status, and by what method |
| collision order | the order on the merged timeline, and whether it is right |
| signs detected? | perception recall, or why it was not measured |
| line evidence | what the onboard lane sensor reported |
| key formal violation | the first property that failed, by id and title |
| physical contributors | vehicles whose own behaviour reaches an outcome |
| responsibility contributors | those with a rule broken *and* a causal path |
| counterfactual validation | what the replays established, or that none ran |
| main limitation | the largest thing standing between this row and certainty |

The last column is the one worth defending. It is derived, not written: for each
run the code asks which of a fixed list of conditions holds -- no common clock,
no camera, an ambiguous contact match, an undecidable property, no replays -- and
names the most serious. A limitation column filled in by hand would drift out of
step with the artifacts within a week.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.io import read_json, write_csv
from ..common.layout import RunLayout
from ..common.schemas import SCHEMA_VERSIONS, CheckStatus

LOGGER = logging.getLogger(__name__)

__all__ = ["SUPERVISOR_COLUMNS", "build_supervisor_rows", "format_supervisor_table"]

SUPERVISOR_COLUMNS: Tuple[str, ...] = (
    "scenario",
    "variant",
    "seed",
    "what_happened",
    "reconstructed",
    "clock_aligned",
    "collision_order",
    "signs_detected",
    "line_evidence",
    "key_formal_violation",
    "physical_contributors",
    "responsibility_contributors",
    "counterfactual_validation",
    "main_limitation",
)

#: Checked in order; the first that holds is the row's main limitation. Ordered
#: by how much it undermines the row: a run with no common clock has no merged
#: timeline at all, which matters more than an undecided property.
_LIMITATIONS: Tuple[Tuple[str, str], ...] = (
    ("no_common_clock",
     "no shared contact, so the recorders were never on one timeline"),
    ("harness_clock",
     "common time came from the experiment harness, not from the vehicles"),
    ("ambiguous_contact",
     "which impact is which could not be decided from the recordings"),
    ("partial_alignment",
     "at least one recorder could not be tied to the others"),
    ("no_camera",
     "recorded without a camera, so no sign or stop-line evidence exists"),
    ("no_counterfactual",
     "no replays, so but-for causation was neither established nor ruled out"),
    ("undecided_property",
     "a safety property could not be decided within the recorded window"),
    ("shared_anchor",
     "one impact related two recorders, so one offset carries a bounded error"),
)


def _maybe(path) -> Optional[Dict[str, Any]]:
    return read_json(path) if path.exists() else None


def _what_happened(manifest: Mapping[str, Any],
                   global_log: Optional[Mapping[str, Any]]) -> str:
    outcome = str(manifest.get("outcome", "unknown")).replace("_", " ")
    if not global_log:
        return outcome
    collisions = [
        r for r in global_log.get("rows", []) or []
        if r.get("event_type") == "COLLISION"
    ]
    if not collisions:
        return outcome
    # A collision is a fact about two vehicles. One recorded without a resolved
    # subject is a vehicle that felt an impact whose counterparty fusion could
    # not name, and rendering it as a one-sided "pair" would read as a vehicle
    # colliding with itself.
    pairs: List[str] = []
    unpaired = 0
    for row in collisions:
        who, other = row.get("participant"), row.get("subject")
        if not who or not other:
            unpaired += 1
            continue
        pair = "-".join(sorted([str(who), str(other)]))
        if pair not in pairs:
            pairs.append(pair)
    described = ", ".join(pairs) if pairs else "counterparty unresolved"
    if unpaired:
        described += ", {0} impact(s) with no counterparty resolved".format(unpaired)
    return "{0}: {1}".format(outcome, described)


def _pair(row_or_event: Mapping[str, Any]) -> Optional[str]:
    """The unordered pair an impact record names, or ``None`` if it names one."""
    who = row_or_event.get("participant") or row_or_event.get("participant_id")
    other = row_or_event.get("subject")
    if not who or not other:
        return None
    return "-".join(sorted([str(who), str(other)]))


def _ordered_pairs(records: Sequence[Mapping[str, Any]], time_key: str) -> List[str]:
    """Distinct impact pairs in the order they occurred, first occurrence wins."""
    out: List[str] = []
    for record in sorted(records, key=lambda r: float(r.get(time_key) or 0.0)):
        pair = _pair(record)
        if pair and pair not in out:
            out.append(pair)
    return out


def _collision_order(
    global_log: Optional[Mapping[str, Any]],
    observable: Optional[Mapping[str, Any]],
    alignment: Optional[Mapping[str, Any]] = None,
) -> str:
    """The order the reconstruction put the impacts in, and whether it is right.

    This is the question §18's multi-impact property deliberately could not
    answer: a consistently wrong order is still self-consistent, so nothing
    inside the trace can catch it. Only the privileged record can, which is why
    it is a metric rather than a property.

    A single-impact run has no order to get wrong and says so, rather than
    reporting a trivially correct one and inflating the column.
    """
    if not global_log:
        return "not fused"
    rows = [
        r for r in global_log.get("rows", []) or []
        if r.get("event_type") == "COLLISION"
    ]
    # The merged log is on common time where it exists and local time where it
    # does not; either way the ordering within one log is what was reconstructed.
    key = "t_common" if any(r.get("t_common") is not None for r in rows) else "t_local"
    reconstructed = _ordered_pairs(rows, key)
    if not reconstructed:
        return "no impact"
    if len(reconstructed) == 1:
        return "single impact ({0})".format(reconstructed[0])

    # An order built on a suspect offset is not an order this method established,
    # however confidently the timestamps happen to be sorted. On a recorded chain
    # the middle vehicle registered one impact and its anchor related both
    # neighbours, which put the second vehicle 200 ms out and flipped two impacts
    # that were 200 ms apart. The column has to say so, or the reader takes an
    # artefact of a shared anchor for a finding.
    suspect = sorted({
        p for caveat in ((alignment or {}).get("shared_anchor_caveats") or [])
        for p in (caveat.get("participants_with_suspect_offset") or [])
    })
    qualifier = ""
    if suspect and any(
        p in pair.split("-") for pair in reconstructed for p in suspect
    ):
        qualifier = (
            "; not established -- {0} offset rests on a shared anchor".format(
                ", ".join(suspect)
            )
        )

    order = " then ".join(reconstructed)
    truth = _ordered_pairs(
        [e for e in (observable or {}).get("events", []) or []
         if e.get("event_type") == "COLLISION"],
        "t_peak",
    ) if observable else []
    if not truth:
        return "{0} (no reference to check against{1})".format(order, qualifier)
    verdict = "correct" if reconstructed == truth else "WRONG, truth {0}".format(
        " then ".join(truth)
    )
    return "{0} ({1}{2})".format(order, verdict, qualifier)


def _line_evidence(
    layout: RunLayout, participants: Sequence[str]
) -> str:
    """What the onboard lane sensor reported, per vehicle.

    Reported rather than scored: the lane sensor *is* the measurement, and there
    is no separate privileged marking-crossing record to compare it against. A
    run recorded without one says so instead of showing a zero, which would read
    as a vehicle that crossed nothing.
    """
    seen = False
    counts: Dict[str, int] = {}
    for pid in participants:
        path = layout.lane_events(pid)
        if not path.exists():
            continue
        seen = True
        payload = read_json(path)
        for event in payload.get("events", []) or []:
            key = str(event.get("event_type", ""))
            counts[key] = counts.get(key, 0) + 1
    if not seen:
        return "no lane sensor"
    if not counts:
        return "no crossing reported"
    order = ("SOLID_LINE_CROSSED", "LANE_MARKING_CROSSED", "ROAD_BOUNDARY_CROSSED")
    parts = [
        "{0} x{1}".format(k.replace("_CROSSED", "").lower().replace("_", " "), counts[k])
        for k in order if k in counts
    ]
    return ", ".join(parts)


def _reconstructed(metrics: Optional[Mapping[str, Any]]) -> str:
    block = (metrics or {}).get("observable_comparison")
    if not block:
        return "not scored"
    accounts = block.get("accounts") or {}
    best = accounts.get("global_inferred") or accounts.get("simple_fusion")
    if not best or not best.get("scored"):
        return "not scored"
    nodes = best.get("nodes") or {}
    edges = best.get("edges") or {}
    return "nodes {0:.2f} / edges {1:.2f}".format(
        float(nodes.get("f1") or 0.0), float(edges.get("f1") or 0.0)
    )


def _clock(alignment: Optional[Mapping[str, Any]]) -> str:
    if not alignment:
        return "not fused"
    status = str(alignment.get("status", "?"))
    method = str(alignment.get("method", ""))
    if method == "acquisition_start_marker":
        return "harness marker (not contact)"
    n = alignment.get("n_shared_contacts") or 0
    return "{0} ({1} shared contact{2})".format(
        status.replace("_", " ").lower(), n, "" if n == 1 else "s"
    )


def _signs(perception: Optional[Mapping[str, Any]]) -> str:
    if not perception:
        return "not measured"
    if not perception.get("scored"):
        return "not measured"
    block = perception.get("signs") or {}
    if not block.get("n_real"):
        return "no signs in this scenario"
    recall = block.get("recall")
    return "{0}/{1} found".format(block.get("n_matched", 0), block["n_real"]) + (
        "" if recall is None else " (recall {0:.2f})".format(float(recall))
    )


def _formal(formal: Optional[Mapping[str, Any]]) -> str:
    if not formal:
        return "not checked"
    failures = [
        r for r in formal.get("results", []) or []
        if r.get("status") == CheckStatus.FAIL.value and not r.get("vacuous")
    ]
    if not failures:
        summary = formal.get("summary") or {}
        if summary.get("n_unknown"):
            return "none failed ({0} undecided)".format(summary["n_unknown"])
        return "none"
    first = failures[0]
    extra = " (+{0} more)".format(len(failures) - 1) if len(failures) > 1 else ""
    return "{0}: {1}{2}".format(first["property_id"], first.get("title", ""), extra)


def _contributors(report: Optional[Mapping[str, Any]]) -> Tuple[str, str]:
    if not report:
        return "not analysed", "not analysed"
    findings = report.get("findings") or {}
    physical = sorted(
        pid for pid, f in findings.items()
        if f.get("physical_causal_contributor") == "yes"
    )
    supported = sorted(
        pid for pid, f in findings.items()
        if f.get("responsibility_evidence") == "supported"
    )
    partial = sorted(
        pid for pid, f in findings.items()
        if f.get("responsibility_evidence") == "partial"
    )
    responsibility = ", ".join(supported) if supported else "none supported"
    if partial:
        responsibility += " ({0} partial)".format(", ".join(partial))
    return (", ".join(physical) or "none"), responsibility


def _counterfactual(report: Optional[Mapping[str, Any]]) -> str:
    if not report:
        return "not analysed"
    findings = report.get("findings") or {}
    established = sorted(
        pid for pid, f in findings.items()
        if (f.get("but_for_contribution") or {}).get("verdict") == "yes"
    )
    tested = [
        pid for pid, f in findings.items()
        if (f.get("but_for_contribution") or {}).get("verdict") in ("yes", "no")
    ]
    if not tested:
        return "not tested"
    if not established:
        return "tested, none established"
    return "but-for established for {0}".format(", ".join(established))


def _limitation(
    alignment: Optional[Mapping[str, Any]],
    perception: Optional[Mapping[str, Any]],
    formal: Optional[Mapping[str, Any]],
    report: Optional[Mapping[str, Any]],
) -> str:
    """The most serious thing standing between this row and certainty.

    Derived rather than written. A hand-filled limitation column drifts out of
    step with the artifacts within a week, and then reads as reassurance.
    """
    status = str((alignment or {}).get("status", ""))
    method = str((alignment or {}).get("method", ""))
    flags = {
        "no_common_clock": (
            alignment is not None and not (alignment.get("offsets_s") or {})
        ),
        "harness_clock": method == "acquisition_start_marker",
        "ambiguous_contact": status == "AMBIGUOUS_CONTACT_MATCH",
        "partial_alignment": status == "PARTIALLY_ALIGNED",
        "no_camera": (
            perception is not None and not perception.get("scored")
            and "without a camera" in str(perception.get("reason", ""))
        ),
        "no_counterfactual": _counterfactual(report) == "not tested",
        "undecided_property": bool(
            ((formal or {}).get("summary") or {}).get("n_unknown")
        ),
        "shared_anchor": bool((alignment or {}).get("shared_anchor_caveats")),
    }
    for key, text in _LIMITATIONS:
        if flags.get(key):
            return text
    return "none identified"


def build_supervisor_rows(
    artifacts_root: Any,
    cfg: Optional[Config] = None,
) -> List[Dict[str, Any]]:
    """One row per run, read from artifacts and sorted for reading."""
    from pathlib import Path

    root = Path(artifacts_root)
    rows: List[Dict[str, Any]] = []
    for manifest_path in sorted(root.glob("*/*/manifest.json")):
        layout = RunLayout.from_run_dir(manifest_path.parent)
        manifest = read_json(manifest_path)
        alignment = _maybe(layout.clock_alignment)
        global_log = _maybe(layout.global_log)
        metrics = _maybe(layout.metrics)
        perception = _maybe(layout.perception_metrics)
        formal = _maybe(layout.formal_results)
        report = _maybe(layout.responsibility_report)

        observable = _maybe(layout.observable_events)
        physical, responsibility = _contributors(report)
        rows.append({
            "scenario": str(manifest.get("scenario_id", "")),
            "variant": str(manifest.get("variant", "")),
            "seed": manifest.get("seed"),
            "what_happened": _what_happened(manifest, global_log),
            "reconstructed": _reconstructed(metrics),
            "clock_aligned": _clock(alignment),
            "collision_order": _collision_order(global_log, observable, alignment),
            "signs_detected": _signs(perception),
            "line_evidence": _line_evidence(layout, layout.participant_ids()),
            "key_formal_violation": _formal(formal),
            "physical_contributors": physical,
            "responsibility_contributors": responsibility,
            "counterfactual_validation": _counterfactual(report),
            "main_limitation": _limitation(alignment, perception, formal, report),
        })

    rows.sort(key=lambda r: (r["scenario"], r["variant"], r["seed"] or 0))
    return rows


def format_supervisor_table(rows: Sequence[Mapping[str, Any]]) -> str:
    """The table as markdown, which is what goes in front of a reader."""
    if not rows:
        return (
            "No runs found. The table is generated from recorded artifacts; an "
            "empty one means no campaign has been recorded, not that a campaign "
            "found nothing."
        )
    headers = [c.replace("_", " ") for c in SUPERVISOR_COLUMNS]
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(
            str(row.get(c, "")) for c in SUPERVISOR_COLUMNS
        ) + " |")
    return "\n".join(lines)


def write_supervisor_table(
    artifacts_root: Any,
    publish_dir: Any = "results",
    cfg: Optional[Config] = None,
) -> Dict[str, Any]:
    """Build the table and write it as CSV and markdown."""
    from pathlib import Path

    rows = build_supervisor_rows(artifacts_root, cfg)
    out = Path(publish_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "supervisor_table.csv", rows, SUPERVISOR_COLUMNS)
    (out / "supervisor_table.md").write_text(
        "# Per-scenario findings\n\n"
        "Generated from artifacts by `cdf.evaluation.supervisor_table`. Every\n"
        "cell is read from a file; where one is missing the cell says so rather\n"
        "than showing a dash, because \"not run\" and \"found nothing\" are\n"
        "different findings.\n\n"
        + format_supervisor_table(rows) + "\n",
        encoding="utf-8",
    )
    return {
        "schema_version": SCHEMA_VERSIONS["evaluation"],
        "n_rows": len(rows),
        "columns": list(SUPERVISOR_COLUMNS),
        "rows": rows,
    }
