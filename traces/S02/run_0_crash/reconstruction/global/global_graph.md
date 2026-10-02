# Global graph - S02/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 4.65 | -4.65 | reported the reference collision collision_001 |
| B | ALIGNED | B:e07 | 4.65 | -4.65 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 2900.23 vs 2900.23 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 2900.23 vs 2900.23 N*s)<br>tracked for 4.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 6.2 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.22 m/s over 3.0 s<br>clearance at the contact 0.20 m<br>the only track of A compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.65 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.65 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.65 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -4.65 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -4.50 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.15 |  |
| g06 | -4.50 | CLOSING_START | A | B | A:e04 @ 0.15 | active_at_first_observation=True |
| g07 | -2.55 | CUT_IN_FROM_LEFT_START | A | B | A:e05 @ 2.10 |  |
| g08 | -1.50 | THROTTLE_END | B | - | B:e03 @ 3.15 |  |
| g09 | -1.50 | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g10 | -1.40 | EGO_PATH_ENTRY | A | B | A:e06 @ 3.25 |  |
| g11 | -1.40 | CRITICAL_TTC_START | A | B | A:e07 @ 3.25 |  |
| g12 | -1.00 | BRAKE_END | B | - | B:e05 @ 3.65 |  |
| g13 | -0.90 | THROTTLE_START | B | - | B:e06 @ 3.75 |  |
| g14 | -0.80 | THROTTLE_END | A | - | A:e08 @ 3.85 |  |
| g15 | -0.80 | BRAKE_START | A | - | A:e09 @ 3.85 |  |
| g16 | 0.00 | COLLISION | - | A, B | A:e10 @ 4.65, B:e07 @ 4.65 | matched_event=collision_001; reference_event=True; peak_impulse=A 2900.23, B 2900.23 |
| g17 | 0.00 | CUT_IN_FROM_LEFT_END | A | B | A:e11 @ 4.65 |  |
| g18 | 0.00 | CRITICAL_TTC_END | A | B | A:e12 @ 4.65 |  |
| g19 | 0.00 | CLOSING_END | A | B | A:e13 @ 4.65 |  |
| g20 | 0.00 | THROTTLE_END | B | - | B:e08 @ 4.65 |  |
| g21 | 0.00 | BRAKE_START | B | - | B:e09 @ 4.65 |  |
| g22 | 0.40 | MOVING_END | A | - | A:e14 @ 5.05 |  |
| g23 | 0.40 | STOP_START | A | - | A:e15 @ 5.05 |  |
| g24 | 0.55 | MOVING_END | B | - | B:e10 @ 5.20 |  |
| g25 | 0.55 | STOP_START | B | - | B:e11 @ 5.20 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g01 --PRECEDES--> g06
    g02 --PRECEDES--> g05
    g02 --PRECEDES--> g06
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g14 --PRECEDES--> g19
    g14 --PRECEDES--> g20
    g14 --PRECEDES--> g21
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g16 --PRECEDES--> g22
    g16 --PRECEDES--> g23
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g07
    g05 --SAME_TRACK--> g10
    g05 --SAME_TRACK--> g11
    g05 --SAME_TRACK--> g17
    g05 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g19
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.65 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B) |
| -4.50 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -2.55 | CUT_IN_FROM_LEFT_START(A,B) |
| -1.50 | THROTTLE_END(B); BRAKE_START(B) |
| -1.40 | EGO_PATH_ENTRY(A,B); CRITICAL_TTC_START(A,B) |
| -1.00 | BRAKE_END(B) |
| -0.90 | THROTTLE_START(B) |
| -0.80 | THROTTLE_END(A); BRAKE_START(A) |
| +0.00 | COLLISION(A,B); CUT_IN_FROM_LEFT_END(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); THROTTLE_END(B); BRAKE_START(B) |
| +0.40 | MOVING_END(A); STOP_START(A) |
| +0.55 | MOVING_END(B); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 2.10 < CRITICAL_TTC_START 3.25 (+1.15 s) < COLLISION with B 4.65 (+1.40 s); EGO_PATH_ENTRY 3.25 together with critical TTC (+0.00 s) [local times; t_global: cut_in -2.55, critical_ttc_start -1.40, ego_path_entry -1.40, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.65 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02) | ego: not yet observed |
| -4.65 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -4.50 | A | g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 CLOSING_START(A,B) (A:e04) | ego: MOVING, THROTTLE |
| -2.55 | A | g07 CUT_IN_FROM_LEFT_START(A,B) (A:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.50 | B | g08 THROTTLE_END(B) (B:e03)<br>g09 BRAKE_START(B) (B:e04) | ego: MOVING, THROTTLE |
| -1.40 | A | g10 EGO_PATH_ENTRY(A,B) (A:e06)<br>g11 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| -1.00 | B | g12 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE |
| -0.90 | B | g13 THROTTLE_START(B) (B:e06) | ego: MOVING |
| -0.80 | A | g14 THROTTLE_END(A) (A:e08)<br>g15 BRAKE_START(A) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | A | g16 COLLISION(A,B) (A:e10)<br>g17 CUT_IN_FROM_LEFT_END(A,B) (A:e11)<br>g18 CRITICAL_TTC_END(A,B) (A:e12)<br>g19 CLOSING_END(A,B) (A:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g16 COLLISION(A,B) (B:e07)<br>g20 THROTTLE_END(B) (B:e08)<br>g21 BRAKE_START(B) (B:e09) | ego: MOVING, THROTTLE |
| +0.40 | A | g22 MOVING_END(A) (A:e14)<br>g23 STOP_START(A) (A:e15) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.55 | B | g24 MOVING_END(B) (B:e10)<br>g25 STOP_START(B) (B:e11) | ego: MOVING, BRAKE |

## Plain-language reading

- 4.65 s before the reference collision, A started moving (already the case when first observed).
- 4.65 s before the reference collision, B started moving (already the case when first observed).
- 4.65 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.65 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.50 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 4.50 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.55 s before the reference collision, A observed B cutting in from the left.
- 1.50 s before the reference collision, B released the accelerator.
- 1.50 s before the reference collision, B started braking.
- 1.40 s before the reference collision, A observed B enter its forward path corridor.
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.00 s before the reference collision, B released the brake.
- 0.90 s before the reference collision, B pressed the accelerator.
- 0.80 s before the reference collision, A released the accelerator.
- 0.80 s before the reference collision, A started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 2900, B: 2900 N*s).
- At the reference collision, A observed B's cut-in from the left settle.
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B released the accelerator.
- At the reference collision, B started braking.
- 0.40 s after the reference collision, A stopped moving.
- 0.40 s after the reference collision, A came to a stop.
- 0.55 s after the reference collision, B stopped moving.
- 0.55 s after the reference collision, B came to a stop.
