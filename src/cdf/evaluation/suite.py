"""End-to-end evaluation of one run, and aggregation across a whole campaign.

EVALUATION LAYER -- reads both the inference side and the oracle side.

This module is the only place that opens local, fused *and* oracle artifacts in
one process. Two invariants keep that from becoming a leak:

1. **Read-only towards inference.** Everything produced here is written under the
   run's ``evaluation/`` directory (and, for a campaign, under
   ``artifacts/summary/``). Nothing is ever written back into ``vehicle_*/`` or
   ``fusion/``: an evaluation that edited the thing it scores would destroy the
   provenance chain the whole project rests on. :func:`_assert_evaluation_path`
   enforces this rather than trusting the call sites.
2. **Absent is not zero.** Every metric block is computed only when its inputs
   exist. When they do not, the block is ``None`` and an entry appears in
   ``reasons`` saying exactly which artifact was missing. A run whose oracle
   graph was never built must not be reported as a reconstruction that scored
   0.0 -- that is a fabricated experimental result, and it would silently drag
   every campaign average down.

Concretely: a run whose oracle graphs have not been built
(:func:`cdf.oracle.graph.build_and_persist`) reports the event, graph-structure
and fusion-benefit blocks as ``None`` with a reason naming the missing file,
while association, model checking and scenario validation still carry real
numbers. The evaluation layer never builds those oracle artifacts itself -- that
would put a privileged producer inside the scorer.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from ..common.config import Config, deep_merge
from ..common.evidence import RunEvidence, load_run
from ..common.io import read_json, write_csv, write_json
from ..common.layout import RunLayout
from ..common.schemas import (
    SCHEMA_VERSIONS,
    Event,
    GraphDocument,
    Provenance,
    _event_from_dict,  # private decoder, shared with cdf.common.evidence
)
from ..graph.export import graph_summary, load_graph
from ..oracle.events import load_oracle_trace
from . import tables
from .association_metrics import evaluate_association
from .attribution_metrics import evaluate_attribution, evaluate_local_unknowns
from .event_metrics import evaluate_events
from .graph_metrics import evaluate_graphs, fusion_benefit
from .clocks import load_clock_truth, simulator_evidence, map_event, map_graph, evaluate_clock_alignment

LOGGER = logging.getLogger(__name__)

__all__ = ["evaluate_run", "aggregate_runs", "summary_dir"]

PathLike = Union[str, Path]

#: Blocks reported in ``metrics.json``. Every one of them is either a mapping or
#: ``None`` with an entry in ``reasons``; none of them is ever a zero-filled
#: stand-in for an absent input.
_BLOCKS = (
    "clock_alignment",
    "events",
    "graphs",
    "fusion_benefit",
    "association",
    "attribution",
    "local_unknowns",
    "model_check",
    "scenario_validation",
)


def summary_dir(artifacts_root: PathLike) -> Path:
    """The campaign-level output directory, ``<artifacts_root>/summary``.

    :class:`cdf.common.layout.RunLayout` describes a single run and has no
    campaign-level concept, so this one path lives here (reported as a contract
    issue rather than hardcoded at each call site).
    """
    return Path(artifacts_root) / "summary"


def _assert_evaluation_path(layout: RunLayout, path: Path) -> Path:
    """Refuse to write anywhere but the run's own ``evaluation/`` directory."""
    try:
        path.resolve().relative_to(layout.evaluation_dir.resolve())
    except ValueError:
        raise ValueError(
            "the evaluation layer may only write under {0}; refused {1}".format(
                layout.evaluation_dir, path
            )
        )
    return path


# ---------------------------------------------------------------------------
# Artifact loading
# ---------------------------------------------------------------------------


def _load_events_file(path: Path) -> List[Event]:
    """Decode an ``events``-shaped JSON document into :class:`Event` records."""
    payload = read_json(path)
    return [_event_from_dict(d) for d in payload.get("events", []) or []]


def _scenario_block(cfg: Config, variant: Optional[str]) -> Optional[Dict[str, Any]]:
    """The scenario definition with its variant merged in, as a plain mapping.

    A mapping rather than a :class:`~cdf.simulation.scenario_base.ScenarioSpec`:
    the fields this layer needs (``causal_template``,
    ``expected_local_unknowns``) are declarative, and reading them from the
    configuration means the evaluation layer never imports the simulation layer
    just to answer a question about a YAML file.
    """
    block = cfg.get("scenario", None)
    if not isinstance(block, Mapping):
        return None
    merged = dict(block)
    variants = merged.get("variants", {}) or {}
    if variant and variant in variants:
        merged = deep_merge(merged, variants[variant] or {})
    return merged


def _load_run_inputs(layout: RunLayout, cfg: Config, spec: Any) -> Dict[str, Any]:
    """Open every artifact the evaluation might need, recording what is absent."""
    manifest: Dict[str, Any] = read_json(layout.manifest) if layout.manifest.exists() else {}
    run: RunEvidence = load_run(layout.root, with_radar=False)

    local_causal: Dict[str, GraphDocument] = {}
    local_event: Dict[str, GraphDocument] = {}
    local_events: Dict[str, List[Event]] = {}
    local_event_source: Dict[str, str] = {}
    for pid in layout.participant_ids():
        if layout.causal_graph(pid).exists():
            local_causal[pid] = load_graph(
                layout.causal_graph(pid), expect_scope=Provenance.LOCAL
            )
        if layout.event_graph(pid).exists():
            local_event[pid] = load_graph(
                layout.event_graph(pid), expect_scope=Provenance.LOCAL
            )
        # ``events.json`` is written by the recorder before extraction and can
        # legitimately be empty while the extracted events live on as the nodes of
        # the event graph. Falling back keeps the event metrics measuring the
        # reconstruction rather than an artifact-writing order, and the source
        # actually used is recorded so a reader can tell which it was.
        events = list(run.get(pid).events) if pid in run.participants else []
        source = "events.json"
        if not events and pid in local_event:
            events, source = list(local_event[pid].nodes), "event_graph.json"
        elif not events and pid in local_causal:
            events, source = list(local_causal[pid].nodes), "causal_graph.json"
        local_events[pid] = events
        local_event_source[pid] = source if events else "none"

    fused_causal: Optional[GraphDocument] = None
    if layout.fused_causal_graph.exists():
        fused_causal = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)
    fused_event: Optional[GraphDocument] = None
    if layout.fused_event_graph.exists():
        fused_event = load_graph(layout.fused_event_graph, expect_scope=Provenance.FUSED)
    fused_events: List[Event] = (
        _load_events_file(layout.fused_events) if layout.fused_events.exists() else []
    )

    oracle_causal: Optional[GraphDocument] = None
    if layout.oracle_causal_graph.exists():
        oracle_causal = load_graph(layout.oracle_causal_graph, expect_scope=Provenance.ORACLE)
    oracle_events: List[Event] = []
    if layout.oracle_events.exists():
        oracle_events = _load_events_file(layout.oracle_events)
    elif oracle_causal is not None:
        oracle_events = list(oracle_causal.nodes)

    # The privileged trace is read through the oracle layer's own loader, so the
    # evaluation never invents a second interpretation of ground truth.
    oracle_trace: Optional[Dict[str, Any]] = None
    if layout.oracle_trace.exists() and (layout.oracle_dir / "oracle_summary.json").exists():
        oracle_trace = load_oracle_trace(layout.root)

    subject_map: Dict[str, str] = {}
    assignments: Optional[List[Dict[str, Any]]] = None
    if layout.fusion_diagnostics.exists():
        diagnostics = read_json(layout.fusion_diagnostics)
        subject_map = dict(diagnostics.get("subject_map", {}) or {})
    if layout.association_report.exists():
        assignments = list(read_json(layout.association_report).get("assignments", []) or [])

    model_check: Optional[Dict[str, Any]] = (
        read_json(layout.model_check_results) if layout.model_check_results.exists() else None
    )
    attribution: Optional[Dict[str, Any]] = None
    if layout.causal_contribution.exists():
        attribution = read_json(layout.causal_contribution)
    elif layout.counterfactual_manifest.exists():
        attribution = read_json(layout.counterfactual_manifest)

    validation: Optional[Dict[str, Any]] = (
        read_json(layout.scenario_validation) if layout.scenario_validation.exists() else None
    )

    variant = str(manifest.get("variant", "")) or None
    resolved_spec = spec if spec is not None else _scenario_block(cfg, variant)

    # Evaluation alone can convert recorder/common times to oracle physical time.
    # These detached copies are never written back into inference artifacts.
    truth = load_clock_truth(layout)
    alignment_path = layout.fusion_dir / "time_alignment.json"
    alignment = read_json(alignment_path) if alignment_path.exists() else {}
    time_scoring_reason = None
    if manifest.get("clock_protocol") == "independent_local_clocks" and (
        set(truth) != set(run.participant_ids) or alignment.get("reference") not in truth
    ):
        time_scoring_reason = (
            "independent-clock scoring requires all oracle clock profiles and an "
            "estimated reference; raw/common times cannot be compared to simulator time"
        )
    if truth:
        run = simulator_evidence(run, truth)
        for pid, profile in truth.items():
            a = 1.0 / float(profile["true_scale"])
            b = -float(profile["true_offset_s"]) * a
            if pid in local_causal:
                local_causal[pid] = map_graph(local_causal[pid], a, b)
            if pid in local_event:
                local_event[pid] = map_graph(local_event[pid], a, b)
            if pid in local_events:
                local_events[pid] = [map_event(e, a, b) for e in local_events[pid]]
        profile = truth.get(alignment.get("reference"))
        if profile:
            a = 1.0 / float(profile["true_scale"])
            b = -float(profile["true_offset_s"]) * a
            fused_causal = map_graph(fused_causal, a, b)
            fused_event = map_graph(fused_event, a, b)
            fused_events = [map_event(e, a, b) for e in fused_events]

    return {
        "manifest": manifest,
        "run": run,
        "local_causal": local_causal,
        "local_event": local_event,
        "local_events": local_events,
        "local_event_source": local_event_source,
        "fused_causal": fused_causal,
        "fused_event": fused_event,
        "fused_events": fused_events,
        "oracle_causal": oracle_causal,
        "oracle_events": oracle_events,
        "oracle_trace": oracle_trace,
        "subject_map": subject_map,
        "assignments": assignments,
        "model_check": model_check,
        "attribution": attribution,
        "scenario_validation": validation,
        "spec": resolved_spec,
        "variant": variant or "",
        "clock_alignment": evaluate_clock_alignment(alignment, truth),
        "clock_protocol": manifest.get("clock_protocol", "synchronized_clock_baseline"),
        "time_scoring_reason": time_scoring_reason,
    }


# ---------------------------------------------------------------------------
# Per-run evaluation
# ---------------------------------------------------------------------------


def _model_check_block(payload: Mapping[str, Any]) -> Dict[str, Any]:
    """Condense a model-checking report to the counts the tables need.

    ``UNKNOWN`` is carried through as its own count, never folded into ``PASS``:
    the three-valued monitor exists precisely so that "the evidence could not
    decide" survives into the results.
    """
    results = list(payload.get("results", []) or [])
    counts: Dict[str, int] = {}
    for r in results:
        status = str(r.get("status", "UNKNOWN"))
        counts[status] = counts.get(status, 0) + 1
    return {
        "n_results": len(results),
        "counts": counts,
        "by_participant": payload.get("by_participant", {}) or {},
        "by_property": {
            pid: block.get("summary", {})
            for pid, block in (payload.get("by_property", {}) or {}).items()
        },
        "results": [
            {
                "property_id": r.get("property_id"),
                "participant_id": r.get("participant_id"),
                "status": r.get("status"),
                "reason": r.get("reason", ""),
            }
            for r in results
        ],
    }


def evaluate_run(
    run_dir: PathLike, cfg: Config, spec: Any = None
) -> Dict[str, Any]:
    """Evaluate one recorded run and persist the result under ``evaluation/``.

    Parameters
    ----------
    run_dir:
        A ``seed_xxx`` run directory produced by the simulation and analysis
        stages.
    cfg:
        The resolved run configuration; supplies every tolerance and, when
        ``spec`` is omitted, the scenario block used for attribution ground truth.
    spec:
        Optional scenario specification (a
        :class:`~cdf.simulation.scenario_base.ScenarioSpec` or the raw scenario
        mapping). Omit it to take the scenario block straight from ``cfg``.

    Returns
    -------
    dict
        The mapping written to ``evaluation/metrics.json``. Blocks whose inputs
        were absent are ``None`` and named in ``reasons``.
    """
    layout = RunLayout.from_run_dir(run_dir)
    if not layout.root.exists():
        raise FileNotFoundError("run directory does not exist: {0}".format(layout.root))

    data = _load_run_inputs(layout, cfg, spec)
    manifest = data["manifest"]
    run: RunEvidence = data["run"]

    metrics: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSIONS["evaluation"],
        "run_dir": layout.root.name,
        "run_path": layout.root.as_posix(),
        "run_id": str(manifest.get("run_id", "")),
        "scenario_id": str(manifest.get("scenario_id", "")),
        "variant": data["variant"],
        "seed": int(manifest.get("seed", 0)),
        "outcome": str(manifest.get("outcome", "")),
        "config_hash": cfg.hash,
        "n_participants": len(run.participant_ids),
        "participants": list(run.participant_ids),
        "subject_map": dict(sorted(data["subject_map"].items())),
    }
    reasons: Dict[str, str] = {}
    for name in _BLOCKS:
        metrics[name] = None
    metrics["clock_alignment"] = data["clock_alignment"]
    metrics["clock_protocol"] = data["clock_protocol"]
    if metrics["clock_alignment"] is None:
        reasons["clock_alignment"] = "clock ground truth or estimated reference absent; legacy synchronized baseline is not a clock-estimation measurement"

    # --- always-available structural summary (no oracle needed) ----------
    metrics["reconstruction"] = {
        "local_causal": {
            pid: graph_summary(doc) for pid, doc in sorted(data["local_causal"].items())
        },
        "local_event": {
            pid: graph_summary(doc) for pid, doc in sorted(data["local_event"].items())
        },
        "fused_causal": (
            graph_summary(data["fused_causal"]) if data["fused_causal"] is not None else None
        ),
        "fused_event": (
            graph_summary(data["fused_event"]) if data["fused_event"] is not None else None
        ),
        "n_local_events": {pid: len(ev) for pid, ev in sorted(data["local_events"].items())},
        "local_event_source": dict(sorted(data["local_event_source"].items())),
        "n_fused_events": len(data["fused_events"]),
        "evidence": {pid: run.get(pid).summary() for pid in run.participant_ids},
    }

    # --- events -----------------------------------------------------------
    if data["time_scoring_reason"]:
        reasons["events"] = data["time_scoring_reason"]
    elif not data["oracle_events"]:
        reasons["events"] = (
            "no oracle event list: neither {0} nor {1} exists".format(
                layout.oracle_events.name, layout.oracle_causal_graph.name
            )
        )
    elif not data["local_events"]:
        reasons["events"] = "no participant produced a local event list"
    else:
        metrics["events"] = evaluate_events(
            data["local_events"],
            data["fused_events"],
            data["oracle_events"],
            data["subject_map"],
            cfg,
        )

    # --- graph structure --------------------------------------------------
    if data["time_scoring_reason"]:
        reasons["graphs"] = data["time_scoring_reason"]
        reasons["fusion_benefit"] = reasons["graphs"]
    elif data["oracle_causal"] is None:
        reasons["graphs"] = "no oracle causal graph at {0}".format(
            layout.oracle_causal_graph.as_posix()
        )
        reasons["fusion_benefit"] = reasons["graphs"]
    elif not data["local_causal"]:
        reasons["graphs"] = "no local causal graph was persisted for any participant"
        reasons["fusion_benefit"] = reasons["graphs"]
    else:
        metrics["graphs"] = evaluate_graphs(
            data["local_causal"],
            data["fused_causal"],
            data["oracle_causal"],
            data["subject_map"],
            cfg,
        )
        if data["fused_causal"] is None:
            reasons["fusion_benefit"] = "no fused causal graph at {0}".format(
                layout.fused_causal_graph.as_posix()
            )
        else:
            metrics["fusion_benefit"] = fusion_benefit(
                data["local_causal"],
                data["fused_causal"],
                data["oracle_causal"],
                cfg,
                subject_map=data["subject_map"],
            )

    # --- association ------------------------------------------------------
    if data["time_scoring_reason"]:
        reasons["association"] = data["time_scoring_reason"]
    elif data["assignments"] is None:
        reasons["association"] = "no association report at {0}".format(
            layout.association_report.as_posix()
        )
    elif not data["oracle_trace"]:
        reasons["association"] = "no privileged trace at {0}; true track identity is unknown".format(
            layout.oracle_trace.as_posix()
        )
    else:
        metrics["association"] = evaluate_association(
            data["assignments"], run, data["oracle_trace"], cfg
        )

    # --- attribution ------------------------------------------------------
    if data["attribution"] is None:
        reasons["attribution"] = (
            "no counterfactual attribution artifact ({0} / {1})".format(
                layout.causal_contribution.name, layout.counterfactual_manifest.name
            )
        )
    elif data["spec"] is None:
        reasons["attribution"] = (
            "no scenario specification: the oracle's causal initiators are declared "
            "by the scenario's causal_template"
        )
    else:
        metrics["attribution"] = evaluate_attribution(
            data["attribution"], data["oracle_causal"], data["spec"], cfg
        )

    # --- epistemic honesty -----------------------------------------------
    unknown_names = _expected_local_unknowns(data["spec"])
    if data["spec"] is None:
        reasons["local_unknowns"] = "no scenario specification was available"
    elif not unknown_names:
        reasons["local_unknowns"] = "scenario declares no expected_local_unknowns"
    else:
        scanned: Dict[str, GraphDocument] = {}
        for pid, doc in data["local_causal"].items():
            scanned["causal:{0}".format(pid)] = doc
        for pid, doc in data["local_event"].items():
            scanned["event:{0}".format(pid)] = doc
        metrics["local_unknowns"] = evaluate_local_unknowns(
            data["spec"],
            scanned,
            data["fused_causal"],
            data["model_check"],
            cfg,
            oracle_doc=data["oracle_causal"],
        )

    # --- model checking ---------------------------------------------------
    if data["model_check"] is None:
        reasons["model_check"] = "no model-check results at {0}".format(
            layout.model_check_results.as_posix()
        )
    else:
        metrics["model_check"] = _model_check_block(data["model_check"])

    # --- scenario validation ---------------------------------------------
    if data["scenario_validation"] is None:
        reasons["scenario_validation"] = "no scenario validation at {0}".format(
            layout.scenario_validation.as_posix()
        )
    else:
        metrics["scenario_validation"] = data["scenario_validation"]

    metrics["reasons"] = dict(sorted(reasons.items()))
    metrics["available"] = {name: metrics[name] is not None for name in _BLOCKS}

    _persist(layout, metrics)
    LOGGER.info(
        "evaluated %s: %d/%d metric blocks available (%s unavailable)",
        layout.root.name,
        sum(1 for v in metrics["available"].values() if v),
        len(_BLOCKS),
        ", ".join(sorted(reasons)) or "none",
    )
    return metrics


def _expected_local_unknowns(spec: Any) -> List[str]:
    if spec is None:
        return []
    if isinstance(spec, Mapping):
        values = spec.get("expected_local_unknowns", []) or []
    else:
        values = getattr(spec, "expected_local_unknowns", []) or []
    return [str(v) for v in values]


def _persist(layout: RunLayout, metrics: Mapping[str, Any]) -> None:
    """Write the four evaluation artifacts, all inside ``evaluation/``."""
    layout.evaluation_dir.mkdir(parents=True, exist_ok=True)
    write_json(_assert_evaluation_path(layout, layout.metrics), metrics)
    write_csv(
        _assert_evaluation_path(layout, layout.event_matches),
        tables.event_match_rows(metrics),
        tables.EVENT_MATCH_COLUMNS,
    )
    write_csv(
        _assert_evaluation_path(layout, layout.edge_matches),
        tables.edge_match_rows(metrics),
        tables.EDGE_MATCH_COLUMNS,
    )
    write_json(
        _assert_evaluation_path(layout, layout.attribution_metrics),
        {
            "schema_version": SCHEMA_VERSIONS["evaluation"],
            "run_id": metrics.get("run_id", ""),
            "scenario_id": metrics.get("scenario_id", ""),
            "variant": metrics.get("variant", ""),
            "seed": metrics.get("seed", 0),
            "attribution": metrics.get("attribution"),
            "local_unknowns": metrics.get("local_unknowns"),
            "reasons": {
                k: v
                for k, v in (metrics.get("reasons") or {}).items()
                if k in ("attribution", "local_unknowns")
            },
        },
    )


# ---------------------------------------------------------------------------
# Campaign aggregation
# ---------------------------------------------------------------------------


#: Where a run sits in the artifacts tree is what it is.
RUN_KIND_PRIMARY = "primary"
RUN_KIND_REPLAY = "replay"
RUN_KIND_ABLATION = "ablation"


def run_kind(run_dir: Path, artifacts_root: Path) -> str:
    """Classify a run by its location: campaign run, replay, or ablation.

    A counterfactual replay lives under ``<run>/counterfactual/replays/<id>``
    and an ablation run under ``<artifacts>/ablation/<profile>``. Both carry a
    ``manifest.json`` and both are genuine runs, but neither is part of the
    recorded campaign: a replay is deliberately a *different* experiment from
    the run it replays, and an ablation run deliberately degrades the sensor.
    Averaging either into the campaign tables would be adding up experiments
    that were built to differ.
    """
    try:
        parts = run_dir.resolve().relative_to(artifacts_root.resolve()).parts
    except ValueError:
        return RUN_KIND_PRIMARY
    if "counterfactual" in parts:
        return RUN_KIND_REPLAY
    if parts and parts[0] == "ablation":
        return RUN_KIND_ABLATION
    return RUN_KIND_PRIMARY


def _run_dirs(
    artifacts_root: Path, kinds: Sequence[str] = (RUN_KIND_PRIMARY,)
) -> List[Path]:
    """Run directories under ``artifacts_root`` of the requested kinds."""
    summary = summary_dir(artifacts_root).resolve()
    out: List[Path] = []
    for manifest in sorted(artifacts_root.rglob("manifest.json")):
        parent = manifest.parent.resolve()
        if parent == summary or summary in parent.parents:
            continue
        if run_kind(manifest.parent, artifacts_root) not in kinds:
            continue
        out.append(manifest.parent)
    return out


def aggregate_runs(artifacts_root: PathLike, cfg: Config) -> Dict[str, Any]:
    """Collect every run's ``metrics.json`` into the campaign tables.

    Writes ``runs.csv``, ``event_metrics.csv``, ``graph_metrics.csv``,
    ``fusion_metrics.csv``, ``association_metrics.csv``,
    ``attribution_metrics.csv``, ``model_check_metrics.csv``,
    ``scenario_validation.csv`` and ``summary.json`` under
    ``<artifacts_root>/summary``.

    Runs that have no ``evaluation/metrics.json`` are listed in
    ``runs_without_metrics`` rather than skipped silently: a campaign summary
    that quietly omits the runs that failed to evaluate is not a summary.
    """
    root = Path(artifacts_root)
    if not root.exists():
        raise FileNotFoundError("artifacts root does not exist: {0}".format(root))

    collected: List[Dict[str, Any]] = []
    missing: List[Dict[str, str]] = []
    excluded = [
        {"run_path": d.as_posix(), "kind": run_kind(d, root)}
        for d in _run_dirs(root, kinds=(RUN_KIND_REPLAY, RUN_KIND_ABLATION))
    ]
    for run_dir in _run_dirs(root):
        layout = RunLayout.from_run_dir(run_dir)
        if not layout.metrics.exists():
            missing.append(
                {
                    "run_dir": run_dir.name,
                    "run_path": run_dir.as_posix(),
                    "reason": "no evaluation/metrics.json; run cdf.evaluation.suite.evaluate_run",
                }
            )
            continue
        collected.append(read_json(layout.metrics))

    out_dir = summary_dir(root)
    out_dir.mkdir(parents=True, exist_ok=True)

    builders = (
        ("runs.csv", tables.run_rows, tables.RUN_COLUMNS),
        ("event_metrics.csv", tables.event_metrics_rows, tables.EVENT_METRICS_COLUMNS),
        ("graph_metrics.csv", tables.graph_metrics_rows, tables.GRAPH_METRICS_COLUMNS),
        ("fusion_metrics.csv", tables.fusion_metrics_rows, tables.FUSION_METRICS_COLUMNS),
        (
            "association_metrics.csv",
            tables.association_metrics_rows,
            tables.ASSOCIATION_METRICS_COLUMNS,
        ),
        (
            "attribution_metrics.csv",
            tables.attribution_metrics_rows,
            tables.ATTRIBUTION_METRICS_COLUMNS,
        ),
        ("model_check_metrics.csv", tables.model_check_rows, tables.MODEL_CHECK_COLUMNS),
        (
            "scenario_validation.csv",
            tables.scenario_validation_rows,
            tables.SCENARIO_VALIDATION_COLUMNS,
        ),
    )
    written: Dict[str, str] = {}
    run_rows: List[Dict[str, Any]] = []
    for filename, builder, columns in builders:
        rows = tables.concat([builder(m) for m in collected])
        if filename == "runs.csv":
            run_rows = rows
        write_csv(out_dir / filename, rows, columns)
        written[filename] = str(len(rows))

    summary = _campaign_summary(collected, missing, run_rows, cfg, excluded)
    summary["tables"] = {k: int(v) for k, v in sorted(written.items())}
    write_json(out_dir / "summary.json", summary)
    LOGGER.info(
        "aggregated %d run(s) into %s (%d without metrics)",
        len(collected),
        out_dir,
        len(missing),
    )
    return summary


def _mean(values: Sequence[Optional[float]]) -> Optional[float]:
    """Mean over the *available* values, or ``None`` when none is available.

    Missing entries are dropped rather than replaced by zero, and the count that
    survived is reported next to the mean, so a campaign average can never be
    quietly computed over runs that were never measured.
    """
    present = [float(v) for v in values if v is not None]
    if not present:
        return None
    return float(sum(present) / len(present))


def _campaign_summary(
    collected: Sequence[Mapping[str, Any]],
    missing: Sequence[Mapping[str, str]],
    run_rows: Sequence[Mapping[str, Any]],
    cfg: Config,
    excluded: Sequence[Mapping[str, str]] = (),
) -> Dict[str, Any]:
    outcomes: Dict[str, int] = {}
    by_scenario: Dict[str, Dict[str, Any]] = {}
    unavailable: Dict[str, int] = {}
    for m in collected:
        outcome = str(m.get("outcome", "") or "unknown")
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        sid = str(m.get("scenario_id", "") or "unknown")
        block = by_scenario.setdefault(
            sid, {"n_runs": 0, "n_validation_passed": 0, "outcomes": {}}
        )
        block["n_runs"] += 1
        block["outcomes"][outcome] = block["outcomes"].get(outcome, 0) + 1
        validation = m.get("scenario_validation")
        if isinstance(validation, Mapping) and validation.get("passed"):
            block["n_validation_passed"] += 1
        for name in (m.get("reasons") or {}):
            unavailable[name] = unavailable.get(name, 0) + 1

    def column(name: str) -> List[Optional[float]]:
        return [r.get(name) for r in run_rows]

    aggregates = {}
    for name in (
        "edge_f1_best_local",
        "edge_f1_fused",
        "delta_edge_f1",
        "node_f1_best_local",
        "node_f1_fused",
        "delta_node_f1",
        "delta_shd",
        "event_f1_best_local",
        "event_f1_fused",
        "association_f1",
        "attribution_f1",
    ):
        values = column(name)
        aggregates[name] = {
            "mean": _mean(values),
            "n_available": sum(1 for v in values if v is not None),
            "n_runs": len(values),
        }

    helped = [r.get("fusion_helped") for r in run_rows if r.get("fusion_helped") is not None]
    honest = [
        r.get("local_unknowns_honest")
        for r in run_rows
        if r.get("local_unknowns_honest") is not None
    ]
    return {
        "schema_version": SCHEMA_VERSIONS["evaluation"],
        "config_hash": cfg.hash,
        "n_runs": len(collected),
        "n_runs_without_metrics": len(missing),
        "runs_without_metrics": list(missing),
        # Held out of every number above: replays and ablation runs are
        # deliberately different experiments, not campaign runs. Listed so the
        # exclusion is visible rather than silent.
        "n_runs_excluded": len(excluded),
        "excluded_runs": list(excluded),
        "outcomes": dict(sorted(outcomes.items())),
        "by_scenario": {k: by_scenario[k] for k in sorted(by_scenario)},
        "unavailable_blocks": dict(sorted(unavailable.items())),
        "aggregates": aggregates,
        "n_runs_where_fusion_helped": sum(1 for v in helped if v),
        "n_runs_with_fusion_comparison": len(helped),
        "n_runs_epistemically_honest": sum(1 for v in honest if v),
        "n_runs_with_unknown_check": len(honest),
    }
