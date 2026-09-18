"""Unit tests for the privileged oracle layer.

These tests encode the properties that make the oracle usable as the reference
the rest of the pipeline is scored against:

* it **measures** rather than infers -- on the real S01 run it finds exactly one
  true collision, at the time the simulator recorded it, and one event per
  scripted action that actually fired;
* it **instantiates the designed causal structure** -- the S01 template's chain
  from B's emergency brake to the impact exists as a path in the causal DAG, and
  the document is acyclic;
* it **refuses to invent** -- a template entry whose cause never occurred is
  dropped and reported, not drawn anyway;
* it answers association **after** the fact -- ``true_track_identity`` names the
  vehicle A's radar track was really on;
* and it is **independent of the local rule engine**, which is asserted by
  reading the oracle package's own source rather than by convention.

The real-run tests are the ones that would catch a regression against actual
CARLA output; the synthetic traces cover the branches that run S01 never reaches
(traffic-light violations, unrealised template edges, cyclic templates).
"""

from __future__ import annotations

import ast
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import networkx as nx
import pytest

from cdf.common.config import load_run_config, repo_root
from cdf.common.evidence import load_participant
from cdf.common.io import read_json
from cdf.common.layout import RunLayout
from cdf.common.schemas import Event, EventType, Provenance, make_event_id
from cdf.graph.export import load_graph, to_networkx
from cdf.oracle import events as oracle_events
from cdf.oracle import evaluator as oracle_evaluator
from cdf.oracle import graph as oracle_graph
from cdf.oracle.events import build_oracle_events, load_oracle_trace, pair_kinematics
from cdf.oracle.evaluator import oracle_outcome, oracle_summary, true_track_identity
from cdf.oracle.graph import (
    build_and_persist,
    build_oracle_causal_graph,
    build_oracle_event_graph,
    persist_oracle,
)

DT = 0.05
REAL_RUN = repo_root() / "artifacts" / "S01_rear_end" / "seed_000_crash"
S01_IMPACT_T = 6.55


# ---------------------------------------------------------------------------
# Fixtures: the real run
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def cfg():
    return load_run_config(scenario_id="S01")


@pytest.fixture(scope="module")
def s01_spec(cfg):
    from cdf.simulation.scenario_base import ScenarioSpec

    return ScenarioSpec.from_config(cfg, "crash")


@pytest.fixture(scope="module")
def s01_trace():
    if not (REAL_RUN / "oracle" / "oracle_trace.jsonl.gz").exists():
        pytest.skip("reference run {0} is not present".format(REAL_RUN))
    return load_oracle_trace(REAL_RUN)


@pytest.fixture(scope="module")
def s01_events(s01_trace, s01_spec, cfg):
    return build_oracle_events(s01_trace, s01_spec, cfg)


# ---------------------------------------------------------------------------
# Fixtures: synthetic traces
# ---------------------------------------------------------------------------


class _Spec(object):
    """Minimal stand-in for :class:`~cdf.simulation.scenario_base.ScenarioSpec`.

    The oracle builders read a scenario only through ``causal_template``,
    ``participant_ids``, ``scenario_id`` and ``variant``, so a synthetic test can
    supply exactly those without needing the simulator to build a real spec.
    """

    def __init__(
        self,
        participant_ids: Sequence[str],
        causal_template: Optional[List[Dict[str, Any]]] = None,
        scenario_id: str = "SYN",
        variant: str = "default",
    ) -> None:
        self.participant_ids = list(participant_ids)
        self.causal_template = list(causal_template or [])
        self.scenario_id = scenario_id
        self.variant = variant


def _actor(
    pid: str,
    actor_id: int,
    x: float,
    y: float,
    vx: float,
    vy: float,
    yaw: float = 0.0,
    brake: float = 0.0,
    is_junction: bool = False,
    junction_id: Optional[int] = None,
    traffic_light_state: Optional[str] = None,
) -> Dict[str, Any]:
    """One privileged actor row, shaped exactly like :class:`OracleActorState`."""
    return {
        "participant_id": pid,
        "actor_id": actor_id,
        "x": x,
        "y": y,
        "z": 0.0,
        "yaw": yaw,
        "pitch": 0.0,
        "roll": 0.0,
        "vx": vx,
        "vy": vy,
        "vz": 0.0,
        "speed": math.hypot(vx, vy),
        "ax": 0.0,
        "ay": 0.0,
        "az": 0.0,
        "yaw_rate": 0.0,
        "throttle": 0.0,
        "brake": brake,
        "steer": 0.0,
        "lane_id": -1,
        "road_id": 1,
        "section_id": 0,
        "is_junction": is_junction,
        "junction_id": junction_id,
        "traffic_light_state": traffic_light_state,
        "traffic_light_id": None if traffic_light_state is None else 7,
        "is_at_traffic_light": traffic_light_state is not None,
    }


def _trace(
    frames: List[Dict[str, Any]],
    participants: Sequence[str],
    interventions: Optional[Dict[str, Any]] = None,
    collisions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Assemble a trace mapping shaped like :func:`load_oracle_trace`'s output."""
    collisions = list(collisions or [])
    pairs: Dict[Any, float] = {}
    for c in collisions:
        other = c.get("other_participant_id")
        if other is None:
            continue
        key = tuple(sorted([c["participant_id"], other]))
        pairs.setdefault(key, float(c["t"]))
    summary = {
        "run_id": "SYN-run",
        "scenario_id": "SYN",
        "seed": 0,
        "variant": "default",
        "participants": list(participants),
        "collisions": collisions,
        "collision_pairs": [{"a": k[0], "b": k[1], "t": t} for k, t in sorted(pairs.items())],
        "interventions": interventions or {},
        "notes": [],
    }
    return {
        "frames": frames,
        "summary": summary,
        "participants": list(participants),
        "collisions": collisions,
        "collision_pairs": summary["collision_pairs"],
        "run_dir": "<synthetic>",
    }


def _rear_end_trace(
    n_frames: int = 37, impact_t: float = 1.80, with_disabled_action: bool = True
) -> Dict[str, Any]:
    """A stopped lead vehicle B and a follower A closing at a constant 14 m/s.

    Exact by construction: the gap is ``30 - 14 t`` metres and the range rate is
    a flat ``-14`` m/s, so every derived quantity in the test has a closed form.
    """
    frames: List[Dict[str, Any]] = []
    for k in range(n_frames):
        t = round((k + 1) * DT, 10)
        ax = 14.0 * t
        avx = 14.0
        if t > impact_t:
            # After the impact both vehicles are at rest at the contact point.
            ax = 14.0 * impact_t
            avx = 0.0
        frames.append(
            {
                "t": t,
                "frame": 1000 + k,
                "actors": [
                    _actor("A", 11, ax, 0.0, avx, 0.0),
                    _actor("B", 12, 30.0, 0.0, 0.0, 0.0, brake=1.0),
                ],
                "traffic_lights": [],
            }
        )

    actions = [
        {
            "action_id": "B_stop",
            "kind": "stop",
            "t_start": 0.20,
            "duration": 5.0,
            "params": {"intensity": 1.0},
            "enabled": True,
        }
    ]
    if with_disabled_action:
        actions.append(
            {
                "action_id": "B_never",
                "kind": "brake",
                "t_start": 0.40,
                "duration": 1.0,
                "params": {"intensity": 0.5},
                "enabled": False,
            }
        )
    collisions = [
        {
            "t": impact_t,
            "frame": 1036,
            "participant_id": "A",
            "other_participant_id": "B",
            "other_actor_id": 12,
            "other_type_id": "vehicle.x",
            "impulse": 1234.5,
            "is_participant_pair": True,
        },
        {
            "t": impact_t,
            "frame": 1036,
            "participant_id": "B",
            "other_participant_id": "A",
            "other_actor_id": 11,
            "other_type_id": "vehicle.y",
            "impulse": 1234.5,
            "is_participant_pair": True,
        },
    ]
    return _trace(
        frames,
        ["A", "B"],
        interventions={"B": {"participant_id": "B", "actions": actions}},
        collisions=collisions,
    )


def _red_light_trace() -> Dict[str, Any]:
    """B approaches a red light and drives into the junction anyway; A has green.

    Reproduces the shape CARLA actually logs: the governing light is reported
    only while the vehicle is *approaching* it, and reads ``None`` once the
    vehicle is inside the junction.
    """
    frames: List[Dict[str, Any]] = []
    for k in range(40):
        t = round((k + 1) * DT, 10)
        b_in_junction = t >= 1.0
        b_light = None if (b_in_junction or t < 0.5) else "Red"
        a_in_junction = t >= 1.1
        a_light = None if (a_in_junction or t < 0.5) else "Green"
        frames.append(
            {
                "t": t,
                "frame": 2000 + k,
                "actors": [
                    _actor(
                        "A",
                        21,
                        -20.0 + 12.0 * t,
                        0.0,
                        12.0,
                        0.0,
                        yaw=0.0,
                        is_junction=a_in_junction,
                        junction_id=838 if a_in_junction else None,
                        traffic_light_state=a_light,
                    ),
                    _actor(
                        "B",
                        22,
                        0.0,
                        -20.0 + 12.0 * t,
                        0.0,
                        12.0,
                        yaw=90.0,
                        is_junction=b_in_junction,
                        junction_id=838 if b_in_junction else None,
                        traffic_light_state=b_light,
                    ),
                ],
                "traffic_lights": [],
            }
        )
    return _trace(
        frames,
        ["A", "B"],
        interventions={
            "B": {
                "participant_id": "B",
                "actions": [
                    {
                        "action_id": "B_run_red_light",
                        "kind": "set_speed",
                        "t_start": 0.10,
                        "duration": 4.0,
                        "params": {"target_speed": 12.0},
                        "enabled": True,
                    }
                ],
            }
        },
    )


# ---------------------------------------------------------------------------
# Real run: measured events
# ---------------------------------------------------------------------------


def test_real_run_yields_exactly_one_true_collision(s01_events):
    """The oracle reports the one impact CARLA recorded, at the time it happened."""
    collisions = [e for e in s01_events if e.event_type is EventType.COLLISION]
    assert len(collisions) == 1, [
        (e.participant_id, e.owners, e.t_peak) for e in collisions
    ]

    impact = collisions[0]
    assert sorted(impact.owners) == ["A", "B"]
    assert impact.t_peak == pytest.approx(S01_IMPACT_T, abs=0.1)
    assert impact.t_start == pytest.approx(impact.t_peak)
    # A recorded contact is not a threshold crossing: it is certain.
    assert impact.confidence == 1.0
    assert impact.provenance is Provenance.ORACLE
    assert impact.values["impulse"] > 0.0
    # Read from the last pre-contact sample, so it is the speed that did the damage.
    assert impact.values["relative_speed_mps"] > 1.0


def test_real_run_emits_one_event_per_enabled_scripted_action(s01_trace, s01_events):
    """Every action the controller actually ran becomes an oracle action event."""
    enabled = {
        action["action_id"]
        for block in s01_trace["summary"]["interventions"].values()
        for action in block["actions"]
        if action.get("enabled", True)
    }
    assert enabled, "the reference run declares no scripted actions"

    emitted = [
        e for e in s01_events if e.event_type is EventType.ORACLE_SCRIPTED_INTERVENTION
    ]
    assert {e.subject for e in emitted} >= enabled
    for event in emitted:
        assert event.confidence == 1.0
        assert event.provenance is Provenance.ORACLE
        assert event.t_end is not None and event.t_end >= event.t_start


def test_real_run_state_events_are_not_overconfident(s01_events):
    """Thresholded states carry less than full confidence; exact facts carry 1.0."""
    thresholded = [
        e
        for e in s01_events
        if e.event_type in (EventType.RANGE_DECREASING, EventType.CRITICAL_TTC)
    ]
    assert thresholded
    for event in thresholded:
        assert 0.0 < event.confidence < 1.0
        assert event.values["oracle_state"] in ("closing", "critical_ttc")
        assert event.subject == event.values["oracle_state"]
        assert sorted(event.owners) == ["A", "B"]


def test_build_oracle_events_is_deterministic(s01_trace, s01_spec, cfg):
    """Two builds of one trace agree byte for byte, ids included."""
    first = build_oracle_events(s01_trace, s01_spec, cfg)
    second = build_oracle_events(s01_trace, s01_spec, cfg)
    assert [e.event_id for e in first] == [e.event_id for e in second]
    assert [e.t_peak for e in first] == [e.t_peak for e in second]


# ---------------------------------------------------------------------------
# Real run: graphs
# ---------------------------------------------------------------------------


def test_s01_causal_graph_realises_the_template(s01_events, s01_trace, s01_spec, cfg):
    """B's emergency brake is an ancestor of the impact, and the graph is a DAG."""
    doc = build_oracle_causal_graph(s01_events, s01_trace, s01_spec, cfg)

    assert doc.graph_kind == "causal"
    assert doc.scope is Provenance.ORACLE
    assert doc.owner is None
    assert doc.meta["unrealised_template_edges"] == []
    assert doc.meta["n_realised_template_edges"] == doc.meta["n_template_edges"]

    g = to_networkx(doc)
    assert nx.is_directed_acyclic_graph(g)

    impact = [n for n in doc.nodes if n.event_type is EventType.COLLISION]
    assert len(impact) == 1
    brake = [
        n
        for n in doc.nodes
        if n.event_type is EventType.ORACLE_SCRIPTED_INTERVENTION
        and n.subject == "B_emergency_brake"
    ]
    assert len(brake) == 1

    ancestors = nx.ancestors(g, impact[0].event_id)
    assert brake[0].event_id in ancestors, (
        "the designed chain B_emergency_brake -> closing -> critical_ttc -> collision "
        "is not connected in the oracle causal graph"
    )
    assert nx.has_path(g, brake[0].event_id, impact[0].event_id)

    for edge in doc.edges:
        assert edge.provenance is Provenance.ORACLE
        assert edge.confidence == 1.0
        assert edge.rule in (
            oracle_graph.TEMPLATE_RULE,
            oracle_graph.MECHANICAL_RULE,
        )
        assert len(edge.evidence) == 2


def test_s01_endpoint_relaxation_picks_the_episode_after_its_cause(
    s01_events, s01_trace, s01_spec, cfg
):
    """``closing`` holds twice in S01; the chain must use the one B's brake caused."""
    closing = [
        e
        for e in s01_events
        if e.event_type is EventType.RANGE_DECREASING
        and e.participant_id == "A"
        and e.subject == "closing"
    ]
    assert len(closing) >= 2, "S01 is expected to contain an early spawn transient too"

    doc = build_oracle_causal_graph(s01_events, s01_trace, s01_spec, cfg)
    brake = next(
        n for n in doc.nodes if n.subject == "B_emergency_brake"
    )
    # Restrict to template edges: the brake also gains a ground-truth mechanical
    # edge to the deceleration it produced, and this assertion is about which
    # `closing` episode the TEMPLATE edge relaxed onto.
    used = [
        doc.node_by_id(e.target)
        for e in template_edges(doc)
        if e.source == brake.event_id
    ]
    assert len(used) == 1
    assert used[0].t_start >= brake.t_start


def test_oracle_event_graph_relates_both_participants(s01_events, s01_trace, s01_spec, cfg):
    """The privileged event graph spans participants, unlike any local one."""
    doc = build_oracle_event_graph(s01_events, s01_trace, s01_spec, cfg)

    assert doc.graph_kind == "event"
    assert doc.scope is Provenance.ORACLE
    assert doc.owner is None
    assert len(doc.nodes) == len(s01_events)
    assert doc.meta["edge_counts"].get("PRECEDES", 0) > 0

    cross = [
        e
        for e in doc.edges
        if e.edge_type == "INTERACTS_WITH"
        and doc.node_by_id(e.source).participant_id
        != doc.node_by_id(e.target).participant_id
    ]
    assert cross, "no INTERACTS_WITH edge relates A's and B's events"
    assert to_networkx(doc).number_of_nodes() == len(s01_events)


def test_persist_oracle_writes_every_artifact(tmp_path, s01_events, s01_trace, s01_spec, cfg):
    """All five oracle artifacts land under ``oracle/`` and reload with ORACLE scope."""
    event_graph = build_oracle_event_graph(s01_events, s01_trace, s01_spec, cfg)
    causal_graph = build_oracle_causal_graph(s01_events, s01_trace, s01_spec, cfg)
    persist_oracle(tmp_path, s01_events, event_graph, causal_graph)

    layout = RunLayout.from_run_dir(tmp_path)
    assert layout.oracle_events.exists()
    assert layout.oracle_event_graph.exists()
    assert layout.oracle_event_graph.with_suffix(".graphml").exists()
    assert layout.oracle_causal_graph.exists()
    assert layout.oracle_causal_graphml.exists()

    payload = read_json(layout.oracle_events)
    assert payload["provenance"] == "oracle"
    assert payload["n_events"] == len(s01_events)

    reloaded = load_graph(layout.oracle_causal_graph, expect_scope=Provenance.ORACLE)
    assert len(reloaded.nodes) == len(causal_graph.nodes)
    assert len(reloaded.edges) == len(causal_graph.edges)

    with pytest.raises(ValueError):
        load_graph(layout.oracle_causal_graph, expect_scope=Provenance.LOCAL)


def test_build_and_persist_round_trip(tmp_path, s01_spec, cfg):
    """The end-to-end entry point reproduces the step-by-step result."""
    run_dir = tmp_path / "run"
    (run_dir / "oracle").mkdir(parents=True)
    source = RunLayout.from_run_dir(REAL_RUN)
    target = RunLayout.from_run_dir(run_dir)
    target.oracle_trace.write_bytes(source.oracle_trace.read_bytes())
    (target.oracle_dir / "oracle_summary.json").write_bytes(
        (source.oracle_dir / "oracle_summary.json").read_bytes()
    )

    events, event_graph, causal_graph = build_and_persist(run_dir, s01_spec, cfg)
    assert events and event_graph.nodes and causal_graph.nodes
    assert target.oracle_events.exists()
    assert target.oracle_causal_graphml.exists()


# ---------------------------------------------------------------------------
# Real run: association ground truth
# ---------------------------------------------------------------------------


def test_true_track_identity_names_b_for_a_s_only_track(s01_trace, cfg):
    """A::T001 was really looking at B -- the answer fusion had to infer."""
    if not (REAL_RUN / "vehicle_A" / "tracks.jsonl.gz").exists():
        pytest.skip("reference run has no local track evidence")
    evidence = load_participant(REAL_RUN, "A")
    samples = [s for s in evidence.tracks if s.track_id == "A::T001"]
    assert samples, "the reference run is expected to contain track A::T001"

    assert true_track_identity(s01_trace, "A", samples, cfg) == "B"
    # The observer can never be the answer, and an empty track has no answer.
    assert true_track_identity(s01_trace, "B", samples, cfg) != "B"
    assert true_track_identity(s01_trace, "A", [], cfg) is None


def test_true_track_identity_refuses_a_track_on_nothing(s01_trace, cfg):
    """A track sitting far from every vehicle gets ``None``, not a nearest guess."""
    ghost = [{"t": 1.0 + 0.05 * k, "gx": 500.0, "gy": 500.0} for k in range(40)]
    assert true_track_identity(s01_trace, "A", ghost, cfg) is None


def test_oracle_outcome_matches_the_recorded_collision(s01_trace, cfg):
    """The true outcome is a collision between A and B, with a non-zero impact speed."""
    outcome = oracle_outcome(s01_trace, cfg)
    assert outcome["outcome"] == "collision"
    assert outcome["collision_order"] == [["A", "B"]]
    (pair,) = outcome["collision_pairs"]
    assert pair["t"] == pytest.approx(S01_IMPACT_T, abs=0.1)
    assert pair["impulse"] > 0.0
    assert pair["relative_speed_mps"] > 1.0
    assert outcome["min_separation"]["A|B"]["distance_m"] < 6.0


def test_oracle_summary_reads_only(cfg):
    """The run-level summary reports the real run without touching it."""
    if not (REAL_RUN / "oracle" / "oracle_trace.jsonl.gz").exists():
        pytest.skip("reference run {0} is not present".format(REAL_RUN))
    before = sorted(p.name for p in (REAL_RUN / "oracle").iterdir())
    summary = oracle_summary(REAL_RUN, cfg)
    after = sorted(p.name for p in (REAL_RUN / "oracle").iterdir())

    assert before == after
    assert summary["scenario_id"] == "S01"
    assert summary["outcome"]["outcome"] == "collision"
    assert summary["participants"]["A"]["n_samples"] > 0
    assert summary["participants"]["A"]["distance_travelled_m"] > 0.0


# ---------------------------------------------------------------------------
# Synthetic traces
# ---------------------------------------------------------------------------


def test_pair_kinematics_is_exact(cfg):
    """Range, range-rate and TTC come straight out of the closed-form geometry."""
    trace = _rear_end_trace()
    states = pair_kinematics(trace, "A", "B")
    assert states

    first = states[0]
    assert first.t == pytest.approx(DT)
    assert first.distance == pytest.approx(30.0 - 14.0 * DT, abs=1e-9)
    assert first.range_rate == pytest.approx(-14.0, abs=1e-9)
    assert first.closing_speed == pytest.approx(14.0, abs=1e-9)
    assert first.ttc == pytest.approx((30.0 - 14.0 * DT) / 14.0, abs=1e-9)
    assert first.d_cpa == pytest.approx(0.0, abs=1e-6)

    with pytest.raises(ValueError):
        pair_kinematics(trace, "A", "A")


def test_synthetic_events_cover_the_template_vocabulary(cfg):
    """A closing approach produces closing, critical TTC and one true collision."""
    trace = _rear_end_trace()
    spec = _Spec(["A", "B"])
    events = build_oracle_events(trace, spec, cfg)

    names = {e.values.get("oracle_state") for e in events}
    assert {"closing", "critical_ttc"} <= names

    collisions = [e for e in events if e.event_type is EventType.COLLISION]
    assert len(collisions) == 1
    assert collisions[0].t_peak == pytest.approx(1.80)
    assert collisions[0].values["impulse"] == pytest.approx(1234.5)
    assert collisions[0].values["relative_speed_mps"] == pytest.approx(14.0, abs=1e-6)

    actions = [e for e in events if e.event_type is EventType.ORACLE_SCRIPTED_INTERVENTION]
    # The disabled action never fired and must not appear.
    assert [e.subject for e in actions] == ["B_stop"]


def test_disabled_action_never_becomes_an_event(cfg):
    """A ``PREVENTS`` edge from an action that was switched off is not drawn."""
    trace = _rear_end_trace()
    spec = _Spec(["A", "B"])
    events = build_oracle_events(trace, spec, cfg)
    assert all(e.subject != "B_never" for e in events)


def test_unrealised_template_edge_is_skipped_and_recorded(cfg):
    """A designed cause that never occurred yields no node and a named diagnostic."""
    trace = _rear_end_trace()
    template = [
        {
            "cause": {"kind": "action", "participant": "B", "action_id": "B_stop"},
            "effect": {"kind": "outcome", "name": "collision", "participants": ["A", "B"]},
            "edge": "CAUSES_OUTCOME",
            "rationale": "stopping in the lane is what the follower runs into",
        },
        {
            # This action is declared but disabled, so nothing realises it.
            "cause": {"kind": "action", "participant": "B", "action_id": "B_never"},
            "effect": {"kind": "outcome", "name": "collision", "participants": ["A", "B"]},
            "edge": "PREVENTS",
            "rationale": "an evasive action that was switched off for this run",
        },
    ]
    spec = _Spec(["A", "B"], template)
    events = build_oracle_events(trace, spec, cfg)
    doc = build_oracle_causal_graph(events, trace, spec, cfg)

    assert doc.meta["n_template_edges"] == 2
    assert doc.meta["n_realised_template_edges"] == 1
    assert len(template_edges(doc)) == 1
    assert template_edges(doc)[0].edge_type == "CAUSES_OUTCOME"

    (unrealised,) = doc.meta["unrealised_template_edges"]
    assert unrealised["template_index"] == 1
    assert unrealised["edge_type"] == "PREVENTS"
    assert "B_never" in unrealised["cause"]
    assert unrealised["reason"]

    # And, critically, no node was invented for the cause that never happened.
    assert all("B_never" != (n.subject or "") for n in doc.nodes)


def test_unrealised_outcome_endpoint_is_reported(cfg):
    """A template that expects an outcome the run never produced is reported, not drawn."""
    trace = _rear_end_trace()
    template = [
        {
            "cause": {"kind": "action", "participant": "B", "action_id": "B_stop"},
            "effect": {"kind": "outcome", "name": "no_collision", "participants": ["A", "B"]},
            "edge": "PREVENTS",
        }
    ]
    spec = _Spec(["A", "B"], template)
    events = build_oracle_events(trace, spec, cfg)
    doc = build_oracle_causal_graph(events, trace, spec, cfg)

    assert template_edges(doc) == []
    (unrealised,) = doc.meta["unrealised_template_edges"]
    assert "no_collision" in unrealised["effect"]


def test_cyclic_template_is_broken_and_the_rejection_recorded(cfg):
    """A template that declares a loop still yields a DAG, and says what it dropped."""
    trace = _rear_end_trace()
    closing = {"kind": "state", "participant": "A", "name": "closing"}
    critical = {"kind": "state", "participant": "A", "name": "critical_ttc"}
    template = [
        {"cause": closing, "effect": critical, "edge": "CONTRIBUTES_TO"},
        {"cause": critical, "effect": closing, "edge": "CONTRIBUTES_TO"},
    ]
    spec = _Spec(["A", "B"], template)
    events = build_oracle_events(trace, spec, cfg)
    doc = build_oracle_causal_graph(events, trace, spec, cfg)

    assert nx.is_directed_acyclic_graph(to_networkx(doc))
    assert len(template_edges(doc)) == 1
    (rejected,) = doc.meta["rejected_edges"]
    assert "cycle" in rejected["reason"]


def test_malformed_template_fails_loudly(cfg):
    """An unknown state name is a configuration bug, not something to skip quietly."""
    trace = _rear_end_trace()
    template = [
        {
            "cause": {"kind": "state", "participant": "A", "name": "teleported"},
            "effect": {"kind": "outcome", "name": "collision", "participants": ["A", "B"]},
            "edge": "CAUSES_OUTCOME",
        }
    ]
    spec = _Spec(["A", "B"], template)
    events = build_oracle_events(trace, spec, _cfg_or(cfg))
    with pytest.raises(ValueError) as excinfo:
        build_oracle_causal_graph(events, trace, spec, cfg)
    assert "teleported" in str(excinfo.value)

    bad_edge = [
        {
            "cause": {"kind": "state", "participant": "A", "name": "closing"},
            "effect": {"kind": "outcome", "name": "collision", "participants": ["A", "B"]},
            "edge": "MAKES_WORSE",
        }
    ]
    with pytest.raises(ValueError):
        build_oracle_causal_graph(events, trace, _Spec(["A", "B"], bad_edge), cfg)


def _cfg_or(cfg):
    """Tiny indirection so the malformed-template test reads in one direction."""
    return cfg


def test_signal_violation_is_detected_through_the_junction(cfg):
    """B enters the junction on a red it was last shown; A on green does not."""
    trace = _red_light_trace()
    spec = _Spec(["A", "B"])
    events = build_oracle_events(trace, spec, cfg)

    violations = [e for e in events if e.event_type is EventType.ORACLE_SIGNAL_VIOLATION]
    assert len(violations) == 1
    assert violations[0].participant_id == "B"
    assert violations[0].subject == "signal_violation"
    assert violations[0].t_start == pytest.approx(1.0, abs=DT + 1e-9)
    assert violations[0].provenance is Provenance.ORACLE

    conflicts = [
        e for e in events if e.event_type is EventType.ORACLE_RIGHT_OF_WAY_CONFLICT
    ]
    # Both parties occupy junction 838 at once, so both points of view are recorded.
    assert {e.participant_id for e in conflicts} == {"A", "B"}


def test_signal_violation_template_edge_resolves(cfg):
    """An ``oracle_state`` endpoint is realised by the privileged event."""
    trace = _red_light_trace()
    template = [
        {
            "cause": {
                "kind": "action",
                "participant": "B",
                "action_id": "B_run_red_light",
            },
            "effect": {
                "kind": "oracle_state",
                "participant": "B",
                "name": "signal_violation",
            },
            "edge": "TRIGGERS",
            "rationale": "ORACLE ONLY -- the light state is unobservable from onboard evidence",
        }
    ]
    spec = _Spec(["A", "B"], template)
    events = build_oracle_events(trace, spec, cfg)
    doc = build_oracle_causal_graph(events, trace, spec, cfg)

    assert doc.meta["unrealised_template_edges"] == []
    assert len(template_edges(doc)) == 1
    edge = doc.edges[0]
    assert edge.edge_type == "TRIGGERS"
    assert edge.detail["rationale"].startswith("ORACLE ONLY")
    assert doc.node_by_id(edge.target).event_type is EventType.ORACLE_SIGNAL_VIOLATION


def test_same_lane_following_is_not_a_conflict_region(cfg):
    """A follower crossing its leader's path through jitter is not a shared conflict."""
    trace = _rear_end_trace()
    spec = _Spec(["A", "B"])
    events = build_oracle_events(trace, spec, cfg)
    assert not [e for e in events if e.event_type is EventType.CONFLICT_REGION_ENTRY]


def test_crossing_paths_do_produce_a_conflict_region(cfg):
    """Two vehicles meeting a junction at right angles enter one conflict region."""
    trace = _red_light_trace()
    spec = _Spec(["A", "B"])
    events = build_oracle_events(trace, spec, cfg)
    entries = [e for e in events if e.event_type is EventType.CONFLICT_REGION_ENTRY]
    assert {e.participant_id for e in entries} == {"A", "B"}
    for entry in entries:
        assert entry.subject == "conflict_entry"
        assert entry.values["crossing_angle_deg"] > 45.0


def test_near_miss_replaces_the_collision_when_nobody_is_hit(cfg):
    """No contact but a close pass is a near miss, and the run is not a collision."""
    trace = _rear_end_trace()
    trace["collisions"] = []
    trace["collision_pairs"] = []
    trace["summary"]["collisions"] = []
    trace["summary"]["collision_pairs"] = []

    spec = _Spec(["A", "B"])
    events = build_oracle_events(trace, spec, cfg)
    near = [e for e in events if e.event_type is EventType.NEAR_MISS]
    assert len(near) == 1
    assert sorted(near[0].owners) == ["A", "B"]
    assert not [e for e in events if e.event_type is EventType.COLLISION]

    outcome = oracle_outcome(trace, cfg)
    assert outcome["outcome"] == "near_miss"


def test_oracle_graphs_refuse_a_local_event(cfg):
    """A local event entering the reference would make the evaluation circular."""
    trace = _rear_end_trace()
    spec = _Spec(["A", "B"])
    events = build_oracle_events(trace, spec, cfg)
    smuggled = Event(
        event_id=make_event_id("local", "A", EventType.HARD_BRAKE.value, 1.0, None),
        event_type=EventType.HARD_BRAKE,
        participant_id="A",
        t_start=1.0,
        t_peak=1.0,
        provenance=Provenance.LOCAL,
    )
    with pytest.raises(ValueError) as excinfo:
        build_oracle_causal_graph(list(events) + [smuggled], trace, spec, cfg)
    assert "provenance" in str(excinfo.value)

    with pytest.raises(ValueError):
        build_oracle_event_graph(list(events) + [smuggled], trace, spec, cfg)


def test_load_oracle_trace_fails_loudly_when_absent(tmp_path):
    """A missing privileged trace must not degrade into a vacuous empty result."""
    with pytest.raises(FileNotFoundError):
        load_oracle_trace(tmp_path)


def test_build_oracle_events_rejects_a_participant_the_run_never_had(cfg):
    """A trace that does not contain the scenario's participants cannot score it."""
    trace = _rear_end_trace()
    with pytest.raises(ValueError) as excinfo:
        build_oracle_events(trace, _Spec(["A", "B", "C"]), cfg)
    assert "C" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Independence from the local causal rule engine
# ---------------------------------------------------------------------------


def _imported_modules(path: Path) -> List[str]:
    """Every module name a source file imports, relative imports included.

    A relative import is reported with its leading dots preserved
    (``"..local.causal_rules"``) so that a substring check catches it exactly the
    way an absolute one would.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    out: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = "." * int(node.level or 0) + (node.module or "")
            out.append(base)
            out.extend("{0}.{1}".format(base, alias.name) for alias in node.names)
    return out


#: The inference machinery the reference exists to score. Written as module
#: paths rather than bare tokens: the oracle has modules of its own whose names
#: legitimately contain "causal_graph", and a substring match would flag those
#: while telling us nothing about where they came from.
FORBIDDEN_INFERENCE_MODULES = (
    "cdf.local.causal_rules",
    "cdf.local.causal_graph",
    "cdf.local.event_extractor",
    "cdf.local.event_graph",
    "cdf.local.pipeline",
    "cdf.fusion.graph_fusion",
    "cdf.fusion.post_fusion_causal",
)


def _resolves_into(name: str, module: str) -> str:
    """The absolute module a possibly-relative import refers to.

    Python's rule, which is easy to get subtly wrong: the anchor is the
    *package* containing ``module``, not the module itself. So from
    ``cdf.oracle.x``, a single dot means ``cdf.oracle`` and two dots mean
    ``cdf``. Resolving one level too few would quietly let ``..local.foo``
    look like an oracle module and defeat the check.
    """
    if not name.startswith("."):
        return name
    depth = len(name) - len(name.lstrip("."))
    package = module.split(".")[:-1]
    base = package[: len(package) - (depth - 1)] if depth > 1 else package
    tail = name.lstrip(".")
    return ".".join(base + ([tail] if tail else [])).rstrip(".")


def test_oracle_does_not_import_the_local_causal_engine():
    """The reference must not be built by the machinery it is used to score.

    Asserted by reading the source rather than by inspecting ``sys.modules``: an
    import made inside a function would never show up in a runtime check on a
    code path the test happens not to take.

    The oracle builds its own causal graph, from its own rules, over exact state.
    That is not the thing this forbids -- what it forbids is the oracle reaching
    into ``cdf.local`` or ``cdf.fusion``, which would make agreement true by
    construction and the whole comparison vacuous.
    """
    package = Path(oracle_events.__file__).parent

    for path in sorted(package.glob("*.py")):
        module = "cdf.oracle." + path.stem
        for name in _imported_modules(path):
            resolved = _resolves_into(name, module)
            for forbidden in FORBIDDEN_INFERENCE_MODULES:
                assert not resolved.startswith(forbidden), (
                    "{0} imports {1!r} (resolving to {2}); the oracle must not "
                    "reuse the inference machinery it is the reference "
                    "for".format(path.name, name, resolved)
                )


def test_the_import_check_would_catch_a_real_violation() -> None:
    """A guard that cannot fail is not a guard."""
    assert _resolves_into("cdf.local.causal_rules", "cdf.oracle.x").startswith(
        "cdf.local.causal_rules"
    )
    assert _resolves_into("..local.causal_graph", "cdf.oracle.x").startswith(
        "cdf.local.causal_graph"
    )
    # ...and the oracle's own graph module is not mistaken for the local one.
    assert not _resolves_into(
        ".observable_graph", "cdf.oracle.ground_truth_package"
    ).startswith("cdf.local")


def test_oracle_analysis_modules_do_not_need_carla():
    """Only the logger talks to the simulator; everything else works off the trace."""
    for module in (oracle_events, oracle_graph, oracle_evaluator):
        path = Path(module.__file__)
        for name in _imported_modules(path):
            assert not name.split(".")[0] == "carla", "{0} imports carla".format(path.name)
            assert "carla_client" not in name, "{0} imports the CARLA client".format(path.name)


# --- helpers -------------------------------------------------------------

def template_edges(doc):
    """Only the edges instantiating the scenario's ``causal_template``.

    The oracle also asserts ground-truth *mechanical* edges (a commanded brake
    decelerates the car; an impact stops it). Those exist so that a
    reconstruction is not charged a false positive for reporting something that
    is in fact true, and tests about template instantiation filter them out.
    """
    from cdf.oracle import graph as oracle_graph

    return [e for e in doc.edges if e.rule == oracle_graph.TEMPLATE_RULE]


def mechanical_edges(doc):
    """Only the ground-truth mechanical edges."""
    from cdf.oracle import graph as oracle_graph

    return [e for e in doc.edges if e.rule == oracle_graph.MECHANICAL_RULE]
