"""End-to-end execution of one scenario run.

The run loop is intentionally explicit about the order of operations within a
tick, because that ordering is what makes the experiment reproducible:

1. ``world.tick()`` advances physics by exactly ``fixed_delta_seconds``.
2. Every participant reads **its own** state, polls **its own** radars, updates
   **its own** tracker and recorder, and computes its next control command.
3. The oracle separately records exact global state for the same tick.

Participants are stepped in a fixed order and never observe each other through
the runner: the runner hands each agent nothing but the current time and frame.

Termination is decided by the recorders, not by a fixed duration: once an
incident triggers, the run continues until every triggered participant has
captured its post-event window, subject to the scenario's duration cap.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.geometry import angle_diff_deg, distance
from ..common.evidence import ParticipantEvidence
from ..common.io import environment_block, write_evidence_manifest, write_json
from ..common.layout import RunLayout
from ..common.schemas import (
    OutcomeClass,
    ParticipantManifest,
    RunManifest,
    SCHEMA_VERSIONS,
    TriggerKind,
)
from ..oracle.logger import OracleLogger
from .traffic_control import (
    place_traffic_control, stop_lines_truth, traffic_control_truth,
)
from .carla_client import import_carla
from .live_view import LiveScenarioView, LiveViewOptions
from .scenario_base import (
    ParticipantSpec,
    ScenarioSpec,
    build_route,
    make_controller,
    resolve_spawn_waypoint,
)
from .variation import apply_seed_variation
from .vehicle_agent import ParticipantAgent
from .world import ScenarioWorld

LOGGER = logging.getLogger(__name__)

__all__ = ["RunResult", "run_scenario", "validate_run"]


@dataclass
class RunResult:
    """Everything one scenario execution produced."""

    layout: RunLayout
    manifest: RunManifest
    evidence: Dict[str, ParticipantEvidence] = field(default_factory=dict)
    oracle_summary: Dict[str, Any] = field(default_factory=dict)
    validation: Dict[str, Any] = field(default_factory=dict)
    spec: Optional[ScenarioSpec] = None

    @property
    def ok(self) -> bool:
        """Whether the scenario produced the encounter it declared."""
        return bool(self.validation.get("passed", False))


def make_run_id(scenario_id: str, seed: int, variant: str, config_hash: str) -> str:
    """Deterministic run identifier -- same inputs give the same id."""
    return "{0}-{1}-seed{2:03d}-{3}".format(
        scenario_id.upper(), variant, int(seed), config_hash[:8]
    )


def _maybe_live_view(
    sworld: ScenarioWorld,
    agents: Sequence[ParticipantAgent],
    *,
    live: bool,
    realtime: bool,
    playback_speed: float,
    spectator_mode: str,
    follow_vehicle: str,
    spectator_height: float,
    show_labels: bool,
) -> Optional[LiveScenarioView]:
    """Create the external spectator view without exposing it to the pipeline."""
    if not live:
        return None
    options = LiveViewOptions(
        mode=spectator_mode,
        follow_vehicle=follow_vehicle,
        spectator_height=spectator_height,
        show_labels=show_labels,
        realtime=realtime,
        playback_speed=playback_speed,
    )
    vehicles = {agent.participant_id: agent.vehicle for agent in agents}
    return LiveScenarioView(sworld.world, vehicles, options=options)


def run_scenario(
    client: Any,
    cfg: Config,
    spec: ScenarioSpec,
    seed: int,
    artifacts_root: str = "artifacts",
    persist: bool = True,
    intervention: Optional[Dict[str, Any]] = None,
    layout: Optional[RunLayout] = None,
    vary_by_seed: bool = True,
    live: bool = False,
    realtime: bool = False,
    playback_speed: float = 1.0,
    spectator_mode: str = "overhead",
    follow_vehicle: str = "A",
    spectator_height: float = 35.0,
    show_labels: bool = True,
) -> RunResult:
    """Execute one scenario and return its evidence, oracle trace and validation.

    ``intervention`` (used by the counterfactual layer) disables, delays or
    weakens named scripted actions *before* the run starts. Everything else --
    map, spawn state, seed, controller parameters -- is held identical, which is
    what makes the comparison a controlled counterfactual rather than a
    different experiment.
    The optional live arguments affect only the external CARLA spectator.  They
    never enter evidence, oracle state, analysis, or persisted artifacts.
    """
    if float(playback_speed) <= 0.0:
        raise ValueError("playback speed must be greater than zero")
    if realtime and not live:
        raise ValueError("realtime pacing requires live=True")
    if not realtime and abs(float(playback_speed) - 1.0) > 1e-12:
        raise ValueError("playback speed other than 1.0 requires realtime=True")

    carla = import_carla()
    # Repeating a deterministic scenario under a different seed alone would
    # reproduce the same trace, so seeds beyond 0 apply a small, reproducible
    # perturbation of approach speeds and action timings instead. Counterfactual
    # replays never vary: they must differ from the factual run in exactly one
    # intervention, otherwise the comparison is not controlled.
    variation_block: Dict[str, Any] = {}
    if vary_by_seed and intervention is None:
        spec, variation = apply_seed_variation(spec, seed)
        variation_block = variation.as_dict()

    run_id = make_run_id(spec.scenario_id, seed, spec.variant, cfg.hash)
    if intervention:
        spec = _apply_intervention(spec, intervention)
        run_id = "{0}-cf-{1}".format(run_id, intervention.get("intervention_id", "x"))

    if layout is None:
        layout = RunLayout.create(artifacts_root, spec.scenario_id, spec.name, seed, spec.variant)

    started_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    env = environment_block()
    oracle = OracleLogger(
        scenario_id=spec.scenario_id,
        run_id=run_id,
        seed=seed,
        variant=spec.variant,
        map_name=spec.map_name,
    )

    agents: List[ParticipantAgent] = []
    evidence: Dict[str, ParticipantEvidence] = {}
    outcome = OutcomeClass.NO_EVENT
    notes: List[str] = []
    n_frames = 0
    duration_sim_s = 0.0
    traffic_light_config: List[Dict[str, Any]] = []
    live_view: Optional[LiveScenarioView] = None

    with ScenarioWorld(client, cfg, spec.map_name, seed=seed) as sworld:
        oracle.bind_map(sworld.map)
        spawn_points = sworld.spawn_points()
        traffic_light_config = configure_traffic_lights(sworld, spec)
        for entry in traffic_light_config:
            oracle.add_note(
                "traffic light {0} forced to {1}".format(
                    entry["traffic_light_id"], entry["state"]
                )
            )

        # --- resolve geometry before spawning anything ---
        placements: List[Tuple[ParticipantSpec, Any, Any]] = []
        for pspec in spec.participants:
            wp = resolve_spawn_waypoint(sworld.map, spawn_points, pspec.spawn)
            route = build_route(sworld.map, wp, pspec.route)
            tf = wp.transform
            transform = carla.Transform(
                carla.Location(
                    x=tf.location.x,
                    y=tf.location.y,
                    z=tf.location.z + float(cfg.get("simulation.spawn_z_offset", 0.3)),
                ),
                carla.Rotation(pitch=0.0, yaw=tf.rotation.yaw, roll=0.0),
            )
            placements.append((pspec, transform, route))

        _assert_spawn_separation(placements, min_gap_m=float(cfg.get("simulation.min_spawn_gap_m", 5.0)))

        # --- place the declared traffic control ---
        # Before any vehicle: a prop cannot spawn into space a vehicle already
        # occupies, and the sign is the fixed part of the scene. An approach with
        # no sign on it cannot be perceived, so a sign that could not be placed
        # is recorded rather than passed over -- a camera that finds nothing
        # where the scenario says there is a sign has not failed, it has been
        # asked an unanswerable question.
        sign_placement = place_traffic_control(sworld, spec.traffic_control, cfg)
        if spec.traffic_control and not sign_placement["all_placed"]:
            missing = sign_placement["n_declared"] - sign_placement["n_placed"]
            notes.append(
                "{0} of {1} declared sign(s) could not be placed".format(
                    missing, sign_placement["n_declared"])
            )
            LOGGER.warning(
                "%s: %d of %d declared sign(s) could not be placed; the "
                "traffic-control findings for those approaches will be empty",
                spec.scenario_id, missing, sign_placement["n_declared"],
            )

        # --- instantiate participants ---
        for pspec, transform, route in placements:
            controller = make_controller(pspec, route)
            agent = ParticipantAgent(
                scenario_world=sworld,
                cfg=cfg,
                spec=pspec,
                controller=controller,
                spawn_transform=transform,
                seed=seed,
                clock_context="{0}/{1}".format(spec.scenario_id, spec.variant),
            )
            agent.spawn()
            agents.append(agent)
            oracle.register(
                pspec.participant_id,
                agent.vehicle,
                collision_sensor=agent.collision_sensor,
                controller=controller,
            )

        live_view = _maybe_live_view(
            sworld,
            agents,
            live=live,
            realtime=realtime,
            playback_speed=playback_speed,
            spectator_mode=spectator_mode,
            follow_vehicle=follow_vehicle,
            spectator_height=spectator_height,
            show_labels=show_labels,
        )

        # --- settle physics, then impart initial speeds ---
        sworld.warmup()
        for agent in agents:
            agent.apply_initial_speed()
        # A few ticks for the imparted velocity to take effect in the physics
        # solver before the scripted timeline starts.
        for _ in range(4):
            sworld.tick()

        t0 = sworld.elapsed_seconds
        oracle.time_offset = t0
        for agent in agents:
            agent.time_offset = t0
            agent.drain_radar_queues(sworld.frame)
        if live_view is not None:
            live_view.start(0.0)

        # --- main loop ---
        dt = sworld.delta_seconds
        max_duration = float(spec.max_duration_s)
        hard_cap = float(cfg.get("simulation.max_duration_s", 45.0))
        limit = min(max_duration, hard_cap) if hard_cap > 0 else max_duration
        post_event_s = float(cfg.get("recorder.post_event_s", 5.0))

        while True:
            snapshot = sworld.tick()
            frame = int(snapshot.frame)
            t = float(snapshot.timestamp.elapsed_seconds) - t0
            n_frames += 1
            duration_sim_s = t

            for agent in agents:
                agent.step(t, frame, dt)

            oracle.capture(t, frame, world=sworld.world)

            # External-only visualization.  It runs after all scientific work for
            # the tick and returns no data to any inference or artifact stage.
            if live_view is not None:
                live_view.update(t)
                live_view.pace(t)

            # Termination is anchored to the LATEST trigger, not the first one.
            # An early near-miss trigger must not end the run before the
            # collision it was warning about has happened and been recorded.
            last_trigger = _latest_trigger_time(agents)
            if last_trigger is not None and t >= last_trigger + post_event_s:
                notes.append(
                    "run ended: post-event window complete "
                    "({0:.2f}s after the last trigger at t={1:.2f}s)".format(post_event_s, last_trigger)
                )
                break
            if t >= limit:
                notes.append("run ended: duration cap {0:.1f}s reached".format(limit))
                break

        # --- finalise ---
        for agent in agents:
            evidence[agent.participant_id] = agent.finalize()

        collided = [a.participant_id for a in agents if a.collided]
        # A near miss is a near miss, not "some trigger fired": a participant
        # braking hard on its own (S04's yielding vehicle) arms the emergency
        # brake trigger without any close encounter having happened.
        near_missed = any(
            trig.kind == TriggerKind.NEAR_MISS
            for a in agents
            for trig in a.recorder.triggers
        )
        if oracle.collision_pairs():
            outcome = OutcomeClass.COLLISION
        elif near_missed:
            outcome = OutcomeClass.NEAR_MISS
        else:
            outcome = OutcomeClass.NO_EVENT

        oracle_summary = oracle.trace()
        validation = validate_run(spec, oracle, agents, cfg)

        if persist:
            for agent in agents:
                evidence[agent.participant_id] = agent.persist(layout)
            oracle_summary = oracle.persist(layout)
            write_json(layout.oracle_dir / "clock_ground_truth.json", {
                "schema_version": "1.0.0", "provenance": "oracle",
                "formula": "t_local = true_scale * t_sim + true_offset_s + jitter",
                "participants": {a.participant_id: a.clock.ground_truth() for a in agents},
            })
            # What the traffic control really is, for scoring what the cameras
            # made of it. Privileged, written only here, and read only by
            # evaluation -- deleting oracle/ must leave every inference artifact
            # byte-identical, which the anti-leakage suite checks.
            write_json(
                layout.traffic_control_truth,
                traffic_control_truth(sworld, spec.traffic_control, sign_placement),
            )
            write_json(
                layout.stop_lines_truth,
                stop_lines_truth(sworld, spec.traffic_control),
            )

    participants_manifest = [
        ParticipantManifest(
            participant_id=a.participant_id,
            blueprint=a.spec.blueprint,
            spawn=a.manifest_block()["spawn"],
            controller="ScriptedController",
            controller_params=a.controller.describe(),
            sensor_profile=str(a.cfg.get("sensors.profile", "?")),
            radar_sensors=a.cfg.get("radar.sensors", []),
            n_telemetry=len(evidence[a.participant_id].telemetry),
            n_radar_frames=len(evidence[a.participant_id].radar),
            n_track_samples=len(evidence[a.participant_id].tracks),
            n_events=0,
            triggers=[
                {"t": tr.t, "kind": tr.kind.value, "impulse": tr.impulse}
                for tr in evidence[a.participant_id].triggers
            ],
        )
        for a in agents
    ]

    manifest = RunManifest(
        run_id=run_id,
        scenario_id=spec.scenario_id,
        variant=spec.variant,
        seed=int(seed),
        map_name=spec.map_name,
        fixed_delta_seconds=float(cfg.get("simulation.fixed_delta_seconds", 0.05)),
        synchronous_mode=bool(cfg.get("simulation.synchronous_mode", True)),
        config_hash=cfg.hash,
        config=cfg.data,
        participants=participants_manifest,
        started_at=started_at,
        finished_at=time.strftime("%Y-%m-%dT%H:%M:%S"),
        duration_sim_s=duration_sim_s,
        n_frames=n_frames,
        outcome=outcome,
        outcome_detail={
            "collision_pairs": [
                {"a": a, "b": b, "t": t} for (a, b, t) in oracle.collision_pairs()
            ],
            "collided_participants": collided,
            "sensor_health": {a.participant_id: a.sensor_health() for a in agents},
            "traffic_lights": traffic_light_config,
            "seed_variation": variation_block,
        },
        git_commit=env["git_commit"],
        python_version=env["python_version"],
        carla_version=env["carla_version"],
        platform=env["platform"],
        package_version=env["package_version"],
        notes=notes + validation.get("problems", []),
        clock_protocol=("independent_local_clocks" if cfg.get("clocks.independent", False)
                        else "synchronized_clock_baseline"),
    )

    if persist:
        write_json(layout.manifest, manifest)
        write_json(layout.scenario_validation, validation)
        # Tamper-evident inventory of what the recording produced. Written last,
        # so it covers the manifest and the validation too. Later stages add
        # artifacts of their own, so the stage is recorded and the manifest is
        # rewritten by `scripts/reprocess_runs.py --stages manifest`.
        write_evidence_manifest(layout.root, extra={"stage": "recording",
                                                    "run_id": run_id})

    LOGGER.info(
        "run %s finished: outcome=%s frames=%d sim=%.2fs validation=%s",
        run_id,
        outcome.value,
        n_frames,
        duration_sim_s,
        "PASS" if validation.get("passed") else "FAIL",
    )
    return RunResult(
        layout=layout,
        manifest=manifest,
        evidence=evidence,
        oracle_summary=oracle_summary,
        validation=validation,
        spec=spec,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def configure_traffic_lights(sworld: ScenarioWorld, spec: ScenarioSpec) -> List[Dict[str, Any]]:
    """Force the signals around a junction into a fixed, declared state.

    A scenario may need an approach to be genuinely red at the moment a vehicle
    crosses it, and it needs that to be identical on every replay. Leaving the
    lights on their normal cycle would make the declared encounter depend on run
    timing.

    Each light is matched to an approach by the heading of its stop waypoints,
    then set and frozen. This is scenario construction using privileged map and
    signal APIs; the resulting states reach only the oracle.

    Returns a record of what was set, for the run manifest.
    """
    block = spec.traffic_lights or {}
    if not block:
        return []
    carla = import_carla()

    jx = float(block.get("junction_x", 0.0))
    jy = float(block.get("junction_y", 0.0))
    radius = float(block.get("radius_m", 60.0))
    default_state = str(block.get("default_state", "Green"))
    overrides = block.get("overrides", []) or []
    freeze = bool(block.get("freeze", True))

    states = {
        "Green": carla.TrafficLightState.Green,
        "Red": carla.TrafficLightState.Red,
        "Yellow": carla.TrafficLightState.Yellow,
        "Off": carla.TrafficLightState.Off,
    }
    applied: List[Dict[str, Any]] = []

    for light in sworld.traffic_lights():
        loc = light.get_transform().location
        if distance(loc.x, loc.y, jx, jy) > radius:
            continue

        # A light's stop waypoints face the traffic it governs, so their heading
        # identifies the approach far more reliably than the light's own yaw.
        headings: List[float] = []
        try:
            for wp in light.get_stop_waypoints():
                headings.append(float(wp.transform.rotation.yaw))
        except RuntimeError as exc:
            LOGGER.warning("could not read stop waypoints for light %s: %s", light.id, exc)

        wanted = default_state
        matched_bearing = None
        if headings:
            for ov in overrides:
                bearing = float(ov.get("bearing_deg", 0.0))
                if any(abs(angle_diff_deg(h, bearing)) <= 35.0 for h in headings):
                    wanted = str(ov.get("state", default_state))
                    matched_bearing = bearing
                    break

        state = states.get(wanted)
        if state is None:
            raise ValueError("unknown traffic light state {0!r}".format(wanted))
        light.set_state(state)
        if freeze:
            light.freeze(True)
        applied.append(
            {
                "traffic_light_id": int(light.id),
                "x": round(float(loc.x), 2),
                "y": round(float(loc.y), 2),
                "state": wanted,
                "matched_bearing_deg": matched_bearing,
                "stop_waypoint_headings": [round(h, 1) for h in headings],
                "frozen": freeze,
            }
        )

    LOGGER.info(
        "configured %d traffic light(s) around (%.1f, %.1f): %s",
        len(applied),
        jx,
        jy,
        ", ".join("{0}={1}".format(a["traffic_light_id"], a["state"]) for a in applied),
    )
    return applied


def _assert_spawn_separation(
    placements: Sequence[Tuple[ParticipantSpec, Any, Any]], min_gap_m: float
) -> None:
    """Fail before spawning if two participants would overlap.

    CARLA's own error ("collision at spawn position") appears only after a
    partial spawn, leaving actors to clean up; checking first gives a clearer
    message and a clean world.
    """
    for i in range(len(placements)):
        for j in range(i + 1, len(placements)):
            a = placements[i][1].location
            b = placements[j][1].location
            gap = float(((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5)
            if gap < float(min_gap_m):
                raise ValueError(
                    "participants {0} and {1} spawn only {2:.2f} m apart "
                    "(minimum {3:.2f} m)".format(
                        placements[i][0].participant_id,
                        placements[j][0].participant_id,
                        gap,
                        min_gap_m,
                    )
                )


def _latest_trigger_time(agents: Sequence[ParticipantAgent]) -> Optional[float]:
    """The most recent trigger time across every participant, or ``None``.

    Using the latest rather than the first trigger is what keeps a precautionary
    near-miss trigger early in the run from cutting the run short before the
    collision it anticipated.
    """
    times: List[float] = []
    for agent in agents:
        if agent.latest_trigger_sim_time is not None:
            times.append(float(agent.latest_trigger_sim_time))
    return max(times) if times else None


def _apply_intervention(spec: ScenarioSpec, intervention: Dict[str, Any]) -> ScenarioSpec:
    """Return a copy of ``spec`` with the intervention's scripted actions modified.

    Supported operations: ``disable`` (remove the action entirely), ``delay`` and
    ``advance`` (shift ``t_start``), ``scale`` (multiply a parameter), ``set``
    (assign a parameter).

    The usual form targets exactly one action, so the comparison isolates a
    single candidate cause. A ``steps`` list targets several at once, each
    action at most once: that is what a *joint* counterfactual is, and two
    vehicles can each contribute without either being individually decisive.
    """
    import copy

    out = copy.deepcopy(spec)
    steps = intervention.get("steps")
    if steps:
        for step in steps:
            out = _apply_one_step(out, step)
        out.variant = "{0}+{1}".format(
            spec.variant, intervention.get("intervention_id", "composite")
        )
        return out
    out = _apply_one_step(out, intervention)
    out.variant = "{0}+{1}".format(
        spec.variant, intervention.get("intervention_id", intervention.get("op", "disable"))
    )
    return out


def _apply_one_step(out: ScenarioSpec, intervention: Dict[str, Any]) -> ScenarioSpec:
    """Apply exactly one operation to exactly one scripted action, in place.

    The caller owns the copy and the variant name; this only edits the action.
    """
    action_id = intervention.get("action_id")
    op = intervention.get("op", "disable")

    target = None
    for p in out.participants:
        for a in p.actions:
            if a.action_id == action_id:
                target = a
                break
    if target is None:
        raise KeyError(
            "intervention targets unknown action {0!r}; declared actions are {1}".format(
                action_id,
                [a.action_id for p in out.participants for a in p.actions],
            )
        )

    if op == "disable":
        target.enabled = False
    elif op == "delay":
        target.t_start = float(target.t_start) + float(intervention.get("seconds", 1.0))
    elif op == "advance":
        target.t_start = max(0.0, float(target.t_start) - float(intervention.get("seconds", 1.0)))
    elif op == "scale":
        key = intervention["param"]
        target.params[key] = float(target.params.get(key, 0.0)) * float(intervention.get("factor", 0.5))
    elif op == "set":
        target.params[intervention["param"]] = float(intervention["value"])
    else:
        raise ValueError("unknown intervention op {0!r}".format(op))

    return out


def validate_run(
    spec: ScenarioSpec,
    oracle: OracleLogger,
    agents: Sequence[ParticipantAgent],
    cfg: Config,
) -> Dict[str, Any]:
    """Check that the run produced the encounter the scenario declared.

    A scenario that quietly stops colliding -- because a controller gain changed,
    or a map was updated -- would otherwise poison every downstream metric. This
    turns that into an explicit, recorded failure.
    """
    problems: List[str] = []
    checks: Dict[str, Any] = {}

    ids = spec.participant_ids
    checks["n_participants"] = len(ids)
    if len(agents) != len(ids):
        problems.append(
            "expected {0} participants, {1} were instantiated".format(len(ids), len(agents))
        )
    if len(ids) > 3:
        problems.append("more than three participant vehicles is not permitted")

    pairs = oracle.collision_pairs()
    checks["collision_pairs"] = [{"a": a, "b": b, "t": t} for (a, b, t) in pairs]
    observed_pairs = {tuple(sorted((a, b))) for (a, b, _t) in pairs}

    if spec.expected_outcome == "collision":
        if not pairs:
            problems.append("expected a collision but none occurred")
        for expected in spec.expected_collision_pairs:
            key = tuple(sorted(expected))
            if key not in observed_pairs:
                problems.append(
                    "expected collision pair {0} did not occur (observed {1})".format(
                        sorted(expected), sorted(observed_pairs)
                    )
                )
        if spec.expected_collision_order:
            ordered = [tuple(sorted((a, b))) for (a, b, _t) in pairs]
            wanted = [tuple(sorted(p)) for p in spec.expected_collision_order]
            filtered = [p for p in ordered if p in set(wanted)]
            if filtered != wanted:
                problems.append(
                    "collision order {0} does not match the required order {1}".format(
                        filtered, wanted
                    )
                )
    elif spec.expected_outcome == "near_miss":
        if pairs:
            problems.append(
                "expected a near miss but a collision occurred between {0}".format(
                    sorted(observed_pairs)
                )
            )
        if not any(a.triggered for a in agents):
            problems.append("expected a near miss but no participant triggered")
    elif spec.expected_outcome == "no_event":
        if pairs:
            problems.append("expected no event but a collision occurred")

    # --- the intended encounter actually happened ---
    encounter = spec.validation.get("min_separation_below_m")
    encounter_pair = spec.validation.get("encounter_pair")
    if encounter is not None and encounter_pair:
        sep = oracle.min_separation(encounter_pair[0], encounter_pair[1])
        checks["min_separation"] = (
            None if sep is None else {"t": sep[0], "distance_m": sep[1]}
        )
        if sep is None:
            problems.append("could not measure separation for the declared encounter pair")
        elif sep[1] > float(encounter):
            problems.append(
                "participants {0} and {1} never came closer than {2:.2f} m "
                "(required below {3:.2f} m): the intended encounter did not happen".format(
                    encounter_pair[0], encounter_pair[1], sep[1], float(encounter)
                )
            )

    # --- every recorder produced usable evidence ---
    for agent in agents:
        health = agent.sensor_health()
        checks.setdefault("sensor_health", {})[agent.participant_id] = health
        if health["radar_frames_seen"] == 0:
            problems.append(
                "participant {0} recorded no radar frames at all".format(agent.participant_id)
            )
        elif health["radar_frames_missed"] > 0.25 * max(1, health["radar_frames_seen"]):
            problems.append(
                "participant {0} missed {1} radar frames out of {2}".format(
                    agent.participant_id,
                    health["radar_frames_missed"],
                    health["radar_frames_seen"] + health["radar_frames_missed"],
                )
            )

    # --- minimum speed sanity: a participant that never moved is a bug ---
    for pid in ids:
        series = oracle.state_series(pid)
        top = max((s.speed for s in series), default=0.0)
        checks.setdefault("max_speed", {})[pid] = round(top, 3)
        if top < 0.5:
            problems.append("participant {0} never moved (max speed {1:.2f} m/s)".format(pid, top))

    return {
        "schema_version": SCHEMA_VERSIONS["manifest"],
        "scenario_id": spec.scenario_id,
        "variant": spec.variant,
        "expected_outcome": spec.expected_outcome,
        "passed": not problems,
        "problems": problems,
        "checks": checks,
    }
