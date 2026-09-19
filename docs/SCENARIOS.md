# Scenarios

Scenarios are pure data: `configs/scenarios/*.yaml`, turned into actors, routes
and scripted controllers by `cdf.simulation.scenario_base`. Keeping them
declarative buys three things the experiment protocol depends on:
reproducibility (the whole spec is hashed into the run manifest), interventions
(every behaviour is a named `ScriptedAction`, so a counterfactual is "the same
spec with one action, or a set of them, disabled, delayed or weakened") and validation (the spec
states what is *supposed* to happen, so a scenario that silently stops producing
its intended encounter fails loudly).

## Maps

**S09 (roundabout) is on Town03_Opt. Every other scenario is on Town05.**

The tested simulator build cannot load base Town03 reliably, so S09 uses the
stable `Town03_Opt` variant with the same roundabout geometry.

Two Town05 sites carry almost everything:

* the **three-lane straight** around `y = -204` (recommended spawn point index
**265**), measured to offer ~160 m of junction-free travel, used by S01, S02, S06
and S07; * **junction 720** at `(101.6, 0.3)`, measured to expose four clean
approaches (maximum bearing error 0.7°) and carrying **no traffic light**, so
signal state cannot confound a crossing scenario, used by S03, S04, S05 and S08;

On Town03_Opt, the central roundabout around `(0.0, 0.0)` is used by S09: four
clean approaches whose routes curve by roughly 90° through the circulating
area. That curvature is the point: constant-velocity path prediction is weakest
exactly where heading changes fastest.

Crossing scenarios name a junction centre and two compass bearings rather than a
table of hand-measured spawn coordinates (`SpawnSpec.anchor: junction_approach` →
`junction_approach_waypoint()`), which is what makes them portable.

---

## Overview

Sixteen scenarios, 35 variants. **S01 to S09 are hash-frozen**: their
configuration may not change, so a better metric on them has to come from the
method. **S10 to S16 are the V2 additions**, and each isolates something the
earlier nine could not ask.

| Id | Name | Vehicles | Main question | Variants |
|---|---|---|---|---|
| S01 | `rear_end` | 2 | does a late reaction to the vehicle ahead braking get recovered? | `crash`, `avoided` |
| S02 | `cut_in` | 2 | is a lateral move into the lane recovered as the thing that closed the gap? | `crash`, `avoided` |
| S03 | `crossing` | 2 | who entered the junction without yielding? | `crash` |
| S04 | `crossing_braking` | 2 | the same conflict without an outcome: does the system stay silent? | `yield` |
| S05 | `simultaneous_crossing` | 2 | two vehicles, neither yielding, arriving together: is the contribution shared? | `crash` |
| S06 | `chain_collision` | 3 | in a chain, which pair collided first? | `a_front_pushed`, `b_rear_first` |
| S07 | `partial_view` | 3 | can a vehicle nobody could see be placed on the timeline at all? | `occluded`, `full_view` |
| S08 | `multidirection_crossing` | 3 | can a cause that consists of *not* yielding be rooted? | `crash` |
| S09 | `roundabout` | 2 | give-way on entry, where the geometry is curved | `merge_conflict` |
| S10 | `single_stop_a` | 2 | A has the STOP sign: is the obligation read off A's own camera and held against A? | `rolls_through`, `stops_safely`, `stops_then_proceeds` |
| S11 | `single_stop_b` | 2 | B has the STOP sign: the mirror of S10, so a bias towards one role would show | `rolls_through`, `stops_safely`, `stops_then_proceeds` |
| S12 | `all_way_stop` | 2 | both have STOP signs: who had priority, and is ambiguity preserved when it cannot be told? | `a_arrives_first`, `b_arrives_first`, `near_simultaneous`, `b_fails_to_stop` |
| S13 | `disputed_lane_change` | 2 | which vehicle closed the gap, when the deciding evidence is split between them? | `cut_in`, `accelerates_into_gap`, `safe_lane_change` |
| S14 | `three_car_chain` | 3 | is the pushed vehicle spared, or blamed for striking the car it was shoved into? | `c_pushes_b`, `b_hits_a_first`, `independent_impacts` |
| S15 | `intersection_pileup` | 3 | a deflection into a bystander: are the deflected car and the bystander left out of the account? | `deflected_into_c`, `single_impact`, `b_stops` |
| S16 | `secondary_collision` | 3 | is the second impact a consequence of the first, or that vehicle's own doing? | `consequential`, `independent`, `avoided` |

All sixteen run on Town05 except S09, which needs Town04's roundabout.

### What the campaign found, including where it did not work

Three of the new scenarios did not stage the encounter they were written to ask
about, and the results pages say so rather than quietly dropping them.

**S12 `near_simultaneous` never collided**, on any of its three seeds. Its
closest approaches were 10.90 m, 8.39 m and 8.23 m against a 6 m requirement.
The junction is the only one in Town05 that renders stop signs on more than one
approach, and its geometry gives the two vehicles very different distances from
their stop lines to the merge point. The priority-ambiguity question is
therefore **not answered by this campaign**.

**S14 `c_pushes_b` came out backwards.** The design names C, the striker. The
analysis named A and B physically and supported B normatively, because B has a
`CONTINUED_ACCELERATION_DURING_CONFLICT` before the first impact and C's own
rule violation is stamped *after* the impact it caused. Both findings are
defensible on the recorded evidence and neither is the answer the variant was
written to test.

**S15 `deflected_into_c` and both S16 impact variants land on the wrong pair**,
on all three seeds each: the collision occurs between A and B rather than the
pair the variant names.

Scenario validation failed on 22 of 105 runs in total, all within S10 to S16.
The full breakdown is in [RESULTS.md](RESULTS.md) §9, and
[LIMITATIONS.md](LIMITATIONS.md) §23, §25 and §27 state what each failure does
and does not invalidate.

---

## Scenario definitions

<!-- BEGIN GENERATED SCENARIO TABLE -->

_Generated from `configs/scenarios/*.yaml` by `scripts/generate_scenario_docs.py`. Do not edit by hand._

### S01: rear end

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s01_rear_end.yaml`

B travels ahead of A in the same lane and brakes hard. A reacts late and strikes B. The avoided variant keeps the geometry but gives A a timely response, which turns the outcome into a near miss.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 28 m | 14 / 14 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake`: brake at t=5.6s for 6s (intensity 0.85)
* **B** &mdash; `B_emergency_brake`: brake at t=4s for 8s (intensity 1)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_emergency_brake`, `A_late_brake`.

*Ground-truth causal template (oracle only):*

* `B.B_emergency_brake` --CONTRIBUTES_TO--> `A.closing`  
  _the lead vehicle's deceleration is what collapses the gap_
* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `A.A_late_brake` --PREVENTS--> `collision(A-B)`  
  _A's braking acts against the outcome but begins too late to avert it_

> A reacts 1.6 s after B begins braking, which is too late

**Variant `avoided`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 28 m | 14 / 14 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake`: brake at t=5.1s for 8s (intensity 1)
* **B** &mdash; `B_emergency_brake`: brake at t=4s for 8s (intensity 1)

*Validation:* expected outcome **near_miss**; A-B must close to under 14 m.

*Counterfactual candidates:* `B_emergency_brake`, `A_late_brake`.

*Ground-truth causal template (oracle only):*

* `B.B_emergency_brake` --CONTRIBUTES_TO--> `A.closing`  
  _the lead vehicle's deceleration is what collapses the gap_
* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `A.A_late_brake` --PREVENTS--> `collision(A-B)`  
  _A's braking acts against the outcome but begins too late to avert it_

> identical geometry and identical lead behaviour to the crash variant
> only A's reaction time changes, so the difference in outcome is attributable to that alone

---

### S02: cut in

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s02_cut_in.yaml`

B starts in the lane to A's left, slightly ahead, then moves laterally into A's lane while travelling slower than A. A closes rapidly and reacts late.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 30 m, lane -1 | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake`: brake at t=3.9s for 6s (intensity 0.85)
* **B** &mdash; `B_cut_in`: lane_shift at t=1s for 2.2s (lateral_m 3.5)
* **B** &mdash; `B_slow_after_cut_in`: set_speed at t=3.2s for 12s (target_speed 6.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_cut_in`, `B_slow_after_cut_in`, `A_late_brake`.

*Ground-truth causal template (oracle only):*

* `B.B_cut_in` --TRIGGERS--> `A.closing`  
  _entering A's path while travelling slower creates the closing conflict_
* `B.B_slow_after_cut_in` --CONTRIBUTES_TO--> `A.closing`  
  _slowing once inside A's lane sharpens the closing rate it created_
* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `A.A_late_brake` --PREVENTS--> `collision(A-B)`  
  _A brakes, but only after the cut-in has already closed the gap_

> B cuts in ~24 m ahead of a faster A, then slows inside A's lane
> A reacts, but not early enough to shed the closing speed in time

**Variant `avoided`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 30 m, lane -1 | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake`: brake at t=2.9s for 9s (intensity 1)
* **B** &mdash; `B_cut_in`: lane_shift at t=1s for 2.2s (lateral_m 3.5)
* **B** &mdash; `B_slow_after_cut_in`: set_speed at t=3.2s for 12s (target_speed 6.5)

*Validation:* expected outcome **near_miss**; A-B must close to under 16 m.

*Counterfactual candidates:* `B_cut_in`, `B_slow_after_cut_in`, `A_late_brake`.

*Ground-truth causal template (oracle only):*

* `B.B_cut_in` --TRIGGERS--> `A.closing`  
  _entering A's path while travelling slower creates the closing conflict_
* `B.B_slow_after_cut_in` --CONTRIBUTES_TO--> `A.closing`  
  _slowing once inside A's lane sharpens the closing rate it created_
* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `A.A_late_brake` --PREVENTS--> `collision(A-B)`  
  _A brakes, but only after the cut-in has already closed the gap_

> identical geometry, cut-in and slowdown as the crash variant
> only A's reaction time changes, isolating it as the difference that decides the outcome

---

### S03: crossing

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s03_crossing.yaml`

A travels through the junction at constant speed. B approaches from a perpendicular direction and accelerates into the crossing instead of yielding, striking A.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 42 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 50 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_fail_to_yield`: set_speed at t=1.2s for 14s (target_speed 12.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_fail_to_yield`.

*Ground-truth causal template (oracle only):*

* `B.B_fail_to_yield` --TRIGGERS--> `B.conflict_entry`  
  _accelerating instead of yielding puts B into the shared conflict region_
* `B.conflict_entry` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`

> B accelerates into the junction while A proceeds at constant speed

---

### S04: crossing braking

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s04_crossing_braking.yaml`

Identical crossing geometry to S03, but B brakes and yields on the approach. The paths still conflict; the outcome does not.

**Variant `yield`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 50 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 42 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_yield_brake`: brake at t=3.2s for 4s (intensity 0.9)
* **B** &mdash; `B_resume`: set_speed at t=8s for 14s (target_speed 7)

*Validation:* expected outcome **no_event**; A-B must close to under 12 m.

*Counterfactual candidates:* `B_yield_brake`.

*Ground-truth causal template (oracle only):*

* `B.B_yield_brake` --PREVENTS--> `no_collision(A-B)`  
  _yielding is what keeps the geometric conflict from becoming a collision_

> negative control: same crossing geometry as S03, but B yields
> a system that infers causality from geometry alone would wrongly flag a conflict outcome here

---

### S05: simultaneous crossing

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s05_simultaneous_crossing.yaml`

A and B approach the same unsignalised junction from perpendicular directions at comparable speeds and neither yields. Both arrive at the conflict region at essentially the same moment.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 40 m | 11 / 11 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 42 m | 11 / 11 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_no_yield`: set_speed at t=0.5s for 14s (target_speed 11.5)
* **B** &mdash; `B_no_yield`: set_speed at t=0.5s for 14s (target_speed 11.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `A_no_yield`, `B_no_yield`.

*Ground-truth causal template (oracle only):*

* `A.A_no_yield` --CONTRIBUTES_TO--> `A.conflict_entry`
* `B.B_no_yield` --CONTRIBUTES_TO--> `B.conflict_entry`
* `A.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`
* `B.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`

> symmetric: both participants contribute, neither is the sole initiator
> expected counterfactual result: intervening on either one prevents the collision

---

### S06: chain collision

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s06_chain_collision.yaml`

Three vehicles in a single lane: C leads, B follows, A is last. C brakes hard. Which pair collides first depends on how B responds.

**Variant `a_front_pushed`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 26 m | 14 / 14 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 44 m | 14 / 14 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_very_late_brake`: brake at t=5.6s for 8s (intensity 0.5)
* **B** &mdash; `B_reaction_brake`: brake at t=3.75s for 2s (intensity 1)
* **C** &mdash; `C_emergency_brake`: brake at t=3s for 10s (intensity 1)

*Validation:* expected outcome **collision**; collision pairs (A-B), (B-C); in order (A-B) then (B-C); A-B must close to under 6 m.

*Counterfactual candidates:* `C_emergency_brake`, `B_reaction_brake`, `A_very_late_brake`.

*Ground-truth causal template (oracle only):*

* `C.C_emergency_brake` --TRIGGERS--> `B.closing`
* `A.A_very_late_brake` --PREVENTS--> `collision(A-B)`  
  _A's braking is far too late to avert the first impact_
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `collision(A-B)` --CAUSES_OUTCOME--> `collision(B-C)`  
  _the second impact is a mechanical consequence of the first_

> S06a: A strikes B, and the impact pushes B into C
> B brakes in time; A brakes far too late

**Variant `b_rear_first`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 26 m | 14 / 14 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 44 m | 14 / 14 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake`: brake at t=6.2s for 8s (intensity 0.8)
* **B** &mdash; `B_no_reaction`: brake at t=5.6s for 8s (intensity 0.35)
* **C** &mdash; `C_emergency_brake`: brake at t=3s for 10s (intensity 1)

*Validation:* expected outcome **collision**; collision pairs (B-C), (A-B); in order (B-C) then (A-B); B-C must close to under 6 m.

*Counterfactual candidates:* `C_emergency_brake`, `B_no_reaction`, `A_late_brake`.

*Ground-truth causal template (oracle only):*

* `C.C_emergency_brake` --TRIGGERS--> `B.closing`
* `B.B_no_reaction` --CONTRIBUTES_TO--> `collision(B-C)`  
  _B's inadequate braking is what makes the first impact happen_
* `collision(B-C)` --CONTRIBUTES_TO--> `A.critical_ttc`  
  _B stopping abruptly on impact collapses A's remaining gap_
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`

> S06b: B strikes C first, then A strikes B
> same spatial layout as S06a, opposite causal order

---

### S07: partial view

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s07_partial_view.yaml`

C brakes hard, B responds, A closes on B and strikes it. A cannot observe C at all (occluded by B and restricted by a narrow-FOV radar), so A's local reconstruction should be missing the initiating cause that B observed.

**Variant `occluded`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | radar_narrow_fov |
| B | `vehicle.audi.tt` | spawn 265, fwd 24 m | 14 / 14 m/s | radar_baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 50 m | 14 / 14 m/s | radar_baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake`: brake at t=6.2s for 8s (intensity 0.8)
* **B** &mdash; `B_reaction_brake`: brake at t=3.7s for 10s (intensity 1)
* **C** &mdash; `C_emergency_brake`: brake at t=3s for 10s (intensity 1)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `C_emergency_brake`, `B_reaction_brake`, `A_late_brake`.

*Ground-truth causal template (oracle only):*

* `C.C_emergency_brake` --TRIGGERS--> `B.closing`  
  _the initiating event, observable by B but not by A_
* `B.closing` --CONTRIBUTES_TO--> `B.B_reaction_brake`
* `B.B_reaction_brake` --TRIGGERS--> `A.closing`
* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `A.A_late_brake` --PREVENTS--> `collision(A-B)`

> A: narrow-FOV radar and physically occluded from C by B
> B: baseline radar with a clear view of C
> the fusion benefit measured here must come from sensing, not from post-hoc edge deletion

**Variant `full_view`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | radar_baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 24 m | 14 / 14 m/s | radar_baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 50 m | 14 / 14 m/s | radar_baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake`: brake at t=6.2s for 8s (intensity 0.8)
* **B** &mdash; `B_reaction_brake`: brake at t=3.7s for 10s (intensity 1)
* **C** &mdash; `C_emergency_brake`: brake at t=3s for 10s (intensity 1)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `C_emergency_brake`, `B_reaction_brake`, `A_late_brake`.

*Ground-truth causal template (oracle only):*

* `C.C_emergency_brake` --TRIGGERS--> `B.closing`  
  _the initiating event, observable by B but not by A_
* `B.closing` --CONTRIBUTES_TO--> `B.B_reaction_brake`
* `B.B_reaction_brake` --TRIGGERS--> `A.closing`
* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `A.A_late_brake` --PREVENTS--> `collision(A-B)`

> control: same dynamics with A on the baseline radar profile

---

### S08: multidirection crossing

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s08_multidirection_crossing.yaml`

A crosses the junction from one direction while B enters from a perpendicular one without yielding, striking A. C approaches from the opposite direction to A, brakes short of the conflict region, and observes the collision from a third viewpoint.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 42 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 50 m | 9 / 9 m/s | baseline |
| C | `vehicle.nissan.patrol` | junction (101.6, 0.3), bearing 180deg, back 46 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_fail_to_yield`: set_speed at t=1.2s for 14s (target_speed 12.5)
* **C** &mdash; `C_defensive_stop`: brake at t=2.4s for 12s (intensity 0.9)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_fail_to_yield`, `C_defensive_stop`.

*Ground-truth causal template (oracle only):*

* `B.B_fail_to_yield` --TRIGGERS--> `B.conflict_entry`
* `B.conflict_entry` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `C.C_defensive_stop` --PREVENTS--> `no_collision(A-C)`  
  _C's stop keeps it out of the conflict region entirely_

> three viewpoints on one conflict region; C is an uninvolved observer
> C's evidence should let fusion recover parts of the interaction A and B each miss

---

### S09: roundabout

*Map:* **Town03_Opt** &nbsp;&nbsp; *Config:* `configs/scenarios/s09_roundabout.yaml`

A is already circulating inside the roundabout on the outer circulating lane. B approaches from the south entry, fails to give way, and collides with A while entering the circulating area.

**Variant `merge_conflict`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | location (3, -23) | 8 / 8 m/s | baseline |
| B | `vehicle.audi.tt` | junction (0, 0), bearing 90deg, back 35 m | 8 / 8 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_fail_to_give_way`: set_speed at t=1s for 14s (target_speed 9.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_fail_to_give_way`.

*Ground-truth causal template (oracle only):*

* `B.B_fail_to_give_way` --TRIGGERS--> `B.conflict_entry`  
  _entering the circulating area without giving way creates the conflict_
* `B.conflict_entry` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`

> both routes curve through the roundabout, so headings change throughout the encounter
> tests map-free reconstruction where constant-velocity prediction is weakest

---

### S10: single stop a

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s10_single_stop_a.yaml`

A faces a stop sign on its approach; B does not and has benchmark priority. The variants differ only in what A does about the sign: stop properly, roll through it, or stop and then pull out correctly.

**Variant `rolls_through`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing 0deg, back 30 m | 9 / 9 m/s | baseline |
| B | `vehicle.audi.tt` | junction (152.54, -0.23), bearing -90deg, back 44 m | 10 / 10 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_roll_through`: set_speed at t=3s for 12s (target_speed 5.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `A_roll_through`.

*Ground-truth causal template (oracle only):*

* `A.no_stop` --CONTRIBUTES_TO--> `A.stop_line_crossed`  
  _not stopping is what leaves A still moving at the line_
* `A.stop_line_crossed` --CONTRIBUTES_TO--> `A.conflict_entry`
* `A.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`

> A decelerates but never reaches rest, which is what makes this a rolling stop rather than a stop

**Variant `stops_safely`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing 0deg, back 30 m | 9 / 9 m/s | baseline |
| B | `vehicle.audi.tt` | junction (152.54, -0.23), bearing -90deg, back 44 m | 10 / 10 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_full_stop`: brake at t=2.6s for 7s (intensity 0.9)

*Validation:* expected outcome **near_miss**; A-B must close to under 18 m.

*Counterfactual candidates:* `A_full_stop`.

*Ground-truth causal template (oracle only):*

* `A.stopped` --PREVENTS--> `no_collision(A-B)`  
  _coming to rest before the line is what keeps A out of the conflict_

> the negative control: identical geometry, and A discharges the obligation
> B passes unobstructed, so the separation stays large

**Variant `stops_then_proceeds`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing 0deg, back 30 m | 9 / 9 m/s | baseline |
| B | `vehicle.audi.tt` | junction (152.54, -0.23), bearing -90deg, back 44 m | 10 / 10 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_full_stop`: brake at t=2.6s for 4.2s (intensity 0.9)
* **A** &mdash; `A_pull_away`: set_speed at t=7.4s for 10s (target_speed 9)

*Validation:* expected outcome **near_miss**; A-B must close to under 14 m.

*Counterfactual candidates:* `A_full_stop`, `A_pull_away`.

*Ground-truth causal template (oracle only):*

* `A.stopped` --PREVENTS--> `no_collision(A-B)`

> the case that distinguishes 'stopped' from 'stopped and then proceeded safely'
> A pulls away after B has cleared the junction, so both the stop and the crossing appear in the log

---

### S11: single stop b

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s11_single_stop_b.yaml`

B faces a stop sign on its approach; A does not and has benchmark priority. Structurally identical to S10 with the roles exchanged, which is what makes it a check on symmetry rather than an extra data point.

**Variant `rolls_through`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing -90deg, back 44 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (152.54, -0.23), bearing 0deg, back 30 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_roll_through`: set_speed at t=3s for 12s (target_speed 5.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_roll_through`.

*Ground-truth causal template (oracle only):*

* `B.no_stop` --CONTRIBUTES_TO--> `B.stop_line_crossed`
* `B.stop_line_crossed` --CONTRIBUTES_TO--> `B.conflict_entry`
* `B.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`

> exists to check that nothing in the method keys on participant identity
> findings should mirror S10 exactly with A and B exchanged

**Variant `stops_safely`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing -90deg, back 44 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (152.54, -0.23), bearing 0deg, back 30 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_full_stop`: brake at t=2.6s for 7s (intensity 0.9)

*Validation:* expected outcome **near_miss**; A-B must close to under 18 m.

*Counterfactual candidates:* `B_full_stop`.

*Ground-truth causal template (oracle only):*

* `B.stopped` --PREVENTS--> `no_collision(A-B)`

> exists to check that nothing in the method keys on participant identity
> findings should mirror S10 exactly with A and B exchanged

**Variant `stops_then_proceeds`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing -90deg, back 44 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (152.54, -0.23), bearing 0deg, back 30 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_full_stop`: brake at t=2.6s for 4.2s (intensity 0.9)
* **B** &mdash; `B_pull_away`: set_speed at t=7.4s for 10s (target_speed 9)

*Validation:* expected outcome **near_miss**; A-B must close to under 14 m.

*Counterfactual candidates:* `B_full_stop`, `B_pull_away`.

*Ground-truth causal template (oracle only):*

* `B.stopped` --PREVENTS--> `no_collision(A-B)`

> exists to check that nothing in the method keys on participant identity
> findings should mirror S10 exactly with A and B exchanged

---

### S12: all way stop

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s12_all_way_stop.yaml`

Both A and B face stop signs. Variants differ in who stops first, whether the two arrivals are distinguishable at all, and whether one vehicle stops.

**Variant `a_arrives_first`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (-283.42, 1.23), bearing 180deg, back 46 m | 9 / 9 m/s | baseline |
| B | `vehicle.audi.tt` | junction (-283.42, 1.23), bearing -90deg, back 46 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_stop`: brake at t=2.4s for 3s (intensity 0.9)
* **A** &mdash; `A_proceed`: set_speed at t=6s for 12s (target_speed 8)
* **B** &mdash; `B_stop`: brake at t=4s for 4.5s (intensity 0.9)
* **B** &mdash; `B_proceed`: set_speed at t=10s for 12s (target_speed 8)

*Validation:* expected outcome **near_miss**; A-B must close to under 16 m.

*Counterfactual candidates:* `A_stop`, `B_stop`.

*Ground-truth causal template (oracle only):*

* `A.stopped` --PREVENTS--> `no_collision(A-B)`
* `B.stopped` --PREVENTS--> `no_collision(A-B)`

> A completes its stop about 1.6 s before B, which clears the margin
> A then proceeds first, so both the stopping and the priority properties pass

**Variant `b_arrives_first`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (-283.42, 1.23), bearing 180deg, back 46 m | 9 / 9 m/s | baseline |
| B | `vehicle.audi.tt` | junction (-283.42, 1.23), bearing -90deg, back 46 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_stop`: brake at t=4s for 3.4s (intensity 0.9)
* **A** &mdash; `A_proceed`: set_speed at t=7.6s for 12s (target_speed 8)
* **B** &mdash; `B_stop`: brake at t=2.4s for 3s (intensity 0.9)
* **B** &mdash; `B_proceed`: set_speed at t=6s for 12s (target_speed 8)

*Validation:* expected outcome **near_miss**; A-B must close to under 16 m.

*Counterfactual candidates:* `A_stop`, `B_stop`.

*Ground-truth causal template (oracle only):*

* `A.stopped` --PREVENTS--> `no_collision(A-B)`
* `B.stopped` --PREVENTS--> `no_collision(A-B)`

> both approaches controlled, so the benchmark falls to arrival order
> no tie-break is configured in any variant, so a close arrival stays ambiguous

**Variant `near_simultaneous`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (-283.42, 1.23), bearing 180deg, back 46 m | 9 / 9 m/s | baseline |
| B | `vehicle.audi.tt` | junction (-283.42, 1.23), bearing -90deg, back 46 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_stop`: brake at t=1.6s for 3.4s (intensity 0.95)
* **A** &mdash; `A_proceed`: set_speed at t=5s for 12s (target_speed 9)
* **B** &mdash; `B_stop`: brake at t=2.7s for 1.2s (intensity 0.95)
* **B** &mdash; `B_proceed`: set_speed at t=3.9s for 12s (target_speed 9)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `A_stop`, `B_stop`, `A_proceed`, `B_proceed`.

*Ground-truth causal template (oracle only):*

* `A.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`
* `B.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`

> both stopped correctly, 0.1 s apart, and both then pulled away together
> the designed answer is AMBIGUOUS_PRIORITY: the stopping properties pass and priority cannot be decided
> a method that always produces a priority verdict scores better here while being wrong

**Variant `b_fails_to_stop`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (-283.42, 1.23), bearing 180deg, back 46 m | 9 / 9 m/s | baseline |
| B | `vehicle.audi.tt` | junction (-283.42, 1.23), bearing -90deg, back 46 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_stop`: brake at t=2.4s for 4.2s (intensity 0.9)
* **A** &mdash; `A_proceed`: set_speed at t=6.6s for 12s (target_speed 8)
* **B** &mdash; `B_roll_through`: set_speed at t=3s for 12s (target_speed 6)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `A_stop`, `B_roll_through`.

*Ground-truth causal template (oracle only):*

* `B.no_stop` --CONTRIBUTES_TO--> `B.stop_line_crossed`
* `B.stop_line_crossed` --CONTRIBUTES_TO--> `B.conflict_entry`
* `B.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`
* `A.stopped` --PREVENTS--> `collision(A-B)`  
  _A discharged its own obligation, which acts against the outcome without averting it_

> A stops and has priority by arrival; B rolls through and strikes it
> the asymmetry is in the normative layer, not in the physical one: both entered the junction

---

### S13: disputed lane change

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s13_disputed_lane_change.yaml`

A travels in the right lane; B is alongside in the left. In the disputed variants the gap between them closes and they touch, and which behaviour closed it differs. The safe variant keeps the same manoeuvre with room.

**Variant `cut_in`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 11 m, lane -1 | 13 / 13 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_cut_in`: lane_shift at t=4s for 3s (lateral_offset 3.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 5 m.

*Counterfactual candidates:* `B_cut_in`.

*Ground-truth causal template (oracle only):*

* `B.solid_line_crossed` --CONTRIBUTES_TO--> `A.closing`  
  _B moving laterally into A's lane is what collapses the gap_
* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`

> B has room ahead but not beside: the lateral move is what creates the conflict
> A holds a constant speed throughout, so nothing A did contributed

**Variant `accelerates_into_gap`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 11 m, lane -1 | 13 / 13 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_accelerate`: set_speed at t=3.4s for 10s (target_speed 17.5)
* **B** &mdash; `B_cut_in`: lane_shift at t=4.6s for 4s (lateral_offset 3.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 5 m.

*Counterfactual candidates:* `B_cut_in`, `A_accelerate`.

*Ground-truth causal template (oracle only):*

* `A.closing` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`
* `B.solid_line_crossed` --CONTRIBUTES_TO--> `A.closing`  
  _both behaviours contribute here, which is what makes the case contested_

> B performs the same lane change with more room; A accelerates into what is left
> the designed answer has both as contributors, not one
> a method that always names a single initiator will be wrong on this variant

**Variant `safe_lane_change`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 11 m, lane -1 | 13 / 13 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_cut_in`: lane_shift at t=6s for 5s (lateral_offset 3.5)

*Validation:* expected outcome **near_miss**; A-B must close to under 12 m.

*Counterfactual candidates:* `B_cut_in`.

*Ground-truth causal template (oracle only):*

* `B.solid_line_crossed` --CONTRIBUTES_TO--> `A.closing`
* `A.closing` --PREVENTS--> `no_collision(A-B)`  
  _the gap closes but never to contact, so the encounter is real and stays short of it_

> the negative control: identical manoeuvre, begun later and taken slower
> the line crossing still appears in B's log, so the normative layer sees the same evidence

---

### S14: three car chain

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s14_three_car_chain.yaml`

A leads, B follows, C is last, all in one lane. A brakes. Which pair collides first, and which vehicle was merely in the way, depends on how B responds.

**Variant `c_pushes_b`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265, fwd 30 m | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 15 m | 13 / 13 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265 | 13 / 13 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_brake`: brake at t=4s for 8s (intensity 0.85)
* **B** &mdash; `B_brake`: brake at t=4.9s for 1.6s (intensity 0.95)
* **C** &mdash; `C_no_response`: set_speed at t=4s for 10s (target_speed 13)

*Validation:* expected outcome **collision**; collision pairs (B-C), (A-B); in order (B-C) then (A-B); B-C must close to under 5 m.

*Counterfactual candidates:* `A_brake`, `B_brake`, `C_no_response`.

*Ground-truth causal template (oracle only):*

* `C.no_braking` --CAUSES_OUTCOME--> `collision(B-C)`  
  _C does not respond to the closing gap, which is what produces the first impact_
* `collision(B-C)` --CONTRIBUTES_TO--> `collision(A-B)`  
  _the shunt: the first impact is what puts B into A_

> B brakes adequately and is struck from behind anyway
> B strikes A, but nothing B did reaches that impact except through being hit

**Variant `b_hits_a_first`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265, fwd 30 m | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 15 m | 13 / 13 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265 | 13 / 13 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_brake`: brake at t=4s for 8s (intensity 0.85)
* **B** &mdash; `B_late_brake`: brake at t=6.3s for 8s (intensity 1)
* **C** &mdash; `C_late_brake`: brake at t=6.9s for 8s (intensity 1)

*Validation:* expected outcome **collision**; collision pairs (A-B), (B-C); in order (A-B) then (B-C); A-B must close to under 5 m.

*Counterfactual candidates:* `A_brake`, `B_late_brake`, `C_late_brake`.

*Ground-truth causal template (oracle only):*

* `B.no_braking` --CAUSES_OUTCOME--> `collision(A-B)`
* `C.no_braking` --CAUSES_OUTCOME--> `collision(B-C)`

> almost the same end configuration as c_pushes_b, and the opposite causal structure
> here B does contribute to the first impact, and C to the second only
> the two variants together test whether the method reads the order or the layout

**Variant `independent_impacts`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265, fwd 30 m | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 15 m | 13 / 13 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265 | 13 / 13 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_brake`: brake at t=4s for 8s (intensity 0.85)
* **B** &mdash; `B_late_brake`: brake at t=6.3s for 6s (intensity 1)
* **C** &mdash; `C_much_later_brake`: brake at t=5s for 4s (intensity 0.7)
* **C** &mdash; `C_creep_forward`: set_speed at t=13s for 8s (target_speed 4)

*Validation:* expected outcome **collision**; collision pairs (A-B), (B-C); in order (A-B) then (B-C); A-B must close to under 5 m.

*Counterfactual candidates:* `A_brake`, `B_late_brake`, `C_much_later_brake`.

*Ground-truth causal template (oracle only):*

* `B.no_braking` --CAUSES_OUTCOME--> `collision(A-B)`
* `C.unsafe_entry` --CAUSES_OUTCOME--> `collision(B-C)`

> two impacts several seconds apart with no causal link between them
> tests that the method does not chain impacts merely because they share a vehicle
> the clock alignment still works: B feels both, so the transitive route is unchanged

---

### S15: intersection pileup

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s15_intersection_pileup.yaml`

B fails to stop and strikes A in the junction. The impact deflects A into C, which is approaching the same junction from a third direction.

**Variant `deflected_into_c`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing -90deg, back 44 m | 11 / 11 m/s | baseline |
| B | `vehicle.nissan.patrol` | junction (152.54, -0.23), bearing 0deg, back 30 m | 10 / 10 m/s | baseline |
| C | `vehicle.audi.tt` | junction (152.54, -0.23), bearing 90deg, back 48 m | 6 / 6 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_roll_through`: set_speed at t=3s for 12s (target_speed 7)

*Validation:* expected outcome **collision**; collision pairs (A-B), (A-C); in order (A-B) then (A-C); A-B must close to under 6 m.

*Counterfactual candidates:* `B_roll_through`.

*Ground-truth causal template (oracle only):*

* `B.no_stop` --CONTRIBUTES_TO--> `B.conflict_entry`
* `B.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`
* `collision(A-B)` --CONTRIBUTES_TO--> `collision(A-C)`  
  _the first impact deflects A out of its path and into C_

> designed answer: B contributes to both impacts, A to neither, C to neither
> A was struck and then struck C, which is the pushed-vehicle shape across a junction

**Variant `single_impact`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing -90deg, back 44 m | 11 / 11 m/s | baseline |
| B | `vehicle.nissan.patrol` | junction (152.54, -0.23), bearing 0deg, back 30 m | 10 / 10 m/s | baseline |
| C | `vehicle.audi.tt` | junction (152.54, -0.23), bearing 90deg, back 70 m | 6 / 6 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_roll_through`: set_speed at t=3s for 12s (target_speed 7)

*Validation:* expected outcome **collision**; collision pairs (A-B); in order (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_roll_through`.

*Ground-truth causal template (oracle only):*

* `B.no_stop` --CONTRIBUTES_TO--> `B.conflict_entry`
* `B.conflict_entry` --CAUSES_OUTCOME--> `collision(A-B)`

> the control for deflected_into_c: one impact instead of two, same initiating behaviour
> C is present and uninvolved, and here there is no impact to be wrongly attributed to it
> also a partial-alignment case: C feels no contact, so C cannot be tied to the common timeline at all

**Variant `b_stops`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (152.54, -0.23), bearing -90deg, back 44 m | 11 / 11 m/s | baseline |
| B | `vehicle.nissan.patrol` | junction (152.54, -0.23), bearing 0deg, back 30 m | 10 / 10 m/s | baseline |
| C | `vehicle.audi.tt` | junction (152.54, -0.23), bearing 90deg, back 48 m | 6 / 6 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_full_stop`: brake at t=2.6s for 8s (intensity 0.9)

*Validation:* expected outcome **near_miss**; A-B must close to under 16 m.

*Counterfactual candidates:* `B_full_stop`.

*Ground-truth causal template (oracle only):*

* `B.stopped` --PREVENTS--> `no_collision(A-B)`

> the negative control, and also the no-collision timing case
> with no contact anywhere, no recorder can be tied to another and the merged log says so

---

### S16: secondary collision

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s16_secondary_collision.yaml`

A brakes hard and B runs into it. What happens next to B -- deflected into C, driving on into C, or stopping clear -- is what the variants change.

**Variant `consequential`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265, fwd 26 m | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265 | 13 / 13 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 34 m, lane -1 | 12 / 12 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_emergency_brake`: brake at t=4s for 8s (intensity 1)
* **B** &mdash; `B_late_brake`: brake at t=5.9s for 5s (intensity 0.9)
* **B** &mdash; `B_deflected`: lane_shift at t=7.4s for 2s (lateral_offset 3.2)

*Validation:* expected outcome **collision**; collision pairs (A-B), (B-C); in order (A-B) then (B-C); A-B must close to under 5 m.

*Counterfactual candidates:* `A_emergency_brake`, `B_late_brake`.

*Ground-truth causal template (oracle only):*

* `A.A_emergency_brake` --CONTRIBUTES_TO--> `B.closing`
* `B.no_braking` --CAUSES_OUTCOME--> `collision(A-B)`
* `collision(A-B)` --CONTRIBUTES_TO--> `collision(B-C)`  
  _the first impact is what puts B across into C_

> designed answer: B contributes to the first impact and not to the second
> B's displacement into C follows from being unable to stop after the impact
> the two impacts are about 1.5 s apart, close enough that contact matching has real work to do

**Variant `independent`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265, fwd 26 m | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265 | 13 / 13 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 52 m, lane -1 | 12 / 12 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_emergency_brake`: brake at t=4s for 8s (intensity 1)
* **B** &mdash; `B_late_brake`: brake at t=5.9s for 5s (intensity 0.9)
* **B** &mdash; `B_resume`: set_speed at t=13s for 8s (target_speed 11)
* **B** &mdash; `B_changes_lane`: lane_shift at t=17s for 3s (lateral_offset 3.2)

*Validation:* expected outcome **collision**; collision pairs (A-B), (B-C); in order (A-B) then (B-C); A-B must close to under 5 m.

*Counterfactual candidates:* `A_emergency_brake`, `B_late_brake`, `B_changes_lane`.

*Ground-truth causal template (oracle only):*

* `A.A_emergency_brake` --CONTRIBUTES_TO--> `B.closing`
* `B.no_braking` --CAUSES_OUTCOME--> `collision(A-B)`
* `B.solid_line_crossed` --CAUSES_OUTCOME--> `collision(B-C)`  
  _the second impact is B's own lane change, not a consequence of the first_

> designed answer: B contributes to both impacts, for two unrelated reasons
> the pair and the geometry of the second impact match the consequential variant
> what differs is that a path from B's own behaviour reaches it without passing through the first impact

**Variant `avoided`**

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265, fwd 26 m | 13 / 13 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265 | 13 / 13 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 52 m, lane -1 | 12 / 12 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_emergency_brake`: brake at t=4s for 8s (intensity 1)
* **B** &mdash; `B_late_brake`: brake at t=5.9s for 9s (intensity 1)

*Validation:* expected outcome **collision**; collision pairs (A-B); in order (A-B); A-B must close to under 5 m.

*Counterfactual candidates:* `A_emergency_brake`, `B_late_brake`.

*Ground-truth causal template (oracle only):*

* `A.A_emergency_brake` --CONTRIBUTES_TO--> `B.closing`
* `B.no_braking` --CAUSES_OUTCOME--> `collision(A-B)`

> one impact only; B stops clear and C is untouched
> C never feels a contact, so C stays off the common timeline and the merged log says so

---

<!-- END GENERATED SCENARIO TABLE -->
