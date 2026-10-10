"""Admissible forensic facts for an LLM: the exporter.

``export_forensic_facts(run_dir)`` writes

    <run>/reconstruction/llm/forensic_facts.jsonl   one fact per line (canonical)
    <run>/reconstruction/llm/forensic_packet.json   the same facts reorganised for a model
    <run>/reconstruction/llm/export_manifest.json   input digests (never sent to a model)

It reads only measured, admissible information:

* ``reconstruction/<R>/local_trace.jsonl``: the ``facts`` of each frame
  (EGO_MOTION, EGO_CONTROL, TRACK_STATE), never ``events`` nor
  ``perceived_state``; TRACK_STATE through an allowlist that drops every output
  of the conflict model and every semantic classification;
* ``reconstruction/<R>/local_graph.json``: the recorder's clock origin,
  observation window, footprint and radar mounts, and its collision-sensor
  reports (time and peak impulse);
* ``reconstruction/global/alignment.json``: each recorder's clock offset and
  how the collision reports were matched;
* ``reconstruction/global/associations.json``: whether a local track was
  identified with a recorder (ASSOCIATED) or not (ANONYMOUS);
* ``vehicles/<R>/metadata.json``: radar coverage (field of view, range);
* ``vehicles/<R>/traffic_signs.jsonl``: the on-board sign detections;
* ``incident_context.json``: the supplied speed limit and road environment.

Never read: ``ground_truth/``, the run's ``metadata.json``, the scenario
configuration, the reconstruction's events, graphs' nodes other than collision
reports, ``report.md`` and ``evaluation/``.  The run is named by a hash of its
facts, never by its directory.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

FACTS_SCHEMA_VERSION = "cdf.forensic_facts/1"
PACKET_SCHEMA_VERSION = "cdf.forensic_packet/1"

EGO_MOTION_FIELDS = ("speed_mps", "acceleration_mps2", "yaw_rate_dps", "x_m", "y_m", "heading_deg")
EGO_CONTROL_FIELDS = ("throttle", "brake", "steer")
# Local-trace attribute -> exported name.  Everything else is dropped.
TRACK_STATE_FIELDS = (
    ("radar", "radar"),
    ("range_m", "range_m"),
    ("clearance_m", "clearance_m"),
    ("bearing_deg", "bearing_deg"),
    ("longitudinal_m", "longitudinal_m"),
    ("lateral_m", "lateral_m"),
    ("x_m", "x_m"),
    ("y_m", "y_m"),
    ("vx_mps", "vx_mps"),
    ("vy_mps", "vy_mps"),
    ("speed_mps", "target_speed_mps"),
    ("acceleration_mps2", "target_acceleration_mps2"),
    ("relative_longitudinal_speed_mps", "relative_longitudinal_speed_mps"),
    ("relative_lateral_speed_mps", "relative_lateral_speed_mps"),
    ("pos_std_m", "pos_std_m"),
    ("vel_std_mps", "vel_std_mps"),
    ("measured", "measured"),
    ("t_cpa_s", "t_cpa_s"),
    ("d_cpa_m", "d_cpa_m"),
    ("d_cpa_clearance_m", "d_cpa_clearance_m"),
    ("closing_speed_mps", "closing_speed_mps"),
    ("closing_ttc_s", "closing_ttc_s"),
)
# What the local trace's TRACK_STATE also carries and the export removes, with why.
TRACK_STATE_REMOVED = {
    "encounter": "conflict-model classification",
    "motion_relation": "semantic classification of the relative motion",
    "collision_course": "conflict-model prediction",
    "ttc_s": "conflict-model time to contact (not the geometric closing_ttc_s)",
    "predicted_overlap_s": "conflict-model prediction",
    "required_deceleration_mps2": "conflict-model output",
    "avoidance_by": "conflict-model output",
    "braking_margin_mps2": "conflict-model output",
    "unavoidable_by_braking": "conflict-model output",
    "critical": "the boolean behind CRITICAL_TTC",
    "critical_reason": "conflict-model output (PREDICTED_OVERLAP / UNSAFE_FORWARD_GAP)",
    "line_of_sight_occluded": "semantic gate of the conflict model (seen past another track)",
    "forward_region": "conflict-model classification (safe following distance)",
    "forward_leader": "conflict-model classification (safe following distance)",
    "longitudinal_clearance_m": "conflict-model geometry (nominal target box)",
    "lateral_body_gap_m": "conflict-model geometry (nominal target box)",
    "time_headway_s": "conflict-model output (safe following distance)",
    "minimum_time_gap_s": "conflict-model threshold (UN R157 table)",
    "time_gap_distance_m": "conflict-model threshold (recorder speed x UN R157 time gap)",
    "required_safe_distance_m": "conflict-model threshold (safe following distance)",
    "safe_distance_margin_m": "conflict-model output (safe following distance)",
    "target_acceleration_used_mps2": "conflict-model input choice",
    "estimate_known": "semantic gate of the conflict model",
    "ahead_of_front_m": "input of the EGO_PATH / CUT_IN classification",
    "surface_offset_m": "internal tracking detail",
    "relative_motion_angle_deg": "input of the CUT_IN / motion-relation classification",
    "ego_speed_mps": "conflict-model copy of the recorder's own speed (EGO_MOTION has it)",
}
SIGN_FIELDS = ("class", "confidence", "t_first_local_s", "t_confirmed_local_s", "t_last_local_s",
               "relevant_to_own_path", "min_bearing_deg", "n_detections")
SUPPLIED_CONTEXT_FIELDS = ("speed_limit_kmh", "road_environment")
FACT_TYPE_ORDER = ("COLLISION_OBSERVATION", "SIGN_DETECTION", "EGO_MOTION", "EGO_CONTROL", "TRACK_STATE")

# Static definitions shipped in every packet (versioned with PACKET_SCHEMA_VERSION).
FIELD_DEFINITIONS = {
    "time": {
        "t_local_s": "seconds on the recorder's own clock (0 = that recorder's first sample)",
        "t_global_s": "seconds on the common clock of the aligned recorders: t_global_s = t_local_s + "
                      "offset_to_global_s; 0 is the time-origin collision (the strongest collision reported by "
                      "two recorders and matched between them); null when the recorder could not be aligned",
    },
    "frames": {
        "recorder_frame": "each recorder has its own fixed frame: origin = its first position, x = its first "
                          "heading, y = 90 degrees to the right of x; frames of different recorders are not "
                          "related to each other",
        "vehicle_frame": "longitudinal = along the recorder's current heading (+ ahead), lateral = across it "
                         "(+ to the right)",
        "angles": "degrees; positive = clockwise seen from above (to the right)",
    },
    "EGO_MOTION": {
        "speed_mps": "the recorder's ground speed",
        "acceleration_mps2": "rate of change of that speed (+ speeding up)",
        "yaw_rate_dps": "rate of change of heading (+ turning right)",
        "x_m/y_m": "position in the recorder's frame",
        "heading_deg": "heading in the recorder's frame (0 = its first heading)",
    },
    "EGO_CONTROL": {
        "throttle": "accelerator pedal, 0..1",
        "brake": "brake pedal, 0..1",
        "steer": "steering, -1 (full left) .. +1 (full right)",
    },
    "TRACK_STATE": {
        "observed_subject": "who the track is: a recorder id when identity_status is ASSOCIATED, otherwise the "
                            "track's own id (an unidentified road user)",
        "local_track_id": "the radar track of the recorder, as <recorder>:track_NNN",
        "identity_status": "ASSOCIATED = identified with a recorder; ANONYMOUS = not identified",
        "radar": "which of the recorder's radars measured the track at that instant",
        "range_m": "horizontal distance from that radar to the tracked point",
        "clearance_m": "free distance from the recorder's body to the near surface of the tracked road user",
        "bearing_deg": "direction of the tracked point from the recorder's heading (+ right, - left)",
        "longitudinal_m/lateral_m": "position of the tracked point in the vehicle frame",
        "x_m/y_m": "position of the tracked point in the recorder's frame",
        "vx_mps/vy_mps": "velocity of the tracked road user in the recorder's frame",
        "target_speed_mps": "speed of the tracked road user",
        "target_acceleration_mps2": "estimated acceleration of the tracked road user (+ speeding up)",
        "relative_longitudinal_speed_mps/relative_lateral_speed_mps": "velocity of the tracked road user minus "
                                                                      "the recorder's, in the vehicle frame",
        "pos_std_m/vel_std_mps": "one-sigma uncertainty of the position / velocity estimate",
        "measured": "true when a radar measurement updated the track at that instant, false when predicted",
        "t_cpa_s": "time until the closest approach if both keep their current velocities (negative = past)",
        "d_cpa_m": "distance between the tracked point and the recorder's origin at that closest approach",
        "d_cpa_clearance_m": "smallest free distance between the two bodies along that straight relative path",
        "closing_speed_mps": "rate at which clearance_m shrinks (+ getting closer)",
        "closing_ttc_s": "clearance_m / closing_speed_mps, a purely geometric line-of-sight time; null when "
                         "not getting closer",
    },
    "SIGN_DETECTION": {
        "sign_id": "a sign tracked by the recorder's camera, as <recorder>:sign-N",
        "class": "STOP or YIELD",
        "confidence": "best detection confidence, 0..1",
        "t_first/t_confirmed/t_last": "first detection, confirmed detection, last detection",
        "relevant_to_own_path": "the detector judged the sign to apply to the recorder's own path (geometry)",
        "min_bearing_deg": "smallest bearing at which it was seen",
        "n_detections": "number of camera frames with the detection",
    },
    "COLLISION_OBSERVATION": {
        "reports": "each recorder's collision-sensor report: local and global time, peak impulse (N*s)",
        "participants": "the recorders whose reports were matched as the same contact; a single recorder when "
                        "the other party is unidentified (no matching report from another recorder)",
        "matching": "how the reports were matched: impulse similarity and confidence",
        "time_origin": "true for the collision that defines t_global_s = 0",
    },
}


class ExportError(ValueError):
    """The run's reconstruction is missing something the export needs."""


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def canonical_json(value: Any) -> str:
    """Byte-stable JSON (sorted keys, no whitespace): what hashes are computed on."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def packet_sha256(packet: Dict[str, Any]) -> str:
    return sha256_text(canonical_json(packet))


def _round_time(value: Optional[float]) -> Optional[float]:
    return None if value is None else round(float(value), 4)


class _Clock:
    def __init__(self, recorder: str, status: str, offset: Optional[float]) -> None:
        self.recorder, self.status, self.offset = recorder, status, offset

    def to_global(self, t_local: Optional[float]) -> Optional[float]:
        if t_local is None or self.offset is None or self.status != "ALIGNED":
            return None
        return _round_time(float(t_local) + float(self.offset))


def _recorders(rec_dir: Path) -> List[str]:
    alignment = _read_json(rec_dir / "global" / "alignment.json")
    names = sorted(alignment["graphs"])
    for name in names:
        if not (rec_dir / name / "local_trace.jsonl").exists():
            raise ExportError("no local trace for recorder {0}".format(name))
    return names


def _identity_table(associations: Sequence[Dict[str, Any]]) -> Dict[Tuple[str, str], Tuple[str, str]]:
    """(recorder, local track) -> (observed_subject, identity_status).  Only ASSOCIATED reveals an identity."""
    table = {}
    for item in associations:
        key = (str(item["local_graph"]), str(item["local_track"]))
        local_id = "{0}:{1}".format(*key)
        if item.get("status") == "ASSOCIATED":
            table[key] = (str(item["global_entity"]), "ASSOCIATED")
        else:
            table[key] = (local_id, "ANONYMOUS")
    return table


def _radar_coverage(vehicle_dir: Path) -> List[Dict[str, Any]]:
    meta = _read_json(vehicle_dir / "metadata.json") if (vehicle_dir / "metadata.json").exists() else {}
    out = []
    for radar in meta.get("radar", []) or []:
        mount = radar.get("sensor_transform") or {}
        out.append({"sensor_id": str(radar["sensor_id"]),
                    "mount_x_m": _round_time(mount.get("x")), "mount_y_m": _round_time(mount.get("y")),
                    "mount_yaw_deg": mount.get("yaw_deg"),
                    "horizontal_fov_deg": radar.get("horizontal_fov_deg"), "range_m": radar.get("range_m")})
    return sorted(out, key=lambda item: item["sensor_id"])


def _footprint(local_graph: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    footprint = ((local_graph.get("recorder") or {}).get("radar") or {}).get("ego_footprint")
    if not footprint:
        return None
    return {"length_m": footprint["length_m"], "width_m": footprint["width_m"]}


def _supplied_context(run_dir: Path) -> Dict[str, Any]:
    path = run_dir / "incident_context.json"
    context = _read_json(path) if path.exists() else {}
    out: Dict[str, Any] = {"provenance": "supplied with the case; not perceived by any recorder"}
    for key in SUPPLIED_CONTEXT_FIELDS:
        out[key] = context.get(key)
    return out


def _collision_facts(rec_dir: Path, recorders: Sequence[str], clocks: Dict[str, _Clock],
                     alignment: Dict[str, Any]) -> List[Dict[str, Any]]:
    reports: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for name in recorders:
        graph = _read_json(rec_dir / name / "local_graph.json")
        for node in graph["nodes"]:
            if node["event_type"] == "COLLISION":
                reports[(name, node["node_id"])] = {"t_local": node["t_local"],
                                                    "peak": node["attributes"]["peak_impulse"]}
    facts = []
    used = set()
    for event in alignment.get("matched_events", []) or []:
        rows = []
        for name in sorted(event["graphs"]):
            used.add((name, event["nodes"][name]))
            t_local = float(event["t_local"][name])
            rows.append({"recorder": name, "t_local_s": _round_time(t_local), "t_global_s": clocks[name].to_global(t_local),
                         "peak_impulse_Ns": round(float(event["peak_impulse"][name]), 2)})
        times = [row["t_global_s"] for row in rows if row["t_global_s"] is not None]
        matching = {"status": "MATCHED", "impulse_similarity": event.get("impulse_similarity"),
                    "confidence": event.get("confidence")}
        if event.get("merged_burst_of"):
            matching["matched_to_a_burst_within_a_longer_contact_of"] = event["merged_burst_of"]
        facts.append({"type": "COLLISION_OBSERVATION", "participants": sorted(event["graphs"]),
                      "t_global_s": _round_time(sum(times) / len(times)) if times else None,
                      "time_origin": event.get("event_id") is not None
                      and event.get("event_id") == alignment.get("reference_event"),
                      "reports": rows, "matching": matching})
    for (name, node_id), report in sorted(reports.items(), key=lambda kv: (kv[1]["t_local"], kv[0])):
        if (name, node_id) in used:
            continue
        row = {"recorder": name, "t_local_s": _round_time(report["t_local"]),
               "t_global_s": clocks[name].to_global(report["t_local"]),
               "peak_impulse_Ns": round(float(report["peak"]), 2)}
        facts.append({"type": "COLLISION_OBSERVATION", "participants": [name], "t_global_s": row["t_global_s"],
                      "time_origin": False, "reports": [row],
                      "matching": {"status": "UNMATCHED", "other_party": "UNIDENTIFIED"}})
    return facts


def _sign_facts(run_dir: Path, name: str, origin: float, clock: _Clock) -> List[Dict[str, Any]]:
    facts = []
    for record in _read_jsonl(run_dir / "vehicles" / name / "traffic_signs.jsonl"):
        first = float(record["timestamp_first"]) - origin
        confirmed = record.get("timestamp_confirmed")
        confirmed = None if confirmed is None else float(confirmed) - origin
        last = float(record["timestamp_last"]) - origin
        values = {"class": str(record["class"]), "confidence": round(float(record["best_confidence"]), 3),
                  "t_first_local_s": _round_time(first), "t_confirmed_local_s": _round_time(confirmed),
                  "t_last_local_s": _round_time(last), "t_first_global_s": clock.to_global(first),
                  "t_confirmed_global_s": clock.to_global(confirmed), "t_last_global_s": clock.to_global(last),
                  "relevant_to_own_path": record.get("relevant_to_ego_path"),
                  "min_bearing_deg": record.get("min_bearing_deg"), "n_detections": record.get("n_detections")}
        t_local = confirmed if confirmed is not None else first
        facts.append({"type": "SIGN_DETECTION", "recorder": name, "t_local_s": _round_time(t_local),
                      "t_global_s": clock.to_global(t_local),
                      "sign_id": "{0}:{1}".format(name, record["sign_track_id"]), "values": values})
    return facts


def _frame_facts(trace_path: Path, name: str, clock: _Clock,
                 identities: Dict[Tuple[str, str], Tuple[str, str]], dropped: Dict[str, int]) -> List[Dict[str, Any]]:
    facts = []
    with trace_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            frame = json.loads(line)  # only frame["facts"] is used
            t_local = float(frame["t_local"])
            for item in frame["facts"]:
                kind, attributes = item["type"], item["attributes"]
                base = {"type": kind, "recorder": name, "t_local_s": _round_time(t_local),
                        "t_global_s": clock.to_global(t_local)}
                if kind == "EGO_MOTION":
                    base["values"] = {key: attributes.get(key) for key in EGO_MOTION_FIELDS}
                elif kind == "EGO_CONTROL":
                    base["values"] = {key: attributes.get(key) for key in EGO_CONTROL_FIELDS}
                elif kind == "TRACK_STATE":
                    track = str(item["subject_id"])
                    subject, status = identities.get((name, track), ("{0}:{1}".format(name, track), "ANONYMOUS"))
                    base.update(observed_subject=subject, local_track_id="{0}:{1}".format(name, track),
                                identity_status=status)
                    base["values"] = {out: attributes.get(key) for key, out in TRACK_STATE_FIELDS}
                    allowed = {key for key, _ in TRACK_STATE_FIELDS}
                    for key in attributes:
                        if key not in allowed:
                            dropped[key] = dropped.get(key, 0) + 1
                else:
                    dropped["fact type " + kind] = dropped.get("fact type " + kind, 0) + 1
                    continue
                facts.append(base)
    return facts


def _sort_key(fact: Dict[str, Any]) -> Tuple[Any, ...]:
    t_global = fact.get("t_global_s")
    return (0 if t_global is not None else 1,
            t_global if t_global is not None else (fact.get("t_local_s") or 0.0),
            fact.get("recorder") or "", FACT_TYPE_ORDER.index(fact["type"]),
            fact.get("local_track_id") or fact.get("sign_id") or "", fact.get("t_local_s") or 0.0)


def build_forensic_facts(run_dir: Path) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """All admissible facts of a run (with ids) and the per-recorder context for the packet."""
    run_dir = Path(run_dir)
    rec_dir = run_dir / "reconstruction"
    if not (rec_dir / "global" / "alignment.json").exists():
        raise ExportError("{0} has no reconstruction; run scripts/reconstruct_run.py first".format(run_dir))
    alignment = _read_json(rec_dir / "global" / "alignment.json")
    associations = _read_json(rec_dir / "global" / "associations.json")
    recorders = _recorders(rec_dir)
    clocks = {name: _Clock(name, alignment["graphs"][name]["status"], alignment["graphs"][name].get("offset_to_global"))
              for name in recorders}
    identities = _identity_table(associations)
    facts: List[Dict[str, Any]] = []
    dropped: Dict[str, int] = {}
    recorder_info = []
    for name in recorders:
        local_graph = _read_json(rec_dir / name / "local_graph.json")
        recorder = local_graph["recorder"]
        origin = float(recorder["clock"]["origin_source_timestamp"])
        start, end = float(recorder["start_t_local"]), float(recorder["end_t_local"])
        facts += _frame_facts(rec_dir / name / "local_trace.jsonl", name, clocks[name], identities, dropped)
        facts += _sign_facts(run_dir, name, origin, clocks[name])
        recorder_info.append({
            "recorder_id": name,
            "clock": {"time_alignment": clocks[name].status, "offset_to_global_s": clocks[name].offset
                      if clocks[name].status == "ALIGNED" else None},
            "observation_window_local_s": [_round_time(start), _round_time(end)],
            "observation_window_global_s": [clocks[name].to_global(start), clocks[name].to_global(end)],
            "vehicle_footprint": _footprint(local_graph),
            "radars": _radar_coverage(run_dir / "vehicles" / name),
            "sample_rate_hz": recorder.get("trace_hz"),
        })
    facts += _collision_facts(rec_dir, recorders, clocks, alignment)
    facts.sort(key=_sort_key)
    width = max(4, len(str(len(facts))))
    for index, fact in enumerate(facts, start=1):
        fact["fact_id"] = "F{0:0{1}d}".format(index, width)
    context = {"recorders": recorder_info, "supplied_context": _supplied_context(run_dir),
               "dropped": dict(sorted(dropped.items()))}
    return [_ordered(fact) for fact in facts], context


def _ordered(fact: Dict[str, Any]) -> Dict[str, Any]:
    first = ("fact_id", "type", "recorder", "t_local_s", "t_global_s", "observed_subject", "local_track_id",
             "identity_status", "sign_id", "participants", "time_origin")
    out = {key: fact[key] for key in first if key in fact}
    out.update((key, fact[key]) for key in fact if key not in out)
    return out


def _entities(facts: Sequence[Dict[str, Any]], recorders: Sequence[str]) -> List[Dict[str, Any]]:
    entities = [{"entity_id": name, "kind": "RECORDER"} for name in recorders]
    tracks: Dict[str, Dict[str, Any]] = {}
    for fact in facts:
        if fact["type"] == "TRACK_STATE":
            entry = tracks.setdefault(fact["local_track_id"], {
                "entity_id": fact["local_track_id"], "kind": "RADAR_TRACK", "observer": fact["recorder"],
                "identity_status": fact["identity_status"], "observed_subject": fact["observed_subject"],
                "first_t_local_s": fact["t_local_s"], "first_t_global_s": fact["t_global_s"], "samples": 0})
            entry["last_t_local_s"], entry["last_t_global_s"] = fact["t_local_s"], fact["t_global_s"]
            entry["samples"] += 1
    signs = {}
    for fact in facts:
        if fact["type"] == "SIGN_DETECTION":
            signs[fact["sign_id"]] = {"entity_id": fact["sign_id"], "kind": "SIGN", "observer": fact["recorder"],
                                      "class": fact["values"]["class"]}
    return entities + [tracks[key] for key in sorted(tracks)] + [signs[key] for key in sorted(signs)]


def _columnar(facts: Sequence[Dict[str, Any]], kind: str, header: Sequence[str],
              value_fields: Sequence[str]) -> Dict[str, Any]:
    rows = []
    for fact in facts:
        if fact["type"] == kind:
            rows.append([fact.get(key) for key in header] + [fact["values"].get(key) for key in value_fields])
    return {"columns": list(header) + list(value_fields), "rows": rows}


def build_packet(facts: Sequence[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic reorganisation of the facts: no fact added, removed or interpreted."""
    recorders = [item["recorder_id"] for item in context["recorders"]]
    common = ("fact_id", "recorder", "t_local_s", "t_global_s")
    packet = {
        "schema_version": PACKET_SCHEMA_VERSION,
        "facts_schema_version": FACTS_SCHEMA_VERSION,
        "run_id": "case-" + sha256_text("\n".join(canonical_json(fact) for fact in facts))[:16],
        "supplied_context": context["supplied_context"],
        "known_recorders": context["recorders"],
        "entities": _entities(facts, recorders),
        "field_definitions": FIELD_DEFINITIONS,
        "facts": {
            "EGO_MOTION": _columnar(facts, "EGO_MOTION", common, EGO_MOTION_FIELDS),
            "EGO_CONTROL": _columnar(facts, "EGO_CONTROL", common, EGO_CONTROL_FIELDS),
            "TRACK_STATE": _columnar(facts, "TRACK_STATE",
                                     common + ("observed_subject", "local_track_id", "identity_status"),
                                     [out for _, out in TRACK_STATE_FIELDS]),
            "SIGN_DETECTION": _columnar(facts, "SIGN_DETECTION", common + ("sign_id",), SIGN_FIELDS),
            "COLLISION_OBSERVATION": [{key: fact[key] for key in ("fact_id", "t_global_s", "participants",
                                                                  "time_origin", "reports", "matching")}
                                      for fact in facts if fact["type"] == "COLLISION_OBSERVATION"],
        },
    }
    return packet


def packet_fact_ids(packet: Dict[str, Any]) -> List[str]:
    ids = []
    for kind, block in packet["facts"].items():
        if isinstance(block, dict):
            index = block["columns"].index("fact_id")
            ids += [row[index] for row in block["rows"]]
        else:
            ids += [item["fact_id"] for item in block]
    return ids


def packet_entity_ids(packet: Dict[str, Any]) -> List[str]:
    return [entity["entity_id"] for entity in packet["entities"]]


def _file_digest(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def export_forensic_facts(run_dir: Path, output_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Write forensic_facts.jsonl, forensic_packet.json and export_manifest.json; return a summary.

    The packet goes through the leak guard before it is written: a packet that
    names anything forbidden is never written (fail closed).
    """
    from .guard import check_packet

    run_dir = Path(run_dir)
    out = Path(output_dir) if output_dir is not None else run_dir / "reconstruction" / "llm"
    facts, context = build_forensic_facts(run_dir)
    packet = build_packet(facts, context)
    check_packet(packet)
    out.mkdir(parents=True, exist_ok=True)
    facts_text = "".join(canonical_json(dict(fact, schema_version=FACTS_SCHEMA_VERSION)) + "\n" for fact in facts)
    (out / "forensic_facts.jsonl").write_text(facts_text, encoding="utf-8")
    packet_text = json.dumps(packet, indent=1, sort_keys=False, ensure_ascii=False) + "\n"
    (out / "forensic_packet.json").write_text(packet_text, encoding="utf-8")
    rec = run_dir / "reconstruction"
    inputs = sorted([path for name in (item["recorder_id"] for item in context["recorders"])
                     for path in (rec / name / "local_trace.jsonl", rec / name / "local_graph.json",
                                  run_dir / "vehicles" / name / "metadata.json",
                                  run_dir / "vehicles" / name / "traffic_signs.jsonl") if path.exists()]
                    + [rec / "global" / "alignment.json", rec / "global" / "associations.json"]
                    + ([run_dir / "incident_context.json"] if (run_dir / "incident_context.json").exists() else []))
    manifest = {
        "note": "export bookkeeping; never sent to a model",
        "facts_schema_version": FACTS_SCHEMA_VERSION,
        "packet_schema_version": PACKET_SCHEMA_VERSION,
        "run_id": packet["run_id"],
        "forensic_packet_sha256": packet_sha256(packet),
        "forensic_facts_sha256": sha256_text(facts_text),
        "fact_counts": {kind: sum(1 for fact in facts if fact["type"] == kind) for kind in FACT_TYPE_ORDER},
        "track_state_fields_exported": [out_name for _, out_name in TRACK_STATE_FIELDS],
        "removed_from_track_state": TRACK_STATE_REMOVED,
        "dropped_attribute_occurrences": context["dropped"],
        "inputs": {path.relative_to(run_dir).as_posix(): _file_digest(path) for path in inputs},
    }
    (out / "export_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"output_dir": out, "run_id": packet["run_id"], "forensic_packet_sha256": manifest["forensic_packet_sha256"],
            "facts": len(facts), "fact_counts": manifest["fact_counts"]}


def load_packet(run_dir: Path) -> Dict[str, Any]:
    path = Path(run_dir) / "reconstruction" / "llm" / "forensic_packet.json"
    if not path.exists():
        raise ExportError("no forensic packet at {0}; run scripts/export_forensic_facts.py first".format(path))
    return _read_json(path)


def iter_packet_facts(packet: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """The packet's facts back as one dict per fact (inverse of the columnar layout)."""
    for kind, block in packet["facts"].items():
        if isinstance(block, dict):
            for row in block["rows"]:
                item = dict(zip(block["columns"], row))
                item["type"] = kind
                yield item
        else:
            for item in block:
                yield dict(item, type=kind)
