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
| A | ALIGNED | A:e09 | 5.70 | -5.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e15 | 5.70 | -5.70 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31406.82 vs 31406.82 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.70 s before the matched collision<br>at the contact: minimum range 0.72 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.28 m/s over 3.0 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 31406.82 vs 31406.82 N*s)<br>tracked for 5.70 s before the matched collision<br>not at the contact: minimum range 10.80 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with A's own speed: RMSE 10.21 m/s (> 1.50) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.70 | TRACK_APPEARED_FRONT | A | B | A:e02 @ 0.00 |  |
| g04 | -5.70 | TRACK_APPEARED_FRONT | B | B:track_001 | B:e02 @ 0.00 |  |
| g05 | -5.25 | STRONG_THROTTLE_START | B | - | B:e03 @ 0.45 |  |
| g06 | -5.25 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g07 | -4.60 | CLOSING_START | B | B:track_001 | B:e04 @ 1.10 |  |
| g08 | -4.55 | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g09 | -4.35 | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g10 | -4.10 | CLOSING_END | A | B | A:e06 @ 1.60 |  |
| g11 | -3.95 | STRONG_THROTTLE_END | B | - | B:e05 @ 1.75 |  |
| g12 | -3.60 | CLOSING_END | B | B:track_001 | B:e06 @ 2.10 |  |
| g13 | -2.45 | CLOSING_START | B | B:track_001 | B:e07 @ 3.25 |  |
| g14 | -2.05 | BRAKE_START | B | - | B:e08 @ 3.65 |  |
| g15 | -2.05 | HARD_BRAKE_START | B | - | B:e09 @ 3.65 |  |
| g16 | -1.80 | CLOSING_START | A | B | A:e07 @ 3.90 |  |
| g17 | -1.80 | CRITICAL_TTC_START | B | B:track_001 | B:e10 @ 3.90 |  |
| g18 | -1.10 | CRITICAL_TTC_START | A | B | A:e08 @ 4.60 |  |
| g19 | -1.05 | CRITICAL_TTC_END | B | B:track_001 | B:e11 @ 4.65 |  |
| g20 | -0.85 | CLOSING_END | B | B:track_001 | B:e12 @ 4.85 |  |
| g21 | -0.85 | MOVING_END | B | - | B:e13 @ 4.85 |  |
| g22 | -0.85 | STOP_START | B | - | B:e14 @ 4.85 |  |
| g23 | 0.00 | COLLISION | - | A, B | A:e09 @ 5.70, B:e15 @ 5.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 31406.82, B 31406.82 |
| g24 | 0.00 | CRITICAL_TTC_END | A | B | A:e10 @ 5.70 |  |
| g25 | 0.00 | CLOSING_END | A | B | A:e11 @ 5.70 |  |
| g26 | 0.00 | STRONG_THROTTLE_START | A | - | A:e12 @ 5.70 |  |
| g27 | 0.05 | STRONG_THROTTLE_END | A | - | A:e13 @ 5.75 |  |
| g28 | 0.05 | BRAKE_START | A | - | A:e14 @ 5.75 |  |
| g29 | 0.05 | HARD_BRAKE_START | A | - | A:e15 @ 5.75 |  |
| g30 | 0.15 | MOVING_END | A | - | A:e16 @ 5.85 |  |
| g31 | 0.15 | STOP_START | A | - | A:e17 @ 5.85 |  |
| g32 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g33 | - | STRONG_THROTTLE_START | C | - | C:e02 @ 0.50 |  |
| g34 | - | STRONG_THROTTLE_END | C | - | C:e03 @ 2.05 |  |
| g35 | - | SPEED_LIMIT_EXCEEDED_START | C | - | C:e04 @ 2.40 |  |
| g36 | - | BRAKE_START | C | - | C:e05 @ 2.95 |  |
| g37 | - | HARD_BRAKE_START | C | - | C:e06 @ 2.95 |  |
| g38 | - | SPEED_LIMIT_EXCEEDED_END | C | - | C:e07 @ 3.10 |  |
| g39 | - | MOVING_END | C | - | C:e08 @ 4.05 |  |
| g40 | - | STOP_START | C | - | C:e09 @ 4.05 |  |
| g41 | - | HARD_BRAKE_END | C | - | C:e10 @ 12.95 |  |
| g42 | - | BRAKE_END | C | - | C:e11 @ 12.95 |  |
| g43 | - | STRONG_THROTTLE_START | C | - | C:e12 @ 12.95 |  |
| g44 | - | STOP_END | C | - | C:e13 @ 13.75 |  |
| g45 | - | MOVING_START | C | - | C:e14 @ 13.75 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g01 --PRECEDES--> g06
    g02 --PRECEDES--> g05
    g02 --PRECEDES--> g06
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g16
    g03 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g24
    g03 --SAME_TRACK--> g25
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g17
    g04 --SAME_TRACK--> g19
    g04 --SAME_TRACK--> g20
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.70 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(A,B); TRACK_APPEARED_FRONT(B,B:track_001) |
| -5.25 | STRONG_THROTTLE_START(B); CLOSING_START(A,B) |
| -4.60 | CLOSING_START(B,B:track_001) |
| -4.55 | STRONG_THROTTLE_START(A) |
| -4.35 | STRONG_THROTTLE_END(A) |
| -4.10 | CLOSING_END(A,B) |
| -3.95 | STRONG_THROTTLE_END(B) |
| -3.60 | CLOSING_END(B,B:track_001) |
| -2.45 | CLOSING_START(B,B:track_001) |
| -2.05 | BRAKE_START(B); HARD_BRAKE_START(B) |
| -1.80 | CLOSING_START(A,B); CRITICAL_TTC_START(B,B:track_001) |
| -1.10 | CRITICAL_TTC_START(A,B) |
| -1.05 | CRITICAL_TTC_END(B,B:track_001) |
| -0.85 | CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A) |
| +0.05 | STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A) |
| +0.15 | MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.70 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_FRONT(A,B) (A:e02) | ego: not yet observed |
| -5.70 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_FRONT(B,B:track_001) (B:e02) | ego: not yet observed |
| -5.25 | B | g05 STRONG_THROTTLE_START(B) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -5.25 | A | g06 CLOSING_START(A,B) (A:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.60 | B | g07 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, STRONG_THROTTLE<br>track_001: IN_EGO_PATH |
| -4.55 | A | g08 STRONG_THROTTLE_START(A) (A:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -4.35 | A | g09 STRONG_THROTTLE_END(A) (A:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, IN_EGO_PATH |
| -4.10 | A | g10 CLOSING_END(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.95 | B | g11 STRONG_THROTTLE_END(B) (B:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, IN_EGO_PATH |
| -3.60 | B | g12 CLOSING_END(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -2.45 | B | g13 CLOSING_START(B,B:track_001) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -2.05 | B | g14 BRAKE_START(B) (B:e08)<br>g15 HARD_BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.80 | A | g16 CLOSING_START(A,B) (A:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -1.80 | B | g17 CRITICAL_TTC_START(B,B:track_001) (B:e10) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| -1.10 | A | g18 CRITICAL_TTC_START(A,B) (A:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -1.05 | B | g19 CRITICAL_TTC_END(B,B:track_001) (B:e11) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -0.85 | B | g20 CLOSING_END(B,B:track_001) (B:e12)<br>g21 MOVING_END(B) (B:e13)<br>g22 STOP_START(B) (B:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH |
| +0.00 | A | g23 COLLISION(A,B) (A:e09)<br>g24 CRITICAL_TTC_END(A,B) (A:e10)<br>g25 CLOSING_END(A,B) (A:e11)<br>g26 STRONG_THROTTLE_START(A) (A:e12) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g23 COLLISION(A,B) (B:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH |
| +0.05 | A | g27 STRONG_THROTTLE_END(A) (A:e13)<br>g28 BRAKE_START(A) (A:e14)<br>g29 HARD_BRAKE_START(A) (A:e15) | ego: MOVING, STRONG_THROTTLE<br>track_001: IN_EGO_PATH |
| +0.15 | A | g30 MOVING_END(A) (A:e16)<br>g31 STOP_START(A) (A:e17) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH |
| - | C | g32 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g33 STRONG_THROTTLE_START(C) (C:e02) | ego: MOVING |
| - | C | g34 STRONG_THROTTLE_END(C) (C:e03) | ego: MOVING, STRONG_THROTTLE |
| - | C | g35 SPEED_LIMIT_EXCEEDED_START(C) (C:e04) | ego: MOVING |
| - | C | g36 BRAKE_START(C) (C:e05)<br>g37 HARD_BRAKE_START(C) (C:e06) | ego: MOVING, SPEED_LIMIT_EXCEEDED |
| - | C | g38 SPEED_LIMIT_EXCEEDED_END(C) (C:e07) | ego: MOVING, BRAKE, HARD_BRAKE, SPEED_LIMIT_EXCEEDED |
| - | C | g39 MOVING_END(C) (C:e08)<br>g40 STOP_START(C) (C:e09) | ego: MOVING, BRAKE, HARD_BRAKE |
| - | C | g41 HARD_BRAKE_END(C) (C:e10)<br>g42 BRAKE_END(C) (C:e11)<br>g43 STRONG_THROTTLE_START(C) (C:e12) | ego: STOP, BRAKE, HARD_BRAKE |
| - | C | g44 STOP_END(C) (C:e13)<br>g45 MOVING_START(C) (C:e14) | ego: STOP, STRONG_THROTTLE |

## Plain-language reading

- 5.70 s before the matched collision, A started moving (already the case when first observed).
- 5.70 s before the matched collision, B started moving (already the case when first observed).
- 5.70 s before the matched collision, A's radar started tracking B, which appeared in front of it.
- 5.70 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared in front of it.
- 5.25 s before the matched collision, B started applying strong throttle.
- 5.25 s before the matched collision, A observed B start closing in.
- 4.60 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.55 s before the matched collision, A started applying strong throttle.
- 4.35 s before the matched collision, A stopped applying strong throttle.
- 4.10 s before the matched collision, A observed B stop closing in.
- 3.95 s before the matched collision, B stopped applying strong throttle.
- 3.60 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 2.45 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.05 s before the matched collision, B started braking.
- 2.05 s before the matched collision, B started braking hard.
- 1.80 s before the matched collision, A observed B start closing in.
- 1.80 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.10 s before the matched collision, A's time-to-contact with B became critical.
- 1.05 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 0.85 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 0.85 s before the matched collision, B stopped moving.
- 0.85 s before the matched collision, B came to a stop.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 31407, B: 31407 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- At the matched collision, A started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.15 s after the matched collision, A stopped moving.
- 0.15 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.50 s) C started applying strong throttle.
- (unaligned, C local time 2.05 s) C stopped applying strong throttle.
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 2.95 s) C started braking hard.
- (unaligned, C local time 3.10 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 12.95 s) C stopped braking hard.
- (unaligned, C local time 12.95 s) C released the brake.
- (unaligned, C local time 12.95 s) C started applying strong throttle.
- (unaligned, C local time 13.75 s) C left its stop.
- (unaligned, C local time 13.75 s) C started moving.
