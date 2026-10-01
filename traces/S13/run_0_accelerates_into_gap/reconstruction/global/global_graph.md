# Global graph - S13/run_0_accelerates_into_gap

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |
| B:track_004 | anonymous_track | seen only by B; candidate: A |
| B:track_005 | anonymous_track | seen only by B; candidate: A |
| B:track_006 | anonymous_track | seen only by B; candidate: A |
| B:track_007 | anonymous_track | seen only by B; candidate: A |
| B:track_008 | anonymous_track | seen only by B; candidate: A |
| B:track_009 | anonymous_track | seen only by B; candidate: A |
| B:track_010 | anonymous_track | seen only by B; candidate: A |
| B:track_011 | anonymous_track | seen only by B; candidate: A |
| B:track_012 | anonymous_track | seen only by B; candidate: A |
| B:track_013 | anonymous_track | seen only by B; candidate: A |
| B:track_014 | anonymous_track | seen only by B; candidate: A |
| B:track_015 | anonymous_track | seen only by B; candidate: A |
| B:track_016 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e13 | 5.65 | -5.65 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 5.65 | -5.65 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5215.85 vs 5215.85 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 5.65 s before the matched collision<br>not at the contact: last seen 4.65 s before the matched collision (window 0.50 s)<br>speed not comparable with B's own speed before the collision |
| A:track_002 | B | ASSOCIATED | 0.93 | A and B both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 2.30 s before the matched collision<br>at the contact: minimum range 1.35 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.58 m/s over 2.3 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.30 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.30 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.35 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.35 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.55 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.60 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.65 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.65 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.70 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.75 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.80 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.85 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.90 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.90 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_015 | B:track_015 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.95 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_016 | B:track_016 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.95 s after the matched collision<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.65 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.65 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.65 | TRACK_APPEARED_LEFT | A | A:track_001 | A:e02 @ 0.00 |  |
| g04 | -5.65 | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -4.85 | BRAKE_START | B | - | B:e02 @ 0.80 |  |
| g06 | -4.65 | TRACK_LOST | A | A:track_001 | A:e04 @ 1.00 |  |
| g07 | -3.70 | STRONG_THROTTLE_START | A | - | A:e05 @ 1.95 |  |
| g08 | -2.90 | STRONG_THROTTLE_END | A | - | A:e06 @ 2.75 |  |
| g09 | -2.90 | SPEED_LIMIT_EXCEEDED_START | A | - | A:e07 @ 2.75 |  |
| g10 | -2.30 | TRACK_APPEARED_LEFT | A | B | A:e08 @ 3.35 |  |
| g11 | -2.30 | CLOSING_START | A | B | A:e09 @ 3.35 | active_at_first_observation=True |
| g12 | -1.85 | CRITICAL_TTC_START | A | B | A:e10 @ 3.80 |  |
| g13 | -1.60 | CUT_IN_FROM_LEFT_START | A | B | A:e11 @ 4.05 |  |
| g14 | -0.40 | EGO_PATH_ENTRY | A | B | A:e12 @ 5.25 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e13 @ 5.65, B:e03 @ 5.65 | matched_event=collision_001; reference_event=True; peak_impulse=A 5215.85, B 5215.85 |
| g16 | 0.00 | SPEED_LIMIT_EXCEEDED_END | A | - | A:e14 @ 5.65 |  |
| g17 | 0.00 | STRONG_THROTTLE_START | A | - | A:e15 @ 5.65 |  |
| g18 | 0.00 | HARD_BRAKE_START | B | - | B:e04 @ 5.65 |  |
| g19 | 0.05 | CRITICAL_TTC_END | A | B | A:e16 @ 5.70 |  |
| g20 | 0.05 | STRONG_THROTTLE_END | A | - | A:e17 @ 5.70 |  |
| g21 | 0.05 | BRAKE_START | A | - | A:e18 @ 5.70 |  |
| g22 | 0.05 | HARD_BRAKE_START | A | - | A:e19 @ 5.70 |  |
| g23 | 0.15 | CLOSING_END | A | B | A:e20 @ 5.80 |  |
| g24 | 0.30 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e05 @ 5.95 |  |
| g25 | 0.30 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e06 @ 5.95 |  |
| g26 | 0.30 | CLOSING_START | B | B:track_001 | B:e07 @ 5.95 | active_at_first_observation=True |
| g27 | 0.30 | CLOSING_START | B | B:track_002 | B:e08 @ 5.95 | active_at_first_observation=True |
| g28 | 0.30 | CRITICAL_TTC_START | B | B:track_001 | B:e09 @ 5.95 | active_at_first_observation=True |
| g29 | 0.30 | CRITICAL_TTC_START | B | B:track_002 | B:e10 @ 5.95 | active_at_first_observation=True |
| g30 | 0.35 | TRACK_APPEARED_RIGHT | B | B:track_003 | B:e11 @ 6.00 |  |
| g31 | 0.35 | TRACK_APPEARED_RIGHT | B | B:track_004 | B:e12 @ 6.00 |  |
| g32 | 0.35 | CLOSING_START | B | B:track_003 | B:e13 @ 6.00 | active_at_first_observation=True |
| g33 | 0.35 | CLOSING_START | B | B:track_004 | B:e14 @ 6.00 | active_at_first_observation=True |
| g34 | 0.55 | TRACK_APPEARED_RIGHT | B | B:track_005 | B:e15 @ 6.20 |  |
| g35 | 0.55 | CLOSING_START | B | B:track_005 | B:e16 @ 6.20 | active_at_first_observation=True |
| g36 | 0.60 | TRACK_APPEARED_LEFT | B | B:track_006 | B:e17 @ 6.25 |  |
| g37 | 0.60 | CLOSING_START | B | B:track_006 | B:e18 @ 6.25 | active_at_first_observation=True |
| g38 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_007 | B:e19 @ 6.30 |  |
| g39 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_008 | B:e20 @ 6.30 |  |
| g40 | 0.65 | CLOSING_START | B | B:track_007 | B:e21 @ 6.30 | active_at_first_observation=True |
| g41 | 0.65 | CLOSING_START | B | B:track_008 | B:e22 @ 6.30 | active_at_first_observation=True |
| g42 | 0.70 | TRACK_APPEARED_LEFT | B | B:track_009 | B:e23 @ 6.35 |  |
| g43 | 0.70 | CLOSING_START | B | B:track_009 | B:e24 @ 6.35 | active_at_first_observation=True |
| g44 | 0.75 | TRACK_APPEARED_LEFT | B | B:track_010 | B:e25 @ 6.40 |  |
| g45 | 0.75 | CLOSING_START | A | B | A:e21 @ 6.40 |  |
| g46 | 0.75 | CLOSING_START | B | B:track_010 | B:e26 @ 6.40 | active_at_first_observation=True |
| g47 | 0.75 | CRITICAL_TTC_START | A | B | A:e22 @ 6.40 |  |
| g48 | 0.80 | TRACK_APPEARED_LEFT | B | B:track_011 | B:e27 @ 6.45 |  |
| g49 | 0.80 | CLOSING_START | B | B:track_011 | B:e28 @ 6.45 | active_at_first_observation=True |
| g50 | 0.80 | TRACK_LOST | B | B:track_006 | B:e29 @ 6.45 |  |
| g51 | 0.85 | TRACK_APPEARED_LEFT | B | B:track_012 | B:e30 @ 6.50 |  |
| g52 | 0.85 | CLOSING_START | B | B:track_012 | B:e31 @ 6.50 | active_at_first_observation=True |
| g53 | 0.90 | TRACK_APPEARED_LEFT | B | B:track_013 | B:e32 @ 6.55 |  |
| g54 | 0.90 | TRACK_APPEARED_RIGHT | B | B:track_014 | B:e33 @ 6.55 |  |
| g55 | 0.90 | CLOSING_START | B | B:track_013 | B:e34 @ 6.55 | active_at_first_observation=True |
| g56 | 0.90 | CLOSING_START | B | B:track_014 | B:e35 @ 6.55 | active_at_first_observation=True |
| g57 | 0.90 | TRACK_LOST | B | B:track_008 | B:e36 @ 6.55 |  |
| g58 | 0.95 | TRACK_APPEARED_LEFT | B | B:track_015 | B:e37 @ 6.60 |  |
| g59 | 0.95 | TRACK_APPEARED_RIGHT | B | B:track_016 | B:e38 @ 6.60 |  |
| g60 | 0.95 | EGO_PATH_ENTRY | B | B:track_001 | B:e39 @ 6.60 |  |
| g61 | 0.95 | EGO_PATH_ENTRY | B | B:track_004 | B:e40 @ 6.60 |  |
| g62 | 0.95 | CLOSING_START | B | B:track_015 | B:e41 @ 6.60 | active_at_first_observation=True |
| g63 | 0.95 | CLOSING_START | B | B:track_016 | B:e42 @ 6.60 | active_at_first_observation=True |
| g64 | 0.95 | TRACK_LOST | B | B:track_007 | B:e43 @ 6.60 |  |
| g65 | 0.95 | TRACK_LOST | B | B:track_009 | B:e44 @ 6.60 |  |
| g66 | 1.00 | TRACK_LOST | B | B:track_010 | B:e45 @ 6.65 |  |
| g67 | 1.05 | EGO_PATH_EXIT | B | B:track_004 | B:e46 @ 6.70 |  |
| g68 | 1.05 | TRACK_LOST | B | B:track_011 | B:e47 @ 6.70 |  |
| g69 | 1.10 | CRITICAL_TTC_END | B | B:track_002 | B:e48 @ 6.75 |  |
| g70 | 1.10 | TRACK_LOST | B | B:track_012 | B:e49 @ 6.75 |  |
| g71 | 1.15 | CRITICAL_TTC_END | B | B:track_001 | B:e50 @ 6.80 |  |
| g72 | 1.15 | EGO_PATH_ENTRY | B | B:track_003 | B:e51 @ 6.80 |  |
| g73 | 1.15 | TRACK_LOST | B | B:track_013 | B:e52 @ 6.80 |  |
| g74 | 1.25 | CUT_IN_FROM_LEFT_END | A | B | A:e23 @ 6.90 |  |
| g75 | 1.25 | CRITICAL_TTC_END | A | B | A:e24 @ 6.90 |  |
| g76 | 1.25 | CLOSING_END | A | B | A:e25 @ 6.90 |  |
| g77 | 1.25 | CLOSING_END | B | B:track_001 | B:e53 @ 6.90 |  |
| g78 | 1.25 | CLOSING_END | B | B:track_003 | B:e54 @ 6.90 |  |
| g79 | 1.25 | CLOSING_END | B | B:track_004 | B:e55 @ 6.90 |  |
| g80 | 1.25 | CLOSING_END | B | B:track_005 | B:e56 @ 6.90 |  |
| g81 | 1.25 | CLOSING_END | B | B:track_014 | B:e57 @ 6.90 |  |
| g82 | 1.25 | CLOSING_END | B | B:track_015 | B:e58 @ 6.90 |  |
| g83 | 1.25 | MOVING_END | B | - | B:e59 @ 6.90 |  |
| g84 | 1.25 | STOP_START | B | - | B:e60 @ 6.90 |  |
| g85 | 1.30 | CLOSING_END | B | B:track_016 | B:e61 @ 6.95 |  |
| g86 | 1.30 | MOVING_END | A | - | A:e26 @ 6.95 |  |
| g87 | 1.30 | STOP_START | A | - | A:e27 @ 6.95 |  |
| g88 | 1.35 | CLOSING_END | B | B:track_002 | B:e62 @ 7.00 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g05
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
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g15 --PRECEDES--> g21
    g15 --PRECEDES--> g22
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g16 --PRECEDES--> g21
    g16 --PRECEDES--> g22
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g18 --PRECEDES--> g21
    g18 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g20 --PRECEDES--> g23
    g21 --PRECEDES--> g23
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g24 --PRECEDES--> g31
    g24 --PRECEDES--> g32
    g24 --PRECEDES--> g33
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g25 --PRECEDES--> g32
    g25 --PRECEDES--> g33
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g26 --PRECEDES--> g33
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g30 --PRECEDES--> g35
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g32 --PRECEDES--> g34
    g32 --PRECEDES--> g35
    g33 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g39 --PRECEDES--> g42
    g39 --PRECEDES--> g43
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g44 --PRECEDES--> g50
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g45 --PRECEDES--> g50
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g48 --PRECEDES--> g52
    g49 --PRECEDES--> g51
    g49 --PRECEDES--> g52
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g51 --PRECEDES--> g57
    g52 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g52 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g53 --PRECEDES--> g58
    g53 --PRECEDES--> g59
    g53 --PRECEDES--> g60
    g53 --PRECEDES--> g61
    g53 --PRECEDES--> g62
    g53 --PRECEDES--> g63
    g53 --PRECEDES--> g64
    g53 --PRECEDES--> g65
    g54 --PRECEDES--> g58
    g54 --PRECEDES--> g59
    g54 --PRECEDES--> g60
    g54 --PRECEDES--> g61
    g54 --PRECEDES--> g62
    g54 --PRECEDES--> g63
    g54 --PRECEDES--> g64
    g54 --PRECEDES--> g65
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g55 --PRECEDES--> g60
    g55 --PRECEDES--> g61
    g55 --PRECEDES--> g62
    g55 --PRECEDES--> g63
    g55 --PRECEDES--> g64
    g55 --PRECEDES--> g65
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g56 --PRECEDES--> g60
    g56 --PRECEDES--> g61
    g56 --PRECEDES--> g62
    g56 --PRECEDES--> g63
    g56 --PRECEDES--> g64
    g56 --PRECEDES--> g65
    g57 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g57 --PRECEDES--> g60
    g57 --PRECEDES--> g61
    g57 --PRECEDES--> g62
    g57 --PRECEDES--> g63
    g57 --PRECEDES--> g64
    g57 --PRECEDES--> g65
    g58 --PRECEDES--> g66
    g59 --PRECEDES--> g66
    g60 --PRECEDES--> g66
    g61 --PRECEDES--> g66
    g62 --PRECEDES--> g66
    g63 --PRECEDES--> g66
    g64 --PRECEDES--> g66
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g66 --PRECEDES--> g68
    g67 --PRECEDES--> g69
    g67 --PRECEDES--> g70
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g69 --PRECEDES--> g71
    g69 --PRECEDES--> g72
    g69 --PRECEDES--> g73
    g70 --PRECEDES--> g71
    g70 --PRECEDES--> g72
    g70 --PRECEDES--> g73
    g71 --PRECEDES--> g74
    g71 --PRECEDES--> g75
    g71 --PRECEDES--> g76
    g71 --PRECEDES--> g77
    g71 --PRECEDES--> g78
    g71 --PRECEDES--> g79
    g71 --PRECEDES--> g80
    g71 --PRECEDES--> g81
    g71 --PRECEDES--> g82
    g71 --PRECEDES--> g83
    g71 --PRECEDES--> g84
    g72 --PRECEDES--> g74
    g72 --PRECEDES--> g75
    g72 --PRECEDES--> g76
    g72 --PRECEDES--> g77
    g72 --PRECEDES--> g78
    g72 --PRECEDES--> g79
    g72 --PRECEDES--> g80
    g72 --PRECEDES--> g81
    g72 --PRECEDES--> g82
    g72 --PRECEDES--> g83
    g72 --PRECEDES--> g84
    g73 --PRECEDES--> g74
    g73 --PRECEDES--> g75
    g73 --PRECEDES--> g76
    g73 --PRECEDES--> g77
    g73 --PRECEDES--> g78
    g73 --PRECEDES--> g79
    g73 --PRECEDES--> g80
    g73 --PRECEDES--> g81
    g73 --PRECEDES--> g82
    g73 --PRECEDES--> g83
    g73 --PRECEDES--> g84
    g74 --PRECEDES--> g85
    g74 --PRECEDES--> g86
    g74 --PRECEDES--> g87
    g75 --PRECEDES--> g85
    g75 --PRECEDES--> g86
    g75 --PRECEDES--> g87
    g76 --PRECEDES--> g85
    g76 --PRECEDES--> g86
    g76 --PRECEDES--> g87
    g77 --PRECEDES--> g85
    g77 --PRECEDES--> g86
    g77 --PRECEDES--> g87
    g78 --PRECEDES--> g85
    g78 --PRECEDES--> g86
    g78 --PRECEDES--> g87
    g79 --PRECEDES--> g85
    g79 --PRECEDES--> g86
    g79 --PRECEDES--> g87
    g80 --PRECEDES--> g85
    g80 --PRECEDES--> g86
    g80 --PRECEDES--> g87
    g81 --PRECEDES--> g85
    g81 --PRECEDES--> g86
    g81 --PRECEDES--> g87
    g82 --PRECEDES--> g85
    g82 --PRECEDES--> g86
    g82 --PRECEDES--> g87
    g83 --PRECEDES--> g85
    g83 --PRECEDES--> g86
    g83 --PRECEDES--> g87
    g84 --PRECEDES--> g85
    g84 --PRECEDES--> g86
    g84 --PRECEDES--> g87
    g85 --PRECEDES--> g88
    g86 --PRECEDES--> g88
    g87 --PRECEDES--> g88
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g06
    g10 --SAME_TRACK--> g11
    g10 --SAME_TRACK--> g12
    g10 --SAME_TRACK--> g13
    g10 --SAME_TRACK--> g14
    g10 --SAME_TRACK--> g19
    g10 --SAME_TRACK--> g23
    g10 --SAME_TRACK--> g45
    g10 --SAME_TRACK--> g47
    g10 --SAME_TRACK--> g74
    g10 --SAME_TRACK--> g75
    g10 --SAME_TRACK--> g76
    g24 --SAME_TRACK--> g26
    g25 --SAME_TRACK--> g27
    g24 --SAME_TRACK--> g28
    g25 --SAME_TRACK--> g29
    g30 --SAME_TRACK--> g32
    g31 --SAME_TRACK--> g33
    g34 --SAME_TRACK--> g35
    g36 --SAME_TRACK--> g37
    g38 --SAME_TRACK--> g40
    g39 --SAME_TRACK--> g41
    g42 --SAME_TRACK--> g43
    g44 --SAME_TRACK--> g46
    g48 --SAME_TRACK--> g49
    g36 --SAME_TRACK--> g50
    g51 --SAME_TRACK--> g52
    g53 --SAME_TRACK--> g55
    g54 --SAME_TRACK--> g56
    g39 --SAME_TRACK--> g57
    g24 --SAME_TRACK--> g60
    g31 --SAME_TRACK--> g61
    g58 --SAME_TRACK--> g62
    g59 --SAME_TRACK--> g63
    g38 --SAME_TRACK--> g64
    g42 --SAME_TRACK--> g65
    g44 --SAME_TRACK--> g66
    g31 --SAME_TRACK--> g67
    g48 --SAME_TRACK--> g68
    g25 --SAME_TRACK--> g69
    g51 --SAME_TRACK--> g70
    g24 --SAME_TRACK--> g71
    g30 --SAME_TRACK--> g72
    g53 --SAME_TRACK--> g73
    g24 --SAME_TRACK--> g77
    g30 --SAME_TRACK--> g78
    g31 --SAME_TRACK--> g79
    g34 --SAME_TRACK--> g80
    g54 --SAME_TRACK--> g81
    g58 --SAME_TRACK--> g82
    g59 --SAME_TRACK--> g85
    g25 --SAME_TRACK--> g88
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.65 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -4.85 | BRAKE_START(B) |
| -4.65 | TRACK_LOST(A,A:track_001) |
| -3.70 | STRONG_THROTTLE_START(A) |
| -2.90 | STRONG_THROTTLE_END(A); SPEED_LIMIT_EXCEEDED_START(A) |
| -2.30 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -1.85 | CRITICAL_TTC_START(A,B) |
| -1.60 | CUT_IN_FROM_LEFT_START(A,B) |
| -0.40 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A); STRONG_THROTTLE_START(A); HARD_BRAKE_START(B) |
| +0.05 | CRITICAL_TTC_END(A,B); STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A) |
| +0.15 | CLOSING_END(A,B) |
| +0.30 | TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001); CRITICAL_TTC_START(B,B:track_002) |
| +0.35 | TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_004); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004) |
| +0.55 | TRACK_APPEARED_RIGHT(B,B:track_005); CLOSING_START(B,B:track_005) |
| +0.60 | TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_006) |
| +0.65 | TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008) |
| +0.70 | TRACK_APPEARED_LEFT(B,B:track_009); CLOSING_START(B,B:track_009) |
| +0.75 | TRACK_APPEARED_LEFT(B,B:track_010); CLOSING_START(A,B); CLOSING_START(B,B:track_010); CRITICAL_TTC_START(A,B) |
| +0.80 | TRACK_APPEARED_LEFT(B,B:track_011); CLOSING_START(B,B:track_011); TRACK_LOST(B,B:track_006) |
| +0.85 | TRACK_APPEARED_LEFT(B,B:track_012); CLOSING_START(B,B:track_012) |
| +0.90 | TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_RIGHT(B,B:track_014); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); TRACK_LOST(B,B:track_008) |
| +0.95 | TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_RIGHT(B,B:track_016); EGO_PATH_ENTRY(B,B:track_001); EGO_PATH_ENTRY(B,B:track_004); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_016); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_009) |
| +1.00 | TRACK_LOST(B,B:track_010) |
| +1.05 | EGO_PATH_EXIT(B,B:track_004); TRACK_LOST(B,B:track_011) |
| +1.10 | CRITICAL_TTC_END(B,B:track_002); TRACK_LOST(B,B:track_012) |
| +1.15 | CRITICAL_TTC_END(B,B:track_001); EGO_PATH_ENTRY(B,B:track_003); TRACK_LOST(B,B:track_013) |
| +1.25 | CUT_IN_FROM_LEFT_END(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_015); MOVING_END(B); STOP_START(B) |
| +1.30 | CLOSING_END(B,B:track_016); MOVING_END(A); STOP_START(A) |
| +1.35 | CLOSING_END(B,B:track_002) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.65 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,A:track_001) (A:e02)<br>g04 CLOSING_START(A,A:track_001) (A:e03) | ego: not yet observed |
| -5.65 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.85 | B | g05 BRAKE_START(B) (B:e02) | ego: MOVING |
| -4.65 | A | g06 TRACK_LOST(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -3.70 | A | g07 STRONG_THROTTLE_START(A) (A:e05) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| -2.90 | A | g08 STRONG_THROTTLE_END(A) (A:e06)<br>g09 SPEED_LIMIT_EXCEEDED_START(A) (A:e07) | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001 |
| -2.30 | A | g10 TRACK_APPEARED_LEFT(A,B) (A:e08)<br>g11 CLOSING_START(A,B) (A:e09) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track lost, states UNKNOWN: track_001 |
| -1.85 | A | g12 CRITICAL_TTC_START(A,B) (A:e10) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.60 | A | g13 CUT_IN_FROM_LEFT_START(A,B) (A:e11) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 |
| -0.40 | A | g14 EGO_PATH_ENTRY(A,B) (A:e12) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.00 | A | g15 COLLISION(A,B) (A:e13)<br>g16 SPEED_LIMIT_EXCEEDED_END(A) (A:e14)<br>g17 STRONG_THROTTLE_START(A) (A:e15) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g15 COLLISION(A,B) (B:e03)<br>g18 HARD_BRAKE_START(B) (B:e04) | ego: MOVING, BRAKE |
| +0.05 | A | g19 CRITICAL_TTC_END(A,B) (A:e16)<br>g20 STRONG_THROTTLE_END(A) (A:e17)<br>g21 BRAKE_START(A) (A:e18)<br>g22 HARD_BRAKE_START(A) (A:e19) | ego: MOVING, STRONG_THROTTLE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.15 | A | g23 CLOSING_END(A,B) (A:e20) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.30 | B | g24 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e05)<br>g25 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e06)<br>g26 CLOSING_START(B,B:track_001) (B:e07)<br>g27 CLOSING_START(B,B:track_002) (B:e08)<br>g28 CRITICAL_TTC_START(B,B:track_001) (B:e09)<br>g29 CRITICAL_TTC_START(B,B:track_002) (B:e10) | ego: MOVING, BRAKE, HARD_BRAKE |
| +0.35 | B | g30 TRACK_APPEARED_RIGHT(B,B:track_003) (B:e11)<br>g31 TRACK_APPEARED_RIGHT(B,B:track_004) (B:e12)<br>g32 CLOSING_START(B,B:track_003) (B:e13)<br>g33 CLOSING_START(B,B:track_004) (B:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| +0.55 | B | g34 TRACK_APPEARED_RIGHT(B,B:track_005) (B:e15)<br>g35 CLOSING_START(B,B:track_005) (B:e16) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.60 | B | g36 TRACK_APPEARED_LEFT(B,B:track_006) (B:e17)<br>g37 CLOSING_START(B,B:track_006) (B:e18) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING |
| +0.65 | B | g38 TRACK_APPEARED_LEFT(B,B:track_007) (B:e19)<br>g39 TRACK_APPEARED_LEFT(B,B:track_008) (B:e20)<br>g40 CLOSING_START(B,B:track_007) (B:e21)<br>g41 CLOSING_START(B,B:track_008) (B:e22) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| +0.70 | B | g42 TRACK_APPEARED_LEFT(B,B:track_009) (B:e23)<br>g43 CLOSING_START(B,B:track_009) (B:e24) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| +0.75 | B | g44 TRACK_APPEARED_LEFT(B,B:track_010) (B:e25)<br>g46 CLOSING_START(B,B:track_010) (B:e26) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| +0.75 | A | g45 CLOSING_START(A,B) (A:e21)<br>g47 CRITICAL_TTC_START(A,B) (A:e22) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.80 | B | g48 TRACK_APPEARED_LEFT(B,B:track_011) (B:e27)<br>g49 CLOSING_START(B,B:track_011) (B:e28)<br>g50 TRACK_LOST(B,B:track_006) (B:e29) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| +0.85 | B | g51 TRACK_APPEARED_LEFT(B,B:track_012) (B:e30)<br>g52 CLOSING_START(B,B:track_012) (B:e31) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_006 |
| +0.90 | B | g53 TRACK_APPEARED_LEFT(B,B:track_013) (B:e32)<br>g54 TRACK_APPEARED_RIGHT(B,B:track_014) (B:e33)<br>g55 CLOSING_START(B,B:track_013) (B:e34)<br>g56 CLOSING_START(B,B:track_014) (B:e35)<br>g57 TRACK_LOST(B,B:track_008) (B:e36) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_006 |
| +0.95 | B | g58 TRACK_APPEARED_LEFT(B,B:track_015) (B:e37)<br>g59 TRACK_APPEARED_RIGHT(B,B:track_016) (B:e38)<br>g60 EGO_PATH_ENTRY(B,B:track_001) (B:e39)<br>g61 EGO_PATH_ENTRY(B,B:track_004) (B:e40)<br>g62 CLOSING_START(B,B:track_015) (B:e41)<br>g63 CLOSING_START(B,B:track_016) (B:e42)<br>g64 TRACK_LOST(B,B:track_007) (B:e43)<br>g65 TRACK_LOST(B,B:track_009) (B:e44) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_006, track_008 |
| +1.00 | B | g66 TRACK_LOST(B,B:track_010) (B:e45) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_006, track_007, track_008, track_009 |
| +1.05 | B | g67 EGO_PATH_EXIT(B,B:track_004) (B:e46)<br>g68 TRACK_LOST(B,B:track_011) (B:e47) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING, IN_EGO_PATH<br>track_005: CLOSING<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_006, track_007, track_008, track_009, track_010 |
| +1.10 | B | g69 CRITICAL_TTC_END(B,B:track_002) (B:e48)<br>g70 TRACK_LOST(B,B:track_012) (B:e49) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_012: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_006, track_007, track_008, track_009, track_010, track_011 |
| +1.15 | B | g71 CRITICAL_TTC_END(B,B:track_001) (B:e50)<br>g72 EGO_PATH_ENTRY(B,B:track_003) (B:e51)<br>g73 TRACK_LOST(B,B:track_013) (B:e52) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_013: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_006, track_007, track_008, track_009, track_010, track_011, track_012 |
| +1.25 | A | g74 CUT_IN_FROM_LEFT_END(A,B) (A:e23)<br>g75 CRITICAL_TTC_END(A,B) (A:e24)<br>g76 CLOSING_END(A,B) (A:e25) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +1.25 | B | g77 CLOSING_END(B,B:track_001) (B:e53)<br>g78 CLOSING_END(B,B:track_003) (B:e54)<br>g79 CLOSING_END(B,B:track_004) (B:e55)<br>g80 CLOSING_END(B,B:track_005) (B:e56)<br>g81 CLOSING_END(B,B:track_014) (B:e57)<br>g82 CLOSING_END(B,B:track_015) (B:e58)<br>g83 MOVING_END(B) (B:e59)<br>g84 STOP_START(B) (B:e60) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING, IN_EGO_PATH<br>track_004: CLOSING<br>track_005: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +1.30 | B | g85 CLOSING_END(B,B:track_016) (B:e61) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +1.30 | A | g86 MOVING_END(A) (A:e26)<br>g87 STOP_START(A) (A:e27) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +1.35 | B | g88 CLOSING_END(B,B:track_002) (B:e62) | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: IN_EGO_PATH<br>track_004: no active state<br>track_005: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track lost, states UNKNOWN: track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |

## Plain-language reading

- 5.65 s before the matched collision, A started moving (already the case when first observed).
- 5.65 s before the matched collision, B started moving (already the case when first observed).
- 5.65 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 5.65 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 4.85 s before the matched collision, B started braking.
- 4.65 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 3.70 s before the matched collision, A started applying strong throttle.
- 2.90 s before the matched collision, A stopped applying strong throttle.
- 2.90 s before the matched collision, A began exceeding the speed limit.
- 2.30 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 2.30 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.85 s before the matched collision, A's time-to-contact with B became critical.
- 1.60 s before the matched collision, A observed B cutting in from the left.
- 0.40 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5216, B: 5216 N*s).
- At the matched collision, A returned within the speed limit.
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started braking hard.
- 0.05 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.15 s after the matched collision, A observed B stop closing in.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 0.30 s after the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 0.30 s after the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.30 s after the matched collision, B's time-to-contact with unidentified object B:track_001 became critical (already the case when first observed).
- 0.30 s after the matched collision, B's time-to-contact with unidentified object B:track_002 became critical (already the case when first observed).
- 0.35 s after the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 0.35 s after the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its right.
- 0.35 s after the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.35 s after the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.55 s after the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its right.
- 0.55 s after the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.60 s after the matched collision, B's radar started tracking unidentified object B:track_006, which appeared on its left.
- 0.60 s after the matched collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_008, which appeared on its left.
- 0.65 s after the matched collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B observed unidentified object B:track_008 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_009, which appeared on its left.
- 0.70 s after the matched collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_010, which appeared on its left.
- 0.75 s after the matched collision, A observed B start closing in.
- 0.75 s after the matched collision, B observed unidentified object B:track_010 start closing in (already the case when first observed).
- 0.75 s after the matched collision, A's time-to-contact with B became critical.
- 0.80 s after the matched collision, B's radar started tracking unidentified object B:track_011, which appeared on its left.
- 0.80 s after the matched collision, B observed unidentified object B:track_011 start closing in (already the case when first observed).
- 0.80 s after the matched collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the matched collision, B's radar started tracking unidentified object B:track_012, which appeared on its left.
- 0.85 s after the matched collision, B observed unidentified object B:track_012 start closing in (already the case when first observed).
- 0.90 s after the matched collision, B's radar started tracking unidentified object B:track_013, which appeared on its left.
- 0.90 s after the matched collision, B's radar started tracking unidentified object B:track_014, which appeared on its right.
- 0.90 s after the matched collision, B observed unidentified object B:track_013 start closing in (already the case when first observed).
- 0.90 s after the matched collision, B observed unidentified object B:track_014 start closing in (already the case when first observed).
- 0.90 s after the matched collision, B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the matched collision, B's radar started tracking unidentified object B:track_015, which appeared on its left.
- 0.95 s after the matched collision, B's radar started tracking unidentified object B:track_016, which appeared on its right.
- 0.95 s after the matched collision, B observed unidentified object B:track_001 enter its forward path corridor.
- 0.95 s after the matched collision, B observed unidentified object B:track_004 enter its forward path corridor.
- 0.95 s after the matched collision, B observed unidentified object B:track_015 start closing in (already the case when first observed).
- 0.95 s after the matched collision, B observed unidentified object B:track_016 start closing in (already the case when first observed).
- 0.95 s after the matched collision, B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the matched collision, B's radar lost unidentified object B:track_009 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the matched collision, B's radar lost unidentified object B:track_010 (its states are UNKNOWN from then on, not ended).
- 1.05 s after the matched collision, B observed unidentified object B:track_004 leave its forward path corridor.
- 1.05 s after the matched collision, B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- 1.10 s after the matched collision, B's time-to-contact with unidentified object B:track_002 stopped being critical.
- 1.10 s after the matched collision, B's radar lost unidentified object B:track_012 (its states are UNKNOWN from then on, not ended).
- 1.15 s after the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.15 s after the matched collision, B observed unidentified object B:track_003 enter its forward path corridor.
- 1.15 s after the matched collision, B's radar lost unidentified object B:track_013 (its states are UNKNOWN from then on, not ended).
- 1.25 s after the matched collision, A observed B's cut-in from the left settle.
- 1.25 s after the matched collision, A's time-to-contact with B stopped being critical.
- 1.25 s after the matched collision, A observed B stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_004 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_005 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_014 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_015 stop closing in.
- 1.25 s after the matched collision, B stopped moving.
- 1.25 s after the matched collision, B came to a stop.
- 1.30 s after the matched collision, B observed unidentified object B:track_016 stop closing in.
- 1.30 s after the matched collision, A stopped moving.
- 1.30 s after the matched collision, A came to a stop.
- 1.35 s after the matched collision, B observed unidentified object B:track_002 stop closing in.
