"""Scientific scorecard of one reconstructed run (PRIVILEGED: evaluation only).

A small set of metrics that answer the study's question (is the accident reconstructed?), built on the
verdicts the existing evaluation already writes (``evaluation.json``, ``fusion_metrics.json``,
``event_oracle.json``) and on the ground truth.  Nothing here changes a threshold of the reconstruction or of
those verdicts; where a new rule is needed it is stated below and kept deliberately simple.

1. Collisions.  The true vehicle-vehicle contacts are those of ``evaluation.json`` (``collisions``).  A contact is
   DETECTED when the reconstruction holds a collision node for it, IDENTIFIED when that node names exactly its
   participants.  ``extra_collisions`` are invented collisions.  precision = identified / (detected +
   invented); recall = detected / true; the timing error is the evaluation's ``report_timing_error_s``.  A contact
   none of whose vehicles records is listed (``involves_recorder`` false): no collision sensor reports it.
2. Completeness.  Every true vehicle is either a recorder (represented by its own pose stream) or a road user
   that recorded nothing.  Such a road user is OBSERVABLE when it lay in the field of view of some recorder radar
   with a clear line of sight (``cdf.evaluation.visibility``, partial bodies count) for at least
   ``min_track_frames`` radar sweeps -- the fewest the tracker can turn into a track.  It is REPRESENTED when an
   anonymous road user of the fusion has it as true identity (``fusion_metrics.entities``).  Duplicates: further
   road users of the same true vehicle; phantoms: road users with no true identity.  Coverage: the represented
   time of a vehicle (sum of its road users' ``coverage_s``, capped) over its observable time.
3. Position and speed of the reconstructed road users against the truth: median, P95 and mean of the centre
   error and of the speed error (``fusion_metrics.state_errors``); heading is a diagnostic only.
4. Association: wrong recorder links, false and missed merges, fragmented vehicles, phantoms.
5. Essential semantics, by physical meaning rather than exact timestamps:
   * CRITICAL_TTC warning: for each true contact and each recorder involved in it, the first CRITICAL_TTC_START
     about the partner in the ``WARNING_WINDOW_S`` before the contact (the reconstruction's subject is the
     track's true identity, as in the oracle).  ``in_time`` when it precedes the contact; the lead time is
     reported.  ``justified`` when the COVERAGE oracle (ideal tracks while observable) also raises one about the
     partner in that window -- otherwise the warning was not observable or not justified by the definition.
   * Path intrusion: EGO_PATH_ENTRY and CUT_IN_*_START about the same subject are one manoeuvre; an oracle
     intrusion is found when the reconstruction reports either kind for the same recorder and subject within
     ``MATCH_WINDOW_S``, in any order.
   * Unconfirmed CRITICAL_TTC alarms: reconstruction CRITICAL_TTC_START with no COVERAGE counterpart within
     ``MATCH_WINDOW_S`` and no true contact of the pair within ``WARNING_WINDOW_S`` after it.  These are
     CANDIDATES for visual review, not proven false alarms: the oracle itself is an idealisation.
"""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from .visibility import Box, coverage, frames_by_participant, RadarView

WARNING_WINDOW_S = 8.0
MATCH_WINDOW_S = 2.0
INTRUSION_TYPES = ("EGO_PATH_ENTRY", "CUT_IN_FROM_LEFT_START", "CUT_IN_FROM_RIGHT_START")


def _json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _jsonl(path: Path) -> List[Dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _radar_views(vehicle_dir: Path) -> List[RadarView]:
    views = []
    radar = Path(vehicle_dir) / "radar"
    for meta in sorted(radar.glob("*/metadata.json")) if radar.is_dir() else []:
        views.append(RadarView.from_metadata(_json(meta)))
    return views


def observable_seconds(run_dir: Path, recorders: List[str], min_frames: int, step: int = 1
                       ) -> Dict[str, Dict[str, Any]]:
    """For each non-recorder vehicle: seconds in view of some recorder radar, and whether that reaches
    ``min_frames`` sweeps (frames sampled every ``step``; radar sweeps are one per frame at 20 Hz)."""
    states = _jsonl(Path(run_dir) / "ground_truth" / "states.jsonl")
    frames = frames_by_participant(states)
    ordered = sorted(frames)
    dt = 0.05
    if len(ordered) > 1:
        a, b = frames[ordered[0]], frames[ordered[1]]
        dt = float(next(iter(b.values()))["timestamp"]) - float(next(iter(a.values()))["timestamp"])
    views = {r: _radar_views(Path(run_dir) / "vehicles" / r) for r in recorders}
    others = sorted({s["participant_id"] for s in states} - set(recorders))
    seen = {pid: 0 for pid in others}
    for frame in ordered[::step]:
        world = frames[frame]
        boxes = {pid: Box(state) for pid, state in world.items()}
        for pid in others:
            if pid not in world:
                continue
            if any(r in world and views[r] and coverage(world[r], pid, world, views[r], boxes).visible
                   for r in recorders):
                seen[pid] += step
    return {pid: {"visible_s": round(n * dt, 3), "observable": n >= min_frames} for pid, n in seen.items()}


def _origins(run_dir: Path, recorders: List[str]) -> Dict[str, float]:
    out = {}
    for r in recorders:
        path = Path(run_dir) / "vehicles" / r / "ego.jsonl"
        with path.open(encoding="utf-8") as handle:
            out[r] = float(json.loads(handle.readline())["timestamp"])
    return out


def _stat(block: Optional[Mapping[str, Any]]) -> Dict[str, Optional[float]]:
    block = block or {}
    return {"n": block.get("n", 0), "median": block.get("median"), "p95": block.get("p95"), "mean": block.get("mean")}


def scorecard(run_dir: Path, min_track_frames: int = 5) -> Dict[str, Any]:
    run_dir = Path(run_dir)
    ev_dir = run_dir / "reconstruction" / "evaluation"
    evaluation = _json(ev_dir / "evaluation.json")
    fusion = _json(ev_dir / "fusion_metrics.json")
    oracle = _json(ev_dir / "event_oracle.json") if (ev_dir / "event_oracle.json").exists() else None
    gt_meta = _json(run_dir / "ground_truth" / "metadata.json")
    recorders = [p["participant_id"] for p in gt_meta.get("participants", []) if p.get("record")]
    all_vehicles = [p["participant_id"] for p in gt_meta.get("participants", [])]
    if not all_vehicles:  # recordings made before the ground-truth metadata listed the participants
        with (run_dir / "ground_truth" / "states.jsonl").open(encoding="utf-8") as handle:
            all_vehicles = sorted({json.loads(line)["participant_id"] for line in handle if line.strip()})
        recorders = sorted(p.name for p in (run_dir / "vehicles").iterdir() if (p / "ego.jsonl").exists())

    # 1. Collisions
    contacts = []
    for c in evaluation.get("collisions", []):
        pair = tuple(sorted(c["participants"]))
        contacts.append({"pair": "-".join(pair), "sim_time": c["sim_time"],
                         "involves_recorder": any(p in recorders for p in pair),
                         "detected": c.get("reconstructed_as") is not None,
                         "participants_correct": bool(c.get("participants_correct")),
                         "timing_error_s": c.get("report_timing_error_s")})
    n_true = len(contacts)
    detected = sum(c["detected"] for c in contacts)
    identified = sum(c["detected"] and c["participants_correct"] for c in contacts)
    invented = len(evaluation.get("extra_collisions", []))
    timing = [abs(c["timing_error_s"]) for c in contacts if c["detected"] and c["timing_error_s"] is not None]
    collisions = {"true": n_true, "detected": detected, "identified": identified, "invented": invented,
                  "recall": detected / n_true if n_true else None,
                  "participants_correct_rate": identified / n_true if n_true else None,
                  "precision": identified / (detected + invented) if (detected + invented) else None,
                  "max_abs_timing_error_s": max(timing) if timing else None, "contacts": contacts,
                  "invented_list": evaluation.get("extra_collisions", [])}

    # 2. Completeness
    visibility = observable_seconds(run_dir, recorders, min_track_frames)
    entities = fusion.get("entities", [])
    per_truth: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    phantoms = []
    for e in entities:
        if e.get("true_identity") is None:
            phantoms.append(e["id"])
        else:
            per_truth[e["true_identity"]].append(e)
    entity_cov = {e["id"]: e.get("coverage_s", 0.0) for e in fusion.get("entity_errors", [])}
    vehicles = []
    for pid in all_vehicles:
        if pid in recorders:
            vehicles.append({"vehicle": pid, "role": "recorder", "observable": True, "represented": True,
                             "road_users": [], "coverage": 1.0})
            continue
        vis = visibility.get(pid, {"visible_s": 0.0, "observable": False})
        mine = [e for e in per_truth.get(pid, []) if not e.get("identity_is_recorder")]
        represented_s = sum(entity_cov.get(e["id"], 0.0) for e in mine)
        cov = min(1.0, represented_s / vis["visible_s"]) if vis["visible_s"] > 0 else None
        vehicles.append({"vehicle": pid, "role": "non-recorder", "observable": vis["observable"],
                         "visible_s": vis["visible_s"], "represented": bool(mine),
                         "road_users": [e["id"] for e in mine], "coverage": None if cov is None else round(cov, 3)})
    observable = [v for v in vehicles if v["observable"]]
    duplicates = sum(max(0, len(v["road_users"]) - 1) for v in vehicles)
    completeness = {"true_vehicles": len(vehicles), "recorders": len(recorders),
                    "observable": len(observable), "represented_observable": sum(v["represented"] for v in observable),
                    "unobservable": [v["vehicle"] for v in vehicles if not v["observable"]],
                    "missed_observable": [v["vehicle"] for v in observable if not v["represented"]],
                    "represented_unobservable": [v["vehicle"] for v in vehicles
                                                 if not v["observable"] and v["represented"]],
                    "duplicates": duplicates, "phantoms": phantoms, "vehicles": vehicles}

    # 3. Errors of the reconstructed road users
    se = fusion.get("state_errors", {})
    errors = {"centre_error_m": _stat(se.get("centre_error_m")), "speed_error_mps": _stat(se.get("speed_error_mps")),
              "velocity_error_mps": _stat(se.get("velocity_error_mps")),
              "heading_error_deg_diagnostic": _stat(se.get("heading_error_deg"))}

    # 4. Association
    counts = fusion.get("decision_counts", {})
    association = {"decisions": counts,
                   "wrong_links": sum(v for k, v in counts.items() if "wrong" in k or "false" in k),
                   "merges": fusion.get("merges", {}),
                   "fragmented_vehicles": {k: v for k, v in (fusion.get("fragmentation") or {}).items() if len(v) > 1},
                   "phantoms": len(phantoms)}

    # 5. Essential semantics
    semantics: Dict[str, Any] = {"available": oracle is not None}
    if oracle is not None:
        origins = _origins(run_dir, recorders)
        rec_events = oracle["events"].get("RECONSTRUCTION", {})
        cov_events = oracle["events"].get("COVERAGE", {})

        def starts(events: Mapping[str, List[Dict[str, Any]]], r: str, s: str, kinds: Tuple[str, ...]) -> List[float]:
            return sorted(float(e["t_local"]) for e in events.get(r, []) if e["type"] in kinds and e["subject"] == s)

        warnings = []
        contact_local: Dict[Tuple[str, str], List[float]] = defaultdict(list)
        for c in contacts:
            a, b = c["pair"].split("-")
            for r, s in ((a, b), (b, a)):
                if r not in recorders:
                    continue
                tc = float(c["sim_time"]) - origins[r]
                contact_local[(r, s)].append(tc)
                window = lambda ts: [t for t in ts if tc - WARNING_WINDOW_S <= t <= tc]  # noqa: E731
                rec = window(starts(rec_events, r, s, ("CRITICAL_TTC_START",)))
                ora = window(starts(cov_events, r, s, ("CRITICAL_TTC_START",)))
                warnings.append({"recorder": r, "partner": s, "contact_t_local": round(tc, 3),
                                 "warned": bool(rec), "in_time": bool([t for t in rec if t < tc]),
                                 "lead_time_s": round(tc - rec[0], 3) if rec else None,
                                 "justified": bool(ora), "oracle_lead_time_s": round(tc - ora[0], 3) if ora else None})
        intrusions = {"expected": 0, "found": 0, "missed": [], "extra": []}
        for r in recorders:
            subjects = {e["subject"] for e in cov_events.get(r, []) + rec_events.get(r, [])
                        if e["type"] in INTRUSION_TYPES}
            for s in subjects:
                o = starts(cov_events, r, s, INTRUSION_TYPES)
                x = starts(rec_events, r, s, INTRUSION_TYPES)
                used = set()
                for t in o:
                    intrusions["expected"] += 1
                    match = next((i for i, u in enumerate(x) if i not in used and abs(u - t) <= MATCH_WINDOW_S), None)
                    if match is None:
                        intrusions["missed"].append("{0}/{1}@{2:.2f}".format(r, s, t))
                    else:
                        used.add(match); intrusions["found"] += 1
                intrusions["extra"] += ["{0}/{1}@{2:.2f}".format(r, s, u) for i, u in enumerate(x) if i not in used
                                        and not any(abs(u - t) <= MATCH_WINDOW_S for t in o)]
        unconfirmed = []
        for r in recorders:
            for e in rec_events.get(r, []):
                if e["type"] != "CRITICAL_TTC_START" or e["subject"] is None:
                    continue
                t, s = float(e["t_local"]), e["subject"]
                if any(abs(t - u) <= MATCH_WINDOW_S for u in starts(cov_events, r, s, ("CRITICAL_TTC_START",))):
                    continue
                if any(0.0 <= tc - t <= WARNING_WINDOW_S for tc in contact_local.get((r, s), [])):
                    continue
                unconfirmed.append("{0}/{1}@{2:.2f}".format(r, s, t))
        in_time = [w for w in warnings if w["justified"]]
        semantics.update({
            "critical_ttc_warnings": warnings,
            "justified_warnings": len(in_time),
            "justified_warned_in_time": sum(w["in_time"] for w in in_time),
            "lead_time_s": [w["lead_time_s"] for w in in_time if w["in_time"]],
            "path_intrusions": intrusions,
            "unconfirmed_critical_ttc": unconfirmed})
    return {"run": "{0}/{1}".format(run_dir.parent.name, run_dir.name), "recorders": recorders,
            "collisions": collisions, "completeness": completeness, "errors": errors,
            "association": association, "semantics": semantics}


def _fmt(v: Any) -> str:
    if v is None:
        return "–"
    if isinstance(v, float):
        return "{0:.3f}".format(v)
    return str(v)


def summary_rows(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for c in cards:
        col, com, err, ass, sem = (c["collisions"], c["completeness"], c["errors"], c["association"], c["semantics"])
        rows.append({
            "run": c["run"], "contacts": col["true"], "detected": col["detected"], "identified": col["identified"],
            "invented": col["invented"], "max_dt_s": col["max_abs_timing_error_s"],
            "vehicles": com["true_vehicles"], "observable": com["observable"],
            "represented": com["represented_observable"], "missed": ",".join(com["missed_observable"]),
            "duplicates": com["duplicates"], "phantoms": len(com["phantoms"]),
            "pos_med_m": err["centre_error_m"]["median"], "pos_p95_m": err["centre_error_m"]["p95"],
            "spd_med_mps": err["speed_error_mps"]["median"], "spd_p95_mps": err["speed_error_mps"]["p95"],
            "wrong_links": ass["wrong_links"], "missed_merges": (ass["merges"] or {}).get("missed"),
            "false_merges": (ass["merges"] or {}).get("false"),
            "ttc_justified": sem.get("justified_warnings"), "ttc_in_time": sem.get("justified_warned_in_time"),
            "intrusions": "{0}/{1}".format((sem.get("path_intrusions") or {}).get("found"),
                                           (sem.get("path_intrusions") or {}).get("expected")),
            "unconfirmed_ttc": len(sem.get("unconfirmed_critical_ttc") or []),
        })
    return rows


def markdown(cards: List[Dict[str, Any]], title: str) -> str:
    rows = summary_rows(cards)
    keys = list(rows[0]) if rows else []
    out = ["# " + title, "", "| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    out += ["| " + " | ".join(_fmt(r[k]) for k in keys) + " |" for r in rows]
    tot = lambda k: sum(r[k] or 0 for r in rows)  # noqa: E731
    out += ["", "Totals: contacts {0}, detected {1}, identified {2}, invented {3}; observable vehicles {4}, "
            "represented {5}, duplicates {6}, phantoms {7}; wrong links {8}; justified CRITICAL_TTC warnings {9}, "
            "in time {10}; unconfirmed alarms {11}.".format(
                tot("contacts"), tot("detected"), tot("identified"), tot("invented"), tot("observable"),
                tot("represented"), tot("duplicates"), tot("phantoms"), tot("wrong_links"), tot("ttc_justified"),
                tot("ttc_in_time"), tot("unconfirmed_ttc"))]
    return "\n".join(out) + "\n"
