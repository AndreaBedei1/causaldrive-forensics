# Global graph - S14/run_0_surrounded

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_003 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_003 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_002, B:track_006 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_004#segment_1, A:track_004#segment_3, B:track_001 |
| U13 | anonymous_road_user | anonymous; observed by A as A:track_004#segment_2 |
| U9 | anonymous_road_user | anonymous; observed by A as A:track_005 |
| U14 | anonymous_road_user | anonymous; observed by A as A:track_006 |
| U15 | anonymous_road_user | anonymous; observed by A as A:track_007 |
| U11 | anonymous_road_user | anonymous; observed by A, B as A:track_008, B:track_011 |
| U6 | anonymous_road_user | anonymous; observed by A, B as A:track_009, B:track_007 |
| U10 | anonymous_road_user | anonymous; observed by A, B as A:track_010, B:track_010 |
| U17 | anonymous_road_user | anonymous; observed by A, B as A:track_011, B:track_014 |
| U4 | anonymous_road_user | anonymous; observed by B as B:track_004 |
| U5 | anonymous_road_user | anonymous; observed by B as B:track_005 |
| U7 | anonymous_road_user | anonymous; observed by B as B:track_008 |
| U8 | anonymous_road_user | anonymous; observed by B as B:track_009 |
| U12 | anonymous_road_user | anonymous; observed by B as B:track_012 |
| U16 | anonymous_road_user | anonymous; observed by B as B:track_013 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e22 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e23 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 254.4 vs 254.4 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 2.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.53 m/s for reference)<br>clearance at the contact 2.02 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U1: A:track_001, B:track_003 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 11.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.50 m/s for reference)<br>clearance at the contact 10.96 m (beyond 3.50 m: confidence factor 0.05)<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_002, track_003)<br>anonymous road user U2: A:track_002, B:track_006 |
| A:track_003 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.36 m/s for reference)<br>clearance at the contact 0.12 m<br>the only compatible track of A touching it at the contact (clearance 0.12 m; track_001, track_002 at 2.04 m, 11.06 m) |
| A:track_004#segment_1 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.95 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.2 m -> 10.3 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.42 m/s for reference)<br>clearance at the contact 10.32 m (beyond 3.50 m: confidence factor 0.08)<br>anonymous road user U3: B:track_001, A:track_004#segment_1, A:track_004#segment_3 |
| A:track_004#segment_2 | U13 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.90 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 10.2 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.57 m/s for reference)<br>clearance at the contact 10.07 m (beyond 3.50 m: confidence factor 0.09)<br>anonymous road user U13: A:track_004#segment_2 |
| A:track_004#segment_3 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: B:track_001, A:track_004#segment_1, A:track_004#segment_3 |
| A:track_005 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 2.95 s before the matched collision<br>continuous up to the contact: last observed 0.50 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 10.3 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.52 m/s for reference)<br>clearance at the contact 9.76 m (beyond 3.50 m: confidence factor 0.11)<br>anonymous road user U9: A:track_005 |
| A:track_006 | U14 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.1 m -> 42.0 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.30 m/s for reference)<br>clearance at the contact 41.88 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U14: A:track_006 |
| A:track_007 | U15 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.30 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.8 m -> 18.4 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.82 m/s for reference)<br>clearance at the contact 18.27 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U15: A:track_007 |
| A:track_008 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.15 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.3 m -> 26.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 26.24 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U11: B:track_011, A:track_008 |
| A:track_009 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 11.13 m (beyond 3.50 m: confidence factor 0.04)<br>anonymous road user U6: B:track_007, A:track_009 |
| A:track_010 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U10: B:track_010, A:track_010 |
| A:track_011 | U17 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 2.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U17: B:track_014, A:track_011 |
| B:track_001 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.5 m -> 9.9 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.04 m/s for reference)<br>clearance at the contact 9.92 m (beyond 3.50 m: confidence factor 0.10)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>anonymous road user U3: B:track_001, A:track_004#segment_1, A:track_004#segment_3 |
| B:track_002 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.8 m -> 0.8 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.66 m/s for reference)<br>clearance at the contact 0.80 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 240 samples; 100% within 3 sigma) at A's own velocity |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.2 m -> 2.8 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.13 m/s for reference)<br>clearance at the contact 2.78 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>anonymous road user U1: A:track_001, B:track_003 |
| B:track_004 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.8 m -> 28.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U4: B:track_004 |
| B:track_005 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 1.05 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 6.6 m -> 7.2 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.09 m/s for reference)<br>anonymous road user U5: B:track_005 |
| B:track_006 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.1 m -> 10.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.06 m/s for reference)<br>clearance at the contact 10.53 m (beyond 3.50 m: confidence factor 0.06)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>anonymous road user U2: A:track_002, B:track_006 |
| B:track_007 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.6 m -> 11.2 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.07 m/s for reference)<br>clearance at the contact 11.13 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>anonymous road user U6: B:track_007, A:track_009 |
| B:track_008 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.60 s before the matched collision<br>lost 3.95 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.5 m -> 28.0 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_008 |
| B:track_009 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.55 s before the matched collision<br>lost 5.55 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 44.6 m -> 44.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U8: B:track_009 |
| B:track_010 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.7 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.10 m/s for reference)<br>clearance at the contact 26.71 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>anonymous road user U10: B:track_010, A:track_010 |
| B:track_011 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.2 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.06 m/s for reference)<br>clearance at the contact 26.18 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>anonymous road user U11: B:track_011, A:track_008 |
| B:track_012 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.75 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.7 m -> 42.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.04 m/s for reference)<br>clearance at the contact 42.56 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_006, track_007, track_010, track_011, track_012)<br>anonymous road user U12: B:track_012 |
| B:track_013 | U16 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U16: B:track_013 |
| B:track_014 | U17 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U17: B:track_014, A:track_011 |

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
| g09 | -7.75 | TRACK_APPEARED_LEFT | B | U4 | B:e04 @ 0.00, B:e14 @ 3.65 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g10 | -7.75 | TRACK_APPEARED_LEFT | B | U5 | B:e05 @ 0.00, B:e19 @ 6.70 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g11 | -7.75 | TRACK_APPEARED_RIGHT | B | A | B:e06 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g12 | -7.75 | TRACK_APPEARED_RIGHT | B | U1 | B:e07 @ 0.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -7.70 | TRACK_APPEARED_LEFT | A | U3 | A:e06 @ 0.05, A:e11 @ 6.80 | initial_in_ego_path=False; source_track=track_004#segment_1; aggregation=entity_state_union; source_tracks=['A:track_004#segment_1'] |
| g14 | -7.70 | TRACK_APPEARED_LEFT | B | U2 | B:e08 @ 0.05 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g15 | -7.70 | TRACK_APPEARED_RIGHT | B | U6 | B:e09 @ 0.05 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g16 | -7.60 | TRACK_APPEARED_RIGHT | B | U7 | B:e10 @ 0.15, B:e15 @ 3.80 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g17 | -7.55 | TRACK_APPEARED_FRONT | B | U8 | B:e11 @ 0.20, B:e13 @ 2.20 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g18 | -7.25 | CRITICAL_TTC_START | A | U1 | A:e07 @ 0.50, A:e34 @ 9.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g19 | -7.25 | CRITICAL_TTC_START | B | U3 | B:e12 @ 0.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g20 | -5.55 | TRACK_LOST | B | U8 | B:e13 @ 2.20 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g21 | -4.10 | TRACK_LOST | B | U4 | B:e14 @ 3.65 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g22 | -3.95 | TRACK_LOST | B | U7 | B:e15 @ 3.80 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g23 | -2.95 | TRACK_APPEARED_LEFT | A | U9 | A:e08 @ 4.80, A:e16 @ 7.25 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g24 | -1.40 | CRITICAL_TTC_START | A | B | A:e09 @ 6.35, A:e23 @ 7.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g25 | -1.35 | TRACK_APPEARED_LEFT | B | U10 | B:e16 @ 6.40, B:e34 @ 9.35 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g26 | -1.25 | TRACK_APPEARED_RIGHT | B | U11 | B:e17 @ 6.50, B:e32 @ 8.85 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g27 | -1.15 | TRACK_APPEARED_FRONT | B | U12 | B:e18 @ 6.60, B:e20 @ 7.00 | initial_in_ego_path=False; source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g28 | -1.05 | CRITICAL_TTC_START | A | U3 | A:e10 @ 6.70 | source_track=track_004#segment_1; aggregation=entity_state_union; source_tracks=['A:track_004#segment_1'] |
| g29 | -1.05 | TRACK_LOST | B | U5 | B:e19 @ 6.70 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g30 | -0.95 | TRACK_LOST | A | U3 | A:e11 @ 6.80 | source_track=track_004#segment_1; aggregation=entity_state_union; source_tracks=['A:track_004#segment_1'] |
| g31 | -0.90 | TRACK_APPEARED_LEFT | A | U13 | A:e12 @ 6.85, A:e29 @ 8.45 | initial_in_ego_path=False; source_track=track_004#segment_2; aggregation=entity_state_union; source_tracks=['A:track_004#segment_2'] |
| g32 | -0.80 | CLOSING_START | A | B | A:e13 @ 6.95, A:e28 @ 7.90 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g33 | -0.75 | TRACK_LOST | B | U12 | B:e20 @ 7.00 | source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g34 | -0.70 | TRACK_APPEARED_FRONT | A | U14 | A:e14 @ 7.05, A:e21 @ 7.70 | initial_in_ego_path=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g35 | -0.70 | TRACK_APPEARED_LEFT | A | U15 | A:e15 @ 7.05, A:e17 @ 7.45 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g36 | -0.70 | CRITICAL_TTC_START | B | A | B:e21 @ 7.05, B:e24 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g37 | -0.60 | CLOSING_START | B | A | B:e22 @ 7.15, B:e26 @ 7.85 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g38 | -0.50 | TRACK_LOST | A | U9 | A:e16 @ 7.25 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g39 | -0.30 | TRACK_LOST | A | U15 | A:e17 @ 7.45 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g40 | -0.15 | EGO_PATH_EXIT | A | U14 | A:e18 @ 7.60 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g41 | -0.15 | TRACK_APPEARED_RIGHT | A | U11 | A:e19 @ 7.60 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g42 | -0.15 | CRITICAL_TTC_START | A | U2 | A:e20 @ 7.60 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g43 | -0.05 | TRACK_LOST | A | U14 | A:e21 @ 7.70 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g44 | 0.00 | COLLISION | - | A, B | A:e22 @ 7.75, B:e23 @ 7.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 254.40, B 254.40 |
| g45 | 0.00 | CRITICAL_TTC_END | A | B | A:e23 @ 7.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g46 | 0.00 | CRITICAL_TTC_END | B | A | B:e24 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g47 | 0.00 | TRACK_APPEARED_RIGHT | A | U6 | A:e24 @ 7.75 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g48 | 0.05 | THROTTLE_END | A | - | A:e25 @ 7.80 |  |
| g49 | 0.05 | THROTTLE_END | B | - | B:e25 @ 7.80 |  |
| g50 | 0.05 | EGO_PATH_ENTRY | A | U6 | A:e26 @ 7.80 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g51 | 0.10 | CLOSING_END | B | A | B:e26 @ 7.85 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g52 | 0.10 | TRACK_APPEARED_LEFT | B | U16 | B:e27 @ 7.85, B:e33 @ 9.00 | initial_in_ego_path=False; source_track=track_013; aggregation=entity_state_union; source_tracks=['B:track_013'] |
| g53 | 0.10 | EGO_PATH_ENTRY | A | B | A:e27 @ 7.85 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g54 | 0.15 | CLOSING_END | A | B | A:e28 @ 7.90 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g55 | 0.25 | EGO_PATH_ENTRY | B | U10 | B:e28 @ 8.00 | geometry=estimated_body; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g56 | 0.40 | TRACK_APPEARED_FRONT | B | U17 | B:e29 @ 8.15 | initial_in_ego_path=True; source_track=track_014; aggregation=entity_state_union; source_tracks=['B:track_014'] |
| g57 | 0.70 | TRACK_LOST | A | U13 | A:e29 @ 8.45 | source_track=track_004#segment_2; aggregation=entity_state_union; source_tracks=['A:track_004#segment_2'] |
| g58 | 0.75 | TRACK_APPEARED_FRONT | A | U3 | A:e30 @ 8.50 | initial_in_ego_path=True; source_track=track_004#segment_3; aggregation=entity_state_union; source_tracks=['A:track_004#segment_3'] |
| g59 | 0.80 | TRACK_APPEARED_LEFT | A | U10 | A:e31 @ 8.55 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g60 | 0.95 | EGO_PATH_ENTRY | B | U2 | B:e30 @ 8.70, B:e38 @ 10.60 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g61 | 0.95 | CRITICAL_TTC_START | B | U2 | B:e31 @ 8.70, B:e37 @ 10.60 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g62 | 1.10 | TRACK_LOST | B | U11 | B:e32 @ 8.85 | source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g63 | 1.25 | EGO_PATH_ENTRY | A | U11 | A:e32 @ 9.00, A:e41 @ 11.55 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g64 | 1.25 | CRITICAL_TTC_START | A | U3 | A:e33 @ 9.00 | source_track=track_004#segment_3; aggregation=entity_state_union; source_tracks=['A:track_004#segment_3'] |
| g65 | 1.25 | TRACK_LOST | B | U16 | B:e33 @ 9.00 | source_track=track_013; aggregation=entity_state_union; source_tracks=['B:track_013'] |
| g66 | 1.40 | CRITICAL_TTC_END | A | U1 | A:e34 @ 9.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g67 | 1.40 | EGO_PATH_EXIT | A | U1 | A:e35 @ 9.15 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g68 | 1.60 | TRACK_LOST | B | U10 | B:e34 @ 9.35 | source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g69 | 1.80 | EGO_PATH_EXIT | B | U17 | B:e35 @ 9.55 | geometry=estimated_body; source_track=track_014; aggregation=entity_state_union; source_tracks=['B:track_014'] |
| g70 | 2.20 | TRACK_APPEARED_LEFT | A | U17 | A:e36 @ 9.95, A:e40 @ 11.15 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g71 | 2.40 | CRITICAL_TTC_START | A | U6 | A:e37 @ 10.15 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g72 | 2.80 | CRITICAL_TTC_START | A | U1 | A:e38 @ 10.55 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g73 | 2.80 | CRITICAL_TTC_START | B | U6 | B:e36 @ 10.55 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g74 | 2.85 | CRITICAL_TTC_END | B | U2 | B:e37 @ 10.60 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g75 | 2.85 | EGO_PATH_EXIT | B | U2 | B:e38 @ 10.60 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g76 | 3.20 | EGO_PATH_ENTRY | A | U1 | A:e39 @ 10.95 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g77 | 3.30 | EGO_PATH_ENTRY | B | U6 | B:e39 @ 11.05 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g78 | 3.35 | CLOSING_START | B | U1 | B:e40 @ 11.10 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g79 | 3.40 | TRACK_LOST | A | U17 | A:e40 @ 11.15 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g80 | 3.55 | CRITICAL_TTC_START | B | U1 | B:e41 @ 11.30 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g81 | 3.80 | EGO_PATH_EXIT | A | U11 | A:e41 @ 11.55 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g82 | 3.85 | EGO_PATH_EXIT | A | U3 | A:e42 @ 11.60 | geometry=estimated_body; source_track=track_004#segment_3; aggregation=entity_state_union; source_tracks=['A:track_004#segment_3'] |
| g83 | 3.85 | CLOSING_START | B | A | B:e42 @ 11.60 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g84 | 4.05 | EGO_PATH_ENTRY | B | U1 | B:e43 @ 11.80 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |

## Edges

```
    g01 --PRECEDES--> g13
    g01 --PRECEDES--> g14
    g01 --PRECEDES--> g15
    g02 --PRECEDES--> g13
    g02 --PRECEDES--> g14
    g02 --PRECEDES--> g15
    g03 --PRECEDES--> g13
    g03 --PRECEDES--> g14
    g03 --PRECEDES--> g15
    g04 --PRECEDES--> g13
    g04 --PRECEDES--> g14
    g04 --PRECEDES--> g15
    g05 --PRECEDES--> g13
    g05 --PRECEDES--> g14
    g05 --PRECEDES--> g15
    g06 --PRECEDES--> g13
    g06 --PRECEDES--> g14
    g06 --PRECEDES--> g15
    g07 --PRECEDES--> g13
    g07 --PRECEDES--> g14
    g07 --PRECEDES--> g15
    g08 --PRECEDES--> g13
    g08 --PRECEDES--> g14
    g08 --PRECEDES--> g15
    g09 --PRECEDES--> g13
    g09 --PRECEDES--> g14
    g09 --PRECEDES--> g15
    g10 --PRECEDES--> g13
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
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
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g43
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g44 --PRECEDES--> g50
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g45 --PRECEDES--> g50
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g48 --PRECEDES--> g53
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g52 --PRECEDES--> g54
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g62
    g62 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g62 --PRECEDES--> g65
    g63 --PRECEDES--> g66
    g63 --PRECEDES--> g67
    g64 --PRECEDES--> g66
    g64 --PRECEDES--> g67
    g65 --PRECEDES--> g66
    g65 --PRECEDES--> g67
    g66 --PRECEDES--> g68
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g69 --PRECEDES--> g70
    g70 --PRECEDES--> g71
    g71 --PRECEDES--> g72
    g71 --PRECEDES--> g73
    g72 --PRECEDES--> g74
    g72 --PRECEDES--> g75
    g73 --PRECEDES--> g74
    g73 --PRECEDES--> g75
    g74 --PRECEDES--> g76
    g75 --PRECEDES--> g76
    g76 --PRECEDES--> g77
    g77 --PRECEDES--> g78
    g78 --PRECEDES--> g79
    g79 --PRECEDES--> g80
    g80 --PRECEDES--> g81
    g81 --PRECEDES--> g82
    g81 --PRECEDES--> g83
    g82 --PRECEDES--> g84
    g83 --PRECEDES--> g84
    g05 --SAME_TRACK--> g18
    g07 --SAME_TRACK--> g24
    g13 --SAME_TRACK--> g28
    g13 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g32
    g23 --SAME_TRACK--> g38
    g35 --SAME_TRACK--> g39
    g34 --SAME_TRACK--> g40
    g08 --SAME_TRACK--> g42
    g34 --SAME_TRACK--> g43
    g07 --SAME_TRACK--> g45
    g47 --SAME_TRACK--> g50
    g07 --SAME_TRACK--> g53
    g07 --SAME_TRACK--> g54
    g31 --SAME_TRACK--> g57
    g41 --SAME_TRACK--> g63
    g58 --SAME_TRACK--> g64
    g05 --SAME_TRACK--> g66
    g05 --SAME_TRACK--> g67
    g47 --SAME_TRACK--> g71
    g05 --SAME_TRACK--> g72
    g05 --SAME_TRACK--> g76
    g70 --SAME_TRACK--> g79
    g41 --SAME_TRACK--> g81
    g58 --SAME_TRACK--> g82
    g06 --SAME_TRACK--> g19
    g17 --SAME_TRACK--> g20
    g09 --SAME_TRACK--> g21
    g16 --SAME_TRACK--> g22
    g10 --SAME_TRACK--> g29
    g27 --SAME_TRACK--> g33
    g11 --SAME_TRACK--> g36
    g11 --SAME_TRACK--> g37
    g11 --SAME_TRACK--> g46
    g11 --SAME_TRACK--> g51
    g25 --SAME_TRACK--> g55
    g14 --SAME_TRACK--> g60
    g14 --SAME_TRACK--> g61
    g26 --SAME_TRACK--> g62
    g52 --SAME_TRACK--> g65
    g25 --SAME_TRACK--> g68
    g56 --SAME_TRACK--> g69
    g15 --SAME_TRACK--> g73
    g14 --SAME_TRACK--> g74
    g14 --SAME_TRACK--> g75
    g15 --SAME_TRACK--> g77
    g12 --SAME_TRACK--> g78
    g12 --SAME_TRACK--> g80
    g11 --SAME_TRACK--> g83
    g12 --SAME_TRACK--> g84
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U1); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U4); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1) |
| -7.70 | TRACK_APPEARED_LEFT(A,U3); TRACK_APPEARED_LEFT(B,U2); TRACK_APPEARED_RIGHT(B,U6) |
| -7.60 | TRACK_APPEARED_RIGHT(B,U7) |
| -7.55 | TRACK_APPEARED_FRONT(B,U8) |
| -7.25 | CRITICAL_TTC_START(A,U1); CRITICAL_TTC_START(B,U3) |
| -5.55 | TRACK_LOST(B,U8) |
| -4.10 | TRACK_LOST(B,U4) |
| -3.95 | TRACK_LOST(B,U7) |
| -2.95 | TRACK_APPEARED_LEFT(A,U9) |
| -1.40 | CRITICAL_TTC_START(A,B) |
| -1.35 | TRACK_APPEARED_LEFT(B,U10) |
| -1.25 | TRACK_APPEARED_RIGHT(B,U11) |
| -1.15 | TRACK_APPEARED_FRONT(B,U12) |
| -1.05 | CRITICAL_TTC_START(A,U3); TRACK_LOST(B,U5) |
| -0.95 | TRACK_LOST(A,U3) |
| -0.90 | TRACK_APPEARED_LEFT(A,U13) |
| -0.80 | CLOSING_START(A,B) |
| -0.75 | TRACK_LOST(B,U12) |
| -0.70 | TRACK_APPEARED_FRONT(A,U14); TRACK_APPEARED_LEFT(A,U15); CRITICAL_TTC_START(B,A) |
| -0.60 | CLOSING_START(B,A) |
| -0.50 | TRACK_LOST(A,U9) |
| -0.30 | TRACK_LOST(A,U15) |
| -0.15 | EGO_PATH_EXIT(A,U14); TRACK_APPEARED_RIGHT(A,U11); CRITICAL_TTC_START(A,U2) |
| -0.05 | TRACK_LOST(A,U14) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); TRACK_APPEARED_RIGHT(A,U6) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); EGO_PATH_ENTRY(A,U6) |
| +0.10 | CLOSING_END(B,A); TRACK_APPEARED_LEFT(B,U16); EGO_PATH_ENTRY(A,B) |
| +0.15 | CLOSING_END(A,B) |
| +0.25 | EGO_PATH_ENTRY(B,U10) |
| +0.40 | TRACK_APPEARED_FRONT(B,U17) |
| +0.70 | TRACK_LOST(A,U13) |
| +0.75 | TRACK_APPEARED_FRONT(A,U3) |
| +0.80 | TRACK_APPEARED_LEFT(A,U10) |
| +0.95 | EGO_PATH_ENTRY(B,U2); CRITICAL_TTC_START(B,U2) |
| +1.10 | TRACK_LOST(B,U11) |
| +1.25 | EGO_PATH_ENTRY(A,U11); CRITICAL_TTC_START(A,U3); TRACK_LOST(B,U16) |
| +1.40 | CRITICAL_TTC_END(A,U1); EGO_PATH_EXIT(A,U1) |
| +1.60 | TRACK_LOST(B,U10) |
| +1.80 | EGO_PATH_EXIT(B,U17) |
| +2.20 | TRACK_APPEARED_LEFT(A,U17) |
| +2.40 | CRITICAL_TTC_START(A,U6) |
| +2.80 | CRITICAL_TTC_START(A,U1); CRITICAL_TTC_START(B,U6) |
| +2.85 | CRITICAL_TTC_END(B,U2); EGO_PATH_EXIT(B,U2) |
| +3.20 | EGO_PATH_ENTRY(A,U1) |
| +3.30 | EGO_PATH_ENTRY(B,U6) |
| +3.35 | CLOSING_START(B,U1) |
| +3.40 | TRACK_LOST(A,U17) |
| +3.55 | CRITICAL_TTC_START(B,U1) |
| +3.80 | EGO_PATH_EXIT(A,U11) |
| +3.85 | EGO_PATH_EXIT(A,U3); CLOSING_START(B,A) |
| +4.05 | EGO_PATH_ENTRY(B,U1) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s); EGO_PATH_ENTRY 10.95 after critical TTC (+10.45 s) [local times; t_global: critical_ttc_start -7.25, ego_path_entry +3.20, collision +0.00]
- A's track_002 (unidentified U2): CRITICAL_TTC_START 7.60, COLLISION 7.75 (+0.15 s) [local times; t_global: critical_ttc_start -0.15, collision +0.00]
- A's track_003 (B): CRITICAL_TTC_START 6.35, COLLISION with B 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -1.40, ego_path_entry +0.10, collision +0.00]
- A's track_004#segment_1 (unidentified U3): CRITICAL_TTC_START 6.70, COLLISION 7.75 (+1.05 s) [local times; t_global: critical_ttc_start -1.05, collision +0.00]
- A's track_004#segment_3 (unidentified U3): CRITICAL_TTC_START 9.00 [local times; t_global: critical_ttc_start +1.25]
- A's track_008 (unidentified U11): EGO_PATH_ENTRY 9.00, no critical TTC [local times; t_global: ego_path_entry +1.25]
- A's track_009 (unidentified U6): CRITICAL_TTC_START 10.15; EGO_PATH_ENTRY 7.80 before critical TTC (-2.35 s) [local times; t_global: critical_ttc_start +2.40, ego_path_entry +0.05]
- B's track_001 (unidentified U3): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.05, COLLISION with A 7.75 (+0.70 s) [local times; t_global: critical_ttc_start -0.70, collision +0.00]
- B's track_003 (unidentified U1): CRITICAL_TTC_START 11.30; EGO_PATH_ENTRY 11.80 after critical TTC (+0.50 s) [local times; t_global: critical_ttc_start +3.55, ego_path_entry +4.05]
- B's track_006 (unidentified U2): CRITICAL_TTC_START 8.70; EGO_PATH_ENTRY 8.70 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start +0.95, ego_path_entry +0.95]
- B's track_007 (unidentified U6): CRITICAL_TTC_START 10.55; EGO_PATH_ENTRY 11.05 after critical TTC (+0.50 s) [local times; t_global: critical_ttc_start +2.80, ego_path_entry +3.30]
- B's track_010 (unidentified U10): EGO_PATH_ENTRY 8.00, no critical TTC [local times; t_global: ego_path_entry +0.25]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U1) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,B) (A:e05)<br>g08 TRACK_APPEARED_LEFT(A,U2) (A:e04) | ego: not yet observed |
| -7.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U3) (B:e03)<br>g09 TRACK_APPEARED_LEFT(B,U4) (B:e04)<br>g10 TRACK_APPEARED_LEFT(B,U5) (B:e05)<br>g11 TRACK_APPEARED_RIGHT(B,A) (B:e06)<br>g12 TRACK_APPEARED_RIGHT(B,U1) (B:e07) | ego: not yet observed |
| -7.75 | B | g09 TRACK_APPEARED_LEFT(B,U4) (B:e04)<br>g21 TRACK_LOST(B,U4) (B:e14) | ego: not yet observed |
| -7.75 | B | g10 TRACK_APPEARED_LEFT(B,U5) (B:e05)<br>g29 TRACK_LOST(B,U5) (B:e19) | ego: not yet observed |
| -7.70 | A | g13 TRACK_APPEARED_LEFT(A,U3) (A:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.70 | A | g13 TRACK_APPEARED_LEFT(A,U3) (A:e06)<br>g30 TRACK_LOST(A,U3) (A:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.70 | B | g14 TRACK_APPEARED_LEFT(B,U2) (B:e08)<br>g15 TRACK_APPEARED_RIGHT(B,U6) (B:e09) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -7.60 | B | g16 TRACK_APPEARED_RIGHT(B,U7) (B:e10) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? |
| -7.60 | B | g16 TRACK_APPEARED_RIGHT(B,U7) (B:e10)<br>g22 TRACK_LOST(B,U7) (B:e15) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC? |
| -7.55 | B | g17 TRACK_APPEARED_FRONT(B,U8) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC? |
| -7.55 | B | g17 TRACK_APPEARED_FRONT(B,U8) (B:e11)<br>g20 TRACK_LOST(B,U8) (B:e13) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC? |
| -7.25 | A | g18 CRITICAL_TTC_START(A,U1) (A:e07) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004#segment_1: CRITICAL_TTC? |
| -7.25 | A | g18 CRITICAL_TTC_START(A,U1) (A:e07)<br>g66 CRITICAL_TTC_END(A,U1) (A:e34)<br>g67 EGO_PATH_EXIT(A,U1) (A:e35) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004#segment_1: CRITICAL_TTC? |
| -7.25 | B | g19 CRITICAL_TTC_START(B,U3) (B:e12) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track_009: CRITICAL_TTC? |
| -2.95 | A | g23 TRACK_APPEARED_LEFT(A,U9) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state |
| -2.95 | A | g23 TRACK_APPEARED_LEFT(A,U9) (A:e08)<br>g38 TRACK_LOST(A,U9) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state |
| -1.40 | A | g24 CRITICAL_TTC_START(A,B) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state<br>track_005: no active state |
| -1.40 | A | g24 CRITICAL_TTC_START(A,B) (A:e09)<br>g44 COLLISION(A,B) (A:e22)<br>g45 CRITICAL_TTC_END(A,B) (A:e23)<br>g47 TRACK_APPEARED_RIGHT(A,U6) (A:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004#segment_1: no active state<br>track_005: no active state |
| -1.35 | B | g25 TRACK_APPEARED_LEFT(B,U10) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_004, track_008, track_009 |
| -1.35 | B | g25 TRACK_APPEARED_LEFT(B,U10) (B:e16)<br>g68 TRACK_LOST(B,U10) (B:e34) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_004, track_008, track_009 |
| -1.25 | B | g26 TRACK_APPEARED_RIGHT(B,U11) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_008, track_009 |
| -1.25 | B | g26 TRACK_APPEARED_RIGHT(B,U11) (B:e17)<br>g62 TRACK_LOST(B,U11) (B:e32) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_008, track_009 |
| -1.15 | B | g27 TRACK_APPEARED_FRONT(B,U12) (B:e18) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track_011: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_008, track_009 |
| -1.15 | B | g27 TRACK_APPEARED_FRONT(B,U12) (B:e18)<br>g33 TRACK_LOST(B,U12) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: CRITICAL_TTC?<br>track_011: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_008, track_009 |
| -1.05 | A | g28 CRITICAL_TTC_START(A,U3) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_1: no active state<br>track_005: no active state |
| -0.90 | A | g31 TRACK_APPEARED_LEFT(A,U13) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.90 | A | g31 TRACK_APPEARED_LEFT(A,U13) (A:e12)<br>g57 TRACK_LOST(A,U13) (A:e29) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.80 | A | g32 CLOSING_START(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.80 | A | g32 CLOSING_START(A,B) (A:e13)<br>g54 CLOSING_END(A,B) (A:e28) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.70 | A | g34 TRACK_APPEARED_FRONT(A,U14) (A:e14)<br>g35 TRACK_APPEARED_LEFT(A,U15) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.70 | A | g34 TRACK_APPEARED_FRONT(A,U14) (A:e14)<br>g43 TRACK_LOST(A,U14) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.70 | A | g35 TRACK_APPEARED_LEFT(A,U15) (A:e15)<br>g39 TRACK_LOST(A,U15) (A:e17) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: no active state<br>track lost, states UNKNOWN: track_004#segment_1 |
| -0.70 | B | g36 CRITICAL_TTC_START(B,A) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| -0.70 | B | g36 CRITICAL_TTC_START(B,A) (B:e21)<br>g44 COLLISION(A,B) (B:e23)<br>g46 CRITICAL_TTC_END(B,A) (B:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| -0.60 | B | g37 CLOSING_START(B,A) (B:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| -0.60 | B | g37 CLOSING_START(B,A) (B:e22)<br>g51 CLOSING_END(B,A) (B:e26)<br>g52 TRACK_APPEARED_LEFT(B,U16) (B:e27) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| -0.15 | A | g40 EGO_PATH_EXIT(A,U14) (A:e18)<br>g41 TRACK_APPEARED_RIGHT(A,U11) (A:e19)<br>g42 CRITICAL_TTC_START(A,U2) (A:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_007 |
| +0.05 | A | g48 THROTTLE_END(A) (A:e25)<br>g50 EGO_PATH_ENTRY(A,U6) (A:e26) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_006, track_007 |
| +0.05 | B | g49 THROTTLE_END(B) (B:e25) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| +0.10 | B | g52 TRACK_APPEARED_LEFT(B,U16) (B:e27)<br>g65 TRACK_LOST(B,U16) (B:e33) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| +0.10 | A | g53 EGO_PATH_ENTRY(A,B) (A:e27) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_004#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_005, track_006, track_007 |
| +0.25 | B | g55 EGO_PATH_ENTRY(B,U10) (B:e28) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| +0.40 | B | g56 TRACK_APPEARED_FRONT(B,U17) (B:e29) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_011: no active state<br>track_013: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| +0.75 | A | g58 TRACK_APPEARED_FRONT(A,U3) (A:e30) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +0.80 | A | g59 TRACK_APPEARED_LEFT(A,U10) (A:e31) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +0.95 | B | g60 EGO_PATH_ENTRY(B,U2) (B:e30)<br>g61 CRITICAL_TTC_START(B,U2) (B:e31) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_011: no active state<br>track_013: no active state<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| +0.95 | B | g60 EGO_PATH_ENTRY(B,U2) (B:e30)<br>g61 CRITICAL_TTC_START(B,U2) (B:e31)<br>g74 CRITICAL_TTC_END(B,U2) (B:e37)<br>g75 EGO_PATH_EXIT(B,U2) (B:e38) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: no active state<br>track_010: IN_EGO_PATH<br>track_011: no active state<br>track_013: no active state<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_012 |
| +1.25 | A | g63 EGO_PATH_ENTRY(A,U11) (A:e32)<br>g64 CRITICAL_TTC_START(A,U3) (A:e33) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +1.25 | A | g63 EGO_PATH_ENTRY(A,U11) (A:e32)<br>g81 EGO_PATH_EXIT(A,U11) (A:e41) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +1.80 | B | g69 EGO_PATH_EXIT(B,U17) (B:e35) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_014: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 |
| +2.20 | A | g70 TRACK_APPEARED_LEFT(A,U17) (A:e36) | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +2.20 | A | g70 TRACK_APPEARED_LEFT(A,U17) (A:e36)<br>g79 TRACK_LOST(A,U17) (A:e40) | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +2.40 | A | g71 CRITICAL_TTC_START(A,U6) (A:e37) | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track_011: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +2.80 | A | g72 CRITICAL_TTC_START(A,U1) (A:e38) | ego: MOVING<br>track_001: no active state<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +2.80 | B | g73 CRITICAL_TTC_START(B,U6) (B:e36) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 |
| +3.20 | A | g76 EGO_PATH_ENTRY(A,U1) (A:e39) | ego: MOVING<br>track_001: CRITICAL_TTC<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007 |
| +3.30 | B | g77 EGO_PATH_ENTRY(B,U6) (B:e39) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: CRITICAL_TTC<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 |
| +3.35 | B | g78 CLOSING_START(B,U1) (B:e40) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 |
| +3.55 | B | g80 CRITICAL_TTC_START(B,U1) (B:e41) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 |
| +3.85 | A | g82 EGO_PATH_EXIT(A,U3) (A:e42) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_004#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004#segment_1, track_004#segment_2, track_005, track_006, track_007, track_011 |
| +3.85 | B | g83 CLOSING_START(B,A) (B:e42) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 |
| +4.05 | B | g84 EGO_PATH_ENTRY(B,U1) (B:e43) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING, CRITICAL_TTC<br>track_006: no active state<br>track_007: CRITICAL_TTC, IN_EGO_PATH<br>track_014: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009, track_010, track_011, track_012, track_013 |

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
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.70 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its left.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 7.60 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 7.55 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared in front of it.
- 7.25 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U3 became critical.
- 5.55 s before the reference collision, B's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 4.10 s before the reference collision, B's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 3.95 s before the reference collision, B's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 2.95 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared on its left.
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared on its left.
- 1.25 s before the reference collision, B's radar started tracking anonymous road user U11, which appeared on its right.
- 1.15 s before the reference collision, B's radar started tracking anonymous road user U12, which appeared in front of it.
- 1.05 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 1.05 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 0.95 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.90 s before the reference collision, A's radar started tracking anonymous road user U13, which appeared on its left.
- 0.80 s before the reference collision, A observed B start closing in.
- 0.75 s before the reference collision, B's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 0.70 s before the reference collision, A's radar started tracking anonymous road user U14, which appeared in front of it.
- 0.70 s before the reference collision, A's radar started tracking anonymous road user U15, which appeared on its left.
- 0.70 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, B observed A start closing in.
- 0.50 s before the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 0.30 s before the reference collision, A's radar lost anonymous road user U15 (its states are UNKNOWN from then on, not ended).
- 0.15 s before the reference collision, A observed anonymous road user U14 leave its forward path corridor.
- 0.15 s before the reference collision, A's radar started tracking anonymous road user U11, which appeared on its right.
- 0.15 s before the reference collision, A's time-to-contact with anonymous road user U2 became critical.
- 0.05 s before the reference collision, A's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 254, B: 254 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A's radar started tracking anonymous road user U6, which appeared on its right.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A observed anonymous road user U6 enter its forward path corridor.
- 0.10 s after the reference collision, B observed A stop closing in.
- 0.10 s after the reference collision, B's radar started tracking anonymous road user U16, which appeared on its left.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.15 s after the reference collision, A observed B stop closing in.
- 0.25 s after the reference collision, B observed anonymous road user U10 enter its forward path corridor.
- 0.40 s after the reference collision, B's radar started tracking anonymous road user U17, which appeared in front of it.
- 0.70 s after the reference collision, A's radar lost anonymous road user U13 (its states are UNKNOWN from then on, not ended).
- 0.75 s after the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 0.80 s after the reference collision, A's radar started tracking anonymous road user U10, which appeared on its left.
- 0.95 s after the reference collision, B observed anonymous road user U2 enter its forward path corridor.
- 0.95 s after the reference collision, B's time-to-contact with anonymous road user U2 became critical.
- 1.10 s after the reference collision, B's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 1.25 s after the reference collision, A observed anonymous road user U11 enter its forward path corridor.
- 1.25 s after the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 1.25 s after the reference collision, B's radar lost anonymous road user U16 (its states are UNKNOWN from then on, not ended).
- 1.40 s after the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 1.40 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 1.60 s after the reference collision, B's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 1.80 s after the reference collision, B observed anonymous road user U17 leave its forward path corridor.
- 2.20 s after the reference collision, A's radar started tracking anonymous road user U17, which appeared on its left.
- 2.40 s after the reference collision, A's time-to-contact with anonymous road user U6 became critical.
- 2.80 s after the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 2.80 s after the reference collision, B's time-to-contact with anonymous road user U6 became critical.
- 2.85 s after the reference collision, B's time-to-contact with anonymous road user U2 stopped being critical.
- 2.85 s after the reference collision, B observed anonymous road user U2 leave its forward path corridor.
- 3.20 s after the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 3.30 s after the reference collision, B observed anonymous road user U6 enter its forward path corridor.
- 3.35 s after the reference collision, B observed anonymous road user U1 start closing in.
- 3.40 s after the reference collision, A's radar lost anonymous road user U17 (its states are UNKNOWN from then on, not ended).
- 3.55 s after the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 3.80 s after the reference collision, A observed anonymous road user U11 leave its forward path corridor.
- 3.85 s after the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 3.85 s after the reference collision, B observed A start closing in.
- 4.05 s after the reference collision, B observed anonymous road user U1 enter its forward path corridor.
