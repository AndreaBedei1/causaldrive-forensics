# Global graph - S18/run_0_abreast

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A as A:track_001#segment_1 |
| U4 | anonymous_road_user | anonymous; observed by A as A:track_001#segment_2 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_001#segment_3, B:track_002, B:track_004 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_003 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e18 | 6.20 | -6.20 | reported the reference collision collision_001 |
| B | ALIGNED | B:e13 | 6.20 | -6.20 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1079.56 vs 1079.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>lost 5.95 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 15.5 m -> 15.6 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001#segment_1 |
| A:track_001#segment_2 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 5.90 s before the matched collision<br>lost 2.80 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 15.2 m -> 15.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.81 m/s over 0.2 s<br>anonymous road user U4: A:track_001#segment_2 |
| A:track_001#segment_3 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 2.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.1 m -> 15.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.91 m/s over 2.8 s<br>clearance at the contact 15.14 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.28 m/s over 3.0 s<br>clearance at the contact 0.18 m<br>the only track of A compatible with the contact |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 5.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.5 m -> 15.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.37 m/s over 3.0 s<br>clearance at the contact 15.39 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: B:track_003, A:track_003 |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.6 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.49 m/s over 3.0 s<br>clearance at the contact 0.52 m<br>the only compatible track of B touching it at the contact (clearance 0.52 m; track_002, track_003 at 16.50 m, 17.18 m) |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 17.6 m -> 16.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.15 m/s over 3.0 s<br>clearance at the contact 16.50 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 3 persistent tracks of B are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.0 m -> 17.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.10 m/s over 3.0 s<br>clearance at the contact 17.14 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 3 persistent tracks of B are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U3: B:track_003, A:track_003 |
| B:track_004 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>lost 1.65 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 21.9 m -> 20.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.06 m/s over 1.3 s<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.20 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.20 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.20 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -6.20 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -6.20 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 |  |
| g06 | -6.20 | TRACK_APPEARED_RIGHT | A | U1 | A:e04 @ 0.00 |  |
| g07 | -6.20 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 |  |
| g08 | -6.20 | TRACK_APPEARED_RIGHT | B | U2 | B:e04 @ 0.00 |  |
| g09 | -6.20 | TRACK_APPEARED_RIGHT | B | U2 | B:e06 @ 0.00 |  |
| g10 | -6.20 | TRACK_APPEARED_RIGHT | B | U3 | B:e05 @ 0.00 |  |
| g11 | -6.20 | CLOSING_START | B | U2 | B:e07 @ 0.00 | active_at_first_observation=True |
| g12 | -6.20 | CLOSING_START | B | U2 | B:e09 @ 0.00 | active_at_first_observation=True |
| g13 | -6.20 | CLOSING_START | B | U3 | B:e08 @ 0.00 | active_at_first_observation=True |
| g14 | -5.95 | TRACK_APPEARED_FRONT | A | U3 | A:e05 @ 0.25 |  |
| g15 | -5.95 | TRACK_LOST | A | U1 | A:e06 @ 0.25 |  |
| g16 | -5.90 | TRACK_APPEARED_RIGHT | A | U4 | A:e07 @ 0.30 |  |
| g17 | -5.45 | EGO_PATH_EXIT | A | U3 | A:e08 @ 0.75 |  |
| g18 | -3.80 | CLOSING_START | A | U3 | A:e09 @ 2.40 |  |
| g19 | -2.80 | TRACK_LOST | A | U4 | A:e10 @ 3.40 |  |
| g20 | -2.75 | TRACK_APPEARED_FRONT | A | U2 | A:e11 @ 3.45 |  |
| g21 | -2.25 | CRITICAL_TTC_START | A | U2 | A:e12 @ 3.95 |  |
| g22 | -2.00 | CLOSING_END | A | U3 | A:e13 @ 4.20 |  |
| g23 | -1.65 | TRACK_LOST | B | U2 | B:e10 @ 4.55 |  |
| g24 | -1.05 | CRITICAL_TTC_START | A | B | A:e14 @ 5.15 |  |
| g25 | -0.65 | CRITICAL_TTC_START | B | A | B:e11 @ 5.55 |  |
| g26 | -0.60 | CLOSING_START | A | B | A:e15 @ 5.60 |  |
| g27 | -0.55 | EGO_PATH_EXIT | A | U2 | A:e16 @ 5.65 |  |
| g28 | -0.55 | CLOSING_START | B | A | B:e12 @ 5.65 |  |
| g29 | -0.45 | CRITICAL_TTC_END | A | U2 | A:e17 @ 5.75 |  |
| g30 | 0.00 | COLLISION | - | A, B | A:e18 @ 6.20, B:e13 @ 6.20 | matched_event=collision_001; reference_event=True; peak_impulse=A 1079.56, B 1079.56 |
| g31 | 0.00 | CRITICAL_TTC_END | A | B | A:e19 @ 6.20 |  |
| g32 | 0.00 | CRITICAL_TTC_END | B | A | B:e14 @ 6.20 |  |
| g33 | 0.05 | THROTTLE_END | A | - | A:e20 @ 6.25 |  |
| g34 | 0.05 | THROTTLE_END | B | - | B:e15 @ 6.25 |  |
| g35 | 0.05 | BRAKE_START | A | - | A:e21 @ 6.25 |  |
| g36 | 0.05 | BRAKE_START | B | - | B:e16 @ 6.25 |  |
| g37 | 0.10 | CLOSING_END | B | U3 | B:e17 @ 6.30 |  |
| g38 | 0.20 | CLOSING_END | A | B | A:e22 @ 6.40 |  |
| g39 | 0.20 | CLOSING_END | B | U2 | B:e18 @ 6.40 |  |
| g40 | 0.30 | CLOSING_END | B | A | B:e19 @ 6.50 |  |
| g41 | 1.05 | MOVING_END | B | - | B:e20 @ 7.25 |  |
| g42 | 1.05 | STOP_START | B | - | B:e21 @ 7.25 |  |
| g43 | 1.15 | MOVING_END | A | - | A:e23 @ 7.35 |  |
| g44 | 1.15 | STOP_START | A | - | A:e24 @ 7.35 |  |
| g45 | 2.75 | TRACK_LOST | B | U2 | B:e22 @ 8.95 |  |
| g46 | 2.75 | TRACK_LOST | B | U3 | B:e23 @ 8.95 |  |
| g47 | 3.70 | CUT_IN_FROM_RIGHT_START | A | U2 | A:e25 @ 9.90 |  |
| g48 | 4.00 | TRACK_LOST | A | U2 | A:e26 @ 10.20 |  |
| g49 | 4.25 | TRACK_LOST | A | U3 | A:e27 @ 10.45 |  |

## Edges

```
    g01 --PRECEDES--> g14
    g01 --PRECEDES--> g15
    g02 --PRECEDES--> g14
    g02 --PRECEDES--> g15
    g03 --PRECEDES--> g14
    g03 --PRECEDES--> g15
    g04 --PRECEDES--> g14
    g04 --PRECEDES--> g15
    g05 --PRECEDES--> g14
    g05 --PRECEDES--> g15
    g06 --PRECEDES--> g14
    g06 --PRECEDES--> g15
    g07 --PRECEDES--> g14
    g07 --PRECEDES--> g15
    g08 --PRECEDES--> g14
    g08 --PRECEDES--> g15
    g09 --PRECEDES--> g14
    g09 --PRECEDES--> g15
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
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
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g40
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g48 --PRECEDES--> g49
    g06 --SAME_TRACK--> g15
    g14 --SAME_TRACK--> g17
    g14 --SAME_TRACK--> g18
    g16 --SAME_TRACK--> g19
    g20 --SAME_TRACK--> g21
    g14 --SAME_TRACK--> g22
    g05 --SAME_TRACK--> g24
    g05 --SAME_TRACK--> g26
    g20 --SAME_TRACK--> g27
    g20 --SAME_TRACK--> g29
    g05 --SAME_TRACK--> g31
    g05 --SAME_TRACK--> g38
    g20 --SAME_TRACK--> g47
    g20 --SAME_TRACK--> g48
    g14 --SAME_TRACK--> g49
    g08 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g13
    g09 --SAME_TRACK--> g12
    g09 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g25
    g07 --SAME_TRACK--> g28
    g07 --SAME_TRACK--> g32
    g10 --SAME_TRACK--> g37
    g08 --SAME_TRACK--> g39
    g07 --SAME_TRACK--> g40
    g08 --SAME_TRACK--> g45
    g10 --SAME_TRACK--> g46
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.20 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U2); TRACK_APPEARED_RIGHT(B,U2); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U2); CLOSING_START(B,U2); CLOSING_START(B,U3) |
| -5.95 | TRACK_APPEARED_FRONT(A,U3); TRACK_LOST(A,U1) |
| -5.90 | TRACK_APPEARED_RIGHT(A,U4) |
| -5.45 | EGO_PATH_EXIT(A,U3) |
| -3.80 | CLOSING_START(A,U3) |
| -2.80 | TRACK_LOST(A,U4) |
| -2.75 | TRACK_APPEARED_FRONT(A,U2) |
| -2.25 | CRITICAL_TTC_START(A,U2) |
| -2.00 | CLOSING_END(A,U3) |
| -1.65 | TRACK_LOST(B,U2) |
| -1.05 | CRITICAL_TTC_START(A,B) |
| -0.65 | CRITICAL_TTC_START(B,A) |
| -0.60 | CLOSING_START(A,B) |
| -0.55 | EGO_PATH_EXIT(A,U2); CLOSING_START(B,A) |
| -0.45 | CRITICAL_TTC_END(A,U2) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CLOSING_END(B,U3) |
| +0.20 | CLOSING_END(A,B); CLOSING_END(B,U2) |
| +0.30 | CLOSING_END(B,A) |
| +1.05 | MOVING_END(B); STOP_START(B) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +2.75 | TRACK_LOST(B,U2); TRACK_LOST(B,U3) |
| +3.70 | CUT_IN_FROM_RIGHT_START(A,U2) |
| +4.00 | TRACK_LOST(A,U2) |
| +4.25 | TRACK_LOST(A,U3) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001#segment_3 (unidentified U2): CUT_IN_FROM_RIGHT_START 9.90, no critical TTC after it [local times; t_global: cut_in +3.70, critical_ttc_start -2.25, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 5.15, COLLISION with B 6.20 (+1.05 s) [local times; t_global: critical_ttc_start -1.05, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 5.55, COLLISION with A 6.20 (+0.65 s) [local times; t_global: critical_ttc_start -0.65, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.20 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04) | ego: not yet observed |
| -6.20 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g09 TRACK_APPEARED_RIGHT(B,U2) (B:e06)<br>g10 TRACK_APPEARED_RIGHT(B,U3) (B:e05)<br>g11 CLOSING_START(B,U2) (B:e07)<br>g12 CLOSING_START(B,U2) (B:e09)<br>g13 CLOSING_START(B,U3) (B:e08) | ego: not yet observed |
| -5.95 | A | g14 TRACK_APPEARED_FRONT(A,U3) (A:e05)<br>g15 TRACK_LOST(A,U1) (A:e06) | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC? |
| -5.90 | A | g16 TRACK_APPEARED_RIGHT(A,U4) (A:e07) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 |
| -5.45 | A | g17 EGO_PATH_EXIT(A,U3) (A:e08) | ego: MOVING, THROTTLE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 |
| -3.80 | A | g18 CLOSING_START(A,U3) (A:e09) | ego: MOVING, THROTTLE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1 |
| -2.80 | A | g19 TRACK_LOST(A,U4) (A:e10) | ego: MOVING, THROTTLE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 |
| -2.75 | A | g20 TRACK_APPEARED_FRONT(A,U2) (A:e11) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -2.25 | A | g21 CRITICAL_TTC_START(A,U2) (A:e12) | ego: MOVING, THROTTLE<br>track_001#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -2.00 | A | g22 CLOSING_END(A,U3) (A:e13) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -1.65 | B | g23 TRACK_LOST(B,U2) (B:e10) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| -1.05 | A | g24 CRITICAL_TTC_START(A,B) (A:e14) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -0.65 | B | g25 CRITICAL_TTC_START(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004 |
| -0.60 | A | g26 CLOSING_START(A,B) (A:e15) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -0.55 | A | g27 EGO_PATH_EXIT(A,U2) (A:e16) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -0.55 | B | g28 CLOSING_START(B,A) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004 |
| -0.45 | A | g29 CRITICAL_TTC_END(A,U2) (A:e17) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +0.00 | A | g30 COLLISION(A,B) (A:e18)<br>g31 CRITICAL_TTC_END(A,B) (A:e19) | ego: MOVING, THROTTLE<br>track_001#segment_3: no active state<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +0.00 | B | g30 COLLISION(A,B) (B:e13)<br>g32 CRITICAL_TTC_END(B,A) (B:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004 |
| +0.05 | A | g33 THROTTLE_END(A) (A:e20)<br>g35 BRAKE_START(A) (A:e21) | ego: MOVING, THROTTLE<br>track_001#segment_3: no active state<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +0.05 | B | g34 THROTTLE_END(B) (B:e15)<br>g36 BRAKE_START(B) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004 |
| +0.10 | B | g37 CLOSING_END(B,U3) (B:e17) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004 |
| +0.20 | A | g38 CLOSING_END(A,B) (A:e22) | ego: MOVING, BRAKE<br>track_001#segment_3: no active state<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +0.20 | B | g39 CLOSING_END(B,U2) (B:e18) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_004 |
| +0.30 | B | g40 CLOSING_END(B,A) (B:e19) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_004 |
| +1.05 | B | g41 MOVING_END(B) (B:e20)<br>g42 STOP_START(B) (B:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_004 |
| +1.15 | A | g43 MOVING_END(A) (A:e23)<br>g44 STOP_START(A) (A:e24) | ego: MOVING, BRAKE<br>track_001#segment_3: no active state<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +2.75 | B | g45 TRACK_LOST(B,U2) (B:e22)<br>g46 TRACK_LOST(B,U3) (B:e23) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_004 |
| +3.70 | A | g47 CUT_IN_FROM_RIGHT_START(A,U2) (A:e25) | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +4.00 | A | g48 TRACK_LOST(A,U2) (A:e26) | ego: STOP, BRAKE<br>track_001#segment_3: CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +4.25 | A | g49 TRACK_LOST(A,U3) (A:e27) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_001#segment_3 |

## Plain-language reading

- 6.20 s before the reference collision, A started moving (already the case when first observed).
- 6.20 s before the reference collision, B started moving (already the case when first observed).
- 6.20 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.20 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.20 s before the reference collision, B observed anonymous road user U2 start closing in (already the case when first observed).
- 6.20 s before the reference collision, B observed anonymous road user U2 start closing in (already the case when first observed).
- 6.20 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 5.95 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 5.95 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 5.90 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 5.45 s before the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 3.80 s before the reference collision, A observed anonymous road user U3 start closing in.
- 2.80 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 2.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 2.25 s before the reference collision, A's time-to-contact with anonymous road user U2 became critical.
- 2.00 s before the reference collision, A observed anonymous road user U3 stop closing in.
- 1.65 s before the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 1.05 s before the reference collision, A's time-to-contact with B became critical.
- 0.65 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, A observed B start closing in.
- 0.55 s before the reference collision, A observed anonymous road user U2 leave its forward path corridor.
- 0.55 s before the reference collision, B observed A start closing in.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U2 stopped being critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1080, B: 1080 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B observed anonymous road user U3 stop closing in.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.20 s after the reference collision, B observed anonymous road user U2 stop closing in.
- 0.30 s after the reference collision, B observed A stop closing in.
- 1.05 s after the reference collision, B stopped moving.
- 1.05 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 2.75 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.75 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.70 s after the reference collision, A observed anonymous road user U2 cutting in from the right.
- 4.00 s after the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
