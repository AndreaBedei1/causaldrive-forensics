# Counterfactual replay

The causal graph says what led to what. It cannot say whether any of it was
*necessary*, because a graph built from correlated evidence will happily draw an
arrow from a behaviour that changed nothing. The only way to settle that in a
simulator is to go back and run the encounter again without the behaviour, with
everything else held identical, and see whether the outcome survives.

That is what this stage does, and the vocabulary it produces is the project's
actual output.

---

## One replay

An **intervention** is a controlled modification of one scripted action:

| Operation | Effect |
|---|---|
| `disable` | the action never fires |
| `delay` / `advance` | its `t_start` moves by *n* seconds |
| `scale` | one of its parameters is multiplied |
| `set` | one of its parameters is assigned |

Everything else — map, spawn points, routes, seeds, controller gains, sensor
configuration, the clock profiles — is byte-identical to the factual run. The
replay is written to `counterfactual/replays/<intervention_id>/` as a complete
run in its own right, with its own recordings, so it can be inspected, scored
and re-analysed exactly like the run it came from.

A replay that no longer produces the designed encounter is marked as failing
validation. This matters: if removing B's brake means A and B never come within
twenty metres of each other, the replay has not shown that the brake caused the
crash — it has shown that the scenario stopped being the scenario. The
validation verdict travels with the outcome and the viewer prints it.

## Sets of actions, not just single ones

Single-action replay answers *was this action necessary?* It cannot answer the
question a multi-vehicle incident usually poses, which is whether **any** single
change would have been enough at all.

Two vehicles can each contribute without either being individually decisive.
Remove A's behaviour and the crash still happens; remove B's and it still
happens; remove both and it does not. Single-action replay reports that as
*insufficient evidence*, which is true and useless.

So a replay may change a **set** of actions at once. The search is bounded and
deliberately lazy:

1. Run the factual encounter.
2. Run every single-action removal.
3. **If any single removal prevented the collision, stop.** A set containing it
   would not be minimal, so there is nothing to learn from running one.
4. Otherwise grow the set size by one, replay the combinations in lexicographic
   order (so a campaign is reproducible), and stop at the first size that
   prevents — which is what makes the set it finds minimal.

`counterfactual.combinations.max_combination_size` and `max_replays` bound the
cost. What the budget did not reach is recorded, never silently dropped.

## The five verdicts

| Class | Established when |
|---|---|
| `single_initiator` | exactly one action, removed alone, prevents the collision |
| `shared_contribution` | two or more actions each prevent it **on their own** — either change alone would have been enough |
| `joint_contribution` | no single action prevents it, but some minimal set of two or more does |
| `contributing_but_not_necessary` | no tested set prevents it, but removing an action measurably reduces its severity |
| `insufficient_evidence` | nothing tested changed the outcome, or there was nothing testable |

`shared_contribution` and `joint_contribution` are different findings and the
distinction is load-bearing. The first says either driver could have avoided it
alone; the second says neither could.

## Minimal prevention sets, honestly scoped

A **minimal prevention set** is an inclusion-minimal tested set whose joint
removal prevents the collision.

Minimality is asserted only over what was **actually replayed**. A set all of
whose proper subsets were tested, none of which prevented, is `minimal`
outright. A set with an untested proper subset is `minimal_within_tested`, and
the subsets nobody ran are named in the artifact and printed in the viewer —
because an untested subset might have sufficed, and claiming otherwise would be
a statement about a replay nobody performed.

```json
{
  "actions": ["B_emergency_brake", "C_late_brake"],
  "size": 2,
  "minimality": "minimal",
  "untested_subsets": [],
  "note": "every proper subset was replayed and none prevented the collision"
}
```

## Severity, when prevention fails

When no tested change prevents the collision, the replays are compared on
severity instead — impact speed, relative impact speed, minimum distance — with
the threshold `counterfactual.contribution.min_severity_reduction` applied
explicitly, so a difference smaller than the noise is reported as nothing rather
than as a weak contribution.

The sign of that difference carries a finding of its own, and the two directions
must not be collapsed:

* removing the action **softened** the impact → `contributing_but_not_necessary`:
  the action contributed to how bad it was, without being necessary for it to
  happen at all;
* removing the action made the impact **worse** → the action is reported in
  `mitigating_actions`: it *reduced* an outcome it did not bring about.

The second is not a weaker version of the first, it is its opposite, and a report
that folded both into "nothing changed" would discard half of what the replay
established. `S06/b_rear_first` is the case in this campaign: no single removal
prevents the chain collision, and removing some of the braking raises the impact
speed. Those brakes did not cause the crash; they reduced one they did not bring
about. The verdict is `insufficient_evidence` — correctly, because no initiator
was established — and the rationale says which of the two it found.

## Negative controls

Three scenario variants are designed **not** to collide: `S01/avoided`,
`S02/avoided` and `S04/yield`. On those the factual run produces no outcome, and
the only thing worth measuring is whether the system stays silent.

It is reported as its own number — `false_attribution` — and never folded into
an F1 mean. Averaging it in would let a confident wrong answer on a control be
cancelled out by a correct answer elsewhere, which is exactly the error a
forensic tool must not make.

---

## What a contribution score is, and is not

A contribution score states **what changed when the simulator re-ran the
encounter under a controlled modification**. Every artifact that carries one
carries this with it:

> Causal contribution under controlled replay semantics. NOT legal fault and NOT
> a fault percentage.

The project's vocabulary is: *causal initiator*, *causal contributor*, *shared
causal contribution*, *joint causal contribution*, *causal chain*, *insufficient
evidence*. It does not say *guilty*, *at fault*, *liable*, or *70% responsible*,
and a test walks the artifacts to make sure it never starts.

Legal fault depends on right of way, traffic law, jurisdiction, duty of care and
what each driver could reasonably have foreseen. None of that is in the
recordings and none of it is inferred here.

---

## Running it

One recorded run:

```bash
python -m cdf.cli counterfactuals --run artifacts_independent_clocks/S06_chain_collision/seed_000_a_front_pushed
```

A whole campaign, one seed per variant:

```bash
python scripts/run_counterfactuals.py --artifacts artifacts_independent_clocks --seeds 0
```

Add `--fresh` to re-record every replay instead of reusing one already on disk.
Use it when the existing replays were recorded back-to-back on a single
simulator session: the configuration warns that repeated runs in one session
drift enough to change an outcome class, which would confound the very
difference being measured. The per-replay restart only happens when the session
can restart the server, which means `$CARLA_ROOT` must point at the
installation; without it the restart degrades to reuse, with a warning.

Outputs, per run:

| File | Contents |
|---|---|
| `counterfactual/intervention_results.csv` | one row per replay, including the factual one |
| `counterfactual/counterfactual_manifest.json` | what was requested, what completed, what failed |
| `counterfactual/causal_contribution.json` | the verdict, the scores, the prevention sets |
| `counterfactual/replays/<id>/` | each replay as a complete run |

The viewer's **Attribution** tab renders all three: the verdict with its
rationale, the prevention sets with their minimality caveats, and the replay
table with the validation status of each.

## Related

- [CAUSAL_MODEL.md](CAUSAL_MODEL.md) — where the candidate causes come from
- [GRAPH_FUSION.md](GRAPH_FUSION.md) — the graph the hypothesis is read off
- [RESULTS.md](RESULTS.md) — what the campaign found
- [LIMITATIONS.md](LIMITATIONS.md) — what replay semantics cannot establish
