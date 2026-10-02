# Global graph - S06/run_0_b_rear_first

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: C:track_002 |
| C | recorder | clock ALIGNED; observed by others as: B:track_001 |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| C:track_001 | anonymous_track | seen only by C; candidate: B |
| C:track_003 | anonymous_track | seen only by C; candidate: B |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 6.00 | -6.00 | reported the reference collision collision_001 |
| B | ALIGNED | B:e18 | 6.00 | -6.00 | reported the reference collision collision_001 |
| C | ALIGNED | C:e16 | 4.60 | -6.00 | shares collision_002 with B, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31488.29 vs 31488.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: B and C both recorded a collision; peak impulses 21812.15 vs 21812.15 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 6.00 s before the matched collision<br>lost 1.45 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 19.0 m -> 19.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.06 m/s over 1.5 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 4.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 17.9 m -> 4.8 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.65 m/s over 3.0 s (> 1.50)<br>clearance at the contact 4.75 m (beyond 3.50 m: confidence factor 0.92) |
| B:track_001 | C | ASSOCIATED | 1.00 | B and C both reported collision_002 at 4.60 s (peak impulse 21812.15 vs 21812.15 N*s)<br>tracked for 4.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.5 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.14 m/s over 3.0 s<br>clearance at the contact 0.15 m<br>the only track of B compatible with the contact<br>collision_001 with A at 6.00 s: not compatible (not approaching before the contact: clearance 0.4 m -> 0.4 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 11.18 m/s over 3.0 s (> 1.50)) |
| B:track_002 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 at 6.00 s (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 6.00 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.4 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 3.0 s<br>clearance at the contact 0.63 m<br>the only track of B compatible with the contact<br>collision_002 with C at 4.60 s: not compatible (not approaching before the contact: clearance 19.5 m -> 19.8 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 7.02 m/s over 3.0 s (> 1.50)) |
| C:track_001 | C:track_001 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 21812.15 vs 21812.15 N*s)<br>tracked for 4.60 s before the matched collision<br>lost 1.65 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 34.9 m -> 36.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.52 m/s over 1.4 s |
| C:track_002 | B | ASSOCIATED | 0.99 | C and B both reported collision_002 (peak impulse 21812.15 vs 21812.15 N*s)<br>tracked for 4.60 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.4 m -> 1.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.24 m/s over 3.0 s<br>clearance at the contact 1.25 m<br>the only track of C compatible with the contact |
| C:track_003 | C:track_003 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 21812.15 vs 21812.15 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.60 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.00 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.00 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.00 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -6.00 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.00 |  |
| g05 | -6.00 | TRACK_APPEARED_FRONT | B | C | B:e02 @ 0.00 |  |
| g06 | -6.00 | TRACK_APPEARED_REAR | B | A | B:e03 @ 0.00 |  |
| g07 | -6.00 | TRACK_APPEARED_REAR | C | B | C:e03 @ 0.00 |  |
| g08 | -6.00 | TRACK_APPEARED_REAR | C | C:track_001 | C:e02 @ 0.00 |  |
| g09 | -5.55 | CLOSING_START | A | A:track_001 | A:e03 @ 0.45 |  |
| g10 | -5.50 | CLOSING_START | B | A | B:e04 @ 0.50 |  |
| g11 | -5.20 | CLOSING_START | C | C:track_001 | C:e04 @ 0.80 |  |
| g12 | -4.95 | CLOSING_START | C | B | C:e05 @ 1.05 |  |
| g13 | -4.90 | CLOSING_START | B | C | B:e05 @ 1.10 |  |
| g14 | -4.85 | TRACK_APPEARED_FRONT | A | A:track_002 | A:e04 @ 1.15 |  |
| g15 | -4.85 | CLOSING_START | A | A:track_002 | A:e05 @ 1.15 | active_at_first_observation=True |
| g16 | -4.35 | CLOSING_END | A | A:track_001 | A:e06 @ 1.65 |  |
| g17 | -4.35 | CLOSING_END | B | A | B:e06 @ 1.65 |  |
| g18 | -4.00 | CLOSING_END | A | A:track_002 | A:e07 @ 2.00 |  |
| g19 | -4.00 | CLOSING_END | C | C:track_001 | C:e06 @ 2.00 |  |
| g20 | -3.95 | CLOSING_END | C | B | C:e07 @ 2.05 |  |
| g21 | -3.90 | CLOSING_END | B | C | B:e07 @ 2.10 |  |
| g22 | -3.60 | SPEED_LIMIT_EXCEEDED_START | C | - | C:e08 @ 2.40 |  |
| g23 | -3.05 | BRAKE_START | C | - | C:e09 @ 2.95 |  |
| g24 | -3.05 | TRACK_LOST | C | C:track_001 | C:e10 @ 2.95 |  |
| g25 | -2.95 | SPEED_LIMIT_EXCEEDED_END | C | - | C:e11 @ 3.05 |  |
| g26 | -2.80 | CLOSING_START | B | C | B:e08 @ 3.20 |  |
| g27 | -2.75 | CLOSING_START | A | A:track_002 | A:e08 @ 3.25 |  |
| g28 | -2.75 | CLOSING_START | C | B | C:e12 @ 3.25 |  |
| g29 | -2.25 | CRITICAL_TTC_START | B | C | B:e09 @ 3.75 |  |
| g30 | -1.95 | MOVING_END | C | - | C:e13 @ 4.05 |  |
| g31 | -1.95 | STOP_START | C | - | C:e14 @ 4.05 |  |
| g32 | -1.85 | CRITICAL_TTC_START | A | A:track_002 | A:e09 @ 4.15 |  |
| g33 | -1.45 | TRACK_LOST | A | A:track_001 | A:e10 @ 4.55 |  |
| g34 | -1.45 | TRACK_LOST | C | B | C:e15 @ 4.55 |  |
| g35 | -1.40 | COLLISION | - | B, C | B:e10 @ 4.60, C:e16 @ 4.60 | matched_event=collision_002; reference_event=False; peak_impulse=B 21812.15, C 21812.15 |
| g36 | -1.40 | CRITICAL_TTC_END | B | C | B:e11 @ 4.60 |  |
| g37 | -1.40 | CLOSING_END | B | C | B:e12 @ 4.60 |  |
| g38 | -1.40 | CLOSING_START | B | A | B:e13 @ 4.60 |  |
| g39 | -1.35 | BRAKE_START | B | - | B:e14 @ 4.65 |  |
| g40 | -1.25 | MOVING_END | B | - | B:e15 @ 4.75 |  |
| g41 | -1.25 | STOP_START | B | - | B:e16 @ 4.75 |  |
| g42 | -0.80 | TRACK_APPEARED_REAR | C | C:track_003 | C:e17 @ 5.20 |  |
| g43 | -0.80 | CLOSING_START | C | C:track_003 | C:e18 @ 5.20 | active_at_first_observation=True |
| g44 | -0.05 | TRACK_LOST | B | A | B:e17 @ 5.95 |  |
| g45 | -0.05 | TRACK_LOST | C | C:track_003 | C:e19 @ 5.95 |  |
| g46 | 0.00 | COLLISION | - | A, B | A:e11 @ 6.00, B:e18 @ 6.00 | matched_event=collision_001; reference_event=True; peak_impulse=A 31488.29, B 31488.29 |
| g47 | 0.00 | CRITICAL_TTC_END | A | A:track_002 | A:e12 @ 6.00 |  |
| g48 | 0.00 | CLOSING_END | A | A:track_002 | A:e13 @ 6.00 |  |
| g49 | 0.05 | BRAKE_START | A | - | A:e14 @ 6.05 |  |
| g50 | 0.20 | MOVING_END | A | - | A:e15 @ 6.20 |  |
| g51 | 0.20 | STOP_START | A | - | A:e16 @ 6.20 |  |

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
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g36 --PRECEDES--> g39
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g04 --SAME_TRACK--> g09
    g14 --SAME_TRACK--> g15
    g04 --SAME_TRACK--> g16
    g14 --SAME_TRACK--> g18
    g14 --SAME_TRACK--> g27
    g14 --SAME_TRACK--> g32
    g04 --SAME_TRACK--> g33
    g14 --SAME_TRACK--> g47
    g14 --SAME_TRACK--> g48
    g06 --SAME_TRACK--> g10
    g05 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g17
    g05 --SAME_TRACK--> g21
    g05 --SAME_TRACK--> g26
    g05 --SAME_TRACK--> g29
    g05 --SAME_TRACK--> g36
    g05 --SAME_TRACK--> g37
    g06 --SAME_TRACK--> g38
    g06 --SAME_TRACK--> g44
    g08 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g12
    g08 --SAME_TRACK--> g19
    g07 --SAME_TRACK--> g20
    g08 --SAME_TRACK--> g24
    g07 --SAME_TRACK--> g28
    g07 --SAME_TRACK--> g34
    g42 --SAME_TRACK--> g43
    g42 --SAME_TRACK--> g45
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.00 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(A,A:track_001); TRACK_APPEARED_FRONT(B,C); TRACK_APPEARED_REAR(B,A); TRACK_APPEARED_REAR(C,B); TRACK_APPEARED_REAR(C,C:track_001) |
| -5.55 | CLOSING_START(A,A:track_001) |
| -5.50 | CLOSING_START(B,A) |
| -5.20 | CLOSING_START(C,C:track_001) |
| -4.95 | CLOSING_START(C,B) |
| -4.90 | CLOSING_START(B,C) |
| -4.85 | TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002) |
| -4.35 | CLOSING_END(A,A:track_001); CLOSING_END(B,A) |
| -4.00 | CLOSING_END(A,A:track_002); CLOSING_END(C,C:track_001) |
| -3.95 | CLOSING_END(C,B) |
| -3.90 | CLOSING_END(B,C) |
| -3.60 | SPEED_LIMIT_EXCEEDED_START(C) |
| -3.05 | BRAKE_START(C); TRACK_LOST(C,C:track_001) |
| -2.95 | SPEED_LIMIT_EXCEEDED_END(C) |
| -2.80 | CLOSING_START(B,C) |
| -2.75 | CLOSING_START(A,A:track_002); CLOSING_START(C,B) |
| -2.25 | CRITICAL_TTC_START(B,C) |
| -1.95 | MOVING_END(C); STOP_START(C) |
| -1.85 | CRITICAL_TTC_START(A,A:track_002) |
| -1.45 | TRACK_LOST(A,A:track_001); TRACK_LOST(C,B) |
| -1.40 | COLLISION(B,C); CRITICAL_TTC_END(B,C); CLOSING_END(B,C); CLOSING_START(B,A) |
| -1.35 | BRAKE_START(B) |
| -1.25 | MOVING_END(B); STOP_START(B) |
| -0.80 | TRACK_APPEARED_REAR(C,C:track_003); CLOSING_START(C,C:track_003) |
| -0.05 | TRACK_LOST(B,A); TRACK_LOST(C,C:track_003) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,A:track_002); CLOSING_END(A,A:track_002) |
| +0.05 | BRAKE_START(A) |
| +0.20 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (unidentified A:track_002): CRITICAL_TTC_START 4.15, COLLISION 6.00 (+1.85 s) [local times; t_global: critical_ttc_start -1.85, collision +0.00]
- B's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 4.60 (+0.85 s) [local times; t_global: critical_ttc_start -2.25, collision -1.40]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.00 | A | g01 MOVING_START(A) (A:e01)<br>g04 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02) | ego: not yet observed |
| -6.00 | B | g02 MOVING_START(B) (B:e01)<br>g05 TRACK_APPEARED_FRONT(B,C) (B:e02)<br>g06 TRACK_APPEARED_REAR(B,A) (B:e03) | ego: not yet observed |
| -6.00 | C | g03 MOVING_START(C) (C:e01)<br>g07 TRACK_APPEARED_REAR(C,B) (C:e03)<br>g08 TRACK_APPEARED_REAR(C,C:track_001) (C:e02) | ego: not yet observed |
| -5.55 | A | g09 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -5.50 | B | g10 CLOSING_START(B,A) (B:e04) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| -5.20 | C | g11 CLOSING_START(C,C:track_001) (C:e04) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -4.95 | C | g12 CLOSING_START(C,B) (C:e05) | ego: MOVING<br>track_001: CLOSING<br>track_002: no active state |
| -4.90 | B | g13 CLOSING_START(B,C) (B:e05) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -4.85 | A | g14 TRACK_APPEARED_FRONT(A,A:track_002) (A:e04)<br>g15 CLOSING_START(A,A:track_002) (A:e05) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -4.35 | A | g16 CLOSING_END(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -4.35 | B | g17 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING |
| -4.00 | A | g18 CLOSING_END(A,A:track_002) (A:e07) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -4.00 | C | g19 CLOSING_END(C,C:track_001) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -3.95 | C | g20 CLOSING_END(C,B) (C:e07) | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING |
| -3.90 | B | g21 CLOSING_END(B,C) (B:e07) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -3.60 | C | g22 SPEED_LIMIT_EXCEEDED_START(C) (C:e08) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -3.05 | C | g23 BRAKE_START(C) (C:e09)<br>g24 TRACK_LOST(C,C:track_001) (C:e10) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: no active state<br>track_002: no active state |
| -2.95 | C | g25 SPEED_LIMIT_EXCEEDED_END(C) (C:e11) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| -2.80 | B | g26 CLOSING_START(B,C) (B:e08) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| -2.75 | A | g27 CLOSING_START(A,A:track_002) (A:e08) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH |
| -2.75 | C | g28 CLOSING_START(C,B) (C:e12) | ego: MOVING, BRAKE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| -2.25 | B | g29 CRITICAL_TTC_START(B,C) (B:e09) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -1.95 | C | g30 MOVING_END(C) (C:e13)<br>g31 STOP_START(C) (C:e14) | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.85 | A | g32 CRITICAL_TTC_START(A,A:track_002) (A:e09) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -1.45 | A | g33 TRACK_LOST(A,A:track_001) (A:e10) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.45 | C | g34 TRACK_LOST(C,B) (C:e15) | ego: STOP, BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.40 | B | g35 COLLISION(B,C) (B:e10)<br>g36 CRITICAL_TTC_END(B,C) (B:e11)<br>g37 CLOSING_END(B,C) (B:e12)<br>g38 CLOSING_START(B,A) (B:e13) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state |
| -1.40 | C | g35 COLLISION(B,C) (C:e16) | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001, track_002 |
| -1.35 | B | g39 BRAKE_START(B) (B:e14) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -1.25 | B | g40 MOVING_END(B) (B:e15)<br>g41 STOP_START(B) (B:e16) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -0.80 | C | g42 TRACK_APPEARED_REAR(C,C:track_003) (C:e17)<br>g43 CLOSING_START(C,C:track_003) (C:e18) | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001, track_002 |
| -0.05 | B | g44 TRACK_LOST(B,A) (B:e17) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -0.05 | C | g45 TRACK_LOST(C,C:track_003) (C:e19) | ego: STOP, BRAKE<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001, track_002 |
| +0.00 | A | g46 COLLISION(A,B) (A:e11)<br>g47 CRITICAL_TTC_END(A,A:track_002) (A:e12)<br>g48 CLOSING_END(A,A:track_002) (A:e13) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g46 COLLISION(A,B) (B:e18) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.05 | A | g49 BRAKE_START(A) (A:e14) | ego: MOVING<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.20 | A | g50 MOVING_END(A) (A:e15)<br>g51 STOP_START(A) (A:e16) | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 6.00 s before the reference collision, A started moving (already the case when first observed).
- 6.00 s before the reference collision, B started moving (already the case when first observed).
- 6.00 s before the reference collision, C started moving (already the case when first observed).
- 6.00 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 6.00 s before the reference collision, B's radar started tracking C, which appeared in front of it.
- 6.00 s before the reference collision, B's radar started tracking A, which appeared behind it.
- 6.00 s before the reference collision, C's radar started tracking B, which appeared behind it.
- 6.00 s before the reference collision, C's radar started tracking unidentified object C:track_001, which appeared behind it.
- 5.55 s before the reference collision, A observed unidentified object A:track_001 start closing in.
- 5.50 s before the reference collision, B observed A start closing in.
- 5.20 s before the reference collision, C observed unidentified object C:track_001 start closing in.
- 4.95 s before the reference collision, C observed B start closing in.
- 4.90 s before the reference collision, B observed C start closing in.
- 4.85 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared in front of it.
- 4.85 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 4.35 s before the reference collision, A observed unidentified object A:track_001 stop closing in.
- 4.35 s before the reference collision, B observed A stop closing in.
- 4.00 s before the reference collision, A observed unidentified object A:track_002 stop closing in.
- 4.00 s before the reference collision, C observed unidentified object C:track_001 stop closing in.
- 3.95 s before the reference collision, C observed B stop closing in.
- 3.90 s before the reference collision, B observed C stop closing in.
- 3.60 s before the reference collision, C began exceeding the speed limit.
- 3.05 s before the reference collision, C started braking.
- 3.05 s before the reference collision, C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- 2.95 s before the reference collision, C returned within the speed limit.
- 2.80 s before the reference collision, B observed C start closing in.
- 2.75 s before the reference collision, A observed unidentified object A:track_002 start closing in.
- 2.75 s before the reference collision, C observed B start closing in.
- 2.25 s before the reference collision, B's time-to-contact with C became critical.
- 1.95 s before the reference collision, C stopped moving.
- 1.95 s before the reference collision, C came to a stop.
- 1.85 s before the reference collision, A's time-to-contact with unidentified object A:track_002 became critical.
- 1.45 s before the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 1.45 s before the reference collision, C's radar lost B (its states are UNKNOWN from then on, not ended).
- 1.40 s before the reference collision, B and C both recorded this same collision (peak impulses B: 21812, C: 21812 N*s).
- 1.40 s before the reference collision, B's time-to-contact with C stopped being critical.
- 1.40 s before the reference collision, B observed C stop closing in.
- 1.40 s before the reference collision, B observed A start closing in.
- 1.35 s before the reference collision, B started braking.
- 1.25 s before the reference collision, B stopped moving.
- 1.25 s before the reference collision, B came to a stop.
- 0.80 s before the reference collision, C's radar started tracking unidentified object C:track_003, which appeared behind it.
- 0.80 s before the reference collision, C observed unidentified object C:track_003 start closing in (already the case when first observed).
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, C's radar lost unidentified object C:track_003 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 31488, B: 31488 N*s).
- At the reference collision, A's time-to-contact with unidentified object A:track_002 stopped being critical.
- At the reference collision, A observed unidentified object A:track_002 stop closing in.
- 0.05 s after the reference collision, A started braking.
- 0.20 s after the reference collision, A stopped moving.
- 0.20 s after the reference collision, A came to a stop.
