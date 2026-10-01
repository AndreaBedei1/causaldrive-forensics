# Global graph - S08/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e11 | 4.25 | -4.25 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 4.20 s before the matched collision<br>not at the contact: minimum range 11.23 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 8.94 m/s (> 1.50) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>not at the contact: last seen 0.90 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.45 m/s over 1.3 s |
| B:track_001 | A | ASSOCIATED | 0.84 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>at the contact: minimum range 0.93 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.89 m/s over 2.1 s |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.05 s before the matched collision<br>not at the contact: minimum range 14.00 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with A's own speed: RMSE 7.21 m/s (> 1.50) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.20 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.05 |  |
| g04 | -4.20 | CLOSING_START | A | A:track_001 | A:e03 @ 0.05 | active_at_first_observation=True |
| g05 | -3.10 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.15 |  |
| g06 | -2.20 | TRACK_APPEARED_RIGHT | A | A:track_002 | A:e04 @ 2.05 |  |
| g07 | -2.20 | CLOSING_START | A | A:track_002 | A:e05 @ 2.05 | active_at_first_observation=True |
| g08 | -2.15 | CRITICAL_TTC_START | A | A:track_001 | A:e06 @ 2.10 |  |
| g09 | -2.10 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 2.15 |  |
| g10 | -2.10 | CLOSING_START | B | A | B:e04 @ 2.15 | active_at_first_observation=True |
| g11 | -2.05 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e05 @ 2.20 |  |
| g12 | -2.05 | CLOSING_START | B | B:track_002 | B:e06 @ 2.20 | active_at_first_observation=True |
| g13 | -1.90 | CRITICAL_TTC_START | A | A:track_002 | A:e07 @ 2.35 |  |
| g14 | -1.90 | CRITICAL_TTC_START | B | A | B:e07 @ 2.35 |  |
| g15 | -1.85 | STRONG_THROTTLE_END | B | - | B:e08 @ 2.40 |  |
| g16 | -1.55 | CRITICAL_TTC_END | A | A:track_001 | A:e08 @ 2.70 |  |
| g17 | -0.90 | TRACK_LOST | A | A:track_002 | A:e09 @ 3.35 |  |
| g18 | -0.80 | CRITICAL_TTC_START | A | A:track_001 | A:e10 @ 3.45 |  |
| g19 | -0.20 | TRACK_LOST | B | B:track_002 | B:e09 @ 4.05 |  |
| g20 | -0.15 | EGO_PATH_ENTRY | B | A | B:e10 @ 4.10 |  |
| g21 | 0.00 | COLLISION | - | A, B | A:e11 @ 4.25, B:e11 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12077.22, B 12077.22 |
| g22 | 0.00 | STRONG_THROTTLE_START | B | - | B:e12 @ 4.25 |  |
| g23 | 0.05 | CRITICAL_TTC_END | B | A | B:e13 @ 4.30 |  |
| g24 | 0.05 | CLOSING_END | B | A | B:e14 @ 4.30 |  |
| g25 | 0.05 | STRONG_THROTTLE_END | B | - | B:e15 @ 4.30 |  |
| g26 | 0.05 | BRAKE_START | A | - | A:e12 @ 4.30 |  |
| g27 | 0.05 | BRAKE_START | B | - | B:e16 @ 4.30 |  |
| g28 | 0.05 | HARD_BRAKE_START | A | - | A:e13 @ 4.30 |  |
| g29 | 0.05 | HARD_BRAKE_START | B | - | B:e17 @ 4.30 |  |
| g30 | 0.30 | MOVING_END | B | - | B:e18 @ 4.55 |  |
| g31 | 0.30 | STOP_START | B | - | B:e19 @ 4.55 |  |
| g32 | 0.45 | EGO_PATH_EXIT | B | A | B:e20 @ 4.70 |  |
| g33 | 0.50 | CRITICAL_TTC_END | A | A:track_001 | A:e14 @ 4.75 |  |
| g34 | 0.65 | CLOSING_END | A | A:track_001 | A:e15 @ 4.90 |  |
| g35 | 0.65 | MOVING_END | A | - | A:e16 @ 4.90 |  |
| g36 | 0.65 | STOP_START | A | - | A:e17 @ 4.90 |  |
| g37 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g38 | - | TRACK_APPEARED_FRONT | C | C:track_001 | C:e02 @ 0.05 |  |
| g39 | - | CLOSING_START | C | C:track_001 | C:e03 @ 0.05 | active_at_first_observation=True |
| g40 | - | CRITICAL_TTC_START | C | C:track_001 | C:e04 @ 2.15 |  |
| g41 | - | BRAKE_START | C | - | C:e05 @ 2.35 |  |
| g42 | - | HARD_BRAKE_START | C | - | C:e06 @ 2.35 |  |
| g43 | - | CRITICAL_TTC_END | C | C:track_001 | C:e07 @ 2.75 |  |
| g44 | - | MOVING_END | C | - | C:e08 @ 2.85 |  |
| g45 | - | STOP_START | C | - | C:e09 @ 2.85 |  |
| g46 | - | TRACK_APPEARED_LEFT | C | C:track_002 | C:e10 @ 3.00 |  |
| g47 | - | CLOSING_START | C | C:track_002 | C:e11 @ 3.00 | active_at_first_observation=True |
| g48 | - | CRITICAL_TTC_START | C | C:track_002 | C:e12 @ 3.35 |  |
| g49 | - | CRITICAL_TTC_START | C | C:track_001 | C:e13 @ 3.55 |  |
| g50 | - | CRITICAL_TTC_END | C | C:track_002 | C:e14 @ 4.20 |  |
| g51 | - | CLOSING_END | C | C:track_002 | C:e15 @ 4.55 |  |
| g52 | - | CRITICAL_TTC_END | C | C:track_001 | C:e16 @ 4.70 |  |
| g53 | - | CLOSING_END | C | C:track_001 | C:e17 @ 4.90 |  |
| g54 | - | HARD_BRAKE_END | C | - | C:e18 @ 14.35 |  |
| g55 | - | BRAKE_END | C | - | C:e19 @ 14.35 |  |
| g56 | - | STRONG_THROTTLE_START | C | - | C:e20 @ 14.35 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g21 --PRECEDES--> g29
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g23 --PRECEDES--> g31
    g24 --PRECEDES--> g30
    g24 --PRECEDES--> g31
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g03 --SAME_TRACK--> g04
    g06 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g06 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g16
    g06 --SAME_TRACK--> g17
    g03 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g33
    g03 --SAME_TRACK--> g34
    g09 --SAME_TRACK--> g10
    g11 --SAME_TRACK--> g12
    g09 --SAME_TRACK--> g14
    g11 --SAME_TRACK--> g19
    g09 --SAME_TRACK--> g20
    g09 --SAME_TRACK--> g23
    g09 --SAME_TRACK--> g24
    g09 --SAME_TRACK--> g32
    g38 --SAME_TRACK--> g39
    g38 --SAME_TRACK--> g40
    g38 --SAME_TRACK--> g43
    g46 --SAME_TRACK--> g47
    g46 --SAME_TRACK--> g48
    g38 --SAME_TRACK--> g49
    g46 --SAME_TRACK--> g50
    g46 --SAME_TRACK--> g51
    g38 --SAME_TRACK--> g52
    g38 --SAME_TRACK--> g53
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B) |
| -4.20 | TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -3.10 | STRONG_THROTTLE_START(B) |
| -2.20 | TRACK_APPEARED_RIGHT(A,A:track_002); CLOSING_START(A,A:track_002) |
| -2.15 | CRITICAL_TTC_START(A,A:track_001) |
| -2.10 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -2.05 | TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(B,B:track_002) |
| -1.90 | CRITICAL_TTC_START(A,A:track_002); CRITICAL_TTC_START(B,A) |
| -1.85 | STRONG_THROTTLE_END(B) |
| -1.55 | CRITICAL_TTC_END(A,A:track_001) |
| -0.90 | TRACK_LOST(A,A:track_002) |
| -0.80 | CRITICAL_TTC_START(A,A:track_001) |
| -0.20 | TRACK_LOST(B,B:track_002) |
| -0.15 | EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(B) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B) |
| +0.30 | MOVING_END(B); STOP_START(B) |
| +0.45 | EGO_PATH_EXIT(B,A) |
| +0.50 | CRITICAL_TTC_END(A,A:track_001) |
| +0.65 | CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.20 | A | g03 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02)<br>g04 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| -3.10 | B | g05 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -2.20 | A | g06 TRACK_APPEARED_RIGHT(A,A:track_002) (A:e04)<br>g07 CLOSING_START(A,A:track_002) (A:e05) | ego: MOVING<br>track_001: CLOSING |
| -2.15 | A | g08 CRITICAL_TTC_START(A,A:track_001) (A:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -2.10 | B | g09 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g10 CLOSING_START(B,A) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| -2.05 | B | g11 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e05)<br>g12 CLOSING_START(B,B:track_002) (B:e06) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING |
| -1.90 | A | g13 CRITICAL_TTC_START(A,A:track_002) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -1.90 | B | g14 CRITICAL_TTC_START(B,A) (B:e07) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.85 | B | g15 STRONG_THROTTLE_END(B) (B:e08) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -1.55 | A | g16 CRITICAL_TTC_END(A,A:track_001) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| -0.90 | A | g17 TRACK_LOST(A,A:track_002) (A:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.80 | A | g18 CRITICAL_TTC_START(A,A:track_001) (A:e10) | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| -0.20 | B | g19 TRACK_LOST(B,B:track_002) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| -0.15 | B | g20 EGO_PATH_ENTRY(B,A) (B:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.00 | A | g21 COLLISION(A,B) (A:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g21 COLLISION(A,B) (B:e11)<br>g22 STRONG_THROTTLE_START(B) (B:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.05 | B | g23 CRITICAL_TTC_END(B,A) (B:e13)<br>g24 CLOSING_END(B,A) (B:e14)<br>g25 STRONG_THROTTLE_END(B) (B:e15)<br>g27 BRAKE_START(B) (B:e16)<br>g29 HARD_BRAKE_START(B) (B:e17) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.05 | A | g26 BRAKE_START(A) (A:e12)<br>g28 HARD_BRAKE_START(A) (A:e13) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.30 | B | g30 MOVING_END(B) (B:e18)<br>g31 STOP_START(B) (B:e19) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.45 | B | g32 EGO_PATH_EXIT(B,A) (B:e20) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.50 | A | g33 CRITICAL_TTC_END(A,A:track_001) (A:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.65 | A | g34 CLOSING_END(A,A:track_001) (A:e15)<br>g35 MOVING_END(A) (A:e16)<br>g36 STOP_START(A) (A:e17) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| - | C | g37 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g38 TRACK_APPEARED_FRONT(C,C:track_001) (C:e02)<br>g39 CLOSING_START(C,C:track_001) (C:e03) | ego: MOVING |
| - | C | g40 CRITICAL_TTC_START(C,C:track_001) (C:e04) | ego: MOVING<br>track_001: CLOSING |
| - | C | g41 BRAKE_START(C) (C:e05)<br>g42 HARD_BRAKE_START(C) (C:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| - | C | g43 CRITICAL_TTC_END(C,C:track_001) (C:e07) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC |
| - | C | g44 MOVING_END(C) (C:e08)<br>g45 STOP_START(C) (C:e09) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING |
| - | C | g46 TRACK_APPEARED_LEFT(C,C:track_002) (C:e10)<br>g47 CLOSING_START(C,C:track_002) (C:e11) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING |
| - | C | g48 CRITICAL_TTC_START(C,C:track_002) (C:e12) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g49 CRITICAL_TTC_START(C,C:track_001) (C:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g50 CRITICAL_TTC_END(C,C:track_002) (C:e14) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| - | C | g51 CLOSING_END(C,C:track_002) (C:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| - | C | g52 CRITICAL_TTC_END(C,C:track_001) (C:e16) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state |
| - | C | g53 CLOSING_END(C,C:track_001) (C:e17) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>track_002: no active state |
| - | C | g54 HARD_BRAKE_END(C) (C:e18)<br>g55 BRAKE_END(C) (C:e19)<br>g56 STRONG_THROTTLE_START(C) (C:e20) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>track_002: no active state |

## Plain-language reading

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 4.20 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 4.20 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 3.10 s before the matched collision, B started applying strong throttle.
- 2.20 s before the matched collision, A's radar started tracking unidentified object A:track_002, which appeared on its right.
- 2.20 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 2.15 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 2.10 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 2.10 s before the matched collision, B observed A start closing in (already the case when first observed).
- 2.05 s before the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 2.05 s before the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 1.90 s before the matched collision, A's time-to-contact with unidentified object A:track_002 became critical.
- 1.90 s before the matched collision, B's time-to-contact with A became critical.
- 1.85 s before the matched collision, B stopped applying strong throttle.
- 1.55 s before the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.90 s before the matched collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 0.80 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 0.20 s before the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.15 s before the matched collision, B observed A enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.30 s after the matched collision, B stopped moving.
- 0.30 s after the matched collision, B came to a stop.
- 0.45 s after the matched collision, B observed A leave its forward path corridor.
- 0.50 s after the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.65 s after the matched collision, A observed unidentified object A:track_001 stop closing in.
- 0.65 s after the matched collision, A stopped moving.
- 0.65 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.05 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.05 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.15 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.35 s) C started braking.
- (unaligned, C local time 2.35 s) C started braking hard.
- (unaligned, C local time 2.75 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 2.85 s) C stopped moving.
- (unaligned, C local time 2.85 s) C came to a stop.
- (unaligned, C local time 3.00 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 3.00 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 3.35 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 3.55 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 4.20 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.55 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 4.70 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 4.90 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 14.35 s) C stopped braking hard.
- (unaligned, C local time 14.35 s) C released the brake.
- (unaligned, C local time 14.35 s) C started applying strong throttle.
