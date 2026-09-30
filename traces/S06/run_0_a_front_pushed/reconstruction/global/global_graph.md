# Global graph - S06/run_0_a_front_pushed

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 5.90 | -5.90 | reported the reference collision collision_001 |
| B | ALIGNED | B:e18 | 5.90 | -5.90 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | its collision report matched no other graph |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 11621.71 vs 11621.71 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.67 | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.90 s before the matched collision<br>at the contact: minimum range 1.23 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 1.33 m/s over 3.0 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 4.35 s before the matched collision<br>not at the contact: last seen 2.95 s before the matched collision (window 0.50 s)<br>speed not comparable with B's own speed before the collision |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 11621.71 vs 11621.71 N*s)<br>tracked for 5.90 s before the matched collision<br>at the contact: minimum range 1.24 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed disagrees with A's own speed: RMSE 10.78 m/s (> 1.50) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.90 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.90 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.90 | TRACK_APPEARED | A | B | A:e02 @ 0.00 |  |
| g04 | -5.90 | TRACK_APPEARED | B | B:track_001 | B:e02 @ 0.00 |  |
| g05 | -5.55 | STRONG_THROTTLE_START | B | - | B:e03 @ 0.35 |  |
| g06 | -5.45 | CLOSING_START | A | B | A:e03 @ 0.45 |  |
| g07 | -4.80 | CLOSING_START | B | B:track_001 | B:e04 @ 1.10 |  |
| g08 | -4.75 | STRONG_THROTTLE_START | A | - | A:e04 @ 1.15 |  |
| g09 | -4.55 | STRONG_THROTTLE_END | A | - | A:e05 @ 1.35 |  |
| g10 | -4.35 | TRACK_APPEARED | A | A:track_002 | A:e06 @ 1.55 |  |
| g11 | -4.30 | CLOSING_END | A | B | A:e07 @ 1.60 |  |
| g12 | -4.15 | STRONG_THROTTLE_END | B | - | B:e05 @ 1.75 |  |
| g13 | -3.80 | CLOSING_END | B | B:track_001 | B:e06 @ 2.10 |  |
| g14 | -2.95 | TRACK_LOST | A | A:track_002 | A:e08 @ 2.95 |  |
| g15 | -2.70 | CLOSING_START | B | B:track_001 | B:e07 @ 3.20 |  |
| g16 | -2.20 | BRAKE_START | B | - | B:e08 @ 3.70 |  |
| g17 | -2.20 | HARD_BRAKE_START | B | - | B:e09 @ 3.70 |  |
| g18 | -2.20 | CRITICAL_TTC_START | B | B:track_001 | B:e10 @ 3.70 |  |
| g19 | -1.90 | CLOSING_START | A | B | A:e09 @ 4.00 |  |
| g20 | -1.20 | CRITICAL_TTC_START | A | B | A:e10 @ 4.70 |  |
| g21 | -1.00 | CRITICAL_TTC_END | B | B:track_001 | B:e11 @ 4.90 |  |
| g22 | -1.00 | CLOSING_END | B | B:track_001 | B:e12 @ 4.90 |  |
| g23 | -1.00 | MOVING_END | B | - | B:e13 @ 4.90 |  |
| g24 | -1.00 | STOP_START | B | - | B:e14 @ 4.90 |  |
| g25 | -0.35 | BRAKE_START | A | - | A:e11 @ 5.55 |  |
| g26 | -0.20 | HARD_BRAKE_END | B | - | B:e15 @ 5.70 |  |
| g27 | -0.20 | BRAKE_END | B | - | B:e16 @ 5.70 |  |
| g28 | -0.20 | STRONG_THROTTLE_START | B | - | B:e17 @ 5.70 |  |
| g29 | 0.00 | COLLISION | - | A, B | A:e12 @ 5.90, B:e18 @ 5.90 | matched_event=collision_001; reference_event=True; peak_impulse=A 11621.71, B 11621.71 |
| g30 | 0.00 | STOP_END | B | - | B:e19 @ 5.90 |  |
| g31 | 0.00 | MOVING_START | B | - | B:e20 @ 5.90 |  |
| g32 | 0.05 | HARD_BRAKE_START | A | - | A:e13 @ 5.95 |  |
| g33 | 0.30 | TRACK_LOST | B | B:track_001 | B:e21 @ 6.20 |  |
| g34 | 0.35 | CRITICAL_TTC_END | A | B | A:e14 @ 6.25 |  |
| g35 | 0.35 | CLOSING_END | A | B | A:e15 @ 6.25 |  |
| g36 | 0.35 | MOVING_END | A | - | A:e16 @ 6.25 |  |
| g37 | 0.35 | STOP_START | A | - | A:e17 @ 6.25 |  |
| g38 | 0.40 | MOVING_END | B | - | B:e22 @ 6.30 |  |
| g39 | 0.40 | STOP_START | B | - | B:e23 @ 6.30 |  |
| g40 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g41 | - | STRONG_THROTTLE_START | C | - | C:e02 @ 0.50 |  |
| g42 | - | STRONG_THROTTLE_END | C | - | C:e03 @ 2.05 |  |
| g43 | - | SPEED_LIMIT_EXCEEDED_START | C | - | C:e04 @ 2.40 |  |
| g44 | - | BRAKE_START | C | - | C:e05 @ 2.95 |  |
| g45 | - | HARD_BRAKE_START | C | - | C:e06 @ 2.95 |  |
| g46 | - | SPEED_LIMIT_EXCEEDED_END | C | - | C:e07 @ 3.05 |  |
| g47 | - | MOVING_END | C | - | C:e08 @ 4.05 |  |
| g48 | - | STOP_START | C | - | C:e09 @ 4.05 |  |
| g49 | - | COLLISION | C | - | C:e10 @ 6.15 | peak_impulse=9832.40 |

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
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g19
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
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
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g19
    g03 --SAME_TRACK--> g20
    g03 --SAME_TRACK--> g34
    g03 --SAME_TRACK--> g35
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g15
    g04 --SAME_TRACK--> g18
    g04 --SAME_TRACK--> g21
    g04 --SAME_TRACK--> g22
    g04 --SAME_TRACK--> g33
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.90 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); TRACK_APPEARED(B,B:track_001) |
| -5.55 | STRONG_THROTTLE_START(B) |
| -5.45 | CLOSING_START(A,B) |
| -4.80 | CLOSING_START(B,B:track_001) |
| -4.75 | STRONG_THROTTLE_START(A) |
| -4.55 | STRONG_THROTTLE_END(A) |
| -4.35 | TRACK_APPEARED(A,A:track_002) |
| -4.30 | CLOSING_END(A,B) |
| -4.15 | STRONG_THROTTLE_END(B) |
| -3.80 | CLOSING_END(B,B:track_001) |
| -2.95 | TRACK_LOST(A,A:track_002) |
| -2.70 | CLOSING_START(B,B:track_001) |
| -2.20 | BRAKE_START(B); HARD_BRAKE_START(B); CRITICAL_TTC_START(B,B:track_001) |
| -1.90 | CLOSING_START(A,B) |
| -1.20 | CRITICAL_TTC_START(A,B) |
| -1.00 | CRITICAL_TTC_END(B,B:track_001); CLOSING_END(B,B:track_001); MOVING_END(B); STOP_START(B) |
| -0.35 | BRAKE_START(A) |
| -0.20 | HARD_BRAKE_END(B); BRAKE_END(B); STRONG_THROTTLE_START(B) |
| +0.00 | COLLISION(A,B); STOP_END(B); MOVING_START(B) |
| +0.05 | HARD_BRAKE_START(A) |
| +0.30 | TRACK_LOST(B,B:track_001) |
| +0.35 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B); MOVING_END(A); STOP_START(A) |
| +0.40 | MOVING_END(B); STOP_START(B) |

## Plain-language reading

- 5.90 s before the matched collision, A started moving (already the case when first observed).
- 5.90 s before the matched collision, B started moving (already the case when first observed).
- 5.90 s before the matched collision, A's radar started tracking B.
- 5.90 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 5.55 s before the matched collision, B started applying strong throttle.
- 5.45 s before the matched collision, A observed B start closing in.
- 4.80 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 4.75 s before the matched collision, A started applying strong throttle.
- 4.55 s before the matched collision, A stopped applying strong throttle.
- 4.35 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 4.30 s before the matched collision, A observed B stop closing in.
- 4.15 s before the matched collision, B stopped applying strong throttle.
- 3.80 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 2.95 s before the matched collision, A's radar lost unidentified object A:track_002.
- 2.70 s before the matched collision, B observed unidentified object B:track_001 start closing in.
- 2.20 s before the matched collision, B started braking.
- 2.20 s before the matched collision, B started braking hard.
- 2.20 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.90 s before the matched collision, A observed B start closing in.
- 1.20 s before the matched collision, A's time-to-contact with B became critical.
- 1.00 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.00 s before the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.00 s before the matched collision, B stopped moving.
- 1.00 s before the matched collision, B came to a stop.
- 0.35 s before the matched collision, A started braking.
- 0.20 s before the matched collision, B stopped braking hard.
- 0.20 s before the matched collision, B released the brake.
- 0.20 s before the matched collision, B started applying strong throttle.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 11622, B: 11622 N*s).
- At the matched collision, B left its stop.
- At the matched collision, B started moving.
- 0.05 s after the matched collision, A started braking hard.
- 0.30 s after the matched collision, B's radar lost unidentified object B:track_001.
- 0.35 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.35 s after the matched collision, A observed B stop closing in.
- 0.35 s after the matched collision, A stopped moving.
- 0.35 s after the matched collision, A came to a stop.
- 0.40 s after the matched collision, B stopped moving.
- 0.40 s after the matched collision, B came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.50 s) C started applying strong throttle.
- (unaligned, C local time 2.05 s) C stopped applying strong throttle.
- (unaligned, C local time 2.40 s) C began exceeding the speed limit.
- (unaligned, C local time 2.95 s) C started braking.
- (unaligned, C local time 2.95 s) C started braking hard.
- (unaligned, C local time 3.05 s) C returned within the speed limit.
- (unaligned, C local time 4.05 s) C stopped moving.
- (unaligned, C local time 4.05 s) C came to a stop.
- (unaligned, C local time 6.15 s) C's collision sensor recorded a contact (peak impulse 9832 N*s).
