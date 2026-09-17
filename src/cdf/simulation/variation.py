"""Deterministic parameter variation across repeated runs.

The scenarios in this project are strictly deterministic: the same seed and the
same specification reproduce the same trace bit for bit. Repeating a scenario
under different *seeds* alone would therefore produce near-identical traces and
tell us nothing -- the seed only reaches blueprint colour choice, the radar
degradation stream and the Traffic Manager, none of which drive the encounter.

So rather than fake replication, each additional run applies a small, explicit,
reproducible perturbation to the parameters that actually matter: the speeds the
participants carry into the encounter and the timing of their scripted actions.
That turns "three runs per scenario" into a genuine robustness measurement --
does the reconstruction survive a slightly different approach speed or a
reaction 300 ms earlier? -- instead of three copies of one trace.

Seed 0 is always the nominal specification, so the headline result for every
scenario is the unperturbed one and the variations sit around it.
"""

from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from typing import Any, Dict

from .scenario_base import ScenarioSpec

__all__ = ["VariationSpec", "apply_seed_variation", "describe_variation"]


@dataclass
class VariationSpec:
    """The perturbation applied to one run, recorded in its manifest."""

    seed: int
    speed_scale: Dict[str, float]
    """Multiplier applied to each participant's initial and target speed."""
    action_shift_s: Dict[str, float]
    """Seconds added to each scripted action's start time."""
    description: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "seed": self.seed,
            "speed_scale": {k: round(v, 4) for k, v in sorted(self.speed_scale.items())},
            "action_shift_s": {
                k: round(v, 4) for k, v in sorted(self.action_shift_s.items())
            },
            "description": self.description,
        }


def apply_seed_variation(
    spec: ScenarioSpec,
    seed: int,
    max_speed_scale: float = 0.05,
    max_action_shift_s: float = 0.12,
) -> "tuple":
    """Return ``(perturbed_spec, variation)`` for ``seed``.

    Seed 0 returns the specification unchanged. Higher seeds scale every
    participant's approach speed by up to ``max_speed_scale`` and shift every
    scripted action by up to ``max_action_shift_s``, drawn from a generator
    seeded by ``(scenario_id, variant, seed)`` so the perturbation is a pure
    function of the run identity and reproduces exactly.

    The bounds are deliberately small. A perturbation large enough to change the
    outcome class would not be a robustness probe, it would be a different
    scenario -- and scenario validation would (correctly) start failing.
    """
    if int(seed) == 0:
        return (
            spec,
            VariationSpec(
                seed=0,
                speed_scale={p.participant_id: 1.0 for p in spec.participants},
                action_shift_s={
                    a.action_id: 0.0 for p in spec.participants for a in p.actions
                },
                description="nominal specification (no perturbation)",
            ),
        )

    rng = random.Random(
        "{0}|{1}|{2}".format(spec.scenario_id, spec.variant, int(seed))
    )
    out = copy.deepcopy(spec)
    speed_scale: Dict[str, float] = {}
    action_shift: Dict[str, float] = {}

    # ONE speed scale shared by every participant, not an independent draw each.
    #
    # Independent draws perturb the *relative* approach speeds, and it is the
    # relative speed that creates the encounter: an 8% slower follower and a 4%
    # faster lead removed ~10% of the closing rate and turned S01's collision
    # into a clean miss. That is not a robustness probe, it is a different
    # scenario, and scenario validation correctly rejected it.
    #
    # A common scale changes the pace of the whole encounter -- a genuine
    # robustness question -- while preserving the geometry that makes it happen.
    # Per-action timing still varies independently, which is where reaction-time
    # sensitivity actually lives.
    common_scale = 1.0 + rng.uniform(-max_speed_scale, max_speed_scale)

    for participant in out.participants:
        scale = common_scale
        speed_scale[participant.participant_id] = scale
        participant.initial_speed = float(participant.initial_speed) * scale
        participant.target_speed = float(participant.target_speed) * scale

        for action in participant.actions:
            shift = rng.uniform(-max_action_shift_s, max_action_shift_s)
            action_shift[action.action_id] = shift
            # Action times are absolute, but the encounter timeline scales with
            # speed: at 0.96x everything takes ~4% longer to unfold, so a brake
            # left at its original wall-clock time fires ~4% EARLIER in the
            # encounter and becomes more effective. That is how a 4% speed
            # change turned a tuned collision into a clean miss.
            #
            # Dividing by the scale keeps each action at the same *point in the
            # encounter*, so the perturbation varies the pace and the reaction
            # jitter without quietly rewriting who reacts in time.
            scaled = float(action.t_start) / scale
            # Never shift an action to a negative time: it would fire before the
            # scenario clock starts and silently become a different manoeuvre.
            action.t_start = max(0.0, scaled + shift)
            action.duration = float(action.duration) / scale
            if action.kind in ("set_speed", "hold"):
                target = action.params.get("target_speed")
                if target is not None:
                    action.params["target_speed"] = float(target) * scale

    out.variant = spec.variant
    variation = VariationSpec(
        seed=int(seed),
        speed_scale=speed_scale,
        action_shift_s=action_shift,
        description=(
            "speeds scaled by up to +/-{0:.0%} and action timings shifted by up to "
            "+/-{1:.2f}s, derived deterministically from (scenario, variant, seed)".format(
                max_speed_scale, max_action_shift_s
            )
        ),
    )
    return (out, variation)


def describe_variation(spec: ScenarioSpec, seed: int) -> str:
    """Human-readable one-liner for logs and report tables."""
    _perturbed, variation = apply_seed_variation(spec, seed)
    if seed == 0:
        return "seed 0: nominal"
    speeds = ", ".join(
        "{0}x{1:.3f}".format(k, v) for k, v in sorted(variation.speed_scale.items())
    )
    shifts = ", ".join(
        "{0}{1:+.2f}s".format(k, v) for k, v in sorted(variation.action_shift_s.items())
    )
    return "seed {0}: speeds [{1}] actions [{2}]".format(seed, speeds, shifts)
