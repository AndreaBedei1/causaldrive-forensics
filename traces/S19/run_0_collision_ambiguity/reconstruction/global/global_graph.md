# Global graph - S19/run_0_collision_ambiguity

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_005#segment_2, A:track_008 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_005 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_002 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003, A:track_009, B:track_003 |
| U4 | anonymous_road_user | anonymous; observed by A as A:track_004 |
| U8 | anonymous_road_user | anonymous; observed by A as A:track_005#segment_1 |
| U7 | anonymous_road_user | anonymous; observed by A, B as A:track_006, B:track_004 |
| U6 | anonymous_road_user | anonymous; observed by A, B as A:track_007, B:track_002 |
| U9 | anonymous_road_user | anonymous; observed by A as A:track_010 |
| U10 | anonymous_road_user | anonymous; observed by A as A:track_011 |
| U5 | anonymous_road_user | anonymous; observed by B as B:track_001 |
| U11 | anonymous_road_user | anonymous; observed by B as B:track_006 |
| U12 | anonymous_road_user | anonymous; observed by B as B:track_007 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e26 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e09 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1897.7 vs 1897.7 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 0.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 3.0 s<br>clearance at the contact 0.61 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006)<br>anonymous road user U1: A:track_001, B:track_005 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 1.80 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.0 m -> 7.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.17 m/s over 1.2 s<br>anonymous road user U2: A:track_002 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 30.7 m -> 28.9 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_003, A:track_009 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 2.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.1 m -> 7.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.08 m/s over 0.9 s<br>anonymous road user U4: A:track_004 |
| A:track_005#segment_1 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 6.45 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 12.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U8: A:track_005#segment_1 |
| A:track_005#segment_2 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 6.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.3 m -> 0.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.42 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006)<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma, over 213 samples; 98% within 3 sigma) at B's own velocity (median difference 0.04 m/s) |
| A:track_006 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.5 m -> 2.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.21 m/s over 3.0 s<br>clearance at the contact 2.26 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006)<br>anonymous road user U7: B:track_004, A:track_006 |
| A:track_007 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.3 m -> 18.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 18.20 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U6: B:track_002, A:track_007 |
| A:track_008 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.6 m -> 3.6 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 3.60 m<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma, over 16 samples; 100% within 3 sigma) at B's own velocity (median difference 0.20 m/s) |
| A:track_009 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.7 m -> 20.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 20.66 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: A:track_003, B:track_003, A:track_009 |
| A:track_010 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U9: A:track_010 |
| A:track_011 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U10: A:track_011 |
| B:track_001 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 16.9 m -> 17.3 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.88 m/s over 3.0 s (> 1.50)<br>clearance at the contact 16.46 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U5: B:track_001 |
| B:track_002 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 13.5 m -> 13.5 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.89 m/s over 3.0 s (> 1.50)<br>clearance at the contact 13.47 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U6: B:track_002, A:track_007 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.9 m -> 15.8 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.06 m/s over 3.0 s (> 1.50)<br>clearance at the contact 15.82 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: A:track_003, B:track_003, A:track_009 |
| B:track_004 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 1.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.96 m/s over 3.0 s (> 1.50)<br>clearance at the contact 1.37 m<br>anonymous road user U7: B:track_004, A:track_006 |
| B:track_005 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 1.5 m -> 1.5 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.92 m/s over 3.0 s (> 1.50)<br>clearance at the contact 1.46 m<br>anonymous road user U1: A:track_001, B:track_005 |
| B:track_006 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U11: B:track_006 |
| B:track_007 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U12: B:track_007 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.75 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.75 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.75 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.75 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -7.75 | TRACK_APPEARED_FRONT | A | U3 | A:e03 @ 0.00, A:e18 @ 3.65 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g06 | -7.75 | TRACK_APPEARED_FRONT | B | U6 | B:e03 @ 0.00 | initial_in_ego_path=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g07 | -7.75 | TRACK_APPEARED_LEFT | A | U2 | A:e04 @ 0.00, A:e20 @ 5.95 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g08 | -7.75 | TRACK_APPEARED_LEFT | B | U3 | B:e05 @ 0.00, B:e22 @ 10.25 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g09 | -7.75 | TRACK_APPEARED_LEFT | B | U5 | B:e04 @ 0.00, B:e29 @ 11.25 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g10 | -7.75 | TRACK_APPEARED_LEFT | B | U7 | B:e06 @ 0.00 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g11 | -7.75 | TRACK_APPEARED_RIGHT | A | U1 | A:e05 @ 0.00, A:e44 @ 9.20 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g12 | -7.75 | TRACK_APPEARED_RIGHT | A | U4 | A:e06 @ 0.00, A:e19 @ 5.65 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g13 | -7.75 | TRACK_APPEARED_RIGHT | B | U1 | B:e07 @ 0.00 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g14 | -7.75 | CLOSING_START | A | U1 | A:e07 @ 0.00, A:e22 @ 7.50 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g15 | -7.75 | CLOSING_START | A | U3 | A:e08 @ 0.00 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g16 | -7.70 | TRACK_APPEARED_LEFT | A | U8 | A:e09 @ 0.05, A:e14 @ 1.30 | initial_in_ego_path=False; source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g17 | -7.70 | CLOSING_START | A | U8 | A:e10 @ 0.05 | active_at_first_observation=True; source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g18 | -7.35 | TRACK_APPEARED_LEFT | A | U7 | A:e11 @ 0.40, A:e43 @ 9.05 | initial_in_ego_path=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g19 | -7.35 | CLOSING_START | A | U7 | A:e12 @ 0.40, A:e29 @ 7.75 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g20 | -7.25 | CRITICAL_TTC_START | B | U6 | B:e08 @ 0.50, B:e12 @ 8.25 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g21 | -6.90 | EGO_PATH_EXIT | A | U7 | A:e13 @ 0.85 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g22 | -6.45 | TRACK_LOST | A | U8 | A:e14 @ 1.30 | source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g23 | -6.40 | TRACK_APPEARED_FRONT | A | B | A:e15 @ 1.35, A:e24 @ 7.70, A:e35 @ 8.45 | initial_in_ego_path=True; source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2', 'A:track_008'] |
| g24 | -6.40 | CLOSING_START | A | B | A:e16 @ 1.35, A:e28 @ 7.75 | active_at_first_observation=True; source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g25 | -5.90 | CRITICAL_TTC_START | A | B | A:e17 @ 1.85, A:e27 @ 7.75 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g26 | -4.10 | TRACK_LOST | A | U3 | A:e18 @ 3.65 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g27 | -2.10 | TRACK_LOST | A | U4 | A:e19 @ 5.65 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g28 | -1.80 | TRACK_LOST | A | U2 | A:e20 @ 5.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g29 | -0.80 | CUT_IN_FROM_RIGHT_START | A | U1 | A:e21 @ 6.95, A:e30 @ 7.80 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g30 | -0.25 | CLOSING_END | A | U1 | A:e22 @ 7.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g31 | -0.05 | TRACK_APPEARED_FRONT | A | U6 | A:e23 @ 7.70, A:e34 @ 8.45 | initial_in_ego_path=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g32 | -0.05 | TRACK_APPEARED_LEFT | A | U3 | A:e25 @ 7.70, A:e36 @ 8.45 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g33 | 0.00 | COLLISION | - | A, B | A:e26 @ 7.75, B:e09 @ 7.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 1897.70, B 1897.70 |
| g34 | 0.00 | CRITICAL_TTC_END | A | B | A:e27 @ 7.75 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g35 | 0.00 | CLOSING_END | A | B | A:e28 @ 7.75 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g36 | 0.00 | CLOSING_END | A | U7 | A:e29 @ 7.75 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g37 | 0.00 | THROTTLE_END | B | - | B:e10 @ 7.75 |  |
| g38 | 0.05 | CUT_IN_FROM_RIGHT_END | A | U1 | A:e30 @ 7.80 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g39 | 0.05 | THROTTLE_END | A | - | A:e31 @ 7.80 |  |
| g40 | 0.05 | BRAKE_START | A | - | A:e32 @ 7.80 |  |
| g41 | 0.05 | BRAKE_START | B | - | B:e11 @ 7.80 |  |
| g42 | 0.50 | CRITICAL_TTC_END | B | U6 | B:e12 @ 8.25 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g43 | 0.70 | TRACK_LOST | A | U3 | A:e36 @ 8.45 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g44 | 0.70 | TRACK_LOST | A | U6 | A:e34 @ 8.45 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g45 | 1.15 | MOVING_END | A | - | A:e37 @ 8.90 |  |
| g46 | 1.15 | STOP_START | A | - | A:e38 @ 8.90 |  |
| g47 | 1.20 | TRACK_APPEARED_LEFT | A | U9 | A:e39 @ 8.95, A:e47 @ 10.85 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g48 | 1.20 | TRACK_APPEARED_RIGHT | A | U10 | A:e40 @ 8.95, A:e48 @ 10.85 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g49 | 1.20 | CLOSING_START | A | U10 | A:e42 @ 8.95, A:e46 @ 9.90 | active_at_first_observation=True; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g50 | 1.20 | CLOSING_START | A | U9 | A:e41 @ 8.95, A:e45 @ 9.85 | active_at_first_observation=True; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g51 | 1.25 | MOVING_END | B | - | B:e13 @ 9.00 |  |
| g52 | 1.25 | STOP_START | B | - | B:e14 @ 9.00 |  |
| g53 | 1.30 | TRACK_LOST | A | U7 | A:e43 @ 9.05 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g54 | 1.45 | TRACK_LOST | A | U1 | A:e44 @ 9.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g55 | 1.65 | TRACK_APPEARED_LEFT | B | U11 | B:e15 @ 9.40 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g56 | 1.65 | CLOSING_START | B | U11 | B:e16 @ 9.40, B:e24 @ 10.30 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g57 | 1.75 | TRACK_APPEARED_RIGHT | B | U12 | B:e17 @ 9.50 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g58 | 1.75 | CLOSING_START | B | U12 | B:e18 @ 9.50, B:e25 @ 10.35 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g59 | 2.10 | CLOSING_END | A | U9 | A:e45 @ 9.85 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g60 | 2.15 | CLOSING_END | A | U10 | A:e46 @ 9.90 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g61 | 2.15 | CRITICAL_TTC_START | B | U11 | B:e19 @ 9.90, B:e21 @ 10.25 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g62 | 2.25 | CRITICAL_TTC_START | B | U12 | B:e20 @ 10.00, B:e23 @ 10.30 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g63 | 2.50 | CRITICAL_TTC_END | B | U11 | B:e21 @ 10.25 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g64 | 2.50 | TRACK_LOST | B | U3 | B:e22 @ 10.25 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g65 | 2.55 | CRITICAL_TTC_END | B | U12 | B:e23 @ 10.30 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g66 | 2.55 | CLOSING_END | B | U11 | B:e24 @ 10.30 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g67 | 2.60 | CLOSING_END | B | U12 | B:e25 @ 10.35 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g68 | 2.90 | EGO_PATH_EXIT | B | U6 | B:e26 @ 10.65 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g69 | 2.90 | CUT_IN_FROM_RIGHT_START | B | U1 | B:e27 @ 10.65 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g70 | 3.10 | TRACK_LOST | A | U10 | A:e48 @ 10.85 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g71 | 3.10 | TRACK_LOST | A | U9 | A:e47 @ 10.85 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g72 | 3.25 | EGO_PATH_ENTRY | B | U1 | B:e28 @ 11.00 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g73 | 3.50 | TRACK_LOST | B | U5 | B:e29 @ 11.25 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |

## Edges

```
    g01 --PRECEDES--> g16
    g01 --PRECEDES--> g17
    g02 --PRECEDES--> g16
    g02 --PRECEDES--> g17
    g03 --PRECEDES--> g16
    g03 --PRECEDES--> g17
    g04 --PRECEDES--> g16
    g04 --PRECEDES--> g17
    g05 --PRECEDES--> g16
    g05 --PRECEDES--> g17
    g06 --PRECEDES--> g16
    g06 --PRECEDES--> g17
    g07 --PRECEDES--> g16
    g07 --PRECEDES--> g17
    g08 --PRECEDES--> g16
    g08 --PRECEDES--> g17
    g09 --PRECEDES--> g16
    g09 --PRECEDES--> g17
    g10 --PRECEDES--> g16
    g10 --PRECEDES--> g17
    g11 --PRECEDES--> g16
    g11 --PRECEDES--> g17
    g12 --PRECEDES--> g16
    g12 --PRECEDES--> g17
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
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
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g33 --PRECEDES--> g39
    g33 --PRECEDES--> g40
    g33 --PRECEDES--> g41
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g34 --PRECEDES--> g41
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g35 --PRECEDES--> g41
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g42
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g45 --PRECEDES--> g50
    g46 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g47 --PRECEDES--> g51
    g47 --PRECEDES--> g52
    g48 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g53
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g54 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g62
    g62 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g63 --PRECEDES--> g65
    g63 --PRECEDES--> g66
    g64 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g65 --PRECEDES--> g67
    g66 --PRECEDES--> g67
    g67 --PRECEDES--> g68
    g67 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g68 --PRECEDES--> g71
    g69 --PRECEDES--> g70
    g69 --PRECEDES--> g71
    g70 --PRECEDES--> g72
    g71 --PRECEDES--> g72
    g72 --PRECEDES--> g73
    g11 --SAME_TRACK--> g14
    g05 --SAME_TRACK--> g15
    g16 --SAME_TRACK--> g17
    g18 --SAME_TRACK--> g19
    g18 --SAME_TRACK--> g21
    g16 --SAME_TRACK--> g22
    g23 --SAME_TRACK--> g24
    g23 --SAME_TRACK--> g25
    g05 --SAME_TRACK--> g26
    g12 --SAME_TRACK--> g27
    g07 --SAME_TRACK--> g28
    g11 --SAME_TRACK--> g29
    g11 --SAME_TRACK--> g30
    g23 --SAME_TRACK--> g34
    g23 --SAME_TRACK--> g35
    g18 --SAME_TRACK--> g36
    g11 --SAME_TRACK--> g38
    g31 --SAME_TRACK--> g44
    g32 --SAME_TRACK--> g43
    g47 --SAME_TRACK--> g50
    g48 --SAME_TRACK--> g49
    g18 --SAME_TRACK--> g53
    g11 --SAME_TRACK--> g54
    g47 --SAME_TRACK--> g59
    g48 --SAME_TRACK--> g60
    g47 --SAME_TRACK--> g71
    g48 --SAME_TRACK--> g70
    g06 --SAME_TRACK--> g20
    g06 --SAME_TRACK--> g42
    g55 --SAME_TRACK--> g56
    g57 --SAME_TRACK--> g58
    g55 --SAME_TRACK--> g61
    g57 --SAME_TRACK--> g62
    g55 --SAME_TRACK--> g63
    g08 --SAME_TRACK--> g64
    g57 --SAME_TRACK--> g65
    g55 --SAME_TRACK--> g66
    g57 --SAME_TRACK--> g67
    g06 --SAME_TRACK--> g68
    g13 --SAME_TRACK--> g69
    g13 --SAME_TRACK--> g72
    g09 --SAME_TRACK--> g73
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U6); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U3); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_LEFT(B,U7); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(A,U3) |
| -7.70 | TRACK_APPEARED_LEFT(A,U8); CLOSING_START(A,U8) |
| -7.35 | TRACK_APPEARED_LEFT(A,U7); CLOSING_START(A,U7) |
| -7.25 | CRITICAL_TTC_START(B,U6) |
| -6.90 | EGO_PATH_EXIT(A,U7) |
| -6.45 | TRACK_LOST(A,U8) |
| -6.40 | TRACK_APPEARED_FRONT(A,B); CLOSING_START(A,B) |
| -5.90 | CRITICAL_TTC_START(A,B) |
| -4.10 | TRACK_LOST(A,U3) |
| -2.10 | TRACK_LOST(A,U4) |
| -1.80 | TRACK_LOST(A,U2) |
| -0.80 | CUT_IN_FROM_RIGHT_START(A,U1) |
| -0.25 | CLOSING_END(A,U1) |
| -0.05 | TRACK_APPEARED_FRONT(A,U6); TRACK_APPEARED_LEFT(A,U3) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(A,U7); THROTTLE_END(B) |
| +0.05 | CUT_IN_FROM_RIGHT_END(A,U1); THROTTLE_END(A); BRAKE_START(A); BRAKE_START(B) |
| +0.50 | CRITICAL_TTC_END(B,U6) |
| +0.70 | TRACK_LOST(A,U3); TRACK_LOST(A,U6) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +1.20 | TRACK_APPEARED_LEFT(A,U9); TRACK_APPEARED_RIGHT(A,U10); CLOSING_START(A,U10); CLOSING_START(A,U9) |
| +1.25 | MOVING_END(B); STOP_START(B) |
| +1.30 | TRACK_LOST(A,U7) |
| +1.45 | TRACK_LOST(A,U1) |
| +1.65 | TRACK_APPEARED_LEFT(B,U11); CLOSING_START(B,U11) |
| +1.75 | TRACK_APPEARED_RIGHT(B,U12); CLOSING_START(B,U12) |
| +2.10 | CLOSING_END(A,U9) |
| +2.15 | CLOSING_END(A,U10); CRITICAL_TTC_START(B,U11) |
| +2.25 | CRITICAL_TTC_START(B,U12) |
| +2.50 | CRITICAL_TTC_END(B,U11); TRACK_LOST(B,U3) |
| +2.55 | CRITICAL_TTC_END(B,U12); CLOSING_END(B,U11) |
| +2.60 | CLOSING_END(B,U12) |
| +2.90 | EGO_PATH_EXIT(B,U6); CUT_IN_FROM_RIGHT_START(B,U1) |
| +3.10 | TRACK_LOST(A,U10); TRACK_LOST(A,U9) |
| +3.25 | EGO_PATH_ENTRY(B,U1) |
| +3.50 | TRACK_LOST(B,U5) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CUT_IN_FROM_RIGHT_START 6.95, no critical TTC after it [local times; t_global: cut_in -0.80, collision +0.00]
- A's track_005#segment_2 (B): CRITICAL_TTC_START 1.85, COLLISION with B 7.75 (+5.90 s) [local times; t_global: critical_ttc_start -5.90, collision +0.00]
- A's track_008 (B): CRITICAL_TTC_START 8.20 [local times; t_global: critical_ttc_start +0.45]
- B's track_002 (unidentified U6): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_005 (unidentified U1): CUT_IN_FROM_RIGHT_START 10.65, no critical TTC after it; EGO_PATH_ENTRY 11.00, no critical TTC [local times; t_global: cut_in +2.90, ego_path_entry +3.25]
- B's track_006 (unidentified U11): CRITICAL_TTC_START 9.90 [local times; t_global: critical_ttc_start +2.15]
- B's track_007 (unidentified U12): CRITICAL_TTC_START 10.00 [local times; t_global: critical_ttc_start +2.25]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U3) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,U2) (A:e04)<br>g11 TRACK_APPEARED_RIGHT(A,U1) (A:e05)<br>g12 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g14 CLOSING_START(A,U1) (A:e07)<br>g15 CLOSING_START(A,U3) (A:e08) | ego: not yet observed |
| -7.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U6) (B:e03)<br>g08 TRACK_APPEARED_LEFT(B,U3) (B:e05)<br>g09 TRACK_APPEARED_LEFT(B,U5) (B:e04)<br>g10 TRACK_APPEARED_LEFT(B,U7) (B:e06)<br>g13 TRACK_APPEARED_RIGHT(B,U1) (B:e07) | ego: not yet observed |
| -7.75 | A | g05 TRACK_APPEARED_FRONT(A,U3) (A:e03)<br>g26 TRACK_LOST(A,U3) (A:e18) | ego: not yet observed |
| -7.75 | A | g07 TRACK_APPEARED_LEFT(A,U2) (A:e04)<br>g28 TRACK_LOST(A,U2) (A:e20) | ego: not yet observed |
| -7.75 | B | g08 TRACK_APPEARED_LEFT(B,U3) (B:e05)<br>g61 CRITICAL_TTC_START(B,U11) (B:e19)<br>g63 CRITICAL_TTC_END(B,U11) (B:e21)<br>g64 TRACK_LOST(B,U3) (B:e22) | ego: not yet observed |
| -7.75 | B | g09 TRACK_APPEARED_LEFT(B,U5) (B:e04)<br>g73 TRACK_LOST(B,U5) (B:e29) | ego: not yet observed |
| -7.75 | A | g11 TRACK_APPEARED_RIGHT(A,U1) (A:e05)<br>g54 TRACK_LOST(A,U1) (A:e44) | ego: not yet observed |
| -7.75 | A | g12 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g27 TRACK_LOST(A,U4) (A:e19) | ego: not yet observed |
| -7.75 | A | g14 CLOSING_START(A,U1) (A:e07)<br>g30 CLOSING_END(A,U1) (A:e22) | ego: not yet observed |
| -7.70 | A | g16 TRACK_APPEARED_LEFT(A,U8) (A:e09)<br>g17 CLOSING_START(A,U8) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.70 | A | g16 TRACK_APPEARED_LEFT(A,U8) (A:e09)<br>g22 TRACK_LOST(A,U8) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.35 | A | g18 TRACK_APPEARED_LEFT(A,U7) (A:e11)<br>g19 CLOSING_START(A,U7) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -7.35 | A | g18 TRACK_APPEARED_LEFT(A,U7) (A:e11)<br>g53 TRACK_LOST(A,U7) (A:e43) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -7.35 | A | g19 CLOSING_START(A,U7) (A:e12)<br>g24 CLOSING_START(A,B) (A:e16)<br>g25 CRITICAL_TTC_START(A,B) (A:e17)<br>g33 COLLISION(A,B) (A:e26)<br>g34 CRITICAL_TTC_END(A,B) (A:e27)<br>g35 CLOSING_END(A,B) (A:e28)<br>g36 CLOSING_END(A,U7) (A:e29) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -7.25 | B | g20 CRITICAL_TTC_START(B,U6) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -7.25 | B | g20 CRITICAL_TTC_START(B,U6) (B:e08)<br>g42 CRITICAL_TTC_END(B,U6) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -6.90 | A | g21 EGO_PATH_EXIT(A,U7) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, IN_EGO_PATH, CRITICAL_TTC? |
| -6.40 | A | g23 TRACK_APPEARED_FRONT(A,B) (A:e15)<br>g24 CLOSING_START(A,B) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005#segment_1 |
| -6.40 | A | g23 TRACK_APPEARED_FRONT(A,B) (A:e15)<br>g31 TRACK_APPEARED_FRONT(A,U6) (A:e23)<br>g32 TRACK_APPEARED_LEFT(A,U3) (A:e25) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005#segment_1 |
| -6.40 | A | g23 TRACK_APPEARED_FRONT(A,B) (A:e15)<br>g31 TRACK_APPEARED_FRONT(A,U6) (A:e23)<br>g32 TRACK_APPEARED_LEFT(A,U3) (A:e25)<br>g43 TRACK_LOST(A,U3) (A:e36)<br>g44 TRACK_LOST(A,U6) (A:e34) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005#segment_1 |
| -5.90 | A | g25 CRITICAL_TTC_START(A,B) (A:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_005#segment_1 |
| -0.80 | A | g29 CUT_IN_FROM_RIGHT_START(A,U1) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 |
| -0.80 | A | g29 CUT_IN_FROM_RIGHT_START(A,U1) (A:e21)<br>g38 CUT_IN_FROM_RIGHT_END(A,U1) (A:e30)<br>g39 THROTTLE_END(A) (A:e31)<br>g40 BRAKE_START(A) (A:e32) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1 |
| +0.00 | B | g33 COLLISION(A,B) (B:e09)<br>g37 THROTTLE_END(B) (B:e10) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| +0.05 | B | g41 BRAKE_START(B) (B:e11) | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| +1.15 | A | g45 MOVING_END(A) (A:e37)<br>g46 STOP_START(A) (A:e38) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 |
| +1.20 | A | g47 TRACK_APPEARED_LEFT(A,U9) (A:e39)<br>g48 TRACK_APPEARED_RIGHT(A,U10) (A:e40)<br>g49 CLOSING_START(A,U10) (A:e42)<br>g50 CLOSING_START(A,U9) (A:e41) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 |
| +1.20 | A | g47 TRACK_APPEARED_LEFT(A,U9) (A:e39)<br>g48 TRACK_APPEARED_RIGHT(A,U10) (A:e40)<br>g70 TRACK_LOST(A,U10) (A:e48)<br>g71 TRACK_LOST(A,U9) (A:e47) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 |
| +1.20 | A | g49 CLOSING_START(A,U10) (A:e42)<br>g60 CLOSING_END(A,U10) (A:e46) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 |
| +1.20 | A | g50 CLOSING_START(A,U9) (A:e41)<br>g59 CLOSING_END(A,U9) (A:e45) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005#segment_2: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1, track_007, track_008, track_009 |
| +1.25 | B | g51 MOVING_END(B) (B:e13)<br>g52 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| +1.65 | B | g55 TRACK_APPEARED_LEFT(B,U11) (B:e15)<br>g56 CLOSING_START(B,U11) (B:e16) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| +1.65 | B | g56 CLOSING_START(B,U11) (B:e16)<br>g62 CRITICAL_TTC_START(B,U12) (B:e20)<br>g65 CRITICAL_TTC_END(B,U12) (B:e23)<br>g66 CLOSING_END(B,U11) (B:e24) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| +1.75 | B | g57 TRACK_APPEARED_RIGHT(B,U12) (B:e17)<br>g58 CLOSING_START(B,U12) (B:e18) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC? |
| +1.75 | B | g58 CLOSING_START(B,U12) (B:e18)<br>g67 CLOSING_END(B,U12) (B:e25) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC? |
| +2.15 | B | g61 CRITICAL_TTC_START(B,U11) (B:e19) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC?<br>track_007: CLOSING, CRITICAL_TTC? |
| +2.25 | B | g62 CRITICAL_TTC_START(B,U12) (B:e20) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC? |
| +2.90 | B | g68 EGO_PATH_EXIT(B,U6) (B:e26)<br>g69 CUT_IN_FROM_RIGHT_START(B,U1) (B:e27) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003 |
| +3.25 | B | g72 EGO_PATH_ENTRY(B,U1) (B:e28) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_005: CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_003 |

## Plain-language reading

- 7.75 s before the reference collision, A started moving (already the case when first observed).
- 7.75 s before the reference collision, B started moving (already the case when first observed).
- 7.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared in front of it.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.75 s before the reference collision, A observed anonymous road user U1 start closing in (already the case when first observed).
- 7.75 s before the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
- 7.70 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared on its left.
- 7.70 s before the reference collision, A observed anonymous road user U8 start closing in (already the case when first observed).
- 7.35 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared on its left.
- 7.35 s before the reference collision, A observed anonymous road user U7 start closing in (already the case when first observed).
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U6 became critical.
- 6.90 s before the reference collision, A observed anonymous road user U7 leave its forward path corridor.
- 6.45 s before the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 6.40 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 6.40 s before the reference collision, A observed B start closing in (already the case when first observed).
- 5.90 s before the reference collision, A's time-to-contact with B became critical.
- 4.10 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.10 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 1.80 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 0.80 s before the reference collision, A observed anonymous road user U1 cutting in from the right.
- 0.25 s before the reference collision, A observed anonymous road user U1 stop closing in.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared in front of it.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1898, B: 1898 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, A observed anonymous road user U7 stop closing in.
- At the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A observed anonymous road user U1's cut-in from the right settle.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.50 s after the reference collision, B's time-to-contact with anonymous road user U6 stopped being critical.
- 0.70 s after the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.20 s after the reference collision, A's radar started tracking anonymous road user U9, which appeared on its left.
- 1.20 s after the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 1.20 s after the reference collision, A observed anonymous road user U10 start closing in (already the case when first observed).
- 1.20 s after the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 1.25 s after the reference collision, B stopped moving.
- 1.25 s after the reference collision, B came to a stop.
- 1.30 s after the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 1.45 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 1.65 s after the reference collision, B's radar started tracking anonymous road user U11, which appeared on its left.
- 1.65 s after the reference collision, B observed anonymous road user U11 start closing in (already the case when first observed).
- 1.75 s after the reference collision, B's radar started tracking anonymous road user U12, which appeared on its right.
- 1.75 s after the reference collision, B observed anonymous road user U12 start closing in (already the case when first observed).
- 2.10 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 2.15 s after the reference collision, A observed anonymous road user U10 stop closing in.
- 2.15 s after the reference collision, B's time-to-contact with anonymous road user U11 became critical.
- 2.25 s after the reference collision, B's time-to-contact with anonymous road user U12 became critical.
- 2.50 s after the reference collision, B's time-to-contact with anonymous road user U11 stopped being critical.
- 2.50 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.55 s after the reference collision, B's time-to-contact with anonymous road user U12 stopped being critical.
- 2.55 s after the reference collision, B observed anonymous road user U11 stop closing in.
- 2.60 s after the reference collision, B observed anonymous road user U12 stop closing in.
- 2.90 s after the reference collision, B observed anonymous road user U6 leave its forward path corridor.
- 2.90 s after the reference collision, B observed anonymous road user U1 cutting in from the right.
- 3.10 s after the reference collision, A's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 3.10 s after the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 3.25 s after the reference collision, B observed anonymous road user U1 enter its forward path corridor.
- 3.50 s after the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
