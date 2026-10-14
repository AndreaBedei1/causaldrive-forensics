"""Orchestration: one run directory in, ``<run>/reconstruction/`` out.

    RAW LOG -> LOCAL TRACE -> LOCAL GRAPH      (every recorder alone)
            -> GRAPH-LEVEL ALIGNMENT           (collision anchors; else observed trajectories)
            -> IDENTITY ASSOCIATION            (anonymous track -> recorder)
            -> ROAD USERS                      (common frame of the recorders' own pose streams:
                                                track -> recorder, anonymous road users U1, U2, ...)
            -> GLOBAL GRAPH + GLOBAL TRACE

Only ``<run>/vehicles/`` and the supplied ``<run>/incident_context.json`` are
read.  ``ground_truth/`` and the run's ``metadata.json`` (scenario design) are
never opened here; the privileged evaluation lives in ``cdf.evaluation`` and
runs afterwards on the files this module wrote.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from .alignment import align_graphs
from .anonymous import RoadUserFusion, align_by_observations, fuse_road_users
from .common_frame import PoseSource, RecordedPoseSource, contact_check
from .config import ReconstructionConfig, load_config
from .fusion import associate_tracks, fuse_graphs, global_temporal_relations, global_trace
from .identity import radar_contact_evidence
from .local import LocalReconstruction, reconstruct_vehicle
from .models import Alignment, Association, GlobalGraph
from .render import (global_graph_dot, global_graph_markdown, local_graph_dot, local_graph_markdown,
                     render_svg, report_markdown, write_json, write_jsonl, write_text)


@dataclass
class RunReconstruction:
    run_dir: Path
    output_dir: Path
    locals: List[LocalReconstruction]
    alignment: Alignment
    associations: List[Association]
    graph: GlobalGraph
    trace: List[Dict[str, Any]]
    road_users: Optional[RoadUserFusion] = None

# A recorder's pose stream in the common frame from (vehicle directory, its clock origin): the recorded
# GNSS-like stream by default; the robustness study substitutes a perturbed one.
PoseFactory = Callable[[Path, float], PoseSource]


def run_title(run_dir: Path) -> str:
    return "{0}/{1}".format(run_dir.parent.name, run_dir.name)


def read_incident_context(run_dir: Path) -> Dict[str, Any]:
    """The run's supplied incident context, e.g. the known speed limit; {} if none.

    ``incident_context.json`` is the only run-level file the reconstruction
    reads: it is known context, not perception and not ground truth.
    """
    path = Path(run_dir) / "incident_context.json"
    if not path.exists():
        return {}
    context = json.loads(path.read_text(encoding="utf-8"))
    limit = context.get("speed_limit_kmh")
    if limit is not None and (isinstance(limit, bool) or not isinstance(limit, (int, float)) or limit <= 0):
        raise ValueError("incident_context.json: speed_limit_kmh must be a positive number")
    return context


def _on_trace_grid(t_local: float, trace_hz: float) -> bool:
    return abs(t_local * trace_hz - round(t_local * trace_hz)) < 1e-3


def write_local_outputs(directory: Path, local: LocalReconstruction, trace_hz: float) -> None:
    write_jsonl(directory / "local_trace.jsonl", (frame.to_dict() for frame in local.trace))
    # Tracks are smoothed at the radar rate; the file keeps the readable trace rate.
    track_rows = []
    for track in local.tracks:
        for sample in track.samples:
            if _on_trace_grid(sample.t_local, trace_hz):
                track_rows.append(sample.to_dict(track.track_id))
    write_jsonl(directory / "local_tracks.jsonl", track_rows)
    write_json(directory / "local_graph.json", local.graph.to_dict())
    write_text(directory / "local_graph.md", local_graph_markdown(local.graph))
    write_text(directory / "local_graph.dot", local_graph_dot(local.graph))
    render_svg(directory / "local_graph.dot")


def fuse_recorders(run_dir: Path, locals_: List[LocalReconstruction], cfg: ReconstructionConfig,
                   pose_factory: Optional[PoseFactory] = None
                   ) -> Tuple[Alignment, List[Association], RoadUserFusion, GlobalGraph]:
    """The cross-recorder steps on finished local reconstructions: alignment, identity association,
    road users in the common frame, global graph (nothing is written)."""
    pose_factory = pose_factory or RecordedPoseSource.from_vehicle_dir
    poses = {local.owner: pose_factory(Path(run_dir) / "vehicles" / local.owner, local.clock_origin)
             for local in locals_}
    # Matched collisions, each checked against the recorders' own pose streams (the two bodies must touch).
    geometry = contact_check(poses, {local.owner: local.footprint for local in locals_},
                             cfg.fusion.contact_consistency_m)
    # Before fixing clocks, the pose streams only veto a pairing (bodies clearly apart, ``contact_check``);
    # what supports or contradicts it is each recorder's own radar view of the contact (no GNSS involved).
    radar = radar_contact_evidence(locals_, cfg)

    def approach_check(a: str, ta: float, b: str, tb: float) -> Optional[bool]:
        return False if radar(a, ta, b, tb) is False else None

    alignment = align_graphs([local.graph for local in locals_], cfg.fusion, geometry, approach_check)
    for event in alignment.matched_events:
        event['evidence'].append("pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted")
    associations = associate_tracks(locals_, alignment, cfg.fusion, cfg.tracking.radial_speed_std_mps)
    # A recorder no matched collision aligned: the clock offset its observed trajectory fixes, if unique,
    # in the common frame of the recorders' own pose streams (then the association is redone).
    align_by_observations(locals_, alignment, associations, poses, cfg)
    if alignment.observed:
        associations = associate_tracks(locals_, alignment, cfg.fusion, cfg.tracking.radial_speed_std_mps)
    # Anonymous tracks that are recorders, and the road users that recorded nothing (U1, U2, ...).
    road_users = fuse_road_users(locals_, alignment, associations, poses, cfg)
    return alignment, associations, road_users, fuse_graphs(locals_, alignment, associations, cfg.fusion.touching_clearance_m)


def reconstruct_run(run_dir: Path, cfg: Optional[ReconstructionConfig] = None,
                    pose_factory: Optional[PoseFactory] = None) -> RunReconstruction:
    run_dir = Path(run_dir)
    cfg = cfg or load_config()
    output_dir = run_dir / "reconstruction"
    # A previous privileged evaluation would describe an older reconstruction.
    for stale in (output_dir / "evaluation" / "evaluation.json", output_dir / "evaluation" / "evaluation.md"):
        if stale.exists():
            stale.unlink()

    # 1-4. Every recorder alone: raw files (+ the supplied incident context)
    #      -> local trace, anonymous tracks, local graph.
    context = read_incident_context(run_dir)
    vehicle_dirs = sorted(path for path in (run_dir / "vehicles").iterdir() if path.is_dir())
    locals_ = [reconstruct_vehicle(path, cfg, context=context) for path in vehicle_dirs]
    for local in locals_:
        write_local_outputs(output_dir / local.owner, local, cfg.trace_hz)

    # 5-8. Only now look across recorders, and only at their graphs, tracks and pose streams.
    alignment, associations, road_users, graph = fuse_recorders(run_dir, locals_, cfg, pose_factory)
    trace = global_trace(graph)
    relations = global_temporal_relations(locals_, alignment, associations)

    # 9. Human-readable files.
    title = run_title(run_dir)
    global_dir = output_dir / "global"
    write_json(global_dir / "alignment.json", alignment.to_dict())
    write_json(global_dir / "associations.json", [item.to_dict() for item in associations])
    road_user_record = road_users.to_dict(cfg, alignment)
    write_json(global_dir / "anonymous_entities.json", road_user_record)
    write_jsonl(global_dir / "global_trace.jsonl", trace)
    write_json(global_dir / "global_graph.json", dict(graph.to_dict(), run=title, incident_context=context or None,
                                                     temporal_safety_relations=relations,
                                                     reconstruction_config=cfg.to_dict()))
    write_text(global_dir / "global_graph.md",
               global_graph_markdown(title, graph, alignment, associations, trace, context, relations))
    write_text(global_dir / "global_graph.dot", global_graph_dot(title, graph))
    render_svg(global_dir / "global_graph.dot")
    write_text(output_dir / "report.md",
               report_markdown(title, locals_, alignment, associations, graph, trace, cfg.to_dict(), context,
                               relations, road_user_record))
    return RunReconstruction(run_dir=run_dir, output_dir=output_dir, locals=locals_, alignment=alignment,
                             associations=associations, graph=graph, trace=trace, road_users=road_users)
