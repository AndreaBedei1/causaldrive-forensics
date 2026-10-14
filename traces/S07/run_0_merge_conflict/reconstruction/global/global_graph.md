# Global graph - S07/run_0_merge_conflict

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001, B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 10.25 | -10.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e11 | 10.25 | -10.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1904.84 vs 1904.84 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.93 | A and B both reported collision_001 (peak impulse 1904.84 vs 1904.84 N*s)<br>tracked for 6.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.9 m -> 1.3 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.58 m/s for reference)<br>clearance at the contact 1.25 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 1904.84 vs 1904.84 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 7.35 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 89.9 m -> 84.6 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma of the relative uncertainty, over 8 samples; 100% within 3 sigma) at A's own velocity |
| B:track_002 | A | ASSOCIATED | 0.92 | B and A both reported collision_001 (peak impulse 1904.84 vs 1904.84 N*s)<br>tracked for 6.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.8 m -> 0.4 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.61 m/s for reference)<br>clearance at the contact 0.36 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -10.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -10.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -10.25 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -10.25 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -10.25 | TURN_LEFT_START | A | - | A:e03 @ 0.00 | active_at_first_observation=True |
| g06 | -7.70 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 2.55, B:e05 @ 2.90 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g07 | -7.70 | CLOSING_START | B | A | B:e04 @ 2.55 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g08 | -7.35 | TRACK_LOST | B | A | B:e05 @ 2.90 | source_track=track_001; aggregation=entity_state_union; source_tracks=['B:track_001'] |
| g09 | -6.95 | TRACK_APPEARED_LEFT | A | B | A:e04 @ 3.30 | initial_in_ego_path=False; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g10 | -6.95 | TRACK_APPEARED_LEFT | B | A | B:e06 @ 3.30 | initial_in_ego_path=False; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g11 | -6.95 | CLOSING_START | A | B | A:e05 @ 3.30, A:e09 @ 10.25 | active_at_first_observation=True; source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g12 | -6.95 | CLOSING_START | B | A | B:e07 @ 3.30, B:e13 @ 10.25 | active_at_first_observation=True; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g13 | -3.55 | CRITICAL_TTC_START | B | A | B:e08 @ 6.70, B:e12 @ 10.25 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g14 | -3.35 | CRITICAL_TTC_START | A | B | A:e06 @ 6.90, A:e08 @ 10.25 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g15 | -2.05 | TURN_RIGHT_START | B | - | B:e09 @ 8.20 |  |
| g16 | -0.30 | TURN_RIGHT_END | B | - | B:e10 @ 9.95 |  |
| g17 | 0.00 | COLLISION | - | A, B | A:e07 @ 10.25, B:e11 @ 10.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 1904.84, B 1904.84 |
| g18 | 0.00 | CRITICAL_TTC_END | A | B | A:e08 @ 10.25 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g19 | 0.00 | CRITICAL_TTC_END | B | A | B:e12 @ 10.25 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g20 | 0.00 | CLOSING_END | A | B | A:e09 @ 10.25 | source_track=track_001; aggregation=entity_state_union; source_tracks=['A:track_001'] |
| g21 | 0.00 | CLOSING_END | B | A | B:e13 @ 10.25 | source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g22 | 0.05 | THROTTLE_END | A | - | A:e10 @ 10.30 |  |
| g23 | 0.05 | THROTTLE_END | B | - | B:e14 @ 10.30 |  |
| g24 | 0.05 | BRAKE_START | A | - | A:e11 @ 10.30 |  |
| g25 | 0.05 | BRAKE_START | B | - | B:e15 @ 10.30 |  |
| g26 | 0.20 | EGO_PATH_ENTRY | B | A | B:e16 @ 10.45 | geometry=estimated_body; source_track=track_002; aggregation=entity_state_union; source_tracks=['B:track_002'] |
| g27 | 0.30 | TURN_LEFT_END | A | - | A:e12 @ 10.55 |  |
| g28 | 0.75 | MOVING_END | B | - | B:e17 @ 11.00 |  |
| g29 | 0.75 | STOP_START | B | - | B:e18 @ 11.00 |  |
| g30 | 0.80 | MOVING_END | A | - | A:e13 @ 11.05 |  |
| g31 | 0.80 | STOP_START | A | - | A:e14 @ 11.05 |  |

## Edges

```
    g01 --PRECEDES--> g06
    g01 --PRECEDES--> g07
    g02 --PRECEDES--> g06
    g02 --PRECEDES--> g07
    g03 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g17 --PRECEDES--> g25
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g18 --PRECEDES--> g24
    g18 --PRECEDES--> g25
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g19 --PRECEDES--> g25
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g09 --SAME_TRACK--> g11
    g09 --SAME_TRACK--> g14
    g09 --SAME_TRACK--> g18
    g09 --SAME_TRACK--> g20
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g08
    g10 --SAME_TRACK--> g12
    g10 --SAME_TRACK--> g13
    g10 --SAME_TRACK--> g19
    g10 --SAME_TRACK--> g21
    g10 --SAME_TRACK--> g26
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -10.25 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TURN_LEFT_START(A) |
| -7.70 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -7.35 | TRACK_LOST(B,A) |
| -6.95 | TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(B,A); CLOSING_START(A,B); CLOSING_START(B,A) |
| -3.55 | CRITICAL_TTC_START(B,A) |
| -3.35 | CRITICAL_TTC_START(A,B) |
| -2.05 | TURN_RIGHT_START(B) |
| -0.30 | TURN_RIGHT_END(B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.20 | EGO_PATH_ENTRY(B,A) |
| +0.30 | TURN_LEFT_END(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |
| +0.80 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 6.90, COLLISION with B 10.25 (+3.35 s) [local times; t_global: critical_ttc_start -3.35, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 6.70, COLLISION with A 10.25 (+3.55 s); EGO_PATH_ENTRY 10.45 after critical TTC (+3.75 s) [local times; t_global: critical_ttc_start -3.55, ego_path_entry +0.20, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -10.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TURN_LEFT_START(A) (A:e03) | ego: not yet observed |
| -10.25 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -7.70 | B | g06 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g07 CLOSING_START(B,A) (B:e04) | ego: MOVING, THROTTLE |
| -7.70 | B | g06 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g08 TRACK_LOST(B,A) (B:e05) | ego: MOVING, THROTTLE |
| -6.95 | A | g09 TRACK_APPEARED_LEFT(A,B) (A:e04)<br>g11 CLOSING_START(A,B) (A:e05) | ego: MOVING, THROTTLE, TURN_LEFT |
| -6.95 | B | g10 TRACK_APPEARED_LEFT(B,A) (B:e06)<br>g12 CLOSING_START(B,A) (B:e07) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| -6.95 | A | g11 CLOSING_START(A,B) (A:e05)<br>g14 CRITICAL_TTC_START(A,B) (A:e06)<br>g17 COLLISION(A,B) (A:e07)<br>g18 CRITICAL_TTC_END(A,B) (A:e08)<br>g20 CLOSING_END(A,B) (A:e09) | ego: MOVING, THROTTLE, TURN_LEFT |
| -6.95 | B | g12 CLOSING_START(B,A) (B:e07)<br>g13 CRITICAL_TTC_START(B,A) (B:e08)<br>g17 COLLISION(A,B) (B:e11)<br>g19 CRITICAL_TTC_END(B,A) (B:e12)<br>g21 CLOSING_END(B,A) (B:e13) | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 |
| -3.55 | B | g13 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -3.35 | A | g14 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING |
| -2.05 | B | g15 TURN_RIGHT_START(B) (B:e09) | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 |
| -0.30 | B | g16 TURN_RIGHT_END(B) (B:e10) | ego: MOVING, THROTTLE, TURN_RIGHT<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 |
| +0.05 | A | g22 THROTTLE_END(A) (A:e10)<br>g24 BRAKE_START(A) (A:e11) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: no active state |
| +0.05 | B | g23 THROTTLE_END(B) (B:e14)<br>g25 BRAKE_START(B) (B:e15) | ego: MOVING, THROTTLE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.20 | B | g26 EGO_PATH_ENTRY(B,A) (B:e16) | ego: MOVING, BRAKE<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 |
| +0.30 | A | g27 TURN_LEFT_END(A) (A:e12) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state |
| +0.75 | B | g28 MOVING_END(B) (B:e17)<br>g29 STOP_START(B) (B:e18) | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.80 | A | g30 MOVING_END(A) (A:e13)<br>g31 STOP_START(A) (A:e14) | ego: MOVING, BRAKE<br>track_001: no active state |

## Plain-language reading

- 10.25 s before the reference collision, A started moving (already the case when first observed).
- 10.25 s before the reference collision, B started moving (already the case when first observed).
- 10.25 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 10.25 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 10.25 s before the reference collision, A started turning left (already the case when first observed).
- 7.70 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 7.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 7.35 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 6.95 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.95 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 6.95 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.95 s before the reference collision, B observed A start closing in (already the case when first observed).
- 3.55 s before the reference collision, B's time-to-contact with A became critical.
- 3.35 s before the reference collision, A's time-to-contact with B became critical.
- 2.05 s before the reference collision, B started turning right.
- 0.30 s before the reference collision, B stopped turning right.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1905, B: 1905 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B observed A enter its forward path corridor.
- 0.30 s after the reference collision, A stopped turning left.
- 0.75 s after the reference collision, B stopped moving.
- 0.75 s after the reference collision, B came to a stop.
- 0.80 s after the reference collision, A stopped moving.
- 0.80 s after the reference collision, A came to a stop.
