# Global graph - S18/run_0_platoon

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_002, B:track_004 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_003 |
| U4 | anonymous_road_user | anonymous; observed by A, B as A:track_004, B:track_005 |
| U3 | anonymous_road_user | anonymous; observed by B as B:track_003 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 6.20 | -6.20 | reported the reference collision collision_001 |
| B | ALIGNED | B:e13 | 6.20 | -6.20 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1097.53 vs 1097.53 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 12.8 m -> 12.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.99 m/s over 3.0 s<br>clearance at the contact 12.70 m (beyond 3.50 m: confidence factor 0.01)<br>anonymous road user U1: A:track_001, B:track_002, B:track_004 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.27 m/s over 3.0 s<br>clearance at the contact 0.18 m<br>the only track of A compatible with the contact |
| A:track_003 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 6.20 s before the matched collision<br>lost 4.80 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 16.6 m -> 16.4 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_003 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U4: A:track_004, B:track_005 |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.6 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.51 m/s over 3.0 s<br>clearance at the contact 0.53 m<br>the only compatible track of B touching it at the contact (clearance 0.53 m; track_002, track_004 at 13.90 m, 15.71 m) |
| B:track_002 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 13.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 13.90 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 3 persistent tracks of B are compatible with the contact (track_001, track_002, track_004)<br>anonymous road user U1: A:track_001, B:track_002, B:track_004 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 6.15 s before the matched collision<br>lost 1.55 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 25.0 m -> 24.4 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.10 m/s over 1.5 s<br>anonymous road user U3: B:track_003 |
| B:track_004 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.6 m -> 15.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.25 m/s over 3.0 s<br>clearance at the contact 15.71 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 3 persistent tracks of B are compatible with the contact (track_001, track_002, track_004)<br>anonymous road user U1: A:track_001, B:track_002, B:track_004 |
| B:track_005 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1097.53 vs 1097.53 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U4: A:track_004, B:track_005 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.20 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.20 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.20 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -6.20 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -6.20 | TRACK_APPEARED_FRONT | A | U1 | A:e03 @ 0.00, A:e22 @ 10.50 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g06 | -6.20 | TRACK_APPEARED_FRONT | A | U2 | A:e04 @ 0.00, A:e07 @ 1.40 | initial_in_ego_path=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g07 | -6.20 | TRACK_APPEARED_LEFT | A | B | A:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g08 | -6.20 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g09 | -6.20 | TRACK_APPEARED_RIGHT | B | U1 | B:e04 @ 0.00, B:e25 @ 8.95, B:e05 @ 0.00, B:e26 @ 9.55 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g10 | -6.20 | CLOSING_START | B | U1 | B:e06 @ 0.00, B:e17 @ 6.35, B:e07 @ 0.00, B:e18 @ 6.35 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g11 | -6.15 | TRACK_APPEARED_RIGHT | B | U3 | B:e08 @ 0.05, B:e10 @ 4.65 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g12 | -6.15 | CLOSING_START | B | U3 | B:e09 @ 0.05 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -5.70 | CRITICAL_TTC_START | A | U1 | A:e06 @ 0.50, A:e10 @ 5.85 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g14 | -4.80 | TRACK_LOST | A | U2 | A:e07 @ 1.40 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g15 | -1.55 | TRACK_LOST | B | U3 | B:e10 @ 4.65 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g16 | -1.05 | CRITICAL_TTC_START | A | B | A:e08 @ 5.15, A:e13 @ 6.20 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g17 | -0.65 | CRITICAL_TTC_START | B | A | B:e11 @ 5.55, B:e14 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g18 | -0.60 | CLOSING_START | A | B | A:e09 @ 5.60, A:e18 @ 6.40 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g19 | -0.55 | CLOSING_START | B | A | B:e12 @ 5.65, B:e20 @ 6.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g20 | -0.35 | CRITICAL_TTC_END | A | U1 | A:e10 @ 5.85 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g21 | -0.35 | EGO_PATH_EXIT | A | U1 | A:e11 @ 5.85 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g22 | 0.00 | COLLISION | - | A, B | A:e12 @ 6.20, B:e13 @ 6.20 | matched_event=collision_001; reference_event=True; peak_impulse=A 1097.53, B 1097.53 |
| g23 | 0.00 | CRITICAL_TTC_END | A | B | A:e13 @ 6.20 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g24 | 0.00 | CRITICAL_TTC_END | B | A | B:e14 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g25 | 0.05 | THROTTLE_END | A | - | A:e14 @ 6.25 |  |
| g26 | 0.05 | THROTTLE_END | B | - | B:e15 @ 6.25 |  |
| g27 | 0.05 | BRAKE_START | A | - | A:e15 @ 6.25 |  |
| g28 | 0.05 | BRAKE_START | B | - | B:e16 @ 6.25 |  |
| g29 | 0.05 | TRACK_APPEARED_RIGHT | A | U4 | A:e16 @ 6.25, A:e21 @ 9.95 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g30 | 0.10 | EGO_PATH_ENTRY | A | B | A:e17 @ 6.30 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g31 | 0.15 | CLOSING_END | B | U1 | B:e17 @ 6.35, B:e18 @ 6.35 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g32 | 0.20 | CLOSING_END | A | B | A:e18 @ 6.40 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g33 | 0.30 | TRACK_APPEARED_RIGHT | B | U4 | B:e19 @ 6.50, B:e24 @ 8.55 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g34 | 0.40 | CLOSING_END | B | A | B:e20 @ 6.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g35 | 1.05 | MOVING_END | B | - | B:e21 @ 7.25 |  |
| g36 | 1.05 | STOP_START | B | - | B:e22 @ 7.25 |  |
| g37 | 1.15 | MOVING_END | A | - | A:e19 @ 7.35 |  |
| g38 | 1.15 | STOP_START | A | - | A:e20 @ 7.35 |  |
| g39 | 1.15 | EGO_PATH_ENTRY | B | A | B:e23 @ 7.35 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g40 | 2.35 | TRACK_LOST | B | U4 | B:e24 @ 8.55 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g41 | 3.35 | TRACK_LOST | B | U1 | B:e25 @ 8.95, B:e26 @ 9.55 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g42 | 3.75 | TRACK_LOST | A | U4 | A:e21 @ 9.95 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g43 | 4.30 | TRACK_LOST | A | U1 | A:e22 @ 10.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |

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
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g40
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g42 --PRECEDES--> g43
    g05 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g14
    g07 --SAME_TRACK--> g16
    g07 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g21
    g07 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g32
    g29 --SAME_TRACK--> g42
    g05 --SAME_TRACK--> g43
    g09 --SAME_TRACK--> g10
    g11 --SAME_TRACK--> g12
    g11 --SAME_TRACK--> g15
    g08 --SAME_TRACK--> g17
    g08 --SAME_TRACK--> g19
    g08 --SAME_TRACK--> g24
    g09 --SAME_TRACK--> g31
    g08 --SAME_TRACK--> g34
    g08 --SAME_TRACK--> g39
    g33 --SAME_TRACK--> g40
    g09 --SAME_TRACK--> g41
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.20 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U1); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(B,U1) |
| -6.15 | TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3) |
| -5.70 | CRITICAL_TTC_START(A,U1) |
| -4.80 | TRACK_LOST(A,U2) |
| -1.55 | TRACK_LOST(B,U3) |
| -1.05 | CRITICAL_TTC_START(A,B) |
| -0.65 | CRITICAL_TTC_START(B,A) |
| -0.60 | CLOSING_START(A,B) |
| -0.55 | CLOSING_START(B,A) |
| -0.35 | CRITICAL_TTC_END(A,U1); EGO_PATH_EXIT(A,U1) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_RIGHT(A,U4) |
| +0.10 | EGO_PATH_ENTRY(A,B) |
| +0.15 | CLOSING_END(B,U1) |
| +0.20 | CLOSING_END(A,B) |
| +0.30 | TRACK_APPEARED_RIGHT(B,U4) |
| +0.40 | CLOSING_END(B,A) |
| +1.05 | MOVING_END(B); STOP_START(B) |
| +1.15 | MOVING_END(A); STOP_START(A); EGO_PATH_ENTRY(B,A) |
| +2.35 | TRACK_LOST(B,U4) |
| +3.35 | TRACK_LOST(B,U1) |
| +3.75 | TRACK_LOST(A,U4) |
| +4.30 | TRACK_LOST(A,U1) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 0.50, COLLISION 6.20 (+5.70 s) [local times; t_global: critical_ttc_start -5.70, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 5.15, COLLISION with B 6.20 (+1.05 s); EGO_PATH_ENTRY 6.30 after critical TTC (+1.15 s) [local times; t_global: critical_ttc_start -1.05, ego_path_entry +0.10, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 5.55, COLLISION with A 6.20 (+0.65 s); EGO_PATH_ENTRY 7.35 after critical TTC (+1.80 s) [local times; t_global: critical_ttc_start -0.65, ego_path_entry +1.15, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.20 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U1) (A:e03)<br>g06 TRACK_APPEARED_FRONT(A,U2) (A:e04)<br>g07 TRACK_APPEARED_LEFT(A,B) (A:e05) | ego: not yet observed |
| -6.20 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g08 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g09 TRACK_APPEARED_RIGHT(B,U1) (B:e04)<br>g09 TRACK_APPEARED_RIGHT(B,U1) (B:e04)<br>g10 CLOSING_START(B,U1) (B:e06)<br>g10 CLOSING_START(B,U1) (B:e06) | ego: not yet observed |
| -6.20 | A | g05 TRACK_APPEARED_FRONT(A,U1) (A:e03)<br>g43 TRACK_LOST(A,U1) (A:e22) | ego: not yet observed |
| -6.20 | A | g06 TRACK_APPEARED_FRONT(A,U2) (A:e04)<br>g14 TRACK_LOST(A,U2) (A:e07) | ego: not yet observed |
| -6.20 | B | g09 TRACK_APPEARED_RIGHT(B,U1) (B:e04)<br>g41 TRACK_LOST(B,U1) (B:e25) | ego: not yet observed |
| -6.20 | B | g09 TRACK_APPEARED_RIGHT(B,U1) (B:e04)<br>g41 TRACK_LOST(B,U1) (B:e25) | ego: not yet observed |
| -6.20 | B | g10 CLOSING_START(B,U1) (B:e06)<br>g10 CLOSING_START(B,U1) (B:e06)<br>g31 CLOSING_END(B,U1) (B:e17)<br>g31 CLOSING_END(B,U1) (B:e17) | ego: not yet observed |
| -6.15 | B | g11 TRACK_APPEARED_RIGHT(B,U3) (B:e08)<br>g12 CLOSING_START(B,U3) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC? |
| -6.15 | B | g11 TRACK_APPEARED_RIGHT(B,U3) (B:e08)<br>g15 TRACK_LOST(B,U3) (B:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC? |
| -5.70 | A | g13 CRITICAL_TTC_START(A,U1) (A:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC? |
| -5.70 | A | g13 CRITICAL_TTC_START(A,U1) (A:e06)<br>g20 CRITICAL_TTC_END(A,U1) (A:e10)<br>g21 EGO_PATH_EXIT(A,U1) (A:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC? |
| -1.05 | A | g16 CRITICAL_TTC_START(A,B) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 |
| -1.05 | A | g16 CRITICAL_TTC_START(A,B) (A:e08)<br>g22 COLLISION(A,B) (A:e12)<br>g23 CRITICAL_TTC_END(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 |
| -0.65 | B | g17 CRITICAL_TTC_START(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 |
| -0.65 | B | g17 CRITICAL_TTC_START(B,A) (B:e11)<br>g22 COLLISION(A,B) (B:e13)<br>g24 CRITICAL_TTC_END(B,A) (B:e14) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 |
| -0.60 | A | g18 CLOSING_START(A,B) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track lost, states UNKNOWN: track_003 |
| -0.60 | A | g18 CLOSING_START(A,B) (A:e09)<br>g32 CLOSING_END(A,B) (A:e18) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track lost, states UNKNOWN: track_003 |
| -0.55 | B | g19 CLOSING_START(B,A) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 |
| -0.55 | B | g19 CLOSING_START(B,A) (B:e12)<br>g34 CLOSING_END(B,A) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.05 | A | g25 THROTTLE_END(A) (A:e14)<br>g27 BRAKE_START(A) (A:e15)<br>g29 TRACK_APPEARED_RIGHT(A,U4) (A:e16) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.05 | B | g26 THROTTLE_END(B) (B:e15)<br>g28 BRAKE_START(B) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.05 | A | g29 TRACK_APPEARED_RIGHT(A,U4) (A:e16)<br>g42 TRACK_LOST(A,U4) (A:e21) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 |
| +0.10 | A | g30 EGO_PATH_ENTRY(A,B) (A:e17) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 |
| +0.30 | B | g33 TRACK_APPEARED_RIGHT(B,U4) (B:e19) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +0.30 | B | g33 TRACK_APPEARED_RIGHT(B,U4) (B:e19)<br>g40 TRACK_LOST(B,U4) (B:e24) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +1.05 | B | g35 MOVING_END(B) (B:e21)<br>g36 STOP_START(B) (B:e22) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_003 |
| +1.15 | A | g37 MOVING_END(A) (A:e19)<br>g38 STOP_START(A) (A:e20) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 |
| +1.15 | B | g39 EGO_PATH_ENTRY(B,A) (B:e23) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_003 |

## Plain-language reading

- 6.20 s before the reference collision, A started moving (already the case when first observed).
- 6.20 s before the reference collision, B started moving (already the case when first observed).
- 6.20 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared in front of it.
- 6.20 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 6.20 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.20 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 6.20 s before the reference collision, B observed anonymous road user U1 start closing in (already the case when first observed).
- 6.15 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.15 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 5.70 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 4.80 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 1.55 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 1.05 s before the reference collision, A's time-to-contact with B became critical.
- 0.65 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, A observed B start closing in.
- 0.55 s before the reference collision, B observed A start closing in.
- 0.35 s before the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 0.35 s before the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1098, B: 1098 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.15 s after the reference collision, B observed anonymous road user U1 stop closing in.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.30 s after the reference collision, B's radar started tracking anonymous road user U4, which appeared on its right.
- 0.40 s after the reference collision, B observed A stop closing in.
- 1.05 s after the reference collision, B stopped moving.
- 1.05 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.15 s after the reference collision, B observed A enter its forward path corridor.
- 2.35 s after the reference collision, B's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 3.35 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 3.75 s after the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 4.30 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
