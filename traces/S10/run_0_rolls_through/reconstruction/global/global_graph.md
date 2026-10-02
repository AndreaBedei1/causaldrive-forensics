# Global graph - S10/run_0_rolls_through

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| B:track_001 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e14 | 5.40 | -5.40 | reported the reference collision collision_001 |
| B | ALIGNED | B:e07 | 5.40 | -5.40 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12940.27 vs 12940.27 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 12940.27 vs 12940.27 N*s)<br>tracked for 2.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.6 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.18 m/s over 2.8 s<br>clearance at the contact 0.09 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 12940.27 vs 12940.27 N*s)<br>tracked for 2.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.3 m -> 0.6 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.61 m/s over 2.7 s (> 1.50)<br>clearance at the contact 0.59 m |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.40 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.40 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.40 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -5.40 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -4.25 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e03 @ 1.15 | relevant_to_ego_path=True |
| g06 | -3.45 | THROTTLE_END | A | - | A:e04 @ 1.95 |  |
| g07 | -3.45 | BRAKE_START | A | - | A:e05 @ 1.95 |  |
| g08 | -2.80 | TRACK_APPEARED_LEFT | A | B | A:e06 @ 2.60 |  |
| g09 | -2.80 | CLOSING_START | A | B | A:e07 @ 2.60 | active_at_first_observation=True |
| g10 | -2.70 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e03 @ 2.70 |  |
| g11 | -2.70 | CLOSING_START | B | B:track_001 | B:e04 @ 2.70 | active_at_first_observation=True |
| g12 | -2.65 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e08 @ 2.75 |  |
| g13 | -2.55 | BRAKE_END | A | - | A:e09 @ 2.85 |  |
| g14 | -2.55 | THROTTLE_START | A | - | A:e10 @ 2.85 |  |
| g15 | -2.00 | CRITICAL_TTC_START | A | B | A:e11 @ 3.40 |  |
| g16 | -1.80 | CRITICAL_TTC_START | B | B:track_001 | B:e05 @ 3.60 |  |
| g17 | -1.70 | TURN_LEFT_START | A | - | A:e12 @ 3.70 |  |
| g18 | -0.15 | EGO_PATH_ENTRY | B | B:track_001 | B:e06 @ 5.25 |  |
| g19 | -0.10 | EGO_PATH_ENTRY | A | B | A:e13 @ 5.30 |  |
| g20 | 0.00 | COLLISION | - | A, B | A:e14 @ 5.40, B:e07 @ 5.40 | matched_event=collision_001; reference_event=True; peak_impulse=A 12940.27, B 12940.27 |
| g21 | 0.00 | CRITICAL_TTC_END | A | B | A:e15 @ 5.40 |  |
| g22 | 0.00 | CRITICAL_TTC_END | B | B:track_001 | B:e08 @ 5.40 |  |
| g23 | 0.00 | CLOSING_END | B | B:track_001 | B:e09 @ 5.40 |  |
| g24 | 0.00 | TURN_LEFT_END | A | - | A:e16 @ 5.40 |  |
| g25 | 0.05 | CLOSING_END | A | B | A:e17 @ 5.45 |  |
| g26 | 0.05 | THROTTLE_END | A | - | A:e18 @ 5.45 |  |
| g27 | 0.05 | THROTTLE_END | B | - | B:e10 @ 5.45 |  |
| g28 | 0.05 | BRAKE_START | A | - | A:e19 @ 5.45 |  |
| g29 | 0.05 | BRAKE_START | B | - | B:e11 @ 5.45 |  |
| g30 | 0.10 | MOVING_END | A | - | A:e20 @ 5.50 |  |
| g31 | 0.10 | STOP_START | A | - | A:e21 @ 5.50 |  |
| g32 | 0.20 | MOVING_END | B | - | B:e12 @ 5.60 |  |
| g33 | 0.20 | STOP_START | B | - | B:e13 @ 5.60 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g05
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
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g20 --PRECEDES--> g28
    g20 --PRECEDES--> g29
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g21 --PRECEDES--> g29
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g15
    g08 --SAME_TRACK--> g19
    g08 --SAME_TRACK--> g21
    g08 --SAME_TRACK--> g25
    g10 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g16
    g10 --SAME_TRACK--> g18
    g10 --SAME_TRACK--> g22
    g10 --SAME_TRACK--> g23
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.40 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B) |
| -4.25 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -3.45 | THROTTLE_END(A); BRAKE_START(A) |
| -2.80 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -2.70 | TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001) |
| -2.65 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -2.55 | BRAKE_END(A); THROTTLE_START(A) |
| -2.00 | CRITICAL_TTC_START(A,B) |
| -1.80 | CRITICAL_TTC_START(B,B:track_001) |
| -1.70 | TURN_LEFT_START(A) |
| -0.15 | EGO_PATH_ENTRY(B,B:track_001) |
| -0.10 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); TURN_LEFT_END(A) |
| +0.05 | CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | MOVING_END(A); STOP_START(A) |
| +0.20 | MOVING_END(B); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 3.40, COLLISION with B 5.40 (+2.00 s); EGO_PATH_ENTRY 5.30 after critical TTC (+1.90 s) [local times; t_global: critical_ttc_start -2.00, ego_path_entry -0.10, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.60, COLLISION 5.40 (+1.80 s); EGO_PATH_ENTRY 5.25 after critical TTC (+1.65 s) [local times; t_global: critical_ttc_start -1.80, ego_path_entry -0.15, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.40 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02) | ego: not yet observed |
| -5.40 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -4.25 | A | g05 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e03) | ego: MOVING, THROTTLE |
| -3.45 | A | g06 THROTTLE_END(A) (A:e04)<br>g07 BRAKE_START(A) (A:e05) | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path |
| -2.80 | A | g08 TRACK_APPEARED_LEFT(A,B) (A:e06)<br>g09 CLOSING_START(A,B) (A:e07) | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path |
| -2.70 | B | g10 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e03)<br>g11 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, THROTTLE |
| -2.65 | A | g12 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -2.55 | A | g13 BRAKE_END(A) (A:e09)<br>g14 THROTTLE_START(A) (A:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path |
| -2.00 | A | g15 CRITICAL_TTC_START(A,B) (A:e11) | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.80 | B | g16 CRITICAL_TTC_START(B,B:track_001) (B:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -1.70 | A | g17 TURN_LEFT_START(A) (A:e12) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.15 | B | g18 EGO_PATH_ENTRY(B,B:track_001) (B:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC |
| -0.10 | A | g19 EGO_PATH_ENTRY(A,B) (A:e13) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | A | g20 COLLISION(A,B) (A:e14)<br>g21 CRITICAL_TTC_END(A,B) (A:e15)<br>g24 TURN_LEFT_END(A) (A:e16) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | B | g20 COLLISION(A,B) (B:e07)<br>g22 CRITICAL_TTC_END(B,B:track_001) (B:e08)<br>g23 CLOSING_END(B,B:track_001) (B:e09) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g25 CLOSING_END(A,B) (A:e17)<br>g26 THROTTLE_END(A) (A:e18)<br>g28 BRAKE_START(A) (A:e19) | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | B | g27 THROTTLE_END(B) (B:e10)<br>g29 BRAKE_START(B) (B:e11) | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH |
| +0.10 | A | g30 MOVING_END(A) (A:e20)<br>g31 STOP_START(A) (A:e21) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.20 | B | g32 MOVING_END(B) (B:e12)<br>g33 STOP_START(B) (B:e13) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |

## Plain-language reading

- 5.40 s before the reference collision, A started moving (already the case when first observed).
- 5.40 s before the reference collision, B started moving (already the case when first observed).
- 5.40 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 5.40 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 4.25 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 3.45 s before the reference collision, A released the accelerator.
- 3.45 s before the reference collision, A started braking.
- 2.80 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 2.80 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.70 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.70 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.65 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 2.55 s before the reference collision, A released the brake.
- 2.55 s before the reference collision, A pressed the accelerator.
- 2.00 s before the reference collision, A's time-to-contact with B became critical.
- 1.80 s before the reference collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.70 s before the reference collision, A started turning left.
- 0.15 s before the reference collision, B observed unidentified object B:track_001 enter its forward path corridor.
- 0.10 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12940, B: 12940 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- At the reference collision, B observed unidentified object B:track_001 stop closing in.
- At the reference collision, A stopped turning left.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A stopped moving.
- 0.10 s after the reference collision, A came to a stop.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
