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
| B | ALIGNED | B:e15 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | ALIGNED | C:e07 | 4.75 | -3.80 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1637.56 vs 1637.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.96 | A and C both reported collision_002 at 4.75 s (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.9 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.43 m/s over 3.0 s<br>clearance at the contact 0.21 m<br>the only track of A compatible with the contact<br>collision_001 with B at 3.80 s: not compatible (track speed disagrees with B's own speed: RMSE 3.64 m/s over 3.0 s (> 1.50)) |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 at 3.80 s (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.64 m/s over 1.6 s<br>clearance at the contact 0.75 m<br>the only track of A compatible with the contact<br>collision_002 with C at 4.75 s: not compatible (track speed disagrees with C's own speed: RMSE 3.27 m/s over 1.6 s (> 1.50)) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.4 m -> 9.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 4.98 m/s over 2.0 s (> 1.50)<br>clearance at the contact 9.17 m (beyond 3.50 m: confidence factor 0.17) |
| B:track_002 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.0 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.49 m/s over 1.7 s<br>clearance at the contact 0.18 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 0.97 | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.1 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.36 m/s over 3.0 s<br>clearance at the contact 1.10 m<br>the only track of C compatible with the contact |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.0 m -> 6.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.99 m/s over 3.0 s (> 1.50)<br>clearance at the contact 6.69 m (beyond 3.50 m: confidence factor 0.57) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.80 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -3.75 | TRACK_APPEARED_FRONT | C | A | C:e02 @ 0.05 |  |
| g05 | -3.75 | CLOSING_START | C | A | C:e03 @ 0.05 | active_at_first_observation=True |
| g06 | -3.60 | TRACK_APPEARED_FRONT | A | C | A:e02 @ 0.20 |  |
| g07 | -3.60 | CLOSING_START | A | C | A:e03 @ 0.20 | active_at_first_observation=True |
| g08 | -3.45 | TRACK_APPEARED_LEFT | C | C:track_002 | C:e04 @ 0.35 |  |
| g09 | -3.45 | CLOSING_START | C | C:track_002 | C:e05 @ 0.35 | active_at_first_observation=True |
| g10 | -2.05 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e02 @ 1.75 |  |
| g11 | -2.05 | CLOSING_START | B | B:track_001 | B:e03 @ 1.75 | active_at_first_observation=True |
| g12 | -2.00 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e04 @ 1.80 | relevant_to_ego_path=False |
| g13 | -1.75 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e05 @ 2.05 |  |
| g14 | -1.70 | TRACK_APPEARED_LEFT | B | A | B:e06 @ 2.10 |  |
| g15 | -1.70 | TRACK_APPEARED_RIGHT | A | B | A:e04 @ 2.10 |  |
| g16 | -1.70 | CLOSING_START | A | B | A:e05 @ 2.10 | active_at_first_observation=True |
| g17 | -1.70 | CLOSING_START | B | A | B:e07 @ 2.10 | active_at_first_observation=True |
| g18 | -1.70 | CRITICAL_TTC_START | A | B | A:e06 @ 2.10 | active_at_first_observation=True |
| g19 | -1.70 | CRITICAL_TTC_START | B | A | B:e08 @ 2.10 | active_at_first_observation=True |
| g20 | -1.55 | TURN_LEFT_START | B | - | B:e09 @ 2.25 |  |
| g21 | -1.55 | CRITICAL_TTC_START | B | B:track_001 | B:e10 @ 2.25 |  |
| g22 | -1.30 | CRITICAL_TTC_START | A | C | A:e07 @ 2.50 |  |
| g23 | -0.95 | CRITICAL_TTC_START | C | A | C:e06 @ 2.85 |  |
| g24 | -0.85 | BRAKE_START | B | - | B:e11 @ 2.95 |  |
| g25 | -0.70 | CRITICAL_TTC_END | B | B:track_001 | B:e12 @ 3.10 |  |
| g26 | -0.30 | BRAKE_END | B | - | B:e13 @ 3.50 |  |
| g27 | -0.15 | EGO_PATH_ENTRY | B | A | B:e14 @ 3.65 |  |
| g28 | -0.05 | TRACK_LOST | A | B | A:e08 @ 3.75 |  |
| g29 | 0.00 | COLLISION | - | A, B | A:e09 @ 3.80, B:e15 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 9797.50, B 9797.50 |
| g30 | 0.00 | TURN_LEFT_END | B | - | B:e16 @ 3.80 |  |
| g31 | 0.00 | TURN_LEFT_START | A | - | A:e10 @ 3.80 |  |
| g32 | 0.05 | BRAKE_START | B | - | B:e17 @ 3.85 |  |
| g33 | 0.05 | CRITICAL_TTC_START | B | B:track_001 | B:e18 @ 3.85 |  |
| g34 | 0.20 | MOVING_END | B | - | B:e19 @ 4.00 |  |
| g35 | 0.20 | STOP_START | B | - | B:e20 @ 4.00 |  |
| g36 | 0.35 | CRITICAL_TTC_END | B | A | B:e21 @ 4.15 |  |
| g37 | 0.35 | CLOSING_END | B | A | B:e22 @ 4.15 |  |
| g38 | 0.65 | CRITICAL_TTC_END | B | B:track_001 | B:e23 @ 4.45 |  |
| g39 | 0.75 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e11 @ 4.55 | relevant_to_ego_path=False |
| g40 | 0.75 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e12 @ 4.55 |  |
| g41 | 0.85 | EGO_PATH_ENTRY | A | C | A:e13 @ 4.65 |  |
| g42 | 0.90 | EGO_PATH_EXIT | B | A | B:e24 @ 4.70 |  |
| g43 | 0.95 | COLLISION | - | A, C | A:e14 @ 4.75, C:e07 @ 4.75 | matched_event=collision_002; reference_event=False; peak_impulse=A 1637.56, C 1637.56 |
| g44 | 1.00 | CLOSING_END | C | C:track_002 | C:e08 @ 4.80 |  |
| g45 | 1.00 | BRAKE_START | C | - | C:e09 @ 4.80 |  |
| g46 | 1.10 | CLOSING_END | B | B:track_001 | B:e25 @ 4.90 |  |
| g47 | 1.15 | CRITICAL_TTC_END | C | A | C:e10 @ 4.95 |  |
| g48 | 1.15 | CLOSING_END | C | A | C:e11 @ 4.95 |  |
| g49 | 1.15 | TURN_LEFT_END | A | - | A:e15 @ 4.95 |  |
| g50 | 1.20 | CRITICAL_TTC_END | A | C | A:e16 @ 5.00 |  |
| g51 | 1.20 | CLOSING_END | A | C | A:e17 @ 5.00 |  |
| g52 | 1.25 | MOVING_END | A | - | A:e18 @ 5.05 |  |
| g53 | 1.25 | MOVING_END | C | - | C:e12 @ 5.05 |  |
| g54 | 1.25 | STOP_START | A | - | A:e19 @ 5.05 |  |
| g55 | 1.25 | STOP_START | C | - | C:e13 @ 5.05 |  |
| g56 | 1.45 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e20 @ 5.25 | relevant_to_ego_path=False |
| g57 | 3.00 | TRACK_LOST | B | A | B:e26 @ 6.80 |  |
| g58 | 3.95 | STOP_SIGN_DETECTED_END | A | A:sign-2 | A:e21 @ 7.75 |  |
| g59 | 4.85 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e22 @ 8.65 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |
| g60 | 4.85 | STOP_SIGN_DETECTED_END | A | A:sign-2 | A:e23 @ 8.65 | sign_track=sign-3 |
| g61 | 5.85 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e24 @ 9.65 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |

## Edges

```
    g01 --PRECEDES--> g04
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g04
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
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
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g13 --PRECEDES--> g18
    g13 --PRECEDES--> g19
    g14 --PRECEDES--> g20
    g14 --PRECEDES--> g21
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
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
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
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
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g42 --PRECEDES--> g43
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g47 --PRECEDES--> g51
    g48 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g53 --PRECEDES--> g56
    g54 --PRECEDES--> g56
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g58 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g60 --PRECEDES--> g61
    g06 --SAME_TRACK--> g07
    g15 --SAME_TRACK--> g16
    g15 --SAME_TRACK--> g18
    g06 --SAME_TRACK--> g22
    g15 --SAME_TRACK--> g28
    g06 --SAME_TRACK--> g41
    g06 --SAME_TRACK--> g50
    g06 --SAME_TRACK--> g51
    g10 --SAME_TRACK--> g11
    g14 --SAME_TRACK--> g17
    g14 --SAME_TRACK--> g19
    g10 --SAME_TRACK--> g21
    g10 --SAME_TRACK--> g25
    g14 --SAME_TRACK--> g27
    g10 --SAME_TRACK--> g33
    g14 --SAME_TRACK--> g36
    g14 --SAME_TRACK--> g37
    g10 --SAME_TRACK--> g38
    g14 --SAME_TRACK--> g42
    g10 --SAME_TRACK--> g46
    g14 --SAME_TRACK--> g57
    g04 --SAME_TRACK--> g05
    g08 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g23
    g08 --SAME_TRACK--> g44
    g04 --SAME_TRACK--> g47
    g04 --SAME_TRACK--> g48
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B); MOVING_START(C) |
| -3.75 | TRACK_APPEARED_FRONT(C,A); CLOSING_START(C,A) |
| -3.60 | TRACK_APPEARED_FRONT(A,C); CLOSING_START(A,C) |
| -3.45 | TRACK_APPEARED_LEFT(C,C:track_002); CLOSING_START(C,C:track_002) |
| -2.05 | TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001) |
| -2.00 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -1.75 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -1.70 | TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -1.55 | TURN_LEFT_START(B); CRITICAL_TTC_START(B,B:track_001) |
| -1.30 | CRITICAL_TTC_START(A,C) |
| -0.95 | CRITICAL_TTC_START(C,A) |
| -0.85 | BRAKE_START(B) |
| -0.70 | CRITICAL_TTC_END(B,B:track_001) |
| -0.30 | BRAKE_END(B) |
| -0.15 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A) |
| +0.05 | BRAKE_START(B); CRITICAL_TTC_START(B,B:track_001) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.35 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.65 | CRITICAL_TTC_END(B,B:track_001) |
| +0.75 | STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0) |
| +0.85 | EGO_PATH_ENTRY(A,C) |
| +0.90 | EGO_PATH_EXIT(B,A) |
| +0.95 | COLLISION(A,C) |
| +1.00 | CLOSING_END(C,C:track_002); BRAKE_START(C) |
| +1.10 | CLOSING_END(B,B:track_001) |
| +1.15 | CRITICAL_TTC_END(C,A); CLOSING_END(C,A); TURN_LEFT_END(A) |
| +1.20 | CRITICAL_TTC_END(A,C); CLOSING_END(A,C) |
| +1.25 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |
| +1.45 | STOP_SIGN_DETECTED_START(A,A:sign-2) |
| +3.00 | TRACK_LOST(B,A) |
| +3.95 | STOP_SIGN_DETECTED_END(A,A:sign-2) |
| +4.85 | STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2) |
| +5.85 | STOP_SIGN_DETECTED_START(A,A:sign-2) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (C): CRITICAL_TTC_START 2.50, COLLISION with C 4.75 (+2.25 s); EGO_PATH_ENTRY 4.65 after critical TTC (+2.15 s) [local times; t_global: critical_ttc_start -1.30, ego_path_entry +0.85, collision +0.95]
- A's track_002 (B): CRITICAL_TTC_START 2.10, COLLISION with B 3.80 (+1.70 s) [local times; t_global: critical_ttc_start -1.70, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 2.25, COLLISION 3.80 (+1.55 s) [local times; t_global: critical_ttc_start -1.55, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.10, COLLISION with A 3.80 (+1.70 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -0.15, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 2.85, COLLISION with A 4.75 (+1.90 s) [local times; t_global: critical_ttc_start -0.95, collision +0.95]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.80 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -3.80 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.80 | C | g03 MOVING_START(C) (C:e01) | ego: not yet observed |
| -3.75 | C | g04 TRACK_APPEARED_FRONT(C,A) (C:e02)<br>g05 CLOSING_START(C,A) (C:e03) | ego: MOVING |
| -3.60 | A | g06 TRACK_APPEARED_FRONT(A,C) (A:e02)<br>g07 CLOSING_START(A,C) (A:e03) | ego: MOVING |
| -3.45 | C | g08 TRACK_APPEARED_LEFT(C,C:track_002) (C:e04)<br>g09 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING |
| -2.05 | B | g10 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e02)<br>g11 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING |
| -2.00 | B | g12 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.75 | B | g13 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e05) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -1.70 | B | g14 TRACK_APPEARED_LEFT(B,A) (B:e06)<br>g17 CLOSING_START(B,A) (B:e07)<br>g19 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -1.70 | A | g15 TRACK_APPEARED_RIGHT(A,B) (A:e04)<br>g16 CLOSING_START(A,B) (A:e05)<br>g18 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| -1.55 | B | g20 TURN_LEFT_START(B) (B:e09)<br>g21 CRITICAL_TTC_START(B,B:track_001) (B:e10) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -1.30 | A | g22 CRITICAL_TTC_START(A,C) (A:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.95 | C | g23 CRITICAL_TTC_START(C,A) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -0.85 | B | g24 BRAKE_START(B) (B:e11) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.70 | B | g25 CRITICAL_TTC_END(B,B:track_001) (B:e12) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.30 | B | g26 BRAKE_END(B) (B:e13) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.15 | B | g27 EGO_PATH_ENTRY(B,A) (B:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.05 | A | g28 TRACK_LOST(A,B) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | A | g29 COLLISION(A,B) (A:e09)<br>g31 TURN_LEFT_START(A) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g29 COLLISION(A,B) (B:e15)<br>g30 TURN_LEFT_END(B) (B:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known |
| +0.05 | B | g32 BRAKE_START(B) (B:e17)<br>g33 CRITICAL_TTC_START(B,B:track_001) (B:e18) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known |
| +0.20 | B | g34 MOVING_END(B) (B:e19)<br>g35 STOP_START(B) (B:e20) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known |
| +0.35 | B | g36 CRITICAL_TTC_END(B,A) (B:e21)<br>g37 CLOSING_END(B,A) (B:e22) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known |
| +0.65 | B | g38 CRITICAL_TTC_END(B,B:track_001) (B:e23) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known |
| +0.75 | A | g39 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e11)<br>g40 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e12) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.85 | A | g41 EGO_PATH_ENTRY(A,C) (A:e13) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +0.90 | B | g42 EGO_PATH_EXIT(B,A) (B:e24) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known |
| +0.95 | A | g43 COLLISION(A,C) (A:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +0.95 | C | g43 COLLISION(A,C) (C:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| +1.00 | C | g44 CLOSING_END(C,C:track_002) (C:e08)<br>g45 BRAKE_START(C) (C:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| +1.10 | B | g46 CLOSING_END(B,B:track_001) (B:e25) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>sign-0: STOP sign known |
| +1.15 | C | g47 CRITICAL_TTC_END(C,A) (C:e10)<br>g48 CLOSING_END(C,A) (C:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state |
| +1.15 | A | g49 TURN_LEFT_END(A) (A:e15) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.20 | A | g50 CRITICAL_TTC_END(A,C) (A:e16)<br>g51 CLOSING_END(A,C) (A:e17) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.25 | A | g52 MOVING_END(A) (A:e18)<br>g54 STOP_START(A) (A:e19) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.25 | C | g53 MOVING_END(C) (C:e12)<br>g55 STOP_START(C) (C:e13) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.45 | A | g56 STOP_SIGN_DETECTED_START(A,A:sign-2) (A:e20) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +3.00 | B | g57 TRACK_LOST(B,A) (B:e26) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>sign-0: STOP sign known |
| +3.95 | A | g58 STOP_SIGN_DETECTED_END(A,A:sign-2) (A:e21) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |
| +4.85 | A | g59 STOP_SIGN_DETECTED_START(A,A:sign-2) (A:e22)<br>g60 STOP_SIGN_DETECTED_END(A,A:sign-2) (A:e23) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |
| +5.85 | A | g61 STOP_SIGN_DETECTED_START(A,A:sign-2) (A:e24) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |

## Plain-language reading

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 3.80 s before the reference collision, C started moving (already the case when first observed).
- 3.75 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 3.75 s before the reference collision, C observed A start closing in (already the case when first observed).
- 3.60 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 3.60 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.45 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared on its left.
- 3.45 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 2.05 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.05 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.00 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.75 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.70 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.70 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.70 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.70 s before the reference collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the reference collision, B's time-to-contact with A became critical (already the case when first observed).
- 1.55 s before the reference collision, B started turning left.
- 1.55 s before the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.30 s before the reference collision, A's time-to-contact with C became critical.
- 0.95 s before the reference collision, C's time-to-contact with A became critical.
- 0.85 s before the reference collision, B started braking.
- 0.70 s before the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 0.30 s before the reference collision, B released the brake.
- 0.15 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the reference collision, B stopped turning left.
- At the reference collision, A started turning left.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.35 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.35 s after the reference collision, B observed A stop closing in.
- 0.65 s after the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 0.75 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.75 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 0.85 s after the reference collision, A observed C enter its forward path corridor.
- 0.90 s after the reference collision, B observed A leave its forward path corridor.
- 0.95 s after the reference collision, A and C both recorded this same collision (peak impulses A: 1638, C: 1638 N*s).
- 1.00 s after the reference collision, C observed unidentified object C:track_002 stop closing in.
- 1.00 s after the reference collision, C started braking.
- 1.10 s after the reference collision, B observed unidentified object B:track_001 stop closing in.
- 1.15 s after the reference collision, C's time-to-contact with A stopped being critical.
- 1.15 s after the reference collision, C observed A stop closing in.
- 1.15 s after the reference collision, A stopped turning left.
- 1.20 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.20 s after the reference collision, A observed C stop closing in.
- 1.25 s after the reference collision, A stopped moving.
- 1.25 s after the reference collision, C stopped moving.
- 1.25 s after the reference collision, A came to a stop.
- 1.25 s after the reference collision, C came to a stop.
- 1.45 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path).
- 3.00 s after the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 3.95 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 4.85 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- 4.85 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 5.85 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
