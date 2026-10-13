#!/usr/bin/env python3
"""Feasibility of retrospective identity association on the S18 false merges (privileged evaluation).

    python scripts/retrospective_feasibility.py <work dir of kept METHOD 1 copies> --conditions consumer,...
           --seeds 0,1,2,3 --out docs/audit/retrospective_feasibility_S18

For every anonymous entity of the CURRENT method that mixes two true vehicles, every link that joined two
tracks of different true vehicles (a wrong link) is examined with the reconstruction's own data only:

* the evidence that would have told the two vehicles apart is searched in the recorders' observations: an
  instant where ONE recorder measures two simultaneous tracks whose returns cannot be faces of one body
  (the one-box test of ``anonymous.pair_evidence`` without the observer's pose error, which is common to
  both tracks of one recorder and cancels in their difference) -- "strong distinctness";
* for the wrong link's two tracks and for every same-recorder track pair that involves one of them or a
  track it is chained to, the strong intervals are listed with their duration, number of instants, range
  from the recorder, time before the recorder's first matched contact, separation, velocity difference,
  radars, and the gaps of the local tracks.

Ground truth (``fusion_metrics.json``: the true identity of every track) is used only to say which links are
wrong; the evidence search never reads it.  Classification of each wrong link:

RECOVERABLE           strong distinctness between the two tracks it joins (or the chain it closes) during at least
                      ``fusion.link_min_samples`` instants before the recorder's first contact;
POSSIBLY_RECOVERABLE  strong distinctness before the contact, but on fewer instants, or only after the contact;
NOT_RECOVERABLE       no instant of the recorded data distinguishes the two vehicles (backward association
                      cannot solve this case).
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]


def rebuild(run_copy: Path, condition: str, seed: int):
    """The reconstruction's in-memory common view of a kept copy (same code, config and pose source)."""
    import robustness
    from retrospective_study import CONDITIONS
    from cdf.reconstruction.anonymous import build_common_view
    from cdf.reconstruction.config import load_config
    from cdf.reconstruction.local import reconstruct_vehicle
    from cdf.reconstruction.pipeline import fuse_recorders, read_incident_context
    family, level, parameter = CONDITIONS[condition]
    _, pose = robustness.build(dict(run=str(run_copy), family=family, level=level, parameter=parameter, seed=seed))
    cfg = load_config()
    context = read_incident_context(run_copy)
    locals_ = [reconstruct_vehicle(p, cfg, context=context) for p in sorted((run_copy / "vehicles").iterdir()) if p.is_dir()]
    alignment, associations, road_users, _ = fuse_recorders(run_copy, locals_, cfg, pose)
    from cdf.reconstruction.common_frame import RecordedPoseSource
    poses = {l.owner: (pose or RecordedPoseSource.from_vehicle_dir)(run_copy / "vehicles" / l.owner, l.clock_origin)
             for l in locals_}
    view = build_common_view(locals_, alignment, associations, poses)
    return cfg, view, alignment, road_users


def pose_free(track):
    """The same track without the observer's pose variance (it is common to two tracks of one recorder)."""
    return dataclasses.replace(track, samples=[dataclasses.replace(s, pose_var=0.0) for s in track.samples])


def distinctness(a, b, cfg) -> List[Dict[str, Any]]:
    """Per simultaneous measured instant of two tracks of one recorder: is one body ruled out?"""
    from cdf.reconstruction.anonymous import chi2_2dof, fit_box, _heading
    gate = chi2_2dof(cfg.fusion.anonymous_gate_probability)
    out = []
    for sa in a.samples:
        if not sa.measured:
            continue
        sb = b.state_at(sa.t_global)
        if sb is None or not sb.measured:
            continue
        sa0, sb0 = dataclasses.replace(sa, pose_var=0.0), dataclasses.replace(sb, pose_var=0.0)
        heading = _heading([sa0, sb0], cfg)
        separation = float(np.hypot(*(sa.point - sb.point)))
        row = {"t_global": sa.t_global, "separation_m": round(separation, 3),
               "range_m": round(float(np.hypot(*(sa.near - sa.observer))), 2),
               "velocity_difference_mps": round(float(np.hypot(*(sa.velocity - sb.velocity))), 3)}
        if heading is None:
            row.update(one_box_chi2=None, distinct=False)
        else:
            try:
                fa, fb = fit_box([(a.recorder, sa0)], heading, cfg), fit_box([(b.recorder, sb0)], heading, cfg)
                joint = fit_box([(a.recorder, sa0), (b.recorder, sb0)], heading, cfg, start=(fa.centre + fb.centre) / 2.0)
                d = max(joint.chi2 - fa.chi2 - fb.chi2, 0.0)
            except (ValueError, np.linalg.LinAlgError):
                d = None
            row.update(one_box_chi2=None if d is None else round(d, 2), distinct=bool(d is not None and d > gate))
        out.append(row)
    return out


def intervals(rows: List[Dict[str, Any]], period: float = 0.051) -> List[Dict[str, Any]]:
    runs, current = [], []
    for row in rows:
        if row["distinct"] and current and row["t_global"] - current[-1]["t_global"] <= 2 * period:
            current.append(row)
        elif row["distinct"]:
            if current:
                runs.append(current)
            current = [row]
    if current:
        runs.append(current)
    return [{"start": r[0]["t_global"], "end": r[-1]["t_global"], "instants": len(r),
             "duration_s": round(r[-1]["t_global"] - r[0]["t_global"], 3),
             "range_m": [min(x["range_m"] for x in r), max(x["range_m"] for x in r)],
             "separation_m": [min(x["separation_m"] for x in r), max(x["separation_m"] for x in r)],
             "velocity_difference_mps": round(float(np.median([x["velocity_difference_mps"] for x in r])), 3)}
            for r in runs]


def analyse(run_copy: Path, condition: str, seed: int) -> List[Dict[str, Any]]:
    cfg, view, alignment, road_users = rebuild(run_copy, condition, seed)
    fm = json.loads((run_copy / "reconstruction/evaluation/fusion_metrics.json").read_text(encoding="utf-8"))
    truth = {}
    for e in fm["entities"]:
        truth.update(e["track_identities"])  # privileged: only labels links as right or wrong
    tracks = {t.name: t for t in view.tracks}
    contacts = {}
    for name, body in view.bodies.items():
        contacts[name] = min([t for t, _ in body.contacts] + [math.inf])
    out = []
    for entity in road_users.entities:
        members = entity["source_tracks"]
        if len({truth.get(t) for t in members} - {None}) < 2:
            continue
        for link in entity["association"]["links"]:
            ta, tb = truth.get(link["a"]), truth.get(link["b"])
            if ta is None or tb is None or ta == tb:
                continue
            # Evidence search (no truth): the two linked tracks, and every same-recorder simultaneous pair of
            # entity members that pairs a track on one side of the link with one on the other (the chain the
            # link closes).
            side_a = {link["a"]}
            side_b = {link["b"]}
            others = [l for l in entity["association"]["links"] if l is not link]
            changed = True
            while changed:  # the components the entity has without this link
                changed = False
                for l in others:
                    for x, y in ((l["a"], l["b"]), (l["b"], l["a"])):
                        if x in side_a and y not in side_a and y not in side_b:
                            side_a.add(y); changed = True
                        if x in side_b and y not in side_b and y not in side_a:
                            side_b.add(y); changed = True
            pairs = []
            for x in sorted(side_a):
                for y in sorted(side_b):
                    a, b = tracks.get(x), tracks.get(y)
                    if a is None or b is None or a.recorder != b.recorder:
                        continue
                    rows = distinctness(a, b, cfg)
                    if not rows:
                        continue
                    contact = contacts.get(a.recorder, math.inf)
                    found = intervals(rows)
                    before = [i for i in found if i["start"] < contact]
                    pairs.append({"tracks": [x, y], "recorder": a.recorder, "simultaneous_instants": len(rows),
                                  "distinct_instants": sum(r["distinct"] for r in rows),
                                  "distinct_before_contact": sum(r["distinct"] for r in rows if r["t_global"] < contact),
                                  "intervals": found, "contact_t_global": None if math.isinf(contact) else contact,
                                  "first_distinct_before_contact_s": None if not before else round(contact - before[0]["start"], 3),
                                  "radars": sorted({s.observer.tobytes().hex()[:0] or a.recorder for s in a.samples})[:1]})
            best = max([p["distinct_before_contact"] for p in pairs], default=0)
            after_only = any(p["distinct_instants"] > p["distinct_before_contact"] for p in pairs)
            verdict = ("RECOVERABLE" if best >= cfg.fusion.link_min_samples else
                       "POSSIBLY_RECOVERABLE" if best > 0 or after_only else "NOT_RECOVERABLE")
            out.append({"run": run_copy.parent.name + "/" + run_copy.name, "condition": condition, "seed": seed,
                        "entity": entity["id"], "link": {k: link[k] for k in ("a", "b", "kind", "passed",
                                                                                 "median_box_chi2", "centre_gap_m")},
                        "true": [ta, tb], "evidence_pairs": pairs, "verdict": verdict,
                        "same_recorder_link": link["kind"] == "same_observer",
                        "link_times": [round(tracks[link["a"]].start, 2), round(tracks[link["a"]].end, 2),
                                       round(tracks[link["b"]].start, 2), round(tracks[link["b"]].end, 2)]
                        if link["a"] in tracks and link["b"] in tracks else None})
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("work", type=Path, help="kept copies: <work>/current/<condition>/seed<k>/S18/<run>")
    parser.add_argument("--conditions", default="consumer")
    parser.add_argument("--seeds", default="0,1,2,3")
    parser.add_argument("--out", type=Path, default=ROOT / "docs/audit/retrospective_feasibility_S18")
    args = parser.parse_args()
    rows = []
    for condition in args.conditions.split(","):
        for seed in [int(s) for s in args.seeds.split(",")]:
            for run in sorted((args.work / "current" / condition / "seed{0}".format(seed) / "S18").glob("run_*")):
                rows += analyse(run, condition, seed)
                print(condition, seed, run.name, len(rows), flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.with_suffix(".json").write_text(json.dumps({"rows": rows}, indent=1) + "\n", encoding="utf-8")
    counts = defaultdict(int)
    for r in rows:
        counts[(r["condition"], r["link"]["kind"], r["verdict"])] += 1
    for key, n in sorted(counts.items()):
        print(key, n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
