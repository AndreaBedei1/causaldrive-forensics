# Global graph - S23/run_0

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_001, B:track_007 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_003 |
| U6 | anonymous_road_user | anonymous; observed by A, B as A:track_004, B:track_006 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_005, A:track_009, B:track_003, B:track_010, B:track_011 |
| U7 | anonymous_road_user | anonymous; observed by A as A:track_006 |
| U9 | anonymous_road_user | anonymous; observed by A, B as A:track_007, B:track_009 |
| U8 | anonymous_road_user | anonymous; observed by A, B as A:track_008, B:track_008 |
| U4 | anonymous_road_user | anonymous; observed by B as B:track_004 |
| U5 | anonymous_road_user | anonymous; observed by B as B:track_005 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e36 | 8.50 | -8.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e30 | 8.50 | -8.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 745.29 vs 745.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 4.30 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 1.7 m -> 7.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_007 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.5 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.32 m/s over 3.0 s<br>clearance at the contact 0.34 m<br>the only track of A compatible with the contact |
| A:track_003 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 7.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 1.6 m -> 7.1 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_003 |
| A:track_004 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.60 s before the matched collision<br>lost 4.70 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 46.3 m -> 39.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U6: B:track_006, A:track_004 |
| A:track_005 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.40 s before the matched collision<br>continuous up to the contact: last observed 0.90 s before it (window 1.00 s)<br>not approaching before the contact: clearance 1.6 m -> 6.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.23 m/s over 2.1 s (> 1.50)<br>clearance at the contact 5.65 m (beyond 3.50 m: confidence factor 0.77)<br>anonymous road user U3: B:track_003, A:track_005, B:track_010, B:track_011, A:track_009 |
| A:track_006 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.50 s before the matched collision<br>lost 6.40 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 61.2 m -> 54.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U7: A:track_006 |
| A:track_007 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.1 m -> 7.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 7.08 m/s over 1.9 s (> 1.50)<br>clearance at the contact 7.04 m (beyond 3.50 m: confidence factor 0.50)<br>anonymous road user U9: A:track_007, B:track_009 |
| A:track_008 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.90 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.1 m -> 8.3 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.93 m/s over 0.9 s (> 1.50)<br>clearance at the contact 8.30 m (beyond 3.50 m: confidence factor 0.28)<br>anonymous road user U8: B:track_008, A:track_008 |
| A:track_009 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 2.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: B:track_003, A:track_005, B:track_010, B:track_011, A:track_009 |
| B:track_001 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 6.20 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 7.4 m -> 4.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_007 |
| B:track_002 | A | ASSOCIATED | 0.91 | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.5 m -> 0.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.63 m/s over 3.0 s<br>clearance at the contact 0.27 m<br>the only track of B compatible with the contact |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.35 s before the matched collision<br>lost 2.70 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 7.2 m -> 4.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.83 m/s over 0.3 s (> 1.50)<br>anonymous road user U3: B:track_003, A:track_005, B:track_010, B:track_011, A:track_009 |
| B:track_004 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.10 s before the matched collision<br>lost 5.95 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 11.0 m -> 17.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U4: B:track_004 |
| B:track_005 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.65 s before the matched collision<br>lost 5.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 49.4 m -> 42.7 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U5: B:track_005 |
| B:track_006 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.65 s before the matched collision<br>lost 5.15 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 49.1 m -> 42.4 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_006, A:track_004 |
| B:track_007 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 5.00 s before the matched collision<br>lost 3.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 16.9 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_007 |
| B:track_008 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.9 m -> 8.6 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 6.95 m/s over 2.0 s (> 1.50)<br>clearance at the contact 8.62 m (beyond 3.50 m: confidence factor 0.23)<br>anonymous road user U8: B:track_008, A:track_008 |
| B:track_009 | U9 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.5 m -> 6.5 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 7.01 m/s over 1.7 s (> 1.50)<br>clearance at the contact 6.54 m (beyond 3.50 m: confidence factor 0.60)<br>anonymous road user U9: A:track_007, B:track_009 |
| B:track_010 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.8 m -> 14.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.79 m/s over 1.5 s (> 1.50)<br>clearance at the contact 7.79 m (beyond 3.50 m: confidence factor 0.36)<br>anonymous road user U3: B:track_003, A:track_005, B:track_010, B:track_011, A:track_009 |
| B:track_011 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.35 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: B:track_003, A:track_005, B:track_010, B:track_011, A:track_009 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -8.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -8.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -8.50 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -8.50 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -8.50 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -8.50 | TRACK_APPEARED_RIGHT | A | U1 | A:e04 @ 0.00, A:e21 @ 4.20 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g07 | -8.50 | TRACK_APPEARED_RIGHT | A | U2 | A:e05 @ 0.00, A:e13 @ 1.25 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g08 | -8.50 | TRACK_APPEARED_RIGHT | B | A | B:e04 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g09 | -8.50 | TRACK_APPEARED_RIGHT | B | U1 | B:e03 @ 0.00, B:e14 @ 2.30 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g10 | -8.50 | CLOSING_START | A | U1 | A:e06 @ 0.00, A:e18 @ 2.60 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g11 | -8.50 | CLOSING_START | B | U1 | B:e05 @ 0.00, B:e13 @ 2.30 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g12 | -8.35 | TRACK_APPEARED_RIGHT | B | U3 | B:e06 @ 0.15, B:e21 @ 5.80 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -8.35 | CLOSING_START | B | U3 | B:e07 @ 0.15, B:e20 @ 5.80 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g14 | -8.10 | TRACK_APPEARED_RIGHT | B | U4 | B:e08 @ 0.40, B:e15 @ 2.55 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g15 | -7.65 | TRACK_APPEARED_FRONT | B | U6 | B:e09 @ 0.85, B:e16 @ 3.35 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g16 | -7.65 | TRACK_APPEARED_RIGHT | B | U5 | B:e10 @ 0.85, B:e17 @ 3.40 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g17 | -7.65 | CLOSING_START | B | U5 | B:e11 @ 0.85 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g18 | -7.65 | CLOSING_START | B | U6 | B:e12 @ 0.85 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g19 | -7.60 | TRACK_APPEARED_FRONT | A | U6 | A:e07 @ 0.90, A:e20 @ 3.80 | initial_in_ego_path=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g20 | -7.60 | CLOSING_START | A | U6 | A:e08 @ 0.90 | active_at_first_observation=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g21 | -7.50 | TRACK_APPEARED_FRONT | A | U7 | A:e09 @ 1.00, A:e16 @ 2.10 | initial_in_ego_path=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g22 | -7.50 | CLOSING_START | A | U7 | A:e10 @ 1.00 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g23 | -7.40 | TRACK_APPEARED_RIGHT | A | U3 | A:e11 @ 1.10, A:e33 @ 7.60 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g24 | -7.40 | CLOSING_START | A | U3 | A:e12 @ 1.10, A:e24 @ 6.05 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g25 | -7.25 | TRACK_LOST | A | U2 | A:e13 @ 1.25 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g26 | -6.75 | CRITICAL_TTC_START | A | U1 | A:e14 @ 1.75, A:e17 @ 2.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g27 | -6.65 | CUT_IN_FROM_RIGHT_START | A | U1 | A:e15 @ 1.85, A:e19 @ 2.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g28 | -6.40 | TRACK_LOST | A | U7 | A:e16 @ 2.10 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g29 | -6.20 | CLOSING_END | B | U1 | B:e13 @ 2.30 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g30 | -6.20 | TRACK_LOST | B | U1 | B:e14 @ 2.30 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g31 | -5.95 | TRACK_LOST | B | U4 | B:e15 @ 2.55 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g32 | -5.90 | CRITICAL_TTC_END | A | U1 | A:e17 @ 2.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g33 | -5.90 | CLOSING_END | A | U1 | A:e18 @ 2.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g34 | -5.85 | CUT_IN_FROM_RIGHT_END | A | U1 | A:e19 @ 2.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g35 | -5.15 | TRACK_LOST | B | U6 | B:e16 @ 3.35 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g36 | -5.10 | TRACK_LOST | B | U5 | B:e17 @ 3.40 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g37 | -5.00 | TRACK_APPEARED_RIGHT | B | U1 | B:e18 @ 3.50, B:e19 @ 5.40 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g38 | -4.70 | TRACK_LOST | A | U6 | A:e20 @ 3.80 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g39 | -4.30 | TRACK_LOST | A | U1 | A:e21 @ 4.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g40 | -3.20 | CRITICAL_TTC_START | A | U3 | A:e22 @ 5.30, A:e25 @ 6.10 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g41 | -3.10 | CUT_IN_FROM_RIGHT_START | A | U3 | A:e23 @ 5.40, A:e26 @ 6.15 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g42 | -3.10 | TRACK_LOST | B | U1 | B:e19 @ 5.40 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g43 | -2.70 | CLOSING_END | B | U3 | B:e20 @ 5.80 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g44 | -2.70 | TRACK_LOST | B | U3 | B:e21 @ 5.80 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g45 | -2.45 | CLOSING_END | A | U3 | A:e24 @ 6.05 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g46 | -2.40 | CRITICAL_TTC_END | A | U3 | A:e25 @ 6.10 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g47 | -2.35 | CUT_IN_FROM_RIGHT_END | A | U3 | A:e26 @ 6.15 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g48 | -1.95 | TRACK_APPEARED_RIGHT | B | U8 | B:e22 @ 6.55 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g49 | -1.95 | CLOSING_START | B | U8 | B:e23 @ 6.55, B:e37 @ 9.30 | active_at_first_observation=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g50 | -1.90 | TRACK_APPEARED_FRONT | A | U9 | A:e27 @ 6.60 | initial_in_ego_path=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g51 | -1.90 | CLOSING_START | A | U9 | A:e28 @ 6.60, A:e44 @ 9.45 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g52 | -1.70 | TRACK_APPEARED_RIGHT | B | U9 | B:e24 @ 6.80 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g53 | -1.70 | CLOSING_START | B | U9 | B:e25 @ 6.80, B:e38 @ 9.30 | active_at_first_observation=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g54 | -1.55 | TRACK_APPEARED_RIGHT | B | U3 | B:e26 @ 6.95, B:e36 @ 9.20 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g55 | -1.40 | CRITICAL_TTC_START | A | U9 | A:e29 @ 7.10, A:e45 @ 9.60 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g56 | -1.35 | CRITICAL_TTC_START | A | B | A:e30 @ 7.15, A:e37 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g57 | -0.90 | TRACK_APPEARED_RIGHT | A | U8 | A:e31 @ 7.60 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g58 | -0.90 | CLOSING_START | A | U8 | A:e32 @ 7.60, A:e43 @ 9.40 | active_at_first_observation=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g59 | -0.90 | TRACK_LOST | A | U3 | A:e33 @ 7.60 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g60 | -0.80 | CRITICAL_TTC_START | B | A | B:e27 @ 7.70, B:e31 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g61 | -0.70 | CLOSING_START | A | B | A:e34 @ 7.80, A:e40 @ 8.60 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g62 | -0.70 | CLOSING_START | B | A | B:e28 @ 7.80, B:e32 @ 8.55 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g63 | -0.20 | EGO_PATH_ENTRY | B | A | B:e29 @ 8.30, B:e35 @ 9.20 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g64 | -0.05 | CRITICAL_TTC_START | A | U8 | A:e35 @ 8.45, A:e41 @ 8.80 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g65 | 0.00 | COLLISION | - | A, B | A:e36 @ 8.50, B:e30 @ 8.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 745.29, B 745.29 |
| g66 | 0.00 | CRITICAL_TTC_END | A | B | A:e37 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g67 | 0.00 | CRITICAL_TTC_END | B | A | B:e31 @ 8.50 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g68 | 0.05 | CLOSING_END | B | A | B:e32 @ 8.55 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g69 | 0.05 | THROTTLE_END | A | - | A:e38 @ 8.55 |  |
| g70 | 0.05 | THROTTLE_END | B | - | B:e33 @ 8.55 |  |
| g71 | 0.05 | BRAKE_START | A | - | A:e39 @ 8.55 |  |
| g72 | 0.05 | BRAKE_START | B | - | B:e34 @ 8.55 |  |
| g73 | 0.10 | CLOSING_END | A | B | A:e40 @ 8.60 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g74 | 0.30 | CRITICAL_TTC_END | A | U8 | A:e41 @ 8.80 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g75 | 0.35 | EGO_PATH_ENTRY | A | B | A:e42 @ 8.85 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g76 | 0.70 | EGO_PATH_EXIT | B | A | B:e35 @ 9.20 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g77 | 0.70 | TRACK_LOST | B | U3 | B:e36 @ 9.20 | source_track=track_010; aggregation=entity_state_union; source_tracks=['B:track_010'] |
| g78 | 0.80 | CLOSING_END | B | U8 | B:e37 @ 9.30 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g79 | 0.80 | CLOSING_END | B | U9 | B:e38 @ 9.30 | source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g80 | 0.90 | CLOSING_END | A | U8 | A:e43 @ 9.40 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g81 | 0.95 | CLOSING_END | A | U9 | A:e44 @ 9.45 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g82 | 1.10 | CRITICAL_TTC_END | A | U9 | A:e45 @ 9.60 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g83 | 1.10 | MOVING_END | B | - | B:e39 @ 9.60 |  |
| g84 | 1.10 | STOP_START | B | - | B:e40 @ 9.60 |  |
| g85 | 1.20 | MOVING_END | A | - | A:e46 @ 9.70 |  |
| g86 | 1.20 | STOP_START | A | - | A:e47 @ 9.70 |  |
| g87 | 1.35 | TRACK_APPEARED_RIGHT | B | U3 | B:e41 @ 9.85 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g88 | 1.35 | CLOSING_START | B | U3 | B:e42 @ 9.85 | active_at_first_observation=True; source_track=track_011; aggregation=entity_state_union; source_tracks=['B:track_011'] |
| g89 | 2.05 | TRACK_APPEARED_RIGHT | A | U3 | A:e48 @ 10.55 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g90 | 2.05 | CLOSING_START | A | U3 | A:e49 @ 10.55 | active_at_first_observation=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |

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
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
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
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g57 --PRECEDES--> g60
    g58 --PRECEDES--> g60
    g59 --PRECEDES--> g60
    g60 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g62 --PRECEDES--> g63
    g63 --PRECEDES--> g64
    g64 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g64 --PRECEDES--> g67
    g65 --PRECEDES--> g68
    g65 --PRECEDES--> g69
    g65 --PRECEDES--> g70
    g65 --PRECEDES--> g71
    g65 --PRECEDES--> g72
    g66 --PRECEDES--> g68
    g66 --PRECEDES--> g69
    g66 --PRECEDES--> g70
    g66 --PRECEDES--> g71
    g66 --PRECEDES--> g72
    g67 --PRECEDES--> g68
    g67 --PRECEDES--> g69
    g67 --PRECEDES--> g70
    g67 --PRECEDES--> g71
    g67 --PRECEDES--> g72
    g68 --PRECEDES--> g73
    g69 --PRECEDES--> g73
    g70 --PRECEDES--> g73
    g71 --PRECEDES--> g73
    g72 --PRECEDES--> g73
    g73 --PRECEDES--> g74
    g74 --PRECEDES--> g75
    g75 --PRECEDES--> g76
    g75 --PRECEDES--> g77
    g76 --PRECEDES--> g78
    g76 --PRECEDES--> g79
    g77 --PRECEDES--> g78
    g77 --PRECEDES--> g79
    g78 --PRECEDES--> g80
    g79 --PRECEDES--> g80
    g80 --PRECEDES--> g81
    g81 --PRECEDES--> g82
    g81 --PRECEDES--> g83
    g81 --PRECEDES--> g84
    g82 --PRECEDES--> g85
    g82 --PRECEDES--> g86
    g83 --PRECEDES--> g85
    g83 --PRECEDES--> g86
    g84 --PRECEDES--> g85
    g84 --PRECEDES--> g86
    g85 --PRECEDES--> g87
    g85 --PRECEDES--> g88
    g86 --PRECEDES--> g87
    g86 --PRECEDES--> g88
    g87 --PRECEDES--> g89
    g87 --PRECEDES--> g90
    g88 --PRECEDES--> g89
    g88 --PRECEDES--> g90
    g06 --SAME_TRACK--> g10
    g19 --SAME_TRACK--> g20
    g21 --SAME_TRACK--> g22
    g23 --SAME_TRACK--> g24
    g07 --SAME_TRACK--> g25
    g06 --SAME_TRACK--> g26
    g06 --SAME_TRACK--> g27
    g21 --SAME_TRACK--> g28
    g06 --SAME_TRACK--> g32
    g06 --SAME_TRACK--> g33
    g06 --SAME_TRACK--> g34
    g19 --SAME_TRACK--> g38
    g06 --SAME_TRACK--> g39
    g23 --SAME_TRACK--> g40
    g23 --SAME_TRACK--> g41
    g23 --SAME_TRACK--> g45
    g23 --SAME_TRACK--> g46
    g23 --SAME_TRACK--> g47
    g50 --SAME_TRACK--> g51
    g50 --SAME_TRACK--> g55
    g05 --SAME_TRACK--> g56
    g57 --SAME_TRACK--> g58
    g23 --SAME_TRACK--> g59
    g05 --SAME_TRACK--> g61
    g57 --SAME_TRACK--> g64
    g05 --SAME_TRACK--> g66
    g05 --SAME_TRACK--> g73
    g57 --SAME_TRACK--> g74
    g05 --SAME_TRACK--> g75
    g57 --SAME_TRACK--> g80
    g50 --SAME_TRACK--> g81
    g50 --SAME_TRACK--> g82
    g89 --SAME_TRACK--> g90
    g09 --SAME_TRACK--> g11
    g12 --SAME_TRACK--> g13
    g16 --SAME_TRACK--> g17
    g15 --SAME_TRACK--> g18
    g09 --SAME_TRACK--> g29
    g09 --SAME_TRACK--> g30
    g14 --SAME_TRACK--> g31
    g15 --SAME_TRACK--> g35
    g16 --SAME_TRACK--> g36
    g37 --SAME_TRACK--> g42
    g12 --SAME_TRACK--> g43
    g12 --SAME_TRACK--> g44
    g48 --SAME_TRACK--> g49
    g52 --SAME_TRACK--> g53
    g08 --SAME_TRACK--> g60
    g08 --SAME_TRACK--> g62
    g08 --SAME_TRACK--> g63
    g08 --SAME_TRACK--> g67
    g08 --SAME_TRACK--> g68
    g08 --SAME_TRACK--> g76
    g54 --SAME_TRACK--> g77
    g48 --SAME_TRACK--> g78
    g52 --SAME_TRACK--> g79
    g87 --SAME_TRACK--> g88
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -8.50 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U2); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(B,U1) |
| -8.35 | TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3) |
| -8.10 | TRACK_APPEARED_RIGHT(B,U4) |
| -7.65 | TRACK_APPEARED_FRONT(B,U6); TRACK_APPEARED_RIGHT(B,U5); CLOSING_START(B,U5); CLOSING_START(B,U6) |
| -7.60 | TRACK_APPEARED_FRONT(A,U6); CLOSING_START(A,U6) |
| -7.50 | TRACK_APPEARED_FRONT(A,U7); CLOSING_START(A,U7) |
| -7.40 | TRACK_APPEARED_RIGHT(A,U3); CLOSING_START(A,U3) |
| -7.25 | TRACK_LOST(A,U2) |
| -6.75 | CRITICAL_TTC_START(A,U1) |
| -6.65 | CUT_IN_FROM_RIGHT_START(A,U1) |
| -6.40 | TRACK_LOST(A,U7) |
| -6.20 | CLOSING_END(B,U1); TRACK_LOST(B,U1) |
| -5.95 | TRACK_LOST(B,U4) |
| -5.90 | CRITICAL_TTC_END(A,U1); CLOSING_END(A,U1) |
| -5.85 | CUT_IN_FROM_RIGHT_END(A,U1) |
| -5.15 | TRACK_LOST(B,U6) |
| -5.10 | TRACK_LOST(B,U5) |
| -5.00 | TRACK_APPEARED_RIGHT(B,U1) |
| -4.70 | TRACK_LOST(A,U6) |
| -4.30 | TRACK_LOST(A,U1) |
| -3.20 | CRITICAL_TTC_START(A,U3) |
| -3.10 | CUT_IN_FROM_RIGHT_START(A,U3); TRACK_LOST(B,U1) |
| -2.70 | CLOSING_END(B,U3); TRACK_LOST(B,U3) |
| -2.45 | CLOSING_END(A,U3) |
| -2.40 | CRITICAL_TTC_END(A,U3) |
| -2.35 | CUT_IN_FROM_RIGHT_END(A,U3) |
| -1.95 | TRACK_APPEARED_RIGHT(B,U8); CLOSING_START(B,U8) |
| -1.90 | TRACK_APPEARED_FRONT(A,U9); CLOSING_START(A,U9) |
| -1.70 | TRACK_APPEARED_RIGHT(B,U9); CLOSING_START(B,U9) |
| -1.55 | TRACK_APPEARED_RIGHT(B,U3) |
| -1.40 | CRITICAL_TTC_START(A,U9) |
| -1.35 | CRITICAL_TTC_START(A,B) |
| -0.90 | TRACK_APPEARED_RIGHT(A,U8); CLOSING_START(A,U8); TRACK_LOST(A,U3) |
| -0.80 | CRITICAL_TTC_START(B,A) |
| -0.70 | CLOSING_START(A,B); CLOSING_START(B,A) |
| -0.20 | EGO_PATH_ENTRY(B,A) |
| -0.05 | CRITICAL_TTC_START(A,U8) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A) |
| +0.05 | CLOSING_END(B,A); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CLOSING_END(A,B) |
| +0.30 | CRITICAL_TTC_END(A,U8) |
| +0.35 | EGO_PATH_ENTRY(A,B) |
| +0.70 | EGO_PATH_EXIT(B,A); TRACK_LOST(B,U3) |
| +0.80 | CLOSING_END(B,U8); CLOSING_END(B,U9) |
| +0.90 | CLOSING_END(A,U8) |
| +0.95 | CLOSING_END(A,U9) |
| +1.10 | CRITICAL_TTC_END(A,U9); MOVING_END(B); STOP_START(B) |
| +1.20 | MOVING_END(A); STOP_START(A) |
| +1.35 | TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3) |
| +2.05 | TRACK_APPEARED_RIGHT(A,U3); CLOSING_START(A,U3) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): critical TTC already active before the cut-in: CRITICAL_TTC_START 1.75 <= CUT_IN_FROM_RIGHT_START 1.85 (+0.10 s) [local times; t_global: cut_in -6.65, critical_ttc_start -6.75, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 7.15, COLLISION with B 8.50 (+1.35 s); EGO_PATH_ENTRY 8.85 after critical TTC (+1.70 s) [local times; t_global: critical_ttc_start -1.35, ego_path_entry +0.35, collision +0.00]
- A's track_005 (unidentified U3): critical TTC already active before the cut-in: CRITICAL_TTC_START 5.30 <= CUT_IN_FROM_RIGHT_START 5.40 (+0.10 s) [local times; t_global: cut_in -3.10, critical_ttc_start -3.20, collision +0.00]
- A's track_007 (unidentified U9): CRITICAL_TTC_START 7.10, COLLISION 8.50 (+1.40 s) [local times; t_global: critical_ttc_start -1.40, collision +0.00]
- A's track_008 (unidentified U8): CRITICAL_TTC_START 8.45, COLLISION 8.50 (+0.05 s) [local times; t_global: critical_ttc_start -0.05, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.70, COLLISION with A 8.50 (+0.80 s); EGO_PATH_ENTRY 8.30 after critical TTC (+0.60 s) [local times; t_global: critical_ttc_start -0.80, ego_path_entry -0.20, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -8.50 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g07 TRACK_APPEARED_RIGHT(A,U2) (A:e05)<br>g10 CLOSING_START(A,U1) (A:e06) | ego: not yet observed |
| -8.50 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g08 TRACK_APPEARED_RIGHT(B,A) (B:e04)<br>g09 TRACK_APPEARED_RIGHT(B,U1) (B:e03)<br>g11 CLOSING_START(B,U1) (B:e05) | ego: not yet observed |
| -8.50 | A | g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g39 TRACK_LOST(A,U1) (A:e21) | ego: not yet observed |
| -8.50 | A | g07 TRACK_APPEARED_RIGHT(A,U2) (A:e05)<br>g25 TRACK_LOST(A,U2) (A:e13) | ego: not yet observed |
| -8.50 | B | g09 TRACK_APPEARED_RIGHT(B,U1) (B:e03)<br>g11 CLOSING_START(B,U1) (B:e05)<br>g29 CLOSING_END(B,U1) (B:e13)<br>g30 TRACK_LOST(B,U1) (B:e14) | ego: not yet observed |
| -8.50 | A | g10 CLOSING_START(A,U1) (A:e06)<br>g26 CRITICAL_TTC_START(A,U1) (A:e14)<br>g32 CRITICAL_TTC_END(A,U1) (A:e17)<br>g33 CLOSING_END(A,U1) (A:e18) | ego: not yet observed |
| -8.35 | B | g12 TRACK_APPEARED_RIGHT(B,U3) (B:e06)<br>g13 CLOSING_START(B,U3) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC? |
| -8.35 | B | g12 TRACK_APPEARED_RIGHT(B,U3) (B:e06)<br>g13 CLOSING_START(B,U3) (B:e07)<br>g43 CLOSING_END(B,U3) (B:e20)<br>g44 TRACK_LOST(B,U3) (B:e21) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC? |
| -8.10 | B | g14 TRACK_APPEARED_RIGHT(B,U4) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC? |
| -8.10 | B | g14 TRACK_APPEARED_RIGHT(B,U4) (B:e08)<br>g31 TRACK_LOST(B,U4) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC? |
| -7.65 | B | g15 TRACK_APPEARED_FRONT(B,U6) (B:e09)<br>g16 TRACK_APPEARED_RIGHT(B,U5) (B:e10)<br>g17 CLOSING_START(B,U5) (B:e11)<br>g18 CLOSING_START(B,U6) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CRITICAL_TTC? |
| -7.65 | B | g15 TRACK_APPEARED_FRONT(B,U6) (B:e09)<br>g35 TRACK_LOST(B,U6) (B:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CRITICAL_TTC? |
| -7.65 | B | g16 TRACK_APPEARED_RIGHT(B,U5) (B:e10)<br>g36 TRACK_LOST(B,U5) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CRITICAL_TTC? |
| -7.60 | A | g19 TRACK_APPEARED_FRONT(A,U6) (A:e07)<br>g20 CLOSING_START(A,U6) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state |
| -7.60 | A | g19 TRACK_APPEARED_FRONT(A,U6) (A:e07)<br>g38 TRACK_LOST(A,U6) (A:e20) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state |
| -7.50 | A | g21 TRACK_APPEARED_FRONT(A,U7) (A:e09)<br>g22 CLOSING_START(A,U7) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC? |
| -7.50 | A | g21 TRACK_APPEARED_FRONT(A,U7) (A:e09)<br>g28 TRACK_LOST(A,U7) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC? |
| -7.40 | A | g23 TRACK_APPEARED_RIGHT(A,U3) (A:e11)<br>g24 CLOSING_START(A,U3) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, IN_EGO_PATH, CRITICAL_TTC? |
| -7.40 | A | g23 TRACK_APPEARED_RIGHT(A,U3) (A:e11)<br>g57 TRACK_APPEARED_RIGHT(A,U8) (A:e31)<br>g58 CLOSING_START(A,U8) (A:e32)<br>g59 TRACK_LOST(A,U3) (A:e33) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, IN_EGO_PATH, CRITICAL_TTC? |
| -7.40 | A | g24 CLOSING_START(A,U3) (A:e12)<br>g45 CLOSING_END(A,U3) (A:e24) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_006: CLOSING, IN_EGO_PATH, CRITICAL_TTC? |
| -6.75 | A | g26 CRITICAL_TTC_START(A,U1) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003 |
| -6.65 | A | g27 CUT_IN_FROM_RIGHT_START(A,U1) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003 |
| -6.65 | A | g27 CUT_IN_FROM_RIGHT_START(A,U1) (A:e15)<br>g34 CUT_IN_FROM_RIGHT_END(A,U1) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_006: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003 |
| -5.00 | B | g37 TRACK_APPEARED_RIGHT(B,U1) (B:e18) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006 |
| -5.00 | B | g37 TRACK_APPEARED_RIGHT(B,U1) (B:e18)<br>g42 TRACK_LOST(B,U1) (B:e19) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006 |
| -3.20 | A | g40 CRITICAL_TTC_START(A,U3) (A:e22) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -3.20 | A | g40 CRITICAL_TTC_START(A,U3) (A:e22)<br>g46 CRITICAL_TTC_END(A,U3) (A:e25) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -3.10 | A | g41 CUT_IN_FROM_RIGHT_START(A,U3) (A:e23) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -3.10 | A | g41 CUT_IN_FROM_RIGHT_START(A,U3) (A:e23)<br>g47 CUT_IN_FROM_RIGHT_END(A,U3) (A:e26) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -1.95 | B | g48 TRACK_APPEARED_RIGHT(B,U8) (B:e22)<br>g49 CLOSING_START(B,U8) (B:e23) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -1.95 | B | g49 CLOSING_START(B,U8) (B:e23)<br>g53 CLOSING_START(B,U9) (B:e25)<br>g78 CLOSING_END(B,U8) (B:e37)<br>g79 CLOSING_END(B,U9) (B:e38) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -1.90 | A | g50 TRACK_APPEARED_FRONT(A,U9) (A:e27)<br>g51 CLOSING_START(A,U9) (A:e28) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -1.90 | A | g51 CLOSING_START(A,U9) (A:e28)<br>g81 CLOSING_END(A,U9) (A:e44) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -1.70 | B | g52 TRACK_APPEARED_RIGHT(B,U9) (B:e24)<br>g53 CLOSING_START(B,U9) (B:e25) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -1.55 | B | g54 TRACK_APPEARED_RIGHT(B,U3) (B:e26) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING, CRITICAL_TTC?<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -1.55 | B | g54 TRACK_APPEARED_RIGHT(B,U3) (B:e26)<br>g63 EGO_PATH_ENTRY(B,A) (B:e29)<br>g76 EGO_PATH_EXIT(B,A) (B:e35)<br>g77 TRACK_LOST(B,U3) (B:e36) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING, CRITICAL_TTC?<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -1.40 | A | g55 CRITICAL_TTC_START(A,U9) (A:e29) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track_007: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -1.40 | A | g55 CRITICAL_TTC_START(A,U9) (A:e29)<br>g82 CRITICAL_TTC_END(A,U9) (A:e45) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track_007: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -1.35 | A | g56 CRITICAL_TTC_START(A,B) (A:e30) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -1.35 | A | g56 CRITICAL_TTC_START(A,B) (A:e30)<br>g65 COLLISION(A,B) (A:e36)<br>g66 CRITICAL_TTC_END(A,B) (A:e37) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_005: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -0.90 | A | g58 CLOSING_START(A,U8) (A:e32)<br>g80 CLOSING_END(A,U8) (A:e43) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_005: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_006 |
| -0.80 | B | g60 CRITICAL_TTC_START(B,A) (B:e27) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -0.80 | B | g60 CRITICAL_TTC_START(B,A) (B:e27)<br>g65 COLLISION(A,B) (B:e30)<br>g67 CRITICAL_TTC_END(B,A) (B:e31) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -0.70 | A | g61 CLOSING_START(A,B) (A:e34) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |
| -0.70 | A | g61 CLOSING_START(A,B) (A:e34)<br>g73 CLOSING_END(A,B) (A:e40) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |
| -0.70 | B | g62 CLOSING_START(B,A) (B:e28) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -0.70 | B | g62 CLOSING_START(B,A) (B:e28)<br>g68 CLOSING_END(B,A) (B:e32)<br>g70 THROTTLE_END(B) (B:e33)<br>g72 BRAKE_START(B) (B:e34) | ego: MOVING, THROTTLE<br>track_002: CRITICAL_TTC<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -0.20 | B | g63 EGO_PATH_ENTRY(B,A) (B:e29) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007 |
| -0.05 | A | g64 CRITICAL_TTC_START(A,U8) (A:e35) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |
| -0.05 | A | g64 CRITICAL_TTC_START(A,U8) (A:e35)<br>g74 CRITICAL_TTC_END(A,U8) (A:e41) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |
| +0.05 | A | g69 THROTTLE_END(A) (A:e38)<br>g71 BRAKE_START(A) (A:e39) | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |
| +0.35 | A | g75 EGO_PATH_ENTRY(A,B) (A:e42) | ego: MOVING, BRAKE<br>track_002: no active state<br>track_007: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |
| +1.10 | B | g83 MOVING_END(B) (B:e39)<br>g84 STOP_START(B) (B:e40) | ego: MOVING, BRAKE<br>track_002: no active state<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_010 |
| +1.20 | A | g85 MOVING_END(A) (A:e46)<br>g86 STOP_START(A) (A:e47) | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |
| +1.35 | B | g87 TRACK_APPEARED_RIGHT(B,U3) (B:e41)<br>g88 CLOSING_START(B,U3) (B:e42) | ego: STOP, BRAKE<br>track_002: no active state<br>track_008: no active state<br>track_009: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_010 |
| +2.05 | A | g89 TRACK_APPEARED_RIGHT(A,U3) (A:e48)<br>g90 CLOSING_START(A,U3) (A:e49) | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006 |

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
- 8.35 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 8.35 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 8.10 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared on its right.
- 7.65 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared in front of it.
- 7.65 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its right.
- 7.65 s before the reference collision, B observed anonymous road user U5 start closing in (already the case when first observed).
- 7.65 s before the reference collision, B observed anonymous road user U6 start closing in (already the case when first observed).
- 7.60 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared in front of it.
- 7.60 s before the reference collision, A observed anonymous road user U6 start closing in (already the case when first observed).
- 7.50 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared in front of it.
- 7.50 s before the reference collision, A observed anonymous road user U7 start closing in (already the case when first observed).
- 7.40 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 7.40 s before the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
- 7.25 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 6.75 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 6.65 s before the reference collision, A observed anonymous road user U1 cutting in from the right.
- 6.40 s before the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 6.20 s before the reference collision, B observed anonymous road user U1 stop closing in.
- 6.20 s before the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 5.95 s before the reference collision, B's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 5.90 s before the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 5.90 s before the reference collision, A observed anonymous road user U1 stop closing in.
- 5.85 s before the reference collision, A observed anonymous road user U1's cut-in from the right settle.
- 5.15 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 5.10 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 5.00 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 4.70 s before the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 4.30 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 3.20 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 3.10 s before the reference collision, A observed anonymous road user U3 cutting in from the right.
- 3.10 s before the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 2.70 s before the reference collision, B observed anonymous road user U3 stop closing in.
- 2.70 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.45 s before the reference collision, A observed anonymous road user U3 stop closing in.
- 2.40 s before the reference collision, A's time-to-contact with anonymous road user U3 stopped being critical.
- 2.35 s before the reference collision, A observed anonymous road user U3's cut-in from the right settle.
- 1.95 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared on its right.
- 1.95 s before the reference collision, B observed anonymous road user U8 start closing in (already the case when first observed).
- 1.90 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared in front of it.
- 1.90 s before the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 1.70 s before the reference collision, B's radar started tracking anonymous road user U9, which appeared on its right.
- 1.70 s before the reference collision, B observed anonymous road user U9 start closing in (already the case when first observed).
- 1.55 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 1.40 s before the reference collision, A's time-to-contact with anonymous road user U9 became critical.
- 1.35 s before the reference collision, A's time-to-contact with B became critical.
- 0.90 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared on its right.
- 0.90 s before the reference collision, A observed anonymous road user U8 start closing in (already the case when first observed).
- 0.90 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.80 s before the reference collision, B's time-to-contact with A became critical.
- 0.70 s before the reference collision, A observed B start closing in.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.20 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's time-to-contact with anonymous road user U8 became critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 745, B: 745 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A observed B stop closing in.
- 0.30 s after the reference collision, A's time-to-contact with anonymous road user U8 stopped being critical.
- 0.35 s after the reference collision, A observed B enter its forward path corridor.
- 0.70 s after the reference collision, B observed A leave its forward path corridor.
- 0.70 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, B observed anonymous road user U8 stop closing in.
- 0.80 s after the reference collision, B observed anonymous road user U9 stop closing in.
- 0.90 s after the reference collision, A observed anonymous road user U8 stop closing in.
- 0.95 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 1.10 s after the reference collision, A's time-to-contact with anonymous road user U9 stopped being critical.
- 1.10 s after the reference collision, B stopped moving.
- 1.10 s after the reference collision, B came to a stop.
- 1.20 s after the reference collision, A stopped moving.
- 1.20 s after the reference collision, A came to a stop.
- 1.35 s after the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 1.35 s after the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 2.05 s after the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 2.05 s after the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
