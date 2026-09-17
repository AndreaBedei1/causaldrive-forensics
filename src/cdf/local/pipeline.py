"""The per-participant local analysis stage.

Recording and inference are deliberately separate stages. The recorder captures
evidence during the run; this module turns that evidence into events, an event
graph and a causal DAG *afterwards*, from the persisted artifacts alone.

That separation is not cosmetic. It means the local inference chain can be
re-run, re-tuned and unit-tested without a simulator, and -- more importantly --
it means the inference code physically never holds a handle to a CARLA world. The
only thing it can read is one participant's own recorded evidence.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from ..common.config import Config
from ..common.evidence import ParticipantEvidence, load_participant
from ..common.io import read_json, write_json
from ..common.layout import RunLayout
from ..common.schemas import Event, GraphDocument, Provenance, SCHEMA_VERSIONS, to_jsonable
from ..graph.export import save_graph
from .causal_graph import build_causal_graph
from .event_extractor import EventExtractor
from .event_graph import build_event_graph

LOGGER = logging.getLogger(__name__)

__all__ = ["analyse_participant", "analyse_run", "LocalAnalysis"]


class LocalAnalysis(object):
    """The output of local inference for one participant."""

    __slots__ = ("participant_id", "events", "event_graph", "causal_graph")

    def __init__(
        self,
        participant_id: str,
        events: List[Event],
        event_graph: GraphDocument,
        causal_graph: GraphDocument,
    ) -> None:
        self.participant_id = participant_id
        self.events = events
        self.event_graph = event_graph
        self.causal_graph = causal_graph

    def summary(self) -> Dict[str, Any]:
        by_type: Dict[str, int] = {}
        for e in self.events:
            key = e.event_type.value
            by_type[key] = by_type.get(key, 0) + 1
        return {
            "participant_id": self.participant_id,
            "n_events": len(self.events),
            "event_types": dict(sorted(by_type.items())),
            "n_event_graph_edges": len(self.event_graph.edges),
            "n_causal_nodes": len(self.causal_graph.nodes),
            "n_causal_edges": len(self.causal_graph.edges),
            "rejected_causal_edges": len(
                self.causal_graph.meta.get("rejected_edges", []) or []
            ),
        }


def analyse_participant(
    ev: ParticipantEvidence,
    cfg: Config,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> LocalAnalysis:
    """Run extraction and graph construction for one participant's evidence."""
    extractor = EventExtractor(cfg)
    events = extractor.extract(ev)

    event_graph = build_event_graph(
        events, ev, cfg, run_id=run_id, scenario_id=scenario_id, seed=seed
    )
    causal_graph = build_causal_graph(
        events, ev, cfg, run_id=run_id, scenario_id=scenario_id, seed=seed
    )

    LOGGER.info(
        "participant %s: %d events, causal graph %d nodes / %d edges",
        ev.participant_id,
        len(events),
        len(causal_graph.nodes),
        len(causal_graph.edges),
    )
    return LocalAnalysis(ev.participant_id, events, event_graph, causal_graph)


def analyse_run(
    run_dir: Any,
    cfg: Config,
    persist: bool = True,
) -> Dict[str, LocalAnalysis]:
    """Analyse every participant of a recorded run and persist their graphs.

    Reads only ``vehicle_*/`` artifacts. The ``oracle/`` subtree is never opened.
    """
    layout = run_dir if isinstance(run_dir, RunLayout) else RunLayout.from_run_dir(run_dir)
    manifest: Dict[str, Any] = {}
    if layout.manifest.exists():
        manifest = read_json(layout.manifest)
    run_id = str(manifest.get("run_id", ""))
    scenario_id = str(manifest.get("scenario_id", ""))
    seed = int(manifest.get("seed", 0))

    out: Dict[str, LocalAnalysis] = {}
    for pid in layout.participant_ids():
        ev = load_participant(layout, pid, with_radar=False)
        analysis = analyse_participant(
            ev, cfg, run_id=run_id, scenario_id=scenario_id, seed=seed
        )
        out[pid] = analysis

        if persist:
            # Re-persist events alongside the recorder metadata already on disk,
            # so that events.json carries both what was retained and what was
            # inferred from it.
            existing: Dict[str, Any] = {}
            if layout.events(pid).exists():
                existing = read_json(layout.events(pid))
            payload = {
                "schema_version": SCHEMA_VERSIONS["events"],
                "participant_id": pid,
                "provenance": Provenance.LOCAL.value,
                "meta": existing.get("meta", {}),
                "summary": analysis.summary(),
                "events": [to_jsonable(e) for e in analysis.events],
            }
            write_json(layout.events(pid), payload)
            save_graph(analysis.event_graph, layout.event_graph(pid), layout.event_graphml(pid))
            save_graph(
                analysis.causal_graph, layout.causal_graph(pid), layout.causal_graphml(pid)
            )
    return out
