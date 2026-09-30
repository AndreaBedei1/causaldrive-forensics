# Global graph - S15/run_0_deflected_into_c

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e17 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1637.56 vs 1637.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 3.80 s before the matched collision<br>not at the contact: minimum range 11.09 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 3.70 m/s (> 1.50) |
| A:track_002 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>at the contact: minimum range 1.67 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 1.8 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.35 s before the matched collision<br>not at the contact: last seen 1.00 s before the matched collision (window 0.50 s)<br>track speed disagrees with A's own speed: RMSE 5.84 m/s (> 1.50) |
| B:track_002 | A | ASSOCIATED | 0.90 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>at the contact: minimum range 0.40 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.68 m/s over 1.8 s |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.80 | TRACK_APPEARED | A | A:track_001 | A:e02 @ 0.00 |  |
| g04 | -3.80 | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -2.60 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.20 |  |
| g06 | -2.35 | TRACK_APPEARED | B | B:track_001 | B:e03 @ 1.45 |  |
| g07 | -2.35 | CLOSING_START | B | B:track_001 | B:e04 @ 1.45 | active_at_first_observation=True |
| g08 | -2.00 | STRONG_THROTTLE_END | B | - | B:e05 @ 1.80 |  |
| g09 | -2.00 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e06 @ 1.80 | relevant_to_ego_path=False |
| g10 | -1.85 | TRACK_APPEARED | B | A | B:e07 @ 1.95 |  |
| g11 | -1.85 | CLOSING_START | B | A | B:e08 @ 1.95 | active_at_first_observation=True |
| g12 | -1.80 | TRACK_APPEARED | A | B | A:e04 @ 2.00 |  |
| g13 | -1.80 | CLOSING_START | A | B | A:e05 @ 2.00 | active_at_first_observation=True |
| g14 | -1.80 | CRITICAL_TTC_START | A | B | A:e06 @ 2.00 | active_at_first_observation=True |
| g15 | -1.80 | CRITICAL_TTC_START | B | A | B:e09 @ 2.00 |  |
| g16 | -1.70 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e10 @ 2.10 |  |
| g17 | -1.45 | CRITICAL_TTC_START | B | B:track_001 | B:e11 @ 2.35 |  |
| g18 | -1.30 | CRITICAL_TTC_START | A | A:track_001 | A:e07 @ 2.50 |  |
| g19 | -1.05 | CRITICAL_TTC_END | B | B:track_001 | B:e12 @ 2.75 |  |
| g20 | -1.00 | TRACK_LOST | B | B:track_001 | B:e13 @ 2.80 |  |
| g21 | -0.85 | BRAKE_START | B | - | B:e14 @ 2.95 |  |
| g22 | -0.30 | BRAKE_END | B | - | B:e15 @ 3.50 |  |
| g23 | -0.20 | EGO_PATH_ENTRY | B | A | B:e16 @ 3.60 |  |
| g24 | -0.05 | TRACK_LOST | A | B | A:e08 @ 3.75 |  |
| g25 | 0.00 | COLLISION | - | A, B | A:e09 @ 3.80, B:e17 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 9797.50, B 9797.50 |
| g26 | 0.00 | STRONG_THROTTLE_START | A | - | A:e10 @ 3.80 |  |
| g27 | 0.00 | STRONG_THROTTLE_START | B | - | B:e18 @ 3.80 |  |
| g28 | 0.05 | STRONG_THROTTLE_END | A | - | A:e11 @ 3.85 |  |
| g29 | 0.05 | STRONG_THROTTLE_END | B | - | B:e19 @ 3.85 |  |
| g30 | 0.05 | BRAKE_START | B | - | B:e20 @ 3.85 |  |
| g31 | 0.05 | HARD_BRAKE_START | B | - | B:e21 @ 3.85 |  |
| g32 | 0.20 | MOVING_END | B | - | B:e22 @ 4.00 |  |
| g33 | 0.20 | STOP_START | B | - | B:e23 @ 4.00 |  |
| g34 | 0.25 | CRITICAL_TTC_END | B | A | B:e24 @ 4.05 |  |
| g35 | 0.25 | CLOSING_END | B | A | B:e25 @ 4.05 |  |
| g36 | 0.75 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e12 @ 4.55 | relevant_to_ego_path=False |
| g37 | 0.75 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e13 @ 4.55 |  |
| g38 | 0.80 | EGO_PATH_ENTRY | A | A:track_001 | A:e14 @ 4.60 |  |
| g39 | 0.95 | COLLISION | A | - | A:e15 @ 4.75 | peak_impulse=1637.56 |
| g40 | 1.15 | CRITICAL_TTC_END | A | A:track_001 | A:e16 @ 4.95 |  |
| g41 | 1.15 | CLOSING_END | A | A:track_001 | A:e17 @ 4.95 |  |
| g42 | 1.25 | MOVING_END | A | - | A:e18 @ 5.05 |  |
| g43 | 1.25 | STOP_START | A | - | A:e19 @ 5.05 |  |
| g44 | 1.50 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e20 @ 5.30 | relevant_to_ego_path=False |
| g45 | 4.00 | STOP_SIGN_DETECTED_END | A | A:sign-2 | A:e21 @ 7.80 |  |
| g46 | 4.90 | STOP_SIGN_DETECTED_START | A | A:sign-3 | A:e22 @ 8.70 | relevant_to_ego_path=False |
| g47 | 4.90 | STOP_SIGN_DETECTED_END | A | A:sign-3 | A:e23 @ 8.70 |  |
| g48 | 5.95 | STOP_SIGN_DETECTED_START | A | A:sign-4 | A:e24 @ 9.75 | relevant_to_ego_path=False |
| g49 | 6.10 | STOP_SIGN_DETECTED_END | A | A:sign-4 | A:e25 @ 9.90 |  |
| g50 | 7.10 | STOP_SIGN_DETECTED_START | A | A:sign-5 | A:e26 @ 10.90 | relevant_to_ego_path=False |
| g51 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g52 | - | TRACK_APPEARED | C | C:track_001 | C:e02 @ 0.00 |  |
| g53 | - | TRACK_APPEARED | C | C:track_002 | C:e03 @ 0.00 |  |
| g54 | - | CLOSING_START | C | C:track_001 | C:e04 @ 0.00 | active_at_first_observation=True |
| g55 | - | CLOSING_START | C | C:track_002 | C:e05 @ 0.00 | active_at_first_observation=True |
| g56 | - | STRONG_THROTTLE_START | C | - | C:e06 @ 1.65 |  |
| g57 | - | STRONG_THROTTLE_END | C | - | C:e07 @ 2.10 |  |
| g58 | - | CRITICAL_TTC_START | C | C:track_002 | C:e08 @ 2.25 |  |
| g59 | - | CRITICAL_TTC_START | C | C:track_001 | C:e09 @ 2.50 |  |
| g60 | - | CRITICAL_TTC_END | C | C:track_002 | C:e10 @ 3.15 |  |
| g61 | - | TRACK_LOST | C | C:track_002 | C:e11 @ 4.45 |  |
| g62 | - | COLLISION | C | - | C:e12 @ 4.75 | peak_impulse=1637.56 |
| g63 | - | STRONG_THROTTLE_START | C | - | C:e13 @ 4.75 |  |
| g64 | - | STRONG_THROTTLE_END | C | - | C:e14 @ 4.80 |  |
| g65 | - | BRAKE_START | C | - | C:e15 @ 4.80 |  |
| g66 | - | HARD_BRAKE_START | C | - | C:e16 @ 4.80 |  |
| g67 | - | EGO_PATH_ENTRY | C | C:track_001 | C:e17 @ 5.00 |  |
| g68 | - | CRITICAL_TTC_END | C | C:track_001 | C:e18 @ 5.05 |  |
| g69 | - | CLOSING_END | C | C:track_001 | C:e19 @ 5.05 |  |
| g70 | - | MOVING_END | C | - | C:e20 @ 5.05 |  |
| g71 | - | STOP_START | C | - | C:e21 @ 5.05 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
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
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g38
    g38 --PRECEDES--> g39
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g44
    g44 --PRECEDES--> g45
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g47 --PRECEDES--> g48
    g48 --PRECEDES--> g49
    g49 --PRECEDES--> g50
    g03 --SAME_TRACK--> g04
    g12 --SAME_TRACK--> g13
    g12 --SAME_TRACK--> g14
    g03 --SAME_TRACK--> g18
    g12 --SAME_TRACK--> g24
    g03 --SAME_TRACK--> g38
    g03 --SAME_TRACK--> g40
    g03 --SAME_TRACK--> g41
    g06 --SAME_TRACK--> g07
    g10 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g15
    g06 --SAME_TRACK--> g17
    g06 --SAME_TRACK--> g19
    g06 --SAME_TRACK--> g20
    g10 --SAME_TRACK--> g23
    g10 --SAME_TRACK--> g34
    g10 --SAME_TRACK--> g35
    g52 --SAME_TRACK--> g54
    g53 --SAME_TRACK--> g55
    g53 --SAME_TRACK--> g58
    g52 --SAME_TRACK--> g59
    g53 --SAME_TRACK--> g60
    g53 --SAME_TRACK--> g61
    g52 --SAME_TRACK--> g67
    g52 --SAME_TRACK--> g68
    g52 --SAME_TRACK--> g69
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001) |
| -2.60 | STRONG_THROTTLE_START(B) |
| -2.35 | TRACK_APPEARED(B,B:track_001); CLOSING_START(B,B:track_001) |
| -2.00 | STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -1.85 | TRACK_APPEARED(B,A); CLOSING_START(B,A) |
| -1.80 | TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -1.70 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -1.45 | CRITICAL_TTC_START(B,B:track_001) |
| -1.30 | CRITICAL_TTC_START(A,A:track_001) |
| -1.05 | CRITICAL_TTC_END(B,B:track_001) |
| -1.00 | TRACK_LOST(B,B:track_001) |
| -0.85 | BRAKE_START(B) |
| -0.30 | BRAKE_END(B) |
| -0.20 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B) |
| +0.05 | STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.25 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.75 | STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0) |
| +0.80 | EGO_PATH_ENTRY(A,A:track_001) |
| +0.95 | COLLISION(A) |
| +1.15 | CRITICAL_TTC_END(A,A:track_001); CLOSING_END(A,A:track_001) |
| +1.25 | MOVING_END(A); STOP_START(A) |
| +1.50 | STOP_SIGN_DETECTED_START(A,A:sign-2) |
| +4.00 | STOP_SIGN_DETECTED_END(A,A:sign-2) |
| +4.90 | STOP_SIGN_DETECTED_START(A,A:sign-3); STOP_SIGN_DETECTED_END(A,A:sign-3) |
| +5.95 | STOP_SIGN_DETECTED_START(A,A:sign-4) |
| +6.10 | STOP_SIGN_DETECTED_END(A,A:sign-4) |
| +7.10 | STOP_SIGN_DETECTED_START(A,A:sign-5) |

## Plain-language reading

- 3.80 s before the matched collision, A started moving (already the case when first observed).
- 3.80 s before the matched collision, B started moving (already the case when first observed).
- 3.80 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 3.80 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.60 s before the matched collision, B started applying strong throttle.
- 2.35 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 2.35 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.00 s before the matched collision, B stopped applying strong throttle.
- 2.00 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the matched collision, B's radar started tracking A.
- 1.85 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.80 s before the matched collision, B's time-to-contact with A became critical.
- 1.70 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.45 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 1.30 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.05 s before the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.00 s before the matched collision, B's radar lost unidentified object B:track_001.
- 0.85 s before the matched collision, B started braking.
- 0.30 s before the matched collision, B released the brake.
- 0.20 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, B started braking hard.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.25 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the matched collision, B observed A stop closing in.
- 0.75 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.75 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 0.80 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.95 s after the matched collision, A's collision sensor recorded a contact (peak impulse 1638 N*s).
- 1.15 s after the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 1.15 s after the matched collision, A observed unidentified object A:track_001 stop closing in.
- 1.25 s after the matched collision, A stopped moving.
- 1.25 s after the matched collision, A came to a stop.
- 1.50 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path).
- 4.00 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 4.90 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-3) (the detector judged it not relevant to its path).
- 4.90 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-3.
- 5.95 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-4) (the detector judged it not relevant to its path).
- 6.10 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-4.
- 7.10 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-5) (the detector judged it not relevant to its path).
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001.
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_002.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 1.65 s) C started applying strong throttle.
- (unaligned, C local time 2.10 s) C stopped applying strong throttle.
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 2.50 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 3.15 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.45 s) C's radar lost unidentified object C:track_002.
- (unaligned, C local time 4.75 s) C's collision sensor recorded a contact (peak impulse 1638 N*s).
- (unaligned, C local time 4.75 s) C started applying strong throttle.
- (unaligned, C local time 4.80 s) C stopped applying strong throttle.
- (unaligned, C local time 4.80 s) C started braking.
- (unaligned, C local time 4.80 s) C started braking hard.
- (unaligned, C local time 5.00 s) C observed unidentified object C:track_001 enter its forward path corridor.
- (unaligned, C local time 5.05 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 5.05 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 5.05 s) C stopped moving.
- (unaligned, C local time 5.05 s) C came to a stop.
