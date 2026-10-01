# Global graph - S06/run_0_b_rear_first

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e06 | 6.00 | -6.00 | reported the reference collision collision_001 |
| B | ALIGNED | B:e13 | 6.00 | -6.00 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31488.29 vs 31488.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: B and C both recorded a collision; peak impulses 21812.15 vs 21812.15 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 5.95 s before the matched collision<br>lost 1.45 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 19.4 m -> 19.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.04 m/s over 1.5 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 6.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 0.3 m -> 0.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 10.92 m/s over 3.0 s (> 1.50)<br>range at the contact 0.20 m |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.00 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.00 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.00 | TRACK_APPEARED_FRONT | B | B:track_001 | B:e02 @ 0.00 |  |
| g04 | -5.95 | TRACK_APPEARED_FRONT | A | A:track_001 | A:e02 @ 0.05 |  |
| g05 | -5.55 | CLOSING_START | A | A:track_001 | A:e03 @ 0.45 |  |
| g06 | -4.90 | CLOSING_START | B | B:track_001 | B:e03 @ 1.10 |  |
| g07 | -4.40 | CLOSING_END | A | A:track_001 | A:e04 @ 1.60 |  |
| g08 | -3.90 | CLOSING_END | B | B:track_001 | B:e04 @ 2.10 |  |
| g09 | -2.80 | CLOSING_START | B | B:track_001 | B:e05 @ 3.20 |  |
| g10 | -2.25 | CRITICAL_TTC_START | B | B:track_001 | B:e06 @ 3.75 |  |
| g11 | -1.45 | TRACK_LOST | A | A:track_001 | A:e05 @ 4.55 |  |
| g12 | -1.40 | COLLISION | B | - | B:e07 @ 4.60 | peak_impulse=21812.15 |
| g13 | -1.35 | CRITICAL_TTC_END | B | B:track_001 | B:e08 @ 4.65 |  |
| g14 | -1.35 | CLOSING_END | B | B:track_001 | B:e09 @ 4.65 |  |
| g15 | -1.35 | BRAKE_START | B | - | B:e10 @ 4.65 |  |
| g16 | -1.25 | MOVING_END | B | - | B:e11 @ 4.75 |  |
| g17 | -1.25 | STOP_START | B | - | B:e12 @ 4.75 |  |
| g18 | 0.00 | COLLISION | - | A, B | A:e06 @ 6.00, B:e13 @ 6.00 | matched_event=collision_001; reference_event=True; peak_impulse=A 31488.29, B 31488.29 |
| g19 | 0.05 | BRAKE_START | A | - | A:e07 @ 6.05 |  |
| g20 | 0.20 | MOVING_END | A | - | A:e08 @ 6.20 |  |
| g21 | 0.20 | STOP_START | A | - | A:e09 @ 6.20 |  |
| g22 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g23 | - | SPEED_LIMIT_EXCEEDED_START | C | - | C:e02 @ 2.40 |  |
| g24 | - | BRAKE_START | C | - | C:e03 @ 2.95 |  |
| g25 | - | SPEED_LIMIT_EXCEEDED_END | C | - | C:e04 @ 3.05 |  |
| g26 | - | MOVING_END | C | - | C:e05 @ 4.05 |  |
| g27 | - | STOP_START | C | - | C:e06 @ 4.05 |  |
| g28 | - | COLLISION | C | - | C:e07 @ 4.60 | peak_impulse=21812.15 |

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
    g12 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.00 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,B:track_001) |
| -5.95 | TRACK_APPEARED_FRONT(A,A:track_001) |
| -5.55 | CLOSING_START(A,A:track_001) |
| -4.90 | CLOSING_START(B,B:track_001) |
| -4.40 | CLOSING_END(A,A:track_001) |
| -3.90 | CLOSING_END(B,B:track_001) |
| -2.80 | CLOSING_START(B,B:track_001) |
| -2.25 | CRITICAL_TTC_START(B,B:track_001) |
| -1.45 | TRACK_LOST(A,A:track_001) |
| -1.40 | COLLISION(B) |
| -1.35 | CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); BRAKE_START(B) |
| -1.25 | MOVING_END(B); STOP_START(B) |
| +0.00 | COLLISION(A,B) |
| +0.05 | BRAKE_START(A) |
| +0.20 | MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 3.75, COLLISION 4.60 (+0.85 s) [local times; t_global: critical_ttc_start -2.25, collision -1.40]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.00 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -6.00 | B | g02 MOVING_START(B) (B:e01)<br>g03 TRACK_APPEARED_FRONT(B,B:track_001) (B:e02) | ego: not yet observed |
| -5.95 | A | g04 TRACK_APPEARED_FRONT(A,A:track_001) (A:e02) | ego: MOVING |
| -5.55 | A | g05 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.90 | B | g06 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.40 | A | g07 CLOSING_END(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.90 | B | g08 CLOSING_END(B,B:track_001) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -2.80 | B | g09 CLOSING_START(B,B:track_001) (B:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -2.25 | B | g10 CRITICAL_TTC_START(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.45 | A | g11 TRACK_LOST(A,A:track_001) (A:e05) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -1.40 | B | g12 COLLISION(B) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.35 | B | g13 CRITICAL_TTC_END(B,B:track_001) (B:e08)<br>g14 CLOSING_END(B,B:track_001) (B:e09)<br>g15 BRAKE_START(B) (B:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.25 | B | g16 MOVING_END(B) (B:e11)<br>g17 STOP_START(B) (B:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.00 | A | g18 COLLISION(A,B) (A:e06) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g18 COLLISION(A,B) (B:e13) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH |
| +0.05 | A | g19 BRAKE_START(A) (A:e07) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.20 | A | g20 MOVING_END(A) (A:e08)<br>g21 STOP_START(A) (A:e09) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |
| - | C | g22 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g23 SPEED_LIMIT_EXCEEDED_START(C) (C:e02) | ego: MOVING |
| - | C | g24 BRAKE_START(C) (C:e03) | ego: MOVING, SPEED_LIMIT_EXCEEDED |
| - | C | g25 SPEED_LIMIT_EXCEEDED_END(C) (C:e04) | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED |
| - | C | g26 MOVING_END(C) (C:e05)<br>g27 STOP_START(C) (C:e06) | ego: MOVING, BRAKE |
| - | C | g28 COLLISION(C) (C:e07) | ego: STOP, BRAKE |

## Plain-language reading

- 6.00 s before the matched collision, A started moving (already the case when first observed).
- 6.00 s before the matched collision, B started moving (already the case when first observed).
- 6.00 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.95 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 5.55 s before the matched collision, A observed unidentified object A:track_001 start closing in.
- 4.90 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.40 s before the matched collision, A observed unidentified object A:track_001 stop closing in.
- 3.90 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 2.80 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.25 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.45 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the matched collision, B's collision sensor recorded a contact (peak impulse 21812 N*s).
- 1.35 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.35 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.35 s before the matched collision, B started braking.
- 1.25 s before the matched collision, B stopped moving.
- 1.25 s before the matched collision, B came to a stop.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 31488, B: 31488 N*s).
- 0.05 s after the matched collision, A started braking.
- 0.20 s after the matched collision, A stopped moving.
- 0.20 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 3.05 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 4.60 s) C's collision sensor recorded a contact (peak impulse 21812 N*s).
