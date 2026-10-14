# Global graph - S12/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| U1 | anonymous_road_user | anonymous; observed by A, B as A:track_001, B:track_002, B:track_003 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 4.95 | -4.95 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 4.95 | -4.95 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1576.92 vs 1576.92 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.9 m -> 1.0 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 1.91 m/s for reference)<br>clearance at the contact 0.99 m<br>anonymous road user U1: A:track_001, B:track_002, B:track_003 |
| A:track_002 | B | ASSOCIATED | 0.93 | A and B both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.6 m -> 0.7 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.57 m/s for reference)<br>clearance at the contact 0.73 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.89 | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 0.6 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.71 m/s for reference)<br>clearance at the contact 0.00 m<br>the only compatible track of B touching it at the contact (clearance 0.00 m; track_002 at 4.94 m) |
| B:track_002 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 4.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 6.9 m -> 4.9 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 1.21 m/s for reference)<br>clearance at the contact 4.94 m (beyond 3.50 m: confidence factor 0.89)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_001, track_002)<br>anonymous road user U1: A:track_001, B:track_002, B:track_003 |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1576.92 vs 1576.92 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_002, B:track_003 |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.95 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.95 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.95 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -4.95 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -4.95 | TRACK_APPEARED_LEFT | A | B | A:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g06 | -4.95 | TRACK_APPEARED_RIGHT | A | U1 | A:e04 @ 0.00, A:e23 @ 7.45 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g07 | -4.95 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 0.00 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g08 | -4.95 | TRACK_APPEARED_RIGHT | B | U1 | B:e04 @ 0.00, B:e18 @ 5.70 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g09 | -4.95 | CLOSING_START | A | U1 | A:e05 @ 0.00, A:e11 @ 4.60 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g10 | -4.95 | CLOSING_START | B | U1 | B:e05 @ 0.00, B:e16 @ 5.15 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g11 | -2.20 | CRITICAL_TTC_START | A | U1 | A:e06 @ 2.75, A:e18 @ 5.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g12 | -2.20 | CUT_IN_FROM_RIGHT_START | A | U1 | A:e07 @ 2.75, A:e17 @ 5.30 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g13 | -2.20 | CUT_IN_FROM_RIGHT_START | B | A | B:e06 @ 2.75, B:e23 @ 8.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g14 | -2.10 | EGO_PATH_ENTRY | A | U1 | A:e08 @ 2.85, A:e19 @ 5.85 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g15 | -1.15 | CRITICAL_TTC_START | A | B | A:e09 @ 3.80, A:e13 @ 4.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g16 | -1.05 | CRITICAL_TTC_START | B | A | B:e07 @ 3.90, B:e11 @ 4.95 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g17 | -0.90 | EGO_PATH_ENTRY | B | A | B:e08 @ 4.05, B:e15 @ 5.05 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g18 | -0.80 | CLOSING_START | B | A | B:e09 @ 4.15, B:e12 @ 4.95 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g19 | -0.60 | CLOSING_START | A | B | A:e10 @ 4.35, A:e14 @ 4.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g20 | -0.35 | CLOSING_END | A | U1 | A:e11 @ 4.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g21 | 0.00 | COLLISION | - | A, B | A:e12 @ 4.95, B:e10 @ 4.95 | matched_event=collision_001; reference_event=True; peak_impulse=A 1576.92, B 1576.92 |
| g22 | 0.00 | CRITICAL_TTC_END | A | B | A:e13 @ 4.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g23 | 0.00 | CRITICAL_TTC_END | B | A | B:e11 @ 4.95 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g24 | 0.00 | CLOSING_END | A | B | A:e14 @ 4.95 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g25 | 0.00 | CLOSING_END | B | A | B:e12 @ 4.95 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g26 | 0.05 | THROTTLE_END | A | - | A:e15 @ 5.00 |  |
| g27 | 0.05 | THROTTLE_END | B | - | B:e13 @ 5.00 |  |
| g28 | 0.05 | BRAKE_START | A | - | A:e16 @ 5.00 |  |
| g29 | 0.05 | BRAKE_START | B | - | B:e14 @ 5.00 |  |
| g30 | 0.10 | EGO_PATH_EXIT | B | A | B:e15 @ 5.05 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g31 | 0.20 | CLOSING_END | B | U1 | B:e16 @ 5.15 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g32 | 0.35 | CUT_IN_FROM_RIGHT_END | A | U1 | A:e17 @ 5.30 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g33 | 0.55 | CRITICAL_TTC_END | A | U1 | A:e18 @ 5.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g34 | 0.70 | EGO_PATH_ENTRY | B | A | B:e17 @ 5.65 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g35 | 0.75 | TRACK_LOST | B | U1 | B:e18 @ 5.70 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g36 | 0.90 | EGO_PATH_EXIT | A | U1 | A:e19 @ 5.85 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g37 | 1.00 | MOVING_END | B | - | B:e19 @ 5.95 |  |
| g38 | 1.00 | STOP_START | B | - | B:e20 @ 5.95 |  |
| g39 | 1.10 | MOVING_END | A | - | A:e20 @ 6.05 |  |
| g40 | 1.10 | STOP_START | A | - | A:e21 @ 6.05 |  |
| g41 | 1.45 | EGO_PATH_ENTRY | A | B | A:e22 @ 6.40 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g42 | 1.65 | TRACK_APPEARED_RIGHT | B | U1 | B:e21 @ 6.60, B:e22 @ 7.00 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g43 | 2.05 | TRACK_LOST | B | U1 | B:e22 @ 7.00 | source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g44 | 2.50 | TRACK_LOST | A | U1 | A:e23 @ 7.45 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g45 | 3.45 | CUT_IN_FROM_RIGHT_END | B | A | B:e23 @ 8.40 | geometry=estimated_body; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |

## Edges

```
    g01 --PRECEDES--> g11
    g01 --PRECEDES--> g12
    g01 --PRECEDES--> g13
    g02 --PRECEDES--> g11
    g02 --PRECEDES--> g12
    g02 --PRECEDES--> g13
    g03 --PRECEDES--> g11
    g03 --PRECEDES--> g12
    g03 --PRECEDES--> g13
    g04 --PRECEDES--> g11
    g04 --PRECEDES--> g12
    g04 --PRECEDES--> g13
    g05 --PRECEDES--> g11
    g05 --PRECEDES--> g12
    g05 --PRECEDES--> g13
    g06 --PRECEDES--> g11
    g06 --PRECEDES--> g12
    g06 --PRECEDES--> g13
    g07 --PRECEDES--> g11
    g07 --PRECEDES--> g12
    g07 --PRECEDES--> g13
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g08 --PRECEDES--> g13
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g21 --PRECEDES--> g29
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g41
    g41 --PRECEDES--> g42
    g42 --PRECEDES--> g43
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g06 --SAME_TRACK--> g09
    g06 --SAME_TRACK--> g11
    g06 --SAME_TRACK--> g12
    g06 --SAME_TRACK--> g14
    g05 --SAME_TRACK--> g15
    g05 --SAME_TRACK--> g19
    g06 --SAME_TRACK--> g20
    g05 --SAME_TRACK--> g22
    g05 --SAME_TRACK--> g24
    g06 --SAME_TRACK--> g32
    g06 --SAME_TRACK--> g33
    g06 --SAME_TRACK--> g36
    g05 --SAME_TRACK--> g41
    g06 --SAME_TRACK--> g44
    g08 --SAME_TRACK--> g10
    g07 --SAME_TRACK--> g13
    g07 --SAME_TRACK--> g16
    g07 --SAME_TRACK--> g17
    g07 --SAME_TRACK--> g18
    g07 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g25
    g07 --SAME_TRACK--> g30
    g08 --SAME_TRACK--> g31
    g07 --SAME_TRACK--> g34
    g08 --SAME_TRACK--> g35
    g42 --SAME_TRACK--> g43
    g07 --SAME_TRACK--> g45
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.95 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(B,U1) |
| -2.20 | CRITICAL_TTC_START(A,U1); CUT_IN_FROM_RIGHT_START(A,U1); CUT_IN_FROM_RIGHT_START(B,A) |
| -2.10 | EGO_PATH_ENTRY(A,U1) |
| -1.15 | CRITICAL_TTC_START(A,B) |
| -1.05 | CRITICAL_TTC_START(B,A) |
| -0.90 | EGO_PATH_ENTRY(B,A) |
| -0.80 | CLOSING_START(B,A) |
| -0.60 | CLOSING_START(A,B) |
| -0.35 | CLOSING_END(A,U1) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | EGO_PATH_EXIT(B,A) |
| +0.20 | CLOSING_END(B,U1) |
| +0.35 | CUT_IN_FROM_RIGHT_END(A,U1) |
| +0.55 | CRITICAL_TTC_END(A,U1) |
| +0.70 | EGO_PATH_ENTRY(B,A) |
| +0.75 | TRACK_LOST(B,U1) |
| +0.90 | EGO_PATH_EXIT(A,U1) |
| +1.00 | MOVING_END(B); STOP_START(B) |
| +1.10 | MOVING_END(A); STOP_START(A) |
| +1.45 | EGO_PATH_ENTRY(A,B) |
| +1.65 | TRACK_APPEARED_RIGHT(B,U1) |
| +2.05 | TRACK_LOST(B,U1) |
| +2.50 | TRACK_LOST(A,U1) |
| +3.45 | CUT_IN_FROM_RIGHT_END(B,A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified U1): critical TTC already active before the cut-in: CRITICAL_TTC_START 2.75 <= CUT_IN_FROM_RIGHT_START 2.75 (+0.00 s); EGO_PATH_ENTRY 2.85 after critical TTC (+0.10 s) [local times; t_global: cut_in -2.20, critical_ttc_start -2.20, ego_path_entry -2.10, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 3.80, COLLISION with B 4.95 (+1.15 s); EGO_PATH_ENTRY 6.40 after critical TTC (+2.60 s) [local times; t_global: critical_ttc_start -1.15, ego_path_entry +1.45, collision +0.00]
- B's track_001 (A): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 2.75 < CRITICAL_TTC_START 3.90 (+1.15 s) < COLLISION with A 4.95 (+1.05 s); EGO_PATH_ENTRY 4.05 after critical TTC (+0.15 s) [local times; t_global: cut_in -2.20, critical_ttc_start -1.05, ego_path_entry -0.90, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.95 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TRACK_APPEARED_LEFT(A,B) (A:e03)<br>g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g09 CLOSING_START(A,U1) (A:e05) | ego: not yet observed |
| -4.95 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02)<br>g07 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g08 TRACK_APPEARED_RIGHT(B,U1) (B:e04)<br>g10 CLOSING_START(B,U1) (B:e05) | ego: not yet observed |
| -4.95 | A | g06 TRACK_APPEARED_RIGHT(A,U1) (A:e04)<br>g44 TRACK_LOST(A,U1) (A:e23) | ego: not yet observed |
| -4.95 | B | g08 TRACK_APPEARED_RIGHT(B,U1) (B:e04)<br>g35 TRACK_LOST(B,U1) (B:e18) | ego: not yet observed |
| -4.95 | A | g09 CLOSING_START(A,U1) (A:e05)<br>g20 CLOSING_END(A,U1) (A:e11) | ego: not yet observed |
| -4.95 | B | g10 CLOSING_START(B,U1) (B:e05)<br>g31 CLOSING_END(B,U1) (B:e16) | ego: not yet observed |
| -2.20 | A | g11 CRITICAL_TTC_START(A,U1) (A:e06)<br>g12 CUT_IN_FROM_RIGHT_START(A,U1) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state |
| -2.20 | A | g11 CRITICAL_TTC_START(A,U1) (A:e06)<br>g33 CRITICAL_TTC_END(A,U1) (A:e18) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state |
| -2.20 | A | g12 CUT_IN_FROM_RIGHT_START(A,U1) (A:e07)<br>g32 CUT_IN_FROM_RIGHT_END(A,U1) (A:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state |
| -2.20 | B | g13 CUT_IN_FROM_RIGHT_START(B,A) (B:e06) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING |
| -2.20 | B | g13 CUT_IN_FROM_RIGHT_START(B,A) (B:e06)<br>g45 CUT_IN_FROM_RIGHT_END(B,A) (B:e23) | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING |
| -2.10 | A | g14 EGO_PATH_ENTRY(A,U1) (A:e08) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -2.10 | A | g14 EGO_PATH_ENTRY(A,U1) (A:e08)<br>g36 EGO_PATH_EXIT(A,U1) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.15 | A | g15 CRITICAL_TTC_START(A,B) (A:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.15 | A | g15 CRITICAL_TTC_START(A,B) (A:e09)<br>g19 CLOSING_START(A,B) (A:e10)<br>g21 COLLISION(A,B) (A:e12)<br>g22 CRITICAL_TTC_END(A,B) (A:e13)<br>g24 CLOSING_END(A,B) (A:e14) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| -1.05 | B | g16 CRITICAL_TTC_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_RIGHT<br>track_002: CLOSING |
| -1.05 | B | g16 CRITICAL_TTC_START(B,A) (B:e07)<br>g18 CLOSING_START(B,A) (B:e09)<br>g21 COLLISION(A,B) (B:e10)<br>g23 CRITICAL_TTC_END(B,A) (B:e11)<br>g25 CLOSING_END(B,A) (B:e12) | ego: MOVING, THROTTLE<br>track_001: CUT_IN_FROM_RIGHT<br>track_002: CLOSING |
| -0.90 | B | g17 EGO_PATH_ENTRY(B,A) (B:e08) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: CLOSING |
| -0.90 | B | g17 EGO_PATH_ENTRY(B,A) (B:e08)<br>g30 EGO_PATH_EXIT(B,A) (B:e15) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: CLOSING |
| -0.80 | B | g18 CLOSING_START(B,A) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CLOSING |
| -0.60 | A | g19 CLOSING_START(A,B) (A:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CRITICAL_TTC |
| +0.05 | A | g26 THROTTLE_END(A) (A:e15)<br>g28 BRAKE_START(A) (A:e16) | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state |
| +0.05 | B | g27 THROTTLE_END(B) (B:e13)<br>g29 BRAKE_START(B) (B:e14) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CLOSING |
| +0.70 | B | g34 EGO_PATH_ENTRY(B,A) (B:e17) | ego: MOVING, BRAKE<br>track_001: CUT_IN_FROM_RIGHT<br>track_002: no active state |
| +1.00 | B | g37 MOVING_END(B) (B:e19)<br>g38 STOP_START(B) (B:e20) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_002 |
| +1.10 | A | g39 MOVING_END(A) (A:e20)<br>g40 STOP_START(A) (A:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.45 | A | g41 EGO_PATH_ENTRY(A,B) (A:e22) | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state |
| +1.65 | B | g42 TRACK_APPEARED_RIGHT(B,U1) (B:e21) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_002 |
| +1.65 | B | g42 TRACK_APPEARED_RIGHT(B,U1) (B:e21)<br>g43 TRACK_LOST(B,U1) (B:e22) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track lost, states UNKNOWN: track_002 |

## Plain-language reading

- 4.95 s before the reference collision, A started moving (already the case when first observed).
- 4.95 s before the reference collision, B started moving (already the case when first observed).
- 4.95 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.95 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.95 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 4.95 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 4.95 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.95 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 4.95 s before the reference collision, A observed anonymous road user U1 start closing in (already the case when first observed).
- 4.95 s before the reference collision, B observed anonymous road user U1 start closing in (already the case when first observed).
- 2.20 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 2.20 s before the reference collision, A observed anonymous road user U1 cutting in from the right.
- 2.20 s before the reference collision, B observed A cutting in from the right.
- 2.10 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 1.15 s before the reference collision, A's time-to-contact with B became critical.
- 1.05 s before the reference collision, B's time-to-contact with A became critical.
- 0.90 s before the reference collision, B observed A enter its forward path corridor.
- 0.80 s before the reference collision, B observed A start closing in.
- 0.60 s before the reference collision, A observed B start closing in.
- 0.35 s before the reference collision, A observed anonymous road user U1 stop closing in.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1577, B: 1577 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B observed A leave its forward path corridor.
- 0.20 s after the reference collision, B observed anonymous road user U1 stop closing in.
- 0.35 s after the reference collision, A observed anonymous road user U1's cut-in from the right settle.
- 0.55 s after the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 0.70 s after the reference collision, B observed A enter its forward path corridor.
- 0.75 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 0.90 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 1.00 s after the reference collision, B stopped moving.
- 1.00 s after the reference collision, B came to a stop.
- 1.10 s after the reference collision, A stopped moving.
- 1.10 s after the reference collision, A came to a stop.
- 1.45 s after the reference collision, A observed B enter its forward path corridor.
- 1.65 s after the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 2.05 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 2.50 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 3.45 s after the reference collision, B observed A's cut-in from the right settle.
