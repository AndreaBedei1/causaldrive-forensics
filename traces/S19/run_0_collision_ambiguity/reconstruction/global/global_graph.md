# Global graph - S19/run_0_collision_ambiguity

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_005#segment_2, A:track_005#segment_4 |
| U1 | anonymous_road_user | anonymous; observed by A as A:track_001#segment_1 |
| U7 | anonymous_road_user | anonymous; observed by A, B as A:track_001#segment_2, B:track_003 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_002 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003, A:track_008, B:track_004 |
| U4 | anonymous_road_user | anonymous; observed by A as A:track_004 |
| U8 | anonymous_road_user | anonymous; observed by A as A:track_005#segment_1 |
| U9 | anonymous_road_user | anonymous; observed by A as A:track_005#segment_3 |
| U6 | anonymous_road_user | anonymous; observed by A, B as A:track_006, B:track_002 |
| U5 | anonymous_road_user | anonymous; observed by A, B as A:track_007, B:track_001 |
| U10 | anonymous_road_user | anonymous; observed by A as A:track_009 |
| U11 | anonymous_road_user | anonymous; observed by A as A:track_010 |
| U12 | anonymous_road_user | anonymous; observed by A as A:track_011 |
| U13 | anonymous_road_user | anonymous; observed by B as B:track_005 |
| U14 | anonymous_road_user | anonymous; observed by B as B:track_006 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e30 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1897.7 vs 1897.7 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 7.00 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 14.0 m -> 13.1 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001#segment_1 |
| A:track_001#segment_2 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 6.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 1.2 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.37 m/s for reference)<br>clearance at the contact 1.18 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001#segment_2, track_005#segment_2, track_006)<br>anonymous road user U7: B:track_003, A:track_001#segment_2 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 1.80 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.0 m -> 7.2 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.17 m/s for reference)<br>anonymous road user U2: A:track_002 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 30.6 m -> 28.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_004, A:track_008 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 2.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.1 m -> 7.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.07 m/s for reference)<br>anonymous road user U4: A:track_004 |
| A:track_005#segment_1 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 6.85 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 14.7 m -> 13.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U8: A:track_005#segment_1 |
| A:track_005#segment_2 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 6.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 0.0 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.70 m/s for reference)<br>clearance at the contact 0.00 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001#segment_2, track_005#segment_2, track_006)<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 138 samples; 100% within 3 sigma) at B's own velocity |
| A:track_005#segment_3 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U9: A:track_005#segment_3 |
| A:track_005#segment_4 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 54 samples; 100% within 3 sigma) at B's own velocity |
| A:track_006 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.5 m -> 2.2 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.21 m/s for reference)<br>clearance at the contact 2.23 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001#segment_2, track_005#segment_2, track_006)<br>anonymous road user U6: B:track_002, A:track_006 |
| A:track_007 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.3 m -> 18.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 18.20 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U5: B:track_001, A:track_007 |
| A:track_008 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.9 m -> 20.9 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 20.88 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: A:track_003, B:track_004, A:track_008 |
| A:track_009 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U10: A:track_009 |
| A:track_010 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U11: A:track_010 |
| A:track_011 | U12 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U12: A:track_011 |
| B:track_001 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 13.5 m -> 13.5 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.88 m/s for reference)<br>clearance at the contact 13.48 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U5: B:track_001, A:track_007 |
| B:track_002 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 1.4 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.95 m/s for reference)<br>clearance at the contact 1.36 m<br>anonymous road user U6: B:track_002, A:track_006 |
| B:track_003 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 1.5 m -> 1.5 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.93 m/s for reference)<br>clearance at the contact 1.45 m<br>anonymous road user U7: B:track_003, A:track_001#segment_2 |
| B:track_004 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.9 m -> 15.9 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 2.06 m/s for reference)<br>clearance at the contact 15.87 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: A:track_003, B:track_004, A:track_008 |
| B:track_005 | U13 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U13: B:track_005 |
| B:track_006 | U14 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U14: B:track_006 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.75 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.75 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.75 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.75 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -7.75 | TRACK_APPEARED_FRONT | A | U3 | A:e03 @ 0.00, A:e22 @ 3.65 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g06 | -7.75 | TRACK_APPEARED_FRONT | B | U5 | B:e03 @ 0.00 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g07 | -7.75 | TRACK_APPEARED_LEFT | A | U2 | A:e04 @ 0.00, A:e24 @ 5.95 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g08 | -7.75 | TRACK_APPEARED_LEFT | B | U6 | B:e04 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g09 | -7.75 | TRACK_APPEARED_RIGHT | A | U1 | A:e05 @ 0.00, A:e13 @ 0.75 | initial_in_ego_path=False; source_track=track_001#segment_1; aggregation=entity_state_union; source_tracks=['A:track_001#segment_1'] |
| g10 | -7.75 | TRACK_APPEARED_RIGHT | A | U4 | A:e06 @ 0.00, A:e23 @ 5.65 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g11 | -7.75 | TRACK_APPEARED_RIGHT | B | U7 | B:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g12 | -7.75 | CLOSING_START | A | U1 | A:e07 @ 0.00 | active_at_first_observation=True; source_track=track_001#segment_1; aggregation=entity_state_union; source_tracks=['A:track_001#segment_1'] |
| g13 | -7.75 | CLOSING_START | A | U3 | A:e08 @ 0.00 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g14 | -7.70 | TRACK_APPEARED_LEFT | A | U8 | A:e09 @ 0.05, A:e16 @ 0.90 | initial_in_ego_path=False; source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g15 | -7.70 | CLOSING_START | A | U8 | A:e10 @ 0.05 | active_at_first_observation=True; source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g16 | -7.65 | TRACK_APPEARED_LEFT | B | U3 | B:e06 @ 0.10, B:e21 @ 10.25 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g17 | -7.40 | TRACK_APPEARED_LEFT | A | U6 | A:e11 @ 0.35, A:e51 @ 9.05 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g18 | -7.40 | CLOSING_START | A | U6 | A:e12 @ 0.35, A:e32 @ 7.75 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g19 | -7.25 | CRITICAL_TTC_START | B | U5 | B:e07 @ 0.50, B:e11 @ 8.25 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g20 | -7.00 | TRACK_LOST | A | U1 | A:e13 @ 0.75 | source_track=track_001#segment_1; aggregation=entity_state_union; source_tracks=['A:track_001#segment_1'] |
| g21 | -6.95 | TRACK_APPEARED_RIGHT | A | U7 | A:e14 @ 0.80, A:e44 @ 8.75 | initial_in_ego_path=False; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g22 | -6.95 | CLOSING_START | A | U7 | A:e15 @ 0.80, A:e26 @ 7.55 | active_at_first_observation=True; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g23 | -6.85 | TRACK_LOST | A | U8 | A:e16 @ 0.90 | source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g24 | -6.80 | TRACK_APPEARED_FRONT | A | B | A:e17 @ 0.95, A:e35 @ 7.80 | initial_in_ego_path=True; source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g25 | -6.80 | CLOSING_START | A | B | A:e18 @ 0.95 | active_at_first_observation=True; source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g26 | -6.30 | CRITICAL_TTC_START | A | B | A:e19 @ 1.45, A:e31 @ 7.75 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g27 | -6.25 | CUT_IN_FROM_RIGHT_START | A | U7 | A:e20 @ 1.50, A:e21 @ 1.75 | geometry=estimated_body; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g28 | -6.00 | CUT_IN_FROM_RIGHT_END | A | U7 | A:e21 @ 1.75 | geometry=estimated_body; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g29 | -4.10 | TRACK_LOST | A | U3 | A:e22 @ 3.65 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g30 | -2.10 | TRACK_LOST | A | U4 | A:e23 @ 5.65 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g31 | -1.80 | TRACK_LOST | A | U2 | A:e24 @ 5.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g32 | -0.80 | CUT_IN_FROM_RIGHT_START | A | U7 | A:e25 @ 6.95, A:e27 @ 7.70 | geometry=estimated_body; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g33 | -0.20 | CLOSING_END | A | U7 | A:e26 @ 7.55 | source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g34 | -0.05 | CUT_IN_FROM_RIGHT_END | A | U7 | A:e27 @ 7.70 | geometry=estimated_body; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g35 | -0.05 | TRACK_APPEARED_FRONT | A | U5 | A:e28 @ 7.70, A:e41 @ 8.45 | initial_in_ego_path=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g36 | -0.05 | TRACK_APPEARED_LEFT | A | U3 | A:e29 @ 7.70, A:e42 @ 8.45 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g37 | 0.00 | COLLISION | - | A, B | A:e30 @ 7.75, B:e08 @ 7.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 1897.70, B 1897.70 |
| g38 | 0.00 | CRITICAL_TTC_END | A | B | A:e31 @ 7.75 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g39 | 0.00 | CLOSING_END | A | U6 | A:e32 @ 7.75 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g40 | 0.00 | THROTTLE_END | B | - | B:e09 @ 7.75 |  |
| g41 | 0.05 | THROTTLE_END | A | - | A:e33 @ 7.80 |  |
| g42 | 0.05 | BRAKE_START | A | - | A:e34 @ 7.80 |  |
| g43 | 0.05 | BRAKE_START | B | - | B:e10 @ 7.80 |  |
| g44 | 0.05 | TRACK_LOST | A | B | A:e35 @ 7.80 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g45 | 0.10 | TRACK_APPEARED_LEFT | A | U9 | A:e36 @ 7.85, A:e53 @ 9.25 | initial_in_ego_path=False; source_track=track_005#segment_3; aggregation=entity_state_union; source_tracks=['A:track_005#segment_3'] |
| g46 | 0.10 | CLOSING_START | A | U9 | A:e37 @ 7.85, A:e38 @ 8.15 | active_at_first_observation=True; source_track=track_005#segment_3; aggregation=entity_state_union; source_tracks=['A:track_005#segment_3'] |
| g47 | 0.40 | CLOSING_END | A | U9 | A:e38 @ 8.15 | source_track=track_005#segment_3; aggregation=entity_state_union; source_tracks=['A:track_005#segment_3'] |
| g48 | 0.45 | EGO_PATH_ENTRY | A | U7 | A:e39 @ 8.20 | geometry=estimated_body; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g49 | 0.45 | CRITICAL_TTC_START | A | U7 | A:e40 @ 8.20 | source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g50 | 0.50 | CRITICAL_TTC_END | B | U5 | B:e11 @ 8.25 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g51 | 0.70 | TRACK_LOST | A | U3 | A:e42 @ 8.45 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g52 | 0.70 | TRACK_LOST | A | U5 | A:e41 @ 8.45 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g53 | 0.80 | TRACK_APPEARED_RIGHT | A | U10 | A:e43 @ 8.55, A:e52 @ 9.20 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g54 | 1.00 | TRACK_LOST | A | U7 | A:e44 @ 8.75 | source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g55 | 1.15 | MOVING_END | A | - | A:e45 @ 8.90 |  |
| g56 | 1.15 | STOP_START | A | - | A:e46 @ 8.90 |  |
| g57 | 1.20 | TRACK_APPEARED_LEFT | A | U11 | A:e47 @ 8.95, A:e57 @ 10.85 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g58 | 1.20 | TRACK_APPEARED_RIGHT | A | U12 | A:e48 @ 8.95, A:e58 @ 10.85 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g59 | 1.20 | CLOSING_START | A | U11 | A:e49 @ 8.95, A:e56 @ 10.00 | active_at_first_observation=True; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g60 | 1.20 | CLOSING_START | A | U12 | A:e50 @ 8.95, A:e55 @ 9.95 | active_at_first_observation=True; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g61 | 1.25 | MOVING_END | B | - | B:e12 @ 9.00 |  |
| g62 | 1.25 | STOP_START | B | - | B:e13 @ 9.00 |  |
| g63 | 1.30 | TRACK_LOST | A | U6 | A:e51 @ 9.05 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g64 | 1.45 | TRACK_LOST | A | U10 | A:e52 @ 9.20 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g65 | 1.50 | TRACK_LOST | A | U9 | A:e53 @ 9.25 | source_track=track_005#segment_3; aggregation=entity_state_union; source_tracks=['A:track_005#segment_3'] |
| g66 | 1.55 | TRACK_APPEARED_FRONT | A | B | A:e54 @ 9.30 | initial_in_ego_path=True; source_track=track_005#segment_4; aggregation=entity_state_union; source_tracks=['A:track_005#segment_4'] |
| g67 | 1.65 | TRACK_APPEARED_LEFT | B | U13 | B:e14 @ 9.40 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g68 | 1.65 | CLOSING_START | B | U13 | B:e15 @ 9.40, B:e23 @ 10.30 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g69 | 1.75 | TRACK_APPEARED_RIGHT | B | U14 | B:e16 @ 9.50 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g70 | 1.75 | CLOSING_START | B | U14 | B:e17 @ 9.50, B:e24 @ 10.40 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g71 | 2.15 | CRITICAL_TTC_START | B | U13 | B:e18 @ 9.90, B:e20 @ 10.25 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g72 | 2.20 | CLOSING_END | A | U12 | A:e55 @ 9.95 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g73 | 2.25 | CLOSING_END | A | U11 | A:e56 @ 10.00 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g74 | 2.25 | CRITICAL_TTC_START | B | U14 | B:e19 @ 10.00, B:e22 @ 10.30 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g75 | 2.50 | CRITICAL_TTC_END | B | U13 | B:e20 @ 10.25 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g76 | 2.50 | TRACK_LOST | B | U3 | B:e21 @ 10.25 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g77 | 2.55 | CRITICAL_TTC_END | B | U14 | B:e22 @ 10.30 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g78 | 2.55 | CLOSING_END | B | U13 | B:e23 @ 10.30 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g79 | 2.65 | CLOSING_END | B | U14 | B:e24 @ 10.40 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g80 | 2.90 | EGO_PATH_EXIT | B | U5 | B:e25 @ 10.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g81 | 3.10 | TRACK_LOST | A | U11 | A:e57 @ 10.85 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g82 | 3.10 | TRACK_LOST | A | U12 | A:e58 @ 10.85 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g83 | 3.15 | EGO_PATH_ENTRY | B | U7 | B:e26 @ 10.90 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |

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
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g37 --PRECEDES--> g44
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g38 --PRECEDES--> g44
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g39 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g41 --PRECEDES--> g46
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g53
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g54 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g55 --PRECEDES--> g60
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g56 --PRECEDES--> g60
    g57 --PRECEDES--> g61
    g57 --PRECEDES--> g62
    g58 --PRECEDES--> g61
    g58 --PRECEDES--> g62
    g59 --PRECEDES--> g61
    g59 --PRECEDES--> g62
    g60 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g62 --PRECEDES--> g63
    g63 --PRECEDES--> g64
    g64 --PRECEDES--> g65
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g66 --PRECEDES--> g68
    g67 --PRECEDES--> g69
    g67 --PRECEDES--> g70
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g69 --PRECEDES--> g71
    g70 --PRECEDES--> g71
    g71 --PRECEDES--> g72
    g72 --PRECEDES--> g73
    g72 --PRECEDES--> g74
    g73 --PRECEDES--> g75
    g73 --PRECEDES--> g76
    g74 --PRECEDES--> g75
    g74 --PRECEDES--> g76
    g75 --PRECEDES--> g77
    g75 --PRECEDES--> g78
    g76 --PRECEDES--> g77
    g76 --PRECEDES--> g78
    g77 --PRECEDES--> g79
    g78 --PRECEDES--> g79
    g79 --PRECEDES--> g80
    g80 --PRECEDES--> g81
    g80 --PRECEDES--> g82
    g81 --PRECEDES--> g83
    g82 --PRECEDES--> g83
    g09 --SAME_TRACK--> g12
    g05 --SAME_TRACK--> g13
    g14 --SAME_TRACK--> g15
    g17 --SAME_TRACK--> g18
    g09 --SAME_TRACK--> g20
    g21 --SAME_TRACK--> g22
    g14 --SAME_TRACK--> g23
    g24 --SAME_TRACK--> g25
    g24 --SAME_TRACK--> g26
    g21 --SAME_TRACK--> g27
    g21 --SAME_TRACK--> g28
    g05 --SAME_TRACK--> g29
    g10 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g31
    g21 --SAME_TRACK--> g32
    g21 --SAME_TRACK--> g33
    g21 --SAME_TRACK--> g34
    g24 --SAME_TRACK--> g38
    g17 --SAME_TRACK--> g39
    g24 --SAME_TRACK--> g44
    g45 --SAME_TRACK--> g46
    g45 --SAME_TRACK--> g47
    g21 --SAME_TRACK--> g48
    g21 --SAME_TRACK--> g49
    g35 --SAME_TRACK--> g52
    g36 --SAME_TRACK--> g51
    g21 --SAME_TRACK--> g54
    g57 --SAME_TRACK--> g59
    g58 --SAME_TRACK--> g60
    g17 --SAME_TRACK--> g63
    g53 --SAME_TRACK--> g64
    g45 --SAME_TRACK--> g65
    g58 --SAME_TRACK--> g72
    g57 --SAME_TRACK--> g73
    g57 --SAME_TRACK--> g81
    g58 --SAME_TRACK--> g82
    g06 --SAME_TRACK--> g19
    g06 --SAME_TRACK--> g50
    g67 --SAME_TRACK--> g68
    g69 --SAME_TRACK--> g70
    g67 --SAME_TRACK--> g71
    g69 --SAME_TRACK--> g74
    g67 --SAME_TRACK--> g75
    g16 --SAME_TRACK--> g76
    g69 --SAME_TRACK--> g77
    g67 --SAME_TRACK--> g78
    g69 --SAME_TRACK--> g79
    g06 --SAME_TRACK--> g80
    g11 --SAME_TRACK--> g83
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U5); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U6); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(B,U7); CLOSING_START(A,U1); CLOSING_START(A,U3) |
| -7.70 | TRACK_APPEARED_LEFT(A,U8); CLOSING_START(A,U8) |
| -7.65 | TRACK_APPEARED_LEFT(B,U3) |
| -7.40 | TRACK_APPEARED_LEFT(A,U6); CLOSING_START(A,U6) |
| -7.25 | CRITICAL_TTC_START(B,U5) |
| -7.00 | TRACK_LOST(A,U1) |
| -6.95 | TRACK_APPEARED_RIGHT(A,U7); CLOSING_START(A,U7) |
| -6.85 | TRACK_LOST(A,U8) |
| -6.80 | TRACK_APPEARED_FRONT(A,B); CLOSING_START(A,B) |
| -6.30 | CRITICAL_TTC_START(A,B) |
| -6.25 | CUT_IN_FROM_RIGHT_START(A,U7) |
| -6.00 | CUT_IN_FROM_RIGHT_END(A,U7) |
| -4.10 | TRACK_LOST(A,U3) |
| -2.10 | TRACK_LOST(A,U4) |
| -1.80 | TRACK_LOST(A,U2) |
| -0.80 | CUT_IN_FROM_RIGHT_START(A,U7) |
| -0.20 | CLOSING_END(A,U7) |
| -0.05 | CUT_IN_FROM_RIGHT_END(A,U7); TRACK_APPEARED_FRONT(A,U5); TRACK_APPEARED_LEFT(A,U3) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,U6); THROTTLE_END(B) |
| +0.05 | THROTTLE_END(A); BRAKE_START(A); BRAKE_START(B); TRACK_LOST(A,B) |
| +0.10 | TRACK_APPEARED_LEFT(A,U9); CLOSING_START(A,U9) |
| +0.40 | CLOSING_END(A,U9) |
| +0.45 | EGO_PATH_ENTRY(A,U7); CRITICAL_TTC_START(A,U7) |
| +0.50 | CRITICAL_TTC_END(B,U5) |
| +0.70 | TRACK_LOST(A,U3); TRACK_LOST(A,U5) |
| +0.80 | TRACK_APPEARED_RIGHT(A,U10) |
| +1.00 | TRACK_LOST(A,U7) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +1.20 | TRACK_APPEARED_LEFT(A,U11); TRACK_APPEARED_RIGHT(A,U12); CLOSING_START(A,U11); CLOSING_START(A,U12) |
| +1.25 | MOVING_END(B); STOP_START(B) |
| +1.30 | TRACK_LOST(A,U6) |
| +1.45 | TRACK_LOST(A,U10) |
| +1.50 | TRACK_LOST(A,U9) |
| +1.55 | TRACK_APPEARED_FRONT(A,B) |
| +1.65 | TRACK_APPEARED_LEFT(B,U13); CLOSING_START(B,U13) |
| +1.75 | TRACK_APPEARED_RIGHT(B,U14); CLOSING_START(B,U14) |
| +2.15 | CRITICAL_TTC_START(B,U13) |
| +2.20 | CLOSING_END(A,U12) |
| +2.25 | CLOSING_END(A,U11); CRITICAL_TTC_START(B,U14) |
| +2.50 | CRITICAL_TTC_END(B,U13); TRACK_LOST(B,U3) |
| +2.55 | CRITICAL_TTC_END(B,U14); CLOSING_END(B,U13) |
| +2.65 | CLOSING_END(B,U14) |
| +2.90 | EGO_PATH_EXIT(B,U5) |
| +3.10 | TRACK_LOST(A,U11); TRACK_LOST(A,U12) |
| +3.15 | EGO_PATH_ENTRY(B,U7) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001#segment_2 (unidentified U7): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 1.50 < CRITICAL_TTC_START 8.20 (+6.70 s); EGO_PATH_ENTRY 8.20 together with critical TTC (+0.00 s) [local times; t_global: cut_in -6.25, critical_ttc_start +0.45, ego_path_entry +0.45]
- A's track_005#segment_2 (B): CRITICAL_TTC_START 1.45, COLLISION with B 7.75 (+6.30 s) [local times; t_global: critical_ttc_start -6.30, collision +0.00]
- B's track_001 (unidentified U5): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_003 (unidentified U7): EGO_PATH_ENTRY 10.90, no critical TTC [local times; t_global: ego_path_entry +3.15]
- B's track_005 (unidentified U13): CRITICAL_TTC_START 9.90 [local times; t_global: critical_ttc_start +2.15]
- B's track_006 (unidentified U14): CRITICAL_TTC_START 10.00 [local times; t_global: critical_ttc_start +2.25]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U3) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,U2) (A:e04)<br>g09 TRACK_APPEARED_RIGHT(A,U1) (A:e05)<br>g10 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g12 CLOSING_START(A,U1) (A:e07)<br>g13 CLOSING_START(A,U3) (A:e08) | ego: not yet observed |
| -7.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U5) (B:e03)<br>g08 TRACK_APPEARED_LEFT(B,U6) (B:e04)<br>g11 TRACK_APPEARED_RIGHT(B,U7) (B:e05) | ego: not yet observed |
| -7.75 | A | g05 TRACK_APPEARED_FRONT(A,U3) (A:e03)<br>g29 TRACK_LOST(A,U3) (A:e22) | ego: not yet observed |
| -7.75 | A | g07 TRACK_APPEARED_LEFT(A,U2) (A:e04)<br>g31 TRACK_LOST(A,U2) (A:e24) | ego: not yet observed |
| -7.75 | A | g09 TRACK_APPEARED_RIGHT(A,U1) (A:e05)<br>g20 TRACK_LOST(A,U1) (A:e13) | ego: not yet observed |
| -7.75 | A | g10 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g30 TRACK_LOST(A,U4) (A:e23) | ego: not yet observed |
| -7.70 | A | g14 TRACK_APPEARED_LEFT(A,U8) (A:e09)<br>g15 CLOSING_START(A,U8) (A:e10) | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.70 | A | g14 TRACK_APPEARED_LEFT(A,U8) (A:e09)<br>g23 TRACK_LOST(A,U8) (A:e16) | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.65 | B | g16 TRACK_APPEARED_LEFT(B,U3) (B:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.65 | B | g16 TRACK_APPEARED_LEFT(B,U3) (B:e06)<br>g71 CRITICAL_TTC_START(B,U13) (B:e18)<br>g75 CRITICAL_TTC_END(B,U13) (B:e20)<br>g76 TRACK_LOST(B,U3) (B:e21) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.40 | A | g17 TRACK_APPEARED_LEFT(A,U6) (A:e11)<br>g18 CLOSING_START(A,U6) (A:e12) | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -7.40 | A | g17 TRACK_APPEARED_LEFT(A,U6) (A:e11)<br>g63 TRACK_LOST(A,U6) (A:e51) | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -7.40 | A | g18 CLOSING_START(A,U6) (A:e12)<br>g26 CRITICAL_TTC_START(A,B) (A:e19)<br>g37 COLLISION(A,B) (A:e30)<br>g38 CRITICAL_TTC_END(A,B) (A:e31)<br>g39 CLOSING_END(A,U6) (A:e32) | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -7.25 | B | g19 CRITICAL_TTC_START(B,U5) (B:e07) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.25 | B | g19 CRITICAL_TTC_START(B,U5) (B:e07)<br>g50 CRITICAL_TTC_END(B,U5) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -6.95 | A | g21 TRACK_APPEARED_RIGHT(A,U7) (A:e14)<br>g22 CLOSING_START(A,U7) (A:e15) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 |
| -6.95 | A | g21 TRACK_APPEARED_RIGHT(A,U7) (A:e14)<br>g54 TRACK_LOST(A,U7) (A:e44) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 |
| -6.95 | A | g22 CLOSING_START(A,U7) (A:e15)<br>g33 CLOSING_END(A,U7) (A:e26) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1 |
| -6.80 | A | g24 TRACK_APPEARED_FRONT(A,B) (A:e17)<br>g25 CLOSING_START(A,B) (A:e18) | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING, CRITICAL_TTC?<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 |
| -6.80 | A | g24 TRACK_APPEARED_FRONT(A,B) (A:e17)<br>g41 THROTTLE_END(A) (A:e33)<br>g42 BRAKE_START(A) (A:e34)<br>g44 TRACK_LOST(A,B) (A:e35) | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING, CRITICAL_TTC?<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 |
| -6.30 | A | g26 CRITICAL_TTC_START(A,B) (A:e19) | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 |
| -6.25 | A | g27 CUT_IN_FROM_RIGHT_START(A,U7) (A:e20) | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 |
| -6.25 | A | g27 CUT_IN_FROM_RIGHT_START(A,U7) (A:e20)<br>g28 CUT_IN_FROM_RIGHT_END(A,U7) (A:e21) | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_005#segment_1 |
| -0.80 | A | g32 CUT_IN_FROM_RIGHT_START(A,U7) (A:e25) | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 |
| -0.80 | A | g32 CUT_IN_FROM_RIGHT_START(A,U7) (A:e25)<br>g34 CUT_IN_FROM_RIGHT_END(A,U7) (A:e27)<br>g35 TRACK_APPEARED_FRONT(A,U5) (A:e28)<br>g36 TRACK_APPEARED_LEFT(A,U3) (A:e29) | ego: MOVING, THROTTLE<br>track_001#segment_2: CLOSING<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 |
| -0.05 | A | g35 TRACK_APPEARED_FRONT(A,U5) (A:e28)<br>g36 TRACK_APPEARED_LEFT(A,U3) (A:e29)<br>g51 TRACK_LOST(A,U3) (A:e42)<br>g52 TRACK_LOST(A,U5) (A:e41) | ego: MOVING, THROTTLE<br>track_001#segment_2: CUT_IN_FROM_RIGHT<br>track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1 |
| +0.00 | B | g37 COLLISION(A,B) (B:e08)<br>g40 THROTTLE_END(B) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +0.05 | B | g43 BRAKE_START(B) (B:e10) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +0.10 | A | g45 TRACK_APPEARED_LEFT(A,U9) (A:e36)<br>g46 CLOSING_START(A,U9) (A:e37) | ego: MOVING, BRAKE<br>track_001#segment_2: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 |
| +0.10 | A | g45 TRACK_APPEARED_LEFT(A,U9) (A:e36)<br>g65 TRACK_LOST(A,U9) (A:e53) | ego: MOVING, BRAKE<br>track_001#segment_2: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 |
| +0.10 | A | g46 CLOSING_START(A,U9) (A:e37)<br>g47 CLOSING_END(A,U9) (A:e38) | ego: MOVING, BRAKE<br>track_001#segment_2: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 |
| +0.45 | A | g48 EGO_PATH_ENTRY(A,U7) (A:e39)<br>g49 CRITICAL_TTC_START(A,U7) (A:e40) | ego: MOVING, BRAKE<br>track_001#segment_2: no active state<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2 |
| +0.80 | A | g53 TRACK_APPEARED_RIGHT(A,U10) (A:e43) | ego: MOVING, BRAKE<br>track_001#segment_2: CRITICAL_TTC, IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 |
| +0.80 | A | g53 TRACK_APPEARED_RIGHT(A,U10) (A:e43)<br>g64 TRACK_LOST(A,U10) (A:e52) | ego: MOVING, BRAKE<br>track_001#segment_2: CRITICAL_TTC, IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 |
| +1.15 | A | g55 MOVING_END(A) (A:e45)<br>g56 STOP_START(A) (A:e46) | ego: MOVING, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 |
| +1.20 | A | g57 TRACK_APPEARED_LEFT(A,U11) (A:e47)<br>g58 TRACK_APPEARED_RIGHT(A,U12) (A:e48)<br>g59 CLOSING_START(A,U11) (A:e49)<br>g60 CLOSING_START(A,U12) (A:e50) | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 |
| +1.20 | A | g57 TRACK_APPEARED_LEFT(A,U11) (A:e47)<br>g58 TRACK_APPEARED_RIGHT(A,U12) (A:e48)<br>g81 TRACK_LOST(A,U11) (A:e57)<br>g82 TRACK_LOST(A,U12) (A:e58) | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 |
| +1.20 | A | g59 CLOSING_START(A,U11) (A:e49)<br>g73 CLOSING_END(A,U11) (A:e56) | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 |
| +1.20 | A | g60 CLOSING_START(A,U12) (A:e50)<br>g72 CLOSING_END(A,U12) (A:e55) | ego: STOP, BRAKE<br>track_005#segment_3: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_007, track_008 |
| +1.25 | B | g61 MOVING_END(B) (B:e12)<br>g62 STOP_START(B) (B:e13) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +1.55 | A | g66 TRACK_APPEARED_FRONT(A,B) (A:e54) | ego: STOP, BRAKE<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005#segment_1, track_005#segment_2, track_005#segment_3, track_006, track_007, track_008, track_009 |
| +1.65 | B | g67 TRACK_APPEARED_LEFT(B,U13) (B:e14)<br>g68 CLOSING_START(B,U13) (B:e15) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +1.65 | B | g68 CLOSING_START(B,U13) (B:e15)<br>g74 CRITICAL_TTC_START(B,U14) (B:e19)<br>g77 CRITICAL_TTC_END(B,U14) (B:e22)<br>g78 CLOSING_END(B,U13) (B:e23) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +1.75 | B | g69 TRACK_APPEARED_RIGHT(B,U14) (B:e16)<br>g70 CLOSING_START(B,U14) (B:e17) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC? |
| +1.75 | B | g70 CLOSING_START(B,U14) (B:e17)<br>g79 CLOSING_END(B,U14) (B:e24) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC? |
| +2.15 | B | g71 CRITICAL_TTC_START(B,U13) (B:e18) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC? |
| +2.25 | B | g74 CRITICAL_TTC_START(B,U14) (B:e19) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING, CRITICAL_TTC? |
| +2.90 | B | g80 EGO_PATH_EXIT(B,U5) (B:e25) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_004 |
| +3.15 | B | g83 EGO_PATH_ENTRY(B,U7) (B:e26) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_004 |

## Plain-language reading

- 7.75 s before the reference collision, A started moving (already the case when first observed).
- 7.75 s before the reference collision, B started moving (already the case when first observed).
- 7.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared in front of it.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 7.75 s before the reference collision, A observed anonymous road user U1 start closing in (already the case when first observed).
- 7.75 s before the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
- 7.70 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared on its left.
- 7.70 s before the reference collision, A observed anonymous road user U8 start closing in (already the case when first observed).
- 7.65 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its left.
- 7.40 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared on its left.
- 7.40 s before the reference collision, A observed anonymous road user U6 start closing in (already the case when first observed).
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U5 became critical.
- 7.00 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 6.95 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared on its right.
- 6.95 s before the reference collision, A observed anonymous road user U7 start closing in (already the case when first observed).
- 6.85 s before the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 6.80 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 6.80 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.30 s before the reference collision, A's time-to-contact with B became critical.
- 6.25 s before the reference collision, A observed anonymous road user U7 cutting in from the right.
- 6.00 s before the reference collision, A observed anonymous road user U7's cut-in from the right settle.
- 4.10 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.10 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 1.80 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 0.80 s before the reference collision, A observed anonymous road user U7 cutting in from the right.
- 0.20 s before the reference collision, A observed anonymous road user U7 stop closing in.
- 0.05 s before the reference collision, A observed anonymous road user U7's cut-in from the right settle.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared in front of it.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1898, B: 1898 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed anonymous road user U6 stop closing in.
- At the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.10 s after the reference collision, A's radar started tracking anonymous road user U9, which appeared on its left.
- 0.10 s after the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 0.40 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 0.45 s after the reference collision, A observed anonymous road user U7 enter its forward path corridor.
- 0.45 s after the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 0.50 s after the reference collision, B's time-to-contact with anonymous road user U5 stopped being critical.
- 0.70 s after the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 1.00 s after the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.20 s after the reference collision, A's radar started tracking anonymous road user U11, which appeared on its left.
- 1.20 s after the reference collision, A's radar started tracking anonymous road user U12, which appeared on its right.
- 1.20 s after the reference collision, A observed anonymous road user U11 start closing in (already the case when first observed).
- 1.20 s after the reference collision, A observed anonymous road user U12 start closing in (already the case when first observed).
- 1.25 s after the reference collision, B stopped moving.
- 1.25 s after the reference collision, B came to a stop.
- 1.30 s after the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.45 s after the reference collision, A's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 1.50 s after the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 1.55 s after the reference collision, A's radar started tracking B, which appeared in front of it.
- 1.65 s after the reference collision, B's radar started tracking anonymous road user U13, which appeared on its left.
- 1.65 s after the reference collision, B observed anonymous road user U13 start closing in (already the case when first observed).
- 1.75 s after the reference collision, B's radar started tracking anonymous road user U14, which appeared on its right.
- 1.75 s after the reference collision, B observed anonymous road user U14 start closing in (already the case when first observed).
- 2.15 s after the reference collision, B's time-to-contact with anonymous road user U13 became critical.
- 2.20 s after the reference collision, A observed anonymous road user U12 stop closing in.
- 2.25 s after the reference collision, A observed anonymous road user U11 stop closing in.
- 2.25 s after the reference collision, B's time-to-contact with anonymous road user U14 became critical.
- 2.50 s after the reference collision, B's time-to-contact with anonymous road user U13 stopped being critical.
- 2.50 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.55 s after the reference collision, B's time-to-contact with anonymous road user U14 stopped being critical.
- 2.55 s after the reference collision, B observed anonymous road user U13 stop closing in.
- 2.65 s after the reference collision, B observed anonymous road user U14 stop closing in.
- 2.90 s after the reference collision, B observed anonymous road user U5 leave its forward path corridor.
- 3.10 s after the reference collision, A's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 3.10 s after the reference collision, A's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 3.15 s after the reference collision, B observed anonymous road user U7 enter its forward path corridor.
