# Global graph - S16/run_0_independent

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| C | recorder | clock ALIGNED; observed by others as: A:track_001 |
| A:track_002 | anonymous_track | seen only by A; candidate: C |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |

## Graph alignment

Reference event: `collision_002`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e22 | 14.10 | -14.10 | reported the reference collision collision_002 |
| B | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |
| C | ALIGNED | C:e06 | 14.10 | -14.10 | reported the reference collision collision_002 |

Estimated relative clock offsets: C - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 9089.81 vs 9089.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 1.00 | A and C both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 2.95 s before the matched collision<br>at the contact: minimum range 0.06 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with C's own speed: RMSE 0.08 m/s over 2.9 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and C both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 2.95 s before the matched collision<br>not at the contact: last seen 0.60 s before the matched collision (window 0.50 s)<br>track speed agrees with C's own speed: RMSE 0.07 m/s over 2.3 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -14.10 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -14.10 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -13.60 | MOVING_END | C | - | C:e02 @ 0.50 |  |
| g04 | -13.60 | STOP_START | C | - | C:e03 @ 0.50 |  |
| g05 | -13.40 | STRONG_THROTTLE_START | A | - | A:e02 @ 0.70 |  |
| g06 | -12.30 | STRONG_THROTTLE_END | A | - | A:e03 @ 1.80 |  |
| g07 | -10.15 | BRAKE_START | A | - | A:e04 @ 3.95 |  |
| g08 | -8.95 | COLLISION | A | - | A:e05 @ 5.15 | peak_impulse=6073.81 |
| g09 | -8.30 | MOVING_END | A | - | A:e06 @ 5.80 |  |
| g10 | -8.30 | STOP_START | A | - | A:e07 @ 5.80 |  |
| g11 | -3.15 | BRAKE_END | A | - | A:e08 @ 10.95 |  |
| g12 | -3.15 | STRONG_THROTTLE_START | A | - | A:e09 @ 10.95 |  |
| g13 | -2.95 | TRACK_APPEARED | A | A:track_002 | A:e11 @ 11.15 |  |
| g14 | -2.95 | TRACK_APPEARED | A | C | A:e10 @ 11.15 |  |
| g15 | -2.70 | STOP_END | A | - | A:e12 @ 11.40 |  |
| g16 | -2.70 | MOVING_START | A | - | A:e13 @ 11.40 |  |
| g17 | -2.30 | CLOSING_START | A | A:track_002 | A:e15 @ 11.80 |  |
| g18 | -2.30 | CLOSING_START | A | C | A:e14 @ 11.80 |  |
| g19 | -2.15 | STOP_END | C | - | C:e04 @ 11.95 |  |
| g20 | -2.15 | MOVING_START | C | - | C:e05 @ 11.95 |  |
| g21 | -2.10 | EGO_PATH_ENTRY | A | A:track_002 | A:e16 @ 12.00 |  |
| g22 | -1.90 | EGO_PATH_ENTRY | A | C | A:e17 @ 12.20 |  |
| g23 | -1.55 | CRITICAL_TTC_START | A | C | A:e18 @ 12.55 |  |
| g24 | -1.40 | STRONG_THROTTLE_END | A | - | A:e19 @ 12.70 |  |
| g25 | -1.35 | CRITICAL_TTC_START | A | A:track_002 | A:e20 @ 12.75 |  |
| g26 | -0.60 | TRACK_LOST | A | A:track_002 | A:e21 @ 13.50 |  |
| g27 | 0.00 | COLLISION | - | A, C | A:e22 @ 14.10, C:e06 @ 14.10 | matched_event=collision_002; reference_event=True; peak_impulse=A 9089.81, C 9089.81 |
| g28 | 0.00 | CRITICAL_TTC_END | A | C | A:e23 @ 14.10 |  |
| g29 | 0.00 | CLOSING_END | A | C | A:e24 @ 14.10 |  |
| g30 | 0.00 | STRONG_THROTTLE_START | A | - | A:e25 @ 14.10 |  |
| g31 | 0.00 | BRAKE_START | C | - | C:e07 @ 14.10 |  |
| g32 | 0.05 | HARD_BRAKE_START | C | - | C:e08 @ 14.15 |  |
| g33 | 0.25 | TRACK_LOST | A | C | A:e26 @ 14.35 |  |
| g34 | 0.55 | MOVING_END | A | - | A:e27 @ 14.65 |  |
| g35 | 0.55 | MOVING_END | C | - | C:e09 @ 14.65 |  |
| g36 | 0.55 | STOP_START | A | - | A:e28 @ 14.65 |  |
| g37 | 0.55 | STOP_START | C | - | C:e10 @ 14.65 |  |
| g38 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g39 | - | TRACK_APPEARED | B | B:track_001 | B:e02 @ 0.00 |  |
| g40 | - | CLOSING_START | B | B:track_001 | B:e03 @ 0.70 |  |
| g41 | - | CRITICAL_TTC_START | B | B:track_001 | B:e04 @ 0.75 |  |
| g42 | - | STRONG_THROTTLE_START | B | - | B:e05 @ 1.35 |  |
| g43 | - | CRITICAL_TTC_END | B | B:track_001 | B:e06 @ 1.40 |  |
| g44 | - | CLOSING_END | B | B:track_001 | B:e07 @ 1.40 |  |
| g45 | - | STRONG_THROTTLE_END | B | - | B:e08 @ 2.50 |  |
| g46 | - | CLOSING_START | B | B:track_001 | B:e09 @ 4.25 |  |
| g47 | - | CRITICAL_TTC_START | B | B:track_001 | B:e10 @ 4.35 |  |
| g48 | - | BRAKE_START | B | - | B:e11 @ 4.75 |  |
| g49 | - | COLLISION | B | - | B:e12 @ 5.15 | peak_impulse=6073.81 |
| g50 | - | CRITICAL_TTC_END | B | B:track_001 | B:e13 @ 5.20 |  |
| g51 | - | CLOSING_END | B | B:track_001 | B:e14 @ 5.20 |  |
| g52 | - | HARD_BRAKE_START | B | - | B:e15 @ 5.20 |  |
| g53 | - | MOVING_END | B | - | B:e16 @ 5.60 |  |
| g54 | - | STOP_START | B | - | B:e17 @ 5.60 |  |
| g55 | - | TRACK_APPEARED | B | B:track_002 | B:e18 @ 12.55 |  |
| g56 | - | EGO_PATH_EXIT | B | B:track_001 | B:e19 @ 13.55 |  |
| g57 | - | TRACK_LOST | B | B:track_001 | B:e20 @ 14.05 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
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
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g28 --PRECEDES--> g32
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g14 --SAME_TRACK--> g18
    g13 --SAME_TRACK--> g17
    g13 --SAME_TRACK--> g21
    g14 --SAME_TRACK--> g22
    g14 --SAME_TRACK--> g23
    g13 --SAME_TRACK--> g25
    g13 --SAME_TRACK--> g26
    g14 --SAME_TRACK--> g28
    g14 --SAME_TRACK--> g29
    g14 --SAME_TRACK--> g33
    g39 --SAME_TRACK--> g40
    g39 --SAME_TRACK--> g41
    g39 --SAME_TRACK--> g43
    g39 --SAME_TRACK--> g44
    g39 --SAME_TRACK--> g46
    g39 --SAME_TRACK--> g47
    g39 --SAME_TRACK--> g50
    g39 --SAME_TRACK--> g51
    g39 --SAME_TRACK--> g56
    g39 --SAME_TRACK--> g57
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -14.10 | MOVING_START(A); MOVING_START(C) |
| -13.60 | MOVING_END(C); STOP_START(C) |
| -13.40 | STRONG_THROTTLE_START(A) |
| -12.30 | STRONG_THROTTLE_END(A) |
| -10.15 | BRAKE_START(A) |
| -8.95 | COLLISION(A) |
| -8.30 | MOVING_END(A); STOP_START(A) |
| -3.15 | BRAKE_END(A); STRONG_THROTTLE_START(A) |
| -2.95 | TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,C) |
| -2.70 | STOP_END(A); MOVING_START(A) |
| -2.30 | CLOSING_START(A,A:track_002); CLOSING_START(A,C) |
| -2.15 | STOP_END(C); MOVING_START(C) |
| -2.10 | EGO_PATH_ENTRY(A,A:track_002) |
| -1.90 | EGO_PATH_ENTRY(A,C) |
| -1.55 | CRITICAL_TTC_START(A,C) |
| -1.40 | STRONG_THROTTLE_END(A) |
| -1.35 | CRITICAL_TTC_START(A,A:track_002) |
| -0.60 | TRACK_LOST(A,A:track_002) |
| +0.00 | COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,C); STRONG_THROTTLE_START(A); BRAKE_START(C) |
| +0.05 | HARD_BRAKE_START(C) |
| +0.25 | TRACK_LOST(A,C) |
| +0.55 | MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |

## Plain-language reading

- 14.10 s before the matched collision, A started moving (already the case when first observed).
- 14.10 s before the matched collision, C started moving (already the case when first observed).
- 13.60 s before the matched collision, C stopped moving.
- 13.60 s before the matched collision, C came to a stop.
- 13.40 s before the matched collision, A started applying strong throttle.
- 12.30 s before the matched collision, A stopped applying strong throttle.
- 10.15 s before the matched collision, A started braking.
- 8.95 s before the matched collision, A's collision sensor recorded a contact (peak impulse 6074 N*s).
- 8.30 s before the matched collision, A stopped moving.
- 8.30 s before the matched collision, A came to a stop.
- 3.15 s before the matched collision, A released the brake.
- 3.15 s before the matched collision, A started applying strong throttle.
- 2.95 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 2.95 s before the matched collision, A's radar started tracking C.
- 2.70 s before the matched collision, A left its stop.
- 2.70 s before the matched collision, A started moving.
- 2.30 s before the matched collision, A observed unidentified object A:track_002 start closing in.
- 2.30 s before the matched collision, A observed C start closing in.
- 2.15 s before the matched collision, C left its stop.
- 2.15 s before the matched collision, C started moving.
- 2.10 s before the matched collision, A observed unidentified object A:track_002 enter its forward path corridor.
- 1.90 s before the matched collision, A observed C enter its forward path corridor.
- 1.55 s before the matched collision, A's time-to-contact with C became critical.
- 1.40 s before the matched collision, A stopped applying strong throttle.
- 1.35 s before the matched collision, A's time-to-contact with unidentified object A:track_002 became critical.
- 0.60 s before the matched collision, A's radar lost unidentified object A:track_002.
- At the matched collision, A and C both recorded this same collision (peak impulses A: 9090, C: 9090 N*s).
- At the matched collision, A's time-to-contact with C stopped being critical.
- At the matched collision, A observed C stop closing in.
- At the matched collision, A started applying strong throttle.
- At the matched collision, C started braking.
- 0.05 s after the matched collision, C started braking hard.
- 0.25 s after the matched collision, A's radar lost C.
- 0.55 s after the matched collision, A stopped moving.
- 0.55 s after the matched collision, C stopped moving.
- 0.55 s after the matched collision, A came to a stop.
- 0.55 s after the matched collision, C came to a stop.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.00 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 0.70 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 0.75 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 1.35 s) B started applying strong throttle.
- (unaligned, B local time 1.40 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 1.40 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 2.50 s) B stopped applying strong throttle.
- (unaligned, B local time 4.25 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 4.35 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 4.75 s) B started braking.
- (unaligned, B local time 5.15 s) B's collision sensor recorded a contact (peak impulse 6074 N*s).
- (unaligned, B local time 5.20 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.20 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 5.20 s) B started braking hard.
- (unaligned, B local time 5.60 s) B stopped moving.
- (unaligned, B local time 5.60 s) B came to a stop.
- (unaligned, B local time 12.55 s) B's radar started tracking unidentified object B:track_002.
- (unaligned, B local time 13.55 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 14.05 s) B's radar lost unidentified object B:track_001.
