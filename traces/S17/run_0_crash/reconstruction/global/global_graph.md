# Global graph - S17/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_002 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e15 | 5.75 | -5.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e11 | 5.75 | -5.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 915.98 vs 915.98 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 915.98 vs 915.98 N*s)<br>tracked for 5.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 3.1 m -> 4.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 2.79 m/s over 3.0 s (> 1.50)<br>clearance at the contact 2.81 m |
| A:track_002 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 915.98 vs 915.98 N*s)<br>tracked for 5.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.21 m/s over 3.0 s<br>clearance at the contact 0.09 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 915.98 vs 915.98 N*s)<br>tracked for 5.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.51 m/s over 3.0 s<br>clearance at the contact 0.33 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 915.98 vs 915.98 N*s)<br>tracked for 5.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 5.7 m -> 6.3 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.45 m/s over 3.0 s (> 1.50)<br>clearance at the contact 5.26 m (beyond 3.50 m: confidence factor 0.84) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.75 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.75 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.75 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -5.75 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -5.75 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 |  |
| g06 | -5.75 | TRACK_APPEARED_RIGHT | A | A:track_001 | A:e04 @ 0.00 |  |
| g07 | -5.75 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 |  |
| g08 | -5.75 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e04 @ 0.00 |  |
| g09 | -3.05 | CLOSING_START | B | B:track_002 | B:e05 @ 2.70 |  |
| g10 | -2.95 | CLOSING_START | A | A:track_001 | A:e05 @ 2.80 |  |
| g11 | -2.30 | CUT_IN_FROM_RIGHT_START | A | A:track_001 | A:e06 @ 3.45 |  |
| g12 | -2.10 | CUT_IN_FROM_RIGHT_START | B | B:track_002 | B:e06 @ 3.65 |  |
| g13 | -1.60 | CRITICAL_TTC_START | A | A:track_001 | A:e07 @ 4.15 |  |
| g14 | -1.50 | EGO_PATH_ENTRY | A | A:track_001 | A:e08 @ 4.25 |  |
| g15 | -1.35 | CRITICAL_TTC_START | A | B | A:e09 @ 4.40 |  |
| g16 | -1.05 | CRITICAL_TTC_END | A | A:track_001 | A:e10 @ 4.70 |  |
| g17 | -0.85 | CUT_IN_FROM_RIGHT_END | A | A:track_001 | A:e11 @ 4.90 |  |
| g18 | -0.80 | CRITICAL_TTC_START | B | A | B:e07 @ 4.95 |  |
| g19 | -0.75 | CLOSING_END | A | A:track_001 | A:e12 @ 5.00 |  |
| g20 | -0.75 | CLOSING_START | A | B | A:e13 @ 5.00 |  |
| g21 | -0.65 | CLOSING_END | B | B:track_002 | B:e08 @ 5.10 |  |
| g22 | -0.60 | CLOSING_START | B | A | B:e09 @ 5.15 |  |
| g23 | -0.30 | EGO_PATH_EXIT | A | A:track_001 | A:e14 @ 5.45 |  |
| g24 | -0.10 | CUT_IN_FROM_RIGHT_END | B | B:track_002 | B:e10 @ 5.65 |  |
| g25 | 0.00 | COLLISION | - | A, B | A:e15 @ 5.75, B:e11 @ 5.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 915.98, B 915.98 |
| g26 | 0.00 | CRITICAL_TTC_END | A | B | A:e16 @ 5.75 |  |
| g27 | 0.00 | CRITICAL_TTC_END | B | A | B:e12 @ 5.75 |  |
| g28 | 0.05 | CLOSING_END | A | B | A:e17 @ 5.80 |  |
| g29 | 0.05 | THROTTLE_END | A | - | A:e18 @ 5.80 |  |
| g30 | 0.05 | THROTTLE_END | B | - | B:e13 @ 5.80 |  |
| g31 | 0.05 | BRAKE_START | A | - | A:e19 @ 5.80 |  |
| g32 | 0.05 | BRAKE_START | B | - | B:e14 @ 5.80 |  |
| g33 | 0.10 | CLOSING_END | B | A | B:e15 @ 5.85 |  |
| g34 | 0.95 | MOVING_END | B | - | B:e16 @ 6.70 |  |
| g35 | 0.95 | STOP_START | B | - | B:e17 @ 6.70 |  |
| g36 | 1.10 | MOVING_END | A | - | A:e20 @ 6.85 |  |
| g37 | 1.10 | STOP_START | A | - | A:e21 @ 6.85 |  |
| g38 | 1.40 | TRACK_LOST | B | B:track_002 | B:e18 @ 7.15 |  |
| g39 | 1.90 | TRACK_LOST | A | A:track_001 | A:e22 @ 7.65 |  |

## Edges

```
    g01 --PRECEDES--> g09
    g02 --PRECEDES--> g09
    g03 --PRECEDES--> g09
    g04 --PRECEDES--> g09
    g05 --PRECEDES--> g09
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g25 --PRECEDES--> g32
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g06 --SAME_TRACK--> g10
    g06 --SAME_TRACK--> g11
    g06 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g14
    g05 --SAME_TRACK--> g15
    g06 --SAME_TRACK--> g16
    g06 --SAME_TRACK--> g17
    g06 --SAME_TRACK--> g19
    g05 --SAME_TRACK--> g20
    g06 --SAME_TRACK--> g23
    g05 --SAME_TRACK--> g26
    g05 --SAME_TRACK--> g28
    g06 --SAME_TRACK--> g39
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g12
    g07 --SAME_TRACK--> g18
    g08 --SAME_TRACK--> g21
    g07 --SAME_TRACK--> g22
    g08 --SAME_TRACK--> g24
    g07 --SAME_TRACK--> g27
    g07 --SAME_TRACK--> g33
    g08 --SAME_TRACK--> g38
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,A:track_001); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,B:track_002) |
| -3.05 | CLOSING_START(B,B:track_002) |
| -2.95 | CLOSING_START(A,A:track_001) |
| -2.30 | CUT_IN_FROM_RIGHT_START(A,A:track_001) |
| -2.10 | CUT_IN_FROM_RIGHT_START(B,B:track_002) |
| -1.60 | CRITICAL_TTC_START(A,A:track_001) |
| -1.50 | EGO_PATH_ENTRY(A,A:track_001) |
| -1.35 | CRITICAL_TTC_START(A,B) |
| -1.05 | CRITICAL_TTC_END(A,A:track_001) |
| -0.85 | CUT_IN_FROM_RIGHT_END(A,A:track_001) |
| -0.80 | CRITICAL_TTC_START(B,A) |
| -0.75 | CLOSING_END(A,A:track_001); CLOSING_START(A,B) |
| -0.65 | CLOSING_END(B,B:track_002) |
| -0.60 | CLOSING_START(B,A) |
| -0.30 | EGO_PATH_EXIT(A,A:track_001) |
| -0.10 | CUT_IN_FROM_RIGHT_END(B,B:track_002) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CLOSING_END(B,A) |
| +0.95 | MOVING_END(B); STOP_START(B) |
| +1.10 | MOVING_END(A); STOP_START(A) |
| +1.40 | TRACK_LOST(B,B:track_002) |
| +1.90 | TRACK_LOST(A,A:track_001) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 3.45 < CRITICAL_TTC_START 4.15 (+0.70 s) < COLLISION 5.75 (+1.60 s); EGO_PATH_ENTRY 4.25 after critical TTC (+0.10 s) [local times; t_global: cut_in -2.30, critical_ttc_start -1.60, ego_path_entry -1.50, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 4.40, COLLISION with B 5.75 (+1.35 s) [local times; t_global: critical_ttc_start -1.35, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 4.95, COLLISION with A 5.75 (+0.80 s) [local times; t_global: critical_ttc_start -0.80, collision +0.00]
- B's track_002 (unidentified B:track_002): CUT_IN_FROM_RIGHT_START 3.65, no critical TTC after it [local times; t_global: cut_in -2.10, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e04) | ego: not yet observed |
| -5.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e04) | ego: not yet observed |
| -3.05 | B | g09 CLOSING_START(B,B:track_002) (B:e05) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state |
| -2.95 | A | g10 CLOSING_START(A,A:track_001) (A:e05) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state |
| -2.30 | A | g11 CUT_IN_FROM_RIGHT_START(A,A:track_001) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state |
| -2.10 | B | g12 CUT_IN_FROM_RIGHT_START(B,B:track_002) (B:e06) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING |
| -1.60 | A | g13 CRITICAL_TTC_START(A,A:track_001) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.50 | A | g14 EGO_PATH_ENTRY(A,A:track_001) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.35 | A | g15 CRITICAL_TTC_START(A,B) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.05 | A | g16 CRITICAL_TTC_END(A,A:track_001) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CRITICAL_TTC |
| -0.85 | A | g17 CUT_IN_FROM_RIGHT_END(A,A:track_001) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CRITICAL_TTC |
| -0.80 | B | g18 CRITICAL_TTC_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| -0.75 | A | g19 CLOSING_END(A,A:track_001) (A:e12)<br>g20 CLOSING_START(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CRITICAL_TTC |
| -0.65 | B | g21 CLOSING_END(B,B:track_002) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| -0.60 | B | g22 CLOSING_START(B,A) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CUT_IN_FROM_RIGHT |
| -0.30 | A | g23 EGO_PATH_EXIT(A,A:track_001) (A:e14) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC |
| -0.10 | B | g24 CUT_IN_FROM_RIGHT_END(B,B:track_002) (B:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CUT_IN_FROM_RIGHT |
| +0.00 | A | g25 COLLISION(A,B) (A:e15)<br>g26 CRITICAL_TTC_END(A,B) (A:e16) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | B | g25 COLLISION(A,B) (B:e11)<br>g27 CRITICAL_TTC_END(B,A) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state |
| +0.05 | A | g28 CLOSING_END(A,B) (A:e17)<br>g29 THROTTLE_END(A) (A:e18)<br>g31 BRAKE_START(A) (A:e19) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING |
| +0.05 | B | g30 THROTTLE_END(B) (B:e13)<br>g32 BRAKE_START(B) (B:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state |
| +0.10 | B | g33 CLOSING_END(B,A) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state |
| +0.95 | B | g34 MOVING_END(B) (B:e16)<br>g35 STOP_START(B) (B:e17) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.10 | A | g36 MOVING_END(A) (A:e20)<br>g37 STOP_START(A) (A:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.40 | B | g38 TRACK_LOST(B,B:track_002) (B:e18) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.90 | A | g39 TRACK_LOST(A,A:track_001) (A:e22) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |

## Plain-language reading

- 5.75 s before the reference collision, A started moving (already the case when first observed).
- 5.75 s before the reference collision, B started moving (already the case when first observed).
- 5.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 5.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 5.75 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 5.75 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its right.
- 5.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 5.75 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 3.05 s before the reference collision, B observed unidentified object B:track_002 start closing in.
- 2.95 s before the reference collision, A observed unidentified object A:track_001 start closing in.
- 2.30 s before the reference collision, A observed unidentified object A:track_001 cutting in from the right.
- 2.10 s before the reference collision, B observed unidentified object B:track_002 cutting in from the right.
- 1.60 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.50 s before the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 1.35 s before the reference collision, A's time-to-contact with B became critical.
- 1.05 s before the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.85 s before the reference collision, A observed unidentified object A:track_001's cut-in from the right settle.
- 0.80 s before the reference collision, B's time-to-contact with A became critical.
- 0.75 s before the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.75 s before the reference collision, A observed B start closing in.
- 0.65 s before the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.60 s before the reference collision, B observed A start closing in.
- 0.30 s before the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.10 s before the reference collision, B observed unidentified object B:track_002's cut-in from the right settle.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 916, B: 916 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B observed A stop closing in.
- 0.95 s after the reference collision, B stopped moving.
- 0.95 s after the reference collision, B came to a stop.
- 1.10 s after the reference collision, A stopped moving.
- 1.10 s after the reference collision, A came to a stop.
- 1.40 s after the reference collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 1.90 s after the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
