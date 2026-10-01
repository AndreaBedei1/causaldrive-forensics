# Global graph - S03/run_0_crash

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
| A | ALIGNED | A:e06 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>not at the contact: minimum range 3.78 m in the last 0.50 s (needs <= 3.50 m)<br>track speed agrees with B's own speed: RMSE 0.38 m/s over 2.0 s |
| B:track_001 | A | ASSOCIATED | 0.75 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.05 s before the matched collision<br>at the contact: minimum range 1.07 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 1.14 m/s over 2.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.10 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.15 |  |
| g04 | -2.20 | TRACK_APPEARED_RIGHT | A | A:track_001 | A:e02 @ 2.05 |  |
| g05 | -2.20 | CLOSING_START | A | A:track_001 | A:e03 @ 2.05 | active_at_first_observation=True |
| g06 | -2.05 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 2.20 |  |
| g07 | -2.05 | CLOSING_START | B | A | B:e04 @ 2.20 | active_at_first_observation=True |
| g08 | -1.85 | STRONG_THROTTLE_END | B | - | B:e05 @ 2.40 |  |
| g09 | -1.85 | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 2.40 |  |
| g10 | -1.85 | CRITICAL_TTC_START | B | A | B:e06 @ 2.40 |  |
| g11 | -0.15 | TRACK_LOST | A | A:track_001 | A:e05 @ 4.10 |  |
| g12 | -0.10 | EGO_PATH_ENTRY | B | A | B:e07 @ 4.15 |  |
| g13 | 0.00 | COLLISION | - | A, B | A:e06 @ 4.25, B:e08 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 12077.22, B 12077.22 |
| g14 | 0.00 | STRONG_THROTTLE_START | B | - | B:e09 @ 4.25 |  |
| g15 | 0.05 | STRONG_THROTTLE_END | B | - | B:e10 @ 4.30 |  |
| g16 | 0.05 | BRAKE_START | A | - | A:e07 @ 4.30 |  |
| g17 | 0.05 | BRAKE_START | B | - | B:e11 @ 4.30 |  |
| g18 | 0.05 | HARD_BRAKE_START | A | - | A:e08 @ 4.30 |  |
| g19 | 0.05 | HARD_BRAKE_START | B | - | B:e12 @ 4.30 |  |
| g20 | 0.10 | CRITICAL_TTC_END | B | A | B:e13 @ 4.35 |  |
| g21 | 0.10 | CLOSING_END | B | A | B:e14 @ 4.35 |  |
| g22 | 0.30 | MOVING_END | B | - | B:e15 @ 4.55 |  |
| g23 | 0.30 | STOP_START | B | - | B:e16 @ 4.55 |  |
| g24 | 0.45 | EGO_PATH_EXIT | B | A | B:e17 @ 4.70 |  |
| g25 | 0.65 | MOVING_END | A | - | A:e09 @ 4.90 |  |
| g26 | 0.65 | STOP_START | A | - | A:e10 @ 4.90 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g06 --PRECEDES--> g10
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g07 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g13 --PRECEDES--> g18
    g13 --PRECEDES--> g19
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g14 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g11
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g10
    g06 --SAME_TRACK--> g12
    g06 --SAME_TRACK--> g20
    g06 --SAME_TRACK--> g21
    g06 --SAME_TRACK--> g24
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B) |
| -3.10 | STRONG_THROTTLE_START(B) |
| -2.20 | TRACK_APPEARED_RIGHT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.05 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.85 | STRONG_THROTTLE_END(B); CRITICAL_TTC_START(A,A:track_001); CRITICAL_TTC_START(B,A) |
| -0.15 | TRACK_LOST(A,A:track_001) |
| -0.10 | EGO_PATH_ENTRY(B,A) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(B) |
| +0.05 | STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B) |
| +0.10 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.30 | MOVING_END(B); STOP_START(B) |
| +0.45 | EGO_PATH_EXIT(B,A) |
| +0.65 | MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.10 | B | g03 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -2.20 | A | g04 TRACK_APPEARED_RIGHT(A,A:track_001) (A:e02)<br>g05 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| -2.05 | B | g06 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g07 CLOSING_START(B,A) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| -1.85 | B | g08 STRONG_THROTTLE_END(B) (B:e05)<br>g10 CRITICAL_TTC_START(B,A) (B:e06) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING |
| -1.85 | A | g09 CRITICAL_TTC_START(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -0.15 | A | g11 TRACK_LOST(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -0.10 | B | g12 EGO_PATH_ENTRY(B,A) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g13 COLLISION(A,B) (A:e06) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g13 COLLISION(A,B) (B:e08)<br>g14 STRONG_THROTTLE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | B | g15 STRONG_THROTTLE_END(B) (B:e10)<br>g17 BRAKE_START(B) (B:e11)<br>g19 HARD_BRAKE_START(B) (B:e12) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g16 BRAKE_START(A) (A:e07)<br>g18 HARD_BRAKE_START(A) (A:e08) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.10 | B | g20 CRITICAL_TTC_END(B,A) (B:e13)<br>g21 CLOSING_END(B,A) (B:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.30 | B | g22 MOVING_END(B) (B:e15)<br>g23 STOP_START(B) (B:e16) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH |
| +0.45 | B | g24 EGO_PATH_EXIT(B,A) (B:e17) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH |
| +0.65 | A | g25 MOVING_END(A) (A:e09)<br>g26 STOP_START(A) (A:e10) | ego: MOVING, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 3.10 s before the matched collision, B started applying strong throttle.
- 2.20 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared on its right.
- 2.20 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.05 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 2.05 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.85 s before the matched collision, B stopped applying strong throttle.
- 1.85 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.85 s before the matched collision, B's time-to-contact with A became critical.
- 0.15 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 0.10 s before the matched collision, B observed A enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.10 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.10 s after the matched collision, B observed A stop closing in.
- 0.30 s after the matched collision, B stopped moving.
- 0.30 s after the matched collision, B came to a stop.
- 0.45 s after the matched collision, B observed A leave its forward path corridor.
- 0.65 s after the matched collision, A stopped moving.
- 0.65 s after the matched collision, A came to a stop.
