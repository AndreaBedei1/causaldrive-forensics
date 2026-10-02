# Global graph - S02/run_0_crash

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
| A | ALIGNED | A:e08 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5953.86 vs 5953.86 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.95 | A and B both reported collision_001 (peak impulse 5953.86 vs 5953.86 N*s)<br>tracked for 4.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 7.0 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.50 m/s over 3.0 s<br>clearance at the contact 0.19 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.99 | B and A both reported collision_001 (peak impulse 5953.86 vs 5953.86 N*s)<br>tracked for 4.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 7.2 m -> 0.8 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.18 m/s over 3.0 s<br>clearance at the contact 0.75 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -4.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -4.25 | TRACK_APPEARED_LEFT | A | B | A:e02 @ 0.00 |  |
| g04 | -4.25 | TRACK_APPEARED_RIGHT | B | A | B:e02 @ 0.00 |  |
| g05 | -4.25 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g06 | -4.25 | CLOSING_START | B | A | B:e03 @ 0.00 | active_at_first_observation=True |
| g07 | -1.85 | CUT_IN_FROM_LEFT_START | A | B | A:e04 @ 2.40 |  |
| g08 | -1.15 | CRITICAL_TTC_START | A | B | A:e05 @ 3.10 |  |
| g09 | -1.10 | BRAKE_START | B | - | B:e04 @ 3.15 |  |
| g10 | -0.90 | EGO_PATH_ENTRY | A | B | A:e06 @ 3.35 |  |
| g11 | -0.65 | BRAKE_END | B | - | B:e05 @ 3.60 |  |
| g12 | -0.40 | BRAKE_START | A | - | A:e07 @ 3.85 |  |
| g13 | 0.00 | COLLISION | - | A, B | A:e08 @ 4.25, B:e06 @ 4.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 5953.86, B 5953.86 |
| g14 | 0.00 | CLOSING_END | B | A | B:e07 @ 4.25 |  |
| g15 | 0.00 | BRAKE_START | B | - | B:e08 @ 4.25 |  |
| g16 | 0.05 | CRITICAL_TTC_END | A | B | A:e09 @ 4.30 |  |
| g17 | 0.05 | CLOSING_END | A | B | A:e10 @ 4.30 |  |
| g18 | 0.60 | MOVING_END | A | - | A:e11 @ 4.85 |  |
| g19 | 0.60 | STOP_START | A | - | A:e12 @ 4.85 |  |
| g20 | 0.75 | MOVING_END | B | - | B:e09 @ 5.00 |  |
| g21 | 0.75 | STOP_START | B | - | B:e10 @ 5.00 |  |
| g22 | 0.95 | CUT_IN_FROM_LEFT_END | A | B | A:e13 @ 5.20 |  |

## Edges

```
    g01 --PRECEDES--> g07
    g02 --PRECEDES--> g07
    g03 --PRECEDES--> g07
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g22
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g16
    g03 --SAME_TRACK--> g17
    g03 --SAME_TRACK--> g22
    g04 --SAME_TRACK--> g06
    g04 --SAME_TRACK--> g14
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -4.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A) |
| -1.85 | CUT_IN_FROM_LEFT_START(A,B) |
| -1.15 | CRITICAL_TTC_START(A,B) |
| -1.10 | BRAKE_START(B) |
| -0.90 | EGO_PATH_ENTRY(A,B) |
| -0.65 | BRAKE_END(B) |
| -0.40 | BRAKE_START(A) |
| +0.00 | COLLISION(A,B); CLOSING_END(B,A); BRAKE_START(B) |
| +0.05 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.60 | MOVING_END(A); STOP_START(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |
| +0.95 | CUT_IN_FROM_LEFT_END(A,B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 2.40 < CRITICAL_TTC_START 3.10 (+0.70 s) < COLLISION with B 4.25 (+1.15 s); EGO_PATH_ENTRY 3.35 after critical TTC (+0.25 s) [local times; t_global: cut_in -1.85, critical_ttc_start -1.15, ego_path_entry -0.90, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -4.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,B) (A:e02)<br>g05 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -4.25 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_RIGHT(B,A) (B:e02)<br>g06 CLOSING_START(B,A) (B:e03) | ego: not yet observed |
| -1.85 | A | g07 CUT_IN_FROM_LEFT_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.15 | A | g08 CRITICAL_TTC_START(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| -1.10 | B | g09 BRAKE_START(B) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -0.90 | A | g10 EGO_PATH_ENTRY(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| -0.65 | B | g11 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| -0.40 | A | g12 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | A | g13 COLLISION(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g13 COLLISION(A,B) (B:e06)<br>g14 CLOSING_END(B,A) (B:e07)<br>g15 BRAKE_START(B) (B:e08) | ego: MOVING<br>track_001: CLOSING |
| +0.05 | A | g16 CRITICAL_TTC_END(A,B) (A:e09)<br>g17 CLOSING_END(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.60 | A | g18 MOVING_END(A) (A:e11)<br>g19 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.75 | B | g20 MOVING_END(B) (B:e09)<br>g21 STOP_START(B) (B:e10) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.95 | A | g22 CUT_IN_FROM_LEFT_END(A,B) (A:e13) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |

## Plain-language reading

- 4.25 s before the reference collision, A started moving (already the case when first observed).
- 4.25 s before the reference collision, B started moving (already the case when first observed).
- 4.25 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 4.25 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.25 s before the reference collision, A observed B start closing in (already the case when first observed).
- 4.25 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.85 s before the reference collision, A observed B cutting in from the left.
- 1.15 s before the reference collision, A's time-to-contact with B became critical.
- 1.10 s before the reference collision, B started braking.
- 0.90 s before the reference collision, A observed B enter its forward path corridor.
- 0.65 s before the reference collision, B released the brake.
- 0.40 s before the reference collision, A started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 5954, B: 5954 N*s).
- At the reference collision, B observed A stop closing in.
- At the reference collision, B started braking.
- 0.05 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.60 s after the reference collision, A stopped moving.
- 0.60 s after the reference collision, A came to a stop.
- 0.75 s after the reference collision, B stopped moving.
- 0.75 s after the reference collision, B came to a stop.
- 0.95 s after the reference collision, A observed B's cut-in from the left settle.
