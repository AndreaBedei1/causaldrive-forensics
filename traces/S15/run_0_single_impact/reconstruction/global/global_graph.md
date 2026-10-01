# Global graph - S15/run_0_single_impact

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |
| B:track_004 | anonymous_track | seen only by B; candidate: A |
| B:track_005 | anonymous_track | seen only by B; candidate: A |
| B:track_006 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e26 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 66.2 m -> 54.3 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.99 m/s over 2.9 s (> 1.50)<br>range at the contact 54.25 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_002 | B | ASSOCIATED | 0.85 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.1 m -> 1.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.85 m/s over 1.8 s<br>range at the contact 1.89 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.88 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 16.9 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.77 m/s over 1.8 s<br>range at the contact 0.98 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 33.3 m -> 30.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.67 m/s over 0.7 s (> 1.50)<br>range at the contact 30.02 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 22.0 m -> 19.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.16 m/s over 0.7 s (> 1.50)<br>range at the contact 19.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 30.4 m -> 27.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 8.37 m/s over 0.7 s (> 1.50)<br>range at the contact 26.97 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 27.3 m -> 24.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.37 m/s over 0.7 s (> 1.50)<br>range at the contact 24.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.3 m -> 15.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.73 m/s over 0.6 s (> 1.50)<br>range at the contact 15.03 m (beyond 3.50 m: confidence factor 0.00) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -2.90 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.90 |  |
| g04 | -2.90 | CLOSING_START | A | A:track_001 | A:e03 @ 0.90 | active_at_first_observation=True |
| g05 | -2.00 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 1.80 | relevant_to_ego_path=False |
| g06 | -1.85 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 1.95 |  |
| g07 | -1.85 | CLOSING_START | B | A | B:e04 @ 1.95 | active_at_first_observation=True |
| g08 | -1.80 | TRACK_APPEARED_RIGHT | A | B | A:e04 @ 2.00 |  |
| g09 | -1.80 | CLOSING_START | A | B | A:e05 @ 2.00 | active_at_first_observation=True |
| g10 | -1.80 | CRITICAL_TTC_START | A | B | A:e06 @ 2.00 | active_at_first_observation=True |
| g11 | -1.70 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e05 @ 2.10 |  |
| g12 | -1.65 | CRITICAL_TTC_START | B | A | B:e06 @ 2.15 |  |
| g13 | -1.55 | TURN_LEFT_START | B | - | B:e07 @ 2.25 |  |
| g14 | -0.85 | BRAKE_START | B | - | B:e08 @ 2.95 |  |
| g15 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e09 @ 3.05 |  |
| g16 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_003 | B:e10 @ 3.05 |  |
| g17 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_004 | B:e11 @ 3.05 |  |
| g18 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_005 | B:e12 @ 3.05 |  |
| g19 | -0.75 | CLOSING_START | B | B:track_002 | B:e13 @ 3.05 | active_at_first_observation=True |
| g20 | -0.75 | CLOSING_START | B | B:track_003 | B:e14 @ 3.05 | active_at_first_observation=True |
| g21 | -0.75 | CLOSING_START | B | B:track_004 | B:e15 @ 3.05 | active_at_first_observation=True |
| g22 | -0.75 | CLOSING_START | B | B:track_005 | B:e16 @ 3.05 | active_at_first_observation=True |
| g23 | -0.70 | TRACK_APPEARED_LEFT | B | B:track_006 | B:e17 @ 3.10 |  |
| g24 | -0.70 | CLOSING_START | B | B:track_006 | B:e18 @ 3.10 | active_at_first_observation=True |
| g25 | -0.30 | BRAKE_END | B | - | B:e19 @ 3.50 |  |
| g26 | -0.10 | EGO_PATH_ENTRY | B | A | B:e20 @ 3.70 |  |
| g27 | -0.05 | TRACK_LOST | A | B | A:e07 @ 3.75 |  |
| g28 | -0.05 | TRACK_LOST | B | B:track_002 | B:e21 @ 3.75 |  |
| g29 | -0.05 | TRACK_LOST | B | B:track_003 | B:e22 @ 3.75 |  |
| g30 | -0.05 | TRACK_LOST | B | B:track_004 | B:e23 @ 3.75 |  |
| g31 | -0.05 | TRACK_LOST | B | B:track_005 | B:e24 @ 3.75 |  |
| g32 | -0.05 | TRACK_LOST | B | B:track_006 | B:e25 @ 3.75 |  |
| g33 | 0.00 | COLLISION | - | A, B | A:e08 @ 3.80, B:e26 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 9797.50, B 9797.50 |
| g34 | 0.00 | TURN_LEFT_END | B | - | B:e27 @ 3.80 |  |
| g35 | 0.00 | TURN_LEFT_START | A | - | A:e09 @ 3.80 |  |
| g36 | 0.00 | EGO_PATH_ENTRY | A | A:track_001 | A:e10 @ 3.80 |  |
| g37 | 0.05 | EGO_PATH_EXIT | A | A:track_001 | A:e11 @ 3.85 |  |
| g38 | 0.05 | BRAKE_START | B | - | B:e28 @ 3.85 |  |
| g39 | 0.20 | MOVING_END | B | - | B:e29 @ 4.00 |  |
| g40 | 0.20 | STOP_START | B | - | B:e30 @ 4.00 |  |
| g41 | 0.30 | CRITICAL_TTC_END | B | A | B:e31 @ 4.10 |  |
| g42 | 0.30 | EGO_PATH_ENTRY | A | A:track_001 | A:e12 @ 4.10 |  |
| g43 | 0.50 | CLOSING_END | B | A | B:e32 @ 4.30 |  |
| g44 | 0.50 | EGO_PATH_EXIT | A | A:track_001 | A:e13 @ 4.30 |  |
| g45 | 0.80 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e14 @ 4.60 | relevant_to_ego_path=False |
| g46 | 1.00 | EGO_PATH_EXIT | B | A | B:e33 @ 4.80 |  |
| g47 | 1.30 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e15 @ 5.10 |  |
| g48 | 1.40 | TURN_LEFT_END | A | - | A:e16 @ 5.20 |  |
| g49 | 6.80 | STOP_SIGN_DETECTED_START | A | A:sign-1 | A:e17 @ 10.60 | relevant_to_ego_path=False |
| g50 | 7.75 | MOVING_END | A | - | A:e18 @ 11.55 |  |
| g51 | 7.75 | STOP_START | A | - | A:e19 @ 11.55 |  |
| g52 | 9.65 | CRITICAL_TTC_START | A | A:track_001 | A:e20 @ 13.45 |  |
| g53 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g54 | - | TRACK_APPEARED_LEFT | C | C:track_002 | C:e02 @ 0.65 |  |
| g55 | - | CLOSING_START | C | C:track_002 | C:e03 @ 0.65 | active_at_first_observation=True |
| g56 | - | TRACK_APPEARED_FRONT | C | C:track_001 | C:e04 @ 0.80 |  |
| g57 | - | CLOSING_START | C | C:track_001 | C:e05 @ 0.80 | active_at_first_observation=True |
| g58 | - | STOP_SIGN_DETECTED_START | C | C:sign-0 | C:e06 @ 2.80 | relevant_to_ego_path=False |
| g59 | - | STOP_SIGN_DETECTED_END | C | C:sign-0 | C:e07 @ 2.80 |  |
| g60 | - | CLOSING_END | C | C:track_002 | C:e08 @ 2.95 |  |
| g61 | - | CLOSING_START | C | C:track_002 | C:e09 @ 3.85 |  |
| g62 | - | EGO_PATH_ENTRY | C | C:track_001 | C:e10 @ 5.15 |  |

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
    g06 --PRECEDES--> g09
    g06 --PRECEDES--> g10
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g14 --PRECEDES--> g19
    g14 --PRECEDES--> g20
    g14 --PRECEDES--> g21
    g14 --PRECEDES--> g22
    g15 --PRECEDES--> g23
    g15 --PRECEDES--> g24
    g16 --PRECEDES--> g23
    g16 --PRECEDES--> g24
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g18 --PRECEDES--> g23
    g18 --PRECEDES--> g24
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g27 --PRECEDES--> g35
    g27 --PRECEDES--> g36
    g28 --PRECEDES--> g33
    g28 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g28 --PRECEDES--> g36
    g29 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g29 --PRECEDES--> g35
    g29 --PRECEDES--> g36
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g30 --PRECEDES--> g35
    g30 --PRECEDES--> g36
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g32 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g52
    g03 --SAME_TRACK--> g04
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g10
    g08 --SAME_TRACK--> g27
    g03 --SAME_TRACK--> g36
    g03 --SAME_TRACK--> g37
    g03 --SAME_TRACK--> g42
    g03 --SAME_TRACK--> g44
    g03 --SAME_TRACK--> g52
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g12
    g15 --SAME_TRACK--> g19
    g16 --SAME_TRACK--> g20
    g17 --SAME_TRACK--> g21
    g18 --SAME_TRACK--> g22
    g23 --SAME_TRACK--> g24
    g06 --SAME_TRACK--> g26
    g15 --SAME_TRACK--> g28
    g16 --SAME_TRACK--> g29
    g17 --SAME_TRACK--> g30
    g18 --SAME_TRACK--> g31
    g23 --SAME_TRACK--> g32
    g06 --SAME_TRACK--> g41
    g06 --SAME_TRACK--> g43
    g06 --SAME_TRACK--> g46
    g54 --SAME_TRACK--> g55
    g56 --SAME_TRACK--> g57
    g54 --SAME_TRACK--> g60
    g54 --SAME_TRACK--> g61
    g56 --SAME_TRACK--> g62
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B) |
| -2.90 | TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.00 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -1.85 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.80 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B) |
| -1.70 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -1.65 | CRITICAL_TTC_START(B,A) |
| -1.55 | TURN_LEFT_START(B) |
| -0.85 | BRAKE_START(B) |
| -0.75 | TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005) |
| -0.70 | TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_006) |
| -0.30 | BRAKE_END(B) |
| -0.10 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006) |
| +0.00 | COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001) |
| +0.05 | EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.30 | CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(A,A:track_001) |
| +0.50 | CLOSING_END(B,A); EGO_PATH_EXIT(A,A:track_001) |
| +0.80 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| +1.00 | EGO_PATH_EXIT(B,A) |
| +1.30 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| +1.40 | TURN_LEFT_END(A) |
| +6.80 | STOP_SIGN_DETECTED_START(A,A:sign-1) |
| +7.75 | MOVING_END(A); STOP_START(A) |
| +9.65 | CRITICAL_TTC_START(A,A:track_001) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 13.45, COLLISION 3.80 (+-9.65 s); EGO_PATH_ENTRY 3.80 before critical TTC (-9.65 s) [local times; t_global: critical_ttc_start +9.65, ego_path_entry +0.00, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 2.00, COLLISION 3.80 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.15, COLLISION 3.80 (+1.65 s); EGO_PATH_ENTRY 3.70 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.65, ego_path_entry -0.10, collision +0.00]
- C's track_001 (unidentified C:track_001): EGO_PATH_ENTRY 5.15, no critical TTC [local times]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.80 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -3.80 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -2.90 | A | g03 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02)<br>g04 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| -2.00 | B | g05 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| -1.85 | B | g06 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g07 CLOSING_START(B,A) (B:e04) | ego: MOVING<br>sign-0: STOP sign known |
| -1.80 | A | g08 TRACK_APPEARED_RIGHT(A,B) (A:e04)<br>g09 CLOSING_START(A,B) (A:e05)<br>g10 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| -1.70 | B | g11 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e05) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -1.65 | B | g12 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -1.55 | B | g13 TURN_LEFT_START(B) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.85 | B | g14 BRAKE_START(B) (B:e08) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.75 | B | g15 TRACK_APPEARED_LEFT(B,B:track_002) (B:e09)<br>g16 TRACK_APPEARED_LEFT(B,B:track_003) (B:e10)<br>g17 TRACK_APPEARED_LEFT(B,B:track_004) (B:e11)<br>g18 TRACK_APPEARED_LEFT(B,B:track_005) (B:e12)<br>g19 CLOSING_START(B,B:track_002) (B:e13)<br>g20 CLOSING_START(B,B:track_003) (B:e14)<br>g21 CLOSING_START(B,B:track_004) (B:e15)<br>g22 CLOSING_START(B,B:track_005) (B:e16) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.70 | B | g23 TRACK_APPEARED_LEFT(B,B:track_006) (B:e17)<br>g24 CLOSING_START(B,B:track_006) (B:e18) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>sign-0: STOP sign known |
| -0.30 | B | g25 BRAKE_END(B) (B:e19) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known |
| -0.10 | B | g26 EGO_PATH_ENTRY(B,A) (B:e20) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known |
| -0.05 | A | g27 TRACK_LOST(A,B) (A:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.05 | B | g28 TRACK_LOST(B,B:track_002) (B:e21)<br>g29 TRACK_LOST(B,B:track_003) (B:e22)<br>g30 TRACK_LOST(B,B:track_004) (B:e23)<br>g31 TRACK_LOST(B,B:track_005) (B:e24)<br>g32 TRACK_LOST(B,B:track_006) (B:e25) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known |
| +0.00 | A | g33 COLLISION(A,B) (A:e08)<br>g35 TURN_LEFT_START(A) (A:e09)<br>g36 EGO_PATH_ENTRY(A,A:track_001) (A:e10) | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g33 COLLISION(A,B) (B:e26)<br>g34 TURN_LEFT_END(B) (B:e27) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known |
| +0.05 | A | g37 EGO_PATH_EXIT(A,A:track_001) (A:e11) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.05 | B | g38 BRAKE_START(B) (B:e28) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known |
| +0.20 | B | g39 MOVING_END(B) (B:e29)<br>g40 STOP_START(B) (B:e30) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known |
| +0.30 | B | g41 CRITICAL_TTC_END(B,A) (B:e31) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known |
| +0.30 | A | g42 EGO_PATH_ENTRY(A,A:track_001) (A:e12) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| +0.50 | B | g43 CLOSING_END(B,A) (B:e32) | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known |
| +0.50 | A | g44 EGO_PATH_EXIT(A,A:track_001) (A:e13) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.80 | A | g45 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 |
| +1.00 | B | g46 EGO_PATH_EXIT(B,A) (B:e33) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known |
| +1.30 | A | g47 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e15) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.40 | A | g48 TURN_LEFT_END(A) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +6.80 | A | g49 STOP_SIGN_DETECTED_START(A,A:sign-1) (A:e17) | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +7.75 | A | g50 MOVING_END(A) (A:e18)<br>g51 STOP_START(A) (A:e19) | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| +9.65 | A | g52 CRITICAL_TTC_START(A,A:track_001) (A:e20) | ego: STOP<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known |
| - | C | g53 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g54 TRACK_APPEARED_LEFT(C,C:track_002) (C:e02)<br>g55 CLOSING_START(C,C:track_002) (C:e03) | ego: MOVING |
| - | C | g56 TRACK_APPEARED_FRONT(C,C:track_001) (C:e04)<br>g57 CLOSING_START(C,C:track_001) (C:e05) | ego: MOVING<br>track_002: CLOSING |
| - | C | g58 STOP_SIGN_DETECTED_START(C,C:sign-0) (C:e06)<br>g59 STOP_SIGN_DETECTED_END(C,C:sign-0) (C:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| - | C | g60 CLOSING_END(C,C:track_002) (C:e08) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known |
| - | C | g61 CLOSING_START(C,C:track_002) (C:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: no active state<br>sign-0: STOP sign known |
| - | C | g62 EGO_PATH_ENTRY(C,C:track_001) (C:e10) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known |

## Plain-language reading

- 3.80 s before the matched collision, A started moving (already the case when first observed).
- 3.80 s before the matched collision, B started moving (already the case when first observed).
- 2.90 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 2.90 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.00 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 1.85 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.65 s before the matched collision, B's time-to-contact with A became critical.
- 1.55 s before the matched collision, B started turning left.
- 0.85 s before the matched collision, B started braking.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its left.
- 0.75 s before the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.75 s before the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.75 s before the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.75 s before the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.70 s before the matched collision, B's radar started tracking unidentified object B:track_006, which appeared on its left.
- 0.70 s before the matched collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.30 s before the matched collision, B released the brake.
- 0.10 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the matched collision, B stopped turning left.
- At the matched collision, A started turning left.
- At the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.05 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.05 s after the matched collision, B started braking.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.30 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.30 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.50 s after the matched collision, B observed A stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.80 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 1.00 s after the matched collision, B observed A leave its forward path corridor.
- 1.30 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 1.40 s after the matched collision, A stopped turning left.
- 6.80 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 7.75 s after the matched collision, A stopped moving.
- 7.75 s after the matched collision, A came to a stop.
- 9.65 s after the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.65 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 0.65 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 0.80 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.80 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.80 s) C's camera established a STOP sign detection (unidentified object C:sign-0) (the detector judged it not relevant to its path).
- (unaligned, C local time 2.80 s) C's camera stopped detecting STOP sign unidentified object C:sign-0.
- (unaligned, C local time 2.95 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 3.85 s) C observed unidentified object C:track_002 start closing in.
- (unaligned, C local time 5.15 s) C observed unidentified object C:track_001 enter its forward path corridor.
