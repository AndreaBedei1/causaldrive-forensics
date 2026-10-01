# Global graph - S01/run_0_crash

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e05 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.5 m -> 0.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.24 m/s over 3.0 s<br>range at the contact 0.77 m<br>the only track of A compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.40 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.10 |  |
| g04 | -6.05 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g05 | -4.90 | CLOSING_END | A | B | A:e04 @ 1.60 |  |
| g06 | -2.55 | BRAKE_START | B | - | B:e02 @ 3.95 |  |
| g07 | -2.25 | CLOSING_START | A | B | A:e05 @ 4.25 |  |
| g08 | -1.50 | CRITICAL_TTC_START | A | B | A:e06 @ 5.00 |  |
| g09 | -1.35 | MOVING_END | B | - | B:e03 @ 5.15 |  |
| g10 | -1.35 | STOP_START | B | - | B:e04 @ 5.15 |  |
| g11 | -0.95 | BRAKE_START | A | - | A:e07 @ 5.55 |  |
| g12 | 0.00 | COLLISION | - | A, B | A:e08 @ 6.50, B:e05 @ 6.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 17663.06, B 17663.06 |
| g13 | 0.00 | CRITICAL_TTC_END | A | B | A:e09 @ 6.50 |  |
| g14 | 0.00 | CLOSING_END | A | B | A:e10 @ 6.50 |  |
| g15 | 0.05 | MOVING_END | A | - | A:e11 @ 6.55 |  |
| g16 | 0.05 | STOP_START | A | - | A:e12 @ 6.55 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.50 | MOVING_START(A); MOVING_START(B) |
| -6.40 | TRACK_APPEARED_FRONT(A,B) |
| -6.05 | CLOSING_START(A,B) |
| -4.90 | CLOSING_END(A,B) |
| -2.55 | BRAKE_START(B) |
| -2.25 | CLOSING_START(A,B) |
| -1.50 | CRITICAL_TTC_START(A,B) |
| -1.35 | MOVING_END(B); STOP_START(B) |
| -0.95 | BRAKE_START(A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.05 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 5.00, COLLISION with B 6.50 (+1.50 s) [local times; t_global: critical_ttc_start -1.50, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.50 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -6.50 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -6.40 | A | g03 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: MOVING |
| -6.05 | A | g04 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.90 | A | g05 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -2.55 | B | g06 BRAKE_START(B) (B:e02) | ego: MOVING |
| -2.25 | A | g07 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -1.50 | A | g08 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.35 | B | g09 MOVING_END(B) (B:e03)<br>g10 STOP_START(B) (B:e04) | ego: MOVING, BRAKE |
| -0.95 | A | g11 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g12 COLLISION(A,B) (A:e08)<br>g13 CRITICAL_TTC_END(A,B) (A:e09)<br>g14 CLOSING_END(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g12 COLLISION(A,B) (B:e05) | ego: STOP, BRAKE |
| +0.05 | A | g15 MOVING_END(A) (A:e11)<br>g16 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |

## Plain-language reading

- 6.50 s before the reference collision, A started moving (already the case when first observed).
- 6.50 s before the reference collision, B started moving (already the case when first observed).
- 6.40 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 6.05 s before the reference collision, A observed B start closing in.
- 4.90 s before the reference collision, A observed B stop closing in.
- 2.55 s before the reference collision, B started braking.
- 2.25 s before the reference collision, A observed B start closing in.
- 1.50 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B stopped moving.
- 1.35 s before the reference collision, B came to a stop.
- 0.95 s before the reference collision, A started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A stopped moving.
- 0.05 s after the reference collision, A came to a stop.
