# Global graph - S19/run_0

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_004 |
| U1 | anonymous_road_user | anonymous; observed by A as A:track_001#segment_1 |
| U8 | anonymous_road_user | anonymous; observed by A, B as A:track_001#segment_2, B:track_006 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_002 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_007 |
| U7 | anonymous_road_user | anonymous; observed by A, B as A:track_005#segment_1, A:track_008, B:track_005 |
| U9 | anonymous_road_user | anonymous; observed by A as A:track_005#segment_2 |
| U4 | anonymous_road_user | anonymous; observed by A, B as A:track_005#segment_3, B:track_001 |
| U12 | anonymous_road_user | anonymous; observed by A as A:track_006 |
| U10 | anonymous_road_user | anonymous; observed by A, B as A:track_007, B:track_008 |
| U11 | anonymous_road_user | anonymous; observed by A, B as A:track_009, B:track_009 |
| U14 | anonymous_road_user | anonymous; observed by A as A:track_010 |
| U5 | anonymous_road_user | anonymous; observed by B as B:track_003 |
| U6 | anonymous_road_user | anonymous; observed by B as B:track_004 |
| U13 | anonymous_road_user | anonymous; observed by B as B:track_010 |
| U15 | anonymous_road_user | anonymous; observed by B as B:track_011 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e22 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e19 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 255.03 vs 255.03 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 7.05 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 10.9 m -> 11.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001#segment_1 |
| A:track_001#segment_2 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 11.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.54 m/s over 3.0 s<br>clearance at the contact 11.07 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001#segment_2, track_004, track_005#segment_2, track_006)<br>anonymous road user U8: B:track_006, A:track_001#segment_2 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 5.45 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 41.4 m -> 41.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_002 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 5.30 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 41.9 m -> 42.0 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_007 |
| A:track_004 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.38 m/s over 3.0 s<br>clearance at the contact 0.13 m<br>the only compatible track of A touching it at the contact (clearance 0.13 m; track_001#segment_2, track_005#segment_2, track_006 at 11.07 m, 10.52 m, 41.98 m) |
| A:track_005#segment_1 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 1.50 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 11.0 m -> 10.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.47 m/s over 1.5 s<br>anonymous road user U7: A:track_005#segment_1, B:track_005, A:track_008 |
| A:track_005#segment_2 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.45 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.6 m -> 10.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.55 m/s over 1.5 s<br>clearance at the contact 10.17 m (beyond 3.50 m: confidence factor 0.08)<br>anonymous road user U9: A:track_005#segment_2 |
| A:track_005#segment_3 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U4: B:track_001, A:track_005#segment_3 |
| A:track_006 | U12 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.20 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.1 m -> 42.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.62 m/s over 1.2 s<br>clearance at the contact 41.88 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001#segment_2, track_004, track_005#segment_2, track_006)<br>anonymous road user U12: A:track_006 |
| A:track_007 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.35 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.3 m -> 26.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.60 m/s over 0.3 s<br>clearance at the contact 26.21 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U10: B:track_008, A:track_007 |
| A:track_008 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U7: A:track_005#segment_1, B:track_005, A:track_008 |
| A:track_009 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U11: B:track_009, A:track_009 |
| A:track_010 | U14 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U14: A:track_010 |
| B:track_001 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.5 m -> 9.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.03 m/s over 3.0 s<br>clearance at the contact 9.92 m (beyond 3.50 m: confidence factor 0.10)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U4: B:track_001, A:track_005#segment_3 |
| B:track_002 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.76 m/s over 3.0 s<br>clearance at the contact 0.71 m<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma, over 240 samples; 94% within 3 sigma) at A's own velocity (median difference 0.20 m/s) |
| B:track_003 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.7 m -> 28.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U5: B:track_003 |
| B:track_004 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 3.95 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.4 m -> 28.0 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_004 |
| B:track_005 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.5 m -> 11.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 3.0 s<br>clearance at the contact 11.10 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U7: A:track_005#segment_1, B:track_005, A:track_008 |
| B:track_006 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 10.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.07 m/s over 3.0 s<br>clearance at the contact 10.56 m (beyond 3.50 m: confidence factor 0.06)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U8: B:track_006, A:track_001#segment_2 |
| B:track_007 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 5.55 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 44.6 m -> 44.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_007 |
| B:track_008 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 1.4 s<br>clearance at the contact 26.21 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U10: B:track_008, A:track_007 |
| B:track_009 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.3 s<br>clearance at the contact 26.68 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U11: B:track_009, A:track_009 |
| B:track_010 | U13 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.5 m -> 41.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.2 s<br>clearance at the contact 41.94 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U13: B:track_010 |
| B:track_011 | U15 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.60 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U15: B:track_011 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.75 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.75 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.75 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.75 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -7.75 | TRACK_APPEARED_FRONT | A | U2 | A:e03 @ 0.00, A:e11 @ 2.30 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -7.75 | TRACK_APPEARED_FRONT | B | U4 | B:e03 @ 0.00 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g07 | -7.75 | TRACK_APPEARED_LEFT | A | B | A:e06 @ 0.00 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g08 | -7.75 | TRACK_APPEARED_LEFT | A | U1 | A:e04 @ 0.00, A:e09 @ 0.70 | initial_in_ego_path=False; source_track=track_001#segment_1; aggregation=entity_state_union; source_tracks=['A:track_001#segment_1'] |
| g09 | -7.75 | TRACK_APPEARED_LEFT | A | U3 | A:e05 @ 0.00, A:e12 @ 2.45 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g10 | -7.75 | TRACK_APPEARED_LEFT | B | U5 | B:e04 @ 0.00, B:e12 @ 3.65 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g11 | -7.75 | TRACK_APPEARED_RIGHT | B | A | B:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g12 | -7.75 | TRACK_APPEARED_RIGHT | B | U6 | B:e06 @ 0.00, B:e13 @ 3.80 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g13 | -7.70 | TRACK_APPEARED_FRONT | A | U7 | A:e07 @ 0.05, A:e13 @ 6.25 | initial_in_ego_path=True; source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g14 | -7.70 | TRACK_APPEARED_FRONT | B | U3 | B:e07 @ 0.05, B:e11 @ 2.20 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g15 | -7.70 | TRACK_APPEARED_LEFT | B | U8 | B:e08 @ 0.05 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g16 | -7.70 | TRACK_APPEARED_RIGHT | B | U7 | B:e09 @ 0.05 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g17 | -7.25 | CRITICAL_TTC_START | B | U4 | B:e10 @ 0.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g18 | -7.20 | CRITICAL_TTC_START | A | U7 | A:e08 @ 0.55 | source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g19 | -7.05 | TRACK_LOST | A | U1 | A:e09 @ 0.70 | source_track=track_001#segment_1; aggregation=entity_state_union; source_tracks=['A:track_001#segment_1'] |
| g20 | -7.00 | TRACK_APPEARED_LEFT | A | U8 | A:e10 @ 0.75 | initial_in_ego_path=False; source_track=track_001#segment_2; aggregation=entity_state_union; source_tracks=['A:track_001#segment_2'] |
| g21 | -5.55 | TRACK_LOST | B | U3 | B:e11 @ 2.20 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g22 | -5.45 | TRACK_LOST | A | U2 | A:e11 @ 2.30 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g23 | -5.30 | TRACK_LOST | A | U3 | A:e12 @ 2.45 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g24 | -4.10 | TRACK_LOST | B | U5 | B:e12 @ 3.65 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g25 | -3.95 | TRACK_LOST | B | U6 | B:e13 @ 3.80 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g26 | -1.50 | TRACK_LOST | A | U7 | A:e13 @ 6.25 | source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g27 | -1.45 | TRACK_APPEARED_FRONT | A | U9 | A:e14 @ 6.30, A:e28 @ 8.25 | initial_in_ego_path=False; source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g28 | -1.40 | TRACK_APPEARED_RIGHT | B | U10 | B:e14 @ 6.35, B:e25 @ 8.85 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g29 | -1.40 | CRITICAL_TTC_START | A | B | A:e15 @ 6.35, A:e23 @ 7.75 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g30 | -1.35 | TRACK_APPEARED_LEFT | B | U11 | B:e15 @ 6.40, B:e28 @ 9.35 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g31 | -1.20 | TRACK_APPEARED_FRONT | A | U12 | A:e16 @ 6.55, A:e21 @ 7.70 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g32 | -1.15 | TRACK_APPEARED_FRONT | B | U13 | B:e16 @ 6.60 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g33 | -1.10 | EGO_PATH_ENTRY | A | U12 | A:e17 @ 6.65, A:e20 @ 7.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g34 | -0.80 | CLOSING_START | A | B | A:e18 @ 6.95, A:e27 @ 7.90 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g35 | -0.75 | CRITICAL_TTC_START | B | A | B:e17 @ 7.00, B:e20 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g36 | -0.70 | CLOSING_START | B | A | B:e18 @ 7.05, B:e21 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g37 | -0.35 | TRACK_APPEARED_RIGHT | A | U10 | A:e19 @ 7.40 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g38 | -0.20 | EGO_PATH_EXIT | A | U12 | A:e20 @ 7.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g39 | -0.05 | TRACK_LOST | A | U12 | A:e21 @ 7.70 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g40 | 0.00 | COLLISION | - | A, B | A:e22 @ 7.75, B:e19 @ 7.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 255.03, B 255.03 |
| g41 | 0.00 | CRITICAL_TTC_END | A | B | A:e23 @ 7.75 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g42 | 0.00 | CRITICAL_TTC_END | B | A | B:e20 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g43 | 0.00 | CLOSING_END | B | A | B:e21 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g44 | 0.05 | THROTTLE_END | A | - | A:e24 @ 7.80 |  |
| g45 | 0.05 | THROTTLE_END | B | - | B:e22 @ 7.80 |  |
| g46 | 0.10 | TRACK_APPEARED_FRONT | A | U7 | A:e25 @ 7.85 | initial_in_ego_path=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g47 | 0.10 | EGO_PATH_ENTRY | A | B | A:e26 @ 7.85 | geometry=estimated_body; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g48 | 0.10 | EGO_PATH_ENTRY | B | U13 | B:e23 @ 7.85, B:e29 @ 9.60 | geometry=estimated_body; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g49 | 0.15 | CLOSING_END | A | B | A:e27 @ 7.90 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g50 | 0.25 | EGO_PATH_ENTRY | B | U11 | B:e24 @ 8.00 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g51 | 0.50 | TRACK_LOST | A | U9 | A:e28 @ 8.25 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g52 | 0.55 | TRACK_APPEARED_FRONT | A | U4 | A:e29 @ 8.30 | initial_in_ego_path=True; source_track=track_005#segment_3; aggregation=entity_state_union; source_tracks=['A:track_005#segment_3'] |
| g53 | 0.60 | CRITICAL_TTC_START | A | U7 | A:e30 @ 8.35, A:e33 @ 8.95 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g54 | 0.70 | TRACK_APPEARED_LEFT | A | U11 | A:e31 @ 8.45 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g55 | 1.05 | CRITICAL_TTC_START | A | U4 | A:e32 @ 8.80 | source_track=track_005#segment_3; aggregation=entity_state_union; source_tracks=['A:track_005#segment_3'] |
| g56 | 1.10 | TRACK_LOST | B | U10 | B:e25 @ 8.85 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g57 | 1.20 | CRITICAL_TTC_END | A | U7 | A:e33 @ 8.95 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g58 | 1.20 | EGO_PATH_EXIT | A | U7 | A:e34 @ 8.95 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g59 | 1.35 | EGO_PATH_ENTRY | A | U10 | A:e35 @ 9.10, A:e41 @ 11.55 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g60 | 1.45 | EGO_PATH_ENTRY | B | U8 | B:e26 @ 9.20, B:e32 @ 10.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g61 | 1.45 | CRITICAL_TTC_START | B | U8 | B:e27 @ 9.20, B:e31 @ 10.55 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g62 | 1.60 | TRACK_LOST | B | U11 | B:e28 @ 9.35 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g63 | 1.75 | TRACK_APPEARED_LEFT | A | U14 | A:e36 @ 9.50, A:e40 @ 11.15 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g64 | 1.85 | EGO_PATH_EXIT | B | U13 | B:e29 @ 9.60 | geometry=estimated_body; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g65 | 1.85 | CUT_IN_FROM_RIGHT_START | B | U7 | B:e30 @ 9.60 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g66 | 2.00 | CRITICAL_TTC_START | A | U7 | A:e37 @ 9.75 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g67 | 2.50 | EGO_PATH_ENTRY | A | U7 | A:e38 @ 10.25 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g68 | 2.70 | CUT_IN_FROM_RIGHT_START | A | U7 | A:e39 @ 10.45 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g69 | 2.80 | CRITICAL_TTC_END | B | U8 | B:e31 @ 10.55 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g70 | 2.80 | EGO_PATH_EXIT | B | U8 | B:e32 @ 10.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g71 | 2.95 | CRITICAL_TTC_START | B | U7 | B:e33 @ 10.70 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g72 | 3.40 | EGO_PATH_ENTRY | B | U7 | B:e34 @ 11.15 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g73 | 3.40 | TRACK_LOST | A | U14 | A:e40 @ 11.15 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g74 | 3.60 | TRACK_APPEARED_LEFT | B | U15 | B:e35 @ 11.35, B:e36 @ 11.65 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g75 | 3.80 | EGO_PATH_EXIT | A | U10 | A:e41 @ 11.55 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g76 | 3.85 | EGO_PATH_EXIT | A | U4 | A:e42 @ 11.60 | geometry=estimated_body; source_track=track_005#segment_3; aggregation=entity_state_union; source_tracks=['A:track_005#segment_3'] |
| g77 | 3.90 | TRACK_LOST | B | U15 | B:e36 @ 11.65 | source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |

## Edges

```
    g01 --PRECEDES--> g13
    g01 --PRECEDES--> g14
    g01 --PRECEDES--> g15
    g01 --PRECEDES--> g16
    g02 --PRECEDES--> g13
    g02 --PRECEDES--> g14
    g02 --PRECEDES--> g15
    g02 --PRECEDES--> g16
    g03 --PRECEDES--> g13
    g03 --PRECEDES--> g14
    g03 --PRECEDES--> g15
    g03 --PRECEDES--> g16
    g04 --PRECEDES--> g13
    g04 --PRECEDES--> g14
    g04 --PRECEDES--> g15
    g04 --PRECEDES--> g16
    g05 --PRECEDES--> g13
    g05 --PRECEDES--> g14
    g05 --PRECEDES--> g15
    g05 --PRECEDES--> g16
    g06 --PRECEDES--> g13
    g06 --PRECEDES--> g14
    g06 --PRECEDES--> g15
    g06 --PRECEDES--> g16
    g07 --PRECEDES--> g13
    g07 --PRECEDES--> g14
    g07 --PRECEDES--> g15
    g07 --PRECEDES--> g16
    g08 --PRECEDES--> g13
    g08 --PRECEDES--> g14
    g08 --PRECEDES--> g15
    g08 --PRECEDES--> g16
    g09 --PRECEDES--> g13
    g09 --PRECEDES--> g14
    g09 --PRECEDES--> g15
    g09 --PRECEDES--> g16
    g10 --PRECEDES--> g13
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g10 --PRECEDES--> g16
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g11 --PRECEDES--> g16
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g17
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
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g39 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g40 --PRECEDES--> g45
    g41 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g51 --PRECEDES--> g52
    g52 --PRECEDES--> g53
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g62
    g62 --PRECEDES--> g63
    g63 --PRECEDES--> g64
    g63 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g69 --PRECEDES--> g71
    g70 --PRECEDES--> g71
    g71 --PRECEDES--> g72
    g71 --PRECEDES--> g73
    g72 --PRECEDES--> g74
    g73 --PRECEDES--> g74
    g74 --PRECEDES--> g75
    g75 --PRECEDES--> g76
    g76 --PRECEDES--> g77
    g13 --SAME_TRACK--> g18
    g08 --SAME_TRACK--> g19
    g05 --SAME_TRACK--> g22
    g09 --SAME_TRACK--> g23
    g13 --SAME_TRACK--> g26
    g07 --SAME_TRACK--> g29
    g31 --SAME_TRACK--> g33
    g07 --SAME_TRACK--> g34
    g31 --SAME_TRACK--> g38
    g31 --SAME_TRACK--> g39
    g07 --SAME_TRACK--> g41
    g07 --SAME_TRACK--> g47
    g07 --SAME_TRACK--> g49
    g27 --SAME_TRACK--> g51
    g46 --SAME_TRACK--> g53
    g52 --SAME_TRACK--> g55
    g46 --SAME_TRACK--> g57
    g46 --SAME_TRACK--> g58
    g37 --SAME_TRACK--> g59
    g46 --SAME_TRACK--> g66
    g46 --SAME_TRACK--> g67
    g46 --SAME_TRACK--> g68
    g63 --SAME_TRACK--> g73
    g37 --SAME_TRACK--> g75
    g52 --SAME_TRACK--> g76
    g06 --SAME_TRACK--> g17
    g14 --SAME_TRACK--> g21
    g10 --SAME_TRACK--> g24
    g12 --SAME_TRACK--> g25
    g11 --SAME_TRACK--> g35
    g11 --SAME_TRACK--> g36
    g11 --SAME_TRACK--> g42
    g11 --SAME_TRACK--> g43
    g32 --SAME_TRACK--> g48
    g30 --SAME_TRACK--> g50
    g28 --SAME_TRACK--> g56
    g15 --SAME_TRACK--> g60
    g15 --SAME_TRACK--> g61
    g30 --SAME_TRACK--> g62
    g32 --SAME_TRACK--> g64
    g16 --SAME_TRACK--> g65
    g15 --SAME_TRACK--> g69
    g15 --SAME_TRACK--> g70
    g16 --SAME_TRACK--> g71
    g16 --SAME_TRACK--> g72
    g74 --SAME_TRACK--> g77
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_FRONT(B,U4); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U3); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U6) |
| -7.70 | TRACK_APPEARED_FRONT(A,U7); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(B,U8); TRACK_APPEARED_RIGHT(B,U7) |
| -7.25 | CRITICAL_TTC_START(B,U4) |
| -7.20 | CRITICAL_TTC_START(A,U7) |
| -7.05 | TRACK_LOST(A,U1) |
| -7.00 | TRACK_APPEARED_LEFT(A,U8) |
| -5.55 | TRACK_LOST(B,U3) |
| -5.45 | TRACK_LOST(A,U2) |
| -5.30 | TRACK_LOST(A,U3) |
| -4.10 | TRACK_LOST(B,U5) |
| -3.95 | TRACK_LOST(B,U6) |
| -1.50 | TRACK_LOST(A,U7) |
| -1.45 | TRACK_APPEARED_FRONT(A,U9) |
| -1.40 | TRACK_APPEARED_RIGHT(B,U10); CRITICAL_TTC_START(A,B) |
| -1.35 | TRACK_APPEARED_LEFT(B,U11) |
| -1.20 | TRACK_APPEARED_FRONT(A,U12) |
| -1.15 | TRACK_APPEARED_FRONT(B,U13) |
| -1.10 | EGO_PATH_ENTRY(A,U12) |
| -0.80 | CLOSING_START(A,B) |
| -0.75 | CRITICAL_TTC_START(B,A) |
| -0.70 | CLOSING_START(B,A) |
| -0.35 | TRACK_APPEARED_RIGHT(A,U10) |
| -0.20 | EGO_PATH_EXIT(A,U12) |
| -0.05 | TRACK_LOST(A,U12) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B) |
| +0.10 | TRACK_APPEARED_FRONT(A,U7); EGO_PATH_ENTRY(A,B); EGO_PATH_ENTRY(B,U13) |
| +0.15 | CLOSING_END(A,B) |
| +0.25 | EGO_PATH_ENTRY(B,U11) |
| +0.50 | TRACK_LOST(A,U9) |
| +0.55 | TRACK_APPEARED_FRONT(A,U4) |
| +0.60 | CRITICAL_TTC_START(A,U7) |
| +0.70 | TRACK_APPEARED_LEFT(A,U11) |
| +1.05 | CRITICAL_TTC_START(A,U4) |
| +1.10 | TRACK_LOST(B,U10) |
| +1.20 | CRITICAL_TTC_END(A,U7); EGO_PATH_EXIT(A,U7) |
| +1.35 | EGO_PATH_ENTRY(A,U10) |
| +1.45 | EGO_PATH_ENTRY(B,U8); CRITICAL_TTC_START(B,U8) |
| +1.60 | TRACK_LOST(B,U11) |
| +1.75 | TRACK_APPEARED_LEFT(A,U14) |
| +1.85 | EGO_PATH_EXIT(B,U13); CUT_IN_FROM_RIGHT_START(B,U7) |
| +2.00 | CRITICAL_TTC_START(A,U7) |
| +2.50 | EGO_PATH_ENTRY(A,U7) |
| +2.70 | CUT_IN_FROM_RIGHT_START(A,U7) |
| +2.80 | CRITICAL_TTC_END(B,U8); EGO_PATH_EXIT(B,U8) |
| +2.95 | CRITICAL_TTC_START(B,U7) |
| +3.40 | EGO_PATH_ENTRY(B,U7); TRACK_LOST(A,U14) |
| +3.60 | TRACK_APPEARED_LEFT(B,U15) |
| +3.80 | EGO_PATH_EXIT(A,U10) |
| +3.85 | EGO_PATH_EXIT(A,U4) |
| +3.90 | TRACK_LOST(B,U15) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_004 (B): CRITICAL_TTC_START 6.35, COLLISION with B 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -1.40, ego_path_entry +0.10, collision +0.00]
- A's track_005#segment_1 (unidentified U7): CRITICAL_TTC_START 0.55, COLLISION 7.75 (+7.20 s) [local times; t_global: critical_ttc_start -7.20, collision +0.00]
- A's track_005#segment_3 (unidentified U4): CRITICAL_TTC_START 8.80 [local times; t_global: critical_ttc_start +1.05]
- A's track_006 (unidentified U12): EGO_PATH_ENTRY 6.65, no critical TTC [local times; t_global: ego_path_entry -1.10, collision +0.00]
- A's track_007 (unidentified U10): EGO_PATH_ENTRY 9.10, no critical TTC [local times; t_global: ego_path_entry +1.35]
- A's track_008 (unidentified U7): critical TTC already active before the cut-in: CRITICAL_TTC_START 9.75 <= CUT_IN_FROM_RIGHT_START 10.45 (+0.70 s); EGO_PATH_ENTRY 10.25 after critical TTC (+0.50 s) [local times; t_global: cut_in +2.70, critical_ttc_start +2.00, ego_path_entry +2.50]
- B's track_001 (unidentified U4): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.00, COLLISION with A 7.75 (+0.75 s) [local times; t_global: critical_ttc_start -0.75, collision +0.00]
- B's track_005 (unidentified U7): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 9.60 < CRITICAL_TTC_START 10.70 (+1.10 s); EGO_PATH_ENTRY 11.15 after critical TTC (+0.45 s) [local times; t_global: cut_in +1.85, critical_ttc_start +2.95, ego_path_entry +3.40]
- B's track_006 (unidentified U8): CRITICAL_TTC_START 9.20; EGO_PATH_ENTRY 9.20 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start +1.45, ego_path_entry +1.45]
- B's track_009 (unidentified U11): EGO_PATH_ENTRY 8.00, no critical TTC [local times; t_global: ego_path_entry +0.25]
- B's track_010 (unidentified U13): EGO_PATH_ENTRY 7.85, no critical TTC [local times; t_global: ego_path_entry +0.10]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U2) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,B) (A:e06)<br>g08 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g09 TRACK_APPEARED_LEFT(A,U3) (A:e05) | ego: not yet observed |
| -7.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U4) (B:e03)<br>g10 TRACK_APPEARED_LEFT(B,U5) (B:e04)<br>g11 TRACK_APPEARED_RIGHT(B,A) (B:e05)<br>g12 TRACK_APPEARED_RIGHT(B,U6) (B:e06) | ego: not yet observed |
| -7.75 | A | g05 TRACK_APPEARED_FRONT(A,U2) (A:e03)<br>g22 TRACK_LOST(A,U2) (A:e11) | ego: not yet observed |
| -7.75 | A | g08 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g19 TRACK_LOST(A,U1) (A:e09) | ego: not yet observed |
| -7.75 | A | g09 TRACK_APPEARED_LEFT(A,U3) (A:e05)<br>g23 TRACK_LOST(A,U3) (A:e12) | ego: not yet observed |
| -7.75 | B | g10 TRACK_APPEARED_LEFT(B,U5) (B:e04)<br>g24 TRACK_LOST(B,U5) (B:e12) | ego: not yet observed |
| -7.75 | B | g12 TRACK_APPEARED_RIGHT(B,U6) (B:e06)<br>g25 TRACK_LOST(B,U6) (B:e13) | ego: not yet observed |
| -7.70 | A | g13 TRACK_APPEARED_FRONT(A,U7) (A:e07) | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.70 | A | g13 TRACK_APPEARED_FRONT(A,U7) (A:e07)<br>g26 TRACK_LOST(A,U7) (A:e13) | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.70 | B | g14 TRACK_APPEARED_FRONT(B,U3) (B:e07)<br>g15 TRACK_APPEARED_LEFT(B,U8) (B:e08)<br>g16 TRACK_APPEARED_RIGHT(B,U7) (B:e09) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.70 | B | g14 TRACK_APPEARED_FRONT(B,U3) (B:e07)<br>g21 TRACK_LOST(B,U3) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.25 | B | g17 CRITICAL_TTC_START(B,U4) (B:e10) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? |
| -7.20 | A | g18 CRITICAL_TTC_START(A,U7) (A:e08) | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005#segment_1: IN_EGO_PATH, CRITICAL_TTC? |
| -7.00 | A | g20 TRACK_APPEARED_LEFT(A,U8) (A:e10) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005#segment_1: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 |
| -1.45 | A | g27 TRACK_APPEARED_FRONT(A,U9) (A:e14) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -1.45 | A | g27 TRACK_APPEARED_FRONT(A,U9) (A:e14)<br>g51 TRACK_LOST(A,U9) (A:e28) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -1.40 | B | g28 TRACK_APPEARED_RIGHT(B,U10) (B:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -1.40 | B | g28 TRACK_APPEARED_RIGHT(B,U10) (B:e14)<br>g56 TRACK_LOST(B,U10) (B:e25) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -1.40 | A | g29 CRITICAL_TTC_START(A,B) (A:e15) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: no active state<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -1.40 | A | g29 CRITICAL_TTC_START(A,B) (A:e15)<br>g40 COLLISION(A,B) (A:e22)<br>g41 CRITICAL_TTC_END(A,B) (A:e23) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: no active state<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -1.35 | B | g30 TRACK_APPEARED_LEFT(B,U11) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -1.35 | B | g30 TRACK_APPEARED_LEFT(B,U11) (B:e15)<br>g62 TRACK_LOST(B,U11) (B:e28) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -1.20 | A | g31 TRACK_APPEARED_FRONT(A,U12) (A:e16) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -1.20 | A | g31 TRACK_APPEARED_FRONT(A,U12) (A:e16)<br>g39 TRACK_LOST(A,U12) (A:e21) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -1.15 | B | g32 TRACK_APPEARED_FRONT(B,U13) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -1.10 | A | g33 EGO_PATH_ENTRY(A,U12) (A:e17) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -1.10 | A | g33 EGO_PATH_ENTRY(A,U12) (A:e17)<br>g38 EGO_PATH_EXIT(A,U12) (A:e20) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -0.80 | A | g34 CLOSING_START(A,B) (A:e18) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -0.80 | A | g34 CLOSING_START(A,B) (A:e18)<br>g49 CLOSING_END(A,B) (A:e27) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| -0.75 | B | g35 CRITICAL_TTC_START(B,A) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -0.75 | B | g35 CRITICAL_TTC_START(B,A) (B:e17)<br>g36 CLOSING_START(B,A) (B:e18)<br>g40 COLLISION(A,B) (B:e19)<br>g42 CRITICAL_TTC_END(B,A) (B:e20)<br>g43 CLOSING_END(B,A) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -0.70 | B | g36 CLOSING_START(B,A) (B:e18) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| -0.35 | A | g37 TRACK_APPEARED_RIGHT(A,U10) (A:e19) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1 |
| +0.05 | A | g44 THROTTLE_END(A) (A:e24) | ego: MOVING, THROTTLE<br>track_001#segment_2: no active state<br>track_004: CLOSING<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006 |
| +0.05 | B | g45 THROTTLE_END(B) (B:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| +0.10 | A | g46 TRACK_APPEARED_FRONT(A,U7) (A:e25)<br>g47 EGO_PATH_ENTRY(A,B) (A:e26) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: CLOSING<br>track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006 |
| +0.10 | B | g48 EGO_PATH_ENTRY(B,U13) (B:e23) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| +0.10 | B | g48 EGO_PATH_ENTRY(B,U13) (B:e23)<br>g64 EGO_PATH_EXIT(B,U13) (B:e29)<br>g65 CUT_IN_FROM_RIGHT_START(B,U7) (B:e30) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| +0.25 | B | g50 EGO_PATH_ENTRY(B,U11) (B:e24) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007 |
| +0.55 | A | g52 TRACK_APPEARED_FRONT(A,U4) (A:e29) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +0.60 | A | g53 CRITICAL_TTC_START(A,U7) (A:e30) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +0.60 | A | g53 CRITICAL_TTC_START(A,U7) (A:e30)<br>g57 CRITICAL_TTC_END(A,U7) (A:e33)<br>g58 EGO_PATH_EXIT(A,U7) (A:e34) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +0.70 | A | g54 TRACK_APPEARED_LEFT(A,U11) (A:e31) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +1.05 | A | g55 CRITICAL_TTC_START(A,U4) (A:e32) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +1.35 | A | g59 EGO_PATH_ENTRY(A,U10) (A:e35) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +1.35 | A | g59 EGO_PATH_ENTRY(A,U10) (A:e35)<br>g75 EGO_PATH_EXIT(A,U10) (A:e41) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +1.45 | B | g60 EGO_PATH_ENTRY(B,U8) (B:e26)<br>g61 CRITICAL_TTC_START(B,U8) (B:e27) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: IN_EGO_PATH<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008 |
| +1.45 | B | g60 EGO_PATH_ENTRY(B,U8) (B:e26)<br>g61 CRITICAL_TTC_START(B,U8) (B:e27)<br>g69 CRITICAL_TTC_END(B,U8) (B:e31)<br>g70 EGO_PATH_EXIT(B,U8) (B:e32) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: IN_EGO_PATH<br>track_010: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008 |
| +1.75 | A | g63 TRACK_APPEARED_LEFT(A,U14) (A:e36) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +1.75 | A | g63 TRACK_APPEARED_LEFT(A,U14) (A:e36)<br>g73 TRACK_LOST(A,U14) (A:e40) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +2.00 | A | g66 CRITICAL_TTC_START(A,U7) (A:e37) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +2.50 | A | g67 EGO_PATH_ENTRY(A,U7) (A:e38) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +2.70 | A | g68 CUT_IN_FROM_RIGHT_START(A,U7) (A:e39) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| +2.95 | B | g71 CRITICAL_TTC_START(B,U7) (B:e33) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 |
| +3.40 | B | g72 EGO_PATH_ENTRY(B,U7) (B:e34) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 |
| +3.60 | B | g74 TRACK_APPEARED_LEFT(B,U15) (B:e35) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 |
| +3.60 | B | g74 TRACK_APPEARED_LEFT(B,U15) (B:e35)<br>g77 TRACK_LOST(B,U15) (B:e36) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_005: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_007, track_008, track_009 |
| +3.85 | A | g76 EGO_PATH_EXIT(A,U4) (A:e42) | ego: MOVING<br>track_001#segment_2: no active state<br>track_004: IN_EGO_PATH<br>track_005#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_009: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_005#segment_2, track_006, track_010 |

## Plain-language reading

- 7.75 s before the reference collision, A started moving (already the case when first observed).
- 7.75 s before the reference collision, B started moving (already the case when first observed).
- 7.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared in front of it.
- 7.75 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 7.70 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared in front of it.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared on its left.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U4 became critical.
- 7.20 s before the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 7.05 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 7.00 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared on its left.
- 5.55 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 5.45 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 5.30 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 4.10 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 3.95 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.50 s before the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 1.45 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared in front of it.
- 1.40 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared on its right.
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B's radar started tracking anonymous road user U11, which appeared on its left.
- 1.20 s before the reference collision, A's radar started tracking anonymous road user U12, which appeared in front of it.
- 1.15 s before the reference collision, B's radar started tracking anonymous road user U13, which appeared in front of it.
- 1.10 s before the reference collision, A observed anonymous road user U12 enter its forward path corridor.
- 0.80 s before the reference collision, A observed B start closing in.
- 0.75 s before the reference collision, B's time-to-contact with A became critical.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.35 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 0.20 s before the reference collision, A observed anonymous road user U12 leave its forward path corridor.
- 0.05 s before the reference collision, A's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 255, B: 255 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.10 s after the reference collision, A's radar started tracking anonymous road user U7, which appeared in front of it.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.10 s after the reference collision, B observed anonymous road user U13 enter its forward path corridor.
- 0.15 s after the reference collision, A observed B stop closing in.
- 0.25 s after the reference collision, B observed anonymous road user U11 enter its forward path corridor.
- 0.50 s after the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the reference collision, A's radar started tracking anonymous road user U4, which appeared in front of it.
- 0.60 s after the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 0.70 s after the reference collision, A's radar started tracking anonymous road user U11, which appeared on its left.
- 1.05 s after the reference collision, A's time-to-contact with anonymous road user U4 became critical.
- 1.10 s after the reference collision, B's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 1.20 s after the reference collision, A's time-to-contact with anonymous road user U7 stopped being critical.
- 1.20 s after the reference collision, A observed anonymous road user U7 leave its forward path corridor.
- 1.35 s after the reference collision, A observed anonymous road user U10 enter its forward path corridor.
- 1.45 s after the reference collision, B observed anonymous road user U8 enter its forward path corridor.
- 1.45 s after the reference collision, B's time-to-contact with anonymous road user U8 became critical.
- 1.60 s after the reference collision, B's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 1.75 s after the reference collision, A's radar started tracking anonymous road user U14, which appeared on its left.
- 1.85 s after the reference collision, B observed anonymous road user U13 leave its forward path corridor.
- 1.85 s after the reference collision, B observed anonymous road user U7 cutting in from the right.
- 2.00 s after the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 2.50 s after the reference collision, A observed anonymous road user U7 enter its forward path corridor.
- 2.70 s after the reference collision, A observed anonymous road user U7 cutting in from the right.
- 2.80 s after the reference collision, B's time-to-contact with anonymous road user U8 stopped being critical.
- 2.80 s after the reference collision, B observed anonymous road user U8 leave its forward path corridor.
- 2.95 s after the reference collision, B's time-to-contact with anonymous road user U7 became critical.
- 3.40 s after the reference collision, B observed anonymous road user U7 enter its forward path corridor.
- 3.40 s after the reference collision, A's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- 3.60 s after the reference collision, B's radar started tracking anonymous road user U15, which appeared on its left.
- 3.80 s after the reference collision, A observed anonymous road user U10 leave its forward path corridor.
- 3.85 s after the reference collision, A observed anonymous road user U4 leave its forward path corridor.
- 3.90 s after the reference collision, B's radar lost anonymous road user U15 (its states are UNKNOWN from then on, not ended).
