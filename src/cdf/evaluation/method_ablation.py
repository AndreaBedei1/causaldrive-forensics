"""What each layer of the method is worth, measured rather than asserted.

Three accounts of the same incident are compared against the same oracle graph:

``best_local``
    the single participant whose own graph scores highest. This is the honest
    baseline: it is what you get without any cooperation at all, and taking the
    *best* one rather than the mean makes the baseline as strong as possible.
``simple_fusion``
    the participants' logs merged -- identities resolved, clocks aligned, nodes
    and edges unioned -- but with no causal claim that a participant did not
    itself make. Every edge in this graph was drawn inside one vehicle's log.
``fusion_global_reasoning``
    the same merge, plus the post-fusion inference stage that proposes causal
    edges *between* claims made by different vehicles, which is the only stage
    that can relate "B braked" to "A's gap closed".

The comparison is run offline, over the recorded evidence, changing exactly one
configuration key between the second and third arm. Nothing is re-simulated, so
the three arms see identical recordings and the difference between them is the
method rather than the run.

Both strict and canonical vocabularies are reported. The strict numbers are the
headline; the canonical ones exist because the oracle names a scripted action
where a vehicle names the brake it applied, and a reconstruction should not be
penalised for the oracle's vocabulary. Where the two disagree, both are shown.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.io import write_json
from ..common.layout import RunLayout
from ..common.schemas import GraphDocument, Provenance
from ..graph.canonical import canonicalise
from ..graph.export import load_graph
from .graph_metrics import evaluate_graphs

LOGGER = logging.getLogger(__name__)

__all__ = ["ARMS", "ablate_run", "ablation_path"]

#: The arms, in the order they are reported: each one adds a capability.
ARMS = ("best_local", "simple_fusion", "fusion_global_reasoning")

#: The single key that separates the last two arms.
INFERENCE_KEY = "fusion.post_fusion.enabled"


def ablation_path(layout: RunLayout) -> Any:
    """Where a run's ablation result is written."""
    return layout.evaluation_dir / "method_ablation.json"


def _scores(block: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """The numbers that describe one arm's agreement with the oracle.

    ``evaluate_graphs`` returns one flat block per graph; this lifts out the
    handful of fields the ablation compares, so a change in the metric module's
    surface fails here loudly instead of silently producing null columns.
    """
    if not block:
        return {"nodes": None, "edges": None}
    return {
        "nodes": {
            "precision": block.get("node_precision"),
            "recall": block.get("node_recall"),
            "f1": block.get("node_f1"),
            "n_matched": block.get("n_nodes_matched"),
            "n_truth": block.get("n_nodes_truth"),
            "n_pred": block.get("n_nodes_pred"),
        },
        "edges": {
            "precision": block.get("edge_precision"),
            "recall": block.get("edge_recall"),
            "f1": block.get("edge_f1"),
            "n_matched": block.get("n_edges_matched"),
            "n_truth": block.get("n_edges_truth"),
            "n_pred": block.get("n_edges_pred"),
            "shd": block.get("structural_hamming_distance"),
        },
    }


def _arm_from_graphs(
    local_docs: Mapping[str, GraphDocument],
    fused: Optional[GraphDocument],
    oracle: GraphDocument,
    subject_map: Optional[Mapping[str, str]],
    cfg: Config,
) -> Dict[str, Any]:
    """Score one fused graph, strictly and canonically, against the oracle."""
    strict = evaluate_graphs(local_docs, fused, oracle, subject_map, cfg)
    canonical = evaluate_graphs(
        {pid: canonicalise(doc) for pid, doc in local_docs.items()},
        canonicalise(fused),
        canonicalise(oracle),
        subject_map,
        cfg,
    )
    return {"strict": strict, "canonical": canonical}


def _best_local(scored: Mapping[str, Any]) -> Optional[str]:
    """The participant whose own graph agrees best with the oracle.

    Ranked on edge F1 first, because an incident is a structure and not a bag of
    events; node F1 breaks ties, then the participant id so the answer is stable.
    """
    per = scored.get("per_participant") or {}
    if not per:
        return None

    def key(pid: str) -> Any:
        block = per[pid] or {}
        edges = block.get("edge_f1")
        nodes = block.get("node_f1")
        # Ties break on the participant id, so the choice is reproducible; the
        # id is sorted ascending while the scores sort descending.
        return (
            -1.0 if edges is None else float(edges),
            -1.0 if nodes is None else float(nodes),
        )

    return sorted(sorted(per), key=key, reverse=True)[0]


def ablate_run(
    run_dir: Any,
    cfg: Config,
    persist: bool = True,
) -> Dict[str, Any]:
    """Re-derive fusion twice over one recorded run and score all three arms.

    Raises
    ------
    FileNotFoundError
        When the run carries no oracle graph. There is then nothing to score
        against, and an ablation with no reference would be three numbers with no
        meaning rather than a result.
    """
    from ..fusion.pipeline import fuse_run

    layout = run_dir if isinstance(run_dir, RunLayout) else RunLayout.from_run_dir(run_dir)
    if not layout.oracle_causal_graph.exists():
        raise FileNotFoundError(
            "no oracle causal graph at {0}; the ablation has no reference to "
            "score against".format(layout.oracle_causal_graph)
        )
    oracle = load_graph(layout.oracle_causal_graph, expect_scope=Provenance.ORACLE)

    # Arm 2 and arm 3 differ in exactly one key. Both are derived in memory:
    # nothing is written over the run's own fused artifacts, so the ablation can
    # be re-run at any time without disturbing the campaign's results.
    arms: Dict[str, Any] = {}
    local_docs: Dict[str, GraphDocument] = {}
    subject_map: Dict[str, str] = {}
    notes: List[str] = []

    for arm, enabled in (("simple_fusion", False), ("fusion_global_reasoning", True)):
        arm_cfg = cfg.with_overrides({"fusion": {"post_fusion": {"enabled": enabled}}})
        result = fuse_run(layout, arm_cfg, persist=False, fuse_event_graph=False)
        fused = result.fused_causal
        if not local_docs:
            local_docs = dict(result.local_causal)
            subject_map = dict(result.subject_map)
        scored = _arm_from_graphs(local_docs, fused, oracle, subject_map, arm_cfg)
        inferred = int(
            ((fused.meta.get("fusion") or {}).get("n_inferred_edges") or 0)
            if fused is not None else 0
        )
        arms[arm] = {
            "strict": _scores((scored["strict"] or {}).get("fused")),
            "canonical": _scores((scored["canonical"] or {}).get("fused")),
            "n_nodes": len(fused.nodes) if fused is not None else 0,
            "n_edges": len(fused.edges) if fused is not None else 0,
            "n_inferred_edges": inferred,
            INFERENCE_KEY: enabled,
        }
        if arm == "simple_fusion" and inferred:
            notes.append(
                "the simple-fusion arm reported {0} inferred edge(s); the "
                "ablation switch did not take effect".format(inferred)
            )
        # The local scores are identical in both arms -- post-fusion inference
        # runs after the merge and cannot touch a local graph -- so the baseline
        # is taken once, from the first arm.
        if "best_local" not in arms:
            best = _best_local(scored["strict"])
            if best is None:
                notes.append("no local graph was scored; there is no baseline")
            else:
                arms["best_local"] = {
                    "participant_id": best,
                    "strict": _scores(
                        (scored["strict"].get("per_participant") or {}).get(best)
                    ),
                    "canonical": _scores(
                        (scored["canonical"].get("per_participant") or {}).get(best)
                    ),
                    "n_nodes": len(local_docs[best].nodes) if best in local_docs else 0,
                    "n_edges": len(local_docs[best].edges) if best in local_docs else 0,
                    "note": (
                        "the strongest single viewpoint, not the mean of them: the "
                        "baseline is made as hard to beat as the evidence allows"
                    ),
                }

    out: Dict[str, Any] = {
        "run_dir": str(layout.root),
        "scenario_id": oracle.scenario_id,
        "seed": oracle.seed,
        "arms": {arm: arms[arm] for arm in ARMS if arm in arms},
        "ablated_key": INFERENCE_KEY,
        "reference_reachability": reference_reachability(oracle),
        "notes": notes,
        "note": (
            "three accounts of one recording, scored against the same oracle "
            "graph. Nothing was re-simulated: the arms differ only in how much "
            "reasoning was applied to identical evidence"
        ),
    }
    out["deltas"] = _deltas(out["arms"])
    if persist:
        write_json(ablation_path(layout), out)
    LOGGER.info(
        "method ablation %s: edge F1 %s -> %s -> %s (strict)",
        layout.root.name,
        _f1(out["arms"].get("best_local"), "strict"),
        _f1(out["arms"].get("simple_fusion"), "strict"),
        _f1(out["arms"].get("fusion_global_reasoning"), "strict"),
    )
    return out


def reference_reachability(oracle: GraphDocument) -> Dict[str, Any]:
    """How much of the oracle graph any reconstruction could match at all.

    The oracle writes a scripted intervention as a node: a privileged fact about
    what the scenario script did, with no counterpart in any vehicle's log. An
    edge leaving such a node can never be matched *strictly*, however well the
    incident was reconstructed, because the reconstruction has no node of that
    type to put at its tail. Reporting this alongside strict recall is what keeps
    the strict number readable -- it is the ceiling, and it is a property of the
    reference rather than a failure of the method.

    Under the canonical vocabulary those nodes fall into the behaviour family
    their declared kind implies -- a scripted brake and a recorded hard brake
    become the same family -- which is precisely the gap this measures.
    """
    from ..common.schemas import EventType

    scripted = EventType.ORACLE_SCRIPTED_INTERVENTION.value
    types = {
        n.event_id: (
            n.event_type.value if hasattr(n.event_type, "value") else str(n.event_type)
        )
        for n in oracle.nodes
    }
    total = len(oracle.edges)
    unreachable = [
        e for e in oracle.edges
        if types.get(e.source) == scripted or types.get(e.target) == scripted
    ]
    return {
        "n_reference_edges": total,
        "n_edges_touching_a_scripted_action": len(unreachable),
        "fraction_unreachable_strictly": (
            round(len(unreachable) / total, 6) if total else None
        ),
        "strict_edge_recall_ceiling": (
            round(1.0 - len(unreachable) / total, 6) if total else None
        ),
        "note": (
            "an edge at a scripted-action node cannot be matched strictly by any "
            "reconstruction, which has no such node type; the canonical "
            "vocabulary maps it to the behaviour family it denotes"
        ),
    }


def _f1(arm: Optional[Mapping[str, Any]], vocabulary: str) -> Optional[float]:
    if not arm:
        return None
    block = (arm.get(vocabulary) or {}).get("edges") or {}
    return block.get("f1")


def _deltas(arms: Mapping[str, Any]) -> Dict[str, Any]:
    """What each added capability changed, per vocabulary and per measure.

    Reported as differences rather than as a verdict: a negative delta is a
    result, not a bug, and this module does not get to decide which way the
    comparison should have come out.
    """
    out: Dict[str, Any] = {}
    steps = (
        ("fusion_over_best_local", "best_local", "simple_fusion"),
        ("reasoning_over_simple_fusion", "simple_fusion", "fusion_global_reasoning"),
        ("reasoning_over_best_local", "best_local", "fusion_global_reasoning"),
    )
    for name, low, high in steps:
        block: Dict[str, Any] = {}
        for vocabulary in ("strict", "canonical"):
            for measure in ("nodes", "edges"):
                a = ((arms.get(low) or {}).get(vocabulary) or {}).get(measure) or {}
                b = ((arms.get(high) or {}).get(vocabulary) or {}).get(measure) or {}
                for metric in ("precision", "recall", "f1"):
                    left, right = a.get(metric), b.get(metric)
                    key = "{0}_{1}_{2}".format(vocabulary, measure, metric)
                    block[key] = (
                        None if left is None or right is None
                        else round(float(right) - float(left), 6)
                    )
        out[name] = block
    return out
