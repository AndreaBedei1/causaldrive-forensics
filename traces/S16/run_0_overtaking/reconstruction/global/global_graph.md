# Global graph - S16/run_0_overtaking

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_006 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_004 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_002 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_002 |
| U4 | anonymous_road_user | anonymous; observed by A, B as A:track_004, A:track_007, B:track_006 |
| U5 | anonymous_road_user | anonymous; observed by A as A:track_005 |
| U9 | anonymous_road_user | anonymous; observed by A as A:track_008 |
| U10 | anonymous_road_user | anonymous; observed by A as A:track_009 |
| U11 | anonymous_road_user | anonymous; observed by A, B as A:track_010, B:track_009 |
| U12 | anonymous_road_user | anonymous; observed by A, B as A:track_011, A:track_012, B:track_008 |
| U6 | anonymous_road_user | anonymous; observed by B as B:track_003 |
| U7 | anonymous_road_user | anonymous; observed by B as B:track_005 |
| U8 | anonymous_road_user | anonymous; observed by B as B:track_007 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e24 | 6.75 | -6.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e25 | 6.75 | -6.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 191.84 vs 191.84 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.5 m -> 12.5 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.10 m/s for reference)<br>clearance at the contact 10.48 m (beyond 3.50 m: confidence factor 0.07)<br>anonymous road user U1: A:track_001, B:track_004 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 3.15 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 21.4 m -> 23.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_002 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 11.9 m -> 12.3 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 1.93 m/s for reference)<br>clearance at the contact 11.91 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U3: A:track_003, B:track_002 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 3.15 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 26.6 m -> 24.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>retrospective: identity resolved from later evidence at -1.15 s (entity seen by several observers), carried back 2.00 s with the motion model; posterior 0.951 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U4: A:track_004, A:track_007, B:track_006 |
| A:track_005 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 6.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 6.4 m -> 7.4 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U5: A:track_005 |
| A:track_006 | B | ASSOCIATED | 0.76 | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.1 m -> 0.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 1.10 m/s for reference)<br>clearance at the contact 0.12 m<br>the only track of A compatible with the contact |
| A:track_007 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.5 m -> 19.2 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 4.03 m/s for reference)<br>clearance at the contact 19.18 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U4: A:track_004, A:track_007, B:track_006 |
| A:track_008 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 27.8 m -> 28.9 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.18 m/s for reference)<br>clearance at the contact 27.77 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U9: A:track_008 |
| A:track_009 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U10: A:track_009 |
| A:track_010 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U11: A:track_010, B:track_009 |
| A:track_011 | U12 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U12: A:track_011, B:track_008, A:track_012 |
| A:track_012 | U12 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 2.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U12: A:track_011, B:track_008, A:track_012 |
| B:track_001 | A | ASSOCIATED | 0.53 | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 0.8 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 1.68 m/s for reference)<br>clearance at the contact 0.00 m<br>the only compatible track of B touching it at the contact (clearance 0.00 m; track_002 at 10.53 m) |
| B:track_002 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.4 m -> 10.5 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.10 m/s for reference)<br>clearance at the contact 10.53 m (beyond 3.50 m: confidence factor 0.06)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_001, track_002)<br>anonymous road user U3: A:track_003, B:track_002 |
| B:track_003 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 1.55 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 12.3 m -> 16.2 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.70 m/s for reference)<br>anonymous road user U6: B:track_003 |
| B:track_004 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.3 m -> 10.3 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.93 m/s for reference)<br>clearance at the contact 10.30 m (beyond 3.50 m: confidence factor 0.08)<br>anonymous road user U1: A:track_001, B:track_004 |
| B:track_005 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 5.95 s before the matched collision<br>lost 3.65 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 35.1 m -> 33.1 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_005 |
| B:track_006 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 21.8 m -> 17.9 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 2.04 m/s for reference)<br>clearance at the contact 17.91 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U4: A:track_004, A:track_007, B:track_006 |
| B:track_007 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.85 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 28.0 m -> 26.3 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.02 m/s for reference)<br>clearance at the contact 26.27 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U8: B:track_007 |
| B:track_008 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U12: A:track_011, B:track_008, A:track_012 |
| B:track_009 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U11: A:track_010, B:track_009 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.75 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.75 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.75 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -6.75 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -6.75 | TRACK_APPEARED_FRONT | A | U3 | A:e03 @ 0.00 | initial_in_ego_path=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g06 | -6.75 | TRACK_APPEARED_LEFT | A | U1 | A:e04 @ 0.00, A:e49 @ 11.20 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g07 | -6.75 | TRACK_APPEARED_LEFT | A | U2 | A:e05 @ 0.00, A:e13 @ 3.60 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g08 | -6.75 | TRACK_APPEARED_RIGHT | A | U4 | A:e06 @ 0.00, A:e14 @ 3.60 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g09 | -6.75 | TRACK_APPEARED_RIGHT | A | U5 | A:e07 @ 0.00, A:e12 @ 0.50 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g10 | -6.75 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g11 | -6.75 | TRACK_APPEARED_RIGHT | B | U3 | B:e04 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g12 | -6.75 | TRACK_APPEARED_RIGHT | B | U6 | B:e05 @ 0.00, B:e16 @ 5.20 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g13 | -6.75 | CLOSING_START | A | U4 | A:e08 @ 0.00 | active_at_first_observation=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g14 | -6.75 | CLOSING_START | B | A | B:e06 @ 0.00, B:e14 @ 4.20 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g15 | -6.75 | CLOSING_START | B | U3 | B:e07 @ 0.00, B:e32 @ 7.10 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g16 | -6.65 | TRACK_APPEARED_FRONT | B | U1 | B:e08 @ 0.10, B:e47 @ 11.10 | initial_in_ego_path=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g17 | -6.35 | TRACK_APPEARED_LEFT | A | B | A:e09 @ 0.40 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g18 | -6.35 | CLOSING_START | A | B | A:e10 @ 0.40, A:e15 @ 3.90 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g19 | -6.25 | CRITICAL_TTC_START | A | U3 | A:e11 @ 0.50, A:e33 @ 7.45 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g20 | -6.25 | TRACK_LOST | A | U5 | A:e12 @ 0.50 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g21 | -6.15 | CRITICAL_TTC_START | B | U1 | B:e09 @ 0.60, B:e37 @ 7.55 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g22 | -5.95 | TRACK_APPEARED_FRONT | B | U7 | B:e10 @ 0.80, B:e12 @ 3.10 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g23 | -5.95 | CLOSING_START | B | U7 | B:e11 @ 0.80 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g24 | -3.65 | TRACK_LOST | B | U7 | B:e12 @ 3.10 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g25 | -3.35 | CUT_IN_FROM_RIGHT_START | B | A | B:e13 @ 3.40, B:e15 @ 4.45 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g26 | -3.15 | TRACK_LOST | A | U2 | A:e13 @ 3.60 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g27 | -3.15 | TRACK_LOST | A | U4 | A:e14 @ 3.60 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g28 | -2.85 | CLOSING_END | A | B | A:e15 @ 3.90 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g29 | -2.55 | CLOSING_END | B | A | B:e14 @ 4.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g30 | -2.30 | CUT_IN_FROM_RIGHT_END | B | A | B:e15 @ 4.45 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g31 | -1.65 | CRITICAL_TTC_START | A | B | A:e16 @ 5.10, A:e25 @ 6.75 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g32 | -1.55 | TRACK_LOST | B | U6 | B:e16 @ 5.20 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g33 | -1.35 | CRITICAL_TTC_START | B | A | B:e17 @ 5.40, B:e26 @ 6.75 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g34 | -1.20 | CRITICAL_TTC_START | A | U1 | A:e17 @ 5.55 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g35 | -1.15 | TRACK_APPEARED_RIGHT | A | U4 | A:e18 @ 5.60 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g36 | -1.15 | CLOSING_START | A | U4 | A:e19 @ 5.60, A:e31 @ 7.20 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g37 | -1.10 | TRACK_APPEARED_RIGHT | B | U4 | B:e18 @ 5.65 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g38 | -1.10 | EGO_PATH_ENTRY | A | U1 | A:e20 @ 5.65, A:e34 @ 7.55 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g39 | -1.10 | CLOSING_START | B | U4 | B:e19 @ 5.65, B:e35 @ 7.35 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g40 | -0.90 | CLOSING_START | B | A | B:e20 @ 5.85, B:e24 @ 6.55 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g41 | -0.85 | TRACK_APPEARED_RIGHT | B | U8 | B:e21 @ 5.90, B:e49 @ 11.55 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g42 | -0.85 | CLOSING_START | B | U8 | B:e22 @ 5.90, B:e31 @ 7.05 | active_at_first_observation=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g43 | -0.75 | TRACK_APPEARED_FRONT | A | U9 | A:e21 @ 6.00, A:e51 @ 11.85 | initial_in_ego_path=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g44 | -0.60 | CLOSING_START | A | B | A:e22 @ 6.15, A:e27 @ 6.80 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g45 | -0.50 | EGO_PATH_ENTRY | B | A | B:e23 @ 6.25, B:e36 @ 7.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g46 | -0.40 | EGO_PATH_ENTRY | A | B | A:e23 @ 6.35 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g47 | -0.20 | CLOSING_END | B | A | B:e24 @ 6.55 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g48 | 0.00 | COLLISION | - | A, B | A:e24 @ 6.75, B:e25 @ 6.75 | matched_event=collision_001; reference_event=True; peak_impulse=A 191.84, B 191.84 |
| g49 | 0.00 | CRITICAL_TTC_END | A | B | A:e25 @ 6.75 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g50 | 0.00 | CRITICAL_TTC_END | B | A | B:e26 @ 6.75 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g51 | 0.00 | EGO_PATH_EXIT | A | U3 | A:e26 @ 6.75 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g52 | 0.05 | CLOSING_END | A | B | A:e27 @ 6.80 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g53 | 0.05 | THROTTLE_END | A | - | A:e28 @ 6.80 |  |
| g54 | 0.05 | THROTTLE_END | B | - | B:e27 @ 6.80 |  |
| g55 | 0.05 | BRAKE_START | A | - | A:e29 @ 6.80 |  |
| g56 | 0.05 | BRAKE_START | B | - | B:e28 @ 6.80 |  |
| g57 | 0.10 | EGO_PATH_ENTRY | A | U3 | A:e30 @ 6.85, A:e44 @ 9.95 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g58 | 0.15 | EGO_PATH_ENTRY | B | U8 | B:e29 @ 6.90, B:e42 @ 9.00 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g59 | 0.20 | CLOSING_START | B | A | B:e30 @ 6.95, B:e34 @ 7.35 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g60 | 0.30 | CLOSING_END | B | U8 | B:e31 @ 7.05 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g61 | 0.35 | CLOSING_END | B | U3 | B:e32 @ 7.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g62 | 0.45 | CLOSING_END | A | U4 | A:e31 @ 7.20 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g63 | 0.45 | EGO_PATH_ENTRY | B | U3 | B:e33 @ 7.20, B:e46 @ 10.35 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g64 | 0.60 | CLOSING_END | B | A | B:e34 @ 7.35 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g65 | 0.60 | CLOSING_END | B | U4 | B:e35 @ 7.35 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g66 | 0.60 | EGO_PATH_EXIT | A | U9 | A:e32 @ 7.35 | geometry=estimated_body; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g67 | 0.65 | EGO_PATH_EXIT | B | A | B:e36 @ 7.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g68 | 0.70 | CRITICAL_TTC_END | A | U3 | A:e33 @ 7.45 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g69 | 0.80 | CRITICAL_TTC_END | B | U1 | B:e37 @ 7.55 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g70 | 0.80 | EGO_PATH_EXIT | A | U1 | A:e34 @ 7.55 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g71 | 1.15 | MOVING_END | B | - | B:e38 @ 7.90 |  |
| g72 | 1.15 | STOP_START | B | - | B:e39 @ 7.90 |  |
| g73 | 1.20 | MOVING_END | A | - | A:e35 @ 7.95 |  |
| g74 | 1.20 | STOP_START | A | - | A:e36 @ 7.95 |  |
| g75 | 1.30 | TRACK_APPEARED_FRONT | A | U10 | A:e37 @ 8.05, A:e48 @ 10.75 | initial_in_ego_path=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g76 | 1.50 | EGO_PATH_ENTRY | A | U4 | A:e38 @ 8.25, A:e50 @ 11.30 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g77 | 1.55 | TRACK_APPEARED_RIGHT | A | U11 | A:e39 @ 8.30 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g78 | 1.55 | CLOSING_START | A | U11 | A:e40 @ 8.30, A:e47 @ 10.15 | active_at_first_observation=True; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g79 | 1.80 | TRACK_APPEARED_LEFT | A | U12 | A:e41 @ 8.55, A:e42 @ 8.85 | initial_in_ego_path=False; source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g80 | 1.80 | TRACK_APPEARED_LEFT | B | U12 | B:e40 @ 8.55, B:e44 @ 9.70 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g81 | 1.85 | EGO_PATH_EXIT | B | U1 | B:e41 @ 8.60 | geometry=estimated_body; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g82 | 2.10 | TRACK_LOST | A | U12 | A:e42 @ 8.85 | source_track=track_011; aggregation=entity_state_union; source_tracks=['A:track_011'] |
| g83 | 2.25 | EGO_PATH_EXIT | B | U8 | B:e42 @ 9.00 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g84 | 2.30 | TRACK_APPEARED_LEFT | A | U12 | A:e43 @ 9.05, A:e45 @ 9.95 | initial_in_ego_path=False; source_track=track_012; aggregation=entity_state_union; source_tracks=['A:track_012'] |
| g85 | 2.35 | EGO_PATH_ENTRY | B | U4 | B:e43 @ 9.10, B:e48 @ 11.50 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g86 | 2.95 | TRACK_LOST | B | U12 | B:e44 @ 9.70 | source_track=track_008; aggregation=entity_state_union; source_tracks=['B:track_008'] |
| g87 | 3.20 | EGO_PATH_EXIT | A | U3 | A:e44 @ 9.95 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g88 | 3.20 | TRACK_LOST | A | U12 | A:e45 @ 9.95 | source_track=track_012; aggregation=entity_state_union; source_tracks=['A:track_012'] |
| g89 | 3.35 | EGO_PATH_EXIT | A | U10 | A:e46 @ 10.10 | geometry=estimated_body; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g90 | 3.40 | CLOSING_END | A | U11 | A:e47 @ 10.15 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g91 | 3.45 | TRACK_APPEARED_RIGHT | B | U11 | B:e45 @ 10.20 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['B:track_009'] |
| g92 | 3.60 | EGO_PATH_EXIT | B | U3 | B:e46 @ 10.35 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g93 | 4.00 | TRACK_LOST | A | U10 | A:e48 @ 10.75 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g94 | 4.35 | TRACK_LOST | B | U1 | B:e47 @ 11.10 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g95 | 4.45 | TRACK_LOST | A | U1 | A:e49 @ 11.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g96 | 4.55 | EGO_PATH_EXIT | A | U4 | A:e50 @ 11.30 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g97 | 4.75 | EGO_PATH_EXIT | B | U4 | B:e48 @ 11.50 | geometry=estimated_body; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g98 | 4.80 | TRACK_LOST | B | U8 | B:e49 @ 11.55 | source_track=track_007; aggregation=entity_state_union; source_tracks=['B:track_007'] |
| g99 | 5.10 | TRACK_LOST | A | U9 | A:e51 @ 11.85 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |

## Edges

```
    g01 --PRECEDES--> g16
    g02 --PRECEDES--> g16
    g03 --PRECEDES--> g16
    g04 --PRECEDES--> g16
    g05 --PRECEDES--> g16
    g06 --PRECEDES--> g16
    g07 --PRECEDES--> g16
    g08 --PRECEDES--> g16
    g09 --PRECEDES--> g16
    g10 --PRECEDES--> g16
    g11 --PRECEDES--> g16
    g12 --PRECEDES--> g16
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
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
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
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
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g47 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g48 --PRECEDES--> g53
    g48 --PRECEDES--> g54
    g48 --PRECEDES--> g55
    g48 --PRECEDES--> g56
    g49 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g49 --PRECEDES--> g54
    g49 --PRECEDES--> g55
    g49 --PRECEDES--> g56
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g50 --PRECEDES--> g56
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g53 --PRECEDES--> g57
    g54 --PRECEDES--> g57
    g55 --PRECEDES--> g57
    g56 --PRECEDES--> g57
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g60 --PRECEDES--> g61
    g61 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g62 --PRECEDES--> g65
    g62 --PRECEDES--> g66
    g63 --PRECEDES--> g64
    g63 --PRECEDES--> g65
    g63 --PRECEDES--> g66
    g64 --PRECEDES--> g67
    g65 --PRECEDES--> g67
    g66 --PRECEDES--> g67
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g69 --PRECEDES--> g71
    g69 --PRECEDES--> g72
    g70 --PRECEDES--> g71
    g70 --PRECEDES--> g72
    g71 --PRECEDES--> g73
    g71 --PRECEDES--> g74
    g72 --PRECEDES--> g73
    g72 --PRECEDES--> g74
    g73 --PRECEDES--> g75
    g74 --PRECEDES--> g75
    g75 --PRECEDES--> g76
    g76 --PRECEDES--> g77
    g76 --PRECEDES--> g78
    g77 --PRECEDES--> g79
    g77 --PRECEDES--> g80
    g78 --PRECEDES--> g79
    g78 --PRECEDES--> g80
    g79 --PRECEDES--> g81
    g80 --PRECEDES--> g81
    g81 --PRECEDES--> g82
    g82 --PRECEDES--> g83
    g83 --PRECEDES--> g84
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
    g97 --PRECEDES--> g98
    g98 --PRECEDES--> g99
    g08 --SAME_TRACK--> g13
    g17 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g19
    g09 --SAME_TRACK--> g20
    g07 --SAME_TRACK--> g26
    g08 --SAME_TRACK--> g27
    g17 --SAME_TRACK--> g28
    g17 --SAME_TRACK--> g31
    g06 --SAME_TRACK--> g34
    g35 --SAME_TRACK--> g36
    g06 --SAME_TRACK--> g38
    g17 --SAME_TRACK--> g44
    g17 --SAME_TRACK--> g46
    g17 --SAME_TRACK--> g49
    g05 --SAME_TRACK--> g51
    g17 --SAME_TRACK--> g52
    g05 --SAME_TRACK--> g57
    g35 --SAME_TRACK--> g62
    g43 --SAME_TRACK--> g66
    g05 --SAME_TRACK--> g68
    g06 --SAME_TRACK--> g70
    g35 --SAME_TRACK--> g76
    g77 --SAME_TRACK--> g78
    g79 --SAME_TRACK--> g82
    g05 --SAME_TRACK--> g87
    g84 --SAME_TRACK--> g88
    g75 --SAME_TRACK--> g89
    g77 --SAME_TRACK--> g90
    g75 --SAME_TRACK--> g93
    g06 --SAME_TRACK--> g95
    g35 --SAME_TRACK--> g96
    g43 --SAME_TRACK--> g99
    g10 --SAME_TRACK--> g14
    g11 --SAME_TRACK--> g15
    g16 --SAME_TRACK--> g21
    g22 --SAME_TRACK--> g23
    g22 --SAME_TRACK--> g24
    g10 --SAME_TRACK--> g25
    g10 --SAME_TRACK--> g29
    g10 --SAME_TRACK--> g30
    g12 --SAME_TRACK--> g32
    g10 --SAME_TRACK--> g33
    g37 --SAME_TRACK--> g39
    g10 --SAME_TRACK--> g40
    g41 --SAME_TRACK--> g42
    g10 --SAME_TRACK--> g45
    g10 --SAME_TRACK--> g47
    g10 --SAME_TRACK--> g50
    g41 --SAME_TRACK--> g58
    g10 --SAME_TRACK--> g59
    g41 --SAME_TRACK--> g60
    g11 --SAME_TRACK--> g61
    g11 --SAME_TRACK--> g63
    g10 --SAME_TRACK--> g64
    g37 --SAME_TRACK--> g65
    g10 --SAME_TRACK--> g67
    g16 --SAME_TRACK--> g69
    g16 --SAME_TRACK--> g81
    g41 --SAME_TRACK--> g83
    g37 --SAME_TRACK--> g85
    g80 --SAME_TRACK--> g86
    g11 --SAME_TRACK--> g92
    g16 --SAME_TRACK--> g94
    g37 --SAME_TRACK--> g97
    g41 --SAME_TRACK--> g98
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.75 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(A,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U3); TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(A,U4); CLOSING_START(B,A); CLOSING_START(B,U3) |
| -6.65 | TRACK_APPEARED_FRONT(B,U1) |
| -6.35 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -6.25 | CRITICAL_TTC_START(A,U3); TRACK_LOST(A,U5) |
| -6.15 | CRITICAL_TTC_START(B,U1) |
| -5.95 | TRACK_APPEARED_FRONT(B,U7); CLOSING_START(B,U7) |
| -3.65 | TRACK_LOST(B,U7) |
| -3.35 | CUT_IN_FROM_RIGHT_START(B,A) |
| -3.15 | TRACK_LOST(A,U2); TRACK_LOST(A,U4) |
| -2.85 | CLOSING_END(A,B) |
| -2.55 | CLOSING_END(B,A) |
| -2.30 | CUT_IN_FROM_RIGHT_END(B,A) |
| -1.65 | CRITICAL_TTC_START(A,B) |
| -1.55 | TRACK_LOST(B,U6) |
| -1.35 | CRITICAL_TTC_START(B,A) |
| -1.20 | CRITICAL_TTC_START(A,U1) |
| -1.15 | TRACK_APPEARED_RIGHT(A,U4); CLOSING_START(A,U4) |
| -1.10 | TRACK_APPEARED_RIGHT(B,U4); EGO_PATH_ENTRY(A,U1); CLOSING_START(B,U4) |
| -0.90 | CLOSING_START(B,A) |
| -0.85 | TRACK_APPEARED_RIGHT(B,U8); CLOSING_START(B,U8) |
| -0.75 | TRACK_APPEARED_FRONT(A,U9) |
| -0.60 | CLOSING_START(A,B) |
| -0.50 | EGO_PATH_ENTRY(B,A) |
| -0.40 | EGO_PATH_ENTRY(A,B) |
| -0.20 | CLOSING_END(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); EGO_PATH_EXIT(A,U3) |
| +0.05 | CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | EGO_PATH_ENTRY(A,U3) |
| +0.15 | EGO_PATH_ENTRY(B,U8) |
| +0.20 | CLOSING_START(B,A) |
| +0.30 | CLOSING_END(B,U8) |
| +0.35 | CLOSING_END(B,U3) |
| +0.45 | CLOSING_END(A,U4); EGO_PATH_ENTRY(B,U3) |
| +0.60 | CLOSING_END(B,A); CLOSING_END(B,U4); EGO_PATH_EXIT(A,U9) |
| +0.65 | EGO_PATH_EXIT(B,A) |
| +0.70 | CRITICAL_TTC_END(A,U3) |
| +0.80 | CRITICAL_TTC_END(B,U1); EGO_PATH_EXIT(A,U1) |
| +1.15 | MOVING_END(B); STOP_START(B) |
| +1.20 | MOVING_END(A); STOP_START(A) |
| +1.30 | TRACK_APPEARED_FRONT(A,U10) |
| +1.50 | EGO_PATH_ENTRY(A,U4) |
| +1.55 | TRACK_APPEARED_RIGHT(A,U11); CLOSING_START(A,U11) |
| +1.80 | TRACK_APPEARED_LEFT(A,U12); TRACK_APPEARED_LEFT(B,U12) |
| +1.85 | EGO_PATH_EXIT(B,U1) |
| +2.10 | TRACK_LOST(A,U12) |
| +2.25 | EGO_PATH_EXIT(B,U8) |
| +2.30 | TRACK_APPEARED_LEFT(A,U12) |
| +2.35 | EGO_PATH_ENTRY(B,U4) |
| +2.95 | TRACK_LOST(B,U12) |
| +3.20 | EGO_PATH_EXIT(A,U3); TRACK_LOST(A,U12) |
| +3.35 | EGO_PATH_EXIT(A,U10) |
| +3.40 | CLOSING_END(A,U11) |
| +3.45 | TRACK_APPEARED_RIGHT(B,U11) |
| +3.60 | EGO_PATH_EXIT(B,U3) |
| +4.00 | TRACK_LOST(A,U10) |
| +4.35 | TRACK_LOST(B,U1) |
| +4.45 | TRACK_LOST(A,U1) |
| +4.55 | EGO_PATH_EXIT(A,U4) |
| +4.75 | EGO_PATH_EXIT(B,U4) |
| +4.80 | TRACK_LOST(B,U8) |
| +5.10 | TRACK_LOST(A,U9) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 5.55, COLLISION 6.75 (+1.20 s); EGO_PATH_ENTRY 5.65 after critical TTC (+0.10 s) [local times; t_global: critical_ttc_start -1.20, ego_path_entry -1.10, collision +0.00]
- A's track_003 (unidentified U3): CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s); EGO_PATH_ENTRY 6.85 after critical TTC (+6.35 s) [local times; t_global: critical_ttc_start -6.25, ego_path_entry +0.10, collision +0.00]
- A's track_006 (B): CRITICAL_TTC_START 5.10, COLLISION with B 6.75 (+1.65 s); EGO_PATH_ENTRY 6.35 after critical TTC (+1.25 s) [local times; t_global: critical_ttc_start -1.65, ego_path_entry -0.40, collision +0.00]
- A's track_007 (unidentified U4): EGO_PATH_ENTRY 8.25, no critical TTC [local times; t_global: ego_path_entry +1.50]
- B's track_001 (A): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 3.40 < CRITICAL_TTC_START 5.40 (+2.00 s) < COLLISION with A 6.75 (+1.35 s); EGO_PATH_ENTRY 6.25 after critical TTC (+0.85 s) [local times; t_global: cut_in -3.35, critical_ttc_start -1.35, ego_path_entry -0.50, collision +0.00]
- B's track_002 (unidentified U3): EGO_PATH_ENTRY 7.20, no critical TTC [local times; t_global: ego_path_entry +0.45]
- B's track_004 (unidentified U1): CRITICAL_TTC_START 0.60, COLLISION 6.75 (+6.15 s) [local times; t_global: critical_ttc_start -6.15, collision +0.00]
- B's track_006 (unidentified U4): EGO_PATH_ENTRY 9.10, no critical TTC [local times; t_global: ego_path_entry +2.35]
- B's track_007 (unidentified U8): EGO_PATH_ENTRY 6.90, no critical TTC [local times; t_global: ego_path_entry +0.15]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.75 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U3) (A:e03)<br>g06 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g07 TRACK_APPEARED_LEFT(A,U2) (A:e05)<br>g08 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g09 TRACK_APPEARED_RIGHT(A,U5) (A:e07)<br>g13 CLOSING_START(A,U4) (A:e08) | ego: not yet observed |
| -6.75 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g10 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g11 TRACK_APPEARED_RIGHT(B,U3) (B:e04)<br>g12 TRACK_APPEARED_RIGHT(B,U6) (B:e05)<br>g14 CLOSING_START(B,A) (B:e06)<br>g15 CLOSING_START(B,U3) (B:e07) | ego: not yet observed |
| -6.75 | A | g06 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g95 TRACK_LOST(A,U1) (A:e49) | ego: not yet observed |
| -6.75 | A | g07 TRACK_APPEARED_LEFT(A,U2) (A:e05)<br>g08 TRACK_APPEARED_RIGHT(A,U4) (A:e06)<br>g26 TRACK_LOST(A,U2) (A:e13)<br>g27 TRACK_LOST(A,U4) (A:e14) | ego: not yet observed |
| -6.75 | A | g09 TRACK_APPEARED_RIGHT(A,U5) (A:e07)<br>g19 CRITICAL_TTC_START(A,U3) (A:e11)<br>g20 TRACK_LOST(A,U5) (A:e12) | ego: not yet observed |
| -6.75 | B | g12 TRACK_APPEARED_RIGHT(B,U6) (B:e05)<br>g32 TRACK_LOST(B,U6) (B:e16) | ego: not yet observed |
| -6.75 | B | g14 CLOSING_START(B,A) (B:e06)<br>g29 CLOSING_END(B,A) (B:e14) | ego: not yet observed |
| -6.75 | B | g15 CLOSING_START(B,U3) (B:e07)<br>g61 CLOSING_END(B,U3) (B:e32) | ego: not yet observed |
| -6.65 | B | g16 TRACK_APPEARED_FRONT(B,U1) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -6.65 | B | g16 TRACK_APPEARED_FRONT(B,U1) (B:e08)<br>g94 TRACK_LOST(B,U1) (B:e47) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -6.35 | A | g17 TRACK_APPEARED_LEFT(A,B) (A:e09)<br>g18 CLOSING_START(A,B) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -6.35 | A | g18 CLOSING_START(A,B) (A:e10)<br>g28 CLOSING_END(A,B) (A:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC? |
| -6.25 | A | g19 CRITICAL_TTC_START(A,U3) (A:e11)<br>g68 CRITICAL_TTC_END(A,U3) (A:e33) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC? |
| -6.15 | B | g21 CRITICAL_TTC_START(B,U1) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: IN_EGO_PATH, CRITICAL_TTC? |
| -6.15 | B | g21 CRITICAL_TTC_START(B,U1) (B:e09)<br>g69 CRITICAL_TTC_END(B,U1) (B:e37) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: IN_EGO_PATH, CRITICAL_TTC? |
| -5.95 | B | g22 TRACK_APPEARED_FRONT(B,U7) (B:e10)<br>g23 CLOSING_START(B,U7) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH |
| -5.95 | B | g22 TRACK_APPEARED_FRONT(B,U7) (B:e10)<br>g24 TRACK_LOST(B,U7) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH |
| -3.35 | B | g25 CUT_IN_FROM_RIGHT_START(B,A) (B:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_005 |
| -3.35 | B | g25 CUT_IN_FROM_RIGHT_START(B,A) (B:e13)<br>g30 CUT_IN_FROM_RIGHT_END(B,A) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_005 |
| -1.65 | A | g31 CRITICAL_TTC_START(A,B) (A:e16) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -1.65 | A | g31 CRITICAL_TTC_START(A,B) (A:e16)<br>g48 COLLISION(A,B) (A:e24)<br>g49 CRITICAL_TTC_END(A,B) (A:e25)<br>g51 EGO_PATH_EXIT(A,U3) (A:e26) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -1.35 | B | g33 CRITICAL_TTC_START(B,A) (B:e17) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| -1.35 | B | g33 CRITICAL_TTC_START(B,A) (B:e17)<br>g48 COLLISION(A,B) (B:e25)<br>g50 CRITICAL_TTC_END(B,A) (B:e26) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| -1.20 | A | g34 CRITICAL_TTC_START(A,U1) (A:e17) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -1.15 | A | g35 TRACK_APPEARED_RIGHT(A,U4) (A:e18)<br>g36 CLOSING_START(A,U4) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -1.15 | A | g36 CLOSING_START(A,U4) (A:e19)<br>g62 CLOSING_END(A,U4) (A:e31) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -1.10 | B | g37 TRACK_APPEARED_RIGHT(B,U4) (B:e18)<br>g39 CLOSING_START(B,U4) (B:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| -1.10 | A | g38 EGO_PATH_ENTRY(A,U1) (A:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -1.10 | A | g38 EGO_PATH_ENTRY(A,U1) (A:e20)<br>g70 EGO_PATH_EXIT(A,U1) (A:e34) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -1.10 | B | g39 CLOSING_START(B,U4) (B:e19)<br>g59 CLOSING_START(B,A) (B:e30)<br>g64 CLOSING_END(B,A) (B:e34)<br>g65 CLOSING_END(B,U4) (B:e35) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.90 | B | g40 CLOSING_START(B,A) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.90 | B | g40 CLOSING_START(B,A) (B:e20)<br>g47 CLOSING_END(B,A) (B:e24) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.85 | B | g41 TRACK_APPEARED_RIGHT(B,U8) (B:e21)<br>g42 CLOSING_START(B,U8) (B:e22) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.85 | B | g41 TRACK_APPEARED_RIGHT(B,U8) (B:e21)<br>g98 TRACK_LOST(B,U8) (B:e49) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.85 | B | g42 CLOSING_START(B,U8) (B:e22)<br>g60 CLOSING_END(B,U8) (B:e31) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.75 | A | g43 TRACK_APPEARED_FRONT(A,U9) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -0.75 | A | g43 TRACK_APPEARED_FRONT(A,U9) (A:e21)<br>g99 TRACK_LOST(A,U9) (A:e51) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -0.60 | A | g44 CLOSING_START(A,B) (A:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -0.60 | A | g44 CLOSING_START(A,B) (A:e22)<br>g52 CLOSING_END(A,B) (A:e27)<br>g53 THROTTLE_END(A) (A:e28)<br>g55 BRAKE_START(A) (A:e29) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| -0.50 | B | g45 EGO_PATH_ENTRY(B,A) (B:e23) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.50 | B | g45 EGO_PATH_ENTRY(B,A) (B:e23)<br>g67 EGO_PATH_EXIT(B,A) (B:e36) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| -0.40 | A | g46 EGO_PATH_ENTRY(A,B) (A:e23) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING, CRITICAL_TTC<br>track_007: CLOSING<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +0.05 | B | g54 THROTTLE_END(B) (B:e27)<br>g56 BRAKE_START(B) (B:e28) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 |
| +0.10 | A | g57 EGO_PATH_ENTRY(A,U3) (A:e30) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +0.10 | A | g57 EGO_PATH_ENTRY(A,U3) (A:e30)<br>g84 TRACK_APPEARED_LEFT(A,U12) (A:e43)<br>g87 EGO_PATH_EXIT(A,U3) (A:e44)<br>g88 TRACK_LOST(A,U12) (A:e45) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC<br>track_006: IN_EGO_PATH<br>track_007: CLOSING<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +0.15 | B | g58 EGO_PATH_ENTRY(B,U8) (B:e29) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 |
| +0.15 | B | g58 EGO_PATH_ENTRY(B,U8) (B:e29)<br>g83 EGO_PATH_EXIT(B,U8) (B:e42) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_003, track_005 |
| +0.20 | B | g59 CLOSING_START(B,A) (B:e30) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| +0.45 | B | g63 EGO_PATH_ENTRY(B,U3) (B:e33) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| +0.45 | B | g63 EGO_PATH_ENTRY(B,U3) (B:e33)<br>g92 EGO_PATH_EXIT(B,U3) (B:e46) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state<br>track_004: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| +0.60 | A | g66 EGO_PATH_EXIT(A,U9) (A:e32) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.15 | B | g71 MOVING_END(B) (B:e38)<br>g72 STOP_START(B) (B:e39) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| +1.20 | A | g73 MOVING_END(A) (A:e35)<br>g74 STOP_START(A) (A:e36) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.30 | A | g75 TRACK_APPEARED_FRONT(A,U10) (A:e37) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.30 | A | g75 TRACK_APPEARED_FRONT(A,U10) (A:e37)<br>g93 TRACK_LOST(A,U10) (A:e48) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.50 | A | g76 EGO_PATH_ENTRY(A,U4) (A:e38) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.50 | A | g76 EGO_PATH_ENTRY(A,U4) (A:e38)<br>g96 EGO_PATH_EXIT(A,U4) (A:e50) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.55 | A | g77 TRACK_APPEARED_RIGHT(A,U11) (A:e39)<br>g78 CLOSING_START(A,U11) (A:e40) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.55 | A | g78 CLOSING_START(A,U11) (A:e40)<br>g90 CLOSING_END(A,U11) (A:e47) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.80 | A | g79 TRACK_APPEARED_LEFT(A,U12) (A:e41) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.80 | A | g79 TRACK_APPEARED_LEFT(A,U12) (A:e41)<br>g82 TRACK_LOST(A,U12) (A:e42) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?<br>track_010: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004, track_005 |
| +1.80 | B | g80 TRACK_APPEARED_LEFT(B,U12) (B:e40) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| +1.80 | B | g80 TRACK_APPEARED_LEFT(B,U12) (B:e40)<br>g86 TRACK_LOST(B,U12) (B:e44) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_003, track_005 |
| +1.85 | B | g81 EGO_PATH_EXIT(B,U1) (B:e41) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: IN_EGO_PATH<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_005 |
| +2.30 | A | g84 TRACK_APPEARED_LEFT(A,U12) (A:e43) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_011 |
| +2.35 | B | g85 EGO_PATH_ENTRY(B,U4) (B:e43) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_003, track_005 |
| +2.35 | B | g85 EGO_PATH_ENTRY(B,U4) (B:e43)<br>g97 EGO_PATH_EXIT(B,U4) (B:e48) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_003, track_005 |
| +3.35 | A | g89 EGO_PATH_EXIT(A,U10) (A:e46) | ego: STOP, BRAKE<br>track_001: CRITICAL_TTC<br>track_003: no active state<br>track_006: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track_008: no active state<br>track_009: IN_EGO_PATH<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_011, track_012 |
| +3.45 | B | g91 TRACK_APPEARED_RIGHT(B,U11) (B:e45) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_004: no active state<br>track_006: IN_EGO_PATH<br>track_007: no active state<br>track lost, states UNKNOWN: track_003, track_005, track_008 |

## Plain-language reading

- 6.75 s before the reference collision, A started moving (already the case when first observed).
- 6.75 s before the reference collision, B started moving (already the case when first observed).
- 6.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
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
- 6.65 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared in front of it.
- 6.35 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.35 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.25 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 6.25 s before the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 6.15 s before the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 5.95 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared in front of it.
- 5.95 s before the reference collision, B observed anonymous road user U7 start closing in (already the case when first observed).
- 3.65 s before the reference collision, B's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 3.35 s before the reference collision, B observed A cutting in from the right.
- 3.15 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 3.15 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 2.85 s before the reference collision, A observed B stop closing in.
- 2.55 s before the reference collision, B observed A stop closing in.
- 2.30 s before the reference collision, B observed A's cut-in from the right settle.
- 1.65 s before the reference collision, A's time-to-contact with B became critical.
- 1.55 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.35 s before the reference collision, B's time-to-contact with A became critical.
- 1.20 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 1.15 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 1.15 s before the reference collision, A observed anonymous road user U4 start closing in (already the case when first observed).
- 1.10 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared on its right.
- 1.10 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 1.10 s before the reference collision, B observed anonymous road user U4 start closing in (already the case when first observed).
- 0.90 s before the reference collision, B observed A start closing in.
- 0.85 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared on its right.
- 0.85 s before the reference collision, B observed anonymous road user U8 start closing in (already the case when first observed).
- 0.75 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared in front of it.
- 0.60 s before the reference collision, A observed B start closing in.
- 0.50 s before the reference collision, B observed A enter its forward path corridor.
- 0.40 s before the reference collision, A observed B enter its forward path corridor.
- 0.20 s before the reference collision, B observed A stop closing in.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 192, B: 192 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A observed anonymous road user U3 enter its forward path corridor.
- 0.15 s after the reference collision, B observed anonymous road user U8 enter its forward path corridor.
- 0.20 s after the reference collision, B observed A start closing in.
- 0.30 s after the reference collision, B observed anonymous road user U8 stop closing in.
- 0.35 s after the reference collision, B observed anonymous road user U3 stop closing in.
- 0.45 s after the reference collision, A observed anonymous road user U4 stop closing in.
- 0.45 s after the reference collision, B observed anonymous road user U3 enter its forward path corridor.
- 0.60 s after the reference collision, B observed A stop closing in.
- 0.60 s after the reference collision, B observed anonymous road user U4 stop closing in.
- 0.60 s after the reference collision, A observed anonymous road user U9 leave its forward path corridor.
- 0.65 s after the reference collision, B observed A leave its forward path corridor.
- 0.70 s after the reference collision, A's time-to-contact with anonymous road user U3 stopped being critical.
- 0.80 s after the reference collision, B's time-to-contact with anonymous road user U1 stopped being critical.
- 0.80 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 1.15 s after the reference collision, B stopped moving.
- 1.15 s after the reference collision, B came to a stop.
- 1.20 s after the reference collision, A stopped moving.
- 1.20 s after the reference collision, A came to a stop.
- 1.30 s after the reference collision, A's radar started tracking anonymous road user U10, which appeared in front of it.
- 1.50 s after the reference collision, A observed anonymous road user U4 enter its forward path corridor.
- 1.55 s after the reference collision, A's radar started tracking anonymous road user U11, which appeared on its right.
- 1.55 s after the reference collision, A observed anonymous road user U11 start closing in (already the case when first observed).
- 1.80 s after the reference collision, A's radar started tracking anonymous road user U12, which appeared on its left.
- 1.80 s after the reference collision, B's radar started tracking anonymous road user U12, which appeared on its left.
- 1.85 s after the reference collision, B observed anonymous road user U1 leave its forward path corridor.
- 2.10 s after the reference collision, A's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 2.25 s after the reference collision, B observed anonymous road user U8 leave its forward path corridor.
- 2.30 s after the reference collision, A's radar started tracking anonymous road user U12, which appeared on its left.
- 2.35 s after the reference collision, B observed anonymous road user U4 enter its forward path corridor.
- 2.95 s after the reference collision, B's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 3.20 s after the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 3.20 s after the reference collision, A's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 3.35 s after the reference collision, A observed anonymous road user U10 leave its forward path corridor.
- 3.40 s after the reference collision, A observed anonymous road user U11 stop closing in.
- 3.45 s after the reference collision, B's radar started tracking anonymous road user U11, which appeared on its right.
- 3.60 s after the reference collision, B observed anonymous road user U3 leave its forward path corridor.
- 4.00 s after the reference collision, A's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 4.35 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 4.45 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 4.55 s after the reference collision, A observed anonymous road user U4 leave its forward path corridor.
- 4.75 s after the reference collision, B observed anonymous road user U4 leave its forward path corridor.
- 4.80 s after the reference collision, B's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 5.10 s after the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
