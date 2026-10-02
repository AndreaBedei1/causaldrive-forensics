# Global graph - S12/run_0_near_simultaneous

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e16 | 9.50 | -9.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 9.50 | -9.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4032.49 vs 4032.49 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.5 m -> 1.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.33 m/s over 3.0 s<br>clearance at the contact 1.00 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.91 | B and A both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.9 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.64 m/s over 3.0 s<br>clearance at the contact 0.07 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -9.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -9.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -8.85 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.65 | relevant_to_ego_path=True |
| g04 | -7.70 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 1.80 | relevant_to_ego_path=True |
| g05 | -7.25 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.25 |  |
| g06 | -6.90 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e03 @ 2.60 |  |
| g07 | -6.90 | TRACK_APPEARED_LEFT | A | B | A:e04 @ 2.60 |  |
| g08 | -6.90 | CLOSING_START | A | B | A:e05 @ 2.60 | active_at_first_observation=True |
| g09 | -6.85 | BRAKE_START | A | - | A:e06 @ 2.65 |  |
| g10 | -6.75 | BRAKE_START | B | - | B:e04 @ 2.75 |  |
| g11 | -6.70 | TRACK_APPEARED_RIGHT | B | A | B:e05 @ 2.80 |  |
| g12 | -6.70 | CLOSING_START | B | A | B:e06 @ 2.80 | active_at_first_observation=True |
| g13 | -6.10 | MOVING_END | A | - | A:e07 @ 3.40 |  |
| g14 | -6.10 | STOP_START | A | - | A:e08 @ 3.40 |  |
| g15 | -6.05 | CLOSING_END | B | A | B:e07 @ 3.45 |  |
| g16 | -6.00 | CLOSING_END | A | B | A:e09 @ 3.50 |  |
| g17 | -6.00 | MOVING_END | B | - | B:e08 @ 3.50 |  |
| g18 | -6.00 | STOP_START | B | - | B:e09 @ 3.50 |  |
| g19 | -2.55 | BRAKE_END | A | - | A:e10 @ 6.95 |  |
| g20 | -2.55 | BRAKE_END | B | - | B:e10 @ 6.95 |  |
| g21 | -2.20 | STOP_END | A | - | A:e11 @ 7.30 |  |
| g22 | -2.20 | MOVING_START | A | - | A:e12 @ 7.30 |  |
| g23 | -2.20 | CLOSING_START | A | B | A:e13 @ 7.30 |  |
| g24 | -2.20 | CLOSING_START | B | A | B:e11 @ 7.30 |  |
| g25 | -2.15 | STOP_END | B | - | B:e12 @ 7.35 |  |
| g26 | -2.15 | MOVING_START | B | - | B:e13 @ 7.35 |  |
| g27 | -1.25 | CRITICAL_TTC_START | A | B | A:e14 @ 8.25 |  |
| g28 | -1.20 | TURN_LEFT_START | A | - | A:e15 @ 8.30 |  |
| g29 | -1.20 | CRITICAL_TTC_START | B | A | B:e14 @ 8.30 |  |
| g30 | -0.55 | EGO_PATH_ENTRY | B | A | B:e15 @ 8.95 |  |
| g31 | 0.00 | COLLISION | - | A, B | A:e16 @ 9.50, B:e16 @ 9.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 4032.49, B 4032.49 |
| g32 | 0.00 | CRITICAL_TTC_END | A | B | A:e17 @ 9.50 |  |
| g33 | 0.00 | CLOSING_END | A | B | A:e18 @ 9.50 |  |
| g34 | 0.00 | EGO_PATH_EXIT | B | A | B:e17 @ 9.50 |  |
| g35 | 0.05 | CRITICAL_TTC_END | B | A | B:e18 @ 9.55 |  |
| g36 | 0.05 | CLOSING_END | B | A | B:e19 @ 9.55 |  |
| g37 | 0.05 | BRAKE_START | A | - | A:e19 @ 9.55 |  |
| g38 | 0.05 | BRAKE_START | B | - | B:e20 @ 9.55 |  |
| g39 | 0.45 | MOVING_END | B | - | B:e21 @ 9.95 |  |
| g40 | 0.45 | STOP_START | B | - | B:e22 @ 9.95 |  |
| g41 | 0.50 | TURN_LEFT_END | A | - | A:e20 @ 10.00 |  |
| g42 | 0.50 | MOVING_END | A | - | A:e21 @ 10.00 |  |
| g43 | 0.50 | STOP_START | A | - | A:e22 @ 10.00 |  |
| g44 | 1.45 | STOP_SIGN_DETECTED_START | A | A:sign-1 | A:e23 @ 10.95 | relevant_to_ego_path=False |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
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
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g27
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g31 --PRECEDES--> g38
    g32 --PRECEDES--> g35
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g32 --PRECEDES--> g38
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g39 --PRECEDES--> g43
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g44
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g16
    g07 --SAME_TRACK--> g23
    g07 --SAME_TRACK--> g27
    g07 --SAME_TRACK--> g32
    g07 --SAME_TRACK--> g33
    g11 --SAME_TRACK--> g12
    g11 --SAME_TRACK--> g15
    g11 --SAME_TRACK--> g24
    g11 --SAME_TRACK--> g29
    g11 --SAME_TRACK--> g30
    g11 --SAME_TRACK--> g34
    g11 --SAME_TRACK--> g35
    g11 --SAME_TRACK--> g36
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -9.50 | MOVING_START(A); MOVING_START(B) |
| -8.85 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -7.70 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -7.25 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -6.90 | STOP_SIGN_DETECTED_END(B,B:sign-0); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -6.85 | BRAKE_START(A) |
| -6.75 | BRAKE_START(B) |
| -6.70 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -6.10 | MOVING_END(A); STOP_START(A) |
| -6.05 | CLOSING_END(B,A) |
| -6.00 | CLOSING_END(A,B); MOVING_END(B); STOP_START(B) |
| -2.55 | BRAKE_END(A); BRAKE_END(B) |
| -2.20 | STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A) |
| -2.15 | STOP_END(B); MOVING_START(B) |
| -1.25 | CRITICAL_TTC_START(A,B) |
| -1.20 | TURN_LEFT_START(A); CRITICAL_TTC_START(B,A) |
| -0.55 | EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); EGO_PATH_EXIT(B,A) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B) |
| +0.45 | MOVING_END(B); STOP_START(B) |
| +0.50 | TURN_LEFT_END(A); MOVING_END(A); STOP_START(A) |
| +1.45 | STOP_SIGN_DETECTED_START(A,A:sign-1) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 8.25, COLLISION with B 9.50 (+1.25 s) [local times; t_global: critical_ttc_start -1.25, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 8.30, COLLISION with A 9.50 (+1.20 s); EGO_PATH_ENTRY 8.95 after critical TTC (+0.65 s) [local times; t_global: critical_ttc_start -1.20, ego_path_entry -0.55, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -9.50 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -9.50 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -8.85 | A | g03 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| -7.70 | B | g04 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| -7.25 | A | g05 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -6.90 | B | g06 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -6.90 | A | g07 TRACK_APPEARED_LEFT(A,B) (A:e04)<br>g08 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -6.85 | A | g09 BRAKE_START(A) (A:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.75 | B | g10 BRAKE_START(B) (B:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -6.70 | B | g11 TRACK_APPEARED_RIGHT(B,A) (B:e05)<br>g12 CLOSING_START(B,A) (B:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| -6.10 | A | g13 MOVING_END(A) (A:e07)<br>g14 STOP_START(A) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.05 | B | g15 CLOSING_END(B,A) (B:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.00 | A | g16 CLOSING_END(A,B) (A:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.00 | B | g17 MOVING_END(B) (B:e08)<br>g18 STOP_START(B) (B:e09) | ego: MOVING, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.55 | A | g19 BRAKE_END(A) (A:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.55 | B | g20 BRAKE_END(B) (B:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.20 | A | g21 STOP_END(A) (A:e11)<br>g22 MOVING_START(A) (A:e12)<br>g23 CLOSING_START(A,B) (A:e13) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.20 | B | g24 CLOSING_START(B,A) (B:e11) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.15 | B | g25 STOP_END(B) (B:e12)<br>g26 MOVING_START(B) (B:e13) | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.25 | A | g27 CRITICAL_TTC_START(A,B) (A:e14) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.20 | A | g28 TURN_LEFT_START(A) (A:e15) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -1.20 | B | g29 CRITICAL_TTC_START(B,A) (B:e14) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -0.55 | B | g30 EGO_PATH_ENTRY(B,A) (B:e15) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | A | g31 COLLISION(A,B) (A:e16)<br>g32 CRITICAL_TTC_END(A,B) (A:e17)<br>g33 CLOSING_END(A,B) (A:e18) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | B | g31 COLLISION(A,B) (B:e16)<br>g34 EGO_PATH_EXIT(B,A) (B:e17) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | B | g35 CRITICAL_TTC_END(B,A) (B:e18)<br>g36 CLOSING_END(B,A) (B:e19)<br>g38 BRAKE_START(B) (B:e20) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | A | g37 BRAKE_START(A) (A:e19) | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| +0.45 | B | g39 MOVING_END(B) (B:e21)<br>g40 STOP_START(B) (B:e22) | ego: MOVING, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| +0.50 | A | g41 TURN_LEFT_END(A) (A:e20)<br>g42 MOVING_END(A) (A:e21)<br>g43 STOP_START(A) (A:e22) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| +1.45 | A | g44 STOP_SIGN_DETECTED_START(A,A:sign-1) (A:e23) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |

## Plain-language reading

- 9.50 s before the reference collision, A started moving (already the case when first observed).
- 9.50 s before the reference collision, B started moving (already the case when first observed).
- 8.85 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 7.70 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 7.25 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 6.90 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 6.90 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.90 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.85 s before the reference collision, A started braking.
- 6.75 s before the reference collision, B started braking.
- 6.70 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 6.10 s before the reference collision, A stopped moving.
- 6.10 s before the reference collision, A came to a stop.
- 6.05 s before the reference collision, B observed A stop closing in.
- 6.00 s before the reference collision, A observed B stop closing in.
- 6.00 s before the reference collision, B stopped moving.
- 6.00 s before the reference collision, B came to a stop.
- 2.55 s before the reference collision, A released the brake.
- 2.55 s before the reference collision, B released the brake.
- 2.20 s before the reference collision, A left its stop.
- 2.20 s before the reference collision, A started moving.
- 2.20 s before the reference collision, A observed B start closing in.
- 2.20 s before the reference collision, B observed A start closing in.
- 2.15 s before the reference collision, B left its stop.
- 2.15 s before the reference collision, B started moving.
- 1.25 s before the reference collision, A's time-to-contact with B became critical.
- 1.20 s before the reference collision, A started turning left.
- 1.20 s before the reference collision, B's time-to-contact with A became critical.
- 0.55 s before the reference collision, B observed A enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 4032, B: 4032 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A leave its forward path corridor.
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.50 s after the reference collision, A stopped turning left.
- 0.50 s after the reference collision, A stopped moving.
- 0.50 s after the reference collision, A came to a stop.
- 1.45 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
