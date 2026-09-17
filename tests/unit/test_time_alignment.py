"""Physical-evidence synchronization tests; periodic grids are not anchors."""

from dataclasses import replace
from pathlib import Path
import math
import numpy as np
import pytest
from cdf.common.config import load_run_config
from cdf.common.evidence import ParticipantEvidence, RunEvidence
from cdf.common.schemas import (
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    LocalTriggerRecord,
    Provenance,
    TelemetrySample,
    TrackSample,
    TriggerKind,
)
from cdf.fusion.time_alignment import (
    align_participants,
    estimate_track_clock,
    apply_offset,
)
from cdf.fusion.aligned_evidence import AlignedRunEvidence
from cdf.fusion.track_association import associate_tracks
from cdf.fusion.event_alignment import align_events
from cdf.fusion.graph_fusion import fuse_graphs


def physical_run(profiles=None, chain=False, span=10.0, jitter=0.0, dropout=False):
    profiles = profiles or {"A": (0.0, 1.0), "B": (0.0, 1.0)}
    ts = np.arange(0, span + 0.01, 0.05)
    participants = {}
    truth = {}
    rng = np.random.RandomState(21)
    for i, (pid, (offset, scale)) in enumerate(profiles.items()):
        x = 20 * i + (7 + 2 * i) * ts + 1.5 * np.sin(0.6 * ts + i)
        y = 4 * i + np.sin(0.3 * ts + i)
        vx = (7 + 2 * i) + 0.9 * np.cos(0.6 * ts + i)
        vy = 0.3 * np.cos(0.3 * ts + i)
        local = scale * ts + offset + rng.normal(0, jitter, len(ts))
        telemetry = [
            TelemetrySample(
                float(t),
                10000 * i + k,
                pid,
                float(px),
                float(py),
                0.0,
                0.0,
                vx=float(vx[k]),
                vy=float(vy[k]),
                speed=float(math.hypot(vx[k], vy[k])),
            )
            for k, (t, px, py) in enumerate(zip(local, x, y))
        ]
        participants[pid] = ParticipantEvidence(
            pid, telemetry=telemetry, meta={"time_domain": "participant_local"}
        )
        truth[pid] = (x, y, vx, vy)
    pairs = [("A", "B")] + ([("B", "C")] if chain else [])
    for obs, cand in pairs:
        own = participants[obs]
        gx, gy, gvx, gvy = truth[cand]
        ox, oy, ovx, ovy = truth[obs]
        dx, dy = gx - ox, gy - oy
        distance = np.hypot(dx, dy)
        rate = ((gvx - ovx) * dx + (gvy - ovy) * dy) / distance
        own.tracks = [
            TrackSample(
                t=own.telemetry[k].t,
                frame=own.telemetry[k].frame,
                participant_id=obs,
                track_id=obs + "::T001",
                gx=float(gx[k]),
                gy=float(gy[k]),
                gvx=float(gvx[k]),
                gvy=float(gvy[k]),
                rel_x=float(dx[k]),
                rel_y=float(dy[k]),
                range_m=float(distance[k]),
                range_rate=float(rate[k]),
                confidence=0.95,
                n_points=5,
            )
            for k in range(len(ts))
            if 1.0 < ts[k] < span - 1.0 and not (dropout and k % 4 == 0)
        ]
    for pid, p in participants.items():
        offset, scale = profiles[pid]
        p.events = [
            Event(
                pid + "own",
                EventType.DECELERATION,
                pid,
                scale * 5 + offset,
                scale * 5 + offset,
                scale * 5.2 + offset,
            )
        ]
    a = participants["A"]
    off, scale = profiles["A"]
    a.events = [
        Event(
            "Aremote",
            EventType.TARGET_DECELERATION,
            "A",
            scale * 5 + off,
            scale * 5 + off,
            scale * 5.2 + off,
            subject="A::T001",
        )
    ]
    if chain:
        off, scale = profiles["B"]
        participants["B"].events.append(
            Event(
                "Bremote",
                EventType.TARGET_DECELERATION,
                "B",
                scale * 8 + off,
                scale * 8 + off,
                scale * 8.2 + off,
                subject="B::T001",
            )
        )
        off, scale = profiles["C"]
        participants["C"].events = [
            Event(
                "Cown",
                EventType.DECELERATION,
                "C",
                scale * 8 + off,
                scale * 8 + off,
                scale * 8.2 + off,
            )
        ]
    return RunEvidence(
        Path("."),
        {"run_id": "physical", "clock_protocol": "independent_local_clocks"},
        participants,
    )


@pytest.fixture
def cfg():
    return load_run_config()


def test_A_zero_offset_regression(cfg):
    result = align_participants(physical_run(), cfg)
    assert result["reference"] == "A"
    assert result["offsets"]["B"]["offset_s"] == pytest.approx(0, abs=1e-5)
    assert result["offsets"]["B"]["confidence"] > 0.99


def test_B_simple_offset_recovered_from_radar(cfg):
    raw = physical_run({"A": (0, 1), "B": (0.37, 1)})
    result = align_participants(raw, cfg)
    assert result["offsets"]["B"]["offset_s"] == pytest.approx(-0.37, abs=0.003)
    assert result["constraints"][0]["range_residual_m"] < 0.03
    assert result["constraints"][0]["range_rate_residual_mps"] < 0.03
    aligned = AlignedRunEvidence(raw, result)
    assert associate_tracks(aligned, cfg)["A::T001"].assigned_participant == "B"
    assert align_events(aligned, {"A::T001": "B"}, cfg)["groups"] == [
        ["Aremote", "Bown"]
    ]
    assert raw.get("B").events[0].t_peak == 5.37
    with pytest.raises(ValueError):
        associate_tracks(raw, cfg)


def test_C_E_three_clocks_and_transitive_constraint_graph(cfg):
    profiles = {"A": (0.41, 1), "B": (-0.23, 1), "C": (0.12, 1)}
    raw = physical_run(profiles, chain=True)
    result = align_participants(raw, cfg)
    ref = result["reference"]
    assert ref == "B"
    assert {(h["observer"], h["candidate"]) for h in result["constraints"]} == {
        ("A", "B"),
        ("B", "C"),
    }
    for pid, (off, scale) in profiles.items():
        assert result["offsets"][pid]["offset_s"] == pytest.approx(
            profiles[ref][0] - off, abs=0.003
        )
    view = AlignedRunEvidence(raw, result)
    assert view.get("A").events[0].t_peak < view.get("C").events[0].t_peak


def test_D_offset_and_drift_are_recovered(cfg):
    # Long, precise synthetic point trajectories make sub-ms scale changes identifiable.
    cfg = cfg.with_overrides(
        {
            "fusion": {
                "time_alignment": {
                    "max_drift_ppm": 5000.0,
                    "min_drift_loss_improvement": 1e-5,
                }
            }
        }
    )
    raw = physical_run({"A": (0, 1), "B": (0.37, 1.003)}, span=60)
    result = align_participants(raw, cfg)
    b = result["offsets"]["B"]
    assert b["scale"] == pytest.approx(1 / 1.003, abs=2e-5)
    assert b["offset_s"] == pytest.approx(-0.37 / 1.003, abs=0.005)
    assert b["drift_status"] == "AFFINE_DRIFT_ESTIMATED"
    assert abs(b["drift_ppm"] - (1 / 1.003 - 1) * 1e6) < 20


def test_F_insufficient_evidence_is_unresolved_not_zero(cfg):
    raw = physical_run({"A": (0, 1), "B": (0.37, 1)})
    raw.get("A").tracks = []
    result = align_participants(raw, cfg)
    assert result["offsets"]["B"]["status"] == "UNRESOLVED_TIME_ALIGNMENT"
    assert result["offsets"]["B"]["offset_s"] is None
    assert result["offsets"]["B"]["scale"] is None
    view = AlignedRunEvidence(raw, result)
    assert align_events(view, {}, cfg)["groups"] == []
    docs = {
        p: GraphDocument("causal", Provenance.LOCAL, p, nodes=raw.get(p).events)
        for p in raw.participant_ids
    }
    fused, diag = fuse_graphs(view, docs, {}, cfg)
    assert diag["unresolved_time_participants"] == ["B"]
    assert all(n.participant_id == "A" for n in fused.nodes)
    assert raw.get("B").events


def test_G_periodic_20hz_grid_does_not_identify_clock(cfg):
    raw = physical_run({"A": (0, 1), "B": (0.4, 1)})
    assert np.diff(raw.get("A").times()) == pytest.approx(np.diff(raw.get("B").times()))
    result = align_participants(raw, cfg)
    assert result["offsets"]["B"]["offset_s"] == pytest.approx(-0.4, abs=0.003)
    raw.get("A").tracks = []
    assert align_participants(raw, cfg)["offsets"]["B"]["offset_s"] is None


def test_H_seeded_jitter_and_dropout_keep_explicit_confidence(cfg):
    raw = physical_run({"A": (0, 1), "B": (0.37, 1)}, jitter=0.001, dropout=True)
    result = align_participants(raw, cfg)
    b = result["offsets"]["B"]
    assert b["status"] == "ALIGNED"
    assert b["offset_s"] == pytest.approx(-0.37, abs=0.01)
    assert 0.8 < b["confidence"] < 1.0
    assert result["constraints"][0]["n_samples"] >= 12


def test_range_is_an_actual_term_in_time_estimation(cfg):
    raw = physical_run({"A": (0, 1), "B": (0.37, 1)})
    raw.get("A").tracks = [replace(t, gx=t.gx + 2.0) for t in raw.get("A").tracks]
    both = estimate_track_clock(raw.get("A"), "A::T001", raw.get("B"), cfg)
    positional = estimate_track_clock(
        raw.get("A"),
        "A::T001",
        raw.get("B"),
        cfg.with_overrides({"fusion": {"time_alignment": {"range_sigma_m": 1e6}}}),
    )
    assert abs(both["offset_s"] + 0.37) < abs(positional["offset_s"] + 0.37)


def test_fusion_invariance_and_original_timestamp_provenance(cfg):
    cfg = cfg.with_overrides(
        {
            "fusion": {
                "time_alignment": {
                    "max_drift_ppm": 5000.0,
                    "min_drift_loss_improvement": 1e-5,
                }
            }
        }
    )
    profiles1 = {"A": (0, 1), "B": (0, 1), "C": (0, 1)}
    profiles2 = {"A": (0.41, 1.001), "B": (-0.23, 0.999), "C": (0.12, 1.002)}
    outputs = []
    for profiles in (profiles1, profiles2):
        raw = physical_run(profiles, chain=True, span=60)
        alignment = align_participants(raw, cfg)
        view = AlignedRunEvidence(raw, alignment)
        assigned = associate_tracks(view, cfg)
        docs = {
            pid: GraphDocument(
                "causal",
                Provenance.LOCAL,
                pid,
                nodes=p.events,
                edges=(
                    [
                        GraphEdge(
                            p.events[0].event_id, p.events[1].event_id, "CONTRIBUTES_TO"
                        )
                    ]
                    if len(p.events) > 1
                    else []
                ),
            )
            for pid, p in raw.participants.items()
        }
        fused, diag = fuse_graphs(view, docs, assigned, cfg)
        ref = alignment["reference"]
        off, scale = profiles[ref]
        key = {n.event_id: tuple(n.merged_from) for n in fused.nodes}
        outputs.append(
            (
                [(t, a.assigned_participant) for t, a in assigned.items()],
                sorted(
                    (tuple(n.merged_from), round((n.t_peak - off) / scale, 2))
                    for n in fused.nodes
                ),
                sorted(
                    (key[e.source], key[e.target], e.edge_type) for e in fused.edges
                ),
            )
        )
        assert any(
            e.kind == "clock_alignment"
            and "local_t_peak" in e.detail
            and "common_t_peak" in e.detail
            for n in fused.nodes
            for e in n.evidence
        )
        assert raw.get("A").events[0].t_peak == pytest.approx(
            profiles["A"][1] * 5 + profiles["A"][0]
        )
    assert outputs[0] == outputs[1]


def test_collision_anchor_supplements_radar_not_identity_or_cadence(cfg):
    raw = physical_run({"A": (0.0, 1.0), "B": (0.37, 1.0)})
    own, other = raw.get("A"), raw.get("B")
    other.telemetry = [replace(s, x=s.x - 28.0) for s in other.telemetry]
    tracks = []
    for s in own.tracks:
        k = min(range(len(own.telemetry)), key=lambda i: abs(own.telemetry[i].t - s.t))
        a, b = own.telemetry[k], other.telemetry[k]
        # Radar reflects a surface one metre ahead of the self-reported origin.
        dx, dy = b.x + 1.0 - a.x, b.y - a.y
        distance = math.hypot(dx, dy)
        rate = ((b.vx - a.vx) * dx + (b.vy - a.vy) * dy) / distance
        tracks.append(
            replace(s, gx=b.x + 1.0, gy=b.y, range_m=distance, range_rate=rate)
        )
    own.tracks = tracks
    without = estimate_track_clock(own, "A::T001", other, cfg)
    for pid, t in [("A", 5.0), ("B", 5.37)]:
        raw.get(pid).triggers = [
            LocalTriggerRecord(t, 123, pid, TriggerKind.COLLISION, True, 100.0)
        ]
    supported = estimate_track_clock(own, "A::T001", other, cfg)
    assert supported["collision_anchors"] == 1
    assert abs(supported["offset_s"] + 0.37) < abs(without["offset_s"] + 0.37)
    assert "radar_range" in supported["methods"]
    own.tracks = []
    assert (
        align_participants(raw, cfg)["offsets"]["B"]["status"]
        == "UNRESOLVED_TIME_ALIGNMENT"
    )


def test_apply_offset_helper():
    assert apply_offset([0, 0.5, 1], -0.25) == [-0.25, 0.25, 0.75]
