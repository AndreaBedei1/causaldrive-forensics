# Global graph - S06/run_0_a_front_pushed

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock ALIGNED; observed by others as: B:track_001 |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 5.90 | -5.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e13 | 5.90 | -5.90 | reported the reference collision collision_001 |
| C | ALIGNED | C:e07 | 6.15 | -5.90 | shares collision_002 with B, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 11621.71 vs 11621.71 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: B and C both recorded a collision; peak impulses 9832.4 vs 9832.4 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.67 | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.1 m -> 1.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.34 m/s over 3.0 s<br>range at the contact 1.24 m<br>the only track of A compatible with the contact |
| B:track_001 | C | ASSOCIATED | 0.99 | B and C both reported collision_002 at 6.15 s (peak impulse 9832.4 vs 9832.4 N*s)<br>tracked for 6.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 1.5 m -> 0.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.24 m/s over 3.0 s<br>range at the contact 0.08 m<br>the only track of B compatible with the contact<br>collision_001 with A at 5.90 s: not compatible (track speed disagrees with A's own speed: RMSE 10.78 m/s over 3.0 s (> 1.50)) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.90 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.90 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.90 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -5.90 | TRACK_APPEARED_FRONT | B | C | B:e02 @ 0.00 |  |
| g05 | -5.85 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.05 |  |
| g06 | -5.45 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g07 | -4.80 | CLOSING_START | B | C | B:e03 @ 1.10 |  |
| g08 | -4.30 | CLOSING_END | A | B | A:e04 @ 1.60 |  |
| g09 | -3.80 | CLOSING_END | B | C | B:e04 @ 2.10 |  |
| g10 | -3.50 | SPEED_LIMIT_EXCEEDED_START | C | - | C:e02 @ 2.40 |  |
| g11 | -2.95 | BRAKE_START | C | - | C:e03 @ 2.95 |  |
| g12 | -2.85 | SPEED_LIMIT_EXCEEDED_END | C | - | C:e04 @ 3.05 |  |
| g13 | -2.70 | CLOSING_START | B | C | B:e05 @ 3.20 |  |
| g14 | -2.20 | BRAKE_START | B | - | B:e06 @ 3.70 |  |
| g15 | -2.15 | CRITICAL_TTC_START | B | C | B:e07 @ 3.75 |  |
| g16 | -1.90 | CLOSING_START | A | B | A:e05 @ 4.00 |  |
| g17 | -1.85 | MOVING_END | C | - | C:e05 @ 4.05 |  |
| g18 | -1.85 | STOP_START | C | - | C:e06 @ 4.05 |  |
| g19 | -1.20 | CRITICAL_TTC_START | A | B | A:e06 @ 4.70 |  |
| g20 | -1.00 | CRITICAL_TTC_END | B | C | B:e08 @ 4.90 |  |
| g21 | -1.00 | CLOSING_END | B | C | B:e09 @ 4.90 |  |
| g22 | -1.00 | MOVING_END | B | - | B:e10 @ 4.90 |  |
| g23 | -1.00 | STOP_START | B | - | B:e11 @ 4.90 |  |
| g24 | -0.35 | BRAKE_START | A | - | A:e07 @ 5.55 |  |
| g25 | -0.20 | BRAKE_END | B | - | B:e12 @ 5.70 |  |
| g26 | 0.00 | COLLISION | - | A, B | A:e08 @ 5.90, B:e13 @ 5.90 | matched_event=collision_001; reference_event=True; peak_impulse=A 11621.71, B 11621.71 |
| g27 | 0.00 | STOP_END | B | - | B:e14 @ 5.90 |  |
| g28 | 0.00 | MOVING_START | B | - | B:e15 @ 5.90 |  |
| g29 | 0.00 | CRITICAL_TTC_START | B | C | B:e16 @ 5.90 |  |
| g30 | 0.25 | COLLISION | - | B, C | B:e17 @ 6.15, C:e07 @ 6.15 | matched_event=collision_002; reference_event=False; peak_impulse=B 9832.40, C 9832.40 |
| g31 | 0.30 | TRACK_LOST | B | C | B:e18 @ 6.20 |  |
| g32 | 0.35 | CRITICAL_TTC_END | A | B | A:e09 @ 6.25 |  |
| g33 | 0.35 | CLOSING_END | A | B | A:e10 @ 6.25 |  |
| g34 | 0.35 | MOVING_END | A | - | A:e11 @ 6.25 |  |
| g35 | 0.35 | STOP_START | A | - | A:e12 @ 6.25 |  |
| g36 | 0.40 | MOVING_END | B | - | B:e19 @ 6.30 |  |
| g37 | 0.40 | STOP_START | B | - | B:e20 @ 6.30 |  |

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
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g08
    g05 --SAME_TRACK--> g16
    g05 --SAME_TRACK--> g19
    g05 --SAME_TRACK--> g32
    g05 --SAME_TRACK--> g33
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g15
    g04 --SAME_TRACK--> g20
    g04 --SAME_TRACK--> g21
    g04 --SAME_TRACK--> g29
    g04 --SAME_TRACK--> g31
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.90 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,C) |
| -5.85 | TRACK_APPEARED_FRONT(A,B) |
| -5.45 | CLOSING_START(A,B) |
| -4.80 | CLOSING_START(B,C) |
| -4.30 | CLOSING_END(A,B) |
| -3.80 | CLOSING_END(B,C) |
| -3.50 | SPEED_LIMIT_EXCEEDED_START(C) |
| -2.95 | BRAKE_START(C) |
| -2.85 | SPEED_LIMIT_EXCEEDED_END(C) |
| -2.70 | CLOSING_START(B,C) |
| -2.20 | BRAKE_START(B) |
| -2.15 | CRITICAL_TTC_START(B,C) |
| -1.90 | CLOSING_START(A,B) |
| -1.85 | MOVING_END(C); STOP_START(C) |
| -1.20 | CRITICAL_TTC_START(A,B) |
| -1.00 | CRITICAL_TTC_END(B,C); CLOSING_END(B,C); MOVING_END(B); STOP_START(B) |
| -0.35 | BRAKE_START(A) |
| -0.20 | BRAKE_END(B) |
| +0.00 | COLLISION(A,B); STOP_END(B); MOVING_START(B); CRITICAL_TTC_START(B,C) |
| +0.25 | COLLISION(B,C) |
| +0.30 | TRACK_LOST(B,C) |
| +0.35 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B); MOVING_END(A); STOP_START(A) |
| +0.40 | MOVING_END(B); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 4.70, COLLISION with B 5.90 (+1.20 s) [local times; t_global: critical_ttc_start -1.20, collision +0.00]
- B's track_001 (C): CRITICAL_TTC_START 3.75, COLLISION with C 6.15 (+2.40 s) [local times; t_global: critical_ttc_start -2.15, collision +0.25]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.90 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.90 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_FRONT(B,C) (B:e02) | ego: not yet observed |
| -5.90 | C | g03 MOVING_START(C) (C:e01) | ego: not yet observed |
| -5.85 | A | g05 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: MOVING |
| -5.45 | A | g06 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.80 | B | g07 CLOSING_START(B,C) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.30 | A | g08 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.80 | B | g09 CLOSING_END(B,C) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.50 | C | g10 SPEED_LIMIT_EXCEEDED_START(C) (C:e02) | ego: MOVING |
| -2.95 | C | g11 BRAKE_START(C) (C:e03) | ego: MOVING, SPEED_LIMIT_EXCEEDED |
| -2.85 | C | g12 SPEED_LIMIT_EXCEEDED_END(C) (C:e04) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED |
| -2.70 | B | g13 CLOSING_START(B,C) (B:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -2.20 | B | g14 BRAKE_START(B) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -2.15 | B | g15 CRITICAL_TTC_START(B,C) (B:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| -1.90 | A | g16 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -1.85 | C | g17 MOVING_END(C) (C:e05)<br>g18 STOP_START(C) (C:e06) | ego: MOVING, BRAKE |
| -1.20 | A | g19 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.00 | B | g20 CRITICAL_TTC_END(B,C) (B:e08)<br>g21 CLOSING_END(B,C) (B:e09)<br>g22 MOVING_END(B) (B:e10)<br>g23 STOP_START(B) (B:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.35 | A | g24 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.20 | B | g25 BRAKE_END(B) (B:e12) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| +0.00 | A | g26 COLLISION(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g26 COLLISION(A,B) (B:e13)<br>g27 STOP_END(B) (B:e14)<br>g28 MOVING_START(B) (B:e15)<br>g29 CRITICAL_TTC_START(B,C) (B:e16) | ego: STOP<br>track_001: IN_EGO_PATH |
| +0.25 | B | g30 COLLISION(B,C) (B:e17) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH |
| +0.25 | C | g30 COLLISION(B,C) (C:e07) | ego: STOP, BRAKE |
| +0.30 | B | g31 TRACK_LOST(B,C) (B:e18) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH |
| +0.35 | A | g32 CRITICAL_TTC_END(A,B) (A:e09)<br>g33 CLOSING_END(A,B) (A:e10)<br>g34 MOVING_END(A) (A:e11)<br>g35 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.40 | B | g36 MOVING_END(B) (B:e19)<br>g37 STOP_START(B) (B:e20) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |

## Plain-language reading

- 5.90 s before the reference collision, A started moving (already the case when first observed).
- 5.90 s before the reference collision, B started moving (already the case when first observed).
- 5.90 s before the reference collision, C started moving (already the case when first observed).
- 5.90 s before the reference collision, B's radar started tracking C, which appeared in front of it.
- 5.85 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 5.45 s before the reference collision, A observed B start closing in.
- 4.80 s before the reference collision, B observed C start closing in.
- 4.30 s before the reference collision, A observed B stop closing in.
- 3.80 s before the reference collision, B observed C stop closing in.
- 3.50 s before the reference collision, C began exceeding the speed limit.
- 2.95 s before the reference collision, C started braking.
- 2.85 s before the reference collision, C returned within the speed limit.
- 2.70 s before the reference collision, B observed C start closing in.
- 2.20 s before the reference collision, B started braking.
- 2.15 s before the reference collision, B's time-to-contact with C became critical.
- 1.90 s before the reference collision, A observed B start closing in.
- 1.85 s before the reference collision, C stopped moving.
- 1.85 s before the reference collision, C came to a stop.
- 1.20 s before the reference collision, A's time-to-contact with B became critical.
- 1.00 s before the reference collision, B's time-to-contact with C stopped being critical.
- 1.00 s before the reference collision, B observed C stop closing in.
- 1.00 s before the reference collision, B stopped moving.
- 1.00 s before the reference collision, B came to a stop.
- 0.35 s before the reference collision, A started braking.
- 0.20 s before the reference collision, B released the brake.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 11622, B: 11622 N*s).
- At the reference collision, B left its stop.
- At the reference collision, B started moving.
- At the reference collision, B's time-to-contact with C became critical.
- 0.25 s after the reference collision, B and C both recorded this same collision (peak impulses B: 9832, C: 9832 N*s).
- 0.30 s after the reference collision, B's radar lost C (its states are UNKNOWN from then on, not ended).
- 0.35 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.35 s after the reference collision, A observed B stop closing in.
- 0.35 s after the reference collision, A stopped moving.
- 0.35 s after the reference collision, A came to a stop.
- 0.40 s after the reference collision, B stopped moving.
- 0.40 s after the reference collision, B came to a stop.
