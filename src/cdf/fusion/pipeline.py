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
from typing import Any, Dict, Optional

from ..common.config import Config
from ..common.evidence import RunEvidence, load_run
from ..common.io import write_json
from ..common.layout import RunLayout
from ..common.schemas import GraphDocument, Provenance, SCHEMA_VERSIONS, to_jsonable
from ..graph.export import graph_summary, load_graph, save_graph
from .event_alignment import resolve_subjects
from .aligned_evidence import AlignedRunEvidence
from .graph_fusion import fuse_graphs
from .time_alignment import align_participants
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
        "fused_event",
        "diagnostics",
        "local_causal",
        "local_event",
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
    ) -> None:
        self.alignment = alignment
        self.assignments = assignments
        self.subject_map = subject_map
        self.fused_causal = fused_causal
        self.fused_event = fused_event
        self.diagnostics = diagnostics
        self.local_causal = local_causal
        self.local_event = local_event

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

    alignment = align_participants(run, cfg)
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

    fused_causal, diagnostics = fuse_graphs(
        run, local_causal, assignments, cfg, graph_kind="causal"
    )

    fused_event: Optional[GraphDocument] = None
    event_diag: Dict[str, Any] = {}
    if fuse_event_graph and local_event:
        fused_event, event_diag = fuse_graphs(
            run, local_event, assignments, cfg, graph_kind="event"
        )

    diagnostics = dict(diagnostics)
    diagnostics["time_alignment"] = alignment
    diagnostics["subject_map"] = subject_map
    diagnostics["event_graph_fusion"] = event_diag
    diagnostics["schema_version"] = SCHEMA_VERSIONS["fusion_diagnostics"]

    if persist:
        layout.fusion_dir.mkdir(parents=True, exist_ok=True)
        write_json(layout.association_report, association_report(assignments, run, cfg))
        write_json(layout.fusion_diagnostics, diagnostics)
        write_json(layout.fusion_dir / "time_alignment.json", alignment)
        write_json(
            layout.fused_events,
            {
                "schema_version": SCHEMA_VERSIONS["events"],
                "provenance": Provenance.FUSED.value,
                "events": [to_jsonable(n) for n in fused_causal.nodes],
            },
        )
        save_graph(fused_causal, layout.fused_causal_graph, layout.fused_causal_graphml)
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
        fused_event=fused_event,
        diagnostics=diagnostics,
        local_causal=local_causal,
        local_event=local_event,
    )
