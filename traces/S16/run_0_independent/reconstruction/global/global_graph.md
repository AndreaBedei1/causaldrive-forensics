# Global graph - S16/run_0_independent

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock ALIGNED; observed by others as: A:track_002 |
| A:track_001 | anonymous_track | seen only by A; candidate: C |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_002` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 14.10 | -14.10 | reported the reference collision collision_002 |
| B | ALIGNED | B:e10 | 5.15 | -14.10 | shares collision_001 with A, aligned through collision_002 -> collision_001 |
| C | ALIGNED | C:e10 | 14.10 | -14.10 | reported the reference collision collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 9095.53 vs 9095.53 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and C both reported collision_002 at 14.10 s (peak impulse 9095.53 vs 9095.53 N*s)<br>tracked for 2.95 s before the matched collision<br>lost 2.20 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 14.9 m -> 14.7 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.26 m/s over 0.8 s<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 6.00 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_002 | C | ASSOCIATED | 1.00 | A and C both reported collision_002 at 14.10 s (peak impulse 9095.53 vs 9095.53 N*s)<br>tracked for 2.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 8.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.15 m/s over 2.9 s<br>range at the contact 0.18 m<br>the only track of A compatible with the contact<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 6.00 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 3.9 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.52 m/s over 3.0 s<br>range at the contact 0.55 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 8.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 8.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -14.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -14.10 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -14.10 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -14.10 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g05 | -13.60 | MOVING_END | C | - | C:e02 @ 0.50 |  |
| g06 | -13.60 | STOP_START | C | - | C:e03 @ 0.50 |  |
| g07 | -13.40 | CLOSING_START | B | A | B:e03 @ 0.70 |  |
| g08 | -13.35 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g09 | -12.70 | CRITICAL_TTC_END | B | A | B:e05 @ 1.40 |  |
| g10 | -12.70 | CLOSING_END | B | A | B:e06 @ 1.40 |  |
| g11 | -10.15 | BRAKE_START | A | - | A:e02 @ 3.95 |  |
| g12 | -9.85 | CLOSING_START | B | A | B:e07 @ 4.25 |  |
| g13 | -9.65 | CRITICAL_TTC_START | B | A | B:e08 @ 4.45 |  |
| g14 | -9.35 | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g15 | -8.95 | COLLISION | - | A, B | A:e03 @ 5.15, B:e10 @ 5.15 | matched_event=collision_001; reference_event=False; peak_impulse=A 6073.81, B 6073.81 |
| g16 | -8.90 | CRITICAL_TTC_END | B | A | B:e11 @ 5.20 |  |
| g17 | -8.90 | CLOSING_END | B | A | B:e12 @ 5.20 |  |
| g18 | -8.50 | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g19 | -8.50 | STOP_START | B | - | B:e14 @ 5.60 |  |
| g20 | -8.30 | MOVING_END | A | - | A:e04 @ 5.80 |  |
| g21 | -8.30 | STOP_START | A | - | A:e05 @ 5.80 |  |
| g22 | -5.00 | YIELD_SIGN_DETECTED_START | C | C:sign-1 | C:e04 @ 9.10 | relevant_to_ego_path=False |
| g23 | -4.50 | YIELD_SIGN_DETECTED_END | C | C:sign-1 | C:e05 @ 9.60 |  |
| g24 | -3.15 | BRAKE_END | A | - | A:e06 @ 10.95 |  |
| g25 | -2.95 | TRACK_APPEARED_LEFT | A | A:track_001 | A:e07 @ 11.15 |  |
| g26 | -2.95 | TRACK_APPEARED_LEFT | A | C | A:e08 @ 11.15 |  |
| g27 | -2.70 | STOP_END | A | - | A:e09 @ 11.40 |  |
| g28 | -2.70 | MOVING_START | A | - | A:e10 @ 11.40 |  |
| g29 | -2.35 | CLOSING_START | A | C | A:e11 @ 11.75 |  |
| g30 | -2.30 | CLOSING_START | A | A:track_001 | A:e12 @ 11.80 |  |
| g31 | -2.20 | TRACK_LOST | A | A:track_001 | A:e13 @ 11.90 |  |
| g32 | -2.15 | STOP_END | C | - | C:e06 @ 11.95 |  |
| g33 | -2.15 | MOVING_START | C | - | C:e07 @ 11.95 |  |
| g34 | -2.00 | EGO_PATH_ENTRY | A | C | A:e14 @ 12.10 |  |
| g35 | -1.45 | CRITICAL_TTC_START | A | C | A:e15 @ 12.65 |  |
| g36 | -0.65 | EGO_PATH_EXIT | B | A | B:e15 @ 13.45 |  |
| g37 | -0.55 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e16 @ 13.55 |  |
| g38 | -0.55 | TRACK_APPEARED_LEFT | B | B:track_003 | B:e17 @ 13.55 |  |
| g39 | -0.30 | STOP_SIGN_DETECTED_START | C | C:sign-3 | C:e08 @ 13.80 | relevant_to_ego_path=False |
| g40 | -0.30 | STOP_SIGN_DETECTED_END | C | C:sign-3 | C:e09 @ 13.80 |  |
| g41 | -0.10 | TRACK_LOST | B | A | B:e18 @ 14.00 |  |
| g42 | 0.00 | COLLISION | - | A, C | A:e16 @ 14.10, C:e10 @ 14.10 | matched_event=collision_002; reference_event=True; peak_impulse=A 9095.53, C 9095.53 |
| g43 | 0.00 | BRAKE_START | C | - | C:e11 @ 14.10 |  |
| g44 | 0.20 | CLOSING_END | A | C | A:e17 @ 14.30 |  |
| g45 | 0.25 | TRACK_LOST | A | C | A:e18 @ 14.35 |  |
| g46 | 0.40 | TRACK_LOST | B | B:track_003 | B:e19 @ 14.50 |  |
| g47 | 0.55 | MOVING_END | A | - | A:e19 @ 14.65 |  |
| g48 | 0.55 | MOVING_END | C | - | C:e12 @ 14.65 |  |
| g49 | 0.55 | STOP_START | A | - | A:e20 @ 14.65 |  |
| g50 | 0.55 | STOP_START | C | - | C:e13 @ 14.65 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g01 --PRECEDES--> g06
    g02 --PRECEDES--> g05
    g02 --PRECEDES--> g06
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
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
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g26 --SAME_TRACK--> g29
    g25 --SAME_TRACK--> g30
    g25 --SAME_TRACK--> g31
    g26 --SAME_TRACK--> g34
    g26 --SAME_TRACK--> g35
    g26 --SAME_TRACK--> g44
    g26 --SAME_TRACK--> g45
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g10
    g04 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g16
    g04 --SAME_TRACK--> g17
    g04 --SAME_TRACK--> g36
    g04 --SAME_TRACK--> g41
    g38 --SAME_TRACK--> g46
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -14.10 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A) |
| -13.60 | MOVING_END(C); STOP_START(C) |
| -13.40 | CLOSING_START(B,A) |
| -13.35 | CRITICAL_TTC_START(B,A) |
| -12.70 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| -10.15 | BRAKE_START(A) |
| -9.85 | CLOSING_START(B,A) |
| -9.65 | CRITICAL_TTC_START(B,A) |
| -9.35 | BRAKE_START(B) |
| -8.95 | COLLISION(A,B) |
| -8.90 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| -8.50 | MOVING_END(B); STOP_START(B) |
| -8.30 | MOVING_END(A); STOP_START(A) |
| -5.00 | YIELD_SIGN_DETECTED_START(C,C:sign-1) |
| -4.50 | YIELD_SIGN_DETECTED_END(C,C:sign-1) |
| -3.15 | BRAKE_END(A) |
| -2.95 | TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_LEFT(A,C) |
| -2.70 | STOP_END(A); MOVING_START(A) |
| -2.35 | CLOSING_START(A,C) |
| -2.30 | CLOSING_START(A,A:track_001) |
| -2.20 | TRACK_LOST(A,A:track_001) |
| -2.15 | STOP_END(C); MOVING_START(C) |
| -2.00 | EGO_PATH_ENTRY(A,C) |
| -1.45 | CRITICAL_TTC_START(A,C) |
| -0.65 | EGO_PATH_EXIT(B,A) |
| -0.55 | TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003) |
| -0.30 | STOP_SIGN_DETECTED_START(C,C:sign-3); STOP_SIGN_DETECTED_END(C,C:sign-3) |
| -0.10 | TRACK_LOST(B,A) |
| +0.00 | COLLISION(A,C); BRAKE_START(C) |
| +0.20 | CLOSING_END(A,C) |
| +0.25 | TRACK_LOST(A,C) |
| +0.40 | TRACK_LOST(B,B:track_003) |
| +0.55 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (C): CRITICAL_TTC_START 12.65, COLLISION with C 14.10 (+1.45 s); EGO_PATH_ENTRY 12.10 before critical TTC (-0.55 s) [local times; t_global: critical_ttc_start -1.45, ego_path_entry -2.00, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -13.35, collision -8.95]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -14.10 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -14.10 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -14.10 | C | g03 MOVING_START(C) (C:e01) | ego: not yet observed |
| -13.60 | C | g05 MOVING_END(C) (C:e02)<br>g06 STOP_START(C) (C:e03) | ego: MOVING |
| -13.40 | B | g07 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -13.35 | B | g08 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -12.70 | B | g09 CRITICAL_TTC_END(B,A) (B:e05)<br>g10 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -10.15 | A | g11 BRAKE_START(A) (A:e02) | ego: MOVING |
| -9.85 | B | g12 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -9.65 | B | g13 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -9.35 | B | g14 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -8.95 | A | g15 COLLISION(A,B) (A:e03) | ego: MOVING, BRAKE |
| -8.95 | B | g15 COLLISION(A,B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -8.90 | B | g16 CRITICAL_TTC_END(B,A) (B:e11)<br>g17 CLOSING_END(B,A) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -8.50 | B | g18 MOVING_END(B) (B:e13)<br>g19 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| -8.30 | A | g20 MOVING_END(A) (A:e04)<br>g21 STOP_START(A) (A:e05) | ego: MOVING, BRAKE |
| -5.00 | C | g22 YIELD_SIGN_DETECTED_START(C,C:sign-1) (C:e04) | ego: STOP |
| -4.50 | C | g23 YIELD_SIGN_DETECTED_END(C,C:sign-1) (C:e05) | ego: STOP<br>sign-1: YIELD sign known |
| -3.15 | A | g24 BRAKE_END(A) (A:e06) | ego: STOP, BRAKE |
| -2.95 | A | g25 TRACK_APPEARED_LEFT(A,A:track_001) (A:e07)<br>g26 TRACK_APPEARED_LEFT(A,C) (A:e08) | ego: STOP |
| -2.70 | A | g27 STOP_END(A) (A:e09)<br>g28 MOVING_START(A) (A:e10) | ego: STOP<br>track_001: no active state<br>track_002: no active state |
| -2.35 | A | g29 CLOSING_START(A,C) (A:e11) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -2.30 | A | g30 CLOSING_START(A,A:track_001) (A:e12) | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING |
| -2.20 | A | g31 TRACK_LOST(A,A:track_001) (A:e13) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -2.15 | C | g32 STOP_END(C) (C:e06)<br>g33 MOVING_START(C) (C:e07) | ego: STOP<br>sign-1: YIELD sign known |
| -2.00 | A | g34 EGO_PATH_ENTRY(A,C) (A:e14) | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.45 | A | g35 CRITICAL_TTC_START(A,C) (A:e15) | ego: MOVING<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| -0.65 | B | g36 EGO_PATH_EXIT(B,A) (B:e15) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| -0.55 | B | g37 TRACK_APPEARED_LEFT(B,B:track_002) (B:e16)<br>g38 TRACK_APPEARED_LEFT(B,B:track_003) (B:e17) | ego: STOP, BRAKE<br>track_001: no active state |
| -0.30 | C | g39 STOP_SIGN_DETECTED_START(C,C:sign-3) (C:e08)<br>g40 STOP_SIGN_DETECTED_END(C,C:sign-3) (C:e09) | ego: MOVING<br>sign-1: YIELD sign known |
| -0.10 | B | g41 TRACK_LOST(B,A) (B:e18) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state |
| +0.00 | A | g42 COLLISION(A,C) (A:e16) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.00 | C | g42 COLLISION(A,C) (C:e10)<br>g43 BRAKE_START(C) (C:e11) | ego: MOVING<br>sign-1: YIELD sign known<br>sign-3: STOP sign known |
| +0.20 | A | g44 CLOSING_END(A,C) (A:e17) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.25 | A | g45 TRACK_LOST(A,C) (A:e18) | ego: MOVING<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.40 | B | g46 TRACK_LOST(B,B:track_003) (B:e19) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.55 | A | g47 MOVING_END(A) (A:e19)<br>g49 STOP_START(A) (A:e20) | ego: MOVING<br>track lost, states UNKNOWN: track_001, track_002 |
| +0.55 | C | g48 MOVING_END(C) (C:e12)<br>g50 STOP_START(C) (C:e13) | ego: MOVING, BRAKE<br>sign-1: YIELD sign known<br>sign-3: STOP sign known |

## Plain-language reading

- 14.10 s before the reference collision, A started moving (already the case when first observed).
- 14.10 s before the reference collision, B started moving (already the case when first observed).
- 14.10 s before the reference collision, C started moving (already the case when first observed).
- 14.10 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 13.60 s before the reference collision, C stopped moving.
- 13.60 s before the reference collision, C came to a stop.
- 13.40 s before the reference collision, B observed A start closing in.
- 13.35 s before the reference collision, B's time-to-contact with A became critical.
- 12.70 s before the reference collision, B's time-to-contact with A stopped being critical.
- 12.70 s before the reference collision, B observed A stop closing in.
- 10.15 s before the reference collision, A started braking.
- 9.85 s before the reference collision, B observed A start closing in.
- 9.65 s before the reference collision, B's time-to-contact with A became critical.
- 9.35 s before the reference collision, B started braking.
- 8.95 s before the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- 8.90 s before the reference collision, B's time-to-contact with A stopped being critical.
- 8.90 s before the reference collision, B observed A stop closing in.
- 8.50 s before the reference collision, B stopped moving.
- 8.50 s before the reference collision, B came to a stop.
- 8.30 s before the reference collision, A stopped moving.
- 8.30 s before the reference collision, A came to a stop.
- 5.00 s before the reference collision, C's camera established a YIELD sign detection (unidentified object C:sign-1) (the detector judged it not relevant to its path).
- 4.50 s before the reference collision, C's camera stopped detecting YIELD sign unidentified object C:sign-1.
- 3.15 s before the reference collision, A released the brake.
- 2.95 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 2.95 s before the reference collision, A's radar started tracking C, which appeared on its left.
- 2.70 s before the reference collision, A left its stop.
- 2.70 s before the reference collision, A started moving.
- 2.35 s before the reference collision, A observed C start closing in.
- 2.30 s before the reference collision, A observed unidentified object A:track_001 start closing in.
- 2.20 s before the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 2.15 s before the reference collision, C left its stop.
- 2.15 s before the reference collision, C started moving.
- 2.00 s before the reference collision, A observed C enter its forward path corridor.
- 1.45 s before the reference collision, A's time-to-contact with C became critical.
- 0.65 s before the reference collision, B observed A leave its forward path corridor.
- 0.55 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 0.55 s before the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 0.30 s before the reference collision, C's camera established a STOP sign detection (unidentified object C:sign-3) (the detector judged it not relevant to its path).
- 0.30 s before the reference collision, C's camera stopped detecting STOP sign unidentified object C:sign-3.
- 0.10 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and C both recorded this same collision (peak impulses A: 9096, C: 9096 N*s).
- At the reference collision, C started braking.
- 0.20 s after the reference collision, A observed C stop closing in.
- 0.25 s after the reference collision, A's radar lost C (its states are UNKNOWN from then on, not ended).
- 0.40 s after the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the reference collision, A stopped moving.
- 0.55 s after the reference collision, C stopped moving.
- 0.55 s after the reference collision, A came to a stop.
- 0.55 s after the reference collision, C came to a stop.
