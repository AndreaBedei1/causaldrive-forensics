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
| B:track_003 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e14 | 4.95 | -4.95 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 4.95 | -4.95 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1576.92 vs 1576.92 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.9 m -> 1.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.90 m/s over 3.0 s (> 1.50)<br>clearance at the contact 1.03 m |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.28 m/s over 3.0 s<br>clearance at the contact 0.10 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.93 | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.2 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.55 m/s over 3.0 s<br>clearance at the contact 0.23 m<br>the only compatible track of B touching it at the contact (clearance 0.23 m; track_002 at 4.94 m) |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 6.8 m -> 4.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.23 m/s over 3.0 s<br>clearance at the contact 4.94 m (beyond 3.50 m: confidence factor 0.89)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_001, track_002) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.95 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.95 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.95 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -4.95 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -4.95 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 |  |
| g06 | -4.95 | TRACK_APPEARED_RIGHT | A | A:track_001 | A:e04 @ 0.00 |  |
| g07 | -4.95 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 |  |
| g08 | -4.95 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e04 @ 0.00 |  |
| g09 | -4.95 | CLOSING_START | A | A:track_001 | A:e05 @ 0.00 | active_at_first_observation=True |
| g10 | -4.95 | CLOSING_START | B | B:track_002 | B:e05 @ 0.00 | active_at_first_observation=True |
| g11 | -2.20 | CUT_IN_FROM_RIGHT_START | A | A:track_001 | A:e06 @ 2.75 |  |
| g12 | -2.10 | CUT_IN_FROM_RIGHT_START | B | B:track_002 | B:e06 @ 2.85 |  |
| g13 | -1.60 | EGO_PATH_ENTRY | A | A:track_001 | A:e07 @ 3.35 |  |
| g14 | -1.35 | CRITICAL_TTC_START | A | A:track_001 | A:e08 @ 3.60 |  |
| g15 | -1.15 | CRITICAL_TTC_START | A | B | A:e09 @ 3.80 |  |
| g16 | -0.85 | CUT_IN_FROM_RIGHT_END | A | A:track_001 | A:e10 @ 4.10 |  |
| g17 | -0.80 | CRITICAL_TTC_START | B | A | B:e07 @ 4.15 |  |
| g18 | -0.75 | CLOSING_START | A | B | A:e11 @ 4.20 |  |
| g19 | -0.70 | CLOSING_START | B | A | B:e08 @ 4.25 |  |
| g20 | -0.40 | CRITICAL_TTC_END | A | A:track_001 | A:e12 @ 4.55 |  |
| g21 | -0.40 | CLOSING_END | A | A:track_001 | A:e13 @ 4.55 |  |
| g22 | -0.05 | CRITICAL_TTC_END | B | A | B:e09 @ 4.90 |  |
| g23 | 0.00 | COLLISION | - | A, B | A:e14 @ 4.95, B:e10 @ 4.95 | matched_event=collision_001; reference_event=True; peak_impulse=A 1576.92, B 1576.92 |
| g24 | 0.00 | CRITICAL_TTC_END | A | B | A:e15 @ 4.95 |  |
| g25 | 0.00 | CLOSING_END | A | B | A:e16 @ 4.95 |  |
| g26 | 0.00 | CLOSING_END | B | A | B:e11 @ 4.95 |  |
| g27 | 0.05 | THROTTLE_END | A | - | A:e17 @ 5.00 |  |
| g28 | 0.05 | THROTTLE_END | B | - | B:e12 @ 5.00 |  |
| g29 | 0.05 | BRAKE_START | A | - | A:e18 @ 5.00 |  |
| g30 | 0.05 | BRAKE_START | B | - | B:e13 @ 5.00 |  |
| g31 | 0.20 | CLOSING_END | B | B:track_002 | B:e14 @ 5.15 |  |
| g32 | 0.25 | EGO_PATH_EXIT | A | A:track_001 | A:e19 @ 5.20 |  |
| g33 | 0.30 | CUT_IN_FROM_RIGHT_END | B | B:track_002 | B:e15 @ 5.25 |  |
| g34 | 0.75 | TRACK_LOST | B | B:track_002 | B:e16 @ 5.70 |  |
| g35 | 1.00 | MOVING_END | B | - | B:e17 @ 5.95 |  |
| g36 | 1.00 | STOP_START | B | - | B:e18 @ 5.95 |  |
| g37 | 1.10 | MOVING_END | A | - | A:e20 @ 6.05 |  |
| g38 | 1.10 | STOP_START | A | - | A:e21 @ 6.05 |  |
| g39 | 1.30 | EGO_PATH_ENTRY | B | A | B:e19 @ 6.25 |  |
| g40 | 1.45 | TRACK_APPEARED_RIGHT | B | B:track_003 | B:e20 @ 6.40 |  |
| g41 | 2.05 | TRACK_LOST | B | B:track_003 | B:e21 @ 7.00 |  |
| g42 | 2.50 | TRACK_LOST | A | A:track_001 | A:e22 @ 7.45 |  |

## Edges

```
    g01 --PRECEDES--> g11
    g02 --PRECEDES--> g11
    g03 --PRECEDES--> g11
    g04 --PRECEDES--> g11
    g05 --PRECEDES--> g11
    g06 --PRECEDES--> g11
    g07 --PRECEDES--> g11
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g06 --SAME_TRACK--> g09
    g06 --SAME_TRACK--> g11
    g06 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g14
    g05 --SAME_TRACK--> g15
    g06 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g18
    g06 --SAME_TRACK--> g20
    g06 --SAME_TRACK--> g21
    g05 --SAME_TRACK--> g24
    g05 --SAME_TRACK--> g25
    g06 --SAME_TRACK--> g32
    g06 --SAME_TRACK--> g42
    g08 --SAME_TRACK--> g10
    g08 --SAME_TRACK--> g12
    g07 --SAME_TRACK--> g17
    g07 --SAME_TRACK--> g19
    g07 --SAME_TRACK--> g22
    g07 --SAME_TRACK--> g26
    g08 --SAME_TRACK--> g31
    g08 --SAME_TRACK--> g33
    g08 --SAME_TRACK--> g34
    g07 --SAME_TRACK--> g39
    g40 --SAME_TRACK--> g41
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.95 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,A:track_001); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(A,A:track_001); CLOSING_START(B,B:track_002) |
| -2.20 | CUT_IN_FROM_RIGHT_START(A,A:track_001) |
| -2.10 | CUT_IN_FROM_RIGHT_START(B,B:track_002) |
| -1.60 | EGO_PATH_ENTRY(A,A:track_001) |
| -1.35 | CRITICAL_TTC_START(A,A:track_001) |
| -1.15 | CRITICAL_TTC_START(A,B) |
| -0.85 | CUT_IN_FROM_RIGHT_END(A,A:track_001) |
| -0.80 | CRITICAL_TTC_START(B,A) |
| -0.75 | CLOSING_START(A,B) |
| -0.70 | CLOSING_START(B,A) |
| -0.40 | CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001) |
| -0.05 | CRITICAL_TTC_END(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.20 | CLOSING_END(B,B:track_002) |
| +0.25 | EGO_PATH_EXIT(A,A:track_001) |
| +0.30 | CUT_IN_FROM_RIGHT_END(B,B:track_002) |
| +0.75 | TRACK_LOST(B,B:track_002) |
| +1.00 | MOVING_END(B); STOP_START(B) |
| +1.10 | MOVING_END(A); STOP_START(A) |
| +1.30 | EGO_PATH_ENTRY(B,A) |
| +1.45 | TRACK_APPEARED_RIGHT(B,B:track_003) |
| +2.05 | TRACK_LOST(B,B:track_003) |
| +2.50 | TRACK_LOST(A,A:track_001) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 2.75 < CRITICAL_TTC_START 3.60 (+0.85 s) < COLLISION 4.95 (+1.35 s); EGO_PATH_ENTRY 3.35 before critical TTC (-0.25 s) [local times; t_global: cut_in -2.20, critical_ttc_start -1.35, ego_path_entry -1.60, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 3.80, COLLISION with B 4.95 (+1.15 s) [local times; t_global: critical_ttc_start -1.15, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 4.15, COLLISION with A 4.95 (+0.80 s); EGO_PATH_ENTRY 6.25 after critical TTC (+2.10 s) [local times; t_global: critical_ttc_start -0.80, ego_path_entry +1.30, collision +0.00]
- B's track_002 (unidentified B:track_002): CUT_IN_FROM_RIGHT_START 2.85, no critical TTC after it [local times; t_global: cut_in -2.10, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.95 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e04)<br>g09 CLOSING_START(A,A:track_001) (A:e05) | ego: not yet observed |
| -4.95 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e04)<br>g10 CLOSING_START(B,B:track_002) (B:e05) | ego: not yet observed |
| -2.20 | A | g11 CUT_IN_FROM_RIGHT_START(A,A:track_001) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state |
| -2.10 | B | g12 CUT_IN_FROM_RIGHT_START(B,B:track_002) (B:e06) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING |
| -1.60 | A | g13 EGO_PATH_ENTRY(A,A:track_001) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.35 | A | g14 CRITICAL_TTC_START(A,A:track_001) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.15 | A | g15 CRITICAL_TTC_START(A,B) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -0.85 | A | g16 CUT_IN_FROM_RIGHT_END(A,A:track_001) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CRITICAL_TTC |
| -0.80 | B | g17 CRITICAL_TTC_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| -0.75 | A | g18 CLOSING_START(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC |
| -0.70 | B | g19 CLOSING_START(B,A) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| -0.40 | A | g20 CRITICAL_TTC_END(A,A:track_001) (A:e12)<br>g21 CLOSING_END(A,A:track_001) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC |
| -0.05 | B | g22 CRITICAL_TTC_END(B,A) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| +0.00 | A | g23 COLLISION(A,B) (A:e14)<br>g24 CRITICAL_TTC_END(A,B) (A:e15)<br>g25 CLOSING_END(A,B) (A:e16) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | B | g23 COLLISION(A,B) (B:e10)<br>g26 CLOSING_END(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| +0.05 | A | g27 THROTTLE_END(A) (A:e17)<br>g29 BRAKE_START(A) (A:e18) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| +0.05 | B | g28 THROTTLE_END(B) (B:e12)<br>g30 BRAKE_START(B) (B:e13) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| +0.20 | B | g31 CLOSING_END(B,B:track_002) (B:e14) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING, CUT_IN_FROM_RIGHT |
| +0.25 | A | g32 EGO_PATH_EXIT(A,A:track_001) (A:e19) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| +0.30 | B | g33 CUT_IN_FROM_RIGHT_END(B,B:track_002) (B:e15) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CUT_IN_FROM_RIGHT |
| +0.75 | B | g34 TRACK_LOST(B,B:track_002) (B:e16) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.00 | B | g35 MOVING_END(B) (B:e17)<br>g36 STOP_START(B) (B:e18) | ego: MOVING, BRAKE<br>track_001: no active state<br>track lost, states UNKNOWN: track_002 |
| +1.10 | A | g37 MOVING_END(A) (A:e20)<br>g38 STOP_START(A) (A:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.30 | B | g39 EGO_PATH_ENTRY(B,A) (B:e19) | ego: STOP, BRAKE<br>track_001: no active state<br>track lost, states UNKNOWN: track_002 |
| +1.45 | B | g40 TRACK_APPEARED_RIGHT(B,B:track_003) (B:e20) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +2.05 | B | g41 TRACK_LOST(B,B:track_003) (B:e21) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_003: no active state<br>track lost, states UNKNOWN: track_002 |
| +2.50 | A | g42 TRACK_LOST(A,A:track_001) (A:e22) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |

## Plain-language reading

- 4.95 s before the reference collision, A started moving (already the case when first observed).
- 4.95 s before the reference collision, B started moving (already the case when first observed).
- 4.95 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.95 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.95 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 4.95 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its right.
- 4.95 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.95 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 4.95 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 4.95 s before the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 2.20 s before the reference collision, A observed unidentified object A:track_001 cutting in from the right.
- 2.10 s before the reference collision, B observed unidentified object B:track_002 cutting in from the right.
- 1.60 s before the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 1.35 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.15 s before the reference collision, A's time-to-contact with B became critical.
- 0.85 s before the reference collision, A observed unidentified object A:track_001's cut-in from the right settle.
- 0.80 s before the reference collision, B's time-to-contact with A became critical.
- 0.75 s before the reference collision, A observed B start closing in.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.40 s before the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.40 s before the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.05 s before the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1577, B: 1577 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.25 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.30 s after the reference collision, B observed unidentified object B:track_002's cut-in from the right settle.
- 0.75 s after the reference collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the reference collision, B stopped moving.
- 1.00 s after the reference collision, B came to a stop.
- 1.10 s after the reference collision, A stopped moving.
- 1.10 s after the reference collision, A came to a stop.
- 1.30 s after the reference collision, B observed A enter its forward path corridor.
- 1.45 s after the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 2.05 s after the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 2.50 s after the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
