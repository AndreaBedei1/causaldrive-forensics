# Global graph - S10/run_0_rolls_through

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
| A | ALIGNED | A:e11 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12489.77 vs 12489.77 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 2.50 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.0 m -> 0.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.10 m/s over 2.5 s<br>clearance at the contact 0.85 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.91 | B and A both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 2.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.3 m -> 0.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.65 m/s over 2.5 s<br>clearance at the contact 0.87 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.40 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.85 | relevant_to_ego_path=False |
| g04 | -3.30 | BRAKE_START | A | - | A:e03 @ 1.95 |  |
| g05 | -3.10 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e04 @ 2.15 |  |
| g06 | -2.55 | TURN_LEFT_START | A | - | A:e05 @ 2.70 |  |
| g07 | -2.55 | TRACK_APPEARED_RIGHT | B | A | B:e02 @ 2.70 |  |
| g08 | -2.55 | CLOSING_START | B | A | B:e03 @ 2.70 | active_at_first_observation=True |
| g09 | -2.50 | TRACK_APPEARED_LEFT | A | B | A:e06 @ 2.75 |  |
| g10 | -2.50 | CLOSING_START | A | B | A:e07 @ 2.75 | active_at_first_observation=True |
| g11 | -1.70 | CRITICAL_TTC_START | B | A | B:e04 @ 3.55 |  |
| g12 | -1.45 | BRAKE_END | A | - | A:e08 @ 3.80 |  |
| g13 | -1.45 | CRITICAL_TTC_START | A | B | A:e09 @ 3.80 |  |
| g14 | -0.30 | EGO_PATH_ENTRY | B | A | B:e05 @ 4.95 |  |
| g15 | -0.05 | TRACK_LOST | A | B | A:e10 @ 5.20 |  |
| g16 | 0.00 | COLLISION | - | A, B | A:e11 @ 5.25, B:e06 @ 5.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12489.77, B 12489.77 |
| g17 | 0.05 | TURN_LEFT_END | A | - | A:e12 @ 5.30 |  |
| g18 | 0.05 | BRAKE_START | A | - | A:e13 @ 5.30 |  |
| g19 | 0.05 | BRAKE_START | B | - | B:e07 @ 5.30 |  |
| g20 | 0.10 | MOVING_END | B | - | B:e08 @ 5.35 |  |
| g21 | 0.10 | STOP_START | B | - | B:e09 @ 5.35 |  |
| g22 | 0.15 | CRITICAL_TTC_END | B | A | B:e10 @ 5.40 |  |
| g23 | 0.15 | CLOSING_END | B | A | B:e11 @ 5.40 |  |
| g24 | 0.15 | MOVING_END | A | - | A:e14 @ 5.40 |  |
| g25 | 0.15 | STOP_START | A | - | A:e15 @ 5.40 |  |

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
    g06 --PRECEDES--> g10
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g09 --SAME_TRACK--> g10
    g09 --SAME_TRACK--> g13
    g09 --SAME_TRACK--> g15
    g07 --SAME_TRACK--> g08
    g07 --SAME_TRACK--> g11
    g07 --SAME_TRACK--> g14
    g07 --SAME_TRACK--> g22
    g07 --SAME_TRACK--> g23
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.25 | MOVING_START(A); MOVING_START(B) |
| -3.40 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -3.30 | BRAKE_START(A) |
| -3.10 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -2.55 | TURN_LEFT_START(A); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -2.50 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -1.70 | CRITICAL_TTC_START(B,A) |
| -1.45 | BRAKE_END(A); CRITICAL_TTC_START(A,B) |
| -0.30 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B) |
| +0.05 | TURN_LEFT_END(A); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | MOVING_END(B); STOP_START(B) |
| +0.15 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 3.80, COLLISION with B 5.25 (+1.45 s) [local times; t_global: critical_ttc_start -1.45, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 3.55, COLLISION with A 5.25 (+1.70 s); EGO_PATH_ENTRY 4.95 after critical TTC (+1.40 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -0.30, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.40 | A | g03 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| -3.30 | A | g04 BRAKE_START(A) (A:e03) | ego: MOVING<br>sign-0: STOP sign known |
| -3.10 | A | g05 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e04) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| -2.55 | A | g06 TURN_LEFT_START(A) (A:e05) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| -2.55 | B | g07 TRACK_APPEARED_RIGHT(B,A) (B:e02)<br>g08 CLOSING_START(B,A) (B:e03) | ego: MOVING |
| -2.50 | A | g09 TRACK_APPEARED_LEFT(A,B) (A:e06)<br>g10 CLOSING_START(A,B) (A:e07) | ego: MOVING, BRAKE, TURN_LEFT<br>sign-0: STOP sign known |
| -1.70 | B | g11 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.45 | A | g12 BRAKE_END(A) (A:e08)<br>g13 CRITICAL_TTC_START(A,B) (A:e09) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -0.30 | B | g14 EGO_PATH_ENTRY(B,A) (B:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -0.05 | A | g15 TRACK_LOST(A,B) (A:e10) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| +0.00 | A | g16 COLLISION(A,B) (A:e11) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| +0.00 | B | g16 COLLISION(A,B) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g17 TURN_LEFT_END(A) (A:e12)<br>g18 BRAKE_START(A) (A:e13) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| +0.05 | B | g19 BRAKE_START(B) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.10 | B | g20 MOVING_END(B) (B:e08)<br>g21 STOP_START(B) (B:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.15 | B | g22 CRITICAL_TTC_END(B,A) (B:e10)<br>g23 CLOSING_END(B,A) (B:e11) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.15 | A | g24 MOVING_END(A) (A:e14)<br>g25 STOP_START(A) (A:e15) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |

## Plain-language reading

- 5.25 s before the reference collision, A started moving (already the case when first observed).
- 5.25 s before the reference collision, B started moving (already the case when first observed).
- 3.40 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 3.30 s before the reference collision, A started braking.
- 3.10 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 2.55 s before the reference collision, A started turning left.
- 2.55 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 2.55 s before the reference collision, B observed A start closing in (already the case when first observed).
- 2.50 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 2.50 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.70 s before the reference collision, B's time-to-contact with A became critical.
- 1.45 s before the reference collision, A released the brake.
- 1.45 s before the reference collision, A's time-to-contact with B became critical.
- 0.30 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 12490, B: 12490 N*s).
- 0.05 s after the reference collision, A stopped turning left.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, B stopped moving.
- 0.10 s after the reference collision, B came to a stop.
- 0.15 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.15 s after the reference collision, B observed A stop closing in.
- 0.15 s after the reference collision, A stopped moving.
- 0.15 s after the reference collision, A came to a stop.
