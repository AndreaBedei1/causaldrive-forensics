# Global graph - S14/run_0_surrounded

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_003 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_003 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_002, B:track_005 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_004#segment_1, A:track_004#segment_3, B:track_001 |
| U11 | anonymous_road_user | anonymous; observed by A as A:track_004#segment_2 |
| U12 | anonymous_road_user | anonymous; observed by A as A:track_005 |
| U9 | anonymous_road_user | anonymous; observed by A, B as A:track_006, B:track_010 |
| U5 | anonymous_road_user | anonymous; observed by A, B as A:track_007, B:track_006 |
| U8 | anonymous_road_user | anonymous; observed by A, B as A:track_008, B:track_009 |
| U13 | anonymous_road_user | anonymous; observed by A, B as A:track_009, B:track_012 |
| U4 | anonymous_road_user | anonymous; observed by B as B:track_004 |
| U6 | anonymous_road_user | anonymous; observed by B as B:track_007 |
| U7 | anonymous_road_user | anonymous; observed by B as B:track_008 |
| U10 | anonymous_road_user | anonymous; observed by B as B:track_011 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e15 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e21 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 497.63 vs 497.63 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 2.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.53 m/s for reference)<br>clearance at the contact 2.01 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U1: A:track_001, B:track_003 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 11.0 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.51 m/s for reference)<br>clearance at the contact 10.95 m (beyond 3.50 m: confidence factor 0.05)<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U2: A:track_002, B:track_005 |
| A:track_003 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.36 m/s for reference)<br>clearance at the contact 0.11 m<br>the only compatible track of A touching it at the contact (clearance 0.11 m; track_001, track_002 at 2.04 m, 11.03 m) |
| A:track_004#segment_1 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.60 s before the matched collision<br>continuous up to the contact: last observed 0.95 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.2 m -> 10.3 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.42 m/s for reference)<br>clearance at the contact 10.32 m (beyond 3.50 m: confidence factor 0.08)<br>anonymous road user U3: B:track_001, A:track_004#segment_1, A:track_004#segment_3 |
| A:track_004#segment_2 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.90 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 10.2 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.55 m/s for reference)<br>clearance at the contact 10.08 m (beyond 3.50 m: confidence factor 0.09)<br>anonymous road user U11: A:track_004#segment_2 |
| A:track_004#segment_3 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.90 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: B:track_001, A:track_004#segment_1, A:track_004#segment_3 |
| A:track_005 | U12 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.1 m -> 42.0 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.36 m/s for reference)<br>clearance at the contact 41.95 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U12: A:track_005 |
| A:track_006 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.15 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.3 m -> 26.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 26.22 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U9: B:track_010, A:track_006 |
| A:track_007 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U5: B:track_006, A:track_007 |
| A:track_008 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U8: B:track_009, A:track_008 |
| A:track_009 | U13 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 2.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U13: B:track_012, A:track_009 |
| B:track_001 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.5 m -> 9.9 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.04 m/s for reference)<br>clearance at the contact 9.92 m (beyond 3.50 m: confidence factor 0.10)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>anonymous road user U3: B:track_001, A:track_004#segment_1, A:track_004#segment_3 |
| B:track_002 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.8 m -> 0.8 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.66 m/s for reference)<br>clearance at the contact 0.79 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 240 samples; 100% within 3 sigma) at A's own velocity |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.2 m -> 2.8 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.13 m/s for reference)<br>clearance at the contact 2.78 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>anonymous road user U1: A:track_001, B:track_003 |
| B:track_004 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.8 m -> 28.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U4: B:track_004 |
| B:track_005 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.1 m -> 10.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.06 m/s for reference)<br>clearance at the contact 10.55 m (beyond 3.50 m: confidence factor 0.06)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>anonymous road user U2: A:track_002, B:track_005 |
| B:track_006 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.6 m -> 11.2 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.07 m/s for reference)<br>clearance at the contact 11.13 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>anonymous road user U5: B:track_006, A:track_007 |
| B:track_007 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.60 s before the matched collision<br>lost 3.95 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.4 m -> 28.0 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_007 |
| B:track_008 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 7.55 s before the matched collision<br>lost 5.55 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 44.6 m -> 44.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_008 |
| B:track_009 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 1.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.7 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.11 m/s for reference)<br>clearance at the contact 26.69 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>anonymous road user U8: B:track_009, A:track_008 |
| B:track_010 | U9 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 1.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.7 m -> 26.1 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.06 m/s for reference)<br>clearance at the contact 26.14 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>anonymous road user U9: B:track_010, A:track_006 |
| B:track_011 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.75 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.7 m -> 42.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.04 m/s for reference)<br>clearance at the contact 42.56 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_005, track_006, track_009, track_010, track_011)<br>anonymous road user U10: B:track_011 |
| B:track_012 | U13 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 497.63 vs 497.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U13: B:track_012, A:track_009 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.75 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.75 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.75 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.75 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -7.75 | TRACK_APPEARED_FRONT | A | U1 | A:e03 @ 0.00 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g06 | -7.75 | TRACK_APPEARED_FRONT | B | U3 | B:e03 @ 0.00 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g07 | -7.75 | TRACK_APPEARED_LEFT | A | B | A:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g08 | -7.75 | TRACK_APPEARED_LEFT | A | U2 | A:e04 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g09 | -7.75 | TRACK_APPEARED_LEFT | B | U4 | B:e04 @ 0.00, B:e13 @ 3.65 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g10 | -7.75 | TRACK_APPEARED_RIGHT | B | A | B:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g11 | -7.75 | TRACK_APPEARED_RIGHT | B | U1 | B:e06 @ 0.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g12 | -7.70 | TRACK_APPEARED_LEFT | B | U2 | B:e07 @ 0.05 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g13 | -7.70 | TRACK_APPEARED_RIGHT | B | U5 | B:e08 @ 0.05 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g14 | -7.60 | TRACK_APPEARED_LEFT | A | U3 | A:e06 @ 0.15, A:e09 @ 6.80 | initial_in_ego_path=False; source_track=track_004#segment_1; aggregation=entity_state_union; source_tracks=['A:track_004#segment_1'] |
| g15 | -7.60 | TRACK_APPEARED_RIGHT | B | U6 | B:e09 @ 0.15, B:e14 @ 3.80 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g16 | -7.55 | TRACK_APPEARED_FRONT | B | U7 | B:e10 @ 0.20, B:e12 @ 2.20 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g17 | -7.25 | CRITICAL_TTC_START | A | U1 | A:e07 @ 0.50, A:e25 @ 9.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g18 | -7.25 | CRITICAL_TTC_START | B | U3 | B:e11 @ 0.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g19 | -5.55 | TRACK_LOST | B | U7 | B:e12 @ 2.20 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g20 | -4.10 | TRACK_LOST | B | U4 | B:e13 @ 3.65 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g21 | -3.95 | TRACK_LOST | B | U6 | B:e14 @ 3.80 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g22 | -1.40 | CRITICAL_TTC_START | A | B | A:e08 @ 6.35, A:e16 @ 7.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g23 | -1.35 | TRACK_APPEARED_LEFT | B | U8 | B:e15 @ 6.40, B:e28 @ 9.35 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g24 | -1.25 | TRACK_APPEARED_RIGHT | B | U9 | B:e16 @ 6.50, B:e26 @ 8.75 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g25 | -1.15 | TRACK_APPEARED_FRONT | B | U10 | B:e17 @ 6.60, B:e18 @ 7.00 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g26 | -0.95 | TRACK_LOST | A | U3 | A:e09 @ 6.80 | source_track=track_004#segment_1; aggregation=entity_state_union; source_tracks=['A:track_004#segment_1'] |
| g27 | -0.90 | TRACK_APPEARED_LEFT | A | U11 | A:e10 @ 6.85, A:e23 @ 8.60 | initial_in_ego_path=False; source_track=track_004#segment_2; aggregation=entity_state_union; source_tracks=['A:track_004#segment_2'] |
| g28 | -0.80 | CLOSING_START | A | B | A:e11 @ 6.95, A:e20 @ 7.90 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g29 | -0.75 | TRACK_LOST | B | U10 | B:e18 @ 7.00 | source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g30 | -0.70 | TRACK_APPEARED_FRONT | A | U12 | A:e12 @ 7.05, A:e18 @ 7.80 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g31 | -0.70 | CRITICAL_TTC_START | B | A | B:e19 @ 7.05, B:e22 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g32 | -0.60 | CLOSING_START | B | A | B:e20 @ 7.15, B:e24 @ 7.85 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g33 | -0.25 | EGO_PATH_ENTRY | A | U12 | A:e13 @ 7.50 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g34 | -0.15 | TRACK_APPEARED_RIGHT | A | U9 | A:e14 @ 7.60 | initial_in_ego_path=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g35 | 0.00 | COLLISION | - | A, B | A:e15 @ 7.75, B:e21 @ 7.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 497.63, B 497.63 |
| g36 | 0.00 | CRITICAL_TTC_END | A | B | A:e16 @ 7.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g37 | 0.00 | CRITICAL_TTC_END | B | A | B:e22 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g38 | 0.05 | THROTTLE_END | A | - | A:e17 @ 7.80 |  |
| g39 | 0.05 | THROTTLE_END | B | - | B:e23 @ 7.80 |  |
| g40 | 0.05 | TRACK_LOST | A | U12 | A:e18 @ 7.80 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g41 | 0.10 | CLOSING_END | B | A | B:e24 @ 7.85 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g42 | 0.10 | EGO_PATH_ENTRY | A | B | A:e19 @ 7.85 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g43 | 0.15 | CLOSING_END | A | B | A:e20 @ 7.90 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g44 | 0.15 | TRACK_APPEARED_RIGHT | A | U5 | A:e21 @ 7.90 | initial_in_ego_path=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g45 | 0.40 | TRACK_APPEARED_FRONT | B | U13 | B:e25 @ 8.15 | initial_in_ego_path=True; source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g46 | 0.80 | TRACK_APPEARED_LEFT | A | U8 | A:e22 @ 8.55 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g47 | 0.85 | TRACK_LOST | A | U11 | A:e23 @ 8.60 | source_track=track_004#segment_2; aggregation=entity_state_union; source_tracks=['A:track_004#segment_2'] |
| g48 | 0.90 | TRACK_APPEARED_FRONT | A | U3 | A:e24 @ 8.65 | initial_in_ego_path=True; source_track=track_004#segment_3; aggregation=entity_state_union; source_tracks=['A:track_004#segment_3'] |
| g49 | 1.00 | TRACK_LOST | B | U9 | B:e26 @ 8.75 | source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g50 | 1.25 | EGO_PATH_ENTRY | B | U8 | B:e27 @ 9.00 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g51 | 1.40 | CRITICAL_TTC_END | A | U1 | A:e25 @ 9.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g52 | 1.40 | CRITICAL_TTC_START | A | U3 | A:e26 @ 9.15 | source_track=track_004#segment_3; aggregation=entity_state_union; source_tracks=['A:track_004#segment_3'] |
| g53 | 1.60 | TRACK_LOST | B | U8 | B:e28 @ 9.35 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g54 | 2.20 | TRACK_APPEARED_LEFT | A | U13 | A:e27 @ 9.95, A:e31 @ 11.25 | initial_in_ego_path=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g55 | 2.20 | EGO_PATH_ENTRY | B | U2 | B:e29 @ 9.95, B:e31 @ 11.40 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g56 | 2.50 | CRITICAL_TTC_START | A | U5 | A:e28 @ 10.25 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g57 | 2.60 | EGO_PATH_EXIT | A | U1 | A:e29 @ 10.35 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g58 | 2.60 | EGO_PATH_EXIT | A | U9 | A:e30 @ 10.35 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g59 | 3.30 | CLOSING_START | B | U1 | B:e30 @ 11.05 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g60 | 3.50 | TRACK_LOST | A | U13 | A:e31 @ 11.25 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g61 | 3.60 | EGO_PATH_ENTRY | A | U1 | A:e32 @ 11.35 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g62 | 3.60 | CRITICAL_TTC_START | A | U1 | A:e33 @ 11.35 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g63 | 3.65 | EGO_PATH_EXIT | B | U2 | B:e31 @ 11.40 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g64 | 3.80 | CLOSING_START | B | A | B:e32 @ 11.55 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g65 | 3.85 | EGO_PATH_ENTRY | A | U9 | A:e34 @ 11.60 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g66 | 3.85 | CRITICAL_TTC_START | B | U1 | B:e33 @ 11.60 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |

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
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g53
    g53 --PRECEDES--> g54
    g53 --PRECEDES--> g55
    g54 --PRECEDES--> g56
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g60 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g62 --PRECEDES--> g63
    g63 --PRECEDES--> g64
    g64 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g05 --SAME_TRACK--> g17
    g07 --SAME_TRACK--> g22
    g14 --SAME_TRACK--> g26
    g07 --SAME_TRACK--> g28
    g30 --SAME_TRACK--> g33
    g07 --SAME_TRACK--> g36
    g30 --SAME_TRACK--> g40
    g07 --SAME_TRACK--> g42
    g07 --SAME_TRACK--> g43
    g27 --SAME_TRACK--> g47
    g05 --SAME_TRACK--> g51
    g48 --SAME_TRACK--> g52
    g44 --SAME_TRACK--> g56
    g05 --SAME_TRACK--> g57
    g34 --SAME_TRACK--> g58
    g54 --SAME_TRACK--> g60
    g05 --SAME_TRACK--> g61
    g05 --SAME_TRACK--> g62
    g34 --SAME_TRACK--> g65
    g06 --SAME_TRACK--> g18
    g16 --SAME_TRACK--> g19
    g09 --SAME_TRACK--> g20
    g15 --SAME_TRACK--> g21
    g25 --SAME_TRACK--> g29
    g10 --SAME_TRACK--> g31
    g10 --SAME_TRACK--> g32
    g10 --SAME_TRACK--> g37
    g10 --SAME_TRACK--> g41
    g24 --SAME_TRACK--> g49
    g23 --SAME_TRACK--> g50
    g23 --SAME_TRACK--> g53
    g12 --SAME_TRACK--> g55
    g11 --SAME_TRACK--> g59
    g12 --SAME_TRACK--> g63
    g10 --SAME_TRACK--> g64
    g11 --SAME_TRACK--> g66
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U1); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U4); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1) |
| -7.70 | TRACK_APPEARED_LEFT(B,U2); TRACK_APPEARED_RIGHT(B,U5) |
| -7.60 | TRACK_APPEARED_LEFT(A,U3); TRACK_APPEARED_RIGHT(B,U6) |
| -7.55 | TRACK_APPEARED_FRONT(B,U7) |
| -7.25 | CRITICAL_TTC_START(A,U1); CRITICAL_TTC_START(B,U3) |
| -5.55 | TRACK_LOST(B,U7) |
| -4.10 | TRACK_LOST(B,U4) |
| -3.95 | TRACK_LOST(B,U6) |
| -1.40 | CRITICAL_TTC_START(A,B) |
| -1.35 | TRACK_APPEARED_LEFT(B,U8) |
| -1.25 | TRACK_APPEARED_RIGHT(B,U9) |
| -1.15 | TRACK_APPEARED_FRONT(B,U10) |
| -0.95 | TRACK_LOST(A,U3) |
| -0.90 | TRACK_APPEARED_LEFT(A,U11) |
| -0.80 | CLOSING_START(A,B) |
| -0.75 | TRACK_LOST(B,U10) |
| -0.70 | TRACK_APPEARED_FRONT(A,U12); CRITICAL_TTC_START(B,A) |
| -0.60 | CLOSING_START(B,A) |
| -0.25 | EGO_PATH_ENTRY(A,U12) |
| -0.15 | TRACK_APPEARED_RIGHT(A,U9) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); TRACK_LOST(A,U12) |
| +0.10 | CLOSING_END(B,A); EGO_PATH_ENTRY(A,B) |
| +0.15 | CLOSING_END(A,B); TRACK_APPEARED_RIGHT(A,U5) |
| +0.40 | TRACK_APPEARED_FRONT(B,U13) |
| +0.80 | TRACK_APPEARED_LEFT(A,U8) |
| +0.85 | TRACK_LOST(A,U11) |
| +0.90 | TRACK_APPEARED_FRONT(A,U3) |
| +1.00 | TRACK_LOST(B,U9) |
| +1.25 | EGO_PATH_ENTRY(B,U8) |
| +1.40 | CRITICAL_TTC_END(A,U1); CRITICAL_TTC_START(A,U3) |
| +1.60 | TRACK_LOST(B,U8) |
| +2.20 | TRACK_APPEARED_LEFT(A,U13); EGO_PATH_ENTRY(B,U2) |
| +2.50 | CRITICAL_TTC_START(A,U5) |
| +2.60 | EGO_PATH_EXIT(A,U1); EGO_PATH_EXIT(A,U9) |
| +3.30 | CLOSING_START(B,U1) |
| +3.50 | TRACK_LOST(A,U13) |
| +3.60 | EGO_PATH_ENTRY(A,U1); CRITICAL_TTC_START(A,U1) |
| +3.65 | EGO_PATH_EXIT(B,U2) |
| +3.80 | CLOSING_START(B,A) |
| +3.85 | EGO_PATH_ENTRY(A,U9); CRITICAL_TTC_START(B,U1) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s); EGO_PATH_ENTRY 11.35 after critical TTC (+10.85 s) [local times; t_global: critical_ttc_start -7.25, ego_path_entry +3.60, collision +0.00]
- A's track_003 (B): CRITICAL_TTC_START 6.35, COLLISION with B 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -1.40, ego_path_entry +0.10, collision +0.00]
- A's track_004#segment_3 (unidentified U3): CRITICAL_TTC_START 9.15 [local times; t_global: critical_ttc_start +1.40]
- A's track_005 (unidentified U12): EGO_PATH_ENTRY 7.50, no critical TTC [local times; t_global: ego_path_entry -0.25, collision +0.00]
- A's track_006 (unidentified U9): EGO_PATH_ENTRY 11.60, no critical TTC [local times; t_global: ego_path_entry +3.85]
- A's track_007 (unidentified U5): CRITICAL_TTC_START 10.25 [local times; t_global: critical_ttc_start +2.50]
- B's track_001 (unidentified U3): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.05, COLLISION with A 7.75 (+0.70 s) [local times; t_global: critical_ttc_start -0.70, collision +0.00]
- B's track_003 (unidentified U1): CRITICAL_TTC_START 11.60 [local times; t_global: critical_ttc_start +3.85]
- B's track_005 (unidentified U2): EGO_PATH_ENTRY 9.95, no critical TTC [local times; t_global: ego_path_entry +2.20]
- B's track_009 (unidentified U8): EGO_PATH_ENTRY 9.00, no critical TTC [local times; t_global: ego_path_entry +1.25]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U1) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,B) (A:e05)<br>g08 TRACK_APPEARED_LEFT(A,U2) (A:e04) | ego: not yet observed |
| -7.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U3) (B:e03)<br>g09 TRACK_APPEARED_LEFT(B,U4) (B:e04)<br>g10 TRACK_APPEARED_RIGHT(B,A) (B:e05)<br>g11 TRACK_APPEARED_RIGHT(B,U1) (B:e06) | ego: not yet observed |
| -7.75 | B | g09 TRACK_APPEARED_LEFT(B,U4) (B:e04)<br>g20 TRACK_LOST(B,U4) (B:e13) | ego: not yet observed |
| -7.70 | B | g12 TRACK_APPEARED_LEFT(B,U2) (B:e07)<br>g13 TRACK_APPEARED_RIGHT(B,U5) (B:e08) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.60 | A | g14 TRACK_APPEARED_LEFT(A,U3) (A:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.60 | A | g14 TRACK_APPEARED_LEFT(A,U3) (A:e06)<br>g26 TRACK_LOST(A,U3) (A:e09) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.60 | B | g15 TRACK_APPEARED_RIGHT(B,U6) (B:e09) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC? |
| -7.60 | B | g15 TRACK_APPEARED_RIGHT(B,U6) (B:e09)<br>g21 TRACK_LOST(B,U6) (B:e14) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC? |
| -7.55 | B | g16 TRACK_APPEARED_FRONT(B,U7) (B:e10) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? |
| -7.55 | B | g16 TRACK_APPEARED_FRONT(B,U7) (B:e10)<br>g19 TRACK_LOST(B,U7) (B:e12) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? |
| -7.25 | A | g17 CRITICAL_TTC_START(A,U1) (A:e07) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004#segment_1: CRITICAL_TTC? |
| -7.25 | A | g17 CRITICAL_TTC_START(A,U1) (A:e07)<br>g51 CRITICAL_TTC_END(A,U1) (A:e25)<br>g52 CRITICAL_TTC_START(A,U3) (A:e26) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004#segment_1: CRITICAL_TTC? |
| -7.25 | B | g18 CRITICAL_TTC_START(B,U3) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC? |
| -1.40 | A | g22 CRITICAL_TTC_START(A,B) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state |
| -1.40 | A | g22 CRITICAL_TTC_START(A,B) (A:e08)<br>g35 COLLISION(A,B) (A:e15)<br>g36 CRITICAL_TTC_END(A,B) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state |
| -1.35 | B | g23 TRACK_APPEARED_LEFT(B,U8) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008 |
| -1.35 | B | g23 TRACK_APPEARED_LEFT(B,U8) (B:e15)<br>g53 TRACK_LOST(B,U8) (B:e28) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008 |
| -1.25 | B | g24 TRACK_APPEARED_RIGHT(B,U9) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_007, track_008 |
| -1.25 | B | g24 TRACK_APPEARED_RIGHT(B,U9) (B:e16)<br>g49 TRACK_LOST(B,U9) (B:e26) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_007, track_008 |
| -1.15 | B | g25 TRACK_APPEARED_FRONT(B,U10) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_007, track_008 |
| -1.15 | B | g25 TRACK_APPEARED_FRONT(B,U10) (B:e17)<br>g29 TRACK_LOST(B,U10) (B:e18) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: CRITICAL_TTC?<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_007, track_008 |
| -0.90 | A | g27 TRACK_APPEARED_LEFT(A,U11) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.90 | A | g27 TRACK_APPEARED_LEFT(A,U11) (A:e10)<br>g47 TRACK_LOST(A,U11) (A:e23) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.80 | A | g28 CLOSING_START(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.80 | A | g28 CLOSING_START(A,B) (A:e11)<br>g43 CLOSING_END(A,B) (A:e20)<br>g44 TRACK_APPEARED_RIGHT(A,U5) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.70 | A | g30 TRACK_APPEARED_FRONT(A,U12) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.70 | A | g30 TRACK_APPEARED_FRONT(A,U12) (A:e12)<br>g38 THROTTLE_END(A) (A:e17)<br>g40 TRACK_LOST(A,U12) (A:e18) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.70 | B | g31 CRITICAL_TTC_START(B,A) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 |
| -0.70 | B | g31 CRITICAL_TTC_START(B,A) (B:e19)<br>g35 COLLISION(A,B) (B:e21)<br>g37 CRITICAL_TTC_END(B,A) (B:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 |
| -0.60 | B | g32 CLOSING_START(B,A) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 |
| -0.60 | B | g32 CLOSING_START(B,A) (B:e20)<br>g41 CLOSING_END(B,A) (B:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 |
| -0.25 | A | g33 EGO_PATH_ENTRY(A,U12) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.15 | A | g34 TRACK_APPEARED_RIGHT(A,U9) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1 |
| +0.05 | B | g39 THROTTLE_END(B) (B:e23) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 |
| +0.10 | A | g42 EGO_PATH_ENTRY(A,B) (A:e19) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005 |
| +0.40 | B | g45 TRACK_APPEARED_FRONT(B,U13) (B:e25) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_011 |
| +0.80 | A | g46 TRACK_APPEARED_LEFT(A,U8) (A:e22) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_005 |
| +0.90 | A | g48 TRACK_APPEARED_FRONT(A,U3) (A:e24) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005 |
| +1.25 | B | g50 EGO_PATH_ENTRY(B,U8) (B:e27) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_009: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_010, track_011 |
| +2.20 | A | g54 TRACK_APPEARED_LEFT(A,U13) (A:e27) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005 |
| +2.20 | A | g54 TRACK_APPEARED_LEFT(A,U13) (A:e27)<br>g60 TRACK_LOST(A,U13) (A:e31) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005 |
| +2.20 | B | g55 EGO_PATH_ENTRY(B,U2) (B:e29) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 |
| +2.20 | B | g55 EGO_PATH_ENTRY(B,U2) (B:e29)<br>g63 EGO_PATH_EXIT(B,U2) (B:e31) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 |
| +2.50 | A | g56 CRITICAL_TTC_START(A,U5) (A:e28) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005 |
| +2.60 | A | g57 EGO_PATH_EXIT(A,U1) (A:e29)<br>g58 EGO_PATH_EXIT(A,U9) (A:e30) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005 |
| +3.30 | B | g59 CLOSING_START(B,U1) (B:e30) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 |
| +3.60 | A | g61 EGO_PATH_ENTRY(A,U1) (A:e32)<br>g62 CRITICAL_TTC_START(A,U1) (A:e33) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_009 |
| +3.80 | B | g64 CLOSING_START(B,A) (B:e32) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_005: no active state<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 |
| +3.85 | A | g65 EGO_PATH_ENTRY(A,U9) (A:e34) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_009 |
| +3.85 | B | g66 CRITICAL_TTC_START(B,U1) (B:e33) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: no active state<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_007, track_008, track_009, track_010, track_011 |

## Plain-language reading

- 7.75 s before the reference collision, A started moving (already the case when first observed).
- 7.75 s before the reference collision, B started moving (already the case when first observed).
- 7.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared in front of it.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.75 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its left.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its right.
- 7.60 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- 7.60 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 7.55 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared in front of it.
- 7.25 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U3 became critical.
- 5.55 s before the reference collision, B's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 4.10 s before the reference collision, B's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 3.95 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared on its left.
- 1.25 s before the reference collision, B's radar started tracking anonymous road user U9, which appeared on its right.
- 1.15 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared in front of it.
- 0.95 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.90 s before the reference collision, A's radar started tracking anonymous road user U11, which appeared on its left.
- 0.80 s before the reference collision, A observed B start closing in.
- 0.75 s before the reference collision, B's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 0.70 s before the reference collision, A's radar started tracking anonymous road user U12, which appeared in front of it.
- 0.70 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, B observed A start closing in.
- 0.25 s before the reference collision, A observed anonymous road user U12 enter its forward path corridor.
- 0.15 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared on its right.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 498, B: 498 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 0.10 s after the reference collision, B observed A stop closing in.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.15 s after the reference collision, A observed B stop closing in.
- 0.15 s after the reference collision, A's radar started tracking anonymous road user U5, which appeared on its right.
- 0.40 s after the reference collision, B's radar started tracking anonymous road user U13, which appeared in front of it.
- 0.80 s after the reference collision, A's radar started tracking anonymous road user U8, which appeared on its left.
- 0.85 s after the reference collision, A's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 0.90 s after the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 1.00 s after the reference collision, B's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 1.25 s after the reference collision, B observed anonymous road user U8 enter its forward path corridor.
- 1.40 s after the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 1.40 s after the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 1.60 s after the reference collision, B's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 2.20 s after the reference collision, A's radar started tracking anonymous road user U13, which appeared on its left.
- 2.20 s after the reference collision, B observed anonymous road user U2 enter its forward path corridor.
- 2.50 s after the reference collision, A's time-to-contact with anonymous road user U5 became critical.
- 2.60 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 2.60 s after the reference collision, A observed anonymous road user U9 leave its forward path corridor.
- 3.30 s after the reference collision, B observed anonymous road user U1 start closing in.
- 3.50 s after the reference collision, A's radar lost anonymous road user U13 (its states are UNKNOWN from then on, not ended).
- 3.60 s after the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 3.60 s after the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 3.65 s after the reference collision, B observed anonymous road user U2 leave its forward path corridor.
- 3.80 s after the reference collision, B observed A start closing in.
- 3.85 s after the reference collision, A observed anonymous road user U9 enter its forward path corridor.
- 3.85 s after the reference collision, B's time-to-contact with anonymous road user U1 became critical.
