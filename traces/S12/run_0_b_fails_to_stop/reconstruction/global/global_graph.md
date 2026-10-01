# Global graph - S12/run_0_b_fails_to_stop

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |
| B:track_004 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e15 | 9.70 | -9.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 9.70 | -9.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 7339.57 vs 7339.57 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.96 | A and B both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 6.55 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 10.9 m -> 1.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.41 m/s over 3.0 s<br>range at the contact 1.83 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.92 | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 1.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 10.1 m -> 1.0 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.60 m/s over 1.5 s<br>range at the contact 1.05 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 15.21 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -9.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -9.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -9.00 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.70 | relevant_to_ego_path=True |
| g04 | -7.75 | BRAKE_START | B | - | B:e02 @ 1.95 |  |
| g05 | -7.45 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.25 |  |
| g06 | -7.05 | BRAKE_END | B | - | B:e03 @ 2.65 |  |
| g07 | -7.05 | BRAKE_START | A | - | A:e04 @ 2.65 |  |
| g08 | -6.55 | TRACK_APPEARED_LEFT | A | B | A:e05 @ 3.15 |  |
| g09 | -6.55 | CLOSING_START | A | B | A:e06 @ 3.15 | active_at_first_observation=True |
| g10 | -6.30 | MOVING_END | A | - | A:e07 @ 3.40 |  |
| g11 | -6.30 | STOP_START | A | - | A:e08 @ 3.40 |  |
| g12 | -6.20 | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e04 @ 3.50 | relevant_to_ego_path=True |
| g13 | -4.40 | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e05 @ 5.30 |  |
| g14 | -1.95 | BRAKE_END | A | - | A:e09 @ 7.75 |  |
| g15 | -1.60 | STOP_END | A | - | A:e10 @ 8.10 |  |
| g16 | -1.60 | MOVING_START | A | - | A:e11 @ 8.10 |  |
| g17 | -1.55 | TRACK_APPEARED_RIGHT | B | A | B:e06 @ 8.15 |  |
| g18 | -1.55 | CLOSING_START | B | A | B:e07 @ 8.15 | active_at_first_observation=True |
| g19 | -1.05 | CRITICAL_TTC_START | A | B | A:e12 @ 8.65 |  |
| g20 | -1.05 | CRITICAL_TTC_START | B | A | B:e08 @ 8.65 |  |
| g21 | -0.60 | TURN_LEFT_START | A | - | A:e13 @ 9.10 |  |
| g22 | -0.10 | EGO_PATH_ENTRY | B | A | B:e09 @ 9.60 |  |
| g23 | -0.05 | TRACK_LOST | A | B | A:e14 @ 9.65 |  |
| g24 | 0.00 | COLLISION | - | A, B | A:e15 @ 9.70, B:e10 @ 9.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 7339.57, B 7339.57 |
| g25 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e11 @ 9.70 |  |
| g26 | 0.00 | CLOSING_START | B | B:track_002 | B:e12 @ 9.70 | active_at_first_observation=True |
| g27 | 0.05 | BRAKE_START | A | - | A:e16 @ 9.75 |  |
| g28 | 0.05 | BRAKE_START | B | - | B:e13 @ 9.75 |  |
| g29 | 0.05 | TRACK_APPEARED_LEFT | B | B:track_003 | B:e14 @ 9.75 |  |
| g30 | 0.05 | TRACK_APPEARED_LEFT | B | B:track_004 | B:e15 @ 9.75 |  |
| g31 | 0.05 | CLOSING_START | B | B:track_003 | B:e16 @ 9.75 | active_at_first_observation=True |
| g32 | 0.05 | CLOSING_START | B | B:track_004 | B:e17 @ 9.75 | active_at_first_observation=True |
| g33 | 0.10 | TURN_LEFT_END | A | - | A:e17 @ 9.80 |  |
| g34 | 0.15 | CRITICAL_TTC_END | B | A | B:e18 @ 9.85 |  |
| g35 | 0.25 | CLOSING_END | B | A | B:e19 @ 9.95 |  |
| g36 | 0.35 | MOVING_END | B | - | B:e20 @ 10.05 |  |
| g37 | 0.35 | STOP_START | B | - | B:e21 @ 10.05 |  |
| g38 | 0.40 | CLOSING_END | B | B:track_002 | B:e22 @ 10.10 |  |
| g39 | 0.40 | CLOSING_END | B | B:track_004 | B:e23 @ 10.10 |  |
| g40 | 0.50 | MOVING_END | A | - | A:e18 @ 10.20 |  |
| g41 | 0.50 | STOP_START | A | - | A:e19 @ 10.20 |  |
| g42 | 0.50 | TRACK_LOST | B | B:track_004 | B:e24 @ 10.20 |  |
| g43 | 0.55 | CLOSING_END | B | B:track_003 | B:e25 @ 10.25 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g24 --PRECEDES--> g31
    g24 --PRECEDES--> g32
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g25 --PRECEDES--> g32
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g43
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g19
    g08 --SAME_TRACK--> g23
    g17 --SAME_TRACK--> g18
    g17 --SAME_TRACK--> g20
    g17 --SAME_TRACK--> g22
    g25 --SAME_TRACK--> g26
    g29 --SAME_TRACK--> g31
    g30 --SAME_TRACK--> g32
    g17 --SAME_TRACK--> g34
    g17 --SAME_TRACK--> g35
    g25 --SAME_TRACK--> g38
    g30 --SAME_TRACK--> g39
    g30 --SAME_TRACK--> g42
    g29 --SAME_TRACK--> g43
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -9.70 | MOVING_START(A); MOVING_START(B) |
| -9.00 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -7.75 | BRAKE_START(B) |
| -7.45 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -7.05 | BRAKE_END(B); BRAKE_START(A) |
| -6.55 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -6.30 | MOVING_END(A); STOP_START(A) |
| -6.20 | STOP_SIGN_DETECTED_START(B,B:sign-1) |
| -4.40 | STOP_SIGN_DETECTED_END(B,B:sign-1) |
| -1.95 | BRAKE_END(A) |
| -1.60 | STOP_END(A); MOVING_START(A) |
| -1.55 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -1.05 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -0.60 | TURN_LEFT_START(A) |
| -0.10 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); TRACK_APPEARED_LEFT(B,B:track_002); CLOSING_START(B,B:track_002) |
| +0.05 | BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004) |
| +0.10 | TURN_LEFT_END(A) |
| +0.15 | CRITICAL_TTC_END(B,A) |
| +0.25 | CLOSING_END(B,A) |
| +0.35 | MOVING_END(B); STOP_START(B) |
| +0.40 | CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_004) |
| +0.50 | MOVING_END(A); STOP_START(A); TRACK_LOST(B,B:track_004) |
| +0.55 | CLOSING_END(B,B:track_003) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 8.65, COLLISION with B 9.70 (+1.05 s) [local times; t_global: critical_ttc_start -1.05, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 8.65, COLLISION with A 9.70 (+1.05 s); EGO_PATH_ENTRY 9.60 after critical TTC (+0.95 s) [local times; t_global: critical_ttc_start -1.05, ego_path_entry -0.10, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -9.70 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -9.70 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -9.00 | A | g03 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| -7.75 | B | g04 BRAKE_START(B) (B:e02) | ego: MOVING |
| -7.45 | A | g05 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -7.05 | B | g06 BRAKE_END(B) (B:e03) | ego: MOVING, BRAKE |
| -7.05 | A | g07 BRAKE_START(A) (A:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -6.55 | A | g08 TRACK_APPEARED_LEFT(A,B) (A:e05)<br>g09 CLOSING_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| -6.30 | A | g10 MOVING_END(A) (A:e07)<br>g11 STOP_START(A) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.20 | B | g12 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e04) | ego: MOVING |
| -4.40 | B | g13 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e05) | ego: MOVING<br>sign-1: STOP sign known, relevant to the path |
| -1.95 | A | g14 BRAKE_END(A) (A:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.60 | A | g15 STOP_END(A) (A:e10)<br>g16 MOVING_START(A) (A:e11) | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.55 | B | g17 TRACK_APPEARED_RIGHT(B,A) (B:e06)<br>g18 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>sign-1: STOP sign known, relevant to the path |
| -1.05 | A | g19 CRITICAL_TTC_START(A,B) (A:e12) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.05 | B | g20 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| -0.60 | A | g21 TURN_LEFT_START(A) (A:e13) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.10 | B | g22 EGO_PATH_ENTRY(B,A) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known, relevant to the path |
| -0.05 | A | g23 TRACK_LOST(A,B) (A:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | A | g24 COLLISION(A,B) (A:e15) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | B | g24 COLLISION(A,B) (B:e10)<br>g25 TRACK_APPEARED_LEFT(B,B:track_002) (B:e11)<br>g26 CLOSING_START(B,B:track_002) (B:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known, relevant to the path |
| +0.05 | A | g27 BRAKE_START(A) (A:e16) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | B | g28 BRAKE_START(B) (B:e13)<br>g29 TRACK_APPEARED_LEFT(B,B:track_003) (B:e14)<br>g30 TRACK_APPEARED_LEFT(B,B:track_004) (B:e15)<br>g31 CLOSING_START(B,B:track_003) (B:e16)<br>g32 CLOSING_START(B,B:track_004) (B:e17) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| +0.10 | A | g33 TURN_LEFT_END(A) (A:e17) | ego: MOVING, BRAKE, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.15 | B | g34 CRITICAL_TTC_END(B,A) (B:e18) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| +0.25 | B | g35 CLOSING_END(B,A) (B:e19) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| +0.35 | B | g36 MOVING_END(B) (B:e20)<br>g37 STOP_START(B) (B:e21) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| +0.40 | B | g38 CLOSING_END(B,B:track_002) (B:e22)<br>g39 CLOSING_END(B,B:track_004) (B:e23) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path |
| +0.50 | A | g40 MOVING_END(A) (A:e18)<br>g41 STOP_START(A) (A:e19) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.50 | B | g42 TRACK_LOST(B,B:track_004) (B:e24) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>sign-1: STOP sign known, relevant to the path |
| +0.55 | B | g43 CLOSING_END(B,B:track_003) (B:e25) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004<br>sign-1: STOP sign known, relevant to the path |

## Plain-language reading

- 9.70 s before the reference collision, A started moving (already the case when first observed).
- 9.70 s before the reference collision, B started moving (already the case when first observed).
- 9.00 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 7.75 s before the reference collision, B started braking.
- 7.45 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.05 s before the reference collision, B released the brake.
- 7.05 s before the reference collision, A started braking.
- 6.55 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.55 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.30 s before the reference collision, A stopped moving.
- 6.30 s before the reference collision, A came to a stop.
- 6.20 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-1).
- 4.40 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 1.95 s before the reference collision, A released the brake.
- 1.60 s before the reference collision, A left its stop.
- 1.60 s before the reference collision, A started moving.
- 1.55 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 1.55 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.05 s before the reference collision, A's time-to-contact with B became critical.
- 1.05 s before the reference collision, B's time-to-contact with A became critical.
- 0.60 s before the reference collision, A started turning left.
- 0.10 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 7340, B: 7340 N*s).
- At the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- At the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 0.05 s after the reference collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 0.05 s after the reference collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.05 s after the reference collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.10 s after the reference collision, A stopped turning left.
- 0.15 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the reference collision, B observed A stop closing in.
- 0.35 s after the reference collision, B stopped moving.
- 0.35 s after the reference collision, B came to a stop.
- 0.40 s after the reference collision, B observed unidentified object B:track_002 stop closing in.
- 0.40 s after the reference collision, B observed unidentified object B:track_004 stop closing in.
- 0.50 s after the reference collision, A stopped moving.
- 0.50 s after the reference collision, A came to a stop.
- 0.50 s after the reference collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the reference collision, B observed unidentified object B:track_003 stop closing in.
