# Global graph - S15/run_0_single_impact

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |
| C:track_003 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 65.9 m -> 53.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.99 m/s over 2.5 s (> 1.50)<br>clearance at the contact 53.92 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.64 m/s over 1.6 s<br>clearance at the contact 0.75 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.0 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.49 m/s over 1.7 s<br>clearance at the contact 0.19 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.90 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 52.4 m -> 53.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 8.54 m/s over 0.9 s (> 1.50)<br>clearance at the contact 52.33 m (beyond 3.50 m: confidence factor 0.00) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_003 | C:track_003 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -2.55 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 1.25 |  |
| g04 | -2.55 | CLOSING_START | A | A:track_001 | A:e03 @ 1.25 | active_at_first_observation=True |
| g05 | -2.05 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 1.75 | relevant_to_ego_path=False |
| g06 | -1.75 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e03 @ 2.05 |  |
| g07 | -1.70 | TRACK_APPEARED_LEFT | B | A | B:e04 @ 2.10 |  |
| g08 | -1.70 | TRACK_APPEARED_RIGHT | A | B | A:e04 @ 2.10 |  |
| g09 | -1.70 | CLOSING_START | A | B | A:e05 @ 2.10 | active_at_first_observation=True |
| g10 | -1.70 | CLOSING_START | B | A | B:e05 @ 2.10 | active_at_first_observation=True |
| g11 | -1.70 | CRITICAL_TTC_START | A | B | A:e06 @ 2.10 | active_at_first_observation=True |
| g12 | -1.70 | CRITICAL_TTC_START | B | A | B:e06 @ 2.10 | active_at_first_observation=True |
| g13 | -1.55 | TURN_LEFT_START | B | - | B:e07 @ 2.25 |  |
| g14 | -0.90 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e08 @ 2.90 |  |
| g15 | -0.85 | BRAKE_START | B | - | B:e09 @ 2.95 |  |
| g16 | -0.30 | BRAKE_END | B | - | B:e10 @ 3.50 |  |
| g17 | -0.15 | EGO_PATH_ENTRY | B | A | B:e11 @ 3.65 |  |
| g18 | -0.05 | TRACK_LOST | A | B | A:e07 @ 3.75 |  |
| g19 | 0.00 | COLLISION | - | A, B | A:e08 @ 3.80, B:e12 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 9797.50, B 9797.50 |
| g20 | 0.00 | TURN_LEFT_END | B | - | B:e13 @ 3.80 |  |
| g21 | 0.00 | TURN_LEFT_START | A | - | A:e09 @ 3.80 |  |
| g22 | 0.00 | EGO_PATH_ENTRY | A | A:track_001 | A:e10 @ 3.80 |  |
| g23 | 0.00 | CLOSING_START | B | B:track_002 | B:e14 @ 3.80 |  |
| g24 | 0.05 | EGO_PATH_EXIT | A | A:track_001 | A:e11 @ 3.85 |  |
| g25 | 0.05 | BRAKE_START | B | - | B:e15 @ 3.85 |  |
| g26 | 0.20 | MOVING_END | B | - | B:e16 @ 4.00 |  |
| g27 | 0.20 | STOP_START | B | - | B:e17 @ 4.00 |  |
| g28 | 0.25 | EGO_PATH_ENTRY | A | A:track_001 | A:e12 @ 4.05 |  |
| g29 | 0.35 | CRITICAL_TTC_END | B | A | B:e18 @ 4.15 |  |
| g30 | 0.35 | CLOSING_END | B | A | B:e19 @ 4.15 |  |
| g31 | 0.50 | EGO_PATH_EXIT | A | A:track_001 | A:e13 @ 4.30 |  |
| g32 | 0.75 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e14 @ 4.55 | relevant_to_ego_path=False |
| g33 | 0.85 | EGO_PATH_EXIT | B | A | B:e20 @ 4.65 |  |
| g34 | 1.25 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e15 @ 5.05 |  |
| g35 | 1.40 | TURN_LEFT_END | A | - | A:e16 @ 5.20 |  |
| g36 | 6.75 | STOP_SIGN_DETECTED_START | A | A:sign-1 | A:e17 @ 10.55 | relevant_to_ego_path=False |
| g37 | 7.75 | MOVING_END | A | - | A:e18 @ 11.55 |  |
| g38 | 7.75 | STOP_START | A | - | A:e19 @ 11.55 |  |
| g39 | 9.60 | CRITICAL_TTC_START | A | A:track_001 | A:e20 @ 13.40 |  |
| g40 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g41 | - | TRACK_APPEARED_LEFT | C | C:track_001 | C:e02 @ 0.40 |  |
| g42 | - | CLOSING_START | C | C:track_001 | C:e03 @ 0.40 | active_at_first_observation=True |
| g43 | - | TRACK_APPEARED_FRONT | C | C:track_002 | C:e04 @ 1.25 |  |
| g44 | - | CLOSING_START | C | C:track_002 | C:e05 @ 1.25 | active_at_first_observation=True |
| g45 | - | TRACK_LOST | C | C:track_001 | C:e06 @ 2.25 |  |
| g46 | - | STOP_SIGN_DETECTED_START | C | C:sign-0 | C:e07 @ 2.80 | relevant_to_ego_path=False |
| g47 | - | STOP_SIGN_DETECTED_END | C | C:sign-0 | C:e08 @ 2.80 |  |
| g48 | - | TRACK_APPEARED_LEFT | C | C:track_003 | C:e09 @ 3.15 |  |
| g49 | - | CLOSING_START | C | C:track_003 | C:e10 @ 3.90 |  |
| g50 | - | EGO_PATH_ENTRY | C | C:track_002 | C:e11 @ 5.20 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g06 --PRECEDES--> g10
    g06 --PRECEDES--> g11
    g06 --PRECEDES--> g12
    g07 --PRECEDES--> g13
    g08 --PRECEDES--> g13
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g19 --PRECEDES--> g25
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g39
    g03 --SAME_TRACK--> g04
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g22
    g03 --SAME_TRACK--> g24
    g03 --SAME_TRACK--> g28
    g03 --SAME_TRACK--> g31
    g03 --SAME_TRACK--> g39
    g07 --SAME_TRACK--> g10
    g07 --SAME_TRACK--> g12
    g07 --SAME_TRACK--> g17
    g14 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g29
    g07 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g33
    g41 --SAME_TRACK--> g42
    g43 --SAME_TRACK--> g44
    g41 --SAME_TRACK--> g45
    g48 --SAME_TRACK--> g49
    g43 --SAME_TRACK--> g50
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B) |
| -2.55 | TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.05 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -1.75 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -1.70 | TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -1.55 | TURN_LEFT_START(B) |
| -0.90 | TRACK_APPEARED_RIGHT(B,B:track_002) |
| -0.85 | BRAKE_START(B) |
| -0.30 | BRAKE_END(B) |
| -0.15 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001); CLOSING_START(B,B:track_002) |
| +0.05 | EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.25 | EGO_PATH_ENTRY(A,A:track_001) |
| +0.35 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.50 | EGO_PATH_EXIT(A,A:track_001) |
| +0.75 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| +0.85 | EGO_PATH_EXIT(B,A) |
| +1.25 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| +1.40 | TURN_LEFT_END(A) |
| +6.75 | STOP_SIGN_DETECTED_START(A,A:sign-1) |
| +7.75 | MOVING_END(A); STOP_START(A) |
| +9.60 | CRITICAL_TTC_START(A,A:track_001) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 13.40; EGO_PATH_ENTRY 3.80 before critical TTC (-9.60 s) [local times; t_global: critical_ttc_start +9.60, ego_path_entry +0.00]
- A's track_002 (B): CRITICAL_TTC_START 2.10, COLLISION with B 3.80 (+1.70 s) [local times; t_global: critical_ttc_start -1.70, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.10, COLLISION with A 3.80 (+1.70 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -0.15, collision +0.00]
- C's track_002 (unidentified C:track_002): EGO_PATH_ENTRY 5.20, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.80 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -3.80 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -2.55 | A | g03 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02)<br>g04 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| -2.05 | B | g05 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| -1.75 | B | g06 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e03) | ego: MOVING<br>sign-0: STOP sign known |
| -1.70 | B | g07 TRACK_APPEARED_LEFT(B,A) (B:e04)<br>g10 CLOSING_START(B,A) (B:e05)<br>g12 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING<br>sign-0: STOP sign known |
| -1.70 | A | g08 TRACK_APPEARED_RIGHT(A,B) (A:e04)<br>g09 CLOSING_START(A,B) (A:e05)<br>g11 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| -1.55 | B | g13 TURN_LEFT_START(B) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.90 | B | g14 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e08) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.85 | B | g15 BRAKE_START(B) (B:e09) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>sign-0: STOP sign known |
| -0.30 | B | g16 BRAKE_END(B) (B:e10) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>sign-0: STOP sign known |
| -0.15 | B | g17 EGO_PATH_ENTRY(B,A) (B:e11) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>sign-0: STOP sign known |
| -0.05 | A | g18 TRACK_LOST(A,B) (A:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | A | g19 COLLISION(A,B) (A:e08)<br>g21 TURN_LEFT_START(A) (A:e09)<br>g22 EGO_PATH_ENTRY(A,A:track_001) (A:e10) | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g19 COLLISION(A,B) (B:e12)<br>g20 TURN_LEFT_END(B) (B:e13)<br>g23 CLOSING_START(B,B:track_002) (B:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>sign-0: STOP sign known |
| +0.05 | A | g24 EGO_PATH_EXIT(A,A:track_001) (A:e11) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.05 | B | g25 BRAKE_START(B) (B:e15) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known |
| +0.20 | B | g26 MOVING_END(B) (B:e16)<br>g27 STOP_START(B) (B:e17) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known |
| +0.25 | A | g28 EGO_PATH_ENTRY(A,A:track_001) (A:e12) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| +0.35 | B | g29 CRITICAL_TTC_END(B,A) (B:e18)<br>g30 CLOSING_END(B,A) (B:e19) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known |
| +0.50 | A | g31 EGO_PATH_EXIT(A,A:track_001) (A:e13) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.75 | A | g32 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| +0.85 | B | g33 EGO_PATH_EXIT(B,A) (B:e20) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known |
| +1.25 | A | g34 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e15) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.40 | A | g35 TURN_LEFT_END(A) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +6.75 | A | g36 STOP_SIGN_DETECTED_START(A,A:sign-1) (A:e17) | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +7.75 | A | g37 MOVING_END(A) (A:e18)<br>g38 STOP_START(A) (A:e19) | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| +9.60 | A | g39 CRITICAL_TTC_START(A,A:track_001) (A:e20) | ego: STOP<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | C | g40 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g41 TRACK_APPEARED_LEFT(C,C:track_001) (C:e02)<br>g42 CLOSING_START(C,C:track_001) (C:e03) | ego: MOVING |
| - | C | g43 TRACK_APPEARED_FRONT(C,C:track_002) (C:e04)<br>g44 CLOSING_START(C,C:track_002) (C:e05) | ego: MOVING<br>track_001: CLOSING |
| - | C | g45 TRACK_LOST(C,C:track_001) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g46 STOP_SIGN_DETECTED_START(C,C:sign-0) (C:e07)<br>g47 STOP_SIGN_DETECTED_END(C,C:sign-0) (C:e08) | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| - | C | g48 TRACK_APPEARED_LEFT(C,C:track_003) (C:e09) | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | C | g49 CLOSING_START(C,C:track_003) (C:e10) | ego: MOVING<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| - | C | g50 EGO_PATH_ENTRY(C,C:track_002) (C:e11) | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |

## Plain-language reading

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 2.55 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 2.55 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.05 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.75 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.70 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.70 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.70 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.70 s before the reference collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the reference collision, B's time-to-contact with A became critical (already the case when first observed).
- 1.55 s before the reference collision, B started turning left.
- 0.90 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 0.85 s before the reference collision, B started braking.
- 0.30 s before the reference collision, B released the brake.
- 0.15 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the reference collision, B stopped turning left.
- At the reference collision, A started turning left.
- At the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- At the reference collision, B observed unidentified object B:track_002 start closing in.
- 0.05 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.25 s after the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.35 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.35 s after the reference collision, B observed A stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.75 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.85 s after the reference collision, B observed A leave its forward path corridor.
- 1.25 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 1.40 s after the reference collision, A stopped turning left.
- 6.75 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 7.75 s after the reference collision, A stopped moving.
- 7.75 s after the reference collision, A came to a stop.
- 9.60 s after the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.40 s) C's radar started tracking unidentified object C:track_001, which appeared on its left.
- (unaligned, C local time 0.40 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 1.25 s) C's radar started tracking unidentified object C:track_002, which appeared in front of it.
- (unaligned, C local time 1.25 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.25 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 2.80 s) C's camera established a STOP sign detection (unidentified object C:sign-0) (the detector judged it not relevant to its path).
- (unaligned, C local time 2.80 s) C's camera stopped detecting STOP sign unidentified object C:sign-0.
- (unaligned, C local time 3.15 s) C's radar started tracking unidentified object C:track_003, which appeared on its left.
- (unaligned, C local time 3.90 s) C observed unidentified object C:track_003 start closing in.
- (unaligned, C local time 5.20 s) C observed unidentified object C:track_002 enter its forward path corridor.
