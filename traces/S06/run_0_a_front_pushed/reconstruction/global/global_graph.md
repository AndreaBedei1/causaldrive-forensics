# Global graph - S06/run_0_a_front_pushed

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
| A | ALIGNED | A:e08 | 5.90 | -5.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e13 | 5.90 | -5.90 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | its collision report matched no other graph |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 11621.71 vs 11621.71 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.67 | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.1 m -> 1.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.34 m/s over 3.0 s<br>range at the contact 1.24 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 1.5 m -> 1.3 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 10.78 m/s over 3.0 s (> 1.50)<br>range at the contact 1.26 m |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.90 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.90 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.90 | TRACK_APPEARED_FRONT | B | B:track_001 | B:e02 @ 0.00 |  |
| g04 | -5.85 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.05 |  |
| g05 | -5.45 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g06 | -4.80 | CLOSING_START | B | B:track_001 | B:e03 @ 1.10 |  |
| g07 | -4.30 | CLOSING_END | A | B | A:e04 @ 1.60 |  |
| g08 | -3.80 | CLOSING_END | B | B:track_001 | B:e04 @ 2.10 |  |
| g09 | -2.70 | CLOSING_START | B | B:track_001 | B:e05 @ 3.20 |  |
| g10 | -2.20 | BRAKE_START | B | - | B:e06 @ 3.70 |  |
| g11 | -2.15 | CRITICAL_TTC_START | B | B:track_001 | B:e07 @ 3.75 |  |
| g12 | -1.90 | CLOSING_START | A | B | A:e05 @ 4.00 |  |
| g13 | -1.20 | CRITICAL_TTC_START | A | B | A:e06 @ 4.70 |  |
| g14 | -1.00 | CRITICAL_TTC_END | B | B:track_001 | B:e08 @ 4.90 |  |
| g15 | -1.00 | CLOSING_END | B | B:track_001 | B:e09 @ 4.90 |  |
| g16 | -1.00 | MOVING_END | B | - | B:e10 @ 4.90 |  |
| g17 | -1.00 | STOP_START | B | - | B:e11 @ 4.90 |  |
| g18 | -0.35 | BRAKE_START | A | - | A:e07 @ 5.55 |  |
| g19 | -0.20 | BRAKE_END | B | - | B:e12 @ 5.70 |  |
| g20 | 0.00 | COLLISION | - | A, B | A:e08 @ 5.90, B:e13 @ 5.90 | matched_event=collision_001; reference_event=True; peak_impulse=A 11621.71, B 11621.71 |
| g21 | 0.00 | STOP_END | B | - | B:e14 @ 5.90 |  |
| g22 | 0.00 | MOVING_START | B | - | B:e15 @ 5.90 |  |
| g23 | 0.00 | CRITICAL_TTC_START | B | B:track_001 | B:e16 @ 5.90 |  |
| g24 | 0.30 | TRACK_LOST | B | B:track_001 | B:e17 @ 6.20 |  |
| g25 | 0.35 | CRITICAL_TTC_END | A | B | A:e09 @ 6.25 |  |
| g26 | 0.35 | CLOSING_END | A | B | A:e10 @ 6.25 |  |
| g27 | 0.35 | MOVING_END | A | - | A:e11 @ 6.25 |  |
| g28 | 0.35 | STOP_START | A | - | A:e12 @ 6.25 |  |
| g29 | 0.40 | MOVING_END | B | - | B:e18 @ 6.30 |  |
| g30 | 0.40 | STOP_START | B | - | B:e19 @ 6.30 |  |
| g31 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g32 | - | SPEED_LIMIT_EXCEEDED_START | C | - | C:e02 @ 2.40 |  |
| g33 | - | BRAKE_START | C | - | C:e03 @ 2.95 |  |
| g34 | - | SPEED_LIMIT_EXCEEDED_END | C | - | C:e04 @ 3.05 |  |
| g35 | - | MOVING_END | C | - | C:e05 @ 4.05 |  |
| g36 | - | STOP_START | C | - | C:e06 @ 4.05 |  |
| g37 | - | COLLISION | C | - | C:e07 @ 6.15 | peak_impulse=9832.40 |

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
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g24
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g25
    g04 --SAME_TRACK--> g26
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g15
    g03 --SAME_TRACK--> g23
    g03 --SAME_TRACK--> g24
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.90 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,B:track_001) |
| -5.85 | TRACK_APPEARED_FRONT(A,B) |
| -5.45 | CLOSING_START(A,B) |
| -4.80 | CLOSING_START(B,B:track_001) |
| -4.30 | CLOSING_END(A,B) |
| -3.80 | CLOSING_END(B,B:track_001) |
| -2.70 | CLOSING_START(B,B:track_001) |
| -2.20 | BRAKE_START(B) |
| -2.15 | CRITICAL_TTC_START(B,B:track_001) |
| -1.90 | CLOSING_START(A,B) |
| -1.20 | CRITICAL_TTC_START(A,B) |
| -1.00 | CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B) |
| -0.35 | BRAKE_START(A) |
| -0.20 | BRAKE_END(B) |
| +0.00 | COLLISION(A,B); STOP_END(B); MOVING_START(B); CRITICAL_TTC_START(B,B:track_001) |
| +0.30 | TRACK_LOST(B,B:track_001) |
| +0.35 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B); MOVING_END(A); STOP_START(A) |
| +0.40 | MOVING_END(B); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 4.70, COLLISION 5.90 (+1.20 s) [local times; t_global: critical_ttc_start -1.20, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.75, COLLISION 5.90 (+2.15 s) [local times; t_global: critical_ttc_start -2.15, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.90 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.90 | B | g02 MOVING_START(B) (B:e01)<br>g03 TRACK_APPEARED_FRONT(B,B:track_001) (B:e02) | ego: not yet observed |
| -5.85 | A | g04 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: MOVING |
| -5.45 | A | g05 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.80 | B | g06 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.30 | A | g07 CLOSING_END(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.80 | B | g08 CLOSING_END(B,B:track_001) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -2.70 | B | g09 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -2.20 | B | g10 BRAKE_START(B) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -2.15 | B | g11 CRITICAL_TTC_START(B,B:track_001) (B:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| -1.90 | A | g12 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -1.20 | A | g13 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.00 | B | g14 CRITICAL_TTC_END(B,B:track_001) (B:e08)<br>g15 CLOSING_END(B,B:track_001) (B:e09)<br>g16 MOVING_END(B) (B:e10)<br>g17 STOP_START(B) (B:e11) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.35 | A | g18 BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.20 | B | g19 BRAKE_END(B) (B:e12) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| +0.00 | A | g20 COLLISION(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g20 COLLISION(A,B) (B:e13)<br>g21 STOP_END(B) (B:e14)<br>g22 MOVING_START(B) (B:e15)<br>g23 CRITICAL_TTC_START(B,B:track_001) (B:e16) | ego: STOP<br>track_001: IN_EGO_PATH |
| +0.30 | B | g24 TRACK_LOST(B,B:track_001) (B:e17) | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH |
| +0.35 | A | g25 CRITICAL_TTC_END(A,B) (A:e09)<br>g26 CLOSING_END(A,B) (A:e10)<br>g27 MOVING_END(A) (A:e11)<br>g28 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.40 | B | g29 MOVING_END(B) (B:e18)<br>g30 STOP_START(B) (B:e19) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| - | C | g31 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g32 SPEED_LIMIT_EXCEEDED_START(C) (C:e02) | ego: MOVING |
| - | C | g33 BRAKE_START(C) (C:e03) | ego: MOVING, SPEED_LIMIT_EXCEEDED |
| - | C | g34 SPEED_LIMIT_EXCEEDED_END(C) (C:e04) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED |
| - | C | g35 MOVING_END(C) (C:e05)<br>g36 STOP_START(C) (C:e06) | ego: MOVING, BRAKE |
| - | C | g37 COLLISION(C) (C:e07) | ego: STOP, BRAKE |

## Plain-language reading

- 5.90 s before the matched collision, A started moving (already the case when first observed).
- 5.90 s before the matched collision, B started moving (already the case when first observed).
- 5.90 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.85 s before the matched collision, A's radar started tracking B, which appeared in front of it.
- 5.45 s before the matched collision, A observed B start closing in.
- 4.80 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.30 s before the matched collision, A observed B stop closing in.
- 3.80 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 2.70 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.20 s before the matched collision, B started braking.
- 2.15 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.90 s before the matched collision, A observed B start closing in.
- 1.20 s before the matched collision, A's time-to-contact with B became critical.
- 1.00 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.00 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.00 s before the matched collision, B stopped moving.
- 1.00 s before the matched collision, B came to a stop.
- 0.35 s before the matched collision, A started braking.
- 0.20 s before the matched collision, B released the brake.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 11622, B: 11622 N*s).
- At the matched collision, B left its stop.
- At the matched collision, B started moving.
- At the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 0.30 s after the matched collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.35 s after the matched collision, A observed B stop closing in.
- 0.35 s after the matched collision, A stopped moving.
- 0.35 s after the matched collision, A came to a stop.
- 0.40 s after the matched collision, B stopped moving.
- 0.40 s after the matched collision, B came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 3.05 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 6.15 s) C's collision sensor recorded a contact (peak impulse 9832 N*s).
