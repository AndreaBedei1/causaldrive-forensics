# Global graph - S13/run_0_cut_in

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
| A | ALIGNED | A:e08 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e05 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 3184.37 vs 3184.37 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 5.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 4.4 m -> 0.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.34 m/s over 3.0 s<br>clearance at the contact 0.50 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.99 | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 5.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 4.7 m -> 0.8 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.18 m/s over 3.0 s<br>clearance at the contact 0.77 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.25 | TRACK_APPEARED_LEFT | A | B | A:e02 @ 0.00 |  |
| g04 | -5.25 | TRACK_APPEARED_RIGHT | B | A | B:e02 @ 0.00 |  |
| g05 | -5.25 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g06 | -5.25 | CLOSING_START | B | A | B:e03 @ 0.00 | active_at_first_observation=True |
| g07 | -4.45 | BRAKE_START | B | - | B:e04 @ 0.80 |  |
| g08 | -2.40 | BRAKE_START | A | - | A:e04 @ 2.85 |  |
| g09 | -1.40 | CRITICAL_TTC_START | A | B | A:e05 @ 3.85 |  |
| g10 | -1.25 | CUT_IN_FROM_LEFT_START | A | B | A:e06 @ 4.00 |  |
| g11 | -0.25 | EGO_PATH_ENTRY | A | B | A:e07 @ 5.00 |  |
| g12 | 0.00 | COLLISION | - | A, B | A:e08 @ 5.25, B:e05 @ 5.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 3184.37, B 3184.37 |
| g13 | 0.00 | CRITICAL_TTC_END | A | B | A:e09 @ 5.25 |  |
| g14 | 0.00 | CLOSING_END | A | B | A:e10 @ 5.25 |  |
| g15 | 0.00 | CLOSING_END | B | A | B:e06 @ 5.25 |  |
| g16 | 0.20 | TURN_RIGHT_START | B | - | B:e07 @ 5.45 |  |
| g17 | 1.15 | TURN_RIGHT_END | B | - | B:e08 @ 6.40 |  |
| g18 | 1.15 | MOVING_END | A | - | A:e11 @ 6.40 |  |
| g19 | 1.15 | STOP_START | A | - | A:e12 @ 6.40 |  |
| g20 | 1.20 | MOVING_END | B | - | B:e09 @ 6.45 |  |
| g21 | 1.20 | STOP_START | B | - | B:e10 @ 6.45 |  |
| g22 | 1.60 | CUT_IN_FROM_LEFT_END | A | B | A:e13 @ 6.85 |  |

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
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g22
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g22
    g04 --SAME_TRACK--> g06
    g04 --SAME_TRACK--> g15
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A) |
| -4.45 | BRAKE_START(B) |
| -2.40 | BRAKE_START(A) |
| -1.40 | CRITICAL_TTC_START(A,B) |
| -1.25 | CUT_IN_FROM_LEFT_START(A,B) |
| -0.25 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,A) |
| +0.20 | TURN_RIGHT_START(B) |
| +1.15 | TURN_RIGHT_END(B); MOVING_END(A); STOP_START(A) |
| +1.20 | MOVING_END(B); STOP_START(B) |
| +1.60 | CUT_IN_FROM_LEFT_END(A,B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): critical TTC already active before the cut-in: CRITICAL_TTC_START 3.85 <= CUT_IN_FROM_LEFT_START 4.00 (+0.15 s); EGO_PATH_ENTRY 5.00 after critical TTC (+1.15 s) [local times; t_global: cut_in -1.25, critical_ttc_start -1.40, ego_path_entry -0.25, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,B) (A:e02)<br>g05 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -5.25 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_RIGHT(B,A) (B:e02)<br>g06 CLOSING_START(B,A) (B:e03) | ego: not yet observed |
| -4.45 | B | g07 BRAKE_START(B) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.40 | A | g08 BRAKE_START(A) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.40 | A | g09 CRITICAL_TTC_START(A,B) (A:e05) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| -1.25 | A | g10 CUT_IN_FROM_LEFT_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC |
| -0.25 | A | g11 EGO_PATH_ENTRY(A,B) (A:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| +0.00 | A | g12 COLLISION(A,B) (A:e08)<br>g13 CRITICAL_TTC_END(A,B) (A:e09)<br>g14 CLOSING_END(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g12 COLLISION(A,B) (B:e05)<br>g15 CLOSING_END(B,A) (B:e06) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| +0.20 | B | g16 TURN_RIGHT_START(B) (B:e07) | ego: MOVING, BRAKE<br>track_001: no active state |
| +1.15 | B | g17 TURN_RIGHT_END(B) (B:e08) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: no active state |
| +1.15 | A | g18 MOVING_END(A) (A:e11)<br>g19 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +1.20 | B | g20 MOVING_END(B) (B:e09)<br>g21 STOP_START(B) (B:e10) | ego: MOVING, BRAKE<br>track_001: no active state |
| +1.60 | A | g22 CUT_IN_FROM_LEFT_END(A,B) (A:e13) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |

## Plain-language reading

- 5.25 s before the reference collision, A started moving (already the case when first observed).
- 5.25 s before the reference collision, B started moving (already the case when first observed).
- 5.25 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 5.25 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 5.25 s before the reference collision, A observed B start closing in (already the case when first observed).
- 5.25 s before the reference collision, B observed A start closing in (already the case when first observed).
- 4.45 s before the reference collision, B started braking.
- 2.40 s before the reference collision, A started braking.
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.25 s before the reference collision, A observed B cutting in from the left.
- 0.25 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 3184, B: 3184 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.20 s after the reference collision, B started turning right.
- 1.15 s after the reference collision, B stopped turning right.
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.20 s after the reference collision, B stopped moving.
- 1.20 s after the reference collision, B came to a stop.
- 1.60 s after the reference collision, A observed B's cut-in from the left settle.
