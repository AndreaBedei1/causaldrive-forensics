"""traces/campaign_summary.json from the persisted reconstructions of every run (evaluation side: it also
reads each run's evaluation.json for the true identity of the tracks with a CRITICAL_TTC).

    python scripts/campaign_summary.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cdf.reconstruction.checks import describe_temporal_relation, open_states, sign_windows  # noqa: E402
from cdf.reconstruction.models import LocalGraph  # noqa: E402

TRACES = ROOT / "traces"
PAIRS = ["BRAKE", "THROTTLE", "TURN_LEFT", "TURN_RIGHT", "MOVING", "STOP", "SPEED_LIMIT_EXCEEDED", "CLOSING", "CRITICAL_TTC",
         "CUT_IN_FROM_LEFT", "CUT_IN_FROM_RIGHT", "STOP_SIGN_DETECTED", "YIELD_SIGN_DETECTED"]
APPEARED = ("TRACK_APPEARED_FRONT", "TRACK_APPEARED_LEFT", "TRACK_APPEARED_RIGHT")
WATCH = ["CLOSING", "CRITICAL_TTC", "CUT_IN_FROM_LEFT", "CUT_IN_FROM_RIGHT", "IN_EGO_PATH"]


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def lost_while_active(graph):
    out = []
    for node in graph.nodes:
        if node.event_type != "TRACK_LOST":
            continue
        state = ((node.perceived_state_before or {}).get("external") or {}).get(node.subject_id) or {}
        out.append({"track": node.subject_id, "t_local": node.t_local,
                    "active": [name for name in WATCH if state.get(name) is True]})
    return out


def radar_summary(vehicle_dir):
    """The three body radars of one vehicle: geometry and acquisition health, per radar."""
    import numpy as np
    out = {}
    for path in sorted((vehicle_dir / "radar").iterdir()):
        meta = json.loads((path / "metadata.json").read_text(encoding="utf-8"))
        with np.load(path / "observations.npz") as data:
            sweeps, returns = len(data["frames"]), len(data["detections"])
        out[path.name] = {"horizontal_fov_deg": meta.get("horizontal_fov_deg"),
                          "vertical_fov_deg": meta.get("vertical_fov_deg"), "range_m": meta.get("range_m"),
                          "points_per_second": meta.get("points_per_second"), "mount": meta.get("sensor_transform"),
                          "sweeps": sweeps, "returns_per_sweep": round(returns / max(sweeps, 1), 1),
                          "missing_frame_count": meta.get("missing_frame_count"),
                          "queue_drops": meta.get("queue_drops"),
                          "frames_without_measurement": meta.get("frames_without_measurement")}
    return out


def criticals(graph, identities):
    return [{"track": node.subject_id, "t_local": node.t_local,
             "true_identity": identities.get(graph.owner + ":" + node.subject_id)}
            for node in graph.nodes if node.event_type == "CRITICAL_TTC_START"]


def summarize(run):
    rec = run / "reconstruction"
    context = json.loads((run / "incident_context.json").read_text()) if (run / "incident_context.json").exists() else {}
    recorders = sorted(p.name for p in rec.iterdir() if (p / "local_graph.json").exists())
    graphs = {name: LocalGraph.from_dict(json.loads((rec / name / "local_graph.json").read_text(encoding="utf-8")))
              for name in recorders}
    alignment = json.loads((rec / "global" / "alignment.json").read_text(encoding="utf-8"))
    associations = json.loads((rec / "global" / "associations.json").read_text(encoding="utf-8"))
    global_graph = json.loads((rec / "global" / "global_graph.json").read_text(encoding="utf-8"))
    trace = jsonl(rec / "global" / "global_trace.jsonl")
    evaluation = json.loads((rec / "evaluation" / "evaluation.json").read_text(encoding="utf-8"))
    counts = Counter(node["event_type"] for node in global_graph["nodes"])
    local_counts = {n: Counter(node.event_type for node in g.nodes) for n, g in graphs.items()}
    return {"run": run.parent.name + "/" + run.name, "speed_limit_kmh": context.get("speed_limit_kmh"),
            "local": {n: (len(g.nodes), len(g.edges)) for n, g in graphs.items()},
            "global": (len(global_graph["nodes"]), len(global_graph["edges"])),
            "alignment": {n: v["status"] for n, v in alignment["graphs"].items()},
            "alignment_chain": {n: v.get("chain", []) for n, v in alignment["graphs"].items()},
            "reference": alignment["reference_event"],
            "rejected_matches": len(alignment.get("rejected_matches", [])),
            "associations": ["{0}:{1}->{2} {3}{4}".format(a["local_graph"], a["local_track"], a["global_entity"],
                                                          a["status"], "" if a["confidence"] is None else " %.2f" % a["confidence"])
                             for a in associations],
            "pairs": {p: (counts.get(p + "_START", 0), counts.get(p + "_END", 0)) for p in PAIRS},
            "track": (sum(counts.get(t, 0) for t in APPEARED), counts.get("TRACK_LOST", 0)),
            "track_appeared": {t.split("_")[-1]: counts.get(t, 0) for t in APPEARED},
            "path": (counts.get("EGO_PATH_ENTRY", 0), counts.get("EGO_PATH_EXIT", 0)),
            "collisions": counts.get("COLLISION", 0),
            "collision_nodes": [{"participants": n["participants"], "t_global": n["t_global"],
                                 "matched_event": n["attributes"].get("matched_event"),
                                 "reference": n["attributes"].get("reference_event", False)}
                                for n in global_graph["nodes"] if n["event_type"] == "COLLISION"],
            "local_collisions": {n: [dict({"t_local": node.t_local}, **node.attributes) for node in g.nodes
                                     if node.event_type == "COLLISION"] for n, g in graphs.items()},
            "open": {n: ["{0}{1}".format(s["state"], "(" + s["subject"] + ")" if s["subject"] else "") for s in open_states(g)]
                     for n, g in graphs.items()},
            "signs": {n: sign_windows(g, "STOP_SIGN_DETECTED") + sign_windows(g, "YIELD_SIGN_DETECTED") for n, g in graphs.items()},
            "radar_tracks": {n: sum(local_counts[n].get(t, 0) for t in APPEARED) for n in graphs},
            "cut_in": {n: (local_counts[n].get("CUT_IN_FROM_LEFT_START", 0), local_counts[n].get("CUT_IN_FROM_RIGHT_START", 0))
                       for n in graphs},
            "temporal_safety_relations": ["{0}:{1} ({2}): {3}".format(r["recorder"], r["track"], r["entity"],
                                                                     describe_temporal_relation(r))
                                          for r in global_graph.get("temporal_safety_relations", [])],
            "lost_while_active": {n: lost_while_active(g) for n, g in graphs.items()},
            "simultaneous": [row["text"] for row in trace if len(row["events"]) > 1],
            "sequence": ["%+.2f %s" % (row["t_global"], row["text"]) for row in trace],
            "unaligned_nodes": sum(1 for node in global_graph["nodes"] if node["t_global"] is None),
            "local_sequences": {n: ["%.2f %s%s%s" % (node.t_local, node.event_type,
                                                     "(" + node.subject_id + ")" if node.subject_id else "",
                                                     "*" if node.attributes.get("active_at_first_observation") else "")
                                    for node in g.nodes] for n, g in graphs.items()},
            "radar": {n: radar_summary(run / "vehicles" / n) for n in graphs},
            "critical_ttc": {n: criticals(g, {t["track"]: t["true_identity"] for t in evaluation.get("tracks", [])})
                             for n, g in graphs.items()},
            "own_body_returns_dropped": {n: ((g.recorder.get("radar") or {}).get("own_body_returns_dropped"))
                                         for n, g in graphs.items()},
            "contact_clearances": evaluation.get("contact_clearances", []),
            "headline": evaluation["headline"],
            "extra_collisions": evaluation.get("extra_collisions", []),
            "clock_shift_identical": (evaluation.get("clock_shift_check") or {}).get("global_graph_identical")}


if __name__ == "__main__":
    runs = sorted(p for p in TRACES.glob("S*/run_*") if (p / "reconstruction" / "evaluation" / "evaluation.json").exists())
    summaries = [summarize(run) for run in runs]
    (TRACES / "campaign_summary.json").write_text(json.dumps(summaries, indent=1, ensure_ascii=False) + "\n",
                                                  encoding="utf-8")
    print("runs:", len(summaries))
