# Global graph - S05/run_0_crash

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
| A | ALIGNED | A:e06 | 3.70 | -3.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e05 | 3.70 | -3.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6116.26 vs 6116.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.93 | A and B both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 3.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.6 m -> 0.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.55 m/s over 3.0 s<br>clearance at the contact 0.27 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.98 | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 3.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.2 m -> 1.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.30 m/s over 3.0 s<br>clearance at the contact 1.45 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.15 | TRACK_APPEARED_LEFT | B | A | B:e02 @ 0.55 |  |
| g04 | -3.15 | CLOSING_START | B | A | B:e03 @ 0.55 | active_at_first_observation=True |
| g05 | -3.00 | TRACK_APPEARED_RIGHT | A | B | A:e02 @ 0.70 |  |
| g06 | -3.00 | CLOSING_START | A | B | A:e03 @ 0.70 | active_at_first_observation=True |
| g07 | -2.05 | CRITICAL_TTC_START | A | B | A:e04 @ 1.65 |  |
| g08 | -2.05 | CRITICAL_TTC_START | B | A | B:e04 @ 1.65 |  |
| g09 | -0.25 | EGO_PATH_ENTRY | A | B | A:e05 @ 3.45 |  |
| g10 | 0.00 | COLLISION | - | A, B | A:e06 @ 3.70, B:e05 @ 3.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 6116.26, B 6116.26 |
| g11 | 0.00 | CRITICAL_TTC_END | A | B | A:e07 @ 3.70 |  |
| g12 | 0.00 | CLOSING_END | A | B | A:e08 @ 3.70 |  |
| g13 | 0.00 | TURN_LEFT_START | B | - | B:e06 @ 3.70 |  |
| g14 | 0.05 | CRITICAL_TTC_END | B | A | B:e07 @ 3.75 |  |
| g15 | 0.05 | CLOSING_END | B | A | B:e08 @ 3.75 |  |
| g16 | 0.05 | BRAKE_START | A | - | A:e09 @ 3.75 |  |
| g17 | 0.05 | BRAKE_START | B | - | B:e09 @ 3.75 |  |
| g18 | 0.10 | EGO_PATH_EXIT | A | B | A:e10 @ 3.80 |  |
| g19 | 0.55 | TURN_LEFT_END | B | - | B:e10 @ 4.25 |  |
| g20 | 0.60 | MOVING_END | B | - | B:e11 @ 4.30 |  |
| g21 | 0.60 | STOP_START | B | - | B:e12 @ 4.30 |  |
| g22 | 0.85 | MOVING_END | A | - | A:e11 @ 4.55 |  |
| g23 | 0.85 | STOP_START | A | - | A:e12 @ 4.55 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g10 --PRECEDES--> g16
    g10 --PRECEDES--> g17
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g11 --PRECEDES--> g16
    g11 --PRECEDES--> g17
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g12 --PRECEDES--> g17
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g07
    g05 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g11
    g05 --SAME_TRACK--> g12
    g05 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g15
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.70 | MOVING_START(A); MOVING_START(B) |
| -3.15 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -3.00 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B) |
| -2.05 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -0.25 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TURN_LEFT_START(B) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_START(A); BRAKE_START(B) |
| +0.10 | EGO_PATH_EXIT(A,B) |
| +0.55 | TURN_LEFT_END(B) |
| +0.60 | MOVING_END(B); STOP_START(B) |
| +0.85 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 1.65, COLLISION with B 3.70 (+2.05 s); EGO_PATH_ENTRY 3.45 after critical TTC (+1.80 s) [local times; t_global: critical_ttc_start -2.05, ego_path_entry -0.25, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 1.65, COLLISION with A 3.70 (+2.05 s) [local times; t_global: critical_ttc_start -2.05, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.70 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -3.70 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.15 | B | g03 TRACK_APPEARED_LEFT(B,A) (B:e02)<br>g04 CLOSING_START(B,A) (B:e03) | ego: MOVING |
| -3.00 | A | g05 TRACK_APPEARED_RIGHT(A,B) (A:e02)<br>g06 CLOSING_START(A,B) (A:e03) | ego: MOVING |
| -2.05 | A | g07 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.05 | B | g08 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -0.25 | A | g09 EGO_PATH_ENTRY(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g10 COLLISION(A,B) (A:e06)<br>g11 CRITICAL_TTC_END(A,B) (A:e07)<br>g12 CLOSING_END(A,B) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g10 COLLISION(A,B) (B:e05)<br>g13 TURN_LEFT_START(B) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.05 | B | g14 CRITICAL_TTC_END(B,A) (B:e07)<br>g15 CLOSING_END(B,A) (B:e08)<br>g17 BRAKE_START(B) (B:e09) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC |
| +0.05 | A | g16 BRAKE_START(A) (A:e09) | ego: MOVING<br>track_001: IN_EGO_PATH |
| +0.10 | A | g18 EGO_PATH_EXIT(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.55 | B | g19 TURN_LEFT_END(B) (B:e10) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state |
| +0.60 | B | g20 MOVING_END(B) (B:e11)<br>g21 STOP_START(B) (B:e12) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.85 | A | g22 MOVING_END(A) (A:e11)<br>g23 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: no active state |

## Plain-language reading

- 3.70 s before the reference collision, A started moving (already the case when first observed).
- 3.70 s before the reference collision, B started moving (already the case when first observed).
- 3.15 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 3.15 s before the reference collision, B observed A start closing in (already the case when first observed).
- 3.00 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 3.00 s before the reference collision, A observed B start closing in (already the case when first observed).
- 2.05 s before the reference collision, A's time-to-contact with B became critical.
- 2.05 s before the reference collision, B's time-to-contact with A became critical.
- 0.25 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 6116, B: 6116 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B started turning left.
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A observed B leave its forward path corridor.
- 0.55 s after the reference collision, B stopped turning left.
- 0.60 s after the reference collision, B stopped moving.
- 0.60 s after the reference collision, B came to a stop.
- 0.85 s after the reference collision, A stopped moving.
- 0.85 s after the reference collision, A came to a stop.
