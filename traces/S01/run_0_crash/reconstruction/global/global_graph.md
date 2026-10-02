# Global graph - S01/run_0_crash

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
| A | ALIGNED | A:e08 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.1 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.15 m/s over 3.0 s<br>clearance at the contact 0.32 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 1.00 | B and A both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.13 m/s over 3.0 s<br>clearance at the contact 0.58 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.50 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.00 |  |
| g04 | -6.50 | TRACK_APPEARED_REAR | B | A | B:e02 @ 0.00 |  |
| g05 | -6.05 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g06 | -6.00 | CLOSING_START | B | A | B:e03 @ 0.50 |  |
| g07 | -4.85 | CLOSING_END | A | B | A:e04 @ 1.65 |  |
| g08 | -4.85 | CLOSING_END | B | A | B:e04 @ 1.65 |  |
| g09 | -2.55 | BRAKE_START | B | - | B:e05 @ 3.95 |  |
| g10 | -2.30 | CLOSING_START | A | B | A:e05 @ 4.20 |  |
| g11 | -2.25 | CLOSING_START | B | A | B:e06 @ 4.25 |  |
| g12 | -1.50 | CRITICAL_TTC_START | A | B | A:e06 @ 5.00 |  |
| g13 | -1.35 | MOVING_END | B | - | B:e07 @ 5.15 |  |
| g14 | -1.35 | STOP_START | B | - | B:e08 @ 5.15 |  |
| g15 | -0.95 | BRAKE_START | A | - | A:e07 @ 5.55 |  |
| g16 | -0.05 | TRACK_LOST | B | A | B:e09 @ 6.45 |  |
| g17 | 0.00 | COLLISION | - | A, B | A:e08 @ 6.50, B:e10 @ 6.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 17663.06, B 17663.06 |
| g18 | 0.00 | CRITICAL_TTC_END | A | B | A:e09 @ 6.50 |  |
| g19 | 0.00 | CLOSING_END | A | B | A:e10 @ 6.50 |  |
| g20 | 0.05 | MOVING_END | A | - | A:e11 @ 6.55 |  |
| g21 | 0.05 | STOP_START | A | - | A:e12 @ 6.55 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
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
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g19
    g04 --SAME_TRACK--> g06
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g11
    g04 --SAME_TRACK--> g16
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.50 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_REAR(B,A) |
| -6.05 | CLOSING_START(A,B) |
| -6.00 | CLOSING_START(B,A) |
| -4.85 | CLOSING_END(A,B); CLOSING_END(B,A) |
| -2.55 | BRAKE_START(B) |
| -2.30 | CLOSING_START(A,B) |
| -2.25 | CLOSING_START(B,A) |
| -1.50 | CRITICAL_TTC_START(A,B) |
| -1.35 | MOVING_END(B); STOP_START(B) |
| -0.95 | BRAKE_START(A) |
| -0.05 | TRACK_LOST(B,A) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.05 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 5.00, COLLISION with B 6.50 (+1.50 s) [local times; t_global: critical_ttc_start -1.50, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.50 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: not yet observed |
| -6.50 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_REAR(B,A) (B:e02) | ego: not yet observed |
| -6.05 | A | g05 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -6.00 | B | g06 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: no active state |
| -4.85 | A | g07 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -4.85 | B | g08 CLOSING_END(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.55 | B | g09 BRAKE_START(B) (B:e05) | ego: MOVING<br>track_001: no active state |
| -2.30 | A | g10 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -2.25 | B | g11 CLOSING_START(B,A) (B:e06) | ego: MOVING, BRAKE<br>track_001: no active state |
| -1.50 | A | g12 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.35 | B | g13 MOVING_END(B) (B:e07)<br>g14 STOP_START(B) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| -0.95 | A | g15 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.05 | B | g16 TRACK_LOST(B,A) (B:e09) | ego: STOP, BRAKE<br>track_001: CLOSING |
| +0.00 | A | g17 COLLISION(A,B) (A:e08)<br>g18 CRITICAL_TTC_END(A,B) (A:e09)<br>g19 CLOSING_END(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g17 COLLISION(A,B) (B:e10) | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001 |
| +0.05 | A | g20 MOVING_END(A) (A:e11)<br>g21 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |

## Plain-language reading

- 6.50 s before the reference collision, A started moving (already the case when first observed).
- 6.50 s before the reference collision, B started moving (already the case when first observed).
- 6.50 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 6.50 s before the reference collision, B's radar started tracking A, which appeared behind it.
- 6.05 s before the reference collision, A observed B start closing in.
- 6.00 s before the reference collision, B observed A start closing in.
- 4.85 s before the reference collision, A observed B stop closing in.
- 4.85 s before the reference collision, B observed A stop closing in.
- 2.55 s before the reference collision, B started braking.
- 2.30 s before the reference collision, A observed B start closing in.
- 2.25 s before the reference collision, B observed A start closing in.
- 1.50 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B stopped moving.
- 1.35 s before the reference collision, B came to a stop.
- 0.95 s before the reference collision, A started braking.
- 0.05 s before the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A stopped moving.
- 0.05 s after the reference collision, A came to a stop.
