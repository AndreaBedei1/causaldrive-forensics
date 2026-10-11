#!/usr/bin/env python3
"""Scenario sweeps: batches of parameterised runs, recorded, reconstructed, evaluated and summarised.

    python scripts/run_sweep.py configs/sweeps/rear_end.yaml --runs 5 --port 3000 --tm-port 8100 \
        --carla-python <python with the carla module>
    python scripts/run_sweep.py configs/sweeps/*.yaml --summarize

A sweep (``configs/sweeps/<name>.yaml``) is a canonical scenario and variant plus parameter ranges.  Run k
draws its values from a Halton sequence (deterministic, extensible: the first n runs cover the ranges
evenly for any n) shifted by the sweep's seed, and becomes the variant ``<name>_<k>`` of the scenario
(seed k), recorded by the unchanged ``scripts/run_scenario.py`` into ``<out>/<name>/<scenario>/``
(``sweeps/`` by default: raw data stay out of the repository), never into ``traces/`` and never over a run
that exists: a completed run is skipped, a left-over incomplete one is moved to ``<out>/<name>/_failed/``.
Then the reconstruction (no ground truth), its privileged evaluation and the run's outcome against ground
truth (crash, borderline -- no contact but two vehicles within 1 m -- or no crash).  ``sweep_manifest.json``
in each run directory records the scenario, variant, parameters, seed, the code at recording and at
reconstruction (git commit, dirty flag, code hash), times, outcome and status; failures are appended to
``<out>/<name>/failures.jsonl`` (one retry per run).  ``--summarize`` collects the manifests of completed
runs into ``results/sweeps/<name>.json|csv|md``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import yaml  # noqa: E402

from cdf.common.config import deep_merge, find_scenario_file  # noqa: E402
from cdf.evaluation.provenance import code_hash, provenance  # noqa: E402
from cdf.evaluation.run_metrics import run_metrics  # noqa: E402

BORDERLINE_GAP_M = 1.0  # no contact, but two vehicles' boxes this close: a near miss
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
SUMMARY_FIELDS = ("k", "variant", "outcome", "min_gap_m", "contacts", "recorders_aligned", "collisions_reconstructed",
                  "associations_correct", "associations_decided", "anonymous_tracks", "max_abs_t_global_error_s",
                  "max_abs_relative_offset_error_s", "links_correct", "links_wrong", "links_missed", "merges_correct",
                  "merges_false", "merges_missed", "entities", "fused_centre_error_median_m",
                  "single_track_centre_error_median_m", "record_wall_s", "reconstruct_wall_s", "evaluate_wall_s")


# --------------------------------------------------------------------------
# Sweep definition and sampling
# --------------------------------------------------------------------------

def load_sweep(path: Path) -> Dict[str, Any]:
    sweep = yaml.safe_load(Path(path).read_text(encoding="utf-8"))["sweep"]
    for key in ("name", "scenario", "base_variant", "seed", "parameters"):
        if key not in sweep:
            raise ValueError("{0}: sweep.{1} missing".format(path, key))
    if len(sweep["parameters"]) > len(PRIMES):
        raise ValueError("{0}: at most {1} parameters".format(path, len(PRIMES)))
    return sweep


def radical_inverse(index: int, base: int) -> float:
    value, fraction = 0.0, 1.0 / base
    while index > 0:
        index, digit = divmod(index, base)
        value += digit * fraction
        fraction /= base
    return value


def seed_shift(seed: int, dimension: int) -> float:
    """A uniform number in [0, 1) fixed by (seed, dimension): the first 8 bytes of a SHA-256."""
    digest = hashlib.sha256("{0}:{1}".format(seed, dimension).encode("ascii")).digest()
    return int.from_bytes(digest[:8], "big") / 2.0 ** 64


def halton_point(k: int, dimensions: int, seed: int) -> List[float]:
    """Point k (0-based) of a Halton sequence in [0, 1)^d, shifted modulo 1 by a seed-fixed vector
    (Cranley-Patterson rotation): deterministic, and every prefix covers the cube evenly."""
    return [(radical_inverse(k + 1, PRIMES[j]) + seed_shift(seed, j)) % 1.0 for j in range(dimensions)]


def scenario_block(scenario: str) -> Dict[str, Any]:
    return yaml.safe_load(find_scenario_file(scenario).read_text(encoding="utf-8"))["scenario"]


def _participants(block: Dict[str, Any], variant: str) -> Dict[str, Dict[str, Any]]:
    """The participants of a scenario under one of its variants (as ScenarioSpec.from_config merges them)."""
    merged = deep_merge(block, (block.get("variants") or {}).get(variant) or {})
    overrides = merged.pop("participant_overrides", {}) or {}
    return {str(p["id"]): deep_merge(p, overrides.get(str(p["id"])) or {}) for p in merged.get("participants", [])}


def _get(participants: Dict[str, Dict[str, Any]], path: str) -> Any:
    parts = path.split(".")
    if parts[0] != "participants" or len(parts) < 3:
        raise ValueError("parameter path must start with participants.<ID>.: " + path)
    node: Any = participants[parts[1]]
    rest = parts[2:]
    if rest[0] == "actions":
        node = next(action for action in node.get("actions", []) if action["action_id"] == rest[1])
        rest = rest[2:]
    for part in rest:
        node = node[part]
    return node


def sample_parameters(sweep: Dict[str, Any], k: int) -> Dict[str, Any]:
    """The values of run k: path -> value (``also`` paths get the same value; ``relative_to`` adds the
    base scenario's value of that path)."""
    base = _participants(scenario_block(sweep["scenario"]), sweep["base_variant"])
    point = halton_point(k, len(sweep["parameters"]), int(sweep["seed"]))
    values: Dict[str, Any] = {}
    for u, spec in zip(point, sweep["parameters"]):
        if "choices" in spec:
            value = spec["choices"][min(int(u * len(spec["choices"])), len(spec["choices"]) - 1)]
        else:
            value = float(spec["low"]) + u * (float(spec["high"]) - float(spec["low"]))
            if spec.get("relative_to"):
                value += float(values.get(spec["relative_to"], _get(base, spec["relative_to"])))
            value = round(value, int(spec.get("decimals", 2)))
        values[spec["path"]] = value
        for other in spec.get("also", []) or []:
            values[other] = value
    return values


def sweep_variant(sweep: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
    """The base variant with the parameter values as participant overrides (a modified action list is
    given whole: lists are replaced, not merged)."""
    block = scenario_block(sweep["scenario"])
    variant = dict((block.get("variants") or {}).get(sweep["base_variant"]) or {})
    participants = _participants(block, sweep["base_variant"])
    overrides: Dict[str, Any] = dict(variant.get("participant_overrides") or {})
    for path, value in values.items():
        parts = path.split(".")
        pid, rest = parts[1], parts[2:]
        entry = dict(overrides.get(pid) or {})
        if rest[0] == "actions":
            actions = [dict(a) for a in (entry.get("actions") or participants[pid].get("actions") or [])]
            action = next(a for a in actions if a["action_id"] == rest[1])
            node = action
            for part in rest[2:-1]:
                node[part] = dict(node.get(part) or {})
                node = node[part]
            node[rest[-1]] = value
            entry["actions"] = actions
        else:
            node = entry
            for part in rest[:-1]:
                node[part] = dict(node.get(part) or {})
                node = node[part]
            node[rest[-1]] = value
        overrides[pid] = entry
    variant["participant_overrides"] = overrides
    variant["description"] = "sweep {0}: {1}".format(sweep["name"], ", ".join(
        "{0}={1}".format(path, value) for path, value in values.items()))
    return variant


# --------------------------------------------------------------------------
# Runs
# --------------------------------------------------------------------------

def run_paths(out_root: Path, sweep: Dict[str, Any], k: int) -> Tuple[str, Path]:
    variant = "{0}_{1:03d}".format(sweep["name"], k)
    return variant, Path(out_root) / sweep["name"] / sweep["scenario"] / "run_{0}_{1}".format(k, variant)


def _code_state() -> Dict[str, Any]:
    record = provenance()
    return {"git_commit": record["git_commit"], "git_dirty": record["git_dirty"], "code_sha256": code_hash()}


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def classify_outcome(run_dir: Path) -> Dict[str, Any]:
    """Crash, borderline or no crash, from ground truth (privileged; evaluation only)."""
    from cdf.evaluation.gt_audit import truth_of
    from cdf.evaluation.reconstruction import box_gap
    truth, actors = truth_of(run_dir)
    contacts = set()
    for line in (run_dir / "ground_truth" / "collisions.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            other = actors.get(record.get("other_actor_id"))
            contacts.add("-".join(sorted([record["participant_id"], other or "static"])))
    names = sorted(truth)
    best = (math.inf, None)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = truth[names[i]], truth[names[j]]
            for state in a.states:  # every simulator frame: the closest approach can fall between two
                other = b.at(state["timestamp"])
                if other is None:
                    continue
                if math.hypot(state["transform"]["x"] - other["transform"]["x"],
                              state["transform"]["y"] - other["transform"]["y"]) > best[0] + 6.0:
                    continue  # centres too far apart to beat the closest gap so far
                gap = box_gap(state, other)
                if gap < best[0]:
                    best = (gap, "{0}-{1}".format(names[i], names[j]))
    vehicle_contacts = sorted(c for c in contacts if "static" not in c)
    outcome = "crash" if vehicle_contacts else ("borderline" if best[0] < BORDERLINE_GAP_M else "no_crash")
    return {"outcome": outcome, "contacts": vehicle_contacts, "static_contacts": sorted(c for c in contacts if "static" in c),
            "min_gap_m": None if math.isinf(best[0]) else round(best[0], 3), "min_gap_pair": best[1],
            "borderline_gap_m": BORDERLINE_GAP_M}


def record_run(args: argparse.Namespace, sweep: Dict[str, Any], k: int, variant: str,
               variant_body: Dict[str, Any]) -> Tuple[int, str, float]:
    command = [args.carla_python, str(ROOT / "scripts" / "run_scenario.py"), "--scenario", sweep["scenario"],
               "--variant", variant, "--seed", str(k), "--output", str(Path(args.out) / sweep["name"]),
               "--no-autostart", "--override", "simulation.port={0}".format(args.port),
               "--override", "simulation.traffic_manager_port={0}".format(args.tm_port),
               "--override", "simulation.real_time_pacing={0}".format("true" if args.pacing else "false"),
               "--override", "scenario.variants.{0}={1}".format(variant, json.dumps(variant_body))]
    start = time.monotonic()
    process = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True, timeout=args.timeout)
    return process.returncode, (process.stdout + process.stderr)[-4000:], round(time.monotonic() - start, 2)


def complete(run_dir: Path) -> bool:
    path = run_dir / "sweep_manifest.json"
    return path.exists() and _read_json(path).get("status") == "complete"


def set_aside(out_root: Path, sweep: Dict[str, Any], run_dir: Path) -> Optional[Path]:
    """Move a left-over incomplete run out of the way (never deleted, never overwritten)."""
    if not run_dir.exists():
        return None
    target = Path(out_root) / sweep["name"] / "_failed" / "{0}_{1}".format(run_dir.name, time.strftime("%Y%m%dT%H%M%S"))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(run_dir), str(target))
    return target


def log_failure(out_root: Path, sweep: Dict[str, Any], record: Dict[str, Any]) -> None:
    path = Path(out_root) / sweep["name"] / "failures.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def server_alive(args: argparse.Namespace) -> bool:
    """Whether the CARLA server answers within 30 s (a hung server would fail every run of the batch)."""
    probe = ("import carla; c = carla.Client('127.0.0.1', {0}); c.set_timeout(20.0); "
             "print(c.get_server_version())").format(int(args.port))
    try:
        return subprocess.run([args.carla_python, "-c", probe], capture_output=True, text=True,
                              timeout=60).returncode == 0
    except subprocess.TimeoutExpired:
        return False


def recorded(run_dir: Path) -> Optional[Dict[str, Any]]:
    """The manifest of a run whose recording succeeded (whatever happened afterwards), else None."""
    path = run_dir / "sweep_manifest.json"
    if not path.exists() or not (run_dir / "vehicles").is_dir():
        return None
    manifest = _read_json(path)
    return manifest if (manifest.get("recording") or {}).get("exit") == 0 else None


def process_run(args: argparse.Namespace, sweep: Dict[str, Any], sweep_path: Path, k: int) -> Dict[str, Any]:
    variant, run_dir = run_paths(Path(args.out), sweep, k)
    if complete(run_dir) and not args.reconstruct_only:
        return {"k": k, "status": "skipped (complete)", "run": str(run_dir)}
    previous = recorded(run_dir)
    if previous is not None:
        # The recording is there: only the reconstruction and its evaluation are (re)done.
        return analyse_run(run_dir, previous)
    if args.reconstruct_only:
        return {"k": k, "status": "skipped (no recording)", "run": str(run_dir)}
    values = sample_parameters(sweep, k)
    body = sweep_variant(sweep, values)
    manifest: Dict[str, Any] = {"sweep": sweep["name"], "sweep_file": str(sweep_path.relative_to(ROOT)).replace("\\", "/"),
                                "scenario": sweep["scenario"], "base_variant": sweep["base_variant"], "variant": variant,
                                "k": k, "seed": k, "parameters": values, "status": "started"}
    for attempt in (1, 2):
        if not server_alive(args):
            raise SystemExit("the CARLA server on port {0} does not answer: batch stopped at k={1} (resume later; "
                             "completed runs are kept)".format(args.port, k))
        aside = set_aside(Path(args.out), sweep, run_dir)
        if aside is not None:
            log_failure(Path(args.out), sweep, {"k": k, "variant": variant, "moved_incomplete_run_to": str(aside)})
        manifest["recording"] = dict(_code_state(), started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                     attempt=attempt)
        code, log, wall = record_run(args, sweep, k, variant, body)
        manifest["recording"].update(exit=code, wall_s=wall)
        if code == 0 and (run_dir / "vehicles").is_dir():
            break
        log_failure(Path(args.out), sweep, {"k": k, "variant": variant, "attempt": attempt, "exit": code, "log": log})
    else:
        manifest["status"] = "failed: recording"
        return manifest
    manifest["status"] = "recorded"
    (run_dir / "sweep_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return analyse_run(run_dir, manifest)


def analyse_run(run_dir: Path, manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Reconstruction (no ground truth), then its privileged evaluation and the run's outcome."""
    if manifest.get('reconstruction'):
        manifest.setdefault('analysis_history', []).append({key: manifest[key] for key in
                                                          ('reconstruction','evaluation','metrics') if key in manifest})
    for key in ("reconstruction", "evaluation", "outcome", "metrics"):
        manifest.pop(key, None)
    try:
        from cdf.evaluation.fusion_metrics import evaluate_fusion
        from cdf.evaluation.reconstruction import evaluate_run
        from cdf.reconstruction.pipeline import reconstruct_run
        start = time.monotonic()
        reconstruct_run(run_dir)
        manifest["reconstruction"] = dict(_code_state(), wall_s=round(time.monotonic() - start, 2),
                                          finished_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        start = time.monotonic()  # privileged, on the files the reconstruction wrote
        evaluation = evaluate_run(run_dir)
        fusion = evaluate_fusion(run_dir)
        fusion.pop("_raw", None)
        manifest["evaluation"] = {"wall_s": round(time.monotonic() - start, 2), "headline": evaluation["headline"]}
        manifest["outcome"] = classify_outcome(run_dir)
        manifest["metrics"] = run_metrics(run_dir, evaluation, fusion)
        manifest["status"] = "complete"
    except Exception as exc:  # the run stays for inspection; the batch goes on
        manifest["status"] = "failed: reconstruction or evaluation"
        manifest["error"] = repr(exc)
        manifest["trace"] = traceback.format_exc()[-4000:]
    (run_dir / "sweep_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return manifest


# --------------------------------------------------------------------------
# Summaries
# --------------------------------------------------------------------------

def summarize(sweep: Dict[str, Any], out_root: Path, results: Path) -> Dict[str, Any]:
    from cdf.evaluation.gt_audit import stats
    from cdf.reconstruction.config import load_config
    folder = Path(out_root) / sweep["name"] / sweep["scenario"]
    manifests = sorted((_read_json(path) for path in folder.glob("run_*/sweep_manifest.json")), key=lambda m: m["k"])
    done = [m for m in manifests if m.get("status") == "complete"]
    failed = [m for m in manifests if m.get("status") != "complete"]
    rows = []
    for m in done:
        metrics, outcome = m["metrics"], m["outcome"]
        rows.append(dict({"k": m["k"], "variant": m["variant"], "outcome": outcome["outcome"],
                          "min_gap_m": outcome["min_gap_m"], "contacts": ";".join(outcome["contacts"]),
                          "record_wall_s": m["recording"]["wall_s"], "reconstruct_wall_s": m["reconstruction"]["wall_s"],
                          "evaluate_wall_s": m["evaluation"]["wall_s"]},
                         **{key: metrics.get(key) for key in SUMMARY_FIELDS if key in metrics},
                         **{"param:" + path: value for path, value in m["parameters"].items()}))
    outcomes = {name: sum(r["outcome"] == name for r in rows) for name in ("crash", "borderline", "no_crash")}
    numeric = ("min_gap_m", "max_abs_t_global_error_s", "max_abs_relative_offset_error_s", "fused_centre_error_median_m",
               "single_track_centre_error_median_m", "record_wall_s", "reconstruct_wall_s", "evaluate_wall_s")
    totals = ("collisions_reconstructed", "associations_correct", "associations_decided", "anonymous_tracks",
              "links_correct", "links_wrong", "links_missed", "merges_correct", "merges_false", "merges_missed", "entities")
    record = {"sweep": sweep["name"], "scenario": sweep["scenario"], "base_variant": sweep["base_variant"],
              "description": sweep.get("description", "").strip(), "parameters": sweep["parameters"],
              "provenance": provenance(load_config().to_dict(), [m["variant"] for m in done], seed=int(sweep["seed"]),
                                       extra={"recording_commits": sorted({m["recording"]["git_commit"] for m in done}),
                                              "recording_code_sha256": sorted({m["recording"]["code_sha256"] for m in done}),
                                              "reconstruction_code_sha256": sorted({m["reconstruction"]["code_sha256"]
                                                                                     for m in done})}),
              "runs_complete": len(done), "runs_failed": [m["k"] for m in failed], "outcomes": outcomes,
              "totals": {key: sum((r.get(key) or 0) for r in rows) for key in totals},
              "distributions": {key: stats([r[key] for r in rows if r.get(key) is not None]) for key in numeric},
              "rows": rows}
    results.mkdir(parents=True, exist_ok=True)
    (results / (sweep["name"] + ".json")).write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    columns = sorted({key for row in rows for key in row}, key=lambda key: (key.startswith("param:"), key))
    with (results / (sweep["name"] + ".csv")).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    lines = ["# Sweep {0} ({1}, base variant {2})".format(sweep["name"], sweep["scenario"], sweep["base_variant"]), "",
             record["description"], "",
             "Runs complete: {0}; failed: {1}.  Outcomes: crash {2}, borderline {3}, no crash {4}.".format(
                 len(done), record["runs_failed"] or "none", outcomes["crash"], outcomes["borderline"], outcomes["no_crash"]),
             "Provenance: code `{0}`, configuration `{1}`, commit `{2}`{3}, {4}.".format(
                 record["provenance"]["code_sha256"][:16], record["provenance"]["config_sha256"][:16],
                 record["provenance"]["git_commit"], " (uncommitted changes)" if record["provenance"]["git_dirty"] else "",
                 record["provenance"]["generated_utc"]), "",
             "Totals: " + ", ".join("{0} {1}".format(key, value) for key, value in record["totals"].items()), "",
             "| quantity | n | median | q25 | q75 | p95 | max |", "|---|--:|--:|--:|--:|--:|--:|"]
    for key, row in record["distributions"].items():
        lines.append("| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(
            key, row["n"], *[("-" if row[f] is None else "{0:.3f}".format(row[f])) for f in ("median", "q25", "q75", "p95", "max")]))
    lines += ["", "| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |",
              "|--:|---|--:|---|--:|--:|---|---|--:|"]
    for r in rows:
        lines.append("| {0} | {1} | {2} | {3} | {4} | {5}/{6} | {7}/{8}/{9} | {10}/{11}/{12} | {13} |".format(
            r["k"], r["outcome"], r["min_gap_m"], r["contacts"] or "-", r.get("recorders_aligned"),
            r.get("associations_correct"), r.get("associations_decided"), r.get("links_correct"), r.get("links_wrong"),
            r.get("links_missed"), r.get("merges_correct"), r.get("merges_false"), r.get("merges_missed"),
            "-" if r.get("fused_centre_error_median_m") is None else "{0:.3f}".format(r["fused_centre_error_median_m"])))
    (results / (sweep["name"] + ".md")).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return record


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Scenario sweeps: record, reconstruct, evaluate, summarise")
    parser.add_argument("sweeps", nargs="+", type=Path, help="configs/sweeps/<name>.yaml")
    parser.add_argument("--runs", type=int, default=0, help="number of runs to process (from --start)")
    parser.add_argument("--start", type=int, default=0, help="first run index k")
    parser.add_argument("--out", default=str(ROOT / "sweeps"), help="raw and reconstructed runs (default sweeps/)")
    parser.add_argument("--results", type=Path, default=ROOT / "results" / "sweeps")
    parser.add_argument("--port", type=int, default=3000, help="CARLA RPC port of the server to record on")
    parser.add_argument("--tm-port", type=int, default=8100)
    parser.add_argument("--carla-python", default=sys.executable, help="python with the carla module")
    parser.add_argument("--timeout", type=float, default=900.0, help="seconds per recording")
    parser.add_argument("--no-pacing", dest="pacing", action="store_false",
                        help="tick as fast as possible (faster; on this machine the engine hung after a few runs)")
    parser.add_argument("--summarize", action="store_true", help="only (re)write the summaries")
    parser.add_argument("--reconstruct-only", action="store_true",
                        help="redo the reconstruction and evaluation of the recorded runs (after a code change)")
    args = parser.parse_args(argv)
    if Path(args.out).resolve() == (ROOT / "traces").resolve():
        parser.error("sweeps never write into traces/ (the canonical runs)")
    for path in args.sweeps:
        sweep = load_sweep(path)
        for k in range(args.start, args.start + args.runs):
            manifest = process_run(args, sweep, path.resolve(), k)
            print("{0} k={1}: {2} {3}".format(sweep["name"], k, manifest["status"],
                                             (manifest.get("outcome") or {}).get("outcome", "")), flush=True)
        if args.summarize or args.runs:
            record = summarize(sweep, Path(args.out), args.results)
            print("{0}: {1} complete, outcomes {2}".format(sweep["name"], record["runs_complete"], record["outcomes"]),
                  flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
