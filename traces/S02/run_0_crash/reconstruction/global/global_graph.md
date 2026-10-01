# Global graph - S02/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5953.86 vs 5953.86 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.95 | A and B both reported collision_001 (peak impulse 5953.86 vs 5953.86 N*s)<br>tracked for 4.25 s before the matched collision<br>at the contact: minimum range 0.93 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.46 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.25 | TRACK_APPEARED_LEFT | A | B | A:e02 @ 0.00 |  |
| g04 | -4.25 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -3.90 | STRONG_THROTTLE_START | B | - | B:e02 @ 0.35 |  |
| g06 | -3.10 | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g07 | -2.95 | STRONG_THROTTLE_END | B | - | B:e03 @ 1.30 |  |
| g08 | -2.90 | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g09 | -1.90 | CUT_IN_FROM_LEFT_START | A | B | A:e06 @ 2.35 |  |
| g10 | -1.45 | CRITICAL_TTC_START | A | B | A:e07 @ 2.80 |  |
| g11 | -1.10 | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g12 | -0.95 | EGO_PATH_ENTRY | A | B | A:e08 @ 3.30 |  |
| g13 | -0.65 | BRAKE_END | B | - | B:e05 @ 3.60 |  |
| g14 | -0.40 | BRAKE_START | A | - | A:e09 @ 3.85 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e10 @ 4.25, B:e06 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 5953.86, B 5953.86 |
| g16 | 0.00 | CUT_IN_FROM_LEFT_END | A | B | A:e11 @ 4.25 |  |
| g17 | 0.00 | BRAKE_START | B | - | B:e07 @ 4.25 |  |
| g18 | 0.00 | HARD_BRAKE_START | B | - | B:e08 @ 4.25 |  |
| g19 | 0.05 | CRITICAL_TTC_END | A | B | A:e12 @ 4.30 |  |
| g20 | 0.05 | CLOSING_END | A | B | A:e13 @ 4.30 |  |
| g21 | 0.05 | HARD_BRAKE_START | A | - | A:e14 @ 4.30 |  |
| g22 | 0.60 | MOVING_END | A | - | A:e15 @ 4.85 |  |
| g23 | 0.60 | STOP_START | A | - | A:e16 @ 4.85 |  |
| g24 | 0.75 | MOVING_END | B | - | B:e09 @ 5.00 |  |
| g25 | 0.75 | STOP_START | B | - | B:e10 @ 5.00 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g16
    g03 --SAME_TRACK--> g19
    g03 --SAME_TRACK--> g20
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -3.90 | STRONG_THROTTLE_START(B) |
| -3.10 | STRONG_THROTTLE_START(A) |
| -2.95 | STRONG_THROTTLE_END(B) |
| -2.90 | STRONG_THROTTLE_END(A) |
| -1.90 | CUT_IN_FROM_LEFT_START(A,B) |
| -1.45 | CRITICAL_TTC_START(A,B) |
| -1.10 | BRAKE_START(B) |
| -0.95 | EGO_PATH_ENTRY(A,B) |
| -0.65 | BRAKE_END(B) |
| -0.40 | BRAKE_START(A) |
| +0.00 | COLLISION(A,B); CUT_IN_FROM_LEFT_END(A,B); BRAKE_START(B); HARD_BRAKE_START(B) |
| +0.05 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B); HARD_BRAKE_START(A) |
| +0.60 | MOVING_END(A); STOP_START(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,B) (A:e02)<br>g04 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.90 | B | g05 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -3.10 | A | g06 STRONG_THROTTLE_START(A) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.95 | B | g07 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| -2.90 | A | g08 STRONG_THROTTLE_END(A) (A:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING |
| -1.90 | A | g09 CUT_IN_FROM_LEFT_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| -1.45 | A | g10 CRITICAL_TTC_START(A,B) (A:e07) | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| -1.10 | B | g11 BRAKE_START(B) (B:e04) | ego: MOVING |
| -0.95 | A | g12 EGO_PATH_ENTRY(A,B) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| -0.65 | B | g13 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE |
| -0.40 | A | g14 BRAKE_START(A) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | A | g15 COLLISION(A,B) (A:e10)<br>g16 CUT_IN_FROM_LEFT_END(A,B) (A:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g15 COLLISION(A,B) (B:e06)<br>g17 BRAKE_START(B) (B:e07)<br>g18 HARD_BRAKE_START(B) (B:e08) | ego: MOVING |
| +0.05 | A | g19 CRITICAL_TTC_END(A,B) (A:e12)<br>g20 CLOSING_END(A,B) (A:e13)<br>g21 HARD_BRAKE_START(A) (A:e14) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.60 | A | g22 MOVING_END(A) (A:e15)<br>g23 STOP_START(A) (A:e16) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH |
| +0.75 | B | g24 MOVING_END(B) (B:e09)<br>g25 STOP_START(B) (B:e10) | ego: MOVING, BRAKE, HARD_BRAKE |

## Plain-language reading

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 4.25 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 4.25 s before the matched collision, A observed B start closing in (already the case when first observed).
- 3.90 s before the matched collision, B started applying strong throttle.
- 3.10 s before the matched collision, A started applying strong throttle.
- 2.95 s before the matched collision, B stopped applying strong throttle.
- 2.90 s before the matched collision, A stopped applying strong throttle.
- 1.90 s before the matched collision, A observed B cutting in from the left.
- 1.45 s before the matched collision, A's time-to-contact with B became critical.
- 1.10 s before the matched collision, B started braking.
- 0.95 s before the matched collision, A observed B enter its forward path corridor.
- 0.65 s before the matched collision, B released the brake.
- 0.40 s before the matched collision, A started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5954, B: 5954 N*s).
- At the matched collision, A observed B's cut-in from the left settle.
- At the matched collision, B started braking.
- At the matched collision, B started braking hard.
- 0.05 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A started braking hard.
- 0.60 s after the matched collision, A stopped moving.
- 0.60 s after the matched collision, A came to a stop.
- 0.75 s after the matched collision, B stopped moving.
- 0.75 s after the matched collision, B came to a stop.
