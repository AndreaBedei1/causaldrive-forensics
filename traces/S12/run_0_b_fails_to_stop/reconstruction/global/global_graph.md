# Global graph - S12/run_0_b_fails_to_stop

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e19 | 9.70 | -9.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 9.70 | -9.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 7339.57 vs 7339.57 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.90 | A and B both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 2.95 s before the matched collision<br>at the contact: minimum range 1.44 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.67 m/s over 2.9 s |
| B:track_001 | A | ASSOCIATED | 0.88 | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 1.55 s before the matched collision<br>at the contact: minimum range 1.11 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.75 m/s over 1.5 s |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 19.01 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -9.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -9.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -9.05 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.65 | relevant_to_ego_path=True |
| g04 | -8.45 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g05 | -7.85 | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g06 | -7.75 | BRAKE_START | B | - | B:e04 @ 1.95 |  |
| g07 | -7.75 | HARD_BRAKE_START | B | - | B:e05 @ 1.95 |  |
| g08 | -7.45 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.25 |  |
| g09 | -7.40 | HARD_BRAKE_END | B | - | B:e06 @ 2.30 |  |
| g10 | -7.05 | BRAKE_END | B | - | B:e07 @ 2.65 |  |
| g11 | -7.05 | BRAKE_START | A | - | A:e04 @ 2.65 |  |
| g12 | -7.05 | HARD_BRAKE_START | A | - | A:e05 @ 2.65 |  |
| g13 | -6.45 | STRONG_THROTTLE_START | B | - | B:e08 @ 3.25 |  |
| g14 | -6.40 | STRONG_THROTTLE_END | B | - | B:e09 @ 3.30 |  |
| g15 | -6.30 | MOVING_END | A | - | A:e06 @ 3.40 |  |
| g16 | -6.30 | STOP_START | A | - | A:e07 @ 3.40 |  |
| g17 | -6.20 | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e10 @ 3.50 | relevant_to_ego_path=False |
| g18 | -4.40 | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e11 @ 5.30 |  |
| g19 | -2.95 | TRACK_APPEARED | A | B | A:e08 @ 6.75 |  |
| g20 | -2.95 | CLOSING_START | A | B | A:e09 @ 6.75 | active_at_first_observation=True |
| g21 | -1.95 | HARD_BRAKE_END | A | - | A:e10 @ 7.75 |  |
| g22 | -1.95 | BRAKE_END | A | - | A:e11 @ 7.75 |  |
| g23 | -1.95 | STRONG_THROTTLE_START | A | - | A:e12 @ 7.75 |  |
| g24 | -1.60 | STOP_END | A | - | A:e13 @ 8.10 |  |
| g25 | -1.60 | MOVING_START | A | - | A:e14 @ 8.10 |  |
| g26 | -1.55 | TRACK_APPEARED | B | A | B:e12 @ 8.15 |  |
| g27 | -1.55 | CLOSING_START | B | A | B:e13 @ 8.15 | active_at_first_observation=True |
| g28 | -1.20 | CRITICAL_TTC_START | A | B | A:e15 @ 8.50 |  |
| g29 | -1.20 | CRITICAL_TTC_START | B | A | B:e14 @ 8.50 |  |
| g30 | -0.60 | STRONG_THROTTLE_END | A | - | A:e16 @ 9.10 |  |
| g31 | -0.10 | EGO_PATH_ENTRY | B | A | B:e15 @ 9.60 |  |
| g32 | -0.05 | EGO_PATH_ENTRY | A | B | A:e17 @ 9.65 |  |
| g33 | -0.05 | TRACK_LOST | A | B | A:e18 @ 9.65 |  |
| g34 | 0.00 | COLLISION | - | A, B | A:e19 @ 9.70, B:e16 @ 9.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 7339.57, B 7339.57 |
| g35 | 0.00 | STRONG_THROTTLE_START | A | - | A:e20 @ 9.70 |  |
| g36 | 0.00 | STRONG_THROTTLE_START | B | - | B:e17 @ 9.70 |  |
| g37 | 0.00 | TRACK_APPEARED | B | B:track_002 | B:e18 @ 9.70 |  |
| g38 | 0.00 | CLOSING_START | B | B:track_002 | B:e19 @ 9.70 | active_at_first_observation=True |
| g39 | 0.05 | STRONG_THROTTLE_END | A | - | A:e21 @ 9.75 |  |
| g40 | 0.05 | STRONG_THROTTLE_END | B | - | B:e20 @ 9.75 |  |
| g41 | 0.05 | BRAKE_START | A | - | A:e22 @ 9.75 |  |
| g42 | 0.05 | BRAKE_START | B | - | B:e21 @ 9.75 |  |
| g43 | 0.05 | HARD_BRAKE_START | A | - | A:e23 @ 9.75 |  |
| g44 | 0.05 | HARD_BRAKE_START | B | - | B:e22 @ 9.75 |  |
| g45 | 0.05 | TRACK_APPEARED | B | B:track_003 | B:e23 @ 9.75 |  |
| g46 | 0.05 | CLOSING_START | B | B:track_003 | B:e24 @ 9.75 | active_at_first_observation=True |
| g47 | 0.35 | MOVING_END | B | - | B:e25 @ 10.05 |  |
| g48 | 0.35 | STOP_START | B | - | B:e26 @ 10.05 |  |
| g49 | 0.40 | CLOSING_END | B | B:track_002 | B:e27 @ 10.10 |  |
| g50 | 0.40 | CLOSING_END | B | B:track_003 | B:e28 @ 10.10 |  |
| g51 | 0.45 | CRITICAL_TTC_END | B | A | B:e29 @ 10.15 |  |
| g52 | 0.45 | CLOSING_END | B | A | B:e30 @ 10.15 |  |
| g53 | 0.50 | MOVING_END | A | - | A:e24 @ 10.20 |  |
| g54 | 0.50 | STOP_START | A | - | A:e25 @ 10.20 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g30
    g30 --PRECEDES--> g31
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g32 --PRECEDES--> g38
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g34 --PRECEDES--> g41
    g34 --PRECEDES--> g42
    g34 --PRECEDES--> g43
    g34 --PRECEDES--> g44
    g34 --PRECEDES--> g45
    g34 --PRECEDES--> g46
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g35 --PRECEDES--> g43
    g35 --PRECEDES--> g44
    g35 --PRECEDES--> g45
    g35 --PRECEDES--> g46
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g36 --PRECEDES--> g43
    g36 --PRECEDES--> g44
    g36 --PRECEDES--> g45
    g36 --PRECEDES--> g46
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g37 --PRECEDES--> g44
    g37 --PRECEDES--> g45
    g37 --PRECEDES--> g46
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g38 --PRECEDES--> g44
    g38 --PRECEDES--> g45
    g38 --PRECEDES--> g46
    g39 --PRECEDES--> g47
    g39 --PRECEDES--> g48
    g40 --PRECEDES--> g47
    g40 --PRECEDES--> g48
    g41 --PRECEDES--> g47
    g41 --PRECEDES--> g48
    g42 --PRECEDES--> g47
    g42 --PRECEDES--> g48
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g46 --PRECEDES--> g47
    g46 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g48 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g52 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g19 --SAME_TRACK--> g20
    g19 --SAME_TRACK--> g28
    g19 --SAME_TRACK--> g32
    g19 --SAME_TRACK--> g33
    g26 --SAME_TRACK--> g27
    g26 --SAME_TRACK--> g29
    g26 --SAME_TRACK--> g31
    g37 --SAME_TRACK--> g38
    g45 --SAME_TRACK--> g46
    g37 --SAME_TRACK--> g49
    g45 --SAME_TRACK--> g50
    g26 --SAME_TRACK--> g51
    g26 --SAME_TRACK--> g52
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -9.70 | MOVING_START(A); MOVING_START(B) |
| -9.05 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -8.45 | STRONG_THROTTLE_START(B) |
| -7.85 | STRONG_THROTTLE_END(B) |
| -7.75 | BRAKE_START(B); HARD_BRAKE_START(B) |
| -7.45 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -7.40 | HARD_BRAKE_END(B) |
| -7.05 | BRAKE_END(B); BRAKE_START(A); HARD_BRAKE_START(A) |
| -6.45 | STRONG_THROTTLE_START(B) |
| -6.40 | STRONG_THROTTLE_END(B) |
| -6.30 | MOVING_END(A); STOP_START(A) |
| -6.20 | STOP_SIGN_DETECTED_START(B,B:sign-1) |
| -4.40 | STOP_SIGN_DETECTED_END(B,B:sign-1) |
| -2.95 | TRACK_APPEARED(A,B); CLOSING_START(A,B) |
| -1.95 | HARD_BRAKE_END(A); BRAKE_END(A); STRONG_THROTTLE_START(A) |
| -1.60 | STOP_END(A); MOVING_START(A) |
| -1.55 | TRACK_APPEARED(B,A); CLOSING_START(B,A) |
| -1.20 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -0.60 | STRONG_THROTTLE_END(A) |
| -0.10 | EGO_PATH_ENTRY(B,A) |
| -0.05 | EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B) |
| +0.00 | COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_002) |
| +0.05 | STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_003); CLOSING_START(B,B:track_003) |
| +0.35 | MOVING_END(B); STOP_START(B) |
| +0.40 | CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003) |
| +0.45 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.50 | MOVING_END(A); STOP_START(A) |

## Plain-language reading

- 9.70 s before the matched collision, A started moving (already the case when first observed).
- 9.70 s before the matched collision, B started moving (already the case when first observed).
- 9.05 s before the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 8.45 s before the matched collision, B started applying strong throttle.
- 7.85 s before the matched collision, B stopped applying strong throttle.
- 7.75 s before the matched collision, B started braking.
- 7.75 s before the matched collision, B started braking hard.
- 7.45 s before the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.40 s before the matched collision, B stopped braking hard.
- 7.05 s before the matched collision, B released the brake.
- 7.05 s before the matched collision, A started braking.
- 7.05 s before the matched collision, A started braking hard.
- 6.45 s before the matched collision, B started applying strong throttle.
- 6.40 s before the matched collision, B stopped applying strong throttle.
- 6.30 s before the matched collision, A stopped moving.
- 6.30 s before the matched collision, A came to a stop.
- 6.20 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- 4.40 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 2.95 s before the matched collision, A's radar started tracking B.
- 2.95 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.95 s before the matched collision, A stopped braking hard.
- 1.95 s before the matched collision, A released the brake.
- 1.95 s before the matched collision, A started applying strong throttle.
- 1.60 s before the matched collision, A left its stop.
- 1.60 s before the matched collision, A started moving.
- 1.55 s before the matched collision, B's radar started tracking A.
- 1.55 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.20 s before the matched collision, A's time-to-contact with B became critical.
- 1.20 s before the matched collision, B's time-to-contact with A became critical.
- 0.60 s before the matched collision, A stopped applying strong throttle.
- 0.10 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A observed B enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 7340, B: 7340 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, B's radar started tracking unidentified object B:track_002.
- At the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_003.
- 0.05 s after the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.35 s after the matched collision, B stopped moving.
- 0.35 s after the matched collision, B came to a stop.
- 0.40 s after the matched collision, B observed unidentified object B:track_002 stop closing in.
- 0.40 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 0.45 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.45 s after the matched collision, B observed A stop closing in.
- 0.50 s after the matched collision, A stopped moving.
- 0.50 s after the matched collision, A came to a stop.
