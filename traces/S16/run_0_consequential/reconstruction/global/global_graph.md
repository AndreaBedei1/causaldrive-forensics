# Global graph - S16/run_0_consequential

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001, C:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock ALIGNED; observed by others as: A:track_001 |
| A:track_002 | anonymous_track | seen only by A; candidate: C |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |
| B:track_004 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 5.55 | -5.55 | reported the reference collision collision_001 |
| B | ALIGNED | B:e15 | 5.55 | -5.55 | reported the reference collision collision_001 |
| C | ALIGNED | C:e09 | 6.60 | -5.55 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4243.51 vs 4243.51 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 322.1 vs 322.1 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.99 | A and C both reported collision_002 at 6.60 s (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 6.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.16 m/s over 3.0 s<br>clearance at the contact 0.07 m<br>the only compatible track of A touching it at the contact (clearance 0.07 m; track_002 at 3.00 m)<br>collision_001 with B at 5.55 s: not compatible (track speed disagrees with B's own speed: RMSE 3.42 m/s over 3.0 s (> 1.50)) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and C both reported collision_002 at 6.60 s (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 6.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 4.4 m -> 3.0 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.04 m/s over 3.0 s<br>clearance at the contact 2.99 m<br>collision_001 with B at 5.55 s: not compatible (not approaching before the contact: clearance 3.9 m -> 4.5 m over the last 1.0 s; track speed disagrees with B's own speed: RMSE 3.49 m/s over 3.0 s (> 1.50))<br>ambiguous: 2 persistent tracks of A are compatible with the contact collision_002 (track_001, track_002) |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 5.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 4.4 m -> 0.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.47 m/s over 3.0 s<br>clearance at the contact 0.04 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 5.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 9.1 m -> 6.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.30 m/s over 3.0 s (> 1.50)<br>clearance at the contact 6.02 m (beyond 3.50 m: confidence factor 0.70) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.70 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.9 m -> 11.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.55 m/s over 2.3 s (> 1.50)<br>clearance at the contact 11.44 m (beyond 3.50 m: confidence factor 0.03) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.25 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| C:track_001 | A | ASSOCIATED | 0.98 | C and A both reported collision_002 (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 3.95 s before the matched collision<br>continuous up to the contact: last observed 0.15 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.3 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.29 m/s over 2.9 s<br>clearance at the contact 1.08 m<br>the only track of C compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.55 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.55 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.55 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -5.55 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -5.55 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g06 | -5.55 | THROTTLE_START | C | - | C:e02 @ 0.00 | active_at_first_observation=True |
| g07 | -5.55 | TRACK_APPEARED_FRONT | B | A | B:e03 @ 0.00 |  |
| g08 | -5.55 | TRACK_APPEARED_LEFT | A | C | A:e03 @ 0.00 |  |
| g09 | -5.55 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e04 @ 0.00 |  |
| g10 | -5.55 | CLOSING_START | A | C | A:e04 @ 0.00 | active_at_first_observation=True |
| g11 | -5.55 | CLOSING_START | B | B:track_002 | B:e05 @ 0.00 | active_at_first_observation=True |
| g12 | -5.50 | TRACK_APPEARED_LEFT | A | A:track_002 | A:e05 @ 0.05 |  |
| g13 | -5.50 | CLOSING_START | A | A:track_002 | A:e06 @ 0.05 | active_at_first_observation=True |
| g14 | -4.70 | TRACK_APPEARED_LEFT | B | B:track_003 | B:e06 @ 0.85 |  |
| g15 | -4.70 | CLOSING_START | B | B:track_003 | B:e07 @ 0.85 | active_at_first_observation=True |
| g16 | -4.20 | CUT_IN_FROM_LEFT_START | B | B:track_003 | B:e08 @ 1.35 |  |
| g17 | -2.90 | TRACK_APPEARED_RIGHT | C | A | C:e03 @ 2.65 |  |
| g18 | -2.90 | CLOSING_START | C | A | C:e04 @ 2.65 | active_at_first_observation=True |
| g19 | -2.85 | CUT_IN_FROM_LEFT_END | B | B:track_003 | B:e09 @ 2.70 |  |
| g20 | -1.60 | THROTTLE_END | A | - | A:e07 @ 3.95 |  |
| g21 | -1.60 | BRAKE_START | A | - | A:e08 @ 3.95 |  |
| g22 | -1.40 | CLOSING_START | B | A | B:e10 @ 4.15 |  |
| g23 | -1.40 | CRITICAL_TTC_START | B | A | B:e11 @ 4.15 |  |
| g24 | -1.15 | CLOSING_END | C | A | C:e05 @ 4.40 |  |
| g25 | -1.10 | CLOSING_END | A | A:track_002 | A:e10 @ 4.45 |  |
| g26 | -1.10 | CLOSING_END | A | C | A:e09 @ 4.45 |  |
| g27 | -1.00 | BRAKE_END | A | - | A:e11 @ 4.55 |  |
| g28 | -0.90 | THROTTLE_START | A | - | A:e12 @ 4.65 |  |
| g29 | -0.70 | TRACK_LOST | B | B:track_003 | B:e12 @ 4.85 |  |
| g30 | -0.35 | CUT_IN_FROM_LEFT_START | A | A:track_002 | A:e13 @ 5.20 |  |
| g31 | -0.15 | THROTTLE_END | B | - | B:e13 @ 5.40 |  |
| g32 | -0.15 | BRAKE_START | B | - | B:e14 @ 5.40 |  |
| g33 | -0.15 | EGO_PATH_ENTRY | A | A:track_002 | A:e14 @ 5.40 |  |
| g34 | -0.10 | CUT_IN_FROM_LEFT_START | A | C | A:e15 @ 5.45 |  |
| g35 | 0.00 | COLLISION | - | A, B | A:e16 @ 5.55, B:e15 @ 5.55 | matched_event=collision_001; reference_event=True; peak_impulse=A 4243.51, B 4243.51 |
| g36 | 0.00 | THROTTLE_END | A | - | A:e17 @ 5.55 |  |
| g37 | 0.00 | BRAKE_START | A | - | A:e18 @ 5.55 |  |
| g38 | 0.00 | CLOSING_START | A | A:track_002 | A:e20 @ 5.55 |  |
| g39 | 0.00 | CLOSING_START | A | C | A:e19 @ 5.55 |  |
| g40 | 0.00 | CLOSING_START | C | A | C:e06 @ 5.55 |  |
| g41 | 0.00 | CRITICAL_TTC_START | A | C | A:e21 @ 5.55 |  |
| g42 | 0.05 | CRITICAL_TTC_END | B | A | B:e16 @ 5.60 |  |
| g43 | 0.05 | BRAKE_END | A | - | A:e22 @ 5.60 |  |
| g44 | 0.05 | CRITICAL_TTC_START | C | A | C:e07 @ 5.60 |  |
| g45 | 0.10 | CLOSING_END | B | A | B:e17 @ 5.65 |  |
| g46 | 0.20 | EGO_PATH_ENTRY | A | C | A:e23 @ 5.75 |  |
| g47 | 0.25 | CLOSING_END | B | B:track_002 | B:e18 @ 5.80 |  |
| g48 | 0.65 | MOVING_END | B | - | B:e19 @ 6.20 |  |
| g49 | 0.65 | STOP_START | B | - | B:e20 @ 6.20 |  |
| g50 | 0.90 | TRACK_LOST | C | A | C:e08 @ 6.45 |  |
| g51 | 1.05 | COLLISION | - | A, C | A:e24 @ 6.60, C:e09 @ 6.60 | matched_event=collision_002; reference_event=False; peak_impulse=A 322.10, C 322.10 |
| g52 | 1.05 | CRITICAL_TTC_END | A | C | A:e25 @ 6.60 |  |
| g53 | 1.05 | CLOSING_END | A | A:track_002 | A:e27 @ 6.60 |  |
| g54 | 1.05 | CLOSING_END | A | C | A:e26 @ 6.60 |  |
| g55 | 1.10 | THROTTLE_END | C | - | C:e10 @ 6.65 |  |
| g56 | 1.10 | BRAKE_START | C | - | C:e11 @ 6.65 |  |
| g57 | 1.20 | TRACK_LOST | A | A:track_002 | A:e28 @ 6.75 |  |
| g58 | 1.25 | TRACK_APPEARED_LEFT | B | B:track_004 | B:e21 @ 6.80 |  |
| g59 | 1.30 | CUT_IN_FROM_LEFT_END | A | C | A:e29 @ 6.85 |  |
| g60 | 1.55 | TRACK_LOST | B | B:track_004 | B:e22 @ 7.10 |  |
| g61 | 1.70 | EGO_PATH_EXIT | B | A | B:e23 @ 7.25 |  |
| g62 | 1.90 | MOVING_END | A | - | A:e30 @ 7.45 |  |
| g63 | 1.90 | MOVING_END | C | - | C:e12 @ 7.45 |  |
| g64 | 1.90 | STOP_START | A | - | A:e31 @ 7.45 |  |
| g65 | 1.90 | STOP_START | C | - | C:e13 @ 7.45 |  |
| g66 | 1.90 | BRAKE_START | A | - | A:e32 @ 7.45 |  |

## Edges

```
    g01 --PRECEDES--> g12
    g01 --PRECEDES--> g13
    g02 --PRECEDES--> g12
    g02 --PRECEDES--> g13
    g03 --PRECEDES--> g12
    g03 --PRECEDES--> g13
    g04 --PRECEDES--> g12
    g04 --PRECEDES--> g13
    g05 --PRECEDES--> g12
    g05 --PRECEDES--> g13
    g06 --PRECEDES--> g12
    g06 --PRECEDES--> g13
    g07 --PRECEDES--> g12
    g07 --PRECEDES--> g13
    g08 --PRECEDES--> g12
    g08 --PRECEDES--> g13
    g09 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g34 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g35 --PRECEDES--> g43
    g35 --PRECEDES--> g44
    g36 --PRECEDES--> g42
    g36 --PRECEDES--> g43
    g36 --PRECEDES--> g44
    g37 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g37 --PRECEDES--> g44
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g38 --PRECEDES--> g44
    g39 --PRECEDES--> g42
    g39 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g43 --PRECEDES--> g45
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g52 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g53 --PRECEDES--> g55
    g53 --PRECEDES--> g56
    g54 --PRECEDES--> g55
    g54 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g56 --PRECEDES--> g57
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g60 --PRECEDES--> g61
    g61 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g61 --PRECEDES--> g64
    g61 --PRECEDES--> g65
    g61 --PRECEDES--> g66
    g08 --SAME_TRACK--> g10
    g12 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g26
    g12 --SAME_TRACK--> g25
    g12 --SAME_TRACK--> g30
    g12 --SAME_TRACK--> g33
    g08 --SAME_TRACK--> g34
    g08 --SAME_TRACK--> g39
    g12 --SAME_TRACK--> g38
    g08 --SAME_TRACK--> g41
    g08 --SAME_TRACK--> g46
    g08 --SAME_TRACK--> g52
    g08 --SAME_TRACK--> g54
    g12 --SAME_TRACK--> g53
    g12 --SAME_TRACK--> g57
    g08 --SAME_TRACK--> g59
    g09 --SAME_TRACK--> g11
    g14 --SAME_TRACK--> g15
    g14 --SAME_TRACK--> g16
    g14 --SAME_TRACK--> g19
    g07 --SAME_TRACK--> g22
    g07 --SAME_TRACK--> g23
    g14 --SAME_TRACK--> g29
    g07 --SAME_TRACK--> g42
    g07 --SAME_TRACK--> g45
    g09 --SAME_TRACK--> g47
    g58 --SAME_TRACK--> g60
    g07 --SAME_TRACK--> g61
    g17 --SAME_TRACK--> g18
    g17 --SAME_TRACK--> g24
    g17 --SAME_TRACK--> g40
    g17 --SAME_TRACK--> g44
    g17 --SAME_TRACK--> g50
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.55 | MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_LEFT(A,C); TRACK_APPEARED_LEFT(B,B:track_002); CLOSING_START(A,C); CLOSING_START(B,B:track_002) |
| -5.50 | TRACK_APPEARED_LEFT(A,A:track_002); CLOSING_START(A,A:track_002) |
| -4.70 | TRACK_APPEARED_LEFT(B,B:track_003); CLOSING_START(B,B:track_003) |
| -4.20 | CUT_IN_FROM_LEFT_START(B,B:track_003) |
| -2.90 | TRACK_APPEARED_RIGHT(C,A); CLOSING_START(C,A) |
| -2.85 | CUT_IN_FROM_LEFT_END(B,B:track_003) |
| -1.60 | THROTTLE_END(A); BRAKE_START(A) |
| -1.40 | CLOSING_START(B,A); CRITICAL_TTC_START(B,A) |
| -1.15 | CLOSING_END(C,A) |
| -1.10 | CLOSING_END(A,A:track_002); CLOSING_END(A,C) |
| -1.00 | BRAKE_END(A) |
| -0.90 | THROTTLE_START(A) |
| -0.70 | TRACK_LOST(B,B:track_003) |
| -0.35 | CUT_IN_FROM_LEFT_START(A,A:track_002) |
| -0.15 | THROTTLE_END(B); BRAKE_START(B); EGO_PATH_ENTRY(A,A:track_002) |
| -0.10 | CUT_IN_FROM_LEFT_START(A,C) |
| +0.00 | COLLISION(A,B); THROTTLE_END(A); BRAKE_START(A); CLOSING_START(A,A:track_002); CLOSING_START(A,C); CLOSING_START(C,A); CRITICAL_TTC_START(A,C) |
| +0.05 | CRITICAL_TTC_END(B,A); BRAKE_END(A); CRITICAL_TTC_START(C,A) |
| +0.10 | CLOSING_END(B,A) |
| +0.20 | EGO_PATH_ENTRY(A,C) |
| +0.25 | CLOSING_END(B,B:track_002) |
| +0.65 | MOVING_END(B); STOP_START(B) |
| +0.90 | TRACK_LOST(C,A) |
| +1.05 | COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,A:track_002); CLOSING_END(A,C) |
| +1.10 | THROTTLE_END(C); BRAKE_START(C) |
| +1.20 | TRACK_LOST(A,A:track_002) |
| +1.25 | TRACK_APPEARED_LEFT(B,B:track_004) |
| +1.30 | CUT_IN_FROM_LEFT_END(A,C) |
| +1.55 | TRACK_LOST(B,B:track_004) |
| +1.70 | EGO_PATH_EXIT(B,A) |
| +1.90 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C); BRAKE_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (C): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 5.45 < CRITICAL_TTC_START 5.55 (+0.10 s) < COLLISION with C 6.60 (+1.05 s); EGO_PATH_ENTRY 5.75 after critical TTC (+0.20 s) [local times; t_global: cut_in -0.10, critical_ttc_start +0.00, ego_path_entry +0.20, collision +1.05]
- A's track_002 (unidentified A:track_002): CUT_IN_FROM_LEFT_START 5.20, no critical TTC after it; EGO_PATH_ENTRY 5.40, no critical TTC [local times; t_global: cut_in -0.35, ego_path_entry -0.15, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 4.15, COLLISION with A 5.55 (+1.40 s) [local times; t_global: critical_ttc_start -1.40, collision +0.00]
- B's track_003 (unidentified B:track_003): CUT_IN_FROM_LEFT_START 1.35, no critical TTC after it [local times; t_global: cut_in -4.20, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 5.60, COLLISION with A 6.60 (+1.00 s) [local times; t_global: critical_ttc_start +0.05, collision +1.05]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.55 | A | g01 MOVING_START(A) (A:e01)<br>g04 THROTTLE_START(A) (A:e02)<br>g08 TRACK_APPEARED_LEFT(A,C) (A:e03)<br>g10 CLOSING_START(A,C) (A:e04) | ego: not yet observed |
| -5.55 | B | g02 MOVING_START(B) (B:e01)<br>g05 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_FRONT(B,A) (B:e03)<br>g09 TRACK_APPEARED_LEFT(B,B:track_002) (B:e04)<br>g11 CLOSING_START(B,B:track_002) (B:e05) | ego: not yet observed |
| -5.55 | C | g03 MOVING_START(C) (C:e01)<br>g06 THROTTLE_START(C) (C:e02) | ego: not yet observed |
| -5.50 | A | g12 TRACK_APPEARED_LEFT(A,A:track_002) (A:e05)<br>g13 CLOSING_START(A,A:track_002) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -4.70 | B | g14 TRACK_APPEARED_LEFT(B,B:track_003) (B:e06)<br>g15 CLOSING_START(B,B:track_003) (B:e07) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING |
| -4.20 | B | g16 CUT_IN_FROM_LEFT_START(B,B:track_003) (B:e08) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING, CRITICAL_TTC? |
| -2.90 | C | g17 TRACK_APPEARED_RIGHT(C,A) (C:e03)<br>g18 CLOSING_START(C,A) (C:e04) | ego: MOVING, THROTTLE |
| -2.85 | B | g19 CUT_IN_FROM_LEFT_END(B,B:track_003) (B:e09) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING, CUT_IN_FROM_LEFT |
| -1.60 | A | g20 THROTTLE_END(A) (A:e07)<br>g21 BRAKE_START(A) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.40 | B | g22 CLOSING_START(B,A) (B:e10)<br>g23 CRITICAL_TTC_START(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| -1.15 | C | g24 CLOSING_END(C,A) (C:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.10 | A | g25 CLOSING_END(A,A:track_002) (A:e10)<br>g26 CLOSING_END(A,C) (A:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.00 | A | g27 BRAKE_END(A) (A:e11) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| -0.90 | A | g28 THROTTLE_START(A) (A:e12) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -0.70 | B | g29 TRACK_LOST(B,B:track_003) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| -0.35 | A | g30 CUT_IN_FROM_LEFT_START(A,A:track_002) (A:e13) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state |
| -0.15 | B | g31 THROTTLE_END(B) (B:e13)<br>g32 BRAKE_START(B) (B:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| -0.15 | A | g33 EGO_PATH_ENTRY(A,A:track_002) (A:e14) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CUT_IN_FROM_LEFT |
| -0.10 | A | g34 CUT_IN_FROM_LEFT_START(A,C) (A:e15) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | A | g35 COLLISION(A,B) (A:e16)<br>g36 THROTTLE_END(A) (A:e17)<br>g37 BRAKE_START(A) (A:e18)<br>g38 CLOSING_START(A,A:track_002) (A:e20)<br>g39 CLOSING_START(A,C) (A:e19)<br>g41 CRITICAL_TTC_START(A,C) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_LEFT<br>track_002: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g35 COLLISION(A,B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.00 | C | g40 CLOSING_START(C,A) (C:e06) | ego: MOVING, THROTTLE<br>track_001: no active state |
| +0.05 | B | g42 CRITICAL_TTC_END(B,A) (B:e16) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.05 | A | g43 BRAKE_END(A) (A:e22) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.05 | C | g44 CRITICAL_TTC_START(C,A) (C:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| +0.10 | B | g45 CLOSING_END(B,A) (B:e17) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.20 | A | g46 EGO_PATH_ENTRY(A,C) (A:e23) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.25 | B | g47 CLOSING_END(B,B:track_002) (B:e18) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.65 | B | g48 MOVING_END(B) (B:e19)<br>g49 STOP_START(B) (B:e20) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 |
| +0.90 | C | g50 TRACK_LOST(C,A) (C:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC |
| +1.05 | A | g51 COLLISION(A,C) (A:e24)<br>g52 CRITICAL_TTC_END(A,C) (A:e25)<br>g53 CLOSING_END(A,A:track_002) (A:e27)<br>g54 CLOSING_END(A,C) (A:e26) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track_002: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +1.05 | C | g51 COLLISION(A,C) (C:e09) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| +1.10 | C | g55 THROTTLE_END(C) (C:e10)<br>g56 BRAKE_START(C) (C:e11) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| +1.20 | A | g57 TRACK_LOST(A,A:track_002) (A:e28) | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track_002: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +1.25 | B | g58 TRACK_APPEARED_LEFT(B,B:track_004) (B:e21) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 |
| +1.30 | A | g59 CUT_IN_FROM_LEFT_END(A,C) (A:e29) | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002 |
| +1.55 | B | g60 TRACK_LOST(B,B:track_004) (B:e22) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_004: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_003 |
| +1.70 | B | g61 EGO_PATH_EXIT(B,A) (B:e23) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003, track_004 |
| +1.90 | A | g62 MOVING_END(A) (A:e30)<br>g64 STOP_START(A) (A:e31)<br>g66 BRAKE_START(A) (A:e32) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +1.90 | C | g63 MOVING_END(C) (C:e12)<br>g65 STOP_START(C) (C:e13) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 5.55 s before the reference collision, A started moving (already the case when first observed).
- 5.55 s before the reference collision, B started moving (already the case when first observed).
- 5.55 s before the reference collision, C started moving (already the case when first observed).
- 5.55 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 5.55 s before the reference collision, A's radar started tracking C, which appeared on its left.
- 5.55 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 5.55 s before the reference collision, A observed C start closing in (already the case when first observed).
- 5.55 s before the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 5.50 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared on its left.
- 5.50 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 4.70 s before the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 4.70 s before the reference collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 4.20 s before the reference collision, B observed unidentified object B:track_003 cutting in from the left.
- 2.90 s before the reference collision, C's radar started tracking A, which appeared on its right.
- 2.90 s before the reference collision, C observed A start closing in (already the case when first observed).
- 2.85 s before the reference collision, B observed unidentified object B:track_003's cut-in from the left settle.
- 1.60 s before the reference collision, A released the accelerator.
- 1.60 s before the reference collision, A started braking.
- 1.40 s before the reference collision, B observed A start closing in.
- 1.40 s before the reference collision, B's time-to-contact with A became critical.
- 1.15 s before the reference collision, C observed A stop closing in.
- 1.10 s before the reference collision, A observed unidentified object A:track_002 stop closing in.
- 1.10 s before the reference collision, A observed C stop closing in.
- 1.00 s before the reference collision, A released the brake.
- 0.90 s before the reference collision, A pressed the accelerator.
- 0.70 s before the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.35 s before the reference collision, A observed unidentified object A:track_002 cutting in from the left.
- 0.15 s before the reference collision, B released the accelerator.
- 0.15 s before the reference collision, B started braking.
- 0.15 s before the reference collision, A observed unidentified object A:track_002 enter its forward path corridor.
- 0.10 s before the reference collision, A observed C cutting in from the left.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 4244, B: 4244 N*s).
- At the reference collision, A released the accelerator.
- At the reference collision, A started braking.
- At the reference collision, A observed unidentified object A:track_002 start closing in.
- At the reference collision, A observed C start closing in.
- At the reference collision, C observed A start closing in.
- At the reference collision, A's time-to-contact with C became critical.
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the brake.
- 0.05 s after the reference collision, C's time-to-contact with A became critical.
- 0.10 s after the reference collision, B observed A stop closing in.
- 0.20 s after the reference collision, A observed C enter its forward path corridor.
- 0.25 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.65 s after the reference collision, B stopped moving.
- 0.65 s after the reference collision, B came to a stop.
- 0.90 s after the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 1.05 s after the reference collision, A and C both recorded this same collision (peak impulses A: 322, C: 322 N*s).
- 1.05 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.05 s after the reference collision, A observed unidentified object A:track_002 stop closing in.
- 1.05 s after the reference collision, A observed C stop closing in.
- 1.10 s after the reference collision, C released the accelerator.
- 1.10 s after the reference collision, C started braking.
- 1.20 s after the reference collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 1.25 s after the reference collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 1.30 s after the reference collision, A observed C's cut-in from the left settle.
- 1.55 s after the reference collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 1.70 s after the reference collision, B observed A leave its forward path corridor.
- 1.90 s after the reference collision, A stopped moving.
- 1.90 s after the reference collision, C stopped moving.
- 1.90 s after the reference collision, A came to a stop.
- 1.90 s after the reference collision, C came to a stop.
- 1.90 s after the reference collision, A started braking.
