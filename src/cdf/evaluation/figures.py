"""Figures for the evidence review and for the paper.

Rendering is head-less: the Agg backend is selected at import time, before
``pyplot`` is imported, so importing this module can never try to open a window
on a machine running a batch of scenarios.

Presentation rules, enforced by construction rather than by convention
---------------------------------------------------------------------
* **Never hide a negative result.** Every bar chart is drawn from a zero
  baseline, and axis limits are only ever *widened* to fit the data -- never
  narrowed to crop a bar that went the wrong way. A figure whose job is to test a
  hypothesis must be able to show the hypothesis failing.
* **A missing metric is not a zero.** When a block was not computed the figure
  draws an explicit "no data" annotation on empty axes. A zero-height bar would
  read as "measured, and the answer was nothing", which is a different and much
  stronger claim than "not measured".
* **Every axis is labelled, with units.** Seconds, metres, m/s, m/s^2 -- an
  unlabelled axis in a forensic report is not evidence.

Every function takes an explicit output path and returns it, so the caller (the
run layout's ``figures/`` directory, or ``artifacts/summary/figures``) decides
where things land.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (must follow the backend selection)
import networkx as nx  # noqa: E402

from ..common.config import Config  # noqa: E402
from ..common.evidence import RunEvidence  # noqa: E402
from ..common.schemas import EventType, GraphDocument, OUTCOME_EVENT_TYPES  # noqa: E402
from ..graph.export import to_networkx  # noqa: E402

__all__ = [
    "DEFAULT_DPI",
    "plot_trajectories",
    "plot_ttc",
    "plot_controls",
    "plot_graph",
    "plot_local_vs_fused_f1",
    "plot_knowledge_gain",
    "plot_attribution",
    "plot_association",
    "plot_robustness",
    "plot_scenario_outcomes",
    "render_run_figures",
    "render_summary_figures",
]

PathLike = Union[str, Path]

#: Raster resolution used when the configuration says nothing. Large enough for a
#: two-column figure without producing multi-megabyte artifacts.
DEFAULT_DPI: int = 150

#: Colour-blind-safe qualitative cycle, applied per participant/series so that the
#: same participant keeps the same colour across every figure of a run.
_SERIES_COLOURS: Tuple[str, ...] = (
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
)

_OUTCOME_TYPE_VALUES = {t.value for t in OUTCOME_EVENT_TYPES}


def _dpi(cfg: Optional[Config]) -> int:
    if cfg is None:
        return DEFAULT_DPI
    return int(cfg.get("evaluation.figures.dpi", DEFAULT_DPI))


def _colour(index: int) -> str:
    return _SERIES_COLOURS[index % len(_SERIES_COLOURS)]


def _save(fig: "plt.Figure", path: PathLike, cfg: Optional[Config] = None) -> Path:
    """Write a figure and always close it, so a long batch cannot leak memory."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.savefig(str(p), dpi=_dpi(cfg), bbox_inches="tight")
    finally:
        plt.close(fig)
    return p


def _no_data(ax: "plt.Axes", message: str) -> None:
    """Annotate empty axes with why there is nothing to show."""
    ax.text(
        0.5,
        0.5,
        "no data\n{0}".format(message),
        ha="center",
        va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="#555555",
        wrap=True,
    )
    ax.set_xticks([])
    ax.set_yticks([])


def _bar_axis(ax: "plt.Axes", values: Sequence[Optional[float]]) -> None:
    """Zero baseline, widened (never cropped) to contain every value.

    Negative values -- a fusion delta that went the wrong way -- stay visible
    below the baseline, which is the whole point of drawing the baseline.
    """
    finite = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    lo = min(finite + [0.0])
    hi = max(finite + [0.0])
    span = hi - lo
    pad = 0.08 * span if span > 0 else 0.1
    ax.set_ylim(lo - pad, hi + pad)
    ax.axhline(0.0, color="#333333", linewidth=0.9)


# ---------------------------------------------------------------------------
# Evidence figures (local artifacts only)
# ---------------------------------------------------------------------------


def plot_trajectories(run: RunEvidence, path: PathLike, cfg: Optional[Config] = None) -> Path:
    """Each participant's own localisation trace in the map plane.

    This is the evidence the fusion layer's identity resolution rests on, so it
    is plotted from the participants' own logs -- never from the oracle poses --
    with an equal aspect ratio so that a geometric claim about the encounter can
    actually be read off the figure.
    """
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    drawn = 0
    for i, pid in enumerate(run.participant_ids):
        t, x, y = run.get(pid).self_trajectory()
        if not t:
            continue
        drawn += 1
        ax.plot(x, y, color=_colour(i), linewidth=1.8, label="vehicle {0}".format(pid))
        ax.plot(x[0], y[0], marker="o", color=_colour(i), markersize=6)
        ax.plot(x[-1], y[-1], marker="s", color=_colour(i), markersize=6)
    if drawn == 0:
        _no_data(ax, "no telemetry recorded for any participant")
    else:
        ax.set_aspect("equal", adjustable="datalim")
        ax.legend(loc="best", fontsize=8)
        ax.grid(True, linewidth=0.3, alpha=0.5)
    ax.set_xlabel("map x [m]")
    ax.set_ylabel("map y [m]")
    ax.set_title("Self-reported trajectories (circle = start, square = end)")
    return _save(fig, path, cfg)


def plot_ttc(run: RunEvidence, path: PathLike, cfg: Optional[Config] = None) -> Path:
    """Time-to-collision of every local radar track, per observer.

    The ``LOW_TTC`` and ``CRITICAL_TTC`` thresholds are drawn from the same
    configuration the event extractor used, so the figure shows exactly which
    crossings produced events.
    """
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    drawn = 0
    for i, pid in enumerate(run.participant_ids):
        ev = run.get(pid)
        for track_id in ev.track_ids():
            samples = [s for s in ev.tracks if s.track_id == track_id and s.ttc is not None]
            if not samples:
                continue
            samples.sort(key=lambda s: float(s.t))
            drawn += 1
            ax.plot(
                [float(s.t) for s in samples],
                [float(s.ttc) for s in samples],
                color=_colour(i),
                linewidth=1.5,
                label="{0} observes {1}".format(pid, track_id),
            )
    if drawn == 0:
        _no_data(ax, "no radar track carried a defined TTC")
    else:
        if cfg is not None:
            low = float(cfg.get("events.radar.low_ttc.ttc_s", 3.0))
            crit = float(cfg.get("events.radar.critical_ttc.ttc_s", 1.6))
            ax.axhline(low, color="#888888", linestyle="--", linewidth=1.0,
                       label="LOW_TTC threshold ({0:.1f} s)".format(low))
            ax.axhline(crit, color="#B00000", linestyle=":", linewidth=1.2,
                       label="CRITICAL_TTC threshold ({0:.1f} s)".format(crit))
        ax.set_ylim(bottom=0.0)
        ax.legend(loc="best", fontsize=7)
        ax.grid(True, linewidth=0.3, alpha=0.5)
    ax.set_xlabel("simulation time [s]")
    ax.set_ylabel("time to collision [s]")
    ax.set_title("Onboard time-to-collision estimates")
    return _save(fig, path, cfg)


def plot_controls(run: RunEvidence, path: PathLike, cfg: Optional[Config] = None) -> Path:
    """Throttle, brake and steering commands of every participant."""
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 6.4), sharex=True)
    channels = (
        ("throttle", "throttle command [0-1]", (0.0, 1.05)),
        ("brake", "brake command [0-1]", (0.0, 1.05)),
        ("steer", "steer command [-1, 1]", (-1.05, 1.05)),
    )
    drawn = 0
    for ax, (attr, label, limits) in zip(axes, channels):
        for i, pid in enumerate(run.participant_ids):
            controls = run.get(pid).controls
            if not controls:
                continue
            drawn += 1
            ax.plot(
                [float(c.t) for c in controls],
                [float(getattr(c, attr)) for c in controls],
                color=_colour(i),
                linewidth=1.4,
                label="vehicle {0}".format(pid),
            )
        ax.set_ylabel(label, fontsize=8)
        ax.grid(True, linewidth=0.3, alpha=0.5)
        ax.set_ylim(*limits)
    if drawn == 0:
        for ax in axes:
            ax.clear()
        _no_data(axes[0], "no control samples recorded")
    else:
        axes[0].legend(loc="upper left", fontsize=8, ncol=len(run.participant_ids) or 1)
    axes[-1].set_xlabel("simulation time [s]")
    axes[0].set_title("Actuator commands")
    return _save(fig, path, cfg)


# ---------------------------------------------------------------------------
# Graph figure
# ---------------------------------------------------------------------------


def _graph_positions(doc: GraphDocument) -> Dict[str, Tuple[float, float]]:
    """Deterministic time-on-x layout, one horizontal lane per participant.

    A force-directed layout would need a random seed and would place events by
    connectivity; putting time on the x axis instead means the figure reads as
    what it is -- a causal chain unfolding through the run -- and two renderings
    of the same graph are byte-identical.
    """
    lanes = sorted({n.participant_id for n in doc.nodes})
    lane_of = {pid: idx for idx, pid in enumerate(lanes)}
    by_lane: Dict[str, List[str]] = {}
    positions: Dict[str, Tuple[float, float]] = {}
    for node in sorted(doc.nodes, key=lambda n: (float(n.t_peak), n.event_id)):
        lane = lane_of[node.participant_id]
        seen = by_lane.setdefault(node.participant_id, [])
        # Stagger events that share a lane and nearly share a time, so that an
        # overlapping pair stays two readable nodes instead of one blob.
        offset = 0.22 * (len(seen) % 3 - 1)
        seen.append(node.event_id)
        positions[node.event_id] = (float(node.t_peak), float(lane) + offset)
    return positions


def plot_graph(
    doc: Optional[GraphDocument],
    path: PathLike,
    cfg: Optional[Config] = None,
    title: str = "",
) -> Path:
    """Draw a :class:`GraphDocument` with time on the x axis and outcomes marked."""
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    if doc is None or not doc.nodes:
        _no_data(ax, "graph was not produced for this run")
        ax.set_title(title or "causal graph")
        return _save(fig, path, cfg)

    graph = to_networkx(doc)
    pos = _graph_positions(doc)
    lanes = sorted({n.participant_id for n in doc.nodes})
    lane_of = {pid: idx for idx, pid in enumerate(lanes)}

    node_colours = []
    node_sizes = []
    for nid in graph.nodes:
        node = doc.node_by_id(nid)
        etype = (
            node.event_type.value if isinstance(node.event_type, EventType)
            else str(node.event_type)
        )
        if etype in _OUTCOME_TYPE_VALUES:
            node_colours.append("#B00000")
            node_sizes.append(240)
        else:
            node_colours.append(_colour(lane_of[node.participant_id]))
            node_sizes.append(120)

    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        edge_color="#666666",
        width=[0.6 + 1.6 * float(d.get("confidence", 0.5)) for _u, _v, d in graph.edges(data=True)],
        arrowsize=10,
        alpha=0.75,
        node_size=node_sizes,
    )
    nx.draw_networkx_nodes(
        graph, pos, ax=ax, node_color=node_colours, node_size=node_sizes, linewidths=0.0
    )
    labels = {}
    for nid in graph.nodes:
        node = doc.node_by_id(nid)
        etype = (
            node.event_type.value if isinstance(node.event_type, EventType)
            else str(node.event_type)
        )
        labels[nid] = etype
    nx.draw_networkx_labels(graph, pos, labels=labels, ax=ax, font_size=5.5)

    ax.set_yticks(list(range(len(lanes))))
    ax.set_yticklabels(["vehicle {0}".format(p) for p in lanes])
    ax.set_xlabel("event peak time [s]")
    ax.set_title(
        title
        or "{0} graph ({1}, {2} nodes / {3} edges)".format(
            doc.graph_kind, doc.scope.value, len(doc.nodes), len(doc.edges)
        )
    )
    ax.grid(True, axis="x", linewidth=0.3, alpha=0.5)
    return _save(fig, path, cfg)


# ---------------------------------------------------------------------------
# Result figures
# ---------------------------------------------------------------------------


def plot_local_vs_fused_f1(
    graphs: Optional[Mapping[str, Any]], path: PathLike, cfg: Optional[Config] = None
) -> Path:
    """Node and edge F1 of every local graph next to the fused graph."""
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    per_participant = (graphs or {}).get("per_participant") or {}
    fused = (graphs or {}).get("fused")
    if not per_participant:
        _no_data(ax, "no graph metrics: the oracle causal graph was unavailable")
        ax.set_title("Reconstruction F1 vs oracle")
        return _save(fig, path, cfg)

    labels: List[str] = []
    node_f1: List[float] = []
    edge_f1: List[float] = []
    for pid in sorted(per_participant):
        labels.append("local {0}".format(pid))
        node_f1.append(float(per_participant[pid].get("node_f1", 0.0)))
        edge_f1.append(float(per_participant[pid].get("edge_f1", 0.0)))
    if isinstance(fused, Mapping):
        labels.append("fused")
        node_f1.append(float(fused.get("node_f1", 0.0)))
        edge_f1.append(float(fused.get("edge_f1", 0.0)))

    xs = list(range(len(labels)))
    width = 0.38
    ax.bar([x - width / 2 for x in xs], node_f1, width, label="node F1", color="#0072B2")
    ax.bar([x + width / 2 for x in xs], edge_f1, width, label="edge F1", color="#D55E00")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    _bar_axis(ax, node_f1 + edge_f1 + [1.0])
    ax.set_ylabel("F1 against the oracle graph [0-1]")
    ax.set_title("Per-vehicle and fused reconstruction quality")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, axis="y", linewidth=0.3, alpha=0.5)
    return _save(fig, path, cfg)


def plot_knowledge_gain(
    benefit: Optional[Mapping[str, Any]], path: PathLike, cfg: Optional[Config] = None
) -> Path:
    """The H1/H2 figure: fused minus best-single-vehicle, with the gain counted.

    The delta panel keeps its zero baseline and is never clipped, so a run where
    fusion helped nothing (or hurt) is as legible as one where it helped.
    """
    fig, (ax_delta, ax_gain) = plt.subplots(1, 2, figsize=(9.0, 4.0))
    if not benefit:
        _no_data(ax_delta, "fusion benefit was not computed")
        _no_data(ax_gain, "fusion benefit was not computed")
        ax_delta.set_title("Fused minus best single vehicle")
        return _save(fig, path, cfg)

    delta_labels = ["edge F1", "node F1", "SHD (lower is better)"]
    deltas = [
        float(benefit.get("delta_edge_f1") or 0.0),
        float(benefit.get("delta_node_f1") or 0.0),
        float(benefit.get("delta_shd") or 0.0),
    ]
    colours = ["#009E73" if d > 0 else ("#B00000" if d < 0 else "#888888") for d in deltas[:2]]
    colours.append("#009E73" if deltas[2] < 0 else ("#B00000" if deltas[2] > 0 else "#888888"))
    ax_delta.bar(range(len(deltas)), deltas, color=colours, width=0.55)
    ax_delta.set_xticks(range(len(deltas)))
    ax_delta.set_xticklabels(delta_labels, fontsize=8)
    _bar_axis(ax_delta, deltas)
    ax_delta.set_ylabel("fused - best single local")
    ax_delta.set_title(
        "Fusion benefit (baseline: vehicle {0})".format(
            benefit.get("best_local_participant_id", "?")
        )
    )
    ax_delta.grid(True, axis="y", linewidth=0.3, alpha=0.5)

    gained = [
        float(benefit.get("n_nodes_gained") or 0),
        float(benefit.get("n_edges_gained") or 0),
    ]
    ax_gain.bar(range(2), gained, color=["#0072B2", "#D55E00"], width=0.55)
    ax_gain.set_xticks(range(2))
    ax_gain.set_xticklabels(["oracle nodes\nrecovered", "oracle edges\nrecovered"], fontsize=8)
    _bar_axis(ax_gain, gained)
    ax_gain.set_ylabel("count recovered by fusion alone")
    ax_gain.set_title("Knowledge gain over the best single view")
    ax_gain.grid(True, axis="y", linewidth=0.3, alpha=0.5)
    return _save(fig, path, cfg)


def plot_attribution(
    attribution: Optional[Mapping[str, Any]], path: PathLike, cfg: Optional[Config] = None
) -> Path:
    """Candidate causal-action set score, plus the counts behind it."""
    fig, (ax_score, ax_counts) = plt.subplots(1, 2, figsize=(9.0, 4.0))
    if not attribution:
        _no_data(ax_score, "no attribution result for this run")
        _no_data(ax_counts, "no attribution result for this run")
        ax_score.set_title("Causal attribution vs oracle initiators")
        return _save(fig, path, cfg)

    scores = [
        float(attribution.get("precision") or 0.0),
        float(attribution.get("recall") or 0.0),
        float(attribution.get("f1") or 0.0),
    ]
    ax_score.bar(range(3), scores, color="#0072B2", width=0.55)
    ax_score.set_xticks(range(3))
    ax_score.set_xticklabels(["precision", "recall", "F1"], fontsize=9)
    _bar_axis(ax_score, scores + [1.0])
    ax_score.set_ylabel("candidate causal-action set score [0-1]")
    ax_score.set_title("Causal attribution vs oracle initiators")
    ax_score.grid(True, axis="y", linewidth=0.3, alpha=0.5)

    counts = [
        float(attribution.get("n_true_positive") or 0),
        float(attribution.get("n_false_positive") or 0),
        float(attribution.get("n_false_negative") or 0),
        float(attribution.get("n_insufficient_evidence") or 0),
    ]
    ax_counts.bar(
        range(4), counts, color=["#009E73", "#D55E00", "#B00000", "#888888"], width=0.55
    )
    ax_counts.set_xticks(range(4))
    ax_counts.set_xticklabels(
        ["correct", "spurious", "missed", "insufficient\nevidence"], fontsize=8
    )
    _bar_axis(ax_counts, counts)
    ax_counts.set_ylabel("number of scripted actions")
    ax_counts.set_title("Attribution outcome breakdown")
    ax_counts.grid(True, axis="y", linewidth=0.3, alpha=0.5)
    return _save(fig, path, cfg)


def plot_association(
    association: Optional[Mapping[str, Any]], path: PathLike, cfg: Optional[Config] = None
) -> Path:
    """Identity-resolution verdicts and the trajectory RMSE that produced them."""
    fig, (ax_counts, ax_rmse) = plt.subplots(1, 2, figsize=(9.0, 4.0))
    if not association:
        _no_data(ax_counts, "association was not scored for this run")
        _no_data(ax_rmse, "association was not scored for this run")
        ax_counts.set_title("Track identity resolution")
        return _save(fig, path, cfg)

    counts = [
        float(association.get("n_correct") or 0),
        float(association.get("n_incorrect") or 0),
        float(association.get("n_unresolved") or 0),
        float(association.get("n_unscorable") or 0),
    ]
    ax_counts.bar(
        range(4), counts, color=["#009E73", "#B00000", "#888888", "#CCCCCC"], width=0.55
    )
    ax_counts.set_xticks(range(4))
    ax_counts.set_xticklabels(
        ["correct", "incorrect", "unresolved", "no ground\ntruth"], fontsize=8
    )
    _bar_axis(ax_counts, counts)
    ax_counts.set_ylabel("number of radar tracks")
    ax_counts.set_title(
        "Track identity resolution (F1 = {0:.2f})".format(float(association.get("f1") or 0.0))
    )
    ax_counts.grid(True, axis="y", linewidth=0.3, alpha=0.5)

    tracks = [t for t in (association.get("tracks") or []) if t.get("rmse_m") is not None]
    if not tracks:
        _no_data(ax_rmse, "no track carried a trajectory RMSE")
    else:
        labels = [str(t.get("track_id")) for t in tracks]
        values = [float(t["rmse_m"]) for t in tracks]
        colours = [
            "#009E73" if t.get("verdict") == "correct" else "#B00000" for t in tracks
        ]
        ax_rmse.bar(range(len(values)), values, color=colours, width=0.55)
        ax_rmse.set_xticks(range(len(values)))
        ax_rmse.set_xticklabels(labels, fontsize=7, rotation=45, ha="right")
        _bar_axis(ax_rmse, values)
        ax_rmse.set_ylabel("trajectory RMSE [m]")
        ax_rmse.set_title("Evidence behind each identity claim")
        ax_rmse.grid(True, axis="y", linewidth=0.3, alpha=0.5)
    return _save(fig, path, cfg)


def plot_robustness(
    rows: Optional[Sequence[Mapping[str, Any]]], path: PathLike, cfg: Optional[Config] = None
) -> Path:
    """Edge F1 of best-local and fused across every run, grouped by scenario.

    Spread across seeds and variants is the robustness claim: one good seed is an
    anecdote. Every run is plotted, including the ones where fusion lost.
    """
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    usable = [
        r
        for r in (rows or [])
        if r.get("edge_f1_fused") is not None or r.get("edge_f1_best_local") is not None
    ]
    if not usable:
        _no_data(ax, "no run produced graph metrics (oracle graphs unavailable)")
        ax.set_title("Reconstruction robustness across runs")
        return _save(fig, path, cfg)

    labels = [
        "{0}/{1}/s{2}".format(r.get("scenario_id", "?"), r.get("variant", ""), r.get("seed", 0))
        for r in usable
    ]
    best = [_finite(r.get("edge_f1_best_local")) for r in usable]
    fused = [_finite(r.get("edge_f1_fused")) for r in usable]
    xs = list(range(len(usable)))
    width = 0.38
    # A missing value is drawn as no bar at all plus an explicit "n/a" label; a
    # zero-height bar would claim the run scored zero rather than went unmeasured.
    ax.bar(
        [x - width / 2 for x in xs],
        [0.0 if v is None else v for v in best],
        width,
        label="best single local",
        color="#0072B2",
    )
    ax.bar(
        [x + width / 2 for x in xs],
        [0.0 if v is None else v for v in fused],
        width,
        label="fused",
        color="#D55E00",
    )
    for x, (b, f) in enumerate(zip(best, fused)):
        if b is None or f is None:
            ax.text(x, 0.02, "n/a", ha="center", fontsize=7, color="#555555")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=7, rotation=45, ha="right")
    _bar_axis(ax, [v for v in best + fused if v is not None] + [1.0])
    ax.set_ylabel("causal edge F1 against the oracle [0-1]")
    ax.set_xlabel("scenario / variant / seed")
    ax.set_title("Reconstruction robustness across runs")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, axis="y", linewidth=0.3, alpha=0.5)
    return _save(fig, path, cfg)


def _finite(value: Any) -> Optional[float]:
    if value is None:
        return None
    v = float(value)
    return None if math.isnan(v) else v


def plot_scenario_outcomes(
    summary: Optional[Mapping[str, Any]], path: PathLike, cfg: Optional[Config] = None
) -> Path:
    """Outcome class per scenario, and whether the scenario validated.

    ``summary`` is the mapping written by
    :func:`cdf.evaluation.suite.aggregate_runs`; ``outcomes`` counts runs by
    outcome class and ``by_scenario`` counts them per scenario.
    """
    fig, (ax_outcome, ax_valid) = plt.subplots(1, 2, figsize=(9.0, 4.0))
    outcomes = (summary or {}).get("outcomes") or {}
    if not outcomes:
        _no_data(ax_outcome, "no run manifests were aggregated")
        _no_data(ax_valid, "no run manifests were aggregated")
        ax_outcome.set_title("Run outcomes")
        return _save(fig, path, cfg)

    labels = sorted(outcomes)
    values = [float(outcomes[k]) for k in labels]
    ax_outcome.bar(range(len(labels)), values, color="#0072B2", width=0.55)
    ax_outcome.set_xticks(range(len(labels)))
    ax_outcome.set_xticklabels(labels, fontsize=8)
    _bar_axis(ax_outcome, values)
    ax_outcome.set_ylabel("number of runs")
    ax_outcome.set_title("Run outcomes")
    ax_outcome.grid(True, axis="y", linewidth=0.3, alpha=0.5)

    by_scenario = (summary or {}).get("by_scenario") or {}
    if not by_scenario:
        _no_data(ax_valid, "no per-scenario validation was recorded")
        return _save(fig, path, cfg)
    names = sorted(by_scenario)
    passed = [float(by_scenario[n].get("n_validation_passed", 0)) for n in names]
    total = [float(by_scenario[n].get("n_runs", 0)) for n in names]
    xs = list(range(len(names)))
    width = 0.38
    ax_valid.bar([x - width / 2 for x in xs], total, width, label="runs", color="#888888")
    ax_valid.bar(
        [x + width / 2 for x in xs], passed, width, label="validated", color="#009E73"
    )
    ax_valid.set_xticks(xs)
    ax_valid.set_xticklabels(names, fontsize=7, rotation=45, ha="right")
    _bar_axis(ax_valid, total + passed)
    ax_valid.set_ylabel("number of runs")
    ax_valid.set_title("Scenario validation")
    ax_valid.legend(loc="best", fontsize=8)
    ax_valid.grid(True, axis="y", linewidth=0.3, alpha=0.5)
    return _save(fig, path, cfg)


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------


def render_run_figures(
    run_dir: PathLike, cfg: Optional[Config] = None
) -> List[Path]:
    """Render every per-run figure into ``<run>/figures/``.

    Each panel is drawn from a persisted artifact, so a figure can always be
    traced back to the file it came from. A missing artifact produces an explicit
    "no data" panel rather than an empty axis or a zero bar -- a reader must be
    able to tell "this was not measured" from "this measured zero".
    """
    from ..common.evidence import load_run
    from ..common.io import read_json
    from ..common.layout import RunLayout
    from ..common.schemas import Provenance
    from ..graph.export import load_graph

    layout = RunLayout.from_run_dir(run_dir)
    layout.figures_dir.mkdir(parents=True, exist_ok=True)
    run = load_run(layout.root, with_radar=False)
    out: List[Path] = []

    out.append(plot_trajectories(run, layout.figures_dir / "trajectories.png", cfg))
    out.append(plot_ttc(run, layout.figures_dir / "ttc.png", cfg))
    out.append(plot_controls(run, layout.figures_dir / "controls.png", cfg))

    for pid in layout.participant_ids():
        path = layout.causal_graph(pid)
        doc = load_graph(path, expect_scope=Provenance.LOCAL) if path.exists() else None
        out.append(
            plot_graph(
                doc,
                layout.figures_dir / "local_{0}_graph.png".format(pid),
                cfg,
                title="LOCAL RECONSTRUCTION - participant {0}".format(pid),
            )
        )

    fused = (
        load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)
        if layout.fused_causal_graph.exists()
        else None
    )
    out.append(
        plot_graph(fused, layout.figures_dir / "fused_graph.png", cfg, title="FUSED RECONSTRUCTION")
    )

    oracle = (
        load_graph(layout.oracle_causal_graph, expect_scope=Provenance.ORACLE)
        if layout.oracle_causal_graph.exists()
        else None
    )
    out.append(
        plot_graph(
            oracle,
            layout.figures_dir / "oracle_graph.png",
            cfg,
            title="PRIVILEGED GROUND TRUTH - EVALUATION ONLY",
        )
    )

    metrics: Dict[str, Any] = {}
    if layout.metrics.exists():
        metrics = read_json(layout.metrics)
    out.append(
        plot_local_vs_fused_f1(
            metrics.get("graphs"), layout.figures_dir / "local_vs_fused_f1.png", cfg
        )
    )
    out.append(
        plot_knowledge_gain(
            metrics.get("fusion_benefit"), layout.figures_dir / "knowledge_gain.png", cfg
        )
    )
    out.append(
        plot_attribution(
            metrics.get("attribution"), layout.figures_dir / "attribution.png", cfg
        )
    )
    out.append(
        plot_association(
            metrics.get("association"), layout.figures_dir / "association.png", cfg
        )
    )
    return out


#: Verdict colours. UNKNOWN is deliberately neither red nor green: it is not a
#: weak FAIL, it is the monitor declining to answer.
_VERDICT_COLOURS = {"PASS": "#2e7d32", "FAIL": "#c62828", "UNKNOWN": "#8e8e8e"}
_VERDICT_ORDER = ("PASS", "FAIL", "UNKNOWN")


def plot_model_check_verdicts(
    rows: Sequence[Mapping[str, Any]], path: PathLike, cfg: Optional[Config] = None
) -> Path:
    """Verdict distribution per property across the campaign.

    ``rows`` are the records of ``summary/model_check_metrics.csv`` -- one per
    (run, property, participant). The point of the figure is the UNKNOWN band:
    a monitor over finite traces cannot decide a property whose antecedent never
    held, and reporting that as PASS would be claiming compliance nobody
    observed.
    """
    fig, (ax_prop, ax_total) = plt.subplots(
        1, 2, figsize=(10.0, 4.0), gridspec_kw={"width_ratios": [3, 1]})

    if not rows:
        _no_data(ax_prop, "no model-checking results were aggregated")
        _no_data(ax_total, "no model-checking results were aggregated")
        return _save(fig, path, cfg)

    per_property: Dict[str, Dict[str, int]] = {}
    totals: Dict[str, int] = {v: 0 for v in _VERDICT_ORDER}
    for row in rows:
        prop = str(row.get("property_id") or "?")
        status = str(row.get("status") or "?")
        counts = per_property.setdefault(prop, {v: 0 for v in _VERDICT_ORDER})
        if status in counts:
            counts[status] += 1
            totals[status] += 1

    names = sorted(per_property)
    positions = list(range(len(names)))
    left = [0.0] * len(names)
    for verdict in _VERDICT_ORDER:
        widths = [per_property[n][verdict] for n in names]
        ax_prop.barh(positions, widths, left=left, label=verdict,
                     color=_VERDICT_COLOURS[verdict], edgecolor="white")
        left = [a + b for a, b in zip(left, widths)]
    ax_prop.set_yticks(positions)
    ax_prop.set_yticklabels(names, fontsize=8)
    ax_prop.invert_yaxis()
    ax_prop.set_xlabel("evaluations")
    ax_prop.set_title("finite-trace verdicts per property")
    ax_prop.legend(loc="lower right", fontsize=8, frameon=False)

    n_total = sum(totals.values()) or 1
    ax_total.bar(list(range(len(_VERDICT_ORDER))),
                 [totals[v] for v in _VERDICT_ORDER],
                 color=[_VERDICT_COLOURS[v] for v in _VERDICT_ORDER])
    ax_total.set_xticks(list(range(len(_VERDICT_ORDER))))
    ax_total.set_xticklabels(_VERDICT_ORDER, fontsize=8)
    ax_total.set_title("all {0} evaluations".format(n_total), fontsize=9)
    for i, verdict in enumerate(_VERDICT_ORDER):
        ax_total.text(i, totals[verdict], " {0}\n {1:.0f}%".format(
            totals[verdict], 100.0 * totals[verdict] / n_total),
            ha="center", va="bottom", fontsize=8)
    ax_total.set_ylim(0, max(totals.values()) * 1.35 if totals else 1)

    fig.tight_layout()
    return _save(fig, path, cfg)


def render_summary_figures(
    artifacts_root: PathLike, cfg: Optional[Config] = None
) -> List[Path]:
    """Render the cross-run figures into ``<artifacts>/summary/figures/``.

    Reads only ``summary/summary.json`` and ``summary/runs.csv``, so the campaign
    figures are reproducible from the aggregate artifacts alone.
    """
    import csv

    from ..common.io import read_json

    root = Path(artifacts_root)
    summary_dir = root / "summary"
    fig_dir = summary_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, Any] = {}
    if (summary_dir / "summary.json").exists():
        summary = read_json(summary_dir / "summary.json")

    def _read(name: str) -> List[Dict[str, Any]]:
        path = summary_dir / name
        if not path.exists():
            return []
        with open(str(path), "r", encoding="utf-8", newline="") as fh:
            return [dict(r) for r in csv.DictReader(fh)]

    rows = _read("runs.csv")
    check_rows = _read("model_check_metrics.csv")

    return [
        plot_robustness(rows, fig_dir / "edge_f1_local_vs_fused.png", cfg),
        plot_scenario_outcomes(summary, fig_dir / "scenario_outcomes.png", cfg),
        plot_model_check_verdicts(
            check_rows, fig_dir / "model_check_verdicts.png", cfg),
    ]
