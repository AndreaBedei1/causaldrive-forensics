# Global graph - S02/run_0_critical_before_cut_in

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 4.10 | -4.10 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 4.10 | -4.10 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 604.48 vs 604.48 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.95 | A and B both reported collision_001 (peak impulse 604.48 vs 604.48 N*s)<br>tracked for 3.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.8 m -> 0.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.47 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.98 | B and A both reported collision_001 (peak impulse 604.48 vs 604.48 N*s)<br>tracked for 1.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.7 m -> 0.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.29 m/s over 1.9 s<br>clearance at the contact 0.35 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.10 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.10 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -4.10 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -3.95 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.15 |  |
| g06 | -3.95 | CLOSING_START | A | B | A:e04 @ 0.15 | active_at_first_observation=True |
| g07 | -1.90 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 2.20 |  |
| g08 | -1.90 | CLOSING_START | B | A | B:e04 @ 2.20 | active_at_first_observation=True |
| g09 | -1.65 | THROTTLE_END | A | - | A:e05 @ 2.45 |  |
| g10 | -1.65 | BRAKE_START | A | - | A:e06 @ 2.45 |  |
| g11 | -1.45 | CRITICAL_TTC_START | A | B | A:e07 @ 2.65 |  |
| g12 | -1.40 | CRITICAL_TTC_START | B | A | B:e05 @ 2.70 |  |
| g13 | -1.15 | CUT_IN_FROM_LEFT_START | A | B | A:e08 @ 2.95 |  |
| g14 | -0.85 | BRAKE_END | A | - | A:e09 @ 3.25 |  |
| g15 | -0.75 | THROTTLE_START | A | - | A:e10 @ 3.35 |  |
| g16 | -0.45 | EGO_PATH_ENTRY | A | B | A:e11 @ 3.65 |  |
| g17 | 0.00 | COLLISION | - | A, B | A:e12 @ 4.10, B:e06 @ 4.10 | matched_event=collision_001; reference_event=True; peak_impulse=A 604.48, B 604.48 |
| g18 | 0.00 | CRITICAL_TTC_END | A | B | A:e13 @ 4.10 |  |
| g19 | 0.00 | CRITICAL_TTC_END | B | A | B:e07 @ 4.10 |  |
| g20 | 0.05 | CLOSING_END | A | B | A:e14 @ 4.15 |  |
| g21 | 0.05 | CLOSING_END | B | A | B:e08 @ 4.15 |  |
| g22 | 0.05 | THROTTLE_END | A | - | A:e15 @ 4.15 |  |
| g23 | 0.05 | THROTTLE_END | B | - | B:e09 @ 4.15 |  |
| g24 | 0.05 | BRAKE_START | A | - | A:e16 @ 4.15 |  |
| g25 | 0.05 | BRAKE_START | B | - | B:e10 @ 4.15 |  |
| g26 | 0.55 | MOVING_END | A | - | A:e17 @ 4.65 |  |
| g27 | 0.55 | MOVING_END | B | - | B:e11 @ 4.65 |  |
| g28 | 0.55 | STOP_START | A | - | A:e18 @ 4.65 |  |
| g29 | 0.55 | STOP_START | B | - | B:e12 @ 4.65 |  |
| g30 | 0.80 | CUT_IN_FROM_LEFT_END | A | B | A:e19 @ 4.90 |  |

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
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g17 --PRECEDES--> g25
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g18 --PRECEDES--> g24
    g18 --PRECEDES--> g25
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g19 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g20 --PRECEDES--> g28
    g20 --PRECEDES--> g29
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g21 --PRECEDES--> g29
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g11
    g05 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g12
    g07 --SAME_TRACK--> g19
    g07 --SAME_TRACK--> g21
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.10 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B) |
| -3.95 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -1.90 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -1.65 | THROTTLE_END(A); BRAKE_START(A) |
| -1.45 | CRITICAL_TTC_START(A,B) |
| -1.40 | CRITICAL_TTC_START(B,A) |
| -1.15 | CUT_IN_FROM_LEFT_START(A,B) |
| -0.85 | BRAKE_END(A) |
| -0.75 | THROTTLE_START(A) |
| -0.45 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | CLOSING_END(A,B); CLOSING_END(B,A); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.55 | MOVING_END(A); MOVING_END(B); STOP_START(A); STOP_START(B) |
| +0.80 | CUT_IN_FROM_LEFT_END(A,B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): critical TTC already active before the cut-in: CRITICAL_TTC_START 2.65 <= CUT_IN_FROM_LEFT_START 2.95 (+0.30 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.00 s) [local times; t_global: cut_in -1.15, critical_ttc_start -1.45, ego_path_entry -0.45, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.70, COLLISION with A 4.10 (+1.40 s) [local times; t_global: critical_ttc_start -1.40, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.10 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02) | ego: not yet observed |
| -4.10 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -3.95 | A | g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 CLOSING_START(A,B) (A:e04) | ego: MOVING, THROTTLE |
| -1.90 | B | g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 CLOSING_START(B,A) (B:e04) | ego: MOVING, THROTTLE |
| -1.65 | A | g09 THROTTLE_END(A) (A:e05)<br>g10 BRAKE_START(A) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.45 | A | g11 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| -1.40 | B | g12 CRITICAL_TTC_START(B,A) (B:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -1.15 | A | g13 CUT_IN_FROM_LEFT_START(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC |
| -0.85 | A | g14 BRAKE_END(A) (A:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| -0.75 | A | g15 THROTTLE_START(A) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| -0.45 | A | g16 EGO_PATH_ENTRY(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| +0.00 | A | g17 COLLISION(A,B) (A:e12)<br>g18 CRITICAL_TTC_END(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g17 COLLISION(A,B) (B:e06)<br>g19 CRITICAL_TTC_END(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC |
| +0.05 | A | g20 CLOSING_END(A,B) (A:e14)<br>g22 THROTTLE_END(A) (A:e15)<br>g24 BRAKE_START(A) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.05 | B | g21 CLOSING_END(B,A) (B:e08)<br>g23 THROTTLE_END(B) (B:e09)<br>g25 BRAKE_START(B) (B:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| +0.55 | A | g26 MOVING_END(A) (A:e17)<br>g28 STOP_START(A) (A:e18) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.55 | B | g27 MOVING_END(B) (B:e11)<br>g29 STOP_START(B) (B:e12) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.80 | A | g30 CUT_IN_FROM_LEFT_END(A,B) (A:e19) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |

## Plain-language reading

- 4.10 s before the reference collision, A started moving (already the case when first observed).
- 4.10 s before the reference collision, B started moving (already the case when first observed).
- 4.10 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 3.95 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 3.95 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.90 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 1.90 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.65 s before the reference collision, A released the accelerator.
- 1.65 s before the reference collision, A started braking.
- 1.45 s before the reference collision, A's time-to-contact with B became critical.
- 1.40 s before the reference collision, B's time-to-contact with A became critical.
- 1.15 s before the reference collision, A observed B cutting in from the left.
- 0.85 s before the reference collision, A released the brake.
- 0.75 s before the reference collision, A pressed the accelerator.
- 0.45 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 604, B: 604 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.55 s after the reference collision, A stopped moving.
- 0.55 s after the reference collision, B stopped moving.
- 0.55 s after the reference collision, A came to a stop.
- 0.55 s after the reference collision, B came to a stop.
- 0.80 s after the reference collision, A observed B's cut-in from the left settle.
