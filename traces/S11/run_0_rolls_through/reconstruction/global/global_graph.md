# Global graph - S11/run_0_rolls_through

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
| A | ALIGNED | A:e06 | 5.50 | -5.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e11 | 5.50 | -5.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 8859.58 vs 8859.58 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 8859.58 vs 8859.58 N*s)<br>tracked for 2.55 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.6 m -> 1.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.34 m/s over 2.5 s<br>clearance at the contact 1.15 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.98 | B and A both reported collision_001 (peak impulse 8859.58 vs 8859.58 N*s)<br>tracked for 2.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.9 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.29 m/s over 2.5 s<br>clearance at the contact 0.46 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.55 | BRAKE_START | B | - | B:e02 @ 1.95 |  |
| g04 | -3.40 | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e03 @ 2.10 | relevant_to_ego_path=False |
| g05 | -3.00 | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e04 @ 2.50 |  |
| g06 | -2.85 | BRAKE_END | B | - | B:e05 @ 2.65 |  |
| g07 | -2.55 | TRACK_APPEARED_RIGHT | A | B | A:e02 @ 2.95 |  |
| g08 | -2.55 | CLOSING_START | A | B | A:e03 @ 2.95 | active_at_first_observation=True |
| g09 | -2.50 | TRACK_APPEARED_LEFT | B | A | B:e06 @ 3.00 |  |
| g10 | -2.50 | CLOSING_START | B | A | B:e07 @ 3.00 | active_at_first_observation=True |
| g11 | -1.75 | CRITICAL_TTC_START | A | B | A:e04 @ 3.75 |  |
| g12 | -1.70 | TURN_LEFT_START | B | - | B:e08 @ 3.80 |  |
| g13 | -1.45 | CRITICAL_TTC_START | B | A | B:e09 @ 4.05 |  |
| g14 | -0.15 | EGO_PATH_ENTRY | B | A | B:e10 @ 5.35 |  |
| g15 | -0.05 | TRACK_LOST | A | B | A:e05 @ 5.45 |  |
| g16 | 0.00 | COLLISION | - | A, B | A:e06 @ 5.50, B:e11 @ 5.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 8859.58, B 8859.58 |
| g17 | 0.00 | TURN_LEFT_END | B | - | B:e12 @ 5.50 |  |
| g18 | 0.05 | BRAKE_START | A | - | A:e07 @ 5.55 |  |
| g19 | 0.05 | BRAKE_START | B | - | B:e13 @ 5.55 |  |
| g20 | 0.20 | MOVING_END | B | - | B:e14 @ 5.70 |  |
| g21 | 0.20 | STOP_START | B | - | B:e15 @ 5.70 |  |
| g22 | 0.40 | CRITICAL_TTC_END | B | A | B:e16 @ 5.90 |  |
| g23 | 0.40 | CLOSING_END | B | A | B:e17 @ 5.90 |  |
| g24 | 0.55 | MOVING_END | A | - | A:e08 @ 6.05 |  |
| g25 | 0.55 | STOP_START | A | - | A:e09 @ 6.05 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g15
    g09 --SAME_TRACK--> g10
    g09 --SAME_TRACK--> g13
    g09 --SAME_TRACK--> g14
    g09 --SAME_TRACK--> g22
    g09 --SAME_TRACK--> g23
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.50 | MOVING_START(A); MOVING_START(B) |
| -3.55 | BRAKE_START(B) |
| -3.40 | STOP_SIGN_DETECTED_START(B,B:sign-1) |
| -3.00 | STOP_SIGN_DETECTED_END(B,B:sign-1) |
| -2.85 | BRAKE_END(B) |
| -2.55 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -2.50 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.75 | CRITICAL_TTC_START(A,B) |
| -1.70 | TURN_LEFT_START(B) |
| -1.45 | CRITICAL_TTC_START(B,A) |
| -0.15 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); TURN_LEFT_END(B) |
| +0.05 | BRAKE_START(A); BRAKE_START(B) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.40 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.55 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 3.75, COLLISION with B 5.50 (+1.75 s) [local times; t_global: critical_ttc_start -1.75, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 4.05, COLLISION with A 5.50 (+1.45 s); EGO_PATH_ENTRY 5.35 after critical TTC (+1.30 s) [local times; t_global: critical_ttc_start -1.45, ego_path_entry -0.15, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.50 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.50 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.55 | B | g03 BRAKE_START(B) (B:e02) | ego: MOVING |
| -3.40 | B | g04 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e03) | ego: MOVING, BRAKE |
| -3.00 | B | g05 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e04) | ego: MOVING, BRAKE<br>sign-1: STOP sign known |
| -2.85 | B | g06 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE<br>sign-1: STOP sign known |
| -2.55 | A | g07 TRACK_APPEARED_RIGHT(A,B) (A:e02)<br>g08 CLOSING_START(A,B) (A:e03) | ego: MOVING |
| -2.50 | B | g09 TRACK_APPEARED_LEFT(B,A) (B:e06)<br>g10 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>sign-1: STOP sign known |
| -1.75 | A | g11 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.70 | B | g12 TURN_LEFT_START(B) (B:e08) | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known |
| -1.45 | B | g13 CRITICAL_TTC_START(B,A) (B:e09) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>sign-1: STOP sign known |
| -0.15 | B | g14 EGO_PATH_ENTRY(B,A) (B:e10) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known |
| -0.05 | A | g15 TRACK_LOST(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g16 COLLISION(A,B) (A:e06) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g16 COLLISION(A,B) (B:e11)<br>g17 TURN_LEFT_END(B) (B:e12) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.05 | A | g18 BRAKE_START(A) (A:e07) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.05 | B | g19 BRAKE_START(B) (B:e13) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.20 | B | g20 MOVING_END(B) (B:e14)<br>g21 STOP_START(B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.40 | B | g22 CRITICAL_TTC_END(B,A) (B:e16)<br>g23 CLOSING_END(B,A) (B:e17) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known |
| +0.55 | A | g24 MOVING_END(A) (A:e08)<br>g25 STOP_START(A) (A:e09) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 5.50 s before the reference collision, A started moving (already the case when first observed).
- 5.50 s before the reference collision, B started moving (already the case when first observed).
- 3.55 s before the reference collision, B started braking.
- 3.40 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- 3.00 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 2.85 s before the reference collision, B released the brake.
- 2.55 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 2.55 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.50 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 2.50 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.75 s before the reference collision, A's time-to-contact with B became critical.
- 1.70 s before the reference collision, B started turning left.
- 1.45 s before the reference collision, B's time-to-contact with A became critical.
- 0.15 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 8860, B: 8860 N*s).
- At the reference collision, B stopped turning left.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.40 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.40 s after the reference collision, B observed A stop closing in.
- 0.55 s after the reference collision, A stopped moving.
- 0.55 s after the reference collision, A came to a stop.
