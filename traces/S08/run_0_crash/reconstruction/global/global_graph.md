# Global graph - S08/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 4.10 | -4.10 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.10 | -4.10 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12137.11 vs 12137.11 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 4.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 21.7 m -> 11.7 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.47 m/s over 3.0 s (> 1.50)<br>clearance at the contact 11.69 m (beyond 3.50 m: confidence factor 0.02) |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.65 m/s over 2.0 s<br>clearance at the contact 0.35 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.6 m -> 10.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 7.61 m/s over 2.0 s (> 1.50)<br>clearance at the contact 10.71 m (beyond 3.50 m: confidence factor 0.06) |
| B:track_002 | A | ASSOCIATED | 0.89 | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.2 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.71 m/s over 2.0 s<br>clearance at the contact 0.46 m<br>the only track of B compatible with the contact |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.10 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.10 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -4.10 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -4.10 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e03 @ 0.00 |  |
| g06 | -4.10 | CLOSING_START | A | A:track_001 | A:e04 @ 0.00 | active_at_first_observation=True |
| g07 | -2.05 | TRACK_APPEARED_RIGHT | A | B | A:e05 @ 2.05 |  |
| g08 | -2.05 | CLOSING_START | A | B | A:e06 @ 2.05 | active_at_first_observation=True |
| g09 | -2.00 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 2.10 |  |
| g10 | -2.00 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e04 @ 2.10 |  |
| g11 | -2.00 | CLOSING_START | B | A | B:e06 @ 2.10 | active_at_first_observation=True |
| g12 | -2.00 | CLOSING_START | B | B:track_001 | B:e05 @ 2.10 | active_at_first_observation=True |
| g13 | -1.55 | CRITICAL_TTC_START | A | B | A:e07 @ 2.55 |  |
| g14 | -1.50 | CRITICAL_TTC_START | B | A | B:e07 @ 2.60 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e08 @ 4.10, B:e08 @ 4.10 | matched_event=collision_001; reference_event=True; peak_impulse=A 12137.11, B 12137.11 |
| g16 | 0.00 | CLOSING_END | A | B | A:e09 @ 4.10 |  |
| g17 | 0.00 | CLOSING_END | B | A | B:e09 @ 4.10 |  |
| g18 | 0.00 | TURN_LEFT_START | A | - | A:e10 @ 4.10 |  |
| g19 | 0.00 | TURN_RIGHT_START | B | - | B:e10 @ 4.10 |  |
| g20 | 0.05 | THROTTLE_END | A | - | A:e11 @ 4.15 |  |
| g21 | 0.05 | THROTTLE_END | B | - | B:e11 @ 4.15 |  |
| g22 | 0.05 | BRAKE_START | A | - | A:e12 @ 4.15 |  |
| g23 | 0.05 | BRAKE_START | B | - | B:e12 @ 4.15 |  |
| g24 | 0.05 | EGO_PATH_ENTRY | A | A:track_001 | A:e13 @ 4.15 |  |
| g25 | 0.15 | EGO_PATH_EXIT | A | A:track_001 | A:e14 @ 4.25 |  |
| g26 | 0.15 | CLOSING_START | A | B | A:e15 @ 4.25 |  |
| g27 | 0.15 | CLOSING_START | B | A | B:e13 @ 4.25 |  |
| g28 | 0.45 | CRITICAL_TTC_END | A | B | A:e16 @ 4.55 |  |
| g29 | 0.50 | CLOSING_END | B | B:track_001 | B:e14 @ 4.60 |  |
| g30 | 0.50 | TURN_RIGHT_END | B | - | B:e15 @ 4.60 |  |
| g31 | 0.50 | MOVING_END | B | - | B:e16 @ 4.60 |  |
| g32 | 0.50 | STOP_START | B | - | B:e17 @ 4.60 |  |
| g33 | 0.55 | CRITICAL_TTC_END | B | A | B:e18 @ 4.65 |  |
| g34 | 0.55 | CLOSING_END | A | B | A:e17 @ 4.65 |  |
| g35 | 0.60 | TURN_LEFT_END | A | - | A:e18 @ 4.70 |  |
| g36 | 0.65 | CLOSING_END | A | A:track_001 | A:e19 @ 4.75 |  |
| g37 | 0.65 | CLOSING_END | B | A | B:e19 @ 4.75 |  |
| g38 | 0.65 | MOVING_END | A | - | A:e20 @ 4.75 |  |
| g39 | 0.65 | STOP_START | A | - | A:e21 @ 4.75 |  |
| g40 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g41 | - | THROTTLE_START | C | - | C:e02 @ 0.00 | active_at_first_observation=True |
| g42 | - | TRACK_APPEARED_FRONT | C | C:track_001 | C:e03 @ 0.00 |  |
| g43 | - | CLOSING_START | C | C:track_001 | C:e04 @ 0.00 | active_at_first_observation=True |
| g44 | - | TRACK_APPEARED_LEFT | C | C:track_002 | C:e05 @ 2.10 |  |
| g45 | - | CLOSING_START | C | C:track_002 | C:e06 @ 2.10 | active_at_first_observation=True |
| g46 | - | THROTTLE_END | C | - | C:e07 @ 2.35 |  |
| g47 | - | BRAKE_START | C | - | C:e08 @ 2.35 |  |
| g48 | - | MOVING_END | C | - | C:e09 @ 2.90 |  |
| g49 | - | STOP_START | C | - | C:e10 @ 2.90 |  |
| g50 | - | CLOSING_END | C | C:track_001 | C:e11 @ 4.65 |  |
| g51 | - | EGO_PATH_ENTRY | C | C:track_002 | C:e12 @ 4.65 |  |
| g52 | - | CLOSING_END | C | C:track_002 | C:e13 @ 4.75 |  |
| g53 | - | TRACK_LOST | C | C:track_002 | C:e14 @ 5.80 |  |
| g54 | - | EGO_PATH_ENTRY | C | C:track_001 | C:e15 @ 6.35 |  |

## Edges

```
    g01 --PRECEDES--> g07
    g01 --PRECEDES--> g08
    g02 --PRECEDES--> g07
    g02 --PRECEDES--> g08
    g03 --PRECEDES--> g07
    g03 --PRECEDES--> g08
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g07 --PRECEDES--> g11
    g07 --PRECEDES--> g12
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g14 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g15 --PRECEDES--> g22
    g15 --PRECEDES--> g23
    g15 --PRECEDES--> g24
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g16 --PRECEDES--> g22
    g16 --PRECEDES--> g23
    g16 --PRECEDES--> g24
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g18 --PRECEDES--> g24
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g05 --SAME_TRACK--> g06
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g13
    g07 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g24
    g05 --SAME_TRACK--> g25
    g07 --SAME_TRACK--> g26
    g07 --SAME_TRACK--> g28
    g07 --SAME_TRACK--> g34
    g05 --SAME_TRACK--> g36
    g10 --SAME_TRACK--> g12
    g09 --SAME_TRACK--> g11
    g09 --SAME_TRACK--> g14
    g09 --SAME_TRACK--> g17
    g09 --SAME_TRACK--> g27
    g10 --SAME_TRACK--> g29
    g09 --SAME_TRACK--> g33
    g09 --SAME_TRACK--> g37
    g42 --SAME_TRACK--> g43
    g44 --SAME_TRACK--> g45
    g42 --SAME_TRACK--> g50
    g44 --SAME_TRACK--> g51
    g44 --SAME_TRACK--> g52
    g44 --SAME_TRACK--> g53
    g42 --SAME_TRACK--> g54
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.10 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.05 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -2.00 | TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,A); CLOSING_START(B,B:track_001) |
| -1.55 | CRITICAL_TTC_START(A,B) |
| -1.50 | CRITICAL_TTC_START(B,A) |
| +0.00 | COLLISION(A,B); CLOSING_END(A,B); CLOSING_END(B,A); TURN_LEFT_START(A); TURN_RIGHT_START(B) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); EGO_PATH_ENTRY(A,A:track_001) |
| +0.15 | EGO_PATH_EXIT(A,A:track_001); CLOSING_START(A,B); CLOSING_START(B,A) |
| +0.45 | CRITICAL_TTC_END(A,B) |
| +0.50 | CLOSING_END(B,B:track_001); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B) |
| +0.55 | CRITICAL_TTC_END(B,A); CLOSING_END(A,B) |
| +0.60 | TURN_LEFT_END(A) |
| +0.65 | CLOSING_END(A,A:track_001); CLOSING_END(B,A); MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): EGO_PATH_ENTRY 4.15, no critical TTC [local times; t_global: ego_path_entry +0.05]
- A's track_002 (B): CRITICAL_TTC_START 2.55, COLLISION with B 4.10 (+1.55 s) [local times; t_global: critical_ttc_start -1.55, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.60, COLLISION with A 4.10 (+1.50 s) [local times; t_global: critical_ttc_start -1.50, collision +0.00]
- C's track_001 (unidentified C:track_001): EGO_PATH_ENTRY 6.35, no critical TTC [local times]
- C's track_002 (unidentified C:track_002): EGO_PATH_ENTRY 4.65, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.10 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,A:track_001) (A:e03)<br>g06 CLOSING_START(A,A:track_001) (A:e04) | ego: not yet observed |
| -4.10 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -2.05 | A | g07 TRACK_APPEARED_RIGHT(A,B) (A:e05)<br>g08 CLOSING_START(A,B) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.00 | B | g09 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g10 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e04)<br>g11 CLOSING_START(B,A) (B:e06)<br>g12 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING, THROTTLE |
| -1.55 | A | g13 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.50 | B | g14 CRITICAL_TTC_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? |
| +0.00 | A | g15 COLLISION(A,B) (A:e08)<br>g16 CLOSING_END(A,B) (A:e09)<br>g18 TURN_LEFT_START(A) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | B | g15 COLLISION(A,B) (B:e08)<br>g17 CLOSING_END(B,A) (B:e09)<br>g19 TURN_RIGHT_START(B) (B:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.05 | A | g20 THROTTLE_END(A) (A:e11)<br>g22 BRAKE_START(A) (A:e12)<br>g24 EGO_PATH_ENTRY(A,A:track_001) (A:e13) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CRITICAL_TTC |
| +0.05 | B | g21 THROTTLE_END(B) (B:e11)<br>g23 BRAKE_START(B) (B:e12) | ego: MOVING, THROTTLE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CRITICAL_TTC |
| +0.15 | A | g25 EGO_PATH_EXIT(A,A:track_001) (A:e14)<br>g26 CLOSING_START(A,B) (A:e15) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CRITICAL_TTC |
| +0.15 | B | g27 CLOSING_START(B,A) (B:e13) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CRITICAL_TTC |
| +0.45 | A | g28 CRITICAL_TTC_END(A,B) (A:e16) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.50 | B | g29 CLOSING_END(B,B:track_001) (B:e14)<br>g30 TURN_RIGHT_END(B) (B:e15)<br>g31 MOVING_END(B) (B:e16)<br>g32 STOP_START(B) (B:e17) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.55 | B | g33 CRITICAL_TTC_END(B,A) (B:e18) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC |
| +0.55 | A | g34 CLOSING_END(A,B) (A:e17) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING |
| +0.60 | A | g35 TURN_LEFT_END(A) (A:e18) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: no active state |
| +0.65 | A | g36 CLOSING_END(A,A:track_001) (A:e19)<br>g38 MOVING_END(A) (A:e20)<br>g39 STOP_START(A) (A:e21) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state |
| +0.65 | B | g37 CLOSING_END(B,A) (B:e19) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: CLOSING |
| - | C | g40 MOVING_START(C) (C:e01)<br>g41 THROTTLE_START(C) (C:e02)<br>g42 TRACK_APPEARED_FRONT(C,C:track_001) (C:e03)<br>g43 CLOSING_START(C,C:track_001) (C:e04) | ego: not yet observed |
| - | C | g44 TRACK_APPEARED_LEFT(C,C:track_002) (C:e05)<br>g45 CLOSING_START(C,C:track_002) (C:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| - | C | g46 THROTTLE_END(C) (C:e07)<br>g47 BRAKE_START(C) (C:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| - | C | g48 MOVING_END(C) (C:e09)<br>g49 STOP_START(C) (C:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g50 CLOSING_END(C,C:track_001) (C:e11)<br>g51 EGO_PATH_ENTRY(C,C:track_002) (C:e12) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g52 CLOSING_END(C,C:track_002) (C:e13) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: CLOSING, IN_EGO_PATH |
| - | C | g53 TRACK_LOST(C,C:track_002) (C:e14) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH |
| - | C | g54 EGO_PATH_ENTRY(C,C:track_001) (C:e15) | ego: STOP, BRAKE<br>track_001: no active state<br>track lost, states UNKNOWN: track_002 |

## Plain-language reading

- 4.10 s before the reference collision, A started moving (already the case when first observed).
- 4.10 s before the reference collision, B started moving (already the case when first observed).
- 4.10 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 4.10 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.05 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 2.05 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.00 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.00 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.00 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.00 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 1.55 s before the reference collision, A's time-to-contact with B became critical.
- 1.50 s before the reference collision, B's time-to-contact with A became critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12137, B: 12137 N*s).
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- At the reference collision, A started turning left.
- At the reference collision, B started turning right.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.15 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.15 s after the reference collision, A observed B start closing in.
- 0.15 s after the reference collision, B observed A start closing in.
- 0.45 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.50 s after the reference collision, B observed unidentified object B:track_001 stop closing in.
- 0.50 s after the reference collision, B stopped turning right.
- 0.50 s after the reference collision, B stopped moving.
- 0.50 s after the reference collision, B came to a stop.
- 0.55 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.55 s after the reference collision, A observed B stop closing in.
- 0.60 s after the reference collision, A stopped turning left.
- 0.65 s after the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.65 s after the reference collision, B observed A stop closing in.
- 0.65 s after the reference collision, A stopped moving.
- 0.65 s after the reference collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C pressed the accelerator (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.10 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 2.10 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.35 s) C released the accelerator.
- (unaligned, C local time 2.35 s) C started braking.
- (unaligned, C local time 2.90 s) C stopped moving.
- (unaligned, C local time 2.90 s) C came to a stop.
- (unaligned, C local time 4.65 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 4.65 s) C observed unidentified object C:track_002 enter its forward path corridor.
- (unaligned, C local time 4.75 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 5.80 s) C's radar lost unidentified object C:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 6.35 s) C observed unidentified object C:track_001 enter its forward path corridor.
