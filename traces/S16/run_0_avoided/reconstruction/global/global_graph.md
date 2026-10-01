# Global graph - S16/run_0_avoided

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e05 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>at the contact: minimum range 0.52 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.47 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.15 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g04 | -4.45 | STRONG_THROTTLE_START | A | - | A:e02 @ 0.70 |  |
| g05 | -4.45 | CLOSING_START | B | A | B:e03 @ 0.70 |  |
| g06 | -4.40 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g07 | -3.80 | STRONG_THROTTLE_START | B | - | B:e05 @ 1.35 |  |
| g08 | -3.75 | CRITICAL_TTC_END | B | A | B:e06 @ 1.40 |  |
| g09 | -3.75 | CLOSING_END | B | A | B:e07 @ 1.40 |  |
| g10 | -3.35 | STRONG_THROTTLE_END | A | - | A:e03 @ 1.80 |  |
| g11 | -2.65 | STRONG_THROTTLE_END | B | - | B:e08 @ 2.50 |  |
| g12 | -1.20 | BRAKE_START | A | - | A:e04 @ 3.95 |  |
| g13 | -0.90 | CLOSING_START | B | A | B:e09 @ 4.25 |  |
| g14 | -0.80 | CRITICAL_TTC_START | B | A | B:e10 @ 4.35 |  |
| g15 | -0.40 | BRAKE_START | B | - | B:e11 @ 4.75 |  |
| g16 | 0.00 | COLLISION | - | A, B | A:e05 @ 5.15, B:e12 @ 5.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 6073.81, B 6073.81 |
| g17 | 0.05 | CRITICAL_TTC_END | B | A | B:e13 @ 5.20 |  |
| g18 | 0.05 | CLOSING_END | B | A | B:e14 @ 5.20 |  |
| g19 | 0.05 | HARD_BRAKE_START | A | - | A:e06 @ 5.20 |  |
| g20 | 0.05 | HARD_BRAKE_START | B | - | B:e15 @ 5.20 |  |
| g21 | 0.45 | MOVING_END | B | - | B:e16 @ 5.60 |  |
| g22 | 0.45 | STOP_START | B | - | B:e17 @ 5.60 |  |
| g23 | 0.60 | MOVING_END | A | - | A:e07 @ 5.75 |  |
| g24 | 0.60 | STOP_START | A | - | A:e08 @ 5.75 |  |
| g25 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g26 | - | MOVING_END | C | - | C:e02 @ 0.30 |  |
| g27 | - | STOP_START | C | - | C:e03 @ 0.30 |  |

## Edges

```
    g01 --PRECEDES--> g04
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g04
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g17
    g03 --SAME_TRACK--> g18
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.15 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,A) |
| -4.45 | STRONG_THROTTLE_START(A); CLOSING_START(B,A) |
| -4.40 | CRITICAL_TTC_START(B,A) |
| -3.80 | STRONG_THROTTLE_START(B) |
| -3.75 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| -3.35 | STRONG_THROTTLE_END(A) |
| -2.65 | STRONG_THROTTLE_END(B) |
| -1.20 | BRAKE_START(A) |
| -0.90 | CLOSING_START(B,A) |
| -0.80 | CRITICAL_TTC_START(B,A) |
| -0.40 | BRAKE_START(B) |
| +0.00 | COLLISION(A,B) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); HARD_BRAKE_START(A); HARD_BRAKE_START(B) |
| +0.45 | MOVING_END(B); STOP_START(B) |
| +0.60 | MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.15 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.15 | B | g02 MOVING_START(B) (B:e01)<br>g03 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -4.45 | A | g04 STRONG_THROTTLE_START(A) (A:e02) | ego: MOVING |
| -4.45 | B | g05 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.40 | B | g06 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.80 | B | g07 STRONG_THROTTLE_START(B) (B:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -3.75 | B | g08 CRITICAL_TTC_END(B,A) (B:e06)<br>g09 CLOSING_END(B,A) (B:e07) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -3.35 | A | g10 STRONG_THROTTLE_END(A) (A:e03) | ego: MOVING, STRONG_THROTTLE |
| -2.65 | B | g11 STRONG_THROTTLE_END(B) (B:e08) | ego: MOVING, STRONG_THROTTLE<br>track_001: IN_EGO_PATH |
| -1.20 | A | g12 BRAKE_START(A) (A:e04) | ego: MOVING |
| -0.90 | B | g13 CLOSING_START(B,A) (B:e09) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -0.80 | B | g14 CRITICAL_TTC_START(B,A) (B:e10) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -0.40 | B | g15 BRAKE_START(B) (B:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g16 COLLISION(A,B) (A:e05) | ego: MOVING, BRAKE |
| +0.00 | B | g16 COLLISION(A,B) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | B | g17 CRITICAL_TTC_END(B,A) (B:e13)<br>g18 CLOSING_END(B,A) (B:e14)<br>g20 HARD_BRAKE_START(B) (B:e15) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g19 HARD_BRAKE_START(A) (A:e06) | ego: MOVING, BRAKE |
| +0.45 | B | g21 MOVING_END(B) (B:e16)<br>g22 STOP_START(B) (B:e17) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH |
| +0.60 | A | g23 MOVING_END(A) (A:e07)<br>g24 STOP_START(A) (A:e08) | ego: MOVING, BRAKE, HARD_BRAKE |
| - | C | g25 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g26 MOVING_END(C) (C:e02)<br>g27 STOP_START(C) (C:e03) | ego: MOVING |

## Plain-language reading

- 5.15 s before the matched collision, A started moving (already the case when first observed).
- 5.15 s before the matched collision, B started moving (already the case when first observed).
- 5.15 s before the matched collision, B's radar started tracking A, which appeared in front of it.
- 4.45 s before the matched collision, A started applying strong throttle.
- 4.45 s before the matched collision, B observed A start closing in.
- 4.40 s before the matched collision, B's time-to-contact with A became critical.
- 3.80 s before the matched collision, B started applying strong throttle.
- 3.75 s before the matched collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the matched collision, B observed A stop closing in.
- 3.35 s before the matched collision, A stopped applying strong throttle.
- 2.65 s before the matched collision, B stopped applying strong throttle.
- 1.20 s before the matched collision, A started braking.
- 0.90 s before the matched collision, B observed A start closing in.
- 0.80 s before the matched collision, B's time-to-contact with A became critical.
- 0.40 s before the matched collision, B started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.60 s after the matched collision, A stopped moving.
- 0.60 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.30 s) C stopped moving.
- (unaligned, C local time 0.30 s) C came to a stop.
