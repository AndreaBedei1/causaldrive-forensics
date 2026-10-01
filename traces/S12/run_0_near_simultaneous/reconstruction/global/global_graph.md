# Global graph - S12/run_0_near_simultaneous

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |
| A:track_004 | anonymous_track | seen only by A; candidate: B |
| A:track_005 | anonymous_track | seen only by A; candidate: B |
| A:track_006 | anonymous_track | seen only by A; candidate: B |
| A:track_007 | anonymous_track | seen only by A; candidate: B |
| A:track_008 | anonymous_track | seen only by A; candidate: B |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e21 | 9.50 | -9.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e25 | 9.50 | -9.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4032.49 vs 4032.49 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 7.00 s before the matched collision<br>not at the contact: last seen 6.70 s before the matched collision (window 0.50 s)<br>speed not comparable with B's own speed before the collision |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.10 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 89.51 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.10 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 87.16 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 11.46 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| A:track_007 | A:track_007 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| A:track_008 | A:track_008 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| B:track_001 | A | ASSOCIATED | 0.79 | B and A both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.95 s before the matched collision<br>at the contact: minimum range 0.70 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 1.04 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -9.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -9.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -8.85 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.65 | relevant_to_ego_path=True |
| g04 | -8.25 | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g05 | -7.65 | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g06 | -7.40 | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e04 @ 2.10 | relevant_to_ego_path=True |
| g07 | -7.25 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.25 |  |
| g08 | -7.00 | TRACK_APPEARED | A | A:track_001 | A:e04 @ 2.50 |  |
| g09 | -7.00 | CLOSING_START | A | A:track_001 | A:e05 @ 2.50 | active_at_first_observation=True |
| g10 | -6.95 | TRACK_APPEARED | B | A | B:e05 @ 2.55 |  |
| g11 | -6.95 | CLOSING_START | B | A | B:e06 @ 2.55 | active_at_first_observation=True |
| g12 | -6.90 | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e07 @ 2.60 |  |
| g13 | -6.85 | BRAKE_START | A | - | A:e06 @ 2.65 |  |
| g14 | -6.85 | HARD_BRAKE_START | A | - | A:e07 @ 2.65 |  |
| g15 | -6.75 | BRAKE_START | B | - | B:e08 @ 2.75 |  |
| g16 | -6.75 | HARD_BRAKE_START | B | - | B:e09 @ 2.75 |  |
| g17 | -6.70 | TRACK_LOST | A | A:track_001 | A:e08 @ 2.80 |  |
| g18 | -6.10 | MOVING_END | A | - | A:e09 @ 3.40 |  |
| g19 | -6.10 | STOP_START | A | - | A:e10 @ 3.40 |  |
| g20 | -6.00 | CLOSING_END | B | A | B:e10 @ 3.50 |  |
| g21 | -6.00 | MOVING_END | B | - | B:e11 @ 3.50 |  |
| g22 | -6.00 | STOP_START | B | - | B:e12 @ 3.50 |  |
| g23 | -2.55 | HARD_BRAKE_END | A | - | A:e11 @ 6.95 |  |
| g24 | -2.55 | HARD_BRAKE_END | B | - | B:e13 @ 6.95 |  |
| g25 | -2.55 | BRAKE_END | A | - | A:e12 @ 6.95 |  |
| g26 | -2.55 | BRAKE_END | B | - | B:e14 @ 6.95 |  |
| g27 | -2.55 | STRONG_THROTTLE_START | A | - | A:e13 @ 6.95 |  |
| g28 | -2.55 | STRONG_THROTTLE_START | B | - | B:e15 @ 6.95 |  |
| g29 | -2.20 | STOP_END | A | - | A:e14 @ 7.30 |  |
| g30 | -2.20 | MOVING_START | A | - | A:e15 @ 7.30 |  |
| g31 | -2.20 | CLOSING_START | B | A | B:e16 @ 7.30 |  |
| g32 | -2.15 | STOP_END | B | - | B:e17 @ 7.35 |  |
| g33 | -2.15 | MOVING_START | B | - | B:e18 @ 7.35 |  |
| g34 | -1.25 | CRITICAL_TTC_START | B | A | B:e19 @ 8.25 |  |
| g35 | -1.20 | STRONG_THROTTLE_END | A | - | A:e16 @ 8.30 |  |
| g36 | -0.85 | STRONG_THROTTLE_END | B | - | B:e20 @ 8.65 |  |
| g37 | -0.55 | EGO_PATH_ENTRY | B | A | B:e21 @ 8.95 |  |
| g38 | -0.55 | PREDICTED_PATH_CONFLICT_START | B | A | B:e22 @ 8.95 |  |
| g39 | -0.10 | TRACK_APPEARED | A | A:track_002 | A:e17 @ 9.40 |  |
| g40 | -0.10 | TRACK_APPEARED | A | A:track_003 | A:e18 @ 9.40 |  |
| g41 | -0.10 | CLOSING_START | A | A:track_002 | A:e19 @ 9.40 | active_at_first_observation=True |
| g42 | -0.10 | CLOSING_START | A | A:track_003 | A:e20 @ 9.40 | active_at_first_observation=True |
| g43 | -0.05 | CRITICAL_TTC_END | B | A | B:e23 @ 9.45 |  |
| g44 | -0.05 | CLOSING_END | B | A | B:e24 @ 9.45 |  |
| g45 | 0.00 | COLLISION | - | A, B | A:e21 @ 9.50, B:e25 @ 9.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 4032.49, B 4032.49 |
| g46 | 0.00 | EGO_PATH_EXIT | B | A | B:e26 @ 9.50 |  |
| g47 | 0.00 | STRONG_THROTTLE_START | A | - | A:e22 @ 9.50 |  |
| g48 | 0.00 | STRONG_THROTTLE_START | B | - | B:e27 @ 9.50 |  |
| g49 | 0.00 | TRACK_APPEARED | A | A:track_004 | A:e23 @ 9.50 |  |
| g50 | 0.05 | STRONG_THROTTLE_END | A | - | A:e24 @ 9.55 |  |
| g51 | 0.05 | STRONG_THROTTLE_END | B | - | B:e28 @ 9.55 |  |
| g52 | 0.05 | BRAKE_START | A | - | A:e25 @ 9.55 |  |
| g53 | 0.05 | BRAKE_START | B | - | B:e29 @ 9.55 |  |
| g54 | 0.05 | HARD_BRAKE_START | A | - | A:e26 @ 9.55 |  |
| g55 | 0.05 | HARD_BRAKE_START | B | - | B:e30 @ 9.55 |  |
| g56 | 0.05 | TRACK_APPEARED | A | A:track_005 | A:e27 @ 9.55 |  |
| g57 | 0.05 | TRACK_APPEARED | A | A:track_006 | A:e28 @ 9.55 |  |
| g58 | 0.05 | TRACK_APPEARED | A | A:track_007 | A:e29 @ 9.55 |  |
| g59 | 0.05 | TRACK_APPEARED | A | A:track_008 | A:e30 @ 9.55 |  |
| g60 | 0.05 | CLOSING_START | A | A:track_005 | A:e31 @ 9.55 | active_at_first_observation=True |
| g61 | 0.05 | CLOSING_START | A | A:track_006 | A:e32 @ 9.55 | active_at_first_observation=True |
| g62 | 0.05 | CLOSING_START | A | A:track_007 | A:e33 @ 9.55 | active_at_first_observation=True |
| g63 | 0.05 | CLOSING_START | A | A:track_008 | A:e34 @ 9.55 | active_at_first_observation=True |
| g64 | 0.10 | CLOSING_START | A | A:track_004 | A:e35 @ 9.60 |  |
| g65 | 0.10 | TRACK_LOST | B | A | B:e31 @ 9.60 |  |
| g66 | 0.30 | TRACK_LOST | A | A:track_002 | A:e36 @ 9.80 |  |
| g67 | 0.45 | MOVING_END | B | - | B:e32 @ 9.95 |  |
| g68 | 0.45 | STOP_START | B | - | B:e33 @ 9.95 |  |
| g69 | 0.50 | CLOSING_END | A | A:track_005 | A:e37 @ 10.00 |  |
| g70 | 0.50 | MOVING_END | A | - | A:e38 @ 10.00 |  |
| g71 | 0.50 | STOP_START | A | - | A:e39 @ 10.00 |  |
| g72 | 0.55 | CLOSING_END | A | A:track_003 | A:e40 @ 10.05 |  |
| g73 | 0.55 | CLOSING_END | A | A:track_004 | A:e41 @ 10.05 |  |
| g74 | 0.55 | CLOSING_END | A | A:track_006 | A:e42 @ 10.05 |  |
| g75 | 0.55 | CLOSING_END | A | A:track_007 | A:e43 @ 10.05 |  |
| g76 | 0.55 | CLOSING_END | A | A:track_008 | A:e44 @ 10.05 |  |
| g77 | 2.20 | STOP_SIGN_DETECTED_START | A | A:sign-1 | A:e45 @ 11.70 | relevant_to_ego_path=False |
| g78 | 2.30 | STOP_SIGN_DETECTED_END | A | A:sign-1 | A:e46 @ 11.80 |  |
| g79 | 4.45 | STOP_SIGN_DETECTED_START | A | A:sign-1 | A:e47 @ 13.95 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| g80 | 4.45 | STOP_SIGN_DETECTED_END | A | A:sign-1 | A:e48 @ 13.95 | sign_track=sign-4 |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g15 --PRECEDES--> g17
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g20 --PRECEDES--> g28
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g22 --PRECEDES--> g23
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g23 --PRECEDES--> g31
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g24 --PRECEDES--> g31
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
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
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g39 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g44 --PRECEDES--> g45
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g45 --PRECEDES--> g50
    g45 --PRECEDES--> g51
    g45 --PRECEDES--> g52
    g45 --PRECEDES--> g53
    g45 --PRECEDES--> g54
    g45 --PRECEDES--> g55
    g45 --PRECEDES--> g56
    g45 --PRECEDES--> g57
    g45 --PRECEDES--> g58
    g45 --PRECEDES--> g59
    g45 --PRECEDES--> g60
    g45 --PRECEDES--> g61
    g45 --PRECEDES--> g62
    g45 --PRECEDES--> g63
    g46 --PRECEDES--> g50
    g46 --PRECEDES--> g51
    g46 --PRECEDES--> g52
    g46 --PRECEDES--> g53
    g46 --PRECEDES--> g54
    g46 --PRECEDES--> g55
    g46 --PRECEDES--> g56
    g46 --PRECEDES--> g57
    g46 --PRECEDES--> g58
    g46 --PRECEDES--> g59
    g46 --PRECEDES--> g60
    g46 --PRECEDES--> g61
    g46 --PRECEDES--> g62
    g46 --PRECEDES--> g63
    g47 --PRECEDES--> g50
    g47 --PRECEDES--> g51
    g47 --PRECEDES--> g52
    g47 --PRECEDES--> g53
    g47 --PRECEDES--> g54
    g47 --PRECEDES--> g55
    g47 --PRECEDES--> g56
    g47 --PRECEDES--> g57
    g47 --PRECEDES--> g58
    g47 --PRECEDES--> g59
    g47 --PRECEDES--> g60
    g47 --PRECEDES--> g61
    g47 --PRECEDES--> g62
    g47 --PRECEDES--> g63
    g48 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g48 --PRECEDES--> g53
    g48 --PRECEDES--> g54
    g48 --PRECEDES--> g55
    g48 --PRECEDES--> g56
    g48 --PRECEDES--> g57
    g48 --PRECEDES--> g58
    g48 --PRECEDES--> g59
    g48 --PRECEDES--> g60
    g48 --PRECEDES--> g61
    g48 --PRECEDES--> g62
    g48 --PRECEDES--> g63
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g49 --PRECEDES--> g54
    g49 --PRECEDES--> g55
    g49 --PRECEDES--> g56
    g49 --PRECEDES--> g57
    g49 --PRECEDES--> g58
    g49 --PRECEDES--> g59
    g49 --PRECEDES--> g60
    g49 --PRECEDES--> g61
    g49 --PRECEDES--> g62
    g49 --PRECEDES--> g63
    g50 --PRECEDES--> g64
    g50 --PRECEDES--> g65
    g51 --PRECEDES--> g64
    g51 --PRECEDES--> g65
    g52 --PRECEDES--> g64
    g52 --PRECEDES--> g65
    g53 --PRECEDES--> g64
    g53 --PRECEDES--> g65
    g54 --PRECEDES--> g64
    g54 --PRECEDES--> g65
    g55 --PRECEDES--> g64
    g55 --PRECEDES--> g65
    g56 --PRECEDES--> g64
    g56 --PRECEDES--> g65
    g57 --PRECEDES--> g64
    g57 --PRECEDES--> g65
    g58 --PRECEDES--> g64
    g58 --PRECEDES--> g65
    g59 --PRECEDES--> g64
    g59 --PRECEDES--> g65
    g60 --PRECEDES--> g64
    g60 --PRECEDES--> g65
    g61 --PRECEDES--> g64
    g61 --PRECEDES--> g65
    g62 --PRECEDES--> g64
    g62 --PRECEDES--> g65
    g63 --PRECEDES--> g64
    g63 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g66 --PRECEDES--> g68
    g67 --PRECEDES--> g69
    g67 --PRECEDES--> g70
    g67 --PRECEDES--> g71
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g68 --PRECEDES--> g71
    g69 --PRECEDES--> g72
    g69 --PRECEDES--> g73
    g69 --PRECEDES--> g74
    g69 --PRECEDES--> g75
    g69 --PRECEDES--> g76
    g70 --PRECEDES--> g72
    g70 --PRECEDES--> g73
    g70 --PRECEDES--> g74
    g70 --PRECEDES--> g75
    g70 --PRECEDES--> g76
    g71 --PRECEDES--> g72
    g71 --PRECEDES--> g73
    g71 --PRECEDES--> g74
    g71 --PRECEDES--> g75
    g71 --PRECEDES--> g76
    g72 --PRECEDES--> g77
    g73 --PRECEDES--> g77
    g74 --PRECEDES--> g77
    g75 --PRECEDES--> g77
    g76 --PRECEDES--> g77
    g77 --PRECEDES--> g78
    g78 --PRECEDES--> g79
    g78 --PRECEDES--> g80
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g17
    g39 --SAME_TRACK--> g41
    g40 --SAME_TRACK--> g42
    g56 --SAME_TRACK--> g60
    g57 --SAME_TRACK--> g61
    g58 --SAME_TRACK--> g62
    g59 --SAME_TRACK--> g63
    g49 --SAME_TRACK--> g64
    g39 --SAME_TRACK--> g66
    g56 --SAME_TRACK--> g69
    g40 --SAME_TRACK--> g72
    g49 --SAME_TRACK--> g73
    g57 --SAME_TRACK--> g74
    g58 --SAME_TRACK--> g75
    g59 --SAME_TRACK--> g76
    g10 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g20
    g10 --SAME_TRACK--> g31
    g10 --SAME_TRACK--> g34
    g10 --SAME_TRACK--> g37
    g10 --SAME_TRACK--> g38
    g10 --SAME_TRACK--> g43
    g10 --SAME_TRACK--> g44
    g10 --SAME_TRACK--> g46
    g10 --SAME_TRACK--> g65
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -9.50 | MOVING_START(A); MOVING_START(B) |
| -8.85 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -8.25 | STRONG_THROTTLE_START(B) |
| -7.65 | STRONG_THROTTLE_END(B) |
| -7.40 | STOP_SIGN_DETECTED_START(B,B:sign-1) |
| -7.25 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -7.00 | TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001) |
| -6.95 | TRACK_APPEARED(B,A); CLOSING_START(B,A) |
| -6.90 | STOP_SIGN_DETECTED_END(B,B:sign-1) |
| -6.85 | BRAKE_START(A); HARD_BRAKE_START(A) |
| -6.75 | BRAKE_START(B); HARD_BRAKE_START(B) |
| -6.70 | TRACK_LOST(A,A:track_001) |
| -6.10 | MOVING_END(A); STOP_START(A) |
| -6.00 | CLOSING_END(B,A); MOVING_END(B); STOP_START(B) |
| -2.55 | HARD_BRAKE_END(A); HARD_BRAKE_END(B); BRAKE_END(A); BRAKE_END(B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B) |
| -2.20 | STOP_END(A); MOVING_START(A); CLOSING_START(B,A) |
| -2.15 | STOP_END(B); MOVING_START(B) |
| -1.25 | CRITICAL_TTC_START(B,A) |
| -1.20 | STRONG_THROTTLE_END(A) |
| -0.85 | STRONG_THROTTLE_END(B) |
| -0.55 | EGO_PATH_ENTRY(B,A); PREDICTED_PATH_CONFLICT_START(B,A) |
| -0.10 | TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,A:track_003); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003) |
| -0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| +0.00 | COLLISION(A,B); EGO_PATH_EXIT(B,A); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(A,A:track_004) |
| +0.05 | STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(A,A:track_005); TRACK_APPEARED(A,A:track_006); TRACK_APPEARED(A,A:track_007); TRACK_APPEARED(A,A:track_008); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008) |
| +0.10 | CLOSING_START(A,A:track_004); TRACK_LOST(B,A) |
| +0.30 | TRACK_LOST(A,A:track_002) |
| +0.45 | MOVING_END(B); STOP_START(B) |
| +0.50 | CLOSING_END(A,A:track_005); MOVING_END(A); STOP_START(A) |
| +0.55 | CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_006); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_008) |
| +2.20 | STOP_SIGN_DETECTED_START(A,A:sign-1) |
| +2.30 | STOP_SIGN_DETECTED_END(A,A:sign-1) |
| +4.45 | STOP_SIGN_DETECTED_START(A,A:sign-1); STOP_SIGN_DETECTED_END(A,A:sign-1) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -9.50 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -9.50 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -8.85 | A | g03 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| -8.25 | B | g04 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -7.65 | B | g05 STRONG_THROTTLE_END(B) (B:e03) | ego: MOVING, STRONG_THROTTLE |
| -7.40 | B | g06 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e04) | ego: MOVING |
| -7.25 | A | g07 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign VISIBLE, known, relevant to the path |
| -7.00 | A | g08 TRACK_APPEARED(A,A:track_001) (A:e04)<br>g09 CLOSING_START(A,A:track_001) (A:e05) | ego: MOVING<br>sign-0: STOP sign not visible, known, relevant to the path |
| -6.95 | B | g10 TRACK_APPEARED(B,A) (B:e05)<br>g11 CLOSING_START(B,A) (B:e06) | ego: MOVING<br>sign-1: STOP sign VISIBLE, known, relevant to the path |
| -6.90 | B | g12 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign VISIBLE, known, relevant to the path |
| -6.85 | A | g13 BRAKE_START(A) (A:e06)<br>g14 HARD_BRAKE_START(A) (A:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>sign-0: STOP sign not visible, known, relevant to the path |
| -6.75 | B | g15 BRAKE_START(B) (B:e08)<br>g16 HARD_BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known, relevant to the path |
| -6.70 | A | g17 TRACK_LOST(A,A:track_001) (A:e08) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>sign-0: STOP sign not visible, known, relevant to the path |
| -6.10 | A | g18 MOVING_END(A) (A:e09)<br>g19 STOP_START(A) (A:e10) | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| -6.00 | B | g20 CLOSING_END(B,A) (B:e10)<br>g21 MOVING_END(B) (B:e11)<br>g22 STOP_START(B) (B:e12) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known, relevant to the path |
| -2.55 | A | g23 HARD_BRAKE_END(A) (A:e11)<br>g25 BRAKE_END(A) (A:e12)<br>g27 STRONG_THROTTLE_START(A) (A:e13) | ego: STOP, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| -2.55 | B | g24 HARD_BRAKE_END(B) (B:e13)<br>g26 BRAKE_END(B) (B:e14)<br>g28 STRONG_THROTTLE_START(B) (B:e15) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE<br>sign-1: STOP sign not visible, known, relevant to the path |
| -2.20 | A | g29 STOP_END(A) (A:e14)<br>g30 MOVING_START(A) (A:e15) | ego: STOP, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| -2.20 | B | g31 CLOSING_START(B,A) (B:e16) | ego: STOP, STRONG_THROTTLE<br>track_001: VISIBLE<br>sign-1: STOP sign not visible, known, relevant to the path |
| -2.15 | B | g32 STOP_END(B) (B:e17)<br>g33 MOVING_START(B) (B:e18) | ego: STOP, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known, relevant to the path |
| -1.25 | B | g34 CRITICAL_TTC_START(B,A) (B:e19) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known, relevant to the path |
| -1.20 | A | g35 STRONG_THROTTLE_END(A) (A:e16) | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| -0.85 | B | g36 STRONG_THROTTLE_END(B) (B:e20) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-1: STOP sign not visible, known, relevant to the path |
| -0.55 | B | g37 EGO_PATH_ENTRY(B,A) (B:e21)<br>g38 PREDICTED_PATH_CONFLICT_START(B,A) (B:e22) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-1: STOP sign not visible, known, relevant to the path |
| -0.10 | A | g39 TRACK_APPEARED(A,A:track_002) (A:e17)<br>g40 TRACK_APPEARED(A,A:track_003) (A:e18)<br>g41 CLOSING_START(A,A:track_002) (A:e19)<br>g42 CLOSING_START(A,A:track_003) (A:e20) | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| -0.05 | B | g43 CRITICAL_TTC_END(B,A) (B:e23)<br>g44 CLOSING_END(B,A) (B:e24) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known, relevant to the path |
| +0.00 | A | g45 COLLISION(A,B) (A:e21)<br>g47 STRONG_THROTTLE_START(A) (A:e22)<br>g49 TRACK_APPEARED(A,A:track_004) (A:e23) | ego: MOVING<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| +0.00 | B | g45 COLLISION(A,B) (B:e25)<br>g46 EGO_PATH_EXIT(B,A) (B:e26)<br>g48 STRONG_THROTTLE_START(B) (B:e27) | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known, relevant to the path |
| +0.05 | A | g50 STRONG_THROTTLE_END(A) (A:e24)<br>g52 BRAKE_START(A) (A:e25)<br>g54 HARD_BRAKE_START(A) (A:e26)<br>g56 TRACK_APPEARED(A,A:track_005) (A:e27)<br>g57 TRACK_APPEARED(A,A:track_006) (A:e28)<br>g58 TRACK_APPEARED(A,A:track_007) (A:e29)<br>g59 TRACK_APPEARED(A,A:track_008) (A:e30)<br>g60 CLOSING_START(A,A:track_005) (A:e31)<br>g61 CLOSING_START(A,A:track_006) (A:e32)<br>g62 CLOSING_START(A,A:track_007) (A:e33)<br>g63 CLOSING_START(A,A:track_008) (A:e34) | ego: MOVING, STRONG_THROTTLE<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| +0.05 | B | g51 STRONG_THROTTLE_END(B) (B:e28)<br>g53 BRAKE_START(B) (B:e29)<br>g55 HARD_BRAKE_START(B) (B:e30) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, PATH_CONFLICT<br>sign-1: STOP sign not visible, known, relevant to the path |
| +0.10 | A | g64 CLOSING_START(A,A:track_004) (A:e35) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| +0.10 | B | g65 TRACK_LOST(B,A) (B:e31) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, PATH_CONFLICT<br>sign-1: STOP sign not visible, known, relevant to the path |
| +0.30 | A | g66 TRACK_LOST(A,A:track_002) (A:e36) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path |
| +0.45 | B | g67 MOVING_END(B) (B:e32)<br>g68 STOP_START(B) (B:e33) | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001<br>sign-1: STOP sign not visible, known, relevant to the path |
| +0.50 | A | g69 CLOSING_END(A,A:track_005) (A:e37)<br>g70 MOVING_END(A) (A:e38)<br>g71 STOP_START(A) (A:e39) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known, relevant to the path |
| +0.55 | A | g72 CLOSING_END(A,A:track_003) (A:e40)<br>g73 CLOSING_END(A,A:track_004) (A:e41)<br>g74 CLOSING_END(A,A:track_006) (A:e42)<br>g75 CLOSING_END(A,A:track_007) (A:e43)<br>g76 CLOSING_END(A,A:track_008) (A:e44) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known, relevant to the path |
| +2.20 | A | g77 STOP_SIGN_DETECTED_START(A,A:sign-1) (A:e45) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>track_004: VISIBLE<br>track_005: VISIBLE<br>track_006: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known, relevant to the path |
| +2.30 | A | g78 STOP_SIGN_DETECTED_END(A,A:sign-1) (A:e46) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>track_004: VISIBLE<br>track_005: VISIBLE<br>track_006: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known, relevant to the path<br>sign-1: STOP sign VISIBLE, known |
| +4.45 | A | g79 STOP_SIGN_DETECTED_START(A,A:sign-1) (A:e47)<br>g80 STOP_SIGN_DETECTED_END(A,A:sign-1) (A:e48) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>track_004: VISIBLE<br>track_005: VISIBLE<br>track_006: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known, relevant to the path<br>sign-1: STOP sign not visible, known |

## Plain-language reading

- 9.50 s before the matched collision, A started moving (already the case when first observed).
- 9.50 s before the matched collision, B started moving (already the case when first observed).
- 8.85 s before the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 8.25 s before the matched collision, B started applying strong throttle.
- 7.65 s before the matched collision, B stopped applying strong throttle.
- 7.40 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-1).
- 7.25 s before the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.00 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 7.00 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 6.95 s before the matched collision, B's radar started tracking A.
- 6.95 s before the matched collision, B observed A start closing in (already the case when first observed).
- 6.90 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 6.85 s before the matched collision, A started braking.
- 6.85 s before the matched collision, A started braking hard.
- 6.75 s before the matched collision, B started braking.
- 6.75 s before the matched collision, B started braking hard.
- 6.70 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 6.10 s before the matched collision, A stopped moving.
- 6.10 s before the matched collision, A came to a stop.
- 6.00 s before the matched collision, B observed A stop closing in.
- 6.00 s before the matched collision, B stopped moving.
- 6.00 s before the matched collision, B came to a stop.
- 2.55 s before the matched collision, A stopped braking hard.
- 2.55 s before the matched collision, B stopped braking hard.
- 2.55 s before the matched collision, A released the brake.
- 2.55 s before the matched collision, B released the brake.
- 2.55 s before the matched collision, A started applying strong throttle.
- 2.55 s before the matched collision, B started applying strong throttle.
- 2.20 s before the matched collision, A left its stop.
- 2.20 s before the matched collision, A started moving.
- 2.20 s before the matched collision, B observed A start closing in.
- 2.15 s before the matched collision, B left its stop.
- 2.15 s before the matched collision, B started moving.
- 1.25 s before the matched collision, B's time-to-contact with A became critical.
- 1.20 s before the matched collision, A stopped applying strong throttle.
- 0.85 s before the matched collision, B stopped applying strong throttle.
- 0.55 s before the matched collision, B observed A enter its forward path corridor.
- 0.55 s before the matched collision, B predicted a path conflict with A (close approach ahead if both keep their motion).
- 0.10 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 0.10 s before the matched collision, A's radar started tracking unidentified object A:track_003.
- 0.10 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 0.10 s before the matched collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- 0.05 s before the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s before the matched collision, B observed A stop closing in.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 4032, B: 4032 N*s).
- At the matched collision, B observed A leave its forward path corridor.
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, A's radar started tracking unidentified object A:track_004.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_005.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_006.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_007.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_008.
- 0.05 s after the matched collision, A observed unidentified object A:track_005 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_006 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_007 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_008 start closing in (already the case when first observed).
- 0.10 s after the matched collision, A observed unidentified object A:track_004 start closing in.
- 0.10 s after the matched collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.30 s after the matched collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.50 s after the matched collision, A observed unidentified object A:track_005 stop closing in.
- 0.50 s after the matched collision, A stopped moving.
- 0.50 s after the matched collision, A came to a stop.
- 0.55 s after the matched collision, A observed unidentified object A:track_003 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_004 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_006 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_007 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_008 stop closing in.
- 2.20 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 2.30 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-1.
- 4.45 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- 4.45 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-1.
