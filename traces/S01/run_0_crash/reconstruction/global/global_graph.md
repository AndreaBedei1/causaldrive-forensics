# Global graph - S01/run_0_crash

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
| A | ALIGNED | A:e10 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>at the contact: minimum range 0.78 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.21 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.50 | TRACK_APPEARED | A | B | A:e02 @ 0.00 |  |
| g04 | -6.10 | STRONG_THROTTLE_START | B | - | B:e02 @ 0.40 |  |
| g05 | -6.05 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g06 | -5.35 | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g07 | -5.15 | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g08 | -4.90 | CLOSING_END | A | B | A:e06 @ 1.60 |  |
| g09 | -4.75 | STRONG_THROTTLE_END | B | - | B:e03 @ 1.75 |  |
| g10 | -2.55 | BRAKE_START | B | - | B:e04 @ 3.95 |  |
| g11 | -2.55 | HARD_BRAKE_START | B | - | B:e05 @ 3.95 |  |
| g12 | -2.25 | CLOSING_START | A | B | A:e07 @ 4.25 |  |
| g13 | -1.50 | CRITICAL_TTC_START | A | B | A:e08 @ 5.00 |  |
| g14 | -1.35 | MOVING_END | B | - | B:e06 @ 5.15 |  |
| g15 | -1.35 | STOP_START | B | - | B:e07 @ 5.15 |  |
| g16 | -0.95 | BRAKE_START | A | - | A:e09 @ 5.55 |  |
| g17 | 0.00 | COLLISION | - | A, B | A:e10 @ 6.50, B:e08 @ 6.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 17663.06, B 17663.06 |
| g18 | 0.00 | CRITICAL_TTC_END | A | B | A:e11 @ 6.50 |  |
| g19 | 0.00 | CLOSING_END | A | B | A:e12 @ 6.50 |  |
| g20 | 0.05 | MOVING_END | A | - | A:e13 @ 6.55 |  |
| g21 | 0.05 | STOP_START | A | - | A:e14 @ 6.55 |  |
| g22 | 0.05 | HARD_BRAKE_START | A | - | A:e15 @ 6.55 |  |

## Edges

```
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g19
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.50 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B) |
| -6.10 | STRONG_THROTTLE_START(B) |
| -6.05 | CLOSING_START(A,B) |
| -5.35 | STRONG_THROTTLE_START(A) |
| -5.15 | STRONG_THROTTLE_END(A) |
| -4.90 | CLOSING_END(A,B) |
| -4.75 | STRONG_THROTTLE_END(B) |
| -2.55 | BRAKE_START(B); HARD_BRAKE_START(B) |
| -2.25 | CLOSING_START(A,B) |
| -1.50 | CRITICAL_TTC_START(A,B) |
| -1.35 | MOVING_END(B); STOP_START(B) |
| -0.95 | BRAKE_START(A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.05 | MOVING_END(A); STOP_START(A); HARD_BRAKE_START(A) |

## Plain-language reading

- 6.50 s before the matched collision, A started moving (already the case when first observed).
- 6.50 s before the matched collision, B started moving (already the case when first observed).
- 6.50 s before the matched collision, A's radar started tracking B.
- 6.10 s before the matched collision, B started applying strong throttle.
- 6.05 s before the matched collision, A observed B start closing in.
- 5.35 s before the matched collision, A started applying strong throttle.
- 5.15 s before the matched collision, A stopped applying strong throttle.
- 4.90 s before the matched collision, A observed B stop closing in.
- 4.75 s before the matched collision, B stopped applying strong throttle.
- 2.55 s before the matched collision, B started braking.
- 2.55 s before the matched collision, B started braking hard.
- 2.25 s before the matched collision, A observed B start closing in.
- 1.50 s before the matched collision, A's time-to-contact with B became critical.
- 1.35 s before the matched collision, B stopped moving.
- 1.35 s before the matched collision, B came to a stop.
- 0.95 s before the matched collision, A started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A stopped moving.
- 0.05 s after the matched collision, A came to a stop.
- 0.05 s after the matched collision, A started braking hard.
