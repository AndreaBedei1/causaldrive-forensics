# Global graph - S18/run_0_collision_ambiguity

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_002 |
| U2 | anonymous_road_user | anonymous; observed by A as A:track_003 |
| U3 | anonymous_road_user | anonymous; observed by A as A:track_004 |
| U5 | anonymous_road_user | anonymous; observed by A, B as A:track_005, B:track_003 |
| U6 | anonymous_road_user | anonymous; observed by A, B as A:track_006, A:track_007, B:track_004 |
| U4 | anonymous_road_user | anonymous; observed by A, B as A:track_008, B:track_001 |
| U7 | anonymous_road_user | anonymous; observed by A, B as A:track_009, B:track_005 |
| U8 | anonymous_road_user | anonymous; observed by A, B as A:track_010, B:track_006 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e20 | 7.65 | -7.65 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 7.65 | -7.65 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1168.63 vs 1168.63 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.4 m -> 2.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.14 m/s for reference)<br>clearance at the contact 2.13 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_002, track_005)<br>anonymous road user U1: A:track_001, B:track_002 |
| A:track_002 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.2 m -> 0.0 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.47 m/s for reference)<br>clearance at the contact 0.00 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_002, track_005)<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 175 samples; 98% within 3 sigma) at B's own velocity |
| A:track_003 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.65 s before the matched collision<br>lost 1.30 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.0 m -> 7.0 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.17 m/s for reference)<br>anonymous road user U2: A:track_003 |
| A:track_004 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.65 s before the matched collision<br>lost 2.00 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.4 m -> 7.3 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.09 m/s for reference)<br>anonymous road user U3: A:track_004 |
| A:track_005 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.2 m -> 0.6 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.34 m/s for reference)<br>clearance at the contact 0.57 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_002, track_005)<br>anonymous road user U5: B:track_003, A:track_005 |
| A:track_006 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.55 s before the matched collision<br>lost 3.00 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.3 m -> 26.1 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U6: A:track_006, B:track_004, A:track_007 |
| A:track_007 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.2 m -> 19.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 19.83 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U6: A:track_006, B:track_004, A:track_007 |
| A:track_008 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.6 m -> 18.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 18.47 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U4: B:track_001, A:track_008 |
| A:track_009 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U7: A:track_009, B:track_005 |
| A:track_010 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U8: A:track_010, B:track_006 |
| B:track_001 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 13.8 m -> 13.8 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.96 m/s for reference)<br>clearance at the contact 13.76 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U4: B:track_001, A:track_008 |
| B:track_002 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 1.3 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.98 m/s for reference)<br>clearance at the contact 1.35 m<br>anonymous road user U1: A:track_001, B:track_002 |
| B:track_003 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 1.5 m -> 1.5 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.97 m/s for reference)<br>clearance at the contact 1.45 m<br>anonymous road user U5: B:track_003, A:track_005 |
| B:track_004 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 7.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.2 m -> 15.4 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.99 m/s for reference)<br>clearance at the contact 15.24 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U6: A:track_006, B:track_004, A:track_007 |
| B:track_005 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: A:track_009, B:track_005 |
| B:track_006 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1168.63 vs 1168.63 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U8: A:track_010, B:track_006 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.65 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.65 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.65 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.65 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -7.65 | TRACK_APPEARED_FRONT | A | B | A:e03 @ 0.00, A:e32 @ 8.70 | initial_in_ego_path=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -7.65 | TRACK_APPEARED_FRONT | B | U4 | B:e03 @ 0.00 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g07 | -7.65 | TRACK_APPEARED_LEFT | A | U1 | A:e04 @ 0.00, A:e37 @ 8.95 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g08 | -7.65 | TRACK_APPEARED_LEFT | A | U2 | A:e05 @ 0.00, A:e16 @ 6.35 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g09 | -7.65 | TRACK_APPEARED_LEFT | B | U1 | B:e04 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g10 | -7.65 | TRACK_APPEARED_RIGHT | A | U3 | A:e06 @ 0.00, A:e15 @ 5.65 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g11 | -7.65 | TRACK_APPEARED_RIGHT | B | U5 | B:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g12 | -7.65 | CLOSING_START | A | B | A:e08 @ 0.00, A:e25 @ 7.75 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g13 | -7.65 | CLOSING_START | A | U1 | A:e07 @ 0.00, A:e22 @ 7.65 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g14 | -7.60 | TRACK_APPEARED_RIGHT | A | U5 | A:e09 @ 0.05, A:e38 @ 9.10 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g15 | -7.60 | CLOSING_START | A | U5 | A:e10 @ 0.05, A:e17 @ 7.45 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g16 | -7.55 | TRACK_APPEARED_FRONT | A | U6 | A:e11 @ 0.10, A:e14 @ 4.65 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g17 | -7.55 | TRACK_APPEARED_LEFT | B | U6 | B:e06 @ 0.10 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g18 | -7.55 | CLOSING_START | A | U6 | A:e12 @ 0.10 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g19 | -7.15 | CRITICAL_TTC_START | A | B | A:e13 @ 0.50, A:e21 @ 7.65 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g20 | -7.15 | CRITICAL_TTC_START | B | U4 | B:e07 @ 0.50, B:e11 @ 8.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g21 | -3.00 | TRACK_LOST | A | U6 | A:e14 @ 4.65 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g22 | -2.00 | TRACK_LOST | A | U3 | A:e15 @ 5.65 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g23 | -1.30 | TRACK_LOST | A | U2 | A:e16 @ 6.35 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g24 | -0.20 | CLOSING_END | A | U5 | A:e17 @ 7.45 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g25 | -0.05 | TRACK_APPEARED_FRONT | A | U4 | A:e18 @ 7.60, A:e27 @ 8.35 | initial_in_ego_path=True; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g26 | -0.05 | TRACK_APPEARED_LEFT | A | U6 | A:e19 @ 7.60, A:e26 @ 8.35 | initial_in_ego_path=False; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g27 | 0.00 | COLLISION | - | A, B | A:e20 @ 7.65, B:e08 @ 7.65 | matched_event=collision_001; reference_event=True; peak_impulse=A 1168.63, B 1168.63 |
| g28 | 0.00 | CRITICAL_TTC_END | A | B | A:e21 @ 7.65 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g29 | 0.00 | CLOSING_END | A | U1 | A:e22 @ 7.65 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g30 | 0.05 | THROTTLE_END | A | - | A:e23 @ 7.70 |  |
| g31 | 0.05 | THROTTLE_END | B | - | B:e09 @ 7.70 |  |
| g32 | 0.05 | BRAKE_START | A | - | A:e24 @ 7.70 |  |
| g33 | 0.05 | BRAKE_START | B | - | B:e10 @ 7.70 |  |
| g34 | 0.10 | CLOSING_END | A | B | A:e25 @ 7.75 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g35 | 0.50 | CRITICAL_TTC_END | B | U4 | B:e11 @ 8.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g36 | 0.70 | TRACK_LOST | A | U4 | A:e27 @ 8.35 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g37 | 0.70 | TRACK_LOST | A | U6 | A:e26 @ 8.35 | source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g38 | 0.75 | EGO_PATH_ENTRY | A | U5 | A:e28 @ 8.40, A:e29 @ 8.60 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g39 | 0.95 | EGO_PATH_EXIT | A | U5 | A:e29 @ 8.60 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g40 | 1.05 | TRACK_APPEARED_LEFT | A | U7 | A:e30 @ 8.70, A:e41 @ 10.60 | initial_in_ego_path=False; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g41 | 1.05 | CLOSING_START | A | U7 | A:e31 @ 8.70, A:e39 @ 9.65 | active_at_first_observation=True; source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g42 | 1.05 | TRACK_LOST | A | B | A:e32 @ 8.70 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g43 | 1.10 | MOVING_END | A | - | A:e33 @ 8.75 |  |
| g44 | 1.10 | STOP_START | A | - | A:e34 @ 8.75 |  |
| g45 | 1.20 | TRACK_APPEARED_RIGHT | A | U8 | A:e35 @ 8.85, A:e42 @ 10.75 | initial_in_ego_path=False; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g46 | 1.20 | CLOSING_START | A | U8 | A:e36 @ 8.85, A:e40 @ 9.75 | active_at_first_observation=True; source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g47 | 1.25 | MOVING_END | B | - | B:e12 @ 8.90 |  |
| g48 | 1.25 | STOP_START | B | - | B:e13 @ 8.90 |  |
| g49 | 1.30 | TRACK_LOST | A | U1 | A:e37 @ 8.95 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g50 | 1.45 | TRACK_LOST | A | U5 | A:e38 @ 9.10 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g51 | 1.55 | TRACK_APPEARED_LEFT | B | U7 | B:e14 @ 9.20 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g52 | 1.55 | CLOSING_START | B | U7 | B:e15 @ 9.20, B:e18 @ 10.10 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g53 | 1.70 | TRACK_APPEARED_RIGHT | B | U8 | B:e16 @ 9.35 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g54 | 1.70 | CLOSING_START | B | U8 | B:e17 @ 9.35, B:e19 @ 10.30 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g55 | 2.00 | CLOSING_END | A | U7 | A:e39 @ 9.65 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g56 | 2.10 | CLOSING_END | A | U8 | A:e40 @ 9.75 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |
| g57 | 2.45 | CLOSING_END | B | U7 | B:e18 @ 10.10 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g58 | 2.65 | CLOSING_END | B | U8 | B:e19 @ 10.30 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g59 | 2.95 | TRACK_LOST | A | U7 | A:e41 @ 10.60 | source_track=track_009; aggregation=entity_state_union; source_tracks=['A:track_009'] |
| g60 | 3.10 | TRACK_LOST | A | U8 | A:e42 @ 10.75 | source_track=track_010; aggregation=entity_state_union; source_tracks=['A:track_010'] |

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
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g31 --PRECEDES--> g34
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g46 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g52 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g53 --PRECEDES--> g55
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g57 --PRECEDES--> g58
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g07 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g12
    g14 --SAME_TRACK--> g15
    g16 --SAME_TRACK--> g18
    g05 --SAME_TRACK--> g19
    g16 --SAME_TRACK--> g21
    g10 --SAME_TRACK--> g22
    g08 --SAME_TRACK--> g23
    g14 --SAME_TRACK--> g24
    g05 --SAME_TRACK--> g28
    g07 --SAME_TRACK--> g29
    g05 --SAME_TRACK--> g34
    g26 --SAME_TRACK--> g37
    g25 --SAME_TRACK--> g36
    g14 --SAME_TRACK--> g38
    g14 --SAME_TRACK--> g39
    g40 --SAME_TRACK--> g41
    g05 --SAME_TRACK--> g42
    g45 --SAME_TRACK--> g46
    g07 --SAME_TRACK--> g49
    g14 --SAME_TRACK--> g50
    g40 --SAME_TRACK--> g55
    g45 --SAME_TRACK--> g56
    g40 --SAME_TRACK--> g59
    g45 --SAME_TRACK--> g60
    g06 --SAME_TRACK--> g20
    g06 --SAME_TRACK--> g35
    g51 --SAME_TRACK--> g52
    g53 --SAME_TRACK--> g54
    g51 --SAME_TRACK--> g57
    g53 --SAME_TRACK--> g58
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.65 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,U4); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U1); TRACK_APPEARED_RIGHT(A,U3); TRACK_APPEARED_RIGHT(B,U5); CLOSING_START(A,B); CLOSING_START(A,U1) |
| -7.60 | TRACK_APPEARED_RIGHT(A,U5); CLOSING_START(A,U5) |
| -7.55 | TRACK_APPEARED_FRONT(A,U6); TRACK_APPEARED_LEFT(B,U6); CLOSING_START(A,U6) |
| -7.15 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,U4) |
| -3.00 | TRACK_LOST(A,U6) |
| -2.00 | TRACK_LOST(A,U3) |
| -1.30 | TRACK_LOST(A,U2) |
| -0.20 | CLOSING_END(A,U5) |
| -0.05 | TRACK_APPEARED_FRONT(A,U4); TRACK_APPEARED_LEFT(A,U6) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,U1) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | CLOSING_END(A,B) |
| +0.50 | CRITICAL_TTC_END(B,U4) |
| +0.70 | TRACK_LOST(A,U4); TRACK_LOST(A,U6) |
| +0.75 | EGO_PATH_ENTRY(A,U5) |
| +0.95 | EGO_PATH_EXIT(A,U5) |
| +1.05 | TRACK_APPEARED_LEFT(A,U7); CLOSING_START(A,U7); TRACK_LOST(A,B) |
| +1.10 | MOVING_END(A); STOP_START(A) |
| +1.20 | TRACK_APPEARED_RIGHT(A,U8); CLOSING_START(A,U8) |
| +1.25 | MOVING_END(B); STOP_START(B) |
| +1.30 | TRACK_LOST(A,U1) |
| +1.45 | TRACK_LOST(A,U5) |
| +1.55 | TRACK_APPEARED_LEFT(B,U7); CLOSING_START(B,U7) |
| +1.70 | TRACK_APPEARED_RIGHT(B,U8); CLOSING_START(B,U8) |
| +2.00 | CLOSING_END(A,U7) |
| +2.10 | CLOSING_END(A,U8) |
| +2.45 | CLOSING_END(B,U7) |
| +2.65 | CLOSING_END(B,U8) |
| +2.95 | TRACK_LOST(A,U7) |
| +3.10 | TRACK_LOST(A,U8) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (B): CRITICAL_TTC_START 0.50, COLLISION with B 7.65 (+7.15 s) [local times; t_global: critical_ttc_start -7.15, collision +0.00]
- A's track_005 (unidentified U5): EGO_PATH_ENTRY 8.40, no critical TTC [local times; t_global: ego_path_entry +0.75]
- B's track_001 (unidentified U4): CRITICAL_TTC_START 0.50, COLLISION 7.65 (+7.15 s) [local times; t_global: critical_ttc_start -7.15, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.65 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,B) (A:e03)<br>g07 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g08 TRACK_APPEARED_LEFT(A,U2) (A:e05)<br>g10 TRACK_APPEARED_RIGHT(A,U3) (A:e06)<br>g12 CLOSING_START(A,B) (A:e08)<br>g13 CLOSING_START(A,U1) (A:e07) | ego: not yet observed |
| -7.65 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g06 TRACK_APPEARED_FRONT(B,U4) (B:e03)<br>g09 TRACK_APPEARED_LEFT(B,U1) (B:e04)<br>g11 TRACK_APPEARED_RIGHT(B,U5) (B:e05) | ego: not yet observed |
| -7.65 | A | g05 TRACK_APPEARED_FRONT(A,B) (A:e03)<br>g40 TRACK_APPEARED_LEFT(A,U7) (A:e30)<br>g41 CLOSING_START(A,U7) (A:e31)<br>g42 TRACK_LOST(A,B) (A:e32) | ego: not yet observed |
| -7.65 | A | g07 TRACK_APPEARED_LEFT(A,U1) (A:e04)<br>g49 TRACK_LOST(A,U1) (A:e37) | ego: not yet observed |
| -7.65 | A | g08 TRACK_APPEARED_LEFT(A,U2) (A:e05)<br>g23 TRACK_LOST(A,U2) (A:e16) | ego: not yet observed |
| -7.65 | A | g10 TRACK_APPEARED_RIGHT(A,U3) (A:e06)<br>g22 TRACK_LOST(A,U3) (A:e15) | ego: not yet observed |
| -7.65 | A | g12 CLOSING_START(A,B) (A:e08)<br>g34 CLOSING_END(A,B) (A:e25) | ego: not yet observed |
| -7.65 | A | g13 CLOSING_START(A,U1) (A:e07)<br>g19 CRITICAL_TTC_START(A,B) (A:e13)<br>g27 COLLISION(A,B) (A:e20)<br>g28 CRITICAL_TTC_END(A,B) (A:e21)<br>g29 CLOSING_END(A,U1) (A:e22) | ego: not yet observed |
| -7.60 | A | g14 TRACK_APPEARED_RIGHT(A,U5) (A:e09)<br>g15 CLOSING_START(A,U5) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.60 | A | g14 TRACK_APPEARED_RIGHT(A,U5) (A:e09)<br>g50 TRACK_LOST(A,U5) (A:e38) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.60 | A | g15 CLOSING_START(A,U5) (A:e10)<br>g24 CLOSING_END(A,U5) (A:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.55 | A | g16 TRACK_APPEARED_FRONT(A,U6) (A:e11)<br>g18 CLOSING_START(A,U6) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CLOSING, CRITICAL_TTC? |
| -7.55 | A | g16 TRACK_APPEARED_FRONT(A,U6) (A:e11)<br>g21 TRACK_LOST(A,U6) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CLOSING, CRITICAL_TTC? |
| -7.55 | B | g17 TRACK_APPEARED_LEFT(B,U6) (B:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.15 | A | g19 CRITICAL_TTC_START(A,B) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CLOSING, CRITICAL_TTC?<br>track_006: CLOSING, CRITICAL_TTC? |
| -7.15 | B | g20 CRITICAL_TTC_START(B,U4) (B:e07) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -7.15 | B | g20 CRITICAL_TTC_START(B,U4) (B:e07)<br>g35 CRITICAL_TTC_END(B,U4) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -0.05 | A | g25 TRACK_APPEARED_FRONT(A,U4) (A:e18)<br>g26 TRACK_APPEARED_LEFT(A,U6) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_006 |
| -0.05 | A | g25 TRACK_APPEARED_FRONT(A,U4) (A:e18)<br>g26 TRACK_APPEARED_LEFT(A,U6) (A:e19)<br>g36 TRACK_LOST(A,U4) (A:e27)<br>g37 TRACK_LOST(A,U6) (A:e26) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_006 |
| +0.00 | B | g27 COLLISION(A,B) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +0.05 | A | g30 THROTTLE_END(A) (A:e23)<br>g32 BRAKE_START(A) (A:e24) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, IN_EGO_PATH<br>track_005: no active state<br>track_007: CRITICAL_TTC?<br>track_008: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003, track_004, track_006 |
| +0.05 | B | g31 THROTTLE_END(B) (B:e09)<br>g33 BRAKE_START(B) (B:e10) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +0.75 | A | g38 EGO_PATH_ENTRY(A,U5) (A:e28) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_006, track_007, track_008 |
| +0.75 | A | g38 EGO_PATH_ENTRY(A,U5) (A:e28)<br>g39 EGO_PATH_EXIT(A,U5) (A:e29) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_006, track_007, track_008 |
| +1.05 | A | g40 TRACK_APPEARED_LEFT(A,U7) (A:e30)<br>g59 TRACK_LOST(A,U7) (A:e41) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_006, track_007, track_008 |
| +1.05 | A | g41 CLOSING_START(A,U7) (A:e31)<br>g55 CLOSING_END(A,U7) (A:e39) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_005: no active state<br>track lost, states UNKNOWN: track_003, track_004, track_006, track_007, track_008 |
| +1.10 | A | g43 MOVING_END(A) (A:e33)<br>g44 STOP_START(A) (A:e34) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006, track_007, track_008 |
| +1.20 | A | g45 TRACK_APPEARED_RIGHT(A,U8) (A:e35)<br>g46 CLOSING_START(A,U8) (A:e36) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006, track_007, track_008 |
| +1.20 | A | g45 TRACK_APPEARED_RIGHT(A,U8) (A:e35)<br>g60 TRACK_LOST(A,U8) (A:e42) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006, track_007, track_008 |
| +1.20 | A | g46 CLOSING_START(A,U8) (A:e36)<br>g56 CLOSING_END(A,U8) (A:e40) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_009: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006, track_007, track_008 |
| +1.25 | B | g47 MOVING_END(B) (B:e12)<br>g48 STOP_START(B) (B:e13) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +1.55 | B | g51 TRACK_APPEARED_LEFT(B,U7) (B:e14)<br>g52 CLOSING_START(B,U7) (B:e15) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +1.55 | B | g52 CLOSING_START(B,U7) (B:e15)<br>g57 CLOSING_END(B,U7) (B:e18) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| +1.70 | B | g53 TRACK_APPEARED_RIGHT(B,U8) (B:e16)<br>g54 CLOSING_START(B,U8) (B:e17) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC? |
| +1.70 | B | g54 CLOSING_START(B,U8) (B:e17)<br>g58 CLOSING_END(B,U8) (B:e19) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC? |

## Plain-language reading

- 7.65 s before the reference collision, A started moving (already the case when first observed).
- 7.65 s before the reference collision, B started moving (already the case when first observed).
- 7.65 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.65 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.65 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 7.65 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared in front of it.
- 7.65 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 7.65 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 7.65 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its left.
- 7.65 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 7.65 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its right.
- 7.65 s before the reference collision, A observed B start closing in (already the case when first observed).
- 7.65 s before the reference collision, A observed anonymous road user U1 start closing in (already the case when first observed).
- 7.60 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared on its right.
- 7.60 s before the reference collision, A observed anonymous road user U5 start closing in (already the case when first observed).
- 7.55 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared in front of it.
- 7.55 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its left.
- 7.55 s before the reference collision, A observed anonymous road user U6 start closing in (already the case when first observed).
- 7.15 s before the reference collision, A's time-to-contact with B became critical.
- 7.15 s before the reference collision, B's time-to-contact with anonymous road user U4 became critical.
- 3.00 s before the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 2.00 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 1.30 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 0.20 s before the reference collision, A observed anonymous road user U5 stop closing in.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared in front of it.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared on its left.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1169, B: 1169 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed anonymous road user U1 stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A observed B stop closing in.
- 0.50 s after the reference collision, B's time-to-contact with anonymous road user U4 stopped being critical.
- 0.70 s after the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 0.75 s after the reference collision, A observed anonymous road user U5 enter its forward path corridor.
- 0.95 s after the reference collision, A observed anonymous road user U5 leave its forward path corridor.
- 1.05 s after the reference collision, A's radar started tracking anonymous road user U7, which appeared on its left.
- 1.05 s after the reference collision, A observed anonymous road user U7 start closing in (already the case when first observed).
- 1.05 s after the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 1.10 s after the reference collision, A stopped moving.
- 1.10 s after the reference collision, A came to a stop.
- 1.20 s after the reference collision, A's radar started tracking anonymous road user U8, which appeared on its right.
- 1.20 s after the reference collision, A observed anonymous road user U8 start closing in (already the case when first observed).
- 1.25 s after the reference collision, B stopped moving.
- 1.25 s after the reference collision, B came to a stop.
- 1.30 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 1.45 s after the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 1.55 s after the reference collision, B's radar started tracking anonymous road user U7, which appeared on its left.
- 1.55 s after the reference collision, B observed anonymous road user U7 start closing in (already the case when first observed).
- 1.70 s after the reference collision, B's radar started tracking anonymous road user U8, which appeared on its right.
- 1.70 s after the reference collision, B observed anonymous road user U8 start closing in (already the case when first observed).
- 2.00 s after the reference collision, A observed anonymous road user U7 stop closing in.
- 2.10 s after the reference collision, A observed anonymous road user U8 stop closing in.
- 2.45 s after the reference collision, B observed anonymous road user U7 stop closing in.
- 2.65 s after the reference collision, B observed anonymous road user U8 stop closing in.
- 2.95 s after the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 3.10 s after the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
