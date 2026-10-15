#!/usr/bin/env python3
"""Held-out generalization study of the frozen reconstruction on new simulated traffic configurations.

    python scripts/generalization.py check     [--port 3000]   static spawn / route resolution, no simulation
    python scripts/generalization.py record    [--port 3000]   record every predeclared case (resumable)
    python scripts/generalization.py evaluate  [--workers N]   frozen reconstruction + existing evaluation
    python scripts/generalization.py report                    tables and figure

The cases are predeclared in ``configs/heldout/frozen_campaign.yaml`` (base scenario, physical changes, intended
outcome, acceptance criteria).  Recordings go to ``heldout/frozen_campaign/<case>/`` (never ``traces/``), the
records of recording, validity and evaluation to ``results/generalization/frozen_campaign/``.  Ground truth is
read by the validity check and the evaluation only; the reconstruction under test never sees it.  Every actual
outcome is kept: a case whose contact differs from the intended one is reported as such, never re-recorded or
replaced, and a physically invalid recording is reported individually and left out of the aggregates.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]

PROTOCOL = ROOT / "configs" / "heldout" / "frozen_campaign.yaml"
RECORDINGS = ROOT / "heldout" / "frozen_campaign"
RESULTS = ROOT / "results" / "generalization" / "frozen_campaign"


def load_protocol(path: Path = PROTOCOL) -> Dict[str, Any]:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _append(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, default=str) + "\n")


def case_spec(case: Dict[str, Any], port: int):
    """(run configuration, scenario spec) of a held-out case: its base scenario with the case's changes as a
    variant of its own, named after the case's family; scenario id = the case id."""
    from cdf.common.config import deep_merge, load_run_config
    from cdf.simulation.scenario_base import ScenarioSpec
    cfg = load_run_config(case["base"], overrides=["simulation.port={0}".format(port),
                                                   "simulation.traffic_manager_port=8100"])
    block = cfg.get("scenario")
    base_variant = case.get("base_variant") or block.get("default_variant", "default")
    base_changes = (block.get("variants") or {}).get(base_variant) or {}
    variant = deep_merge(base_changes, case.get("changes") or {})
    variant = deep_merge(variant, {"scenario_id": case["id"], "description": case.get("description", "")})
    name = case["family"]
    cfg = cfg.with_overrides({"scenario": {"variants": {name: variant}}})
    spec = ScenarioSpec.from_config(cfg, variant=name)
    for action_id in case.get("disable_actions") or []:
        matches = [a for p in spec.participants for a in p.actions if a.action_id == action_id]
        if not matches:
            raise KeyError("case {0}: no action {1!r}".format(case["id"], action_id))
        for action in matches:
            action.enabled = False
    return cfg, spec


def run_dir_of(case: Dict[str, Any]) -> Path:
    return RECORDINGS / case["id"] / "run_0_{0}".format(case["family"])


# --------------------------------------------------------------------------------------------------------------
# check / record
# --------------------------------------------------------------------------------------------------------------

def _world(client: Any, map_name: str):
    world = client.get_world()
    if not world.get_map().name.endswith(map_name):
        client.load_world(map_name)
        deadline = time.monotonic() + 120.0
        while time.monotonic() < deadline:  # the server switches maps asynchronously
            world = client.get_world()
            if world.get_map().name.endswith(map_name):
                break
            time.sleep(1.0)
        else:
            raise RuntimeError("map {0} did not load".format(map_name))
    return world


def check(args: argparse.Namespace) -> int:
    """Static check: every spawn and route resolves and no two spawns overlap.  No simulation, no outcome."""
    import carla
    from cdf.simulation.scenario_base import build_route, resolve_spawn_waypoint
    protocol = load_protocol()
    client = carla.Client("127.0.0.1", args.port)
    client.set_timeout(120.0)
    rows = []
    for case in protocol["cases"]:
        row = {"case": case["id"], "family": case["family"], "base": case["base"]}
        try:
            cfg, spec = case_spec(case, args.port)
            world = _world(client, spec.map_name)
            carla_map = world.get_map()
            spawns = carla_map.get_spawn_points()
            points, lanes = {}, {}
            for p in spec.participants:
                wp = resolve_spawn_waypoint(carla_map, spawns, p.spawn)
                build_route(carla_map, wp, p.route)
                points[p.participant_id] = wp.transform.location
                lanes[p.participant_id] = (wp.road_id, wp.lane_id)
            # Overlap: closer than 3 m (bodies touch), or in the same lane closer than 6 m (abreast vehicles in
            # adjacent lanes, 3.5 m apart, are a normal configuration).
            close = [(a, b, round(points[a].distance(points[b]), 2)) for i, a in enumerate(points)
                     for b in list(points)[i + 1:] if points[a].distance(points[b]) < 3.0
                     or (lanes[a] == lanes[b] and points[a].distance(points[b]) < 6.0)]
            row.update(status="ok" if not close else "overlapping spawns", overlapping=close,
                       participants=len(spec.participants), recorders=spec.recorder_ids, map=spec.map_name)
        except Exception as exc:
            row.update(status="error", error=repr(exc))
        rows.append(row)
        print(row, flush=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "static_check.json").write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")
    return 0 if all(r["status"] == "ok" for r in rows) else 1


def validity(run: Path, carla_map: Any, spec: Any, acceptance: Dict[str, Any]) -> Dict[str, Any]:
    """The predeclared physical acceptance checks of one recording (privileged: simulator truth)."""
    import carla
    states = _read_jsonl(run / "ground_truth" / "states.jsonl")
    collisions = _read_jsonl(run / "ground_truth" / "collisions.jsonl")
    first_contact: Dict[str, float] = {}
    for c in collisions:
        pid = c["participant_id"]
        first_contact[pid] = min(first_contact.get(pid, math.inf), float(c["timestamp"]))
    limits = {}
    for p in spec.participants:
        speeds = [p.initial_speed, p.target_speed] + [a.params.get("target_speed", 0.0) for a in p.actions
                                                     if a.kind in ("set_speed", "hold") and a.enabled]
        limits[p.participant_id] = max(speeds) + float(acceptance["speed_bound_mps"])
    problems: List[str] = []
    seen = set()
    off_road, fast, tilted, flipped = {}, {}, {}, {}
    for s in states:
        pid = s["participant_id"]
        seen.add(pid)
        t = float(s["timestamp"])
        tf = s["transform"]
        before = t < first_contact.get(pid, math.inf)
        if abs(tf["pitch_deg"]) > acceptance["attitude_whole_run_deg"] or abs(tf["roll_deg"]) > acceptance["attitude_whole_run_deg"]:
            flipped[pid] = flipped.get(pid, 0) + 1
        if not before:
            continue
        if abs(tf["pitch_deg"]) > acceptance["attitude_before_contact_deg"] or abs(tf["roll_deg"]) > acceptance["attitude_before_contact_deg"]:
            tilted[pid] = tilted.get(pid, 0) + 1
        speed = math.hypot(s["velocity"]["x"], s["velocity"]["y"])
        if speed > limits.get(pid, math.inf):
            fast[pid] = max(fast.get(pid, 0.0), round(speed, 2))
        wp = carla_map.get_waypoint(carla.Location(x=tf["x"], y=tf["y"], z=tf["z"]), project_to_road=False,
                                    lane_type=carla.LaneType.Driving)
        if wp is None:
            off_road[pid] = off_road.get(pid, 0) + 1
    missing = sorted(set(spec.participant_ids) - seen)
    if missing:
        problems.append("participants without ground truth: {0}".format(missing))
    if off_road:
        problems.append("off a driving lane before contact (samples): {0}".format(off_road))
    if fast:
        problems.append("speed above the scripted bound before contact (m/s): {0}".format(fast))
    if tilted:
        problems.append("pitch/roll above {0} deg before contact (samples): {1}".format(
            acceptance["attitude_before_contact_deg"], tilted))
    if flipped:
        problems.append("pitch/roll above {0} deg (samples): {1}".format(acceptance["attitude_whole_run_deg"], flipped))
    return {"valid": not problems, "problems": problems}


def actual_contacts(run: Path) -> List[List[str]]:
    """The true vehicle-vehicle contact pairs of a recording (ground truth)."""
    actor = {}
    for s in _read_jsonl(run / "ground_truth" / "states.jsonl")[:400]:
        actor.setdefault(s["actor_id"], s["participant_id"])
    pairs = set()
    for c in _read_jsonl(run / "ground_truth" / "collisions.jsonl"):
        other = actor.get(c.get("other_actor_id"))
        if other is not None:
            pairs.add(tuple(sorted((c["participant_id"], other))))
    return [list(p) for p in sorted(pairs)]


def record(args: argparse.Namespace) -> int:
    from cdf.simulation.carla_client import client_from_config
    from cdf.simulation.runner import run_scenario
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    protocol = load_protocol()
    log = RESULTS / "recordings.jsonl"
    done = {r["case"] for r in _read_jsonl(log) if r.get("status") == "recorded"}
    attempts: Dict[str, int] = {}
    for r in _read_jsonl(log):
        attempts[r["case"]] = attempts.get(r["case"], 0) + 1
    for case in protocol["cases"]:
        if args.cases and case["id"] not in args.cases:
            continue
        if case["id"] in done or attempts.get(case["id"], 0) >= args.max_attempts:
            continue
        row: Dict[str, Any] = {"case": case["id"], "family": case["family"], "base": case["base"],
                               "intended": case.get("intended"), "attempt": attempts.get(case["id"], 0) + 1}
        start = time.monotonic()
        try:
            cfg, spec = case_spec(case, args.port)
            target = run_dir_of(case)
            if target.exists():
                import shutil
                shutil.rmtree(str(target))  # an interrupted attempt: never a completed recording
            client = client_from_config(cfg, autostart=False)
            path = run_scenario(client, cfg, spec, 0, output_root=str(RECORDINGS))
            row["run"] = str(Path(path).relative_to(ROOT).as_posix())
            row["validity"] = validity(Path(path), client.get_world().get_map(), spec, protocol["protocol"]["acceptance"])
            row["actual_contacts"] = actual_contacts(Path(path))
            row["status"] = "recorded"
        except Exception as exc:
            row.update(status="failed", error=repr(exc), trace=traceback.format_exc()[-3000:])
        row["wall_s"] = round(time.monotonic() - start, 1)
        _append(log, row)
        print(case["id"], row["status"], row.get("validity"), row.get("actual_contacts"), row.get("error", ""), flush=True)
        if row["status"] == "failed" and "time-out" in row.get("error", "").lower():
            print("engine not responding: stop here and restart the private engine, then resume", flush=True)
            return 2
    return 0


# --------------------------------------------------------------------------------------------------------------
# evaluate
# --------------------------------------------------------------------------------------------------------------

def evaluate_one(run: str) -> Dict[str, Any]:
    """The frozen reconstruction of one held-out recording and the campaign's existing evaluation."""
    from cdf.evaluation.fusion_metrics import evaluate_fusion
    from cdf.evaluation.provenance import provenance
    from cdf.evaluation.reconstruction import evaluate_run
    from cdf.evaluation.run_metrics import run_metrics
    from cdf.reconstruction.config import load_config
    from cdf.reconstruction.pipeline import reconstruct_run
    import robustness
    path = ROOT / run
    result: Dict[str, Any] = {"run": run, "configuration": "frozen"}
    start = time.monotonic()
    cfg = load_config()
    result["provenance"] = provenance(cfg.to_dict(), runs=[run], perturbation="none (held-out recording)", seed=0)
    try:
        reconstruct_run(path, cfg)
        result["reconstruction_wall_s"] = round(time.monotonic() - start, 2)
        evaluation = evaluate_run(path, clock_shift_check=False)
        fusion = evaluate_fusion(path, write=True)
        full = dict(fusion)
        fusion.pop("_raw", None)
        result["metrics"] = run_metrics(path, evaluation, fusion)
        result["collision_unmatched"] = sum(c.get("reconstructed_as") is None for c in evaluation["collisions"])
        result.update(robustness.extra_evaluation(path, evaluation, full))
        result["status"] = "complete"
    except Exception as exc:
        result.update(status="failed", error=repr(exc), trace=traceback.format_exc()[-3000:])
    result["wall_s"] = round(time.monotonic() - start, 2)
    result["resources"] = robustness._resources()
    return result


def evaluate(args: argparse.Namespace) -> int:
    recordings = {r["case"]: r for r in _read_jsonl(RESULTS / "recordings.jsonl") if r.get("status") == "recorded"}
    log = RESULTS / "jobs.jsonl"
    finished = {r["case"] for r in _read_jsonl(log) if r.get("status") == "complete"}
    pending = [r for case, r in sorted(recordings.items()) if case not in finished]
    print(len(pending), "held-out runs to evaluate", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(evaluate_one, r["run"]): r for r in pending}
        for future in as_completed(futures):
            rec = futures[future]
            result = future.result()
            result.update(case=rec["case"], family=rec["family"], valid=rec["validity"]["valid"],
                          intended=rec.get("intended"), actual_contacts=rec.get("actual_contacts"))
            _append(log, result)
            print(rec["case"], result["status"], result.get("wall_s"), result.get("error", ""), flush=True)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("check", "record", "evaluate", "report"))
    parser.add_argument("--port", type=int, default=3000)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-attempts", type=int, default=2)
    parser.add_argument("--cases", nargs="*", default=[])
    args = parser.parse_args(argv)
    if args.command == "check":
        return check(args)
    if args.command == "record":
        return record(args)
    if args.command == "evaluate":
        return evaluate(args)
    import campaign_report
    return campaign_report.generalization_report(RESULTS)


if __name__ == "__main__":
    raise SystemExit(main())
