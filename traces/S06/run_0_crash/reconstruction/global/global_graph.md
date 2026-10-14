# Global graph - S06/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002, C:track_001, C:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002, C:track_003 |
| C | recorder | clock ALIGNED; observed by others as: A:track_001, B:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 4.10 | -4.10 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.10 | -4.10 | reported the reference collision collision_001 |
| C | ALIGNED | - | - | -4.15 | aligned through observed trajectories: the near surfaces of A:track_001, B:track_001, C:track_002 on A, C:track_003 on B lie where their lines of sight enter the body (pooled median 0.65 sigma) at this offset; offsets within 2.00 sigma span [-4.20, -4.00] s and nothing else fits |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.050 s, C - B = +0.050 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12137.11 vs 12137.11 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 4.00 s before the matched collision<br>lost 1.50 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 46.8 m -> 27.7 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 2.91 m/s for reference)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 51 samples; 100% within 3 sigma) at C's own velocity |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.05 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 0.4 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.65 m/s for reference)<br>clearance at the contact 0.43 m<br>the only track of A compatible with the contact |
| B:track_001 | C | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.4 m -> 10.7 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 7.61 m/s for reference)<br>clearance at the contact 10.71 m (beyond 3.50 m: confidence factor 0.06)<br>common frame: its returns lie on C's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 261 samples; 100% within 3 sigma) at C's own velocity |
| B:track_002 | A | ASSOCIATED | 0.90 | B and A both reported collision_001 (peak impulse 12137.11 vs 12137.11 N*s)<br>tracked for 2.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.0 m -> 0.5 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.70 m/s for reference)<br>clearance at the contact 0.49 m<br>the only track of B compatible with the contact |
| C:track_001 | A | ASSOCIATED | 1.00 | no matched collision of C names a partner<br>common frame: its returns lie on A's own footprint (median 0.01 m, 0.01 sigma of the relative uncertainty, over 5 samples; 100% within 3 sigma) at A's own velocity |
| C:track_002 | A | ASSOCIATED | 1.00 | no matched collision of C names a partner<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 73 samples; 100% within 3 sigma) at A's own velocity |
| C:track_003 | B | ASSOCIATED | 1.00 | no matched collision of C names a partner<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 41 samples; 100% within 3 sigma) at B's own velocity |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.15 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.15 | THROTTLE_START | C | - | C:e02 @ 0.00 | active_at_first_observation=True |
| g03 | -4.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -4.10 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g05 | -4.10 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g06 | -4.10 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g07 | -4.05 | TRACK_APPEARED_LEFT | C | A | C:e03 @ 0.10, C:e05 @ 0.30 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g08 | -4.05 | CLOSING_START | C | A | C:e04 @ 0.10 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g09 | -4.00 | TRACK_APPEARED_FRONT | A | C | A:e03 @ 0.10, A:e08 @ 2.60 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g10 | -4.00 | CLOSING_START | A | C | A:e04 @ 0.10 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g11 | -3.85 | TRACK_LOST | C | A | C:e05 @ 0.30 | source_track=track_001; aggregation=entity_state_union; source_tracks=['C:track_001'] |
| g12 | -3.75 | TRACK_APPEARED_LEFT | C | A | C:e06 @ 0.40, C:e16 @ 4.60 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g13 | -3.75 | CLOSING_START | C | A | C:e07 @ 0.40 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g14 | -2.05 | TRACK_APPEARED_LEFT | C | B | C:e08 @ 2.10 | initial_in_ego_path=False; source_track=track_003; aggregation=entity_state_union; source_tracks=['C:track_003'] |
| g15 | -2.05 | TRACK_APPEARED_RIGHT | A | B | A:e05 @ 2.05 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g16 | -2.05 | CLOSING_START | A | B | A:e06 @ 2.05, A:e11 @ 4.10 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g17 | -2.05 | CLOSING_START | C | B | C:e09 @ 2.10, C:e14 @ 4.60 | active_at_first_observation=True; source_track=track_003; aggregation=entity_state_union; source_tracks=['C:track_003'] |
| g18 | -2.00 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 2.10 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g19 | -2.00 | TRACK_APPEARED_RIGHT | B | C | B:e04 @ 2.10 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g20 | -2.00 | CLOSING_START | B | A | B:e06 @ 2.10, B:e10 @ 4.10 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g21 | -2.00 | CLOSING_START | B | C | B:e05 @ 2.10, B:e15 @ 4.60 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g22 | -1.80 | THROTTLE_END | C | - | C:e10 @ 2.35 |  |
| g23 | -1.80 | BRAKE_START | C | - | C:e11 @ 2.35 |  |
| g24 | -1.55 | CRITICAL_TTC_START | A | B | A:e07 @ 2.55, A:e10 @ 4.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g25 | -1.50 | CRITICAL_TTC_START | B | A | B:e07 @ 2.60, B:e09 @ 4.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g26 | -1.50 | TRACK_LOST | A | C | A:e08 @ 2.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g27 | -1.25 | MOVING_END | C | - | C:e12 @ 2.90 |  |
| g28 | -1.25 | STOP_START | C | - | C:e13 @ 2.90 |  |
| g29 | 0.00 | COLLISION | - | A, B | A:e09 @ 4.10, B:e08 @ 4.10 | matched_event=collision_001; reference_event=True; peak_impulse=A 12137.11, B 12137.11 |
| g30 | 0.00 | CRITICAL_TTC_END | A | B | A:e10 @ 4.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g31 | 0.00 | CRITICAL_TTC_END | B | A | B:e09 @ 4.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g32 | 0.00 | CLOSING_END | A | B | A:e11 @ 4.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g33 | 0.00 | CLOSING_END | B | A | B:e10 @ 4.10 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g34 | 0.00 | TURN_LEFT_START | A | - | A:e12 @ 4.10 |  |
| g35 | 0.00 | TURN_RIGHT_START | B | - | B:e11 @ 4.10 |  |
| g36 | 0.05 | THROTTLE_END | A | - | A:e13 @ 4.15 |  |
| g37 | 0.05 | THROTTLE_END | B | - | B:e12 @ 4.15 |  |
| g38 | 0.05 | BRAKE_START | A | - | A:e14 @ 4.15 |  |
| g39 | 0.05 | BRAKE_START | B | - | B:e13 @ 4.15 |  |
| g40 | 0.15 | CLOSING_START | A | B | A:e15 @ 4.25, A:e19 @ 4.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g41 | 0.15 | CLOSING_START | B | A | B:e14 @ 4.25, B:e19 @ 4.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g42 | 0.45 | CLOSING_END | C | B | C:e14 @ 4.60 | source_track=track_003; aggregation=entity_state_union; source_tracks=['C:track_003'] |
| g43 | 0.45 | EGO_PATH_ENTRY | C | B | C:e15 @ 4.60 | geometry=estimated_body; source_track=track_003; aggregation=entity_state_union; source_tracks=['C:track_003'] |
| g44 | 0.45 | TRACK_LOST | C | A | C:e16 @ 4.60 | source_track=track_002; aggregation=entity_state_union; source_tracks=['C:track_002'] |
| g45 | 0.50 | CLOSING_END | B | C | B:e15 @ 4.60 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g46 | 0.50 | TURN_RIGHT_END | B | - | B:e16 @ 4.60 |  |
| g47 | 0.50 | MOVING_END | B | - | B:e17 @ 4.60 |  |
| g48 | 0.50 | STOP_START | B | - | B:e18 @ 4.60 |  |
| g49 | 0.60 | TURN_LEFT_END | A | - | A:e16 @ 4.70 |  |
| g50 | 0.65 | MOVING_END | A | - | A:e17 @ 4.75 |  |
| g51 | 0.65 | STOP_START | A | - | A:e18 @ 4.75 |  |
| g52 | 0.70 | CLOSING_END | A | B | A:e19 @ 4.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |
| g53 | 0.70 | CLOSING_END | B | A | B:e19 @ 4.80 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g54 | 0.70 | EGO_PATH_ENTRY | B | A | B:e20 @ 4.80 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g55 | 0.85 | EGO_PATH_ENTRY | A | B | A:e20 @ 4.95 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['A:track_002'] |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g01 --PRECEDES--> g05
    g01 --PRECEDES--> g06
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g02 --PRECEDES--> g05
    g02 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g03 --PRECEDES--> g08
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g12 --PRECEDES--> g17
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g14 --PRECEDES--> g19
    g14 --PRECEDES--> g20
    g14 --PRECEDES--> g21
    g15 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g27 --PRECEDES--> g35
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g28 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g29 --PRECEDES--> g36
    g29 --PRECEDES--> g37
    g29 --PRECEDES--> g38
    g29 --PRECEDES--> g39
    g30 --PRECEDES--> g36
    g30 --PRECEDES--> g37
    g30 --PRECEDES--> g38
    g30 --PRECEDES--> g39
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g31 --PRECEDES--> g38
    g31 --PRECEDES--> g39
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g32 --PRECEDES--> g38
    g32 --PRECEDES--> g39
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g33 --PRECEDES--> g39
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
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
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g52 --PRECEDES--> g55
    g53 --PRECEDES--> g55
    g54 --PRECEDES--> g55
    g09 --SAME_TRACK--> g10
    g15 --SAME_TRACK--> g16
    g15 --SAME_TRACK--> g24
    g09 --SAME_TRACK--> g26
    g15 --SAME_TRACK--> g30
    g15 --SAME_TRACK--> g32
    g15 --SAME_TRACK--> g40
    g15 --SAME_TRACK--> g52
    g15 --SAME_TRACK--> g55
    g19 --SAME_TRACK--> g21
    g18 --SAME_TRACK--> g20
    g18 --SAME_TRACK--> g25
    g18 --SAME_TRACK--> g31
    g18 --SAME_TRACK--> g33
    g18 --SAME_TRACK--> g41
    g19 --SAME_TRACK--> g45
    g18 --SAME_TRACK--> g53
    g18 --SAME_TRACK--> g54
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g11
    g12 --SAME_TRACK--> g13
    g14 --SAME_TRACK--> g17
    g14 --SAME_TRACK--> g42
    g14 --SAME_TRACK--> g43
    g12 --SAME_TRACK--> g44
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.15 | MOVING_START(C); THROTTLE_START(C) |
| -4.10 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B) |
| -4.05 | TRACK_APPEARED_LEFT(C,A); CLOSING_START(C,A) |
| -4.00 | TRACK_APPEARED_FRONT(A,C); CLOSING_START(A,C) |
| -3.85 | TRACK_LOST(C,A) |
| -3.75 | TRACK_APPEARED_LEFT(C,A); CLOSING_START(C,A) |
| -2.05 | TRACK_APPEARED_LEFT(C,B); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(C,B) |
| -2.00 | TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(B,C); CLOSING_START(B,A); CLOSING_START(B,C) |
| -1.80 | THROTTLE_END(C); BRAKE_START(C) |
| -1.55 | CRITICAL_TTC_START(A,B) |
| -1.50 | CRITICAL_TTC_START(B,A); TRACK_LOST(A,C) |
| -1.25 | MOVING_END(C); STOP_START(C) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A); TURN_LEFT_START(A); TURN_RIGHT_START(B) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.15 | CLOSING_START(A,B); CLOSING_START(B,A) |
| +0.45 | CLOSING_END(C,B); EGO_PATH_ENTRY(C,B); TRACK_LOST(C,A) |
| +0.50 | CLOSING_END(B,C); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B) |
| +0.60 | TURN_LEFT_END(A) |
| +0.65 | MOVING_END(A); STOP_START(A) |
| +0.70 | CLOSING_END(A,B); CLOSING_END(B,A); EGO_PATH_ENTRY(B,A) |
| +0.85 | EGO_PATH_ENTRY(A,B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (B): CRITICAL_TTC_START 2.55, COLLISION with B 4.10 (+1.55 s); EGO_PATH_ENTRY 4.95 after critical TTC (+2.40 s) [local times; t_global: critical_ttc_start -1.55, ego_path_entry +0.85, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.60, COLLISION with A 4.10 (+1.50 s); EGO_PATH_ENTRY 4.80 after critical TTC (+2.20 s) [local times; t_global: critical_ttc_start -1.50, ego_path_entry +0.70, collision +0.00]
- C's track_003 (B): EGO_PATH_ENTRY 4.60, no critical TTC [local times; t_global: ego_path_entry +0.45]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.15 | C | g01 MOVING_START(C) (C:e01)<br>g02 THROTTLE_START(C) (C:e02) | ego: not yet observed |
| -4.10 | A | g03 MOVING_START(A) (A:e01)<br>g05 THROTTLE_START(A) (A:e02) | ego: not yet observed |
| -4.10 | B | g04 MOVING_START(B) (B:e01)<br>g06 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -4.05 | C | g07 TRACK_APPEARED_LEFT(C,A) (C:e03)<br>g08 CLOSING_START(C,A) (C:e04) | ego: MOVING, THROTTLE |
| -4.05 | C | g07 TRACK_APPEARED_LEFT(C,A) (C:e03)<br>g11 TRACK_LOST(C,A) (C:e05) | ego: MOVING, THROTTLE |
| -4.00 | A | g09 TRACK_APPEARED_FRONT(A,C) (A:e03)<br>g10 CLOSING_START(A,C) (A:e04) | ego: MOVING, THROTTLE |
| -4.00 | A | g09 TRACK_APPEARED_FRONT(A,C) (A:e03)<br>g26 TRACK_LOST(A,C) (A:e08) | ego: MOVING, THROTTLE |
| -3.75 | C | g12 TRACK_APPEARED_LEFT(C,A) (C:e06)<br>g13 CLOSING_START(C,A) (C:e07) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| -3.75 | C | g12 TRACK_APPEARED_LEFT(C,A) (C:e06)<br>g17 CLOSING_START(C,B) (C:e09)<br>g42 CLOSING_END(C,B) (C:e14)<br>g43 EGO_PATH_ENTRY(C,B) (C:e15)<br>g44 TRACK_LOST(C,A) (C:e16) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| -2.05 | C | g14 TRACK_APPEARED_LEFT(C,B) (C:e08)<br>g17 CLOSING_START(C,B) (C:e09) | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -2.05 | A | g15 TRACK_APPEARED_RIGHT(A,B) (A:e05)<br>g16 CLOSING_START(A,B) (A:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.05 | A | g16 CLOSING_START(A,B) (A:e06)<br>g24 CRITICAL_TTC_START(A,B) (A:e07)<br>g29 COLLISION(A,B) (A:e09)<br>g30 CRITICAL_TTC_END(A,B) (A:e10)<br>g32 CLOSING_END(A,B) (A:e11)<br>g34 TURN_LEFT_START(A) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -2.00 | B | g18 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g19 TRACK_APPEARED_RIGHT(B,C) (B:e04)<br>g20 CLOSING_START(B,A) (B:e06)<br>g21 CLOSING_START(B,C) (B:e05) | ego: MOVING, THROTTLE |
| -2.00 | B | g20 CLOSING_START(B,A) (B:e06)<br>g25 CRITICAL_TTC_START(B,A) (B:e07)<br>g29 COLLISION(A,B) (B:e08)<br>g31 CRITICAL_TTC_END(B,A) (B:e09)<br>g33 CLOSING_END(B,A) (B:e10)<br>g35 TURN_RIGHT_START(B) (B:e11) | ego: MOVING, THROTTLE |
| -2.00 | B | g21 CLOSING_START(B,C) (B:e05)<br>g45 CLOSING_END(B,C) (B:e15)<br>g46 TURN_RIGHT_END(B) (B:e16)<br>g47 MOVING_END(B) (B:e17)<br>g48 STOP_START(B) (B:e18) | ego: MOVING, THROTTLE |
| -1.80 | C | g22 THROTTLE_END(C) (C:e10)<br>g23 BRAKE_START(C) (C:e11) | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track_003: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001 |
| -1.55 | A | g24 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.50 | B | g25 CRITICAL_TTC_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? |
| -1.25 | C | g27 MOVING_END(C) (C:e12)<br>g28 STOP_START(C) (C:e13) | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.05 | A | g36 THROTTLE_END(A) (A:e13)<br>g38 BRAKE_START(A) (A:e14) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.05 | B | g37 THROTTLE_END(B) (B:e12)<br>g39 BRAKE_START(B) (B:e13) | ego: MOVING, THROTTLE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: no active state |
| +0.15 | A | g40 CLOSING_START(A,B) (A:e15) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.15 | A | g40 CLOSING_START(A,B) (A:e15)<br>g52 CLOSING_END(A,B) (A:e19) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.15 | B | g41 CLOSING_START(B,A) (B:e14) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: no active state |
| +0.15 | B | g41 CLOSING_START(B,A) (B:e14)<br>g53 CLOSING_END(B,A) (B:e19)<br>g54 EGO_PATH_ENTRY(B,A) (B:e20) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: no active state |
| +0.60 | A | g49 TURN_LEFT_END(A) (A:e16) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.65 | A | g50 MOVING_END(A) (A:e17)<br>g51 STOP_START(A) (A:e18) | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.85 | A | g55 EGO_PATH_ENTRY(A,B) (A:e20) | ego: STOP, BRAKE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 4.15 s before the reference collision, C started moving (already the case when first observed).
- 4.15 s before the reference collision, C pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, A started moving (already the case when first observed).
- 4.10 s before the reference collision, B started moving (already the case when first observed).
- 4.10 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 4.10 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.05 s before the reference collision, C's radar started tracking A, which appeared on its left.
- 4.05 s before the reference collision, C observed A start closing in (already the case when first observed).
- 4.00 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 4.00 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.85 s before the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 3.75 s before the reference collision, C's radar started tracking A, which appeared on its left.
- 3.75 s before the reference collision, C observed A start closing in (already the case when first observed).
- 2.05 s before the reference collision, C's radar started tracking B, which appeared on its left.
- 2.05 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 2.05 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.05 s before the reference collision, C observed B start closing in (already the case when first observed).
- 2.00 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.00 s before the reference collision, B's radar started tracking C, which appeared on its right.
- 2.00 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.00 s before the reference collision, B observed C start closing in (already the case when first observed).
- 1.80 s before the reference collision, C released the accelerator.
- 1.80 s before the reference collision, C started braking.
- 1.55 s before the reference collision, A's time-to-contact with B became critical.
- 1.50 s before the reference collision, B's time-to-contact with A became critical.
- 1.50 s before the reference collision, A's radar lost C (its states are UNKNOWN from then on, not ended).
- 1.25 s before the reference collision, C stopped moving.
- 1.25 s before the reference collision, C came to a stop.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12137, B: 12137 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- At the reference collision, A started turning left.
- At the reference collision, B started turning right.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.15 s after the reference collision, A observed B start closing in.
- 0.15 s after the reference collision, B observed A start closing in.
- 0.45 s after the reference collision, C observed B stop closing in.
- 0.45 s after the reference collision, C observed B enter its forward path corridor.
- 0.45 s after the reference collision, C's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.50 s after the reference collision, B observed C stop closing in.
- 0.50 s after the reference collision, B stopped turning right.
- 0.50 s after the reference collision, B stopped moving.
- 0.50 s after the reference collision, B came to a stop.
- 0.60 s after the reference collision, A stopped turning left.
- 0.65 s after the reference collision, A stopped moving.
- 0.65 s after the reference collision, A came to a stop.
- 0.70 s after the reference collision, A observed B stop closing in.
- 0.70 s after the reference collision, B observed A stop closing in.
- 0.70 s after the reference collision, B observed A enter its forward path corridor.
- 0.85 s after the reference collision, A observed B enter its forward path corridor.
