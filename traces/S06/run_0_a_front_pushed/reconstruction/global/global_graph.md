# Global graph - S06/run_0_a_front_pushed

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock ALIGNED; observed by others as: B:track_001 |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| C:track_001 | anonymous_track | seen only by C; candidate: B |
| C:track_002 | anonymous_track | seen only by C; candidate: B |
| C:track_003 | anonymous_track | seen only by C; candidate: B |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e13 | 5.90 | -5.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e18 | 5.90 | -5.90 | reported the reference collision collision_001 |
| C | ALIGNED | C:e19 | 6.05 | -5.90 | shares collision_002 with B, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 11621.71 vs 11621.71 N*s (similarity 1.000, tolerance 0.10); 2 competing report(s) within tolerance; best match kept

Matched `collision_002`: B and C both recorded a collision; peak impulses 10857.64 vs 10857.64 N*s (similarity 1.000, tolerance 0.10); 2 competing report(s) within tolerance; best match kept

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.66 | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.7 m -> 0.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.37 m/s over 3.0 s<br>clearance at the contact 0.53 m<br>the only track of A compatible with the contact |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 4.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.7 m -> 5.3 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.44 m/s over 3.0 s (> 1.50)<br>clearance at the contact 5.31 m (beyond 3.50 m: confidence factor 0.83) |
| B:track_001 | C | ASSOCIATED | 1.00 | B and C both reported collision_002 at 6.05 s (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 6.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 0.23 m<br>the only track of B compatible with the contact<br>collision_001 with A at 5.90 s: not compatible (not approaching before the contact: clearance 1.1 m -> 1.1 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 10.87 m/s over 3.0 s (> 1.50)) |
| B:track_002 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 at 5.90 s (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.5 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.09 m/s over 2.9 s<br>clearance at the contact 0.50 m<br>the only track of B compatible with the contact<br>collision_002 with C at 6.05 s: not compatible (track speed disagrees with C's own speed: RMSE 11.40 m/s over 2.8 s (> 1.50)) |
| C:track_001 | C:track_001 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 6.05 s before the matched collision<br>lost 3.05 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 34.3 m -> 35.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 6.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 3.0 m -> 3.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.23 m/s over 3.0 s<br>clearance at the contact 2.95 m |
| C:track_003 | C:track_003 | ANONYMOUS | - | C and B both reported collision_002 (peak impulse 10857.64 vs 10857.64 N*s)<br>tracked for 1.45 s before the matched collision<br>continuous up to the contact: last observed 0.20 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.2 m -> 6.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 12.78 m/s over 1.2 s (> 1.50)<br>clearance at the contact 6.46 m (beyond 3.50 m: confidence factor 0.62) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.90 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.90 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.90 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -5.90 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.00 |  |
| g05 | -5.90 | TRACK_APPEARED_FRONT | B | C | B:e02 @ 0.00 |  |
| g06 | -5.90 | TRACK_APPEARED_REAR | B | A | B:e03 @ 0.00 |  |
| g07 | -5.90 | TRACK_APPEARED_REAR | C | C:track_001 | C:e02 @ 0.00 |  |
| g08 | -5.90 | TRACK_APPEARED_REAR | C | C:track_002 | C:e03 @ 0.00 |  |
| g09 | -5.45 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g10 | -5.40 | CLOSING_START | B | A | B:e04 @ 0.50 |  |
| g11 | -5.10 | CLOSING_START | C | C:track_001 | C:e04 @ 0.80 |  |
| g12 | -4.90 | TRACK_APPEARED_FRONT | A | A:track_002 | A:e04 @ 1.00 |  |
| g13 | -4.90 | CLOSING_START | A | A:track_002 | A:e05 @ 1.00 | active_at_first_observation=True |
| g14 | -4.85 | CLOSING_START | B | C | B:e05 @ 1.05 |  |
| g15 | -4.85 | CLOSING_START | C | C:track_002 | C:e05 @ 1.05 |  |
| g16 | -4.25 | CLOSING_END | A | B | A:e06 @ 1.65 |  |
| g17 | -4.25 | CLOSING_END | B | A | B:e06 @ 1.65 |  |
| g18 | -3.95 | CLOSING_END | A | A:track_002 | A:e07 @ 1.95 |  |
| g19 | -3.95 | CLOSING_END | C | C:track_001 | C:e06 @ 1.95 |  |
| g20 | -3.85 | CLOSING_END | B | C | B:e07 @ 2.05 |  |
| g21 | -3.85 | CLOSING_END | C | C:track_002 | C:e07 @ 2.05 |  |
| g22 | -3.50 | SPEED_LIMIT_EXCEEDED_START | C | - | C:e08 @ 2.40 |  |
| g23 | -2.95 | BRAKE_START | C | - | C:e09 @ 2.95 |  |
| g24 | -2.90 | TRACK_LOST | C | C:track_001 | C:e10 @ 3.00 |  |
| g25 | -2.85 | SPEED_LIMIT_EXCEEDED_END | C | - | C:e11 @ 3.05 |  |
| g26 | -2.70 | CLOSING_START | B | C | B:e08 @ 3.20 |  |
| g27 | -2.65 | CLOSING_START | A | A:track_002 | A:e08 @ 3.25 |  |
| g28 | -2.60 | CLOSING_START | C | C:track_002 | C:e12 @ 3.30 |  |
| g29 | -2.20 | BRAKE_START | B | - | B:e09 @ 3.70 |  |
| g30 | -2.15 | CRITICAL_TTC_START | B | C | B:e10 @ 3.75 |  |
| g31 | -1.95 | CLOSING_START | B | A | B:e11 @ 3.95 |  |
| g32 | -1.90 | CLOSING_START | A | B | A:e09 @ 4.00 |  |
| g33 | -1.85 | MOVING_END | C | - | C:e13 @ 4.05 |  |
| g34 | -1.85 | STOP_START | C | - | C:e14 @ 4.05 |  |
| g35 | -1.75 | CRITICAL_TTC_START | A | A:track_002 | A:e10 @ 4.15 |  |
| g36 | -1.30 | TRACK_APPEARED_REAR | C | C:track_003 | C:e15 @ 4.60 |  |
| g37 | -1.30 | CLOSING_START | C | C:track_003 | C:e16 @ 4.60 | active_at_first_observation=True |
| g38 | -1.20 | CRITICAL_TTC_START | A | B | A:e11 @ 4.70 |  |
| g39 | -1.00 | CRITICAL_TTC_END | B | C | B:e12 @ 4.90 |  |
| g40 | -1.00 | CLOSING_END | B | C | B:e13 @ 4.90 |  |
| g41 | -1.00 | CLOSING_END | C | C:track_002 | C:e17 @ 4.90 |  |
| g42 | -1.00 | MOVING_END | B | - | B:e14 @ 4.90 |  |
| g43 | -1.00 | STOP_START | B | - | B:e15 @ 4.90 |  |
| g44 | -0.35 | BRAKE_START | A | - | A:e12 @ 5.55 |  |
| g45 | -0.20 | BRAKE_END | B | - | B:e16 @ 5.70 |  |
| g46 | -0.05 | TRACK_LOST | B | A | B:e17 @ 5.85 |  |
| g47 | -0.05 | TRACK_LOST | C | C:track_003 | C:e18 @ 5.85 |  |
| g48 | 0.00 | COLLISION | - | A, B | A:e13 @ 5.90, B:e18 @ 5.90 | matched_event=collision_001; reference_event=True; peak_impulse=A 11621.71, B 11621.71 |
| g49 | 0.00 | STOP_END | B | - | B:e19 @ 5.90 |  |
| g50 | 0.00 | MOVING_START | B | - | B:e20 @ 5.90 |  |
| g51 | 0.15 | COLLISION | - | B, C | B:e21 @ 6.05, C:e19 @ 6.05 | matched_event=collision_002; reference_event=False; peak_impulse=B 10857.64, C 10857.64 |
| g52 | 0.20 | CRITICAL_TTC_END | A | A:track_002 | A:e15 @ 6.10 |  |
| g53 | 0.20 | CRITICAL_TTC_END | A | B | A:e14 @ 6.10 |  |
| g54 | 0.20 | CLOSING_END | A | A:track_002 | A:e17 @ 6.10 |  |
| g55 | 0.20 | CLOSING_END | A | B | A:e16 @ 6.10 |  |
| g56 | 0.25 | MOVING_END | A | - | A:e18 @ 6.15 |  |
| g57 | 0.25 | MOVING_END | B | - | B:e22 @ 6.15 |  |
| g58 | 0.25 | STOP_START | A | - | A:e19 @ 6.15 |  |
| g59 | 0.25 | STOP_START | B | - | B:e23 @ 6.15 |  |

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
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
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
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g40 --PRECEDES--> g44
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g51
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g52 --PRECEDES--> g58
    g52 --PRECEDES--> g59
    g53 --PRECEDES--> g56
    g53 --PRECEDES--> g57
    g53 --PRECEDES--> g58
    g53 --PRECEDES--> g59
    g54 --PRECEDES--> g56
    g54 --PRECEDES--> g57
    g54 --PRECEDES--> g58
    g54 --PRECEDES--> g59
    g55 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g04 --SAME_TRACK--> g09
    g12 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g16
    g12 --SAME_TRACK--> g18
    g12 --SAME_TRACK--> g27
    g04 --SAME_TRACK--> g32
    g12 --SAME_TRACK--> g35
    g04 --SAME_TRACK--> g38
    g04 --SAME_TRACK--> g53
    g12 --SAME_TRACK--> g52
    g04 --SAME_TRACK--> g55
    g12 --SAME_TRACK--> g54
    g06 --SAME_TRACK--> g10
    g05 --SAME_TRACK--> g14
    g06 --SAME_TRACK--> g17
    g05 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g26
    g05 --SAME_TRACK--> g30
    g06 --SAME_TRACK--> g31
    g05 --SAME_TRACK--> g39
    g05 --SAME_TRACK--> g40
    g06 --SAME_TRACK--> g46
    g07 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g15
    g07 --SAME_TRACK--> g19
    g08 --SAME_TRACK--> g21
    g07 --SAME_TRACK--> g24
    g08 --SAME_TRACK--> g28
    g36 --SAME_TRACK--> g37
    g08 --SAME_TRACK--> g41
    g36 --SAME_TRACK--> g47
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.90 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,C); TRACK_APPEARED_REAR(B,A); TRACK_APPEARED_REAR(C,C:track_001); TRACK_APPEARED_REAR(C,C:track_002) |
| -5.45 | CLOSING_START(A,B) |
| -5.40 | CLOSING_START(B,A) |
| -5.10 | CLOSING_START(C,C:track_001) |
| -4.90 | TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002) |
| -4.85 | CLOSING_START(B,C); CLOSING_START(C,C:track_002) |
| -4.25 | CLOSING_END(A,B); CLOSING_END(B,A) |
| -3.95 | CLOSING_END(A,A:track_002); CLOSING_END(C,C:track_001) |
| -3.85 | CLOSING_END(B,C); CLOSING_END(C,C:track_002) |
| -3.50 | SPEED_LIMIT_EXCEEDED_START(C) |
| -2.95 | BRAKE_START(C) |
| -2.90 | TRACK_LOST(C,C:track_001) |
| -2.85 | SPEED_LIMIT_EXCEEDED_END(C) |
| -2.70 | CLOSING_START(B,C) |
| -2.65 | CLOSING_START(A,A:track_002) |
| -2.60 | CLOSING_START(C,C:track_002) |
| -2.20 | BRAKE_START(B) |
| -2.15 | CRITICAL_TTC_START(B,C) |
| -1.95 | CLOSING_START(B,A) |
| -1.90 | CLOSING_START(A,B) |
| -1.85 | MOVING_END(C); STOP_START(C) |
| -1.75 | CRITICAL_TTC_START(A,A:track_002) |
| -1.30 | TRACK_APPEARED_REAR(C,C:track_003); CLOSING_START(C,C:track_003) |
| -1.20 | CRITICAL_TTC_START(A,B) |
| -1.00 | CRITICAL_TTC_END(B,C); CLOSING_END(B,C); CLOSING_END(C,C:track_002); MOVING_END(B); STOP_START(B) |
| -0.35 | BRAKE_START(A) |
| -0.20 | BRAKE_END(B) |
| -0.05 | TRACK_LOST(B,A); TRACK_LOST(C,C:track_003) |
| +0.00 | COLLISION(A,B); STOP_END(B); MOVING_START(B) |
| +0.15 | COLLISION(B,C) |
| +0.20 | CRITICAL_TTC_END(A,A:track_002); CRITICAL_TTC_END(A,B); CLOSING_END(A,A:track_002); CLOSING_END(A,B) |
| +0.25 | MOVING_END(A); MOVING_END(B); STOP_START(A); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 4.70, COLLISION with B 5.90 (+1.20 s) [local times; t_global: critical_ttc_start -1.20, collision +0.00]
- A's track_002 (unidentified A:track_002): CRITICAL_TTC_START 4.15, COLLISION 5.90 (+1.75 s) [local times; t_global: critical_ttc_start -1.75, collision +0.00]
- B's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 6.05 (+2.30 s) [local times; t_global: critical_ttc_start -2.15, collision +0.15]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.90 | A | g01 MOVING_START(A) (A:e01)<br>g04 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: not yet observed |
| -5.90 | B | g02 MOVING_START(B) (B:e01)<br>g05 TRACK_APPEARED_FRONT(B,C) (B:e02)<br>g06 TRACK_APPEARED_REAR(B,A) (B:e03) | ego: not yet observed |
| -5.90 | C | g03 MOVING_START(C) (C:e01)<br>g07 TRACK_APPEARED_REAR(C,C:track_001) (C:e02)<br>g08 TRACK_APPEARED_REAR(C,C:track_002) (C:e03) | ego: not yet observed |
| -5.45 | A | g09 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -5.40 | B | g10 CLOSING_START(B,A) (B:e04) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| -5.10 | C | g11 CLOSING_START(C,C:track_001) (C:e04) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -4.90 | A | g12 TRACK_APPEARED_FRONT(A,A:track_002) (A:e04)<br>g13 CLOSING_START(A,A:track_002) (A:e05) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -4.85 | B | g14 CLOSING_START(B,C) (B:e05) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -4.85 | C | g15 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING<br>track_002: no active state |
| -4.25 | A | g16 CLOSING_END(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -4.25 | B | g17 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING |
| -3.95 | A | g18 CLOSING_END(A,A:track_002) (A:e07) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -3.95 | C | g19 CLOSING_END(C,C:track_001) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -3.85 | B | g20 CLOSING_END(B,C) (B:e07) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -3.85 | C | g21 CLOSING_END(C,C:track_002) (C:e07) | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING |
| -3.50 | C | g22 SPEED_LIMIT_EXCEEDED_START(C) (C:e08) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -2.95 | C | g23 BRAKE_START(C) (C:e09) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: no active state<br>track_002: no active state |
| -2.90 | C | g24 TRACK_LOST(C,C:track_001) (C:e10) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED<br>track_001: no active state<br>track_002: no active state |
| -2.85 | C | g25 SPEED_LIMIT_EXCEEDED_END(C) (C:e11) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| -2.70 | B | g26 CLOSING_START(B,C) (B:e08) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| -2.65 | A | g27 CLOSING_START(A,A:track_002) (A:e08) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH |
| -2.60 | C | g28 CLOSING_START(C,C:track_002) (C:e12) | ego: MOVING, BRAKE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| -2.20 | B | g29 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -2.15 | B | g30 CRITICAL_TTC_START(B,C) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| -1.95 | B | g31 CLOSING_START(B,A) (B:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state |
| -1.90 | A | g32 CLOSING_START(A,B) (A:e09) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -1.85 | C | g33 MOVING_END(C) (C:e13)<br>g34 STOP_START(C) (C:e14) | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.75 | A | g35 CRITICAL_TTC_START(A,A:track_002) (A:e10) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| -1.30 | C | g36 TRACK_APPEARED_REAR(C,C:track_003) (C:e15)<br>g37 CLOSING_START(C,C:track_003) (C:e16) | ego: STOP, BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.20 | A | g38 CRITICAL_TTC_START(A,B) (A:e11) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.00 | B | g39 CRITICAL_TTC_END(B,C) (B:e12)<br>g40 CLOSING_END(B,C) (B:e13)<br>g42 MOVING_END(B) (B:e14)<br>g43 STOP_START(B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING |
| -1.00 | C | g41 CLOSING_END(C,C:track_002) (C:e17) | ego: STOP, BRAKE<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -0.35 | A | g44 BRAKE_START(A) (A:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.20 | B | g45 BRAKE_END(B) (B:e16) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -0.05 | B | g46 TRACK_LOST(B,A) (B:e17) | ego: STOP<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -0.05 | C | g47 TRACK_LOST(C,C:track_003) (C:e18) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.00 | A | g48 COLLISION(A,B) (A:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g48 COLLISION(A,B) (B:e18)<br>g49 STOP_END(B) (B:e19)<br>g50 MOVING_START(B) (B:e20) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.15 | B | g51 COLLISION(B,C) (B:e21) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.15 | C | g51 COLLISION(B,C) (C:e19) | ego: STOP, BRAKE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001, track_003 |
| +0.20 | A | g52 CRITICAL_TTC_END(A,A:track_002) (A:e15)<br>g53 CRITICAL_TTC_END(A,B) (A:e14)<br>g54 CLOSING_END(A,A:track_002) (A:e17)<br>g55 CLOSING_END(A,B) (A:e16) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.25 | A | g56 MOVING_END(A) (A:e18)<br>g58 STOP_START(A) (A:e19) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH |
| +0.25 | B | g57 MOVING_END(B) (B:e22)<br>g59 STOP_START(B) (B:e23) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |

## Plain-language reading

- 5.90 s before the reference collision, A started moving (already the case when first observed).
- 5.90 s before the reference collision, B started moving (already the case when first observed).
- 5.90 s before the reference collision, C started moving (already the case when first observed).
- 5.90 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 5.90 s before the reference collision, B's radar started tracking C, which appeared in front of it.
- 5.90 s before the reference collision, B's radar started tracking A, which appeared behind it.
- 5.90 s before the reference collision, C's radar started tracking unidentified object C:track_001, which appeared behind it.
- 5.90 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared behind it.
- 5.45 s before the reference collision, A observed B start closing in.
- 5.40 s before the reference collision, B observed A start closing in.
- 5.10 s before the reference collision, C observed unidentified object C:track_001 start closing in.
- 4.90 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared in front of it.
- 4.90 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 4.85 s before the reference collision, B observed C start closing in.
- 4.85 s before the reference collision, C observed unidentified object C:track_002 start closing in.
- 4.25 s before the reference collision, A observed B stop closing in.
- 4.25 s before the reference collision, B observed A stop closing in.
- 3.95 s before the reference collision, A observed unidentified object A:track_002 stop closing in.
- 3.95 s before the reference collision, C observed unidentified object C:track_001 stop closing in.
- 3.85 s before the reference collision, B observed C stop closing in.
- 3.85 s before the reference collision, C observed unidentified object C:track_002 stop closing in.
- 3.50 s before the reference collision, C began exceeding the speed limit.
- 2.95 s before the reference collision, C started braking.
- 2.90 s before the reference collision, C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- 2.85 s before the reference collision, C returned within the speed limit.
- 2.70 s before the reference collision, B observed C start closing in.
- 2.65 s before the reference collision, A observed unidentified object A:track_002 start closing in.
- 2.60 s before the reference collision, C observed unidentified object C:track_002 start closing in.
- 2.20 s before the reference collision, B started braking.
- 2.15 s before the reference collision, B's time-to-contact with C became critical.
- 1.95 s before the reference collision, B observed A start closing in.
- 1.90 s before the reference collision, A observed B start closing in.
- 1.85 s before the reference collision, C stopped moving.
- 1.85 s before the reference collision, C came to a stop.
- 1.75 s before the reference collision, A's time-to-contact with unidentified object A:track_002 became critical.
- 1.30 s before the reference collision, C's radar started tracking unidentified object C:track_003, which appeared behind it.
- 1.30 s before the reference collision, C observed unidentified object C:track_003 start closing in (already the case when first observed).
- 1.20 s before the reference collision, A's time-to-contact with B became critical.
- 1.00 s before the reference collision, B's time-to-contact with C stopped being critical.
- 1.00 s before the reference collision, B observed C stop closing in.
- 1.00 s before the reference collision, C observed unidentified object C:track_002 stop closing in.
- 1.00 s before the reference collision, B stopped moving.
- 1.00 s before the reference collision, B came to a stop.
- 0.35 s before the reference collision, A started braking.
- 0.20 s before the reference collision, B released the brake.
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, C's radar lost unidentified object C:track_003 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 11622, B: 11622 N*s).
- At the reference collision, B left its stop.
- At the reference collision, B started moving.
- 0.15 s after the reference collision, B and C both recorded this same collision (peak impulses B: 10858, C: 10858 N*s).
- 0.20 s after the reference collision, A's time-to-contact with unidentified object A:track_002 stopped being critical.
- 0.20 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.20 s after the reference collision, A observed unidentified object A:track_002 stop closing in.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.25 s after the reference collision, A stopped moving.
- 0.25 s after the reference collision, B stopped moving.
- 0.25 s after the reference collision, A came to a stop.
- 0.25 s after the reference collision, B came to a stop.
