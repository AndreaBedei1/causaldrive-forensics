# Global graph - S16/run_0_independent

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock ALIGNED; observed by others as: - |
| A:track_002 | anonymous_track | seen only by A; candidate: C |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: A |
| C:track_002 | anonymous_track | seen only by C; candidate: A |
| C:track_003 | anonymous_track | seen only by C; candidate: A |

## Graph alignment

Reference event: `collision_002` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e17 | 14.10 | -14.10 | reported the reference collision collision_002 |
| B | ALIGNED | B:e10 | 5.15 | -14.10 | shares collision_001 with A, aligned through collision_002 -> collision_001 |
| C | ALIGNED | C:e18 | 14.10 | -14.10 | reported the reference collision collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 9089.81 vs 9089.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.4 m -> 0.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.14 m/s over 3.0 s<br>clearance at the contact 0.37 m<br>the only track of A compatible with the contact<br>collision_002 with C at 14.10 s: not compatible (not approaching before the contact: clearance 11.5 m -> 20.3 m over the last 1.0 s) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and C both reported collision_002 at 14.10 s (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 7.4 m -> 0.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.24 m/s over 0.9 s<br>clearance at the contact 0.10 m<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 8.00 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.7 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.50 m/s over 3.0 s<br>clearance at the contact 0.65 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 6.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| C:track_001 | C:track_001 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 10.65 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>not approaching before the contact: clearance 24.0 m -> 25.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 6.46 m/s over 3.0 s (> 1.50)<br>clearance at the contact 24.07 m (beyond 3.50 m: confidence factor 0.00) |
| C:track_002 | C:track_002 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 9.90 s before the matched collision<br>lost 8.85 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 22.7 m -> 14.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision |
| C:track_003 | C:track_003 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 2.60 s before the matched collision<br>lost 1.85 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 16.7 m -> 15.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.41 m/s over 0.8 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -14.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -14.10 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -14.10 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -14.10 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g05 | -14.10 | TRACK_APPEARED_REAR | A | B | A:e02 @ 0.00 |  |
| g06 | -13.60 | MOVING_END | C | - | C:e02 @ 0.50 |  |
| g07 | -13.60 | STOP_START | C | - | C:e03 @ 0.50 |  |
| g08 | -13.45 | CLOSING_START | B | A | B:e03 @ 0.65 |  |
| g09 | -13.40 | CLOSING_START | A | B | A:e03 @ 0.70 |  |
| g10 | -13.35 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g11 | -12.70 | CRITICAL_TTC_END | B | A | B:e05 @ 1.40 |  |
| g12 | -12.70 | CLOSING_END | A | B | A:e04 @ 1.40 |  |
| g13 | -12.70 | CLOSING_END | B | A | B:e06 @ 1.40 |  |
| g14 | -10.65 | TRACK_APPEARED_REAR | C | C:track_001 | C:e04 @ 3.45 |  |
| g15 | -10.65 | CLOSING_START | C | C:track_001 | C:e05 @ 3.45 | active_at_first_observation=True |
| g16 | -10.15 | BRAKE_START | A | - | A:e05 @ 3.95 |  |
| g17 | -9.90 | TRACK_APPEARED_RIGHT | C | C:track_002 | C:e06 @ 4.20 |  |
| g18 | -9.90 | CLOSING_START | A | B | A:e06 @ 4.20 |  |
| g19 | -9.90 | CLOSING_START | B | A | B:e07 @ 4.20 |  |
| g20 | -9.90 | CLOSING_START | C | C:track_002 | C:e07 @ 4.20 | active_at_first_observation=True |
| g21 | -9.70 | CRITICAL_TTC_START | B | A | B:e08 @ 4.40 |  |
| g22 | -9.35 | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g23 | -8.95 | COLLISION | - | A, B | A:e07 @ 5.15, B:e10 @ 5.15 | matched_event=collision_001; reference_event=False; peak_impulse=A 6073.81, B 6073.81 |
| g24 | -8.95 | CLOSING_END | A | B | A:e08 @ 5.15 |  |
| g25 | -8.90 | CRITICAL_TTC_END | B | A | B:e11 @ 5.20 |  |
| g26 | -8.90 | CLOSING_END | B | A | B:e12 @ 5.20 |  |
| g27 | -8.85 | TRACK_LOST | C | C:track_002 | C:e08 @ 5.25 |  |
| g28 | -8.50 | CLOSING_END | C | C:track_001 | C:e09 @ 5.60 |  |
| g29 | -8.50 | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g30 | -8.50 | STOP_START | B | - | B:e14 @ 5.60 |  |
| g31 | -8.30 | MOVING_END | A | - | A:e09 @ 5.80 |  |
| g32 | -8.30 | STOP_START | A | - | A:e10 @ 5.80 |  |
| g33 | -3.15 | BRAKE_END | A | - | A:e11 @ 10.95 |  |
| g34 | -2.70 | STOP_END | A | - | A:e12 @ 11.40 |  |
| g35 | -2.70 | MOVING_START | A | - | A:e13 @ 11.40 |  |
| g36 | -2.60 | TRACK_APPEARED_RIGHT | C | C:track_003 | C:e10 @ 11.50 |  |
| g37 | -2.35 | CLOSING_START | C | C:track_003 | C:e11 @ 11.75 |  |
| g38 | -2.15 | STOP_END | C | - | C:e12 @ 11.95 |  |
| g39 | -2.15 | MOVING_START | C | - | C:e13 @ 11.95 |  |
| g40 | -2.15 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e15 @ 11.95 |  |
| g41 | -1.85 | TRACK_LOST | C | C:track_003 | C:e14 @ 12.25 |  |
| g42 | -0.95 | TRACK_APPEARED_FRONT | A | A:track_002 | A:e14 @ 13.15 |  |
| g43 | -0.95 | CLOSING_START | A | A:track_002 | A:e15 @ 13.15 | active_at_first_observation=True |
| g44 | -0.95 | CRITICAL_TTC_START | A | A:track_002 | A:e16 @ 13.15 | active_at_first_observation=True |
| g45 | -0.70 | EGO_PATH_EXIT | B | A | B:e16 @ 13.40 |  |
| g46 | -0.70 | STOP_SIGN_DETECTED_START | C | C:sign-3 | C:e15 @ 13.40 | relevant_to_ego_path=False |
| g47 | -0.50 | STOP_SIGN_DETECTED_END | C | C:sign-3 | C:e16 @ 13.60 |  |
| g48 | -0.05 | TRACK_LOST | B | A | B:e17 @ 14.05 |  |
| g49 | -0.05 | TRACK_LOST | C | C:track_001 | C:e17 @ 14.05 |  |
| g50 | 0.00 | COLLISION | - | A, C | A:e17 @ 14.10, C:e18 @ 14.10 | matched_event=collision_002; reference_event=True; peak_impulse=A 9089.81, C 9089.81 |
| g51 | 0.00 | CRITICAL_TTC_END | A | A:track_002 | A:e18 @ 14.10 |  |
| g52 | 0.00 | CLOSING_END | A | A:track_002 | A:e19 @ 14.10 |  |
| g53 | 0.00 | BRAKE_START | C | - | C:e19 @ 14.10 |  |
| g54 | 0.55 | MOVING_END | A | - | A:e20 @ 14.65 |  |
| g55 | 0.55 | MOVING_END | C | - | C:e20 @ 14.65 |  |
| g56 | 0.55 | STOP_START | A | - | A:e21 @ 14.65 |  |
| g57 | 0.55 | STOP_START | C | - | C:e21 @ 14.65 |  |
| g58 | 3.70 | TRACK_LOST | A | B | A:e22 @ 17.80 |  |

## Edges

```
    g01 --PRECEDES--> g06
    g01 --PRECEDES--> g07
    g02 --PRECEDES--> g06
    g02 --PRECEDES--> g07
    g03 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g48 --PRECEDES--> g53
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g50 --PRECEDES--> g56
    g50 --PRECEDES--> g57
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g51 --PRECEDES--> g57
    g52 --PRECEDES--> g54
    g52 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g53 --PRECEDES--> g54
    g53 --PRECEDES--> g55
    g53 --PRECEDES--> g56
    g53 --PRECEDES--> g57
    g54 --PRECEDES--> g58
    g55 --PRECEDES--> g58
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g58
    g05 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g12
    g05 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g24
    g42 --SAME_TRACK--> g43
    g42 --SAME_TRACK--> g44
    g42 --SAME_TRACK--> g51
    g42 --SAME_TRACK--> g52
    g05 --SAME_TRACK--> g58
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g10
    g04 --SAME_TRACK--> g11
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g19
    g04 --SAME_TRACK--> g21
    g04 --SAME_TRACK--> g25
    g04 --SAME_TRACK--> g26
    g04 --SAME_TRACK--> g45
    g04 --SAME_TRACK--> g48
    g14 --SAME_TRACK--> g15
    g17 --SAME_TRACK--> g20
    g17 --SAME_TRACK--> g27
    g14 --SAME_TRACK--> g28
    g36 --SAME_TRACK--> g37
    g36 --SAME_TRACK--> g41
    g14 --SAME_TRACK--> g49
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -14.10 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_REAR(A,B) |
| -13.60 | MOVING_END(C); STOP_START(C) |
| -13.45 | CLOSING_START(B,A) |
| -13.40 | CLOSING_START(A,B) |
| -13.35 | CRITICAL_TTC_START(B,A) |
| -12.70 | CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A) |
| -10.65 | TRACK_APPEARED_REAR(C,C:track_001); CLOSING_START(C,C:track_001) |
| -10.15 | BRAKE_START(A) |
| -9.90 | TRACK_APPEARED_RIGHT(C,C:track_002); CLOSING_START(A,B); CLOSING_START(B,A); CLOSING_START(C,C:track_002) |
| -9.70 | CRITICAL_TTC_START(B,A) |
| -9.35 | BRAKE_START(B) |
| -8.95 | COLLISION(A,B); CLOSING_END(A,B) |
| -8.90 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| -8.85 | TRACK_LOST(C,C:track_002) |
| -8.50 | CLOSING_END(C,C:track_001); MOVING_END(B); STOP_START(B) |
| -8.30 | MOVING_END(A); STOP_START(A) |
| -3.15 | BRAKE_END(A) |
| -2.70 | STOP_END(A); MOVING_START(A) |
| -2.60 | TRACK_APPEARED_RIGHT(C,C:track_003) |
| -2.35 | CLOSING_START(C,C:track_003) |
| -2.15 | STOP_END(C); MOVING_START(C); TRACK_APPEARED_LEFT(B,B:track_002) |
| -1.85 | TRACK_LOST(C,C:track_003) |
| -0.95 | TRACK_APPEARED_FRONT(A,A:track_002); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_002) |
| -0.70 | EGO_PATH_EXIT(B,A); STOP_SIGN_DETECTED_START(C,C:sign-3) |
| -0.50 | STOP_SIGN_DETECTED_END(C,C:sign-3) |
| -0.05 | TRACK_LOST(B,A); TRACK_LOST(C,C:track_001) |
| +0.00 | COLLISION(A,C); CRITICAL_TTC_END(A,A:track_002); CLOSING_END(A,A:track_002); BRAKE_START(C) |
| +0.55 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |
| +3.70 | TRACK_LOST(A,B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (unidentified A:track_002): CRITICAL_TTC_START 13.15, COLLISION 14.10 (+0.95 s) [local times; t_global: critical_ttc_start -0.95, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -13.35, collision -8.95]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -14.10 | A | g01 MOVING_START(A) (A:e01)<br>g05 TRACK_APPEARED_REAR(A,B) (A:e02) | ego: not yet observed |
| -14.10 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -14.10 | C | g03 MOVING_START(C) (C:e01) | ego: not yet observed |
| -13.60 | C | g06 MOVING_END(C) (C:e02)<br>g07 STOP_START(C) (C:e03) | ego: MOVING |
| -13.45 | B | g08 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -13.40 | A | g09 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: no active state |
| -13.35 | B | g10 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -12.70 | B | g11 CRITICAL_TTC_END(B,A) (B:e05)<br>g13 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -12.70 | A | g12 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -10.65 | C | g14 TRACK_APPEARED_REAR(C,C:track_001) (C:e04)<br>g15 CLOSING_START(C,C:track_001) (C:e05) | ego: STOP |
| -10.15 | A | g16 BRAKE_START(A) (A:e05) | ego: MOVING<br>track_001: no active state |
| -9.90 | C | g17 TRACK_APPEARED_RIGHT(C,C:track_002) (C:e06)<br>g20 CLOSING_START(C,C:track_002) (C:e07) | ego: STOP<br>track_001: CLOSING |
| -9.90 | A | g18 CLOSING_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>track_001: no active state |
| -9.90 | B | g19 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -9.70 | B | g21 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -9.35 | B | g22 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -8.95 | A | g23 COLLISION(A,B) (A:e07)<br>g24 CLOSING_END(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| -8.95 | B | g23 COLLISION(A,B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -8.90 | B | g25 CRITICAL_TTC_END(B,A) (B:e11)<br>g26 CLOSING_END(B,A) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -8.85 | C | g27 TRACK_LOST(C,C:track_002) (C:e08) | ego: STOP<br>track_001: CLOSING<br>track_002: CLOSING |
| -8.50 | C | g28 CLOSING_END(C,C:track_001) (C:e09) | ego: STOP<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| -8.50 | B | g29 MOVING_END(B) (B:e13)<br>g30 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| -8.30 | A | g31 MOVING_END(A) (A:e09)<br>g32 STOP_START(A) (A:e10) | ego: MOVING, BRAKE<br>track_001: no active state |
| -3.15 | A | g33 BRAKE_END(A) (A:e11) | ego: STOP, BRAKE<br>track_001: no active state |
| -2.70 | A | g34 STOP_END(A) (A:e12)<br>g35 MOVING_START(A) (A:e13) | ego: STOP<br>track_001: no active state |
| -2.60 | C | g36 TRACK_APPEARED_RIGHT(C,C:track_003) (C:e10) | ego: STOP<br>track_001: no active state<br>track lost, states UNKNOWN: track_002 |
| -2.35 | C | g37 CLOSING_START(C,C:track_003) (C:e11) | ego: STOP<br>track_001: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_002 |
| -2.15 | C | g38 STOP_END(C) (C:e12)<br>g39 MOVING_START(C) (C:e13) | ego: STOP<br>track_001: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_002 |
| -2.15 | B | g40 TRACK_APPEARED_LEFT(B,B:track_002) (B:e15) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| -1.85 | C | g41 TRACK_LOST(C,C:track_003) (C:e14) | ego: MOVING<br>track_001: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_002 |
| -0.95 | A | g42 TRACK_APPEARED_FRONT(A,A:track_002) (A:e14)<br>g43 CLOSING_START(A,A:track_002) (A:e15)<br>g44 CRITICAL_TTC_START(A,A:track_002) (A:e16) | ego: MOVING<br>track_001: no active state |
| -0.70 | B | g45 EGO_PATH_EXIT(B,A) (B:e16) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| -0.70 | C | g46 STOP_SIGN_DETECTED_START(C,C:sign-3) (C:e15) | ego: MOVING<br>track_001: no active state<br>track lost, states UNKNOWN: track_002, track_003 |
| -0.50 | C | g47 STOP_SIGN_DETECTED_END(C,C:sign-3) (C:e16) | ego: MOVING<br>track_001: no active state<br>track lost, states UNKNOWN: track_002, track_003<br>sign-3: STOP sign known |
| -0.05 | B | g48 TRACK_LOST(B,A) (B:e17) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |
| -0.05 | C | g49 TRACK_LOST(C,C:track_001) (C:e17) | ego: MOVING<br>track_001: no active state<br>track lost, states UNKNOWN: track_002, track_003<br>sign-3: STOP sign known |
| +0.00 | A | g50 COLLISION(A,C) (A:e17)<br>g51 CRITICAL_TTC_END(A,A:track_002) (A:e18)<br>g52 CLOSING_END(A,A:track_002) (A:e19) | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | C | g50 COLLISION(A,C) (C:e18)<br>g53 BRAKE_START(C) (C:e19) | ego: MOVING<br>track lost, states UNKNOWN: track_001, track_002, track_003<br>sign-3: STOP sign known |
| +0.55 | A | g54 MOVING_END(A) (A:e20)<br>g56 STOP_START(A) (A:e21) | ego: MOVING<br>track_001: no active state<br>track_002: IN_EGO_PATH |
| +0.55 | C | g55 MOVING_END(C) (C:e20)<br>g57 STOP_START(C) (C:e21) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001, track_002, track_003<br>sign-3: STOP sign known |
| +3.70 | A | g58 TRACK_LOST(A,B) (A:e22) | ego: STOP<br>track_001: no active state<br>track_002: IN_EGO_PATH |

## Plain-language reading

- 14.10 s before the reference collision, A started moving (already the case when first observed).
- 14.10 s before the reference collision, B started moving (already the case when first observed).
- 14.10 s before the reference collision, C started moving (already the case when first observed).
- 14.10 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 14.10 s before the reference collision, A's radar started tracking B, which appeared behind it.
- 13.60 s before the reference collision, C stopped moving.
- 13.60 s before the reference collision, C came to a stop.
- 13.45 s before the reference collision, B observed A start closing in.
- 13.40 s before the reference collision, A observed B start closing in.
- 13.35 s before the reference collision, B's time-to-contact with A became critical.
- 12.70 s before the reference collision, B's time-to-contact with A stopped being critical.
- 12.70 s before the reference collision, A observed B stop closing in.
- 12.70 s before the reference collision, B observed A stop closing in.
- 10.65 s before the reference collision, C's radar started tracking unidentified object C:track_001, which appeared behind it.
- 10.65 s before the reference collision, C observed unidentified object C:track_001 start closing in (already the case when first observed).
- 10.15 s before the reference collision, A started braking.
- 9.90 s before the reference collision, C's radar started tracking unidentified object C:track_002, which appeared on its right.
- 9.90 s before the reference collision, A observed B start closing in.
- 9.90 s before the reference collision, B observed A start closing in.
- 9.90 s before the reference collision, C observed unidentified object C:track_002 start closing in (already the case when first observed).
- 9.70 s before the reference collision, B's time-to-contact with A became critical.
- 9.35 s before the reference collision, B started braking.
- 8.95 s before the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- 8.95 s before the reference collision, A observed B stop closing in.
- 8.90 s before the reference collision, B's time-to-contact with A stopped being critical.
- 8.90 s before the reference collision, B observed A stop closing in.
- 8.85 s before the reference collision, C's radar lost unidentified object C:track_002 (its states are UNKNOWN from then on, not ended).
- 8.50 s before the reference collision, C observed unidentified object C:track_001 stop closing in.
- 8.50 s before the reference collision, B stopped moving.
- 8.50 s before the reference collision, B came to a stop.
- 8.30 s before the reference collision, A stopped moving.
- 8.30 s before the reference collision, A came to a stop.
- 3.15 s before the reference collision, A released the brake.
- 2.70 s before the reference collision, A left its stop.
- 2.70 s before the reference collision, A started moving.
- 2.60 s before the reference collision, C's radar started tracking unidentified object C:track_003, which appeared on its right.
- 2.35 s before the reference collision, C observed unidentified object C:track_003 start closing in.
- 2.15 s before the reference collision, C left its stop.
- 2.15 s before the reference collision, C started moving.
- 2.15 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 1.85 s before the reference collision, C's radar lost unidentified object C:track_003 (its states are UNKNOWN from then on, not ended).
- 0.95 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared in front of it.
- 0.95 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 0.95 s before the reference collision, A's time-to-contact with unidentified object A:track_002 became critical (already the case when first observed).
- 0.70 s before the reference collision, B observed A leave its forward path corridor.
- 0.70 s before the reference collision, C's camera established a STOP sign detection (unidentified object C:sign-3) (the detector judged it not relevant to its path).
- 0.50 s before the reference collision, C's camera stopped detecting STOP sign unidentified object C:sign-3.
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and C both recorded this same collision (peak impulses A: 9090, C: 9090 N*s).
- At the reference collision, A's time-to-contact with unidentified object A:track_002 stopped being critical.
- At the reference collision, A observed unidentified object A:track_002 stop closing in.
- At the reference collision, C started braking.
- 0.55 s after the reference collision, A stopped moving.
- 0.55 s after the reference collision, C stopped moving.
- 0.55 s after the reference collision, A came to a stop.
- 0.55 s after the reference collision, C came to a stop.
- 3.70 s after the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
