# Global graph - S16/run_0_consequential

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001, C:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock ALIGNED; observed by others as: A:track_001, A:track_002, B:track_002, B:track_003 |
| U1 | anonymous_road_user | anonymous; observed by B as B:track_004 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 5.55 | -5.55 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.55 | -5.55 | reported the reference collision collision_001 |
| C | ALIGNED | C:e09 | 6.60 | -5.55 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4243.51 vs 4243.51 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

Matched `collision_002`: A and C both recorded a collision; peak impulses 322.1 vs 322.1 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.99 | A and C both reported collision_002 at 6.60 s (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 6.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.15 m/s over 3.0 s<br>clearance at the contact 0.06 m<br>the only compatible track of A touching it at the contact (clearance 0.06 m; track_002 at 2.01 m)<br>collision_001 with B at 5.55 s: not compatible (track speed disagrees with B's own speed: RMSE 3.43 m/s over 3.0 s (> 1.50)) |
| A:track_002 | C | ASSOCIATED | 1.00 | A and C both reported collision_002 at 6.60 s (peak impulse 322.1 vs 322.1 N*s)<br>tracked for 6.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.4 m -> 2.0 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.10 m/s over 3.0 s<br>clearance at the contact 2.01 m<br>collision_001 with B at 5.55 s: not compatible (not approaching before the contact: clearance 3.0 m -> 3.5 m over the last 1.0 s; track speed disagrees with B's own speed: RMSE 3.58 m/s over 3.0 s (> 1.50))<br>ambiguous: 2 persistent tracks of A are compatible with the contact collision_002 (track_001, track_002)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma, over 135 samples; 100% within 3 sigma) at C's own velocity (median difference 0.12 m/s) |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 5.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 4.4 m -> 0.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.47 m/s over 3.0 s<br>clearance at the contact 0.04 m<br>the only track of B compatible with the contact |
| B:track_002 | C | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 5.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 9.1 m -> 6.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.31 m/s over 3.0 s (> 1.50)<br>clearance at the contact 6.04 m (beyond 3.50 m: confidence factor 0.70)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma, over 123 samples before C's contact with a third body at +1.05 s; 100% within 3 sigma) at C's own velocity (median difference 0.20 m/s) |
| B:track_003 | C | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.3 m -> 7.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.38 m/s over 3.0 s (> 1.50)<br>clearance at the contact 7.70 m (beyond 3.50 m: confidence factor 0.38)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma, over 53 samples before C's contact with a third body at +1.05 s; 100% within 3 sigma) at C's own velocity (median difference 0.12 m/s) |
| B:track_004 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 4243.51 vs 4243.51 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.25 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: B:track_004 |
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
| g09 | -5.55 | TRACK_APPEARED_LEFT | B | C | B:e04 @ 0.00 |  |
| g10 | -5.55 | CLOSING_START | A | C | A:e04 @ 0.00 | active_at_first_observation=True |
| g11 | -5.55 | CLOSING_START | B | C | B:e05 @ 0.00 | active_at_first_observation=True |
| g12 | -5.50 | TRACK_APPEARED_LEFT | A | C | A:e05 @ 0.05 |  |
| g13 | -5.50 | CLOSING_START | A | C | A:e06 @ 0.05 | active_at_first_observation=True |
| g14 | -5.05 | CRITICAL_TTC_START | B | A | B:e06 @ 0.50 |  |
| g15 | -4.70 | TRACK_APPEARED_LEFT | B | C | B:e07 @ 0.85 |  |
| g16 | -4.70 | CLOSING_START | B | C | B:e08 @ 0.85 | active_at_first_observation=True |
| g17 | -2.90 | TRACK_APPEARED_RIGHT | C | A | C:e03 @ 2.65 |  |
| g18 | -2.90 | CLOSING_START | C | A | C:e04 @ 2.65 | active_at_first_observation=True |
| g19 | -1.60 | THROTTLE_END | A | - | A:e07 @ 3.95 |  |
| g20 | -1.60 | BRAKE_START | A | - | A:e08 @ 3.95 |  |
| g21 | -1.40 | CLOSING_START | B | A | B:e09 @ 4.15 |  |
| g22 | -1.15 | CLOSING_END | C | A | C:e05 @ 4.40 |  |
| g23 | -1.10 | CLOSING_END | A | C | A:e09 @ 4.45 |  |
| g24 | -1.00 | CLOSING_END | A | C | A:e10 @ 4.55 |  |
| g25 | -1.00 | BRAKE_END | A | - | A:e11 @ 4.55 |  |
| g26 | -0.90 | THROTTLE_START | A | - | A:e12 @ 4.65 |  |
| g27 | -0.35 | CRITICAL_TTC_START | A | C | A:e13 @ 5.20 |  |
| g28 | -0.15 | THROTTLE_END | B | - | B:e10 @ 5.40 |  |
| g29 | -0.15 | BRAKE_START | B | - | B:e11 @ 5.40 |  |
| g30 | -0.10 | CUT_IN_FROM_LEFT_START | A | C | A:e14 @ 5.45 |  |
| g31 | -0.05 | EGO_PATH_ENTRY | A | C | A:e15 @ 5.50 |  |
| g32 | 0.00 | COLLISION | - | A, B | A:e16 @ 5.55, B:e12 @ 5.55 | matched_event=collision_001; reference_event=True; peak_impulse=A 4243.51, B 4243.51 |
| g33 | 0.00 | CRITICAL_TTC_END | B | A | B:e13 @ 5.55 |  |
| g34 | 0.00 | THROTTLE_END | A | - | A:e17 @ 5.55 |  |
| g35 | 0.00 | BRAKE_START | A | - | A:e18 @ 5.55 |  |
| g36 | 0.00 | CLOSING_START | A | C | A:e19 @ 5.55 |  |
| g37 | 0.00 | CLOSING_START | A | C | A:e20 @ 5.55 |  |
| g38 | 0.00 | CLOSING_START | C | A | C:e06 @ 5.55 |  |
| g39 | 0.00 | CRITICAL_TTC_START | A | C | A:e21 @ 5.55 |  |
| g40 | 0.00 | TRACK_LOST | B | C | B:e14 @ 5.55 |  |
| g41 | 0.05 | BRAKE_END | A | - | A:e22 @ 5.60 |  |
| g42 | 0.05 | CRITICAL_TTC_START | C | A | C:e07 @ 5.60 |  |
| g43 | 0.10 | CLOSING_END | B | A | B:e15 @ 5.65 |  |
| g44 | 0.25 | CLOSING_END | B | C | B:e16 @ 5.80 |  |
| g45 | 0.25 | EGO_PATH_ENTRY | A | C | A:e23 @ 5.80 |  |
| g46 | 0.65 | MOVING_END | B | - | B:e17 @ 6.20 |  |
| g47 | 0.65 | STOP_START | B | - | B:e18 @ 6.20 |  |
| g48 | 0.90 | TRACK_LOST | C | A | C:e08 @ 6.45 |  |
| g49 | 1.05 | COLLISION | - | A, C | A:e24 @ 6.60, C:e09 @ 6.60 | matched_event=collision_002; reference_event=False; peak_impulse=A 322.10, C 322.10 |
| g50 | 1.05 | CRITICAL_TTC_END | A | C | A:e25 @ 6.60 |  |
| g51 | 1.05 | CLOSING_END | A | C | A:e26 @ 6.60 |  |
| g52 | 1.05 | CLOSING_END | A | C | A:e27 @ 6.60 |  |
| g53 | 1.10 | THROTTLE_END | C | - | C:e10 @ 6.65 |  |
| g54 | 1.10 | BRAKE_START | C | - | C:e11 @ 6.65 |  |
| g55 | 1.20 | TRACK_LOST | A | C | A:e28 @ 6.75 |  |
| g56 | 1.25 | TRACK_APPEARED_LEFT | B | U1 | B:e19 @ 6.80 |  |
| g57 | 1.35 | CUT_IN_FROM_LEFT_END | A | C | A:e29 @ 6.90 |  |
| g58 | 1.55 | TRACK_LOST | B | U1 | B:e20 @ 7.10 |  |
| g59 | 1.70 | EGO_PATH_EXIT | B | A | B:e21 @ 7.25 |  |
| g60 | 1.90 | MOVING_END | A | - | A:e30 @ 7.45 |  |
| g61 | 1.90 | MOVING_END | C | - | C:e12 @ 7.45 |  |
| g62 | 1.90 | STOP_START | A | - | A:e31 @ 7.45 |  |
| g63 | 1.90 | STOP_START | C | - | C:e13 @ 7.45 |  |
| g64 | 1.90 | BRAKE_START | A | - | A:e32 @ 7.45 |  |

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
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
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
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g31 --PRECEDES--> g38
    g31 --PRECEDES--> g39
    g31 --PRECEDES--> g40
    g32 --PRECEDES--> g41
    g32 --PRECEDES--> g42
    g33 --PRECEDES--> g41
    g33 --PRECEDES--> g42
    g34 --PRECEDES--> g41
    g34 --PRECEDES--> g42
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g43
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g47 --PRECEDES--> g48
    g48 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g49 --PRECEDES--> g54
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g52 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g53 --PRECEDES--> g55
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g59 --PRECEDES--> g62
    g59 --PRECEDES--> g63
    g59 --PRECEDES--> g64
    g08 --SAME_TRACK--> g10
    g12 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g23
    g12 --SAME_TRACK--> g24
    g08 --SAME_TRACK--> g27
    g08 --SAME_TRACK--> g30
    g12 --SAME_TRACK--> g31
    g08 --SAME_TRACK--> g36
    g12 --SAME_TRACK--> g37
    g12 --SAME_TRACK--> g39
    g08 --SAME_TRACK--> g45
    g08 --SAME_TRACK--> g50
    g08 --SAME_TRACK--> g51
    g12 --SAME_TRACK--> g52
    g12 --SAME_TRACK--> g55
    g08 --SAME_TRACK--> g57
    g09 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g14
    g15 --SAME_TRACK--> g16
    g07 --SAME_TRACK--> g21
    g07 --SAME_TRACK--> g33
    g15 --SAME_TRACK--> g40
    g07 --SAME_TRACK--> g43
    g09 --SAME_TRACK--> g44
    g56 --SAME_TRACK--> g58
    g07 --SAME_TRACK--> g59
    g17 --SAME_TRACK--> g18
    g17 --SAME_TRACK--> g22
    g17 --SAME_TRACK--> g38
    g17 --SAME_TRACK--> g42
    g17 --SAME_TRACK--> g48
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.55 | MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(B,A); TRACK_APPEARED_LEFT(A,C); TRACK_APPEARED_LEFT(B,C); CLOSING_START(A,C); CLOSING_START(B,C) |
| -5.50 | TRACK_APPEARED_LEFT(A,C); CLOSING_START(A,C) |
| -5.05 | CRITICAL_TTC_START(B,A) |
| -4.70 | TRACK_APPEARED_LEFT(B,C); CLOSING_START(B,C) |
| -2.90 | TRACK_APPEARED_RIGHT(C,A); CLOSING_START(C,A) |
| -1.60 | THROTTLE_END(A); BRAKE_START(A) |
| -1.40 | CLOSING_START(B,A) |
| -1.15 | CLOSING_END(C,A) |
| -1.10 | CLOSING_END(A,C) |
| -1.00 | CLOSING_END(A,C); BRAKE_END(A) |
| -0.90 | THROTTLE_START(A) |
| -0.35 | CRITICAL_TTC_START(A,C) |
| -0.15 | THROTTLE_END(B); BRAKE_START(B) |
| -0.10 | CUT_IN_FROM_LEFT_START(A,C) |
| -0.05 | EGO_PATH_ENTRY(A,C) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(B,A); THROTTLE_END(A); BRAKE_START(A); CLOSING_START(A,C); CLOSING_START(A,C); CLOSING_START(C,A); CRITICAL_TTC_START(A,C); TRACK_LOST(B,C) |
| +0.05 | BRAKE_END(A); CRITICAL_TTC_START(C,A) |
| +0.10 | CLOSING_END(B,A) |
| +0.25 | CLOSING_END(B,C); EGO_PATH_ENTRY(A,C) |
| +0.65 | MOVING_END(B); STOP_START(B) |
| +0.90 | TRACK_LOST(C,A) |
| +1.05 | COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,C); CLOSING_END(A,C) |
| +1.10 | THROTTLE_END(C); BRAKE_START(C) |
| +1.20 | TRACK_LOST(A,C) |
| +1.25 | TRACK_APPEARED_LEFT(B,U1) |
| +1.35 | CUT_IN_FROM_LEFT_END(A,C) |
| +1.55 | TRACK_LOST(B,U1) |
| +1.70 | EGO_PATH_EXIT(B,A) |
| +1.90 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C); BRAKE_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (C): critical TTC already active before the cut-in: CRITICAL_TTC_START 5.20 <= CUT_IN_FROM_LEFT_START 5.45 (+0.25 s); EGO_PATH_ENTRY 5.80 after critical TTC (+0.60 s) [local times; t_global: cut_in -0.10, critical_ttc_start -0.35, ego_path_entry +0.25, collision +1.05]
- A's track_002 (C): CRITICAL_TTC_START 5.55, COLLISION with C 6.60 (+1.05 s); EGO_PATH_ENTRY 5.50 before critical TTC (-0.05 s) [local times; t_global: critical_ttc_start +0.00, ego_path_entry -0.05, collision +1.05]
- B's track_001 (A): CRITICAL_TTC_START 0.50, COLLISION with A 5.55 (+5.05 s) [local times; t_global: critical_ttc_start -5.05, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 5.60, COLLISION with A 6.60 (+1.00 s) [local times; t_global: critical_ttc_start +0.05, collision +1.05]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.55 | A | g01 MOVING_START(A) (A:e01)<br>g04 THROTTLE_START(A) (A:e02)<br>g08 TRACK_APPEARED_LEFT(A,C) (A:e03)<br>g10 CLOSING_START(A,C) (A:e04) | ego: not yet observed |
| -5.55 | B | g02 MOVING_START(B) (B:e01)<br>g05 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_FRONT(B,A) (B:e03)<br>g09 TRACK_APPEARED_LEFT(B,C) (B:e04)<br>g11 CLOSING_START(B,C) (B:e05) | ego: not yet observed |
| -5.55 | C | g03 MOVING_START(C) (C:e01)<br>g06 THROTTLE_START(C) (C:e02) | ego: not yet observed |
| -5.50 | A | g12 TRACK_APPEARED_LEFT(A,C) (A:e05)<br>g13 CLOSING_START(A,C) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -5.05 | B | g14 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? |
| -4.70 | B | g15 TRACK_APPEARED_LEFT(B,C) (B:e07)<br>g16 CLOSING_START(B,C) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING |
| -2.90 | C | g17 TRACK_APPEARED_RIGHT(C,A) (C:e03)<br>g18 CLOSING_START(C,A) (C:e04) | ego: MOVING, THROTTLE |
| -1.60 | A | g19 THROTTLE_END(A) (A:e07)<br>g20 BRAKE_START(A) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.40 | B | g21 CLOSING_START(B,A) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| -1.15 | C | g22 CLOSING_END(C,A) (C:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.10 | A | g23 CLOSING_END(A,C) (A:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING |
| -1.00 | A | g24 CLOSING_END(A,C) (A:e10)<br>g25 BRAKE_END(A) (A:e11) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING |
| -0.90 | A | g26 THROTTLE_START(A) (A:e12) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |
| -0.35 | A | g27 CRITICAL_TTC_START(A,C) (A:e13) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state |
| -0.15 | B | g28 THROTTLE_END(B) (B:e10)<br>g29 BRAKE_START(B) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| -0.10 | A | g30 CUT_IN_FROM_LEFT_START(A,C) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: no active state |
| -0.05 | A | g31 EGO_PATH_ENTRY(A,C) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: no active state |
| +0.00 | A | g32 COLLISION(A,B) (A:e16)<br>g34 THROTTLE_END(A) (A:e17)<br>g35 BRAKE_START(A) (A:e18)<br>g36 CLOSING_START(A,C) (A:e19)<br>g37 CLOSING_START(A,C) (A:e20)<br>g39 CRITICAL_TTC_START(A,C) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: IN_EGO_PATH |
| +0.00 | B | g32 COLLISION(A,B) (B:e12)<br>g33 CRITICAL_TTC_END(B,A) (B:e13)<br>g40 TRACK_LOST(B,C) (B:e14) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING |
| +0.00 | C | g38 CLOSING_START(C,A) (C:e06) | ego: MOVING, THROTTLE<br>track_001: no active state |
| +0.05 | A | g41 BRAKE_END(A) (A:e22) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | C | g42 CRITICAL_TTC_START(C,A) (C:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| +0.10 | B | g43 CLOSING_END(B,A) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.25 | B | g44 CLOSING_END(B,C) (B:e16) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.25 | A | g45 EGO_PATH_ENTRY(A,C) (A:e23) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.65 | B | g46 MOVING_END(B) (B:e17)<br>g47 STOP_START(B) (B:e18) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 |
| +0.90 | C | g48 TRACK_LOST(C,A) (C:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC |
| +1.05 | A | g49 COLLISION(A,C) (A:e24)<br>g50 CRITICAL_TTC_END(A,C) (A:e25)<br>g51 CLOSING_END(A,C) (A:e26)<br>g52 CLOSING_END(A,C) (A:e27) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +1.05 | C | g49 COLLISION(A,C) (C:e09) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| +1.10 | C | g53 THROTTLE_END(C) (C:e10)<br>g54 BRAKE_START(C) (C:e11) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| +1.20 | A | g55 TRACK_LOST(A,C) (A:e28) | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track_002: CRITICAL_TTC, IN_EGO_PATH |
| +1.25 | B | g56 TRACK_APPEARED_LEFT(B,U1) (B:e19) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 |
| +1.35 | A | g57 CUT_IN_FROM_LEFT_END(A,C) (A:e29) | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002 |
| +1.55 | B | g58 TRACK_LOST(B,U1) (B:e20) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_004: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_003 |
| +1.70 | B | g59 EGO_PATH_EXIT(B,A) (B:e21) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003, track_004 |
| +1.90 | A | g60 MOVING_END(A) (A:e30)<br>g62 STOP_START(A) (A:e31)<br>g64 BRAKE_START(A) (A:e32) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +1.90 | C | g61 MOVING_END(C) (C:e12)<br>g63 STOP_START(C) (C:e13) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 5.55 s before the reference collision, A started moving (already the case when first observed).
- 5.55 s before the reference collision, B started moving (already the case when first observed).
- 5.55 s before the reference collision, C started moving (already the case when first observed).
- 5.55 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 5.55 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 5.55 s before the reference collision, A's radar started tracking C, which appeared on its left.
- 5.55 s before the reference collision, B's radar started tracking C, which appeared on its left.
- 5.55 s before the reference collision, A observed C start closing in (already the case when first observed).
- 5.55 s before the reference collision, B observed C start closing in (already the case when first observed).
- 5.50 s before the reference collision, A's radar started tracking C, which appeared on its left.
- 5.50 s before the reference collision, A observed C start closing in (already the case when first observed).
- 5.05 s before the reference collision, B's time-to-contact with A became critical.
- 4.70 s before the reference collision, B's radar started tracking C, which appeared on its left.
- 4.70 s before the reference collision, B observed C start closing in (already the case when first observed).
- 2.90 s before the reference collision, C's radar started tracking A, which appeared on its right.
- 2.90 s before the reference collision, C observed A start closing in (already the case when first observed).
- 1.60 s before the reference collision, A released the accelerator.
- 1.60 s before the reference collision, A started braking.
- 1.40 s before the reference collision, B observed A start closing in.
- 1.15 s before the reference collision, C observed A stop closing in.
- 1.10 s before the reference collision, A observed C stop closing in.
- 1.00 s before the reference collision, A observed C stop closing in.
- 1.00 s before the reference collision, A released the brake.
- 0.90 s before the reference collision, A pressed the accelerator.
- 0.35 s before the reference collision, A's time-to-contact with C became critical.
- 0.15 s before the reference collision, B released the accelerator.
- 0.15 s before the reference collision, B started braking.
- 0.10 s before the reference collision, A observed C cutting in from the left.
- 0.05 s before the reference collision, A observed C enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 4244, B: 4244 N*s).
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A released the accelerator.
- At the reference collision, A started braking.
- At the reference collision, A observed C start closing in.
- At the reference collision, A observed C start closing in.
- At the reference collision, C observed A start closing in.
- At the reference collision, A's time-to-contact with C became critical.
- At the reference collision, B's radar lost C (its states are UNKNOWN from then on, not ended).
- 0.05 s after the reference collision, A released the brake.
- 0.05 s after the reference collision, C's time-to-contact with A became critical.
- 0.10 s after the reference collision, B observed A stop closing in.
- 0.25 s after the reference collision, B observed C stop closing in.
- 0.25 s after the reference collision, A observed C enter its forward path corridor.
- 0.65 s after the reference collision, B stopped moving.
- 0.65 s after the reference collision, B came to a stop.
- 0.90 s after the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 1.05 s after the reference collision, A and C both recorded this same collision (peak impulses A: 322, C: 322 N*s).
- 1.05 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.05 s after the reference collision, A observed C stop closing in.
- 1.05 s after the reference collision, A observed C stop closing in.
- 1.10 s after the reference collision, C released the accelerator.
- 1.10 s after the reference collision, C started braking.
- 1.20 s after the reference collision, A's radar lost C (its states are UNKNOWN from then on, not ended).
- 1.25 s after the reference collision, B's radar started tracking anonymous road user U1, which appeared on its left.
- 1.35 s after the reference collision, A observed C's cut-in from the left settle.
- 1.55 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 1.70 s after the reference collision, B observed A leave its forward path corridor.
- 1.90 s after the reference collision, A stopped moving.
- 1.90 s after the reference collision, C stopped moving.
- 1.90 s after the reference collision, A came to a stop.
- 1.90 s after the reference collision, C came to a stop.
- 1.90 s after the reference collision, A started braking.
