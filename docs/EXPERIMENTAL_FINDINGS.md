# Experimental findings — the synchronized-clock baseline

> **This page describes the earlier campaign in `artifacts/`, in which every
> recorder read one shared simulator clock.** It is retained as a historical
> baseline and is not the project's final result. The final campaign — every
> recorder on its own clock, with the common timeline estimated from shared
> observations alone — is in [RESULTS.md](RESULTS.md), and the two are
> deliberately never averaged together: `cdf.common.campaign` marks a run
> recorded under a different clock protocol as foreign rather than folding it in.

Technical results only. This is not a paper and contains no related work. Every
number below was read from a persisted artifact; `scripts/extract_findings.py`
reproduces them from `artifacts/` without re-running anything.

Read `docs/LIMITATIONS.md` first. In particular: everything here is a statement
about CARLA 0.9.15 on one machine, with a simulated radar and scripted vehicles.

---

## 1. What was actually executed

A campaign of **39 recorded runs**: 13 scenario/variant combinations at three
seeds each. Each run was recorded on a **freshly started simulator process**
(see §2), then analysed, fused, scored against the oracle, model-checked and
bundled for the viewer.

| Scenario | Map | Variants run | Seeds | Outcome produced |
|---|---|---|---|---|
| S01 rear-end | Town05 | `crash`, `avoided` | 0,1,2 | collision / no contact |
| S02 cut-in | Town05 | `crash`, `avoided` | 0,1,2 | collision / no contact |
| S03 crossing | Town05 | `crash` | 0,1,2 | collision |
| S04 crossing + braking | Town05 | `yield` | 0,1,2 | no event |
| S05 simultaneous crossing | Town05 | `crash` | 0,1,2 | collision |
| S06 chain collision | Town05 | `a_front_pushed`, `b_rear_first` | 0,1,2 | two ordered collisions |
| S07 partial view | Town05 | `occluded`, `full_view` | 0,1,2 | collision |
| S08 multi-direction crossing | Town05 | `crash` | 0,1,2 | collision |
| S09 roundabout | **Town04** | `merge_conflict` | 0,1,2 | collision |

Scenario validation (the run produced the encounter its specification declares)
passed on **38 of 39** runs in the first campaign and on **39 of 39** after one
fix. The single failure was `S02/crash/seed 2`, whose collision margin was too
tight for the seed perturbation to preserve; S02 was strengthened (the cutting-in
vehicle now also slows once inside the lane, which is both the realistic form of
the manoeuvre and a decisive rather than marginal closing rate) and re-recorded
at all three seeds.

Seed 0 is the nominal specification. Seeds 1 and 2 apply a reproducible
perturbation — one common speed scale of up to ±5% and independent action-timing
jitter of up to ±0.12 s — because these scenarios are deterministic and repeating
one under a different seed alone would reproduce the same trace.

---

## 2. Reproducibility is conditional on restarting the simulator

The most consequential operational finding, and it was measured rather than
assumed.

Running **S05 three times in one server session**, identical specification and
seed:

| repeat | minimum separation | outcome |
|---|---|---|
| 1 | 6.996 m | near miss |
| 2 | 6.687 m | near miss |
| 3 | 6.228 m | near miss |

The result drifts monotonically; final positions differ by about a metre. Actors
are destroyed and world settings restored between runs regardless, so this is
accumulated simulator state unreachable through the API.

Running the **same** specification twice, each on a freshly started server,
reproduced it exactly: minimum separation `3.453 m`, collision at `t = 3.75 s`,
final pose `(108.3544, 1.0848)` both times, matching a value recorded earlier on
another fresh server.

Note the size of the discrepancy: the drifted result and the reproducible one
differ by enough to flip the outcome class. Server reuse is not a numerical
nuisance here, it can change what the experiment concludes. The protocol
therefore restarts the simulator before every recorded run and before every
counterfactual replay, at roughly 45 s per run.

**Making that restart actually happen took a second fix.** `CarlaUE4.exe` is a
launcher that spawns `CarlaUE4-Win64-Shipping.exe` and exits, so terminating the
launched process leaves the engine alive and still holding the RPC port. Every
later "fresh" server then failed to bind and the client silently reconnected to
the first one — producing exactly the shared state the restart existed to
prevent, while appearing to work. The first counterfactual campaign was run
under that defect and was discarded; the results in §9 come from a re-run on
genuinely fresh engines. The 39-run recording campaign was unaffected, because
its supervisor killed the simulator by image name rather than through the
process handle.

**And the re-run itself had to be run past a third problem.** On this build the
native CARLA client aborts the whole interpreter -- `Fatal Python error:
Aborted`, inside `world.apply_settings()` -- on the third simulator process of a
suite. It is reproducible, produces no Python traceback and no Windows error
report, and the cause is not established; `docs/ENVIRONMENT.md` finding 10
records what was tried and what it did not fix. The campaign gets through it by
structure rather than repair: `counterfactual.resume` reuses the replays already
on disk and `scripts/run_counterfactual_campaign.py` retries each suite, so
successive attempts need fewer restarts until one completes. The five suites
needed 4, 3, 4, 4 and 4 attempts. This is a workaround, and §9 says so where it
reports the replays.

One guard mattered more than it looks. Resume matches a replay by configuration
hash, which proves the *parameters* agree and says nothing about whether the
recording was sound -- so the discarded campaign's replays, whose hashes still
matched, would have been folded straight into the re-run. They were deleted
instead, and `--fresh` now makes that an explicit operation rather than a
remembered one.

---

## 3. Radar reconstruction quality

### 3.1 World-fixed clutter dominates raw output

Measured CARLA radar output is ~145 detections per frame at 6000 points/s, the
large majority reflections from the road surface. Tracking those directly
produced **45 track ids for participant A in a two-vehicle rear-end**, of which
one corresponded to the other vehicle.

Gating track birth on the standard automotive stationary-target test — comparing
each return's measured range rate against the `-(v_forward·cos az +
v_lateral·sin az)` a world-fixed point would produce — reduced this to **one
track over the whole approach**, holding the other vehicle from 25.3 m down to
3.6 m at impact with a **mean position error of 1.322 m** against its true pose
over 117 samples.

The recorded run ends with four track ids, not one: the other three are born
*after* the impact and correspond to no participant (§3.2). Over the approach —
the part of the recording a reconstruction depends on — there is exactly one.

Three corrections were needed before it worked, each found by running against
real output rather than by reasoning:

1. pairing the measured range rate with the bearing it was measured along (the
   sensor-frame azimuth) rather than the body-frame centroid bearing — the
   parallax error over a 2.2 m mounting offset is large enough at short range to
   make roadside structure read as traffic;
2. projecting the full body-frame velocity vector instead of assuming motion
   along the body x axis, which breaks during a post-impact spin;
3. compensating the sensor lever-arm velocity (`ω × r`), which reaches several
   m/s while spinning. This alone cut one participant's spurious tracks from 17
   to 6.

### 3.2 Pre-impact evidence is clean; post-impact evidence is not

Across the scenarios examined, **every spurious track was born after the
impact**. Before it, each observing participant held exactly one track of the
vehicle it was observing, at 1.2–1.4 m mean position error:

| run | observer | track | mean error vs the observed vehicle |
|---|---|---|---|
| S01 crash | A | `A::T001` | 1.32 m |
| S03 crash | A | `A::T001` | 1.36 m |
| S05 crash | B | `B::T001` | 1.22 m |

Post-impact tracking degrades because the sensor's own motion is large and
rapidly changing. Tracks sustained only by world-fixed returns are now dropped
after a bounded number of frames, which reduced the sample counts substantially
(S03 participant A: 365 → 168 track samples) without removing the genuine track.

This also independently confirms the azimuth convention: a mirrored azimuth
would put the reconstructed position on the wrong side of the observer and the
errors would be tens of metres, not ~1.3 m.

---

## 4. Track-to-participant association without actor identities

The central mechanism — deciding which participant an anonymous radar track was
observing, from trajectory evidence alone.

On the recorded S01 run, participant A's single track resolved to participant B
with **confidence 0.850** and a **trajectory RMSE of 1.356 m over 5.90 s (119
samples)**, using no CARLA actor id at any point.

On the three-vehicle S07 run the subject map resolved to
`{"A::T001": "B", "B::T001": "C"}` — the follower's track onto the middle
vehicle, the middle vehicle's track onto the leader — again from trajectory
evidence alone.

Association scoring is performed before any oracle data is consulted; the oracle
identity is used only afterwards, to score the result.

---

## 5. Partial observability and the benefit of fusion (H1, H2)

### 5.1 The occlusion is real, not manufactured

S07 places three vehicles in one lane. Measured from the recorded run:

| participant | tracks held | what they correspond to |
|---|---|---|
| A (rear) | 2 | both of B — 1.56 m and 3.11 m mean error; **23.9 m and 25.2 m from C** |
| B (middle) | 1 | C — 1.88 m mean error |
| C (lead) | 0 | nothing ahead of it |

A therefore never observes C at all, while B observes it clearly. The missing
information comes from sensing, not from deleting graph elements afterwards.

The `full_view` control, which gives A the baseline radar instead of the
narrow-FOV profile, does **not** recover C: A's additional tracks there sit 8.8 –
12.9 m from both B and C and are post-impact artifacts. **Physical occlusion by
the intermediate vehicle, not the field of view, is what hides C.** That is an
honest correction to the scenario's original rationale, which expected the FOV
restriction to matter.

### 5.2 What fusion recovers

Measured on the recorded S07 `occluded` run, scored against the oracle:

| quantity | best single local (A) | fused |
|---|---|---|
| node recall | 0.231 | **0.500** |
| node F1 | 0.222 | **0.342** |
| edge recall | 0.222 | 0.222 |
| edge F1 | 0.125 | 0.078 |

Fusion **more than doubles node recall**, recovering 7 oracle-relevant events the
blind participant did not have, among them `HARD_DECELERATION` — the braking of
the vehicle A never tracked.

Structurally, the fused collision node's ancestry spans owners `A`, `B` **and
`C`**, including C's `HARD_BRAKE` and `BRAKE_ONSET`, and the fusion diagnostics
report **76 bridged reachability pairs** — causal reachability that exists in no
single participant's graph. The merges are the asymmetric ones the design calls
for, for example A's `TARGET_DECELERATION` of track `A::T001` merged with B's own
`DECELERATION` into a single node owned by both.

### 5.3 Where fusion does not help, and why

Edge recall is unchanged and edge F1 *decreases*. This is a real negative result
and it has a specific cause: causal edges are built locally, before fusion, so a
cause observed by one participant and an effect observed by another are merged as
nodes but never linked by a new edge. Fusion also contributes edges the oracle
models no part of, which costs precision.

So the supported claim is narrower than "fusion reconstructs the causal
structure". What is demonstrated is that **fusion recovers events and causal
reachability that no single ego view contains**, including the initiating cause
under genuine occlusion. Improving oracle-referenced *edge* agreement would
require a post-fusion causal rule pass over the merged node set, which this
implementation does not perform.

### 5.3b The same pattern holds across the whole campaign

Averaged per scenario over all 39 runs, scored against the oracle:

| scenario | runs | best local node F1 | fused node F1 | Δ node F1 | Δ edge F1 | nodes gained | association correct |
|---|---|---|---|---|---|---|---|
| S01 | 6 | 0.297 | 0.369 | **+0.072** | −0.012 | 2.7 | 6/6 |
| S02 | 6 | 0.204 | 0.237 | **+0.033** | −0.011 | 2.8 | 6/11 |
| S03 | 3 | 0.201 | 0.292 | **+0.091** | −0.093 | 6.0 | 5/6 |
| S04 | 3 | 0.087 | 0.073 | −0.014 | ±0.000 | 0.0 | 3/10 |
| S05 | 3 | 0.315 | 0.254 | −0.061 | −0.056 | 2.7 | 6/9 |
| S06 | 6 | 0.251 | 0.365 | **+0.114** | −0.059 | 9.5 | 12/13 |
| S07 | 6 | 0.211 | 0.333 | **+0.123** | −0.060 | 7.0 | 12/15 |
| S08 | 3 | 0.228 | 0.309 | **+0.081** | −0.094 | 10.0 | 15/21 |
| S09 | 3 | 0.255 | 0.290 | **+0.035** | −0.098 | 4.3 | 5/9 |

Campaign means: **Δ node F1 = +0.063**, **Δ edge F1 = −0.048**. Fusion improved
node F1 in **30 of 39 runs** and improved edge F1 in **0 of 39**. The split is
systematic, not noise, and it is the split §5.3 explains.

The largest node gains are in the three-vehicle scenarios — S07 (+0.123), S06
(+0.114) and S08 (+0.081) — which is the direction H2 predicts: the more
viewpoints there are and the less any one of them sees, the more there is for
fusion to contribute.

The two negative rows are informative rather than anomalous. **S04** is the
negative control: nothing happens, there is nothing to recover, and fusion adds
zero nodes while diluting an already-thin graph. **S05** is the symmetric
crossing in which both participants see each other well, so neither has much to
learn from the other, and merging costs more in precision than it returns in
recall.

### 5.5 Track association across the campaign

The association layer reported on **191 tracks** across the 39 runs. They divide
in two, and the division matters for reading the numbers:

| | tracks | |
|---|---|---|
| **scorable** — the track really does correspond to a participant | 100 | 70 correct, 2 incorrect, **28 left unresolved** |
| **unscorable** — the track corresponds to no participant at all | 91 | correctly left `UNRESOLVED`; excluded from scoring |

Over the scorable 100: **precision 0.972, recall 0.700, F1 0.814**, mean
trajectory RMSE **1.564 m**.

Two separate readings, and it is worth not conflating them.

*Of the tracks it committed to, 97.4% were right* — two wrong names in 78
commitments. That is the number that matters for a forensic claim, because a
confidently wrong identity is the failure that would put the wrong vehicle in a
reconstruction.

*It declines to name 26% of the tracks it could have named.* The 28 unresolved
are **not** the post-impact phantoms of §3.2 — those are the 97 unscorable ones,
which have no true counterpart and are excluded from scoring precisely so that
declining to name them is neither rewarded nor punished. The 28 are genuine
misses: a track that did correspond to a participant, which the layer looked at
and would not commit to. Most are short, low-overlap fragments where the
trajectory evidence is too thin to separate candidates.

That trade is deliberate (`evaluation.association.count_unresolved_as_miss` is
`true`, so those 28 count against recall rather than being hidden), and for this
application it is the right way round: `INSUFFICIENT EVIDENCE` is a usable
forensic answer and a wrong name is not. But the honest summary is that the
association layer is *cautious*, not that it is nearly perfect — the 97.4% figure
alone would overstate it.

### 5.6 Which safeguards actually fired

Fusion carries three safeguards against merging away a disagreement. In the
remaining 39-run campaign, contradiction retention and cycle rejection did not
fire on recorded data; `UNRESOLVED` association remained the deliberate
insufficient-evidence outcome for 28 tracks. The cycle path is exercised by
unit tests that construct the cycle deliberately, while the association layer
continues to prefer an honest unresolved result over a wrong identity.

### 5.4 A caution about edge precision generally

Absolute edge F1 values are low throughout (0.06 – 0.16). The dominant reason is
a vocabulary mismatch rather than wrong claims: the local rule engine emits
mechanical relations (a brake command producing a deceleration, an impact
producing a stop) and interaction relations that the scenario's causal template
does not model. Adding ground-truth mechanical edges to the oracle — derived from
the exact action timeline and exact kinematics, not from the local rule table —
raised S01 fused edge F1 from 0.062 to 0.114 and is the fairer comparison, but a
gap remains by construction. **Edge recall against the oracle is the more
meaningful of the two numbers here**, and it is reported alongside.

---

## 6. The chain collision: same layout, opposite causal order (H4)

S06 produces two variants from an almost identical spatial layout:

| variant | true collision order |
|---|---|
| `a_front_pushed` | (A,B) at 5.95 s, then (B,C) at 6.15 s |
| `b_rear_first` | (B,C) at 4.65 s, then (A,B) at 6.05 s |

The oracle causal graphs differ structurally in the expected way — the direction
of the relation between the two impacts is reversed:

* `a_front_pushed`: `A/COLLISION → B/COLLISION [CAUSES_OUTCOME]` — the first
  impact pushes B into C;
* `b_rear_first`: `B/B_no_reaction → B/COLLISION [CONTRIBUTES_TO]` and
  `B/COLLISION → A/critical_ttc [CONTRIBUTES_TO]` — B's inadequate braking causes
  the first impact, which then collapses A's remaining gap.

Producing S06a required the middle vehicle to release its brakes before the rear
impact: with them locked the "pushed into C" mechanism cannot occur at all and
the variant silently degenerates into S06b's layout. That is recorded because it
is the kind of detail that makes a scenario quietly stop testing what it claims
to test.

---

## 8. Finite-trace model checking

Across all 39 runs, 372 property evaluations:

| verdict | count |
|---|---|
| PASS | 72 |
| FAIL | 147 |
| UNKNOWN | 153 |

| property | PASS | FAIL | UNKNOWN |
|---|---|---|---|
| `P1_brake_response` | 22 | 36 | 35 |
| `P2_no_throttle_while_closing` | 17 | 31 | 45 |
| `P3_post_collision_stop` | 24 | 42 | 27 |
| `P4_conflict_without_response` | 9 | 38 | 46 |

(`python scripts/extract_findings.py --section campaign` prints this table from
the artifacts.)

The high FAIL count is expected: these are scenarios deliberately constructed so
that at least one vehicle does not respond adequately. The result worth noting is
the **UNKNOWN count**, which is 41.1% of all evaluations. UNKNOWN is returned with
an explicit reason, for example on S01:

* `P1` for participant B: *"no radar track and no CRITICAL_TTC event evidence:
  this participant never observed a time-to-collision, so the antecedent cannot
  be evaluated"* — B is the lead vehicle and its forward radar sees nothing;
* `P4` for participant A: *"antecedent never held: this participant detected no
  predicted path conflict and no conflict-region entry"* — correct for a purely
  longitudinal encounter.

A monitor that returned PASS in those cases would be reporting compliance it had
no evidence for.

---

## 9. Counterfactual attribution

Twenty controlled replays across five runs. Each replay re-runs the identical
scenario -- same map, spawn state, seed and parameters -- on a freshly restarted
simulator, with exactly one scripted action disabled or weakened.

Reproduce the tables below with

```bash
python scripts/extract_findings.py --section counterfactuals
```

**How these were executed.** The counterfactual driver aborts the interpreter
part-way through a suite on this build (§2 and `docs/ENVIRONMENT.md`, finding
10), so each suite was run repeatedly with `counterfactual.resume` reusing the
replays already on disk. The five suites needed 4, 3, 4, 4 and 4 attempts
respectively. Every replay still ran on its own freshly started engine -- the
property the comparison depends on -- but not in one uninterrupted session.

### 9.1 S01 rear-end: a single initiator, correctly identified

| intervention | outcome | minimum separation |
|---|---|---|
| `B_emergency_brake__disable` | **no collision** | 24.17 m |
| `B_emergency_brake__scale_intensity_0_4` | **no collision** | 7.22 m |
| `A_late_brake__disable` | collision at 6.35 s | 4.49 m |
| `A_late_brake__scale_intensity_0_4` | collision at 6.50 s | 4.47 m |

Factual: collision (A,B) at 6.55 s, minimum separation 4.47 m.

Attribution: `single_initiator`, primary `B_emergency_brake`, scores
`{B_emergency_brake: 1.0, A_late_brake: 0.0}`. Scored against the oracle:
**precision 1.00, recall 1.00, F1 1.00**, primary-initiator accuracy correct,
single-vs-shared classification correct.

Both halves are informative: removing the lead vehicle's braking prevents the
crash, and removing the follower's braking changes nothing -- it was applied too
late to matter, which is precisely what the scenario was built to represent.

### 9.2 S06 chain collision: the same action is necessary in one variant and not the other (H4)

This is the sharpest result in the campaign. The two variants have near-identical
spatial layouts and near-identical end states; the factual collision orders are
(A,B) 5.95 s then (B,C) 6.15 s in `a_front_pushed`, and (B,C) 4.65 s then (A,B)
6.05 s in `b_rear_first`.

| intervention | S06a `a_front_pushed` | S06b `b_rear_first` |
|---|---|---|
| `C_emergency_brake__disable` | (A,B) still at 5.95 s; **(B,C) disappears** | **no collision at all**, 16.53 m |
| `C_emergency_brake__scale_intensity_0_4` | (A,B) 5.95 s, (B,C) 6.90 s | (B,C) 5.05 s, (A,B) 6.45 s |
| `B_reaction_brake__disable` / `B_no_reaction__disable` | **order flips to (B,C) 4.65 s then (A,B) 6.10 s** | unchanged |
| `A_*_brake__disable` | (A,B) 5.95 s unchanged, (B,C) one tick earlier at 6.10 s | unchanged |

Two things fall out of this, neither of which could be read off the final
positions:

* **The leading vehicle's braking is a but-for cause in S06b and is not in
  S06a.** Removing it in S06b prevents every impact; removing it in S06a leaves
  the first impact exactly where it was and only removes the second.
* **Disabling the middle vehicle's reaction turns S06a into S06b** -- the end
  state is similar, the causal order is reversed.

H4 is supported: counterfactual intervention recovers different causal structure
from near-identical spatial configurations.

### 9.3 Where but-for analysis reaches its limit

Three of the five runs are negative results, and they have two causes:
**scripted controllers do not react**, so removing an upstream cause does not
propagate to a downstream "reaction", and **an omission cannot be removed**,
because there is no action to disable.

**S06a and S07: no intervention prevents the outcome.** In both, the striking
vehicle hits the middle vehicle because the middle vehicle brakes -- and the
middle vehicle's braking is a *scripted* action at a fixed time, not a response
to what it observed. Removing the leading vehicle's brake therefore leaves the
middle vehicle braking anyway and the first impact unchanged. Attribution
returns `insufficient_evidence` for both rather than naming a cause it could not
demonstrate.

In S07 one intervention is informative in the other direction: disabling the
middle vehicle's reaction *adds* an impact -- (B,C) at 5.25 s that does not occur
in the factual run -- and delays the original one to 6.50 s. The action is
protective of one pair and causal for another, which a single "contributed /
did not contribute" label cannot express.

This also means the scenario's declared causal template asserts a dependency
(`C_emergency_brake -> B/closing`) that the controlled replay does **not**
confirm for S06a. The designed intent and the counterfactually supported
structure differ, and the honest reading is that the template records what the
scenario was built to represent, not what the replay demonstrates.

**S05 simultaneous crossing: the shared contribution is not recovered.**

| intervention | outcome | minimum separation |
|---|---|---|
| `A_no_yield__scale_target_speed_0_8` | **no collision** | 6.91 m |
| `A_no_yield__disable` | collision at 3.85 s | 3.89 m |
| `B_no_yield__disable` | collision at 3.75 s | 3.35 m |
| `B_no_yield__scale_target_speed_0_8` | collision at 3.80 s | 3.01 m |

The oracle expects shared contribution (both participants); the replay finds one
contributing action, so attribution reports `single` where the reference says
`shared` (F1 0.67, recall 0.50).

The reason is structural, not a scoring defect. S05's `no_yield` actions raise
each vehicle's speed only from 11.0 to 11.5 m/s on an approach that already
collides; disabling them barely shifts the arrival times. The thing both drivers
actually do wrong is *fail to yield*, and failing to yield is an omission. The
intervention API can disable, delay or weaken an action that exists -- it cannot
remove an absence. Testing shared contribution properly would require the
scenario to carry a *yield* action that the counterfactual adds, which inverts
the direction of the intervention API and is not implemented here.

### 9.4 Attribution scored against the oracle, all five runs

| run | predicted | oracle reference | precision | recall | F1 |
|---|---|---|---|---|---|
| S01 `crash` | `single` — `B_emergency_brake` | `single` — `B_emergency_brake` | 1.00 | 1.00 | **1.00** |
| S05 `crash` | `single` — `A_no_yield` | `shared` — `A_no_yield`, `B_no_yield` | 1.00 | 0.50 | 0.67 |
| S06b `b_rear_first` | `single` — `C_emergency_brake` | `shared` — `B_no_reaction`, `C_emergency_brake` | 1.00 | 0.50 | 0.67 |
| S06a `a_front_pushed` | `insufficient_evidence` | `single` — `C_emergency_brake` | 0.00 | 0.00 | 0.00 |
| S07 `occluded` | `insufficient_evidence` | `shared` — `B_reaction_brake`, `C_emergency_brake` | 0.00 | 0.00 | 0.00 |

**Precision is 1.00 in every run that named anything at all: there is not one
false positive in the campaign.** Every failure is a false *negative* -- an
action the scenario declares causal that the replay could not demonstrate. For a
forensic tool that is the right direction to fail in, and it is a direct
consequence of the design: an action is only reported as contributing when
removing or weakening it measurably changed the outcome.

### 9.5 What the counterfactual layer demonstrated

* Controlled replay works end to end against the simulator: 20 replays, each on
  a fresh server, each differing from the factual run in exactly one action.
* Where a scripted action is genuinely load-bearing, the layer identifies it
  exactly (S01: precision and recall 1.00).
* Where it is not, the layer says so rather than naming a cause
  (`insufficient_evidence` in two of five runs), which is the required behaviour.
* No false positive in 20 replays.
* The comparison between S06a and S06b recovers genuinely different causal
  structure from near-identical end states.
* Its limits are a property of the scenario design -- scripted rather than
  reactive controllers, and omissions that cannot be intervened upon -- not of
  the replay machinery.

### 9.6 What re-running the campaign on genuinely fresh engines changed

The first counterfactual campaign was executed while the simulator was being
restarted ineffectively (§2): every "fresh" server silently reconnected to a
leaked engine. That campaign was discarded and all five suites were re-run. The
comparison is worth reporting, because it is the only evidence of how much the
defect actually mattered:

| | first campaign | re-run on fresh engines |
|---|---|---|
| collision / no-collision outcome, every replay | — | **identical** |
| collision times, every replay | — | **identical** |
| collision pairs and their order | — | **identical** |
| attribution class, primary initiator, scores | — | **identical** |
| minimum separation, replays that collided | — | **identical** |
| minimum separation, replays that avoided collision | 23.51 / 6.59 / 16.53 m | 24.17 / 6.91 / 16.53 m |

Only the minimum separations of *avoided* collisions moved, by up to 0.66 m, and
only in two of the four such replays. That is the expected shape: once the
vehicles no longer touch, they keep travelling and small differences accumulate,
whereas a collision time is pinned by the geometry.

So the defect changed no conclusion in this campaign. That is a measurement, not
a reprieve: §2 records a case where the same class of drift flipped an outcome
between near-miss and collision, and nothing about the first campaign made it
knowable in advance which of those two situations it was in. The result is
reported here because the campaign was re-run, not because the first one was
trustworthy.

---

## 10. Robustness: the same encounter through worse sensors

S01 `crash` seed 0, recorded four times. The map, the spawn state, the seed, the
scripted actions and the controller parameters are identical in all four; only
the radar profile differs, and the degradation is injected in the local radar
front-end from a seeded stream rather than requested from the simulator, so the
*physics of the encounter is the same run* and only what the vehicle could see
changes.

```bash
python scripts/run_ablation.py --scenario S01 --variant crash --seed 0 \
    --profiles radar_baseline radar_noisy radar_dropout radar_degraded
python scripts/extract_findings.py --section ablation
```

| profile | FOV / range | injected degradation | outcome | tracks | association | fused node F1 | fused edge F1 |
|---|---|---|---|---|---|---|---|
| `radar_baseline` | 120° / 90 m | none | collision | 4 | 1 correct | 0.375 | 0.114 |
| `radar_noisy` | 120° / 90 m | 10% point loss, σ 0.45 m / 0.020 rad / 0.40 m·s⁻¹ | collision | 3 | 1 correct | 0.360 | 0.118 |
| `radar_dropout` | 120° / 90 m | 35% frame loss, 30% point loss | collision | 5 | 1 correct, **2 unresolved** | **0.286** | 0.105 |
| `radar_degraded` | **45° / 70 m** | 25% frame loss, 25% point loss, σ 0.60 m / 0.030 rad | collision | **1** | 1 correct | **0.409** | 0.114 |

Three things are worth stating, and the third is the interesting one.

**The encounter survives every profile.** All four runs produce the collision,
all four pass scenario validation, and in all four the association layer names
the other vehicle correctly and names no wrong one. Trajectory RMSE stays between
1.20 and 1.36 m throughout. Whatever the reconstruction loses under degradation,
it is not the basic ability to say what happened and to whom.

**Frame dropout is the profile that actually hurts.** `radar_dropout` is the
worst row on every graph measure — node F1 0.286 against 0.375 at baseline, node
recall 0.571 against 0.643 — and the only profile that leaves associations
`UNRESOLVED` (two of them). Losing 35% of *frames* fragments tracks into short
pieces, and a short piece carries too little trajectory to identify; losing
individual returns within a frame, as `radar_noisy` does, is much better
tolerated because the cluster survives.

**The heaviest degradation scores the best, and that is a warning about the
metric, not a result about the sensor.** `radar_degraded` — narrowest field of
view, shortest range, dropout *and* noise — produces the highest fused node F1 of
the four (0.409). The reason is visible in the track counts: it holds **one**
track where the baseline holds four. The three extra baseline tracks are the
post-impact phantoms of §3.2, and the events they generate are events the oracle
graph does not contain, so removing them raises precision. A profile that sees
less produces a graph that scores better against the oracle.

This does not mean degraded sensing is preferable. It means **node F1 against the
oracle is not a monotone measure of sensing quality** — it rewards silence about
things the oracle does not model. The measures that do behave monotonically here
are the ones about evidence rather than graph agreement: node recall and the
association status, both of which are worst exactly where the evidence is worst
(`radar_dropout`). Where this document compares reconstructions it uses the
oracle-referenced F1 because that is the available reference; §5.4 already
cautions about its edge component, and this sweep shows the node component has
its own failure mode.

### 10.1 The baseline run is also a reproducibility control

`radar_baseline` is the campaign's own S01 `crash` seed 0 configuration,
re-recorded at a **later commit** on a freshly started engine. It reproduced the
campaign run exactly:

| | campaign run (commit `31f29a13`) | re-record (commit `ea5be3ee`) |
|---|---|---|
| outcome | collision | collision |
| collision pair and time | (A,B) at 6.55 s | (A,B) at 6.55 s |
| minimum separation | 4.471420 m | 4.471420 m |
| association trajectory RMSE | 1.3561327263302574 m | 1.3561327263302574 m |

Identical to the last digit the artifacts record. This is the direct evidence
behind the claim in `docs/EXPERIMENT_PROTOCOL.md` that the campaign is
reproducible run-by-run from its recorded parameters, and that recording it
across eleven commits did not perturb the recordings: the parameters that govern
a recording did not change, and re-running one at HEAD proves it rather than
asserting it.

---

## 11. Summary against the hypotheses

| | statement | result |
|---|---|---|
| **H1** | fusing local graphs improves reconstruction over a single local graph | **partially supported** — node F1 improves in 30 of 39 runs, campaign mean +0.063; edge F1 improves in 0 of 39, mean −0.048. The split is systematic and explained in §5.3 |
| **H2** | the benefit is especially visible under partial observability | **supported for node recovery** — the largest node gains are the three-vehicle scenarios, S07 highest at +0.123; under real occlusion fusion recovers the initiating event the blind participant never observed, plus 76 causal reachability pairs no single view contains |
| **H3** | the fused graph approaches the oracle without equalling it | **supported** — fused node F1 0.342 against the oracle on S07; the gap is large and its causes are identified in §5.4 |
| **H4** | counterfactuals recover different causal structures for S06a and S06b | **supported** — the leading vehicle's braking is a but-for cause in S06b (removing it prevents every impact) and is not in S06a (the first impact is unchanged); disabling the middle vehicle's reaction turns S06a into S06b (§9.2) |
| **H5** | S04 is a useful negative control | **supported** — identical crossing geometry to S03, opposite outcome: 24.8–25.6 m minimum separation across three seeds, no collision, while S03 collides at 3.06–3.14 m |

Negative and partial results above are reported as measured. None of the
scenarios or thresholds was adjusted to improve a metric after seeing it; the
changes recorded in the git history were made to fix defects (a mirrored
stationarity test, a matching inconsistency, an unfair oracle reference) and are
described in their commit messages.
