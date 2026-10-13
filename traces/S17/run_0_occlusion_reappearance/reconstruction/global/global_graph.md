# Global graph - S17/run_0_occlusion_reappearance

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_006 |
| B | recorder | clock ALIGNED; observed by others as: A:track_007 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, A:track_005, B:track_004, B:track_007 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_002, A:track_008, B:track_002, B:track_009 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_003, B:track_005 |
| U4 | anonymous_road_user | anonymous; observed by A as A:track_004 |
| U5 | anonymous_road_user | anonymous; observed by A, B as A:track_006, A:track_009, B:track_001 |
| U7 | anonymous_road_user | anonymous; observed by A as A:track_010 |
| U6 | anonymous_road_user | anonymous; observed by B as B:track_008, B:track_010 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e28 | 7.30 | -7.30 | reported the reference collision collision_001 |
| B | ALIGNED | B:e29 | 7.30 | -7.30 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 389.26 vs 389.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.2 m -> 10.2 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 4.61 m/s over 3.0 s (> 1.50)<br>clearance at the contact 7.19 m (beyond 3.50 m: confidence factor 0.47)<br>anonymous road user U1: A:track_001, B:track_004, A:track_005, B:track_007 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 2.50 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 20.4 m -> 20.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 2.03 m/s over 0.5 s (> 1.50)<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_009 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 4.00 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 37.5 m -> 37.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_003, B:track_005 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.55 s before it (window 1.00 s)<br>not approaching before the contact: clearance 16.0 m -> 18.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.36 m/s over 2.5 s<br>clearance at the contact 17.39 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U4: A:track_004 |
| A:track_005 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 9.0 m -> 13.1 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 4.73 m/s over 3.0 s (> 1.50)<br>clearance at the contact 9.03 m (beyond 3.50 m: confidence factor 0.18)<br>anonymous road user U1: A:track_001, B:track_004, A:track_005, B:track_007 |
| A:track_006 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 2.75 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 19.1 m -> 17.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.40 m/s over 0.2 s<br>anonymous road user U5: A:track_006, B:track_001, A:track_009 |
| A:track_007 | B | ASSOCIATED | 0.68 | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 6.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.6 m -> 0.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.31 m/s over 3.0 s<br>clearance at the contact 0.42 m<br>the only track of A compatible with the contact |
| A:track_008 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 20.7 m -> 20.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.95 m/s over 1.1 s (> 1.50)<br>clearance at the contact 20.64 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_009 |
| A:track_009 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.0 m -> 11.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.25 m/s over 1.0 s<br>clearance at the contact 11.80 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U5: A:track_006, B:track_001, A:track_009 |
| A:track_010 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U7: A:track_010 |
| B:track_001 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 13.5 m -> 13.8 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.90 m/s over 3.0 s (> 1.50)<br>clearance at the contact 13.42 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U5: A:track_006, B:track_001, A:track_009 |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 2.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 17.5 m -> 19.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.17 m/s over 0.8 s<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_009 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 29.8 m -> 31.8 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_003, B:track_005 |
| B:track_004 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.6 m -> 12.6 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.54 m/s over 3.0 s (> 1.50)<br>clearance at the contact 7.64 m (beyond 3.50 m: confidence factor 0.39)<br>anonymous road user U1: A:track_001, B:track_004, A:track_005, B:track_007 |
| B:track_005 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 3.90 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 32.2 m -> 34.1 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_003, B:track_005 |
| B:track_006 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 4.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.5 m -> 0.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.52 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>the only compatible track of B touching it at the contact (clearance 0.00 m; track_008 at 11.56 m) |
| B:track_007 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 3.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 9.9 m -> 15.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.67 m/s over 3.0 s (> 1.50)<br>clearance at the contact 9.85 m (beyond 3.50 m: confidence factor 0.11)<br>anonymous road user U1: A:track_001, B:track_004, A:track_005, B:track_007 |
| B:track_008 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 2.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.6 m -> 11.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.33 m/s over 2.5 s<br>clearance at the contact 11.56 m (beyond 3.50 m: confidence factor 0.03)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_006, track_008)<br>anonymous road user U6: B:track_008, B:track_010 |
| B:track_009 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.50 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 22.8 m -> 23.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.26 m/s over 0.5 s<br>clearance at the contact 22.77 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_009 |
| B:track_010 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.00 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_008, B:track_010 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.30 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.30 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.30 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.30 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -7.30 | TRACK_APPEARED_FRONT | A | U2 | A:e03 @ 0.00, A:e15 @ 4.80 | initial_in_ego_path=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -7.30 | TRACK_APPEARED_FRONT | A | U3 | A:e04 @ 0.00, A:e12 @ 3.30 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g07 | -7.30 | TRACK_APPEARED_FRONT | B | U3 | B:e04 @ 0.00, B:e12 @ 3.40, B:e06 @ 0.00, B:e11 @ 3.20 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_003', 'B:track_005'] |
| g08 | -7.30 | TRACK_APPEARED_FRONT | B | U5 | B:e03 @ 0.00, B:e40 @ 8.00 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g09 | -7.30 | TRACK_APPEARED_LEFT | A | U1 | A:e05 @ 0.00, A:e47 @ 11.90, A:e09 @ 0.05 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001', 'A:track_005'] |
| g10 | -7.30 | TRACK_APPEARED_LEFT | A | U4 | A:e06 @ 0.00, A:e25 @ 6.75 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g11 | -7.30 | TRACK_APPEARED_LEFT | A | U5 | A:e07 @ 0.00, A:e14 @ 4.55 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g12 | -7.30 | TRACK_APPEARED_RIGHT | B | U1 | B:e07 @ 0.00, B:e38 @ 7.80, B:e14 @ 3.80, B:e39 @ 7.90 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004', 'B:track_007'] |
| g13 | -7.30 | TRACK_APPEARED_RIGHT | B | U2 | B:e05 @ 0.00, B:e17 @ 5.05 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g14 | -7.30 | CLOSING_START | A | U5 | A:e08 @ 0.00 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g15 | -6.80 | CRITICAL_TTC_START | B | U5 | B:e08 @ 0.50, B:e24 @ 6.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g16 | -6.40 | TRACK_APPEARED_LEFT | A | B | A:e10 @ 0.90 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g17 | -6.40 | CLOSING_START | A | B | A:e11 @ 0.90, A:e13 @ 4.30 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g18 | -4.30 | TRACK_APPEARED_RIGHT | B | A | B:e09 @ 3.00 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g19 | -4.30 | CLOSING_START | B | A | B:e10 @ 3.00, B:e13 @ 3.55 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g20 | -4.00 | TRACK_LOST | A | U3 | A:e12 @ 3.30 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g21 | -3.90 | TRACK_LOST | B | U3 | B:e12 @ 3.40, B:e11 @ 3.20 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_003', 'B:track_005'] |
| g22 | -3.75 | CLOSING_END | B | A | B:e13 @ 3.55 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g23 | -3.00 | CLOSING_END | A | B | A:e13 @ 4.30 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g24 | -2.75 | TRACK_LOST | A | U5 | A:e14 @ 4.55 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g25 | -2.50 | TRACK_APPEARED_RIGHT | B | U6 | B:e15 @ 4.80, B:e33 @ 7.40 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g26 | -2.50 | CLOSING_START | B | U6 | B:e16 @ 4.80 | active_at_first_observation=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g27 | -2.50 | TRACK_LOST | A | U2 | A:e15 @ 4.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g28 | -2.25 | TRACK_LOST | B | U2 | B:e17 @ 5.05 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g29 | -1.85 | EGO_PATH_ENTRY | A | U1 | A:e16 @ 5.45, A:e36 @ 7.55, A:e21 @ 5.85, A:e38 @ 7.65 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_001', 'A:track_005'] |
| g30 | -1.85 | CLOSING_START | A | B | A:e17 @ 5.45, A:e30 @ 7.30 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g31 | -1.85 | CLOSING_START | B | A | B:e18 @ 5.45, B:e28 @ 7.20 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g32 | -1.85 | CRITICAL_TTC_START | A | B | A:e19 @ 5.45, A:e29 @ 7.30 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g33 | -1.85 | CRITICAL_TTC_START | A | U1 | A:e18 @ 5.45, A:e20 @ 5.55, A:e37 @ 7.65 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_001', 'A:track_005'] |
| g34 | -1.80 | EGO_PATH_ENTRY | B | U1 | B:e19 @ 5.50, B:e23 @ 5.85 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_004', 'B:track_007'] |
| g35 | -1.75 | CRITICAL_TTC_START | B | A | B:e20 @ 5.55, B:e44 @ 8.30 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g36 | -1.75 | CRITICAL_TTC_START | B | U1 | B:e21 @ 5.55, B:e22 @ 5.60 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_004', 'B:track_007'] |
| g37 | -1.15 | CRITICAL_TTC_END | B | U5 | B:e24 @ 6.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g38 | -1.15 | EGO_PATH_EXIT | B | U5 | B:e25 @ 6.15 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g39 | -1.15 | TRACK_APPEARED_RIGHT | A | U2 | A:e22 @ 6.15 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g40 | -0.95 | TRACK_APPEARED_LEFT | A | U5 | A:e23 @ 6.35 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g41 | -0.95 | CLOSING_START | A | U5 | A:e24 @ 6.35, A:e35 @ 7.50 | active_at_first_observation=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g42 | -0.55 | TRACK_LOST | A | U4 | A:e25 @ 6.75 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g43 | -0.50 | TRACK_APPEARED_FRONT | B | U2 | B:e26 @ 6.80, B:e36 @ 7.60 | initial_in_ego_path=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g44 | -0.45 | CRITICAL_TTC_START | A | U5 | A:e26 @ 6.85, A:e39 @ 7.85 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g45 | -0.35 | EGO_PATH_ENTRY | B | A | B:e27 @ 6.95 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g46 | -0.25 | CUT_IN_FROM_LEFT_START | A | U5 | A:e27 @ 7.05, A:e46 @ 10.90 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g47 | -0.10 | CLOSING_END | B | A | B:e28 @ 7.20 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g48 | 0.00 | COLLISION | - | A, B | A:e28 @ 7.30, B:e29 @ 7.30 | matched_event=collision_001; reference_event=True; peak_impulse=A 389.26, B 389.26 |
| g49 | 0.00 | CRITICAL_TTC_END | A | B | A:e29 @ 7.30 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g50 | 0.00 | CLOSING_END | A | B | A:e30 @ 7.30 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g51 | 0.05 | THROTTLE_END | A | - | A:e31 @ 7.35 |  |
| g52 | 0.05 | THROTTLE_END | B | - | B:e30 @ 7.35 |  |
| g53 | 0.05 | BRAKE_START | A | - | A:e32 @ 7.35 |  |
| g54 | 0.05 | BRAKE_START | B | - | B:e31 @ 7.35 |  |
| g55 | 0.05 | TURN_LEFT_START | B | - | B:e32 @ 7.35 |  |
| g56 | 0.10 | TURN_LEFT_START | A | - | A:e33 @ 7.40 |  |
| g57 | 0.10 | EGO_PATH_ENTRY | A | U5 | A:e34 @ 7.40, A:e40 @ 7.95 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g58 | 0.10 | TRACK_LOST | B | U6 | B:e33 @ 7.40 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g59 | 0.15 | CUT_IN_FROM_RIGHT_START | B | A | B:e34 @ 7.45, B:e47 @ 8.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g60 | 0.20 | CLOSING_END | A | U5 | A:e35 @ 7.50 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g61 | 0.20 | EGO_PATH_EXIT | B | U2 | B:e35 @ 7.50 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g62 | 0.30 | TRACK_LOST | B | U2 | B:e36 @ 7.60 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g63 | 0.35 | EGO_PATH_EXIT | A | U1 | A:e36 @ 7.55, A:e38 @ 7.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001', 'A:track_005'] |
| g64 | 0.35 | EGO_PATH_ENTRY | B | U5 | B:e37 @ 7.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g65 | 0.55 | CRITICAL_TTC_END | A | U5 | A:e39 @ 7.85 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g66 | 0.60 | TRACK_LOST | B | U1 | B:e38 @ 7.80, B:e39 @ 7.90 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_004', 'B:track_007'] |
| g67 | 0.65 | EGO_PATH_EXIT | A | U5 | A:e40 @ 7.95 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g68 | 0.70 | TRACK_LOST | B | U5 | B:e40 @ 8.00 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g69 | 0.80 | TRACK_APPEARED_RIGHT | A | U7 | A:e41 @ 8.10, A:e48 @ 11.90 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g70 | 0.95 | TURN_LEFT_END | A | - | A:e42 @ 8.25 |  |
| g71 | 0.95 | TURN_LEFT_END | B | - | B:e41 @ 8.25 |  |
| g72 | 0.95 | MOVING_END | B | - | B:e42 @ 8.25 |  |
| g73 | 0.95 | STOP_START | B | - | B:e43 @ 8.25 |  |
| g74 | 0.95 | EGO_PATH_ENTRY | A | B | A:e43 @ 8.25 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g75 | 1.00 | CRITICAL_TTC_END | B | A | B:e44 @ 8.30 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g76 | 1.00 | MOVING_END | A | - | A:e44 @ 8.30 |  |
| g77 | 1.00 | STOP_START | A | - | A:e45 @ 8.30 |  |
| g78 | 1.00 | TRACK_APPEARED_RIGHT | B | U6 | B:e45 @ 8.30 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g79 | 1.00 | CLOSING_START | B | U6 | B:e46 @ 8.30, B:e48 @ 9.30 | active_at_first_observation=True; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g80 | 1.25 | CUT_IN_FROM_RIGHT_END | B | A | B:e47 @ 8.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g81 | 2.00 | CLOSING_END | B | U6 | B:e48 @ 9.30 | source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g82 | 3.60 | CUT_IN_FROM_LEFT_END | A | U5 | A:e46 @ 10.90 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g83 | 4.60 | TRACK_LOST | A | U7 | A:e48 @ 11.90 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |

## Edges

```
    g01 --PRECEDES--> g15
    g02 --PRECEDES--> g15
    g03 --PRECEDES--> g15
    g04 --PRECEDES--> g15
    g05 --PRECEDES--> g15
    g06 --PRECEDES--> g15
    g07 --PRECEDES--> g15
    g08 --PRECEDES--> g15
    g09 --PRECEDES--> g15
    g10 --PRECEDES--> g15
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g30 --PRECEDES--> g34
    g31 --PRECEDES--> g34
    g32 --PRECEDES--> g34
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
    g37 --PRECEDES--> g41
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g42
    g42 --PRECEDES--> g43
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g48 --PRECEDES--> g53
    g48 --PRECEDES--> g54
    g48 --PRECEDES--> g55
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g49 --PRECEDES--> g54
    g49 --PRECEDES--> g55
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g51 --PRECEDES--> g57
    g51 --PRECEDES--> g58
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g52 --PRECEDES--> g58
    g53 --PRECEDES--> g56
    g53 --PRECEDES--> g57
    g53 --PRECEDES--> g58
    g54 --PRECEDES--> g56
    g54 --PRECEDES--> g57
    g54 --PRECEDES--> g58
    g55 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g57 --PRECEDES--> g59
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g62
    g62 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g63 --PRECEDES--> g65
    g64 --PRECEDES--> g65
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g69 --PRECEDES--> g70
    g69 --PRECEDES--> g71
    g69 --PRECEDES--> g72
    g69 --PRECEDES--> g73
    g69 --PRECEDES--> g74
    g70 --PRECEDES--> g75
    g70 --PRECEDES--> g76
    g70 --PRECEDES--> g77
    g70 --PRECEDES--> g78
    g70 --PRECEDES--> g79
    g71 --PRECEDES--> g75
    g71 --PRECEDES--> g76
    g71 --PRECEDES--> g77
    g71 --PRECEDES--> g78
    g71 --PRECEDES--> g79
    g72 --PRECEDES--> g75
    g72 --PRECEDES--> g76
    g72 --PRECEDES--> g77
    g72 --PRECEDES--> g78
    g72 --PRECEDES--> g79
    g73 --PRECEDES--> g75
    g73 --PRECEDES--> g76
    g73 --PRECEDES--> g77
    g73 --PRECEDES--> g78
    g73 --PRECEDES--> g79
    g74 --PRECEDES--> g75
    g74 --PRECEDES--> g76
    g74 --PRECEDES--> g77
    g74 --PRECEDES--> g78
    g74 --PRECEDES--> g79
    g75 --PRECEDES--> g80
    g76 --PRECEDES--> g80
    g77 --PRECEDES--> g80
    g78 --PRECEDES--> g80
    g79 --PRECEDES--> g80
    g80 --PRECEDES--> g81
    g81 --PRECEDES--> g82
    g82 --PRECEDES--> g83
    g11 --SAME_TRACK--> g14
    g16 --SAME_TRACK--> g17
    g06 --SAME_TRACK--> g20
    g16 --SAME_TRACK--> g23
    g11 --SAME_TRACK--> g24
    g05 --SAME_TRACK--> g27
    g09 --SAME_TRACK--> g29
    g16 --SAME_TRACK--> g30
    g09 --SAME_TRACK--> g33
    g16 --SAME_TRACK--> g32
    g40 --SAME_TRACK--> g41
    g10 --SAME_TRACK--> g42
    g40 --SAME_TRACK--> g44
    g40 --SAME_TRACK--> g46
    g16 --SAME_TRACK--> g49
    g16 --SAME_TRACK--> g50
    g40 --SAME_TRACK--> g57
    g40 --SAME_TRACK--> g60
    g09 --SAME_TRACK--> g63
    g40 --SAME_TRACK--> g65
    g40 --SAME_TRACK--> g67
    g16 --SAME_TRACK--> g74
    g40 --SAME_TRACK--> g82
    g69 --SAME_TRACK--> g83
    g08 --SAME_TRACK--> g15
    g18 --SAME_TRACK--> g19
    g07 --SAME_TRACK--> g21
    g18 --SAME_TRACK--> g22
    g25 --SAME_TRACK--> g26
    g13 --SAME_TRACK--> g28
    g18 --SAME_TRACK--> g31
    g12 --SAME_TRACK--> g34
    g18 --SAME_TRACK--> g35
    g12 --SAME_TRACK--> g36
    g08 --SAME_TRACK--> g37
    g08 --SAME_TRACK--> g38
    g18 --SAME_TRACK--> g45
    g18 --SAME_TRACK--> g47
    g25 --SAME_TRACK--> g58
    g18 --SAME_TRACK--> g59
    g43 --SAME_TRACK--> g61
    g43 --SAME_TRACK--> g62
    g08 --SAME_TRACK--> g64
    g12 --SAME_TRACK--> g66
    g08 --SAME_TRACK--> g68
    g18 --SAME_TRACK--> g75
    g78 --SAME_TRACK--> g79
    g18 --SAME_TRACK--> g80
    g78 --SAME_TRACK--> g81
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.30 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_FRONT(B,U5); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U4); TRACK_APPEARED_LEFT(A,U5); TRACK_APPEARED_RIGHT(B,U1); TRACK_APPEARED_RIGHT(B,U2); CLOSING_START(A,U5) |
| -6.80 | CRITICAL_TTC_START(B,U5) |
| -6.40 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -4.30 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -4.00 | TRACK_LOST(A,U3) |
| -3.90 | TRACK_LOST(B,U3) |
| -3.75 | CLOSING_END(B,A) |
| -3.00 | CLOSING_END(A,B) |
| -2.75 | TRACK_LOST(A,U5) |
| -2.50 | TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(B,U6); TRACK_LOST(A,U2) |
| -2.25 | TRACK_LOST(B,U2) |
| -1.85 | EGO_PATH_ENTRY(A,U1); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(A,U1) |
| -1.80 | EGO_PATH_ENTRY(B,U1) |
| -1.75 | CRITICAL_TTC_START(B,A); CRITICAL_TTC_START(B,U1) |
| -1.15 | CRITICAL_TTC_END(B,U5); EGO_PATH_EXIT(B,U5); TRACK_APPEARED_RIGHT(A,U2) |
| -0.95 | TRACK_APPEARED_LEFT(A,U5); CLOSING_START(A,U5) |
| -0.55 | TRACK_LOST(A,U4) |
| -0.50 | TRACK_APPEARED_FRONT(B,U2) |
| -0.45 | CRITICAL_TTC_START(A,U5) |
| -0.35 | EGO_PATH_ENTRY(B,A) |
| -0.25 | CUT_IN_FROM_LEFT_START(A,U5) |
| -0.10 | CLOSING_END(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B) |
| +0.10 | TURN_LEFT_START(A); EGO_PATH_ENTRY(A,U5); TRACK_LOST(B,U6) |
| +0.15 | CUT_IN_FROM_RIGHT_START(B,A) |
| +0.20 | CLOSING_END(A,U5); EGO_PATH_EXIT(B,U2) |
| +0.30 | TRACK_LOST(B,U2) |
| +0.35 | EGO_PATH_EXIT(A,U1); EGO_PATH_ENTRY(B,U5) |
| +0.55 | CRITICAL_TTC_END(A,U5) |
| +0.60 | TRACK_LOST(B,U1) |
| +0.65 | EGO_PATH_EXIT(A,U5) |
| +0.70 | TRACK_LOST(B,U5) |
| +0.80 | TRACK_APPEARED_RIGHT(A,U7) |
| +0.95 | TURN_LEFT_END(A); TURN_LEFT_END(B); MOVING_END(B); STOP_START(B); EGO_PATH_ENTRY(A,B) |
| +1.00 | CRITICAL_TTC_END(B,A); MOVING_END(A); STOP_START(A); TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(B,U6) |
| +1.25 | CUT_IN_FROM_RIGHT_END(B,A) |
| +2.00 | CLOSING_END(B,U6) |
| +3.60 | CUT_IN_FROM_LEFT_END(A,U5) |
| +4.60 | TRACK_LOST(A,U7) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 5.85 after critical TTC (+0.30 s) [local times; t_global: critical_ttc_start -1.75, ego_path_entry -1.45, collision +0.00]
- A's track_005 (unidentified U1): CRITICAL_TTC_START 5.45, COLLISION 7.30 (+1.85 s); EGO_PATH_ENTRY 5.45 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start -1.85, ego_path_entry -1.85, collision +0.00]
- A's track_007 (B): CRITICAL_TTC_START 5.45, COLLISION with B 7.30 (+1.85 s); EGO_PATH_ENTRY 8.25 after critical TTC (+2.80 s) [local times; t_global: critical_ttc_start -1.85, ego_path_entry +0.95, collision +0.00]
- A's track_009 (unidentified U5): critical TTC already active before the cut-in: CRITICAL_TTC_START 6.85 <= CUT_IN_FROM_LEFT_START 7.05 (+0.20 s); EGO_PATH_ENTRY 7.40 after critical TTC (+0.55 s) [local times; t_global: cut_in -0.25, critical_ttc_start -0.45, ego_path_entry +0.10, collision +0.00]
- B's track_001 (unidentified U5): CRITICAL_TTC_START 0.50, COLLISION 7.30 (+6.80 s); EGO_PATH_ENTRY 7.65 after critical TTC (+7.15 s) [local times; t_global: critical_ttc_start -6.80, ego_path_entry +0.35, collision +0.00]
- B's track_004 (unidentified U1): CRITICAL_TTC_START 5.60, COLLISION 7.30 (+1.70 s); EGO_PATH_ENTRY 5.85 after critical TTC (+0.25 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -1.45, collision +0.00]
- B's track_006 (A): critical TTC already active before the cut-in: CRITICAL_TTC_START 5.55 <= CUT_IN_FROM_RIGHT_START 7.45 (+1.90 s); EGO_PATH_ENTRY 6.95 after critical TTC (+1.40 s) [local times; t_global: cut_in +0.15, critical_ttc_start -1.75, ego_path_entry -0.35, collision +0.00]
- B's track_007 (unidentified U1): CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 5.50 before critical TTC (-0.05 s) [local times; t_global: critical_ttc_start -1.75, ego_path_entry -1.80, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.30 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U2) (A:e03)<br>g06 TRACK_APPEARED_FRONT(A,U3) (A:e04)<br>g09 TRACK_APPEARED_LEFT(A,U1) (A:e05)<br>g10 TRACK_APPEARED_LEFT(A,U4) (A:e06)<br>g11 TRACK_APPEARED_LEFT(A,U5) (A:e07)<br>g14 CLOSING_START(A,U5) (A:e08) | ego: not yet observed |
| -7.30 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_FRONT(B,U3) (B:e04)<br>g07 TRACK_APPEARED_FRONT(B,U3) (B:e04)<br>g08 TRACK_APPEARED_FRONT(B,U5) (B:e03)<br>g12 TRACK_APPEARED_RIGHT(B,U1) (B:e07)<br>g13 TRACK_APPEARED_RIGHT(B,U2) (B:e05) | ego: not yet observed |
| -7.30 | A | g05 TRACK_APPEARED_FRONT(A,U2) (A:e03)<br>g27 TRACK_LOST(A,U2) (A:e15) | ego: not yet observed |
| -7.30 | A | g06 TRACK_APPEARED_FRONT(A,U3) (A:e04)<br>g20 TRACK_LOST(A,U3) (A:e12) | ego: not yet observed |
| -7.30 | B | g07 TRACK_APPEARED_FRONT(B,U3) (B:e04)<br>g21 TRACK_LOST(B,U3) (B:e12) | ego: not yet observed |
| -7.30 | B | g07 TRACK_APPEARED_FRONT(B,U3) (B:e04)<br>g21 TRACK_LOST(B,U3) (B:e12) | ego: not yet observed |
| -7.30 | B | g08 TRACK_APPEARED_FRONT(B,U5) (B:e03)<br>g68 TRACK_LOST(B,U5) (B:e40) | ego: not yet observed |
| -7.30 | A | g09 TRACK_APPEARED_LEFT(A,U1) (A:e05)<br>g69 TRACK_APPEARED_RIGHT(A,U7) (A:e41)<br>g83 TRACK_LOST(A,U7) (A:e48) | ego: not yet observed |
| -7.30 | A | g09 TRACK_APPEARED_LEFT(A,U1) (A:e05) | ego: not yet observed |
| -7.30 | A | g10 TRACK_APPEARED_LEFT(A,U4) (A:e06)<br>g42 TRACK_LOST(A,U4) (A:e25) | ego: not yet observed |
| -7.30 | A | g11 TRACK_APPEARED_LEFT(A,U5) (A:e07)<br>g24 TRACK_LOST(A,U5) (A:e14) | ego: not yet observed |
| -7.30 | B | g12 TRACK_APPEARED_RIGHT(B,U1) (B:e07)<br>g66 TRACK_LOST(B,U1) (B:e38) | ego: not yet observed |
| -7.30 | B | g12 TRACK_APPEARED_RIGHT(B,U1) (B:e07) | ego: not yet observed |
| -7.30 | B | g12 TRACK_APPEARED_RIGHT(B,U1) (B:e07)<br>g66 TRACK_LOST(B,U1) (B:e38) | ego: not yet observed |
| -7.30 | B | g13 TRACK_APPEARED_RIGHT(B,U2) (B:e05)<br>g28 TRACK_LOST(B,U2) (B:e17) | ego: not yet observed |
| -6.80 | B | g15 CRITICAL_TTC_START(B,U5) (B:e08) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -6.80 | B | g15 CRITICAL_TTC_START(B,U5) (B:e08)<br>g37 CRITICAL_TTC_END(B,U5) (B:e24)<br>g38 EGO_PATH_EXIT(B,U5) (B:e25) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -6.40 | A | g16 TRACK_APPEARED_LEFT(A,B) (A:e10)<br>g17 CLOSING_START(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING |
| -6.40 | A | g17 CLOSING_START(A,B) (A:e11)<br>g23 CLOSING_END(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING |
| -4.30 | B | g18 TRACK_APPEARED_RIGHT(B,A) (B:e09)<br>g19 CLOSING_START(B,A) (B:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| -4.30 | B | g19 CLOSING_START(B,A) (B:e10)<br>g22 CLOSING_END(B,A) (B:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| -2.50 | B | g25 TRACK_APPEARED_RIGHT(B,U6) (B:e15)<br>g26 CLOSING_START(B,U6) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003, track_005 |
| -2.50 | B | g25 TRACK_APPEARED_RIGHT(B,U6) (B:e15)<br>g58 TRACK_LOST(B,U6) (B:e33) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003, track_005 |
| -1.85 | A | g29 EGO_PATH_ENTRY(A,U1) (A:e16)<br>g30 CLOSING_START(A,B) (A:e17)<br>g32 CRITICAL_TTC_START(A,B) (A:e19)<br>g33 CRITICAL_TTC_START(A,U1) (A:e18) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -1.85 | A | g29 EGO_PATH_ENTRY(A,U1) (A:e16)<br>g63 EGO_PATH_EXIT(A,U1) (A:e36) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -1.85 | A | g29 EGO_PATH_ENTRY(A,U1) (A:e16) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -1.85 | A | g29 EGO_PATH_ENTRY(A,U1) (A:e16)<br>g33 CRITICAL_TTC_START(A,U1) (A:e18)<br>g63 EGO_PATH_EXIT(A,U1) (A:e36) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -1.85 | A | g30 CLOSING_START(A,B) (A:e17)<br>g32 CRITICAL_TTC_START(A,B) (A:e19)<br>g48 COLLISION(A,B) (A:e28)<br>g49 CRITICAL_TTC_END(A,B) (A:e29)<br>g50 CLOSING_END(A,B) (A:e30) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -1.85 | B | g31 CLOSING_START(B,A) (B:e18) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -1.85 | B | g31 CLOSING_START(B,A) (B:e18)<br>g47 CLOSING_END(B,A) (B:e28) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -1.85 | A | g33 CRITICAL_TTC_START(A,U1) (A:e18) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -1.80 | B | g34 EGO_PATH_ENTRY(B,U1) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING<br>track_007: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -1.80 | B | g34 EGO_PATH_ENTRY(B,U1) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING<br>track_007: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -1.75 | B | g35 CRITICAL_TTC_START(B,A) (B:e20)<br>g36 CRITICAL_TTC_START(B,U1) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -1.75 | B | g35 CRITICAL_TTC_START(B,A) (B:e20)<br>g75 CRITICAL_TTC_END(B,A) (B:e44)<br>g78 TRACK_APPEARED_RIGHT(B,U6) (B:e45)<br>g79 CLOSING_START(B,U6) (B:e46) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -1.75 | B | g36 CRITICAL_TTC_START(B,U1) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -1.15 | A | g39 TRACK_APPEARED_RIGHT(A,U2) (A:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -0.95 | A | g40 TRACK_APPEARED_LEFT(A,U5) (A:e23)<br>g41 CLOSING_START(A,U5) (A:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -0.95 | A | g41 CLOSING_START(A,U5) (A:e24)<br>g60 CLOSING_END(A,U5) (A:e35) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_004: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_006 |
| -0.50 | B | g43 TRACK_APPEARED_FRONT(B,U2) (B:e26) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -0.50 | B | g43 TRACK_APPEARED_FRONT(B,U2) (B:e26)<br>g62 TRACK_LOST(B,U2) (B:e36) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -0.45 | A | g44 CRITICAL_TTC_START(A,U5) (A:e26) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| -0.45 | A | g44 CRITICAL_TTC_START(A,U5) (A:e26)<br>g65 CRITICAL_TTC_END(A,U5) (A:e39) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| -0.35 | B | g45 EGO_PATH_ENTRY(B,A) (B:e27) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| -0.25 | A | g46 CUT_IN_FROM_LEFT_START(A,U5) (A:e27) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| -0.25 | A | g46 CUT_IN_FROM_LEFT_START(A,U5) (A:e27)<br>g82 CUT_IN_FROM_LEFT_END(A,U5) (A:e46) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CLOSING, CRITICAL_TTC<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| +0.00 | B | g48 COLLISION(A,B) (B:e29) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| +0.05 | A | g51 THROTTLE_END(A) (A:e31)<br>g53 BRAKE_START(A) (A:e32) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| +0.05 | B | g52 THROTTLE_END(B) (B:e30)<br>g54 BRAKE_START(B) (B:e31)<br>g55 TURN_LEFT_START(B) (B:e32) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005 |
| +0.10 | A | g56 TURN_LEFT_START(A) (A:e33)<br>g57 EGO_PATH_ENTRY(A,U5) (A:e34) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| +0.10 | A | g57 EGO_PATH_ENTRY(A,U5) (A:e34)<br>g67 EGO_PATH_EXIT(A,U5) (A:e40) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| +0.15 | B | g59 CUT_IN_FROM_RIGHT_START(B,A) (B:e34) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008 |
| +0.15 | B | g59 CUT_IN_FROM_RIGHT_START(B,A) (B:e34)<br>g80 CUT_IN_FROM_RIGHT_END(B,A) (B:e47) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008 |
| +0.20 | B | g61 EGO_PATH_EXIT(B,U2) (B:e35) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008 |
| +0.35 | B | g64 EGO_PATH_ENTRY(B,U5) (B:e37) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_005, track_008, track_009 |
| +0.80 | A | g69 TRACK_APPEARED_RIGHT(A,U7) (A:e41) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: no active state<br>track_008: no active state<br>track_009: CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| +0.95 | A | g70 TURN_LEFT_END(A) (A:e42)<br>g74 EGO_PATH_ENTRY(A,B) (A:e43) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: no active state<br>track_008: no active state<br>track_009: CUT_IN_FROM_LEFT<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| +0.95 | B | g71 TURN_LEFT_END(B) (B:e41)<br>g72 MOVING_END(B) (B:e42)<br>g73 STOP_START(B) (B:e43) | ego: MOVING, BRAKE, TURN_LEFT<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009 |
| +1.00 | A | g76 MOVING_END(A) (A:e44)<br>g77 STOP_START(A) (A:e45) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005: CRITICAL_TTC<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: CUT_IN_FROM_LEFT<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 |
| +1.00 | B | g79 CLOSING_START(B,U6) (B:e46)<br>g81 CLOSING_END(B,U6) (B:e48) | ego: STOP, BRAKE<br>track_006: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_007, track_008, track_009 |

## Plain-language reading

- 7.30 s before the reference collision, A started moving (already the case when first observed).
- 7.30 s before the reference collision, B started moving (already the case when first observed).
- 7.30 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.30 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared in front of it.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its left.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared on its left.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 7.30 s before the reference collision, A observed anonymous road user U5 start closing in (already the case when first observed).
- 6.80 s before the reference collision, B's time-to-contact with anonymous road user U5 became critical.
- 6.40 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.40 s before the reference collision, A observed B start closing in (already the case when first observed).
- 4.30 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.30 s before the reference collision, B observed A start closing in (already the case when first observed).
- 4.00 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.90 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.75 s before the reference collision, B observed A stop closing in.
- 3.00 s before the reference collision, A observed B stop closing in.
- 2.75 s before the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 2.50 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 2.50 s before the reference collision, B observed anonymous road user U6 start closing in (already the case when first observed).
- 2.50 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.25 s before the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 1.85 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 1.85 s before the reference collision, A observed B start closing in.
- 1.85 s before the reference collision, B observed A start closing in.
- 1.85 s before the reference collision, A's time-to-contact with B became critical.
- 1.85 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 1.80 s before the reference collision, B observed anonymous road user U1 enter its forward path corridor.
- 1.75 s before the reference collision, B's time-to-contact with A became critical.
- 1.75 s before the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 1.15 s before the reference collision, B's time-to-contact with anonymous road user U5 stopped being critical.
- 1.15 s before the reference collision, B observed anonymous road user U5 leave its forward path corridor.
- 1.15 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its right.
- 0.95 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared on its left.
- 0.95 s before the reference collision, A observed anonymous road user U5 start closing in (already the case when first observed).
- 0.55 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 0.50 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared in front of it.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U5 became critical.
- 0.35 s before the reference collision, B observed A enter its forward path corridor.
- 0.25 s before the reference collision, A observed anonymous road user U5 cutting in from the left.
- 0.10 s before the reference collision, B observed A stop closing in.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 389, B: 389 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B started turning left.
- 0.10 s after the reference collision, A started turning left.
- 0.10 s after the reference collision, A observed anonymous road user U5 enter its forward path corridor.
- 0.10 s after the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 0.15 s after the reference collision, B observed A cutting in from the right.
- 0.20 s after the reference collision, A observed anonymous road user U5 stop closing in.
- 0.20 s after the reference collision, B observed anonymous road user U2 leave its forward path corridor.
- 0.30 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 0.35 s after the reference collision, B observed anonymous road user U5 enter its forward path corridor.
- 0.55 s after the reference collision, A's time-to-contact with anonymous road user U5 stopped being critical.
- 0.60 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the reference collision, A observed anonymous road user U5 leave its forward path corridor.
- 0.70 s after the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, A's radar started tracking anonymous road user U7, which appeared on its right.
- 0.95 s after the reference collision, A stopped turning left.
- 0.95 s after the reference collision, B stopped turning left.
- 0.95 s after the reference collision, B stopped moving.
- 0.95 s after the reference collision, B came to a stop.
- 0.95 s after the reference collision, A observed B enter its forward path corridor.
- 1.00 s after the reference collision, B's time-to-contact with A stopped being critical.
- 1.00 s after the reference collision, A stopped moving.
- 1.00 s after the reference collision, A came to a stop.
- 1.00 s after the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 1.00 s after the reference collision, B observed anonymous road user U6 start closing in (already the case when first observed).
- 1.25 s after the reference collision, B observed A's cut-in from the right settle.
- 2.00 s after the reference collision, B observed anonymous road user U6 stop closing in.
- 3.60 s after the reference collision, A observed anonymous road user U5's cut-in from the left settle.
- 4.60 s after the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
