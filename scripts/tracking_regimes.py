#!/usr/bin/env python3
"""Errors of the fused road users by motion regime: a diagnostic of the tracking (Kalman filter and
Rauch-Tung-Striebel smoother) when the true vehicle brakes, turns, collides or is seen by several recorders.

    python scripts/tracking_regimes.py [--out results/g0_scorecard_20261022]      (the 22 canonical runs)

PRIVILEGED (evaluation only).  For every fused road user (``reconstruction/global/anonymous_entities.json``)
whose true identity is pure (``fusion_metrics.json``: purity 1.0), every state of its trajectory is compared
with the true state of that vehicle at the same simulator time (t_global mapped as in
``cdf.evaluation.fusion_metrics``); the true state at that instant labels the sample:

* ``after contact (0-3 s)`` / ``after contact (> 3 s)``: after the vehicle's first true contact with a vehicle;
* otherwise ``turning`` (yaw rate >= TURNING_DEG_S), else ``braking`` (deceleration along the velocity >=
  BRAKING_MPS2), else ``steady``;
* and ``one recorder`` / ``several recorders``: the road user was fused from the tracks of one or of several
  recorders.

Each sample has one motion label and one observer label.  Thresholds are diagnostic choices, not parameters of
the method.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from bisect import bisect_left
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]

BRAKING_MPS2 = 2.0
TURNING_DEG_S = 5.0
POST_CONTACT_S = 3.0
LABELS = ("steady", "braking", "turning", "after contact (0-3 s)", "after contact (> 3 s)", "one recorder",
          "several recorders")


def regimes(state: Mapping[str, Any], t_sim: float, first_contact: Optional[float], observers: int) -> List[str]:
    """The labels of one sample (module docstring) from the true state at that instant."""
    labels = []
    if first_contact is not None and t_sim >= first_contact:
        labels.append("after contact (0-3 s)" if t_sim - first_contact <= POST_CONTACT_S else "after contact (> 3 s)")
    else:
        v, a = state["velocity"], state["acceleration"]
        speed = math.hypot(v["x"], v["y"])
        along = (a["x"] * v["x"] + a["y"] * v["y"]) / speed if speed > 0.5 else 0.0
        if abs(float(state["angular_velocity"]["z"])) >= TURNING_DEG_S:
            labels.append("turning")
        elif along <= -BRAKING_MPS2:
            labels.append("braking")
        else:
            labels.append("steady")
    labels.append("several recorders" if observers >= 2 else "one recorder")
    return labels


def error_stats(values: Sequence[float]) -> Dict[str, Optional[float]]:
    if not values:
        return {"n": 0, "median": None, "p95": None, "rmse": None}
    ordered = sorted(values)
    return {"n": len(values), "median": round(statistics.median(ordered), 4),
            "p95": round(ordered[min(len(ordered) - 1, int(math.ceil(0.95 * len(ordered))) - 1)], 4),
            "rmse": round(math.sqrt(sum(v * v for v in ordered) / len(ordered)), 4)}


def _json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _jsonl(path: Path) -> List[Dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def run_samples(run_dir: Path) -> List[Dict[str, Any]]:
    """Per state of every pure fused road user: its labels and its centre and speed errors."""
    rec = Path(run_dir) / "reconstruction"
    alignment = _json(rec / "global" / "alignment.json")
    entities = _json(rec / "global" / "anonymous_entities.json").get("entities", [])
    fusion = {e["id"]: e for e in _json(rec / "evaluation" / "fusion_metrics.json").get("entities", [])}
    reference_sim = None
    for name, clock in sorted(alignment["graphs"].items()):
        if clock["status"] == "ALIGNED" and clock.get("method", "matched_collisions") in ("matched_collisions",
                                                                                         "reference_recorder"):
            origin = float(_json(rec / name / "local_graph.json")["recorder"]["clock"]["origin_source_timestamp"])
            reference_sim = -clock["offset_to_global"] + origin
            break
    if reference_sim is None:
        return []
    truth: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    actors: Dict[int, str] = {}
    for s in _jsonl(Path(run_dir) / "ground_truth" / "states.jsonl"):
        truth[str(s["participant_id"])].append(s)
        actors[int(s["actor_id"])] = str(s["participant_id"])
    times = {pid: [float(s["timestamp"]) for s in rows] for pid, rows in truth.items()}
    first_contact: Dict[str, float] = {}
    for c in _jsonl(Path(run_dir) / "ground_truth" / "collisions.jsonl"):
        if int(c["other_actor_id"]) in actors:
            pid = str(c["participant_id"])
            first_contact[pid] = min(first_contact.get(pid, math.inf), float(c["timestamp"]))
    samples = []
    for entity in entities:
        row = fusion.get(entity["id"]) or {}
        identity = row.get("true_identity")
        if identity is None or row.get("identity_is_recorder") or (row.get("purity") or 0.0) < 1.0 \
                or identity not in truth:
            continue
        observers = len({name.split(":", 1)[0] for name in entity.get("source_tracks", [])})
        for state in entity["trajectory"]:
            t_sim = reference_sim + float(state["t_global"])
            k = bisect_left(times[identity], t_sim)
            near = [j for j in (k - 1, k) if 0 <= j < len(times[identity])]
            if not near:
                continue
            j = min(near, key=lambda i: abs(times[identity][i] - t_sim))
            if abs(times[identity][j] - t_sim) > 0.03:
                continue
            true = truth[identity][j]
            centre = math.hypot(state["x"] - true["transform"]["x"], state["y"] - true["transform"]["y"])
            speed = abs(math.hypot(state["vx"], state["vy"]) - math.hypot(true["velocity"]["x"], true["velocity"]["y"]))
            samples.append({"labels": regimes(true, t_sim, first_contact.get(identity), observers),
                            "centre_error_m": centre, "speed_error_mps": speed})
    return samples


def table(samples: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for label in LABELS:
        mine = [s for s in samples if label in s["labels"]]
        rows.append({"regime": label, "centre_error_m": error_stats([s["centre_error_m"] for s in mine]),
                     "speed_error_mps": error_stats([s["speed_error_mps"] for s in mine])})
    return rows


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("runs", nargs="*", type=Path)
    parser.add_argument("--out", type=Path, default=None, help="write tracking_regimes.{json,md} here")
    args = parser.parse_args(argv)
    runs = list(args.runs)
    if not runs:
        sys.path.insert(0, str(ROOT / "scripts"))
        from validate_canonical import canonical_runs
        runs = [ROOT / run for run in canonical_runs()]
    samples = [s for run in runs for s in run_samples(run)]
    rows = table(samples)
    lines = ["# Fused road users: errors by motion regime (diagnostic)", "",
             "All pure fused road users of the runs; thresholds: braking >= {0} m/s2 along the velocity, turning >= {1} "
             "deg/s, after contact split at {2} s (`scripts/tracking_regimes.py`).".format(
                 BRAKING_MPS2, TURNING_DEG_S, POST_CONTACT_S), "",
             "| regime | samples | centre median [m] | centre P95 [m] | centre RMSE [m] | speed median [m/s] | speed P95 [m/s] |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    fmt = lambda v: "-" if v is None else "{0:.3f}".format(v)  # noqa: E731
    for r in rows:
        c, s = r["centre_error_m"], r["speed_error_mps"]
        lines.append("| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(
            r["regime"], c["n"], fmt(c["median"]), fmt(c["p95"]), fmt(c["rmse"]), fmt(s["median"]), fmt(s["p95"])))
    text = "\n".join(lines) + "\n"
    print(text)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "tracking_regimes.md").write_text(text, encoding="utf-8")
        (args.out / "tracking_regimes.json").write_text(json.dumps({"runs": [str(r) for r in runs], "rows": rows},
                                                                   indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
