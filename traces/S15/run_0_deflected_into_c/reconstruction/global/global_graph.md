# Global graph - S15/run_0_deflected_into_c

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002, C:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock ALIGNED; observed by others as: A:track_001 |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| C:track_002 | anonymous_track | seen only by C; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | ALIGNED | C:e08 | 4.70 | -3.80 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 10358.22 vs 10358.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1880.32 vs 1880.32 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.98 | A and C both reported collision_002 at 4.70 s (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 0.0 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.34 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>the only track of A compatible with the contact<br>collision_001 with B at 3.80 s: not compatible (track speed disagrees with B's own speed: RMSE 3.67 m/s over 3.0 s (> 1.50)) |
| A:track_002 | B | ASSOCIATED | 0.82 | A and B both reported collision_001 at 3.80 s (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 1.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.5 m -> 0.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.94 m/s over 1.8 s<br>clearance at the contact 0.56 m<br>the only track of A compatible with the contact<br>collision_002 with C at 4.70 s: not compatible (not approaching before the contact: clearance 1.1 m -> 1.3 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 3.39 m/s over 2.7 s (> 1.50)) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 2.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.2 m -> 9.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 4.95 m/s over 2.1 s (> 1.50)<br>clearance at the contact 9.08 m (beyond 3.50 m: confidence factor 0.18) |
| B:track_002 | A | ASSOCIATED | 0.93 | B and A both reported collision_001 (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.6 m -> 0.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.57 m/s over 1.8 s<br>clearance at the contact 0.34 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 0.98 | C and A both reported collision_002 (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 0.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.27 m/s over 3.0 s<br>clearance at the contact 0.06 m<br>the only track of C compatible with the contact |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 9.7 m -> 5.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.90 m/s over 3.0 s (> 1.50)<br>clearance at the contact 5.19 m (beyond 3.50 m: confidence factor 0.85) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.80 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -3.80 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -3.80 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g06 | -3.80 | THROTTLE_START | C | - | C:e02 @ 0.00 | active_at_first_observation=True |
| g07 | -3.80 | TRACK_APPEARED_FRONT | A | C | A:e03 @ 0.00 |  |
| g08 | -3.80 | TRACK_APPEARED_FRONT | C | A | C:e03 @ 0.00 |  |
| g09 | -3.80 | CLOSING_START | A | C | A:e04 @ 0.00 | active_at_first_observation=True |
| g10 | -3.80 | CLOSING_START | C | A | C:e04 @ 0.00 | active_at_first_observation=True |
| g11 | -3.60 | TRACK_APPEARED_LEFT | C | C:track_002 | C:e05 @ 0.20 |  |
| g12 | -3.60 | CLOSING_START | C | C:track_002 | C:e06 @ 0.20 | active_at_first_observation=True |
| g13 | -2.70 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e03 @ 1.10 | relevant_to_ego_path=True |
| g14 | -2.10 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e04 @ 1.70 |  |
| g15 | -2.10 | CLOSING_START | B | B:track_001 | B:e05 @ 1.70 | active_at_first_observation=True |
| g16 | -1.80 | TRACK_APPEARED_LEFT | B | A | B:e06 @ 2.00 |  |
| g17 | -1.80 | CLOSING_START | B | A | B:e07 @ 2.00 | active_at_first_observation=True |
| g18 | -1.75 | TRACK_APPEARED_RIGHT | A | B | A:e05 @ 2.05 |  |
| g19 | -1.75 | CLOSING_START | A | B | A:e06 @ 2.05 | active_at_first_observation=True |
| g20 | -1.55 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e08 @ 2.25 |  |
| g21 | -1.50 | TURN_LEFT_START | B | - | B:e09 @ 2.30 |  |
| g22 | -1.30 | CRITICAL_TTC_START | B | A | B:e10 @ 2.50 |  |
| g23 | -1.25 | CRITICAL_TTC_START | A | B | A:e07 @ 2.55 |  |
| g24 | -0.85 | THROTTLE_END | B | - | B:e11 @ 2.95 |  |
| g25 | -0.85 | BRAKE_START | B | - | B:e12 @ 2.95 |  |
| g26 | -0.30 | BRAKE_END | B | - | B:e13 @ 3.50 |  |
| g27 | -0.15 | THROTTLE_START | B | - | B:e14 @ 3.65 |  |
| g28 | -0.05 | EGO_PATH_ENTRY | B | A | B:e15 @ 3.75 |  |
| g29 | -0.05 | CRITICAL_TTC_START | A | C | A:e08 @ 3.75 |  |
| g30 | -0.05 | CRITICAL_TTC_START | C | A | C:e07 @ 3.75 |  |
| g31 | 0.00 | COLLISION | - | A, B | A:e09 @ 3.80, B:e16 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 10358.22, B 10358.22 |
| g32 | 0.00 | CLOSING_END | A | B | A:e10 @ 3.80 |  |
| g33 | 0.00 | TURN_LEFT_END | B | - | B:e17 @ 3.80 |  |
| g34 | 0.05 | CRITICAL_TTC_END | A | B | A:e11 @ 3.85 |  |
| g35 | 0.05 | THROTTLE_END | A | - | A:e12 @ 3.85 |  |
| g36 | 0.05 | THROTTLE_END | B | - | B:e18 @ 3.85 |  |
| g37 | 0.05 | BRAKE_START | B | - | B:e19 @ 3.85 |  |
| g38 | 0.05 | TURN_LEFT_START | A | - | A:e13 @ 3.85 |  |
| g39 | 0.15 | CLOSING_END | B | A | B:e20 @ 3.95 |  |
| g40 | 0.15 | CRITICAL_TTC_START | B | B:track_001 | B:e21 @ 3.95 |  |
| g41 | 0.20 | MOVING_END | B | - | B:e22 @ 4.00 |  |
| g42 | 0.20 | STOP_START | B | - | B:e23 @ 4.00 |  |
| g43 | 0.25 | CRITICAL_TTC_END | B | A | B:e24 @ 4.05 |  |
| g44 | 0.55 | EGO_PATH_ENTRY | A | C | A:e14 @ 4.35 |  |
| g45 | 0.75 | EGO_PATH_EXIT | B | A | B:e25 @ 4.55 |  |
| g46 | 0.90 | COLLISION | - | A, C | A:e15 @ 4.70, C:e08 @ 4.70 | matched_event=collision_002; reference_event=False; peak_impulse=A 1880.32, C 1880.32 |
| g47 | 0.90 | CRITICAL_TTC_END | C | A | C:e09 @ 4.70 |  |
| g48 | 0.90 | CLOSING_END | C | A | C:e10 @ 4.70 |  |
| g49 | 0.90 | EGO_PATH_EXIT | A | C | A:e16 @ 4.70 |  |
| g50 | 0.95 | THROTTLE_END | C | - | C:e11 @ 4.75 |  |
| g51 | 0.95 | BRAKE_START | C | - | C:e12 @ 4.75 |  |
| g52 | 1.05 | CRITICAL_TTC_END | A | C | A:e17 @ 4.85 |  |
| g53 | 1.05 | CLOSING_END | A | C | A:e18 @ 4.85 |  |
| g54 | 1.15 | CRITICAL_TTC_END | B | B:track_001 | B:e26 @ 4.95 |  |
| g55 | 1.20 | CLOSING_END | C | C:track_002 | C:e13 @ 5.00 |  |
| g56 | 1.20 | MOVING_END | C | - | C:e14 @ 5.00 |  |
| g57 | 1.20 | STOP_START | C | - | C:e15 @ 5.00 |  |
| g58 | 1.25 | TURN_LEFT_END | A | - | A:e19 @ 5.05 |  |
| g59 | 1.30 | MOVING_END | A | - | A:e20 @ 5.10 |  |
| g60 | 1.30 | STOP_START | A | - | A:e21 @ 5.10 |  |
| g61 | 1.70 | TRACK_LOST | B | A | B:e27 @ 5.50 |  |
| g62 | 1.80 | CLOSING_END | B | B:track_001 | B:e28 @ 5.60 |  |

## Edges

```
    g01 --PRECEDES--> g11
    g01 --PRECEDES--> g12
    g02 --PRECEDES--> g11
    g02 --PRECEDES--> g12
    g03 --PRECEDES--> g11
    g03 --PRECEDES--> g12
    g04 --PRECEDES--> g11
    g04 --PRECEDES--> g12
    g05 --PRECEDES--> g11
    g05 --PRECEDES--> g12
    g06 --PRECEDES--> g11
    g06 --PRECEDES--> g12
    g07 --PRECEDES--> g11
    g07 --PRECEDES--> g12
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
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
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g31 --PRECEDES--> g38
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g32 --PRECEDES--> g38
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g43
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g46 --PRECEDES--> g51
    g47 --PRECEDES--> g50
    g47 --PRECEDES--> g51
    g48 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g54 --PRECEDES--> g56
    g54 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g58 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g60 --PRECEDES--> g61
    g61 --PRECEDES--> g62
    g07 --SAME_TRACK--> g09
    g18 --SAME_TRACK--> g19
    g18 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g29
    g18 --SAME_TRACK--> g32
    g18 --SAME_TRACK--> g34
    g07 --SAME_TRACK--> g44
    g07 --SAME_TRACK--> g49
    g07 --SAME_TRACK--> g52
    g07 --SAME_TRACK--> g53
    g14 --SAME_TRACK--> g15
    g16 --SAME_TRACK--> g17
    g16 --SAME_TRACK--> g22
    g16 --SAME_TRACK--> g28
    g16 --SAME_TRACK--> g39
    g14 --SAME_TRACK--> g40
    g16 --SAME_TRACK--> g43
    g16 --SAME_TRACK--> g45
    g14 --SAME_TRACK--> g54
    g16 --SAME_TRACK--> g61
    g14 --SAME_TRACK--> g62
    g08 --SAME_TRACK--> g10
    g11 --SAME_TRACK--> g12
    g08 --SAME_TRACK--> g30
    g08 --SAME_TRACK--> g47
    g08 --SAME_TRACK--> g48
    g11 --SAME_TRACK--> g55
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A) |
| -3.60 | TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002) |
| -2.70 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -2.10 | TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001) |
| -1.80 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.75 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -1.55 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -1.50 | TURN_LEFT_START(B) |
| -1.30 | CRITICAL_TTC_START(B,A) |
| -1.25 | CRITICAL_TTC_START(A,B) |
| -0.85 | THROTTLE_END(B); BRAKE_START(B) |
| -0.30 | BRAKE_END(B) |
| -0.15 | THROTTLE_START(B) |
| -0.05 | EGO_PATH_ENTRY(B,A); CRITICAL_TTC_START(A,C); CRITICAL_TTC_START(C,A) |
| +0.00 | COLLISION(A,B); CLOSING_END(A,B); TURN_LEFT_END(B) |
| +0.05 | CRITICAL_TTC_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(B); TURN_LEFT_START(A) |
| +0.15 | CLOSING_END(B,A); CRITICAL_TTC_START(B,B:track_001) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.25 | CRITICAL_TTC_END(B,A) |
| +0.55 | EGO_PATH_ENTRY(A,C) |
| +0.75 | EGO_PATH_EXIT(B,A) |
| +0.90 | COLLISION(A,C); CRITICAL_TTC_END(C,A); CLOSING_END(C,A); EGO_PATH_EXIT(A,C) |
| +0.95 | THROTTLE_END(C); BRAKE_START(C) |
| +1.05 | CRITICAL_TTC_END(A,C); CLOSING_END(A,C) |
| +1.15 | CRITICAL_TTC_END(B,B:track_001) |
| +1.20 | CLOSING_END(C,C:track_002); MOVING_END(C); STOP_START(C) |
| +1.25 | TURN_LEFT_END(A) |
| +1.30 | MOVING_END(A); STOP_START(A) |
| +1.70 | TRACK_LOST(B,A) |
| +1.80 | CLOSING_END(B,B:track_001) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 4.70 (+0.95 s); EGO_PATH_ENTRY 4.35 after critical TTC (+0.60 s) [local times; t_global: critical_ttc_start -0.05, ego_path_entry +0.55, collision +0.90]
- A's track_002 (B): CRITICAL_TTC_START 2.55, COLLISION with B 3.80 (+1.25 s) [local times; t_global: critical_ttc_start -1.25, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.95 [local times; t_global: critical_ttc_start +0.15]
- B's track_002 (A): CRITICAL_TTC_START 2.50, COLLISION with A 3.80 (+1.30 s); EGO_PATH_ENTRY 3.75 after critical TTC (+1.25 s) [local times; t_global: critical_ttc_start -1.30, ego_path_entry -0.05, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 3.75, COLLISION with A 4.70 (+0.95 s) [local times; t_global: critical_ttc_start -0.05, collision +0.90]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.80 | A | g01 MOVING_START(A) (A:e01)<br>g04 THROTTLE_START(A) (A:e02)<br>g07 TRACK_APPEARED_FRONT(A,C) (A:e03)<br>g09 CLOSING_START(A,C) (A:e04) | ego: not yet observed |
| -3.80 | B | g02 MOVING_START(B) (B:e01)<br>g05 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -3.80 | C | g03 MOVING_START(C) (C:e01)<br>g06 THROTTLE_START(C) (C:e02)<br>g08 TRACK_APPEARED_FRONT(C,A) (C:e03)<br>g10 CLOSING_START(C,A) (C:e04) | ego: not yet observed |
| -3.60 | C | g11 TRACK_APPEARED_LEFT(C,C:track_002) (C:e05)<br>g12 CLOSING_START(C,C:track_002) (C:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -2.70 | B | g13 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e03) | ego: MOVING, THROTTLE |
| -2.10 | B | g14 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e04)<br>g15 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -1.80 | B | g16 TRACK_APPEARED_LEFT(B,A) (B:e06)<br>g17 CLOSING_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.75 | A | g18 TRACK_APPEARED_RIGHT(A,B) (A:e05)<br>g19 CLOSING_START(A,B) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.55 | B | g20 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.50 | B | g21 TURN_LEFT_START(B) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.30 | B | g22 CRITICAL_TTC_START(B,A) (B:e10) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.25 | A | g23 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -0.85 | B | g24 THROTTLE_END(B) (B:e11)<br>g25 BRAKE_START(B) (B:e12) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.30 | B | g26 BRAKE_END(B) (B:e13) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.15 | B | g27 THROTTLE_START(B) (B:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.05 | B | g28 EGO_PATH_ENTRY(B,A) (B:e15) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.05 | A | g29 CRITICAL_TTC_START(A,C) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.05 | C | g30 CRITICAL_TTC_START(C,A) (C:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| +0.00 | A | g31 COLLISION(A,B) (A:e09)<br>g32 CLOSING_END(A,B) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | B | g31 COLLISION(A,B) (B:e16)<br>g33 TURN_LEFT_END(B) (B:e17) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | A | g34 CRITICAL_TTC_END(A,B) (A:e11)<br>g35 THROTTLE_END(A) (A:e12)<br>g38 TURN_LEFT_START(A) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CRITICAL_TTC |
| +0.05 | B | g36 THROTTLE_END(B) (B:e18)<br>g37 BRAKE_START(B) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.15 | B | g39 CLOSING_END(B,A) (B:e20)<br>g40 CRITICAL_TTC_START(B,B:track_001) (B:e21) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.20 | B | g41 MOVING_END(B) (B:e22)<br>g42 STOP_START(B) (B:e23) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.25 | B | g43 CRITICAL_TTC_END(B,A) (B:e24) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.55 | A | g44 EGO_PATH_ENTRY(A,C) (A:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state |
| +0.75 | B | g45 EGO_PATH_EXIT(B,A) (B:e25) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.90 | A | g46 COLLISION(A,C) (A:e15)<br>g49 EGO_PATH_EXIT(A,C) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state |
| +0.90 | C | g46 COLLISION(A,C) (C:e08)<br>g47 CRITICAL_TTC_END(C,A) (C:e09)<br>g48 CLOSING_END(C,A) (C:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| +0.95 | C | g50 THROTTLE_END(C) (C:e11)<br>g51 BRAKE_START(C) (C:e12) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING |
| +1.05 | A | g52 CRITICAL_TTC_END(A,C) (A:e17)<br>g53 CLOSING_END(A,C) (A:e18) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state |
| +1.15 | B | g54 CRITICAL_TTC_END(B,B:track_001) (B:e26) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>sign-0: STOP sign known, relevant to the path |
| +1.20 | C | g55 CLOSING_END(C,C:track_002) (C:e13)<br>g56 MOVING_END(C) (C:e14)<br>g57 STOP_START(C) (C:e15) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING |
| +1.25 | A | g58 TURN_LEFT_END(A) (A:e19) | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>track_002: no active state |
| +1.30 | A | g59 MOVING_END(A) (A:e20)<br>g60 STOP_START(A) (A:e21) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| +1.70 | B | g61 TRACK_LOST(B,A) (B:e27) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>sign-0: STOP sign known, relevant to the path |
| +1.80 | B | g62 CLOSING_END(B,B:track_001) (B:e28) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known, relevant to the path |

## Plain-language reading

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 3.80 s before the reference collision, C started moving (already the case when first observed).
- 3.80 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 3.80 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 3.80 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.80 s before the reference collision, C observed A start closing in (already the case when first observed).
- 3.60 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared on its left.
- 3.60 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 2.70 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 2.10 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.10 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 1.80 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.80 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.75 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.75 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.55 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.50 s before the reference collision, B started turning left.
- 1.30 s before the reference collision, B's time-to-contact with A became critical.
- 1.25 s before the reference collision, A's time-to-contact with B became critical.
- 0.85 s before the reference collision, B released the accelerator.
- 0.85 s before the reference collision, B started braking.
- 0.30 s before the reference collision, B released the brake.
- 0.15 s before the reference collision, B pressed the accelerator.
- 0.05 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's time-to-contact with C became critical.
- 0.05 s before the reference collision, C's time-to-contact with A became critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 10358, B: 10358 N*s).
- At the reference collision, A observed B stop closing in.
- At the reference collision, B stopped turning left.
- 0.05 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A started turning left.
- 0.15 s after the reference collision, B observed A stop closing in.
- 0.15 s after the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.25 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.55 s after the reference collision, A observed C enter its forward path corridor.
- 0.75 s after the reference collision, B observed A leave its forward path corridor.
- 0.90 s after the reference collision, A and C both recorded this same collision (peak impulses A: 1880, C: 1880 N*s).
- 0.90 s after the reference collision, C's time-to-contact with A stopped being critical.
- 0.90 s after the reference collision, C observed A stop closing in.
- 0.90 s after the reference collision, A observed C leave its forward path corridor.
- 0.95 s after the reference collision, C released the accelerator.
- 0.95 s after the reference collision, C started braking.
- 1.05 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.05 s after the reference collision, A observed C stop closing in.
- 1.15 s after the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.20 s after the reference collision, C observed unidentified object C:track_002 stop closing in.
- 1.20 s after the reference collision, C stopped moving.
- 1.20 s after the reference collision, C came to a stop.
- 1.25 s after the reference collision, A stopped turning left.
- 1.30 s after the reference collision, A stopped moving.
- 1.30 s after the reference collision, A came to a stop.
- 1.70 s after the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 1.80 s after the reference collision, B observed unidentified object B:track_001 stop closing in.
