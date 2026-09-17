"""Read-only common-clock copies; persisted local records are never overwritten."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from typing import Any, Dict
from ..common.evidence import RunEvidence
from ..common.schemas import Event, Evidence, GraphDocument


def participant_is_aligned(run: RunEvidence, pid: str) -> bool:
    if run.time_alignment is None:
        # Low-level APIs also accept explicitly synchronized legacy evidence.
        return run.manifest.get("clock_protocol") != "independent_local_clocks"
    return run.time_alignment["offsets"].get(pid, {}).get("status") == "ALIGNED"


def require_common_time(run: RunEvidence) -> None:
    if run.time_alignment is None and (
        run.manifest.get("clock_protocol") == "independent_local_clocks"
        or any(
            p.meta.get("time_domain") == "participant_local"
            for p in run.participants.values()
        )
    ):
        raise ValueError(
            "independent local evidence requires AlignedRunEvidence before cross-vehicle comparison"
        )


class AlignedRunEvidence(RunEvidence):
    """Owns copies of all time-bearing records, plus their estimated transforms."""

    def __init__(self, raw: RunEvidence, alignment: Dict[str, Any]):
        self.raw = raw
        super().__init__(raw.run_dir, deepcopy(raw.manifest), {}, deepcopy(alignment))
        for pid, ev in raw.participants.items():
            model = alignment["offsets"].get(pid, {})
            meta = deepcopy(ev.meta)
            if model.get("status") != "ALIGNED":
                meta["time_domain"] = "unresolved_participant_local"
                self.participants[pid] = replace(deepcopy(ev), meta=meta)
                continue

            def copy_stream(stream):
                return [replace(s, t=self.time(pid, s.t)) for s in stream]

            meta["time_domain"] = "common"
            self.participants[pid] = replace(
                ev,
                telemetry=copy_stream(ev.telemetry),
                controls=copy_stream(ev.controls),
                radar=copy_stream(ev.radar),
                tracks=copy_stream(ev.tracks),
                triggers=copy_stream(ev.triggers),
                events=[self.align_event(pid, e) for e in ev.events],
                meta=meta,
            )

    def time(self, pid: str, local_t):
        if local_t is None:
            return None
        model = self.time_alignment["offsets"].get(pid, {})
        if model.get("status") != "ALIGNED":
            raise ValueError("UNRESOLVED_TIME_ALIGNMENT: " + pid)
        return float(model["scale"]) * float(local_t) + float(model["offset_s"])

    def align_evidence(self, pid: str, evidence: Evidence):
        detail = deepcopy(evidence.detail)
        detail.update(
            {
                "participant": pid,
                "local_t_start": evidence.t_start,
                "local_t_end": evidence.t_end,
                "clock_confidence": self.time_alignment["offsets"][pid]["confidence"],
            }
        )
        return replace(
            evidence,
            t_start=self.time(pid, evidence.t_start),
            t_end=self.time(pid, evidence.t_end),
            detail=detail,
        )

    def align_event(self, pid: str, event: Event):
        if any(e.kind == "clock_alignment" for e in event.evidence):
            return event
        model = self.time_alignment["offsets"][pid]
        start, peak, end = [
            self.time(pid, t) for t in (event.t_start, event.t_peak, event.t_end)
        ]
        support = Evidence(
            kind="clock_alignment",
            ref=pid,
            t_start=start,
            t_end=end,
            detail={
                "participant": pid,
                "local_t_start": event.t_start,
                "local_t_peak": event.t_peak,
                "local_t_end": event.t_end,
                "common_t_start": start,
                "common_t_peak": peak,
                "common_t_end": end,
                "clock_confidence": model["confidence"],
                "time_domain": "common",
            },
        )
        return replace(
            event,
            t_start=start,
            t_peak=peak,
            t_end=end,
            values=deepcopy(event.values),
            evidence=[self.align_evidence(pid, e) for e in event.evidence] + [support],
        )

    def align_graph(self, pid: str, graph: GraphDocument):
        if graph.meta.get("time_domain") == "common":
            return graph

        def edge_detail(edge):
            detail = deepcopy(edge.detail)
            for key in ("track_t_start", "track_t_end"):
                if key in detail:
                    detail["local_" + key] = detail[key]
                    detail[key] = self.time(pid, detail[key])
            return detail

        edges = [
            replace(
                e,
                evidence=[self.align_evidence(pid, v) for v in e.evidence],
                detail=edge_detail(e),
            )
            for e in graph.edges
        ]
        meta = deepcopy(graph.meta)
        meta.update(
            {
                "time_domain": "common",
                "time_reference": self.time_alignment["reference"],
            }
        )
        return replace(
            graph,
            nodes=[self.align_event(pid, n) for n in graph.nodes],
            edges=edges,
            meta=meta,
        )
