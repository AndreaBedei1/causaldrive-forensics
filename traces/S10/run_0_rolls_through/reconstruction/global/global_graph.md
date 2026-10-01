# Global graph - S10/run_0_rolls_through

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12489.77 vs 12489.77 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 2.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.9 m -> 1.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.55 m/s over 2.8 s (> 1.50)<br>range at the contact 1.44 m |
| B:track_001 | A | ASSOCIATED | 0.91 | B and A both reported collision_001 (peak impulse 12489.77 vs 12489.77 N*s)<br>tracked for 2.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.6 m -> 1.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.66 m/s over 2.6 s<br>range at the contact 1.17 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.45 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.80 | relevant_to_ego_path=False |
| g04 | -3.30 | BRAKE_START | A | - | A:e03 @ 1.95 |  |
| g05 | -3.10 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e04 @ 2.15 |  |
| g06 | -2.80 | TRACK_APPEARED_LEFT | A | A:track_001 | A:e05 @ 2.45 |  |
| g07 | -2.80 | CLOSING_START | A | A:track_001 | A:e06 @ 2.45 | active_at_first_observation=True |
| g08 | -2.65 | TRACK_APPEARED_RIGHT | B | A | B:e02 @ 2.60 |  |
| g09 | -2.65 | CLOSING_START | B | A | B:e03 @ 2.60 | active_at_first_observation=True |
| g10 | -2.55 | TURN_LEFT_START | A | - | A:e07 @ 2.70 |  |
| g11 | -1.70 | CRITICAL_TTC_START | B | A | B:e04 @ 3.55 |  |
| g12 | -1.45 | BRAKE_END | A | - | A:e08 @ 3.80 |  |
| g13 | -1.40 | CRITICAL_TTC_START | A | A:track_001 | A:e09 @ 3.85 |  |
| g14 | -0.30 | EGO_PATH_ENTRY | B | A | B:e05 @ 4.95 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e10 @ 5.25, B:e06 @ 5.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12489.77, B 12489.77 |
| g16 | 0.00 | CLOSING_END | A | A:track_001 | A:e11 @ 5.25 |  |
| g17 | 0.00 | TRACK_LOST | A | A:track_001 | A:e12 @ 5.25 |  |
| g18 | 0.05 | TURN_LEFT_END | A | - | A:e13 @ 5.30 |  |
| g19 | 0.05 | BRAKE_START | A | - | A:e14 @ 5.30 |  |
| g20 | 0.05 | BRAKE_START | B | - | B:e07 @ 5.30 |  |
| g21 | 0.10 | MOVING_END | B | - | B:e08 @ 5.35 |  |
| g22 | 0.10 | STOP_START | B | - | B:e09 @ 5.35 |  |
| g23 | 0.15 | CRITICAL_TTC_END | B | A | B:e10 @ 5.40 |  |
| g24 | 0.15 | CLOSING_END | B | A | B:e11 @ 5.40 |  |
| g25 | 0.15 | MOVING_END | A | - | A:e15 @ 5.40 |  |
| g26 | 0.15 | STOP_START | A | - | A:e16 @ 5.40 |  |

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
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g13
    g06 --SAME_TRACK--> g16
    g06 --SAME_TRACK--> g17
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g14
    g08 --SAME_TRACK--> g23
    g08 --SAME_TRACK--> g24
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.25 | MOVING_START(A); MOVING_START(B) |
| -3.45 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -3.30 | BRAKE_START(A) |
| -3.10 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -2.80 | TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.65 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -2.55 | TURN_LEFT_START(A) |
| -1.70 | CRITICAL_TTC_START(B,A) |
| -1.45 | BRAKE_END(A) |
| -1.40 | CRITICAL_TTC_START(A,A:track_001) |
| -0.30 | EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B); CLOSING_END(A,A:track_001); TRACK_LOST(A,A:track_001) |
| +0.05 | TURN_LEFT_END(A); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | MOVING_END(B); STOP_START(B) |
| +0.15 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 3.85, COLLISION 5.25 (+1.40 s) [local times; t_global: critical_ttc_start -1.40, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 3.55, COLLISION 5.25 (+1.70 s); EGO_PATH_ENTRY 4.95 after critical TTC (+1.40 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -0.30, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.45 | A | g03 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| -3.30 | A | g04 BRAKE_START(A) (A:e03) | ego: MOVING<br>sign-0: STOP sign known |
| -3.10 | A | g05 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e04) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| -2.80 | A | g06 TRACK_APPEARED_LEFT(A,A:track_001) (A:e05)<br>g07 CLOSING_START(A,A:track_001) (A:e06) | ego: MOVING, BRAKE<br>sign-0: STOP sign known |
| -2.65 | B | g08 TRACK_APPEARED_RIGHT(B,A) (B:e02)<br>g09 CLOSING_START(B,A) (B:e03) | ego: MOVING |
| -2.55 | A | g10 TURN_LEFT_START(A) (A:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -1.70 | B | g11 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.45 | A | g12 BRAKE_END(A) (A:e08) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -1.40 | A | g13 CRITICAL_TTC_START(A,A:track_001) (A:e09) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -0.30 | B | g14 EGO_PATH_ENTRY(B,A) (B:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g15 COLLISION(A,B) (A:e10)<br>g16 CLOSING_END(A,A:track_001) (A:e11)<br>g17 TRACK_LOST(A,A:track_001) (A:e12) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| +0.00 | B | g15 COLLISION(A,B) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g18 TURN_LEFT_END(A) (A:e13)<br>g19 BRAKE_START(A) (A:e14) | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| +0.05 | B | g20 BRAKE_START(B) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.10 | B | g21 MOVING_END(B) (B:e08)<br>g22 STOP_START(B) (B:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.15 | B | g23 CRITICAL_TTC_END(B,A) (B:e10)<br>g24 CLOSING_END(B,A) (B:e11) | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.15 | A | g25 MOVING_END(A) (A:e15)<br>g26 STOP_START(A) (A:e16) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |

## Plain-language reading

- 5.25 s before the matched collision, A started moving (already the case when first observed).
- 5.25 s before the matched collision, B started moving (already the case when first observed).
- 3.45 s before the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 3.30 s before the matched collision, A started braking.
- 3.10 s before the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 2.80 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 2.80 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.65 s before the matched collision, B's radar started tracking A, which appeared on its right.
- 2.65 s before the matched collision, B observed A start closing in (already the case when first observed).
- 2.55 s before the matched collision, A started turning left.
- 1.70 s before the matched collision, B's time-to-contact with A became critical.
- 1.45 s before the matched collision, A released the brake.
- 1.40 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 0.30 s before the matched collision, B observed A enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12490, B: 12490 N*s).
- At the matched collision, A observed unidentified object A:track_001 stop closing in.
- At the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 0.05 s after the matched collision, A stopped turning left.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.10 s after the matched collision, B stopped moving.
- 0.10 s after the matched collision, B came to a stop.
- 0.15 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.15 s after the matched collision, B observed A stop closing in.
- 0.15 s after the matched collision, A stopped moving.
- 0.15 s after the matched collision, A came to a stop.
