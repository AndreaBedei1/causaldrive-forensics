"""Evaluation-only A/B/C clock ablation on one fixed physical recording.

A is an oracle-restamped synchronized-clock control, not another physics run.
B deliberately bypasses correction only here. C uses the normal evidence-based
estimator. All outputs go under evaluation/; local/fusion inputs are read-only.
"""

from ..common.evidence import load_run
from ..common.io import write_json
from ..common.layout import RunLayout
from ..common.schemas import Provenance
from ..graph.export import load_graph
from ..fusion.aligned_evidence import AlignedRunEvidence
from ..fusion.time_alignment import align_participants
from ..fusion.track_association import associate_tracks
from ..fusion.event_alignment import resolve_subjects
from ..fusion.graph_fusion import fuse_graphs
from ..oracle.events import load_oracle_trace
from .association_metrics import evaluate_association
from .event_metrics import evaluate_events
from .graph_metrics import evaluate_graphs
from .clocks import (
    load_clock_truth,
    simulator_evidence,
    map_graph,
    map_event,
    evaluate_clock_alignment,
)


def run_clock_ablation(run_dir, cfg):
    layout = RunLayout.from_run_dir(run_dir)
    raw = load_run(layout.root, with_radar=True)
    truth = load_clock_truth(layout)
    if set(truth) != set(raw.participant_ids):
        raise ValueError("ablation requires all recorder clock profiles under oracle/")
    docs = {
        p: load_graph(layout.causal_graph(p), expect_scope=Provenance.LOCAL)
        for p in raw.participant_ids
    }
    oracle = load_graph(layout.oracle_causal_graph, expect_scope=Provenance.ORACLE)
    trace = load_oracle_trace(layout.root)
    physical = simulator_evidence(raw, truth)
    synchronized = {}
    for p, doc in docs.items():
        profile = truth[p]
        a = 1 / profile["true_scale"]
        b = -a * profile["true_offset_s"]
        synchronized[p] = map_graph(doc, a, b)
    results = {}
    for mode in [
        "A_synchronized",
        "B_independent_uncorrected",
        "C_independent_aligned",
    ]:
        source = physical if mode == "A_synchronized" else raw
        local = synchronized if mode == "A_synchronized" else docs
        if mode == "C_independent_aligned":
            alignment = align_participants(source, cfg)
        else:
            alignment = {
                "reference": source.participant_ids[0],
                "offsets": {
                    p: {
                        "scale": 1.0,
                        "offset_s": 0.0,
                        "confidence": 1.0,
                        "status": "ALIGNED",
                    }
                    for p in source.participant_ids
                },
                "constraints": [],
            }
        view = AlignedRunEvidence(source, alignment)
        assignments = associate_tracks(view, cfg)
        fused, diagnostics = fuse_graphs(view, local, assignments, cfg)
        subjects = resolve_subjects(assignments)
        scored = fused
        if mode != "A_synchronized":
            ref = truth[alignment["reference"]]
            a = 1 / ref["true_scale"]
            b = -a * ref["true_offset_s"]
            scored = map_graph(fused, a, b)
        graph_metrics = evaluate_graphs(synchronized, scored, oracle, subjects, cfg)
        event_metrics = evaluate_events(
            {p: doc.nodes for p, doc in synchronized.items()},
            scored.nodes,
            oracle.nodes,
            subjects,
            cfg,
        )
        results[mode] = {
            "clock": (
                evaluate_clock_alignment(alignment, truth)
                if mode != "A_synchronized"
                else {
                    "mean_abs_offset_error_s": 0.0,
                    "mean_abs_drift_error_ppm": 0.0,
                    "control": "oracle-restamped time-only control",
                }
            ),
            "association": evaluate_association(assignments, physical, trace, cfg),
            "event_matching": event_metrics,
            "graphs": graph_metrics,
            "n_merged_groups": diagnostics["n_merged_groups"],
            "alignment": alignment,
        }
    report = {
        "schema_version": "1.0.0",
        "run_id": raw.run_id,
        "protocol": "fixed physical recording; A restamps clocks only; B is evaluation-only; C uses local evidence",
        "modes": results,
    }
    write_json(layout.evaluation_dir / "clock_ablation.json", report)
    return report
