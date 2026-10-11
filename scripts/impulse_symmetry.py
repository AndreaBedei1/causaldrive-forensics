#!/usr/bin/env python3
"""Collision impulses in CARLA and what the alignment's impulse test can survive (privileged: evaluation side).

    python scripts/impulse_symmetry.py traces/S*/run_* [--out results/robustness/impulse_symmetry]

The collision-anchored alignment (``cdf.reconstruction.alignment``) pairs two recorders' reports of one
contact when their peak impulses agree within ``fusion.impulse_tolerance``.  CARLA's collision sensor
reports to both bodies of a contact the magnitude of the same contact impulse, to every digit: real
recorders would each estimate it from their own sensors (mass, accelerometer, sampling), with errors.  For
every run this script

1. checks the symmetry in the ground-truth contact log (both bodies, same frame: equal magnitudes);
2. lists every matched pair of reports in the reconstruction (``global/alignment.json``) with its impulse
   similarity, and the most similar report of a different contact from the other recorder (the margin a
   noisy impulse has before another contact competes; then only the clock consistency of the earlier
   matches separates them);
3. gives, per relative impulse noise of the robustness study (independent per report), the probability
   that the two reports of each matched contact still pass the test (Monte Carlo, 20000 draws).

Ground truth is read for (1) only; nothing here feeds the reconstruction.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

NOISE_LEVELS = (0.02, 0.05, 0.10, 0.20)  # the impulse family of scripts/robustness.py
DRAWS = 20000


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def survival(a: float, b: float, sigma: float, tolerance: float, rng: np.random.Generator) -> float:
    """P(similarity of the noisy peaks >= 1 - tolerance), multiplicative Gaussian noise per report."""
    x = a * np.maximum(0.0, 1.0 + rng.normal(0.0, sigma, DRAWS))
    y = b * np.maximum(0.0, 1.0 + rng.normal(0.0, sigma, DRAWS))
    similarity = 1.0 - np.abs(x - y) / np.maximum(np.maximum(x, y), 1e-9)
    return float(np.mean(similarity >= 1.0 - tolerance))


def analyse(run_dir: Path, tolerance: float, rng: np.random.Generator) -> Dict[str, Any]:
    states = _read_jsonl(run_dir / "ground_truth" / "states.jsonl")
    participant = {s["actor_id"]: s["participant_id"] for s in states}
    by_frame: Dict[Any, List[Dict[str, Any]]] = defaultdict(list)
    for row in _read_jsonl(run_dir / "ground_truth" / "collisions.jsonl"):
        other = participant.get(row["other_actor_id"])
        if other is not None:  # vehicle-vehicle contacts between scenario participants
            by_frame[(row["frame"], tuple(sorted((row["participant_id"], other))))].append(row)
    pairs = [rows for rows in by_frame.values() if len({r["participant_id"] for r in rows}) == 2]
    worst = max((abs(rows[0]["impulse"] - rows[1]["impulse"]) / max(rows[0]["impulse"], rows[1]["impulse"], 1e-9)
                 for rows in pairs), default=None)

    alignment = json.loads((run_dir / "reconstruction" / "global" / "alignment.json").read_text(encoding="utf-8"))
    graphs = {}
    for name in alignment["graphs"]:
        graph = json.loads((run_dir / "reconstruction" / name / "local_graph.json").read_text(encoding="utf-8"))
        graphs[name] = [n for n in graph["nodes"] if n["event_type"] == "COLLISION"]
    events = []
    for event in alignment["matched_events"]:
        (first, second) = event["graphs"]
        peaks = event["peak_impulse"]
        nodes = event["nodes"]
        # The most similar report of another contact, from either recorder against the other's report.
        competitor = 0.0
        for mine, other in ((first, second), (second, first)):
            for node in graphs[other]:
                if node["node_id"] == nodes[other]:
                    continue
                a, b = float(peaks[mine]), float(node["attributes"]["peak_impulse"])
                competitor = max(competitor, 1.0 - abs(a - b) / max(a, b, 1e-9))
        events.append({"event": event["event_id"], "graphs": [first, second],
                       "peak_impulse": {k: float(v) for k, v in peaks.items()},
                       "similarity": event["impulse_similarity"], "merged_burst": "merged_burst_of" in event,
                       "nearest_competitor_similarity": round(competitor, 4),
                       "survival": {str(s): round(survival(float(peaks[first]), float(peaks[second]), s, tolerance, rng), 4)
                                    for s in NOISE_LEVELS}})
    return {"run": "{0}/{1}".format(run_dir.parent.name, run_dir.name),
            "true_vehicle_contacts_with_two_reports": len(pairs),
            "max_relative_difference_between_the_two_reports": None if worst is None else round(worst, 9),
            "matched_events": events}


def markdown(record: Dict[str, Any]) -> str:
    lines = ["# Collision impulses: symmetry and noise margin", "",
             "CARLA's collision sensor gives both bodies of a contact the magnitude of the same contact impulse "
             "(ground-truth log: largest relative difference between the two reports of one contact, over all "
             "runs: {0}).  The alignment pairs reports whose peak impulses agree within {1:.0%} "
             "(`fusion.impulse_tolerance`, an engineering assumption); a real recorder would estimate the impulse "
             "from its own sensors, with errors.  Per matched contact: its similarity, the most similar report of "
             "another contact (above 1 - tolerance it competes, and only the clock consistency of the earlier "
             "matches separates the two), and the probability that the pair still passes the test when every "
             "report carries an independent multiplicative Gaussian error (Monte Carlo, {2} draws).".format(
                 record["max_relative_difference"], record["impulse_tolerance"], DRAWS), "",
             "| run | contact | recorders | peaks [N s] | similarity | nearest other contact | "
             + " | ".join("P(pass) at {0:.0%}".format(s) for s in NOISE_LEVELS) + " |",
             "|---|---|---|---|--:|--:|" + "--:|" * len(NOISE_LEVELS)]
    for run in record["runs"]:
        for e in run["matched_events"]:
            lines.append("| {0} | {1}{2} | {3} | {4} | {5:.3f} | {6:.3f} | {7} |".format(
                run["run"], e["event"], " (merged burst)" if e["merged_burst"] else "", "-".join(e["graphs"]),
                " / ".join("{0:.0f}".format(e["peak_impulse"][g]) for g in e["graphs"]), e["similarity"],
                e["nearest_competitor_similarity"], " | ".join("{0:.2f}".format(e["survival"][str(s)]) for s in NOISE_LEVELS)))
    lines += ["", "Mean probability over the matched contacts that a pair still passes: " + ", ".join(
        "{0:.0%} noise: {1:.2f}".format(s, record["mean_survival"][str(s)]) for s in NOISE_LEVELS) + "."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "robustness" / "impulse_symmetry")
    args = parser.parse_args()
    from cdf.evaluation.provenance import provenance
    from cdf.reconstruction.config import load_config
    cfg = load_config()
    rng = np.random.default_rng(20261011)
    runs = [analyse(run, cfg.fusion.impulse_tolerance, rng) for run in args.runs
            if (run / "reconstruction" / "global" / "alignment.json").exists()]
    differences = [r["max_relative_difference_between_the_two_reports"] for r in runs
                   if r["max_relative_difference_between_the_two_reports"] is not None]
    events = [e for r in runs for e in r["matched_events"]]
    record = {"definition": __doc__.split("\n\n")[1].replace("\n", " "),
              "provenance": provenance(cfg.to_dict(), [r["run"] for r in runs], seed=20261011),
              "impulse_tolerance": cfg.fusion.impulse_tolerance, "noise_levels": list(NOISE_LEVELS),
              "max_relative_difference": max(differences) if differences else None,
              "mean_survival": {str(s): round(statistics.fmean(e["survival"][str(s)] for e in events), 4) if events else None
                                for s in NOISE_LEVELS},
              "runs": runs}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.with_suffix(".json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    args.out.with_suffix(".md").write_text(markdown(record), encoding="utf-8")
    print(markdown(record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
