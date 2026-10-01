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
| A | ALIGNED | A:e09 | 5.25 | -5.25 | reported the reference collision collision_001 |
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
| g07 | -1.65 | PREDICTED_PATH_CONFLICT_START | A | B | A:e05 @ 3.60 |  |
| g08 | -1.60 | CRITICAL_TTC_START | A | B | A:e06 @ 3.65 |  |
| g09 | -1.35 | CUT_IN_FROM_LEFT_START | A | B | A:e07 @ 3.90 |  |
| g10 | -0.45 | EGO_PATH_ENTRY | A | B | A:e08 @ 4.80 |  |
| g11 | 0.00 | COLLISION | - | A, B | A:e09 @ 5.25, B:e03 @ 5.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 3184.37, B 3184.37 |
| g12 | 0.00 | CRITICAL_TTC_END | A | B | A:e10 @ 5.25 |  |
| g13 | 0.00 | HARD_BRAKE_START | B | - | B:e04 @ 5.25 |  |
| g14 | 0.05 | CLOSING_END | A | B | A:e11 @ 5.30 |  |
| g15 | 0.05 | HARD_BRAKE_START | A | - | A:e12 @ 5.30 |  |
| g16 | 1.10 | PREDICTED_PATH_CONFLICT_END | A | B | A:e13 @ 6.35 |  |
| g17 | 1.15 | MOVING_END | A | - | A:e14 @ 6.40 |  |
| g18 | 1.15 | STOP_START | A | - | A:e15 @ 6.40 |  |
| g19 | 1.20 | MOVING_END | B | - | B:e05 @ 6.45 |  |
| g20 | 1.20 | STOP_START | B | - | B:e06 @ 6.45 |  |
| g21 | 1.40 | CUT_IN_FROM_LEFT_END | A | B | A:e16 @ 6.65 |  |

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
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g16
    g03 --SAME_TRACK--> g21
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B) |
| -4.45 | BRAKE_START(B) |
| -2.40 | BRAKE_START(A) |
| -1.65 | PREDICTED_PATH_CONFLICT_START(A,B) |
| -1.60 | CRITICAL_TTC_START(A,B) |
| -1.35 | CUT_IN_FROM_LEFT_START(A,B) |
| -0.45 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); HARD_BRAKE_START(B) |
| +0.05 | CLOSING_END(A,B); HARD_BRAKE_START(A) |
| +1.10 | PREDICTED_PATH_CONFLICT_END(A,B) |
| +1.15 | MOVING_END(A); STOP_START(A) |
| +1.20 | MOVING_END(B); STOP_START(B) |
| +1.40 | CUT_IN_FROM_LEFT_END(A,B) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED(A,B) (A:e02)<br>g04 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -5.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.45 | B | g05 BRAKE_START(B) (B:e02) | ego: MOVING |
| -2.40 | A | g06 BRAKE_START(A) (A:e04) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| -1.65 | A | g07 PREDICTED_PATH_CONFLICT_START(A,B) (A:e05) | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING |
| -1.60 | A | g08 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT |
| -1.35 | A | g09 CUT_IN_FROM_LEFT_START(A,B) (A:e07) | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT |
| -0.45 | A | g10 EGO_PATH_ENTRY(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| +0.00 | A | g11 COLLISION(A,B) (A:e09)<br>g12 CRITICAL_TTC_END(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| +0.00 | B | g11 COLLISION(A,B) (B:e03)<br>g13 HARD_BRAKE_START(B) (B:e04) | ego: MOVING, BRAKE |
| +0.05 | A | g14 CLOSING_END(A,B) (A:e11)<br>g15 HARD_BRAKE_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| +1.10 | A | g16 PREDICTED_PATH_CONFLICT_END(A,B) (A:e13) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT, CUT_IN_FROM_LEFT |
| +1.15 | A | g17 MOVING_END(A) (A:e14)<br>g18 STOP_START(A) (A:e15) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +1.20 | B | g19 MOVING_END(B) (B:e05)<br>g20 STOP_START(B) (B:e06) | ego: MOVING, BRAKE, HARD_BRAKE |
| +1.40 | A | g21 CUT_IN_FROM_LEFT_END(A,B) (A:e16) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, CUT_IN_FROM_LEFT |

## Plain-language reading

- 5.25 s before the matched collision, A started moving (already the case when first observed).
- 5.25 s before the matched collision, B started moving (already the case when first observed).
- 5.25 s before the matched collision, A's radar started tracking B.
- 5.25 s before the matched collision, A observed B start closing in (already the case when first observed).
- 4.45 s before the matched collision, B started braking.
- 2.40 s before the matched collision, A started braking.
- 1.65 s before the matched collision, A predicted a path conflict with B (close approach ahead if both keep their motion).
- 1.60 s before the matched collision, A's time-to-contact with B became critical.
- 1.35 s before the matched collision, A observed B cutting in from the left.
- 0.45 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 3184, B: 3184 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, B started braking hard.
- 0.05 s after the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A started braking hard.
- 1.10 s after the matched collision, A stopped predicting a path conflict with B.
- 1.15 s after the matched collision, A stopped moving.
- 1.15 s after the matched collision, A came to a stop.
- 1.20 s after the matched collision, B stopped moving.
- 1.20 s after the matched collision, B came to a stop.
- 1.40 s after the matched collision, A observed B's cut-in from the left settle.
