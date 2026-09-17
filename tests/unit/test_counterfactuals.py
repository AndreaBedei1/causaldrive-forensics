"""Unit tests for the counterfactual layer: SCM, interventions, outcomes.

Everything here runs without CARLA. The replay driver itself needs a simulator,
so what is tested is the part that must be right *before* a replay is worth
running: which interventions get enumerated, whether the runner accepts them, and
whether the metrics extracted from a finished run are the ones a forensic report
would quote.

The oracle frames used below are hand-built so the expected impact speed, TTC and
separation are known exactly; the one test that touches real data reads the
recorded S01 run and asserts against its documented ground truth (A rear-ends B
at t = 6.55 s).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from cdf.causal.counterfactuals import (
    FACTUAL_ID,
    CounterfactualOutcome,
    _completed_replay,
    outcome_from_artifacts,
    outcome_from_run,
    replay_layout,
)
from cdf.causal.interventions import (
    InterventionSpec,
    enumerate_interventions,
    interventions_for_action,
)
from cdf.causal.scm import scm_from_graph
from cdf.common.config import Config, load_run_config
from cdf.common.io import write_json
from cdf.common.layout import RunLayout
from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from cdf.graph.export import load_graph
from cdf.simulation.controllers import ScriptedAction
from cdf.simulation.runner import _apply_intervention
from cdf.simulation.scenario_base import ScenarioSpec

REPO_ROOT = Path(__file__).resolve().parents[2]
S01_RUN = REPO_ROOT / "artifacts" / "S01_rear_end" / "seed_000_crash"


# ---------------------------------------------------------------------------
# Fixtures and doubles
# ---------------------------------------------------------------------------


@dataclass
class FakeSpec:
    """The two ``ScenarioSpec`` attributes ``outcome_from_run`` consults."""

    validation: Dict[str, Any] = field(default_factory=dict)
    expected_collision_pairs: List[List[str]] = field(default_factory=list)


@dataclass
class FakeRun:
    """A ``RunResult``-shaped double: no simulator, no artifacts on disk."""

    oracle_summary: Optional[Dict[str, Any]] = None
    validation: Dict[str, Any] = field(default_factory=dict)
    layout: Optional[RunLayout] = None
    spec: Optional[FakeSpec] = None


def actor(pid: str, x: float, vx: float, speed: float) -> Dict[str, Any]:
    """One participant's privileged state, travelling along +x."""
    return {"participant_id": pid, "x": x, "y": 0.0, "vx": vx, "vy": 0.0, "speed": speed}


#: A closes on a stationary B and strikes it between t=0.9 and t=1.0. The frame
#: stamped with the collision already carries the post-impact state, exactly as
#: the real oracle records it.
FRAMES: List[Dict[str, Any]] = [
    {"t": 0.8, "frame": 8, "actors": [actor("A", -2.0, 10.0, 10.0), actor("B", 0.0, 0.0, 0.0)]},
    {"t": 0.9, "frame": 9, "actors": [actor("A", -1.0, 10.0, 10.0), actor("B", 0.0, 0.0, 0.0)]},
    {"t": 1.0, "frame": 10, "actors": [actor("A", -0.2, 1.0, 1.0), actor("B", 0.0, 0.0, 0.0)]},
]

COLLIDED_SUMMARY: Dict[str, Any] = {
    "participants": ["A", "B"],
    "collision_pairs": [{"a": "B", "b": "A", "t": 1.0}],
}

CLEAN_SUMMARY: Dict[str, Any] = {"participants": ["A", "B"], "collision_pairs": []}


@pytest.fixture(scope="module")
def cfg() -> Config:
    return load_run_config(scenario_id="S01")


@pytest.fixture(scope="module")
def s01_spec(cfg: Config) -> ScenarioSpec:
    return ScenarioSpec.from_config(cfg, "crash")


# ---------------------------------------------------------------------------
# outcome_from_run
# ---------------------------------------------------------------------------


def test_outcome_from_run_extracts_collision_fields(cfg: Config) -> None:
    run = FakeRun(
        oracle_summary=COLLIDED_SUMMARY,
        validation={"passed": True, "checks": {"min_separation": {"t": 1.0, "distance_m": 0.35}}},
    )
    outcome = outcome_from_run(run, cfg, oracle_frames=FRAMES)

    assert outcome.intervention_id == FACTUAL_ID
    assert outcome.collision is True
    # The pair is canonicalised, so ("B", "A") is reported as ["A", "B"].
    assert outcome.collision_pairs == [["A", "B"]]
    assert outcome.t_collision == pytest.approx(1.0)
    # Last PRE-impact frame: A at 10 m/s, B stationary.
    assert outcome.impact_speed == pytest.approx(10.0)
    assert outcome.relative_impact_speed == pytest.approx(10.0)
    assert outcome.min_ttc == pytest.approx(0.1)
    # The runner's own validated separation wins over the trace-derived one.
    assert outcome.min_distance == pytest.approx(0.35)
    assert outcome.near_miss is False
    assert outcome.validation_passed is True


def test_outcome_from_run_falls_back_to_trace_for_separation(cfg: Config) -> None:
    run = FakeRun(oracle_summary=COLLIDED_SUMMARY, validation={"passed": True})
    outcome = outcome_from_run(run, cfg, oracle_frames=FRAMES)
    assert outcome.min_distance == pytest.approx(0.2)


def test_outcome_from_run_without_trace_leaves_severity_undefined(cfg: Config) -> None:
    """An unmeasurable severity stays unmeasurable: no silent zero."""
    run = FakeRun(oracle_summary=COLLIDED_SUMMARY, validation={"passed": True})
    outcome = outcome_from_run(run, cfg)

    assert outcome.collision is True
    assert outcome.impact_speed is None
    assert outcome.relative_impact_speed is None
    assert outcome.min_ttc is None
    assert outcome.min_distance == float("inf")
    assert outcome.to_dict()["min_distance"] is None
    assert any("oracle trace unavailable" in note for note in outcome.notes)


def test_outcome_from_run_identity_comes_from_the_intervention(cfg: Config) -> None:
    intervention = InterventionSpec(
        intervention_id="B_brake__disable",
        action_id="B_brake",
        op="disable",
        targets_participant="B",
    )
    outcome = outcome_from_run(
        FakeRun(oracle_summary=CLEAN_SUMMARY, validation={"passed": False}),
        cfg,
        intervention=intervention,
        oracle_frames=FRAMES,
    )
    assert outcome.intervention_id == "B_brake__disable"
    assert outcome.action_id == "B_brake"
    assert outcome.op == "disable"
    assert outcome.targets_participant == "B"
    assert outcome.collision is False
    assert outcome.is_factual is False


def test_outcome_from_run_flags_a_near_miss_without_collision(cfg: Config) -> None:
    run = FakeRun(
        oracle_summary=CLEAN_SUMMARY,
        validation={"passed": False, "checks": {"min_separation": {"distance_m": 1.2}}},
        spec=FakeSpec(validation={"encounter_pair": ["A", "B"]}),
    )
    outcome = outcome_from_run(run, cfg)
    assert outcome.collision is False
    assert outcome.near_miss is True


def test_outcome_from_run_wide_separation_is_not_a_near_miss(cfg: Config) -> None:
    run = FakeRun(
        oracle_summary=CLEAN_SUMMARY,
        validation={"passed": False, "checks": {"min_separation": {"distance_m": 40.0}}},
        spec=FakeSpec(validation={"encounter_pair": ["A", "B"]}),
    )
    outcome = outcome_from_run(run, cfg)
    assert outcome.collision is False
    assert outcome.near_miss is False


def test_outcome_from_run_requires_ground_truth(cfg: Config) -> None:
    with pytest.raises(ValueError) as excinfo:
        outcome_from_run(FakeRun(oracle_summary=None), cfg)
    assert "oracle summary" in str(excinfo.value)


def test_outcome_from_run_rejects_a_malformed_collision_record(cfg: Config) -> None:
    run = FakeRun(oracle_summary={"participants": ["A", "B"], "collision_pairs": [{"a": "A"}]})
    with pytest.raises(ValueError) as excinfo:
        outcome_from_run(run, cfg)
    assert "both participants" in str(excinfo.value)


def test_outcome_from_run_takes_the_earliest_collision_time(cfg: Config) -> None:
    summary = {
        "participants": ["A", "B", "C"],
        "collision_pairs": [
            {"a": "B", "b": "C", "t": 9.0},
            {"a": "A", "b": "B", "t": 7.25},
        ],
    }
    outcome = outcome_from_run(FakeRun(oracle_summary=summary), cfg)
    assert outcome.t_collision == pytest.approx(7.25)
    assert outcome.collision_pairs == [["A", "B"], ["B", "C"]]


# ---------------------------------------------------------------------------
# The recorded S01 run
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not S01_RUN.exists(), reason="the recorded S01 run is not present")
def test_outcome_from_artifacts_reads_the_recorded_s01_crash(cfg: Config) -> None:
    """Ground truth of the reference run: A rear-ends B at t = 6.55 s."""
    outcome = outcome_from_artifacts(S01_RUN, cfg)

    assert outcome.collision is True
    assert outcome.collision_pairs == [["A", "B"]]
    assert outcome.t_collision == pytest.approx(6.55, abs=1e-3)
    assert outcome.validation_passed is True
    # Pre-impact, not post-rebound: the striking vehicle was still doing ~7.9 m/s.
    assert outcome.impact_speed == pytest.approx(7.91, abs=0.05)
    assert outcome.relative_impact_speed == pytest.approx(7.88, abs=0.05)
    assert 0.0 < outcome.min_ttc < 1.0
    assert outcome.min_distance < 6.0


@pytest.mark.skipif(not S01_RUN.exists(), reason="the recorded S01 run is not present")
def test_scm_from_the_recorded_fused_graph(cfg: Config) -> None:
    layout = RunLayout.from_run_dir(S01_RUN)
    doc = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)
    model = scm_from_graph(doc, cfg)

    assert len(model) == len(doc.nodes)
    assert model.variables_of_kind("outcome"), "a crash reconstruction must have an outcome"
    order = model.topological_order()
    assert len(order) == len(model)
    for source, target in model.edges:
        assert order.index(source) < order.index(target)


# ---------------------------------------------------------------------------
# Structural causal model
# ---------------------------------------------------------------------------


def _event(event_id: str, event_type: EventType, t: float, pid: str = "A") -> Event:
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=pid,
        t_start=t - 0.1,
        t_peak=t,
        t_end=t + 0.1,
        values={"ttc_s": 1.25},
    )


def _causal_doc() -> GraphDocument:
    nodes = [
        _event("brake", EventType.HARD_BRAKE, 4.0, "B"),
        _event("closing", EventType.RAPID_CLOSING, 5.0, "A"),
        _event("crash", EventType.COLLISION, 6.0, "A"),
    ]
    edges = [
        GraphEdge("brake", "closing", CausalEdgeType.CONTRIBUTES_TO.value, confidence=0.7),
        GraphEdge("closing", "crash", CausalEdgeType.CAUSES_OUTCOME.value, confidence=0.9),
    ]
    return GraphDocument(graph_kind="causal", scope=Provenance.FUSED, nodes=nodes, edges=edges)


def test_scm_from_graph_classifies_variables(cfg: Config) -> None:
    model = scm_from_graph(_causal_doc(), cfg)
    assert model.variables_of_kind("action") == ["brake"]
    assert model.variables_of_kind("state") == ["closing"]
    assert model.variables_of_kind("outcome") == ["crash"]
    assert model.parents("crash") == ["closing"]
    assert model.children("brake") == ["closing"]
    assert model.ancestors("crash") == ["brake", "closing"]
    assert model.variables["brake"].observed_value == pytest.approx(1.25)
    assert model.topological_order() == ["brake", "closing", "crash"]


def test_scm_intervene_cuts_incoming_edges_only(cfg: Config) -> None:
    """do(X=x) mutilates the parents of X and leaves its children alone."""
    model = scm_from_graph(_causal_doc(), cfg)
    mutilated = model.intervene("closing", 0.0)

    assert mutilated.parents("closing") == []
    assert mutilated.children("closing") == ["crash"]
    assert mutilated.variables["closing"].observed_value == pytest.approx(0.0)
    # The original model is untouched: analysis must stay repeatable.
    assert model.parents("closing") == ["brake"]


def test_scm_from_graph_refuses_an_event_graph(cfg: Config) -> None:
    doc = GraphDocument(graph_kind="event", scope=Provenance.LOCAL, nodes=[], edges=[])
    with pytest.raises(ValueError) as excinfo:
        scm_from_graph(doc, cfg)
    assert "causal" in str(excinfo.value)


def test_scm_topological_order_reports_a_cycle(cfg: Config) -> None:
    doc = _causal_doc()
    doc.edges.append(
        GraphEdge("crash", "brake", CausalEdgeType.CONTRIBUTES_TO.value, confidence=0.5)
    )
    model = scm_from_graph(doc, cfg)
    with pytest.raises(ValueError) as excinfo:
        model.topological_order()
    assert "cycle" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Intervention enumeration
# ---------------------------------------------------------------------------


def test_enumerate_interventions_covers_both_s01_actions(
    s01_spec: ScenarioSpec, cfg: Config
) -> None:
    interventions = enumerate_interventions(s01_spec, None, cfg)
    by_action: Dict[str, List[InterventionSpec]] = {}
    for iv in interventions:
        by_action.setdefault(iv.action_id, []).append(iv)

    assert set(by_action) == {"B_emergency_brake", "A_late_brake"}
    for action_id, items in by_action.items():
        ops = [iv.op for iv in items]
        # A brake affords three meaningful questions: removed, weakened, earlier.
        assert ops == ["disable", "scale", "advance"], action_id
    assert by_action["B_emergency_brake"][0].targets_participant == "B"
    assert by_action["A_late_brake"][0].targets_participant == "A"
    assert len({iv.intervention_id for iv in interventions}) == len(interventions)


def test_every_s01_intervention_is_accepted_by_the_runner(
    s01_spec: ScenarioSpec, cfg: Config
) -> None:
    """The contract that matters: the runner must understand every spec emitted."""
    for iv in enumerate_interventions(s01_spec, None, cfg):
        modified = _apply_intervention(s01_spec, iv.as_runner_dict())
        actions = {a.action_id: a for p in modified.participants for a in p.actions}
        target = actions[iv.action_id]
        original = {a.action_id: a for p in s01_spec.participants for a in p.actions}[
            iv.action_id
        ]

        if iv.op == "disable":
            assert target.enabled is False
        elif iv.op == "advance":
            assert target.t_start == pytest.approx(
                max(0.0, original.t_start - iv.params["seconds"])
            )
        elif iv.op == "scale":
            key = iv.params["param"]
            assert target.params[key] == pytest.approx(
                original.params[key] * iv.params["factor"]
            )
        # The factual spec must not have been mutated by the replay preparation.
        assert original.enabled is True


def test_enumerate_interventions_uses_the_fused_graph_ranking(
    s01_spec: ScenarioSpec, cfg: Config
) -> None:
    """Graph-nominated actions are annotated with why they were chosen."""
    if not S01_RUN.exists():
        pytest.skip("the recorded S01 run is not present")
    doc = load_graph(
        RunLayout.from_run_dir(S01_RUN).fused_causal_graph, expect_scope=Provenance.FUSED
    )
    interventions = enumerate_interventions(s01_spec, doc, cfg)
    assert {iv.action_id for iv in interventions} == {"B_emergency_brake", "A_late_brake"}
    assert any("fused causal graph" in iv.description for iv in interventions)


def test_enumerate_interventions_respects_the_replay_budget(
    s01_spec: ScenarioSpec, cfg: Config
) -> None:
    capped = cfg.with_overrides({"counterfactual": {"max_interventions": 2}})
    interventions = enumerate_interventions(s01_spec, None, capped)
    assert len(interventions) == 2

    # The budget is spent BREADTH-FIRST: every candidate action is asked the
    # strongest question (remove it entirely) before any action is asked a
    # second, weaker one. Spending it depth-first would fill the budget with
    # variations of one action and silently leave another untested -- which on
    # the chain-collision scenario dropped the very action that distinguishes
    # its two variants.
    assert [iv.op for iv in interventions] == ["disable", "disable"]
    assert len({iv.action_id for iv in interventions}) == 2

    # With room for more, the second op of the first action appears only after
    # every action has had its first.
    wider = cfg.with_overrides({"counterfactual": {"max_interventions": 3}})
    three = enumerate_interventions(s01_spec, None, wider)
    assert [iv.op for iv in three][:2] == ["disable", "disable"]
    assert three[2].op != "disable"


def test_interventions_for_action_skips_no_ops(cfg: Config) -> None:
    """Advancing an action that already starts at t=0 would waste a replay."""
    action = ScriptedAction(
        action_id="A_brake", kind="brake", t_start=0.0, duration=3.0, params={"intensity": 0.9}
    )
    ops = [iv.op for iv in interventions_for_action(action, "A", cfg)]
    assert ops == ["disable", "scale"]


def test_interventions_for_action_by_kind(cfg: Config) -> None:
    set_speed = ScriptedAction(
        action_id="A_no_yield",
        kind="set_speed",
        t_start=0.5,
        duration=14.0,
        params={"target_speed": 11.5},
    )
    assert [iv.op for iv in interventions_for_action(set_speed, "A", cfg)] == [
        "disable",
        "scale",
    ]

    lane_shift = ScriptedAction(
        action_id="B_cut_in",
        kind="lane_shift",
        t_start=3.0,
        duration=2.0,
        params={"lateral_m": -3.5},
    )
    assert [iv.op for iv in interventions_for_action(lane_shift, "B", cfg)] == [
        "disable",
        "advance",
        "delay",
    ]

    hold = ScriptedAction(
        action_id="B_hold", kind="hold", t_start=1.0, duration=5.0, params={"target_speed": 9.0}
    )
    assert [iv.op for iv in interventions_for_action(hold, "B", cfg)] == ["disable"]


def test_intervention_spec_validates_its_parameters() -> None:
    with pytest.raises(ValueError):
        InterventionSpec("x", "A_brake", "teleport", {})
    with pytest.raises(ValueError):
        InterventionSpec("x", "A_brake", "scale", {"param": "intensity"})
    with pytest.raises(ValueError):
        InterventionSpec("x", "", "disable", {})


def test_as_runner_dict_carries_only_runner_keys() -> None:
    iv = InterventionSpec(
        intervention_id="A_brake__scale_intensity_0_4",
        action_id="A_brake",
        op="scale",
        params={"param": "intensity", "factor": 0.4},
        description="anything at all",
        targets_participant="A",
    )
    assert iv.as_runner_dict() == {
        "intervention_id": "A_brake__scale_intensity_0_4",
        "action_id": "A_brake",
        "op": "scale",
        "param": "intensity",
        "factor": 0.4,
    }


# ---------------------------------------------------------------------------
# Replay isolation
# ---------------------------------------------------------------------------


def test_replay_layout_never_shadows_the_factual_run(tmp_path: Path) -> None:
    factual = RunLayout.create(str(tmp_path), "S01", "rear_end", 0, "crash")
    first = replay_layout(factual, "B_emergency_brake__disable")
    second = replay_layout(factual, "A_late_brake__disable")

    assert first.root != second.root != factual.root
    assert first.root.is_dir() and second.root.is_dir()
    assert factual.counterfactual_dir in first.root.parents
    assert first.manifest != factual.manifest
    assert first.oracle_trace != factual.oracle_trace


def test_suite_records_a_failed_replay_and_keeps_going(
    s01_spec: ScenarioSpec, cfg: Config, tmp_path: Path, monkeypatch: Any
) -> None:
    """One broken replay must not cost the suite the replays that did work.

    The simulator is replaced by a stub so the driver itself -- isolation,
    failure handling, artifact writing -- is exercised without CARLA. The stub
    returns a prevented collision for the first intervention and raises for the
    second, which is exactly the situation a flaky server produces.
    """
    import cdf.causal.counterfactuals as module

    seen: List[str] = []

    def fake_run_scenario(client, config, spec, seed, **kwargs):
        intervention = kwargs["intervention"]
        layout = kwargs["layout"]
        seen.append(intervention["intervention_id"])
        if intervention["action_id"] == "A_late_brake":
            raise RuntimeError("simulator lost the connection")
        return FakeRun(
            oracle_summary=CLEAN_SUMMARY,
            validation={"passed": False, "checks": {"min_separation": {"distance_m": 22.0}}},
            layout=layout,
        )

    monkeypatch.setattr(module, "run_scenario", fake_run_scenario)

    interventions = [
        InterventionSpec(
            "B_emergency_brake__disable", "B_emergency_brake", "disable", {}, "", "B"
        ),
        InterventionSpec("A_late_brake__disable", "A_late_brake", "disable", {}, "", "A"),
    ]
    factual = CounterfactualOutcome(
        intervention_id=FACTUAL_ID,
        collision=True,
        collision_pairs=[["A", "B"]],
        t_collision=6.55,
        impact_speed=7.9,
        relative_impact_speed=7.88,
        min_distance=4.47,
        validation_passed=True,
    )

    result = module.run_counterfactual_suite(
        session=object(),
        cfg=cfg,
        spec=s01_spec,
        seed=0,
        interventions=interventions,
        artifacts_root=str(tmp_path),
        factual_outcome=factual,
    )

    assert seen == ["B_emergency_brake__disable", "A_late_brake__disable"]
    assert len(result["outcomes"]) == 1
    assert len(result["failures"]) == 1
    assert "simulator lost the connection" in result["failures"][0]["error"]

    layout = result["layout"]
    assert layout.counterfactual_manifest.exists()
    assert layout.intervention_results.exists()
    assert layout.causal_contribution.exists()

    from cdf.common.io import read_json

    manifest = read_json(layout.counterfactual_manifest)
    assert manifest["n_requested"] == 2
    assert manifest["n_completed"] == 1
    assert manifest["n_failed"] == 1
    assert manifest["replay_dirs"]["A_late_brake__disable"].startswith("counterfactual/replays/")

    contribution = read_json(layout.causal_contribution)
    verdict = contribution["classification"]
    assert verdict["attribution_class"] == "single_initiator"
    assert verdict["primary_initiator"] == "B_emergency_brake"
    # The replay that never produced evidence is reported as missing, not as a
    # hypothesis that was tested and rejected.
    assert "A_late_brake" not in verdict["scores"]
    assert any("A_late_brake__disable" in note for note in contribution["notes"])

    csv_text = layout.intervention_results.read_text(encoding="utf-8")
    assert "factual" in csv_text and "failed" in csv_text


def test_counterfactual_outcome_serialises_without_nonfinite_floats() -> None:
    outcome = CounterfactualOutcome(intervention_id="iv", min_distance=float("inf"))
    data = outcome.to_dict()
    assert data["min_distance"] is None
    assert data["collision"] is False
    assert data["collision_pairs"] == []


# ---------------------------------------------------------------------------
# Resuming an interrupted suite
# ---------------------------------------------------------------------------


def _persist_replay(root, cfg: Config, config_hash: str = None) -> RunLayout:
    """A replay directory that looks exactly like one a finished replay leaves."""
    layout = RunLayout.create(root, "S01", "rear_end", 0, "crash").ensure()
    write_json(layout.manifest, {
        "scenario_id": "S01",
        "variant": "crash",
        "seed": 0,
        "config_hash": cfg.hash if config_hash is None else config_hash,
    })
    write_json(layout.oracle_dir / "oracle_summary.json", COLLIDED_SUMMARY)
    write_json(layout.scenario_validation, {"passed": True})
    return layout


def test_completed_replay_is_reused(tmp_path, cfg: Config) -> None:
    """A replay recorded under this configuration is not simulated again."""
    layout = _persist_replay(tmp_path, cfg)
    spec = InterventionSpec(
        intervention_id="B_emergency_brake__disable",
        action_id="B_emergency_brake",
        op="disable",
        targets_participant="B",
    )

    outcome = _completed_replay(layout, cfg, spec)

    assert outcome is not None
    assert outcome.collision is True
    # The identity comes from the intervention being resumed, not from the run.
    assert outcome.intervention_id == "B_emergency_brake__disable"
    assert outcome.action_id == "B_emergency_brake"


def test_replay_recorded_under_another_config_is_rerun(tmp_path, cfg: Config) -> None:
    """Different thresholds mean it is not the replay this suite is asking for."""
    layout = _persist_replay(tmp_path, cfg, config_hash="0000000000000000")
    spec = InterventionSpec(
        intervention_id="B_emergency_brake__disable",
        action_id="B_emergency_brake",
        op="disable",
        targets_participant="B",
    )

    assert _completed_replay(layout, cfg, spec) is None


def test_half_finished_replay_is_rerun(tmp_path, cfg: Config) -> None:
    """A manifest without the oracle summary is an interrupted run, not a result."""
    layout = _persist_replay(tmp_path, cfg)
    (layout.oracle_dir / "oracle_summary.json").unlink()
    spec = InterventionSpec(
        intervention_id="B_emergency_brake__disable",
        action_id="B_emergency_brake",
        op="disable",
        targets_participant="B",
    )

    assert _completed_replay(layout, cfg, spec) is None


def test_missing_replay_is_rerun(tmp_path, cfg: Config) -> None:
    layout = RunLayout.create(tmp_path, "S01", "rear_end", 0, "crash")
    spec = InterventionSpec(
        intervention_id="B_emergency_brake__disable",
        action_id="B_emergency_brake",
        op="disable",
        targets_participant="B",
    )

    assert _completed_replay(layout, cfg, spec) is None
