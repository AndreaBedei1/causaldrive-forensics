#!/usr/bin/env python3
"""Three-method comparison of the identity association (current / corrected / retrospective).

    python scripts/retrospective_study.py traces/S18/run_* --methods current,corrected,retrospective
           --conditions exact,rtk,consumer,... --seeds 0,1,2 [--workers 8] [--keep]

Every job: a non-destructive copy of the run (hard links; the GNSS error enters as the pose source and the
impulse noise as perturbed collision reports, ``cdf.robustness.perturb``, identical draws for every
method), the reconstruction with ``fusion.association_method`` set to the method, then the privileged
evaluation (``evaluate_run``, ``evaluate_fusion``, ``identity_timeline``).  Ground truth is read only by
the evaluation, after the reconstruction wrote its files.  One line per job in
``results/retrospective/<method>/jobs.jsonl`` with its provenance (commit, config hash, method, seed,
perturbation, run, generation time).  The copies live under ``robustness/retrospective/`` (git-ignored) and
are deleted unless ``--keep``.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import shutil
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]

# name -> (robustness family, level label, parameter): the profiles of docs/robustness_profiles.md.
CONDITIONS: Dict[str, Any] = {
    "exact": ("baseline", "none", None),
    "rtk": ("gnss", "rtk", "rtk"),
    "consumer": ("gnss", "consumer", "consumer"),
    "consumer_common_0.5": ("gnss_correlated", "consumer common 0.5", 0.5),
    "consumer_common_0.9": ("gnss_correlated", "consumer common 0.9", 0.9),
    "consumer_common_1.0": ("gnss_correlated", "consumer common 1.0", 1.0),
    "degraded": ("gnss", "degraded", "degraded"),
    "exact_impulse10": ("combined", "exact + 10%", ("ideal", 0.0)),
    "rtk_impulse10": ("combined", "RTK + 10%", ("rtk", 0.0)),
    "consumer_impulse10": ("combined", "consumer independent + 10%", ("consumer", 0.0)),
    "consumer_common_0.9_impulse10": ("combined", "consumer common 0.9 + 10%", ("consumer", 0.9)),
}
METHODS = ("current", "corrected", "retrospective")
# Seeds never used to develop or tune anything (docs/RETROSPECTIVE_RECONSTRUCTION_PLAN.md, held-out policy).
DEVELOPMENT_SEEDS = (0, 1, 2, 3)
HELD_OUT_SEEDS = tuple(range(100, 110))


def run_job(job: Dict[str, Any]) -> Dict[str, Any]:
    import robustness
    from cdf.evaluation.fusion_metrics import evaluate_fusion
    from cdf.evaluation.identity_timeline import identity_samples, summarize
    from cdf.evaluation.provenance import provenance
    from cdf.evaluation.reconstruction import evaluate_run
    from cdf.evaluation.run_metrics import run_metrics
    from cdf.reconstruction.config import load_config
    from cdf.reconstruction.pipeline import reconstruct_run
    from cdf.robustness.perturb import perturbed_copy

    run_dir = Path(job["run"])
    family, level, parameter = CONDITIONS[job["condition"]]
    perturbation, pose = robustness.build(dict(run=str(run_dir), family=family, level=level,
                                               parameter=parameter, seed=job["seed"]))
    cfg = load_config()
    cfg = dataclasses.replace(cfg, fusion=dataclasses.replace(cfg.fusion, association_method=job["method"]))
    work = Path(job["work"]) / job["method"] / job["condition"] / "seed{0}".format(job["seed"])
    target = work / run_dir.parent.name / run_dir.name
    if target.exists():
        shutil.rmtree(str(target))  # a stale copy of an interrupted job (never a recording)
    result: Dict[str, Any] = {k: v for k, v in job.items() if k != "work"}
    result["provenance"] = provenance(cfg.to_dict(), runs=[str(run_dir)], perturbation=perturbation.name,
                                      seed=int(job["seed"]), extra={"method": job["method"],
                                                                    "condition": job["condition"]})
    start = time.monotonic()
    try:
        perturbed_copy(run_dir, target, perturbation, int(job["seed"]))
        reconstruct_run(target, cfg, pose_factory=pose)
        result["reconstruction_s"] = round(time.monotonic() - start, 2)
        evaluation = evaluate_run(target, clock_shift_check=False)
        fusion = evaluate_fusion(target, write=True, pose_factory=pose)
        fusion.pop("_raw", None)
        result["metrics"] = run_metrics(target, evaluation, fusion)
        result["collision_unmatched"] = sum(c.get("reconstructed_as") is None for c in evaluation["collisions"])
        alignment = json.loads((target / "reconstruction/global/alignment.json").read_text(encoding="utf-8"))
        result["ambiguous_refusals"] = sum("ambig" in str(e).lower() for e in alignment["rejected_matches"])
        result["collision_pairs"] = [{"graphs": e["graphs"], "t_local": e["t_local"]} for e in alignment["matched_events"]]
        identity = identity_samples(target)
        rows = identity["samples"]
        result["identity"] = {"all": summarize(rows), "by_distance": summarize(rows, "distance_bin"),
                              "by_time": summarize(rows, "time_bin"),
                              "relevant": summarize([r for r in rows if r.get("relevant")]),
                              "not_relevant": summarize([r for r in rows if not r.get("relevant")]),
                              "early_2s": summarize([r for r in rows if (r.get("time_before_contact_s") or 0) > 2.0])}
        verdicts: Dict[str, int] = {}
        for d in fusion["track_decisions"]:
            key = d["verdict"].split(" (")[0]
            verdicts[key] = verdicts.get(key, 0) + 1
        result["verdicts"] = verdicts
        result["merges"] = fusion["merges"]
        result["entity_purity_min"] = min((e["purity"] for e in fusion["entities"] if e["purity"] is not None), default=None)
        result["duplicate_entities"] = sum(max(0, n - 1) for n in __import__("collections").Counter(
            e["true_identity"] for e in fusion["entities"] if e["true_identity"] is not None).values())
        tracks = {}
        for r in rows:
            t = tracks.setdefault(r["track"], {"track": r["track"], "assigned": r["assigned"], "samples": 0,
                                               "outcomes": {}, "first_t": r["t_global"], "min_range_m": r["range_m"],
                                               "confidence": r["confidence"], "retrospective": r["retrospective"],
                                               "resolved_from_t_global": r["resolved_from_t_global"],
                                               "time_before_contact_s": r["time_before_contact_s"]})
            t["samples"] += 1
            t["outcomes"][r["outcome"]] = t["outcomes"].get(r["outcome"], 0) + 1
            t["min_range_m"] = min(t["min_range_m"], r["range_m"])
        votes: Dict[str, Dict[Any, int]] = {}
        for r in rows:
            if r["true"] is not None:
                votes.setdefault(r["track"], {})[r["true"]] = votes.setdefault(r["track"], {}).get(r["true"], 0) + 1
        for name, t in tracks.items():
            t["true"] = max(votes[name], key=votes[name].get) if name in votes else None
        result["tracks"] = list(tracks.values())
        entities = json.loads((target / "reconstruction/global/anonymous_entities.json").read_text(encoding="utf-8"))
        result["cannot_links"] = len(entities.get("cannot_links") or [])
        result["retrospective_decisions"] = [
            {k: d.get(k) for k in ("earlier", "later", "posterior", "gap_s", "chi2", "resolved", "candidates",
                                   "position_sigma_m", "t_old", "t_new")} for d in entities.get("retrospective") or []]
        if job.get("samples_dir"):
            out = Path(job["samples_dir"]) / job["method"] / job["condition"] / "seed{0}".format(job["seed"])
            out.mkdir(parents=True, exist_ok=True)
            (out / (run_dir.parent.name + "_" + run_dir.name + ".json")).write_text(json.dumps(identity), encoding="utf-8")
        result["status"] = "complete"
    except Exception as exc:  # recorded; the study goes on
        import traceback
        result["status"] = "failed"
        result["error"] = repr(exc)
        result["trace"] = traceback.format_exc()[-3000:]
    result["wall_s"] = round(time.monotonic() - start, 2)
    if not job.get("keep") and target.exists():
        shutil.rmtree(str(target), ignore_errors=True)
    return result


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--conditions", default="exact,rtk,consumer")
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--results", type=Path, default=ROOT / "results" / "retrospective")
    parser.add_argument("--work", type=Path, default=ROOT / "robustness" / "retrospective")
    parser.add_argument("--samples", type=Path, default=None, help="keep per-sample identity rows here")
    parser.add_argument("--tag", default="", help="suffix of the jobs file (jobs<tag>.jsonl)")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args(argv)
    methods = [m for m in args.methods.split(",") if m]
    conditions = [c for c in args.conditions.split(",") if c]
    seeds = [int(s) for s in args.seeds.split(",") if s != ""]
    for name in methods:
        if name not in METHODS:
            raise SystemExit("unknown method " + name)
    for name in conditions:
        if name not in CONDITIONS:
            raise SystemExit("unknown condition " + name)
    jobs = []
    for run in args.runs:
        for condition in conditions:
            stochastic = CONDITIONS[condition][0] != "baseline"
            for seed in (seeds if stochastic else seeds[:1]):
                for method in methods:
                    jobs.append(dict(run=str(run.resolve()), condition=condition, seed=seed, method=method,
                                     work=str(args.work.resolve()), keep=args.keep,
                                     samples_dir=str(args.samples.resolve()) if args.samples else None))
    handles = {}
    for method in methods:
        out = args.results / method
        out.mkdir(parents=True, exist_ok=True)
        handles[method] = (out / "jobs{0}.jsonl".format(args.tag)).open("a", encoding="utf-8")
    done = 0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_job, job) for job in jobs]
        for future in as_completed(futures):
            result = future.result()
            handles[result["method"]].write(json.dumps(result) + "\n")
            handles[result["method"]].flush()
            done += 1
            print(done, "/", len(jobs), result["method"], result["condition"], result["seed"],
                  Path(result["run"]).name, result["status"], result.get("wall_s"), flush=True)
    for handle in handles.values():
        handle.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
