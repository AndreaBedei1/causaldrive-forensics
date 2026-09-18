> **Superseded by [CLOCKS.md](CLOCKS.md).**
>
> This describes the V1 radar-based clock estimator, which fitted range and
> range rate against another vehicle's recorded trajectory and read both an
> offset and a drift rate off that fit.
> 
> It is still accurate, and the estimator still runs as a diagnostic so the
> clock ablation can compare the two. It is no longer the method the results
> are computed from: a drift rate fitted over a 25 s window from noisy radar
> is a number with more decimal places than evidence behind it. The V2 method
> anchors on shared physical contact -- one equation, one unknown, no fitting.
> Read [CLOCKS.md](CLOCKS.md).

---

# Clock synchronisation

Three cars crash. Three recorders describe it. Nothing guarantees their clocks
agree, and everything downstream — which vehicle braked first, whether A's gap
closed *because* B slowed, which impact came first in a chain collision —
depends on placing those three descriptions on one timeline.

This is the part of the problem a simulator makes it easy to cheat on. CARLA
hands every actor the same `elapsed_seconds`, so a fusion stage that reads it
gets perfect synchronisation for free and the resulting reconstruction proves
nothing about the real problem. This project therefore gives every recorder its
own clock, and the fusion stage is never allowed to see the simulator's.

---

## The two clocks

Each recorder stamps its own samples with

```
t_local = true_scale * t_sim + true_offset_s + jitter
```

`true_scale`, `true_offset_s` and the jitter distribution are drawn per
participant per run from `clocks.*` in `configs/default.yaml`, and written to
`oracle/clock_ground_truth.json` — a **privileged** file. It exists so the
evaluation can score the estimate. Nothing in `cdf.local`, `cdf.fusion`,
`cdf.graph` or `cdf.checking` may read it, and
`tests/test_no_privileged_leakage.py` fails the build if any of them imports the
module that writes it.

Fusion estimates, for every participant, a transform onto a shared timeline:

```
t_common = scale * t_local + offset_s
```

One participant is chosen as the **gauge** — its transform is the identity, by
definition, because a common timeline has no natural zero. Every other
recorder's transform is fitted against it.

---

## What the estimate is fitted from

Only from evidence the participants exchanged. Five independent families of
residual, each of which relates one vehicle's observation of another to that
other vehicle's own record of itself:

| Constraint | What it compares |
|---|---|
| `radar_position` | where A's radar puts B against where B says it was |
| `radar_range` | the range A measured against the distance implied by both trajectories |
| `radar_range_rate` | the closing speed A measured against the relative velocity implied |
| `target_velocity` | the velocity A estimated for B against B's own recorded velocity |
| `heading` | the heading A observed for B against B's own recorded heading |

Each family yields a set of `(t_a, t_b)` correspondences. A single pair of
recorders usually produces hundreds of them, and they disagree, because radar is
noisy and a track is an estimate. The offset that best explains them all is
found by a robust least-squares fit (`soft_l1` loss), which is what keeps one
badly-tracked frame from dragging the answer.

Collisions supply a sixth, much stronger constraint. Two vehicles that touch
were in the same place at the same instant, and both recorded a local collision
trigger. The trigger says *that* the vehicle was struck — the local sensor
channel deliberately does not reveal *by whom*, which is a separate inference
described in [GRAPH_FUSION.md](GRAPH_FUSION.md) — but the timestamps alone anchor
the two timelines tightly.

## Solving it as a graph

With three or more participants the pairwise estimates are over-determined and
mutually inconsistent: A→B and B→C and A→C will not compose exactly. The fit is
therefore global. Participants are nodes, pairwise constraints are edges
weighted by how much evidence supports them, the gauge is the node with the
highest evidence-weighted degree (lexical tie-break, so the choice is
reproducible), and every transform is solved simultaneously against it.

A pair with no shared observations is not silently given the identity transform.
It is reported `UNRESOLVED`, and every downstream claim that would have needed
it is reported as unresolved too.

## Drift

`scale` is drift. In a run of ten to fifteen seconds a realistic crystal
deviation of tens of parts per million moves a timestamp by well under a
millisecond — far below the radar noise the estimate is fitted from. The solver
therefore usually cannot observe drift at all, and says so: the participant's
`drift_status` reads `OFFSET_ONLY_UNOBSERVABLE_DRIFT`, `scale` is pinned to 1.0,
and only the offset is fitted.

This is a deliberate refusal. Fitting a two-parameter model to data that
constrains one parameter would produce a scale estimate that looks like a
measurement and is actually noise. The viewer's clock panel and every uncertainty
listing carry the status, so a reader can see which parameter was measured and
which was declined.

## What the residual means

Each participant's `residual` is what the fit itself reports: the spread of the
constraints it could not satisfy. It is computed without reference to the truth,
so it is available at inference time and is used — the post-fusion causal stage
widens its temporal tolerance by exactly the alignment's own residual, so a pair
of recorders that reconciled badly is given a correspondingly wider benefit of
the doubt rather than a fixed constant.

The evaluation additionally computes `offset_error_s` and `drift_error_ppm`
against `clock_ground_truth.json`. Those are scoring quantities and never reach
the inference path.

---

## Why the errors show up as metres

The campaign's headline reconstruction figure is a *cross-view* trajectory RMSE:
where one vehicle's radar, resolved to an identity and placed on the estimated
common clock, puts another vehicle, against where that vehicle truly was. That
number folds radar error, identity resolution and clock error together, which is
the honest accounting — a position estimate at the wrong time is a wrong
position estimate.

Only the last hop — common time to physical time, through the gauge's true
profile — is privileged, and it is unavoidable: the common clock's zero is
arbitrary and nothing else can anchor it.

A second figure, self-localisation RMSE, is reported and explicitly discounted.
It is exactly zero, because this simulator models no localisation noise: it
verifies that the recorder copies the pose faithfully and says nothing at all
about reconstruction quality. It is labelled as such in every artifact rather
than quoted as a result.

---

## Reading the result

`fusion/time_alignment.json` per run:

```json
{
  "reference": "A",
  "reference_rule": "maximum accepted evidence-weighted degree; lexical tie break",
  "formula": "t_common = scale * t_local + offset_s",
  "offsets": {
    "B": {
      "scale": 1.0,
      "offset_s": 0.0424,
      "residual": 0.1069,
      "confidence": 0.903,
      "status": "ALIGNED",
      "drift_status": "OFFSET_ONLY_UNOBSERVABLE_DRIFT",
      "methods": ["heading", "local_collision_supplement", "radar_position",
                  "radar_range", "radar_range_rate", "target_velocity"],
      "n_constraints": 1,
      "n_samples": 117
    }
  }
}
```

The viewer renders the same table under **Evidence → Recorder clocks**, with the
residual column beside the estimate, because an estimate shown without its
residual is an assertion.

---

## Ablation

`cdf.evaluation.clock_ablation` re-runs the campaign's scoring under three
protocols:

- **A — shared clock.** Every recorder reads the simulator. This is the
  historical baseline in `artifacts/`, retained for comparison and never mixed
  with the final campaign; `cdf.common.campaign` marks a run recorded under a
  different protocol as *foreign* rather than averaging it in.
- **B — independent clocks, estimated alignment.** The final campaign.
- **C — independent clocks, no alignment.** Timestamps taken at face value, to
  show what the alignment is buying.

## Related

- [DATA_BOUNDARY.md](DATA_BOUNDARY.md) — why the simulator clock is privileged
- [GRAPH_FUSION.md](GRAPH_FUSION.md) — what the common timeline is then used for
- [EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md) — how the ablation is run
