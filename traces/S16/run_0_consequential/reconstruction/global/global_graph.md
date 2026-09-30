# Global graph - S16/run_0_consequential

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e05 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 2695.68 vs 2695.68 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 5.60 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 15.63 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.40 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>at the contact: minimum range 0.59 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.46 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.15 | TRACK_APPEARED | B | A | B:e02 @ 0.00 |  |
| g04 | -4.45 | STRONG_THROTTLE_START | A | - | A:e02 @ 0.70 |  |
| g05 | -4.45 | CLOSING_START | B | A | B:e03 @ 0.70 |  |
| g06 | -4.40 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g07 | -3.80 | STRONG_THROTTLE_START | B | - | B:e05 @ 1.35 |  |
| g08 | -3.75 | CRITICAL_TTC_END | B | A | B:e06 @ 1.40 |  |
| g09 | -3.75 | CLOSING_END | B | A | B:e07 @ 1.40 |  |
| g10 | -3.35 | STRONG_THROTTLE_END | A | - | A:e03 @ 1.80 |  |
| g11 | -2.65 | STRONG_THROTTLE_END | B | - | B:e08 @ 2.50 |  |
| g12 | -1.20 | BRAKE_START | A | - | A:e04 @ 3.95 |  |
| g13 | -0.90 | CLOSING_START | B | A | B:e09 @ 4.25 |  |
| g14 | -0.75 | CRITICAL_TTC_START | B | A | B:e10 @ 4.40 |  |
| g15 | -0.40 | BRAKE_START | B | - | B:e11 @ 4.75 |  |
| g16 | 0.00 | COLLISION | - | A, B | A:e05 @ 5.15, B:e12 @ 5.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 6073.81, B 6073.81 |
| g17 | 0.00 | TRACK_APPEARED | A | A:track_001 | A:e06 @ 5.15 |  |
| g18 | 0.00 | TRACK_APPEARED | A | A:track_002 | A:e07 @ 5.15 |  |
| g19 | 0.00 | CLOSING_START | A | A:track_001 | A:e08 @ 5.15 | active_at_first_observation=True |
| g20 | 0.00 | CLOSING_START | A | A:track_002 | A:e09 @ 5.15 | active_at_first_observation=True |
| g21 | 0.00 | CRITICAL_TTC_START | A | A:track_001 | A:e10 @ 5.15 | active_at_first_observation=True |
| g22 | 0.05 | CRITICAL_TTC_END | B | A | B:e13 @ 5.20 |  |
| g23 | 0.05 | CLOSING_END | B | A | B:e14 @ 5.20 |  |
| g24 | 0.05 | BRAKE_END | A | - | A:e11 @ 5.20 |  |
| g25 | 0.05 | HARD_BRAKE_START | B | - | B:e15 @ 5.20 |  |
| g26 | 0.40 | TRACK_APPEARED | A | A:track_003 | A:e12 @ 5.55 |  |
| g27 | 0.45 | CLOSING_END | A | A:track_002 | A:e13 @ 5.60 |  |
| g28 | 0.45 | MOVING_END | B | - | B:e16 @ 5.60 |  |
| g29 | 0.45 | STOP_START | B | - | B:e17 @ 5.60 |  |
| g30 | 0.50 | EGO_PATH_ENTRY | A | A:track_001 | A:e14 @ 5.65 |  |
| g31 | 0.50 | TRACK_LOST | A | A:track_002 | A:e15 @ 5.65 |  |
| g32 | 0.75 | COLLISION | A | - | A:e16 @ 5.90 | peak_impulse=2695.68 |
| g33 | 0.85 | CRITICAL_TTC_END | A | A:track_001 | A:e17 @ 6.00 |  |
| g34 | 0.85 | CLOSING_END | A | A:track_001 | A:e18 @ 6.00 |  |
| g35 | 0.90 | MOVING_END | A | - | A:e19 @ 6.05 |  |
| g36 | 0.90 | STOP_START | A | - | A:e20 @ 6.05 |  |
| g37 | 1.05 | TRACK_LOST | A | A:track_003 | A:e21 @ 6.20 |  |
| g38 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g39 | - | MOVING_END | C | - | C:e02 @ 0.30 |  |
| g40 | - | STOP_START | C | - | C:e03 @ 0.30 |  |
| g41 | - | COLLISION | C | - | C:e04 @ 5.90 | peak_impulse=2695.68 |
| g42 | - | STOP_END | C | - | C:e05 @ 5.90 |  |
| g43 | - | MOVING_START | C | - | C:e06 @ 5.90 |  |
| g44 | - | BRAKE_START | C | - | C:e07 @ 5.95 |  |
| g45 | - | HARD_BRAKE_START | C | - | C:e08 @ 5.95 |  |
| g46 | - | MOVING_END | C | - | C:e09 @ 6.05 |  |
| g47 | - | STOP_START | C | - | C:e10 @ 6.05 |  |

## Edges

```
    g01 --PRECEDES--> g04
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g04
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
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
    g15 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g16 --PRECEDES--> g22
    g16 --PRECEDES--> g23
    g16 --PRECEDES--> g24
    g16 --PRECEDES--> g25
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g17 --PRECEDES--> g25
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g18 --PRECEDES--> g24
    g18 --PRECEDES--> g25
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g19 --PRECEDES--> g25
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g37
    g17 --SAME_TRACK--> g19
    g18 --SAME_TRACK--> g20
    g17 --SAME_TRACK--> g21
    g18 --SAME_TRACK--> g27
    g17 --SAME_TRACK--> g30
    g18 --SAME_TRACK--> g31
    g17 --SAME_TRACK--> g33
    g17 --SAME_TRACK--> g34
    g26 --SAME_TRACK--> g37
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g13
    g03 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g22
    g03 --SAME_TRACK--> g23
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.15 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED(B,A) |
| -4.45 | STRONG_THROTTLE_START(A); CLOSING_START(B,A) |
| -4.40 | CRITICAL_TTC_START(B,A) |
| -3.80 | STRONG_THROTTLE_START(B) |
| -3.75 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| -3.35 | STRONG_THROTTLE_END(A) |
| -2.65 | STRONG_THROTTLE_END(B) |
| -1.20 | BRAKE_START(A) |
| -0.90 | CLOSING_START(B,A) |
| -0.75 | CRITICAL_TTC_START(B,A) |
| -0.40 | BRAKE_START(B) |
| +0.00 | COLLISION(A,B); TRACK_APPEARED(A,A:track_001); TRACK_APPEARED(A,A:track_002); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CRITICAL_TTC_START(A,A:track_001) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A); HARD_BRAKE_START(B) |
| +0.40 | TRACK_APPEARED(A,A:track_003) |
| +0.45 | CLOSING_END(A,A:track_002); MOVING_END(B); STOP_START(B) |
| +0.50 | EGO_PATH_ENTRY(A,A:track_001); TRACK_LOST(A,A:track_002) |
| +0.75 | COLLISION(A) |
| +0.85 | CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001) |
| +0.90 | MOVING_END(A); STOP_START(A) |
| +1.05 | TRACK_LOST(A,A:track_003) |

## Plain-language reading

- 5.15 s before the matched collision, A started moving (already the case when first observed).
- 5.15 s before the matched collision, B started moving (already the case when first observed).
- 5.15 s before the matched collision, B's radar started tracking A.
- 4.45 s before the matched collision, A started applying strong throttle.
- 4.45 s before the matched collision, B observed A start closing in.
- 4.40 s before the matched collision, B's time-to-contact with A became critical.
- 3.80 s before the matched collision, B started applying strong throttle.
- 3.75 s before the matched collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the matched collision, B observed A stop closing in.
- 3.35 s before the matched collision, A stopped applying strong throttle.
- 2.65 s before the matched collision, B stopped applying strong throttle.
- 1.20 s before the matched collision, A started braking.
- 0.90 s before the matched collision, B observed A start closing in.
- 0.75 s before the matched collision, B's time-to-contact with A became critical.
- 0.40 s before the matched collision, B started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- At the matched collision, A's radar started tracking unidentified object A:track_001.
- At the matched collision, A's radar started tracking unidentified object A:track_002.
- At the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- At the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- At the matched collision, A's time-to-contact with unidentified object A:track_001 became critical (already the case when first observed).
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, A released the brake.
- 0.05 s after the matched collision, B started braking hard.
- 0.40 s after the matched collision, A's radar started tracking unidentified object A:track_003.
- 0.45 s after the matched collision, A observed unidentified object A:track_002 stop closing in.
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.50 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.50 s after the matched collision, A's radar lost unidentified object A:track_002.
- 0.75 s after the matched collision, A's collision sensor recorded a contact (peak impulse 2696 N*s).
- 0.85 s after the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.85 s after the matched collision, A observed unidentified object A:track_001 stop closing in.
- 0.90 s after the matched collision, A stopped moving.
- 0.90 s after the matched collision, A came to a stop.
- 1.05 s after the matched collision, A's radar lost unidentified object A:track_003.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.30 s) C stopped moving.
- (unaligned, C local time 0.30 s) C came to a stop.
- (unaligned, C local time 5.90 s) C's collision sensor recorded a contact (peak impulse 2696 N*s).
- (unaligned, C local time 5.90 s) C left its stop.
- (unaligned, C local time 5.90 s) C started moving.
- (unaligned, C local time 5.95 s) C started braking.
- (unaligned, C local time 5.95 s) C started braking hard.
- (unaligned, C local time 6.05 s) C stopped moving.
- (unaligned, C local time 6.05 s) C came to a stop.
