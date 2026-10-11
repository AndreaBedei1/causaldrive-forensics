#!/usr/bin/env python3
"""How many runs per sweep: bootstrap of the pilot, rule of three for errors never seen, stabilisation.

    python scripts/experiment_size.py results/sweeps/*.json [--pilot 5] [--cap 40] [--write docs/experiment_size.md]

For every sweep summary (``results/sweeps/<name>.json``, written by ``scripts/run_sweep.py``) and every metric
of the paper with a value per run, the first ``--pilot`` runs are resampled with replacement (2000 times)
at sizes N, and N is the smallest size whose 95 % bootstrap interval of the campaign statistic (the median
of a per-run error, the mean of a per-run rate) is no wider than +- the metric's tolerance.  An error never
observed in the pilot (a wrong link, a false merge) gets the rule of three: after n independent trials with
none, 3/n bounds its probability at 95 %.  The chosen N is the largest over the metrics, capped by
``--cap`` (the recording budget); the interval reached at that N is reported.  With more runs recorded, the
same file shows how the statistics settle as runs are added (median, IQR and p95 at 5, 10, 20, ... runs).
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.evaluation.gt_audit import stats  # noqa: E402
from cdf.evaluation.provenance import provenance  # noqa: E402

SIZES = (5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100)
REPLICATES = 2000

# metric -> (per-run value, statistic, tolerance, relative tolerance, unit, why)
METRICS: Dict[str, Dict[str, Any]] = {
    "association_accuracy": {
        "value": lambda r: (r["associations_correct"] / r["associations_decided"]) if r.get("associations_decided") else None,
        "statistic": "mean", "tolerance": 0.05, "relative": 0.0, "unit": "share",
        "why": "identity association (contribution 2): share of decided tracks named correctly"},
    "fused_centre_error": {
        "value": lambda r: r.get("fused_centre_error_median_m"), "statistic": "median", "tolerance": 0.05,
        "relative": 0.10, "unit": "m", "why": "fusion of road users that recorded nothing (contribution 3)"},
    "alignment_error": {
        "value": lambda r: r.get("max_abs_relative_offset_error_s"), "statistic": "median", "tolerance": 0.025,
        "relative": 0.0, "unit": "s", "why": "temporal alignment (contribution 1): half a radar period"},
    "event_time_error": {
        "value": lambda r: r.get("max_abs_t_global_error_s"), "statistic": "median", "tolerance": 0.025,
        "relative": 0.0, "unit": "s", "why": "global event times (contribution 4): half a radar period"},
}
RARE = {"wrong links": ("links_wrong", ("links_correct", "links_wrong", "links_missed")),
        "false merges": ("merges_false", ("merges_correct", "merges_false", "merges_missed"))}


def _statistic(name: str) -> Callable[[Sequence[float]], float]:
    return statistics.median if name == "median" else statistics.fmean


def bootstrap_half_width(values: Sequence[float], n: int, statistic: str, seed: int) -> float:
    rng = random.Random(seed)
    function = _statistic(statistic)
    draws = sorted(function([rng.choice(values) for _ in range(n)]) for _ in range(REPLICATES))
    return (draws[int(0.975 * (REPLICATES - 1))] - draws[int(0.025 * (REPLICATES - 1))]) / 2.0


def size_for(values: Sequence[float], spec: Dict[str, Any], seed: int) -> Dict[str, Any]:
    centre = _statistic(spec["statistic"])(values)
    tolerance = max(spec["tolerance"], spec["relative"] * abs(centre))
    curve = {n: round(bootstrap_half_width(values, n, spec["statistic"], seed + n), 4) for n in SIZES}
    needed = next((n for n in SIZES if curve[n] <= tolerance + 1e-12), None)
    return {"pilot_values": [round(v, 4) for v in values], "pilot_statistic": round(centre, 4),
            "tolerance": round(tolerance, 4), "half_width_by_n": curve, "n_needed": needed}


def settling(values: Sequence[float]) -> List[Dict[str, Any]]:
    """Median, IQR and p95 of the first n runs as runs are added."""
    out = []
    for n in [n for n in (5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100) if n <= len(values)] + [len(values)]:
        row = stats(values[:n])
        out.append({"n": n, "median": row["median"], "iqr": row["iqr"], "p95": row["p95"]})
    return list({row["n"]: row for row in out}.values())


def analyse(summary: Dict[str, Any], pilot: int, cap: int) -> Dict[str, Any]:
    rows = sorted(summary["rows"], key=lambda r: r["k"])
    head = rows[:pilot]
    record: Dict[str, Any] = {"sweep": summary["sweep"], "runs": len(rows), "pilot_runs": len(head),
                              "pilot_outcomes": {o: sum(r["outcome"] == o for r in head) for o in ("crash", "borderline", "no_crash")},
                              "outcomes": summary["outcomes"], "metrics": {}, "rare": {}}
    for index, (name, spec) in enumerate(METRICS.items()):
        pilot_values = [v for v in (spec["value"](r) for r in head) if v is not None]
        all_values = [v for v in (spec["value"](r) for r in rows) if v is not None]
        if len(pilot_values) < 3:
            record["metrics"][name] = {"note": "fewer than 3 pilot values: not used to size the sweep",
                                       "unit": spec["unit"], "why": spec["why"]}
            continue
        entry = size_for(pilot_values, spec, 1000 * index + 17)
        entry.update(unit=spec["unit"], statistic=spec["statistic"], why=spec["why"], settling=settling(all_values))
        record["metrics"][name] = entry
    for name, (key, parts) in RARE.items():
        errors = sum(r.get(key) or 0 for r in rows)
        trials = sum(sum(r.get(part) or 0 for part in parts) for r in rows)
        pilot_trials = sum(sum(r.get(part) or 0 for part in parts) for r in head)
        record["rare"][name] = {"errors": errors, "trials": trials,
                                "upper_bound_95": round(3.0 / trials, 4) if trials and not errors else None,
                                "trials_per_run_in_pilot": round(pilot_trials / max(len(head), 1), 2),
                                "runs_for_5_percent_bound": (None if not pilot_trials else
                                                             int(-(-60 // max(pilot_trials / max(len(head), 1), 1e-9))))}
    needed = [m["n_needed"] for m in record["metrics"].values() if m.get("n_needed")]
    unreachable = [name for name, m in record["metrics"].items() if "n_needed" in m and m["n_needed"] is None]
    rare = [r["runs_for_5_percent_bound"] for r in record["rare"].values() if r["runs_for_5_percent_bound"]]
    choice = max(needed + rare + [pilot]) if needed or rare else pilot
    record["n_chosen"] = min(max(choice, pilot), cap) if not unreachable else cap
    record["n_capped"] = (choice > cap) or bool(unreachable)
    record["unreachable_metrics"] = unreachable
    return record


def markdown(records: List[Dict[str, Any]], pilot: int, cap: int, meta: Dict[str, Any]) -> str:
    lines = ["# Experiment size", "",
             "How many runs each sweep needs, chosen from data (`scripts/experiment_size.py`), not by habit.  Each sweep "
             "first recorded a pilot of {0} runs (`scripts/run_sweep.py --runs {0}`).  For every paper metric with a "
             "value per run, the pilot values were resampled with replacement ({1} times) at sizes N; N is the smallest "
             "size whose 95 % bootstrap interval of the campaign statistic (median of a per-run error, mean of a per-run "
             "share) is within +- the tolerance below.  Errors never seen (a wrong link, a false merge) cannot be sized "
             "by a bootstrap: after n independent trials without one, 3/n bounds their probability at 95 % (rule of "
             "three), so a 5 % bound needs 60 trials.  The chosen N is the largest over the metrics, capped at {2} runs "
             "per sweep (recording budget: about 35 s per run); where the cap binds, the interval reached is stated.  "
             "A bootstrap from a five-run pilot is crude (it cannot see values the pilot missed): the settling tables "
             "below, computed on every run recorded, check the choice after the fact.".format(pilot, REPLICATES, cap), "",
             "Tolerances: " + "; ".join("{0} +-{1} {2}{3} ({4})".format(
                 name, spec["tolerance"], spec["unit"], " or {0:.0%} of the pilot value".format(spec["relative"])
                 if spec["relative"] else "", spec["why"]) for name, spec in METRICS.items()) + ".", "",
             "Provenance: commit `{0}`{1}, code `{2}`, {3}.".format(meta["git_commit"], " (uncommitted changes)" if
                                                                  meta["git_dirty"] else "", meta["code_sha256"][:16],
                                                                  meta["generated_utc"]), "",
             "| sweep | pilot outcomes c/b/n | runs recorded | outcomes c/b/n | N chosen | capped |",
             "|---|---|--:|---|--:|---|"]
    totals = {name: (sum(r["rare"][name]["errors"] for r in records), sum(r["rare"][name]["trials"] for r in records))
              for name in RARE}
    runs = sum(r["runs"] for r in records)
    summary_line = "Over all {0} runs of the sweeps: ".format(runs) + "; ".join(
        "{0} {1} in {2} trials{3}".format(name, errors, trials, " (95 % upper bound {0:.4f})".format(3.0 / trials)
                                          if trials and not errors else "")
        for name, (errors, trials) in totals.items()) + "."
    lines.insert(lines.index("| sweep | pilot outcomes c/b/n | runs recorded | outcomes c/b/n | N chosen | capped |"), summary_line)
    lines.insert(lines.index(summary_line) + 1, "")
    for r in records:
        po, o = r["pilot_outcomes"], r["outcomes"]
        lines.append("| {0} | {1}/{2}/{3} | {4} | {5}/{6}/{7} | {8} | {9} |".format(
            r["sweep"], po["crash"], po["borderline"], po["no_crash"], r["runs"], o["crash"], o["borderline"],
            o["no_crash"], r["n_chosen"], "yes" if r["n_capped"] else "no"))
    for r in records:
        lines += ["", "## " + r["sweep"], ""]
        for name, m in r["metrics"].items():
            if "note" in m:
                lines.append("- {0}: {1}.".format(name, m["note"]))
                continue
            curve = ", ".join("N={0}: +-{1}".format(n, w) for n, w in m["half_width_by_n"].items() if n <= 60)
            lines.append("- {0} ({1} of per-run values, {2}): pilot {3} = {4}, tolerance +-{5}; 95 % half-width {6}; "
                         "needs N = {7}.".format(name, m["statistic"], m["unit"], m["statistic"], m["pilot_statistic"],
                                                 m["tolerance"], curve, m["n_needed"] or "> 100"))
            lines.append("  Settling: " + "; ".join("n={0}: median {1}, IQR {2}, p95 {3}".format(
                s["n"], s["median"], s["iqr"], s["p95"]) for s in m["settling"]) + ".")
        for name, rare in r["rare"].items():
            lines.append("- {0}: {1} in {2} trials{3}; {4} trials per run in the pilot -> {5} runs for a 5 % bound.".format(
                name, rare["errors"], rare["trials"], "" if rare["upper_bound_95"] is None else
                " (95 % upper bound {0})".format(rare["upper_bound_95"]), rare["trials_per_run_in_pilot"],
                rare["runs_for_5_percent_bound"] or "-"))
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Number of runs per sweep from the pilot (bootstrap, rule of three)")
    parser.add_argument("summaries", nargs="+", type=Path)
    parser.add_argument("--pilot", type=int, default=5)
    parser.add_argument("--cap", type=int, default=40)
    parser.add_argument("--write", type=Path, default=ROOT / "docs" / "experiment_size.md")
    parser.add_argument("--json", type=Path, default=ROOT / "results" / "sweeps" / "experiment_size.json")
    args = parser.parse_args(argv)
    summaries = [json.loads(path.read_text(encoding="utf-8")) for path in args.summaries
                 if path.name != "experiment_size.json"]
    records = [analyse(summary, args.pilot, args.cap) for summary in summaries]
    meta = provenance(runs=[r["sweep"] for r in records])
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps({"provenance": meta, "pilot": args.pilot, "cap": args.cap, "sweeps": records},
                                    indent=1) + "\n", encoding="utf-8")
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(markdown(records, args.pilot, args.cap, meta), encoding="utf-8")
    for r in records:
        print("{0}: N = {1}{2}".format(r["sweep"], r["n_chosen"], " (capped)" if r["n_capped"] else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
