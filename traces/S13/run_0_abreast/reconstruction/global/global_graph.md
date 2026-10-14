# Global graph - S13/run_0_abreast

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_003 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_002 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 6.20 | -6.20 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 6.20 | -6.20 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1079.56 vs 1079.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.1 m -> 15.5 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.97 m/s for reference)<br>clearance at the contact 15.09 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U1: A:track_001, B:track_003 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.5 m -> 0.2 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.27 m/s for reference)<br>clearance at the contact 0.16 m<br>the only track of A compatible with the contact |
| A:track_003 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.1 m -> 15.3 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.87 m/s for reference)<br>clearance at the contact 15.10 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: A:track_003, B:track_002 |
| B:track_001 | A | ASSOCIATED | 0.96 | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.6 m -> 0.5 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.43 m/s for reference)<br>clearance at the contact 0.49 m<br>the only compatible track of B touching it at the contact (clearance 0.49 m; track_002, track_003 at 16.52 m, 17.21 m) |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 17.6 m -> 16.5 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.13 m/s for reference)<br>clearance at the contact 16.52 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 3 persistent tracks of B are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U2: A:track_003, B:track_002 |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.1 m -> 17.2 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.11 m/s for reference)<br>clearance at the contact 17.17 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 3 persistent tracks of B are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U1: A:track_001, B:track_003 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.20 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.20 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.20 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -6.20 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -6.20 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -6.20 | TRACK_APPEARED_RIGHT | A | U1 | A:e04 @ 0.00, A:e20 @ 10.45 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g07 | -6.20 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g08 | -6.15 | TRACK_APPEARED_FRONT | A | U2 | A:e05 @ 0.05, A:e19 @ 10.20 | initial_in_ego_path=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g09 | -6.10 | TRACK_APPEARED_RIGHT | B | U2 | B:e04 @ 0.10, B:e20 @ 8.95 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g10 | -6.10 | CLOSING_START | B | U2 | B:e05 @ 0.10, B:e15 @ 6.40 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g11 | -5.90 | TRACK_APPEARED_RIGHT | B | U1 | B:e06 @ 0.30, B:e21 @ 8.95 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g12 | -5.90 | CLOSING_START | B | U1 | B:e07 @ 0.30, B:e14 @ 6.30 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -5.65 | CRITICAL_TTC_START | A | U2 | A:e06 @ 0.55, A:e09 @ 5.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g14 | -1.05 | CRITICAL_TTC_START | A | B | A:e07 @ 5.15, A:e12 @ 6.20 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g15 | -0.65 | CLOSING_START | A | B | A:e08 @ 5.55, A:e16 @ 6.40 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g16 | -0.65 | CRITICAL_TTC_START | B | A | B:e08 @ 5.55, B:e11 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g17 | -0.60 | CLOSING_START | B | A | B:e09 @ 5.60, B:e16 @ 6.45 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g18 | -0.45 | CRITICAL_TTC_END | A | U2 | A:e09 @ 5.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g19 | -0.45 | EGO_PATH_EXIT | A | U2 | A:e10 @ 5.75 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g20 | 0.00 | COLLISION | - | A, B | A:e11 @ 6.20, B:e10 @ 6.20 | matched_event=collision_001; reference_event=True; peak_impulse=A 1079.56, B 1079.56 |
| g21 | 0.00 | CRITICAL_TTC_END | A | B | A:e12 @ 6.20 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g22 | 0.00 | CRITICAL_TTC_END | B | A | B:e11 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g23 | 0.05 | THROTTLE_END | A | - | A:e13 @ 6.25 |  |
| g24 | 0.05 | THROTTLE_END | B | - | B:e12 @ 6.25 |  |
| g25 | 0.05 | BRAKE_START | A | - | A:e14 @ 6.25 |  |
| g26 | 0.05 | BRAKE_START | B | - | B:e13 @ 6.25 |  |
| g27 | 0.10 | CLOSING_END | B | U1 | B:e14 @ 6.30 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g28 | 0.10 | EGO_PATH_ENTRY | A | B | A:e15 @ 6.30 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g29 | 0.20 | CLOSING_END | A | B | A:e16 @ 6.40 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g30 | 0.20 | CLOSING_END | B | U2 | B:e15 @ 6.40 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g31 | 0.25 | CLOSING_END | B | A | B:e16 @ 6.45 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g32 | 1.05 | MOVING_END | B | - | B:e17 @ 7.25 |  |
| g33 | 1.05 | STOP_START | B | - | B:e18 @ 7.25 |  |
| g34 | 1.15 | MOVING_END | A | - | A:e17 @ 7.35 |  |
| g35 | 1.15 | STOP_START | A | - | A:e18 @ 7.35 |  |
| g36 | 1.25 | EGO_PATH_ENTRY | B | A | B:e19 @ 7.45 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g37 | 2.75 | TRACK_LOST | B | U1 | B:e21 @ 8.95 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g38 | 2.75 | TRACK_LOST | B | U2 | B:e20 @ 8.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g39 | 4.00 | TRACK_LOST | A | U2 | A:e19 @ 10.20 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g40 | 4.25 | TRACK_LOST | A | U1 | A:e20 @ 10.45 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |

## Edges

```
    g01 --PRECEDES--> g08
    g02 --PRECEDES--> g08
    g03 --PRECEDES--> g08
    g04 --PRECEDES--> g08
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g08 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g14
    g05 --SAME_TRACK--> g15
    g08 --SAME_TRACK--> g18
    g08 --SAME_TRACK--> g19
    g05 --SAME_TRACK--> g21
    g05 --SAME_TRACK--> g28
    g05 --SAME_TRACK--> g29
    g08 --SAME_TRACK--> g39
    g06 --SAME_TRACK--> g40
    g09 --SAME_TRACK--> g10
    g11 --SAME_TRACK--> g12
    g07 --SAME_TRACK--> g16
    g07 --SAME_TRACK--> g17
    g07 --SAME_TRACK--> g22
    g11 --SAME_TRACK--> g27
    g09 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g31
    g07 --SAME_TRACK--> g36
    g09 --SAME_TRACK--> g38
    g11 --SAME_TRACK--> g37
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.20 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(B,A) |
| -6.15 | TRACK_APPEARED_FRONT(A,U2) |
| -6.10 | TRACK_APPEARED_RIGHT(B,U2); CLOSING_START(B,U2) |
| -5.90 | TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(B,U1) |
| -5.65 | CRITICAL_TTC_START(A,U2) |
| -1.05 | CRITICAL_TTC_START(A,B) |
| -0.65 | CLOSING_START(A,B); CRITICAL_TTC_START(B,A) |
| -0.60 | CLOSING_START(B,A) |
| -0.45 | CRITICAL_TTC_END(A,U2); EGO_PATH_EXIT(A,U2) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CLOSING_END(B,U1); EGO_PATH_ENTRY(A,B) |
| +0.20 | CLOSING_END(A,B); CLOSING_END(B,U2) |
| +0.25 | CLOSING_END(B,A) |
| +1.05 | MOVING_END(B); STOP_START(B) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +1.25 | EGO_PATH_ENTRY(B,A) |
| +2.75 | TRACK_LOST(B,U1); TRACK_LOST(B,U2) |
| +4.00 | TRACK_LOST(A,U2) |
| +4.25 | TRACK_LOST(A,U1) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (B): CRITICAL_TTC_START 5.15, COLLISION with B 6.20 (+1.05 s); EGO_PATH_ENTRY 6.30 after critical TTC (+1.15 s) [local times; t_global: critical_ttc_start -1.05, ego_path_entry +0.10, collision +0.00]
- A's track_003 (unidentified U2): CRITICAL_TTC_START 0.55, COLLISION 6.20 (+5.65 s) [local times; t_global: critical_ttc_start -5.65, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 5.55, COLLISION with A 6.20 (+0.65 s); EGO_PATH_ENTRY 7.45 after critical TTC (+1.90 s) [local times; t_global: critical_ttc_start -0.65, ego_path_entry +1.25, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.20 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04) | ego: not yet observed |
| -6.20 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03) | ego: not yet observed |
| -6.20 | A | g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g40 TRACK_LOST(A,U1) (A:e20) | ego: not yet observed |
| -6.15 | A | g08 TRACK_APPEARED_FRONT(A,U2) (A:e05) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC? |
| -6.15 | A | g08 TRACK_APPEARED_FRONT(A,U2) (A:e05)<br>g39 TRACK_LOST(A,U2) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC? |
| -6.10 | B | g09 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g10 CLOSING_START(B,U2) (B:e05) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC? |
| -6.10 | B | g09 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g11 TRACK_APPEARED_RIGHT(B,U1) (B:e06)<br>g37 TRACK_LOST(B,U1) (B:e21)<br>g38 TRACK_LOST(B,U2) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC? |
| -6.10 | B | g10 CLOSING_START(B,U2) (B:e05)<br>g30 CLOSING_END(B,U2) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC? |
| -5.90 | B | g11 TRACK_APPEARED_RIGHT(B,U1) (B:e06)<br>g12 CLOSING_START(B,U1) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? |
| -5.90 | B | g12 CLOSING_START(B,U1) (B:e07)<br>g27 CLOSING_END(B,U1) (B:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? |
| -5.65 | A | g13 CRITICAL_TTC_START(A,U2) (A:e06) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH, CRITICAL_TTC? |
| -5.65 | A | g13 CRITICAL_TTC_START(A,U2) (A:e06)<br>g18 CRITICAL_TTC_END(A,U2) (A:e09)<br>g19 EGO_PATH_EXIT(A,U2) (A:e10) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH, CRITICAL_TTC? |
| -1.05 | A | g14 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -1.05 | A | g14 CRITICAL_TTC_START(A,B) (A:e07)<br>g20 COLLISION(A,B) (A:e11)<br>g21 CRITICAL_TTC_END(A,B) (A:e12) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -0.65 | A | g15 CLOSING_START(A,B) (A:e08) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -0.65 | A | g15 CLOSING_START(A,B) (A:e08)<br>g29 CLOSING_END(A,B) (A:e16) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH |
| -0.65 | B | g16 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING |
| -0.65 | B | g16 CRITICAL_TTC_START(B,A) (B:e08)<br>g20 COLLISION(A,B) (B:e10)<br>g22 CRITICAL_TTC_END(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING |
| -0.60 | B | g17 CLOSING_START(B,A) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING |
| -0.60 | B | g17 CLOSING_START(B,A) (B:e09)<br>g31 CLOSING_END(B,A) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING |
| +0.05 | A | g23 THROTTLE_END(A) (A:e13)<br>g25 BRAKE_START(A) (A:e14) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: no active state |
| +0.05 | B | g24 THROTTLE_END(B) (B:e12)<br>g26 BRAKE_START(B) (B:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING |
| +0.10 | A | g28 EGO_PATH_ENTRY(A,B) (A:e15) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: no active state |
| +1.05 | B | g32 MOVING_END(B) (B:e17)<br>g33 STOP_START(B) (B:e18) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state |
| +1.15 | A | g34 MOVING_END(A) (A:e17)<br>g35 STOP_START(A) (A:e18) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state |
| +1.25 | B | g36 EGO_PATH_ENTRY(B,A) (B:e19) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state |

## Plain-language reading

- 6.20 s before the reference collision, A started moving (already the case when first observed).
- 6.20 s before the reference collision, B started moving (already the case when first observed).
- 6.20 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.20 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.15 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 6.10 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 6.10 s before the reference collision, B observed anonymous road user U2 start closing in (already the case when first observed).
- 5.90 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 5.90 s before the reference collision, B observed anonymous road user U1 start closing in (already the case when first observed).
- 5.65 s before the reference collision, A's time-to-contact with anonymous road user U2 became critical.
- 1.05 s before the reference collision, A's time-to-contact with B became critical.
- 0.65 s before the reference collision, A observed B start closing in.
- 0.65 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, B observed A start closing in.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U2 stopped being critical.
- 0.45 s before the reference collision, A observed anonymous road user U2 leave its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1080, B: 1080 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B observed anonymous road user U1 stop closing in.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.20 s after the reference collision, B observed anonymous road user U2 stop closing in.
- 0.25 s after the reference collision, B observed A stop closing in.
- 1.05 s after the reference collision, B stopped moving.
- 1.05 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.25 s after the reference collision, B observed A enter its forward path corridor.
- 2.75 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 2.75 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 4.00 s after the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
