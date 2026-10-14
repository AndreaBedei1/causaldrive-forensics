# Global graph - S17/run_0_occlusion_reappearance

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_005 |
| B | recorder | clock ALIGNED; observed by others as: A:track_005 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_003 |
| U2 | anonymous_road_user | anonymous; observed by A, B as A:track_002, A:track_007, B:track_002, B:track_006 |
| U3 | anonymous_road_user | anonymous; observed by A, B as A:track_003, B:track_004 |
| U4 | anonymous_road_user | anonymous; observed by A, B as A:track_004, A:track_006, B:track_001 |
| U5 | anonymous_road_user | anonymous; observed by A as A:track_008 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e21 | 7.30 | -7.30 | reported the reference collision collision_001 |
| B | ALIGNED | B:e21 | 7.30 | -7.30 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 389.26 vs 389.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.2 m -> 10.3 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 4.62 m/s for reference)<br>clearance at the contact 7.17 m (beyond 3.50 m: confidence factor 0.47)<br>anonymous road user U1: A:track_001, B:track_003 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 2.50 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 20.4 m -> 20.5 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 2.02 m/s for reference)<br>retrospective: identity resolved from later evidence at -0.85 s (entity seen by several observers), carried back 1.40 s with the motion model; posterior 0.992 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U2: A:track_002, B:track_002, A:track_007, B:track_006 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 4.00 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 37.5 m -> 37.6 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_004 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.15 s before the matched collision<br>lost 2.75 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 19.2 m -> 17.9 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.30 m/s for reference)<br>anonymous road user U4: B:track_001, A:track_004, A:track_006 |
| A:track_005 | B | ASSOCIATED | 0.88 | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 6.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.9 m -> 0.8 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.76 m/s for reference)<br>clearance at the contact 0.84 m<br>the only track of A compatible with the contact |
| A:track_006 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.0 m -> 11.8 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.27 m/s for reference)<br>clearance at the contact 11.75 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U4: B:track_001, A:track_004, A:track_006 |
| A:track_007 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.85 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 20.6 m -> 20.9 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 1.97 m/s for reference)<br>clearance at the contact 20.60 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: A:track_002, B:track_002, A:track_007, B:track_006 |
| A:track_008 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U5: A:track_008 |
| B:track_001 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 13.5 m -> 13.8 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.90 m/s for reference)<br>clearance at the contact 13.42 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U4: B:track_001, A:track_004, A:track_006 |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 2.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 17.4 m -> 19.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.15 m/s for reference)<br>retrospective: identity resolved from later evidence at -0.85 s (entity seen by several observers), carried back 1.40 s with the motion model; posterior 0.992 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U2: A:track_002, B:track_002, A:track_007, B:track_006 |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.9 m -> 12.8 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 2.44 m/s for reference)<br>clearance at the contact 7.85 m (beyond 3.50 m: confidence factor 0.35)<br>anonymous road user U1: A:track_001, B:track_003 |
| B:track_004 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.00 s before the matched collision<br>lost 3.90 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 30.4 m -> 32.4 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_004 |
| B:track_005 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 4.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.5 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.52 m/s for reference)<br>clearance at the contact 0.00 m<br>the only track of B compatible with the contact |
| B:track_006 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.40 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 23.0 m -> 23.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.27 m/s for reference)<br>clearance at the contact 22.99 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: A:track_002, B:track_002, A:track_007, B:track_006 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.30 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.30 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.30 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.30 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -7.30 | TRACK_APPEARED_FRONT | A | U2 | A:e03 @ 0.00, A:e13 @ 4.80 | initial_in_ego_path=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -7.30 | TRACK_APPEARED_FRONT | A | U3 | A:e04 @ 0.00, A:e10 @ 3.30 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g07 | -7.30 | TRACK_APPEARED_FRONT | B | U4 | B:e03 @ 0.00, B:e28 @ 8.00 | initial_in_ego_path=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g08 | -7.30 | TRACK_APPEARED_LEFT | A | U1 | A:e05 @ 0.00 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g09 | -7.30 | TRACK_APPEARED_RIGHT | B | U1 | B:e05 @ 0.00, B:e27 @ 7.80 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g10 | -7.30 | TRACK_APPEARED_RIGHT | B | U2 | B:e04 @ 0.00, B:e12 @ 5.05 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g11 | -7.15 | TRACK_APPEARED_LEFT | A | U4 | A:e06 @ 0.15, A:e12 @ 4.55 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g12 | -7.15 | CLOSING_START | A | U4 | A:e07 @ 0.15 | active_at_first_observation=True; source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g13 | -7.00 | TRACK_APPEARED_RIGHT | B | U3 | B:e06 @ 0.30, B:e10 @ 3.40 | initial_in_ego_path=False; source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g14 | -6.80 | CRITICAL_TTC_START | B | U4 | B:e07 @ 0.50, B:e15 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g15 | -6.40 | TRACK_APPEARED_LEFT | A | B | A:e08 @ 0.90 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g16 | -6.40 | CLOSING_START | A | B | A:e09 @ 0.90, A:e11 @ 4.15 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g17 | -4.30 | TRACK_APPEARED_RIGHT | B | A | B:e08 @ 3.00 | initial_in_ego_path=False; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g18 | -4.30 | CLOSING_START | B | A | B:e09 @ 3.00, B:e11 @ 3.55 | active_at_first_observation=True; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g19 | -4.00 | TRACK_LOST | A | U3 | A:e10 @ 3.30 | source_track=track_003; aggregation=entity_state_union; source_tracks=['A:track_003'] |
| g20 | -3.90 | TRACK_LOST | B | U3 | B:e10 @ 3.40 | source_track=track_004; aggregation=entity_state_union; source_tracks=['B:track_004'] |
| g21 | -3.75 | CLOSING_END | B | A | B:e11 @ 3.55 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g22 | -3.15 | CLOSING_END | A | B | A:e11 @ 4.15 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g23 | -2.75 | TRACK_LOST | A | U4 | A:e12 @ 4.55 | source_track=track_004; aggregation=entity_state_union; source_tracks=['A:track_004'] |
| g24 | -2.50 | TRACK_LOST | A | U2 | A:e13 @ 4.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g25 | -2.25 | TRACK_LOST | B | U2 | B:e12 @ 5.05 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g26 | -1.85 | CLOSING_START | B | A | B:e13 @ 5.45, B:e20 @ 7.20 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g27 | -1.80 | CLOSING_START | A | B | A:e14 @ 5.50, A:e23 @ 7.30 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g28 | -1.80 | CRITICAL_TTC_START | A | B | A:e15 @ 5.50, A:e22 @ 7.30 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g29 | -1.75 | CRITICAL_TTC_START | B | A | B:e14 @ 5.55, B:e22 @ 7.30 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g30 | -1.20 | EGO_PATH_ENTRY | A | U1 | A:e16 @ 6.10, A:e30 @ 8.00 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g31 | -1.20 | CRITICAL_TTC_START | A | U1 | A:e17 @ 6.10, A:e28 @ 7.65 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g32 | -1.10 | CRITICAL_TTC_END | B | U4 | B:e15 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g33 | -0.95 | TRACK_APPEARED_LEFT | A | U4 | A:e18 @ 6.35 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g34 | -0.95 | CLOSING_START | A | U4 | A:e19 @ 6.35, A:e27 @ 7.50 | active_at_first_observation=True; source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g35 | -0.90 | EGO_PATH_ENTRY | B | U1 | B:e16 @ 6.40 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g36 | -0.90 | CRITICAL_TTC_START | B | U1 | B:e17 @ 6.40 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g37 | -0.85 | TRACK_APPEARED_RIGHT | A | U2 | A:e20 @ 6.45 | initial_in_ego_path=True; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g38 | -0.40 | TRACK_APPEARED_FRONT | B | U2 | B:e18 @ 6.90, B:e26 @ 7.60 | initial_in_ego_path=False; source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g39 | -0.25 | EGO_PATH_ENTRY | B | A | B:e19 @ 7.05 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g40 | -0.10 | CLOSING_END | B | A | B:e20 @ 7.20 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g41 | 0.00 | COLLISION | - | A, B | A:e21 @ 7.30, B:e21 @ 7.30 | matched_event=collision_001; reference_event=True; peak_impulse=A 389.26, B 389.26 |
| g42 | 0.00 | CRITICAL_TTC_END | A | B | A:e22 @ 7.30 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g43 | 0.00 | CRITICAL_TTC_END | B | A | B:e22 @ 7.30 | source_track=track_005; aggregation=entity_state_union; source_tracks=['B:track_005'] |
| g44 | 0.00 | CLOSING_END | A | B | A:e23 @ 7.30 | source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g45 | 0.05 | THROTTLE_END | A | - | A:e24 @ 7.35 |  |
| g46 | 0.05 | THROTTLE_END | B | - | B:e23 @ 7.35 |  |
| g47 | 0.05 | BRAKE_START | A | - | A:e25 @ 7.35 |  |
| g48 | 0.05 | BRAKE_START | B | - | B:e24 @ 7.35 |  |
| g49 | 0.05 | TURN_LEFT_START | B | - | B:e25 @ 7.35 |  |
| g50 | 0.10 | TURN_LEFT_START | A | - | A:e26 @ 7.40 |  |
| g51 | 0.20 | CLOSING_END | A | U4 | A:e27 @ 7.50 | source_track=track_006; aggregation=entity_state_union; source_tracks=['A:track_006'] |
| g52 | 0.30 | TRACK_LOST | B | U2 | B:e26 @ 7.60 | source_track=track_006; aggregation=entity_state_union; source_tracks=['B:track_006'] |
| g53 | 0.35 | CRITICAL_TTC_END | A | U1 | A:e28 @ 7.65 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g54 | 0.50 | EGO_PATH_EXIT | A | U2 | A:e29 @ 7.80 | geometry=estimated_body; source_track=track_007; aggregation=entity_state_union; source_tracks=['A:track_007'] |
| g55 | 0.50 | TRACK_LOST | B | U1 | B:e27 @ 7.80 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g56 | 0.70 | EGO_PATH_EXIT | A | U1 | A:e30 @ 8.00 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g57 | 0.70 | TRACK_LOST | B | U4 | B:e28 @ 8.00 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g58 | 0.95 | TURN_LEFT_END | A | - | A:e31 @ 8.25 |  |
| g59 | 0.95 | TURN_LEFT_END | B | - | B:e29 @ 8.25 |  |
| g60 | 0.95 | MOVING_END | B | - | B:e30 @ 8.25 |  |
| g61 | 0.95 | STOP_START | B | - | B:e31 @ 8.25 |  |
| g62 | 1.00 | MOVING_END | A | - | A:e32 @ 8.30 |  |
| g63 | 1.00 | STOP_START | A | - | A:e33 @ 8.30 |  |
| g64 | 1.15 | TRACK_APPEARED_RIGHT | A | U5 | A:e34 @ 8.45, A:e36 @ 11.90 | initial_in_ego_path=False; source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |
| g65 | 1.40 | EGO_PATH_ENTRY | A | B | A:e35 @ 8.70 | geometry=estimated_body; source_track=track_005; aggregation=entity_state_union; source_tracks=['A:track_005'] |
| g66 | 4.60 | TRACK_LOST | A | U5 | A:e36 @ 11.90 | source_track=track_008; aggregation=entity_state_union; source_tracks=['A:track_008'] |

## Edges

```
    g01 --PRECEDES--> g11
    g01 --PRECEDES--> g12
    g02 --PRECEDES--> g11
    g02 --PRECEDES--> g12
    g03 --PRECEDES--> g11
    g03 --PRECEDES--> g12
    g04 --PRECEDES--> g11
    g04 --PRECEDES--> g12
    g05 --PRECEDES--> g11
    g05 --PRECEDES--> g12
    g06 --PRECEDES--> g11
    g06 --PRECEDES--> g12
    g07 --PRECEDES--> g11
    g07 --PRECEDES--> g12
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
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
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g29
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g41 --PRECEDES--> g46
    g41 --PRECEDES--> g47
    g41 --PRECEDES--> g48
    g41 --PRECEDES--> g49
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g42 --PRECEDES--> g48
    g42 --PRECEDES--> g49
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g45 --PRECEDES--> g50
    g46 --PRECEDES--> g50
    g47 --PRECEDES--> g50
    g48 --PRECEDES--> g50
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g51 --PRECEDES--> g52
    g52 --PRECEDES--> g53
    g53 --PRECEDES--> g54
    g53 --PRECEDES--> g55
    g54 --PRECEDES--> g56
    g54 --PRECEDES--> g57
    g55 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g56 --PRECEDES--> g60
    g56 --PRECEDES--> g61
    g57 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g57 --PRECEDES--> g60
    g57 --PRECEDES--> g61
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
    g11 --SAME_TRACK--> g12
    g15 --SAME_TRACK--> g16
    g06 --SAME_TRACK--> g19
    g15 --SAME_TRACK--> g22
    g11 --SAME_TRACK--> g23
    g05 --SAME_TRACK--> g24
    g15 --SAME_TRACK--> g27
    g15 --SAME_TRACK--> g28
    g08 --SAME_TRACK--> g30
    g08 --SAME_TRACK--> g31
    g33 --SAME_TRACK--> g34
    g15 --SAME_TRACK--> g42
    g15 --SAME_TRACK--> g44
    g33 --SAME_TRACK--> g51
    g08 --SAME_TRACK--> g53
    g37 --SAME_TRACK--> g54
    g08 --SAME_TRACK--> g56
    g15 --SAME_TRACK--> g65
    g64 --SAME_TRACK--> g66
    g07 --SAME_TRACK--> g14
    g17 --SAME_TRACK--> g18
    g13 --SAME_TRACK--> g20
    g17 --SAME_TRACK--> g21
    g10 --SAME_TRACK--> g25
    g17 --SAME_TRACK--> g26
    g17 --SAME_TRACK--> g29
    g07 --SAME_TRACK--> g32
    g09 --SAME_TRACK--> g35
    g09 --SAME_TRACK--> g36
    g17 --SAME_TRACK--> g39
    g17 --SAME_TRACK--> g40
    g17 --SAME_TRACK--> g43
    g38 --SAME_TRACK--> g52
    g09 --SAME_TRACK--> g55
    g07 --SAME_TRACK--> g57
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.30 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U4); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_RIGHT(B,U1); TRACK_APPEARED_RIGHT(B,U2) |
| -7.15 | TRACK_APPEARED_LEFT(A,U4); CLOSING_START(A,U4) |
| -7.00 | TRACK_APPEARED_RIGHT(B,U3) |
| -6.80 | CRITICAL_TTC_START(B,U4) |
| -6.40 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -4.30 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -4.00 | TRACK_LOST(A,U3) |
| -3.90 | TRACK_LOST(B,U3) |
| -3.75 | CLOSING_END(B,A) |
| -3.15 | CLOSING_END(A,B) |
| -2.75 | TRACK_LOST(A,U4) |
| -2.50 | TRACK_LOST(A,U2) |
| -2.25 | TRACK_LOST(B,U2) |
| -1.85 | CLOSING_START(B,A) |
| -1.80 | CLOSING_START(A,B); CRITICAL_TTC_START(A,B) |
| -1.75 | CRITICAL_TTC_START(B,A) |
| -1.20 | EGO_PATH_ENTRY(A,U1); CRITICAL_TTC_START(A,U1) |
| -1.10 | CRITICAL_TTC_END(B,U4) |
| -0.95 | TRACK_APPEARED_LEFT(A,U4); CLOSING_START(A,U4) |
| -0.90 | EGO_PATH_ENTRY(B,U1); CRITICAL_TTC_START(B,U1) |
| -0.85 | TRACK_APPEARED_RIGHT(A,U2) |
| -0.40 | TRACK_APPEARED_FRONT(B,U2) |
| -0.25 | EGO_PATH_ENTRY(B,A) |
| -0.10 | CLOSING_END(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B) |
| +0.10 | TURN_LEFT_START(A) |
| +0.20 | CLOSING_END(A,U4) |
| +0.30 | TRACK_LOST(B,U2) |
| +0.35 | CRITICAL_TTC_END(A,U1) |
| +0.50 | EGO_PATH_EXIT(A,U2); TRACK_LOST(B,U1) |
| +0.70 | EGO_PATH_EXIT(A,U1); TRACK_LOST(B,U4) |
| +0.95 | TURN_LEFT_END(A); TURN_LEFT_END(B); MOVING_END(B); STOP_START(B) |
| +1.00 | MOVING_END(A); STOP_START(A) |
| +1.15 | TRACK_APPEARED_RIGHT(A,U5) |
| +1.40 | EGO_PATH_ENTRY(A,B) |
| +4.60 | TRACK_LOST(A,U5) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 6.10, COLLISION 7.30 (+1.20 s); EGO_PATH_ENTRY 6.10 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start -1.20, ego_path_entry -1.20, collision +0.00]
- A's track_005 (B): CRITICAL_TTC_START 5.50, COLLISION with B 7.30 (+1.80 s); EGO_PATH_ENTRY 8.70 after critical TTC (+3.20 s) [local times; t_global: critical_ttc_start -1.80, ego_path_entry +1.40, collision +0.00]
- B's track_001 (unidentified U4): CRITICAL_TTC_START 0.50, COLLISION 7.30 (+6.80 s) [local times; t_global: critical_ttc_start -6.80, collision +0.00]
- B's track_003 (unidentified U1): CRITICAL_TTC_START 6.40, COLLISION 7.30 (+0.90 s); EGO_PATH_ENTRY 6.40 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start -0.90, ego_path_entry -0.90, collision +0.00]
- B's track_005 (A): CRITICAL_TTC_START 5.55, COLLISION with A 7.30 (+1.75 s); EGO_PATH_ENTRY 7.05 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -1.75, ego_path_entry -0.25, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.30 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_FRONT(A,U2) (A:e03)<br>g06 TRACK_APPEARED_FRONT(A,U3) (A:e04)<br>g08 TRACK_APPEARED_LEFT(A,U1) (A:e05) | ego: not yet observed |
| -7.30 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_FRONT(B,U4) (B:e03)<br>g09 TRACK_APPEARED_RIGHT(B,U1) (B:e05)<br>g10 TRACK_APPEARED_RIGHT(B,U2) (B:e04) | ego: not yet observed |
| -7.30 | A | g05 TRACK_APPEARED_FRONT(A,U2) (A:e03)<br>g24 TRACK_LOST(A,U2) (A:e13) | ego: not yet observed |
| -7.30 | A | g06 TRACK_APPEARED_FRONT(A,U3) (A:e04)<br>g19 TRACK_LOST(A,U3) (A:e10) | ego: not yet observed |
| -7.30 | B | g07 TRACK_APPEARED_FRONT(B,U4) (B:e03)<br>g57 TRACK_LOST(B,U4) (B:e28) | ego: not yet observed |
| -7.30 | B | g09 TRACK_APPEARED_RIGHT(B,U1) (B:e05)<br>g55 TRACK_LOST(B,U1) (B:e27) | ego: not yet observed |
| -7.30 | B | g10 TRACK_APPEARED_RIGHT(B,U2) (B:e04)<br>g25 TRACK_LOST(B,U2) (B:e12) | ego: not yet observed |
| -7.15 | A | g11 TRACK_APPEARED_LEFT(A,U4) (A:e06)<br>g12 CLOSING_START(A,U4) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.15 | A | g11 TRACK_APPEARED_LEFT(A,U4) (A:e06)<br>g23 TRACK_LOST(A,U4) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: IN_EGO_PATH, CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.00 | B | g13 TRACK_APPEARED_RIGHT(B,U3) (B:e06) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -7.00 | B | g13 TRACK_APPEARED_RIGHT(B,U3) (B:e06)<br>g20 TRACK_LOST(B,U3) (B:e10) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? |
| -6.80 | B | g14 CRITICAL_TTC_START(B,U4) (B:e07) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -6.80 | B | g14 CRITICAL_TTC_START(B,U4) (B:e07)<br>g32 CRITICAL_TTC_END(B,U4) (B:e15) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? |
| -6.40 | A | g15 TRACK_APPEARED_LEFT(A,B) (A:e08)<br>g16 CLOSING_START(A,B) (A:e09) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: CLOSING |
| -6.40 | A | g16 CLOSING_START(A,B) (A:e09)<br>g22 CLOSING_END(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_004: CLOSING |
| -4.30 | B | g17 TRACK_APPEARED_RIGHT(B,A) (B:e08)<br>g18 CLOSING_START(B,A) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| -4.30 | B | g18 CLOSING_START(B,A) (B:e09)<br>g21 CLOSING_END(B,A) (B:e11) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state |
| -1.85 | B | g26 CLOSING_START(B,A) (B:e13) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_002, track_004 |
| -1.85 | B | g26 CLOSING_START(B,A) (B:e13)<br>g40 CLOSING_END(B,A) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_002, track_004 |
| -1.80 | A | g27 CLOSING_START(A,B) (A:e14)<br>g28 CRITICAL_TTC_START(A,B) (A:e15) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -1.80 | A | g27 CLOSING_START(A,B) (A:e14)<br>g28 CRITICAL_TTC_START(A,B) (A:e15)<br>g41 COLLISION(A,B) (A:e21)<br>g42 CRITICAL_TTC_END(A,B) (A:e22)<br>g44 CLOSING_END(A,B) (A:e23) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -1.75 | B | g29 CRITICAL_TTC_START(B,A) (B:e14) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_002, track_004 |
| -1.75 | B | g29 CRITICAL_TTC_START(B,A) (B:e14)<br>g41 COLLISION(A,B) (B:e21)<br>g43 CRITICAL_TTC_END(B,A) (B:e22) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_002, track_004 |
| -1.20 | A | g30 EGO_PATH_ENTRY(A,U1) (A:e16)<br>g31 CRITICAL_TTC_START(A,U1) (A:e17) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -1.20 | A | g30 EGO_PATH_ENTRY(A,U1) (A:e16)<br>g56 EGO_PATH_EXIT(A,U1) (A:e30) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -1.20 | A | g31 CRITICAL_TTC_START(A,U1) (A:e17)<br>g53 CRITICAL_TTC_END(A,U1) (A:e28) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -0.95 | A | g33 TRACK_APPEARED_LEFT(A,U4) (A:e18)<br>g34 CLOSING_START(A,U4) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -0.95 | A | g34 CLOSING_START(A,U4) (A:e19)<br>g51 CLOSING_END(A,U4) (A:e27) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -0.90 | B | g35 EGO_PATH_ENTRY(B,U1) (B:e16)<br>g36 CRITICAL_TTC_START(B,U1) (B:e17) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004 |
| -0.85 | A | g37 TRACK_APPEARED_RIGHT(A,U2) (A:e20) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| -0.40 | B | g38 TRACK_APPEARED_FRONT(B,U2) (B:e18) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004 |
| -0.40 | B | g38 TRACK_APPEARED_FRONT(B,U2) (B:e18)<br>g52 TRACK_LOST(B,U2) (B:e26) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004 |
| -0.25 | B | g39 EGO_PATH_ENTRY(B,A) (B:e19) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 |
| +0.05 | A | g45 THROTTLE_END(A) (A:e24)<br>g47 BRAKE_START(A) (A:e25) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| +0.05 | B | g46 THROTTLE_END(B) (B:e23)<br>g48 BRAKE_START(B) (B:e24)<br>g49 TURN_LEFT_START(B) (B:e25) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 |
| +0.10 | A | g50 TURN_LEFT_START(A) (A:e26) | ego: MOVING, BRAKE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_005: no active state<br>track_006: CLOSING<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| +0.50 | A | g54 EGO_PATH_EXIT(A,U2) (A:e29) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_005: no active state<br>track_006: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| +0.95 | A | g58 TURN_LEFT_END(A) (A:e31) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| +0.95 | B | g59 TURN_LEFT_END(B) (B:e29)<br>g60 MOVING_END(B) (B:e30)<br>g61 STOP_START(B) (B:e31) | ego: MOVING, BRAKE, TURN_LEFT<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_006 |
| +1.00 | A | g62 MOVING_END(A) (A:e32)<br>g63 STOP_START(A) (A:e33) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| +1.15 | A | g64 TRACK_APPEARED_RIGHT(A,U5) (A:e34) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| +1.15 | A | g64 TRACK_APPEARED_RIGHT(A,U5) (A:e34)<br>g66 TRACK_LOST(A,U5) (A:e36) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_004 |
| +1.40 | A | g65 EGO_PATH_ENTRY(A,B) (A:e35) | ego: STOP, BRAKE<br>track_001: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_003, track_004 |

## Plain-language reading

- 7.30 s before the reference collision, A started moving (already the case when first observed).
- 7.30 s before the reference collision, B started moving (already the case when first observed).
- 7.30 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.30 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared in front of it.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 7.15 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its left.
- 7.15 s before the reference collision, A observed anonymous road user U4 start closing in (already the case when first observed).
- 7.00 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.80 s before the reference collision, B's time-to-contact with anonymous road user U4 became critical.
- 6.40 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.40 s before the reference collision, A observed B start closing in (already the case when first observed).
- 4.30 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.30 s before the reference collision, B observed A start closing in (already the case when first observed).
- 4.00 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.90 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.75 s before the reference collision, B observed A stop closing in.
- 3.15 s before the reference collision, A observed B stop closing in.
- 2.75 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 2.50 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.25 s before the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 1.85 s before the reference collision, B observed A start closing in.
- 1.80 s before the reference collision, A observed B start closing in.
- 1.80 s before the reference collision, A's time-to-contact with B became critical.
- 1.75 s before the reference collision, B's time-to-contact with A became critical.
- 1.20 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 1.20 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 1.10 s before the reference collision, B's time-to-contact with anonymous road user U4 stopped being critical.
- 0.95 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its left.
- 0.95 s before the reference collision, A observed anonymous road user U4 start closing in (already the case when first observed).
- 0.90 s before the reference collision, B observed anonymous road user U1 enter its forward path corridor.
- 0.90 s before the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 0.85 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its right.
- 0.40 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared in front of it.
- 0.25 s before the reference collision, B observed A enter its forward path corridor.
- 0.10 s before the reference collision, B observed A stop closing in.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 389, B: 389 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B started turning left.
- 0.10 s after the reference collision, A started turning left.
- 0.20 s after the reference collision, A observed anonymous road user U4 stop closing in.
- 0.30 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 0.50 s after the reference collision, A observed anonymous road user U2 leave its forward path corridor.
- 0.50 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 0.70 s after the reference collision, B's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the reference collision, A stopped turning left.
- 0.95 s after the reference collision, B stopped turning left.
- 0.95 s after the reference collision, B stopped moving.
- 0.95 s after the reference collision, B came to a stop.
- 1.00 s after the reference collision, A stopped moving.
- 1.00 s after the reference collision, A came to a stop.
- 1.15 s after the reference collision, A's radar started tracking anonymous road user U5, which appeared on its right.
- 1.40 s after the reference collision, A observed B enter its forward path corridor.
- 4.60 s after the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
