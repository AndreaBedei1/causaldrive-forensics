# Global graph - S09/run_0_near_simultaneous

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001, B:track_002, B:track_003 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001, A:track_002 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e20 | 7.15 | -7.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e25 | 7.15 | -7.15 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 7661.46 vs 7661.46 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 7661.46 vs 7661.46 N*s)<br>tracked for 4.65 s before the matched collision<br>lost 3.65 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 26.9 m -> 17.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 21 samples; 100% within 3 sigma) at B's own velocity |
| A:track_002 | B | ASSOCIATED | 0.89 | A and B both reported collision_001 (peak impulse 7661.46 vs 7661.46 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.8 m -> 0.2 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.73 m/s for reference)<br>clearance at the contact 0.22 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.85 | B and A both reported collision_001 (peak impulse 7661.46 vs 7661.46 N*s)<br>tracked for 4.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.3 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.84 m/s for reference)<br>clearance at the contact 0.00 m<br>the only track of B compatible with the contact |
| B:track_002 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 7661.46 vs 7661.46 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.15 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 2.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.71 m/s for reference)<br>clearance at the contact 1.95 m<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 16 samples; 100% within 3 sigma) at A's own velocity |
| B:track_003 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 7661.46 vs 7661.46 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 111 samples; 100% within 3 sigma) at A's own velocity |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -7.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -7.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -7.15 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -7.15 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -6.95 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e03 @ 0.20 | relevant_to_ego_path=True |
| g06 | -6.45 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e03 @ 0.70 | relevant_to_ego_path=True |
| g07 | -4.75 | THROTTLE_END | A | - | A:e04 @ 2.40 |  |
| g08 | -4.75 | BRAKE_START | A | - | A:e05 @ 2.40 |  |
| g09 | -4.65 | THROTTLE_END | B | - | B:e04 @ 2.50 |  |
| g10 | -4.65 | BRAKE_START | B | - | B:e05 @ 2.50 |  |
| g11 | -4.65 | TRACK_APPEARED_LEFT | A | B | A:e06 @ 2.50, A:e09 @ 3.50 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g12 | -4.65 | TRACK_APPEARED_RIGHT | B | A | B:e06 @ 2.50, B:e28 @ 7.15, B:e18 @ 6.20, B:e24 @ 7.00 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001', 'B:track_002'] |
| g13 | -4.65 | CLOSING_START | A | B | A:e07 @ 2.50 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g14 | -4.65 | CLOSING_START | B | A | B:e07 @ 2.50, B:e11 @ 3.70 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g15 | -4.40 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e08 @ 2.75 |  |
| g16 | -4.35 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e08 @ 2.80 |  |
| g17 | -3.65 | TRACK_LOST | A | B | A:e09 @ 3.50 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g18 | -3.55 | MOVING_END | B | - | B:e09 @ 3.60 |  |
| g19 | -3.55 | STOP_START | B | - | B:e10 @ 3.60 |  |
| g20 | -3.45 | CLOSING_END | B | A | B:e11 @ 3.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g21 | -3.45 | MOVING_END | A | - | A:e10 @ 3.70 |  |
| g22 | -3.45 | STOP_START | A | - | A:e11 @ 3.70 |  |
| g23 | -2.45 | BRAKE_END | B | - | B:e12 @ 4.70 |  |
| g24 | -2.45 | THROTTLE_START | B | - | B:e13 @ 4.70 |  |
| g25 | -2.30 | BRAKE_END | A | - | A:e12 @ 4.85 |  |
| g26 | -2.30 | THROTTLE_START | A | - | A:e13 @ 4.85 |  |
| g27 | -2.05 | CLOSING_START | B | A | B:e14 @ 5.10, B:e27 @ 7.15, B:e19 @ 6.20 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001', 'B:track_002'] |
| g28 | -2.00 | STOP_END | B | - | B:e15 @ 5.15 |  |
| g29 | -2.00 | MOVING_START | B | - | B:e16 @ 5.15 |  |
| g30 | -2.00 | TRACK_APPEARED_LEFT | A | B | A:e14 @ 5.15 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g31 | -2.00 | CLOSING_START | A | B | A:e15 @ 5.15, A:e22 @ 7.20 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g32 | -1.95 | STOP_END | A | - | A:e16 @ 5.20 |  |
| g33 | -1.95 | MOVING_START | A | - | A:e17 @ 5.20 |  |
| g34 | -1.25 | CRITICAL_TTC_START | A | B | A:e18 @ 5.90, A:e21 @ 7.15 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g35 | -1.10 | CRITICAL_TTC_START | B | A | B:e17 @ 6.05, B:e26 @ 7.15, B:e21 @ 6.70 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001', 'B:track_002'] |
| g36 | -1.00 | TURN_LEFT_START | A | - | A:e19 @ 6.15 |  |
| g37 | -0.80 | EGO_PATH_ENTRY | B | A | B:e20 @ 6.35, B:e23 @ 7.00, B:e22 @ 6.80 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_001', 'B:track_002'] |
| g38 | 0.00 | COLLISION | - | A, B | A:e20 @ 7.15, B:e25 @ 7.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 7661.46, B 7661.46 |
| g39 | 0.00 | CRITICAL_TTC_END | A | B | A:e21 @ 7.15 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g40 | 0.00 | CRITICAL_TTC_END | B | A | B:e26 @ 7.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001', 'B:track_002'] |
| g41 | 0.00 | CLOSING_END | B | A | B:e27 @ 7.15 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001', 'B:track_002'] |
| g42 | 0.00 | TRACK_LOST | B | A | B:e28 @ 7.15, B:e24 @ 7.00 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001', 'B:track_002'] |
| g43 | 0.05 | CLOSING_END | A | B | A:e22 @ 7.20 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g44 | 0.05 | THROTTLE_END | A | - | A:e23 @ 7.20 |  |
| g45 | 0.05 | THROTTLE_END | B | - | B:e29 @ 7.20 |  |
| g46 | 0.05 | BRAKE_START | A | - | A:e24 @ 7.20 |  |
| g47 | 0.05 | BRAKE_START | B | - | B:e30 @ 7.20 |  |
| g48 | 0.20 | TRACK_APPEARED_LEFT | B | A | B:e31 @ 7.35 | initial_in_ego_path=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['B:track_003'] |
| g49 | 0.30 | MOVING_END | B | - | B:e32 @ 7.45 |  |
| g50 | 0.30 | STOP_START | B | - | B:e33 @ 7.45 |  |
| g51 | 0.50 | TURN_LEFT_END | A | - | A:e25 @ 7.65 |  |
| g52 | 0.50 | MOVING_END | A | - | A:e26 @ 7.65 |  |
| g53 | 0.50 | STOP_START | A | - | A:e27 @ 7.65 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g07 --PRECEDES--> g11
    g07 --PRECEDES--> g12
    g07 --PRECEDES--> g13
    g07 --PRECEDES--> g14
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g08 --PRECEDES--> g13
    g08 --PRECEDES--> g14
    g09 --PRECEDES--> g15
    g10 --PRECEDES--> g15
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g38 --PRECEDES--> g44
    g38 --PRECEDES--> g45
    g38 --PRECEDES--> g46
    g38 --PRECEDES--> g47
    g39 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g39 --PRECEDES--> g45
    g39 --PRECEDES--> g46
    g39 --PRECEDES--> g47
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g40 --PRECEDES--> g45
    g40 --PRECEDES--> g46
    g40 --PRECEDES--> g47
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g41 --PRECEDES--> g46
    g41 --PRECEDES--> g47
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g44 --PRECEDES--> g48
    g45 --PRECEDES--> g48
    g46 --PRECEDES--> g48
    g47 --PRECEDES--> g48
    g48 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g11 --SAME_TRACK--> g13
    g11 --SAME_TRACK--> g17
    g30 --SAME_TRACK--> g31
    g30 --SAME_TRACK--> g34
    g30 --SAME_TRACK--> g39
    g30 --SAME_TRACK--> g43
    g12 --SAME_TRACK--> g14
    g12 --SAME_TRACK--> g20
    g12 --SAME_TRACK--> g27
    g12 --SAME_TRACK--> g35
    g12 --SAME_TRACK--> g37
    g12 --SAME_TRACK--> g42
    g12 --SAME_TRACK--> g40
    g12 --SAME_TRACK--> g41
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -7.15 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B) |
| -6.95 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -6.45 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -4.75 | THROTTLE_END(A); BRAKE_START(A) |
| -4.65 | THROTTLE_END(B); BRAKE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A) |
| -4.40 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -4.35 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -3.65 | TRACK_LOST(A,B) |
| -3.55 | MOVING_END(B); STOP_START(B) |
| -3.45 | CLOSING_END(B,A); MOVING_END(A); STOP_START(A) |
| -2.45 | BRAKE_END(B); THROTTLE_START(B) |
| -2.30 | BRAKE_END(A); THROTTLE_START(A) |
| -2.05 | CLOSING_START(B,A) |
| -2.00 | STOP_END(B); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -1.95 | STOP_END(A); MOVING_START(A) |
| -1.25 | CRITICAL_TTC_START(A,B) |
| -1.10 | CRITICAL_TTC_START(B,A) |
| -1.00 | TURN_LEFT_START(A) |
| -0.80 | EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A); TRACK_LOST(B,A) |
| +0.05 | CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.20 | TRACK_APPEARED_LEFT(B,A) |
| +0.30 | MOVING_END(B); STOP_START(B) |
| +0.50 | TURN_LEFT_END(A); MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (B): CRITICAL_TTC_START 5.90, COLLISION with B 7.15 (+1.25 s) [local times; t_global: critical_ttc_start -1.25, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 6.05, COLLISION with A 7.15 (+1.10 s); EGO_PATH_ENTRY 6.80 after critical TTC (+0.75 s) [local times; t_global: critical_ttc_start -1.10, ego_path_entry -0.35, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 6.70, COLLISION with A 7.15 (+0.45 s); EGO_PATH_ENTRY 6.35 before critical TTC (-0.35 s) [local times; t_global: critical_ttc_start -0.45, ego_path_entry -0.80, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -7.15 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02) | ego: not yet observed |
| -7.15 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -6.95 | A | g05 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e03) | ego: MOVING, THROTTLE |
| -6.45 | B | g06 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e03) | ego: MOVING, THROTTLE |
| -4.75 | A | g07 THROTTLE_END(A) (A:e04)<br>g08 BRAKE_START(A) (A:e05) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -4.65 | B | g09 THROTTLE_END(B) (B:e04)<br>g10 BRAKE_START(B) (B:e05)<br>g12 TRACK_APPEARED_RIGHT(B,A) (B:e06)<br>g14 CLOSING_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -4.65 | A | g11 TRACK_APPEARED_LEFT(A,B) (A:e06)<br>g13 CLOSING_START(A,B) (A:e07) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| -4.65 | A | g11 TRACK_APPEARED_LEFT(A,B) (A:e06)<br>g17 TRACK_LOST(A,B) (A:e09) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| -4.65 | B | g12 TRACK_APPEARED_RIGHT(B,A) (B:e06)<br>g27 CLOSING_START(B,A) (B:e14)<br>g35 CRITICAL_TTC_START(B,A) (B:e17)<br>g38 COLLISION(A,B) (B:e25)<br>g40 CRITICAL_TTC_END(B,A) (B:e26)<br>g41 CLOSING_END(B,A) (B:e27)<br>g42 TRACK_LOST(B,A) (B:e28) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -4.65 | B | g12 TRACK_APPEARED_RIGHT(B,A) (B:e06)<br>g27 CLOSING_START(B,A) (B:e14) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -4.65 | B | g12 TRACK_APPEARED_RIGHT(B,A) (B:e06)<br>g37 EGO_PATH_ENTRY(B,A) (B:e20)<br>g42 TRACK_LOST(B,A) (B:e28) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -4.65 | B | g14 CLOSING_START(B,A) (B:e07)<br>g20 CLOSING_END(B,A) (B:e11) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -4.40 | A | g15 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -4.35 | B | g16 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -3.55 | B | g18 MOVING_END(B) (B:e09)<br>g19 STOP_START(B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -3.45 | A | g21 MOVING_END(A) (A:e10)<br>g22 STOP_START(A) (A:e11) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -2.45 | B | g23 BRAKE_END(B) (B:e12)<br>g24 THROTTLE_START(B) (B:e13) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.30 | A | g25 BRAKE_END(A) (A:e12)<br>g26 THROTTLE_START(A) (A:e13) | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -2.05 | B | g27 CLOSING_START(B,A) (B:e14) | ego: STOP, THROTTLE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.00 | B | g28 STOP_END(B) (B:e15)<br>g29 MOVING_START(B) (B:e16) | ego: STOP, THROTTLE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -2.00 | A | g30 TRACK_APPEARED_LEFT(A,B) (A:e14)<br>g31 CLOSING_START(A,B) (A:e15) | ego: STOP, THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -2.00 | A | g31 CLOSING_START(A,B) (A:e15)<br>g43 CLOSING_END(A,B) (A:e22)<br>g44 THROTTLE_END(A) (A:e23)<br>g46 BRAKE_START(A) (A:e24) | ego: STOP, THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -1.95 | A | g32 STOP_END(A) (A:e16)<br>g33 MOVING_START(A) (A:e17) | ego: STOP, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -1.25 | A | g34 CRITICAL_TTC_START(A,B) (A:e18) | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -1.25 | A | g34 CRITICAL_TTC_START(A,B) (A:e18)<br>g38 COLLISION(A,B) (A:e20)<br>g39 CRITICAL_TTC_END(A,B) (A:e21) | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -1.10 | B | g35 CRITICAL_TTC_START(B,A) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.10 | B | g35 CRITICAL_TTC_START(B,A) (B:e17) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.00 | A | g36 TURN_LEFT_START(A) (A:e19) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -0.80 | B | g37 EGO_PATH_ENTRY(B,A) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -0.80 | B | g37 EGO_PATH_ENTRY(B,A) (B:e20) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | B | g45 THROTTLE_END(B) (B:e29)<br>g47 BRAKE_START(B) (B:e30) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path |
| +0.20 | B | g48 TRACK_APPEARED_LEFT(B,A) (B:e31) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path |
| +0.30 | B | g49 MOVING_END(B) (B:e32)<br>g50 STOP_START(B) (B:e33) | ego: MOVING, BRAKE<br>track_003: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path |
| +0.50 | A | g51 TURN_LEFT_END(A) (A:e25)<br>g52 MOVING_END(A) (A:e26)<br>g53 STOP_START(A) (A:e27) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |

## Plain-language reading

- 7.15 s before the reference collision, A started moving (already the case when first observed).
- 7.15 s before the reference collision, B started moving (already the case when first observed).
- 7.15 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.15 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.95 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 6.45 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 4.75 s before the reference collision, A released the accelerator.
- 4.75 s before the reference collision, A started braking.
- 4.65 s before the reference collision, B released the accelerator.
- 4.65 s before the reference collision, B started braking.
- 4.65 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 4.65 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.65 s before the reference collision, A observed B start closing in (already the case when first observed).
- 4.65 s before the reference collision, B observed A start closing in (already the case when first observed).
- 4.40 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 4.35 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 3.65 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 3.55 s before the reference collision, B stopped moving.
- 3.55 s before the reference collision, B came to a stop.
- 3.45 s before the reference collision, B observed A stop closing in.
- 3.45 s before the reference collision, A stopped moving.
- 3.45 s before the reference collision, A came to a stop.
- 2.45 s before the reference collision, B released the brake.
- 2.45 s before the reference collision, B pressed the accelerator.
- 2.30 s before the reference collision, A released the brake.
- 2.30 s before the reference collision, A pressed the accelerator.
- 2.05 s before the reference collision, B observed A start closing in.
- 2.00 s before the reference collision, B left its stop.
- 2.00 s before the reference collision, B started moving.
- 2.00 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 2.00 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.95 s before the reference collision, A left its stop.
- 1.95 s before the reference collision, A started moving.
- 1.25 s before the reference collision, A's time-to-contact with B became critical.
- 1.10 s before the reference collision, B's time-to-contact with A became critical.
- 1.00 s before the reference collision, A started turning left.
- 0.80 s before the reference collision, B observed A enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 7661, B: 7661 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, B observed A stop closing in.
- At the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B's radar started tracking A, which appeared on its left.
- 0.30 s after the reference collision, B stopped moving.
- 0.30 s after the reference collision, B came to a stop.
- 0.50 s after the reference collision, A stopped turning left.
- 0.50 s after the reference collision, A stopped moving.
- 0.50 s after the reference collision, A came to a stop.
