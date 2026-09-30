# Global graph - S13/run_0_cut_in

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
| A | ALIGNED | A:e07 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 3184.37 vs 3184.37 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 5.25 s before the matched collision<br>at the contact: minimum range 1.19 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.36 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.25 | TRACK_APPEARED | A | B | A:e02 @ 0.00 |  |
| g04 | -5.25 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -4.45 | BRAKE_START | B | - | B:e02 @ 0.80 |  |
| g06 | -2.40 | BRAKE_START | A | - | A:e04 @ 2.85 |  |
| g07 | -1.60 | CRITICAL_TTC_START | A | B | A:e05 @ 3.65 |  |
| g08 | -0.45 | EGO_PATH_ENTRY | A | B | A:e06 @ 4.80 |  |
| g09 | 0.00 | COLLISION | - | A, B | A:e07 @ 5.25, B:e03 @ 5.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 3184.37, B 3184.37 |
| g10 | 0.00 | CRITICAL_TTC_END | A | B | A:e08 @ 5.25 |  |
| g11 | 0.00 | HARD_BRAKE_START | B | - | B:e04 @ 5.25 |  |
| g12 | 0.05 | CLOSING_END | A | B | A:e09 @ 5.30 |  |
| g13 | 0.05 | HARD_BRAKE_START | A | - | A:e10 @ 5.30 |  |
| g14 | 1.15 | MOVING_END | A | - | A:e11 @ 6.40 |  |
| g15 | 1.15 | STOP_START | A | - | A:e12 @ 6.40 |  |
| g16 | 1.20 | MOVING_END | B | - | B:e05 @ 6.45 |  |
| g17 | 1.20 | STOP_START | B | - | B:e06 @ 6.45 |  |

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
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g12
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B) |
| -4.45 | BRAKE_START(B) |
| -2.40 | BRAKE_START(A) |
| -1.60 | CRITICAL_TTC_START(A,B) |
| -0.45 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); HARD_BRAKE_START(B) |
| +0.05 | CLOSING_END(A,B); HARD_BRAKE_START(A) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +1.20 | MOVING_END(B); STOP_START(B) |

## Plain-language reading

- 5.25 s before the matched collision, A started moving (already the case when first observed).
- 5.25 s before the matched collision, B started moving (already the case when first observed).
- 5.25 s before the matched collision, A's radar started tracking B.
- 5.25 s before the matched collision, A observed B start closing in (already the case when first observed).
- 4.45 s before the matched collision, B started braking.
- 2.40 s before the matched collision, A started braking.
- 1.60 s before the matched collision, A's time-to-contact with B became critical.
- 0.45 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 3184, B: 3184 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, B started braking hard.
- 0.05 s after the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A started braking hard.
- 1.15 s after the matched collision, A stopped moving.
- 1.15 s after the matched collision, A came to a stop.
- 1.20 s after the matched collision, B stopped moving.
- 1.20 s after the matched collision, B came to a stop.
