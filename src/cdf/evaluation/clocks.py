"""Clock ground-truth access and scoring, exclusively on the evaluation side."""

from copy import deepcopy
from dataclasses import replace
from ..common.evidence import RunEvidence
from ..common.io import read_json


def load_clock_truth(layout):
    path = layout.oracle_dir / "clock_ground_truth.json"
    return read_json(path).get("participants", {}) if path.exists() else {}


def map_event(event, a, b):
    def time(t):
        return None if t is None else a * float(t) + b

    return replace(
        event,
        t_start=time(event.t_start),
        t_peak=time(event.t_peak),
        t_end=time(event.t_end),
        evidence=[
            replace(
                e,
                t_start=time(e.t_start),
                t_end=time(e.t_end),
                detail=deepcopy(e.detail),
            )
            for e in event.evidence
        ],
    )


def map_graph(graph, a, b):
    if graph is None:
        return None

    def time(t):
        return None if t is None else a * float(t) + b

    return replace(
        graph,
        nodes=[map_event(n, a, b) for n in graph.nodes],
        edges=[
            replace(
                e,
                evidence=[
                    replace(v, t_start=time(v.t_start), t_end=time(v.t_end))
                    for v in e.evidence
                ],
            )
            for e in graph.edges
        ],
    )


def simulator_evidence(run, truth):
    """Evaluation copy in physical time for privileged track-identity scoring."""
    participants = {}
    for pid, ev in run.participants.items():
        profile = truth.get(pid)
        if not profile:
            participants[pid] = ev
            continue
        a = 1 / float(profile["true_scale"])
        b = -float(profile["true_offset_s"]) * a

        def stream(s):
            return [replace(v, t=a * v.t + b) for v in s]

        participants[pid] = replace(
            ev,
            telemetry=stream(ev.telemetry),
            controls=stream(ev.controls),
            radar=stream(ev.radar),
            tracks=stream(ev.tracks),
            triggers=stream(ev.triggers),
            events=[map_event(e, a, b) for e in ev.events],
            meta={**ev.meta, "time_domain": "synchronized_baseline"},
        )
    return RunEvidence(
        run.run_dir,
        {**run.manifest, "clock_protocol": "synchronized_clock_baseline"},
        participants,
    )


def evaluate_clock_alignment(alignment, truth):
    reference = alignment.get("reference")
    ref = truth.get(reference)
    if ref is None:
        return None
    rows = []
    for pid, profile in sorted(truth.items()):
        model = alignment.get("offsets", {}).get(pid, {})
        a = float(ref["true_scale"]) / float(profile["true_scale"])
        b = float(ref["true_offset_s"]) - a * float(profile["true_offset_s"])
        resolved = model.get("status") == "ALIGNED"
        rows.append(
            {
                "participant": pid,
                "status": model.get("status", "UNRESOLVED_TIME_ALIGNMENT"),
                "true_relative_scale": a,
                "true_relative_offset_s": b,
                "offset_error_s": float(model["offset_s"]) - b if resolved else None,
                "drift_error_ppm": (
                    (float(model["scale"]) - a) * 1e6 if resolved else None
                ),
                "confidence": model.get("confidence", 0.0),
            }
        )
    measured = [
        r
        for r in rows
        if r["participant"] != reference and r["offset_error_s"] is not None
    ]

    def mean(key):
        return sum(abs(r[key]) for r in measured) / len(measured) if measured else None

    residuals = [h["residual"] for h in alignment.get("constraints", [])]
    return {
        "reference": reference,
        "participants": rows,
        "n_resolved": sum(r["offset_error_s"] is not None for r in rows),
        "mean_abs_offset_error_s": mean("offset_error_s"),
        "mean_abs_drift_error_ppm": mean("drift_error_ppm"),
        "alignment_residual": sum(residuals) / len(residuals) if residuals else None,
        "time_gauge": "reference recorder; absolute simulator clock is evaluation-only",
    }
