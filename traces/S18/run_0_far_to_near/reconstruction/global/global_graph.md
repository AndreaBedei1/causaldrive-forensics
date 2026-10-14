# Global graph - S18/run_0_far_to_near

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_001, B:track_009 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_003 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_004, A:track_009, B:track_004, B:track_005, B:track_012, B:track_013 |
| U4 | anonymous_road_user | anonymous; observed by A as A:track_005#segment_1 |
| U5 | anonymous_road_user | anonymous; observed by A, B as A:track_005#segment_2, B:track_006 |
| U6 | anonymous_road_user | anonymous; observed by A, B as A:track_006, B:track_008 |
| U8 | anonymous_road_user | anonymous; observed by A as A:track_007#segment_1 |
| U9 | anonymous_road_user | anonymous; observed by A, B as A:track_007#segment_2, B:track_010 |
| U10 | anonymous_road_user | anonymous; observed by A, B as A:track_008, B:track_011 |
| U7 | anonymous_road_user | anonymous; observed by B as B:track_007 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e42 | 8.50 | -8.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e35 | 8.50 | -8.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 745.29 vs 745.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 4.30 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 1.6 m -> 7.0 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_009 |
| A:track_002 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.5 m -> 0.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.07 m/s for reference)<br>clearance at the contact 0.09 m<br>the only track of A compatible with the contact |
| A:track_003 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 7.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 1.6 m -> 7.1 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_003, B:track_003 |
| A:track_004 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.90 s before it (window 1.00 s)<br>not approaching before the contact: clearance 1.4 m -> 6.1 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 5.14 m/s for reference)<br>clearance at the contact 5.35 m (beyond 3.50 m: confidence factor 0.83)<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| A:track_005#segment_1 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.60 s before the matched collision<br>lost 6.30 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 57.0 m -> 50.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U4: A:track_005#segment_1 |
| A:track_005#segment_2 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 6.25 s before the matched collision<br>lost 4.70 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 46.4 m -> 39.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U5: B:track_006, A:track_005#segment_2 |
| A:track_006 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 6.90 s before the matched collision<br>lost 4.85 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 47.9 m -> 41.3 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U6: A:track_006, B:track_008 |
| A:track_007#segment_1 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.90 s before the matched collision<br>continuous up to the contact: last observed 1.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.4 m -> 14.4 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 6.78 m/s for reference)<br>clearance at the contact 14.41 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U8: A:track_007#segment_1 |
| A:track_007#segment_2 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.6 m -> 6.9 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 7.05 m/s for reference)<br>clearance at the contact 6.94 m (beyond 3.50 m: confidence factor 0.52)<br>anonymous road user U9: B:track_010, A:track_007#segment_2 |
| A:track_008 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.7 m -> 8.3 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 6.98 m/s for reference)<br>clearance at the contact 8.33 m (beyond 3.50 m: confidence factor 0.27)<br>anonymous road user U10: B:track_011, A:track_008 |
| A:track_009 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 2.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_001 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 6.20 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 7.3 m -> 4.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_009 |
| B:track_002 | A | ASSOCIATED | 0.99 | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.17 m/s for reference)<br>clearance at the contact 0.03 m<br>the only track of B compatible with the contact |
| B:track_003 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.10 s before the matched collision<br>lost 5.95 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 11.0 m -> 17.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U2: A:track_003, B:track_003 |
| B:track_004 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.00 s before the matched collision<br>lost 7.75 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 35.7 m -> 33.7 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_005 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.60 s before the matched collision<br>lost 2.70 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 7.2 m -> 4.4 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 5.89 m/s for reference)<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_006 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.55 s before the matched collision<br>lost 5.15 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 48.8 m -> 42.1 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U5: B:track_006, A:track_005#segment_2 |
| B:track_007 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 6.35 s before the matched collision<br>lost 6.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 50.9 m -> 49.0 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_007 |
| B:track_008 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 5.95 s before the matched collision<br>lost 5.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 48.6 m -> 42.9 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: A:track_006, B:track_008 |
| B:track_009 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 5.00 s before the matched collision<br>lost 3.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 16.9 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_009 |
| B:track_010 | U9 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.5 m -> 6.6 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 7.00 m/s for reference)<br>clearance at the contact 6.57 m (beyond 3.50 m: confidence factor 0.59)<br>anonymous road user U9: B:track_010, A:track_007#segment_2 |
| B:track_011 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 8.6 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 6.94 m/s for reference)<br>clearance at the contact 8.61 m (beyond 3.50 m: confidence factor 0.23)<br>anonymous road user U10: B:track_011, A:track_008 |
| B:track_012 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.8 m -> 14.4 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 5.82 m/s for reference)<br>clearance at the contact 7.77 m (beyond 3.50 m: confidence factor 0.36)<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_013 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.35 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -8.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -8.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -8.50 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -8.50 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -8.50 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -8.50 | TRACK_APPEARED_RIGHT | A | U1 | A:e04 @ 0.00, A:e24 @ 4.20 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g07 | -8.50 | TRACK_APPEARED_RIGHT | A | U2 | A:e05 @ 0.00, A:e11 @ 1.25 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g08 | -8.50 | TRACK_APPEARED_RIGHT | B | A | B:e04 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g09 | -8.50 | TRACK_APPEARED_RIGHT | B | U1 | B:e03 @ 0.00, B:e17 @ 2.30 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g10 | -8.50 | CLOSING_START | A | U1 | A:e06 @ 0.00, A:e19 @ 2.60 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g11 | -8.50 | CLOSING_START | B | U1 | B:e05 @ 0.00, B:e16 @ 2.30 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g12 | -8.10 | TRACK_APPEARED_RIGHT | B | U2 | B:e06 @ 0.40, B:e21 @ 2.55 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -8.00 | TRACK_APPEARED_RIGHT | B | U3 | B:e07 @ 0.50, B:e09 @ 0.75 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g14 | -8.00 | CLOSING_START | B | U3 | B:e08 @ 0.50 | active_at_first_observation=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g15 | -7.75 | TRACK_LOST | B | U3 | B:e09 @ 0.75 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g16 | -7.65 | TRACK_APPEARED_RIGHT | A | U3 | A:e07 @ 0.85, A:e38 @ 7.60 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g17 | -7.65 | CLOSING_START | A | U3 | A:e08 @ 0.85, A:e27 @ 6.10 | active_at_first_observation=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g18 | -7.60 | TRACK_APPEARED_FRONT | A | U4 | A:e09 @ 0.90, A:e16 @ 2.20 | initial_in_ego_path=False; source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g19 | -7.60 | TRACK_APPEARED_RIGHT | B | U3 | B:e10 @ 0.90, B:e27 @ 5.80 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g20 | -7.60 | CLOSING_START | A | U4 | A:e10 @ 0.90 | active_at_first_observation=True; source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g21 | -7.60 | CLOSING_START | B | U3 | B:e11 @ 0.90, B:e26 @ 5.80 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g22 | -7.55 | TRACK_APPEARED_RIGHT | B | U5 | B:e12 @ 0.95, B:e22 @ 3.35 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g23 | -7.55 | CLOSING_START | B | U5 | B:e13 @ 0.95 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g24 | -7.25 | TRACK_LOST | A | U2 | A:e11 @ 1.25 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g25 | -6.90 | TRACK_APPEARED_FRONT | A | U6 | A:e12 @ 1.60, A:e22 @ 3.65 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g26 | -6.90 | CLOSING_START | A | U6 | A:e13 @ 1.60 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g27 | -6.70 | CRITICAL_TTC_START | A | U1 | A:e14 @ 1.80, A:e21 @ 2.65 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g28 | -6.55 | CUT_IN_FROM_RIGHT_START | A | U1 | A:e15 @ 1.95, A:e20 @ 2.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g29 | -6.35 | TRACK_APPEARED_RIGHT | B | U7 | B:e14 @ 2.15, B:e18 @ 2.40 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g30 | -6.35 | CLOSING_START | B | U7 | B:e15 @ 2.15 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g31 | -6.30 | TRACK_LOST | A | U4 | A:e16 @ 2.20 | source_track=track_005#segment_1; aggregation=entity_state_union; source_tracks=['A:track_005#segment_1'] |
| g32 | -6.25 | TRACK_APPEARED_FRONT | A | U5 | A:e17 @ 2.25, A:e23 @ 3.80 | initial_in_ego_path=True; source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g33 | -6.25 | CLOSING_START | A | U5 | A:e18 @ 2.25 | active_at_first_observation=True; source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g34 | -6.20 | CLOSING_END | B | U1 | B:e16 @ 2.30 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g35 | -6.20 | TRACK_LOST | B | U1 | B:e17 @ 2.30 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g36 | -6.10 | TRACK_LOST | B | U7 | B:e18 @ 2.40 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g37 | -5.95 | TRACK_APPEARED_RIGHT | B | U6 | B:e19 @ 2.55, B:e23 @ 3.40 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g38 | -5.95 | CLOSING_START | B | U6 | B:e20 @ 2.55 | active_at_first_observation=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g39 | -5.95 | TRACK_LOST | B | U2 | B:e21 @ 2.55 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g40 | -5.90 | CLOSING_END | A | U1 | A:e19 @ 2.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g41 | -5.85 | CUT_IN_FROM_RIGHT_END | A | U1 | A:e20 @ 2.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g42 | -5.85 | CRITICAL_TTC_END | A | U1 | A:e21 @ 2.65 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g43 | -5.15 | TRACK_LOST | B | U5 | B:e22 @ 3.35 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g44 | -5.10 | TRACK_LOST | B | U6 | B:e23 @ 3.40 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g45 | -5.00 | TRACK_APPEARED_RIGHT | B | U1 | B:e24 @ 3.50, B:e25 @ 5.40 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g46 | -4.85 | TRACK_LOST | A | U6 | A:e22 @ 3.65 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g47 | -4.70 | TRACK_LOST | A | U5 | A:e23 @ 3.80 | source_track=track_005#segment_2; aggregation=entity_state_union; source_tracks=['A:track_005#segment_2'] |
| g48 | -4.30 | TRACK_LOST | A | U1 | A:e24 @ 4.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g49 | -3.10 | TRACK_LOST | B | U1 | B:e25 @ 5.40 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g50 | -3.05 | CRITICAL_TTC_START | A | U3 | A:e25 @ 5.45, A:e28 @ 6.15 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g51 | -2.90 | CUT_IN_FROM_RIGHT_START | A | U3 | A:e26 @ 5.60, A:e29 @ 6.20 | geometry=estimated_body; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g52 | -2.70 | CLOSING_END | B | U3 | B:e26 @ 5.80 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g53 | -2.70 | TRACK_LOST | B | U3 | B:e27 @ 5.80 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g54 | -2.40 | CLOSING_END | A | U3 | A:e27 @ 6.10 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g55 | -2.35 | CRITICAL_TTC_END | A | U3 | A:e28 @ 6.15 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g56 | -2.30 | CUT_IN_FROM_RIGHT_END | A | U3 | A:e29 @ 6.20 | geometry=estimated_body; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g57 | -1.90 | TRACK_APPEARED_FRONT | A | U8 | A:e30 @ 6.60, A:e35 @ 7.50 | initial_in_ego_path=False; source_track=track_007#segment_1; aggregation=entity_state_union; source_tracks=['A:track_007#segment_1'] |
| g58 | -1.90 | CLOSING_START | A | U8 | A:e31 @ 6.60 | active_at_first_observation=True; source_track=track_007#segment_1; aggregation=entity_state_union; source_tracks=['A:track_007#segment_1'] |
| g59 | -1.85 | TRACK_APPEARED_RIGHT | B | U9 | B:e28 @ 6.65 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g60 | -1.85 | CLOSING_START | B | U9 | B:e29 @ 6.65, B:e42 @ 9.30 | active_at_first_observation=True; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g61 | -1.80 | TRACK_APPEARED_RIGHT | B | U10 | B:e30 @ 6.70 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g62 | -1.80 | CLOSING_START | B | U10 | B:e31 @ 6.70, B:e43 @ 9.30 | active_at_first_observation=True; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g63 | -1.65 | TRACK_APPEARED_RIGHT | A | U10 | A:e32 @ 6.85 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g64 | -1.65 | CLOSING_START | A | U10 | A:e33 @ 6.85, A:e49 @ 9.40 | active_at_first_observation=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g65 | -1.55 | TRACK_APPEARED_RIGHT | B | U3 | B:e32 @ 6.95, B:e41 @ 9.20 | initial_in_ego_path=False; source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g66 | -1.35 | CRITICAL_TTC_START | A | B | A:e34 @ 7.15, A:e43 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g67 | -1.00 | TRACK_LOST | A | U8 | A:e35 @ 7.50 | source_track=track_007#segment_1; aggregation=entity_state_union; source_tracks=['A:track_007#segment_1'] |
| g68 | -0.95 | TRACK_APPEARED_FRONT | A | U9 | A:e36 @ 7.55 | initial_in_ego_path=True; source_track=track_007#segment_2; aggregation=entity_state_union; source_tracks=['A:track_007#segment_2'] |
| g69 | -0.95 | CLOSING_START | A | U9 | A:e37 @ 7.55, A:e50 @ 9.45 | active_at_first_observation=True; source_track=track_007#segment_2; aggregation=entity_state_union; source_tracks=['A:track_007#segment_2'] |
| g70 | -0.90 | CRITICAL_TTC_START | B | A | B:e33 @ 7.60, B:e36 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g71 | -0.90 | TRACK_LOST | A | U3 | A:e38 @ 7.60 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g72 | -0.85 | CLOSING_START | A | B | A:e39 @ 7.65, A:e45 @ 8.55 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g73 | -0.80 | CLOSING_START | B | A | B:e34 @ 7.70, B:e39 @ 9.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g74 | -0.45 | CRITICAL_TTC_START | A | U9 | A:e40 @ 8.05, A:e51 @ 9.60 | source_track=track_007#segment_2; aggregation=entity_state_union; source_tracks=['A:track_007#segment_2'] |
| g75 | -0.05 | CRITICAL_TTC_START | A | U10 | A:e41 @ 8.45, A:e48 @ 8.80 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g76 | 0.00 | COLLISION | - | A, B | A:e42 @ 8.50, B:e35 @ 8.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 745.29, B 745.29 |
| g77 | 0.00 | CRITICAL_TTC_END | A | B | A:e43 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g78 | 0.00 | CRITICAL_TTC_END | B | A | B:e36 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g79 | 0.00 | EGO_PATH_ENTRY | A | B | A:e44 @ 8.50 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g80 | 0.05 | CLOSING_END | A | B | A:e45 @ 8.55 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g81 | 0.05 | THROTTLE_END | A | - | A:e46 @ 8.55 |  |
| g82 | 0.05 | THROTTLE_END | B | - | B:e37 @ 8.55 |  |
| g83 | 0.05 | BRAKE_START | A | - | A:e47 @ 8.55 |  |
| g84 | 0.05 | BRAKE_START | B | - | B:e38 @ 8.55 |  |
| g85 | 0.30 | CRITICAL_TTC_END | A | U10 | A:e48 @ 8.80 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g86 | 0.60 | CLOSING_END | B | A | B:e39 @ 9.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g87 | 0.60 | EGO_PATH_ENTRY | B | A | B:e40 @ 9.10, B:e44 @ 9.50 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g88 | 0.70 | TRACK_LOST | B | U3 | B:e41 @ 9.20 | source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g89 | 0.80 | CLOSING_END | B | U10 | B:e43 @ 9.30 | source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g90 | 0.80 | CLOSING_END | B | U9 | B:e42 @ 9.30 | source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g91 | 0.90 | CLOSING_END | A | U10 | A:e49 @ 9.40 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g92 | 0.95 | CLOSING_END | A | U9 | A:e50 @ 9.45 | source_track=track_007#segment_2; aggregation=entity_state_union; source_tracks=['A:track_007#segment_2'] |
| g93 | 1.00 | EGO_PATH_EXIT | B | A | B:e44 @ 9.50 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g94 | 1.10 | CRITICAL_TTC_END | A | U9 | A:e51 @ 9.60 | source_track=track_007#segment_2; aggregation=entity_state_union; source_tracks=['A:track_007#segment_2'] |
| g95 | 1.10 | MOVING_END | B | - | B:e45 @ 9.60 |  |
| g96 | 1.10 | STOP_START | B | - | B:e46 @ 9.60 |  |
| g97 | 1.20 | MOVING_END | A | - | A:e52 @ 9.70 |  |
| g98 | 1.20 | STOP_START | A | - | A:e53 @ 9.70 |  |
| g99 | 1.35 | TRACK_APPEARED_RIGHT | B | U3 | B:e47 @ 9.85 | initial_in_ego_path=False; source_track=track_013; aggregation=entity_state_union; source_tracks=['B:track_013'] |
| g100 | 1.35 | CLOSING_START | B | U3 | B:e48 @ 9.85 | active_at_first_observation=True; source_track=track_013; aggregation=entity_state_union; source_tracks=['B:track_013'] |
| g101 | 2.05 | TRACK_APPEARED_RIGHT | A | U3 | A:e54 @ 10.55 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g102 | 2.05 | EGO_PATH_ENTRY | B | A | B:e49 @ 10.55 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g103 | 2.05 | CLOSING_START | A | U3 | A:e55 @ 10.55 | active_at_first_observation=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |

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
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
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
    g36 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g40
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g43
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g46 --PRECEDES--> g47
    g47 --PRECEDES--> g48
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g57 --PRECEDES--> g60
    g58 --PRECEDES--> g59
    g58 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g59 --PRECEDES--> g62
    g60 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g61 --PRECEDES--> g64
    g62 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g63 --PRECEDES--> g65
    g64 --PRECEDES--> g65
    g65 --PRECEDES--> g66
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
    g73 --PRECEDES--> g74
    g74 --PRECEDES--> g75
    g75 --PRECEDES--> g76
    g75 --PRECEDES--> g77
    g75 --PRECEDES--> g78
    g75 --PRECEDES--> g79
    g76 --PRECEDES--> g80
    g76 --PRECEDES--> g81
    g76 --PRECEDES--> g82
    g76 --PRECEDES--> g83
    g76 --PRECEDES--> g84
    g77 --PRECEDES--> g80
    g77 --PRECEDES--> g81
    g77 --PRECEDES--> g82
    g77 --PRECEDES--> g83
    g77 --PRECEDES--> g84
    g78 --PRECEDES--> g80
    g78 --PRECEDES--> g81
    g78 --PRECEDES--> g82
    g78 --PRECEDES--> g83
    g78 --PRECEDES--> g84
    g79 --PRECEDES--> g80
    g79 --PRECEDES--> g81
    g79 --PRECEDES--> g82
    g79 --PRECEDES--> g83
    g79 --PRECEDES--> g84
    g80 --PRECEDES--> g85
    g81 --PRECEDES--> g85
    g82 --PRECEDES--> g85
    g83 --PRECEDES--> g85
    g84 --PRECEDES--> g85
    g85 --PRECEDES--> g86
    g85 --PRECEDES--> g87
    g86 --PRECEDES--> g88
    g87 --PRECEDES--> g88
    g88 --PRECEDES--> g89
    g88 --PRECEDES--> g90
    g89 --PRECEDES--> g91
    g90 --PRECEDES--> g91
    g91 --PRECEDES--> g92
    g92 --PRECEDES--> g93
    g93 --PRECEDES--> g94
    g93 --PRECEDES--> g95
    g93 --PRECEDES--> g96
    g94 --PRECEDES--> g97
    g94 --PRECEDES--> g98
    g95 --PRECEDES--> g97
    g95 --PRECEDES--> g98
    g96 --PRECEDES--> g97
    g96 --PRECEDES--> g98
    g97 --PRECEDES--> g99
    g97 --PRECEDES--> g100
    g98 --PRECEDES--> g99
    g98 --PRECEDES--> g100
    g99 --PRECEDES--> g101
    g99 --PRECEDES--> g102
    g99 --PRECEDES--> g103
    g100 --PRECEDES--> g101
    g100 --PRECEDES--> g102
    g100 --PRECEDES--> g103
    g06 --SAME_TRACK--> g10
    g16 --SAME_TRACK--> g17
    g18 --SAME_TRACK--> g20
    g07 --SAME_TRACK--> g24
    g25 --SAME_TRACK--> g26
    g06 --SAME_TRACK--> g27
    g06 --SAME_TRACK--> g28
    g18 --SAME_TRACK--> g31
    g32 --SAME_TRACK--> g33
    g06 --SAME_TRACK--> g40
    g06 --SAME_TRACK--> g41
    g06 --SAME_TRACK--> g42
    g25 --SAME_TRACK--> g46
    g32 --SAME_TRACK--> g47
    g06 --SAME_TRACK--> g48
    g16 --SAME_TRACK--> g50
    g16 --SAME_TRACK--> g51
    g16 --SAME_TRACK--> g54
    g16 --SAME_TRACK--> g55
    g16 --SAME_TRACK--> g56
    g57 --SAME_TRACK--> g58
    g63 --SAME_TRACK--> g64
    g05 --SAME_TRACK--> g66
    g57 --SAME_TRACK--> g67
    g68 --SAME_TRACK--> g69
    g16 --SAME_TRACK--> g71
    g05 --SAME_TRACK--> g72
    g68 --SAME_TRACK--> g74
    g63 --SAME_TRACK--> g75
    g05 --SAME_TRACK--> g77
    g05 --SAME_TRACK--> g79
    g05 --SAME_TRACK--> g80
    g63 --SAME_TRACK--> g85
    g63 --SAME_TRACK--> g91
    g68 --SAME_TRACK--> g92
    g68 --SAME_TRACK--> g94
    g101 --SAME_TRACK--> g103
    g09 --SAME_TRACK--> g11
    g13 --SAME_TRACK--> g14
    g13 --SAME_TRACK--> g15
    g19 --SAME_TRACK--> g21
    g22 --SAME_TRACK--> g23
    g29 --SAME_TRACK--> g30
    g09 --SAME_TRACK--> g34
    g09 --SAME_TRACK--> g35
    g29 --SAME_TRACK--> g36
    g37 --SAME_TRACK--> g38
    g12 --SAME_TRACK--> g39
    g22 --SAME_TRACK--> g43
    g37 --SAME_TRACK--> g44
    g45 --SAME_TRACK--> g49
    g19 --SAME_TRACK--> g52
    g19 --SAME_TRACK--> g53
    g59 --SAME_TRACK--> g60
    g61 --SAME_TRACK--> g62
    g08 --SAME_TRACK--> g70
    g08 --SAME_TRACK--> g73
    g08 --SAME_TRACK--> g78
    g08 --SAME_TRACK--> g86
    g08 --SAME_TRACK--> g87
    g65 --SAME_TRACK--> g88
    g59 --SAME_TRACK--> g90
    g61 --SAME_TRACK--> g89
    g08 --SAME_TRACK--> g93
    g99 --SAME_TRACK--> g100
    g08 --SAME_TRACK--> g102
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -8.50 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U2); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(B,U1) |
| -8.10 | TRACK_APPEARED_RIGHT(B,U2) |
| -8.00 | TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3) |
| -7.75 | TRACK_LOST(B,U3) |
| -7.65 | TRACK_APPEARED_RIGHT(A,U3); CLOSING_START(A,U3) |
| -7.60 | TRACK_APPEARED_FRONT(A,U4); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(A,U4); CLOSING_START(B,U3) |
| -7.55 | TRACK_APPEARED_RIGHT(B,U5); CLOSING_START(B,U5) |
| -7.25 | TRACK_LOST(A,U2) |
| -6.90 | TRACK_APPEARED_FRONT(A,U6); CLOSING_START(A,U6) |
| -6.70 | CRITICAL_TTC_START(A,U1) |
| -6.55 | CUT_IN_FROM_RIGHT_START(A,U1) |
| -6.35 | TRACK_APPEARED_RIGHT(B,U7); CLOSING_START(B,U7) |
| -6.30 | TRACK_LOST(A,U4) |
| -6.25 | TRACK_APPEARED_FRONT(A,U5); CLOSING_START(A,U5) |
| -6.20 | CLOSING_END(B,U1); TRACK_LOST(B,U1) |
| -6.10 | TRACK_LOST(B,U7) |
| -5.95 | TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(B,U6); TRACK_LOST(B,U2) |
| -5.90 | CLOSING_END(A,U1) |
| -5.85 | CUT_IN_FROM_RIGHT_END(A,U1); CRITICAL_TTC_END(A,U1) |
| -5.15 | TRACK_LOST(B,U5) |
| -5.10 | TRACK_LOST(B,U6) |
| -5.00 | TRACK_APPEARED_RIGHT(B,U1) |
| -4.85 | TRACK_LOST(A,U6) |
| -4.70 | TRACK_LOST(A,U5) |
| -4.30 | TRACK_LOST(A,U1) |
| -3.10 | TRACK_LOST(B,U1) |
| -3.05 | CRITICAL_TTC_START(A,U3) |
| -2.90 | CUT_IN_FROM_RIGHT_START(A,U3) |
| -2.70 | CLOSING_END(B,U3); TRACK_LOST(B,U3) |
| -2.40 | CLOSING_END(A,U3) |
| -2.35 | CRITICAL_TTC_END(A,U3) |
| -2.30 | CUT_IN_FROM_RIGHT_END(A,U3) |
| -1.90 | TRACK_APPEARED_FRONT(A,U8); CLOSING_START(A,U8) |
| -1.85 | TRACK_APPEARED_RIGHT(B,U9); CLOSING_START(B,U9) |
| -1.80 | TRACK_APPEARED_RIGHT(B,U10); CLOSING_START(B,U10) |
| -1.65 | TRACK_APPEARED_RIGHT(A,U10); CLOSING_START(A,U10) |
| -1.55 | TRACK_APPEARED_RIGHT(B,U3) |
| -1.35 | CRITICAL_TTC_START(A,B) |
| -1.00 | TRACK_LOST(A,U8) |
| -0.95 | TRACK_APPEARED_FRONT(A,U9); CLOSING_START(A,U9) |
| -0.90 | CRITICAL_TTC_START(B,A); TRACK_LOST(A,U3) |
| -0.85 | CLOSING_START(A,B) |
| -0.80 | CLOSING_START(B,A) |
| -0.45 | CRITICAL_TTC_START(A,U9) |
| -0.05 | CRITICAL_TTC_START(A,U10) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(A,B) |
| +0.05 | CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.30 | CRITICAL_TTC_END(A,U10) |
| +0.60 | CLOSING_END(B,A); EGO_PATH_ENTRY(B,A) |
| +0.70 | TRACK_LOST(B,U3) |
| +0.80 | CLOSING_END(B,U10); CLOSING_END(B,U9) |
| +0.90 | CLOSING_END(A,U10) |
| +0.95 | CLOSING_END(A,U9) |
| +1.00 | EGO_PATH_EXIT(B,A) |
| +1.10 | CRITICAL_TTC_END(A,U9); MOVING_END(B); STOP_START(B) |
| +1.20 | MOVING_END(A); STOP_START(A) |
| +1.35 | TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3) |
| +2.05 | TRACK_APPEARED_RIGHT(A,U3); EGO_PATH_ENTRY(B,A); CLOSING_START(A,U3) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): critical TTC already active before the cut-in: CRITICAL_TTC_START 1.80 <= CUT_IN_FROM_RIGHT_START 1.95 (+0.15 s) [local times; t_global: cut_in -6.55, critical_ttc_start -6.70, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 7.15, COLLISION with B 8.50 (+1.35 s); EGO_PATH_ENTRY 8.50 after critical TTC (+1.35 s) [local times; t_global: critical_ttc_start -1.35, ego_path_entry +0.00, collision +0.00]
- A's track_004 (unidentified U3): critical TTC already active before the cut-in: CRITICAL_TTC_START 5.45 <= CUT_IN_FROM_RIGHT_START 5.60 (+0.15 s) [local times; t_global: cut_in -2.90, critical_ttc_start -3.05, collision +0.00]
- A's track_007#segment_2 (unidentified U9): CRITICAL_TTC_START 8.05, COLLISION 8.50 (+0.45 s) [local times; t_global: critical_ttc_start -0.45, collision +0.00]
- A's track_008 (unidentified U10): CRITICAL_TTC_START 8.45, COLLISION 8.50 (+0.05 s) [local times; t_global: critical_ttc_start -0.05, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.60, COLLISION with A 8.50 (+0.90 s); EGO_PATH_ENTRY 9.10 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -0.90, ego_path_entry +0.60, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -8.50 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g07 TRACK_APPEARED_RIGHT(A,U2) (A:e05)<br>g10 CLOSING_START(A,U1) (A:e06) | ego: not yet observed |
| -8.50 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g08 TRACK_APPEARED_RIGHT(B,A) (B:e04)<br>g09 TRACK_APPEARED_RIGHT(B,U1) (B:e03)<br>g11 CLOSING_START(B,U1) (B:e05) | ego: not yet observed |
| -8.50 | A | g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g48 TRACK_LOST(A,U1) (A:e24) | ego: not yet observed |
| -8.50 | A | g07 TRACK_APPEARED_RIGHT(A,U2) (A:e05)<br>g24 TRACK_LOST(A,U2) (A:e11) | ego: not yet observed |
| -8.50 | B | g09 TRACK_APPEARED_RIGHT(B,U1) (B:e03)<br>g11 CLOSING_START(B,U1) (B:e05)<br>g34 CLOSING_END(B,U1) (B:e16)<br>g35 TRACK_LOST(B,U1) (B:e17) | ego: not yet observed |
| -8.50 | A | g10 CLOSING_START(A,U1) (A:e06)<br>g40 CLOSING_END(A,U1) (A:e19) | ego: not yet observed |
| -8.10 | B | g12 TRACK_APPEARED_RIGHT(B,U2) (B:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC? |
| -8.10 | B | g12 TRACK_APPEARED_RIGHT(B,U2) (B:e06)<br>g37 TRACK_APPEARED_RIGHT(B,U6) (B:e19)<br>g38 CLOSING_START(B,U6) (B:e20)<br>g39 TRACK_LOST(B,U2) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC? |
| -8.00 | B | g13 TRACK_APPEARED_RIGHT(B,U3) (B:e07)<br>g14 CLOSING_START(B,U3) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -8.00 | B | g13 TRACK_APPEARED_RIGHT(B,U3) (B:e07)<br>g15 TRACK_LOST(B,U3) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.65 | A | g16 TRACK_APPEARED_RIGHT(A,U3) (A:e07)<br>g17 CLOSING_START(A,U3) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state |
| -7.65 | A | g16 TRACK_APPEARED_RIGHT(A,U3) (A:e07)<br>g71 TRACK_LOST(A,U3) (A:e38) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state |
| -7.65 | A | g17 CLOSING_START(A,U3) (A:e08)<br>g54 CLOSING_END(A,U3) (A:e27) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state |
| -7.60 | A | g18 TRACK_APPEARED_FRONT(A,U4) (A:e09)<br>g20 CLOSING_START(A,U4) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, CRITICAL_TTC? |
| -7.60 | A | g18 TRACK_APPEARED_FRONT(A,U4) (A:e09)<br>g31 TRACK_LOST(A,U4) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, CRITICAL_TTC? |
| -7.60 | B | g19 TRACK_APPEARED_RIGHT(B,U3) (B:e10)<br>g21 CLOSING_START(B,U3) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 |
| -7.60 | B | g19 TRACK_APPEARED_RIGHT(B,U3) (B:e10)<br>g21 CLOSING_START(B,U3) (B:e11)<br>g52 CLOSING_END(B,U3) (B:e26)<br>g53 TRACK_LOST(B,U3) (B:e27) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 |
| -7.55 | B | g22 TRACK_APPEARED_RIGHT(B,U5) (B:e12)<br>g23 CLOSING_START(B,U5) (B:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 |
| -7.55 | B | g22 TRACK_APPEARED_RIGHT(B,U5) (B:e12)<br>g43 TRACK_LOST(B,U5) (B:e22) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 |
| -6.90 | A | g25 TRACK_APPEARED_FRONT(A,U6) (A:e12)<br>g26 CLOSING_START(A,U6) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_003 |
| -6.90 | A | g25 TRACK_APPEARED_FRONT(A,U6) (A:e12)<br>g46 TRACK_LOST(A,U6) (A:e22) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_003 |
| -6.70 | A | g27 CRITICAL_TTC_START(A,U1) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 |
| -6.70 | A | g27 CRITICAL_TTC_START(A,U1) (A:e14)<br>g28 CUT_IN_FROM_RIGHT_START(A,U1) (A:e15)<br>g41 CUT_IN_FROM_RIGHT_END(A,U1) (A:e20)<br>g42 CRITICAL_TTC_END(A,U1) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 |
| -6.55 | A | g28 CUT_IN_FROM_RIGHT_START(A,U1) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_004: CLOSING<br>track_005#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 |
| -6.35 | B | g29 TRACK_APPEARED_RIGHT(B,U7) (B:e14)<br>g30 CLOSING_START(B,U7) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_004 |
| -6.35 | B | g29 TRACK_APPEARED_RIGHT(B,U7) (B:e14)<br>g36 TRACK_LOST(B,U7) (B:e18) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_004 |
| -6.25 | A | g32 TRACK_APPEARED_FRONT(A,U5) (A:e17)<br>g33 CLOSING_START(A,U5) (A:e18) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1 |
| -6.25 | A | g32 TRACK_APPEARED_FRONT(A,U5) (A:e17)<br>g47 TRACK_LOST(A,U5) (A:e23) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_004: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_003, track_005#segment_1 |
| -5.95 | B | g37 TRACK_APPEARED_RIGHT(B,U6) (B:e19)<br>g44 TRACK_LOST(B,U6) (B:e23) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_007 |
| -5.00 | B | g45 TRACK_APPEARED_RIGHT(B,U1) (B:e24) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006, track_007, track_008 |
| -5.00 | B | g45 TRACK_APPEARED_RIGHT(B,U1) (B:e24)<br>g49 TRACK_LOST(B,U1) (B:e25) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006, track_007, track_008 |
| -3.05 | A | g50 CRITICAL_TTC_START(A,U3) (A:e25) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -3.05 | A | g50 CRITICAL_TTC_START(A,U3) (A:e25)<br>g55 CRITICAL_TTC_END(A,U3) (A:e28) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -2.90 | A | g51 CUT_IN_FROM_RIGHT_START(A,U3) (A:e26) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -2.90 | A | g51 CUT_IN_FROM_RIGHT_START(A,U3) (A:e26)<br>g56 CUT_IN_FROM_RIGHT_END(A,U3) (A:e29) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -1.90 | A | g57 TRACK_APPEARED_FRONT(A,U8) (A:e30)<br>g58 CLOSING_START(A,U8) (A:e31) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -1.90 | A | g57 TRACK_APPEARED_FRONT(A,U8) (A:e30)<br>g67 TRACK_LOST(A,U8) (A:e35) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -1.85 | B | g59 TRACK_APPEARED_RIGHT(B,U9) (B:e28)<br>g60 CLOSING_START(B,U9) (B:e29) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -1.85 | B | g60 CLOSING_START(B,U9) (B:e29)<br>g62 CLOSING_START(B,U10) (B:e31)<br>g89 CLOSING_END(B,U10) (B:e43)<br>g90 CLOSING_END(B,U9) (B:e42) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -1.80 | B | g61 TRACK_APPEARED_RIGHT(B,U10) (B:e30)<br>g62 CLOSING_START(B,U10) (B:e31) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -1.65 | A | g63 TRACK_APPEARED_RIGHT(A,U10) (A:e32)<br>g64 CLOSING_START(A,U10) (A:e33) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track_007#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -1.65 | A | g64 CLOSING_START(A,U10) (A:e33)<br>g91 CLOSING_END(A,U10) (A:e49) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track_007#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -1.55 | B | g65 TRACK_APPEARED_RIGHT(B,U3) (B:e32) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -1.55 | B | g65 TRACK_APPEARED_RIGHT(B,U3) (B:e32)<br>g88 TRACK_LOST(B,U3) (B:e41) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING, CRITICAL_TTC?<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -1.35 | A | g66 CRITICAL_TTC_START(A,B) (A:e34) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track_007#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -1.35 | A | g66 CRITICAL_TTC_START(A,B) (A:e34)<br>g76 COLLISION(A,B) (A:e42)<br>g77 CRITICAL_TTC_END(A,B) (A:e43)<br>g79 EGO_PATH_ENTRY(A,B) (A:e44) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: no active state<br>track_007#segment_1: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006 |
| -0.95 | A | g68 TRACK_APPEARED_FRONT(A,U9) (A:e36)<br>g69 CLOSING_START(A,U9) (A:e37) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_004: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| -0.95 | A | g69 CLOSING_START(A,U9) (A:e37)<br>g92 CLOSING_END(A,U9) (A:e50) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_004: no active state<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| -0.90 | B | g70 CRITICAL_TTC_START(B,A) (B:e33) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -0.90 | B | g70 CRITICAL_TTC_START(B,A) (B:e33)<br>g76 COLLISION(A,B) (B:e35)<br>g78 CRITICAL_TTC_END(B,A) (B:e36) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -0.85 | A | g72 CLOSING_START(A,B) (A:e39) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_007#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| -0.85 | A | g72 CLOSING_START(A,B) (A:e39)<br>g80 CLOSING_END(A,B) (A:e45)<br>g81 THROTTLE_END(A) (A:e46)<br>g83 BRAKE_START(A) (A:e47) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_007#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| -0.80 | B | g73 CLOSING_START(B,A) (B:e34) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -0.80 | B | g73 CLOSING_START(B,A) (B:e34)<br>g86 CLOSING_END(B,A) (B:e39)<br>g87 EGO_PATH_ENTRY(B,A) (B:e40) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| -0.45 | A | g74 CRITICAL_TTC_START(A,U9) (A:e40) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| -0.45 | A | g74 CRITICAL_TTC_START(A,U9) (A:e40)<br>g94 CRITICAL_TTC_END(A,U9) (A:e51) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007#segment_2: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| -0.05 | A | g75 CRITICAL_TTC_START(A,U10) (A:e41) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| -0.05 | A | g75 CRITICAL_TTC_START(A,U10) (A:e41)<br>g85 CRITICAL_TTC_END(A,U10) (A:e48) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| +0.05 | B | g82 THROTTLE_END(B) (B:e37)<br>g84 BRAKE_START(B) (B:e38) | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| +0.60 | B | g87 EGO_PATH_ENTRY(B,A) (B:e40)<br>g93 EGO_PATH_EXIT(B,A) (B:e44) | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009 |
| +1.10 | B | g95 MOVING_END(B) (B:e45)<br>g96 STOP_START(B) (B:e46) | ego: MOVING, BRAKE<br>track_002: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 |
| +1.20 | A | g97 MOVING_END(A) (A:e52)<br>g98 STOP_START(A) (A:e53) | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| +1.35 | B | g99 TRACK_APPEARED_RIGHT(B,U3) (B:e47)<br>g100 CLOSING_START(B,U3) (B:e48) | ego: STOP, BRAKE<br>track_002: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 |
| +2.05 | A | g101 TRACK_APPEARED_RIGHT(A,U3) (A:e54)<br>g103 CLOSING_START(A,U3) (A:e55) | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_007#segment_2: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1 |
| +2.05 | B | g102 EGO_PATH_ENTRY(B,A) (B:e49) | ego: STOP, BRAKE<br>track_002: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_012 |

## Plain-language reading

- 8.50 s before the reference collision, A started moving (already the case when first observed).
- 8.50 s before the reference collision, B started moving (already the case when first observed).
- 8.50 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 8.50 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 8.50 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 8.50 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 8.50 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its right.
- 8.50 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 8.50 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 8.50 s before the reference collision, A observed anonymous road user U1 start closing in (already the case when first observed).
- 8.50 s before the reference collision, B observed anonymous road user U1 start closing in (already the case when first observed).
- 8.10 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 8.00 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 8.00 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 7.75 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 7.65 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 7.65 s before the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
- 7.60 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared in front of it.
- 7.60 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 7.60 s before the reference collision, A observed anonymous road user U4 start closing in (already the case when first observed).
- 7.60 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 7.55 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its right.
- 7.55 s before the reference collision, B observed anonymous road user U5 start closing in (already the case when first observed).
- 7.25 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 6.90 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared in front of it.
- 6.90 s before the reference collision, A observed anonymous road user U6 start closing in (already the case when first observed).
- 6.70 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 6.55 s before the reference collision, A observed anonymous road user U1 cutting in from the right.
- 6.35 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 6.35 s before the reference collision, B observed anonymous road user U7 start closing in (already the case when first observed).
- 6.30 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 6.25 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared in front of it.
- 6.25 s before the reference collision, A observed anonymous road user U5 start closing in (already the case when first observed).
- 6.20 s before the reference collision, B observed anonymous road user U1 stop closing in.
- 6.20 s before the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 6.10 s before the reference collision, B's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 5.95 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 5.95 s before the reference collision, B observed anonymous road user U6 start closing in (already the case when first observed).
- 5.95 s before the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 5.90 s before the reference collision, A observed anonymous road user U1 stop closing in.
- 5.85 s before the reference collision, A observed anonymous road user U1's cut-in from the right settle.
- 5.85 s before the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 5.15 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 5.10 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 5.00 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 4.85 s before the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 4.70 s before the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 4.30 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 3.10 s before the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 3.05 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 2.90 s before the reference collision, A observed anonymous road user U3 cutting in from the right.
- 2.70 s before the reference collision, B observed anonymous road user U3 stop closing in.
- 2.70 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.40 s before the reference collision, A observed anonymous road user U3 stop closing in.
- 2.35 s before the reference collision, A's time-to-contact with anonymous road user U3 stopped being critical.
- 2.30 s before the reference collision, A observed anonymous road user U3's cut-in from the right settle.
- 1.90 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared in front of it.
- 1.90 s before the reference collision, A observed anonymous road user U8 start closing in (already the case when first observed).
- 1.85 s before the reference collision, B's radar started tracking anonymous road user U9, which appeared on its right.
- 1.85 s before the reference collision, B observed anonymous road user U9 start closing in (already the case when first observed).
- 1.80 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared on its right.
- 1.80 s before the reference collision, B observed anonymous road user U10 start closing in (already the case when first observed).
- 1.65 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 1.65 s before the reference collision, A observed anonymous road user U10 start closing in (already the case when first observed).
- 1.55 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 1.35 s before the reference collision, A's time-to-contact with B became critical.
- 1.00 s before the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 0.95 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared in front of it.
- 0.95 s before the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 0.90 s before the reference collision, B's time-to-contact with A became critical.
- 0.90 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.85 s before the reference collision, A observed B start closing in.
- 0.80 s before the reference collision, B observed A start closing in.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U9 became critical.
- 0.05 s before the reference collision, A's time-to-contact with anonymous road user U10 became critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 745, B: 745 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B enter its forward path corridor.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.30 s after the reference collision, A's time-to-contact with anonymous road user U10 stopped being critical.
- 0.60 s after the reference collision, B observed A stop closing in.
- 0.60 s after the reference collision, B observed A enter its forward path corridor.
- 0.70 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, B observed anonymous road user U10 stop closing in.
- 0.80 s after the reference collision, B observed anonymous road user U9 stop closing in.
- 0.90 s after the reference collision, A observed anonymous road user U10 stop closing in.
- 0.95 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 1.00 s after the reference collision, B observed A leave its forward path corridor.
- 1.10 s after the reference collision, A's time-to-contact with anonymous road user U9 stopped being critical.
- 1.10 s after the reference collision, B stopped moving.
- 1.10 s after the reference collision, B came to a stop.
- 1.20 s after the reference collision, A stopped moving.
- 1.20 s after the reference collision, A came to a stop.
- 1.35 s after the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 1.35 s after the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 2.05 s after the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 2.05 s after the reference collision, B observed A enter its forward path corridor.
- 2.05 s after the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
