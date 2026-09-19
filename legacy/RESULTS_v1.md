> **These are V1 results. The current ones are in
> [`docs/RESULTS.md`](../docs/RESULTS.md), generated into
> [`results/`](../results/README.md).**
>
> Recorded from `artifacts_independent_clocks/` and, for the structural
> figures, scored against the scenario template rather than against a
> ground truth a reconstruction could match. [`docs/EVENTS.md`](../docs/EVENTS.md) explains why
> that comparison was unfair in both directions; `results/README.md` gives
> the same recordings rescored.
>
> Kept because the argument for the V2 refactor rests on being able to see
> what it replaced.

---

# Results

Every figure in this document is read from
[`legacy/results_v1/final_results.md`](results_v1/final_results.md), which
`cdf.evaluation.final_results` generates from the campaign's own artifacts.
Nothing here is transcribed by hand.

The recorded artifacts are far too large to commit, so the generator publishes
the three result files to `results/`, which is. That is the only reason this
page can link to a table at all — otherwise every reference would point into a
directory a fresh clone does not have, and "the numbers are checkable" would be
a claim you could not check. To regenerate:

```bash
python -c "import sys; sys.path.insert(0,'src'); \
           from cdf.evaluation.final_results import write_final_results; \
           write_final_results('artifacts_independent_clocks')"
```

The campaign: **13 scenario/variant combinations across nine scenarios, three
seeds each, 39 runs**, every recorder on its own clock, no stage of the
reconstruction able to read the simulator's. Counterfactual replays were run on
seed 0 of every variant; a replay sweep costs a full simulator run per
intervention, and the verdict is a property of the scenario rather than of the
seed.

The earlier synchronized-clock campaign is retained in `artifacts/` as a
historical baseline. It is **not** averaged in: `cdf.common.campaign` marks a
run recorded under a different clock protocol as foreign, because two campaigns
averaged together answer no question anyone asked.

---

## How to read these numbers

Three things will otherwise mislead.

**A negative control has nothing to attribute.** `S01/avoided`, `S02/avoided`
and `S04/yield` were designed not to collide. Their precision, recall and F1 are
vacuously 1.0, and including them would inflate every attribution mean. They are
excluded from those means and reported separately, on the only question that
applies to them: did the system name anybody who did not exist?

**Strict structural recall has a ceiling well below 1.0.** The reference graph
is built from the scenario's designed causal template, and most of its edges
leave an `ORACLE_SCRIPTED_INTERVENTION` node — a privileged event type recording
that the scenario script fired. No reconstruction has a node of that type to put
at the tail of an edge, so those edges cannot be matched strictly no matter how
well the incident was reconstructed. Every ablation record carries the resulting
ceiling, and the achieved recall is reported against it.

**A richer reconstruction loses precision against a sparse reference.** The
oracle template is an intentionally minimal account of the designed mechanism.
A reconstruction that recovers the mechanism *and* the surrounding kinematics
produces more edges than the template contains, and is scored down for them.
This is why edge F1 and edge recall move in opposite directions across the
ablation, and both are reported.

---

## The results

**[`legacy/results_v1/final_results.md`](results_v1/final_results.md)** holds the two
tables this project is judged on — per-scenario attribution, and the method
ablation — together with the campaign's headline figures, the clock ablation and
the model-checking tally. It is the authoritative version of every number
discussed below, `results/final_results.csv` is the same per-scenario table for
a spreadsheet, and `results/final_results.json` carries everything including the
per-run rows the means were taken over.

### What the replays established

The counterfactual sweep is where the vocabulary earns its keep, and the answers
it produced are more varied than a single-verdict system could express.

**S06, the three-vehicle chain, is `contributing_but_not_necessary`.** Eight
single-action replays and three pairwise composites — the bounded joint search
ran, because no single removal had prevented anything — and none of the eleven
prevented the collision. All three drivers' braking substantially reduced its
severity. The chain happens either way; the braking cascade is what makes it
hard. The report says exactly that, and names no initiator, because none was
established.

**S06's other variant, `b_rear_first`, is `insufficient_evidence` for a reason
worth stating.** No single removal prevents the crash, and removing some of the
braking makes the impact *worse*. Those actions did not contribute to the
collision; they reduced one they did not bring about. That is reported as a
mitigating finding rather than as "nothing changed", because the two are
opposites and a report that collapsed them would discard half of what the replay
showed.

**S01, the rear-end, is `shared_contribution`.** Removing either driver's
braking independently prevents the collision: B's emergency brake is what A
fails to leave room for, and A's late brake is what fails to recover. Either
change alone would have been enough, so no single initiator is named — which is
a different finding from a joint contribution, where neither change alone would
have sufficed.

### What went right

**Restraint holds completely.** Across the negative controls the system named
nobody. Zero false attributions. This is the result the project would most
regret getting wrong: a forensic tool that invents a culprit when nothing
happened is worse than one that stays silent when something did, and averaging
the controls into an F1 would have let a confident wrong answer on one be
cancelled by a correct answer elsewhere.

**Causal reasoning after fusion recovers relations no single vehicle could
claim.** Canonical edge recall rises monotonically across the three arms:
best single vehicle → merged logs → merged logs plus global reasoning. The
inferred edges are exactly the cross-vehicle ones — *B braked, so the gap A was
measuring closed* — which no local rule can produce, because no recorder
observed both events.

**The incident is reconstructed accurately in space and time.** Collision times
are recovered to within tens of milliseconds of the truth on the estimated
common clock, with pair recall close to 1.0 and a single spurious collision
across the whole campaign — including in the three-vehicle chain, where the two
impacts must also be put in the right order.

**Strict edge recall improves monotonically too, and reaches its ceiling on
roughly half the runs.** Read against the ceiling rather than against 1.0, the
merged-plus-reasoning account recovers every strictly reachable edge on a large
fraction of the campaign. The exact counts are in the generated table; they are
not restated here, because a number transcribed into prose is a number that will
eventually be wrong.

### What went wrong

These are reported because they happened, not because they are convenient.

**Strict edge F1 does not improve across the ablation — it falls.** Precision
drops faster than recall rises, for the reason given above: the reconstruction
is richer than the reference. On two scenarios the best *single vehicle* scores
a higher strict edge F1 than the merged account, because its graph is smaller
and therefore denser in template-matching edges. A reader who cares only about
strict F1 should conclude that fusion did not help by that measure, and that is
a fair reading of it.

**Attribution is only partly correct.** Exactly the designed contributors are
named on some scenarios; a subset or a superset on others. The per-scenario
verdict column says which is which, and the campaign's exact-set accuracy is
well below 1.0.

**The graph alone names the wrong vehicle when the cause was an absence.** S08's
designed cause is `B_fail_to_yield` — B enters the junction without slowing.
Nothing happened, so no event node exists to root a causal chain at, while A's
reaction produces a chain full of them. The graph-only hypothesis therefore names
A: the vehicle that responded to the hazard rather than the one that created it.

The counterfactual replay gets it right, because removing the non-action is
something the simulator can do even though no recorder could observe it. This is
the clearest argument in the campaign for reporting both: where they disagree,
the replay is the one to believe, and the disagreement itself is informative
about what kinds of cause the reasoning layer cannot see.

**One scenario variant was not reconstructed at all.** In `S02/avoided`, one
recorder shares too few observations with the other for the alignment to place
it on the common timeline. The run produces no reconstruction rather than a
guessed one, which is the correct behaviour and also a real gap in coverage.

**Model checking reports many violations, and they are real.** Across the
campaign the properties fail far more often than they pass. That is what a set
of crash scenarios should produce: a vehicle that entered a conflict without
responding, or applied throttle within three seconds of an impact, genuinely
violated the property being monitored. The counterexample witnesses carry the
evidence — response latencies, throttle magnitudes, conflict counts. `UNKNOWN`
outnumbers both, because a finite trace that never exhibits a property's premise
can neither satisfy nor violate it, and that is reported as its own verdict
rather than folded into a pass rate.

**Some clocks cannot be aligned at all.** In runs where two recorders share too
few observations, the alignment reports `UNRESOLVED_TIME_ALIGNMENT` rather than
guessing. Those runs produce no cross-view reconstruction figure, which is
recorded as `unaligned_recorders` rather than quietly scored as zero error.

**Clock drift is not observable.** Over a ten-to-fifteen-second encounter a
realistic crystal deviation moves a timestamp by far less than the radar noise
the estimate is fitted from, so the solver pins `scale` to 1.0 and fits the
offset only. The drift error reported by the evaluation is therefore the error
of a parameter that was *declined*, not one that was estimated badly.

---

## Ablations

### Clock protocol

| Arm | Protocol |
|---|---|
| A | synchronized control — the same recording restamped onto the simulator clock using the true profiles |
| B | independent recorder clocks, timestamps taken at face value |
| C | independent recorder clocks, alignment estimated from shared observations (**the protocol the campaign reports**) |

Arm A is a **control, not a separate physics run**: the same recording is
restamped onto the simulator clock using the true profiles, so all three arms
describe one set of physical events and the comparison is about time alone.

The result splits, and both halves matter.

**The alignment substantially improves timestamp accuracy.** Mean absolute
offset error falls roughly fourfold from arm B to arm C. Every quantity measured
in seconds or metres — collision time, collision location, the cross-view
trajectory RMSE — depends directly on that, and at the speeds in these scenarios
a fifth of a second is several metres of position error.

**It does not measurably change the graph.** Node F1, edge F1 and edge recall are
flat across all three arms, within the noise of the campaign. This is not a
failure of the alignment; it is a property of the comparison. The event matcher's
tolerance is 1.5 s, and the uncorrected offset is an order of magnitude smaller
than that, so a misalignment of this size never moves an event across the
matching threshold. The structural metrics are simply insensitive to a clock
error this small.

Reporting it the other way round — quoting the improvement in seconds and
implying the graph improved with it — would be the easy and dishonest reading.
What the ablation actually establishes is that the alignment is necessary for
the *reconstruction* claims and, at these offset magnitudes, neutral for the
*structural* ones.

### Method

| Arm | What it has |
|---|---|
| Best Local (`best_local`) | one vehicle's own graph; the strongest of them, not the mean |
| Simple Fusion (`simple_fusion`) | identities resolved, clocks aligned, graphs merged — every edge still claimed inside one vehicle's log |
| Fusion + Global Causal Reasoning (`fusion_global_reasoning`) | the same merge, plus edges between claims made by different vehicles |

The arms differ in exactly one configuration key
(`fusion.post_fusion.enabled`), are derived from identical recordings, and are
scored against the same reference. Nothing is re-simulated, so the difference
between them is the method rather than the run.

Taking the *best* local viewpoint rather than the mean is deliberate: it makes
the baseline as hard to beat as the evidence allows.

---

## Related

- [EXPERIMENT_PROTOCOL.md](../docs/EXPERIMENT_PROTOCOL.md) — what the campaign measures
- [LIMITATIONS.md](../docs/LIMITATIONS.md) — what these numbers do not establish
- [REPRODUCIBILITY.md](../docs/REPRODUCIBILITY.md) — regenerating all of it
