# Global graph - S21/run_0

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_006 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_001 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_002 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003#segment_1, A:track_003#segment_3, B:track_003 |
| U8 | anonymous_road_user | anonymous; observed by A as A:track_003#segment_2 |
| U4 | anonymous_road_user | anonymous; observed by A as A:track_004 |
| U5 | anonymous_road_user | anonymous; observed by A as A:track_005 |
| U9 | anonymous_road_user | anonymous; observed by A, B as A:track_007, B:track_006 |
| U10 | anonymous_road_user | anonymous; observed by A as A:track_008 |
| U13 | anonymous_road_user | anonymous; observed by A as A:track_009 |
| U15 | anonymous_road_user | anonymous; observed by A, B as A:track_010, B:track_010 |
| U14 | anonymous_road_user | anonymous; observed by A, B as A:track_011, B:track_009 |
| U6 | anonymous_road_user | anonymous; observed by B as B:track_004 |
| U7 | anonymous_road_user | anonymous; observed by B as B:track_005 |
| U11 | anonymous_road_user | anonymous; observed by B as B:track_007 |
| U12 | anonymous_road_user | anonymous; observed by B as B:track_008 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e28 | 6.75 | -6.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e25 | 6.75 | -6.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 191.84 vs 191.84 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.5 m -> 12.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.09 m/s over 3.0 s<br>clearance at the contact 10.49 m (beyond 3.50 m: confidence factor 0.07)<br>anonymous road user U1: A:track_001, B:track_001 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 3.15 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 21.4 m -> 23.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_002 |
| A:track_003#segment_1 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 2.00 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 12.1 m -> 11.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.82 m/s over 1.0 s (> 1.50)<br>anonymous road user U3: A:track_003#segment_1, B:track_003, A:track_003#segment_3 |
| A:track_003#segment_2 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.95 s before the matched collision<br>continuous up to the contact: last observed 0.55 s before it (window 1.00 s)<br>not approaching before the contact: clearance 12.2 m -> 12.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.94 m/s over 1.4 s (> 1.50)<br>clearance at the contact 12.10 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U8: A:track_003#segment_2 |
| A:track_003#segment_3 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.50 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 12.2 m -> 12.2 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 2.04 m/s over 0.5 s (> 1.50)<br>clearance at the contact 12.16 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U3: A:track_003#segment_1, B:track_003, A:track_003#segment_3 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 3.15 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 26.6 m -> 24.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U4: A:track_004 |
| A:track_005 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 6.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 6.4 m -> 7.4 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U5: A:track_005 |
| A:track_006 | B | ASSOCIATED | 0.73 | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.18 m/s over 3.0 s<br>clearance at the contact 0.16 m<br>the only track of A compatible with the contact |
| A:track_007 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.45 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.6 m -> 19.2 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 4.06 m/s over 1.5 s (> 1.50)<br>clearance at the contact 19.16 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U9: A:track_007, B:track_006 |
| A:track_008 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.85 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 28.0 m -> 29.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.14 m/s over 0.8 s<br>clearance at the contact 27.96 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U10: A:track_008 |
| A:track_009 | U13 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U13: A:track_009 |
| A:track_010 | U15 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U15: A:track_010, B:track_010 |
| A:track_011 | U14 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U14: B:track_009, A:track_011 |
| B:track_001 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.3 m -> 10.3 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.93 m/s over 3.0 s (> 1.50)<br>clearance at the contact 10.28 m (beyond 3.50 m: confidence factor 0.08)<br>anonymous road user U1: A:track_001, B:track_001 |
| B:track_002 | A | ASSOCIATED | 0.73 | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.19 m/s over 3.0 s<br>clearance at the contact 0.19 m<br>the only compatible track of B touching it at the contact (clearance 0.19 m; track_003 at 10.50 m) |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.4 m -> 10.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 10.50 m (beyond 3.50 m: confidence factor 0.07)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_002, track_003)<br>anonymous road user U3: A:track_003#segment_1, B:track_003, A:track_003#segment_3 |
| B:track_004 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 1.55 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 12.3 m -> 16.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.70 m/s over 1.5 s (> 1.50)<br>anonymous road user U6: B:track_004 |
| B:track_005 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.55 s before the matched collision<br>lost 3.65 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 35.1 m -> 33.1 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_005 |
| B:track_006 | U9 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 21.7 m -> 17.9 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.05 m/s over 1.1 s (> 1.50)<br>clearance at the contact 17.87 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U9: A:track_007, B:track_006 |
| B:track_007 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.85 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 27.9 m -> 26.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.03 m/s over 0.8 s<br>clearance at the contact 26.20 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U11: B:track_007 |
| B:track_008 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.55 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 35.8 m -> 33.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.96 m/s over 0.5 s (> 1.50)<br>clearance at the contact 33.46 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U12: B:track_008 |
| B:track_009 | U14 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.50 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U14: B:track_009, A:track_011 |
| B:track_010 | U15 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U15: A:track_010, B:track_010 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.75 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.75 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.75 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -6.75 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -6.75 | TRACK_APPEARED_FRONT | A | U3 | A:e03 @ 0.00, A:e16 @ 4.75 | initial_in_ego_path=True; source_track=track_003#segment_1; aggregation=entity_state_union; source_tracks=['A:track_003#segment_1'] |
| g06 | -6.75 | TRACK_APPEARED_FRONT | B | U1 | B:e03 @ 0.00, B:e53 @ 11.10 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g07 | -6.75 | TRACK_APPEARED_LEFT | A | U1 | A:e04 @ 0.00, A:e53 @ 11.20 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g08 | -6.75 | TRACK_APPEARED_LEFT | A | U2 | A:e05 @ 0.00, A:e13 @ 3.60 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g09 | -6.75 | TRACK_APPEARED_RIGHT | A | U4 | A:e06 @ 0.00, A:e14 @ 3.60 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g10 | -6.75 | TRACK_APPEARED_RIGHT | A | U5 | A:e07 @ 0.00, A:e12 @ 0.50 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g11 | -6.75 | TRACK_APPEARED_RIGHT | B | A | B:e04 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g12 | -6.75 | TRACK_APPEARED_RIGHT | B | U3 | B:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -6.75 | TRACK_APPEARED_RIGHT | B | U6 | B:e06 @ 0.00, B:e16 @ 5.20 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g14 | -6.75 | CLOSING_START | A | U4 | A:e08 @ 0.00 | active_at_first_observation=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g15 | -6.75 | CLOSING_START | B | A | B:e07 @ 0.00, B:e14 @ 4.15 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g16 | -6.75 | CLOSING_START | B | U3 | B:e08 @ 0.00, B:e32 @ 7.10 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g17 | -6.55 | TRACK_APPEARED_FRONT | B | U7 | B:e09 @ 0.20, B:e12 @ 3.10 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g18 | -6.55 | CLOSING_START | B | U7 | B:e10 @ 0.20 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g19 | -6.35 | TRACK_APPEARED_LEFT | A | B | A:e09 @ 0.40 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g20 | -6.35 | CLOSING_START | A | B | A:e10 @ 0.40, A:e15 @ 3.85 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g21 | -6.25 | CRITICAL_TTC_START | A | U3 | A:e11 @ 0.50 | source_track=track_003#segment_1; aggregation=entity_state_union; source_tracks=['A:track_003#segment_1'] |
| g22 | -6.25 | CRITICAL_TTC_START | B | U1 | B:e11 @ 0.50, B:e38 @ 7.55 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g23 | -6.25 | TRACK_LOST | A | U5 | A:e12 @ 0.50 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g24 | -3.65 | TRACK_LOST | B | U7 | B:e12 @ 3.10 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g25 | -3.25 | CUT_IN_FROM_RIGHT_START | B | A | B:e13 @ 3.50, B:e15 @ 4.30 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g26 | -3.15 | TRACK_LOST | A | U2 | A:e13 @ 3.60 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g27 | -3.15 | TRACK_LOST | A | U4 | A:e14 @ 3.60 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g28 | -2.90 | CLOSING_END | A | B | A:e15 @ 3.85 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g29 | -2.60 | CLOSING_END | B | A | B:e14 @ 4.15 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g30 | -2.45 | CUT_IN_FROM_RIGHT_END | B | A | B:e15 @ 4.30 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g31 | -2.00 | TRACK_LOST | A | U3 | A:e16 @ 4.75 | source_track=track_003#segment_1; aggregation=entity_state_union; source_tracks=['A:track_003#segment_1'] |
| g32 | -1.95 | TRACK_APPEARED_FRONT | A | U8 | A:e17 @ 4.80, A:e25 @ 6.20 | initial_in_ego_path=False; source_track=track_003#segment_2; aggregation=entity_state_union; source_tracks=['A:track_003#segment_2'] |
| g33 | -1.65 | CRITICAL_TTC_START | A | B | A:e18 @ 5.10, A:e29 @ 6.75 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g34 | -1.55 | TRACK_LOST | B | U6 | B:e16 @ 5.20 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g35 | -1.45 | TRACK_APPEARED_RIGHT | A | U9 | A:e19 @ 5.30 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g36 | -1.45 | CLOSING_START | A | U9 | A:e20 @ 5.30, A:e36 @ 7.20 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g37 | -1.20 | CRITICAL_TTC_START | B | A | B:e17 @ 5.55, B:e26 @ 6.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g38 | -1.15 | CRITICAL_TTC_START | A | U1 | A:e21 @ 5.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g39 | -1.10 | TRACK_APPEARED_RIGHT | B | U9 | B:e18 @ 5.65 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g40 | -1.10 | CLOSING_START | B | U9 | B:e19 @ 5.65, B:e34 @ 7.35 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g41 | -1.05 | EGO_PATH_ENTRY | A | U1 | A:e22 @ 5.70, A:e38 @ 7.55 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g42 | -0.85 | TRACK_APPEARED_FRONT | A | U10 | A:e23 @ 5.90, A:e55 @ 11.85 | initial_in_ego_path=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g43 | -0.85 | TRACK_APPEARED_RIGHT | B | U11 | B:e20 @ 5.90, B:e55 @ 11.55 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g44 | -0.85 | CLOSING_START | B | U11 | B:e21 @ 5.90, B:e31 @ 7.05 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g45 | -0.55 | TRACK_APPEARED_RIGHT | B | U12 | B:e22 @ 6.20, B:e39 @ 7.55 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g46 | -0.55 | CLOSING_START | A | B | A:e24 @ 6.20, A:e31 @ 6.80 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g47 | -0.55 | CLOSING_START | B | U12 | B:e23 @ 6.20, B:e35 @ 7.35 | active_at_first_observation=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g48 | -0.55 | TRACK_LOST | A | U8 | A:e25 @ 6.20 | source_track=track_003#segment_2; aggregation=entity_state_union; source_tracks=['A:track_003#segment_2'] |
| g49 | -0.50 | TRACK_APPEARED_RIGHT | A | U3 | A:e26 @ 6.25 | initial_in_ego_path=True; source_track=track_003#segment_3; aggregation=entity_state_union; source_tracks=['A:track_003#segment_3'] |
| g50 | -0.45 | CLOSING_START | B | A | B:e24 @ 6.30, B:e27 @ 6.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g51 | -0.35 | EGO_PATH_ENTRY | A | B | A:e27 @ 6.40, A:e41 @ 7.95 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g52 | 0.00 | COLLISION | - | A, B | A:e28 @ 6.75, B:e25 @ 6.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 191.84, B 191.84 |
| g53 | 0.00 | CRITICAL_TTC_END | A | B | A:e29 @ 6.75 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g54 | 0.00 | CRITICAL_TTC_END | B | A | B:e26 @ 6.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g55 | 0.00 | EGO_PATH_EXIT | A | U3 | A:e30 @ 6.75 | geometry=estimated_body; source_track=track_003#segment_3; aggregation=entity_state_union; source_tracks=['A:track_003#segment_3'] |
| g56 | 0.05 | CLOSING_END | A | B | A:e31 @ 6.80 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g57 | 0.05 | CLOSING_END | B | A | B:e27 @ 6.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g58 | 0.05 | THROTTLE_END | A | - | A:e32 @ 6.80 |  |
| g59 | 0.05 | THROTTLE_END | B | - | B:e28 @ 6.80 |  |
| g60 | 0.05 | BRAKE_START | A | - | A:e33 @ 6.80 |  |
| g61 | 0.05 | BRAKE_START | B | - | B:e29 @ 6.80 |  |
| g62 | 0.10 | EGO_PATH_ENTRY | A | U3 | A:e34 @ 6.85, A:e49 @ 9.95 | geometry=estimated_body; source_track=track_003#segment_3; aggregation=entity_state_union; source_tracks=['A:track_003#segment_3'] |
| g63 | 0.10 | CRITICAL_TTC_START | A | U3 | A:e35 @ 6.85, A:e37 @ 7.45 | source_track=track_003#segment_3; aggregation=entity_state_union; source_tracks=['A:track_003#segment_3'] |
| g64 | 0.20 | EGO_PATH_ENTRY | B | U11 | B:e30 @ 6.95, B:e46 @ 9.05 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g65 | 0.30 | CLOSING_END | B | U11 | B:e31 @ 7.05 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g66 | 0.35 | CLOSING_END | B | U3 | B:e32 @ 7.10 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g67 | 0.45 | CLOSING_END | A | U9 | A:e36 @ 7.20 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g68 | 0.50 | EGO_PATH_ENTRY | B | U3 | B:e33 @ 7.25, B:e51 @ 10.35 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g69 | 0.60 | CLOSING_END | B | U12 | B:e35 @ 7.35 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g70 | 0.60 | CLOSING_END | B | U9 | B:e34 @ 7.35 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g71 | 0.60 | EGO_PATH_ENTRY | B | U12 | B:e36 @ 7.35 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g72 | 0.65 | CRITICAL_TTC_START | B | U3 | B:e37 @ 7.40, B:e44 @ 8.50 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g73 | 0.70 | CRITICAL_TTC_END | A | U3 | A:e37 @ 7.45 | source_track=track_003#segment_3; aggregation=entity_state_union; source_tracks=['A:track_003#segment_3'] |
| g74 | 0.80 | CRITICAL_TTC_END | B | U1 | B:e38 @ 7.55 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g75 | 0.80 | EGO_PATH_EXIT | A | U1 | A:e38 @ 7.55 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g76 | 0.80 | EGO_PATH_EXIT | A | U10 | A:e39 @ 7.55 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g77 | 0.80 | TRACK_LOST | B | U12 | B:e39 @ 7.55 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g78 | 1.15 | MOVING_END | B | - | B:e40 @ 7.90 |  |
| g79 | 1.15 | STOP_START | B | - | B:e41 @ 7.90 |  |
| g80 | 1.15 | TRACK_APPEARED_FRONT | A | U13 | A:e40 @ 7.90 | initial_in_ego_path=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g81 | 1.15 | EGO_PATH_ENTRY | B | A | B:e42 @ 7.90 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g82 | 1.20 | EGO_PATH_EXIT | A | B | A:e41 @ 7.95 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g83 | 1.20 | MOVING_END | A | - | A:e42 @ 7.95 |  |
| g84 | 1.20 | STOP_START | A | - | A:e43 @ 7.95 |  |
| g85 | 1.30 | EGO_PATH_ENTRY | A | B | A:e44 @ 8.05 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g86 | 1.50 | TRACK_APPEARED_LEFT | B | U14 | B:e43 @ 8.25, B:e49 @ 9.70 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g87 | 1.55 | TRACK_APPEARED_RIGHT | A | U15 | A:e45 @ 8.30 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g88 | 1.55 | CLOSING_START | A | U15 | A:e46 @ 8.30, A:e52 @ 10.15 | active_at_first_observation=True; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g89 | 1.60 | EGO_PATH_ENTRY | A | U9 | A:e47 @ 8.35, A:e54 @ 11.35 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g90 | 1.75 | CRITICAL_TTC_END | B | U3 | B:e44 @ 8.50 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g91 | 1.80 | TRACK_APPEARED_LEFT | A | U14 | A:e48 @ 8.55, A:e50 @ 9.95 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g92 | 1.90 | EGO_PATH_EXIT | B | U1 | B:e45 @ 8.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g93 | 2.30 | EGO_PATH_EXIT | B | U11 | B:e46 @ 9.05 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g94 | 2.40 | EGO_PATH_ENTRY | B | U9 | B:e47 @ 9.15, B:e54 @ 11.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g95 | 2.90 | CUT_IN_FROM_RIGHT_START | B | U3 | B:e48 @ 9.65 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g96 | 2.95 | TRACK_LOST | B | U14 | B:e49 @ 9.70 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g97 | 3.20 | EGO_PATH_EXIT | A | U3 | A:e49 @ 9.95 | geometry=estimated_body; source_track=track_003#segment_3; aggregation=entity_state_union; source_tracks=['A:track_003#segment_3'] |
| g98 | 3.20 | TRACK_LOST | A | U14 | A:e50 @ 9.95 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g99 | 3.35 | EGO_PATH_EXIT | A | U13 | A:e51 @ 10.10 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g100 | 3.40 | CLOSING_END | A | U15 | A:e52 @ 10.15 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g101 | 3.45 | TRACK_APPEARED_RIGHT | B | U15 | B:e50 @ 10.20 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g102 | 3.60 | EGO_PATH_EXIT | B | U3 | B:e51 @ 10.35 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g103 | 4.15 | CUT_IN_FROM_RIGHT_START | B | U9 | B:e52 @ 10.90 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g104 | 4.35 | TRACK_LOST | B | U1 | B:e53 @ 11.10 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g105 | 4.45 | TRACK_LOST | A | U1 | A:e53 @ 11.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g106 | 4.60 | EGO_PATH_EXIT | A | U9 | A:e54 @ 11.35 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g107 | 4.80 | EGO_PATH_EXIT | B | U9 | B:e54 @ 11.55 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g108 | 4.80 | TRACK_LOST | B | U11 | B:e55 @ 11.55 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g109 | 5.10 | TRACK_LOST | A | U10 | A:e55 @ 11.85 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |

## Edges

```
    g01 --PRECEDES--> g17
    g01 --PRECEDES--> g18
    g02 --PRECEDES--> g17
    g02 --PRECEDES--> g18
    g03 --PRECEDES--> g17
    g03 --PRECEDES--> g18
    g04 --PRECEDES--> g17
    g04 --PRECEDES--> g18
    g05 --PRECEDES--> g17
    g05 --PRECEDES--> g18
    g06 --PRECEDES--> g17
    g06 --PRECEDES--> g18
    g07 --PRECEDES--> g17
    g07 --PRECEDES--> g18
    g08 --PRECEDES--> g17
    g08 --PRECEDES--> g18
    g09 --PRECEDES--> g17
    g09 --PRECEDES--> g18
    g10 --PRECEDES--> g17
    g10 --PRECEDES--> g18
    g11 --PRECEDES--> g17
    g11 --PRECEDES--> g18
    g12 --PRECEDES--> g17
    g12 --PRECEDES--> g18
    g13 --PRECEDES--> g17
    g13 --PRECEDES--> g18
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g42 --PRECEDES--> g48
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g46 --PRECEDES--> g49
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g52 --PRECEDES--> g58
    g52 --PRECEDES--> g59
    g52 --PRECEDES--> g60
    g52 --PRECEDES--> g61
    g53 --PRECEDES--> g56
    g53 --PRECEDES--> g57
    g53 --PRECEDES--> g58
    g53 --PRECEDES--> g59
    g53 --PRECEDES--> g60
    g53 --PRECEDES--> g61
    g54 --PRECEDES--> g56
    g54 --PRECEDES--> g57
    g54 --PRECEDES--> g58
    g54 --PRECEDES--> g59
    g54 --PRECEDES--> g60
    g54 --PRECEDES--> g61
    g55 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g55 --PRECEDES--> g60
    g55 --PRECEDES--> g61
    g56 --PRECEDES--> g62
    g56 --PRECEDES--> g63
    g57 --PRECEDES--> g62
    g57 --PRECEDES--> g63
    g58 --PRECEDES--> g62
    g58 --PRECEDES--> g63
    g59 --PRECEDES--> g62
    g59 --PRECEDES--> g63
    g60 --PRECEDES--> g62
    g60 --PRECEDES--> g63
    g61 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g63 --PRECEDES--> g64
    g64 --PRECEDES--> g65
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g68 --PRECEDES--> g71
    g69 --PRECEDES--> g72
    g70 --PRECEDES--> g72
    g71 --PRECEDES--> g72
    g72 --PRECEDES--> g73
    g73 --PRECEDES--> g74
    g73 --PRECEDES--> g75
    g73 --PRECEDES--> g76
    g73 --PRECEDES--> g77
    g74 --PRECEDES--> g78
    g74 --PRECEDES--> g79
    g74 --PRECEDES--> g80
    g74 --PRECEDES--> g81
    g75 --PRECEDES--> g78
    g75 --PRECEDES--> g79
    g75 --PRECEDES--> g80
    g75 --PRECEDES--> g81
    g76 --PRECEDES--> g78
    g76 --PRECEDES--> g79
    g76 --PRECEDES--> g80
    g76 --PRECEDES--> g81
    g77 --PRECEDES--> g78
    g77 --PRECEDES--> g79
    g77 --PRECEDES--> g80
    g77 --PRECEDES--> g81
    g78 --PRECEDES--> g82
    g78 --PRECEDES--> g83
    g78 --PRECEDES--> g84
    g79 --PRECEDES--> g82
    g79 --PRECEDES--> g83
    g79 --PRECEDES--> g84
    g80 --PRECEDES--> g82
    g80 --PRECEDES--> g83
    g80 --PRECEDES--> g84
    g81 --PRECEDES--> g82
    g81 --PRECEDES--> g83
    g81 --PRECEDES--> g84
    g82 --PRECEDES--> g85
    g83 --PRECEDES--> g85
    g84 --PRECEDES--> g85
    g85 --PRECEDES--> g86
    g86 --PRECEDES--> g87
    g86 --PRECEDES--> g88
    g87 --PRECEDES--> g89
    g88 --PRECEDES--> g89
    g89 --PRECEDES--> g90
    g90 --PRECEDES--> g91
    g91 --PRECEDES--> g92
    g92 --PRECEDES--> g93
    g93 --PRECEDES--> g94
    g94 --PRECEDES--> g95
    g95 --PRECEDES--> g96
    g96 --PRECEDES--> g97
    g96 --PRECEDES--> g98
    g97 --PRECEDES--> g99
    g98 --PRECEDES--> g99
    g99 --PRECEDES--> g100
    g100 --PRECEDES--> g101
    g101 --PRECEDES--> g102
    g102 --PRECEDES--> g103
    g103 --PRECEDES--> g104
    g104 --PRECEDES--> g105
    g105 --PRECEDES--> g106
    g106 --PRECEDES--> g107
    g106 --PRECEDES--> g108
    g107 --PRECEDES--> g109
    g108 --PRECEDES--> g109
    g09 --SAME_TRACK--> g14
    g19 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g21
    g10 --SAME_TRACK--> g23
    g08 --SAME_TRACK--> g26
    g09 --SAME_TRACK--> g27
    g19 --SAME_TRACK--> g28
    g05 --SAME_TRACK--> g31
    g19 --SAME_TRACK--> g33
    g35 --SAME_TRACK--> g36
    g07 --SAME_TRACK--> g38
    g07 --SAME_TRACK--> g41
    g19 --SAME_TRACK--> g46
    g32 --SAME_TRACK--> g48
    g19 --SAME_TRACK--> g51
    g19 --SAME_TRACK--> g53
    g49 --SAME_TRACK--> g55
    g19 --SAME_TRACK--> g56
    g49 --SAME_TRACK--> g62
    g49 --SAME_TRACK--> g63
    g35 --SAME_TRACK--> g67
    g49 --SAME_TRACK--> g73
    g07 --SAME_TRACK--> g75
    g42 --SAME_TRACK--> g76
    g19 --SAME_TRACK--> g82
    g19 --SAME_TRACK--> g85
    g87 --SAME_TRACK--> g88
    g35 --SAME_TRACK--> g89
    g49 --SAME_TRACK--> g97
    g91 --SAME_TRACK--> g98
    g80 --SAME_TRACK--> g99
    g87 --SAME_TRACK--> g100
    g07 --SAME_TRACK--> g105
    g35 --SAME_TRACK--> g106
    g42 --SAME_TRACK--> g109
    g11 --SAME_TRACK--> g15
    g12 --SAME_TRACK--> g16
    g17 --SAME_TRACK--> g18
    g06 --SAME_TRACK--> g22
    g17 --SAME_TRACK--> g24
    g11 --SAME_TRACK--> g25
    g11 --SAME_TRACK--> g29
    g11 --SAME_TRACK--> g30
    g13 --SAME_TRACK--> g34
    g11 --SAME_TRACK--> g37
    g39 --SAME_TRACK--> g40
    g43 --SAME_TRACK--> g44
    g45 --SAME_TRACK--> g47
    g11 --SAME_TRACK--> g50
    g11 --SAME_TRACK--> g54
    g11 --SAME_TRACK--> g57
    g43 --SAME_TRACK--> g64
    g43 --SAME_TRACK--> g65
    g12 --SAME_TRACK--> g66
    g12 --SAME_TRACK--> g68
    g39 --SAME_TRACK--> g70
    g45 --SAME_TRACK--> g69
    g45 --SAME_TRACK--> g71
    g12 --SAME_TRACK--> g72
    g06 --SAME_TRACK--> g74
    g45 --SAME_TRACK--> g77
    g11 --SAME_TRACK--> g81
    g12 --SAME_TRACK--> g90
    g06 --SAME_TRACK--> g92
    g43 --SAME_TRACK--> g93
    g39 --SAME_TRACK--> g94
    g12 --SAME_TRACK--> g95
    g86 --SAME_TRACK--> g96
    g12 --SAME_TRACK--> g102
    g39 --SAME_TRACK--> g103
    g06 --SAME_TRACK--> g104
    g39 --SAME_TRACK--> g107
    g43 --SAME_TRACK--> g108
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U1); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(A,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U3); TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(A,U4); CLOSING_START(B,A); CLOSING_START(B,U3) |
| -6.55 | TRACK_APPEARED_FRONT(B,U7); CLOSING_START(B,U7) |
| -6.35 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -6.25 | CRITICAL_TTC_START(A,U3); CRITICAL_TTC_START(B,U1); TRACK_LOST(A,U5) |
| -3.65 | TRACK_LOST(B,U7) |
| -3.25 | CUT_IN_FROM_RIGHT_START(B,A) |
| -3.15 | TRACK_LOST(A,U2); TRACK_LOST(A,U4) |
| -2.90 | CLOSING_END(A,B) |
| -2.60 | CLOSING_END(B,A) |
| -2.45 | CUT_IN_FROM_RIGHT_END(B,A) |
| -2.00 | TRACK_LOST(A,U3) |
| -1.95 | TRACK_APPEARED_FRONT(A,U8) |
| -1.65 | CRITICAL_TTC_START(A,B) |
| -1.55 | TRACK_LOST(B,U6) |
| -1.45 | TRACK_APPEARED_RIGHT(A,U9); CLOSING_START(A,U9) |
| -1.20 | CRITICAL_TTC_START(B,A) |
| -1.15 | CRITICAL_TTC_START(A,U1) |
| -1.10 | TRACK_APPEARED_RIGHT(B,U9); CLOSING_START(B,U9) |
| -1.05 | EGO_PATH_ENTRY(A,U1) |
| -0.85 | TRACK_APPEARED_FRONT(A,U10); TRACK_APPEARED_RIGHT(B,U11); CLOSING_START(B,U11) |
| -0.55 | TRACK_APPEARED_RIGHT(B,U12); CLOSING_START(A,B); CLOSING_START(B,U12); TRACK_LOST(A,U8) |
| -0.50 | TRACK_APPEARED_RIGHT(A,U3) |
| -0.45 | CLOSING_START(B,A) |
| -0.35 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); EGO_PATH_EXIT(A,U3) |
| +0.05 | CLOSING_END(A,B); CLOSING_END(B,A); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | EGO_PATH_ENTRY(A,U3); CRITICAL_TTC_START(A,U3) |
| +0.20 | EGO_PATH_ENTRY(B,U11) |
| +0.30 | CLOSING_END(B,U11) |
| +0.35 | CLOSING_END(B,U3) |
| +0.45 | CLOSING_END(A,U9) |
| +0.50 | EGO_PATH_ENTRY(B,U3) |
| +0.60 | CLOSING_END(B,U12); CLOSING_END(B,U9); EGO_PATH_ENTRY(B,U12) |
| +0.65 | CRITICAL_TTC_START(B,U3) |
| +0.70 | CRITICAL_TTC_END(A,U3) |
| +0.80 | CRITICAL_TTC_END(B,U1); EGO_PATH_EXIT(A,U1); EGO_PATH_EXIT(A,U10); TRACK_LOST(B,U12) |
| +1.15 | MOVING_END(B); STOP_START(B); TRACK_APPEARED_FRONT(A,U13); EGO_PATH_ENTRY(B,A) |
| +1.20 | EGO_PATH_EXIT(A,B); MOVING_END(A); STOP_START(A) |
| +1.30 | EGO_PATH_ENTRY(A,B) |
| +1.50 | TRACK_APPEARED_LEFT(B,U14) |
| +1.55 | TRACK_APPEARED_RIGHT(A,U15); CLOSING_START(A,U15) |
| +1.60 | EGO_PATH_ENTRY(A,U9) |
| +1.75 | CRITICAL_TTC_END(B,U3) |
| +1.80 | TRACK_APPEARED_LEFT(A,U14) |
| +1.90 | EGO_PATH_EXIT(B,U1) |
| +2.30 | EGO_PATH_EXIT(B,U11) |
| +2.40 | EGO_PATH_ENTRY(B,U9) |
| +2.90 | CUT_IN_FROM_RIGHT_START(B,U3) |
| +2.95 | TRACK_LOST(B,U14) |
| +3.20 | EGO_PATH_EXIT(A,U3); TRACK_LOST(A,U14) |
| +3.35 | EGO_PATH_EXIT(A,U13) |
| +3.40 | CLOSING_END(A,U15) |
| +3.45 | TRACK_APPEARED_RIGHT(B,U15) |
| +3.60 | EGO_PATH_EXIT(B,U3) |
| +4.15 | CUT_IN_FROM_RIGHT_START(B,U9) |
| +4.35 | TRACK_LOST(B,U1) |
| +4.45 | TRACK_LOST(A,U1) |
| +4.60 | EGO_PATH_EXIT(A,U9) |
| +4.80 | EGO_PATH_EXIT(B,U9); TRACK_LOST(B,U11) |
| +5.10 | TRACK_LOST(A,U10) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 5.60, COLLISION 6.75 (+1.15 s); EGO_PATH_ENTRY 5.70 after critical TTC (+0.10 s) [local times; t_global: critical_ttc_start -1.15, ego_path_entry -1.05, collision +0.00]
- A's track_003#segment_1 (unidentified U3): CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s) [local times; t_global: critical_ttc_start -6.25, collision +0.00]
- A's track_003#segment_3 (unidentified U3): CRITICAL_TTC_START 6.85; EGO_PATH_ENTRY 6.85 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start +0.10, ego_path_entry +0.10]
- A's track_006 (B): CRITICAL_TTC_START 5.10, COLLISION with B 6.75 (+1.65 s); EGO_PATH_ENTRY 6.40 after critical TTC (+1.30 s) [local times; t_global: critical_ttc_start -1.65, ego_path_entry -0.35, collision +0.00]
- A's track_007 (unidentified U9): EGO_PATH_ENTRY 8.35, no critical TTC [local times; t_global: ego_path_entry +1.60]
- B's track_001 (unidentified U1): CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s) [local times; t_global: critical_ttc_start -6.25, collision +0.00]
- B's track_002 (A): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 3.50 < CRITICAL_TTC_START 5.55 (+2.05 s) < COLLISION with A 6.75 (+1.20 s); EGO_PATH_ENTRY 7.90 after critical TTC (+2.35 s) [local times; t_global: cut_in -3.25, critical_ttc_start -1.20, ego_path_entry +1.15, collision +0.00]
- B's track_003 (unidentified U3): CUT_IN_FROM_RIGHT_START 9.65, no critical TTC after it; EGO_PATH_ENTRY 7.25 before critical TTC (-0.15 s) [local times; t_global: cut_in +2.90, critical_ttc_start +0.65, ego_path_entry +0.50]
- B's track_006 (unidentified U9): CUT_IN_FROM_RIGHT_START 10.90, no critical TTC after it; EGO_PATH_ENTRY 9.15, no critical TTC [local times; t_global: cut_in +4.15, ego_path_entry +2.40]
- B's track_007 (unidentified U11): EGO_PATH_ENTRY 6.95, no critical TTC [local times; t_global: ego_path_entry +0.20]
- B's track_008 (unidentified U12): EGO_PATH_ENTRY 7.35, no critical TTC [local times; t_global: ego_path_entry +0.60]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U3) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g08 TRACK_APPEARED_LEFT(A,U2) (A:e05)<br>g09 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g10 TRACK_APPEARED_RIGHT(A,U5) (A:e07)<br>g14 CLOSING_START(A,U4) (A:e08) | ego: not yet observed |
| -6.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U1) (B:e03)<br>g11 TRACK_APPEARED_RIGHT(B,A) (B:e04)<br>g12 TRACK_APPEARED_RIGHT(B,U3) (B:e05)<br>g13 TRACK_APPEARED_RIGHT(B,U6) (B:e06)<br>g15 CLOSING_START(B,A) (B:e07)<br>g16 CLOSING_START(B,U3) (B:e08) | ego: not yet observed |
| -6.75 | A | g05 TRACK_APPEARED_FRONT(A,U3) (A:e03)<br>g31 TRACK_LOST(A,U3) (A:e16) | ego: not yet observed |
| -6.75 | B | g06 TRACK_APPEARED_FRONT(B,U1) (B:e03)<br>g104 TRACK_LOST(B,U1) (B:e53) | ego: not yet observed |
| -6.75 | A | g07 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g105 TRACK_LOST(A,U1) (A:e53) | ego: not yet observed |
| -6.75 | A | g08 TRACK_APPEARED_LEFT(A,U2) (A:e05)<br>g09 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g26 TRACK_LOST(A,U2) (A:e13)<br>g27 TRACK_LOST(A,U4) (A:e14) | ego: not yet observed |
| -6.75 | A | g10 TRACK_APPEARED_RIGHT(A,U5) (A:e07)<br>g21 CRITICAL_TTC_START(A,U3) (A:e11)<br>g23 TRACK_LOST(A,U5) (A:e12) | ego: not yet observed |
| -6.75 | B | g13 TRACK_APPEARED_RIGHT(B,U6) (B:e06)<br>g34 TRACK_LOST(B,U6) (B:e16) | ego: not yet observed |
| -6.75 | B | g15 CLOSING_START(B,A) (B:e07)<br>g29 CLOSING_END(B,A) (B:e14) | ego: not yet observed |
| -6.75 | B | g16 CLOSING_START(B,U3) (B:e08)<br>g66 CLOSING_END(B,U3) (B:e32) | ego: not yet observed |
| -6.55 | B | g17 TRACK_APPEARED_FRONT(B,U7) (B:e09)<br>g18 CLOSING_START(B,U7) (B:e10) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -6.55 | B | g17 TRACK_APPEARED_FRONT(B,U7) (B:e09)<br>g24 TRACK_LOST(B,U7) (B:e12) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -6.35 | A | g19 TRACK_APPEARED_LEFT(A,B) (A:e09)<br>g20 CLOSING_START(A,B) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003#segment_1: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -6.35 | A | g20 CLOSING_START(A,B) (A:e10)<br>g28 CLOSING_END(A,B) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003#segment_1: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -6.25 | B | g22 CRITICAL_TTC_START(B,U1) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CLOSING, CRITICAL_TTC? |
| -6.25 | B | g22 CRITICAL_TTC_START(B,U1) (B:e11)<br>g45 TRACK_APPEARED_RIGHT(B,U12) (B:e22)<br>g74 CRITICAL_TTC_END(B,U1) (B:e38)<br>g77 TRACK_LOST(B,U12) (B:e39) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CLOSING, CRITICAL_TTC? |
| -3.25 | B | g25 CUT_IN_FROM_RIGHT_START(B,A) (B:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005 |
| -3.25 | B | g25 CUT_IN_FROM_RIGHT_START(B,A) (B:e13)<br>g30 CUT_IN_FROM_RIGHT_END(B,A) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005 |
| -1.95 | A | g32 TRACK_APPEARED_FRONT(A,U8) (A:e17) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.95 | A | g32 TRACK_APPEARED_FRONT(A,U8) (A:e17)<br>g46 CLOSING_START(A,B) (A:e24)<br>g48 TRACK_LOST(A,U8) (A:e25) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.65 | A | g33 CRITICAL_TTC_START(A,B) (A:e18) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.65 | A | g33 CRITICAL_TTC_START(A,B) (A:e18)<br>g52 COLLISION(A,B) (A:e28)<br>g53 CRITICAL_TTC_END(A,B) (A:e29)<br>g55 EGO_PATH_EXIT(A,U3) (A:e30) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.45 | A | g35 TRACK_APPEARED_RIGHT(A,U9) (A:e19)<br>g36 CLOSING_START(A,U9) (A:e20) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.45 | A | g36 CLOSING_START(A,U9) (A:e20)<br>g67 CLOSING_END(A,U9) (A:e36) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.20 | B | g37 CRITICAL_TTC_START(B,A) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| -1.20 | B | g37 CRITICAL_TTC_START(B,A) (B:e17)<br>g52 COLLISION(A,B) (B:e25)<br>g54 CRITICAL_TTC_END(B,A) (B:e26) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| -1.15 | A | g38 CRITICAL_TTC_START(A,U1) (A:e21) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.10 | B | g39 TRACK_APPEARED_RIGHT(B,U9) (B:e18)<br>g40 CLOSING_START(B,U9) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| -1.10 | B | g40 CLOSING_START(B,U9) (B:e19)<br>g47 CLOSING_START(B,U12) (B:e23)<br>g69 CLOSING_END(B,U12) (B:e35)<br>g70 CLOSING_END(B,U9) (B:e34)<br>g71 EGO_PATH_ENTRY(B,U12) (B:e36) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| -1.05 | A | g41 EGO_PATH_ENTRY(A,U1) (A:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -1.05 | A | g41 EGO_PATH_ENTRY(A,U1) (A:e22)<br>g75 EGO_PATH_EXIT(A,U1) (A:e38)<br>g76 EGO_PATH_EXIT(A,U10) (A:e39) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -0.85 | A | g42 TRACK_APPEARED_FRONT(A,U10) (A:e23) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -0.85 | A | g42 TRACK_APPEARED_FRONT(A,U10) (A:e23)<br>g109 TRACK_LOST(A,U10) (A:e55) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -0.85 | B | g43 TRACK_APPEARED_RIGHT(B,U11) (B:e20)<br>g44 CLOSING_START(B,U11) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 |
| -0.85 | B | g43 TRACK_APPEARED_RIGHT(B,U11) (B:e20)<br>g94 EGO_PATH_ENTRY(B,U9) (B:e47)<br>g107 EGO_PATH_EXIT(B,U9) (B:e54)<br>g108 TRACK_LOST(B,U11) (B:e55) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 |
| -0.85 | B | g44 CLOSING_START(B,U11) (B:e21)<br>g65 CLOSING_END(B,U11) (B:e31) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 |
| -0.55 | B | g45 TRACK_APPEARED_RIGHT(B,U12) (B:e22)<br>g47 CLOSING_START(B,U12) (B:e23) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 |
| -0.55 | A | g46 CLOSING_START(A,B) (A:e24)<br>g56 CLOSING_END(A,B) (A:e31)<br>g58 THROTTLE_END(A) (A:e32)<br>g60 BRAKE_START(A) (A:e33) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_004, track_005 |
| -0.50 | A | g49 TRACK_APPEARED_RIGHT(A,U3) (A:e26) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| -0.45 | B | g50 CLOSING_START(B,A) (B:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 |
| -0.45 | B | g50 CLOSING_START(B,A) (B:e24)<br>g57 CLOSING_END(B,A) (B:e27)<br>g59 THROTTLE_END(B) (B:e28)<br>g61 BRAKE_START(B) (B:e29) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005 |
| -0.35 | A | g51 EGO_PATH_ENTRY(A,B) (A:e27) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| -0.35 | A | g51 EGO_PATH_ENTRY(A,B) (A:e27)<br>g82 EGO_PATH_EXIT(A,B) (A:e41)<br>g83 MOVING_END(A) (A:e42)<br>g84 STOP_START(A) (A:e43) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +0.10 | A | g62 EGO_PATH_ENTRY(A,U3) (A:e34)<br>g63 CRITICAL_TTC_START(A,U3) (A:e35) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +0.10 | A | g62 EGO_PATH_ENTRY(A,U3) (A:e34)<br>g91 TRACK_APPEARED_LEFT(A,U14) (A:e48)<br>g97 EGO_PATH_EXIT(A,U3) (A:e49)<br>g98 TRACK_LOST(A,U14) (A:e50) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +0.10 | A | g63 CRITICAL_TTC_START(A,U3) (A:e35)<br>g73 CRITICAL_TTC_END(A,U3) (A:e37) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +0.20 | B | g64 EGO_PATH_ENTRY(B,U11) (B:e30) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| +0.20 | B | g64 EGO_PATH_ENTRY(B,U11) (B:e30)<br>g93 EGO_PATH_EXIT(B,U11) (B:e46) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| +0.50 | B | g68 EGO_PATH_ENTRY(B,U3) (B:e33) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| +0.50 | B | g68 EGO_PATH_ENTRY(B,U3) (B:e33)<br>g102 EGO_PATH_EXIT(B,U3) (B:e51) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_004, track_005 |
| +0.65 | B | g72 CRITICAL_TTC_START(B,U3) (B:e37) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005 |
| +0.65 | B | g72 CRITICAL_TTC_START(B,U3) (B:e37)<br>g90 CRITICAL_TTC_END(B,U3) (B:e44) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005 |
| +1.15 | B | g78 MOVING_END(B) (B:e40)<br>g79 STOP_START(B) (B:e41)<br>g81 EGO_PATH_ENTRY(B,A) (B:e42) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008 |
| +1.15 | A | g80 TRACK_APPEARED_FRONT(A,U13) (A:e40) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +1.30 | A | g85 EGO_PATH_ENTRY(A,B) (A:e44) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +1.50 | B | g86 TRACK_APPEARED_LEFT(B,U14) (B:e43) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008 |
| +1.50 | B | g86 TRACK_APPEARED_LEFT(B,U14) (B:e43)<br>g96 TRACK_LOST(B,U14) (B:e49) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_004, track_005, track_008 |
| +1.55 | A | g87 TRACK_APPEARED_RIGHT(A,U15) (A:e45)<br>g88 CLOSING_START(A,U15) (A:e46) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +1.55 | A | g88 CLOSING_START(A,U15) (A:e46)<br>g100 CLOSING_END(A,U15) (A:e52) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +1.60 | A | g89 EGO_PATH_ENTRY(A,U9) (A:e47) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +1.60 | A | g89 EGO_PATH_ENTRY(A,U9) (A:e47)<br>g106 EGO_PATH_EXIT(A,U9) (A:e54) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +1.80 | A | g91 TRACK_APPEARED_LEFT(A,U14) (A:e48) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005 |
| +1.90 | B | g92 EGO_PATH_EXIT(B,U1) (B:e45) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_009: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_004, track_005, track_008 |
| +2.40 | B | g94 EGO_PATH_ENTRY(B,U9) (B:e47) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: no active state<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008 |
| +2.90 | B | g95 CUT_IN_FROM_RIGHT_START(B,U3) (B:e48) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008 |
| +3.35 | A | g99 EGO_PATH_EXIT(A,U13) (A:e51) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003#segment_3: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005, track_011 |
| +3.45 | B | g101 TRACK_APPEARED_RIGHT(B,U15) (B:e50) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009 |
| +4.15 | B | g103 CUT_IN_FROM_RIGHT_START(B,U9) (B:e52) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: CUT_IN_FROM_RIGHT<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_008, track_009 |

## Plain-language reading

- 6.75 s before the reference collision, A started moving (already the case when first observed).
- 6.75 s before the reference collision, B started moving (already the case when first observed).
- 6.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 6.75 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared in front of it.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared on its right.
- 6.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.75 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 6.75 s before the reference collision, A observed anonymous road user U4 start closing in (already the case when first observed).
- 6.75 s before the reference collision, B observed A start closing in (already the case when first observed).
- 6.75 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 6.55 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared in front of it.
- 6.55 s before the reference collision, B observed anonymous road user U7 start closing in (already the case when first observed).
- 6.35 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.35 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.25 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 6.25 s before the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 6.25 s before the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 3.65 s before the reference collision, B's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 3.25 s before the reference collision, B observed A cutting in from the right.
- 3.15 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 3.15 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 2.90 s before the reference collision, A observed B stop closing in.
- 2.60 s before the reference collision, B observed A stop closing in.
- 2.45 s before the reference collision, B observed A's cut-in from the right settle.
- 2.00 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 1.95 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared in front of it.
- 1.65 s before the reference collision, A's time-to-contact with B became critical.
- 1.55 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.45 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared on its right.
- 1.45 s before the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 1.20 s before the reference collision, B's time-to-contact with A became critical.
- 1.15 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 1.10 s before the reference collision, B's radar started tracking anonymous road user U9, which appeared on its right.
- 1.10 s before the reference collision, B observed anonymous road user U9 start closing in (already the case when first observed).
- 1.05 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 0.85 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared in front of it.
- 0.85 s before the reference collision, B's radar started tracking anonymous road user U11, which appeared on its right.
- 0.85 s before the reference collision, B observed anonymous road user U11 start closing in (already the case when first observed).
- 0.55 s before the reference collision, B's radar started tracking anonymous road user U12, which appeared on its right.
- 0.55 s before the reference collision, A observed B start closing in.
- 0.55 s before the reference collision, B observed anonymous road user U12 start closing in (already the case when first observed).
- 0.55 s before the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 0.50 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 0.45 s before the reference collision, B observed A start closing in.
- 0.35 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 192, B: 192 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A observed anonymous road user U3 enter its forward path corridor.
- 0.10 s after the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 0.20 s after the reference collision, B observed anonymous road user U11 enter its forward path corridor.
- 0.30 s after the reference collision, B observed anonymous road user U11 stop closing in.
- 0.35 s after the reference collision, B observed anonymous road user U3 stop closing in.
- 0.45 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 0.50 s after the reference collision, B observed anonymous road user U3 enter its forward path corridor.
- 0.60 s after the reference collision, B observed anonymous road user U12 stop closing in.
- 0.60 s after the reference collision, B observed anonymous road user U9 stop closing in.
- 0.60 s after the reference collision, B observed anonymous road user U12 enter its forward path corridor.
- 0.65 s after the reference collision, B's time-to-contact with anonymous road user U3 became critical.
- 0.70 s after the reference collision, A's time-to-contact with anonymous road user U3 stopped being critical.
- 0.80 s after the reference collision, B's time-to-contact with anonymous road user U1 stopped being critical.
- 0.80 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 0.80 s after the reference collision, A observed anonymous road user U10 leave its forward path corridor.
- 0.80 s after the reference collision, B's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 1.15 s after the reference collision, B stopped moving.
- 1.15 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A's radar started tracking anonymous road user U13, which appeared in front of it.
- 1.15 s after the reference collision, B observed A enter its forward path corridor.
- 1.20 s after the reference collision, A observed B leave its forward path corridor.
- 1.20 s after the reference collision, A stopped moving.
- 1.20 s after the reference collision, A came to a stop.
- 1.30 s after the reference collision, A observed B enter its forward path corridor.
- 1.50 s after the reference collision, B's radar started tracking anonymous road user U14, which appeared on its left.
- 1.55 s after the reference collision, A's radar started tracking anonymous road user U15, which appeared on its right.
- 1.55 s after the reference collision, A observed anonymous road user U15 start closing in (already the case when first observed).
- 1.60 s after the reference collision, A observed anonymous road user U9 enter its forward path corridor.
- 1.75 s after the reference collision, B's time-to-contact with anonymous road user U3 stopped being critical.
- 1.80 s after the reference collision, A's radar started tracking anonymous road user U14, which appeared on its left.
- 1.90 s after the reference collision, B observed anonymous road user U1 leave its forward path corridor.
- 2.30 s after the reference collision, B observed anonymous road user U11 leave its forward path corridor.
- 2.40 s after the reference collision, B observed anonymous road user U9 enter its forward path corridor.
- 2.90 s after the reference collision, B observed anonymous road user U3 cutting in from the right.
- 2.95 s after the reference collision, B's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- 3.20 s after the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 3.20 s after the reference collision, A's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- 3.35 s after the reference collision, A observed anonymous road user U13 leave its forward path corridor.
- 3.40 s after the reference collision, A observed anonymous road user U15 stop closing in.
- 3.45 s after the reference collision, B's radar started tracking anonymous road user U15, which appeared on its right.
- 3.60 s after the reference collision, B observed anonymous road user U3 leave its forward path corridor.
- 4.15 s after the reference collision, B observed anonymous road user U9 cutting in from the right.
- 4.35 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 4.45 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 4.60 s after the reference collision, A observed anonymous road user U9 leave its forward path corridor.
- 4.80 s after the reference collision, B observed anonymous road user U9 leave its forward path corridor.
- 4.80 s after the reference collision, B's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 5.10 s after the reference collision, A's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
