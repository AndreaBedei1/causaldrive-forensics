# Global graph - S08/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002, C:track_001#segment_1 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock ALIGNED; observed by others as: A:track_001, B:track_001 |
| U2 | anonymous_road_user | anonymous; observed by C as C:track_001#segment_2 |
| U3 | anonymous_road_user | anonymous; observed by C as C:track_001#segment_3 |
| U1 | anonymous_road_user | anonymous; observed by C as C:track_002 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 4.10 | -4.10 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.10 | -4.10 | reported the reference collision collision_001 |
| C | ALIGNED | - | - | -4.10 | aligned through observed trajectories: the near surfaces of A:track_001, B:track_001, C:track_001#segment_1 on A, C:track_001#segment_2 on A, C:track_001#segment_3 on B, C:track_002 on B lie where their lines of sight enter the body (pooled median 0.62 sigma) at this offset; offsets within 2.00 sigma span [-4.20, -4.00] s and nothing else fits |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12137.11 vs 12137.11 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 4.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 21.7 m -> 11.7 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.47 m/s over 3.0 s (> 1.50)<br>clearance at the contact 11.69 m (beyond 3.50 m: confidence factor 0.02)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma, over 303 samples; 100% within 3 sigma) at C's own velocity (median difference 0.09 m/s) |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.65 m/s over 2.0 s<br>clearance at the contact 0.35 m<br>the only track of A compatible with the contact |
| B:track_001 | C | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.6 m -> 10.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 7.61 m/s over 2.0 s (> 1.50)<br>clearance at the contact 10.71 m (beyond 3.50 m: confidence factor 0.06)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma, over 262 samples; 94% within 3 sigma) at C's own velocity (median difference 0.05 m/s) |
| B:track_002 | A | ASSOCIATED | 0.89 | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.2 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.71 m/s over 2.0 s<br>clearance at the contact 0.46 m<br>the only track of B compatible with the contact |
| C:track_001#segment_1 | A | ASSOCIATED | 1.00 | no matched collision of C names a partner<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma, over 69 samples before A's contact with a third body at +0.00 s; 100% within 3 sigma) at A's own velocity (median difference 0.13 m/s) |
| C:track_001#segment_2 | U2 | ANONYMOUS | - | no matched collision of C names a partner<br>anonymous road user U2: C:track_001#segment_2 |
| C:track_001#segment_3 | U3 | ANONYMOUS | - | no matched collision of C names a partner<br>anonymous road user U3: C:track_001#segment_3 |
| C:track_002 | U1 | ANONYMOUS | - | no matched collision of C names a partner<br>anonymous road user U1: C:track_002 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.10 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.10 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -4.10 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -4.10 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g06 | -4.10 | THROTTLE_START | C | - | C:e02 @ 0.00 | active_at_first_observation=True |
| g07 | -4.10 | TRACK_APPEARED_FRONT | A | C | A:e03 @ 0.00 |  |
| g08 | -4.10 | TRACK_APPEARED_FRONT | C | A | C:e03 @ 0.00 |  |
| g09 | -4.10 | CLOSING_START | A | C | A:e04 @ 0.00 | active_at_first_observation=True |
| g10 | -4.10 | CLOSING_START | C | A | C:e04 @ 0.00 | active_at_first_observation=True |
| g11 | -2.05 | TRACK_APPEARED_RIGHT | A | B | A:e05 @ 2.05 |  |
| g12 | -2.05 | CLOSING_START | A | B | A:e06 @ 2.05 | active_at_first_observation=True |
| g13 | -2.00 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 2.10 |  |
| g14 | -2.00 | TRACK_APPEARED_LEFT | C | U1 | C:e05 @ 2.10 |  |
| g15 | -2.00 | TRACK_APPEARED_RIGHT | B | C | B:e04 @ 2.10 |  |
| g16 | -2.00 | CLOSING_START | B | A | B:e06 @ 2.10 | active_at_first_observation=True |
| g17 | -2.00 | CLOSING_START | B | C | B:e05 @ 2.10 | active_at_first_observation=True |
| g18 | -2.00 | CLOSING_START | C | U1 | C:e06 @ 2.10 | active_at_first_observation=True |
| g19 | -1.75 | THROTTLE_END | C | - | C:e07 @ 2.35 |  |
| g20 | -1.75 | BRAKE_START | C | - | C:e08 @ 2.35 |  |
| g21 | -1.55 | CRITICAL_TTC_START | A | B | A:e07 @ 2.55 |  |
| g22 | -1.50 | CRITICAL_TTC_START | B | A | B:e07 @ 2.60 |  |
| g23 | -1.20 | MOVING_END | C | - | C:e09 @ 2.90 |  |
| g24 | -1.20 | STOP_START | C | - | C:e10 @ 2.90 |  |
| g25 | -0.45 | TRACK_LOST | C | A | C:e11 @ 3.65 |  |
| g26 | -0.40 | TRACK_APPEARED_LEFT | C | U2 | C:e12 @ 3.70 |  |
| g27 | -0.40 | CLOSING_START | C | U2 | C:e13 @ 3.70 | active_at_first_observation=True |
| g28 | 0.00 | COLLISION | - | A, B | A:e08 @ 4.10, B:e08 @ 4.10 | matched_event=collision_001; reference_event=True; peak_impulse=A 12137.11, B 12137.11 |
| g29 | 0.00 | CRITICAL_TTC_END | A | B | A:e09 @ 4.10 |  |
| g30 | 0.00 | CRITICAL_TTC_END | B | A | B:e09 @ 4.10 |  |
| g31 | 0.00 | CLOSING_END | A | B | A:e10 @ 4.10 |  |
| g32 | 0.00 | CLOSING_END | B | A | B:e10 @ 4.10 |  |
| g33 | 0.00 | TURN_LEFT_START | A | - | A:e11 @ 4.10 |  |
| g34 | 0.00 | TURN_RIGHT_START | B | - | B:e11 @ 4.10 |  |
| g35 | 0.05 | THROTTLE_END | A | - | A:e12 @ 4.15 |  |
| g36 | 0.05 | THROTTLE_END | B | - | B:e12 @ 4.15 |  |
| g37 | 0.05 | BRAKE_START | A | - | A:e13 @ 4.15 |  |
| g38 | 0.05 | BRAKE_START | B | - | B:e13 @ 4.15 |  |
| g39 | 0.05 | EGO_PATH_ENTRY | A | C | A:e14 @ 4.15 |  |
| g40 | 0.15 | EGO_PATH_EXIT | A | C | A:e15 @ 4.25 |  |
| g41 | 0.15 | CLOSING_START | A | B | A:e16 @ 4.25 |  |
| g42 | 0.15 | CLOSING_START | B | A | B:e14 @ 4.25 |  |
| g43 | 0.50 | CLOSING_END | B | C | B:e15 @ 4.60 |  |
| g44 | 0.50 | CLOSING_END | C | U2 | C:e14 @ 4.60 |  |
| g45 | 0.50 | TURN_RIGHT_END | B | - | B:e16 @ 4.60 |  |
| g46 | 0.50 | MOVING_END | B | - | B:e17 @ 4.60 |  |
| g47 | 0.50 | STOP_START | B | - | B:e18 @ 4.60 |  |
| g48 | 0.55 | CLOSING_END | A | B | A:e17 @ 4.65 |  |
| g49 | 0.55 | EGO_PATH_ENTRY | C | U1 | C:e15 @ 4.65 |  |
| g50 | 0.60 | TURN_LEFT_END | A | - | A:e18 @ 4.70 |  |
| g51 | 0.65 | CLOSING_END | A | C | A:e19 @ 4.75 |  |
| g52 | 0.65 | CLOSING_END | B | A | B:e19 @ 4.75 |  |
| g53 | 0.65 | CLOSING_END | C | U1 | C:e16 @ 4.75 |  |
| g54 | 0.65 | MOVING_END | A | - | A:e20 @ 4.75 |  |
| g55 | 0.65 | STOP_START | A | - | A:e21 @ 4.75 |  |
| g56 | 0.95 | TRACK_LOST | C | U2 | C:e17 @ 5.05 |  |
| g57 | 1.00 | TRACK_APPEARED_LEFT | C | U3 | C:e18 @ 5.10 |  |
| g58 | 1.70 | TRACK_LOST | C | U1 | C:e19 @ 5.80 |  |
| g59 | 2.15 | EGO_PATH_ENTRY | C | U3 | C:e20 @ 6.25 |  |

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
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g11 --PRECEDES--> g16
    g11 --PRECEDES--> g17
    g11 --PRECEDES--> g18
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g12 --PRECEDES--> g17
    g12 --PRECEDES--> g18
    g13 --PRECEDES--> g19
    g13 --PRECEDES--> g20
    g14 --PRECEDES--> g19
    g14 --PRECEDES--> g20
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g26 --PRECEDES--> g33
    g26 --PRECEDES--> g34
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g28 --PRECEDES--> g36
    g28 --PRECEDES--> g37
    g28 --PRECEDES--> g38
    g28 --PRECEDES--> g39
    g29 --PRECEDES--> g35
    g29 --PRECEDES--> g36
    g29 --PRECEDES--> g37
    g29 --PRECEDES--> g38
    g29 --PRECEDES--> g39
    g30 --PRECEDES--> g35
    g30 --PRECEDES--> g36
    g30 --PRECEDES--> g37
    g30 --PRECEDES--> g38
    g30 --PRECEDES--> g39
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g31 --PRECEDES--> g38
    g31 --PRECEDES--> g39
    g32 --PRECEDES--> g35
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g32 --PRECEDES--> g38
    g32 --PRECEDES--> g39
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g33 --PRECEDES--> g39
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g40 --PRECEDES--> g45
    g40 --PRECEDES--> g46
    g40 --PRECEDES--> g47
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g41 --PRECEDES--> g46
    g41 --PRECEDES--> g47
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g52 --PRECEDES--> g56
    g53 --PRECEDES--> g56
    g54 --PRECEDES--> g56
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g07 --SAME_TRACK--> g09
    g11 --SAME_TRACK--> g12
    g11 --SAME_TRACK--> g21
    g11 --SAME_TRACK--> g29
    g11 --SAME_TRACK--> g31
    g07 --SAME_TRACK--> g39
    g07 --SAME_TRACK--> g40
    g11 --SAME_TRACK--> g41
    g11 --SAME_TRACK--> g48
    g07 --SAME_TRACK--> g51
    g15 --SAME_TRACK--> g17
    g13 --SAME_TRACK--> g16
    g13 --SAME_TRACK--> g22
    g13 --SAME_TRACK--> g30
    g13 --SAME_TRACK--> g32
    g13 --SAME_TRACK--> g42
    g15 --SAME_TRACK--> g43
    g13 --SAME_TRACK--> g52
    g08 --SAME_TRACK--> g10
    g14 --SAME_TRACK--> g18
    g08 --SAME_TRACK--> g25
    g26 --SAME_TRACK--> g27
    g26 --SAME_TRACK--> g44
    g14 --SAME_TRACK--> g49
    g14 --SAME_TRACK--> g53
    g26 --SAME_TRACK--> g56
    g14 --SAME_TRACK--> g58
    g57 --SAME_TRACK--> g59
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.10 | MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C); TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A) |
| -2.05 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -2.00 | TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_LEFT(C,U1); TRACK_APPEARED_RIGHT(B,C); CLOSING_START(B,A); CLOSING_START(B,C); CLOSING_START(C,U1) |
| -1.75 | THROTTLE_END(C); BRAKE_START(C) |
| -1.55 | CRITICAL_TTC_START(A,B) |
| -1.50 | CRITICAL_TTC_START(B,A) |
| -1.20 | MOVING_END(C); STOP_START(C) |
| -0.45 | TRACK_LOST(C,A) |
| -0.40 | TRACK_APPEARED_LEFT(C,U2); CLOSING_START(C,U2) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A); TURN_LEFT_START(A); TURN_RIGHT_START(B) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); EGO_PATH_ENTRY(A,C) |
| +0.15 | EGO_PATH_EXIT(A,C); CLOSING_START(A,B); CLOSING_START(B,A) |
| +0.50 | CLOSING_END(B,C); CLOSING_END(C,U2); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B) |
| +0.55 | CLOSING_END(A,B); EGO_PATH_ENTRY(C,U1) |
| +0.60 | TURN_LEFT_END(A) |
| +0.65 | CLOSING_END(A,C); CLOSING_END(B,A); CLOSING_END(C,U1); MOVING_END(A); STOP_START(A) |
| +0.95 | TRACK_LOST(C,U2) |
| +1.00 | TRACK_APPEARED_LEFT(C,U3) |
| +1.70 | TRACK_LOST(C,U1) |
| +2.15 | EGO_PATH_ENTRY(C,U3) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (C): EGO_PATH_ENTRY 4.15, no critical TTC [local times; t_global: ego_path_entry +0.05]
- A's track_002 (B): CRITICAL_TTC_START 2.55, COLLISION with B 4.10 (+1.55 s) [local times; t_global: critical_ttc_start -1.55, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.60, COLLISION with A 4.10 (+1.50 s) [local times; t_global: critical_ttc_start -1.50, collision +0.00]
- C's track_001#segment_3 (unidentified U3): EGO_PATH_ENTRY 6.25, no critical TTC [local times; t_global: ego_path_entry +2.15]
- C's track_002 (unidentified U1): EGO_PATH_ENTRY 4.65, no critical TTC [local times; t_global: ego_path_entry +0.55]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.10 | A | g01 MOVING_START(A) (A:e01)<br>g04 THROTTLE_START(A) (A:e02)<br>g07 TRACK_APPEARED_FRONT(A,C) (A:e03)<br>g09 CLOSING_START(A,C) (A:e04) | ego: not yet observed |
| -4.10 | B | g02 MOVING_START(B) (B:e01)<br>g05 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -4.10 | C | g03 MOVING_START(C) (C:e01)<br>g06 THROTTLE_START(C) (C:e02)<br>g08 TRACK_APPEARED_FRONT(C,A) (C:e03)<br>g10 CLOSING_START(C,A) (C:e04) | ego: not yet observed |
| -2.05 | A | g11 TRACK_APPEARED_RIGHT(A,B) (A:e05)<br>g12 CLOSING_START(A,B) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.00 | B | g13 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g15 TRACK_APPEARED_RIGHT(B,C) (B:e04)<br>g16 CLOSING_START(B,A) (B:e06)<br>g17 CLOSING_START(B,C) (B:e05) | ego: MOVING, THROTTLE |
| -2.00 | C | g14 TRACK_APPEARED_LEFT(C,U1) (C:e05)<br>g18 CLOSING_START(C,U1) (C:e06) | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING |
| -1.75 | C | g19 THROTTLE_END(C) (C:e07)<br>g20 BRAKE_START(C) (C:e08) | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.55 | A | g21 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.50 | B | g22 CRITICAL_TTC_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.20 | C | g23 MOVING_END(C) (C:e09)<br>g24 STOP_START(C) (C:e10) | ego: MOVING, BRAKE<br>track_001#segment_1: CLOSING<br>track_002: CLOSING |
| -0.45 | C | g25 TRACK_LOST(C,A) (C:e11) | ego: STOP, BRAKE<br>track_001#segment_1: CLOSING<br>track_002: CLOSING |
| -0.40 | C | g26 TRACK_APPEARED_LEFT(C,U2) (C:e12)<br>g27 CLOSING_START(C,U2) (C:e13) | ego: STOP, BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 |
| +0.00 | A | g28 COLLISION(A,B) (A:e08)<br>g29 CRITICAL_TTC_END(A,B) (A:e09)<br>g31 CLOSING_END(A,B) (A:e10)<br>g33 TURN_LEFT_START(A) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.00 | B | g28 COLLISION(A,B) (B:e08)<br>g30 CRITICAL_TTC_END(B,A) (B:e09)<br>g32 CLOSING_END(B,A) (B:e10)<br>g34 TURN_RIGHT_START(B) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.05 | A | g35 THROTTLE_END(A) (A:e12)<br>g37 BRAKE_START(A) (A:e13)<br>g39 EGO_PATH_ENTRY(A,C) (A:e14) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: no active state |
| +0.05 | B | g36 THROTTLE_END(B) (B:e12)<br>g38 BRAKE_START(B) (B:e13) | ego: MOVING, THROTTLE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: no active state |
| +0.15 | A | g40 EGO_PATH_EXIT(A,C) (A:e15)<br>g41 CLOSING_START(A,B) (A:e16) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state |
| +0.15 | B | g42 CLOSING_START(B,A) (B:e14) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: no active state |
| +0.50 | B | g43 CLOSING_END(B,C) (B:e15)<br>g45 TURN_RIGHT_END(B) (B:e16)<br>g46 MOVING_END(B) (B:e17)<br>g47 STOP_START(B) (B:e18) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING |
| +0.50 | C | g44 CLOSING_END(C,U2) (C:e14) | ego: STOP, BRAKE<br>track_001#segment_2: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 |
| +0.55 | A | g48 CLOSING_END(A,B) (A:e17) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING |
| +0.55 | C | g49 EGO_PATH_ENTRY(C,U1) (C:e15) | ego: STOP, BRAKE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 |
| +0.60 | A | g50 TURN_LEFT_END(A) (A:e18) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: no active state |
| +0.65 | A | g51 CLOSING_END(A,C) (A:e19)<br>g54 MOVING_END(A) (A:e20)<br>g55 STOP_START(A) (A:e21) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state |
| +0.65 | B | g52 CLOSING_END(B,A) (B:e19) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: CLOSING |
| +0.65 | C | g53 CLOSING_END(C,U1) (C:e16) | ego: STOP, BRAKE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 |
| +0.95 | C | g56 TRACK_LOST(C,U2) (C:e17) | ego: STOP, BRAKE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 |
| +1.00 | C | g57 TRACK_APPEARED_LEFT(C,U3) (C:e18) | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +1.70 | C | g58 TRACK_LOST(C,U1) (C:e19) | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +2.15 | C | g59 EGO_PATH_ENTRY(C,U3) (C:e20) | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002 |

## Plain-language reading

- 4.10 s before the reference collision, A started moving (already the case when first observed).
- 4.10 s before the reference collision, B started moving (already the case when first observed).
- 4.10 s before the reference collision, C started moving (already the case when first observed).
- 4.10 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 4.10 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 4.10 s before the reference collision, A observed C start closing in (already the case when first observed).
- 4.10 s before the reference collision, C observed A start closing in (already the case when first observed).
- 2.05 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 2.05 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.00 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.00 s before the reference collision, C's radar started tracking anonymous road user U1, which appeared on its left.
- 2.00 s before the reference collision, B's radar started tracking C, which appeared on its right.
- 2.00 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.00 s before the reference collision, B observed C start closing in (already the case when first observed).
- 2.00 s before the reference collision, C observed anonymous road user U1 start closing in (already the case when first observed).
- 1.75 s before the reference collision, C released the accelerator.
- 1.75 s before the reference collision, C started braking.
- 1.55 s before the reference collision, A's time-to-contact with B became critical.
- 1.50 s before the reference collision, B's time-to-contact with A became critical.
- 1.20 s before the reference collision, C stopped moving.
- 1.20 s before the reference collision, C came to a stop.
- 0.45 s before the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.40 s before the reference collision, C's radar started tracking anonymous road user U2, which appeared on its left.
- 0.40 s before the reference collision, C observed anonymous road user U2 start closing in (already the case when first observed).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12137, B: 12137 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- At the reference collision, A started turning left.
- At the reference collision, B started turning right.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A observed C enter its forward path corridor.
- 0.15 s after the reference collision, A observed C leave its forward path corridor.
- 0.15 s after the reference collision, A observed B start closing in.
- 0.15 s after the reference collision, B observed A start closing in.
- 0.50 s after the reference collision, B observed C stop closing in.
- 0.50 s after the reference collision, C observed anonymous road user U2 stop closing in.
- 0.50 s after the reference collision, B stopped turning right.
- 0.50 s after the reference collision, B stopped moving.
- 0.50 s after the reference collision, B came to a stop.
- 0.55 s after the reference collision, A observed B stop closing in.
- 0.55 s after the reference collision, C observed anonymous road user U1 enter its forward path corridor.
- 0.60 s after the reference collision, A stopped turning left.
- 0.65 s after the reference collision, A observed C stop closing in.
- 0.65 s after the reference collision, B observed A stop closing in.
- 0.65 s after the reference collision, C observed anonymous road user U1 stop closing in.
- 0.65 s after the reference collision, A stopped moving.
- 0.65 s after the reference collision, A came to a stop.
- 0.95 s after the reference collision, C's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the reference collision, C's radar started tracking anonymous road user U3, which appeared on its left.
- 1.70 s after the reference collision, C's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 2.15 s after the reference collision, C observed anonymous road user U3 enter its forward path corridor.
