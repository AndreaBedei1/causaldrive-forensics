"""The post-event fusion stage.

Runs the fusion chain over one recorded run and persists its artifacts:

1. **Time alignment** -- estimate each participant's clock offset explicitly,
   rather than assuming the shared simulator clock.
2. **Track association** -- decide which participant each anonymous local radar
   track was actually observing, by comparing the track's globally transformed
   trajectory estimate against that participant's own shared telemetry. No CARLA
   actor identity is involved at any point.
3. **Event alignment and graph fusion** -- merge the independently built local
   graphs into one multi-vehicle event graph and causal DAG, preserving
   provenance and keeping disagreements visible.

The stage loads only ``vehicle_*/`` artifacts. It never opens ``oracle/``, and
:func:`cdf.graph.export.load_graph` is called with an explicit ``LOCAL`` scope so
that a mis-wired path fails loudly instead of leaking ground truth.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from ..common.config import Config
from ..common.evidence import RunEvidence, load_run
from ..common.event_log import build_global_log
from ..common.io import write_json
from ..common.layout import RunLayout
from ..common.schemas import GraphDocument, Provenance, SCHEMA_VERSIONS, to_jsonable
from ..graph.export import graph_summary, load_graph, save_graph
from .event_alignment import resolve_subjects
from .aligned_evidence import AlignedRunEvidence
from .graph_fusion import fuse_graphs
from ..graph.episodes import CausalEpisode, extract_episodes
from ..graph.reconstruction import (
    build_attribution_hypothesis,
    build_incident_reconstruction,
)
from ..formal import EventTrace, check_all, describe_properties
from ..responsibility import (
    benchmark_priority, build_responsibility_graph, build_responsibility_report,
)
from .time_alignment import align_participants
from .hybrid_alignment import align_hybrid
from .contact_alignment import (
    CONTACT_DERIVED_STATUSES, align_by_acquisition_start, align_by_contact,
)
from .track_association import associate_tracks, association_report

LOGGER = logging.getLogger(__name__)

__all__ = ["FusionResult", "fuse_run"]


class FusionResult(object):
    """Everything the fusion stage produced for one run."""

    __slots__ = (
        "alignment",
        "assignments",
        "subject_map",
        "fused_causal",
        "simple_fused_causal",
        "fused_event",
        "diagnostics",
        "local_causal",
        "local_event",
        "episodes",
        "reconstruction",
        "attribution",
    )

    def __init__(
        self,
        alignment: Dict[str, Any],
        assignments: Dict[str, Any],
        subject_map: Dict[str, str],
        fused_causal: GraphDocument,
        fused_event: Optional[GraphDocument],
        diagnostics: Dict[str, Any],
        local_causal: Dict[str, GraphDocument],
        local_event: Dict[str, GraphDocument],
        simple_fused_causal: Optional[GraphDocument] = None,
        episodes: Optional[List[CausalEpisode]] = None,
        reconstruction: Optional[Dict[str, Any]] = None,
        attribution: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.alignment = alignment
        self.assignments = assignments
        self.subject_map = subject_map
        self.fused_causal = fused_causal
        #: The union baseline the global graph was built on top of: same nodes,
        #: local edges only. Kept so a caller can compare the two without
        #: re-running fusion, and without reconstructing it by subtraction,
        #: which would not give the same graph.
        self.simple_fused_causal = simple_fused_causal
        self.fused_event = fused_event
        self.diagnostics = diagnostics
        self.local_causal = local_causal
        self.local_event = local_event
        self.episodes = list(episodes or [])
        self.reconstruction = reconstruction
        self.attribution = attribution

    def summary(self) -> Dict[str, Any]:
        resolved = sum(
            1 for a in self.assignments.values() if getattr(a, "status", "") == "RESOLVED"
        )
        return {
            "n_tracks": len(self.assignments),
            "n_resolved": resolved,
            "n_ambiguous": sum(
                1 for a in self.assignments.values() if getattr(a, "status", "") == "AMBIGUOUS"
            ),
            "n_unresolved": sum(
                1 for a in self.assignments.values() if getattr(a, "status", "") == "UNRESOLVED"
            ),
            "fused_causal": graph_summary(self.fused_causal),
            "clock_offsets": {
                pid: blk.get("offset_s") for pid, blk in self.alignment.get("offsets", {}).items()
            },
        }


def _choose_alignment(
    run: RunEvidence,
    cfg: Config,
) -> Dict[str, Any]:
    """The clock alignment to fuse on, and an honest record of where it came from.

    Contact first, always: two recorders that felt the same impact give the
    difference between their clocks directly, with nothing fitted.

    Contact alone is not enough, and two recorded cases showed why -- a vehicle
    that never collides has no anchor at all, and a chain can yield one anchor
    where two impacts happened, which on the recorded three-car case moved a
    whole timeline by exactly the 0.200 s between them. So where contact is
    missing, ambiguous or impeached by its own caveat, an offset-only radar and
    trajectory fit is tried, and each participant records which source placed it.
    That hierarchy lives in :mod:`cdf.fusion.hybrid_alignment`.

    If neither source is sufficient the recorder stays unresolved. There is no
    hidden simulator-time fallback: the acquisition-start marker remains for the
    negative controls, which have no contact *and* no useful radar geometry, and
    it keeps its own status so it can never be read as a reconstruction result.
    """
    hybrid = align_hybrid(run, cfg)
    if hybrid.get("offsets_s"):
        return hybrid

    contact = hybrid.get("contact_stage") or {}
    if not bool(cfg.get("fusion.contact_alignment.acquisition_start_fallback", True)):
        LOGGER.info(
            "neither contact nor radar placed any recorder and the "
            "acquisition-start fallback is disabled: recorders stay on their own "
            "clocks"
        )
        return hybrid

    fallback = align_by_acquisition_start(run, cfg)
    if not fallback.get("offsets_s"):
        return hybrid
    fallback["contact_alignment_attempted"] = {
        "status": contact.get("status"),
        "reason": contact.get("reason"),
        "n_contact_anchors": contact.get("n_contact_anchors", 0),
    }
    fallback["hybrid_alignment_attempted"] = {
        "status": hybrid.get("status"),
        "clock_sources": hybrid.get("clock_sources"),
        "decisions": hybrid.get("decisions"),
    }
    LOGGER.info(
        "neither contact nor radar placed any recorder (%s); falling back to the "
        "declared acquisition-start marker, which is reported apart from "
        "reconstructed alignments",
        hybrid.get("status"),
    )
    return fallback


def fuse_run(
    run_dir: Any,
    cfg: Config,
    persist: bool = True,
    fuse_event_graph: bool = True,
) -> FusionResult:
    """Execute the fusion chain over a recorded run."""
    layout = run_dir if isinstance(run_dir, RunLayout) else RunLayout.from_run_dir(run_dir)
    run: RunEvidence = load_run(layout.root, with_radar=True)

    if len(run.participant_ids) < 2:
        raise ValueError(
            "fusion needs at least two participants; run {0} has {1}".format(
                layout.root, run.participant_ids
            )
        )

    # V2 final: contact is the primary anchor and an offset-only radar fit is the
    # fallback behind it, per participant. The V1 whole-run radar estimator is
    # still run unchanged, because the clock ablation compares against it, but it
    # does not decide the timeline the results are computed on.
    alignment = _choose_alignment(run, cfg)
    radar_alignment: Optional[Dict[str, Any]] = None
    if bool(cfg.get("fusion.keep_radar_alignment_diagnostic", True)):
        try:
            radar_alignment = align_participants(run, cfg)
        except Exception as exc:  # pragma: no cover - diagnostic only
            LOGGER.warning("radar alignment diagnostic failed: %s", exc)
            radar_alignment = {"status": "FAILED", "error": str(exc)}

    if not alignment.get("offsets_s"):
        LOGGER.warning(
            "no common timeline for %s (%s): the merged log will show separate "
            "local timelines and say so",
            layout.root.name, alignment["status"],
        )
    run = AlignedRunEvidence(run, alignment)
    assignments = associate_tracks(run, cfg)
    subject_map = resolve_subjects(assignments)
    LOGGER.info(
        "track association: %d track(s), subject map %s",
        len(assignments),
        subject_map,
    )

    local_causal: Dict[str, GraphDocument] = {}
    local_event: Dict[str, GraphDocument] = {}
    for pid in run.participant_ids:
        cpath = layout.causal_graph(pid)
        if cpath.exists():
            local_causal[pid] = load_graph(cpath, expect_scope=Provenance.LOCAL)
        epath = layout.event_graph(pid)
        if epath.exists():
            local_event[pid] = load_graph(epath, expect_scope=Provenance.LOCAL)

    if not local_causal:
        raise FileNotFoundError(
            "no local causal graphs under {0}; run the local analysis stage first "
            "(cdf.local.pipeline.analyse_run)".format(layout.root)
        )

    products: Dict[str, Any] = {}
    fused_causal, diagnostics = fuse_graphs(
        run, local_causal, assignments, cfg, graph_kind="causal",
        products=products,
    )
    simple_fused_causal = products.get("simple_fusion")

    fused_event: Optional[GraphDocument] = None
    event_diag: Dict[str, Any] = {}
    if fuse_event_graph and local_event:
        fused_event, event_diag = fuse_graphs(
            run, local_event, assignments, cfg, graph_kind="event"
        )

    diagnostics = dict(diagnostics)
    diagnostics["time_alignment"] = alignment
    diagnostics["clock_method"] = alignment.get("method")
    diagnostics["clock_status"] = alignment.get("status")
    diagnostics["clock_is_contact_derived"] = (
        alignment.get("status") in CONTACT_DERIVED_STATUSES
    )
    diagnostics["radar_alignment_diagnostic"] = radar_alignment
    diagnostics["subject_map"] = subject_map
    diagnostics["event_graph_fusion"] = event_diag
    diagnostics["schema_version"] = SCHEMA_VERSIONS["fusion_diagnostics"]

    # What the merged account actually says happened, and which behaviours it
    # implicates. Both are read off the fused causal graph, so they are produced
    # here rather than in a separate pass that could drift out of step with it.
    # The readable table, before any of the claims built on it. Written from the
    # fused nodes because those are the events that survived deduplication, and
    # on common time only where common time exists.
    global_log = build_global_log(
        fused_causal.nodes, alignment=alignment,
        run_id=run.run_id, scenario_id=run.scenario_id, seed=run.seed,
    )
    global_log["clock_method"] = alignment.get("method")
    if alignment.get("caveat"):
        global_log["clock_caveat"] = alignment["caveat"]

    # Temporal properties over the merged trace. The trace carries which clock it
    # is on and which recorders share it, so a property relating two vehicles can
    # refuse rather than compare timestamps from two different clocks.
    trace = EventTrace.from_events(
        fused_causal.nodes,
        coverage=None,
        time_axis="common" if alignment.get("offsets_s") else "local",
        aligned_participants=alignment.get("aligned_participants", []),
    )
    formal = check_all(trace, cfg, scope=Provenance.FUSED)

    episodes = extract_episodes(fused_causal, cfg, run.participant_ids)
    reconstruction = build_incident_reconstruction(
        fused_causal, cfg, run.participant_ids, alignment, episodes
    )
    attribution = build_attribution_hypothesis(reconstruction, fused_causal, cfg)

    # Normative reasoning, in its own graph. Built from the physical graph and the
    # observed events, so a reader can accept the physics and dispute the norm.
    priority = benchmark_priority(
        fused_causal.nodes, participants=run.participant_ids, cfg=cfg,
    )
    responsibility = build_responsibility_graph(
        fused_causal.nodes, physical_graph=fused_causal, formal_results=formal,
        priority=priority, cfg=cfg, run_id=run.run_id,
        scenario_id=run.scenario_id, seed=run.seed,
    )
    responsibility_report = build_responsibility_report(
        responsibility, fused_causal.nodes, formal_results=formal,
        attribution=attribution, priority=priority, cfg=cfg,
        run_id=run.run_id, scenario_id=run.scenario_id, seed=run.seed,
    )

    if persist:
        layout.fusion_dir.mkdir(parents=True, exist_ok=True)
        write_json(layout.association_report, association_report(assignments, run, cfg))
        write_json(layout.fusion_diagnostics, diagnostics)
        write_json(layout.clock_alignment, alignment)
        write_json(layout.global_log, global_log)
        write_json(layout.identity_association, {
            "schema_version": SCHEMA_VERSIONS["fusion_diagnostics"],
            "subject_map": subject_map,
            "note": (
                "which anonymous local track turned out to be which participant. "
                "Resolved from trajectory agreement, never from actor identity"
            ),
        })
        layout.formal_dir.mkdir(parents=True, exist_ok=True)
        write_json(layout.formal_properties, describe_properties())
        write_json(layout.formal_results, formal)
        write_json(layout.responsibility_graph, responsibility)
        write_json(layout.responsibility_report, responsibility_report)
        # Retained under its historical name as well, because the clock ablation
        # reads it and because a V1 artifact tree has it.
        write_json(layout.fusion_dir / "time_alignment.json", alignment)
        write_json(
            layout.fused_events,
            {
                "schema_version": SCHEMA_VERSIONS["events"],
                "provenance": Provenance.FUSED.value,
                "events": [to_jsonable(n) for n in fused_causal.nodes],
            },
        )
        write_json(layout.incident_reconstruction, reconstruction)
        write_json(layout.causal_attribution, attribution)
        save_graph(fused_causal, layout.fused_causal_graph, layout.fused_causal_graphml)
        if simple_fused_causal is not None:
            save_graph(
                simple_fused_causal,
                layout.simple_fused_causal_graph,
                layout.simple_fused_causal_graphml,
            )
        if fused_event is not None:
            save_graph(fused_event, layout.fused_event_graph, layout.fused_event_graphml)

    LOGGER.info(
        "fusion complete: %d fused causal nodes / %d edges",
        len(fused_causal.nodes),
        len(fused_causal.edges),
    )
    return FusionResult(
        alignment=alignment,
        assignments=assignments,
        subject_map=subject_map,
        fused_causal=fused_causal,
        simple_fused_causal=simple_fused_causal,
        fused_event=fused_event,
        diagnostics=diagnostics,
        local_causal=local_causal,
        local_event=local_event,
        episodes=episodes,
        reconstruction=reconstruction,
        attribution=attribution,
    )
