# Global graph - S15/run_0_single_impact

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 3.00 s before the matched collision<br>not at the contact: minimum range 54.18 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 7.07 m/s (> 1.50) |
| A:track_002 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>at the contact: minimum range 1.67 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 1.8 s |
| B:track_001 | A | ASSOCIATED | 0.90 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>at the contact: minimum range 0.41 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.68 m/s over 1.8 s |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.00 | TRACK_APPEARED | A | A:track_001 | A:e02 @ 0.80 |  |
| g04 | -3.00 | CLOSING_START | A | A:track_001 | A:e03 @ 0.80 | active_at_first_observation=True |
| g05 | -2.60 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.20 |  |
| g06 | -2.00 | STRONG_THROTTLE_END | B | - | B:e03 @ 1.80 |  |
| g07 | -2.00 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e04 @ 1.80 | relevant_to_ego_path=False |
| g08 | -1.85 | TRACK_APPEARED | B | A | B:e05 @ 1.95 |  |
| g09 | -1.85 | CLOSING_START | B | A | B:e06 @ 1.95 | active_at_first_observation=True |
| g10 | -1.80 | TRACK_APPEARED | A | B | A:e04 @ 2.00 |  |
| g11 | -1.80 | CLOSING_START | A | B | A:e05 @ 2.00 | active_at_first_observation=True |
| g12 | -1.80 | CRITICAL_TTC_START | A | B | A:e06 @ 2.00 | active_at_first_observation=True |
| g13 | -1.80 | CRITICAL_TTC_START | B | A | B:e07 @ 2.00 |  |
| g14 | -1.70 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e08 @ 2.10 |  |
| g15 | -0.85 | BRAKE_START | B | - | B:e09 @ 2.95 |  |
| g16 | -0.30 | BRAKE_END | B | - | B:e10 @ 3.50 |  |
| g17 | -0.20 | EGO_PATH_ENTRY | B | A | B:e11 @ 3.60 |  |
| g18 | -0.05 | TRACK_LOST | A | B | A:e07 @ 3.75 |  |
| g19 | 0.00 | COLLISION | - | A, B | A:e08 @ 3.80, B:e12 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 9797.50, B 9797.50 |
| g20 | 0.00 | STRONG_THROTTLE_START | A | - | A:e09 @ 3.80 |  |
| g21 | 0.00 | STRONG_THROTTLE_START | B | - | B:e13 @ 3.80 |  |
| g22 | 0.00 | EGO_PATH_ENTRY | A | A:track_001 | A:e10 @ 3.80 |  |
| g23 | 0.05 | EGO_PATH_EXIT | A | A:track_001 | A:e11 @ 3.85 |  |
| g24 | 0.05 | STRONG_THROTTLE_END | A | - | A:e12 @ 3.85 |  |
| g25 | 0.05 | STRONG_THROTTLE_END | B | - | B:e14 @ 3.85 |  |
| g26 | 0.05 | BRAKE_START | B | - | B:e15 @ 3.85 |  |
| g27 | 0.05 | HARD_BRAKE_START | B | - | B:e16 @ 3.85 |  |
| g28 | 0.20 | MOVING_END | B | - | B:e17 @ 4.00 |  |
| g29 | 0.20 | STOP_START | B | - | B:e18 @ 4.00 |  |
| g30 | 0.25 | CRITICAL_TTC_END | B | A | B:e19 @ 4.05 |  |
| g31 | 0.25 | CLOSING_END | B | A | B:e20 @ 4.05 |  |
| g32 | 0.30 | EGO_PATH_ENTRY | A | A:track_001 | A:e13 @ 4.10 |  |
| g33 | 0.50 | EGO_PATH_EXIT | A | A:track_001 | A:e14 @ 4.30 |  |
| g34 | 0.80 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e15 @ 4.60 | relevant_to_ego_path=False |
| g35 | 0.80 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e16 @ 4.60 |  |
| g36 | 1.05 | EGO_PATH_EXIT | B | A | B:e21 @ 4.85 |  |
| g37 | 1.70 | TRACK_LOST | B | A | B:e22 @ 5.50 |  |
| g38 | 6.75 | STOP_SIGN_DETECTED_START | A | A:sign-1 | A:e17 @ 10.55 | relevant_to_ego_path=False |
| g39 | 7.75 | MOVING_END | A | - | A:e18 @ 11.55 |  |
| g40 | 7.75 | STOP_START | A | - | A:e19 @ 11.55 |  |
| g41 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g42 | - | TRACK_APPEARED | C | C:track_001 | C:e02 @ 0.80 |  |
| g43 | - | TRACK_APPEARED | C | C:track_002 | C:e03 @ 0.80 |  |
| g44 | - | CLOSING_START | C | C:track_001 | C:e04 @ 0.80 | active_at_first_observation=True |
| g45 | - | CLOSING_START | C | C:track_002 | C:e05 @ 0.80 | active_at_first_observation=True |
| g46 | - | STOP_SIGN_DETECTED_START | C | C:sign-0 | C:e06 @ 2.80 | relevant_to_ego_path=False |
| g47 | - | STOP_SIGN_DETECTED_END | C | C:sign-0 | C:e07 @ 2.80 |  |
| g48 | - | CLOSING_END | C | C:track_002 | C:e08 @ 2.95 |  |
| g49 | - | CLOSING_START | C | C:track_002 | C:e09 @ 3.85 |  |
| g50 | - | EGO_PATH_ENTRY | C | C:track_001 | C:e10 @ 5.00 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g08 --PRECEDES--> g13
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g10 --PRECEDES--> g14
    g11 --PRECEDES--> g14
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g19 --PRECEDES--> g25
    g19 --PRECEDES--> g26
    g19 --PRECEDES--> g27
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g32
    g32 --PRECEDES--> g33
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g03 --SAME_TRACK--> g04
    g10 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g12
    g10 --SAME_TRACK--> g18
    g03 --SAME_TRACK--> g22
    g03 --SAME_TRACK--> g23
    g03 --SAME_TRACK--> g32
    g03 --SAME_TRACK--> g33
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g17
    g08 --SAME_TRACK--> g30
    g08 --SAME_TRACK--> g31
    g08 --SAME_TRACK--> g36
    g08 --SAME_TRACK--> g37
    g42 --SAME_TRACK--> g44
    g43 --SAME_TRACK--> g45
    g43 --SAME_TRACK--> g48
    g43 --SAME_TRACK--> g49
    g42 --SAME_TRACK--> g50
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B) |
| -3.00 | TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.60 | STRONG_THROTTLE_START(B) |
| -2.00 | STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -1.85 | TRACK_APPEARED(B,A); CLOSING_START(B,A) |
| -1.80 | TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -1.70 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -0.85 | BRAKE_START(B) |
| -0.30 | BRAKE_END(B) |
| -0.20 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); EGO_PATH_ENTRY(A,A:track_001) |
| +0.05 | EGO_PATH_EXIT(A,A:track_001); STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.25 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.30 | EGO_PATH_ENTRY(A,A:track_001) |
| +0.50 | EGO_PATH_EXIT(A,A:track_001) |
| +0.80 | STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0) |
| +1.05 | EGO_PATH_EXIT(B,A) |
| +1.70 | TRACK_LOST(B,A) |
| +6.75 | STOP_SIGN_DETECTED_START(A,A:sign-1) |
| +7.75 | MOVING_END(A); STOP_START(A) |

## Plain-language reading

- 3.80 s before the matched collision, A started moving (already the case when first observed).
- 3.80 s before the matched collision, B started moving (already the case when first observed).
- 3.00 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 3.00 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.60 s before the matched collision, B started applying strong throttle.
- 2.00 s before the matched collision, B stopped applying strong throttle.
- 2.00 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the matched collision, B's radar started tracking A.
- 1.85 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.80 s before the matched collision, B's time-to-contact with A became critical.
- 1.70 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 0.85 s before the matched collision, B started braking.
- 0.30 s before the matched collision, B released the brake.
- 0.20 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.05 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, B started braking hard.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.25 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the matched collision, B observed A stop closing in.
- 0.30 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.50 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.80 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.80 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 1.05 s after the matched collision, B observed A leave its forward path corridor.
- 1.70 s after the matched collision, B's radar lost A.
- 6.75 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 7.75 s after the matched collision, A stopped moving.
- 7.75 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.80 s) C's radar started tracking unidentified object C:track_001.
- (unaligned, C local time 0.80 s) C's radar started tracking unidentified object C:track_002.
- (unaligned, C local time 0.80 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.80 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.80 s) C's camera established a STOP sign detection (unidentified object C:sign-0) (the detector judged it not relevant to its path).
- (unaligned, C local time 2.80 s) C's camera stopped detecting STOP sign unidentified object C:sign-0.
- (unaligned, C local time 2.95 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 3.85 s) C observed unidentified object C:track_002 start closing in.
- (unaligned, C local time 5.00 s) C observed unidentified object C:track_001 enter its forward path corridor.
