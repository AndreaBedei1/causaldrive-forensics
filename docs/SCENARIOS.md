# Scenarios

Scenarios are pure data: `configs/scenarios/*.yaml`, turned into actors, routes
and scripted controllers by `cdf.simulation.scenario_base`. Keeping them
declarative buys three things the experiment protocol depends on --
reproducibility (the whole spec is hashed into the run manifest), interventions
(every behaviour is a named `ScriptedAction`, so a counterfactual is "the same
spec with one action disabled, delayed or weakened") and validation (the spec
states what is *supposed* to happen, so a scenario that silently stops producing
its intended encounter fails loudly).

## Maps

**S09 (roundabout) is on Town03_Opt. Every other scenario is on Town05.**

The tested simulator build cannot load base Town03 reliably, so S09 uses the
stable `Town03_Opt` variant with the same roundabout geometry.

Two Town05 sites carry almost everything:

* the **three-lane straight** around `y = -204` (recommended spawn point index
  **265**), measured to offer ~160 m of junction-free travel -- used by S01, S02,
  S06 and S07;
* **junction 720** at `(101.6, 0.3)`, measured to expose four clean approaches
  (maximum bearing error 0.7°) and carrying **no traffic light**, so signal state
  cannot confound a crossing scenario -- used by S03, S04, S05 and S08;

On Town03_Opt, the central roundabout around `(0.0, 0.0)` is used by S09:
four clean approaches whose routes curve by roughly 90° through the circulating
area. That curvature is the point -- constant-velocity path prediction is
weakest exactly where heading changes fastest.

Crossing scenarios name a junction centre and two compass bearings rather than a
table of hand-measured spawn coordinates (`SpawnSpec.anchor: junction_approach` →
`junction_approach_waypoint()`), which is what makes them portable.

---

## Overview

| Id | Name | Map | Vehicles | Variants (default **bold**) | Expected outcome | Max duration |
|---|---|---|---|---|---|---|
| S01 | `rear_end` | Town05 | 2 (A, B) | **`crash`**, `avoided` | collision / near miss | 26 s |
| S02 | `cut_in` | Town05 | 2 (A, B) | **`crash`**, `avoided` | collision / near miss | 26 s |
| S03 | `crossing` | Town05 | 2 (A, B) | **`crash`** | collision | 28 s |
| S04 | `crossing_braking` | Town05 | 2 (A, B) | **`yield`** | **no event** | 28 s |
| S05 | `simultaneous_crossing` | Town05 | 2 (A, B) | **`crash`** | collision | 28 s |
| S06 | `chain_collision` | Town05 | 3 (A, B, C) | **`a_front_pushed`**, `b_rear_first` | collision (2 impacts, ordered) | 30 s |
| S07 | `partial_view` | Town05 | 3 (A, B, C) | **`occluded`**, `full_view` | collision | 30 s |
| S08 | `multidirection_crossing` | Town05 | 3 (A, B, C) | **`crash`** | collision | 30 s |
| S09 | `roundabout` | **Town04** | 2 (A, B) | **`merge_conflict`** | collision | 30 s |

---

## Scenario definitions

<!-- BEGIN GENERATED SCENARIO TABLE -->

_Generated from `configs/scenarios/*.yaml` by `scripts/generate_scenario_docs.py`. Do not edit by hand._

### S01 -- rear end

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s01_rear_end.yaml`

B travels ahead of A in the same lane and brakes hard. A reacts late and strikes B. The avoided variant keeps the geometry but gives A a timely response, which turns the outcome into a near miss.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 28 m | 14 / 14 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake` -- brake at t=5.6s for 6s (intensity 0.85)
* **B** &mdash; `B_emergency_brake` -- brake at t=4s for 8s (intensity 1)

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

* **A** &mdash; `A_late_brake` -- brake at t=5.1s for 8s (intensity 1)
* **B** &mdash; `B_emergency_brake` -- brake at t=4s for 8s (intensity 1)

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

### S02 -- cut in

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s02_cut_in.yaml`

B starts in the lane to A's left, slightly ahead, then moves laterally into A's lane while travelling slower than A. A closes rapidly and reacts late.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 30 m, lane -1 | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake` -- brake at t=3.9s for 6s (intensity 0.85)
* **B** &mdash; `B_cut_in` -- lane_shift at t=1s for 2.2s (lateral_m 3.5)
* **B** &mdash; `B_slow_after_cut_in` -- set_speed at t=3.2s for 12s (target_speed 6.5)

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

* **A** &mdash; `A_late_brake` -- brake at t=2.9s for 9s (intensity 1)
* **B** &mdash; `B_cut_in` -- lane_shift at t=1s for 2.2s (lateral_m 3.5)
* **B** &mdash; `B_slow_after_cut_in` -- set_speed at t=3.2s for 12s (target_speed 6.5)

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

### S03 -- crossing

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s03_crossing.yaml`

A travels through the junction at constant speed. B approaches from a perpendicular direction and accelerates into the crossing instead of yielding, striking A.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 42 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 50 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_fail_to_yield` -- set_speed at t=1.2s for 14s (target_speed 12.5)

*Validation:* expected outcome **collision**; collision pairs (A-B); A-B must close to under 6 m.

*Counterfactual candidates:* `B_fail_to_yield`.

*Ground-truth causal template (oracle only):*

* `B.B_fail_to_yield` --TRIGGERS--> `B.conflict_entry`  
  _accelerating instead of yielding puts B into the shared conflict region_
* `B.conflict_entry` --CONTRIBUTES_TO--> `A.critical_ttc`
* `A.critical_ttc` --CAUSES_OUTCOME--> `collision(A-B)`

> B accelerates into the junction while A proceeds at constant speed

---

### S04 -- crossing braking

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s04_crossing_braking.yaml`

Identical crossing geometry to S03, but B brakes and yields on the approach. The paths still conflict; the outcome does not.

**Variant `yield`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 50 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 42 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_yield_brake` -- brake at t=3.2s for 4s (intensity 0.9)
* **B** &mdash; `B_resume` -- set_speed at t=8s for 14s (target_speed 7)

*Validation:* expected outcome **no_event**; A-B must close to under 12 m.

*Counterfactual candidates:* `B_yield_brake`.

*Ground-truth causal template (oracle only):*

* `B.B_yield_brake` --PREVENTS--> `no_collision(A-B)`  
  _yielding is what keeps the geometric conflict from becoming a collision_

> negative control: same crossing geometry as S03, but B yields
> a system that infers causality from geometry alone would wrongly flag a conflict outcome here

---

### S05 -- simultaneous crossing

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s05_simultaneous_crossing.yaml`

A and B approach the same unsignalised junction from perpendicular directions at comparable speeds and neither yields. Both arrive at the conflict region at essentially the same moment.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 40 m | 11 / 11 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 42 m | 11 / 11 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_no_yield` -- set_speed at t=0.5s for 14s (target_speed 11.5)
* **B** &mdash; `B_no_yield` -- set_speed at t=0.5s for 14s (target_speed 11.5)

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

### S06 -- chain collision

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s06_chain_collision.yaml`

Three vehicles in a single lane: C leads, B follows, A is last. C brakes hard. Which pair collides first depends on how B responds.

**Variant `a_front_pushed`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | baseline |
| B | `vehicle.audi.tt` | spawn 265, fwd 26 m | 14 / 14 m/s | baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 44 m | 14 / 14 m/s | baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_very_late_brake` -- brake at t=5.6s for 8s (intensity 0.5)
* **B** &mdash; `B_reaction_brake` -- brake at t=3.75s for 2s (intensity 1)
* **C** &mdash; `C_emergency_brake` -- brake at t=3s for 10s (intensity 1)

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

* **A** &mdash; `A_late_brake` -- brake at t=6.2s for 8s (intensity 0.8)
* **B** &mdash; `B_no_reaction` -- brake at t=5.6s for 8s (intensity 0.35)
* **C** &mdash; `C_emergency_brake` -- brake at t=3s for 10s (intensity 1)

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

### S07 -- partial view

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s07_partial_view.yaml`

C brakes hard, B responds, A closes on B and strikes it. A cannot observe C at all (occluded by B and restricted by a narrow-FOV radar), so A's local reconstruction should be missing the initiating cause that B observed.

**Variant `occluded`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | spawn 265 | 14 / 14 m/s | radar_narrow_fov |
| B | `vehicle.audi.tt` | spawn 265, fwd 24 m | 14 / 14 m/s | radar_baseline |
| C | `vehicle.nissan.patrol` | spawn 265, fwd 50 m | 14 / 14 m/s | radar_baseline |

Scripted actions (these are the intervention handles):

* **A** &mdash; `A_late_brake` -- brake at t=6.2s for 8s (intensity 0.8)
* **B** &mdash; `B_reaction_brake` -- brake at t=3.7s for 10s (intensity 1)
* **C** &mdash; `C_emergency_brake` -- brake at t=3s for 10s (intensity 1)

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

* **A** &mdash; `A_late_brake` -- brake at t=6.2s for 8s (intensity 0.8)
* **B** &mdash; `B_reaction_brake` -- brake at t=3.7s for 10s (intensity 1)
* **C** &mdash; `C_emergency_brake` -- brake at t=3s for 10s (intensity 1)

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

### S08 -- multidirection crossing

*Map:* **Town05** &nbsp;&nbsp; *Config:* `configs/scenarios/s08_multidirection_crossing.yaml`

A crosses the junction from one direction while B enters from a perpendicular one without yielding, striking A. C approaches from the opposite direction to A, brakes short of the conflict region, and observes the collision from a third viewpoint.

**Variant `crash`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | junction (101.6, 0.3), bearing 0deg, back 42 m | 10 / 10 m/s | baseline |
| B | `vehicle.audi.tt` | junction (101.6, 0.3), bearing -90deg, back 50 m | 9 / 9 m/s | baseline |
| C | `vehicle.nissan.patrol` | junction (101.6, 0.3), bearing 180deg, back 46 m | 9 / 9 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_fail_to_yield` -- set_speed at t=1.2s for 14s (target_speed 12.5)
* **C** &mdash; `C_defensive_stop` -- brake at t=2.4s for 12s (intensity 0.9)

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

### S09 -- roundabout

*Map:* **Town03_Opt** &nbsp;&nbsp; *Config:* `configs/scenarios/s09_roundabout.yaml`

A is already circulating inside the roundabout on the outer circulating lane. B approaches from the south entry, fails to give way, and collides with A while entering the circulating area.

**Variant `merge_conflict`** *(default)*

| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |
|---|---|---|---|---|
| A | `vehicle.tesla.model3` | location (3, -23) | 8 / 8 m/s | baseline |
| B | `vehicle.audi.tt` | junction (0, 0), bearing 90deg, back 35 m | 8 / 8 m/s | baseline |

Scripted actions (these are the intervention handles):

* **B** &mdash; `B_fail_to_give_way` -- set_speed at t=1s for 14s (target_speed 9.5)

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

<!-- END GENERATED SCENARIO TABLE -->
