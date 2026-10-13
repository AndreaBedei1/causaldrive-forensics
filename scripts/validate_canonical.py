#!/usr/bin/env python3
"""Automatic acceptance check of the canonical development set (run after the reconstruction and evaluation).

    python scripts/validate_canonical.py [--out docs/CANONICAL_VALIDATION.md]

Checks the manifest (S01..S19, 23 runs, no gaps, no stray folders), then per run: reconstruction files present
and finite (no NaN/Inf in any JSON), every recorder aligned, collisions reconstructed (evaluation), no wrong
collision pairing, no wrong recorder link, no false merge, no global CRITICAL_TTC episode of a colliding pair
after its contact while touching, replay loading (global clock, boxes, events) and the standard replay panels
(no '?', no PREDICTED, at most the panel line limit, no repeated global subject, no recent event lost).  Ground
truth is read only through the evaluation files.  Exit status 1 on any FAIL.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.replay.model import ReplayRun  # noqa: E402
from cdf.replay.presentation import EVENT, MAX_PANEL_LINES, MORE, standard_panel_lines, subject_label  # noqa: E402

CANONICAL = {
    "S01": ["crash"], "S02": ["crash", "critical_before_cut_in"], "S03": ["crash"],
    "S04": ["a_front_pushed", "b_rear_first"], "S05": ["crash"], "S06": ["crash"], "S07": ["merge_conflict"],
    "S08": ["rolls_through"], "S09": ["near_simultaneous"], "S10": ["deflected_into_c"], "S11": ["consequential"],
    "S12": ["crash"], "S13": ["abreast", "platoon", "passing"], "S14": ["surrounded"], "S15": ["dense_platoon"],
    "S16": ["overtaking"], "S17": ["occlusion_reappearance"], "S18": ["far_to_near"], "S19": ["collision_ambiguity"],
}


def canonical_runs():
    return [ROOT / "traces" / sid / ("run_0_" + variant) for sid in sorted(CANONICAL) for variant in CANONICAL[sid]]


def _finite(value):
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(_finite(v) for v in value.values())
    if isinstance(value, list):
        return all(_finite(v) for v in value)
    return True


def manifest_problems():
    problems = []
    ids = sorted(p.name for p in (ROOT / "traces").iterdir() if p.is_dir())
    if ids != ["S{0:02d}".format(k) for k in range(1, 20)]:
        problems.append("scenario folders are not exactly S01..S19: {0}".format(ids))
    found = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "traces").glob("S*/run_*"))
    expected = sorted(p.relative_to(ROOT).as_posix() for p in canonical_runs())
    if found != expected:
        problems.append("run folders differ from the canonical set: extra {0}, missing {1}".format(
            sorted(set(found) - set(expected)), sorted(set(expected) - set(found))))
    configs = sorted(p.name.split("_")[0].upper() for p in (ROOT / "configs/scenarios").glob("*.yaml"))
    if configs != sorted(CANONICAL):
        problems.append("scenario configs are not exactly S01..S19: {0}".format(configs))
    return problems


def check_run(run: Path):
    fails, warns, info = [], [], {}
    rec = run / "reconstruction"
    for name in ("global/global_graph.json", "global/alignment.json", "global/associations.json",
                 "global/anonymous_entities.json", "evaluation/evaluation.json"):
        if not (rec / name).exists():
            fails.append("missing " + name)
    if fails:
        return fails, warns, info
    for path in rec.rglob("*.json"):
        if not _finite(json.loads(path.read_text(encoding="utf-8"))):
            fails.append("non-finite number in " + path.relative_to(rec).as_posix())
    alignment = json.loads((rec / "global/alignment.json").read_text(encoding="utf-8"))
    unaligned = [g for g, c in alignment["graphs"].items() if c["status"] != "ALIGNED"]
    if unaligned:
        warns.append("recorders not aligned: {0}".format(unaligned))
    fusion = json.loads((rec / "evaluation/fusion_metrics.json").read_text(encoding="utf-8"))
    evaluation = json.loads((rec / "evaluation/evaluation.json").read_text(encoding="utf-8"))
    collisions = evaluation.get("collisions", [])
    lost = [c for c in collisions if c.get("reconstructed_as") is None]
    info["collisions"] = "{0}/{1}".format(len(collisions) - len(lost), len(collisions))
    if lost:
        warns.append("{0} vehicle contact(s) not reconstructed".format(len(lost)))
    wrong_pairs = [c for c in collisions if c.get("reconstructed_as") is not None and c.get("participants_correct") is False]
    if wrong_pairs or evaluation.get("extra_collisions"):
        fails.append("wrong collision pairing ({0} wrong, {1} reconstructed without a contact)".format(
            len(wrong_pairs), len(evaluation.get("extra_collisions") or [])))
    verdicts = {}
    for d in fusion.get("track_decisions", []):
        key = d["verdict"].split(" (")[0]
        verdicts[key] = verdicts.get(key, 0) + 1
    info["links"] = verdicts
    if any(k.lower().startswith("wrong") for k in verdicts):
        fails.append("wrong recorder link / identity: {0}".format({k: v for k, v in verdicts.items() if k.lower().startswith("wrong")}))
    if verdicts.get("missed link"):
        warns.append("{0} missed recorder link(s) (a track of a recorder left anonymous)".format(verdicts["missed link"]))
    merges = fusion.get("merges", {})
    info["merges"] = merges
    if merges.get("false", 0):
        fails.append("{0} false merge(s)".format(merges["false"]))
    if merges.get("missed", 0):
        warns.append("{0} missed merge(s) (unresolved identities, conservative)".format(merges["missed"]))
    graph = json.loads((rec / "global/global_graph.json").read_text(encoding="utf-8"))
    for c in (n for n in graph["nodes"] if n["event_type"] == "COLLISION" and n.get("participants")):
        late = [n for n in graph["nodes"] if n["event_type"] == "CRITICAL_TTC_START" and n.get("t_global") is not None
                and n["t_global"] > c["t_global"] and {n["actor_id"], n["subject_id"]} == set(c["participants"])]
        if late:
            fails.append("global CRITICAL_TTC of {0} after their contact".format(c["participants"]))
    try:
        replay = ReplayRun.load(run)
    except Exception as exc:  # reported, never hidden
        fails.append("replay does not load: {0!r}".format(exc))
        return fails, warns, info
    if replay.clock != "t_global":
        fails.append("replay not on the global clock")
    steps = [k * 0.1 for k in range(int(replay.duration / 0.1) + 1)]
    info["boxes_max"] = max(len(replay.entities_at(t)) for t in steps)
    info["events"] = len(replay.display_events())
    for t in steps:
        for p in replay.participants:
            lines = standard_panel_lines(replay, p.participant_id, t, 1.0)
            texts = [text for text, _ in lines]
            if len(lines) > MAX_PANEL_LINES or any("?" in x or "PREDICTED" in x for x in texts):
                fails.append("panel rule broken at t={0:.1f} ({1})".format(t, p.participant_id))
                break
            subjects = [text.split(":")[0] for text, kind in lines if kind not in (EVENT, MORE)]
            if len(subjects) != len(set(subjects)):
                fails.append("a global subject repeated in a panel at t={0:.1f}".format(t))
            recent = {(e.event_type, subject_label(replay, p.participant_id, e.subject))
                      for e in replay.recent_events(p.participant_id, t, 1.0)}
            if len(recent) < MAX_PANEL_LINES and sum(kind == EVENT for _, kind in lines) != len(recent):
                fails.append("a recent event hidden at t={0:.1f}".format(t))
        if fails:
            break
    return fails, warns, info


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    lines = ["# Canonical development set: automatic validation", ""]
    problems = manifest_problems()
    lines.append("Manifest: " + ("OK (S01..S19, {0} runs)".format(len(canonical_runs())) if not problems else "FAIL: " + "; ".join(problems)))
    lines += ["", "| run | status | collisions | recorder/identity decisions | merges (correct/false/missed) | boxes (max at once) | events | warnings / failures |",
              "|---|---|---|---|---|--:|--:|---|"]
    failed = bool(problems)
    for run in canonical_runs():
        fails, warns, info = check_run(run)
        status = "FAIL" if fails else ("WARN" if warns else "PASS")
        failed |= bool(fails)
        merges = info.get("merges", {})
        lines.append("| {0} | {1} | {2} | {3} | {4}/{5}/{6} | {7} | {8} | {9} |".format(
            run.relative_to(ROOT / "traces").as_posix(), status, info.get("collisions", "-"),
            ", ".join("{0} {1}".format(k, v) for k, v in sorted(info.get("links", {}).items())),
            merges.get("correct", 0), merges.get("false", 0), merges.get("missed", 0), info.get("boxes_max", "-"),
            info.get("events", "-"), "; ".join(["FAIL: " + f for f in fails] + ["WARN: " + w for w in warns]) or "-"))
    text = "\n".join(lines) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
