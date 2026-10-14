# Global graph - S10/run_0_deflected_into_c

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002, C:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002, C:track_002 |
| C | recorder | clock ALIGNED; observed by others as: A:track_001, B:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e28 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e18 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | ALIGNED | C:e12 | 4.70 | -3.80 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 10358.22 vs 10358.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

Matched `collision_002`: A and C both recorded a collision; peak impulses 1880.32 vs 1880.32 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.97 | A and C both reported collision_002 at 4.70 s (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.3 m -> 0.0 m over the last 1.0 s<br>track motion compatible with C's own speed in the observed direction (3 sigma; full-speed RMSE 0.39 m/s for reference)<br>clearance at the contact 0.00 m<br>the only track of A compatible with the contact<br>collision_001 with B at 3.80 s: not compatible (track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 3.69 m/s for reference)) |
| A:track_002 | B | ASSOCIATED | 0.82 | A and B both reported collision_001 at 3.80 s (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 1.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.5 m -> 0.6 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.94 m/s for reference)<br>clearance at the contact 0.62 m<br>the only track of A compatible with the contact<br>collision_002 with C at 4.70 s: not compatible (not approaching before the contact: clearance 1.2 m -> 1.3 m over the last 1.0 s) |
| B:track_001 | C | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 2.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.6 m -> 9.7 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 5.06 m/s for reference)<br>clearance at the contact 9.71 m (beyond 3.50 m: confidence factor 0.12)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 60 samples; 100% within 3 sigma) at C's own velocity |
| B:track_002 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 10358.22 vs 10358.22 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.8 m -> 0.5 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.54 m/s for reference)<br>clearance at the contact 0.54 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 0.99 | C and A both reported collision_002 (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.1 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.22 m/s for reference)<br>clearance at the contact 0.01 m<br>the only track of C compatible with the contact |
| C:track_002 | B | ASSOCIATED | 1.00 | C and A both reported collision_002 (peak impulse 1880.32 vs 1880.32 N*s)<br>tracked for 4.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 9.6 m -> 5.1 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 3.75 m/s for reference)<br>clearance at the contact 5.13 m (beyond 3.50 m: confidence factor 0.86)<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 72 samples; 100% within 3 sigma) at B's own velocity |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.80 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -3.80 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -3.80 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g06 | -3.80 | THROTTLE_START | C | - | C:e02 @ 0.00 | active_at_first_observation=True |
| g07 | -3.70 | TRACK_APPEARED_FRONT | A | C | A:e03 @ 0.10 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g08 | -3.70 | TRACK_APPEARED_FRONT | C | A | C:e03 @ 0.10 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g09 | -3.70 | CLOSING_START | A | C | A:e04 @ 0.10, A:e37 @ 5.00 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g10 | -3.70 | CLOSING_START | C | A | C:e04 @ 0.10, C:e14 @ 4.70 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g11 | -3.65 | EGO_PATH_ENTRY | A | C | A:e05 @ 0.15, A:e06 @ 0.20 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g12 | -3.60 | EGO_PATH_EXIT | A | C | A:e06 @ 0.20 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g13 | -3.60 | TRACK_APPEARED_LEFT | C | B | C:e05 @ 0.20 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g14 | -3.60 | CLOSING_START | C | B | C:e06 @ 0.20, C:e18 @ 4.95 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g15 | -3.10 | EGO_PATH_ENTRY | A | C | A:e07 @ 0.70, A:e08 @ 0.75 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g16 | -3.05 | EGO_PATH_EXIT | A | C | A:e08 @ 0.75 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g17 | -2.75 | EGO_PATH_ENTRY | A | C | A:e09 @ 1.05, A:e10 @ 1.10 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g18 | -2.70 | EGO_PATH_EXIT | A | C | A:e10 @ 1.10 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g19 | -2.70 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e03 @ 1.10 | relevant_to_ego_path=True |
| g20 | -2.20 | EGO_PATH_ENTRY | A | C | A:e11 @ 1.60, A:e12 @ 1.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g21 | -2.15 | EGO_PATH_EXIT | A | C | A:e12 @ 1.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g22 | -2.10 | TRACK_APPEARED_RIGHT | B | C | B:e04 @ 1.70, B:e31 @ 5.50 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g23 | -2.10 | CLOSING_START | B | C | B:e05 @ 1.70, B:e28 @ 4.70 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g24 | -1.85 | EGO_PATH_ENTRY | A | C | A:e13 @ 1.95, A:e14 @ 2.00 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g25 | -1.80 | EGO_PATH_EXIT | A | C | A:e14 @ 2.00 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g26 | -1.80 | TRACK_APPEARED_LEFT | B | A | B:e06 @ 2.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g27 | -1.80 | CLOSING_START | B | A | B:e07 @ 2.00, B:e27 @ 4.15 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g28 | -1.75 | TRACK_APPEARED_RIGHT | A | B | A:e15 @ 2.05 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g29 | -1.75 | CLOSING_START | A | B | A:e16 @ 2.05, A:e30 @ 3.80 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g30 | -1.65 | EGO_PATH_ENTRY | A | C | A:e17 @ 2.15, A:e18 @ 2.20 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g31 | -1.60 | EGO_PATH_EXIT | A | C | A:e18 @ 2.20 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g32 | -1.55 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e08 @ 2.25 |  |
| g33 | -1.50 | TURN_LEFT_START | B | - | B:e09 @ 2.30 |  |
| g34 | -1.30 | EGO_PATH_ENTRY | A | C | A:e19 @ 2.50, A:e20 @ 2.55 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g35 | -1.30 | CRITICAL_TTC_START | B | A | B:e10 @ 2.50, B:e19 @ 3.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g36 | -1.25 | EGO_PATH_EXIT | A | C | A:e20 @ 2.55 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g37 | -1.25 | CRITICAL_TTC_START | A | B | A:e21 @ 2.55, A:e29 @ 3.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g38 | -0.85 | THROTTLE_END | B | - | B:e11 @ 2.95 |  |
| g39 | -0.85 | BRAKE_START | B | - | B:e12 @ 2.95 |  |
| g40 | -0.75 | EGO_PATH_ENTRY | A | C | A:e22 @ 3.05, A:e23 @ 3.10 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g41 | -0.75 | EGO_PATH_ENTRY | B | C | B:e13 @ 3.05, B:e14 @ 3.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g42 | -0.70 | EGO_PATH_EXIT | A | C | A:e23 @ 3.10 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g43 | -0.70 | EGO_PATH_ENTRY | C | B | C:e07 @ 3.10, C:e08 @ 3.90 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g44 | -0.40 | EGO_PATH_EXIT | B | C | B:e14 @ 3.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g45 | -0.30 | BRAKE_END | B | - | B:e15 @ 3.50 |  |
| g46 | -0.20 | EGO_PATH_ENTRY | A | C | A:e24 @ 3.60, A:e25 @ 3.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g47 | -0.20 | EGO_PATH_ENTRY | B | A | B:e16 @ 3.60, B:e21 @ 3.85 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g48 | -0.15 | EGO_PATH_EXIT | A | C | A:e25 @ 3.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g49 | -0.15 | THROTTLE_START | B | - | B:e17 @ 3.65 |  |
| g50 | -0.15 | EGO_PATH_ENTRY | A | B | A:e26 @ 3.65, A:e33 @ 4.05 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g51 | -0.05 | CRITICAL_TTC_START | A | C | A:e27 @ 3.75, A:e36 @ 4.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g52 | 0.00 | COLLISION | - | A, B | A:e28 @ 3.80, B:e18 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 10358.22, B 10358.22 |
| g53 | 0.00 | CRITICAL_TTC_END | A | B | A:e29 @ 3.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g54 | 0.00 | CRITICAL_TTC_END | B | A | B:e19 @ 3.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g55 | 0.00 | CLOSING_END | A | B | A:e30 @ 3.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g56 | 0.00 | TURN_LEFT_END | B | - | B:e20 @ 3.80 |  |
| g57 | 0.05 | EGO_PATH_EXIT | B | A | B:e21 @ 3.85 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g58 | 0.05 | THROTTLE_END | A | - | A:e31 @ 3.85 |  |
| g59 | 0.05 | THROTTLE_END | B | - | B:e22 @ 3.85 |  |
| g60 | 0.05 | BRAKE_START | B | - | B:e23 @ 3.85 |  |
| g61 | 0.05 | TURN_LEFT_START | A | - | A:e32 @ 3.85 |  |
| g62 | 0.10 | EGO_PATH_EXIT | C | B | C:e08 @ 3.90 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g63 | 0.20 | MOVING_END | B | - | B:e24 @ 4.00 |  |
| g64 | 0.20 | STOP_START | B | - | B:e25 @ 4.00 |  |
| g65 | 0.20 | CRITICAL_TTC_START | C | A | C:e09 @ 4.00, C:e13 @ 4.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g66 | 0.25 | EGO_PATH_EXIT | A | B | A:e33 @ 4.05 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g67 | 0.25 | EGO_PATH_ENTRY | A | C | A:e34 @ 4.05, A:e38 @ 5.00 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g68 | 0.25 | EGO_PATH_ENTRY | B | A | B:e26 @ 4.05 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g69 | 0.35 | CLOSING_END | B | A | B:e27 @ 4.15 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g70 | 0.50 | EGO_PATH_ENTRY | C | A | C:e10 @ 4.30 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g71 | 0.70 | EGO_PATH_ENTRY | C | B | C:e11 @ 4.50, C:e17 @ 4.80 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g72 | 0.90 | COLLISION | - | A, C | A:e35 @ 4.70, C:e12 @ 4.70 | matched_event=collision_002; reference_event=False; peak_impulse=A 1880.32, C 1880.32 |
| g73 | 0.90 | CRITICAL_TTC_END | A | C | A:e36 @ 4.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g74 | 0.90 | CRITICAL_TTC_END | C | A | C:e13 @ 4.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g75 | 0.90 | CLOSING_END | B | C | B:e28 @ 4.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g76 | 0.90 | CLOSING_END | C | A | C:e14 @ 4.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g77 | 0.90 | EGO_PATH_ENTRY | B | C | B:e29 @ 4.70, B:e30 @ 5.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g78 | 0.95 | THROTTLE_END | C | - | C:e15 @ 4.75 |  |
| g79 | 0.95 | BRAKE_START | C | - | C:e16 @ 4.75 |  |
| g80 | 1.00 | EGO_PATH_EXIT | C | B | C:e17 @ 4.80 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g81 | 1.15 | CLOSING_END | C | B | C:e18 @ 4.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g82 | 1.20 | CLOSING_END | A | C | A:e37 @ 5.00 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g83 | 1.20 | EGO_PATH_EXIT | A | C | A:e38 @ 5.00 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g84 | 1.20 | MOVING_END | C | - | C:e19 @ 5.00 |  |
| g85 | 1.20 | STOP_START | C | - | C:e20 @ 5.00 |  |
| g86 | 1.25 | TURN_LEFT_END | A | - | A:e39 @ 5.05 |  |
| g87 | 1.30 | MOVING_END | A | - | A:e40 @ 5.10 |  |
| g88 | 1.30 | STOP_START | A | - | A:e41 @ 5.10 |  |
| g89 | 1.60 | EGO_PATH_EXIT | B | C | B:e30 @ 5.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g90 | 1.70 | TRACK_LOST | B | C | B:e31 @ 5.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |

## Edges

```
    g01 --PRECEDES--> g07
    g01 --PRECEDES--> g08
    g01 --PRECEDES--> g09
    g01 --PRECEDES--> g10
    g02 --PRECEDES--> g07
    g02 --PRECEDES--> g08
    g02 --PRECEDES--> g09
    g02 --PRECEDES--> g10
    g03 --PRECEDES--> g07
    g03 --PRECEDES--> g08
    g03 --PRECEDES--> g09
    g03 --PRECEDES--> g10
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g04 --PRECEDES--> g09
    g04 --PRECEDES--> g10
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g05 --PRECEDES--> g09
    g05 --PRECEDES--> g10
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g06 --PRECEDES--> g10
    g07 --PRECEDES--> g11
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
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
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g52 --PRECEDES--> g58
    g52 --PRECEDES--> g59
    g52 --PRECEDES--> g60
    g52 --PRECEDES--> g61
    g53 --PRECEDES--> g57
    g53 --PRECEDES--> g58
    g53 --PRECEDES--> g59
    g53 --PRECEDES--> g60
    g53 --PRECEDES--> g61
    g54 --PRECEDES--> g57
    g54 --PRECEDES--> g58
    g54 --PRECEDES--> g59
    g54 --PRECEDES--> g60
    g54 --PRECEDES--> g61
    g55 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g55 --PRECEDES--> g60
    g55 --PRECEDES--> g61
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g56 --PRECEDES--> g60
    g56 --PRECEDES--> g61
    g57 --PRECEDES--> g62
    g58 --PRECEDES--> g62
    g59 --PRECEDES--> g62
    g60 --PRECEDES--> g62
    g61 --PRECEDES--> g62
    g62 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g62 --PRECEDES--> g65
    g63 --PRECEDES--> g66
    g63 --PRECEDES--> g67
    g63 --PRECEDES--> g68
    g64 --PRECEDES--> g66
    g64 --PRECEDES--> g67
    g64 --PRECEDES--> g68
    g65 --PRECEDES--> g66
    g65 --PRECEDES--> g67
    g65 --PRECEDES--> g68
    g66 --PRECEDES--> g69
    g67 --PRECEDES--> g69
    g68 --PRECEDES--> g69
    g69 --PRECEDES--> g70
    g70 --PRECEDES--> g71
    g71 --PRECEDES--> g72
    g71 --PRECEDES--> g73
    g71 --PRECEDES--> g74
    g71 --PRECEDES--> g75
    g71 --PRECEDES--> g76
    g71 --PRECEDES--> g77
    g72 --PRECEDES--> g78
    g72 --PRECEDES--> g79
    g73 --PRECEDES--> g78
    g73 --PRECEDES--> g79
    g74 --PRECEDES--> g78
    g74 --PRECEDES--> g79
    g75 --PRECEDES--> g78
    g75 --PRECEDES--> g79
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
    g81 --PRECEDES--> g85
    g82 --PRECEDES--> g86
    g83 --PRECEDES--> g86
    g84 --PRECEDES--> g86
    g85 --PRECEDES--> g86
    g86 --PRECEDES--> g87
    g86 --PRECEDES--> g88
    g87 --PRECEDES--> g89
    g88 --PRECEDES--> g89
    g89 --PRECEDES--> g90
    g07 --SAME_TRACK--> g09
    g07 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g12
    g07 --SAME_TRACK--> g15
    g07 --SAME_TRACK--> g16
    g07 --SAME_TRACK--> g17
    g07 --SAME_TRACK--> g18
    g07 --SAME_TRACK--> g20
    g07 --SAME_TRACK--> g21
    g07 --SAME_TRACK--> g24
    g07 --SAME_TRACK--> g25
    g28 --SAME_TRACK--> g29
    g07 --SAME_TRACK--> g30
    g07 --SAME_TRACK--> g31
    g07 --SAME_TRACK--> g34
    g07 --SAME_TRACK--> g36
    g28 --SAME_TRACK--> g37
    g07 --SAME_TRACK--> g40
    g07 --SAME_TRACK--> g42
    g07 --SAME_TRACK--> g46
    g07 --SAME_TRACK--> g48
    g28 --SAME_TRACK--> g50
    g07 --SAME_TRACK--> g51
    g28 --SAME_TRACK--> g53
    g28 --SAME_TRACK--> g55
    g28 --SAME_TRACK--> g66
    g07 --SAME_TRACK--> g67
    g07 --SAME_TRACK--> g73
    g07 --SAME_TRACK--> g82
    g07 --SAME_TRACK--> g83
    g22 --SAME_TRACK--> g23
    g26 --SAME_TRACK--> g27
    g26 --SAME_TRACK--> g35
    g22 --SAME_TRACK--> g41
    g22 --SAME_TRACK--> g44
    g26 --SAME_TRACK--> g47
    g26 --SAME_TRACK--> g54
    g26 --SAME_TRACK--> g57
    g26 --SAME_TRACK--> g68
    g26 --SAME_TRACK--> g69
    g22 --SAME_TRACK--> g75
    g22 --SAME_TRACK--> g77
    g22 --SAME_TRACK--> g89
    g22 --SAME_TRACK--> g90
    g08 --SAME_TRACK--> g10
    g13 --SAME_TRACK--> g14
    g13 --SAME_TRACK--> g43
    g13 --SAME_TRACK--> g62
    g08 --SAME_TRACK--> g65
    g08 --SAME_TRACK--> g70
    g13 --SAME_TRACK--> g71
    g08 --SAME_TRACK--> g74
    g08 --SAME_TRACK--> g76
    g13 --SAME_TRACK--> g80
    g13 --SAME_TRACK--> g81
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B); MOVING_START(C); THROTTLE_START(A); THROTTLE_START(B); THROTTLE_START(C) |
| -3.70 | TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A) |
| -3.65 | EGO_PATH_ENTRY(A,C) |
| -3.60 | EGO_PATH_EXIT(A,C); TRACK_APPEARED_LEFT(C,B); CLOSING_START(C,B) |
| -3.10 | EGO_PATH_ENTRY(A,C) |
| -3.05 | EGO_PATH_EXIT(A,C) |
| -2.75 | EGO_PATH_ENTRY(A,C) |
| -2.70 | EGO_PATH_EXIT(A,C); STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -2.20 | EGO_PATH_ENTRY(A,C) |
| -2.15 | EGO_PATH_EXIT(A,C) |
| -2.10 | TRACK_APPEARED_RIGHT(B,C); CLOSING_START(B,C) |
| -1.85 | EGO_PATH_ENTRY(A,C) |
| -1.80 | EGO_PATH_EXIT(A,C); TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.75 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -1.65 | EGO_PATH_ENTRY(A,C) |
| -1.60 | EGO_PATH_EXIT(A,C) |
| -1.55 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -1.50 | TURN_LEFT_START(B) |
| -1.30 | EGO_PATH_ENTRY(A,C); CRITICAL_TTC_START(B,A) |
| -1.25 | EGO_PATH_EXIT(A,C); CRITICAL_TTC_START(A,B) |
| -0.85 | THROTTLE_END(B); BRAKE_START(B) |
| -0.75 | EGO_PATH_ENTRY(A,C); EGO_PATH_ENTRY(B,C) |
| -0.70 | EGO_PATH_EXIT(A,C); EGO_PATH_ENTRY(C,B) |
| -0.40 | EGO_PATH_EXIT(B,C) |
| -0.30 | BRAKE_END(B) |
| -0.20 | EGO_PATH_ENTRY(A,C); EGO_PATH_ENTRY(B,A) |
| -0.15 | EGO_PATH_EXIT(A,C); THROTTLE_START(B); EGO_PATH_ENTRY(A,B) |
| -0.05 | CRITICAL_TTC_START(A,C) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); TURN_LEFT_END(B) |
| +0.05 | EGO_PATH_EXIT(B,A); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(B); TURN_LEFT_START(A) |
| +0.10 | EGO_PATH_EXIT(C,B) |
| +0.20 | MOVING_END(B); STOP_START(B); CRITICAL_TTC_START(C,A) |
| +0.25 | EGO_PATH_EXIT(A,B); EGO_PATH_ENTRY(A,C); EGO_PATH_ENTRY(B,A) |
| +0.35 | CLOSING_END(B,A) |
| +0.50 | EGO_PATH_ENTRY(C,A) |
| +0.70 | EGO_PATH_ENTRY(C,B) |
| +0.90 | COLLISION(A,C); CRITICAL_TTC_END(A,C); CRITICAL_TTC_END(C,A); CLOSING_END(B,C); CLOSING_END(C,A); EGO_PATH_ENTRY(B,C) |
| +0.95 | THROTTLE_END(C); BRAKE_START(C) |
| +1.00 | EGO_PATH_EXIT(C,B) |
| +1.15 | CLOSING_END(C,B) |
| +1.20 | CLOSING_END(A,C); EGO_PATH_EXIT(A,C); MOVING_END(C); STOP_START(C) |
| +1.25 | TURN_LEFT_END(A) |
| +1.30 | MOVING_END(A); STOP_START(A) |
| +1.60 | EGO_PATH_EXIT(B,C) |
| +1.70 | TRACK_LOST(B,C) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 4.70 (+0.95 s); EGO_PATH_ENTRY 0.15 before critical TTC (-3.60 s) [local times; t_global: critical_ttc_start -0.05, ego_path_entry -3.65, collision +0.90]
- A's track_002 (B): CRITICAL_TTC_START 2.55, COLLISION with B 3.80 (+1.25 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.10 s) [local times; t_global: critical_ttc_start -1.25, ego_path_entry -0.15, collision +0.00]
- B's track_001 (C): EGO_PATH_ENTRY 3.05, no critical TTC [local times; t_global: ego_path_entry -0.75]
- B's track_002 (A): CRITICAL_TTC_START 2.50, COLLISION with A 3.80 (+1.30 s); EGO_PATH_ENTRY 3.60 after critical TTC (+1.10 s) [local times; t_global: critical_ttc_start -1.30, ego_path_entry -0.20, collision +0.00]
- C's track_001 (A): CRITICAL_TTC_START 4.00, COLLISION with A 4.70 (+0.70 s); EGO_PATH_ENTRY 4.30 after critical TTC (+0.30 s) [local times; t_global: critical_ttc_start +0.20, ego_path_entry +0.50, collision +0.90]
- C's track_002 (B): EGO_PATH_ENTRY 3.10, no critical TTC [local times; t_global: ego_path_entry -0.70]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.80 | A | g01 MOVING_START(A) (A:e01)<br>g04 THROTTLE_START(A) (A:e02) | ego: not yet observed |
| -3.80 | B | g02 MOVING_START(B) (B:e01)<br>g05 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -3.80 | C | g03 MOVING_START(C) (C:e01)<br>g06 THROTTLE_START(C) (C:e02) | ego: not yet observed |
| -3.70 | A | g07 TRACK_APPEARED_FRONT(A,C) (A:e03)<br>g09 CLOSING_START(A,C) (A:e04) | ego: MOVING, THROTTLE |
| -3.70 | C | g08 TRACK_APPEARED_FRONT(C,A) (C:e03)<br>g10 CLOSING_START(C,A) (C:e04) | ego: MOVING, THROTTLE |
| -3.70 | A | g09 CLOSING_START(A,C) (A:e04)<br>g67 EGO_PATH_ENTRY(A,C) (A:e34)<br>g82 CLOSING_END(A,C) (A:e37)<br>g83 EGO_PATH_EXIT(A,C) (A:e38) | ego: MOVING, THROTTLE |
| -3.70 | C | g10 CLOSING_START(C,A) (C:e04)<br>g65 CRITICAL_TTC_START(C,A) (C:e09)<br>g72 COLLISION(A,C) (C:e12)<br>g74 CRITICAL_TTC_END(C,A) (C:e13)<br>g76 CLOSING_END(C,A) (C:e14) | ego: MOVING, THROTTLE |
| -3.65 | A | g11 EGO_PATH_ENTRY(A,C) (A:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -3.65 | A | g11 EGO_PATH_ENTRY(A,C) (A:e05)<br>g12 EGO_PATH_EXIT(A,C) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -3.60 | C | g13 TRACK_APPEARED_LEFT(C,B) (C:e05)<br>g14 CLOSING_START(C,B) (C:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -3.60 | C | g14 CLOSING_START(C,B) (C:e06)<br>g81 CLOSING_END(C,B) (C:e18) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? |
| -3.10 | A | g15 EGO_PATH_ENTRY(A,C) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -3.10 | A | g15 EGO_PATH_ENTRY(A,C) (A:e07)<br>g16 EGO_PATH_EXIT(A,C) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.75 | A | g17 EGO_PATH_ENTRY(A,C) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.75 | A | g17 EGO_PATH_ENTRY(A,C) (A:e09)<br>g18 EGO_PATH_EXIT(A,C) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.70 | B | g19 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e03) | ego: MOVING, THROTTLE |
| -2.20 | A | g20 EGO_PATH_ENTRY(A,C) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.20 | A | g20 EGO_PATH_ENTRY(A,C) (A:e11)<br>g21 EGO_PATH_EXIT(A,C) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.10 | B | g22 TRACK_APPEARED_RIGHT(B,C) (B:e04)<br>g23 CLOSING_START(B,C) (B:e05) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -2.10 | B | g22 TRACK_APPEARED_RIGHT(B,C) (B:e04)<br>g90 TRACK_LOST(B,C) (B:e31) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -2.10 | B | g23 CLOSING_START(B,C) (B:e05)<br>g75 CLOSING_END(B,C) (B:e28)<br>g77 EGO_PATH_ENTRY(B,C) (B:e29) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -1.85 | A | g24 EGO_PATH_ENTRY(A,C) (A:e13) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.85 | A | g24 EGO_PATH_ENTRY(A,C) (A:e13)<br>g25 EGO_PATH_EXIT(A,C) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.80 | B | g26 TRACK_APPEARED_LEFT(B,A) (B:e06)<br>g27 CLOSING_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.80 | B | g27 CLOSING_START(B,A) (B:e07)<br>g69 CLOSING_END(B,A) (B:e27) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.75 | A | g28 TRACK_APPEARED_RIGHT(A,B) (A:e15)<br>g29 CLOSING_START(A,B) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.75 | A | g29 CLOSING_START(A,B) (A:e16)<br>g37 CRITICAL_TTC_START(A,B) (A:e21)<br>g52 COLLISION(A,B) (A:e28)<br>g53 CRITICAL_TTC_END(A,B) (A:e29)<br>g55 CLOSING_END(A,B) (A:e30) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.65 | A | g30 EGO_PATH_ENTRY(A,C) (A:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.65 | A | g30 EGO_PATH_ENTRY(A,C) (A:e17)<br>g31 EGO_PATH_EXIT(A,C) (A:e18) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.55 | B | g32 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.50 | B | g33 TURN_LEFT_START(B) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.30 | A | g34 EGO_PATH_ENTRY(A,C) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.30 | A | g34 EGO_PATH_ENTRY(A,C) (A:e19)<br>g36 EGO_PATH_EXIT(A,C) (A:e20)<br>g37 CRITICAL_TTC_START(A,B) (A:e21) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.30 | B | g35 CRITICAL_TTC_START(B,A) (B:e10) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -1.30 | B | g35 CRITICAL_TTC_START(B,A) (B:e10)<br>g52 COLLISION(A,B) (B:e18)<br>g54 CRITICAL_TTC_END(B,A) (B:e19)<br>g56 TURN_LEFT_END(B) (B:e20) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -0.85 | B | g38 THROTTLE_END(B) (B:e11)<br>g39 BRAKE_START(B) (B:e12) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.75 | A | g40 EGO_PATH_ENTRY(A,C) (A:e22) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.75 | A | g40 EGO_PATH_ENTRY(A,C) (A:e22)<br>g42 EGO_PATH_EXIT(A,C) (A:e23) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.75 | B | g41 EGO_PATH_ENTRY(B,C) (B:e13) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.75 | B | g41 EGO_PATH_ENTRY(B,C) (B:e13)<br>g44 EGO_PATH_EXIT(B,C) (B:e14) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.70 | C | g43 EGO_PATH_ENTRY(C,B) (C:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| -0.70 | C | g43 EGO_PATH_ENTRY(C,B) (C:e07)<br>g62 EGO_PATH_EXIT(C,B) (C:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| -0.30 | B | g45 BRAKE_END(B) (B:e15) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.20 | A | g46 EGO_PATH_ENTRY(A,C) (A:e24) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.20 | A | g46 EGO_PATH_ENTRY(A,C) (A:e24)<br>g48 EGO_PATH_EXIT(A,C) (A:e25)<br>g50 EGO_PATH_ENTRY(A,B) (A:e26) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.20 | B | g47 EGO_PATH_ENTRY(B,A) (B:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.20 | B | g47 EGO_PATH_ENTRY(B,A) (B:e16)<br>g57 EGO_PATH_EXIT(B,A) (B:e21)<br>g59 THROTTLE_END(B) (B:e22)<br>g60 BRAKE_START(B) (B:e23) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.15 | B | g49 THROTTLE_START(B) (B:e17) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| -0.15 | A | g50 EGO_PATH_ENTRY(A,B) (A:e26)<br>g66 EGO_PATH_EXIT(A,B) (A:e33)<br>g67 EGO_PATH_ENTRY(A,C) (A:e34) | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC |
| -0.05 | A | g51 CRITICAL_TTC_START(A,C) (A:e27) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.05 | A | g51 CRITICAL_TTC_START(A,C) (A:e27)<br>g72 COLLISION(A,C) (A:e35)<br>g73 CRITICAL_TTC_END(A,C) (A:e36) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g58 THROTTLE_END(A) (A:e31)<br>g61 TURN_LEFT_START(A) (A:e32) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: IN_EGO_PATH |
| +0.20 | B | g63 MOVING_END(B) (B:e24)<br>g64 STOP_START(B) (B:e25) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| +0.20 | C | g65 CRITICAL_TTC_START(C,A) (C:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING |
| +0.25 | B | g68 EGO_PATH_ENTRY(B,A) (B:e26) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| +0.50 | C | g70 EGO_PATH_ENTRY(C,A) (C:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING |
| +0.70 | C | g71 EGO_PATH_ENTRY(C,B) (C:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING |
| +0.70 | C | g71 EGO_PATH_ENTRY(C,B) (C:e11)<br>g80 EGO_PATH_EXIT(C,B) (C:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING |
| +0.90 | B | g77 EGO_PATH_ENTRY(B,C) (B:e29)<br>g89 EGO_PATH_EXIT(B,C) (B:e30) | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.95 | C | g78 THROTTLE_END(C) (C:e15)<br>g79 BRAKE_START(C) (C:e16) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH |
| +1.20 | C | g84 MOVING_END(C) (C:e19)<br>g85 STOP_START(C) (C:e20) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state |
| +1.25 | A | g86 TURN_LEFT_END(A) (A:e39) | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>track_002: no active state |
| +1.30 | A | g87 MOVING_END(A) (A:e40)<br>g88 STOP_START(A) (A:e41) | ego: MOVING<br>track_001: no active state<br>track_002: no active state |

## Plain-language reading

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 3.80 s before the reference collision, C started moving (already the case when first observed).
- 3.80 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 3.80 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 3.70 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 3.70 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 3.70 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.70 s before the reference collision, C observed A start closing in (already the case when first observed).
- 3.65 s before the reference collision, A observed C enter its forward path corridor.
- 3.60 s before the reference collision, A observed C leave its forward path corridor.
- 3.60 s before the reference collision, C's radar started tracking B, which appeared on its left.
- 3.60 s before the reference collision, C observed B start closing in (already the case when first observed).
- 3.10 s before the reference collision, A observed C enter its forward path corridor.
- 3.05 s before the reference collision, A observed C leave its forward path corridor.
- 2.75 s before the reference collision, A observed C enter its forward path corridor.
- 2.70 s before the reference collision, A observed C leave its forward path corridor.
- 2.70 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 2.20 s before the reference collision, A observed C enter its forward path corridor.
- 2.15 s before the reference collision, A observed C leave its forward path corridor.
- 2.10 s before the reference collision, B's radar started tracking C, which appeared on its right.
- 2.10 s before the reference collision, B observed C start closing in (already the case when first observed).
- 1.85 s before the reference collision, A observed C enter its forward path corridor.
- 1.80 s before the reference collision, A observed C leave its forward path corridor.
- 1.80 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.80 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.75 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.75 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.65 s before the reference collision, A observed C enter its forward path corridor.
- 1.60 s before the reference collision, A observed C leave its forward path corridor.
- 1.55 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.50 s before the reference collision, B started turning left.
- 1.30 s before the reference collision, A observed C enter its forward path corridor.
- 1.30 s before the reference collision, B's time-to-contact with A became critical.
- 1.25 s before the reference collision, A observed C leave its forward path corridor.
- 1.25 s before the reference collision, A's time-to-contact with B became critical.
- 0.85 s before the reference collision, B released the accelerator.
- 0.85 s before the reference collision, B started braking.
- 0.75 s before the reference collision, A observed C enter its forward path corridor.
- 0.75 s before the reference collision, B observed C enter its forward path corridor.
- 0.70 s before the reference collision, A observed C leave its forward path corridor.
- 0.70 s before the reference collision, C observed B enter its forward path corridor.
- 0.40 s before the reference collision, B observed C leave its forward path corridor.
- 0.30 s before the reference collision, B released the brake.
- 0.20 s before the reference collision, A observed C enter its forward path corridor.
- 0.20 s before the reference collision, B observed A enter its forward path corridor.
- 0.15 s before the reference collision, A observed C leave its forward path corridor.
- 0.15 s before the reference collision, B pressed the accelerator.
- 0.15 s before the reference collision, A observed B enter its forward path corridor.
- 0.05 s before the reference collision, A's time-to-contact with C became critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 10358, B: 10358 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B stopped turning left.
- 0.05 s after the reference collision, B observed A leave its forward path corridor.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A started turning left.
- 0.10 s after the reference collision, C observed B leave its forward path corridor.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.20 s after the reference collision, C's time-to-contact with A became critical.
- 0.25 s after the reference collision, A observed B leave its forward path corridor.
- 0.25 s after the reference collision, A observed C enter its forward path corridor.
- 0.25 s after the reference collision, B observed A enter its forward path corridor.
- 0.35 s after the reference collision, B observed A stop closing in.
- 0.50 s after the reference collision, C observed A enter its forward path corridor.
- 0.70 s after the reference collision, C observed B enter its forward path corridor.
- 0.90 s after the reference collision, A and C both recorded this same collision (peak impulses A: 1880, C: 1880 N*s).
- 0.90 s after the reference collision, A's time-to-contact with C stopped being critical.
- 0.90 s after the reference collision, C's time-to-contact with A stopped being critical.
- 0.90 s after the reference collision, B observed C stop closing in.
- 0.90 s after the reference collision, C observed A stop closing in.
- 0.90 s after the reference collision, B observed C enter its forward path corridor.
- 0.95 s after the reference collision, C released the accelerator.
- 0.95 s after the reference collision, C started braking.
- 1.00 s after the reference collision, C observed B leave its forward path corridor.
- 1.15 s after the reference collision, C observed B stop closing in.
- 1.20 s after the reference collision, A observed C stop closing in.
- 1.20 s after the reference collision, A observed C leave its forward path corridor.
- 1.20 s after the reference collision, C stopped moving.
- 1.20 s after the reference collision, C came to a stop.
- 1.25 s after the reference collision, A stopped turning left.
- 1.30 s after the reference collision, A stopped moving.
- 1.30 s after the reference collision, A came to a stop.
- 1.60 s after the reference collision, B observed C leave its forward path corridor.
- 1.70 s after the reference collision, B's radar lost C (its states are UNKNOWN from then on, not ended).
