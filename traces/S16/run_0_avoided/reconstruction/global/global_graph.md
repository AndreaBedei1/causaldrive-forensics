# Global graph - S16/run_0_avoided

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e03 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 3.9 m -> 0.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.52 m/s over 3.0 s<br>range at the contact 0.54 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.15 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g04 | -4.45 | CLOSING_START | B | A | B:e03 @ 0.70 |  |
| g05 | -4.40 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g06 | -3.75 | CRITICAL_TTC_END | B | A | B:e05 @ 1.40 |  |
| g07 | -3.75 | CLOSING_END | B | A | B:e06 @ 1.40 |  |
| g08 | -1.20 | BRAKE_START | A | - | A:e02 @ 3.95 |  |
| g09 | -0.90 | CLOSING_START | B | A | B:e07 @ 4.25 |  |
| g10 | -0.70 | CRITICAL_TTC_START | B | A | B:e08 @ 4.45 |  |
| g11 | -0.40 | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g12 | 0.00 | COLLISION | - | A, B | A:e03 @ 5.15, B:e10 @ 5.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 6073.81, B 6073.81 |
| g13 | 0.05 | CRITICAL_TTC_END | B | A | B:e11 @ 5.20 |  |
| g14 | 0.05 | CLOSING_END | B | A | B:e12 @ 5.20 |  |
| g15 | 0.45 | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g16 | 0.45 | STOP_START | B | - | B:e14 @ 5.60 |  |
| g17 | 0.60 | MOVING_END | A | - | A:e04 @ 5.75 |  |
| g18 | 0.60 | STOP_START | A | - | A:e05 @ 5.75 |  |
| g19 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g20 | - | MOVING_END | C | - | C:e02 @ 0.30 |  |
| g21 | - | STOP_START | C | - | C:e03 @ 0.30 |  |

## Edges

```
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.15 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,A) |
| -4.45 | CLOSING_START(B,A) |
| -4.40 | CRITICAL_TTC_START(B,A) |
| -3.75 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| -1.20 | BRAKE_START(A) |
| -0.90 | CLOSING_START(B,A) |
| -0.70 | CRITICAL_TTC_START(B,A) |
| -0.40 | BRAKE_START(B) |
| +0.00 | COLLISION(A,B) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.45 | MOVING_END(B); STOP_START(B) |
| +0.60 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -4.40, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.15 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.15 | B | g02 MOVING_START(B) (B:e01)<br>g03 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -4.45 | B | g04 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.40 | B | g05 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.75 | B | g06 CRITICAL_TTC_END(B,A) (B:e05)<br>g07 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.20 | A | g08 BRAKE_START(A) (A:e02) | ego: MOVING |
| -0.90 | B | g09 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -0.70 | B | g10 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -0.40 | B | g11 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g12 COLLISION(A,B) (A:e03) | ego: MOVING, BRAKE |
| +0.00 | B | g12 COLLISION(A,B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | B | g13 CRITICAL_TTC_END(B,A) (B:e11)<br>g14 CLOSING_END(B,A) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.45 | B | g15 MOVING_END(B) (B:e13)<br>g16 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.60 | A | g17 MOVING_END(A) (A:e04)<br>g18 STOP_START(A) (A:e05) | ego: MOVING, BRAKE |
| - | C | g19 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g20 MOVING_END(C) (C:e02)<br>g21 STOP_START(C) (C:e03) | ego: MOVING |

## Plain-language reading

- 5.15 s before the matched collision, A started moving (already the case when first observed).
- 5.15 s before the matched collision, B started moving (already the case when first observed).
- 5.15 s before the matched collision, B's radar started tracking A, which appeared in front of it.
- 4.45 s before the matched collision, B observed A start closing in.
- 4.40 s before the matched collision, B's time-to-contact with A became critical.
- 3.75 s before the matched collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the matched collision, B observed A stop closing in.
- 1.20 s before the matched collision, A started braking.
- 0.90 s before the matched collision, B observed A start closing in.
- 0.70 s before the matched collision, B's time-to-contact with A became critical.
- 0.40 s before the matched collision, B started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.60 s after the matched collision, A stopped moving.
- 0.60 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.30 s) C stopped moving.
- (unaligned, C local time 0.30 s) C came to a stop.
