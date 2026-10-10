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
| A | ALIGNED | A:e13 | 4.95 | -4.95 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.95 | -4.95 | reported the reference collision collision_001 |

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
| g11 | -2.35 | CRITICAL_TTC_START | A | A:track_001 | A:e06 @ 2.60 |  |
| g12 | -2.20 | CUT_IN_FROM_RIGHT_START | A | A:track_001 | A:e07 @ 2.75 |  |
| g13 | -1.60 | EGO_PATH_ENTRY | A | A:track_001 | A:e08 @ 3.35 |  |
| g14 | -1.15 | CRITICAL_TTC_START | A | B | A:e09 @ 3.80 |  |
| g15 | -0.85 | CUT_IN_FROM_RIGHT_END | A | A:track_001 | A:e10 @ 4.10 |  |
| g16 | -0.80 | CRITICAL_TTC_START | B | A | B:e06 @ 4.15 |  |
| g17 | -0.75 | CLOSING_START | A | B | A:e11 @ 4.20 |  |
| g18 | -0.70 | CLOSING_START | B | A | B:e07 @ 4.25 |  |
| g19 | -0.40 | CLOSING_END | A | A:track_001 | A:e12 @ 4.55 |  |
| g20 | 0.00 | COLLISION | - | A, B | A:e13 @ 4.95, B:e08 @ 4.95 | matched_event=collision_001; reference_event=True; peak_impulse=A 1576.92, B 1576.92 |
| g21 | 0.00 | CLOSING_END | A | B | A:e14 @ 4.95 |  |
| g22 | 0.00 | CLOSING_END | B | A | B:e09 @ 4.95 |  |
| g23 | 0.05 | THROTTLE_END | A | - | A:e15 @ 5.00 |  |
| g24 | 0.05 | THROTTLE_END | B | - | B:e10 @ 5.00 |  |
| g25 | 0.05 | BRAKE_START | A | - | A:e16 @ 5.00 |  |
| g26 | 0.05 | BRAKE_START | B | - | B:e11 @ 5.00 |  |
| g27 | 0.20 | CLOSING_END | B | B:track_002 | B:e12 @ 5.15 |  |
| g28 | 0.25 | EGO_PATH_EXIT | A | A:track_001 | A:e17 @ 5.20 |  |
| g29 | 0.55 | CRITICAL_TTC_END | A | A:track_001 | A:e18 @ 5.50 |  |
| g30 | 0.75 | TRACK_LOST | B | B:track_002 | B:e13 @ 5.70 |  |
| g31 | 1.00 | CRITICAL_TTC_END | A | B | A:e19 @ 5.95 |  |
| g32 | 1.00 | MOVING_END | B | - | B:e14 @ 5.95 |  |
| g33 | 1.00 | STOP_START | B | - | B:e15 @ 5.95 |  |
| g34 | 1.10 | MOVING_END | A | - | A:e20 @ 6.05 |  |
| g35 | 1.10 | STOP_START | A | - | A:e21 @ 6.05 |  |
| g36 | 1.30 | CRITICAL_TTC_END | B | A | B:e16 @ 6.25 |  |
| g37 | 1.30 | EGO_PATH_ENTRY | B | A | B:e17 @ 6.25 |  |
| g38 | 1.45 | TRACK_APPEARED_RIGHT | B | B:track_003 | B:e18 @ 6.40 |  |
| g39 | 2.05 | TRACK_LOST | B | B:track_003 | B:e19 @ 7.00 |  |
| g40 | 2.50 | TRACK_LOST | A | A:track_001 | A:e22 @ 7.45 |  |

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
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g06 --SAME_TRACK--> g09
    g06 --SAME_TRACK--> g11
    g06 --SAME_TRACK--> g12
    g06 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g14
    g06 --SAME_TRACK--> g15
    g05 --SAME_TRACK--> g17
    g06 --SAME_TRACK--> g19
    g05 --SAME_TRACK--> g21
    g06 --SAME_TRACK--> g28
    g06 --SAME_TRACK--> g29
    g05 --SAME_TRACK--> g31
    g06 --SAME_TRACK--> g40
    g08 --SAME_TRACK--> g10
    g07 --SAME_TRACK--> g16
    g07 --SAME_TRACK--> g18
    g07 --SAME_TRACK--> g22
    g08 --SAME_TRACK--> g27
    g08 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g36
    g07 --SAME_TRACK--> g37
    g38 --SAME_TRACK--> g39
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.95 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,A:track_001); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(A,A:track_001); CLOSING_START(B,B:track_002) |
| -2.35 | CRITICAL_TTC_START(A,A:track_001) |
| -2.20 | CUT_IN_FROM_RIGHT_START(A,A:track_001) |
| -1.60 | EGO_PATH_ENTRY(A,A:track_001) |
| -1.15 | CRITICAL_TTC_START(A,B) |
| -0.85 | CUT_IN_FROM_RIGHT_END(A,A:track_001) |
| -0.80 | CRITICAL_TTC_START(B,A) |
| -0.75 | CLOSING_START(A,B) |
| -0.70 | CLOSING_START(B,A) |
| -0.40 | CLOSING_END(A,A:track_001) |
| +0.00 | COLLISION(A,B); CLOSING_END(A,B); CLOSING_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.20 | CLOSING_END(B,B:track_002) |
| +0.25 | EGO_PATH_EXIT(A,A:track_001) |
| +0.55 | CRITICAL_TTC_END(A,A:track_001) |
| +0.75 | TRACK_LOST(B,B:track_002) |
| +1.00 | CRITICAL_TTC_END(A,B); MOVING_END(B); STOP_START(B) |
| +1.10 | MOVING_END(A); STOP_START(A) |
| +1.30 | CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(B,A) |
| +1.45 | TRACK_APPEARED_RIGHT(B,B:track_003) |
| +2.05 | TRACK_LOST(B,B:track_003) |
| +2.50 | TRACK_LOST(A,A:track_001) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): critical TTC already active before the cut-in: CRITICAL_TTC_START 2.60 <= CUT_IN_FROM_RIGHT_START 2.75 (+0.15 s); EGO_PATH_ENTRY 3.35 after critical TTC (+0.75 s) [local times; t_global: cut_in -2.20, critical_ttc_start -2.35, ego_path_entry -1.60, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 3.80, COLLISION with B 4.95 (+1.15 s) [local times; t_global: critical_ttc_start -1.15, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 4.15, COLLISION with A 4.95 (+0.80 s); EGO_PATH_ENTRY 6.25 after critical TTC (+2.10 s) [local times; t_global: critical_ttc_start -0.80, ego_path_entry +1.30, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.95 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e04)<br>g09 CLOSING_START(A,A:track_001) (A:e05) | ego: not yet observed |
| -4.95 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e04)<br>g10 CLOSING_START(B,B:track_002) (B:e05) | ego: not yet observed |
| -2.35 | A | g11 CRITICAL_TTC_START(A,A:track_001) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state |
| -2.20 | A | g12 CUT_IN_FROM_RIGHT_START(A,A:track_001) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state |
| -1.60 | A | g13 EGO_PATH_ENTRY(A,A:track_001) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.15 | A | g14 CRITICAL_TTC_START(A,B) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -0.85 | A | g15 CUT_IN_FROM_RIGHT_END(A,A:track_001) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CRITICAL_TTC |
| -0.80 | B | g16 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING |
| -0.75 | A | g17 CLOSING_START(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC |
| -0.70 | B | g18 CLOSING_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING |
| -0.40 | A | g19 CLOSING_END(A,A:track_001) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | A | g20 COLLISION(A,B) (A:e13)<br>g21 CLOSING_END(A,B) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | B | g20 COLLISION(A,B) (B:e08)<br>g22 CLOSING_END(B,A) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| +0.05 | A | g23 THROTTLE_END(A) (A:e15)<br>g25 BRAKE_START(A) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC |
| +0.05 | B | g24 THROTTLE_END(B) (B:e10)<br>g26 BRAKE_START(B) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING |
| +0.20 | B | g27 CLOSING_END(B,B:track_002) (B:e12) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING |
| +0.25 | A | g28 EGO_PATH_EXIT(A,A:track_001) (A:e17) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC |
| +0.55 | A | g29 CRITICAL_TTC_END(A,A:track_001) (A:e18) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_002: CRITICAL_TTC |
| +0.75 | B | g30 TRACK_LOST(B,B:track_002) (B:e13) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_002: no active state |
| +1.00 | A | g31 CRITICAL_TTC_END(A,B) (A:e19) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CRITICAL_TTC |
| +1.00 | B | g32 MOVING_END(B) (B:e14)<br>g33 STOP_START(B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +1.10 | A | g34 MOVING_END(A) (A:e20)<br>g35 STOP_START(A) (A:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.30 | B | g36 CRITICAL_TTC_END(B,A) (B:e16)<br>g37 EGO_PATH_ENTRY(B,A) (B:e17) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +1.45 | B | g38 TRACK_APPEARED_RIGHT(B,B:track_003) (B:e18) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +2.05 | B | g39 TRACK_LOST(B,B:track_003) (B:e19) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_003: no active state<br>track lost, states UNKNOWN: track_002 |
| +2.50 | A | g40 TRACK_LOST(A,A:track_001) (A:e22) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |

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
- 2.35 s before the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 2.20 s before the reference collision, A observed unidentified object A:track_001 cutting in from the right.
- 1.60 s before the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 1.15 s before the reference collision, A's time-to-contact with B became critical.
- 0.85 s before the reference collision, A observed unidentified object A:track_001's cut-in from the right settle.
- 0.80 s before the reference collision, B's time-to-contact with A became critical.
- 0.75 s before the reference collision, A observed B start closing in.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.40 s before the reference collision, A observed unidentified object A:track_001 stop closing in.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1577, B: 1577 N*s).
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.25 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.55 s after the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.75 s after the reference collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the reference collision, A's time-to-contact with B stopped being critical.
- 1.00 s after the reference collision, B stopped moving.
- 1.00 s after the reference collision, B came to a stop.
- 1.10 s after the reference collision, A stopped moving.
- 1.10 s after the reference collision, A came to a stop.
- 1.30 s after the reference collision, B's time-to-contact with A stopped being critical.
- 1.30 s after the reference collision, B observed A enter its forward path corridor.
- 1.45 s after the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 2.05 s after the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 2.50 s after the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
