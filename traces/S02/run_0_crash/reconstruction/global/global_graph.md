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
| A | ALIGNED | A:e08 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e04 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5953.86 vs 5953.86 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.95 | A and B both reported collision_001 (peak impulse 5953.86 vs 5953.86 N*s)<br>tracked for 4.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 7.4 m -> 0.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.46 m/s over 3.0 s<br>range at the contact 0.93 m<br>the only track of A compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.25 | TRACK_APPEARED_LEFT | A | B | A:e02 @ 0.00 |  |
| g04 | -4.25 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -1.90 | CUT_IN_FROM_LEFT_START | A | B | A:e04 @ 2.35 |  |
| g06 | -1.10 | BRAKE_START | B | - | B:e02 @ 3.15 |  |
| g07 | -1.05 | CRITICAL_TTC_START | A | B | A:e05 @ 3.20 |  |
| g08 | -0.95 | EGO_PATH_ENTRY | A | B | A:e06 @ 3.30 |  |
| g09 | -0.65 | BRAKE_END | B | - | B:e03 @ 3.60 |  |
| g10 | -0.40 | BRAKE_START | A | - | A:e07 @ 3.85 |  |
| g11 | 0.00 | COLLISION | - | A, B | A:e08 @ 4.25, B:e04 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 5953.86, B 5953.86 |
| g12 | 0.00 | CUT_IN_FROM_LEFT_END | A | B | A:e09 @ 4.25 |  |
| g13 | 0.00 | BRAKE_START | B | - | B:e05 @ 4.25 |  |
| g14 | 0.05 | CRITICAL_TTC_END | A | B | A:e10 @ 4.30 |  |
| g15 | 0.05 | CLOSING_END | A | B | A:e11 @ 4.30 |  |
| g16 | 0.60 | MOVING_END | A | - | A:e12 @ 4.85 |  |
| g17 | 0.60 | STOP_START | A | - | A:e13 @ 4.85 |  |
| g18 | 0.75 | MOVING_END | B | - | B:e06 @ 5.00 |  |
| g19 | 0.75 | STOP_START | B | - | B:e07 @ 5.00 |  |

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
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g15
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -1.90 | CUT_IN_FROM_LEFT_START(A,B) |
| -1.10 | BRAKE_START(B) |
| -1.05 | CRITICAL_TTC_START(A,B) |
| -0.95 | EGO_PATH_ENTRY(A,B) |
| -0.65 | BRAKE_END(B) |
| -0.40 | BRAKE_START(A) |
| +0.00 | COLLISION(A,B); CUT_IN_FROM_LEFT_END(A,B); BRAKE_START(B) |
| +0.05 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.60 | MOVING_END(A); STOP_START(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 2.35 < CRITICAL_TTC_START 3.20 (+0.85 s) < COLLISION 4.25 (+1.05 s); EGO_PATH_ENTRY 3.30 after critical TTC (+0.10 s) [local times; t_global: cut_in -1.90, critical_ttc_start -1.05, ego_path_entry -0.95, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,B) (A:e02)<br>g04 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -1.90 | A | g05 CUT_IN_FROM_LEFT_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.10 | B | g06 BRAKE_START(B) (B:e02) | ego: MOVING |
| -1.05 | A | g07 CRITICAL_TTC_START(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| -0.95 | A | g08 EGO_PATH_ENTRY(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| -0.65 | B | g09 BRAKE_END(B) (B:e03) | ego: MOVING, BRAKE |
| -0.40 | A | g10 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | A | g11 COLLISION(A,B) (A:e08)<br>g12 CUT_IN_FROM_LEFT_END(A,B) (A:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g11 COLLISION(A,B) (B:e04)<br>g13 BRAKE_START(B) (B:e05) | ego: MOVING |
| +0.05 | A | g14 CRITICAL_TTC_END(A,B) (A:e10)<br>g15 CLOSING_END(A,B) (A:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.60 | A | g16 MOVING_END(A) (A:e12)<br>g17 STOP_START(A) (A:e13) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.75 | B | g18 MOVING_END(B) (B:e06)<br>g19 STOP_START(B) (B:e07) | ego: MOVING, BRAKE |

## Plain-language reading

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 4.25 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 4.25 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.90 s before the matched collision, A observed B cutting in from the left.
- 1.10 s before the matched collision, B started braking.
- 1.05 s before the matched collision, A's time-to-contact with B became critical.
- 0.95 s before the matched collision, A observed B enter its forward path corridor.
- 0.65 s before the matched collision, B released the brake.
- 0.40 s before the matched collision, A started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5954, B: 5954 N*s).
- At the matched collision, A observed B's cut-in from the left settle.
- At the matched collision, B started braking.
- 0.05 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the matched collision, A observed B stop closing in.
- 0.60 s after the matched collision, A stopped moving.
- 0.60 s after the matched collision, A came to a stop.
- 0.75 s after the matched collision, B stopped moving.
- 0.75 s after the matched collision, B came to a stop.
