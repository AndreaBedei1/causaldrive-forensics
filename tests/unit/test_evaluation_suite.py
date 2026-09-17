"""Unit tests for the cdf.evaluation layer.

Two kinds of case appear here and they are deliberately not mixed.

*Synthetic cases* build graphs whose correct answer is known by construction, so
an assertion can name the exact number (F1 exactly 1.0, SHD exactly 0, exactly
one gained node). They also include the *negative* controls: a fusion that adds
nothing must report a non-positive delta, and a local graph that claims an
unobservable quantity must be reported as dishonest. A metric that cannot fail
measures nothing.

*The real-run case* runs the whole suite over
``artifacts/S01_rear_end/seed_000_crash`` -- a genuine CARLA recording, not a
fixture -- and asserts both that the available blocks carry real numbers and that
the unavailable ones come back ``None`` with a reason rather than zero.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.evidence import load_run
from cdf.common.io import read_json
from cdf.common.layout import RunLayout
from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from cdf.evaluation import figures, tables
from cdf.evaluation.association_metrics import evaluate_association, true_track_identities
from cdf.evaluation.attribution_metrics import (
    evaluate_attribution,
    evaluate_local_unknowns,
    oracle_causal_initiators,
)
from cdf.evaluation.event_metrics import evaluate_events
from cdf.evaluation.graph_metrics import evaluate_graphs, fusion_benefit
from cdf.evaluation.suite import aggregate_runs, evaluate_run, summary_dir
from cdf.graph.export import load_graph

REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_RUN = REPO_ROOT / "artifacts" / "S01_rear_end" / "seed_000_crash"

CONTRIB = CausalEdgeType.CONTRIBUTES_TO.value
CAUSES = CausalEdgeType.CAUSES_OUTCOME.value


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


def make_event(
    event_id: str,
    event_type: EventType,
    t_peak: float,
    participant_id: str = "A",
    subject: Optional[str] = None,
    provenance: Provenance = Provenance.LOCAL,
) -> Event:
    """A minimal but schema-valid event centred on ``t_peak``."""
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=participant_id,
        t_start=t_peak - 0.1,
        t_peak=t_peak,
        t_end=t_peak + 0.1,
        subject=subject,
        provenance=provenance,
    )


def make_doc(
    nodes: List[Event],
    edges: List[GraphEdge],
    owner: Optional[str] = "A",
    scope: Provenance = Provenance.LOCAL,
) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal",
        scope=scope,
        owner=owner,
        run_id="run-test",
        scenario_id="S01",
        seed=0,
        nodes=list(nodes),
        edges=list(edges),
    )


def cfg_for_tests(**overrides: Any) -> Config:
    """A configuration carrying only the evaluation contract the tests need."""
    data: Dict[str, Any] = {
        "evaluation": {
            "event_match": {"time_tolerance_s": 1.5, "require_same_type": True},
            # False is the project default: an oracle edge onto a node the
            # reconstruction never found must count as MISSING, not be
            # excluded, or a half-seen graph scores perfect edge recall.
            "graph_match": {"use_matched_nodes_only": False},
            "association": {"count_unresolved_as_miss": True},
        }
    }
    data.update(overrides)
    return Config(data)


def three_node_chain(
    prefix: str, scope: Provenance = Provenance.LOCAL, owner: Optional[str] = "A"
) -> GraphDocument:
    """``HARD_BRAKE(B) -> CRITICAL_TTC(A) -> COLLISION(A)`` with both edges."""
    n1 = make_event(prefix + "-1", EventType.HARD_BRAKE, 1.0, participant_id="B")
    n2 = make_event(prefix + "-2", EventType.CRITICAL_TTC, 2.0, participant_id="A", subject="B")
    n3 = make_event(prefix + "-3", EventType.COLLISION, 3.0, participant_id="A")
    edges = [
        GraphEdge(source=n1.event_id, target=n2.event_id, edge_type=CONTRIB),
        GraphEdge(source=n2.event_id, target=n3.event_id, edge_type=CAUSES),
    ]
    return make_doc([n1, n2, n3], edges, owner=owner, scope=scope)


def partial_chain(prefix: str, owner: str = "A") -> GraphDocument:
    """Only the ``CRITICAL_TTC -> COLLISION`` half of :func:`three_node_chain`."""
    n2 = make_event(prefix + "-2", EventType.CRITICAL_TTC, 2.0, participant_id="A", subject="B")
    n3 = make_event(prefix + "-3", EventType.COLLISION, 3.0, participant_id="A")
    return make_doc(
        [n2, n3],
        [GraphEdge(source=n2.event_id, target=n3.event_id, edge_type=CAUSES)],
        owner=owner,
    )


# ---------------------------------------------------------------------------
# Graph metrics
# ---------------------------------------------------------------------------


def test_evaluate_graphs_against_itself_is_perfect() -> None:
    """A graph compared to itself must score F1 1.0 with zero edit distance."""
    doc = three_node_chain("x")
    result = evaluate_graphs({"A": doc}, doc, doc, None, cfg_for_tests())

    fused = result["fused"]
    assert fused["node_f1"] == 1.0
    assert fused["edge_f1"] == 1.0
    assert fused["node_precision"] == 1.0
    assert fused["edge_recall"] == 1.0
    assert fused["structural_hamming_distance"] == 0
    assert fused["n_missing_edges"] == 0
    assert fused["n_extra_edges"] == 0
    assert fused["n_reversed_edges"] == 0

    local = result["per_participant"]["A"]
    assert local["edge_f1"] == 1.0
    assert local["structural_hamming_distance"] == 0
    assert result["delta_edge_f1"] == 0.0
    assert result["delta_shd"] == 0


def test_evaluate_graphs_reports_missing_edges_against_a_richer_oracle() -> None:
    """A half-seen chain must not be able to claim perfect edge recall."""
    oracle = three_node_chain("o", scope=Provenance.ORACLE, owner=None)
    local = partial_chain("a")
    result = evaluate_graphs({"A": local}, None, oracle, None, cfg_for_tests())

    metrics = result["per_participant"]["A"]
    assert metrics["n_nodes_matched"] == 2
    assert metrics["n_missing_edges"] == 1
    assert metrics["edge_recall"] < 1.0
    assert metrics["structural_hamming_distance"] == 1
    assert result["fused"] is None
    assert "fused_reason" in result


def test_evaluate_graphs_refuses_an_empty_reference() -> None:
    doc = three_node_chain("x")
    with pytest.raises(ValueError, match="non-empty oracle graph"):
        evaluate_graphs({"A": doc}, doc, None, None, cfg_for_tests())


def test_fusion_benefit_positive_and_names_the_gain() -> None:
    """Fusion that strictly extends the best local view must show a positive delta."""
    oracle = three_node_chain("o", scope=Provenance.ORACLE, owner=None)
    local_a = partial_chain("a")
    only_root = make_event("b-1", EventType.HARD_BRAKE, 1.0, participant_id="B")
    local_b = make_doc([only_root], [], owner="B")
    fused = three_node_chain("f", scope=Provenance.FUSED, owner=None)

    benefit = fusion_benefit({"A": local_a, "B": local_b}, fused, oracle, cfg_for_tests())

    assert benefit["best_local_participant_id"] == "A"
    assert benefit["delta_edge_f1"] > 0.0
    assert benefit["delta_node_f1"] > 0.0
    assert benefit["delta_shd"] < 0
    assert benefit["fusion_helped"] is True

    # The gain must be named, not merely counted.
    assert benefit["n_nodes_gained"] >= 1
    gained_types = {n["event_type"] for n in benefit["gained_nodes"]}
    assert EventType.HARD_BRAKE.value in gained_types
    gained_edges = {(e["source_type"], e["target_type"]) for e in benefit["gained_edges"]}
    assert (EventType.HARD_BRAKE.value, EventType.CRITICAL_TTC.value) in gained_edges
    assert benefit["knowledge_gain"]["self_edge_recall"] > (
        benefit["knowledge_gain"]["baseline_edge_recall"]
    )


def test_fusion_benefit_is_non_positive_when_fusion_adds_nothing() -> None:
    """A null result must survive: no gain means no positive delta, and it is reported."""
    oracle = three_node_chain("o", scope=Provenance.ORACLE, owner=None)
    local_a = partial_chain("a")
    fused = copy.deepcopy(local_a)
    fused.scope = Provenance.FUSED

    benefit = fusion_benefit({"A": local_a}, fused, oracle, cfg_for_tests())

    assert benefit["delta_edge_f1"] <= 0.0
    assert benefit["delta_node_f1"] <= 0.0
    assert benefit["delta_shd"] >= 0
    assert benefit["fusion_helped"] is False
    assert benefit["n_nodes_gained"] == 0
    assert benefit["n_edges_gained"] == 0
    assert benefit["gained_nodes"] == []


def test_fusion_benefit_reports_a_negative_delta_when_fusion_hurts() -> None:
    """Fusion that invents structure must show up as a loss, not be smoothed away."""
    oracle = three_node_chain("o", scope=Provenance.ORACLE, owner=None)
    local_a = three_node_chain("a")
    fused = three_node_chain("f", scope=Provenance.FUSED, owner=None)
    bogus = make_event("f-9", EventType.LANE_CHANGE_LIKE_MANEUVER, 5.0, participant_id="A")
    fused.nodes.append(bogus)
    fused.edges.append(
        GraphEdge(source=bogus.event_id, target="f-3", edge_type=CONTRIB)
    )

    benefit = fusion_benefit({"A": local_a}, fused, oracle, cfg_for_tests())

    assert benefit["delta_edge_f1"] < 0.0
    assert benefit["delta_shd"] > 0
    assert benefit["fusion_helped"] is False


# ---------------------------------------------------------------------------
# Event metrics
# ---------------------------------------------------------------------------


def test_evaluate_events_scores_local_and_fused_against_the_oracle() -> None:
    oracle_events = [
        make_event("o-1", EventType.HARD_BRAKE, 1.0, participant_id="B",
                   provenance=Provenance.ORACLE),
        make_event("o-2", EventType.CRITICAL_TTC, 2.0, participant_id="A", subject="B",
                   provenance=Provenance.ORACLE),
        make_event("o-3", EventType.COLLISION, 3.0, participant_id="A",
                   provenance=Provenance.ORACLE),
    ]
    local = {
        "A": [
            make_event("a-2", EventType.CRITICAL_TTC, 2.2, participant_id="A", subject="A::T001"),
            make_event("a-3", EventType.COLLISION, 3.05, participant_id="A"),
        ],
        "B": [make_event("b-1", EventType.HARD_BRAKE, 1.1, participant_id="B")],
    }
    fused = [
        make_event("f-1", EventType.HARD_BRAKE, 1.1, participant_id="B",
                   provenance=Provenance.FUSED),
        make_event("f-2", EventType.CRITICAL_TTC, 2.2, participant_id="A", subject="A::T001",
                   provenance=Provenance.FUSED),
        make_event("f-3", EventType.COLLISION, 3.05, participant_id="A",
                   provenance=Provenance.FUSED),
    ]
    result = evaluate_events(local, fused, oracle_events, {"A::T001": "B"}, cfg_for_tests())

    assert result["per_participant"]["A"]["n_matched"] == 2
    assert result["per_participant"]["B"]["n_matched"] == 1
    assert result["best_local_participant_id"] == "A"
    assert result["fused"]["recall"] == 1.0
    assert result["fused"]["f1"] == 1.0
    assert result["delta_f1"] > 0.0
    assert result["fusion_helped"] is True
    assert result["fused"]["mean_abs_timing_error"] == pytest.approx(
        (0.1 + 0.2 + 0.05) / 3.0, abs=1e-9
    )
    # The matched pairs must survive so event_matches.csv can be written.
    assert len(result["fused_detail"]["matches"]) == 3


def test_evaluate_events_refuses_an_empty_reference() -> None:
    with pytest.raises(ValueError, match="non-empty oracle event list"):
        evaluate_events({"A": []}, [], [], None, cfg_for_tests())


# ---------------------------------------------------------------------------
# Attribution and the S10 epistemic check
# ---------------------------------------------------------------------------


S10_SPEC: Dict[str, Any] = {
    "scenario_id": "S10",
    "name": "signalized_limitation",
    "expected_local_unknowns": ["signal_violation"],
    "causal_template": [
        {
            "cause": {"kind": "action", "participant": "B", "action_id": "B_run_red_light"},
            "effect": {"kind": "oracle_state", "participant": "B", "name": "signal_violation"},
            "edge": "TRIGGERS",
        },
        {
            "cause": {"kind": "oracle_state", "participant": "B", "name": "signal_violation"},
            "effect": {"kind": "state", "participant": "B", "name": "conflict_entry"},
            "edge": "CONTRIBUTES_TO",
        },
    ],
}


def test_evaluate_local_unknowns_honest_when_the_claim_is_absent() -> None:
    """The system refused to claim the unobservable: honest, and the oracle does assert it."""
    local = {"causal:A": partial_chain("a"), "causal:B": partial_chain("b", owner="B")}
    fused = three_node_chain("f", scope=Provenance.FUSED, owner=None)

    result = evaluate_local_unknowns(S10_SPEC, local, fused, None, cfg_for_tests())

    assert result["honest"] is True
    assert result["hallucinated"] == []
    assert result["oracle_asserted"] == ["signal_violation"]
    assert result["vacuous_names"] == []
    assert result["findings"]["signal_violation"]["claimed_in"] == []


def test_evaluate_local_unknowns_catches_a_hallucinating_local_graph() -> None:
    """A local graph that names the unobservable quantity must fail the check."""
    hallucinating = partial_chain("a")
    hallucinating.nodes[0].values = {"signal_violation": 1.0}
    local = {"causal:A": hallucinating}
    fused = three_node_chain("f", scope=Provenance.FUSED, owner=None)

    result = evaluate_local_unknowns(S10_SPEC, local, fused, None, cfg_for_tests())

    assert result["honest"] is False
    assert result["hallucinated"] == ["signal_violation"]
    assert result["findings"]["signal_violation"]["claimed_in"] == ["local:causal:A"]
    # The oracle side still asserts it: the failure is the local claim, not the design.
    assert result["oracle_asserted"] == ["signal_violation"]


def test_evaluate_local_unknowns_scans_the_fused_graph_and_the_model_check() -> None:
    local = {"causal:A": partial_chain("a")}
    fused = three_node_chain("f", scope=Provenance.FUSED, owner=None)
    model_check = {
        "results": [
            {"property_id": "P9_signal_violation", "status": "FAIL", "participant_id": "B"}
        ]
    }
    result = evaluate_local_unknowns(S10_SPEC, local, fused, model_check, cfg_for_tests())
    assert result["honest"] is False
    assert "model_check" in result["findings"]["signal_violation"]["claimed_in"]


def test_evaluate_local_unknowns_not_applicable_without_a_declaration() -> None:
    result = evaluate_local_unknowns(
        {"scenario_id": "S01"}, {"causal:A": partial_chain("a")}, None, None, cfg_for_tests()
    )
    assert result["applicable"] is False
    assert result["honest"] is True


def test_oracle_initiators_exclude_preventive_actions() -> None:
    """A's late brake acts against the crash; counting it as a cause would be wrong."""
    spec = {
        "causal_template": [
            {
                "cause": {"kind": "action", "participant": "B", "action_id": "B_emergency_brake"},
                "effect": {"kind": "state", "participant": "A", "name": "closing"},
                "edge": "CONTRIBUTES_TO",
            },
            {
                "cause": {"kind": "action", "participant": "A", "action_id": "A_late_brake"},
                "effect": {"kind": "outcome", "name": "collision"},
                "edge": "PREVENTS",
            },
        ]
    }
    truth = oracle_causal_initiators(None, spec, cfg_for_tests())
    assert truth["action_ids"] == ["B_emergency_brake"]
    assert truth["preventive_action_ids"] == ["A_late_brake"]


def test_evaluate_attribution_scores_the_candidate_set_and_the_primary() -> None:
    spec = {
        "causal_template": [
            {
                "cause": {"kind": "action", "participant": "B", "action_id": "B_emergency_brake"},
                "effect": {"kind": "state", "participant": "A", "name": "closing"},
                "edge": "CONTRIBUTES_TO",
            },
            {
                "cause": {"kind": "action", "participant": "A", "action_id": "A_late_brake"},
                "effect": {"kind": "outcome", "name": "collision"},
                "edge": "PREVENTS",
            },
        ]
    }
    attribution = {
        "candidates": [
            {"action_id": "B_emergency_brake", "is_causal": True},
            {"action_id": "A_late_brake", "is_causal": True},
            {"action_id": "C_phantom", "is_causal": True, "insufficient_evidence": True},
        ],
        "primary_initiator": "B_emergency_brake",
        "classification": "single",
    }
    result = evaluate_attribution(attribution, None, spec, cfg_for_tests())

    assert result["reference_initiators"] == ["B_emergency_brake"]
    assert result["predicted_candidates"] == ["A_late_brake", "B_emergency_brake"]
    assert result["n_true_positive"] == 1
    assert result["n_false_positive"] == 1
    assert result["precision"] == pytest.approx(0.5)
    assert result["recall"] == 1.0
    assert result["primary_initiator"]["correct"] is True
    assert result["classification"]["reference"] == "single"
    assert result["classification"]["correct"] is True
    assert result["n_insufficient_evidence"] == 1
    # Explicitly not collapsed into one number.
    assert "fault_score" not in result


def test_evaluate_attribution_has_no_primary_when_the_scenario_is_ambiguous() -> None:
    spec = {
        "causal_template": [
            {
                "cause": {"kind": "action", "participant": "B", "action_id": "act_b"},
                "effect": {"kind": "outcome", "name": "collision"},
                "edge": "CONTRIBUTES_TO",
            },
            {
                "cause": {"kind": "action", "participant": "C", "action_id": "act_c"},
                "effect": {"kind": "outcome", "name": "collision"},
                "edge": "CONTRIBUTES_TO",
            },
        ]
    }
    result = evaluate_attribution(["act_b", "act_c"], None, spec, cfg_for_tests())
    assert result["primary_initiator"]["correct"] is None
    assert "unambiguous" in result["primary_initiator"]["reason"]
    assert result["classification"]["reference"] == "shared"
    assert result["classification"]["predicted"] == "shared"
    assert result["f1"] == 1.0


# ---------------------------------------------------------------------------
# Association (real evidence + real privileged trace)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not REAL_RUN.exists(), reason="the recorded S01 run is not present")
def test_true_track_identity_resolves_the_real_track_to_B() -> None:
    cfg = load_run_config("S01")
    run = load_run(REAL_RUN, with_radar=False)
    from cdf.common.io import read_jsonl_gz

    trace = read_jsonl_gz(RunLayout.from_run_dir(REAL_RUN).oracle_trace)
    identity = true_track_identities(run, trace, cfg)

    assert "A::T001" in identity
    entry = identity["A::T001"]
    assert entry["observer_id"] == "A"
    assert entry["true_participant"] == "B"
    assert entry["mean_distance_m"] is not None
    assert entry["mean_distance_m"] < 6.0


@pytest.mark.skipif(not REAL_RUN.exists(), reason="the recorded S01 run is not present")
def test_evaluate_association_on_the_real_run() -> None:
    cfg = load_run_config("S01")
    run = load_run(REAL_RUN, with_radar=False)
    layout = RunLayout.from_run_dir(REAL_RUN)
    from cdf.common.io import read_jsonl_gz

    trace = read_jsonl_gz(layout.oracle_trace)
    assignments = read_json(layout.association_report)["assignments"]

    result = evaluate_association(assignments, run, trace, cfg)

    # A's pre-impact track of B is the one that carries causal weight; the run
    # also holds short-lived post-impact tracks, so assert the scoring property
    # rather than a count frozen at the time this test was written.
    assert result["n_tracks"] >= 1
    assert result["n_incorrect"] == 0
    assert result["n_correct"] >= 1
    assert result["precision"] == 1.0
    by_id = {t["track_id"]: t for t in result["tracks"]}
    assert "A::T001" in by_id
    main = by_id["A::T001"]
    assert main["assigned_participant"] == "B"
    assert main["true_participant"] == "B"
    assert main["rmse_m"] < 3.0
    assert main["verdict"] == "correct"


def test_evaluate_association_counts_an_unresolved_track_as_a_miss() -> None:
    """Abstention is honest, but it must not be a free way to keep precision at 1.0."""

    class _FakeRun(object):
        participant_ids = ["A", "B"]

        def get(self, pid: str) -> Any:
            raise AssertionError("ground truth must come from the oracle delegate here")

    # A hand-made identity table keeps this test about the scoring rule only.
    identity = {"A::T001": {"observer_id": "A", "true_participant": "B"}}
    assignments = [
        {"track_id": "A::T001", "observer_id": "A", "assigned_participant": None,
         "status": "UNRESOLVED", "confidence": 0.1, "rmse_m": None, "overlap_s": 2.0}
    ]

    import cdf.evaluation.association_metrics as am

    original = am.true_track_identities
    am.true_track_identities = lambda run, trace, cfg: identity  # type: ignore[assignment]
    try:
        strict = am.evaluate_association(assignments, _FakeRun(), [], cfg_for_tests())
        lenient = am.evaluate_association(
            assignments,
            _FakeRun(),
            [],
            Config(
                {
                    "evaluation": {
                        "event_match": {"time_tolerance_s": 1.5},
                        "association": {"count_unresolved_as_miss": False},
                    }
                }
            ),
        )
    finally:
        am.true_track_identities = original  # type: ignore[assignment]

    assert strict["n_unresolved"] == 1
    assert strict["recall"] == 0.0
    assert lenient["recall"] == 0.0  # no true positive either way
    assert strict["count_unresolved_as_miss"] is True
    assert lenient["count_unresolved_as_miss"] is False


# ---------------------------------------------------------------------------
# The suite over the real run
# ---------------------------------------------------------------------------


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.skipif(not REAL_RUN.exists(), reason="the recorded S01 run is not present")
def test_evaluate_run_on_the_real_recording() -> None:
    cfg = load_run_config("S01")
    layout = RunLayout.from_run_dir(REAL_RUN)

    guarded = [
        layout.causal_graph("A"),
        layout.causal_graph("B"),
        layout.fused_causal_graph,
        layout.events("A"),
    ]
    before = {p: _digest(p) for p in guarded}

    metrics = evaluate_run(REAL_RUN, cfg)

    # 1. The evaluation never writes into a local or fused artifact.
    assert {p: _digest(p) for p in guarded} == before

    # 2. metrics.json exists, is valid JSON and round-trips.
    assert layout.metrics.exists()
    on_disk = read_json(layout.metrics)
    assert on_disk["run_id"] == read_json(layout.manifest)["run_id"]
    assert on_disk["scenario_id"] == "S01"
    assert on_disk["variant"] == "crash"
    assert on_disk["outcome"] == "collision"
    assert on_disk["participants"] == ["A", "B"]

    # 3. Real numbers where the inputs exist.
    assert metrics["subject_map"] == {"A::T001": "B"}
    reconstruction = metrics["reconstruction"]
    # Structural invariants of THIS recording rather than counts frozen at the
    # time the test was written: node counts move whenever an extraction
    # threshold is retuned, but these relationships must hold regardless.
    a_local = reconstruction["local_causal"]["A"]
    b_local = reconstruction["local_causal"]["B"]
    fused_recon = reconstruction["fused_causal"]
    assert a_local["n_nodes"] > 0 and a_local["n_edges"] > 0
    assert b_local["n_nodes"] > 0
    # A observed the interaction; B is the lead vehicle and saw only static world.
    assert a_local["n_nodes"] > b_local["n_nodes"]
    # Fusion may merge nodes but must not lose the richer view entirely.
    assert fused_recon["n_nodes"] >= a_local["n_nodes"]
    assert reconstruction["evidence"]["A"]["n_tracks"] >= 1
    assert reconstruction["evidence"]["B"]["n_tracks"] == 0

    association = metrics["association"]
    assert association is not None
    assert association["n_correct"] >= 1
    assert association["n_incorrect"] == 0
    assert association["f1"] == 1.0

    validation = metrics["scenario_validation"]
    assert validation is not None and validation["passed"] is True

    # 4. Every block is either a real computation or null WITH a reason. Which
    #    blocks are populated depends on how far the pipeline has been run over
    #    this recording, so assert the CONTRACT rather than a fixed set: never a
    #    silent zero standing in for a missing input.
    for block in ("events", "graphs", "fusion_benefit", "attribution", "model_check"):
        if metrics[block] is None:
            assert metrics["reasons"][block], "{0} must carry a reason".format(block)
            assert on_disk[block] is None
            assert metrics["available"][block] is False
        else:
            assert metrics["available"][block] is True
            assert on_disk[block] is not None
    assert metrics["available"]["association"] is True

    # 5. The CSV side-cars exist, with their headers, even when empty.
    assert layout.event_matches.exists()
    header = layout.event_matches.read_text(encoding="utf-8").splitlines()[0]
    assert header.split(",")[:5] == tables.EVENT_MATCH_COLUMNS[:5]
    assert layout.edge_matches.exists()
    assert layout.attribution_metrics.exists()
    side_car = read_json(layout.attribution_metrics)
    # Whether this block is populated depends on whether the counterfactual
    # campaign has been run over the reference recording, so assert the contract
    # rather than one state of it: a real computation, or null WITH a reason.
    if side_car["attribution"] is None:
        assert side_car["reasons"]["attribution"]
    else:
        assert "f1" in side_car["attribution"]
        assert "reference_initiators" in side_car["attribution"]


@pytest.mark.skipif(not REAL_RUN.exists(), reason="the recorded S01 run is not present")
def test_evaluate_run_is_deterministic() -> None:
    cfg = load_run_config("S01")
    layout = RunLayout.from_run_dir(REAL_RUN)
    evaluate_run(REAL_RUN, cfg)
    first = layout.metrics.read_bytes()
    evaluate_run(REAL_RUN, cfg)
    assert layout.metrics.read_bytes() == first


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------


def _fake_run_metrics(scenario_id: str, seed: int, edge_f1_fused: float) -> Dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "run_dir": "seed_{0:03d}".format(seed),
        "run_id": "{0}-seed{1:03d}".format(scenario_id, seed),
        "scenario_id": scenario_id,
        "variant": "crash",
        "seed": seed,
        "outcome": "collision",
        "n_participants": 2,
        "graphs": {
            "per_participant": {
                "A": {
                    "node_f1": 0.5,
                    "edge_f1": 0.4,
                    "structural_hamming_distance": 3,
                    "matched_edges": [],
                    "missing_edges": [
                        {"b_source": "o-1", "b_target": "o-2", "edge_type": CONTRIB}
                    ],
                    "extra_edges": [],
                    "reversed_edges": [],
                }
            },
            "fused": {
                "node_f1": 0.9,
                "edge_f1": edge_f1_fused,
                "structural_hamming_distance": 1,
                "matched_edges": [],
                "missing_edges": [],
                "extra_edges": [],
                "reversed_edges": [],
            },
            "best_single_local": {
                "participant_id": "A",
                "metrics": {"node_f1": 0.5, "edge_f1": 0.4, "structural_hamming_distance": 3},
            },
            "delta_edge_f1": edge_f1_fused - 0.4,
            "delta_node_f1": 0.4,
            "delta_shd": -2,
        },
        "fusion_benefit": {
            "best_local_participant_id": "A",
            "best_local": {"edge_f1": 0.4, "node_f1": 0.5, "structural_hamming_distance": 3},
            "fused": {"edge_f1": edge_f1_fused, "node_f1": 0.9, "structural_hamming_distance": 1},
            "delta_edge_f1": edge_f1_fused - 0.4,
            "delta_node_f1": 0.4,
            "delta_shd": -2,
            "fusion_helped": edge_f1_fused > 0.4,
            "n_nodes_gained": 1,
            "n_edges_gained": 1,
            "knowledge_gain": {"baseline_edge_recall": 0.5, "self_edge_recall": 1.0},
            "gained_nodes": [{"event_type": "HARD_BRAKE", "t_peak": 1.0}],
            "gained_edges": [
                {"source_type": "HARD_BRAKE", "target_type": "CRITICAL_TTC", "edge_type": CONTRIB}
            ],
        },
        "events": None,
        "association": None,
        "attribution": None,
        "local_unknowns": None,
        "model_check": None,
        "scenario_validation": {"passed": True, "expected_outcome": "collision", "problems": [],
                                "checks": {"min_separation": {"distance_m": 4.5},
                                           "collision_pairs": [{"a": "A", "b": "B", "t": 6.5}]}},
        "reasons": {"events": "no oracle event list"},
        "available": {"graphs": True},
    }


def test_aggregate_runs_excludes_replays_and_ablation_runs(tmp_path: Path) -> None:
    """A replay and an ablation run are different experiments, not campaign runs.

    Both carry a manifest and a metrics file, so a naive walk of the artifacts
    tree sweeps them into the campaign averages -- which then answer a question
    nobody asked: the mean over the recorded runs *plus* the deliberately
    degraded ones *plus* the ones whose scripted actions were removed.
    """
    root = tmp_path / "artifacts"

    def write_run(run_dir, scenario, seed, f1):
        (run_dir / "evaluation").mkdir(parents=True)
        (run_dir / "manifest.json").write_text(
            json.dumps({"run_id": "r", "scenario_id": scenario, "seed": seed}),
            encoding="utf-8",
        )
        (run_dir / "evaluation" / "metrics.json").write_text(
            json.dumps(_fake_run_metrics(scenario, seed, f1)), encoding="utf-8"
        )

    campaign = root / "S01_rear_end" / "seed_000"
    write_run(campaign, "S01", 0, 0.8)
    write_run(campaign / "counterfactual" / "replays" / "B_brake__disable", "S01", 0, 0.1)
    write_run(root / "ablation" / "radar_dropout" / "S01_rear_end" / "seed_000", "S01", 0, 0.2)

    summary = aggregate_runs(root, cfg_for_tests())

    assert summary["n_runs"] == 1
    assert summary["aggregates"]["edge_f1_fused"]["mean"] == pytest.approx(0.8)
    # Held out, but visibly so.
    assert summary["n_runs_excluded"] == 2
    kinds = sorted(r["kind"] for r in summary["excluded_runs"])
    assert kinds == ["ablation", "replay"]
    assert summary["n_runs_without_metrics"] == 0


def test_aggregate_runs_writes_every_summary_table(tmp_path: Path) -> None:
    root = tmp_path / "artifacts"
    for seed, f1 in ((0, 0.8), (1, 0.3)):
        run_dir = root / "S01_rear_end" / "seed_{0:03d}".format(seed)
        (run_dir / "evaluation").mkdir(parents=True)
        (run_dir / "manifest.json").write_text(
            json.dumps({"run_id": "r{0}".format(seed), "scenario_id": "S01", "seed": seed}),
            encoding="utf-8",
        )
        (run_dir / "evaluation" / "metrics.json").write_text(
            json.dumps(_fake_run_metrics("S01", seed, f1)), encoding="utf-8"
        )
    # A run that was never evaluated must be reported, not silently dropped.
    unevaluated = root / "S02_cut_in" / "seed_000"
    unevaluated.mkdir(parents=True)
    (unevaluated / "manifest.json").write_text(json.dumps({"scenario_id": "S02"}), encoding="utf-8")

    summary = aggregate_runs(root, cfg_for_tests())
    out = summary_dir(root)

    for name in (
        "runs.csv",
        "event_metrics.csv",
        "graph_metrics.csv",
        "fusion_metrics.csv",
        "association_metrics.csv",
        "attribution_metrics.csv",
        "model_check_metrics.csv",
        "scenario_validation.csv",
        "summary.json",
    ):
        assert (out / name).exists(), name
        assert (out / name).stat().st_size > 0

    assert summary["n_runs"] == 2
    assert summary["n_runs_without_metrics"] == 1
    assert summary["runs_without_metrics"][0]["run_dir"] == "seed_000"
    assert summary["outcomes"] == {"collision": 2}
    assert summary["by_scenario"]["S01"]["n_runs"] == 2
    assert summary["by_scenario"]["S01"]["n_validation_passed"] == 2
    assert summary["aggregates"]["edge_f1_fused"]["mean"] == pytest.approx(0.55)
    assert summary["aggregates"]["edge_f1_fused"]["n_available"] == 2
    # A block nobody could compute must not be averaged as zero.
    assert summary["aggregates"]["association_f1"]["mean"] is None
    assert summary["aggregates"]["association_f1"]["n_available"] == 0
    assert summary["n_runs_where_fusion_helped"] == 1
    assert summary["n_runs_with_fusion_comparison"] == 2

    runs_csv = (out / "runs.csv").read_text(encoding="utf-8").splitlines()
    assert runs_csv[0].split(",") == tables.RUN_COLUMNS
    assert len(runs_csv) == 3  # header + two runs

    graph_rows = (out / "graph_metrics.csv").read_text(encoding="utf-8").splitlines()
    assert len(graph_rows) == 5  # header + (local + fused) per run


def test_aggregate_runs_refuses_a_missing_root(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        aggregate_runs(tmp_path / "nope", cfg_for_tests())


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------


def test_tables_emit_no_rows_for_an_unavailable_block() -> None:
    metrics = {"scenario_id": "S01", "variant": "crash", "seed": 0, "run_id": "r",
               "run_dir": "seed_000", "events": None, "graphs": None, "association": None,
               "attribution": None, "model_check": None, "scenario_validation": None,
               "reasons": {"events": "absent"}}
    assert tables.event_match_rows(metrics) == []
    assert tables.edge_match_rows(metrics) == []
    assert tables.event_metrics_rows(metrics) == []
    assert tables.graph_metrics_rows(metrics) == []
    assert tables.association_metrics_rows(metrics) == []
    assert tables.attribution_metrics_rows(metrics) == []
    assert tables.model_check_rows(metrics) == []
    assert tables.scenario_validation_rows(metrics) == []
    row = tables.run_rows(metrics)[0]
    assert row["edge_f1_fused"] is None
    assert row["unavailable_blocks"] == "events"


def test_edge_match_rows_include_missing_edges() -> None:
    metrics = _fake_run_metrics("S01", 0, 0.8)
    metrics.update({"run_dir": "seed_000"})
    rows = tables.edge_match_rows(metrics)
    statuses = {r["status"] for r in rows}
    assert "missing" in statuses
    assert all(set(tables.EDGE_MATCH_COLUMNS) >= set(r.keys()) for r in rows)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------


def _assert_png(path: Path) -> None:
    assert path.exists(), path
    data = path.read_bytes()
    assert len(data) > 1000, "{0} is suspiciously small ({1} bytes)".format(path, len(data))
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "{0} is not a PNG".format(path)


@pytest.mark.skipif(not REAL_RUN.exists(), reason="the recorded S01 run is not present")
def test_every_figure_renders_from_the_real_run(tmp_path: Path) -> None:
    cfg = load_run_config("S01")
    run = load_run(REAL_RUN, with_radar=False)
    layout = RunLayout.from_run_dir(REAL_RUN)
    causal = load_graph(layout.causal_graph("A"), expect_scope=Provenance.LOCAL)
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)
    metrics = read_json(layout.metrics) if layout.metrics.exists() else evaluate_run(REAL_RUN, cfg)

    _assert_png(figures.plot_trajectories(run, tmp_path / "trajectories.png", cfg))
    _assert_png(figures.plot_ttc(run, tmp_path / "ttc.png", cfg))
    _assert_png(figures.plot_controls(run, tmp_path / "controls.png", cfg))
    _assert_png(figures.plot_graph(causal, tmp_path / "causal_A.png", cfg, title="vehicle A"))
    _assert_png(figures.plot_graph(fused, tmp_path / "causal_fused.png", cfg))
    _assert_png(
        figures.plot_association(metrics["association"], tmp_path / "association.png", cfg)
    )


def test_result_figures_render_from_synthetic_blocks(tmp_path: Path) -> None:
    oracle = three_node_chain("o", scope=Provenance.ORACLE, owner=None)
    local_a = partial_chain("a")
    fused = three_node_chain("f", scope=Provenance.FUSED, owner=None)
    cfg = cfg_for_tests()
    graphs = evaluate_graphs({"A": local_a}, fused, oracle, None, cfg)
    benefit = fusion_benefit({"A": local_a}, fused, oracle, cfg)
    attribution = evaluate_attribution(
        {"candidates": ["act_b"], "primary_initiator": "act_b"},
        None,
        {
            "causal_template": [
                {
                    "cause": {"kind": "action", "participant": "B", "action_id": "act_b"},
                    "effect": {"kind": "outcome", "name": "collision"},
                    "edge": "CONTRIBUTES_TO",
                }
            ]
        },
        cfg,
    )
    rows = [
        {"scenario_id": "S01", "variant": "crash", "seed": 0,
         "edge_f1_best_local": 0.4, "edge_f1_fused": 0.9},
        {"scenario_id": "S02", "variant": "crash", "seed": 0,
         "edge_f1_best_local": 0.6, "edge_f1_fused": 0.5},
    ]
    summary = {
        "outcomes": {"collision": 2, "near_miss": 1},
        "by_scenario": {"S01": {"n_runs": 2, "n_validation_passed": 2}},
    }

    _assert_png(figures.plot_local_vs_fused_f1(graphs, tmp_path / "f1.png", cfg))
    _assert_png(figures.plot_knowledge_gain(benefit, tmp_path / "gain.png", cfg))
    _assert_png(figures.plot_attribution(attribution, tmp_path / "attribution.png", cfg))
    _assert_png(figures.plot_robustness(rows, tmp_path / "robustness.png", cfg))
    _assert_png(figures.plot_scenario_outcomes(summary, tmp_path / "outcomes.png", cfg))

    check_rows = [
        {"property_id": "P1_brake_response", "participant_id": "A", "status": "PASS"},
        {"property_id": "P1_brake_response", "participant_id": "B", "status": "UNKNOWN"},
        {"property_id": "P2_no_throttle_while_closing", "participant_id": "A",
         "status": "FAIL"},
    ]
    _assert_png(figures.plot_model_check_verdicts(
        check_rows, tmp_path / "verdicts.png", cfg))


def test_figures_draw_an_explicit_no_data_annotation(tmp_path: Path) -> None:
    """A missing metric must be drawn as "no data", never as a zero-height bar."""
    cfg = cfg_for_tests()
    _assert_png(figures.plot_local_vs_fused_f1(None, tmp_path / "f1.png", cfg))
    _assert_png(figures.plot_knowledge_gain(None, tmp_path / "gain.png", cfg))
    _assert_png(figures.plot_attribution(None, tmp_path / "attribution.png", cfg))
    _assert_png(figures.plot_association(None, tmp_path / "association.png", cfg))
    _assert_png(figures.plot_robustness([], tmp_path / "robustness.png", cfg))
    _assert_png(figures.plot_scenario_outcomes({}, tmp_path / "outcomes.png", cfg))
    _assert_png(figures.plot_graph(None, tmp_path / "graph.png", cfg))
    _assert_png(figures.plot_model_check_verdicts([], tmp_path / "verdicts.png", cfg))
