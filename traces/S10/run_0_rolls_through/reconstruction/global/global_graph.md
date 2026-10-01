# Global graph - S10/run_0_rolls_through

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e13 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12489.77 vs 12489.77 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.96 | A and B both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 1.45 s before the matched collision<br>at the contact: minimum range 1.64 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.45 m/s over 1.4 s |
| B:track_001 | A | ASSOCIATED | 0.91 | B and A both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 2.60 s before the matched collision<br>at the contact: minimum range 1.17 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.67 m/s over 2.6 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.05 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.20 |  |
| g04 | -3.45 | STRONG_THROTTLE_END | B | - | B:e03 @ 1.80 |  |
| g05 | -3.40 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.85 | relevant_to_ego_path=False |
| g06 | -3.30 | BRAKE_START | A | - | A:e03 @ 1.95 |  |
| g07 | -3.30 | HARD_BRAKE_START | A | - | A:e04 @ 1.95 |  |
| g08 | -3.10 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e05 @ 2.15 |  |
| g09 | -3.05 | HARD_BRAKE_END | A | - | A:e06 @ 2.20 |  |
| g10 | -2.60 | TRACK_APPEARED_RIGHT | B | A | B:e04 @ 2.65 |  |
| g11 | -2.60 | CLOSING_START | B | A | B:e05 @ 2.65 | active_at_first_observation=True |
| g12 | -1.75 | CRITICAL_TTC_START | B | A | B:e06 @ 3.50 |  |
| g13 | -1.45 | BRAKE_END | A | - | A:e07 @ 3.80 |  |
| g14 | -1.45 | TRACK_APPEARED_LEFT | A | B | A:e08 @ 3.80 |  |
| g15 | -1.45 | CLOSING_START | A | B | A:e09 @ 3.80 | active_at_first_observation=True |
| g16 | -1.45 | CRITICAL_TTC_START | A | B | A:e10 @ 3.80 | active_at_first_observation=True |
| g17 | -0.35 | EGO_PATH_ENTRY | B | A | B:e07 @ 4.90 |  |
| g18 | -0.05 | EGO_PATH_ENTRY | A | B | A:e11 @ 5.20 |  |
| g19 | -0.05 | TRACK_LOST | A | B | A:e12 @ 5.20 |  |
| g20 | 0.00 | COLLISION | - | A, B | A:e13 @ 5.25, B:e08 @ 5.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12489.77, B 12489.77 |
| g21 | 0.00 | STRONG_THROTTLE_START | A | - | A:e14 @ 5.25 |  |
| g22 | 0.00 | STRONG_THROTTLE_START | B | - | B:e09 @ 5.25 |  |
| g23 | 0.05 | STRONG_THROTTLE_END | A | - | A:e15 @ 5.30 |  |
| g24 | 0.05 | STRONG_THROTTLE_END | B | - | B:e10 @ 5.30 |  |
| g25 | 0.05 | BRAKE_START | A | - | A:e16 @ 5.30 |  |
| g26 | 0.05 | BRAKE_START | B | - | B:e11 @ 5.30 |  |
| g27 | 0.05 | HARD_BRAKE_START | A | - | A:e17 @ 5.30 |  |
| g28 | 0.05 | HARD_BRAKE_START | B | - | B:e12 @ 5.30 |  |
| g29 | 0.10 | MOVING_END | B | - | B:e13 @ 5.35 |  |
| g30 | 0.10 | STOP_START | B | - | B:e14 @ 5.35 |  |
| g31 | 0.15 | CRITICAL_TTC_END | B | A | B:e15 @ 5.40 |  |
| g32 | 0.15 | CLOSING_END | B | A | B:e16 @ 5.40 |  |
| g33 | 0.15 | MOVING_END | A | - | A:e18 @ 5.40 |  |
| g34 | 0.15 | STOP_START | A | - | A:e19 @ 5.40 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g17
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
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g20 --PRECEDES--> g28
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g14 --SAME_TRACK--> g15
    g14 --SAME_TRACK--> g16
    g14 --SAME_TRACK--> g18
    g14 --SAME_TRACK--> g19
    g10 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g12
    g10 --SAME_TRACK--> g17
    g10 --SAME_TRACK--> g31
    g10 --SAME_TRACK--> g32
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.25 | MOVING_START(A); MOVING_START(B) |
| -4.05 | STRONG_THROTTLE_START(B) |
| -3.45 | STRONG_THROTTLE_END(B) |
| -3.40 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -3.30 | BRAKE_START(A); HARD_BRAKE_START(A) |
| -3.10 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -3.05 | HARD_BRAKE_END(A) |
| -2.60 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -1.75 | CRITICAL_TTC_START(B,A) |
| -1.45 | BRAKE_END(A); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B) |
| -0.35 | EGO_PATH_ENTRY(B,A) |
| -0.05 | EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B) |
| +0.05 | STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B) |
| +0.10 | MOVING_END(B); STOP_START(B) |
| +0.15 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.05 | B | g03 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -3.45 | B | g04 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| -3.40 | A | g05 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| -3.30 | A | g06 BRAKE_START(A) (A:e03)<br>g07 HARD_BRAKE_START(A) (A:e04) | ego: MOVING<br>sign-0: STOP sign known |
| -3.10 | A | g08 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e05) | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign known |
| -3.05 | A | g09 HARD_BRAKE_END(A) (A:e06) | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign known |
| -2.60 | B | g10 TRACK_APPEARED_RIGHT(B,A) (B:e04)<br>g11 CLOSING_START(B,A) (B:e05) | ego: MOVING |
| -1.75 | B | g12 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING |
| -1.45 | A | g13 BRAKE_END(A) (A:e07)<br>g14 TRACK_APPEARED_LEFT(A,B) (A:e08)<br>g15 CLOSING_START(A,B) (A:e09)<br>g16 CRITICAL_TTC_START(A,B) (A:e10) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| -0.35 | B | g17 EGO_PATH_ENTRY(B,A) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -0.05 | A | g18 EGO_PATH_ENTRY(A,B) (A:e11)<br>g19 TRACK_LOST(A,B) (A:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| +0.00 | A | g20 COLLISION(A,B) (A:e13)<br>g21 STRONG_THROTTLE_START(A) (A:e14) | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| +0.00 | B | g20 COLLISION(A,B) (B:e08)<br>g22 STRONG_THROTTLE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g23 STRONG_THROTTLE_END(A) (A:e15)<br>g25 BRAKE_START(A) (A:e16)<br>g27 HARD_BRAKE_START(A) (A:e17) | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| +0.05 | B | g24 STRONG_THROTTLE_END(B) (B:e10)<br>g26 BRAKE_START(B) (B:e11)<br>g28 HARD_BRAKE_START(B) (B:e12) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.10 | B | g29 MOVING_END(B) (B:e13)<br>g30 STOP_START(B) (B:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.15 | B | g31 CRITICAL_TTC_END(B,A) (B:e15)<br>g32 CLOSING_END(B,A) (B:e16) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.15 | A | g33 MOVING_END(A) (A:e18)<br>g34 STOP_START(A) (A:e19) | ego: MOVING, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |

## Plain-language reading

- 5.25 s before the matched collision, A started moving (already the case when first observed).
- 5.25 s before the matched collision, B started moving (already the case when first observed).
- 4.05 s before the matched collision, B started applying strong throttle.
- 3.45 s before the matched collision, B stopped applying strong throttle.
- 3.40 s before the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 3.30 s before the matched collision, A started braking.
- 3.30 s before the matched collision, A started braking hard.
- 3.10 s before the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 3.05 s before the matched collision, A stopped braking hard.
- 2.60 s before the matched collision, B's radar started tracking A, which appeared on its right.
- 2.60 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.75 s before the matched collision, B's time-to-contact with A became critical.
- 1.45 s before the matched collision, A released the brake.
- 1.45 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 1.45 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.45 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 0.35 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A observed B enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12490, B: 12490 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.10 s after the matched collision, B stopped moving.
- 0.10 s after the matched collision, B came to a stop.
- 0.15 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.15 s after the matched collision, B observed A stop closing in.
- 0.15 s after the matched collision, A stopped moving.
- 0.15 s after the matched collision, A came to a stop.
