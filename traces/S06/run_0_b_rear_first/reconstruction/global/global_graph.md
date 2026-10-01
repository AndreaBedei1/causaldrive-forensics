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
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 6.00 | -6.00 | reported the reference collision collision_001 |
| B | ALIGNED | B:e20 | 6.00 | -6.00 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 31488.29 vs 31488.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: B and C both recorded a collision; peak impulses 21812.15 vs 21812.15 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 6.00 s before the matched collision<br>not at the contact: last seen 1.45 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.04 m/s over 1.5 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 4.45 s before the matched collision<br>not at the contact: last seen 3.05 s before the matched collision (window 0.50 s)<br>speed not comparable with B's own speed before the collision |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 31488.29 vs 31488.29 N*s)<br>tracked for 6.00 s before the matched collision<br>at the contact: minimum range 0.21 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed disagrees with A's own speed: RMSE 11.16 m/s (> 1.50) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.00 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -6.00 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -6.00 | TRACK_APPEARED | A | A:track_001 | A:e02 @ 0.00 |  |
| g04 | -6.00 | TRACK_APPEARED | B | B:track_001 | B:e02 @ 0.00 |  |
| g05 | -5.65 | STRONG_THROTTLE_START | B | - | B:e03 @ 0.35 |  |
| g06 | -5.55 | CLOSING_START | A | A:track_001 | A:e03 @ 0.45 |  |
| g07 | -4.90 | CLOSING_START | B | B:track_001 | B:e04 @ 1.10 |  |
| g08 | -4.85 | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g09 | -4.65 | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g10 | -4.45 | TRACK_APPEARED | A | A:track_002 | A:e06 @ 1.55 |  |
| g11 | -4.40 | CLOSING_END | A | A:track_001 | A:e07 @ 1.60 |  |
| g12 | -4.25 | STRONG_THROTTLE_END | B | - | B:e05 @ 1.75 |  |
| g13 | -3.90 | CLOSING_END | B | B:track_001 | B:e06 @ 2.10 |  |
| g14 | -3.05 | TRACK_LOST | A | A:track_002 | A:e08 @ 2.95 |  |
| g15 | -2.80 | CLOSING_START | B | B:track_001 | B:e07 @ 3.20 |  |
| g16 | -2.55 | PREDICTED_PATH_CONFLICT_START | B | B:track_001 | B:e08 @ 3.45 |  |
| g17 | -2.30 | CRITICAL_TTC_START | B | B:track_001 | B:e09 @ 3.70 |  |
| g18 | -1.45 | TRACK_LOST | A | A:track_001 | A:e09 @ 4.55 |  |
| g19 | -1.40 | COLLISION | B | - | B:e10 @ 4.60 | peak_impulse=21812.15 |
| g20 | -1.40 | STRONG_THROTTLE_START | B | - | B:e11 @ 4.60 |  |
| g21 | -1.35 | PREDICTED_PATH_CONFLICT_END | B | B:track_001 | B:e12 @ 4.65 |  |
| g22 | -1.35 | CRITICAL_TTC_END | B | B:track_001 | B:e13 @ 4.65 |  |
| g23 | -1.35 | CLOSING_END | B | B:track_001 | B:e14 @ 4.65 |  |
| g24 | -1.35 | STRONG_THROTTLE_END | B | - | B:e15 @ 4.65 |  |
| g25 | -1.35 | BRAKE_START | B | - | B:e16 @ 4.65 |  |
| g26 | -1.35 | HARD_BRAKE_START | B | - | B:e17 @ 4.65 |  |
| g27 | -1.25 | MOVING_END | B | - | B:e18 @ 4.75 |  |
| g28 | -1.25 | STOP_START | B | - | B:e19 @ 4.75 |  |
| g29 | 0.00 | COLLISION | - | A, B | A:e10 @ 6.00, B:e20 @ 6.00 | matched_event=collision_001; reference_event=True; peak_impulse=A 31488.29, B 31488.29 |
| g30 | 0.00 | STRONG_THROTTLE_START | A | - | A:e11 @ 6.00 |  |
| g31 | 0.05 | STRONG_THROTTLE_END | A | - | A:e12 @ 6.05 |  |
| g32 | 0.05 | BRAKE_START | A | - | A:e13 @ 6.05 |  |
| g33 | 0.05 | HARD_BRAKE_START | A | - | A:e14 @ 6.05 |  |
| g34 | 0.20 | MOVING_END | A | - | A:e15 @ 6.20 |  |
| g35 | 0.20 | STOP_START | A | - | A:e16 @ 6.20 |  |
| g36 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g37 | - | STRONG_THROTTLE_START | C | - | C:e02 @ 0.50 |  |
| g38 | - | STRONG_THROTTLE_END | C | - | C:e03 @ 2.05 |  |
| g39 | - | SPEED_LIMIT_EXCEEDED_START | C | - | C:e04 @ 2.40 |  |
| g40 | - | BRAKE_START | C | - | C:e05 @ 2.95 |  |
| g41 | - | HARD_BRAKE_START | C | - | C:e06 @ 2.95 |  |
| g42 | - | SPEED_LIMIT_EXCEEDED_END | C | - | C:e07 @ 3.05 |  |
| g43 | - | MOVING_END | C | - | C:e08 @ 4.05 |  |
| g44 | - | STOP_START | C | - | C:e09 @ 4.05 |  |
| g45 | - | COLLISION | C | - | C:e10 @ 4.60 | peak_impulse=21812.15 |

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
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g19 --PRECEDES--> g25
    g19 --PRECEDES--> g26
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g18
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g15
    g04 --SAME_TRACK--> g16
    g04 --SAME_TRACK--> g17
    g04 --SAME_TRACK--> g21
    g04 --SAME_TRACK--> g22
    g04 --SAME_TRACK--> g23
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -6.00 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(B,B:track_001) |
| -5.65 | STRONG_THROTTLE_START(B) |
| -5.55 | CLOSING_START(A,A:track_001) |
| -4.90 | CLOSING_START(B,B:track_001) |
| -4.85 | STRONG_THROTTLE_START(A) |
| -4.65 | STRONG_THROTTLE_END(A) |
| -4.45 | TRACK_APPEARED(A,A:track_002) |
| -4.40 | CLOSING_END(A,A:track_001) |
| -4.25 | STRONG_THROTTLE_END(B) |
| -3.90 | CLOSING_END(B,B:track_001) |
| -3.05 | TRACK_LOST(A,A:track_002) |
| -2.80 | CLOSING_START(B,B:track_001) |
| -2.55 | PREDICTED_PATH_CONFLICT_START(B,B:track_001) |
| -2.30 | CRITICAL_TTC_START(B,B:track_001) |
| -1.45 | TRACK_LOST(A,A:track_001) |
| -1.40 | COLLISION(B); STRONG_THROTTLE_START(B) |
| -1.35 | PREDICTED_PATH_CONFLICT_END(B,B:track_001); CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B) |
| -1.25 | MOVING_END(B); STOP_START(B) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(A) |
| +0.05 | STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A) |
| +0.20 | MOVING_END(A); STOP_START(A) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -6.00 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED(A,A:track_001) (A:e02) | ego: not yet observed |
| -6.00 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED(B,B:track_001) (B:e02) | ego: not yet observed |
| -5.65 | B | g05 STRONG_THROTTLE_START(B) (B:e03) | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH |
| -5.55 | A | g06 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH |
| -4.90 | B | g07 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, IN_EGO_PATH |
| -4.85 | A | g08 STRONG_THROTTLE_START(A) (A:e04) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH |
| -4.65 | A | g09 STRONG_THROTTLE_END(A) (A:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH |
| -4.45 | A | g10 TRACK_APPEARED(A,A:track_002) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH |
| -4.40 | A | g11 CLOSING_END(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>track_002: VISIBLE, IN_EGO_PATH |
| -4.25 | B | g12 STRONG_THROTTLE_END(B) (B:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH |
| -3.90 | B | g13 CLOSING_END(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH |
| -3.05 | A | g14 TRACK_LOST(A,A:track_002) (A:e08) | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH<br>track_002: VISIBLE, IN_EGO_PATH |
| -2.80 | B | g15 CLOSING_START(B,B:track_001) (B:e07) | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH |
| -2.55 | B | g16 PREDICTED_PATH_CONFLICT_START(B,B:track_001) (B:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH |
| -2.30 | B | g17 CRITICAL_TTC_START(B,B:track_001) (B:e09) | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT |
| -1.45 | A | g18 TRACK_LOST(A,A:track_001) (A:e09) | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002 |
| -1.40 | B | g19 COLLISION(B) (B:e10)<br>g20 STRONG_THROTTLE_START(B) (B:e11) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT |
| -1.35 | B | g21 PREDICTED_PATH_CONFLICT_END(B,B:track_001) (B:e12)<br>g22 CRITICAL_TTC_END(B,B:track_001) (B:e13)<br>g23 CLOSING_END(B,B:track_001) (B:e14)<br>g24 STRONG_THROTTLE_END(B) (B:e15)<br>g25 BRAKE_START(B) (B:e16)<br>g26 HARD_BRAKE_START(B) (B:e17) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT |
| -1.25 | B | g27 MOVING_END(B) (B:e18)<br>g28 STOP_START(B) (B:e19) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH |
| +0.00 | A | g29 COLLISION(A,B) (A:e10)<br>g30 STRONG_THROTTLE_START(A) (A:e11) | ego: MOVING<br>lost (states UNKNOWN): track_001, track_002 |
| +0.00 | B | g29 COLLISION(A,B) (B:e20) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH |
| +0.05 | A | g31 STRONG_THROTTLE_END(A) (A:e12)<br>g32 BRAKE_START(A) (A:e13)<br>g33 HARD_BRAKE_START(A) (A:e14) | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001, track_002 |
| +0.20 | A | g34 MOVING_END(A) (A:e15)<br>g35 STOP_START(A) (A:e16) | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001, track_002 |
| - | C | g36 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g37 STRONG_THROTTLE_START(C) (C:e02) | ego: MOVING |
| - | C | g38 STRONG_THROTTLE_END(C) (C:e03) | ego: MOVING, STRONG_THROTTLE |
| - | C | g39 SPEED_LIMIT_EXCEEDED_START(C) (C:e04) | ego: MOVING |
| - | C | g40 BRAKE_START(C) (C:e05)<br>g41 HARD_BRAKE_START(C) (C:e06) | ego: MOVING, SPEED_LIMIT_EXCEEDED |
| - | C | g42 SPEED_LIMIT_EXCEEDED_END(C) (C:e07) | ego: MOVING, BRAKE, HARD_BRAKE, SPEED_LIMIT_EXCEEDED |
| - | C | g43 MOVING_END(C) (C:e08)<br>g44 STOP_START(C) (C:e09) | ego: MOVING, BRAKE, HARD_BRAKE |
| - | C | g45 COLLISION(C) (C:e10) | ego: STOP, BRAKE, HARD_BRAKE |

## Plain-language reading

- 6.00 s before the matched collision, A started moving (already the case when first observed).
- 6.00 s before the matched collision, B started moving (already the case when first observed).
- 6.00 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 6.00 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 5.65 s before the matched collision, B started applying strong throttle.
- 5.55 s before the matched collision, A observed unidentified object A:track_001 start closing in.
- 4.90 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.85 s before the matched collision, A started applying strong throttle.
- 4.65 s before the matched collision, A stopped applying strong throttle.
- 4.45 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 4.40 s before the matched collision, A observed unidentified object A:track_001 stop closing in.
- 4.25 s before the matched collision, B stopped applying strong throttle.
- 3.90 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 3.05 s before the matched collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 2.80 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.55 s before the matched collision, B predicted a path conflict with unidentified object B:track_001 (close approach ahead if both keep their motion).
- 2.30 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.45 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the matched collision, B's collision sensor recorded a contact (peak impulse 21812 N*s).
- 1.40 s before the matched collision, B started applying strong throttle.
- 1.35 s before the matched collision, B stopped predicting a path conflict with unidentified object B:track_001.
- 1.35 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.35 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.35 s before the matched collision, B stopped applying strong throttle.
- 1.35 s before the matched collision, B started braking.
- 1.35 s before the matched collision, B started braking hard.
- 1.25 s before the matched collision, B stopped moving.
- 1.25 s before the matched collision, B came to a stop.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 31488, B: 31488 N*s).
- At the matched collision, A started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.20 s after the matched collision, A stopped moving.
- 0.20 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.50 s) C started applying strong throttle.
- (unaligned, C local time 2.05 s) C stopped applying strong throttle.
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 2.95 s) C started braking hard.
- (unaligned, C local time 3.05 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 4.60 s) C's collision sensor recorded a contact (peak impulse 21812 N*s).
