# Global graph - S14/run_0_surrounded

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_003 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_003 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_002, B:track_008 |
| U9 | anonymous_road_user | anonymous; observed by A as A:track_004 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_005, B:track_001 |
| U13 | anonymous_road_user | anonymous; observed by A as A:track_006 |
| U14 | anonymous_road_user | anonymous; observed by A as A:track_007 |
| U10 | anonymous_road_user | anonymous; observed by A, B as A:track_008, B:track_011 |
| U7 | anonymous_road_user | anonymous; observed by A, B as A:track_009, B:track_007 |
| U11 | anonymous_road_user | anonymous; observed by A, B as A:track_010, B:track_012 |
| U15 | anonymous_road_user | anonymous; observed by A as A:track_011 |
| U4 | anonymous_road_user | anonymous; observed by B as B:track_004 |
| U5 | anonymous_road_user | anonymous; observed by B as B:track_005, B:track_014 |
| U6 | anonymous_road_user | anonymous; observed by B as B:track_006, B:track_010 |
| U8 | anonymous_road_user | anonymous; observed by B as B:track_009 |
| U12 | anonymous_road_user | anonymous; observed by B as B:track_013 |
| U16 | anonymous_road_user | anonymous; observed by B as B:track_015 |
| U17 | anonymous_road_user | anonymous; observed by B as B:track_016 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e20 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e25 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 254.4 vs 254.4 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 2.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.53 m/s over 3.0 s<br>clearance at the contact 2.02 m<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>anonymous road user U1: A:track_001, B:track_003 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 11.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.55 m/s over 3.0 s<br>clearance at the contact 11.12 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>anonymous road user U2: A:track_002, B:track_008 |
| A:track_003 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.38 m/s over 3.0 s<br>clearance at the contact 0.13 m<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma, over 240 samples; 100% within 3 sigma) at B's own velocity (median difference 0.15 m/s) |
| A:track_004 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 3.30 s before the matched collision<br>continuous up to the contact: last observed 0.50 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 10.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.51 m/s over 2.5 s<br>clearance at the contact 9.81 m (beyond 3.50 m: confidence factor 0.11)<br>anonymous road user U9: A:track_004 |
| A:track_005 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.90 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.2 m -> 10.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.71 m/s over 0.9 s<br>clearance at the contact 9.98 m (beyond 3.50 m: confidence factor 0.10)<br>anonymous road user U3: B:track_001, A:track_005 |
| A:track_006 | U13 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.00 s before the matched collision<br>continuous up to the contact: last observed 0.30 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.9 m -> 18.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.89 m/s over 0.7 s<br>clearance at the contact 18.30 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>anonymous road user U13: A:track_006 |
| A:track_007 | U14 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.1 m -> 41.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 0.7 s<br>clearance at the contact 41.86 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U14: A:track_007 |
| A:track_008 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.35 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.3 m -> 26.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.60 m/s over 0.3 s<br>clearance at the contact 26.19 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U10: B:track_011, A:track_008 |
| A:track_009 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.15 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.9 m -> 10.9 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 10.86 m (beyond 3.50 m: confidence factor 0.05)<br>anonymous road user U7: B:track_007, A:track_009 |
| A:track_010 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U11: B:track_012, A:track_010 |
| A:track_011 | U15 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U15: A:track_011 |
| B:track_001 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.5 m -> 9.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.03 m/s over 3.0 s<br>clearance at the contact 9.92 m (beyond 3.50 m: confidence factor 0.10)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U3: B:track_001, A:track_005 |
| B:track_002 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.76 m/s over 3.0 s<br>clearance at the contact 0.71 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma, over 240 samples; 94% within 3 sigma) at A's own velocity (median difference 0.22 m/s) |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.2 m -> 2.8 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 2.80 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U1: A:track_001, B:track_003 |
| B:track_004 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.7 m -> 28.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U4: B:track_004 |
| B:track_005 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 1.05 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 6.6 m -> 7.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.10 m/s over 2.0 s<br>anonymous road user U5: B:track_005, B:track_014 |
| B:track_006 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.05 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.4 m -> 27.9 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_006, B:track_010 |
| B:track_007 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.6 m -> 11.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 3.0 s<br>clearance at the contact 11.11 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U7: B:track_007, A:track_009 |
| B:track_008 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 10.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.07 m/s over 3.0 s<br>clearance at the contact 10.56 m (beyond 3.50 m: confidence factor 0.06)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U2: A:track_002, B:track_008 |
| B:track_009 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 5.55 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 44.6 m -> 44.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U8: B:track_009 |
| B:track_010 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 3.95 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 30.2 m -> 29.8 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_006, B:track_010 |
| B:track_011 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 1.4 s<br>clearance at the contact 26.19 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U10: B:track_011, A:track_008 |
| B:track_012 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.3 s<br>clearance at the contact 26.70 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U11: B:track_012, A:track_010 |
| B:track_013 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.5 m -> 41.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.2 s<br>clearance at the contact 41.94 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U12: B:track_013 |
| B:track_014 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U5: B:track_005, B:track_014 |
| B:track_015 | U16 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.60 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U16: B:track_015 |
| B:track_016 | U17 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.95 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U17: B:track_016 |

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
| g09 | -7.75 | TRACK_APPEARED_LEFT | B | U4 | B:e04 @ 0.00, B:e16 @ 3.65 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g10 | -7.75 | TRACK_APPEARED_LEFT | B | U5 | B:e05 @ 0.00, B:e22 @ 6.70 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g11 | -7.75 | TRACK_APPEARED_RIGHT | B | A | B:e06 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g12 | -7.75 | TRACK_APPEARED_RIGHT | B | U1 | B:e07 @ 0.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -7.75 | TRACK_APPEARED_RIGHT | B | U6 | B:e08 @ 0.00, B:e17 @ 3.70, B:e09 @ 0.00, B:e18 @ 3.80 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006', 'B:track_010'] |
| g14 | -7.70 | TRACK_APPEARED_FRONT | B | U8 | B:e10 @ 0.05, B:e15 @ 2.20 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g15 | -7.70 | TRACK_APPEARED_LEFT | B | U2 | B:e11 @ 0.05 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g16 | -7.70 | TRACK_APPEARED_RIGHT | B | U7 | B:e12 @ 0.05 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g17 | -7.25 | CRITICAL_TTC_START | A | U1 | A:e06 @ 0.50, A:e26 @ 9.05 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g18 | -7.25 | CRITICAL_TTC_START | B | U3 | B:e13 @ 0.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g19 | -7.15 | CLOSING_START | B | U6 | B:e14 @ 0.60 | source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g20 | -5.55 | TRACK_LOST | B | U8 | B:e15 @ 2.20 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g21 | -4.10 | TRACK_LOST | B | U4 | B:e16 @ 3.65 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g22 | -3.95 | TRACK_LOST | B | U6 | B:e17 @ 3.70, B:e18 @ 3.80 | source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_006', 'B:track_010'] |
| g23 | -3.30 | TRACK_APPEARED_LEFT | A | U9 | A:e07 @ 4.45, A:e13 @ 7.25 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g24 | -1.40 | TRACK_APPEARED_RIGHT | B | U10 | B:e19 @ 6.35, B:e33 @ 8.85 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g25 | -1.40 | CRITICAL_TTC_START | A | B | A:e08 @ 6.35, A:e21 @ 7.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g26 | -1.35 | TRACK_APPEARED_LEFT | B | U11 | B:e20 @ 6.40, B:e36 @ 9.35 | initial_in_ego_path=False; source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g27 | -1.15 | TRACK_APPEARED_FRONT | B | U12 | B:e21 @ 6.60 | initial_in_ego_path=False; source_track=track_013; aggregation=entity_state_union; source_tracks=['B:track_013'] |
| g28 | -1.05 | TRACK_LOST | B | U5 | B:e22 @ 6.70 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g29 | -1.00 | TRACK_APPEARED_LEFT | A | U13 | A:e09 @ 6.75, A:e16 @ 7.45 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g30 | -0.90 | TRACK_APPEARED_LEFT | A | U3 | A:e10 @ 6.85 | initial_in_ego_path=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g31 | -0.80 | CLOSING_START | A | B | A:e11 @ 6.95, A:e24 @ 7.90 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g32 | -0.75 | CRITICAL_TTC_START | B | A | B:e23 @ 7.00, B:e26 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g33 | -0.70 | TRACK_APPEARED_FRONT | A | U14 | A:e12 @ 7.05, A:e19 @ 7.70 | initial_in_ego_path=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g34 | -0.70 | CLOSING_START | B | A | B:e24 @ 7.05, B:e27 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g35 | -0.50 | TRACK_LOST | A | U9 | A:e13 @ 7.25 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g36 | -0.40 | CRITICAL_TTC_START | A | U3 | A:e14 @ 7.35 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g37 | -0.35 | TRACK_APPEARED_RIGHT | A | U10 | A:e15 @ 7.40 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g38 | -0.30 | TRACK_LOST | A | U13 | A:e16 @ 7.45 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g39 | -0.15 | EGO_PATH_EXIT | A | U14 | A:e17 @ 7.60 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g40 | -0.15 | TRACK_APPEARED_RIGHT | A | U7 | A:e18 @ 7.60 | initial_in_ego_path=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g41 | -0.05 | TRACK_LOST | A | U14 | A:e19 @ 7.70 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g42 | 0.00 | COLLISION | - | A, B | A:e20 @ 7.75, B:e25 @ 7.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 254.40, B 254.40 |
| g43 | 0.00 | CRITICAL_TTC_END | A | B | A:e21 @ 7.75 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g44 | 0.00 | CRITICAL_TTC_END | B | A | B:e26 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g45 | 0.00 | CLOSING_END | B | A | B:e27 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g46 | 0.05 | THROTTLE_END | A | - | A:e22 @ 7.80 |  |
| g47 | 0.05 | THROTTLE_END | B | - | B:e28 @ 7.80 |  |
| g48 | 0.10 | TRACK_APPEARED_LEFT | B | U5 | B:e29 @ 7.85, B:e32 @ 8.05 | initial_in_ego_path=False; source_track=track_014; aggregation=entity_state_union; source_tracks=['B:track_014'] |
| g49 | 0.10 | EGO_PATH_ENTRY | A | B | A:e23 @ 7.85 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g50 | 0.10 | EGO_PATH_ENTRY | B | U12 | B:e30 @ 7.85, B:e37 @ 9.60 | geometry=estimated_body; source_track=track_013; aggregation=entity_state_union; source_tracks=['B:track_013'] |
| g51 | 0.15 | CLOSING_END | A | B | A:e24 @ 7.90 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g52 | 0.25 | EGO_PATH_ENTRY | B | U11 | B:e31 @ 8.00 | geometry=estimated_body; source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g53 | 0.30 | TRACK_LOST | B | U5 | B:e32 @ 8.05 | source_track=track_014; aggregation=entity_state_union; source_tracks=['B:track_014'] |
| g54 | 0.70 | TRACK_APPEARED_LEFT | A | U11 | A:e25 @ 8.45 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g55 | 1.10 | TRACK_LOST | B | U10 | B:e33 @ 8.85 | source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g56 | 1.30 | CRITICAL_TTC_END | A | U1 | A:e26 @ 9.05 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g57 | 1.30 | EGO_PATH_EXIT | A | U1 | A:e27 @ 9.05 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g58 | 1.35 | EGO_PATH_ENTRY | A | U10 | A:e28 @ 9.10, A:e36 @ 11.55 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g59 | 1.40 | EGO_PATH_EXIT | A | U7 | A:e29 @ 9.15 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g60 | 1.45 | EGO_PATH_ENTRY | B | U2 | B:e34 @ 9.20, B:e41 @ 10.55 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g61 | 1.45 | CRITICAL_TTC_START | B | U2 | B:e35 @ 9.20, B:e40 @ 10.55 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g62 | 1.60 | TRACK_LOST | B | U11 | B:e36 @ 9.35 | source_track=track_012; aggregation=entity_state_union; source_tracks=['B:track_012'] |
| g63 | 1.75 | TRACK_APPEARED_LEFT | A | U15 | A:e30 @ 9.50, A:e35 @ 11.15 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g64 | 1.85 | EGO_PATH_EXIT | B | U12 | B:e37 @ 9.60 | geometry=estimated_body; source_track=track_013; aggregation=entity_state_union; source_tracks=['B:track_013'] |
| g65 | 2.35 | CUT_IN_FROM_RIGHT_START | B | U7 | B:e38 @ 10.10 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g66 | 2.40 | CRITICAL_TTC_START | A | U7 | A:e31 @ 10.15 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g67 | 2.50 | EGO_PATH_ENTRY | A | U7 | A:e32 @ 10.25 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g68 | 2.70 | CUT_IN_FROM_RIGHT_START | B | U1 | B:e39 @ 10.45 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g69 | 2.75 | CRITICAL_TTC_START | A | U1 | A:e33 @ 10.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g70 | 2.80 | CRITICAL_TTC_END | B | U2 | B:e40 @ 10.55 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g71 | 2.80 | EGO_PATH_EXIT | B | U2 | B:e41 @ 10.55 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g72 | 2.95 | CRITICAL_TTC_START | B | U7 | B:e42 @ 10.70 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g73 | 3.25 | EGO_PATH_ENTRY | A | U1 | A:e34 @ 11.00 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g74 | 3.35 | CLOSING_START | B | U1 | B:e43 @ 11.10 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g75 | 3.40 | EGO_PATH_ENTRY | B | U7 | B:e44 @ 11.15 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g76 | 3.40 | TRACK_LOST | A | U15 | A:e35 @ 11.15 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g77 | 3.55 | CRITICAL_TTC_START | B | U1 | B:e45 @ 11.30 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g78 | 3.60 | TRACK_APPEARED_LEFT | B | U16 | B:e46 @ 11.35, B:e47 @ 11.65 | initial_in_ego_path=False; source_track=track_015; aggregation=entity_state_union; source_tracks=['B:track_015'] |
| g79 | 3.80 | EGO_PATH_EXIT | A | U10 | A:e36 @ 11.55 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g80 | 3.85 | EGO_PATH_EXIT | A | U3 | A:e37 @ 11.60 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g81 | 3.90 | TRACK_LOST | B | U16 | B:e47 @ 11.65 | source_track=track_015; aggregation=entity_state_union; source_tracks=['B:track_015'] |
| g82 | 3.95 | TRACK_APPEARED_FRONT | B | U17 | B:e48 @ 11.70 | initial_in_ego_path=True; source_track=track_016; aggregation=entity_state_union; source_tracks=['B:track_016'] |
| g83 | 4.05 | EGO_PATH_ENTRY | B | U1 | B:e49 @ 11.80 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g84 | 4.20 | EGO_PATH_EXIT | B | U17 | B:e50 @ 11.95 | geometry=estimated_body; source_track=track_016; aggregation=entity_state_union; source_tracks=['B:track_016'] |

## Edges

```
    g01 --PRECEDES--> g14
    g01 --PRECEDES--> g15
    g01 --PRECEDES--> g16
    g02 --PRECEDES--> g14
    g02 --PRECEDES--> g15
    g02 --PRECEDES--> g16
    g03 --PRECEDES--> g14
    g03 --PRECEDES--> g15
    g03 --PRECEDES--> g16
    g04 --PRECEDES--> g14
    g04 --PRECEDES--> g15
    g04 --PRECEDES--> g16
    g05 --PRECEDES--> g14
    g05 --PRECEDES--> g15
    g05 --PRECEDES--> g16
    g06 --PRECEDES--> g14
    g06 --PRECEDES--> g15
    g06 --PRECEDES--> g16
    g07 --PRECEDES--> g14
    g07 --PRECEDES--> g15
    g07 --PRECEDES--> g16
    g08 --PRECEDES--> g14
    g08 --PRECEDES--> g15
    g08 --PRECEDES--> g16
    g09 --PRECEDES--> g14
    g09 --PRECEDES--> g15
    g09 --PRECEDES--> g16
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g10 --PRECEDES--> g16
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g11 --PRECEDES--> g16
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
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
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g51
    g51 --PRECEDES--> g52
    g52 --PRECEDES--> g53
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g62
    g62 --PRECEDES--> g63
    g63 --PRECEDES--> g64
    g64 --PRECEDES--> g65
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g69 --PRECEDES--> g70
    g69 --PRECEDES--> g71
    g70 --PRECEDES--> g72
    g71 --PRECEDES--> g72
    g72 --PRECEDES--> g73
    g73 --PRECEDES--> g74
    g74 --PRECEDES--> g75
    g74 --PRECEDES--> g76
    g75 --PRECEDES--> g77
    g76 --PRECEDES--> g77
    g77 --PRECEDES--> g78
    g78 --PRECEDES--> g79
    g79 --PRECEDES--> g80
    g80 --PRECEDES--> g81
    g81 --PRECEDES--> g82
    g82 --PRECEDES--> g83
    g83 --PRECEDES--> g84
    g05 --SAME_TRACK--> g17
    g07 --SAME_TRACK--> g25
    g07 --SAME_TRACK--> g31
    g23 --SAME_TRACK--> g35
    g30 --SAME_TRACK--> g36
    g29 --SAME_TRACK--> g38
    g33 --SAME_TRACK--> g39
    g33 --SAME_TRACK--> g41
    g07 --SAME_TRACK--> g43
    g07 --SAME_TRACK--> g49
    g07 --SAME_TRACK--> g51
    g05 --SAME_TRACK--> g56
    g05 --SAME_TRACK--> g57
    g37 --SAME_TRACK--> g58
    g40 --SAME_TRACK--> g59
    g40 --SAME_TRACK--> g66
    g40 --SAME_TRACK--> g67
    g05 --SAME_TRACK--> g69
    g05 --SAME_TRACK--> g73
    g63 --SAME_TRACK--> g76
    g37 --SAME_TRACK--> g79
    g30 --SAME_TRACK--> g80
    g06 --SAME_TRACK--> g18
    g13 --SAME_TRACK--> g19
    g14 --SAME_TRACK--> g20
    g09 --SAME_TRACK--> g21
    g13 --SAME_TRACK--> g22
    g10 --SAME_TRACK--> g28
    g11 --SAME_TRACK--> g32
    g11 --SAME_TRACK--> g34
    g11 --SAME_TRACK--> g44
    g11 --SAME_TRACK--> g45
    g27 --SAME_TRACK--> g50
    g26 --SAME_TRACK--> g52
    g48 --SAME_TRACK--> g53
    g24 --SAME_TRACK--> g55
    g15 --SAME_TRACK--> g60
    g15 --SAME_TRACK--> g61
    g26 --SAME_TRACK--> g62
    g27 --SAME_TRACK--> g64
    g16 --SAME_TRACK--> g65
    g12 --SAME_TRACK--> g68
    g15 --SAME_TRACK--> g70
    g15 --SAME_TRACK--> g71
    g16 --SAME_TRACK--> g72
    g12 --SAME_TRACK--> g74
    g16 --SAME_TRACK--> g75
    g12 --SAME_TRACK--> g77
    g78 --SAME_TRACK--> g81
    g12 --SAME_TRACK--> g83
    g82 --SAME_TRACK--> g84
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U1); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U4); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); TRACK_APPEARED_RIGHT(B,U6) |
| -7.70 | TRACK_APPEARED_FRONT(B,U8); TRACK_APPEARED_LEFT(B,U2); TRACK_APPEARED_RIGHT(B,U7) |
| -7.25 | CRITICAL_TTC_START(A,U1); CRITICAL_TTC_START(B,U3) |
| -7.15 | CLOSING_START(B,U6) |
| -5.55 | TRACK_LOST(B,U8) |
| -4.10 | TRACK_LOST(B,U4) |
| -3.95 | TRACK_LOST(B,U6) |
| -3.30 | TRACK_APPEARED_LEFT(A,U9) |
| -1.40 | TRACK_APPEARED_RIGHT(B,U10); CRITICAL_TTC_START(A,B) |
| -1.35 | TRACK_APPEARED_LEFT(B,U11) |
| -1.15 | TRACK_APPEARED_FRONT(B,U12) |
| -1.05 | TRACK_LOST(B,U5) |
| -1.00 | TRACK_APPEARED_LEFT(A,U13) |
| -0.90 | TRACK_APPEARED_LEFT(A,U3) |
| -0.80 | CLOSING_START(A,B) |
| -0.75 | CRITICAL_TTC_START(B,A) |
| -0.70 | TRACK_APPEARED_FRONT(A,U14); CLOSING_START(B,A) |
| -0.50 | TRACK_LOST(A,U9) |
| -0.40 | CRITICAL_TTC_START(A,U3) |
| -0.35 | TRACK_APPEARED_RIGHT(A,U10) |
| -0.30 | TRACK_LOST(A,U13) |
| -0.15 | EGO_PATH_EXIT(A,U14); TRACK_APPEARED_RIGHT(A,U7) |
| -0.05 | TRACK_LOST(A,U14) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B) |
| +0.10 | TRACK_APPEARED_LEFT(B,U5); EGO_PATH_ENTRY(A,B); EGO_PATH_ENTRY(B,U12) |
| +0.15 | CLOSING_END(A,B) |
| +0.25 | EGO_PATH_ENTRY(B,U11) |
| +0.30 | TRACK_LOST(B,U5) |
| +0.70 | TRACK_APPEARED_LEFT(A,U11) |
| +1.10 | TRACK_LOST(B,U10) |
| +1.30 | CRITICAL_TTC_END(A,U1); EGO_PATH_EXIT(A,U1) |
| +1.35 | EGO_PATH_ENTRY(A,U10) |
| +1.40 | EGO_PATH_EXIT(A,U7) |
| +1.45 | EGO_PATH_ENTRY(B,U2); CRITICAL_TTC_START(B,U2) |
| +1.60 | TRACK_LOST(B,U11) |
| +1.75 | TRACK_APPEARED_LEFT(A,U15) |
| +1.85 | EGO_PATH_EXIT(B,U12) |
| +2.35 | CUT_IN_FROM_RIGHT_START(B,U7) |
| +2.40 | CRITICAL_TTC_START(A,U7) |
| +2.50 | EGO_PATH_ENTRY(A,U7) |
| +2.70 | CUT_IN_FROM_RIGHT_START(B,U1) |
| +2.75 | CRITICAL_TTC_START(A,U1) |
| +2.80 | CRITICAL_TTC_END(B,U2); EGO_PATH_EXIT(B,U2) |
| +2.95 | CRITICAL_TTC_START(B,U7) |
| +3.25 | EGO_PATH_ENTRY(A,U1) |
| +3.35 | CLOSING_START(B,U1) |
| +3.40 | EGO_PATH_ENTRY(B,U7); TRACK_LOST(A,U15) |
| +3.55 | CRITICAL_TTC_START(B,U1) |
| +3.60 | TRACK_APPEARED_LEFT(B,U16) |
| +3.80 | EGO_PATH_EXIT(A,U10) |
| +3.85 | EGO_PATH_EXIT(A,U3) |
| +3.90 | TRACK_LOST(B,U16) |
| +3.95 | TRACK_APPEARED_FRONT(B,U17) |
| +4.05 | EGO_PATH_ENTRY(B,U1) |
| +4.20 | EGO_PATH_EXIT(B,U17) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s); EGO_PATH_ENTRY 11.00 after critical TTC (+10.50 s) [local times; t_global: critical_ttc_start -7.25, ego_path_entry +3.25, collision +0.00]
- A's track_003 (B): CRITICAL_TTC_START 6.35, COLLISION with B 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -1.40, ego_path_entry +0.10, collision +0.00]
- A's track_005 (unidentified U3): CRITICAL_TTC_START 7.35, COLLISION 7.75 (+0.40 s) [local times; t_global: critical_ttc_start -0.40, collision +0.00]
- A's track_008 (unidentified U10): EGO_PATH_ENTRY 9.10, no critical TTC [local times; t_global: ego_path_entry +1.35]
- A's track_009 (unidentified U7): CRITICAL_TTC_START 10.15; EGO_PATH_ENTRY 10.25 after critical TTC (+0.10 s) [local times; t_global: critical_ttc_start +2.40, ego_path_entry +2.50]
- B's track_001 (unidentified U3): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.00, COLLISION with A 7.75 (+0.75 s) [local times; t_global: critical_ttc_start -0.75, collision +0.00]
- B's track_003 (unidentified U1): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 10.45 < CRITICAL_TTC_START 11.30 (+0.85 s); EGO_PATH_ENTRY 11.80 after critical TTC (+0.50 s) [local times; t_global: cut_in +2.70, critical_ttc_start +3.55, ego_path_entry +4.05]
- B's track_007 (unidentified U7): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 10.10 < CRITICAL_TTC_START 10.70 (+0.60 s); EGO_PATH_ENTRY 11.15 after critical TTC (+0.45 s) [local times; t_global: cut_in +2.35, critical_ttc_start +2.95, ego_path_entry +3.40]
- B's track_008 (unidentified U2): CRITICAL_TTC_START 9.20; EGO_PATH_ENTRY 9.20 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start +1.45, ego_path_entry +1.45]
- B's track_012 (unidentified U11): EGO_PATH_ENTRY 8.00, no critical TTC [local times; t_global: ego_path_entry +0.25]
- B's track_013 (unidentified U12): EGO_PATH_ENTRY 7.85, no critical TTC [local times; t_global: ego_path_entry +0.10]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U1) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,B) (A:e05)<br>g08 TRACK_APPEARED_LEFT(A,U2) (A:e04) | ego: not yet observed |
| -7.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U3) (B:e03)<br>g09 TRACK_APPEARED_LEFT(B,U4) (B:e04)<br>g10 TRACK_APPEARED_LEFT(B,U5) (B:e05)<br>g11 TRACK_APPEARED_RIGHT(B,A) (B:e06)<br>g12 TRACK_APPEARED_RIGHT(B,U1) (B:e07)<br>g13 TRACK_APPEARED_RIGHT(B,U6) (B:e08)<br>g13 TRACK_APPEARED_RIGHT(B,U6) (B:e08) | ego: not yet observed |
| -7.75 | B | g09 TRACK_APPEARED_LEFT(B,U4) (B:e04)<br>g21 TRACK_LOST(B,U4) (B:e16) | ego: not yet observed |
| -7.75 | B | g10 TRACK_APPEARED_LEFT(B,U5) (B:e05)<br>g28 TRACK_LOST(B,U5) (B:e22) | ego: not yet observed |
| -7.75 | B | g13 TRACK_APPEARED_RIGHT(B,U6) (B:e08)<br>g22 TRACK_LOST(B,U6) (B:e17) | ego: not yet observed |
| -7.75 | B | g13 TRACK_APPEARED_RIGHT(B,U6) (B:e08)<br>g22 TRACK_LOST(B,U6) (B:e17) | ego: not yet observed |
| -7.70 | B | g14 TRACK_APPEARED_FRONT(B,U8) (B:e10)<br>g15 TRACK_APPEARED_LEFT(B,U2) (B:e11)<br>g16 TRACK_APPEARED_RIGHT(B,U7) (B:e12) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_010: CRITICAL_TTC? |
| -7.70 | B | g14 TRACK_APPEARED_FRONT(B,U8) (B:e10)<br>g20 TRACK_LOST(B,U8) (B:e15) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_010: CRITICAL_TTC? |
| -7.25 | A | g17 CRITICAL_TTC_START(A,U1) (A:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.25 | A | g17 CRITICAL_TTC_START(A,U1) (A:e06)<br>g56 CRITICAL_TTC_END(A,U1) (A:e26)<br>g57 EGO_PATH_EXIT(A,U1) (A:e27) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.25 | B | g18 CRITICAL_TTC_START(B,U3) (B:e13) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CRITICAL_TTC?<br>track_007: CRITICAL_TTC?<br>track_008: CRITICAL_TTC?<br>track_009: CRITICAL_TTC?<br>track_010: CRITICAL_TTC? |
| -7.15 | B | g19 CLOSING_START(B,U6) (B:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state |
| -3.30 | A | g23 TRACK_APPEARED_LEFT(A,U9) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state |
| -3.30 | A | g23 TRACK_APPEARED_LEFT(A,U9) (A:e07)<br>g35 TRACK_LOST(A,U9) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state |
| -1.40 | B | g24 TRACK_APPEARED_RIGHT(B,U10) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_009, track_010 |
| -1.40 | B | g24 TRACK_APPEARED_RIGHT(B,U10) (B:e19)<br>g55 TRACK_LOST(B,U10) (B:e33) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_009, track_010 |
| -1.40 | A | g25 CRITICAL_TTC_START(A,B) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| -1.40 | A | g25 CRITICAL_TTC_START(A,B) (A:e08)<br>g42 COLLISION(A,B) (A:e20)<br>g43 CRITICAL_TTC_END(A,B) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| -1.35 | B | g26 TRACK_APPEARED_LEFT(B,U11) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_009, track_010 |
| -1.35 | B | g26 TRACK_APPEARED_LEFT(B,U11) (B:e20)<br>g62 TRACK_LOST(B,U11) (B:e36) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_009, track_010 |
| -1.15 | B | g27 TRACK_APPEARED_FRONT(B,U12) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: CRITICAL_TTC?<br>track_012: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_009, track_010 |
| -1.00 | A | g29 TRACK_APPEARED_LEFT(A,U13) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state |
| -1.00 | A | g29 TRACK_APPEARED_LEFT(A,U13) (A:e09)<br>g38 TRACK_LOST(A,U13) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state |
| -0.90 | A | g30 TRACK_APPEARED_LEFT(A,U3) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state<br>track_006: CRITICAL_TTC? |
| -0.80 | A | g31 CLOSING_START(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CRITICAL_TTC? |
| -0.80 | A | g31 CLOSING_START(A,B) (A:e11)<br>g51 CLOSING_END(A,B) (A:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC<br>track_004: no active state<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CRITICAL_TTC? |
| -0.75 | B | g32 CRITICAL_TTC_START(B,A) (B:e23) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| -0.75 | B | g32 CRITICAL_TTC_START(B,A) (B:e23)<br>g34 CLOSING_START(B,A) (B:e24)<br>g42 COLLISION(A,B) (B:e25)<br>g44 CRITICAL_TTC_END(B,A) (B:e26)<br>g45 CLOSING_END(B,A) (B:e27) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| -0.70 | A | g33 TRACK_APPEARED_FRONT(A,U14) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CRITICAL_TTC? |
| -0.70 | A | g33 TRACK_APPEARED_FRONT(A,U14) (A:e12)<br>g41 TRACK_LOST(A,U14) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CRITICAL_TTC? |
| -0.70 | B | g34 CLOSING_START(B,A) (B:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| -0.40 | A | g36 CRITICAL_TTC_START(A,U3) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 |
| -0.35 | A | g37 TRACK_APPEARED_RIGHT(A,U10) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004 |
| -0.15 | A | g39 EGO_PATH_EXIT(A,U14) (A:e17)<br>g40 TRACK_APPEARED_RIGHT(A,U7) (A:e18) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006 |
| +0.05 | A | g46 THROTTLE_END(A) (A:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +0.05 | B | g47 THROTTLE_END(B) (B:e28) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| +0.10 | B | g48 TRACK_APPEARED_LEFT(B,U5) (B:e29)<br>g50 EGO_PATH_ENTRY(B,U12) (B:e30) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| +0.10 | B | g48 TRACK_APPEARED_LEFT(B,U5) (B:e29)<br>g53 TRACK_LOST(B,U5) (B:e32) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| +0.10 | A | g49 EGO_PATH_ENTRY(A,B) (A:e23) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +0.10 | B | g50 EGO_PATH_ENTRY(B,U12) (B:e30)<br>g64 EGO_PATH_EXIT(B,U12) (B:e37) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| +0.25 | B | g52 EGO_PATH_ENTRY(B,U11) (B:e31) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_011: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010 |
| +0.70 | A | g54 TRACK_APPEARED_LEFT(A,U11) (A:e25) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +1.35 | A | g58 EGO_PATH_ENTRY(A,U10) (A:e28) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +1.35 | A | g58 EGO_PATH_ENTRY(A,U10) (A:e28)<br>g79 EGO_PATH_EXIT(A,U10) (A:e36) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +1.40 | A | g59 EGO_PATH_EXIT(A,U7) (A:e29) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +1.45 | B | g60 EGO_PATH_ENTRY(B,U2) (B:e34)<br>g61 CRITICAL_TTC_START(B,U2) (B:e35) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_014 |
| +1.45 | B | g60 EGO_PATH_ENTRY(B,U2) (B:e34)<br>g61 CRITICAL_TTC_START(B,U2) (B:e35)<br>g70 CRITICAL_TTC_END(B,U2) (B:e40)<br>g71 EGO_PATH_EXIT(B,U2) (B:e41) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_014 |
| +1.75 | A | g63 TRACK_APPEARED_LEFT(A,U15) (A:e30) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +1.75 | A | g63 TRACK_APPEARED_LEFT(A,U15) (A:e30)<br>g76 TRACK_LOST(A,U15) (A:e35) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +2.35 | B | g65 CUT_IN_FROM_RIGHT_START(B,U7) (B:e38) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: no active state<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +2.40 | A | g66 CRITICAL_TTC_START(A,U7) (A:e31) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +2.50 | A | g67 EGO_PATH_ENTRY(A,U7) (A:e32) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +2.70 | B | g68 CUT_IN_FROM_RIGHT_START(B,U1) (B:e39) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_007: CUT_IN_FROM_RIGHT<br>track_008: CRITICAL_TTC, IN_EGO_PATH<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +2.75 | A | g69 CRITICAL_TTC_START(A,U1) (A:e33) | ego: MOVING<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +2.95 | B | g72 CRITICAL_TTC_START(B,U7) (B:e42) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CUT_IN_FROM_RIGHT<br>track_007: CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +3.25 | A | g73 EGO_PATH_ENTRY(A,U1) (A:e34) | ego: MOVING<br>track_001: CRITICAL_TTC<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007 |
| +3.35 | B | g74 CLOSING_START(B,U1) (B:e43) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +3.40 | B | g75 EGO_PATH_ENTRY(B,U7) (B:e44) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +3.55 | B | g77 CRITICAL_TTC_START(B,U1) (B:e45) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +3.60 | B | g78 TRACK_APPEARED_LEFT(B,U16) (B:e46) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +3.60 | B | g78 TRACK_APPEARED_LEFT(B,U16) (B:e46)<br>g81 TRACK_LOST(B,U16) (B:e47) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014 |
| +3.85 | A | g80 EGO_PATH_EXIT(A,U3) (A:e37) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_008: no active state<br>track_009: CRITICAL_TTC, IN_EGO_PATH<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_006, track_007, track_011 |
| +3.95 | B | g82 TRACK_APPEARED_FRONT(B,U17) (B:e48) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014, track_015 |
| +4.05 | B | g83 EGO_PATH_ENTRY(B,U1) (B:e49) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track_016: IN_EGO_PATH, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014, track_015 |
| +4.20 | B | g84 EGO_PATH_EXIT(B,U17) (B:e50) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_007: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_008: no active state<br>track_013: no active state<br>track_016: IN_EGO_PATH, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010, track_011, track_012, track_014, track_015 |

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
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared in front of it.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its left.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 7.25 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U3 became critical.
- 7.15 s before the reference collision, B observed anonymous road user U6 start closing in.
- 5.55 s before the reference collision, B's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 4.10 s before the reference collision, B's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 3.95 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 3.30 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared on its left.
- 1.40 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared on its right.
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B's radar started tracking anonymous road user U11, which appeared on its left.
- 1.15 s before the reference collision, B's radar started tracking anonymous road user U12, which appeared in front of it.
- 1.05 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 1.00 s before the reference collision, A's radar started tracking anonymous road user U13, which appeared on its left.
- 0.90 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- 0.80 s before the reference collision, A observed B start closing in.
- 0.75 s before the reference collision, B's time-to-contact with A became critical.
- 0.70 s before the reference collision, A's radar started tracking anonymous road user U14, which appeared in front of it.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.50 s before the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 0.40 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 0.35 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 0.30 s before the reference collision, A's radar lost anonymous road user U13 (its states are UNKNOWN from then on, not ended).
- 0.15 s before the reference collision, A observed anonymous road user U14 leave its forward path corridor.
- 0.15 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared on its right.
- 0.05 s before the reference collision, A's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 254, B: 254 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.10 s after the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.10 s after the reference collision, B observed anonymous road user U12 enter its forward path corridor.
- 0.15 s after the reference collision, A observed B stop closing in.
- 0.25 s after the reference collision, B observed anonymous road user U11 enter its forward path corridor.
- 0.30 s after the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A's radar started tracking anonymous road user U11, which appeared on its left.
- 1.10 s after the reference collision, B's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 1.30 s after the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 1.30 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 1.35 s after the reference collision, A observed anonymous road user U10 enter its forward path corridor.
- 1.40 s after the reference collision, A observed anonymous road user U7 leave its forward path corridor.
- 1.45 s after the reference collision, B observed anonymous road user U2 enter its forward path corridor.
- 1.45 s after the reference collision, B's time-to-contact with anonymous road user U2 became critical.
- 1.60 s after the reference collision, B's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 1.75 s after the reference collision, A's radar started tracking anonymous road user U15, which appeared on its left.
- 1.85 s after the reference collision, B observed anonymous road user U12 leave its forward path corridor.
- 2.35 s after the reference collision, B observed anonymous road user U7 cutting in from the right.
- 2.40 s after the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 2.50 s after the reference collision, A observed anonymous road user U7 enter its forward path corridor.
- 2.70 s after the reference collision, B observed anonymous road user U1 cutting in from the right.
- 2.75 s after the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 2.80 s after the reference collision, B's time-to-contact with anonymous road user U2 stopped being critical.
- 2.80 s after the reference collision, B observed anonymous road user U2 leave its forward path corridor.
- 2.95 s after the reference collision, B's time-to-contact with anonymous road user U7 became critical.
- 3.25 s after the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 3.35 s after the reference collision, B observed anonymous road user U1 start closing in.
- 3.40 s after the reference collision, B observed anonymous road user U7 enter its forward path corridor.
- 3.40 s after the reference collision, A's radar lost anonymous road user U15 (its states are UNKNOWN from then on, not ended).
- 3.55 s after the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 3.60 s after the reference collision, B's radar started tracking anonymous road user U16, which appeared on its left.
- 3.80 s after the reference collision, A observed anonymous road user U10 leave its forward path corridor.
- 3.85 s after the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 3.90 s after the reference collision, B's radar lost anonymous road user U16 (its states are UNKNOWN from then on, not ended).
- 3.95 s after the reference collision, B's radar started tracking anonymous road user U17, which appeared in front of it.
- 4.05 s after the reference collision, B observed anonymous road user U1 enter its forward path corridor.
- 4.20 s after the reference collision, B observed anonymous road user U17 leave its forward path corridor.
