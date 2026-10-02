# Global graph - S09/run_0_merge_conflict

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
| A | ALIGNED | A:e07 | 1.80 | -1.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e09 | 1.80 | -1.80 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1247.19 vs 1247.19 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.85 | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.6 m -> 1.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.86 m/s over 1.8 s<br>clearance at the contact 0.99 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.99 | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.4 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.22 m/s over 1.8 s<br>clearance at the contact 0.74 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -1.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -1.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -1.80 | TURN_LEFT_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -1.80 | TURN_RIGHT_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -1.80 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 0.00 |  |
| g06 | -1.80 | TRACK_APPEARED_RIGHT | A | B | A:e03 @ 0.00 |  |
| g07 | -1.80 | CLOSING_START | A | B | A:e04 @ 0.00 | active_at_first_observation=True |
| g08 | -1.80 | CLOSING_START | B | A | B:e04 @ 0.00 | active_at_first_observation=True |
| g09 | -1.80 | CRITICAL_TTC_START | A | B | A:e05 @ 0.00 | active_at_first_observation=True |
| g10 | -1.80 | CRITICAL_TTC_START | B | A | B:e05 @ 0.00 | active_at_first_observation=True |
| g11 | -0.95 | CRITICAL_TTC_END | B | A | B:e06 @ 0.85 |  |
| g12 | -0.60 | TURN_RIGHT_END | B | - | B:e07 @ 1.20 |  |
| g13 | -0.35 | CRITICAL_TTC_START | B | A | B:e08 @ 1.45 |  |
| g14 | -0.15 | CRITICAL_TTC_END | A | B | A:e06 @ 1.65 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e07 @ 1.80, B:e09 @ 1.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 1247.19, B 1247.19 |
| g16 | 0.00 | CRITICAL_TTC_END | B | A | B:e10 @ 1.80 |  |
| g17 | 0.00 | CLOSING_END | A | B | A:e08 @ 1.80 |  |
| g18 | 0.00 | CLOSING_END | B | A | B:e11 @ 1.80 |  |
| g19 | 0.05 | BRAKE_START | A | - | A:e09 @ 1.85 |  |
| g20 | 0.05 | BRAKE_START | B | - | B:e12 @ 1.85 |  |
| g21 | 0.05 | TURN_LEFT_START | B | - | B:e13 @ 1.85 |  |
| g22 | 0.65 | TURN_LEFT_END | A | - | A:e10 @ 2.45 |  |
| g23 | 0.70 | TURN_LEFT_END | B | - | B:e14 @ 2.50 |  |
| g24 | 0.70 | MOVING_END | A | - | A:e11 @ 2.50 |  |
| g25 | 0.70 | STOP_START | A | - | A:e12 @ 2.50 |  |
| g26 | 0.75 | MOVING_END | B | - | B:e15 @ 2.55 |  |
| g27 | 0.75 | STOP_START | B | - | B:e16 @ 2.55 |  |

## Edges

```
    g01 --PRECEDES--> g11
    g02 --PRECEDES--> g11
    g03 --PRECEDES--> g11
    g04 --PRECEDES--> g11
    g05 --PRECEDES--> g11
    g06 --PRECEDES--> g11
    g07 --PRECEDES--> g11
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g22
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g09
    g06 --SAME_TRACK--> g14
    g06 --SAME_TRACK--> g17
    g05 --SAME_TRACK--> g08
    g05 --SAME_TRACK--> g10
    g05 --SAME_TRACK--> g11
    g05 --SAME_TRACK--> g13
    g05 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g18
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -1.80 | MOVING_START(A); MOVING_START(B); TURN_LEFT_START(A); TURN_RIGHT_START(B); TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -0.95 | CRITICAL_TTC_END(B,A) |
| -0.60 | TURN_RIGHT_END(B) |
| -0.35 | CRITICAL_TTC_START(B,A) |
| -0.15 | CRITICAL_TTC_END(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A) |
| +0.05 | BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B) |
| +0.65 | TURN_LEFT_END(A) |
| +0.70 | TURN_LEFT_END(B); MOVING_END(A); STOP_START(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 0.00, COLLISION with B 1.80 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.00, COLLISION with A 1.80 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -1.80 | A | g01 MOVING_START(A) (A:e01)<br>g03 TURN_LEFT_START(A) (A:e02)<br>g06 TRACK_APPEARED_RIGHT(A,B) (A:e03)<br>g07 CLOSING_START(A,B) (A:e04)<br>g09 CRITICAL_TTC_START(A,B) (A:e05) | ego: not yet observed |
| -1.80 | B | g02 MOVING_START(B) (B:e01)<br>g04 TURN_RIGHT_START(B) (B:e02)<br>g05 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g08 CLOSING_START(B,A) (B:e04)<br>g10 CRITICAL_TTC_START(B,A) (B:e05) | ego: not yet observed |
| -0.95 | B | g11 CRITICAL_TTC_END(B,A) (B:e06) | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC |
| -0.60 | B | g12 TURN_RIGHT_END(B) (B:e07) | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING |
| -0.35 | B | g13 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING |
| -0.15 | A | g14 CRITICAL_TTC_END(A,B) (A:e06) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g15 COLLISION(A,B) (A:e07)<br>g17 CLOSING_END(A,B) (A:e08) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING |
| +0.00 | B | g15 COLLISION(A,B) (B:e09)<br>g16 CRITICAL_TTC_END(B,A) (B:e10)<br>g18 CLOSING_END(B,A) (B:e11) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.05 | A | g19 BRAKE_START(A) (A:e09) | ego: MOVING, TURN_LEFT<br>track_001: no active state |
| +0.05 | B | g20 BRAKE_START(B) (B:e12)<br>g21 TURN_LEFT_START(B) (B:e13) | ego: MOVING<br>track_001: no active state |
| +0.65 | A | g22 TURN_LEFT_END(A) (A:e10) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state |
| +0.70 | B | g23 TURN_LEFT_END(B) (B:e14) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state |
| +0.70 | A | g24 MOVING_END(A) (A:e11)<br>g25 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.75 | B | g26 MOVING_END(B) (B:e15)<br>g27 STOP_START(B) (B:e16) | ego: MOVING, BRAKE<br>track_001: no active state |

## Plain-language reading

- 1.80 s before the reference collision, A started moving (already the case when first observed).
- 1.80 s before the reference collision, B started moving (already the case when first observed).
- 1.80 s before the reference collision, A started turning left (already the case when first observed).
- 1.80 s before the reference collision, B started turning right (already the case when first observed).
- 1.80 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.80 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.80 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the reference collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.80 s before the reference collision, B's time-to-contact with A became critical (already the case when first observed).
- 0.95 s before the reference collision, B's time-to-contact with A stopped being critical.
- 0.60 s before the reference collision, B stopped turning right.
- 0.35 s before the reference collision, B's time-to-contact with A became critical.
- 0.15 s before the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1247, B: 1247 N*s).
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B started turning left.
- 0.65 s after the reference collision, A stopped turning left.
- 0.70 s after the reference collision, B stopped turning left.
- 0.70 s after the reference collision, A stopped moving.
- 0.70 s after the reference collision, A came to a stop.
- 0.75 s after the reference collision, B stopped moving.
- 0.75 s after the reference collision, B came to a stop.
