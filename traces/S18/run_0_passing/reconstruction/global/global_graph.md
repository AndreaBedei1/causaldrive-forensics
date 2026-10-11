# Global graph - S18/run_0_passing

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A as A:track_001 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_002, B:track_004 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_004, B:track_003, B:track_005 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e17 | 6.20 | -6.20 | reported the reference collision collision_001 |
| B | ALIGNED | B:e14 | 6.20 | -6.20 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1092.43 vs 1092.43 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m)

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.2 m -> 15.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.81 m/s over 3.0 s<br>clearance at the contact 15.18 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U1: A:track_001 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.27 m/s over 3.0 s<br>clearance at the contact 0.18 m<br>the only track of A compatible with the contact |
| A:track_003 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 6.05 s before the matched collision<br>lost 2.70 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 15.2 m -> 15.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.98 m/s over 0.3 s<br>anonymous road user U2: B:track_002, B:track_004, A:track_003 |
| A:track_004 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 2.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 17.1 m -> 18.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.17 m/s over 2.3 s<br>clearance at the contact 17.06 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: B:track_003, A:track_004, B:track_005 |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.6 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.50 m/s over 3.0 s<br>clearance at the contact 0.53 m<br>the only compatible track of B touching it at the contact (clearance 0.53 m; track_002 at 16.69 m) |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 17.6 m -> 16.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.14 m/s over 3.0 s<br>clearance at the contact 16.69 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_001, track_002)<br>anonymous road user U2: B:track_002, B:track_004, A:track_003 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 6.20 s before the matched collision<br>lost 1.15 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 19.5 m -> 20.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.88 m/s over 1.8 s<br>anonymous road user U3: B:track_003, A:track_004, B:track_005 |
| B:track_004 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 6.20 s before the matched collision<br>lost 1.65 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 21.9 m -> 20.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.07 m/s over 1.3 s<br>anonymous road user U2: B:track_002, B:track_004, A:track_003 |
| B:track_005 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1092.43 vs 1092.43 N*s)<br>tracked for 0.25 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 20.3 m -> 20.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.87 m/s over 0.2 s<br>clearance at the contact 20.28 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: B:track_003, A:track_004, B:track_005 |

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
| g12 | -6.10 | CLOSING_START | B | U2 | B:e08 @ 0.10 |  |
| g13 | -6.05 | TRACK_APPEARED_FRONT | A | U2 | A:e05 @ 0.15 |  |
| g14 | -5.55 | CRITICAL_TTC_START | A | U2 | A:e06 @ 0.65 |  |
| g15 | -3.60 | CRITICAL_TTC_START | A | U1 | A:e07 @ 2.60 |  |
| g16 | -3.20 | CUT_IN_FROM_RIGHT_START | A | U1 | A:e08 @ 3.00 |  |
| g17 | -2.75 | EGO_PATH_ENTRY | A | U1 | A:e09 @ 3.45 |  |
| g18 | -2.70 | TRACK_LOST | A | U2 | A:e10 @ 3.50 |  |
| g19 | -2.30 | TRACK_APPEARED_RIGHT | A | U3 | A:e11 @ 3.90 |  |
| g20 | -1.90 | CUT_IN_FROM_RIGHT_END | A | U1 | A:e12 @ 4.30 |  |
| g21 | -1.65 | TRACK_LOST | B | U2 | B:e09 @ 4.55 |  |
| g22 | -1.15 | TRACK_LOST | B | U3 | B:e10 @ 5.05 |  |
| g23 | -1.05 | CRITICAL_TTC_START | A | B | A:e13 @ 5.15 |  |
| g24 | -0.65 | CRITICAL_TTC_START | B | A | B:e11 @ 5.55 |  |
| g25 | -0.60 | CLOSING_START | A | B | A:e14 @ 5.60 |  |
| g26 | -0.55 | EGO_PATH_EXIT | A | U1 | A:e15 @ 5.65 |  |
| g27 | -0.55 | CLOSING_START | B | A | B:e12 @ 5.65 |  |
| g28 | -0.45 | CRITICAL_TTC_END | A | U1 | A:e16 @ 5.75 |  |
| g29 | -0.25 | TRACK_APPEARED_RIGHT | B | U3 | B:e13 @ 5.95 |  |
| g30 | 0.00 | COLLISION | - | A, B | A:e17 @ 6.20, B:e14 @ 6.20 | matched_event=collision_001; reference_event=True; peak_impulse=A 1092.43, B 1092.43 |
| g31 | 0.00 | CRITICAL_TTC_END | A | B | A:e18 @ 6.20 |  |
| g32 | 0.00 | CRITICAL_TTC_END | B | A | B:e15 @ 6.20 |  |
| g33 | 0.05 | THROTTLE_END | A | - | A:e19 @ 6.25 |  |
| g34 | 0.05 | THROTTLE_END | B | - | B:e16 @ 6.25 |  |
| g35 | 0.05 | BRAKE_START | A | - | A:e20 @ 6.25 |  |
| g36 | 0.05 | BRAKE_START | B | - | B:e17 @ 6.25 |  |
| g37 | 0.20 | CLOSING_END | A | B | A:e21 @ 6.40 |  |
| g38 | 0.20 | CLOSING_END | B | U2 | B:e18 @ 6.40 |  |
| g39 | 0.30 | CLOSING_END | B | A | B:e19 @ 6.50 |  |
| g40 | 1.05 | MOVING_END | B | - | B:e20 @ 7.25 |  |
| g41 | 1.05 | STOP_START | B | - | B:e21 @ 7.25 |  |
| g42 | 1.15 | MOVING_END | A | - | A:e22 @ 7.35 |  |
| g43 | 1.15 | STOP_START | A | - | A:e23 @ 7.35 |  |
| g44 | 2.55 | TRACK_LOST | B | U3 | B:e22 @ 8.75 |  |
| g45 | 2.75 | TRACK_LOST | B | U2 | B:e23 @ 8.95 |  |
| g46 | 3.50 | TRACK_LOST | A | U3 | A:e24 @ 9.70 |  |
| g47 | 3.70 | CUT_IN_FROM_RIGHT_START | A | U1 | A:e25 @ 9.90 |  |
| g48 | 4.00 | TRACK_LOST | A | U1 | A:e26 @ 10.20 |  |

## Edges

```
    g01 --PRECEDES--> g12
    g02 --PRECEDES--> g12
    g03 --PRECEDES--> g12
    g04 --PRECEDES--> g12
    g05 --PRECEDES--> g12
    g06 --PRECEDES--> g12
    g07 --PRECEDES--> g12
    g08 --PRECEDES--> g12
    g09 --PRECEDES--> g12
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
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
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g28
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
    g33 --PRECEDES--> g38
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g13 --SAME_TRACK--> g14
    g06 --SAME_TRACK--> g15
    g06 --SAME_TRACK--> g16
    g06 --SAME_TRACK--> g17
    g13 --SAME_TRACK--> g18
    g06 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g23
    g05 --SAME_TRACK--> g25
    g06 --SAME_TRACK--> g26
    g06 --SAME_TRACK--> g28
    g05 --SAME_TRACK--> g31
    g05 --SAME_TRACK--> g37
    g19 --SAME_TRACK--> g46
    g06 --SAME_TRACK--> g47
    g06 --SAME_TRACK--> g48
    g08 --SAME_TRACK--> g11
    g09 --SAME_TRACK--> g12
    g09 --SAME_TRACK--> g21
    g10 --SAME_TRACK--> g22
    g07 --SAME_TRACK--> g24
    g07 --SAME_TRACK--> g27
    g07 --SAME_TRACK--> g32
    g08 --SAME_TRACK--> g38
    g07 --SAME_TRACK--> g39
    g29 --SAME_TRACK--> g44
    g08 --SAME_TRACK--> g45
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.20 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U2); TRACK_APPEARED_RIGHT(B,U2); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U2) |
| -6.10 | CLOSING_START(B,U2) |
| -6.05 | TRACK_APPEARED_FRONT(A,U2) |
| -5.55 | CRITICAL_TTC_START(A,U2) |
| -3.60 | CRITICAL_TTC_START(A,U1) |
| -3.20 | CUT_IN_FROM_RIGHT_START(A,U1) |
| -2.75 | EGO_PATH_ENTRY(A,U1) |
| -2.70 | TRACK_LOST(A,U2) |
| -2.30 | TRACK_APPEARED_RIGHT(A,U3) |
| -1.90 | CUT_IN_FROM_RIGHT_END(A,U1) |
| -1.65 | TRACK_LOST(B,U2) |
| -1.15 | TRACK_LOST(B,U3) |
| -1.05 | CRITICAL_TTC_START(A,B) |
| -0.65 | CRITICAL_TTC_START(B,A) |
| -0.60 | CLOSING_START(A,B) |
| -0.55 | EGO_PATH_EXIT(A,U1); CLOSING_START(B,A) |
| -0.45 | CRITICAL_TTC_END(A,U1) |
| -0.25 | TRACK_APPEARED_RIGHT(B,U3) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.20 | CLOSING_END(A,B); CLOSING_END(B,U2) |
| +0.30 | CLOSING_END(B,A) |
| +1.05 | MOVING_END(B); STOP_START(B) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +2.55 | TRACK_LOST(B,U3) |
| +2.75 | TRACK_LOST(B,U2) |
| +3.50 | TRACK_LOST(A,U3) |
| +3.70 | CUT_IN_FROM_RIGHT_START(A,U1) |
| +4.00 | TRACK_LOST(A,U1) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): critical TTC already active before the cut-in: CRITICAL_TTC_START 2.60 <= CUT_IN_FROM_RIGHT_START 3.00 (+0.40 s); EGO_PATH_ENTRY 3.45 after critical TTC (+0.85 s) [local times; t_global: cut_in -3.20, critical_ttc_start -3.60, ego_path_entry -2.75, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 5.15, COLLISION with B 6.20 (+1.05 s) [local times; t_global: critical_ttc_start -1.05, collision +0.00]
- A's track_003 (unidentified U2): CRITICAL_TTC_START 0.65, COLLISION 6.20 (+5.55 s) [local times; t_global: critical_ttc_start -5.55, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 5.55, COLLISION with A 6.20 (+0.65 s) [local times; t_global: critical_ttc_start -0.65, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.20 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04) | ego: not yet observed |
| -6.20 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g09 TRACK_APPEARED_RIGHT(B,U2) (B:e06)<br>g10 TRACK_APPEARED_RIGHT(B,U3) (B:e05)<br>g11 CLOSING_START(B,U2) (B:e07) | ego: not yet observed |
| -6.10 | B | g12 CLOSING_START(B,U2) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -6.05 | A | g13 TRACK_APPEARED_FRONT(A,U2) (A:e05) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC? |
| -5.55 | A | g14 CRITICAL_TTC_START(A,U2) (A:e06) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH, CRITICAL_TTC? |
| -3.60 | A | g15 CRITICAL_TTC_START(A,U1) (A:e07) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -3.20 | A | g16 CUT_IN_FROM_RIGHT_START(A,U1) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -2.75 | A | g17 EGO_PATH_ENTRY(A,U1) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -2.70 | A | g18 TRACK_LOST(A,U2) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -2.30 | A | g19 TRACK_APPEARED_RIGHT(A,U3) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 |
| -1.90 | A | g20 CUT_IN_FROM_RIGHT_END(A,U1) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 |
| -1.65 | B | g21 TRACK_LOST(B,U2) (B:e09) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CLOSING |
| -1.15 | B | g22 TRACK_LOST(B,U3) (B:e10) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_004 |
| -1.05 | A | g23 CRITICAL_TTC_START(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| -0.65 | B | g24 CRITICAL_TTC_START(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003, track_004 |
| -0.60 | A | g25 CLOSING_START(A,B) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| -0.55 | A | g26 EGO_PATH_EXIT(A,U1) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| -0.55 | B | g27 CLOSING_START(B,A) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003, track_004 |
| -0.45 | A | g28 CRITICAL_TTC_END(A,U1) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| -0.25 | B | g29 TRACK_APPEARED_RIGHT(B,U3) (B:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003, track_004 |
| +0.00 | A | g30 COLLISION(A,B) (A:e17)<br>g31 CRITICAL_TTC_END(A,B) (A:e18) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +0.00 | B | g30 COLLISION(A,B) (B:e14)<br>g32 CRITICAL_TTC_END(B,A) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_005: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004 |
| +0.05 | A | g33 THROTTLE_END(A) (A:e19)<br>g35 BRAKE_START(A) (A:e20) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +0.05 | B | g34 THROTTLE_END(B) (B:e16)<br>g36 BRAKE_START(B) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_005: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004 |
| +0.20 | A | g37 CLOSING_END(A,B) (A:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +0.20 | B | g38 CLOSING_END(B,U2) (B:e18) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_005: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004 |
| +0.30 | B | g39 CLOSING_END(B,A) (B:e19) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004 |
| +1.05 | B | g40 MOVING_END(B) (B:e20)<br>g41 STOP_START(B) (B:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004 |
| +1.15 | A | g42 MOVING_END(A) (A:e22)<br>g43 STOP_START(A) (A:e23) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +2.55 | B | g44 TRACK_LOST(B,U3) (B:e22) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004 |
| +2.75 | B | g45 TRACK_LOST(B,U2) (B:e23) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_005 |
| +3.50 | A | g46 TRACK_LOST(A,U3) (A:e24) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +3.70 | A | g47 CUT_IN_FROM_RIGHT_START(A,U1) (A:e25) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track lost, states UNKNOWN: track_003, track_004 |
| +4.00 | A | g48 TRACK_LOST(A,U1) (A:e26) | ego: STOP, BRAKE<br>track_001: CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track lost, states UNKNOWN: track_003, track_004 |

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
- 6.10 s before the reference collision, B observed anonymous road user U2 start closing in.
- 6.05 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 5.55 s before the reference collision, A's time-to-contact with anonymous road user U2 became critical.
- 3.60 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 3.20 s before the reference collision, A observed anonymous road user U1 cutting in from the right.
- 2.75 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 2.70 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.30 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 1.90 s before the reference collision, A observed anonymous road user U1's cut-in from the right settle.
- 1.65 s before the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 1.15 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 1.05 s before the reference collision, A's time-to-contact with B became critical.
- 0.65 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, A observed B start closing in.
- 0.55 s before the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 0.55 s before the reference collision, B observed A start closing in.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 0.25 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1092, B: 1092 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.20 s after the reference collision, B observed anonymous road user U2 stop closing in.
- 0.30 s after the reference collision, B observed A stop closing in.
- 1.05 s after the reference collision, B stopped moving.
- 1.05 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 2.55 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.75 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 3.50 s after the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.70 s after the reference collision, A observed anonymous road user U1 cutting in from the right.
- 4.00 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
