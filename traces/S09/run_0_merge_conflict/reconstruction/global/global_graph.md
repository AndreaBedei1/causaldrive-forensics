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
| A | ALIGNED | A:e10 | 10.25 | -10.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 10.25 | -10.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1904.84 vs 1904.84 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.93 | A and B both reported collision_001 (peak impulse 1904.84 vs 1904.84 N*s)<br>tracked for 7.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.7 m -> 0.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.58 m/s over 3.0 s<br>clearance at the contact 0.94 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.90 | B and A both reported collision_001 (peak impulse 1904.84 vs 1904.84 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.8 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.70 m/s over 3.0 s<br>clearance at the contact 0.47 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -10.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -10.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -10.25 | THROTTLE_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -10.25 | THROTTLE_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -10.25 | TURN_LEFT_START | A | - | A:e03 @ 0.00 | active_at_first_observation=True |
| g06 | -7.70 | TRACK_APPEARED_LEFT | B | A | B:e03 @ 2.55 |  |
| g07 | -7.70 | CLOSING_START | B | A | B:e04 @ 2.55 | active_at_first_observation=True |
| g08 | -7.50 | TRACK_APPEARED_LEFT | A | B | A:e04 @ 2.75 |  |
| g09 | -7.50 | CLOSING_START | A | B | A:e05 @ 2.75 | active_at_first_observation=True |
| g10 | -4.95 | EGO_PATH_ENTRY | A | B | A:e06 @ 5.30 |  |
| g11 | -4.70 | EGO_PATH_EXIT | A | B | A:e07 @ 5.55 |  |
| g12 | -3.60 | CRITICAL_TTC_START | B | A | B:e05 @ 6.65 |  |
| g13 | -3.35 | CRITICAL_TTC_START | A | B | A:e08 @ 6.90 |  |
| g14 | -2.05 | TURN_RIGHT_START | B | - | B:e06 @ 8.20 |  |
| g15 | -0.80 | CRITICAL_TTC_END | A | B | A:e09 @ 9.45 |  |
| g16 | -0.30 | TURN_RIGHT_END | B | - | B:e07 @ 9.95 |  |
| g17 | 0.00 | COLLISION | - | A, B | A:e10 @ 10.25, B:e08 @ 10.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 1904.84, B 1904.84 |
| g18 | 0.00 | CRITICAL_TTC_END | B | A | B:e09 @ 10.25 |  |
| g19 | 0.00 | CLOSING_END | A | B | A:e11 @ 10.25 |  |
| g20 | 0.00 | CLOSING_END | B | A | B:e10 @ 10.25 |  |
| g21 | 0.05 | THROTTLE_END | A | - | A:e12 @ 10.30 |  |
| g22 | 0.05 | THROTTLE_END | B | - | B:e11 @ 10.30 |  |
| g23 | 0.05 | BRAKE_START | A | - | A:e13 @ 10.30 |  |
| g24 | 0.05 | BRAKE_START | B | - | B:e12 @ 10.30 |  |
| g25 | 0.30 | TURN_LEFT_END | A | - | A:e14 @ 10.55 |  |
| g26 | 0.75 | MOVING_END | B | - | B:e13 @ 11.00 |  |
| g27 | 0.75 | STOP_START | B | - | B:e14 @ 11.00 |  |
| g28 | 0.80 | MOVING_END | A | - | A:e15 @ 11.05 |  |
| g29 | 0.80 | STOP_START | A | - | A:e16 @ 11.05 |  |

## Edges

```
    g01 --PRECEDES--> g06
    g01 --PRECEDES--> g07
    g02 --PRECEDES--> g06
    g02 --PRECEDES--> g07
    g03 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g18 --PRECEDES--> g24
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g10
    g08 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g15
    g08 --SAME_TRACK--> g19
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g12
    g06 --SAME_TRACK--> g18
    g06 --SAME_TRACK--> g20
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -10.25 | MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TURN_LEFT_START(A) |
| -7.70 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -7.50 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -4.95 | EGO_PATH_ENTRY(A,B) |
| -4.70 | EGO_PATH_EXIT(A,B) |
| -3.60 | CRITICAL_TTC_START(B,A) |
| -3.35 | CRITICAL_TTC_START(A,B) |
| -2.05 | TURN_RIGHT_START(B) |
| -0.80 | CRITICAL_TTC_END(A,B) |
| -0.30 | TURN_RIGHT_END(B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B); CLOSING_END(B,A) |
| +0.05 | THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B) |
| +0.30 | TURN_LEFT_END(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |
| +0.80 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 6.90, COLLISION with B 10.25 (+3.35 s); EGO_PATH_ENTRY 5.30 before critical TTC (-1.60 s) [local times; t_global: critical_ttc_start -3.35, ego_path_entry -4.95, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 6.65, COLLISION with A 10.25 (+3.60 s) [local times; t_global: critical_ttc_start -3.60, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -10.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 THROTTLE_START(A) (A:e02)<br>g05 TURN_LEFT_START(A) (A:e03) | ego: not yet observed |
| -10.25 | B | g02 MOVING_START(B) (B:e01)<br>g04 THROTTLE_START(B) (B:e02) | ego: not yet observed |
| -7.70 | B | g06 TRACK_APPEARED_LEFT(B,A) (B:e03)<br>g07 CLOSING_START(B,A) (B:e04) | ego: MOVING, THROTTLE |
| -7.50 | A | g08 TRACK_APPEARED_LEFT(A,B) (A:e04)<br>g09 CLOSING_START(A,B) (A:e05) | ego: MOVING, THROTTLE, TURN_LEFT |
| -4.95 | A | g10 EGO_PATH_ENTRY(A,B) (A:e06) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING |
| -4.70 | A | g11 EGO_PATH_EXIT(A,B) (A:e07) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH |
| -3.60 | B | g12 CRITICAL_TTC_START(B,A) (B:e05) | ego: MOVING, THROTTLE<br>track_001: CLOSING |
| -3.35 | A | g13 CRITICAL_TTC_START(A,B) (A:e08) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING |
| -2.05 | B | g14 TURN_RIGHT_START(B) (B:e06) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC |
| -0.80 | A | g15 CRITICAL_TTC_END(A,B) (A:e09) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC |
| -0.30 | B | g16 TURN_RIGHT_END(B) (B:e07) | ego: MOVING, THROTTLE, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g17 COLLISION(A,B) (A:e10)<br>g19 CLOSING_END(A,B) (A:e11) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING |
| +0.00 | B | g17 COLLISION(A,B) (B:e08)<br>g18 CRITICAL_TTC_END(B,A) (B:e09)<br>g20 CLOSING_END(B,A) (B:e10) | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC |
| +0.05 | A | g21 THROTTLE_END(A) (A:e12)<br>g23 BRAKE_START(A) (A:e13) | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: no active state |
| +0.05 | B | g22 THROTTLE_END(B) (B:e11)<br>g24 BRAKE_START(B) (B:e12) | ego: MOVING, THROTTLE<br>track_001: no active state |
| +0.30 | A | g25 TURN_LEFT_END(A) (A:e14) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state |
| +0.75 | B | g26 MOVING_END(B) (B:e13)<br>g27 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.80 | A | g28 MOVING_END(A) (A:e15)<br>g29 STOP_START(A) (A:e16) | ego: MOVING, BRAKE<br>track_001: no active state |

## Plain-language reading

- 10.25 s before the reference collision, A started moving (already the case when first observed).
- 10.25 s before the reference collision, B started moving (already the case when first observed).
- 10.25 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 10.25 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 10.25 s before the reference collision, A started turning left (already the case when first observed).
- 7.70 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 7.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 7.50 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 7.50 s before the reference collision, A observed B start closing in (already the case when first observed).
- 4.95 s before the reference collision, A observed B enter its forward path corridor.
- 4.70 s before the reference collision, A observed B leave its forward path corridor.
- 3.60 s before the reference collision, B's time-to-contact with A became critical.
- 3.35 s before the reference collision, A's time-to-contact with B became critical.
- 2.05 s before the reference collision, B started turning right.
- 0.80 s before the reference collision, A's time-to-contact with B stopped being critical.
- 0.30 s before the reference collision, B stopped turning right.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1905, B: 1905 N*s).
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.30 s after the reference collision, A stopped turning left.
- 0.75 s after the reference collision, B stopped moving.
- 0.75 s after the reference collision, B came to a stop.
- 0.80 s after the reference collision, A stopped moving.
- 0.80 s after the reference collision, A came to a stop.
