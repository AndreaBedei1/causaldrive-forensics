# Global graph - S11/run_0_rolls_through

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
| A | ALIGNED | A:e07 | 5.50 | -5.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 5.50 | -5.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 8859.58 vs 8859.58 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.94 | A and B both reported collision_001 (peak impulse 8859.58 vs 8859.58 N*s)<br>tracked for 2.75 s before the matched collision<br>at the contact: minimum range 1.59 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.51 m/s over 2.7 s |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 8859.58 vs 8859.58 N*s)<br>tracked for 1.55 s before the matched collision<br>at the contact: minimum range 0.62 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.46 m/s over 1.5 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.25 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g04 | -3.65 | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g05 | -3.55 | BRAKE_START | B | - | B:e04 @ 1.95 |  |
| g06 | -3.55 | HARD_BRAKE_START | B | - | B:e05 @ 1.95 |  |
| g07 | -3.40 | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e06 @ 2.10 | relevant_to_ego_path=False |
| g08 | -3.30 | HARD_BRAKE_END | B | - | B:e07 @ 2.20 |  |
| g09 | -3.05 | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e08 @ 2.45 |  |
| g10 | -2.85 | BRAKE_END | B | - | B:e09 @ 2.65 |  |
| g11 | -2.75 | TRACK_APPEARED_RIGHT | A | B | A:e02 @ 2.75 |  |
| g12 | -2.75 | CLOSING_START | A | B | A:e03 @ 2.75 | active_at_first_observation=True |
| g13 | -2.50 | STRONG_THROTTLE_START | B | - | B:e10 @ 3.00 |  |
| g14 | -2.25 | STRONG_THROTTLE_END | B | - | B:e11 @ 3.25 |  |
| g15 | -1.80 | CRITICAL_TTC_START | A | B | A:e04 @ 3.70 |  |
| g16 | -1.55 | TRACK_APPEARED_LEFT | B | A | B:e12 @ 3.95 |  |
| g17 | -1.55 | CLOSING_START | B | A | B:e13 @ 3.95 | active_at_first_observation=True |
| g18 | -1.55 | CRITICAL_TTC_START | B | A | B:e14 @ 3.95 | active_at_first_observation=True |
| g19 | -0.20 | EGO_PATH_ENTRY | B | A | B:e15 @ 5.30 |  |
| g20 | -0.05 | EGO_PATH_ENTRY | A | B | A:e05 @ 5.45 |  |
| g21 | -0.05 | TRACK_LOST | A | B | A:e06 @ 5.45 |  |
| g22 | 0.00 | COLLISION | - | A, B | A:e07 @ 5.50, B:e16 @ 5.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 8859.58, B 8859.58 |
| g23 | 0.00 | STRONG_THROTTLE_START | A | - | A:e08 @ 5.50 |  |
| g24 | 0.00 | STRONG_THROTTLE_START | B | - | B:e17 @ 5.50 |  |
| g25 | 0.05 | STRONG_THROTTLE_END | A | - | A:e09 @ 5.55 |  |
| g26 | 0.05 | STRONG_THROTTLE_END | B | - | B:e18 @ 5.55 |  |
| g27 | 0.05 | BRAKE_START | A | - | A:e10 @ 5.55 |  |
| g28 | 0.05 | BRAKE_START | B | - | B:e19 @ 5.55 |  |
| g29 | 0.05 | HARD_BRAKE_START | A | - | A:e11 @ 5.55 |  |
| g30 | 0.05 | HARD_BRAKE_START | B | - | B:e20 @ 5.55 |  |
| g31 | 0.20 | MOVING_END | B | - | B:e21 @ 5.70 |  |
| g32 | 0.20 | STOP_START | B | - | B:e22 @ 5.70 |  |
| g33 | 0.25 | CRITICAL_TTC_END | B | A | B:e23 @ 5.75 |  |
| g34 | 0.25 | CLOSING_END | B | A | B:e24 @ 5.75 |  |
| g35 | 0.55 | MOVING_END | A | - | A:e12 @ 6.05 |  |
| g36 | 0.55 | STOP_START | A | - | A:e13 @ 6.05 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g22 --PRECEDES--> g30
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g25 --PRECEDES--> g32
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g11 --SAME_TRACK--> g12
    g11 --SAME_TRACK--> g15
    g11 --SAME_TRACK--> g20
    g11 --SAME_TRACK--> g21
    g16 --SAME_TRACK--> g17
    g16 --SAME_TRACK--> g18
    g16 --SAME_TRACK--> g19
    g16 --SAME_TRACK--> g33
    g16 --SAME_TRACK--> g34
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.50 | MOVING_START(A); MOVING_START(B) |
| -4.25 | STRONG_THROTTLE_START(B) |
| -3.65 | STRONG_THROTTLE_END(B) |
| -3.55 | BRAKE_START(B); HARD_BRAKE_START(B) |
| -3.40 | STOP_SIGN_DETECTED_START(B,B:sign-1) |
| -3.30 | HARD_BRAKE_END(B) |
| -3.05 | STOP_SIGN_DETECTED_END(B,B:sign-1) |
| -2.85 | BRAKE_END(B) |
| -2.75 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -2.50 | STRONG_THROTTLE_START(B) |
| -2.25 | STRONG_THROTTLE_END(B) |
| -1.80 | CRITICAL_TTC_START(A,B) |
| -1.55 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A); CRITICAL_TTC_START(B,A) |
| -0.20 | EGO_PATH_ENTRY(B,A) |
| -0.05 | EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B) |
| +0.05 | STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.25 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.55 | MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.50 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.50 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.25 | B | g03 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -3.65 | B | g04 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| -3.55 | B | g05 BRAKE_START(B) (B:e04)<br>g06 HARD_BRAKE_START(B) (B:e05) | ego: MOVING |
| -3.40 | B | g07 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e06) | ego: MOVING, BRAKE, HARD_BRAKE |
| -3.30 | B | g08 HARD_BRAKE_END(B) (B:e07) | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign known |
| -3.05 | B | g09 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e08) | ego: MOVING, BRAKE<br>sign-1: STOP sign known |
| -2.85 | B | g10 BRAKE_END(B) (B:e09) | ego: MOVING, BRAKE<br>sign-1: STOP sign known |
| -2.75 | A | g11 TRACK_APPEARED_RIGHT(A,B) (A:e02)<br>g12 CLOSING_START(A,B) (A:e03) | ego: MOVING |
| -2.50 | B | g13 STRONG_THROTTLE_START(B) (B:e10) | ego: MOVING<br>sign-1: STOP sign known |
| -2.25 | B | g14 STRONG_THROTTLE_END(B) (B:e11) | ego: MOVING, STRONG_THROTTLE<br>sign-1: STOP sign known |
| -1.80 | A | g15 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.55 | B | g16 TRACK_APPEARED_LEFT(B,A) (B:e12)<br>g17 CLOSING_START(B,A) (B:e13)<br>g18 CRITICAL_TTC_START(B,A) (B:e14) | ego: MOVING<br>sign-1: STOP sign known |
| -0.20 | B | g19 EGO_PATH_ENTRY(B,A) (B:e15) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known |
| -0.05 | A | g20 EGO_PATH_ENTRY(A,B) (A:e05)<br>g21 TRACK_LOST(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g22 COLLISION(A,B) (A:e07)<br>g23 STRONG_THROTTLE_START(A) (A:e08) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g22 COLLISION(A,B) (B:e16)<br>g24 STRONG_THROTTLE_START(B) (B:e17) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.05 | A | g25 STRONG_THROTTLE_END(A) (A:e09)<br>g27 BRAKE_START(A) (A:e10)<br>g29 HARD_BRAKE_START(A) (A:e11) | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001 |
| +0.05 | B | g26 STRONG_THROTTLE_END(B) (B:e18)<br>g28 BRAKE_START(B) (B:e19)<br>g30 HARD_BRAKE_START(B) (B:e20) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.20 | B | g31 MOVING_END(B) (B:e21)<br>g32 STOP_START(B) (B:e22) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.25 | B | g33 CRITICAL_TTC_END(B,A) (B:e23)<br>g34 CLOSING_END(B,A) (B:e24) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.55 | A | g35 MOVING_END(A) (A:e12)<br>g36 STOP_START(A) (A:e13) | ego: MOVING, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 5.50 s before the matched collision, A started moving (already the case when first observed).
- 5.50 s before the matched collision, B started moving (already the case when first observed).
- 4.25 s before the matched collision, B started applying strong throttle.
- 3.65 s before the matched collision, B stopped applying strong throttle.
- 3.55 s before the matched collision, B started braking.
- 3.55 s before the matched collision, B started braking hard.
- 3.40 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- 3.30 s before the matched collision, B stopped braking hard.
- 3.05 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 2.85 s before the matched collision, B released the brake.
- 2.75 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 2.75 s before the matched collision, A observed B start closing in (already the case when first observed).
- 2.50 s before the matched collision, B started applying strong throttle.
- 2.25 s before the matched collision, B stopped applying strong throttle.
- 1.80 s before the matched collision, A's time-to-contact with B became critical.
- 1.55 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 1.55 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.55 s before the matched collision, B's time-to-contact with A became critical (already the case when first observed).
- 0.20 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A observed B enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 8860, B: 8860 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.25 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the matched collision, B observed A stop closing in.
- 0.55 s after the matched collision, A stopped moving.
- 0.55 s after the matched collision, A came to a stop.
