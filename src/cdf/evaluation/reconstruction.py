"""Privileged evaluation of a finished reconstruction.

Runs only after ``<run>/reconstruction/`` has been written.  It reads those
files plus ``<run>/ground_truth/`` and writes ``reconstruction/evaluation/``;
it never changes the reconstruction.  ``cdf.reconstruction`` never imports
this module.

Privileged assumption used only here: in these CARLA recordings every
recorder's raw clock is the simulator clock, so ``t_local + clock origin`` is
simulator time and can be compared with ``ground_truth/``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..reconstruction.alignment import align_graphs
from ..reconstruction.config import ReconstructionConfig, config_from_mapping
from ..reconstruction.fusion import associate_tracks, fuse_graphs
from ..reconstruction.local import reconstruct_vehicle
from ..reconstruction.pipeline import run_title
from ..reconstruction.render import write_json, write_text

# A track "is" a vehicle when its median distance to that vehicle's box is below this.
IDENTITY_MAX_BOX_DISTANCE_M = 1.5
# The clock-robustness check makes one recorder's local clock read this much later.
CLOCK_SHIFT_S = 0.73


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


class TruthTrack:
    """Ground-truth states of one participant, looked up by simulator time."""

    def __init__(self, states: Sequence[Dict[str, Any]]) -> None:
        self.states = sorted(states, key=lambda state: state["timestamp"])
        self.times = np.array([state["timestamp"] for state in self.states])

    def at(self, sim_time: float) -> Optional[Dict[str, Any]]:
        index = int(np.clip(np.searchsorted(self.times, sim_time), 0, len(self.times) - 1))
        if index > 0 and abs(self.times[index - 1] - sim_time) < abs(self.times[index] - sim_time):
            index -= 1
        return self.states[index] if abs(self.times[index] - sim_time) <= 0.03 else None


def _box_distance(point: Tuple[float, float], state: Dict[str, Any]) -> float:
    """2-D distance from a point to the vehicle's oriented bounding box (0 inside)."""
    along, across, extent = _in_box_frame(point, state)
    return math.hypot(max(abs(along) - extent["x"], 0.0), max(abs(across) - extent["y"], 0.0))


def _surface_distance(point: Tuple[float, float], state: Dict[str, Any]) -> float:
    """2-D distance from a point to the box outline: what a radar return lies on."""
    along, across, extent = _in_box_frame(point, state)
    outside = _box_distance(point, state)
    if outside > 0.0:
        return outside
    return min(extent["x"] - abs(along), extent["y"] - abs(across))


def _in_box_frame(point: Tuple[float, float], state: Dict[str, Any]) -> Tuple[float, float, Dict[str, float]]:
    transform = state["transform"]
    extent = state.get("bbox_extent") or {"x": 2.4, "y": 1.0}
    yaw = math.radians(transform["yaw_deg"])
    dx, dy = point[0] - transform["x"], point[1] - transform["y"]
    return math.cos(yaw) * dx + math.sin(yaw) * dy, -math.sin(yaw) * dx + math.cos(yaw) * dy, extent


def _speed(state: Dict[str, Any]) -> float:
    return math.hypot(state["velocity"]["x"], state["velocity"]["y"])


def _rmse(values: Sequence[float]) -> Optional[float]:
    return round(math.sqrt(sum(v * v for v in values) / len(values)), 3) if values else None


def _to_world(first_pose: Dict[str, Any], x: float, y: float) -> Tuple[float, float]:
    """Local frame of a recorder -> CARLA world (evaluation only)."""
    yaw = math.radians(first_pose["yaw_deg"])
    return (first_pose["x"] + math.cos(yaw) * x - math.sin(yaw) * y,
            first_pose["y"] + math.sin(yaw) * x + math.cos(yaw) * y)


def _truth_contacts(collisions: Sequence[Dict[str, Any]], actor_to_participant: Dict[int, str]) -> List[Dict[str, Any]]:
    """Ground-truth contacts between recorded participants, first callback per pair and episode."""
    contacts: List[Dict[str, Any]] = []
    for record in sorted(collisions, key=lambda item: item["timestamp"]):
        other = actor_to_participant.get(record.get("other_actor_id"))
        pair = sorted([record["participant_id"], other]) if other else [record["participant_id"], "static/unrecorded"]
        previous = next((contact for contact in contacts if contact["participants"] == pair
                         and record["timestamp"] - contact["last_time"] <= 0.5), None)
        if previous is None:
            contacts.append({"participants": pair, "sim_time": record["timestamp"], "last_time": record["timestamp"],
                             "peak_impulse": record["impulse"]})
        else:
            previous["last_time"] = record["timestamp"]
            previous["peak_impulse"] = max(previous["peak_impulse"], record["impulse"])
    for contact in contacts:
        contact.pop("last_time")
    return contacts


def _clock_shift_check(run_dir: Path, graph: Dict[str, Any], alignment: Dict[str, Any],
                       config: ReconstructionConfig) -> Dict[str, Any]:
    """Would the global graph change if one recorder's clock had started differently?

    The last recorder is rebuilt with its local clock reading ``CLOCK_SHIFT_S``
    later, then alignment and fusion are rerun in memory.  Uses no ground truth.
    """
    locals_ = []
    shifted = sorted(alignment["graphs"])[-1]
    for vehicle_dir in sorted(path for path in (run_dir / "vehicles").iterdir() if path.is_dir()):
        origin = None
        if vehicle_dir.name == shifted:
            origin = _read_jsonl(vehicle_dir / "ego.jsonl")[0]["timestamp"] - CLOCK_SHIFT_S
        locals_.append(reconstruct_vehicle(vehicle_dir, config, clock_origin=origin))
    shifted_alignment = align_graphs([local.graph for local in locals_], config.fusion)
    associations = associate_tracks(locals_, shifted_alignment, config.fusion)
    shifted_graph = fuse_graphs(locals_, shifted_alignment, associations)

    def signature(nodes: List[Tuple[Any, ...]]) -> List[Tuple[Any, ...]]:
        return [(kind, actor, subject, None if t is None else round(t, 3)) for kind, actor, subject, t in nodes]

    before_nodes = signature([(n["event_type"], n["actor_id"], n["subject_id"], n["t_global"]) for n in graph["nodes"]])
    after_nodes = signature([(n.event_type, n.actor_id, n.subject_id, n.t_global) for n in shifted_graph.nodes])
    shifted_local = next(local for local in locals_ if local.owner == shifted)
    before = alignment["graphs"][shifted]["offset_to_global"]
    after = shifted_alignment.graphs[shifted].offset_to_global
    return {"shifted_recorder": shifted, "shift_s": CLOCK_SHIFT_S,
            "shifted_local_collision_times": [node.t_local for node in shifted_local.graph.nodes
                                              if node.event_type == "COLLISION"],
            "global_graph_identical": before_nodes == after_nodes,
            "offset_to_global_before": before, "offset_to_global_after": after,
            "offset_change_s": None if before is None or after is None else round(after - before, 4)}


def evaluate_run(run_dir: Path, clock_shift_check: bool = True) -> Dict[str, Any]:
    run_dir = Path(run_dir)
    rec = run_dir / "reconstruction"
    alignment = _read_json(rec / "global" / "alignment.json")
    associations = _read_json(rec / "global" / "associations.json")
    graph = _read_json(rec / "global" / "global_graph.json")
    recorders = sorted(alignment["graphs"])
    local_graphs = {name: _read_json(rec / name / "local_graph.json") for name in recorders}
    origins = {name: local_graphs[name]["recorder"]["clock"]["origin_source_timestamp"] for name in recorders}
    first_poses = {name: _read_jsonl(run_dir / "vehicles" / name / "ego.jsonl")[0] for name in recorders}

    # Privileged inputs.
    states = _read_jsonl(run_dir / "ground_truth" / "states.jsonl")
    truth = {name: TruthTrack([s for s in states if s["participant_id"] == name])
             for name in sorted({s["participant_id"] for s in states})}
    actor_to_participant = {s["actor_id"]: s["participant_id"] for s in states}
    contacts = _truth_contacts(_read_jsonl(run_dir / "ground_truth" / "collisions.jsonl"), actor_to_participant)
    # The true contact behind the reconstruction's reference collision node.
    collision_nodes = [node for node in graph["nodes"] if node["event_type"] == "COLLISION"]
    reference_node = next((node for node in collision_nodes
                           if node["attributes"].get("reference_event")), None)
    reference_truth = None
    if reference_node is not None:
        observation = reference_node["observations"][0]
        reported_at = observation["t_local"] + origins[observation["graph"]]
        candidates = [c for c in contacts if c["participants"] == sorted(reference_node["participants"])]
        if candidates:
            reference_truth = min(candidates, key=lambda c: abs(c["sim_time"] - reported_at))

    # 1. Collisions.
    collision_rows = []
    for contact in contacts:
        match = next((node for node in collision_nodes
                      if sorted(node["participants"]) == contact["participants"]), None)
        timing = None
        if match is not None:
            timing = max(abs(obs["t_local"] + origins[obs["graph"]] - contact["sim_time"]) for obs in match["observations"])
        collision_rows.append({"participants": contact["participants"], "sim_time": contact["sim_time"],
                               "peak_impulse": contact["peak_impulse"],
                               "reconstructed_as": None if match is None else match["node_id"],
                               "participants_correct": match is not None,
                               "report_timing_error_s": None if timing is None else round(timing, 4)})

    # 2. Alignment accuracy (true local time of the reference contact per recorder).
    alignment_rows = []
    for name in recorders:
        clock = alignment["graphs"][name]
        true_anchor = None if reference_truth is None else round(reference_truth["sim_time"] - origins[name], 4)
        error = (None if clock["anchor_t_local"] is None or true_anchor is None
                 else round(clock["anchor_t_local"] - true_anchor, 4))
        alignment_rows.append({"graph": name, "status": clock["status"],
                               "estimated_anchor_t_local": clock["anchor_t_local"],
                               "true_contact_t_local": true_anchor, "error_s": error})
    relative = []
    for name, estimated in alignment["relative_clock_offsets_s"].items():
        second, first = [part.strip() for part in name.split(" - ")]
        true_offset = round(origins[first] - origins[second], 4)
        relative.append({"pair": name, "estimated_s": estimated, "true_s": true_offset,
                         "error_s": round(estimated - true_offset, 4)})

    # 3. Global event times and order.
    timed = [node for node in graph["nodes"] if node["t_global"] is not None]
    time_errors = []
    true_times = []
    for node in timed:
        observation = node["observations"][0]
        true_global = (observation["t_local"] + origins[observation["graph"]]
                       - (reference_truth["sim_time"] if reference_truth else 0.0))
        true_times.append(true_global)
        time_errors.append(node["t_global"] - true_global)
    concordant = total = 0
    for i in range(len(timed)):
        for j in range(i + 1, len(timed)):
            if abs(timed[i]["t_global"] - timed[j]["t_global"]) < 1e-9 or abs(true_times[i] - true_times[j]) < 1e-9:
                continue
            total += 1
            concordant += (timed[i]["t_global"] < timed[j]["t_global"]) == (true_times[i] < true_times[j])

    # 4-5. Track identities and trajectory accuracy.
    track_rows = []
    for item in associations:
        owner, track_id = item["local_graph"], item["local_track"]
        samples = [row for row in _read_jsonl(rec / owner / "local_tracks.jsonl") if row["track_id"] == track_id]
        distances: Dict[str, List[float]] = {}
        for sample in samples:
            point = _to_world(first_poses[owner], sample["x_m"], sample["y_m"])
            for name, track in truth.items():
                if name == owner:
                    continue
                state = track.at(sample["t_local"] + origins[owner])
                if state is not None:
                    distances.setdefault(name, []).append(_box_distance(point, state))
        medians = {name: float(np.median(values)) for name, values in distances.items() if values}
        best = min(medians, key=medians.get) if medians else None
        identity = best if best is not None and medians[best] <= IDENTITY_MAX_BOX_DISTANCE_M else None
        if item["status"] == "ASSOCIATED":
            verdict = "correct" if item["global_entity"] == identity else "WRONG"
        else:
            verdict = ("correctly left anonymous" if identity not in recorders
                       else "left anonymous (true identity {0})".format(identity))
        row = {"track": owner + ":" + track_id, "decision": item["global_entity"], "status": item["status"],
               "true_identity": identity, "median_box_distance_m": {k: round(v, 2) for k, v in medians.items()},
               "verdict": verdict}
        if identity is not None:
            raw, smooth, centre, speed, raw_speed = [], [], [], [], []
            previous = None
            for sample in samples:
                state = truth[identity].at(sample["t_local"] + origins[owner])
                if state is None or not sample["measured"]:
                    previous = None
                    continue  # compare raw and smoothed on the same sweeps
                point = _to_world(first_poses[owner], sample["x_m"], sample["y_m"])
                measured = _to_world(first_poses[owner], sample["meas_x_m"], sample["meas_y_m"])
                smooth.append(_surface_distance(point, state))
                raw.append(_surface_distance(measured, state))
                centre.append(math.hypot(point[0] - state["transform"]["x"], point[1] - state["transform"]["y"]))
                speed.append(sample["speed_mps"] - _speed(state))
                # Speed from consecutive raw returns: what one gets without the filter.
                if previous is not None and sample["t_local"] - previous[0] < 0.11:
                    dt = sample["t_local"] - previous[0]
                    raw_speed.append(math.hypot(measured[0] - previous[1][0], measured[1] - previous[1][1]) / dt
                                     - _speed(state))
                previous = (sample["t_local"], measured)
            row.update({"samples": len(smooth), "raw_rmse_to_surface_m": _rmse(raw),
                        "smoothed_rmse_to_surface_m": _rmse(smooth), "smoothed_rmse_to_centre_m": _rmse(centre),
                        "raw_difference_speed_rmse_mps": _rmse(raw_speed), "speed_rmse_mps": _rmse(speed)})
        track_rows.append(row)

    robustness = None
    if clock_shift_check and alignment["reference_event"] is not None:
        config = config_from_mapping(graph.get("reconstruction_config"))
        robustness = _clock_shift_check(run_dir, graph, alignment, config)

    reconstructed = all(row["participants_correct"] for row in collision_rows if "static/unrecorded" not in row["participants"])
    decided = [row for row in track_rows if row["status"] == "ASSOCIATED"]
    headline = "collision reconstructed: {0}; associations correct: {1}/{2}; anonymous: {3}; max |t_global error| {4} s".format(
        "yes" if reconstructed and collision_rows else "NO",
        sum(row["verdict"] == "correct" for row in decided), len(decided),
        sum(row["status"] != "ASSOCIATED" for row in track_rows),
        None if not time_errors else round(max(abs(e) for e in time_errors), 4))
    result = {"run": run_title(run_dir), "headline": headline,
              "privileged_assumption": "recorder raw clocks are CARLA simulator time",
              "collisions": collision_rows, "alignment": alignment_rows, "relative_clock_offsets": relative,
              "event_timing": {"nodes": len(timed),
                               "max_abs_error_s": None if not time_errors else round(max(abs(e) for e in time_errors), 4),
                               "order_pairs": total, "order_concordant": concordant},
              "tracks": track_rows, "clock_shift_check": robustness}
    write_json(rec / "evaluation" / "evaluation.json", result)
    write_text(rec / "evaluation" / "evaluation.md", evaluation_markdown(result))
    return result


def evaluation_markdown(result: Dict[str, Any]) -> str:
    def cell(value: Any) -> str:
        return "-" if value is None else str(value)

    lines = ["# Privileged evaluation - " + result["run"], "",
             "This compares the finished reconstruction with `ground_truth/` (simulator state). The "
             "reconstruction never read it and was not changed by this evaluation.", "",
             "**" + result["headline"] + "**", "",
             "Privileged assumption: " + result["privileged_assumption"] + ".", "",
             "## Collisions", "",
             "| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |",
             "|--------------|---------:|-------------:|------------------|----------------------|--------------------:|"]
    for row in result["collisions"]:
        lines.append("| {0} | {1:.3f} | {2:.1f} | {3} | {4} | {5} s |".format(
            " + ".join(row["participants"]), row["sim_time"], row["peak_impulse"], cell(row["reconstructed_as"]),
            "yes" if row["participants_correct"] else "NO", cell(row["report_timing_error_s"])))
    lines += ["", "## Graph alignment accuracy", "",
              "| Graph | Status | Estimated anchor (local) | True contact (local) | Error |",
              "|-------|--------|-------------------------:|---------------------:|------:|"]
    for row in result["alignment"]:
        lines.append("| {0} | {1} | {2} | {3} | {4} s |".format(
            row["graph"], row["status"], cell(row["estimated_anchor_t_local"]),
            cell(row["true_contact_t_local"]), cell(row["error_s"])))
    for row in result["relative_clock_offsets"]:
        lines.append("")
        lines.append("Relative clock offset {0}: estimated {1:+.3f} s, true {2:+.3f} s (error {3:+.3f} s).".format(
            row["pair"], row["estimated_s"], row["true_s"], row["error_s"]))
    timing = result["event_timing"]
    lines += ["", "## Global event times", "",
              "{0} timed global nodes; max |t_global - true global time| = {1} s; event order agrees "
              "with the truth for {2}/{3} pairs.".format(timing["nodes"], cell(timing["max_abs_error_s"]),
                                                          timing["order_concordant"], timing["order_pairs"])]
    lines += ["", "## Anonymous tracks: identity and trajectory", "",
              "| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |",
              "|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|"]
    for row in result["tracks"]:
        lines.append("| {0} | {1} | {2} | {3} | {4} | {5} / {6} m | {7} m | {8} / {9} m/s |".format(
            row["track"], row["decision"], cell(row["true_identity"]), row["verdict"], cell(row.get("samples")),
            cell(row.get("raw_rmse_to_surface_m")), cell(row.get("smoothed_rmse_to_surface_m")),
            cell(row.get("smoothed_rmse_to_centre_m")), cell(row.get("raw_difference_speed_rmse_mps")),
            cell(row.get("speed_rmse_mps"))))
    lines += ["", "Surface distance = distance from a track point to the outline of the true vehicle's "
              "bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; "
              "smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on "
              "the surface by construction, so smoothing cannot be expected to bring the position closer to "
              "it; its gain shows in the speed (raw differences of consecutive returns vs smoothed "
              "velocity). The distance to the centre includes the surface-to-centre offset. True identity = "
              "the vehicle whose box is closest (median <= {0} m).".format(IDENTITY_MAX_BOX_DISTANCE_M)]
    check = result["clock_shift_check"]
    if check:
        lines += ["", "## Clock-shift check (uses no ground truth)", "",
                  "Recorder {0} was rebuilt with its local clock reading {1:+.2f} s later (its collision is then "
                  "at local time {2}), and alignment and fusion were rerun. Global graph identical: **{3}**. "
                  "{0}'s offset_to_global changed by {4} s (expected {5:+.2f} s).".format(
                      check["shifted_recorder"], check["shift_s"],
                      ", ".join("{0:.2f} s".format(t) for t in check["shifted_local_collision_times"]) or "-",
                      "yes" if check["global_graph_identical"] else "NO",
                      cell(check["offset_change_s"]), -check["shift_s"])]
    return "\n".join(lines) + "\n"
