"""Controlled counterfactual replays and the outcome metrics they produce.

The strong causal claims in this project do not come from the shape of a
reconstructed graph. They come from *replaying the same crash*: identical map,
identical spawn state, identical seed, identical controller parameters, with one
named scripted action disabled, delayed, advanced or weakened. Whatever the
outcome then is, it was measured, not inferred.

Two halves live here, deliberately separated so that the reasoning can be tested
without a simulator:

:func:`outcome_from_run`
    Pure extraction. Turns a finished run (its privileged oracle summary, its
    scenario validation and, when it was persisted, its oracle trace) into a
    :class:`CounterfactualOutcome`. No CARLA, no side effects.
:func:`run_counterfactual_suite`
    The driver. Replays every requested intervention into its own artifact
    directory, extracts an outcome from each, and persists the manifest, the
    per-intervention CSV and the causal-contribution report.

PRIVILEGED LAYER. Deciding whether a replay collided requires ground truth, so
this module reads oracle artifacts -- exactly like :mod:`cdf.evaluation`. It
writes only under ``counterfactual/`` and never back into a local or fused
artifact.

Resilience matters more than completeness here: a replay can fail (the simulator
drops the connection, a spawn point is occupied, a scenario assertion trips).
Such a failure is recorded with its error message and the suite continues. A
missing replay is reported as missing; it is never replaced by an assumption.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.geometry import time_to_collision_1d
from ..common.io import read_json, read_jsonl_gz, write_csv, write_json
from ..common.layout import RunLayout
from ..common.schemas import SCHEMA_VERSIONS
from ..simulation.runner import run_scenario
from ..simulation.scenario_base import ScenarioSpec
from .interventions import InterventionSpec

LOGGER = logging.getLogger(__name__)

__all__ = [
    "FACTUAL_ID",
    "CounterfactualOutcome",
    "outcome_from_run",
    "outcome_from_artifacts",
    "replay_layout",
    "run_counterfactual_suite",
]

#: Identity given to the unmodified run, so that factual and counterfactual
#: outcomes can share one table without a nullable key.
FACTUAL_ID = "factual"

#: Columns of ``intervention_results.csv``, fixed so the file stays diffable.
_CSV_COLUMNS: Tuple[str, ...] = (
    "intervention_id",
    "action_id",
    "op",
    "targets_participant",
    "status",
    "collision",
    "t_collision",
    "impact_speed",
    "relative_impact_speed",
    "min_ttc",
    "min_distance",
    "near_miss",
    "validation_passed",
    "but_for",
    "severity_reduction",
    "contribution_score",
    "error",
    "notes",
)


@dataclass
class CounterfactualOutcome:
    """What happened in one replay (or in the factual run).

    Every field is measured from that run's own privileged record. ``None`` means
    *undefined* -- for example ``impact_speed`` when there was no impact, or when
    the run's oracle trace was not persisted -- and is never silently turned into
    a zero: attribution has to be able to tell "no severity" from "severity
    unknown".
    """

    intervention_id: str
    action_id: str = ""
    #: Every action this replay removed: one entry for a single-action replay,
    #: several for a joint one, empty for the factual run. ``action_id`` stays
    #: the first of them so every existing consumer keeps working.
    action_ids: List[str] = field(default_factory=list)
    op: str = "none"
    params: Dict[str, Any] = field(default_factory=dict)
    """The intervention's own parameters, carried so attribution can read them.

    ``establishes_but_for`` needs the scale factor to tell weakening from
    strengthening, and until this field existed it read an attribute that was
    never populated -- so the guard fell through and *any* scale counted as
    establishing causation. Latent rather than live, since the enumerated
    factors are 0.4 and 0.8, but both are configurable and a value above 1.0
    would have been counted as causation silently.
    """
    targets_participant: str = ""
    repairs_non_action: str = ""
    """The non-action this replay supplied the missing behaviour for, if any.

    Empty for every replay that modifies something the vehicle actually did. It
    travels with the outcome because the attribution layer cannot otherwise tell
    an omission repair from an ordinary safety improvement: both insert braking,
    and only one of them is about a behaviour the evidence says was required.
    """

    collision: bool = False
    collision_pairs: List[List[str]] = field(default_factory=list)
    t_collision: Optional[float] = None
    impact_speed: Optional[float] = None
    """Ground speed of the faster of the two colliding vehicles at impact (m/s)."""
    relative_impact_speed: Optional[float] = None
    """Magnitude of the relative velocity at impact (m/s): the delta-v proxy and
    the default ``counterfactual.severity_metric``."""
    min_ttc: Optional[float] = None
    min_distance: float = float("inf")
    """Minimum centre-to-centre separation of the encounter pair (m). ``inf``
    when no separation could be measured; serialised as ``null``."""
    near_miss: bool = False
    validation_passed: bool = False
    notes: List[str] = field(default_factory=list)

    @property
    def is_factual(self) -> bool:
        return self.intervention_id == FACTUAL_ID

    def to_dict(self) -> Dict[str, Any]:
        """Serialisable record; non-finite floats become ``None``."""
        return {
            "intervention_id": self.intervention_id,
            "action_id": self.action_id,
            "action_ids": list(self.action_ids or ([self.action_id] if self.action_id else [])),
            "op": self.op,
            "targets_participant": self.targets_participant,
            "collision": bool(self.collision),
            "collision_pairs": [list(p) for p in self.collision_pairs],
            "t_collision": _finite_or_none(self.t_collision),
            "impact_speed": _finite_or_none(self.impact_speed),
            "relative_impact_speed": _finite_or_none(self.relative_impact_speed),
            "min_ttc": _finite_or_none(self.min_ttc),
            "min_distance": _finite_or_none(self.min_distance),
            "near_miss": bool(self.near_miss),
            "validation_passed": bool(self.validation_passed),
            "notes": list(self.notes),
        }


# ---------------------------------------------------------------------------
# Pure extraction
# ---------------------------------------------------------------------------


def outcome_from_run(
    result: Any,
    cfg: Optional[Config] = None,
    intervention: Optional[InterventionSpec] = None,
    oracle_frames: Optional[Sequence[Mapping[str, Any]]] = None,
) -> CounterfactualOutcome:
    """Extract the outcome metrics of a finished run. Pure -- no simulator.

    ``result`` is a :class:`cdf.simulation.runner.RunResult` (or anything exposing
    the same ``oracle_summary`` / ``validation`` / ``layout`` / ``spec``
    attributes, which is what makes this testable without CARLA).

    Whether a collision happened, and between whom, is ground truth and comes
    from the oracle summary. Impact speeds and the minimum time-to-collision need
    per-tick state, so they are read from the persisted oracle trace when there
    is one and reported as ``None`` when there is not -- an unmeasurable severity
    must stay unmeasurable rather than default to zero.
    """
    summary = getattr(result, "oracle_summary", None)
    if summary is None:
        raise ValueError(
            "run result for {0!r} carries no oracle summary, so its outcome "
            "cannot be established. A counterfactual replay must be run with "
            "the oracle logger enabled.".format(
                intervention.intervention_id if intervention else FACTUAL_ID
            )
        )
    if not isinstance(summary, Mapping):
        raise TypeError(
            "oracle summary must be a mapping, got {0!r}".format(type(summary))
        )

    validation = getattr(result, "validation", None) or {}
    notes: List[str] = []

    pairs, t_collision = _collision_pairs(summary)
    collided = bool(pairs)

    pair = _encounter_pair(result, summary, pairs)
    frames = oracle_frames if oracle_frames is not None else _load_oracle_frames(result)
    if frames is None:
        notes.append(
            "oracle trace unavailable: impact speed and min TTC are undefined"
        )

    impact_speed: Optional[float] = None
    relative_impact_speed: Optional[float] = None
    if collided and frames and t_collision is not None and pair is not None:
        impact_speed, relative_impact_speed = _impact_speeds(frames, pair, t_collision)
        if impact_speed is None:
            notes.append(
                "no oracle frame within reach of t={0:.2f}s: impact speed "
                "undefined".format(t_collision)
            )

    min_ttc: Optional[float] = None
    traced_min_distance: Optional[float] = None
    if frames and pair is not None:
        min_ttc, traced_min_distance = _min_ttc_and_distance(frames, pair)

    min_distance = _validated_min_distance(validation)
    if min_distance is None:
        min_distance = traced_min_distance
    if min_distance is None:
        min_distance = float("inf")
        notes.append("no separation measurement available for the encounter pair")

    validation_passed = bool(validation.get("passed", False))
    problems = list(validation.get("problems", []) or [])
    if problems:
        notes.append("scenario validation problems: {0}".format("; ".join(problems)))

    near_miss = (not collided) and _is_near_miss(
        result, min_distance, min_ttc, cfg
    )

    return CounterfactualOutcome(
        intervention_id=intervention.intervention_id if intervention else FACTUAL_ID,
        action_id=intervention.action_id if intervention else "",
        action_ids=list(getattr(intervention, "action_ids", ()) or ()) if intervention else [],
        op=intervention.op if intervention else "none",
        params=dict(getattr(intervention, "params", {}) or {}) if intervention else {},
        targets_participant=intervention.targets_participant if intervention else "",
        repairs_non_action=(
            str(getattr(intervention, "repairs_non_action", "") or "")
            if intervention else ""
        ),
        collision=collided,
        collision_pairs=pairs,
        t_collision=t_collision,
        impact_speed=impact_speed,
        relative_impact_speed=relative_impact_speed,
        min_ttc=min_ttc,
        min_distance=float(min_distance),
        near_miss=near_miss,
        validation_passed=validation_passed,
        notes=notes,
    )


def outcome_from_artifacts(
    run_dir: Any,
    cfg: Optional[Config] = None,
    intervention: Optional[InterventionSpec] = None,
) -> CounterfactualOutcome:
    """Rebuild an outcome from a run that was already persisted.

    Used to obtain the factual outcome without re-running the factual scenario:
    the crash under investigation was recorded once, and re-simulating it to
    measure it again would be both wasteful and an opportunity for drift.
    """
    layout = run_dir if isinstance(run_dir, RunLayout) else RunLayout.from_run_dir(run_dir)
    summary_path = layout.oracle_dir / "oracle_summary.json"
    if not summary_path.exists():
        raise FileNotFoundError(
            "no oracle summary at {0}; the run was either never executed or was "
            "run with persist=False".format(summary_path)
        )
    validation: Dict[str, Any] = {}
    if layout.scenario_validation.exists():
        validation = read_json(layout.scenario_validation)
    return outcome_from_run(
        _PersistedRun(
            layout=layout,
            oracle_summary=read_json(summary_path),
            validation=validation,
        ),
        cfg,
        intervention=intervention,
    )


@dataclass
class _PersistedRun:
    """A :class:`RunResult`-shaped view over artifacts already on disk."""

    layout: RunLayout
    oracle_summary: Dict[str, Any]
    validation: Dict[str, Any] = field(default_factory=dict)
    spec: Optional[ScenarioSpec] = None


# ---------------------------------------------------------------------------
# Replay driver
# ---------------------------------------------------------------------------


def replay_layout(factual: RunLayout, intervention_id: str) -> RunLayout:
    """Artifact directory for one replay, nested under the factual run.

    Replays live in ``counterfactual/replays/<intervention_id>/`` of the run they
    interrogate. Keeping them inside the investigated run (rather than beside it)
    means a run directory remains a self-contained forensic bundle: the crash,
    every replay that was tried, and the attribution they support travel
    together. Each replay gets its own full layout, so no replay can overwrite
    the factual evidence.
    """
    root = factual.counterfactual_dir / "replays" / str(intervention_id)
    return RunLayout.from_run_dir(root).ensure()


def run_counterfactual_suite(
    session: Any,
    cfg: Config,
    spec: ScenarioSpec,
    seed: int,
    interventions: Sequence[InterventionSpec],
    artifacts_root: str = "artifacts",
    factual_outcome: Optional[CounterfactualOutcome] = None,
) -> Dict[str, Any]:
    """Replay every intervention and persist the counterfactual evidence.

    ``session`` is a :class:`cdf.simulation.carla_client.SimulatorSession` (a bare
    client also works, but then a map change cannot restart a wedged server).
    Each intervention is replayed into its own directory via :func:`replay_layout`
    so that the factual run is never touched.

    When ``factual_outcome`` is omitted it is read back from the factual run's
    persisted artifacts. If that run has not been executed yet, the suite still
    runs every replay and still writes its manifest, but the contribution report
    says ``insufficient_evidence``: without the factual outcome there is nothing
    to compare against, and inventing a baseline would be fabricating a result.
    """
    from .attribution import attribution_report  # local: attribution imports this module

    layout = RunLayout.create(artifacts_root, spec.scenario_id, spec.name, seed, spec.variant)

    if factual_outcome is None:
        factual_outcome = _read_factual_outcome(layout, cfg)

    client = _client_for(session, spec)

    # A counterfactual is a COMPARISON, so the two runs must differ only in the
    # intervention. Repeated runs on one server session drift far enough to
    # change an outcome class (docs/ENVIRONMENT.md), which would confound exactly
    # the difference being measured, so each replay starts from a fresh server.
    restart_each = bool(cfg.get("counterfactual.restart_server_per_replay", True))
    can_restart = hasattr(session, "fresh_world_for_map")
    if restart_each and not can_restart:
        LOGGER.warning(
            "counterfactual.restart_server_per_replay is set but no simulator "
            "session was supplied; replays will share one server and are NOT "
            "independently reproducible"
        )
    # Whether the restart *can actually happen* is a property of how the session
    # was started: `fresh_world_for_map` falls back to reusing the current
    # server when no CARLA installation was found to restart, and only logs a
    # warning about it. A warning in a log nobody reads is how a degraded sweep
    # produces a verdict that does not reproduce, so the protocol that really
    # ran is written into the report beside the verdict it produced.
    server = getattr(session, "server", None)
    server_restartable = bool(getattr(server, "available", False))
    replay_protocol: Dict[str, Any] = {
        "restart_server_per_replay_requested": restart_each,
        "session_can_restart": can_restart,
        "server_restartable": server_restartable,
    }

    resume = bool(cfg.get("counterfactual.resume", True))

    outcomes: List[CounterfactualOutcome] = []
    failures: List[Dict[str, Any]] = []
    replay_dirs: Dict[str, str] = {}

    for intervention in interventions:
        target = replay_layout(layout, intervention.intervention_id)
        replay_dirs[intervention.intervention_id] = str(
            target.root.relative_to(layout.root).as_posix()
        )
        if resume:
            done = _completed_replay(target, cfg, intervention)
            if done is not None:
                LOGGER.info(
                    "counterfactual replay %s: reusing the completed replay at %s",
                    intervention.intervention_id, target.root,
                )
                outcomes.append(done)
                continue
        if restart_each and can_restart:
            # The caller's own reference must go too, or the session's release
            # is not the last one and the dead server's streaming thread stays
            # alive in this process (see SimulatorSession.release_client).
            client = None
            session.fresh_world_for_map(spec.map_name)
            client = session.client()
        LOGGER.info(
            "counterfactual replay %s: %s",
            intervention.intervention_id,
            intervention.description or intervention.op,
        )
        try:
            result = run_scenario(
                client,
                cfg,
                spec,
                seed,
                artifacts_root=artifacts_root,
                persist=True,
                intervention=intervention.as_runner_dict(),
                layout=target,
            )
        except Exception as exc:  # replay failures must not abort the suite
            LOGGER.exception(
                "counterfactual replay %s failed", intervention.intervention_id
            )
            failures.append(
                {
                    "intervention_id": intervention.intervention_id,
                    "action_id": intervention.action_id,
                    "op": intervention.op,
                    "targets_participant": intervention.targets_participant,
                    "error": "{0}: {1}".format(type(exc).__name__, exc),
                }
            )
            continue
        outcomes.append(outcome_from_run(result, cfg, intervention=intervention))

    # Bounded multi-action search. Only worth running when the factual run
    # collided and no single removal prevented it: if one did, a set containing
    # it would not be minimal. Sizes grow one at a time and the search stops at
    # the first size that prevents, which is what makes the set it finds minimal.
    combo_outcomes, combo_failures, combo_specs = _run_combination_search(
        session=session,
        cfg=cfg,
        spec=spec,
        seed=seed,
        artifacts_root=artifacts_root,
        layout=layout,
        factual_outcome=factual_outcome,
        single_outcomes=outcomes,
        restart_each=restart_each,
        can_restart=can_restart,
        replay_dirs=replay_dirs,
    )
    outcomes.extend(combo_outcomes)
    failures.extend(combo_failures)
    interventions = list(interventions) + list(combo_specs)

    report = attribution_report(
        factual_outcome,
        outcomes,
        cfg,
        interventions=interventions,
        failures=failures,
        scenario_id=spec.scenario_id,
        variant=spec.variant,
        seed=int(seed),
    )
    # Filled in only now, because whether the restarts *took effect* is not
    # knowable before they have been attempted. A pre-existing engine holding
    # the RPC port defeats every one of them while every log line claims
    # success, so this records the verified outcome rather than the intent.
    verified = getattr(server, "last_restart_verified", None)
    replay_protocol["restarts_verified_fresh"] = verified
    replay_protocol["effective"] = (
        "fresh_server_per_replay"
        if restart_each and can_restart and server_restartable and verified
        else "shared_server_session"
    )
    if replay_protocol["effective"] != "fresh_server_per_replay" and restart_each:
        replay_protocol["warning"] = (
            "replays shared one simulator session. Repeated runs in one session "
            "drift enough to change an outcome class, so these replays are not "
            "reliably comparable with each other. Set $CARLA_ROOT so the session "
            "can restart the server, and make sure no other simulator is already "
            "holding the RPC port -- a pre-existing one is not killed, and every "
            "restart silently reconnects to it."
        )
        LOGGER.warning("%s", replay_protocol["warning"])
    report["replay_protocol"] = replay_protocol

    manifest = {
        "schema_version": SCHEMA_VERSIONS["counterfactual"],
        "scenario_id": spec.scenario_id,
        "variant": spec.variant,
        "seed": int(seed),
        "map_name": spec.map_name,
        "config_hash": cfg.hash,
        "n_requested": len(interventions),
        "n_completed": len(outcomes),
        "n_failed": len(failures),
        "factual": factual_outcome.to_dict() if factual_outcome else None,
        "interventions": [iv.to_dict() for iv in interventions],
        "outcomes": [o.to_dict() for o in outcomes],
        "failures": failures,
        "replay_dirs": replay_dirs,
    }

    write_json(layout.counterfactual_manifest, manifest)
    write_csv(
        layout.intervention_results,
        _result_rows(factual_outcome, outcomes, failures, cfg),
        columns=list(_CSV_COLUMNS),
    )
    write_json(layout.causal_contribution, report)

    LOGGER.info(
        "counterfactual suite for %s/%s: %d replay(s) completed, %d failed -> %s",
        spec.scenario_id,
        spec.variant,
        len(outcomes),
        len(failures),
        report.get("classification", {}).get("attribution_class", "?"),
    )

    return {
        "manifest": manifest,
        "attribution": report,
        "outcomes": outcomes,
        "failures": failures,
        "factual": factual_outcome,
        "layout": layout,
        "artifacts": {
            "counterfactual_manifest": str(layout.counterfactual_manifest),
            "intervention_results": str(layout.intervention_results),
            "causal_contribution": str(layout.causal_contribution),
        },
    }


# ---------------------------------------------------------------------------
# Suite helpers
# ---------------------------------------------------------------------------


def _client_for(session: Any, spec: ScenarioSpec) -> Any:
    """Resolve a usable CARLA client from a session (or accept a bare client).

    A :class:`SimulatorSession` is asked for the scenario's map first: it is the
    only object that knows whether reaching that map needs a server restart, and
    doing it once up front keeps the per-replay cost down.
    """
    if hasattr(session, "world_for_map") and hasattr(session, "client"):
        session.world_for_map(spec.map_name)
        return session.client()
    if hasattr(session, "client") and callable(getattr(session, "client")):
        return session.client()
    return session


def _completed_replay(
    target: RunLayout,
    cfg: Optional[Config],
    intervention: InterventionSpec,
) -> Optional[CounterfactualOutcome]:
    """The outcome of a replay that already ran to completion, or ``None``.

    A replay is a whole simulator run on a freshly started engine, so a campaign
    that is interrupted -- an engine that failed to come up, a machine that was
    rebooted -- would otherwise repeat an hour of work that is already on disk.
    Reusing it costs nothing in comparability, because each replay is an
    independent server session by construction.

    A replay counts as complete only when its manifest and its oracle summary
    are both present and the manifest was produced by the configuration in
    force now; a replay recorded under different thresholds is not the replay
    this suite is asking for, so it is re-run rather than trusted.

    Note what the hash does **not** prove. It says the parameters agree; it says
    nothing about whether the recording was sound. Replays invalidated by
    something outside the configuration -- a simulator-lifecycle defect, an
    interrupted machine -- carry a matching hash and would be resumed straight
    into new results. Discarding such a campaign is therefore an explicit act:
    delete the ``counterfactual/`` directory, or use
    ``scripts/run_counterfactual_campaign.py --fresh``.
    """
    if not target.manifest.exists():
        return None
    try:
        manifest = read_json(target.manifest)
    except (OSError, ValueError) as exc:
        LOGGER.warning("unreadable replay manifest at %s (%s); re-running it",
                       target.manifest, exc)
        return None
    expected = None if cfg is None else str(cfg.hash)
    recorded = str(manifest.get("config_hash", ""))
    if expected is not None and recorded and recorded != expected:
        LOGGER.info(
            "replay %s was recorded under config %s but the current config is "
            "%s; re-running it", intervention.intervention_id, recorded, expected,
        )
        return None
    try:
        return outcome_from_artifacts(target, cfg, intervention=intervention)
    except FileNotFoundError:
        return None


def _run_combination_search(
    session: Any,
    cfg: Config,
    spec: Any,
    seed: int,
    artifacts_root: str,
    layout: RunLayout,
    factual_outcome: Optional[CounterfactualOutcome],
    single_outcomes: Sequence[CounterfactualOutcome],
    restart_each: bool,
    can_restart: bool,
    replay_dirs: Dict[str, str],
) -> Tuple[List[CounterfactualOutcome], List[Dict[str, Any]], List[Any]]:
    """Replay sets of actions until one prevents the collision, or the budget ends.

    Two vehicles can each contribute without either being individually decisive.
    Single-action replay reports that as insufficient evidence, which is true and
    uninformative; this finds the smallest set of changes that would have been
    enough, and reports honestly when none of the ones it could afford to try was.
    """
    from .combinations import plan_combinations
    from .interventions import InterventionSpec

    if not bool(cfg.get("counterfactual.combinations.enabled", True)):
        return [], [], []
    if factual_outcome is None or not factual_outcome.collision:
        return [], [], []

    prevented_alone = {
        o.action_id
        for o in single_outcomes
        if o.action_id and not o.collision
    }
    if prevented_alone:
        return [], [], []

    max_size = int(cfg.get("counterfactual.combinations.max_combination_size", 2))
    max_replays = int(cfg.get("counterfactual.combinations.max_replays", 6))
    candidates = sorted({o.action_id for o in single_outcomes if o.action_id})
    if len(candidates) < 2 or max_size < 2 or max_replays < 1:
        return [], [], []

    tested = [frozenset([o.action_id]) for o in single_outcomes if o.action_id]
    new_outcomes: List[CounterfactualOutcome] = []
    failures: List[Dict[str, Any]] = []
    specs: List[Any] = []
    budget = max_replays
    resume = bool(cfg.get("counterfactual.resume", True))

    for size in range(2, max_size + 1):
        if budget <= 0:
            break
        prevented_here = False
        for combo in plan_combinations(candidates, tested, size, budget):
            if budget <= 0:
                break
            budget -= 1
            actions = sorted(combo)
            iv = InterventionSpec(
                intervention_id="joint__" + "__".join(actions),
                action_id=actions[0],
                op="disable",
                params={},
                description=(
                    "none of {0} performs its action; everything else in the run "
                    "is held identical [joint counterfactual: no single removal "
                    "prevented the collision]".format(", ".join(actions))
                ),
                steps=[{"action_id": a, "op": "disable"} for a in actions],
            )
            specs.append(iv)
            tested.append(combo)
            target = replay_layout(layout, iv.intervention_id)
            replay_dirs[iv.intervention_id] = str(
                target.root.relative_to(layout.root).as_posix()
            )
            done = _completed_replay(target, cfg, iv) if resume else None
            if done is not None:
                LOGGER.info(
                    "joint replay %s: reusing the completed replay", iv.intervention_id
                )
                new_outcomes.append(done)
                if not done.collision:
                    prevented_here = True
                continue
            if restart_each and can_restart:
                session.fresh_world_for_map(spec.map_name)
            LOGGER.info("joint replay %s: %s", iv.intervention_id, iv.description)
            try:
                result = run_scenario(
                    _client_for(session, spec),
                    cfg,
                    spec,
                    seed,
                    artifacts_root=artifacts_root,
                    persist=True,
                    intervention=iv.as_runner_dict(),
                    layout=target,
                )
            except Exception as exc:  # noqa: BLE001 - recorded, never swallowed
                LOGGER.exception("joint replay %s failed", iv.intervention_id)
                failures.append(
                    {
                        "intervention_id": iv.intervention_id,
                        "action_id": iv.action_id,
                        "op": "disable",
                        "targets_participant": "",
                        "error": "{0}: {1}".format(type(exc).__name__, exc),
                    }
                )
                continue
            outcome = outcome_from_run(result, cfg, intervention=iv)
            new_outcomes.append(outcome)
            if not outcome.collision:
                prevented_here = True
        if prevented_here:
            # A set of this size prevented it; any larger set containing it is
            # not minimal, so the search stops here.
            break
    return new_outcomes, failures, specs


def _read_factual_outcome(
    layout: RunLayout, cfg: Optional[Config]
) -> Optional[CounterfactualOutcome]:
    """Load the factual outcome from disk, or ``None`` when it is not there."""
    try:
        return outcome_from_artifacts(layout, cfg)
    except FileNotFoundError as exc:
        LOGGER.warning(
            "no factual outcome to compare against (%s); the contribution report "
            "will report insufficient evidence",
            exc,
        )
        return None


def _result_rows(
    factual: Optional[CounterfactualOutcome],
    outcomes: Sequence[CounterfactualOutcome],
    failures: Sequence[Mapping[str, Any]],
    cfg: Optional[Config],
) -> List[Dict[str, Any]]:
    """One CSV row per replay, plus the factual run and any failed replay."""
    from .attribution import but_for, contribution_score, severity_reduction

    rows: List[Dict[str, Any]] = []
    if factual is not None:
        row = _base_row(factual)
        row["status"] = "factual"
        rows.append(row)

    for outcome in outcomes:
        row = _base_row(outcome)
        row["status"] = "completed"
        if factual is not None:
            row["but_for"] = but_for(factual, outcome)
            row["severity_reduction"] = severity_reduction(factual, outcome, cfg)
            row["contribution_score"] = round(
                contribution_score(factual, outcome, cfg), 6
            )
        rows.append(row)

    for failure in failures:
        rows.append(
            {
                "intervention_id": failure.get("intervention_id", ""),
                "action_id": failure.get("action_id", ""),
                "op": failure.get("op", ""),
                "targets_participant": failure.get("targets_participant", ""),
                "status": "failed",
                "error": failure.get("error", ""),
            }
        )
    return rows


def _base_row(outcome: CounterfactualOutcome) -> Dict[str, Any]:
    data = outcome.to_dict()
    return {
        "intervention_id": data["intervention_id"],
        "action_id": data["action_id"],
        "op": data["op"],
        "targets_participant": data["targets_participant"],
        "collision": data["collision"],
        "t_collision": data["t_collision"],
        "impact_speed": data["impact_speed"],
        "relative_impact_speed": data["relative_impact_speed"],
        "min_ttc": data["min_ttc"],
        "min_distance": data["min_distance"],
        "near_miss": data["near_miss"],
        "validation_passed": data["validation_passed"],
        "notes": "; ".join(data["notes"]),
        "error": "",
    }


# ---------------------------------------------------------------------------
# Metric extraction
# ---------------------------------------------------------------------------


def _collision_pairs(
    summary: Mapping[str, Any]
) -> Tuple[List[List[str]], Optional[float]]:
    """Canonical ``[[a, b], ...]`` pairs and the earliest collision time."""
    pairs: List[List[str]] = []
    times: List[float] = []
    for entry in summary.get("collision_pairs", []) or []:
        if isinstance(entry, Mapping):
            a, b, t = entry.get("a"), entry.get("b"), entry.get("t")
        elif isinstance(entry, (list, tuple)) and len(entry) >= 2:
            a, b = entry[0], entry[1]
            t = entry[2] if len(entry) > 2 else None
        else:
            raise ValueError(
                "unrecognised collision pair record {0!r} in the oracle "
                "summary".format(entry)
            )
        if a is None or b is None:
            raise ValueError(
                "collision pair record {0!r} does not name both participants".format(entry)
            )
        pairs.append(sorted([str(a), str(b)]))
        if t is not None:
            times.append(float(t))
    pairs.sort()
    return pairs, (min(times) if times else None)


def _encounter_pair(
    result: Any, summary: Mapping[str, Any], pairs: Sequence[Sequence[str]]
) -> Optional[Tuple[str, str]]:
    """The two participants whose separation defines this scenario's encounter.

    Preference order: the pair that actually collided, then the pair the scenario
    declared as its encounter, then the only two participants present. Anything
    else (three participants, no collision, no declaration) is genuinely
    ambiguous and yields ``None`` rather than a guess.
    """
    if pairs:
        first = pairs[0]
        return (str(first[0]), str(first[1]))

    spec = getattr(result, "spec", None)
    if spec is not None:
        declared = (getattr(spec, "validation", {}) or {}).get("encounter_pair")
        if declared and len(declared) >= 2:
            return (str(declared[0]), str(declared[1]))
        expected = getattr(spec, "expected_collision_pairs", None) or []
        if expected and len(expected[0]) >= 2:
            return (str(expected[0][0]), str(expected[0][1]))

    participants = [str(p) for p in summary.get("participants", []) or []]
    if len(participants) == 2:
        return (participants[0], participants[1])
    return None


def _validated_min_distance(validation: Mapping[str, Any]) -> Optional[float]:
    """Minimum separation as measured by the runner's scenario validation."""
    checks = validation.get("checks", {}) or {}
    block = checks.get("min_separation")
    if isinstance(block, Mapping) and block.get("distance_m") is not None:
        return float(block["distance_m"])
    return None


def _load_oracle_frames(result: Any) -> Optional[List[Dict[str, Any]]]:
    """Per-tick privileged state of a run, or ``None`` when it was not kept."""
    layout = getattr(result, "layout", None)
    if layout is None:
        return None
    path = Path(str(layout.oracle_trace))
    if not path.exists():
        return None
    return read_jsonl_gz(path)


def _actor_at(
    frame: Mapping[str, Any], participant_id: str
) -> Optional[Mapping[str, Any]]:
    for actor in frame.get("actors", []) or []:
        if str(actor.get("participant_id")) == participant_id:
            return actor
    return None


def _impact_speeds(
    frames: Sequence[Mapping[str, Any]],
    pair: Tuple[str, str],
    t_collision: float,
    max_gap_s: float = 0.25,
    tick_tolerance_s: float = 1e-3,
) -> Tuple[Optional[float], Optional[float]]:
    """Ground speed and relative speed of the pair immediately before impact.

    The **last pre-impact frame** is used, not the frame at the collision
    timestamp. The oracle records actor state after ``world.tick()``, and the
    collision sensor fires during the tick that resolves the contact, so the
    state stamped with the collision time already has the impulse applied: in the
    reference S01 run the striking vehicle reads 7.91 m/s one frame earlier and
    1.41 m/s at the collision frame. Reading the collision frame would therefore
    report the *rebound* speed and make every severity comparison meaningless.

    ``tick_tolerance_s`` absorbs the float noise between the sensor's timestamp
    and the tick's own. When the last pre-impact sample is further back than
    ``max_gap_s`` the trace and the collision record disagree, and ``None`` is
    the honest answer.
    """
    best: Optional[Tuple[float, Mapping[str, Any]]] = None
    for frame in frames:
        if _actor_at(frame, pair[0]) is None or _actor_at(frame, pair[1]) is None:
            continue
        t = float(frame.get("t", 0.0))
        if t > float(t_collision) - float(tick_tolerance_s):
            continue
        gap = float(t_collision) - t
        if best is None or gap < best[0]:
            best = (gap, frame)
    if best is None or best[0] > float(max_gap_s):
        return (None, None)

    frame = best[1]
    a = _actor_at(frame, pair[0])
    b = _actor_at(frame, pair[1])
    if a is None or b is None:
        return (None, None)

    speed_a = float(a.get("speed", 0.0))
    speed_b = float(b.get("speed", 0.0))
    dvx = float(a.get("vx", 0.0)) - float(b.get("vx", 0.0))
    dvy = float(a.get("vy", 0.0)) - float(b.get("vy", 0.0))
    relative = float((dvx * dvx + dvy * dvy) ** 0.5)
    return (max(speed_a, speed_b), relative)


def _min_ttc_and_distance(
    frames: Sequence[Mapping[str, Any]], pair: Tuple[str, str]
) -> Tuple[Optional[float], Optional[float]]:
    """Smallest defined time-to-collision and smallest separation of a pair.

    TTC follows the radar convention used everywhere else in the project: the
    range rate is negative while closing and TTC is undefined when the pair is
    not closing, which is "no evidence", not "safe".
    """
    min_ttc: Optional[float] = None
    min_distance: Optional[float] = None
    for frame in frames:
        a = _actor_at(frame, pair[0])
        b = _actor_at(frame, pair[1])
        if a is None or b is None:
            continue
        dx = float(b.get("x", 0.0)) - float(a.get("x", 0.0))
        dy = float(b.get("y", 0.0)) - float(a.get("y", 0.0))
        range_m = float((dx * dx + dy * dy) ** 0.5)
        if min_distance is None or range_m < min_distance:
            min_distance = range_m
        if range_m <= 1e-6:
            continue
        dvx = float(b.get("vx", 0.0)) - float(a.get("vx", 0.0))
        dvy = float(b.get("vy", 0.0)) - float(a.get("vy", 0.0))
        range_rate = (dx * dvx + dy * dvy) / range_m
        ttc = time_to_collision_1d(range_m, range_rate)
        if ttc is not None and (min_ttc is None or ttc < min_ttc):
            min_ttc = ttc
    return (min_ttc, min_distance)


def _is_near_miss(
    result: Any,
    min_distance: float,
    min_ttc: Optional[float],
    cfg: Optional[Config],
) -> bool:
    """Whether a collision-free run still came dangerously close.

    A replay that merely moves the crash out of frame is not a prevention worth
    celebrating, so the report distinguishes "no collision" from "no collision
    but a near miss". The run's own outcome classification counts when the runner
    produced one; otherwise the separation and TTC thresholds decide.
    """
    manifest = getattr(result, "manifest", None)
    outcome = getattr(manifest, "outcome", None)
    if outcome is not None and str(getattr(outcome, "value", outcome)) == "near_miss":
        return True

    distance_limit = (
        float(cfg.get("counterfactual.near_miss.min_distance_m", 5.0)) if cfg else 5.0
    )
    ttc_limit = (
        float(
            cfg.get(
                "counterfactual.near_miss.ttc_s",
                cfg.get("recorder.triggers.near_miss.ttc_s", 0.9),
            )
        )
        if cfg
        else 0.9
    )
    if min_distance <= distance_limit:
        return True
    return min_ttc is not None and min_ttc <= ttc_limit


def _finite_or_none(value: Optional[float]) -> Optional[float]:
    """``None`` for a missing or non-finite value; JSON has no ``inf``."""
    if value is None:
        return None
    number = float(value)
    if number != number or number in (float("inf"), float("-inf")):
        return None
    return number
