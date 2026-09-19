# Results

The final V2 campaign. Every figure on this page is read from
[`results/final_results.md`](../results/final_results.md) and
[`results/final_results.json`](../results/final_results.json), which
`cdf.evaluation.final_results` generates from the campaign's own artifacts.
Nothing here is transcribed by hand.

To regenerate:

```bash
python -c "import sys; sys.path.insert(0,'src'); \
           from cdf.evaluation.final_results import write_final_results; \
           write_final_results('artifacts_v2')"
```

Historical V1 results are in [`legacy/RESULTS_v1.md`](../legacy/RESULTS_v1.md)
and [`legacy/results_v1/`](../legacy/results_v1/). They are not averaged in: V2
changed the sensors and the timing semantics, so a figure over both campaigns
would describe neither, and `cdf.common.campaign` refuses an artifacts root
holding runs of both generations.

---

## 1. Campaign

| | |
|---|---|
| Artifacts root | `artifacts_v2` |
| Clock protocol | `independent_local_clocks` |
| Scenarios | 16 |
| Scenario variants | 35, of which 26 are designed to collide and 9 are negative controls |
| Seeds | 0, 1, 2 |
| Runs | 105 recorded, 105 evaluated, 0 evaluation exceptions |
| Simulator | CARLA 0.9.15, Town05, synchronous mode, 0.05 s tick |
| Scenario validation | passed on 83 of 105 runs |

Every recorder is on its own clock. No stage of the reconstruction reads the
simulator's clock, the map, or any other vehicle's state. The privileged record
is opened only afterwards, to score.

The 22 validation failures are all in the new S10 to S16 set and are listed in
section 9. A run that failed validation is still recorded, still evaluated and
still counted; what failed is the scenario staging its intended encounter, and
suppressing those runs would be choosing the sample after seeing it.

## 2. Reconstruction

This is the part that works.

| Measure | Value |
|---|---|
| Incidents reconstructed | 32 of 35 variants |
| Collision pair recall | 0.994 |
| Collision time error | 0.0043 s mean |
| Collision location error | 0.0211 m mean |
| Spurious collisions | 42, spread over 33 of the 105 runs |
| Cross-view trajectory RMSE | 1.503 m |

An incident is a collision or a near miss, so the 32 includes the negative
controls where the correct answer is a near miss and no collision.

Recall is near perfect and precision is the weak side. The 42 spurious
collisions concentrate in a few scenarios: S13 contributes 12, S12 and S16 six
each, S04 five, S10 and S11 four each, S06 three, S14 two. A spurious collision
is a claimed impact that no true impact matches on both pair and time.

The 1.503 m cross-view RMSE is the distance between where one vehicle's radar
put another and where that vehicle really was, on the estimated common clock. It
is not localisation error: this simulator models no localisation noise, so a
recorder's own position is exact by construction, and that self-localisation
figure is reported separately as the control it is.

## 3. Time synchronization

Each recorder has its own offset. The method estimates them from evidence the
vehicles recorded, preferring a shared physical impact, falling back to radar
trajectory consistency, and refusing to place a recorder it cannot reach.

| Source | Recorders | Scored | Offset MAE | Worst |
|---|---|---|---|---|
| `REFERENCE` | 105 | 105 | 0.000000 s | 0.000000 s |
| `CONTACT` | 89 | 89 | 0.007717 s | 0.249677 s |
| `RADAR` | 14 | 14 | 0.013007 s | 0.046226 s |
| `ACQUISITION_START` | 30 | 30 | 0.000003 s | 0.000008 s |
| `UNRESOLVED` | 14 | 0 | no offset to score | |
| **all** | 252 | 238 | **0.003651 s** | 0.249677 s |

Participant-weighted: every recorder counts once. The reference recorder's error
is zero by definition, because a common timeline is only fixed up to a constant.

`ACQUISITION_START` is not part of the method. Thirty runs never had an impact
and never had usable radar geometry, so they fall back on a marker declared by
the experiment harness, which starts every recorder within one tick. It is
labelled apart and never counted as a contact result. It is not simulator time:
each recorder keeps its own clock and its own jitter, and only the single
constant relating them comes from the harness.

Fourteen recorders stayed `UNRESOLVED`. They keep their own clock and say so,
rather than being placed on a guess.

**Drift is not estimated; scale is fixed to 1.** Over the 133 non-reference
recorders the true relative drift this leaves unmodelled averages 59.23 ppm and
reaches 180.60 ppm at worst. Over the longest run in the campaign, 30 s, that
worst case accumulates 0.0054 s against a 0.05 s tick, which is why fitting a
rate was not worth the extra parameter. It is a control value, not an estimator
score.

The headline table in the generated report quotes 0.00519 s instead. That is the
same error averaged per scenario variant rather than per recorder. The two
numbers average different populations and do not contradict each other; both are
labelled for what they aggregate.

Details of the hierarchy: [CLOCKS.md](CLOCKS.md).

## 4. Perception

From real campaign frames only. The synthetic detector tests are unit tests, not
perception results.

| What | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| STOP signs | 46 | 37 | 5 | 55.4% | 90.2% |
| Give-way signs | 0 | 1 | 0 | 0.0% | no real instances |
| Stop lines | 26 detections | no reference | | | |
| Lane markings | 0 detections | no reference | | | |

The STOP detector is classical colour and shape, deterministic, with no training
data. It finds nine signs in ten and reports roughly two for every three that
are there. Recall is the useful half: a missed sign removes the obligation from
the analysis entirely, while an extra one is visible and can be argued with.

**There is no verified stop-line reference in Town05.** The stop-line position is
derived from the sign and the lane, and the map paints no bar at these junctions,
so no line here is physically verified. The 26 crossings the detector reported
are counted and not scored. Calling them false positives would charge the
detector with missing markings the map never painted.

Lane markings have no independent reference by construction: the lane sensor is
an onboard ADAS signal, so the sensor is the measurement.

Detection latency is not reported. The privileged record says where each sign is,
not when it first became visible from the approach, and that depends on speed and
geometry. A latency against a baseline that was never recorded would be a
fabricated number.

## 5. Temporal properties

The same formulae run over the merged reconstruction and over the observable
ground truth, so a disagreement is about the reconstruction rather than about two
readings of the same word. UNKNOWN is never folded into PASS.

| Comparable | Agree | Agreement | False violations | Missed violations |
|---|---|---|---|---|
| 171 | 130 | 76.0% | 7 (4.1%) | 34 (19.9%) |

Missed violations concentrate in P3 (23) and P4 (11); false violations in P4 (6)
and P3 (1). Undecided verdicts concentrate in P7 (22), P4 (9) and P5 (6).

A property whose premise never occurs in a finite trace can neither be satisfied
nor violated, and reports UNKNOWN. Reading that as a pass would inflate every
rate on this page.

Details: [FORMAL_METHODS.md](FORMAL_METHODS.md).

## 6. Physical causality and responsibility

Two different claims, kept apart. A vehicle that brakes hard is a physical cause
of the crash behind it and has broken no rule.

| Comparison | Runs | Precision | Recall | F1 | Exact set match |
|---|---|---|---|---|---|
| Physical contributors | 105 | 69.9% | 62.0% | 65.7% | 39.1% |
| Normative contributors | 42 | 63.3% | 39.6% | 48.7% | not applicable |

Forty-two of the 105 runs carry a normative reference. A scenario that designs no
rule violation has nothing for the normative comparison to score and reports not
applicable rather than zero.

Naming who violated an obligation is much harder than naming who was involved,
and the normative recall of 0.396 is the weakest headline figure in the campaign.
Over all findings the evidence classes are 66 supported, 140 partial, 32
insufficient.

**On the design-template attribution table, read the reference before the
number.** That table scores against each scenario's causal template, which names
contributors only through edges whose cause is a scripted action. S10 to S15
express their design in states instead, so of the 26 variants designed to
collide, 13 declare a contributor there and 13 do not. Nine of the ten
`incorrect` verdicts in that table sit on a row with no reference, where naming
anybody scores zero by construction; the one remaining is `S08/crash`. The
generated report marks those rows.

A contribution score states what changed when the encounter was re-run under a
controlled modification. It is not a finding of legal fault and not a fault
percentage.

Details: [RESPONSIBILITY.md](RESPONSIBILITY.md).

## 7. Counterfactuals

Across the 105 replay reports, 39 findings carry a but-for verdict of yes and 199
were not tested. A replay costs a full simulator run per intervention, so the
sweep is deliberately narrow.

A prevention opportunity is not factual causation. The `counterfactual_role`
records which question each replay answered: removing what happened
(`factual_removal`), supplying what did not (`prevention_opportunity`), or
improving what did (`omission_repair`).

Details: [COUNTERFACTUALS.md](COUNTERFACTUALS.md).

## 8. Important case studies

### S07: the vehicle that never collides

S07 has three vehicles and one of them, C, never touches anything. Contact
alignment cannot reach it. In all six S07 runs the hybrid aligner placed A as
reference, B by contact and C by radar, and every run finished
`HYBRID_ALIGNED`. C's offset error across those six runs is 0.0021 s mean and
0.0032 s worst.

This is the clearest result on the page: a recorder with no physical anchor was
placed on the common timeline to within a fifteenth of a tick, from trajectory
consistency alone.

### S14/c_pushes_b: three cameras, one instant

C runs into B and pushes B into A. The three recorders' clocks sat 0.576 s and
0.637 s apart. Estimated from their shared contacts alone, the offsets place all
three on one timeline to 36 microseconds mean absolute error in that run, and the
reconstruction orders the two impacts correctly: B and C at 6.760 s, then A and B
at 7.960 s on the common clock. The image on the front page is that run.

### S06: when the middle vehicle registers one impact

In a chain, B is struck from behind and then strikes the vehicle ahead, and B's
contact sensor often reports one impact rather than two. That single anchor then
relates both neighbours, and the third vehicle's whole timeline goes out by
roughly the interval between the two impacts.

The method detects this. On the three `S06/a_front_pushed` seeds the contact
stage recorded that B's one anchor was matched to two counterparties and named C
as having a suspect offset, and it put **no error bound on it**: if B never
registered its second impact, nothing in the recordings bounds how far the
derived offset is out. On seed 2 the offset was out by 0.200 s, exactly the
interval between the impacts.

The consequence is reported, not absorbed. Across the campaign the method claimed
an impact order on 11 of the 14 multi-impact runs and was right on all 11. On the
other 3 it declined, because the offset rested on a shared anchor. Declining is
its own verdict and is not scored as a wrong answer, and equally is not scored as
a right one.

### S10/rolls_through: two references, two answers

A rolls through its STOP sign and collides with B. The design-template table
reads `incorrect`, because that scenario's template declares no action-caused
contributor and so anything named scores zero. The responsibility analysis
reports A as supported, which is the right answer: A did roll through the stop,
and the violation lies on the physical path to the collision.

The two are answering different questions and the page now says which.

## 9. Negative results

Not hidden, not softened.

**Scenario validation failed on 22 of 105 runs**, all in S10 to S16:

| Variant | Failed | What went wrong |
|---|---|---|
| S15/b_stops | 3 of 3 | expected a near miss, a collision occurred between B and C |
| S15/deflected_into_c | 3 of 3 | expected the A to C impact; A and B collided instead |
| S16/consequential | 3 of 3 | expected the B to C impact; A and B collided instead |
| S16/independent | 3 of 3 | expected the B to C impact; A and B collided instead |
| S12/near_simultaneous | 3 of 3 | expected a collision; none occurred |
| S11/stops_then_proceeds | 2 of 3 | expected a near miss, a collision occurred |
| S13/cut_in | 2 of 3 | expected a collision; none occurred |
| S10/stops_then_proceeds | 1 of 3 | expected a near miss, a collision occurred |
| S13/safe_lane_change | 1 of 3 | expected a near miss, a collision occurred |
| S14/c_pushes_b | 1 of 3 | the impacts occurred in the other order |

**S12/near_simultaneous never happened.** The scenario exists to ask whether a
method will invent a priority winner when two vehicles arrive too close to call.
In all three seeds the two vehicles never came closer than 8.2 m against a 6.0 m
requirement, so the encounter the question needs was never staged. The system
stayed restrained on all three, which is the right behaviour, but restraint on an
encounter that did not occur does not answer the question. The question remains
open.

**S14 pushed-vehicle discrimination failed.** The scenario asks whether a pushed
vehicle is treated as an initiating contributor merely because it physically
struck the vehicle ahead. The design names C; the analysis named A and B, and
supported B normatively. It got this backwards, on all three variants of S14.

**Normative recall is 0.396.** The method finds under two in five of the
obligations that were violated.

**STOP precision is 55.4 percent.** Thirty-seven of the 83 detections were not
signs.

**S06 hybrid alignment does not fix every seed.** The radar fallback resolves
some chains where contact alone collapses two impacts, and not others; the
ambiguous cases stay flagged rather than being forced.

**Attribution is substantially weaker than reconstruction.** Recovering who was
in the collision and when is close to solved here. Recovering who caused it is
not.

## 10. Limitations

The full list is in [LIMITATIONS.md](LIMITATIONS.md). The ones that most
constrain how this page should be read:

- **Simulation only.** CARLA sensors, CARLA physics, one town, three vehicles at
  most. Nothing here has been tested against a real recording.
- **Small sample.** Thirty-five variants, three seeds. A per-scenario figure
  rests on three runs and should be read as an illustration, not an estimate.
- **No verified stop-line ground truth**, so one perception quantity is reported
  and not scored.
- **Drift is not estimated.** Over runs of this length that is defensible and the
  size of the approximation is measured above. Over longer recordings it would
  not be.
- **The design-template reference does not reach S10 to S15**, so the attribution
  table covers about half the collision variants.
- **Not legal liability.** The vocabulary is causal initiator, causal
  contributor, shared causal contribution, causal chain and insufficient
  evidence. No number here is a share of fault.

---

## Related

- [`results/final_results.md`](../results/final_results.md), the generated tables
- [LIMITATIONS.md](LIMITATIONS.md), what this does not establish
- [SCENARIOS.md](SCENARIOS.md), what each scenario is for
- [REPRODUCIBILITY.md](REPRODUCIBILITY.md), running it again
- [`legacy/RESULTS_v1.md`](../legacy/RESULTS_v1.md), the historical V1 results
