# Global graph - S07/run_0_full_view

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| B:track_001 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 5.70 | -5.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.70 | -5.70 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31406.82 vs 31406.82 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 13.5 m -> 0.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.29 m/s over 3.0 s<br>range at the contact 0.74 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.0 m -> 10.8 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 10.21 m/s over 3.0 s (> 1.50)<br>range at the contact 10.79 m (beyond 3.50 m: confidence factor 0.05) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.70 | TRACK_APPEARED_FRONT | B | B:track_001 | B:e02 @ 0.00 |  |
| g04 | -5.65 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.05 |  |
| g05 | -5.25 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g06 | -4.60 | CLOSING_START | B | B:track_001 | B:e03 @ 1.10 |  |
| g07 | -4.10 | CLOSING_END | A | B | A:e04 @ 1.60 |  |
| g08 | -3.60 | CLOSING_END | B | B:track_001 | B:e04 @ 2.10 |  |
| g09 | -2.45 | CLOSING_START | B | B:track_001 | B:e05 @ 3.25 |  |
| g10 | -2.05 | BRAKE_START | B | - | B:e06 @ 3.65 |  |
| g11 | -1.80 | CLOSING_START | A | B | A:e05 @ 3.90 |  |
| g12 | -1.75 | CRITICAL_TTC_START | B | B:track_001 | B:e07 @ 3.95 |  |
| g13 | -1.10 | CRITICAL_TTC_END | B | B:track_001 | B:e08 @ 4.60 |  |
| g14 | -1.10 | CRITICAL_TTC_START | A | B | A:e06 @ 4.60 |  |
| g15 | -0.85 | CLOSING_END | B | B:track_001 | B:e09 @ 4.85 |  |
| g16 | -0.85 | MOVING_END | B | - | B:e10 @ 4.85 |  |
| g17 | -0.85 | STOP_START | B | - | B:e11 @ 4.85 |  |
| g18 | 0.00 | COLLISION | - | A, B | A:e07 @ 5.70, B:e12 @ 5.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 31406.82, B 31406.82 |
| g19 | 0.00 | CRITICAL_TTC_END | A | B | A:e08 @ 5.70 |  |
| g20 | 0.00 | CLOSING_END | A | B | A:e09 @ 5.70 |  |
| g21 | 0.05 | BRAKE_START | A | - | A:e10 @ 5.75 |  |
| g22 | 0.15 | MOVING_END | A | - | A:e11 @ 5.85 |  |
| g23 | 0.15 | STOP_START | A | - | A:e12 @ 5.85 |  |
| g24 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g25 | - | SPEED_LIMIT_EXCEEDED_START | C | - | C:e02 @ 2.40 |  |
| g26 | - | BRAKE_START | C | - | C:e03 @ 2.95 |  |
| g27 | - | SPEED_LIMIT_EXCEEDED_END | C | - | C:e04 @ 3.10 |  |
| g28 | - | MOVING_END | C | - | C:e05 @ 4.05 |  |
| g29 | - | STOP_START | C | - | C:e06 @ 4.05 |  |
| g30 | - | BRAKE_END | C | - | C:e07 @ 12.95 |  |
| g31 | - | STOP_END | C | - | C:e08 @ 13.75 |  |
| g32 | - | MOVING_START | C | - | C:e09 @ 13.75 |  |

## Edges

```
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
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
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g16 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g11
    g04 --SAME_TRACK--> g14
    g04 --SAME_TRACK--> g19
    g04 --SAME_TRACK--> g20
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g15
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.70 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,B:track_001) |
| -5.65 | TRACK_APPEARED_FRONT(A,B) |
| -5.25 | CLOSING_START(A,B) |
| -4.60 | CLOSING_START(B,B:track_001) |
| -4.10 | CLOSING_END(A,B) |
| -3.60 | CLOSING_END(B,B:track_001) |
| -2.45 | CLOSING_START(B,B:track_001) |
| -2.05 | BRAKE_START(B) |
| -1.80 | CLOSING_START(A,B) |
| -1.75 | CRITICAL_TTC_START(B,B:track_001) |
| -1.10 | CRITICAL_TTC_END(B,B:track_001); CRITICAL_TTC_START(A,B) |
| -0.85 | CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.05 | BRAKE_START(A) |
| +0.15 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 4.60, COLLISION 5.70 (+1.10 s) [local times; t_global: critical_ttc_start -1.10, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.95, COLLISION 5.70 (+1.75 s) [local times; t_global: critical_ttc_start -1.75, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.70 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.70 | B | g02 MOVING_START(B) (B:e01)<br>g03 TRACK_APPEARED_FRONT(B,B:track_001) (B:e02) | ego: not yet observed |
| -5.65 | A | g04 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: MOVING |
| -5.25 | A | g05 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.60 | B | g06 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.10 | A | g07 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.60 | B | g08 CLOSING_END(B,B:track_001) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -2.45 | B | g09 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -2.05 | B | g10 BRAKE_START(B) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.80 | A | g11 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -1.75 | B | g12 CRITICAL_TTC_START(B,B:track_001) (B:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| -1.10 | B | g13 CRITICAL_TTC_END(B,B:track_001) (B:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.10 | A | g14 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -0.85 | B | g15 CLOSING_END(B,B:track_001) (B:e09)<br>g16 MOVING_END(B) (B:e10)<br>g17 STOP_START(B) (B:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| +0.00 | A | g18 COLLISION(A,B) (A:e07)<br>g19 CRITICAL_TTC_END(A,B) (A:e08)<br>g20 CLOSING_END(A,B) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g18 COLLISION(A,B) (B:e12) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| +0.05 | A | g21 BRAKE_START(A) (A:e10) | ego: MOVING<br>track_001: IN_EGO_PATH |
| +0.15 | A | g22 MOVING_END(A) (A:e11)<br>g23 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| - | C | g24 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g25 SPEED_LIMIT_EXCEEDED_START(C) (C:e02) | ego: MOVING |
| - | C | g26 BRAKE_START(C) (C:e03) | ego: MOVING, SPEED_LIMIT_EXCEEDED |
| - | C | g27 SPEED_LIMIT_EXCEEDED_END(C) (C:e04) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED |
| - | C | g28 MOVING_END(C) (C:e05)<br>g29 STOP_START(C) (C:e06) | ego: MOVING, BRAKE |
| - | C | g30 BRAKE_END(C) (C:e07) | ego: STOP, BRAKE |
| - | C | g31 STOP_END(C) (C:e08)<br>g32 MOVING_START(C) (C:e09) | ego: STOP |

## Plain-language reading

- 5.70 s before the matched collision, A started moving (already the case when first observed).
- 5.70 s before the matched collision, B started moving (already the case when first observed).
- 5.70 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.65 s before the matched collision, A's radar started tracking B, which appeared in front of it.
- 5.25 s before the matched collision, A observed B start closing in.
- 4.60 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.10 s before the matched collision, A observed B stop closing in.
- 3.60 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 2.45 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.05 s before the matched collision, B started braking.
- 1.80 s before the matched collision, A observed B start closing in.
- 1.75 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.10 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.10 s before the matched collision, A's time-to-contact with B became critical.
- 0.85 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 0.85 s before the matched collision, B stopped moving.
- 0.85 s before the matched collision, B came to a stop.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 31407, B: 31407 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A started braking.
- 0.15 s after the matched collision, A stopped moving.
- 0.15 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 3.10 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 12.95 s) C released the brake.
- (unaligned, C local time 13.75 s) C left its stop.
- (unaligned, C local time 13.75 s) C started moving.
