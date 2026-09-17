"""Unit tests for event alignment, confidence fusion and graph fusion.

These tests encode the properties that make the fused graph usable as evidence:

* an observation of another vehicle's behaviour and that vehicle's own record of
  the same behaviour become **one** node, carrying **both** owners;
* two halves of a causal chain held by different participants join into a single
  chain that reaches the outcome -- something neither local graph contains;
* a disagreement between participants survives fusion in full, in the edges and
  in the diagnostics;
* the result is still a DAG, and every edge removed to make it one is named.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import networkx as nx
import pytest

from cdf.common.config import load_run_config
from cdf.common.evidence import ParticipantEvidence, RunEvidence
from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    Evidence,
    GraphDocument,
    GraphEdge,
    Provenance,
    TelemetrySample,
    TrackSample,
    make_event_id,
)
from cdf.fusion.confidence import fuse_confidence, noisy_or
from cdf.fusion.event_alignment import align_events, resolve_subjects
from cdf.fusion.graph_fusion import fuse_graphs
from cdf.fusion.track_association import (
    STATUS_RESOLVED,
    STATUS_UNRESOLVED,
    TrackAssignment,
    associate_tracks,
)

DT = 0.05


@pytest.fixture(scope="module")
def cfg():
    return load_run_config()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _event(
    pid: str,
    event_type: EventType,
    t_peak: float,
    subject: Optional[str] = None,
    confidence: float = 0.8,
    values: Optional[Dict[str, float]] = None,
) -> Event:
    return Event(
        event_id=make_event_id("local", pid, event_type.value, t_peak, subject),
        event_type=event_type,
        participant_id=pid,
        t_start=t_peak - 0.2,
        t_peak=t_peak,
        t_end=t_peak + 0.2,
        subject=subject,
        values=dict(values or {}),
        confidence=confidence,
        evidence=[Evidence(kind="telemetry", ref=pid, t_start=t_peak - 0.2, t_end=t_peak + 0.2)],
        provenance=Provenance.LOCAL,
    )


def _edge(
    source: Event,
    target: Event,
    edge_type: CausalEdgeType,
    owner: str,
    confidence: float = 0.7,
    rule: str = "unit_rule",
) -> GraphEdge:
    return GraphEdge(
        source=source.event_id,
        target=target.event_id,
        edge_type=edge_type.value,
        confidence=confidence,
        provenance=Provenance.LOCAL,
        rule=rule,
        temporal_relation="before",
        owners=[owner],
    )


def _doc(owner: str, nodes: List[Event], edges: List[GraphEdge]) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal",
        scope=Provenance.LOCAL,
        owner=owner,
        run_id="unit",
        scenario_id="S00",
        seed=0,
        nodes=nodes,
        edges=edges,
    )


def _participant(pid: str, y: float = 0.0, x0: float = 0.0) -> ParticipantEvidence:
    times = [round(9.0 + k * DT, 6) for k in range(80)]
    return ParticipantEvidence(
        participant_id=pid,
        telemetry=[
            TelemetrySample(
                t=t,
                frame=i,
                participant_id=pid,
                x=x0 + 8.0 * (t - 9.0),
                y=y,
                z=0.0,
                yaw=0.0,
                vx=8.0,
                vy=0.0,
                speed=8.0,
            )
            for i, t in enumerate(times)
        ],
    )


def _closing_track(observer: ParticipantEvidence, track_id: str) -> None:
    """A track that closes from 20 m to ~2 m, so a collision counterpart is nameable."""
    for i, sample in enumerate(observer.telemetry):
        gap = max(2.0, 20.0 - 0.3 * i)
        observer.tracks.append(
            TrackSample(
                t=sample.t,
                frame=sample.frame,
                participant_id=observer.participant_id,
                track_id=track_id,
                rel_x=gap,
                rel_y=0.0,
                gx=sample.x + gap,
                gy=sample.y,
                gvx=8.0,
                gvy=0.0,
                range_m=gap,
                range_rate=-0.3 / DT,
                confidence=0.8,
                n_points=5,
                age=i,
            )
        )


def _run(*participants: ParticipantEvidence) -> RunEvidence:
    return RunEvidence(
        run_dir=Path("."),
        manifest={"run_id": "unit", "scenario_id": "S00", "seed": 0},
        participants={p.participant_id: p for p in participants},
    )


def _assignment(track_id: str, observer: str, participant: str) -> TrackAssignment:
    return TrackAssignment(
        track_id=track_id,
        observer_id=observer,
        assigned_participant=participant,
        confidence=0.92,
        status=STATUS_RESOLVED,
        rmse_m=0.31,
        overlap_s=4.0,
        reason="unit fixture",
    )


def _fused_id(fused: GraphDocument, local_id: str) -> str:
    matches = [n.event_id for n in fused.nodes if local_id in n.merged_from]
    assert len(matches) == 1, "local event {0} must map to exactly one fused node".format(local_id)
    return matches[0]


# ---------------------------------------------------------------------------
# Event alignment
# ---------------------------------------------------------------------------


def test_observation_of_a_deceleration_merges_with_the_vehicles_own_record(cfg):
    """The asymmetric case that makes fusion worth doing.

    ``A`` sees an anonymous track decelerate; ``B`` records its own deceleration.
    Different event types, different subjects, one physical fact.
    """
    a = _participant("A")
    b = _participant("B", x0=20.0)
    _closing_track(a, "A::T001")
    a.events = [_event("A", EventType.TARGET_DECELERATION, 10.55, subject="A::T001")]
    b.events = [_event("B", EventType.HARD_DECELERATION, 10.50)]
    run = _run(a, b)

    subjects = resolve_subjects({"A::T001": _assignment("A::T001", "A", "B")})
    assert subjects == {"A::T001": "B"}

    result = align_events(run, subjects, cfg)

    assert result["singletons"] == []
    assert len(result["groups"]) == 1
    assert sorted(result["groups"][0]) == sorted(
        [a.events[0].event_id, b.events[0].event_id]
    )


def test_unresolved_subject_blocks_the_merge(cfg):
    """Without an identity there is no basis for merging, so nothing is merged."""
    a = _participant("A")
    b = _participant("B", x0=20.0)
    a.events = [_event("A", EventType.TARGET_DECELERATION, 10.55, subject="A::T001")]
    b.events = [_event("B", EventType.HARD_DECELERATION, 10.50)]

    result = align_events(_run(a, b), {}, cfg)

    assert result["groups"] == []
    assert len(result["singletons"]) == 2
    assert "unresolved_subject" in [d["kind"] for d in result["diagnostics"]]


def test_events_about_different_vehicles_are_kept_apart(cfg):
    """Same type, same instant, different subject vehicle -- two distinct facts."""
    a = _participant("A")
    b = _participant("B", x0=20.0)
    c = _participant("C", y=6.0)
    _closing_track(a, "A::T001")
    a.events = [_event("A", EventType.TARGET_DECELERATION, 10.50, subject="A::T001")]
    b.events = [_event("B", EventType.HARD_DECELERATION, 10.50)]
    c.events = [_event("C", EventType.HARD_DECELERATION, 10.50)]

    result = align_events(
        _run(a, b, c), resolve_subjects({"A::T001": _assignment("A::T001", "A", "B")}), cfg
    )

    assert len(result["groups"]) == 1
    merged = set(result["groups"][0])
    assert merged == {a.events[0].event_id, b.events[0].event_id}
    assert result["singletons"] == [c.events[0].event_id]


def test_events_outside_the_time_tolerance_are_kept_apart(cfg):
    """Agreement in time is a necessary condition, and it is configurable."""
    a = _participant("A")
    b = _participant("B", x0=20.0)
    _closing_track(a, "A::T001")
    a.events = [_event("A", EventType.TARGET_DECELERATION, 13.0, subject="A::T001")]
    b.events = [_event("B", EventType.HARD_DECELERATION, 10.5)]

    result = align_events(
        _run(a, b), resolve_subjects({"A::T001": _assignment("A::T001", "A", "B")}), cfg
    )

    assert result["groups"] == []
    assert len(result["singletons"]) == 2


def _fixed_range_track(observer: ParticipantEvidence, track_id: str, range_m: float) -> None:
    """A track held at a constant range from ``observer`` for the whole log."""
    for i, sample in enumerate(observer.telemetry):
        observer.tracks.append(
            TrackSample(
                t=sample.t,
                frame=sample.frame,
                participant_id=observer.participant_id,
                track_id=track_id,
                rel_x=range_m,
                rel_y=0.0,
                gx=sample.x + range_m,
                gy=sample.y,
                gvx=8.0,
                gvy=0.0,
                range_m=range_m,
                confidence=0.8,
                n_points=5,
                age=i,
            )
        )


def _collision_counterpart_case(cfg, range_to_b: float, range_to_c: float):
    """``A``'s onboard collision trigger, with two resolved tracks nearby.

    An onboard collision sensor records *that* an impact happened, never with
    whom, so the counterpart has to be inferred. Two candidates are in contention
    and the only thing separating them is a millimetre of range.

    ``B`` and ``C`` are placed symmetrically about ``A`` -- one ahead, one to the
    side, both about three metres away -- so that the ambiguity survives every
    source of evidence fusion has, the exchanged trajectories included. An
    ambiguity that the exchanged logs could resolve is not an ambiguity; this one
    genuinely cannot be resolved, which is what the discipline is for.
    """
    a = _participant("A")
    b = _participant("B", x0=range_to_b)
    c = _participant("C", y=range_to_c)
    _fixed_range_track(a, "A::T001", range_to_b)
    _fixed_range_track(a, "A::T002", range_to_c)
    _fixed_range_track(b, "B::T001", 3.0)
    _fixed_range_track(c, "C::T001", 3.0)
    a.events = [_event("A", EventType.COLLISION, 12.00, confidence=0.95)]
    b.events = [_event("B", EventType.COLLISION, 12.02, confidence=0.95)]
    c.events = [_event("C", EventType.COLLISION, 12.01, confidence=0.95)]
    subjects = resolve_subjects(
        {
            "A::T001": _assignment("A::T001", "A", "B"),
            "A::T002": _assignment("A::T002", "A", "C"),
            "B::T001": _assignment("B::T001", "B", "A"),
            "C::T001": _assignment("C::T001", "C", "A"),
        }
    )
    return align_events(_run(a, b, c), subjects, cfg), a, b, c


def test_an_indistinguishable_collision_counterpart_is_refused_not_guessed(cfg):
    """Range must *single out* the counterpart before fusion may name one.

    This is the one place in the fusion layer where an identity is inferred from
    proximity rather than from trajectory agreement, and it is the place where a
    guess would do the most damage: the fused ``COLLISION`` node names the pair of
    vehicles the artifact accuses. With two resolved tracks a millimetre apart
    nothing in the local evidence distinguishes them, so ``AMBIGUOUS`` -- here,
    refusing to merge -- is the only defensible verdict. Picking the nearer one
    would make a millimetre of measurement noise decide who was hit, and would do
    it silently.
    """
    close, _a, _b, _c = _collision_counterpart_case(cfg, 3.000, 3.001)
    swapped, _a2, _b2, _c2 = _collision_counterpart_case(cfg, 3.001, 3.000)

    kinds_close = [d["kind"] for d in close["diagnostics"]]
    assert "counterpart_ambiguous" in kinds_close
    assert "counterpart_inferred" not in [
        d["kind"] for d in close["diagnostics"] if d.get("participant_id") == "A"
    ]

    # No merge may rest on the coin flip, and the verdict must not depend on which
    # of the two indistinguishable candidates happened to be a millimetre nearer.
    merged_close = [set(g) for g in close["groups"]]
    merged_swapped = [set(g) for g in swapped["groups"]]
    assert merged_close == merged_swapped, (
        "a 1 mm range difference changed which vehicles fusion merged: the "
        "counterpart was guessed, not established"
    )
    assert all(_a.events[0].event_id not in g for g in merged_close), (
        "A's collision must stay unmerged while its counterpart is indistinguishable"
    )

    # The diagnostic has to say *why*, naming both candidates and the threshold.
    reason = [d for d in close["diagnostics"] if d["kind"] == "counterpart_ambiguous"][0]
    assert "B" in reason["message"] and "C" in reason["message"]
    assert "counterpart_ambiguity_margin_m" in reason["message"]

    # And the guard must not become a blanket refusal: when the two candidates are
    # genuinely far apart, the nearer one is still named and the merge happens.
    separated, a3, b3, _c3 = _collision_counterpart_case(cfg, 3.0, 6.5)
    # The counterpart may be established either by proximity alone or by the two
    # vehicles' mutually corroborating impact records -- reciprocity is the
    # stronger evidence and takes precedence when both sides recorded the impact.
    # What must hold either way is the *outcome*: A is paired with B, the vehicle
    # the evidence singles out, and not with the one 3.5 m further away.
    settled = [
        d
        for d in separated["diagnostics"]
        if d["kind"] in ("counterpart_inferred", "mutual_impact_reconciled")
        and (
            d.get("participant_id") == "A" or "A" in (d.get("participants") or [])
        )
    ]
    assert settled, "a decisively nearer counterpart must still be named"
    named = {
        d.get("counterpart")
        for d in settled
        if d["kind"] == "counterpart_inferred"
    } | {
        p
        for d in settled
        if d["kind"] == "mutual_impact_reconciled"
        for p in (d.get("participants") or [])
        if p != "A"
    }
    assert named == {"B"}, "A must be paired with B, not {0}".format(sorted(named))
    assert [sorted(g) for g in separated["groups"]] == [
        sorted([a3.events[0].event_id, b3.events[0].event_id])
    ]


# ---------------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------------


def test_noisy_or_accumulates_and_is_capped(cfg):
    """Two half-strength independent observations support a claim more than one."""
    assert noisy_or([0.5, 0.5]) == pytest.approx(0.75)
    assert noisy_or([0.5]) == pytest.approx(0.5)
    assert noisy_or([]) == 0.0
    assert noisy_or([0.9] * 10) == pytest.approx(0.99)
    assert noisy_or([0.9] * 10, cap=0.5) == pytest.approx(0.5)
    assert noisy_or([1.5, -0.2]) == pytest.approx(0.99)


def test_fuse_confidence_dispatches_on_configuration(cfg):
    assert fuse_confidence([0.5, 0.5], cfg) == pytest.approx(0.75)
    assert fuse_confidence([], cfg) == 0.0
    assert float(cfg.get("fusion.confidence_fusion.cap")) == pytest.approx(0.99)

    as_max = cfg.with_overrides({"fusion": {"confidence_fusion": {"method": "max"}}})
    as_mean = cfg.with_overrides({"fusion": {"confidence_fusion": {"method": "mean"}}})
    assert fuse_confidence([0.4, 0.8], as_max) == pytest.approx(0.8)
    assert fuse_confidence([0.4, 0.8], as_mean) == pytest.approx(0.6)

    broken = cfg.with_overrides({"fusion": {"confidence_fusion": {"method": "magic"}}})
    with pytest.raises(ValueError):
        fuse_confidence([0.4], broken)


# ---------------------------------------------------------------------------
# Graph fusion: joining two halves of a chain
# ---------------------------------------------------------------------------


def _half_chain_case():
    """``B`` holds the cause, ``A`` holds the reaction and the outcome."""
    a = _participant("A")
    b = _participant("B", x0=20.0)
    _closing_track(a, "A::T001")

    b0 = _event("B", EventType.BRAKE_ONSET, 10.40, confidence=0.9)
    b1 = _event(
        "B", EventType.HARD_DECELERATION, 10.50, confidence=0.8, values={"accel_long": -5.0}
    )
    a1 = _event(
        "A",
        EventType.TARGET_DECELERATION,
        10.55,
        subject="A::T001",
        confidence=0.7,
        values={"accel_long": -4.0, "range_m": 12.0},
    )
    a2 = _event("A", EventType.HARD_BRAKE, 11.20, confidence=0.85)
    a3 = _event("A", EventType.COLLISION, 12.00, confidence=0.95)

    docs = {
        "A": _doc(
            "A",
            [a1, a2, a3],
            [
                _edge(a1, a2, CausalEdgeType.TRIGGERS, "A", confidence=0.75),
                _edge(a2, a3, CausalEdgeType.CAUSES_OUTCOME, "A", confidence=0.8),
            ],
        ),
        "B": _doc("B", [b0, b1], [_edge(b0, b1, CausalEdgeType.CONTRIBUTES_TO, "B", 0.9)]),
    }
    a.events = [a1, a2, a3]
    b.events = [b0, b1]
    return _run(a, b), docs, {"b0": b0, "b1": b1, "a1": a1, "a2": a2, "a3": a3}


def test_two_half_chains_fuse_into_one_chain_reaching_the_outcome(cfg):
    run, docs, ev = _half_chain_case()
    assignments = {"A::T001": _assignment("A::T001", "A", "B")}

    fused, diag = fuse_graphs(run, docs, assignments, cfg, graph_kind="causal")

    assert fused.scope is Provenance.FUSED
    assert fused.owner is None
    assert diag["n_input_nodes"] == {"A": 3, "B": 2}
    assert diag["n_merged_groups"] == 1
    assert diag["n_fused_nodes"] == 4
    assert len(fused.nodes) == 4

    merged_id = _fused_id(fused, ev["b1"].event_id)
    assert merged_id == _fused_id(fused, ev["a1"].event_id)
    merged = fused.node_by_id(merged_id)
    assert merged is not None
    assert merged.owners == ["A", "B"], "a fused node must name every contributor"
    assert merged.provenance is Provenance.FUSED
    assert sorted(merged.merged_from) == sorted([ev["a1"].event_id, ev["b1"].event_id])
    # B's own account of its own deceleration is the canonical description.
    assert merged.event_type is EventType.HARD_DECELERATION
    assert merged.subject is None
    assert 10.50 <= merged.t_peak <= 10.55
    assert merged.values["accel_long"] == pytest.approx(-4.5)
    assert merged.values["range_m"] == pytest.approx(12.0)
    assert merged.confidence == pytest.approx(noisy_or([0.8, 0.7]))
    assert merged.confidence > max(0.8, 0.7)

    g = nx.DiGraph()
    g.add_nodes_from(n.event_id for n in fused.nodes)
    g.add_edges_from((e.source, e.target) for e in fused.edges)
    start = _fused_id(fused, ev["b0"].event_id)
    outcome = _fused_id(fused, ev["a3"].event_id)
    assert nx.has_path(g, start, outcome)
    assert nx.shortest_path(g, start, outcome) == [
        start,
        merged_id,
        _fused_id(fused, ev["a2"].event_id),
        outcome,
    ]
    assert nx.is_directed_acyclic_graph(g)
    assert diag["dag"]["is_dag"] is True

    # No single local graph contains this node, nor the chain it completes.
    assert merged_id in diag["fusion_added"]["nodes"]
    assert {"source": start, "target": outcome} in diag["fusion_added"]["bridged_paths"]
    touching = {(e["source"], e["target"]) for e in diag["fusion_added"]["edges"]}
    assert (start, merged_id) in touching
    assert diag["rejected_edges"] == []
    assert diag["contradictions"] == []


def test_fused_edges_keep_every_contributor(cfg):
    """An edge asserted by two participants is one edge that names both."""
    a = _participant("A")
    b = _participant("B", x0=20.0)
    _closing_track(a, "A::T001")
    _closing_track(b, "B::T001")

    x_a = _event("A", EventType.LOW_TTC, 9.00, subject="A::T001", confidence=0.6)
    y_a = _event("A", EventType.CRITICAL_TTC, 10.00, subject="A::T001", confidence=0.7)
    x_b = _event("B", EventType.LOW_TTC, 9.05, subject="B::T001", confidence=0.5)
    y_b = _event("B", EventType.CRITICAL_TTC, 10.05, subject="B::T001", confidence=0.6)
    a.events, b.events = [x_a, y_a], [x_b, y_b]

    docs = {
        "A": _doc("A", [x_a, y_a], [_edge(x_a, y_a, CausalEdgeType.CONTRIBUTES_TO, "A", 0.6)]),
        "B": _doc("B", [x_b, y_b], [_edge(x_b, y_b, CausalEdgeType.CONTRIBUTES_TO, "B", 0.5)]),
    }
    assignments = {
        "A::T001": _assignment("A::T001", "A", "B"),
        "B::T001": _assignment("B::T001", "B", "A"),
    }

    fused, diag = fuse_graphs(_run(a, b), docs, assignments, cfg)

    assert diag["n_fused_nodes"] == 2
    assert diag["n_fused_edges"] == 1
    edge = fused.edges[0]
    assert edge.owners == ["A", "B"]
    assert edge.provenance is Provenance.FUSED
    assert edge.confidence == pytest.approx(noisy_or([0.6, 0.5]))
    assert edge.detail["n_contributors"] == 2
    assert len(edge.merged_from) == 2
    assert len(edge.evidence) == 0 or all(isinstance(e, Evidence) for e in edge.evidence)


# ---------------------------------------------------------------------------
# Graph fusion: disagreement
# ---------------------------------------------------------------------------


def _contradiction_case(edge_type_b: CausalEdgeType, reverse: bool = False):
    a = _participant("A")
    b = _participant("B", x0=20.0)
    _closing_track(a, "A::T001")
    _closing_track(b, "B::T001")

    x_a = _event("A", EventType.LOW_TTC, 9.00, subject="A::T001", confidence=0.8)
    y_a = _event("A", EventType.CRITICAL_TTC, 10.00, subject="A::T001", confidence=0.8)
    x_b = _event("B", EventType.LOW_TTC, 9.05, subject="B::T001", confidence=0.6)
    y_b = _event("B", EventType.CRITICAL_TTC, 10.05, subject="B::T001", confidence=0.6)
    a.events, b.events = [x_a, y_a], [x_b, y_b]

    b_edge = (
        _edge(y_b, x_b, edge_type_b, "B", 0.4)
        if reverse
        else _edge(x_b, y_b, edge_type_b, "B", 0.4)
    )
    docs = {
        "A": _doc("A", [x_a, y_a], [_edge(x_a, y_a, CausalEdgeType.CONTRIBUTES_TO, "A", 0.9)]),
        "B": _doc("B", [x_b, y_b], [b_edge]),
    }
    assignments = {
        "A::T001": _assignment("A::T001", "A", "B"),
        "B::T001": _assignment("B::T001", "B", "A"),
    }
    return _run(a, b), docs, assignments, {"x_a": x_a, "y_a": y_a, "x_b": x_b, "y_b": y_b}


def test_conflicting_edge_types_both_survive_fusion(cfg):
    """One participant says PREVENTS where another says CONTRIBUTES_TO.

    Averaging them away would destroy the single most informative fact in the
    artifact, so both claims stay in the graph and the disagreement is reported.
    """
    run, docs, assignments, ev = _contradiction_case(CausalEdgeType.PREVENTS)

    fused, diag = fuse_graphs(run, docs, assignments, cfg)

    assert diag["n_fused_nodes"] == 2
    x = _fused_id(fused, ev["x_a"].event_id)
    y = _fused_id(fused, ev["y_a"].event_id)
    assert x == _fused_id(fused, ev["x_b"].event_id)

    types = sorted(e.edge_type for e in fused.edges if (e.source, e.target) == (x, y))
    assert types == ["CONTRIBUTES_TO", "PREVENTS"], "no claim may be discarded"

    contradictions = [
        c for c in diag["contradictions"] if c["kind"] == "edge_type_disagreement"
    ]
    assert len(contradictions) == 1
    assert contradictions[0]["source"] == x
    assert contradictions[0]["target"] == y
    assert contradictions[0]["edge_types"] == ["CONTRIBUTES_TO", "PREVENTS"]
    assert {c["participant_id"] for c in contradictions[0]["claims"]} == {"A", "B"}
    assert contradictions[0]["resolution"] == "kept_both"

    for e in fused.edges:
        assert "contradiction" in e.detail
        assert e.detail["contradiction"]["competing_edge_types"]
    assert diag["dag"]["is_dag"] is True


def test_adjudication_is_opt_in_and_still_reports_what_it_dropped(cfg):
    """``keep_contradictions: false`` may resolve a conflict but never hide it."""
    run, docs, assignments, _ev = _contradiction_case(CausalEdgeType.PREVENTS)
    strict = cfg.with_overrides({"fusion": {"conflict": {"keep_contradictions": False}}})

    fused, diag = fuse_graphs(run, docs, assignments, strict)

    assert len(fused.edges) == 1
    assert fused.edges[0].edge_type == "CONTRIBUTES_TO"
    dropped = [r for r in diag["rejected_edges"] if r["reason"] == "contradiction_adjudicated"]
    assert len(dropped) == 1
    assert dropped[0]["edge_type"] == "PREVENTS"
    assert diag["contradictions"][0]["resolution"] == "kept_strongest"


def test_opposite_directions_are_recorded_and_the_cycle_is_broken(cfg):
    """Fusion can create a cycle; the weakest claim in it is removed and named."""
    run, docs, assignments, ev = _contradiction_case(
        CausalEdgeType.CONTRIBUTES_TO, reverse=True
    )

    fused, diag = fuse_graphs(run, docs, assignments, cfg)

    x = _fused_id(fused, ev["x_a"].event_id)
    y = _fused_id(fused, ev["y_a"].event_id)
    assert [(e.source, e.target) for e in fused.edges] == [(x, y)]

    broken = [r for r in diag["rejected_edges"] if r["reason"] == "cycle_broken"]
    assert len(broken) == 1
    assert (broken[0]["source"], broken[0]["target"]) == (y, x)
    assert any(c["kind"] == "direction_disagreement" for c in diag["contradictions"])
    assert diag["dag"]["is_dag"] is True
    assert diag["dag"]["enforced"] is True
    assert diag["dag"]["notes"], "the DAG stage must say how acyclicity was obtained"


# ---------------------------------------------------------------------------
# Guard rails
# ---------------------------------------------------------------------------


def test_unresolved_tracks_are_reported_in_the_diagnostics(cfg):
    run, docs, _assignments, _ev = _contradiction_case(CausalEdgeType.PREVENTS)
    assignments = {
        "A::T001": _assignment("A::T001", "A", "B"),
        "B::T001": TrackAssignment(
            track_id="B::T001",
            observer_id="B",
            assigned_participant=None,
            confidence=0.1,
            status=STATUS_UNRESOLVED,
            overlap_s=2.0,
            reason="no participant matched",
        ),
    }

    fused, diag = fuse_graphs(run, docs, assignments, cfg)

    assert [t["track_id"] for t in diag["unresolved_tracks"]] == ["B::T001"]
    # B's events concern an unresolved track, so nothing merges and both of B's
    # nodes keep their local subject label.
    assert diag["n_merged_groups"] == 0
    assert diag["n_fused_nodes"] == 4
    assert {n.subject for n in fused.nodes if n.participant_id == "B"} == {"B::T001"}


def test_an_edge_with_an_unknown_endpoint_is_rejected_not_dropped(cfg):
    a = _participant("A")
    n1 = _event("A", EventType.HARD_BRAKE, 10.0)
    n2 = _event("A", EventType.COLLISION, 11.0)
    ghost = _event("A", EventType.LOW_TTC, 9.0)
    a.events = [n1, n2]
    docs = {
        "A": _doc(
            "A",
            [n1, n2],
            [
                _edge(n1, n2, CausalEdgeType.CAUSES_OUTCOME, "A", 0.9),
                _edge(ghost, n2, CausalEdgeType.CONTRIBUTES_TO, "A", 0.5),
            ],
        )
    }

    fused, diag = fuse_graphs(_run(a), docs, {}, cfg)

    assert len(fused.edges) == 1
    rejected = [r for r in diag["rejected_edges"] if r["reason"] == "endpoint_not_in_fused_graph"]
    assert len(rejected) == 1
    assert rejected[0]["source"] == ghost.event_id


def test_an_oracle_graph_cannot_enter_fusion(cfg):
    a = _participant("A")
    n1 = _event("A", EventType.HARD_BRAKE, 10.0)
    a.events = [n1]
    doc = _doc("A", [n1], [])
    doc.scope = Provenance.ORACLE

    with pytest.raises(ValueError):
        fuse_graphs(_run(a), {"A": doc}, {}, cfg)


def test_mismatched_graph_kind_fails_loudly(cfg):
    a = _participant("A")
    n1 = _event("A", EventType.HARD_BRAKE, 10.0)
    a.events = [n1]
    with pytest.raises(ValueError):
        fuse_graphs(_run(a), {"A": _doc("A", [n1], [])}, {}, cfg, graph_kind="event")


def test_association_and_fusion_compose_without_any_identifier(cfg):
    """End to end: identity is derived, then used, with no hand-written assignment.

    ``A`` records a track that happens to follow ``B``'s own trajectory. Nothing
    tells fusion that the track *is* ``B`` -- :func:`associate_tracks` has to
    establish it from the trajectories alone, and only then can ``A``'s
    observation merge with ``B``'s own account.
    """
    a = _participant("A")
    b = _participant("B", x0=25.0)
    for i, sample in enumerate(a.telemetry):
        lead = b.telemetry[i]
        a.tracks.append(
            TrackSample(
                t=sample.t,
                frame=sample.frame,
                participant_id="A",
                track_id="A::T001",
                rel_x=lead.x - sample.x,
                rel_y=0.0,
                gx=lead.x + 0.12 * ((-1) ** i),
                gy=lead.y + 0.08 * ((-1) ** i),
                gvx=8.0,
                gvy=0.0,
                range_m=lead.x - sample.x,
                confidence=0.8,
                n_points=6,
                age=i,
            )
        )

    observed = _event("A", EventType.TARGET_DECELERATION, 10.55, subject="A::T001", confidence=0.7)
    own = _event("B", EventType.HARD_DECELERATION, 10.50, confidence=0.8)
    a.events, b.events = [observed], [own]
    run = _run(a, b)

    assignments = associate_tracks(run, cfg)
    assert assignments["A::T001"].status == STATUS_RESOLVED
    assert assignments["A::T001"].assigned_participant == "B"

    docs = {"A": _doc("A", [observed], []), "B": _doc("B", [own], [])}
    fused, diag = fuse_graphs(run, docs, assignments, cfg)

    assert diag["n_merged_groups"] == 1
    assert len(fused.nodes) == 1
    assert fused.nodes[0].owners == ["A", "B"]
    assert sorted(fused.nodes[0].merged_from) == sorted([observed.event_id, own.event_id])


def test_fusion_is_deterministic(cfg):
    """Identical inputs must produce byte-identical fused documents."""
    run, docs, assignments, _ev = _contradiction_case(CausalEdgeType.PREVENTS)

    first, diag_a = fuse_graphs(run, docs, assignments, cfg)
    second, diag_b = fuse_graphs(run, docs, assignments, cfg)

    assert first.to_dict() == second.to_dict()
    assert diag_a == diag_b
