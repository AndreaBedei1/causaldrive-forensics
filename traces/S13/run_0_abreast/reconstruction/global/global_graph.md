# Global graph - S13/run_0_abreast

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
| A | ALIGNED | A:e16 | 6.20 | -6.20 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 6.20 | -6.20 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1079.56 vs 1079.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>lost 5.95 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 15.5 m -> 15.6 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001#segment_1 |
| A:track_001#segment_2 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 5.90 s before the matched collision<br>lost 2.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 15.1 m -> 15.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.53 m/s over 0.9 s<br>anonymous road user U4: A:track_001#segment_2 |
| A:track_001#segment_3 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.2 m -> 15.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.93 m/s over 2.0 s<br>clearance at the contact 15.19 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.28 m/s over 3.0 s<br>clearance at the contact 0.18 m<br>the only track of A compatible with the contact |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 5.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.4 m -> 15.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.36 m/s over 3.0 s<br>clearance at the contact 15.38 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: B:track_003, A:track_003 |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.6 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.49 m/s over 3.0 s<br>clearance at the contact 0.52 m<br>the only compatible track of B touching it at the contact (clearance 0.52 m; track_002, track_003, track_004 at 16.71 m, 17.18 m, 18.06 m) |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 17.6 m -> 16.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 16.71 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.0 m -> 17.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.10 m/s over 3.0 s<br>clearance at the contact 17.14 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004)<br>anonymous road user U3: B:track_003, A:track_003 |
| B:track_004 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1079.56 vs 1079.56 N*s)<br>tracked for 6.20 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 19.1 m -> 18.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.18 m/s over 3.0 s<br>clearance at the contact 18.06 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_004)<br>anonymous road user U2: B:track_002, B:track_004, A:track_001#segment_3 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.20 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.20 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.20 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -6.20 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -6.20 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -6.20 | TRACK_APPEARED_RIGHT | A | U1 | A:e04 @ 0.00, A:e06 @ 0.25 | initial_in_ego_path=False; source_track=track_001#segment_1; aggregation=entity_state_union; source_tracks=['A:track_001#segment_1'] |
| g07 | -6.20 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g08 | -6.20 | TRACK_APPEARED_RIGHT | B | U2 | B:e04 @ 0.00, B:e24 @ 8.95, B:e06 @ 0.00, B:e23 @ 8.55 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g09 | -6.20 | TRACK_APPEARED_RIGHT | B | U3 | B:e05 @ 0.00, B:e25 @ 8.95 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g10 | -6.20 | CLOSING_START | B | U2 | B:e07 @ 0.00, B:e18 @ 6.40, B:e09 @ 0.00, B:e17 @ 6.35 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g11 | -6.20 | CLOSING_START | B | U3 | B:e08 @ 0.00, B:e16 @ 6.30 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g12 | -5.95 | TRACK_APPEARED_FRONT | A | U3 | A:e05 @ 0.25, A:e26 @ 10.45 | initial_in_ego_path=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g13 | -5.95 | TRACK_LOST | A | U1 | A:e06 @ 0.25 | source_track=track_001#segment_1; aggregation=entity_state_union; source_tracks=['A:track_001#segment_1'] |
| g14 | -5.90 | TRACK_APPEARED_RIGHT | A | U4 | A:e07 @ 0.30, A:e09 @ 4.10 | initial_in_ego_path=False; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g15 | -2.50 | EGO_PATH_EXIT | A | U3 | A:e08 @ 3.70 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g16 | -2.10 | TRACK_LOST | A | U4 | A:e09 @ 4.10 | source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g17 | -2.05 | TRACK_APPEARED_FRONT | A | U2 | A:e10 @ 4.15, A:e25 @ 10.20 | initial_in_ego_path=True; source_track=track_001#segment_3; aggregation=entity_state_union; source_tracks=['A:track_001#segment_3'] |
| g18 | -1.55 | CRITICAL_TTC_START | A | U2 | A:e11 @ 4.65, A:e14 @ 5.75 | source_track=track_001#segment_3; aggregation=entity_state_union; source_tracks=['A:track_001#segment_3'] |
| g19 | -1.05 | CRITICAL_TTC_START | A | B | A:e12 @ 5.15, A:e17 @ 6.20 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g20 | -0.65 | CRITICAL_TTC_START | B | A | B:e10 @ 5.55, B:e13 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g21 | -0.60 | CLOSING_START | A | B | A:e13 @ 5.60, A:e21 @ 6.40 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g22 | -0.55 | CLOSING_START | B | A | B:e11 @ 5.65, B:e19 @ 6.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g23 | -0.45 | CRITICAL_TTC_END | A | U2 | A:e14 @ 5.75 | source_track=track_001#segment_3; aggregation=entity_state_union; source_tracks=['A:track_001#segment_3'] |
| g24 | -0.45 | EGO_PATH_EXIT | A | U2 | A:e15 @ 5.75 | geometry=estimated_body; source_track=track_001#segment_3; aggregation=entity_state_union; source_tracks=['A:track_001#segment_3'] |
| g25 | 0.00 | COLLISION | - | A, B | A:e16 @ 6.20, B:e12 @ 6.20 | matched_event=collision_001; reference_event=True; peak_impulse=A 1079.56, B 1079.56 |
| g26 | 0.00 | CRITICAL_TTC_END | A | B | A:e17 @ 6.20 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g27 | 0.00 | CRITICAL_TTC_END | B | A | B:e13 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g28 | 0.05 | THROTTLE_END | A | - | A:e18 @ 6.25 |  |
| g29 | 0.05 | THROTTLE_END | B | - | B:e14 @ 6.25 |  |
| g30 | 0.05 | BRAKE_START | A | - | A:e19 @ 6.25 |  |
| g31 | 0.05 | BRAKE_START | B | - | B:e15 @ 6.25 |  |
| g32 | 0.10 | CLOSING_END | B | U3 | B:e16 @ 6.30 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g33 | 0.10 | EGO_PATH_ENTRY | A | B | A:e20 @ 6.30 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g34 | 0.20 | CLOSING_END | A | B | A:e21 @ 6.40 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g35 | 0.20 | CLOSING_END | B | U2 | B:e18 @ 6.40, B:e17 @ 6.35 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g36 | 0.30 | CLOSING_END | B | A | B:e19 @ 6.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g37 | 1.05 | MOVING_END | B | - | B:e20 @ 7.25 |  |
| g38 | 1.05 | STOP_START | B | - | B:e21 @ 7.25 |  |
| g39 | 1.15 | MOVING_END | A | - | A:e22 @ 7.35 |  |
| g40 | 1.15 | STOP_START | A | - | A:e23 @ 7.35 |  |
| g41 | 1.20 | EGO_PATH_ENTRY | B | A | B:e22 @ 7.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g42 | 2.75 | TRACK_LOST | B | U2 | B:e24 @ 8.95, B:e23 @ 8.55 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002', 'B:track_004'] |
| g43 | 2.75 | TRACK_LOST | B | U3 | B:e25 @ 8.95 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g44 | 3.20 | CUT_IN_FROM_RIGHT_START | A | U3 | A:e24 @ 9.40 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g45 | 4.00 | TRACK_LOST | A | U2 | A:e25 @ 10.20 | source_track=track_001#segment_3; aggregation=entity_state_union; source_tracks=['A:track_001#segment_3'] |
| g46 | 4.25 | TRACK_LOST | A | U3 | A:e26 @ 10.45 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |

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
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
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
    g06 --SAME_TRACK--> g13
    g12 --SAME_TRACK--> g15
    g14 --SAME_TRACK--> g16
    g17 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g19
    g05 --SAME_TRACK--> g21
    g17 --SAME_TRACK--> g23
    g17 --SAME_TRACK--> g24
    g05 --SAME_TRACK--> g26
    g05 --SAME_TRACK--> g33
    g05 --SAME_TRACK--> g34
    g12 --SAME_TRACK--> g44
    g17 --SAME_TRACK--> g45
    g12 --SAME_TRACK--> g46
    g08 --SAME_TRACK--> g10
    g09 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g20
    g07 --SAME_TRACK--> g22
    g07 --SAME_TRACK--> g27
    g09 --SAME_TRACK--> g32
    g08 --SAME_TRACK--> g35
    g07 --SAME_TRACK--> g36
    g07 --SAME_TRACK--> g41
    g08 --SAME_TRACK--> g42
    g09 --SAME_TRACK--> g43
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.20 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U2); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U2); CLOSING_START(B,U3) |
| -5.95 | TRACK_APPEARED_FRONT(A,U3); TRACK_LOST(A,U1) |
| -5.90 | TRACK_APPEARED_RIGHT(A,U4) |
| -2.50 | EGO_PATH_EXIT(A,U3) |
| -2.10 | TRACK_LOST(A,U4) |
| -2.05 | TRACK_APPEARED_FRONT(A,U2) |
| -1.55 | CRITICAL_TTC_START(A,U2) |
| -1.05 | CRITICAL_TTC_START(A,B) |
| -0.65 | CRITICAL_TTC_START(B,A) |
| -0.60 | CLOSING_START(A,B) |
| -0.55 | CLOSING_START(B,A) |
| -0.45 | CRITICAL_TTC_END(A,U2); EGO_PATH_EXIT(A,U2) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CLOSING_END(B,U3); EGO_PATH_ENTRY(A,B) |
| +0.20 | CLOSING_END(A,B); CLOSING_END(B,U2) |
| +0.30 | CLOSING_END(B,A) |
| +1.05 | MOVING_END(B); STOP_START(B) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +1.20 | EGO_PATH_ENTRY(B,A) |
| +2.75 | TRACK_LOST(B,U2); TRACK_LOST(B,U3) |
| +3.20 | CUT_IN_FROM_RIGHT_START(A,U3) |
| +4.00 | TRACK_LOST(A,U2) |
| +4.25 | TRACK_LOST(A,U3) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001#segment_3 (unidentified U2): CRITICAL_TTC_START 4.65, COLLISION 6.20 (+1.55 s) [local times; t_global: critical_ttc_start -1.55, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 5.15, COLLISION with B 6.20 (+1.05 s); EGO_PATH_ENTRY 6.30 after critical TTC (+1.15 s) [local times; t_global: critical_ttc_start -1.05, ego_path_entry +0.10, collision +0.00]
- A's track_003 (unidentified U3): CUT_IN_FROM_RIGHT_START 9.40, no critical TTC after it [local times; t_global: cut_in +3.20]
- B's track_001 (A): CRITICAL_TTC_START 5.55, COLLISION with A 6.20 (+0.65 s); EGO_PATH_ENTRY 7.40 after critical TTC (+1.85 s) [local times; t_global: critical_ttc_start -0.65, ego_path_entry +1.20, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.20 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04) | ego: not yet observed |
| -6.20 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g08 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g09 TRACK_APPEARED_RIGHT(B,U3) (B:e05)<br>g10 CLOSING_START(B,U2) (B:e07)<br>g10 CLOSING_START(B,U2) (B:e07)<br>g11 CLOSING_START(B,U3) (B:e08) | ego: not yet observed |
| -6.20 | A | g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g12 TRACK_APPEARED_FRONT(A,U3) (A:e05)<br>g13 TRACK_LOST(A,U1) (A:e06) | ego: not yet observed |
| -6.20 | B | g08 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g09 TRACK_APPEARED_RIGHT(B,U3) (B:e05)<br>g42 TRACK_LOST(B,U2) (B:e24)<br>g43 TRACK_LOST(B,U3) (B:e25) | ego: not yet observed |
| -6.20 | B | g08 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g42 TRACK_LOST(B,U2) (B:e24) | ego: not yet observed |
| -6.20 | B | g10 CLOSING_START(B,U2) (B:e07)<br>g35 CLOSING_END(B,U2) (B:e18) | ego: not yet observed |
| -6.20 | B | g10 CLOSING_START(B,U2) (B:e07)<br>g35 CLOSING_END(B,U2) (B:e18) | ego: not yet observed |
| -6.20 | B | g11 CLOSING_START(B,U3) (B:e08)<br>g32 CLOSING_END(B,U3) (B:e16) | ego: not yet observed |
| -5.95 | A | g12 TRACK_APPEARED_FRONT(A,U3) (A:e05)<br>g46 TRACK_LOST(A,U3) (A:e26) | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC? |
| -5.90 | A | g14 TRACK_APPEARED_RIGHT(A,U4) (A:e07) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 |
| -5.90 | A | g14 TRACK_APPEARED_RIGHT(A,U4) (A:e07)<br>g16 TRACK_LOST(A,U4) (A:e09) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 |
| -2.50 | A | g15 EGO_PATH_EXIT(A,U3) (A:e08) | ego: MOVING, THROTTLE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 |
| -2.05 | A | g17 TRACK_APPEARED_FRONT(A,U2) (A:e10) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -2.05 | A | g17 TRACK_APPEARED_FRONT(A,U2) (A:e10)<br>g45 TRACK_LOST(A,U2) (A:e25) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -1.55 | A | g18 CRITICAL_TTC_START(A,U2) (A:e11) | ego: MOVING, THROTTLE<br>track_001#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -1.55 | A | g18 CRITICAL_TTC_START(A,U2) (A:e11)<br>g23 CRITICAL_TTC_END(A,U2) (A:e14)<br>g24 EGO_PATH_EXIT(A,U2) (A:e15) | ego: MOVING, THROTTLE<br>track_001#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -1.05 | A | g19 CRITICAL_TTC_START(A,B) (A:e12) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -1.05 | A | g19 CRITICAL_TTC_START(A,B) (A:e12)<br>g25 COLLISION(A,B) (A:e16)<br>g26 CRITICAL_TTC_END(A,B) (A:e17) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -0.65 | B | g20 CRITICAL_TTC_START(B,A) (B:e10) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| -0.65 | B | g20 CRITICAL_TTC_START(B,A) (B:e10)<br>g25 COLLISION(A,B) (B:e12)<br>g27 CRITICAL_TTC_END(B,A) (B:e13) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| -0.60 | A | g21 CLOSING_START(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -0.60 | A | g21 CLOSING_START(A,B) (A:e13)<br>g34 CLOSING_END(A,B) (A:e21) | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| -0.55 | B | g22 CLOSING_START(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| -0.55 | B | g22 CLOSING_START(B,A) (B:e11)<br>g36 CLOSING_END(B,A) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.05 | A | g28 THROTTLE_END(A) (A:e18)<br>g30 BRAKE_START(A) (A:e19) | ego: MOVING, THROTTLE<br>track_001#segment_3: no active state<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +0.05 | B | g29 THROTTLE_END(B) (B:e14)<br>g31 BRAKE_START(B) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.10 | A | g33 EGO_PATH_ENTRY(A,B) (A:e20) | ego: MOVING, BRAKE<br>track_001#segment_3: no active state<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +1.05 | B | g37 MOVING_END(B) (B:e20)<br>g38 STOP_START(B) (B:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +1.15 | A | g39 MOVING_END(A) (A:e22)<br>g40 STOP_START(A) (A:e23) | ego: MOVING, BRAKE<br>track_001#segment_3: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |
| +1.20 | B | g41 EGO_PATH_ENTRY(B,A) (B:e22) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +3.20 | A | g44 CUT_IN_FROM_RIGHT_START(A,U3) (A:e24) | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 |

## Plain-language reading

- 6.20 s before the reference collision, A started moving (already the case when first observed).
- 6.20 s before the reference collision, B started moving (already the case when first observed).
- 6.20 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.20 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.20 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 6.20 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.20 s before the reference collision, B observed anonymous road user U2 start closing in (already the case when first observed).
- 6.20 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 5.95 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 5.95 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 5.90 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 2.50 s before the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 2.10 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 2.05 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 1.55 s before the reference collision, A's time-to-contact with anonymous road user U2 became critical.
- 1.05 s before the reference collision, A's time-to-contact with B became critical.
- 0.65 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, A observed B start closing in.
- 0.55 s before the reference collision, B observed A start closing in.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U2 stopped being critical.
- 0.45 s before the reference collision, A observed anonymous road user U2 leave its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1080, B: 1080 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B observed anonymous road user U3 stop closing in.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.20 s after the reference collision, A observed B stop closing in.
- 0.20 s after the reference collision, B observed anonymous road user U2 stop closing in.
- 0.30 s after the reference collision, B observed A stop closing in.
- 1.05 s after the reference collision, B stopped moving.
- 1.05 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.20 s after the reference collision, B observed A enter its forward path corridor.
- 2.75 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.75 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.20 s after the reference collision, A observed anonymous road user U3 cutting in from the right.
- 4.00 s after the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
