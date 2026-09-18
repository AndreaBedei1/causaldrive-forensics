"""Assembly of the single JSON document consumed by the static forensic viewer.

Why one document
----------------
The viewer is a static page with no build step, no framework and no server-side
logic: it issues exactly one ``fetch`` and renders whatever comes back.
Everything it needs -- own telemetry, own controls, own radar tracks, events,
both graph families, the fusion association, the checking verdicts and the
privileged ground truth -- therefore has to arrive together. Assembling it here
rather than in the page keeps artifact interpretation in Python, where the
schemas live, and keeps the JavaScript to layout and interaction.

Quarantine
----------
Blending ground truth into a reconstruction is the one thing a forensic viewer
must never do. That is enforced structurally rather than by convention: every
privileged series is read into -- and readable only from -- the top-level
``"oracle"`` block, which carries :data:`PRIVILEGED_WARNING`. No participant or
fusion block has a field capable of holding an oracle series, so the page cannot
mix the two even by mistake. Simulator bookkeeping (CARLA actor ids, lane/road
ids, traffic-light state) is dropped even inside the oracle block: an
investigator needs to know where a vehicle truly was, not how the simulator
numbered it.

This module reads ``oracle/`` artifacts as plain files. It imports nothing from
:mod:`cdf.oracle` and nothing from :mod:`cdf.simulation`, so the viewer layer
cannot pull privileged *code* into a process that only wanted to draw.

Size
----
A run records at 20 Hz for tens of seconds and the bundle is fetched and parsed
before the first frame is drawn. Long series are reduced by a deterministic
stride that always keeps the first and last sample; nothing is interpolated, so
every point the viewer plots is a point that was actually recorded. The stride is
written into the bundle next to the series it applies to, because a reader who
cannot tell a decimated trace from a raw one cannot judge what they are seeing.

Missing artifacts
-----------------
A block whose source files do not exist is omitted, and the omission is recorded
in ``notes`` with the paths that were looked for. Nothing is defaulted or
back-filled: "this run has no counterfactual analysis" and "this run attributes
nothing to anybody" are different statements, and the viewer prints the first one
as such.
"""

from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from ..common.config import Config, repo_root
from ..common.evidence import ParticipantEvidence, load_participant
from ..common.io import read_json, read_jsonl_gz, write_json
from ..common.layout import RunLayout
from ..common.schemas import (
    GraphDocument,
    Provenance,
    SCHEMA_VERSIONS,
    to_jsonable,
)
from ..graph.export import graph_summary, load_graph

__all__ = [
    "PRIVILEGED_WARNING",
    "VIEWER_ASSETS",
    "build_run_bundle",
    "install_viewer_assets",
    "viewer_assets_dir",
    "write_bundle",
]

#: Banner text the viewer must display over every oracle view. Kept here so the
#: page and the bundle cannot drift apart.
PRIVILEGED_WARNING = "PRIVILEGED GROUND TRUTH - EVALUATION ONLY"

#: Static files that make up the viewer page, copied next to ``run_data.json``.
VIEWER_ASSETS: Tuple[str, ...] = ("index.html", "app.js", "styles.css")

#: Default cap on samples per emitted series (``output.viewer_max_samples``).
DEFAULT_MAX_SAMPLES = 1200


# ---------------------------------------------------------------------------
# Top-level assembly
# ---------------------------------------------------------------------------


def build_run_bundle(run_dir: Union[str, Path], cfg: Config) -> Dict[str, Any]:
    """Assemble the viewer document for one run directory.

    Parameters
    ----------
    run_dir:
        A ``seed_xxx`` run directory as produced by the simulation and analysis
        pipelines.
    cfg:
        Resolved configuration. Only ``output.viewer_max_samples`` (series size
        cap) and ``indicators.conflict.region_radius_m`` (drawn conflict region)
        are read; both have defaults, so a bare configuration still works.

    Returns
    -------
    dict
        A JSON-serialisable document. Blocks whose source artifacts are absent
        are omitted and listed in ``notes``.

    Raises
    ------
    FileNotFoundError
        If ``run_dir`` does not exist, or contains no ``vehicle_*`` directory --
        both of which mean the caller pointed at something that is not a run.
    """
    layout = RunLayout.from_run_dir(run_dir)
    if not layout.root.exists():
        raise FileNotFoundError("run directory does not exist: {0}".format(layout.root))
    participant_ids = layout.participant_ids()
    if not participant_ids:
        raise FileNotFoundError(
            "no vehicle_* directory under {0}; this is not a run directory".format(layout.root)
        )

    max_samples = int(cfg.get("output.viewer_max_samples", DEFAULT_MAX_SAMPLES))
    notes: List[Dict[str, Any]] = []

    participants: Dict[str, Any] = {}
    for pid in participant_ids:
        participants[pid] = _participant_block(layout, pid, max_samples)

    bundle: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSIONS["viewer"],
        "run": _run_block(layout, participants, cfg, notes),
        "sampling": {
            "max_samples": max_samples,
            "policy": (
                "stride decimation; first and last sample always kept; "
                "no interpolation, every emitted point was recorded"
            ),
        },
        "params": {
            "conflict_region_radius_m": float(
                cfg.get("indicators.conflict.region_radius_m", 6.0)
            ),
            "ttc_critical_s": float(cfg.get("indicators.ttc.critical_s", 1.5)),
            "config_hash": cfg.hash,
        },
        "participants": participants,
    }

    fusion = _fusion_block(layout, notes)
    if fusion is not None:
        bundle["fusion"] = fusion

    oracle = _oracle_block(layout, max_samples, notes)
    if oracle is not None:
        bundle["oracle"] = oracle

    checking = _checking_block(layout, notes)
    if checking is not None:
        bundle["checking"] = checking

    counterfactual = _counterfactual_block(layout, notes)
    if counterfactual is not None:
        bundle["counterfactual"] = counterfactual

    evaluation = _evaluation_block(layout, notes)
    if evaluation is not None:
        bundle["evaluation"] = evaluation

    ablation_path = layout.evaluation_dir / "method_ablation.json"
    if ablation_path.exists():
        bundle.setdefault("evaluation", {})["method_ablation"] = read_json(ablation_path)

    # --- V2 blocks --------------------------------------------------------
    # Each is omitted when its artifact is absent, and the absence is noted
    # rather than silently producing an empty panel: a viewer that renders a
    # blank Responsibility tab looks the same whether nothing was found or
    # nothing was run.
    # The ground truth the graph toggle compares against is the *observable*
    # one, not the scenario template: the template asserts scripted actions no
    # reconstruction can emit, so a diff against it would show a wall of
    # unmatchable nodes and tell the reader nothing about the reconstruction.
    if layout.observable_causal_graph.exists():
        bundle.setdefault("oracle", {})["observable_causal_graph"] = read_json(
            layout.observable_causal_graph
        )
    else:
        notes.append({
            "block": "oracle.observable_causal_graph",
            "reason": (
                "no observable ground truth; the graph toggle will offer the "
                "scenario design reference instead, which is not comparable "
                "node-for-node"
            ),
        })
    if layout.graph_diff.exists():
        bundle.setdefault("evaluation", {})["graph_diff"] = read_json(
            layout.graph_diff
        )

    logs = _logs_block(layout, participant_ids, notes)
    if logs is not None:
        bundle["logs"] = logs

    formal = _formal_block(layout, notes)
    if formal is not None:
        bundle["formal"] = formal

    responsibility = _responsibility_block(layout, notes)
    if responsibility is not None:
        bundle["responsibility"] = responsibility

    video = _video_block(layout, participant_ids, notes)
    if video is not None:
        bundle["video"] = video

    bundle["notes"] = notes
    # to_jsonable also maps NaN/Inf to null, which json.dump(allow_nan=False)
    # would otherwise refuse -- a single bad float must not lose the whole run.
    return to_jsonable(bundle)


def write_bundle(run_dir: Union[str, Path], cfg: Config) -> Path:
    """Build the bundle and write it to ``<run_dir>/viewer/run_data.json``.

    The static page is copied next to the bundle (unless
    ``output.viewer_copy_assets`` is false) because the page fetches
    ``run_data.json`` *relative to itself*: a viewer directory holding only data
    is not openable, and a page that lives elsewhere cannot find the data.
    """
    layout = RunLayout.from_run_dir(run_dir)
    bundle = build_run_bundle(run_dir, cfg)
    path = write_json(layout.viewer_bundle, bundle)
    if bool(cfg.get("output.viewer_copy_assets", True)):
        install_viewer_assets(layout.viewer_dir)
    return path


def viewer_assets_dir() -> Path:
    """Directory of the static viewer page shipped with the repository."""
    return repo_root() / "viewer"


def install_viewer_assets(dest_dir: Union[str, Path]) -> List[Path]:
    """Copy ``index.html``/``app.js``/``styles.css`` into ``dest_dir``.

    Raises loudly when an asset is missing: a viewer directory containing data
    but no page looks like a successful export and is not one.
    """
    src = viewer_assets_dir()
    missing = [name for name in VIEWER_ASSETS if not (src / name).exists()]
    if missing:
        raise FileNotFoundError(
            "viewer asset(s) {0} not found under {1}; the static viewer page is "
            "part of the repository and must be present to export a run".format(
                ", ".join(missing), src
            )
        )
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    out: List[Path] = []
    for name in VIEWER_ASSETS:
        target = dest / name
        shutil.copyfile(str(src / name), str(target))
        out.append(target)
    return out


# ---------------------------------------------------------------------------
# Run header
# ---------------------------------------------------------------------------


def _run_block(
    layout: RunLayout,
    participants: Dict[str, Any],
    cfg: Config,
    notes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Run identity and time base, taken from the manifest where available.

    The timeline bounds are recomputed from the emitted telemetry rather than
    copied from the manifest, so the slider can never address a time for which
    the bundle carries no sample.
    """
    manifest: Dict[str, Any] = {}
    if layout.manifest.exists():
        manifest = read_json(layout.manifest)
    else:
        notes.append(
            _note(
                "run.manifest",
                "manifest.json is missing; run identity and outcome are unknown",
                [layout.manifest],
            )
        )

    starts = [p["t_start"] for p in participants.values() if p["t_start"] is not None]
    ends = [p["t_end"] for p in participants.values() if p["t_end"] is not None]
    t_start = min(starts) if starts else 0.0
    t_end = max(ends) if ends else 0.0

    dt = manifest.get("fixed_delta_seconds")
    if dt is None:
        dt = cfg.get("simulation.fixed_delta_seconds", 0.05)

    return {
        "run_id": manifest.get("run_id", layout.root.name),
        "scenario_id": manifest.get("scenario_id", ""),
        "variant": manifest.get("variant", ""),
        "seed": manifest.get("seed"),
        "map": manifest.get("map_name", ""),
        "outcome": manifest.get("outcome"),
        "duration_s": manifest.get("duration_sim_s", t_end - t_start),
        "dt": float(dt),
        "n_frames": manifest.get("n_frames"),
        "config_hash": manifest.get("config_hash", cfg.hash),
        "participant_ids": sorted(participants.keys()),
        "t_start": t_start,
        "t_end": t_end,
        "run_dir": layout.root.name,
    }


# ---------------------------------------------------------------------------
# Participants (local reconstruction)
# ---------------------------------------------------------------------------


def _participant_block(layout: RunLayout, pid: str, max_samples: int) -> Dict[str, Any]:
    """One participant's own evidence and own reconstruction.

    Radar *detections* are deliberately not loaded: the viewer draws tracks, and
    the raw point cloud is by far the largest artifact in a run.
    """
    ev: ParticipantEvidence = load_participant(layout, pid, with_radar=False)
    notes: List[Dict[str, Any]] = []
    sampling: Dict[str, Any] = {}

    telemetry, sampling["telemetry"] = _decimate(
        [
            {
                "t": float(s.t),
                "x": float(s.x),
                "y": float(s.y),
                "yaw": float(s.yaw),
                "speed": float(s.speed),
                "accel_long": float(s.accel_long),
            }
            for s in ev.telemetry
        ],
        max_samples,
    )
    controls, sampling["controls"] = _decimate(
        [
            {
                "t": float(s.t),
                "throttle": float(s.throttle),
                "brake": float(s.brake),
                "steer": float(s.steer),
            }
            for s in ev.controls
        ],
        max_samples,
    )

    tracks: Dict[str, List[Dict[str, Any]]] = {}
    track_sampling: Dict[str, Any] = {}
    for track_id, samples in sorted(ev.tracks_by_id().items()):
        rows, meta = _decimate(
            [
                {
                    "t": float(s.t),
                    "gx": float(s.gx),
                    "gy": float(s.gy),
                    "range_m": float(s.range_m),
                    "ttc": None if s.ttc is None else float(s.ttc),
                    "confidence": float(s.confidence),
                }
                for s in samples
            ],
            max_samples,
        )
        tracks[track_id] = rows
        track_sampling[track_id] = meta
    sampling["tracks"] = track_sampling

    if not ev.telemetry:
        notes.append(
            _note(
                "participants.{0}.telemetry".format(pid),
                "no telemetry recorded for participant {0}".format(pid),
                [layout.telemetry(pid)],
            )
        )

    span = ev.span()
    block: Dict[str, Any] = {
        "participant_id": pid,
        "telemetry": telemetry,
        "controls": controls,
        "tracks": tracks,
        "events": [to_jsonable(e) for e in ev.events],
        "triggers": [to_jsonable(t) for t in ev.triggers],
        "summary": ev.summary(),
        "sampling": sampling,
        "t_start": span[0] if span else None,
        "t_end": span[1] if span else None,
        "notes": notes,
    }

    causal = _maybe_graph(layout.causal_graph(pid), Provenance.LOCAL, notes, "participants.{0}.causal_graph".format(pid))
    if causal is not None:
        block["causal_graph"] = causal
    event_graph = _maybe_graph(layout.event_graph(pid), Provenance.LOCAL, notes, "participants.{0}.event_graph".format(pid))
    if event_graph is not None:
        block["event_graph"] = event_graph
    return block


# ---------------------------------------------------------------------------
# Fusion
# ---------------------------------------------------------------------------


def _fusion_block(layout: RunLayout, notes: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """The fused reconstruction: graphs, track association, diagnostics digest.

    The full diagnostics artifact is a debugging record, not a display record, so
    only the parts a reader can act on are carried over -- the association
    outcome per track, what fusion merged, and whether the fused graph is still
    acyclic.
    """
    paths = [
        layout.fused_causal_graph,
        layout.fused_event_graph,
        layout.association_report,
        layout.fusion_diagnostics,
    ]
    if not any(p.exists() for p in paths):
        notes.append(
            _note("fusion", "no fusion artifacts in this run", paths)
        )
        return None

    inner: List[Dict[str, Any]] = []
    block: Dict[str, Any] = {"notes": inner}

    causal = _maybe_graph(layout.fused_causal_graph, Provenance.FUSED, inner, "fusion.causal_graph")
    if causal is not None:
        block["causal_graph"] = causal
    event_graph = _maybe_graph(layout.fused_event_graph, Provenance.FUSED, inner, "fusion.event_graph")
    if event_graph is not None:
        block["event_graph"] = event_graph

    if layout.association_report.exists():
        report = read_json(layout.association_report)
        block["association"] = [
            _projected_assignment(a) for a in report.get("assignments", [])
        ]
        block["association_counts"] = report.get("counts", {})
        block["association_thresholds"] = report.get("thresholds", {})
    else:
        block["association"] = []
        inner.append(
            _note(
                "fusion.association",
                "association report missing; reconstructed identities unavailable",
                [layout.association_report],
            )
        )

    if layout.fusion_diagnostics.exists():
        block["diagnostics_summary"] = _diagnostics_summary(
            read_json(layout.fusion_diagnostics)
        )
    else:
        inner.append(
            _note(
                "fusion.diagnostics_summary",
                "fusion diagnostics missing",
                [layout.fusion_diagnostics],
            )
        )

    # What fusion concluded, in the terms a reader asks in: what happened, in
    # what order, through which chain, and whose behaviour sits at the root of
    # it. The graph is the evidence for this; this is the answer.
    if layout.incident_reconstruction.exists():
        block["reconstruction"] = read_json(layout.incident_reconstruction)
    else:
        inner.append(
            _note(
                "fusion.reconstruction",
                "no incident reconstruction; the viewer can show the graph but "
                "not the account derived from it",
                [layout.incident_reconstruction],
            )
        )
    if layout.causal_attribution.exists():
        block["graph_attribution"] = read_json(layout.causal_attribution)
    else:
        inner.append(
            _note(
                "fusion.graph_attribution",
                "no graph-derived attribution hypothesis",
                [layout.causal_attribution],
            )
        )

    alignment_path = layout.fusion_dir / "time_alignment.json"
    if alignment_path.exists():
        block["clock"] = _clock_block(read_json(alignment_path))
    else:
        inner.append(
            _note(
                "fusion.clock",
                "no time alignment; the common timeline is unexplained",
                [alignment_path],
            )
        )
    return block


def _clock_block(alignment: Dict[str, Any]) -> Dict[str, Any]:
    """How each recorder's own clock was placed on the common timeline.

    Every timestamp the viewer shows outside a vehicle's own panel has been
    through this transform, so a reader must be able to see it: which recorder
    is the gauge, what scale and offset each other one was given, how well it
    fitted, and on what evidence. An estimate presented without its residual is
    an assertion.
    """
    offsets = alignment.get("offsets") or {}
    rows = []
    for pid in sorted(offsets):
        entry = offsets[pid] or {}
        rows.append(
            {
                "participant_id": pid,
                "is_reference": bool(entry.get("is_reference")),
                "scale": entry.get("scale"),
                "offset_s": entry.get("offset_s"),
                "residual_s": entry.get("residual"),
                "confidence": entry.get("confidence"),
                "status": entry.get("status"),
                "drift_ppm": entry.get("drift_ppm"),
                "drift_status": entry.get("drift_status"),
                "method": entry.get("method"),
                "methods": list(entry.get("methods") or []),
                "n_constraints": entry.get("n_constraints"),
                "n_samples": entry.get("n_samples"),
            }
        )
    return {
        "reference": alignment.get("reference"),
        "reference_rule": alignment.get("reference_rule"),
        "formula": alignment.get("formula"),
        "common_span": alignment.get("common_span"),
        "participants": rows,
        "note": (
            "each recorder kept its own clock; these are the estimated "
            "transforms onto the common timeline, fitted from shared "
            "observations alone"
        ),
    }


def _projected_assignment(a: Dict[str, Any]) -> Dict[str, Any]:
    """One track-association verdict, with the numbers that justify it.

    ``status`` and ``confidence`` travel together on purpose: the viewer is
    required to render an uncertain identity *as* uncertain, and it can only do
    that if the evidence for the claim is next to the claim.
    """
    return {
        "track_id": a.get("track_id"),
        "observer_id": a.get("observer_id"),
        "assigned_participant": a.get("assigned_participant"),
        "confidence": a.get("confidence"),
        "status": a.get("status"),
        "rmse_m": a.get("rmse_m"),
        "overlap_s": a.get("overlap_s"),
        "runner_up": a.get("runner_up"),
        "runner_up_margin": a.get("runner_up_margin"),
        "reason": a.get("reason", ""),
        "candidates": [
            {
                "participant_id": c.get("participant_id"),
                "score": c.get("score"),
                "rmse_m": c.get("rmse_m"),
                "overlap_s": c.get("overlap_s"),
                "n_samples": c.get("n_samples"),
            }
            for c in a.get("candidates", [])
        ],
    }


def _diagnostics_summary(diag: Dict[str, Any]) -> Dict[str, Any]:
    """Display-sized digest of ``fusion_diagnostics.json``."""
    alignment = diag.get("time_alignment", {}) or {}
    added = diag.get("fusion_added", {}) or {}
    return {
        "n_fused_nodes": diag.get("n_fused_nodes"),
        "n_fused_edges": diag.get("n_fused_edges"),
        "n_input_nodes": diag.get("n_input_nodes", {}),
        "n_input_edges": diag.get("n_input_edges", {}),
        "n_alignment_groups": diag.get("n_alignment_groups"),
        "n_merged_groups": diag.get("n_merged_groups"),
        "merged_groups": diag.get("merged_groups", []),
        "subject_map": diag.get("subject_map", {}),
        "unresolved_tracks": diag.get("unresolved_tracks", []),
        "contradictions": diag.get("contradictions", []),
        "dag": diag.get("dag", {}),
        "participants": diag.get("participants", []),
        "time_alignment": {
            "reference": alignment.get("reference"),
            "grid_dt": alignment.get("grid_dt"),
            "common_span": alignment.get("common_span"),
            "offsets": alignment.get("offsets", {}),
        },
        "fusion_added": {
            "nodes": added.get("nodes"),
            "edges": added.get("edges"),
            "n_bridged_paths": added.get("n_bridged_paths"),
            "criterion": added.get("criterion", ""),
        },
        "alignment_diagnostics": diag.get("alignment_diagnostics", []),
    }


# ---------------------------------------------------------------------------
# Oracle (privileged, quarantined)
# ---------------------------------------------------------------------------


def _oracle_block(
    layout: RunLayout, max_samples: int, notes: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Ground truth, in the only block of the bundle allowed to hold it.

    Simulator identities are stripped on the way in (actor ids, lane/road ids,
    traffic-light state): they are how the simulator bookkeeps, not what a
    reconstruction is scored against, and leaving them out means no consumer of
    this bundle can accidentally key on them.
    """
    # The summary has no RunLayout accessor of its own; it is written next to the
    # trace by cdf.oracle.logger and named here so the path stays in one place.
    summary_path = layout.oracle_dir / "oracle_summary.json"
    paths = [
        layout.oracle_trace,
        summary_path,
        layout.oracle_events,
        layout.oracle_causal_graph,
    ]
    if not any(p.exists() for p in paths):
        notes.append(_note("oracle", "no oracle artifacts in this run", paths))
        return None

    inner: List[Dict[str, Any]] = []
    block: Dict[str, Any] = {
        "_warning": PRIVILEGED_WARNING,
        "notes": inner,
    }

    trajectories: Dict[str, List[Dict[str, Any]]] = {}
    sampling: Dict[str, Any] = {}
    if layout.oracle_trace.exists():
        raw: Dict[str, List[Dict[str, Any]]] = {}
        for frame in read_jsonl_gz(layout.oracle_trace):
            t = float(frame.get("t", 0.0))
            for actor in frame.get("actors", []) or []:
                pid = actor.get("participant_id")
                if pid is None:
                    continue
                raw.setdefault(str(pid), []).append(
                    {
                        "t": t,
                        "x": float(actor.get("x", 0.0)),
                        "y": float(actor.get("y", 0.0)),
                        "yaw": float(actor.get("yaw", 0.0)),
                        "speed": float(actor.get("speed", 0.0)),
                    }
                )
        for pid in sorted(raw):
            rows = sorted(raw[pid], key=lambda r: r["t"])
            trajectories[pid], sampling[pid] = _decimate(rows, max_samples)
    else:
        inner.append(
            _note("oracle.trajectories", "oracle trace missing", [layout.oracle_trace])
        )
    block["trajectories"] = trajectories
    block["sampling"] = sampling

    collisions: List[Dict[str, Any]] = []
    if summary_path.exists():
        summary = read_json(summary_path)
        for c in summary.get("collisions", []) or []:
            collisions.append(
                {
                    "t": c.get("t"),
                    "participant_id": c.get("participant_id"),
                    "other_participant_id": c.get("other_participant_id"),
                    "impulse": c.get("impulse"),
                    "is_participant_pair": c.get("is_participant_pair"),
                }
            )
        block["summary"] = {
            "run_id": summary.get("run_id", ""),
            "scenario_id": summary.get("scenario_id", ""),
            "seed": summary.get("seed"),
            "variant": summary.get("variant", ""),
            "map": summary.get("map_name", ""),
            "n_frames": summary.get("n_frames"),
            "participants": summary.get("participants", []),
            "collision_pairs": summary.get("collision_pairs", []),
            "interventions": summary.get("interventions", {}),
            "notes": summary.get("notes", []),
        }
    else:
        inner.append(
            _note("oracle.summary", "oracle summary missing", [summary_path])
        )
    block["collisions"] = collisions

    if layout.oracle_events.exists():
        payload = read_json(layout.oracle_events)
        block["events"] = payload.get("events", [])
    else:
        block["events"] = []
        inner.append(
            _note("oracle.events", "oracle events missing", [layout.oracle_events])
        )

    causal = _maybe_graph(
        layout.oracle_causal_graph, Provenance.ORACLE, inner, "oracle.causal_graph"
    )
    if causal is not None:
        block["causal_graph"] = causal
    return block


# ---------------------------------------------------------------------------
# Checking / counterfactual / evaluation
# ---------------------------------------------------------------------------


def _checking_block(layout: RunLayout, notes: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Property verdicts and, for each ``FAIL``, the trace that shows it."""
    paths = [layout.model_check_results, layout.counterexamples]
    if not any(p.exists() for p in paths):
        notes.append(_note("checking", "no model-checking artifacts in this run", paths))
        return None

    inner: List[Dict[str, Any]] = []
    block: Dict[str, Any] = {"notes": inner}

    if layout.model_check_results.exists():
        results = read_json(layout.model_check_results)
        block["results"] = results.get("results", [])
        block["properties"] = results.get("properties", [])
        block["summary"] = results.get("summary", {})
        block["by_participant"] = results.get("by_participant", {})
        block["by_property"] = results.get("by_property", {})
    else:
        block["results"] = []
        inner.append(
            _note("checking.results", "model-check results missing", [layout.model_check_results])
        )

    if layout.counterexamples.exists():
        payload = read_json(layout.counterexamples)
        by_ref = payload.get("counterexamples", {}) or {}
        # Emitted as a list so the page can iterate; the ref stays inside each
        # entry, which is what links a counterexample back to its verdict.
        block["counterexamples"] = [by_ref[ref] for ref in sorted(by_ref)]
        block["counterexample_index"] = payload.get("index", [])
        block["counterexamples_skipped"] = payload.get("skipped", [])
    else:
        block["counterexamples"] = []
        inner.append(
            _note("checking.counterexamples", "counterexample report missing", [layout.counterexamples])
        )
    return block


def _counterfactual_block(
    layout: RunLayout, notes: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Intervention replays and the causal contribution they support."""
    paths = [
        layout.counterfactual_manifest,
        layout.causal_contribution,
        layout.intervention_results,
    ]
    if not any(p.exists() for p in paths):
        notes.append(
            _note("counterfactual", "no counterfactual artifacts in this run", paths)
        )
        return None

    inner: List[Dict[str, Any]] = []
    block: Dict[str, Any] = {"notes": inner}
    if layout.counterfactual_manifest.exists():
        block["manifest"] = read_json(layout.counterfactual_manifest)
    else:
        inner.append(
            _note(
                "counterfactual.manifest",
                "counterfactual manifest missing",
                [layout.counterfactual_manifest],
            )
        )
    if layout.causal_contribution.exists():
        block["contribution"] = read_json(layout.causal_contribution)
    else:
        inner.append(
            _note(
                "counterfactual.contribution",
                "causal contribution missing; attribution is undetermined",
                [layout.causal_contribution],
            )
        )
    if layout.intervention_results.exists():
        block["interventions"] = _read_csv(layout.intervention_results)
    else:
        block["interventions"] = []
        inner.append(
            _note(
                "counterfactual.interventions",
                "intervention results missing",
                [layout.intervention_results],
            )
        )
    return block


def _evaluation_block(layout: RunLayout, notes: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Scores of the reconstruction against ground truth.

    Evaluation compares the two sides, so its artifacts are neither local nor
    privileged; they are carried as computed and never merged into either view.
    """
    paths = [
        layout.metrics,
        layout.attribution_metrics,
        layout.event_matches,
        layout.edge_matches,
    ]
    if not any(p.exists() for p in paths):
        notes.append(_note("evaluation", "no evaluation artifacts in this run", paths))
        return None

    inner: List[Dict[str, Any]] = []
    block: Dict[str, Any] = {"notes": inner}
    if layout.metrics.exists():
        block["metrics"] = read_json(layout.metrics)
    else:
        inner.append(_note("evaluation.metrics", "metrics missing", [layout.metrics]))
    if layout.attribution_metrics.exists():
        block["attribution"] = read_json(layout.attribution_metrics)
    else:
        inner.append(
            _note(
                "evaluation.attribution",
                "attribution metrics missing",
                [layout.attribution_metrics],
            )
        )
    block["event_matches"] = (
        _read_csv(layout.event_matches) if layout.event_matches.exists() else []
    )
    block["edge_matches"] = (
        _read_csv(layout.edge_matches) if layout.edge_matches.exists() else []
    )
    return block


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _decimate(
    rows: Sequence[Any], max_samples: int
) -> Tuple[List[Any], Dict[str, Any]]:
    """Reduce ``rows`` to at most ``max_samples`` by a fixed stride.

    Both endpoints are preserved: a trajectory that stops short of the collision
    because its last sample was dropped would be actively misleading. When the
    stride alone would leave the final sample out, it replaces the last kept
    index rather than being appended, so the cap is never exceeded.

    Returns the emitted rows and a record of what was done to them.
    """
    n = len(rows)
    if int(max_samples) < 2:
        raise ValueError(
            "output.viewer_max_samples must be >= 2, got {0}".format(max_samples)
        )
    if n <= int(max_samples):
        return list(rows), {
            "n_source": n,
            "n_emitted": n,
            "stride": 1,
            "decimated": False,
        }
    stride = int(math.ceil(float(n) / float(max_samples)))
    idx = list(range(0, n, stride))
    if idx[-1] != n - 1:
        if len(idx) >= int(max_samples):
            idx[-1] = n - 1
        else:
            idx.append(n - 1)
    return [rows[i] for i in idx], {
        "n_source": n,
        "n_emitted": len(idx),
        "stride": stride,
        "decimated": True,
    }


def _maybe_graph(
    path: Path,
    expect_scope: Provenance,
    notes: List[Dict[str, Any]],
    block_name: str,
) -> Optional[Dict[str, Any]]:
    """Load and project a graph document, or record that it is absent.

    ``expect_scope`` is passed through to :func:`cdf.graph.export.load_graph`, so
    a graph filed in the wrong place raises here instead of being rendered under
    the wrong badge.
    """
    if not path.exists():
        notes.append(_note(block_name, "graph artifact missing", [path]))
        return None
    return _project_graph(load_graph(path, expect_scope=expect_scope))


def _project_graph(doc: GraphDocument) -> Dict[str, Any]:
    """Display projection of a graph document.

    Per-node and per-edge evidence lists are replaced by their references: the
    viewer shows *which* records support a claim and lets the reader open them in
    the run directory, whereas inlining every evidence payload would more than
    double the bundle for information no panel displays.
    """
    nodes: List[Dict[str, Any]] = []
    for n in doc.nodes:
        nodes.append(
            {
                "event_id": n.event_id,
                "event_type": _enum_value(n.event_type),
                "participant_id": n.participant_id,
                "subject": n.subject,
                "t_start": float(n.t_start),
                "t_peak": float(n.t_peak),
                "t_end": None if n.t_end is None else float(n.t_end),
                "confidence": float(n.confidence),
                "provenance": _enum_value(n.provenance),
                "owners": list(n.owners),
                "values": dict(n.values),
                "source_sensors": list(n.source_sensors),
                "merged_from": list(n.merged_from),
                "evidence_refs": [e.ref for e in n.evidence],
            }
        )
    edges: List[Dict[str, Any]] = []
    for e in doc.edges:
        edges.append(
            {
                "source": e.source,
                "target": e.target,
                "edge_type": e.edge_type,
                "confidence": float(e.confidence),
                "provenance": _enum_value(e.provenance),
                "rule": e.rule,
                "temporal_relation": e.temporal_relation,
                "owners": list(e.owners),
                "detail": dict(e.detail),
                "evidence_refs": [ev.ref for ev in e.evidence],
            }
        )
    return {
        "graph_kind": doc.graph_kind,
        "scope": _enum_value(doc.scope),
        "owner": doc.owner,
        "run_id": doc.run_id,
        "scenario_id": doc.scenario_id,
        "seed": doc.seed,
        "nodes": nodes,
        "edges": edges,
        "meta": dict(doc.meta),
        "summary": graph_summary(doc),
    }


def _enum_value(value: Any) -> str:
    """String value of an enum-or-string field."""
    return value.value if hasattr(value, "value") else str(value)


def _read_csv(path: Path) -> List[Dict[str, Any]]:
    """Read a CSV artifact into row dicts, preserving column order."""
    with open(str(path), "r", encoding="utf-8", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def _note(block: str, message: str, paths: Sequence[Path]) -> Dict[str, Any]:
    """A recorded omission: which block, why, and what was looked for."""
    return {
        "block": block,
        "status": "missing",
        "message": message,
        "paths": [Path(p).name for p in paths],
    }

# ---------------------------------------------------------------------------
# V2 blocks
# ---------------------------------------------------------------------------


def _logs_block(
    layout: RunLayout,
    participant_ids: Sequence[str],
    notes: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """The readable tables: each vehicle's own account, and the merged one.

    Rows are passed through whole rather than summarised. They are already the
    summary -- that is what the log is for -- and a viewer that re-derived them
    could disagree with the artifact, which is the one thing a viewer must never
    do.
    """
    per_participant: Dict[str, Any] = {}
    for pid in participant_ids:
        path = layout.local_log(pid)
        if path.exists():
            per_participant[pid] = read_json(path)

    global_log = None
    if layout.global_log.exists():
        global_log = read_json(layout.global_log)

    if not per_participant and global_log is None:
        notes.append({
            "block": "logs",
            "reason": (
                "no local_log.json or global_log.json; this run predates the "
                "log-first pipeline, or the analysis stage has not been run"
            ),
        })
        return None

    if global_log is None:
        notes.append({
            "block": "logs.global",
            "reason": (
                "no merged log: fusion has not been run, so only the separate "
                "local timelines are available"
            ),
        })
    return {"local": per_participant, "global": global_log}


def _formal_block(
    layout: RunLayout, notes: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Property verdicts, with the formulae that produced them."""
    if not layout.formal_results.exists():
        notes.append({
            "block": "formal",
            "reason": "no formal/results.json; the property checker has not run",
        })
        return None
    out = {"results": read_json(layout.formal_results)}
    if layout.formal_properties.exists():
        out["properties"] = read_json(layout.formal_properties)
    return out


def _responsibility_block(
    layout: RunLayout, notes: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """The normative account, graph and per-participant findings."""
    if not layout.responsibility_report.exists():
        notes.append({
            "block": "responsibility",
            "reason": (
                "no fusion/responsibility_report.json; the normative layer has "
                "not run for this run"
            ),
        })
        return None
    out = {"report": read_json(layout.responsibility_report)}
    if layout.responsibility_graph.exists():
        out["graph"] = read_json(layout.responsibility_graph)
    return out


def _video_block(
    layout: RunLayout,
    participant_ids: Sequence[str],
    notes: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Where each vehicle's clip is, and which frame each instant maps to.

    Only the index travels in the bundle; the video itself stays on disk and is
    referenced by relative path. A bundle that embedded 20 MB of frames per
    vehicle would be unopenable for no benefit.
    """
    per_participant: Dict[str, Any] = {}
    for pid in participant_ids:
        index_path = layout.frame_index(pid)
        if not index_path.exists():
            continue
        index = read_json(index_path)
        video = layout.front_video(pid)
        per_participant[pid] = {
            "frame_index": index,
            "video_path": (
                video.relative_to(layout.root).as_posix() if video.exists() else None
            ),
            "available": video.exists(),
        }

    if not per_participant:
        notes.append({
            "block": "video",
            "reason": (
                "no camera artifacts; this run was recorded without a camera, "
                "which is a supported configuration"
            ),
        })
        return None

    missing = sorted(p for p, v in per_participant.items() if not v["available"])
    if missing:
        notes.append({
            "block": "video",
            "reason": (
                "frame index present but no video file for {0}; the clip was "
                "buffered and not encoded".format(", ".join(missing))
            ),
        })
    return {"per_participant": per_participant}
