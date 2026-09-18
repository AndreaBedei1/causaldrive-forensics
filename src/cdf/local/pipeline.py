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
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.evidence import ParticipantEvidence, load_participant
from ..common.io import read_json, write_json
from ..common.layout import RunLayout
from ..common.schemas import Event, GraphDocument, Provenance, SCHEMA_VERSIONS, to_jsonable
from ..common.event_log import build_local_log
from ..graph.export import save_graph
from ..graph.non_actions import build_non_actions, coverage_from_samples
from .causal_graph import build_causal_graph
from .event_extractor import EventExtractor
from .event_graph import build_event_graph

LOGGER = logging.getLogger(__name__)

__all__ = ["analyse_participant", "analyse_run", "LocalAnalysis"]


class LocalAnalysis(object):
    """The output of local inference for one participant."""

    __slots__ = (
        "participant_id", "events", "event_graph", "causal_graph",
        "non_actions", "unknown_non_actions", "perception_events",
    )

    def __init__(
        self,
        participant_id: str,
        events: List[Event],
        event_graph: GraphDocument,
        causal_graph: GraphDocument,
        non_actions: Optional[List[Event]] = None,
        unknown_non_actions: Optional[List[Dict[str, Any]]] = None,
        perception_events: Optional[List[Event]] = None,
    ) -> None:
        self.participant_id = participant_id
        self.events = events
        self.event_graph = event_graph
        self.causal_graph = causal_graph
        self.non_actions = list(non_actions or [])
        #: Obligations that arose but whose interval was not covered well enough
        #: to judge. Kept because a detector that stayed silent invisibly cannot
        #: be told apart from one that found nothing.
        self.unknown_non_actions = list(unknown_non_actions or [])
        self.perception_events = list(perception_events or [])

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
            "n_non_actions": len(self.non_actions),
            "n_non_actions_unknown": len(self.unknown_non_actions),
            "n_perception_events": len(self.perception_events),
        }


def perception_events(
    layout: RunLayout, participant_id: str
) -> List[Any]:
    """Events already written by the camera and lane pipelines, if any.

    Sign detections, stop-line inference and marking crossings are produced while
    the run is recorded, because they need the frames, and the frames are not
    kept. So they arrive here as artifacts rather than as computation, and a run
    recorded without a camera simply has none -- which is why every caller has to
    cope with their absence rather than assume them.
    """
    from ..common.schemas import events_from_payload

    out: List[Any] = []
    for path in (
        layout.traffic_sign_detections(participant_id),
        layout.lane_events(participant_id),
    ):
        if not path.exists():
            continue
        payload = read_json(path)
        if isinstance(payload, Mapping):
            out.extend(events_from_payload(payload.get("events", []) or []))
    return out


def analyse_participant(
    ev: ParticipantEvidence,
    cfg: Config,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
    extra_events: Optional[Sequence[Any]] = None,
) -> LocalAnalysis:
    """Run extraction and graph construction for one participant's evidence.

    ``extra_events`` are the perception events recorded during the run -- signs,
    stop lines, marking crossings. They are folded in *before* the non-action
    pass, because a non-action is defined by an obligation, and the obligations in
    this system come from what the camera saw.
    """
    extractor = EventExtractor(cfg)
    events = list(extractor.extract(ev))
    events.extend(extra_events or [])

    # Non-actions last, from everything else, and only where the recorder was
    # actually watching. Coverage comes from the telemetry the vehicle really
    # produced, so a dropout makes the claim UNKNOWN instead of confident.
    period = ev.sample_period() or 0.05
    coverage = coverage_from_samples([float(s.t) for s in ev.telemetry], period)
    derived = build_non_actions(
        ev.participant_id, events, coverage=coverage, cfg=cfg,
        id_prefix="na-{0}".format(ev.participant_id),
    )
    events.extend(derived["events"])
    events.sort(key=lambda e: (float(e.t_peak), e.event_id))

    event_graph = build_event_graph(
        events, ev, cfg, run_id=run_id, scenario_id=scenario_id, seed=seed
    )
    causal_graph = build_causal_graph(
        events, ev, cfg, run_id=run_id, scenario_id=scenario_id, seed=seed
    )

    LOGGER.info(
        "participant %s: %d events (%d perceived, %d non-actions, %d undecidable), "
        "causal graph %d nodes / %d edges",
        ev.participant_id,
        len(events),
        len(extra_events or []),
        derived["n_asserted"],
        derived["n_unknown"],
        len(causal_graph.nodes),
        len(causal_graph.edges),
    )
    return LocalAnalysis(
        ev.participant_id, events, event_graph, causal_graph,
        non_actions=derived["events"],
        unknown_non_actions=derived["unknown"],
        perception_events=list(extra_events or []),
    )


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
            ev, cfg, run_id=run_id, scenario_id=scenario_id, seed=seed,
            extra_events=perception_events(layout, pid),
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
            # The readable form, written beside the graph rather than instead of
            # it. A reader checks the table; the graph is the claim built on it.
            log = build_local_log(
                pid, analysis.events, run_id=run_id, scenario_id=scenario_id,
                seed=seed,
            )
            log["undecidable_non_actions"] = analysis.unknown_non_actions
            write_json(layout.local_log(pid), log)
    return out
