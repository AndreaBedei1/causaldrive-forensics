"""Evaluation-only check of recorded CARLA clock smoke tests; no simulation writes."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from cdf.common.evidence import load_run
from cdf.common.io import read_json, write_json
from cdf.common.layout import RunLayout
from cdf.common.schemas import EventType, Provenance
from cdf.evaluation.clocks import load_clock_truth, evaluate_clock_alignment
from cdf.graph.export import load_graph


def validate(run_dir):
    layout = RunLayout.from_run_dir(run_dir)
    run = load_run(layout.root)
    truth = load_clock_truth(layout)
    alignment = read_json(layout.fusion_dir / "time_alignment.json")
    validation = read_json(layout.scenario_validation)
    assert validation["passed"], validation["problems"]
    assert run.manifest["clock_protocol"] == "independent_local_clocks"
    assert set(truth) == set(run.participant_ids)
    assert len({p["true_offset_s"] for p in truth.values()}) == len(truth)
    assert all(m["status"] == "ALIGNED" for m in alignment["offsets"].values())
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)
    assert fused.meta["time_domain"] == "common"
    collisions = read_json(layout.oracle_dir / "oracle_summary.json")["collision_pairs"]
    rows = []
    for hit in collisions:
        support = []
        for pid in (hit["a"], hit["b"]):
            profile = truth[pid]
            expected_local = profile["true_scale"] * hit["t"] + profile["true_offset_s"]
            events = [
                e for e in run.get(pid).events if e.event_type == EventType.COLLISION
            ]
            if not events:
                continue
            event = min(events, key=lambda e: abs(e.t_peak - expected_local))
            if abs(event.t_peak - expected_local) > 0.08:
                continue  # e.g. another impact suppressed by recorder debounce
            model = alignment["offsets"][pid]
            common = model["scale"] * event.t_peak + model["offset_s"]
            assert any(
                e.kind == "clock_alignment"
                and e.detail.get("participant") == pid
                and abs(e.detail["common_t_peak"] - common) < 1e-8
                for node in fused.nodes
                for e in node.evidence
            ), (pid, common)
            support.append(
                {
                    "participant": pid,
                    "local_t_peak": event.t_peak,
                    "common_t_peak": common,
                }
            )
        assert support, hit
        rows.append(
            {
                "pair": sorted([hit["a"], hit["b"]]),
                "common_t_peak": sum(s["common_t_peak"] for s in support)
                / len(support),
                "support": support,
            }
        )
    expected = {
        ("S01", "crash"): [["A", "B"]],
        ("S06", "a_front_pushed"): [["A", "B"], ["B", "C"]],
        ("S06", "b_rear_first"): [["B", "C"], ["A", "B"]],
    }[(run.manifest["scenario_id"], run.manifest["variant"])]
    actual = [r["pair"] for r in sorted(rows, key=lambda r: r["common_t_peak"])]
    assert actual == expected, (actual, expected)
    report = {
        "passed": True,
        "run_id": run.run_id,
        "common_collision_order": rows,
        "clock": evaluate_clock_alignment(alignment, truth),
        "note": "Oracle labels/time are used only here for evaluation; fused provenance supplies common/local timestamps.",
    }
    write_json(layout.evaluation_dir / "clock_smoke_validation.json", report)
    print(
        run.manifest["scenario_id"],
        run.manifest["variant"],
        "PASS",
        actual,
        "offset MAE(s)=",
        report["clock"]["mean_abs_offset_error_s"],
        "drift MAE(ppm)=",
        report["clock"]["mean_abs_drift_error_ppm"],
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", default="artifacts/independent_clock_smoke")
    args = parser.parse_args()
    layouts = sorted(Path(args.artifacts).glob("*/*/manifest.json"))
    assert len(layouts) == 3, "expected the three required smoke recordings"
    for manifest in layouts:
        validate(manifest.parent)


if __name__ == "__main__":
    main()
