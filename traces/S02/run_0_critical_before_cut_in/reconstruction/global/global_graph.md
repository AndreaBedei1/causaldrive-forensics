# Global graph - S02/run_0_critical_before_cut_in

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
| A | ALIGNED | A:e08 | 3.90 | -3.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 3.90 | -3.90 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 406.35 vs 406.35 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 (peak impulse 406.35 vs 406.35 N*s)<br>tracked for 3.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.5 m -> 0.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.65 m/s over 3.0 s<br>clearance at the contact 0.44 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.97 | B and A both reported collision_001 (peak impulse 406.35 vs 406.35 N*s)<br>tracked for 3.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.6 m -> 0.3 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.37 m/s over 3.0 s<br>clearance at the contact 0.35 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.90 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.90 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.90 | TRACK_APPEARED_LEFT | A | B | A:e02 @ 0.00 |  |
| g04 | -3.90 | TRACK_APPEARED_RIGHT | B | A | B:e02 @ 0.00 |  |
| g05 | -3.90 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g06 | -3.90 | CLOSING_START | B | A | B:e03 @ 0.00 | active_at_first_observation=True |
| g07 | -3.10 | CRITICAL_TTC_START | A | B | A:e04 @ 0.80 |  |
| g08 | -2.40 | BRAKE_START | B | - | B:e04 @ 1.50 |  |
| g09 | -2.25 | BRAKE_END | B | - | B:e05 @ 1.65 |  |
| g10 | -1.45 | BRAKE_START | A | - | A:e05 @ 2.45 |  |
| g11 | -1.30 | CUT_IN_FROM_LEFT_START | A | B | A:e06 @ 2.60 |  |
| g12 | -0.70 | BRAKE_END | A | - | A:e07 @ 3.20 |  |
| g13 | 0.00 | COLLISION | - | A, B | A:e08 @ 3.90, B:e06 @ 3.90 | matched_event=collision_001; reference_event=True; peak_impulse=A 406.35, B 406.35 |
| g14 | 0.00 | CUT_IN_FROM_LEFT_END | A | B | A:e09 @ 3.90 |  |
| g15 | 0.05 | CRITICAL_TTC_END | A | B | A:e10 @ 3.95 |  |
| g16 | 0.05 | CLOSING_END | A | B | A:e11 @ 3.95 |  |
| g17 | 0.05 | CLOSING_END | B | A | B:e07 @ 3.95 |  |
| g18 | 0.05 | BRAKE_START | A | - | A:e12 @ 3.95 |  |
| g19 | 0.05 | BRAKE_START | B | - | B:e08 @ 3.95 |  |
| g20 | 0.50 | MOVING_END | B | - | B:e09 @ 4.40 |  |
| g21 | 0.50 | STOP_START | B | - | B:e10 @ 4.40 |  |
| g22 | 0.55 | MOVING_END | A | - | A:e13 @ 4.45 |  |
| g23 | 0.55 | STOP_START | A | - | A:e14 @ 4.45 |  |

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
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g15
    g03 --SAME_TRACK--> g16
    g04 --SAME_TRACK--> g06
    g04 --SAME_TRACK--> g17
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.90 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(B,A); CLOSING_START(A,B); CLOSING_START(B,A) |
| -3.10 | CRITICAL_TTC_START(A,B) |
| -2.40 | BRAKE_START(B) |
| -2.25 | BRAKE_END(B) |
| -1.45 | BRAKE_START(A) |
| -1.30 | CUT_IN_FROM_LEFT_START(A,B) |
| -0.70 | BRAKE_END(A) |
| +0.00 | COLLISION(A,B); CUT_IN_FROM_LEFT_END(A,B) |
| +0.05 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B) |
| +0.50 | MOVING_END(B); STOP_START(B) |
| +0.55 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): critical TTC already active before the cut-in: CRITICAL_TTC_START 0.80 <= CUT_IN_FROM_LEFT_START 2.60 (+1.80 s) [local times; t_global: cut_in -1.30, critical_ttc_start -3.10, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.90 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,B) (A:e02)<br>g05 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -3.90 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_RIGHT(B,A) (B:e02)<br>g06 CLOSING_START(B,A) (B:e03) | ego: not yet observed |
| -3.10 | A | g07 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.40 | B | g08 BRAKE_START(B) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.25 | B | g09 BRAKE_END(B) (B:e05) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| -1.45 | A | g10 BRAKE_START(A) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -1.30 | A | g11 CUT_IN_FROM_LEFT_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC |
| -0.70 | A | g12 BRAKE_END(A) (A:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| +0.00 | A | g13 COLLISION(A,B) (A:e08)<br>g14 CUT_IN_FROM_LEFT_END(A,B) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| +0.00 | B | g13 COLLISION(A,B) (B:e06) | ego: MOVING<br>track_001: CLOSING |
| +0.05 | A | g15 CRITICAL_TTC_END(A,B) (A:e10)<br>g16 CLOSING_END(A,B) (A:e11)<br>g18 BRAKE_START(A) (A:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.05 | B | g17 CLOSING_END(B,A) (B:e07)<br>g19 BRAKE_START(B) (B:e08) | ego: MOVING<br>track_001: CLOSING |
| +0.50 | B | g20 MOVING_END(B) (B:e09)<br>g21 STOP_START(B) (B:e10) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.55 | A | g22 MOVING_END(A) (A:e13)<br>g23 STOP_START(A) (A:e14) | ego: MOVING, BRAKE<br>track_001: no active state |

## Plain-language reading

- 3.90 s before the reference collision, A started moving (already the case when first observed).
- 3.90 s before the reference collision, B started moving (already the case when first observed).
- 3.90 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 3.90 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 3.90 s before the reference collision, A observed B start closing in (already the case when first observed).
- 3.90 s before the reference collision, B observed A start closing in (already the case when first observed).
- 3.10 s before the reference collision, A's time-to-contact with B became critical.
- 2.40 s before the reference collision, B started braking.
- 2.25 s before the reference collision, B released the brake.
- 1.45 s before the reference collision, A started braking.
- 1.30 s before the reference collision, A observed B cutting in from the left.
- 0.70 s before the reference collision, A released the brake.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 406, B: 406 N*s).
- At the reference collision, A observed B's cut-in from the left settle.
- 0.05 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.50 s after the reference collision, B stopped moving.
- 0.50 s after the reference collision, B came to a stop.
- 0.55 s after the reference collision, A stopped moving.
- 0.55 s after the reference collision, A came to a stop.
