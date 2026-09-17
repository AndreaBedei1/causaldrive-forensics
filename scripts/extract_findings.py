#!/usr/bin/env python
"""Pull the numbers that `docs/EXPERIMENTAL_FINDINGS.md` reports, with their sources.

Every figure quoted in the findings document has to be traceable to a file on
disk. This script is the bridge: it reads the persisted artifacts and prints, for
each claim, both the value and the artifact path it came from, so a reader can
check any number without re-running anything.

    python scripts/extract_findings.py --artifacts artifacts
    python scripts/extract_findings.py --json > findings.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cdf.common.io import read_json  # noqa: E402
from cdf.common.layout import RunLayout  # noqa: E402


def _get(mapping: Any, *path: str, default: Any = None) -> Any:
    node = mapping
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return default
        node = node[key]
    return node


def _outcome_row(outcome: Dict[str, Any]) -> Dict[str, Any]:
    """The subset of a replay outcome that the findings document quotes."""
    return {
        "intervention_id": outcome.get("intervention_id"),
        "action_id": outcome.get("action_id"),
        "op": outcome.get("op"),
        "targets_participant": outcome.get("targets_participant"),
        "collision": outcome.get("collision"),
        "t_collision": outcome.get("t_collision"),
        "collision_pairs": outcome.get("collision_pairs", []),
        "min_distance": outcome.get("min_distance"),
        "impact_speed": outcome.get("impact_speed"),
        "relative_impact_speed": outcome.get("relative_impact_speed"),
        "near_miss": outcome.get("near_miss"),
        "validation_passed": outcome.get("validation_passed"),
    }


def collect(artifacts_root: Path) -> Dict[str, Any]:
    """Every reportable quantity, keyed by run, with source paths attached."""
    # RunLayout resolves to an absolute path, so the root must be absolute too
    # for the relative run ids below to be computable.
    artifacts_root = artifacts_root.resolve()
    runs: List[Dict[str, Any]] = []
    for manifest_path in sorted(artifacts_root.glob("*/*/manifest.json")):
        if "counterfactual" in manifest_path.parts:
            continue
        layout = RunLayout.from_run_dir(manifest_path.parent)
        manifest = read_json(manifest_path)
        row: Dict[str, Any] = {
            "run_dir": str(layout.root.relative_to(artifacts_root).as_posix()),
            "scenario": manifest.get("scenario_id"),
            "variant": manifest.get("variant"),
            "seed": manifest.get("seed"),
            "map": manifest.get("map_name"),
            "outcome": manifest.get("outcome"),
            "collision_pairs": _get(manifest, "outcome_detail", "collision_pairs", default=[]),
            "config_hash": manifest.get("config_hash"),
            "git_commit": manifest.get("git_commit"),
            "n_frames": manifest.get("n_frames"),
            "duration_sim_s": manifest.get("duration_sim_s"),
        }

        if layout.scenario_validation.exists():
            val = read_json(layout.scenario_validation)
            row["validation_passed"] = val.get("passed")
            row["validation_problems"] = val.get("problems", [])
            sep = _get(val, "checks", "min_separation")
            row["min_separation_m"] = None if not sep else round(float(sep["distance_m"]), 3)

        row["participants"] = {}
        for pid in layout.participant_ids():
            block: Dict[str, Any] = {}
            if layout.events(pid).exists():
                payload = read_json(layout.events(pid))
                block["n_events"] = len(payload.get("events", []))
                block["event_types"] = _get(payload, "summary", "event_types", default={})
            if layout.causal_graph(pid).exists():
                doc = read_json(layout.causal_graph(pid))
                block["n_causal_nodes"] = len(doc.get("nodes", []))
                block["n_causal_edges"] = len(doc.get("edges", []))
            row["participants"][pid] = block

        if layout.fused_causal_graph.exists():
            doc = read_json(layout.fused_causal_graph)
            row["fused"] = {
                "n_nodes": len(doc.get("nodes", [])),
                "n_edges": len(doc.get("edges", [])),
            }
        if layout.fusion_diagnostics.exists():
            diag = read_json(layout.fusion_diagnostics)
            row["contradictions"] = len(diag.get("contradictions", []) or [])
            row["subject_map"] = diag.get("subject_map", {})

        if layout.oracle_causal_graph.exists():
            doc = read_json(layout.oracle_causal_graph)
            row["oracle"] = {
                "n_nodes": len(doc.get("nodes", [])),
                "n_edges": len(doc.get("edges", [])),
                "template_edges": _get(doc, "meta", "n_realised_template_edges"),
                "mechanical_edges": _get(doc, "meta", "n_mechanical_edges"),
                "unrealised": len(_get(doc, "meta", "unrealised_template_edges", default=[])),
            }

        if layout.metrics.exists():
            m = read_json(layout.metrics)
            graphs = m.get("graphs") or {}
            best = _get(graphs, "best_single_local", "metrics", default={}) or {}
            fused = graphs.get("fused") or {}
            row["metrics"] = {
                "best_local_participant": graphs.get("best_local_participant_id"),
                "best_local_edge_f1": best.get("edge_f1"),
                "best_local_node_f1": best.get("node_f1"),
                "fused_edge_f1": fused.get("edge_f1"),
                "fused_node_f1": fused.get("node_f1"),
                "fused_edge_recall": fused.get("edge_recall"),
                "fused_node_recall": fused.get("node_recall"),
                "delta_edge_f1": graphs.get("delta_edge_f1"),
                "delta_node_f1": graphs.get("delta_node_f1"),
                "delta_shd": graphs.get("delta_shd"),
            }
            benefit = m.get("fusion_benefit") or {}
            row["fusion_benefit"] = {
                "fusion_helped": benefit.get("fusion_helped"),
                "n_nodes_gained": benefit.get("n_nodes_gained"),
                "n_edges_gained": benefit.get("n_edges_gained"),
                "gained_node_types": sorted(
                    {n.get("event_type") for n in (benefit.get("gained_nodes") or [])}
                ),
                "baseline_node_recall": _get(benefit, "knowledge_gain", "baseline_node_recall"),
                "self_node_recall": _get(benefit, "knowledge_gain", "self_node_recall"),
                "baseline_edge_recall": _get(benefit, "knowledge_gain", "baseline_edge_recall"),
                "self_edge_recall": _get(benefit, "knowledge_gain", "self_edge_recall"),
            }
            assoc = m.get("association") or {}
            row["association"] = {
                "n_tracks": assoc.get("n_tracks"),
                "n_scorable": assoc.get("n_scorable"),
                "n_unscorable": assoc.get("n_unscorable"),
                "f1": assoc.get("f1"),
                "n_correct": assoc.get("n_correct"),
                "n_incorrect": assoc.get("n_incorrect"),
                "n_unresolved": assoc.get("n_unresolved"),
                "precision": assoc.get("precision"),
                "recall": assoc.get("recall"),
                "mean_rmse_m": assoc.get("mean_rmse_m"),
                "mean_confidence": assoc.get("mean_confidence"),
            }
            events = m.get("events") or {}
            row["event_metrics"] = {
                "best_local_f1": _get(events, "best_local", "f1"),
                "fused_f1": _get(events, "fused", "f1"),
                "delta_f1": events.get("delta_f1"),
            }
            row["attribution"] = m.get("attribution")
            row["local_unknowns"] = m.get("local_unknowns")

        if layout.model_check_results.exists():
            check = read_json(layout.model_check_results)
            row["model_check"] = check.get("summary")
            row["model_check_by_property"] = {
                pid: (block or {}).get("summary") or {}
                for pid, block in (check.get("by_property") or {}).items()
            }

        if layout.causal_contribution.exists():
            row["causal_contribution"] = read_json(layout.causal_contribution)

        if layout.counterfactual_manifest.exists():
            cfm = read_json(layout.counterfactual_manifest)
            contributions = _get(row, "causal_contribution", "contributions", default=[]) or []
            row["counterfactual"] = {
                "source": str(layout.counterfactual_manifest.relative_to(
                    artifacts_root).as_posix()),
                "factual": _outcome_row(cfm.get("factual") or {}),
                "n_interventions": len(cfm.get("interventions", []) or []),
                "failures": cfm.get("failures", []) or [],
                "replays": [_outcome_row(c.get("outcome") or {}) for c in contributions],
                "scores": _get(row, "causal_contribution", "classification", "scores",
                               default={}),
                "attribution_class": _get(row, "causal_contribution", "classification",
                                          "attribution_class"),
                "primary_initiator": _get(row, "causal_contribution", "classification",
                                          "primary_initiator"),
                "necessary_actions": _get(row, "causal_contribution", "classification",
                                          "necessary_actions", default=[]),
            }

        runs.append(row)

    out: Dict[str, Any] = {"artifacts_root": str(artifacts_root),
                           "n_runs": len(runs), "runs": runs}

    ablation_path = artifacts_root / "summary" / "ablation.json"
    if ablation_path.exists():
        out["ablation"] = dict(read_json(ablation_path),
                               source=str(ablation_path.relative_to(
                                   artifacts_root).as_posix()))
    return out


def render(data: Dict[str, Any]) -> str:
    """A compact console view with the source path beside every block."""
    lines: List[str] = []
    lines.append("runs: {0}".format(data["n_runs"]))
    lines.append("")
    lines.append("{0:<44} {1:<11} {2:<6} {3:<9} {4:>8}".format(
        "run", "outcome", "valid", "minsep", "fusedF1"))
    lines.append("-" * 88)
    for r in data["runs"]:
        met = r.get("metrics") or {}
        lines.append("{0:<44} {1:<11} {2:<6} {3:<9} {4:>8}".format(
            r["run_dir"][:44],
            str(r.get("outcome")),
            "yes" if r.get("validation_passed") else "NO",
            "" if r.get("min_separation_m") is None else "{0:.2f}".format(r["min_separation_m"]),
            "" if met.get("fused_edge_f1") is None else "{0:.3f}".format(met["fused_edge_f1"]),
        ))
    return "\n".join(lines)


def _fmt(value: Any, digits: int = 2) -> str:
    """Numbers as the findings document quotes them; missing stays visible."""
    if value is None:
        return "-"
    try:
        return "{0:.{1}f}".format(float(value), digits)
    except (TypeError, ValueError):
        return str(value)


def render_counterfactuals(data: Dict[str, Any]) -> str:
    """The replay tables quoted in `docs/EXPERIMENTAL_FINDINGS.md` section 9."""
    lines: List[str] = []
    for r in data["runs"]:
        cf = r.get("counterfactual")
        if not cf:
            continue
        lines.append("")
        lines.append("{0}  [{1}]".format(r["run_dir"], cf["source"]))
        head = "  {0:<42} {1:<10} {2:<8} {3:<8} {4}"
        lines.append(head.format("intervention", "collision", "t_coll",
                                 "min_sep", "pairs"))
        lines.append("  " + "-" * 84)
        fact = cf["factual"]
        lines.append(head.format(
            "(factual)", "yes" if fact.get("collision") else "no",
            _fmt(fact.get("t_collision")), _fmt(fact.get("min_distance")),
            ",".join("+".join(p) for p in fact.get("collision_pairs") or [])))
        for rep in cf["replays"]:
            lines.append(head.format(
                str(rep.get("intervention_id"))[:42],
                "yes" if rep.get("collision") else "NO",
                _fmt(rep.get("t_collision")), _fmt(rep.get("min_distance")),
                ",".join("+".join(p) for p in rep.get("collision_pairs") or [])))
        lines.append("  class={0} primary={1} necessary={2}".format(
            cf.get("attribution_class"), cf.get("primary_initiator"),
            ",".join(cf.get("necessary_actions") or []) or "-"))
        lines.append("  scores: {0}".format(
            ", ".join("{0}={1}".format(k, _fmt(v, 3))
                      for k, v in sorted((cf.get("scores") or {}).items()))))
        if cf.get("failures"):
            lines.append("  FAILED REPLAYS: {0}".format(cf["failures"]))
    return "\n".join(lines) if lines else "(no counterfactual artifacts)"


def render_ablation(data: Dict[str, Any]) -> str:
    """The radar-degradation sweep from `<artifacts>/summary/ablation.json`."""
    abl = data.get("ablation")
    if not abl:
        return "(no ablation artifacts)"
    row_fmt = "{0:<18} {1:<10} {2:>7} {3:>4} {4:>4} {5:>6} {6:>8} {7:>8} {8:>8}"
    lines = ["ablation: scenario {0} variant {1} seed {2}  [{3}]".format(
        abl.get("scenario"), abl.get("variant"), abl.get("seed"),
        abl.get("source"))]
    lines.append(row_fmt.format("profile", "outcome", "tracks", "ok", "bad",
                                "unres", "rmse_m", "node_f1", "edge_f1"))
    lines.append("-" * 82)
    for row in abl.get("rows", []):
        if "error" in row:
            lines.append("{0:<18} ERROR {1}".format(row.get("profile"),
                                                    row["error"]))
            continue
        lines.append(row_fmt.format(
            str(row.get("profile")), str(row.get("outcome")),
            str(row.get("n_tracks_total")), str(row.get("assoc_correct")),
            str(row.get("assoc_incorrect")), str(row.get("assoc_unresolved")),
            _fmt(row.get("assoc_mean_rmse_m")),
            _fmt(row.get("fused_node_f1"), 3), _fmt(row.get("fused_edge_f1"), 3)))
    return "\n".join(lines)

def render_campaign(data: Dict[str, Any]) -> str:
    """Every campaign-level number `docs/EXPERIMENTAL_FINDINGS.md` quotes.

    Replays and ablation runs are excluded: they are deliberately different
    experiments, and averaging them into the campaign would answer a question
    nobody asked.
    """
    runs = [r for r in data["runs"] if r.get("metrics")]
    lines: List[str] = []
    lines.append("campaign: {0} run(s) with metrics of {1} recorded".format(
        len(runs), data["n_runs"]))

    outcomes: Dict[str, int] = {}
    for r in data["runs"]:
        outcomes[str(r.get("outcome"))] = outcomes.get(str(r.get("outcome")), 0) + 1
    lines.append("outcomes: {0}".format(
        ", ".join("{0}={1}".format(k, v) for k, v in sorted(outcomes.items()))))
    passed = sum(1 for r in data["runs"] if r.get("validation_passed"))
    lines.append("scenario validation: {0}/{1} passed".format(passed, data["n_runs"]))
    lines.append("")

    by_scenario: Dict[str, List[Dict[str, Any]]] = {}
    for r in runs:
        by_scenario.setdefault(str(r.get("scenario")), []).append(r)

    row_fmt = ("{0:<5} {1:>4} {2:>10} {3:>10} {4:>9} {5:>9} {6:>8} {7:>12}")
    lines.append(row_fmt.format("scen", "runs", "bestlocalN", "fusedN",
                                "dNodeF1", "dEdgeF1", "nodes+", "assoc ok/n"))
    lines.append("-" * 76)
    for sid in sorted(by_scenario):
        rs = by_scenario[sid]
        def mean(key: str, block: str = "metrics") -> Optional[float]:
            vals = [r[block].get(key) for r in rs
                    if isinstance(r.get(block), dict) and r[block].get(key) is not None]
            return sum(vals) / float(len(vals)) if vals else None
        ok = sum((r.get("association") or {}).get("n_correct") or 0 for r in rs)
        tot = sum(((r.get("association") or {}).get("n_correct") or 0)
                  + ((r.get("association") or {}).get("n_incorrect") or 0)
                  + ((r.get("association") or {}).get("n_unresolved") or 0) for r in rs)
        gained = [(r.get("fusion_benefit") or {}).get("n_nodes_gained") for r in rs]
        gained = [g for g in gained if g is not None]
        lines.append(row_fmt.format(
            sid, len(rs),
            _fmt(mean("best_local_node_f1"), 3), _fmt(mean("fused_node_f1"), 3),
            _fmt(mean("delta_node_f1"), 3), _fmt(mean("delta_edge_f1"), 3),
            _fmt(sum(gained) / float(len(gained)) if gained else None, 1),
            "{0}/{1}".format(ok, tot)))
    lines.append("")

    def column(key: str) -> List[float]:
        return [r["metrics"][key] for r in runs
                if isinstance(r.get("metrics"), dict)
                and r["metrics"].get(key) is not None]

    dn, de = column("delta_node_f1"), column("delta_edge_f1")
    if dn:
        lines.append("campaign mean delta node F1: {0} over {1} run(s); "
                     "improved in {2}".format(
                         _fmt(sum(dn) / len(dn), 3), len(dn),
                         sum(1 for v in dn if v > 0)))
    if de:
        lines.append("campaign mean delta edge F1: {0} over {1} run(s); "
                     "improved in {2}".format(
                         _fmt(sum(de) / len(de), 3), len(de),
                         sum(1 for v in de if v > 0)))

    assoc = [r.get("association") or {} for r in runs]
    rmse = [a["mean_rmse_m"] for a in assoc if a.get("mean_rmse_m") is not None]
    n_correct = sum(a.get("n_correct") or 0 for a in assoc)
    n_incorrect = sum(a.get("n_incorrect") or 0 for a in assoc)
    n_unresolved = sum(a.get("n_unresolved") or 0 for a in assoc)
    lines.append("association: {0} track(s) reported = {1} scorable + {2} with no "
                 "true counterpart".format(
                     sum(a.get("n_tracks") or 0 for a in assoc),
                     sum(a.get("n_scorable") or 0 for a in assoc),
                     sum(a.get("n_unscorable") or 0 for a in assoc)))
    lines.append("  of the scorable: {0} correct, {1} incorrect, {2} unresolved "
                 "(a miss: the track HAS a true counterpart)".format(
                     n_correct, n_incorrect, n_unresolved))
    committed = n_correct + n_incorrect
    scorable = committed + n_unresolved
    if scorable:
        precision = n_correct / float(committed) if committed else 0.0
        recall = n_correct / float(scorable)
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
        lines.append("  precision {0}  recall {1}  F1 {2}".format(
            _fmt(precision, 3), _fmt(recall, 3), _fmt(f1, 3)))
    lines.append("  mean trajectory RMSE {0} m over {1} run(s)".format(
        _fmt(sum(rmse) / len(rmse) if rmse else None, 3), len(rmse)))

    verdicts: Dict[str, int] = {}
    for r in runs:
        for key, value in (r.get("model_check") or {}).items():
            if isinstance(value, int):
                verdicts[key] = verdicts.get(key, 0) + value
    if verdicts:
        lines.append("model checking: {0} (total {1})".format(
            ", ".join("{0}={1}".format(k, verdicts[k]) for k in sorted(verdicts)),
            sum(verdicts.values())))
        per_property: Dict[str, Dict[str, int]] = {}
        for r in runs:
            for pid, block in (r.get("model_check_by_property") or {}).items():
                acc = per_property.setdefault(pid, {})
                for key, value in (block or {}).items():
                    if isinstance(value, int):
                        acc[key] = acc.get(key, 0) + value
        for pid in sorted(per_property):
            acc = per_property[pid]
            lines.append("  {0:<34} PASS={1:<4} FAIL={2:<4} UNKNOWN={3}".format(
                pid, acc.get("PASS", 0), acc.get("FAIL", 0), acc.get("UNKNOWN", 0)))
        total = sum(verdicts.values())
        if total:
            lines.append("  UNKNOWN share: {0:.1f}%".format(
                100.0 * verdicts.get("UNKNOWN", 0) / total))
    return "\n".join(lines)

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", default=None)
    parser.add_argument(
        "--section", default="runs",
        choices=["runs", "campaign", "counterfactuals", "ablation", "all"],
        help="which console view to print (ignored with --json)")
    args = parser.parse_args(argv)

    data = collect(Path(args.artifacts))
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")
        print("wrote {0}".format(args.out))
    if args.json:
        print(json.dumps(data, indent=1, sort_keys=True))
    else:
        if args.section in ("runs", "all"):
            print(render(data))
        if args.section in ("campaign", "all"):
            print(render_campaign(data))
        if args.section in ("counterfactuals", "all"):
            print(render_counterfactuals(data))
        if args.section in ("ablation", "all"):
            print(render_ablation(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
