# Global graph - S05/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
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
| B:track_017 | anonymous_track | seen only by B; candidate: A |
| B:track_018 | anonymous_track | seen only by B; candidate: A |
| B:track_019 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e06 | 3.70 | -3.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 3.70 | -3.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6116.26 vs 6116.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.90 | A and B both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.50 s before the matched collision<br>at the contact: minimum range 0.90 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.70 m/s over 2.5 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.50 s before the matched collision<br>not at the contact: minimum range 5.59 m in the last 0.50 s (needs <= 3.50 m)<br>track speed agrees with A's own speed: RMSE 0.58 m/s over 2.2 s |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 18.91 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 32.42 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 37.27 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 22.75 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 29.98 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.10 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.10 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.10 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.10 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.15 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.15 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_015 | B:track_015 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.20 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_016 | B:track_016 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.20 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_017 | B:track_017 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.20 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_018 | B:track_018 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 27.37 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_019 | B:track_019 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.30 s after the matched collision<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -2.85 | STRONG_THROTTLE_START | B | - | B:e02 @ 0.85 |  |
| g04 | -2.50 | TRACK_APPEARED_LEFT | B | B:track_001 | B:e03 @ 1.20 |  |
| g05 | -2.50 | TRACK_APPEARED_RIGHT | A | B | A:e02 @ 1.20 |  |
| g06 | -2.50 | CLOSING_START | A | B | A:e03 @ 1.20 | active_at_first_observation=True |
| g07 | -2.50 | CLOSING_START | B | B:track_001 | B:e04 @ 1.20 | active_at_first_observation=True |
| g08 | -2.10 | STRONG_THROTTLE_END | B | - | B:e05 @ 1.60 |  |
| g09 | -2.05 | CRITICAL_TTC_START | A | B | A:e04 @ 1.65 |  |
| g10 | -2.05 | CRITICAL_TTC_START | B | B:track_001 | B:e06 @ 1.65 |  |
| g11 | -0.35 | TRACK_LOST | B | B:track_001 | B:e07 @ 3.35 |  |
| g12 | -0.25 | EGO_PATH_ENTRY | A | B | A:e05 @ 3.45 |  |
| g13 | 0.00 | COLLISION | - | A, B | A:e06 @ 3.70, B:e08 @ 3.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 6116.26, B 6116.26 |
| g14 | 0.00 | CRITICAL_TTC_END | A | B | A:e07 @ 3.70 |  |
| g15 | 0.00 | CLOSING_END | A | B | A:e08 @ 3.70 |  |
| g16 | 0.00 | STRONG_THROTTLE_START | A | - | A:e09 @ 3.70 |  |
| g17 | 0.00 | STRONG_THROTTLE_START | B | - | B:e09 @ 3.70 |  |
| g18 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e10 @ 3.70 |  |
| g19 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_003 | B:e11 @ 3.70 |  |
| g20 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_004 | B:e12 @ 3.70 |  |
| g21 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_005 | B:e13 @ 3.70 |  |
| g22 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_007 | B:e14 @ 3.70 |  |
| g23 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_018 | B:e15 @ 3.70 |  |
| g24 | 0.00 | CLOSING_START | B | B:track_002 | B:e16 @ 3.70 | active_at_first_observation=True |
| g25 | 0.00 | CLOSING_START | B | B:track_004 | B:e17 @ 3.70 | active_at_first_observation=True |
| g26 | 0.00 | CLOSING_START | B | B:track_005 | B:e18 @ 3.70 | active_at_first_observation=True |
| g27 | 0.00 | CLOSING_START | B | B:track_007 | B:e19 @ 3.70 | active_at_first_observation=True |
| g28 | 0.00 | CLOSING_START | B | B:track_018 | B:e20 @ 3.70 | active_at_first_observation=True |
| g29 | 0.05 | STRONG_THROTTLE_END | A | - | A:e10 @ 3.75 |  |
| g30 | 0.05 | STRONG_THROTTLE_END | B | - | B:e21 @ 3.75 |  |
| g31 | 0.05 | BRAKE_START | A | - | A:e11 @ 3.75 |  |
| g32 | 0.05 | BRAKE_START | B | - | B:e22 @ 3.75 |  |
| g33 | 0.05 | HARD_BRAKE_START | A | - | A:e12 @ 3.75 |  |
| g34 | 0.05 | HARD_BRAKE_START | B | - | B:e23 @ 3.75 |  |
| g35 | 0.05 | TRACK_APPEARED_LEFT | B | B:track_012 | B:e24 @ 3.75 |  |
| g36 | 0.05 | TRACK_APPEARED_RIGHT | B | B:track_006 | B:e25 @ 3.75 |  |
| g37 | 0.05 | EGO_PATH_ENTRY | B | B:track_003 | B:e26 @ 3.75 |  |
| g38 | 0.05 | CLOSING_START | B | B:track_012 | B:e27 @ 3.75 | active_at_first_observation=True |
| g39 | 0.10 | EGO_PATH_EXIT | B | B:track_003 | B:e28 @ 3.80 |  |
| g40 | 0.10 | TRACK_APPEARED_LEFT | B | B:track_008 | B:e29 @ 3.80 |  |
| g41 | 0.10 | TRACK_APPEARED_LEFT | B | B:track_009 | B:e30 @ 3.80 |  |
| g42 | 0.10 | TRACK_APPEARED_LEFT | B | B:track_010 | B:e31 @ 3.80 |  |
| g43 | 0.10 | TRACK_APPEARED_RIGHT | B | B:track_011 | B:e32 @ 3.80 |  |
| g44 | 0.10 | EGO_PATH_ENTRY | B | B:track_005 | B:e33 @ 3.80 |  |
| g45 | 0.10 | CLOSING_START | B | B:track_009 | B:e34 @ 3.80 | active_at_first_observation=True |
| g46 | 0.15 | EGO_PATH_EXIT | B | B:track_005 | B:e35 @ 3.85 |  |
| g47 | 0.15 | TRACK_APPEARED_LEFT | B | B:track_013 | B:e36 @ 3.85 |  |
| g48 | 0.15 | TRACK_APPEARED_LEFT | B | B:track_014 | B:e37 @ 3.85 |  |
| g49 | 0.15 | EGO_PATH_ENTRY | B | B:track_002 | B:e38 @ 3.85 |  |
| g50 | 0.15 | CLOSING_START | B | B:track_008 | B:e39 @ 3.85 |  |
| g51 | 0.20 | EGO_PATH_EXIT | A | B | A:e13 @ 3.90 |  |
| g52 | 0.20 | EGO_PATH_EXIT | B | B:track_002 | B:e40 @ 3.90 |  |
| g53 | 0.20 | TRACK_APPEARED_LEFT | B | B:track_015 | B:e41 @ 3.90 |  |
| g54 | 0.20 | TRACK_APPEARED_LEFT | B | B:track_016 | B:e42 @ 3.90 |  |
| g55 | 0.20 | TRACK_APPEARED_LEFT | B | B:track_017 | B:e43 @ 3.90 |  |
| g56 | 0.20 | EGO_PATH_ENTRY | B | B:track_018 | B:e44 @ 3.90 |  |
| g57 | 0.20 | CLOSING_START | B | B:track_013 | B:e45 @ 3.90 |  |
| g58 | 0.20 | CLOSING_START | B | B:track_014 | B:e46 @ 3.90 |  |
| g59 | 0.20 | CLOSING_START | B | B:track_015 | B:e47 @ 3.90 | active_at_first_observation=True |
| g60 | 0.20 | CRITICAL_TTC_START | B | B:track_015 | B:e48 @ 3.90 | active_at_first_observation=True |
| g61 | 0.25 | EGO_PATH_EXIT | B | B:track_018 | B:e49 @ 3.95 |  |
| g62 | 0.25 | CLOSING_START | B | B:track_016 | B:e50 @ 3.95 |  |
| g63 | 0.25 | CLOSING_START | B | B:track_017 | B:e51 @ 3.95 |  |
| g64 | 0.25 | TRACK_LOST | B | B:track_006 | B:e52 @ 3.95 |  |
| g65 | 0.30 | CLOSING_END | B | B:track_002 | B:e53 @ 4.00 |  |
| g66 | 0.30 | CLOSING_END | B | B:track_005 | B:e54 @ 4.00 |  |
| g67 | 0.30 | TRACK_APPEARED_LEFT | B | B:track_019 | B:e55 @ 4.00 |  |
| g68 | 0.30 | TRACK_LOST | B | B:track_011 | B:e56 @ 4.00 |  |
| g69 | 0.35 | CLOSING_END | B | B:track_004 | B:e57 @ 4.05 |  |
| g70 | 0.35 | CLOSING_END | B | B:track_007 | B:e58 @ 4.05 |  |
| g71 | 0.35 | CLOSING_END | B | B:track_012 | B:e59 @ 4.05 |  |
| g72 | 0.35 | EGO_PATH_ENTRY | B | B:track_009 | B:e60 @ 4.05 |  |
| g73 | 0.35 | TRACK_LOST | A | B | A:e14 @ 4.05 |  |
| g74 | 0.35 | TRACK_LOST | B | B:track_003 | B:e61 @ 4.05 |  |
| g75 | 0.40 | CLOSING_END | B | B:track_009 | B:e62 @ 4.10 |  |
| g76 | 0.40 | CLOSING_END | B | B:track_018 | B:e63 @ 4.10 |  |
| g77 | 0.40 | EGO_PATH_EXIT | B | B:track_009 | B:e64 @ 4.10 |  |
| g78 | 0.40 | EGO_PATH_ENTRY | B | B:track_010 | B:e65 @ 4.10 |  |
| g79 | 0.45 | CLOSING_END | B | B:track_008 | B:e66 @ 4.15 |  |
| g80 | 0.45 | EGO_PATH_EXIT | B | B:track_010 | B:e67 @ 4.15 |  |
| g81 | 0.45 | EGO_PATH_ENTRY | B | B:track_008 | B:e68 @ 4.15 |  |
| g82 | 0.45 | TRACK_LOST | B | B:track_005 | B:e69 @ 4.15 |  |
| g83 | 0.50 | CRITICAL_TTC_END | B | B:track_015 | B:e70 @ 4.20 |  |
| g84 | 0.55 | CLOSING_END | B | B:track_013 | B:e71 @ 4.25 |  |
| g85 | 0.55 | CLOSING_END | B | B:track_015 | B:e72 @ 4.25 |  |
| g86 | 0.55 | EGO_PATH_EXIT | B | B:track_008 | B:e73 @ 4.25 |  |
| g87 | 0.55 | EGO_PATH_ENTRY | B | B:track_013 | B:e74 @ 4.25 |  |
| g88 | 0.55 | TRACK_LOST | B | B:track_018 | B:e75 @ 4.25 |  |
| g89 | 0.60 | CLOSING_END | B | B:track_014 | B:e76 @ 4.30 |  |
| g90 | 0.60 | CLOSING_END | B | B:track_016 | B:e77 @ 4.30 |  |
| g91 | 0.60 | CLOSING_END | B | B:track_017 | B:e78 @ 4.30 |  |
| g92 | 0.60 | MOVING_END | B | - | B:e79 @ 4.30 |  |
| g93 | 0.60 | STOP_START | B | - | B:e80 @ 4.30 |  |
| g94 | 0.85 | MOVING_END | A | - | A:e15 @ 4.55 |  |
| g95 | 0.85 | STOP_START | A | - | A:e16 @ 4.55 |  |
| g96 | 1.25 | EGO_PATH_ENTRY | B | B:track_008 | B:e81 @ 4.95 |  |
| g97 | 1.40 | EGO_PATH_EXIT | B | B:track_013 | B:e82 @ 5.10 |  |
| g98 | 3.75 | EGO_PATH_ENTRY | B | B:track_013 | B:e83 @ 7.45 |  |
| g99 | 10.70 | TRACK_LOST | B | B:track_004 | B:e84 @ 14.40 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g12 --PRECEDES--> g15
    g12 --PRECEDES--> g16
    g12 --PRECEDES--> g17
    g12 --PRECEDES--> g18
    g12 --PRECEDES--> g19
    g12 --PRECEDES--> g20
    g12 --PRECEDES--> g21
    g12 --PRECEDES--> g22
    g12 --PRECEDES--> g23
    g12 --PRECEDES--> g24
    g12 --PRECEDES--> g25
    g12 --PRECEDES--> g26
    g12 --PRECEDES--> g27
    g12 --PRECEDES--> g28
    g13 --PRECEDES--> g29
    g13 --PRECEDES--> g30
    g13 --PRECEDES--> g31
    g13 --PRECEDES--> g32
    g13 --PRECEDES--> g33
    g13 --PRECEDES--> g34
    g13 --PRECEDES--> g35
    g13 --PRECEDES--> g36
    g13 --PRECEDES--> g37
    g13 --PRECEDES--> g38
    g14 --PRECEDES--> g29
    g14 --PRECEDES--> g30
    g14 --PRECEDES--> g31
    g14 --PRECEDES--> g32
    g14 --PRECEDES--> g33
    g14 --PRECEDES--> g34
    g14 --PRECEDES--> g35
    g14 --PRECEDES--> g36
    g14 --PRECEDES--> g37
    g14 --PRECEDES--> g38
    g15 --PRECEDES--> g29
    g15 --PRECEDES--> g30
    g15 --PRECEDES--> g31
    g15 --PRECEDES--> g32
    g15 --PRECEDES--> g33
    g15 --PRECEDES--> g34
    g15 --PRECEDES--> g35
    g15 --PRECEDES--> g36
    g15 --PRECEDES--> g37
    g15 --PRECEDES--> g38
    g16 --PRECEDES--> g29
    g16 --PRECEDES--> g30
    g16 --PRECEDES--> g31
    g16 --PRECEDES--> g32
    g16 --PRECEDES--> g33
    g16 --PRECEDES--> g34
    g16 --PRECEDES--> g35
    g16 --PRECEDES--> g36
    g16 --PRECEDES--> g37
    g16 --PRECEDES--> g38
    g17 --PRECEDES--> g29
    g17 --PRECEDES--> g30
    g17 --PRECEDES--> g31
    g17 --PRECEDES--> g32
    g17 --PRECEDES--> g33
    g17 --PRECEDES--> g34
    g17 --PRECEDES--> g35
    g17 --PRECEDES--> g36
    g17 --PRECEDES--> g37
    g17 --PRECEDES--> g38
    g18 --PRECEDES--> g29
    g18 --PRECEDES--> g30
    g18 --PRECEDES--> g31
    g18 --PRECEDES--> g32
    g18 --PRECEDES--> g33
    g18 --PRECEDES--> g34
    g18 --PRECEDES--> g35
    g18 --PRECEDES--> g36
    g18 --PRECEDES--> g37
    g18 --PRECEDES--> g38
    g19 --PRECEDES--> g29
    g19 --PRECEDES--> g30
    g19 --PRECEDES--> g31
    g19 --PRECEDES--> g32
    g19 --PRECEDES--> g33
    g19 --PRECEDES--> g34
    g19 --PRECEDES--> g35
    g19 --PRECEDES--> g36
    g19 --PRECEDES--> g37
    g19 --PRECEDES--> g38
    g20 --PRECEDES--> g29
    g20 --PRECEDES--> g30
    g20 --PRECEDES--> g31
    g20 --PRECEDES--> g32
    g20 --PRECEDES--> g33
    g20 --PRECEDES--> g34
    g20 --PRECEDES--> g35
    g20 --PRECEDES--> g36
    g20 --PRECEDES--> g37
    g20 --PRECEDES--> g38
    g21 --PRECEDES--> g29
    g21 --PRECEDES--> g30
    g21 --PRECEDES--> g31
    g21 --PRECEDES--> g32
    g21 --PRECEDES--> g33
    g21 --PRECEDES--> g34
    g21 --PRECEDES--> g35
    g21 --PRECEDES--> g36
    g21 --PRECEDES--> g37
    g21 --PRECEDES--> g38
    g22 --PRECEDES--> g29
    g22 --PRECEDES--> g30
    g22 --PRECEDES--> g31
    g22 --PRECEDES--> g32
    g22 --PRECEDES--> g33
    g22 --PRECEDES--> g34
    g22 --PRECEDES--> g35
    g22 --PRECEDES--> g36
    g22 --PRECEDES--> g37
    g22 --PRECEDES--> g38
    g23 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g23 --PRECEDES--> g31
    g23 --PRECEDES--> g32
    g23 --PRECEDES--> g33
    g23 --PRECEDES--> g34
    g23 --PRECEDES--> g35
    g23 --PRECEDES--> g36
    g23 --PRECEDES--> g37
    g23 --PRECEDES--> g38
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g24 --PRECEDES--> g31
    g24 --PRECEDES--> g32
    g24 --PRECEDES--> g33
    g24 --PRECEDES--> g34
    g24 --PRECEDES--> g35
    g24 --PRECEDES--> g36
    g24 --PRECEDES--> g37
    g24 --PRECEDES--> g38
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g25 --PRECEDES--> g32
    g25 --PRECEDES--> g33
    g25 --PRECEDES--> g34
    g25 --PRECEDES--> g35
    g25 --PRECEDES--> g36
    g25 --PRECEDES--> g37
    g25 --PRECEDES--> g38
    g26 --PRECEDES--> g29
    g26 --PRECEDES--> g30
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g26 --PRECEDES--> g33
    g26 --PRECEDES--> g34
    g26 --PRECEDES--> g35
    g26 --PRECEDES--> g36
    g26 --PRECEDES--> g37
    g26 --PRECEDES--> g38
    g27 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g27 --PRECEDES--> g35
    g27 --PRECEDES--> g36
    g27 --PRECEDES--> g37
    g27 --PRECEDES--> g38
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g28 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g28 --PRECEDES--> g36
    g28 --PRECEDES--> g37
    g28 --PRECEDES--> g38
    g29 --PRECEDES--> g39
    g29 --PRECEDES--> g40
    g29 --PRECEDES--> g41
    g29 --PRECEDES--> g42
    g29 --PRECEDES--> g43
    g29 --PRECEDES--> g44
    g29 --PRECEDES--> g45
    g30 --PRECEDES--> g39
    g30 --PRECEDES--> g40
    g30 --PRECEDES--> g41
    g30 --PRECEDES--> g42
    g30 --PRECEDES--> g43
    g30 --PRECEDES--> g44
    g30 --PRECEDES--> g45
    g31 --PRECEDES--> g39
    g31 --PRECEDES--> g40
    g31 --PRECEDES--> g41
    g31 --PRECEDES--> g42
    g31 --PRECEDES--> g43
    g31 --PRECEDES--> g44
    g31 --PRECEDES--> g45
    g32 --PRECEDES--> g39
    g32 --PRECEDES--> g40
    g32 --PRECEDES--> g41
    g32 --PRECEDES--> g42
    g32 --PRECEDES--> g43
    g32 --PRECEDES--> g44
    g32 --PRECEDES--> g45
    g33 --PRECEDES--> g39
    g33 --PRECEDES--> g40
    g33 --PRECEDES--> g41
    g33 --PRECEDES--> g42
    g33 --PRECEDES--> g43
    g33 --PRECEDES--> g44
    g33 --PRECEDES--> g45
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g34 --PRECEDES--> g41
    g34 --PRECEDES--> g42
    g34 --PRECEDES--> g43
    g34 --PRECEDES--> g44
    g34 --PRECEDES--> g45
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g35 --PRECEDES--> g43
    g35 --PRECEDES--> g44
    g35 --PRECEDES--> g45
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g36 --PRECEDES--> g43
    g36 --PRECEDES--> g44
    g36 --PRECEDES--> g45
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g37 --PRECEDES--> g44
    g37 --PRECEDES--> g45
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g38 --PRECEDES--> g44
    g38 --PRECEDES--> g45
    g39 --PRECEDES--> g46
    g39 --PRECEDES--> g47
    g39 --PRECEDES--> g48
    g39 --PRECEDES--> g49
    g39 --PRECEDES--> g50
    g40 --PRECEDES--> g46
    g40 --PRECEDES--> g47
    g40 --PRECEDES--> g48
    g40 --PRECEDES--> g49
    g40 --PRECEDES--> g50
    g41 --PRECEDES--> g46
    g41 --PRECEDES--> g47
    g41 --PRECEDES--> g48
    g41 --PRECEDES--> g49
    g41 --PRECEDES--> g50
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g42 --PRECEDES--> g48
    g42 --PRECEDES--> g49
    g42 --PRECEDES--> g50
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g43 --PRECEDES--> g50
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g44 --PRECEDES--> g50
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g45 --PRECEDES--> g50
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
    g50 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g50 --PRECEDES--> g56
    g50 --PRECEDES--> g57
    g50 --PRECEDES--> g58
    g50 --PRECEDES--> g59
    g50 --PRECEDES--> g60
    g51 --PRECEDES--> g61
    g51 --PRECEDES--> g62
    g51 --PRECEDES--> g63
    g51 --PRECEDES--> g64
    g52 --PRECEDES--> g61
    g52 --PRECEDES--> g62
    g52 --PRECEDES--> g63
    g52 --PRECEDES--> g64
    g53 --PRECEDES--> g61
    g53 --PRECEDES--> g62
    g53 --PRECEDES--> g63
    g53 --PRECEDES--> g64
    g54 --PRECEDES--> g61
    g54 --PRECEDES--> g62
    g54 --PRECEDES--> g63
    g54 --PRECEDES--> g64
    g55 --PRECEDES--> g61
    g55 --PRECEDES--> g62
    g55 --PRECEDES--> g63
    g55 --PRECEDES--> g64
    g56 --PRECEDES--> g61
    g56 --PRECEDES--> g62
    g56 --PRECEDES--> g63
    g56 --PRECEDES--> g64
    g57 --PRECEDES--> g61
    g57 --PRECEDES--> g62
    g57 --PRECEDES--> g63
    g57 --PRECEDES--> g64
    g58 --PRECEDES--> g61
    g58 --PRECEDES--> g62
    g58 --PRECEDES--> g63
    g58 --PRECEDES--> g64
    g59 --PRECEDES--> g61
    g59 --PRECEDES--> g62
    g59 --PRECEDES--> g63
    g59 --PRECEDES--> g64
    g60 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g60 --PRECEDES--> g63
    g60 --PRECEDES--> g64
    g61 --PRECEDES--> g65
    g61 --PRECEDES--> g66
    g61 --PRECEDES--> g67
    g61 --PRECEDES--> g68
    g62 --PRECEDES--> g65
    g62 --PRECEDES--> g66
    g62 --PRECEDES--> g67
    g62 --PRECEDES--> g68
    g63 --PRECEDES--> g65
    g63 --PRECEDES--> g66
    g63 --PRECEDES--> g67
    g63 --PRECEDES--> g68
    g64 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g64 --PRECEDES--> g67
    g64 --PRECEDES--> g68
    g65 --PRECEDES--> g69
    g65 --PRECEDES--> g70
    g65 --PRECEDES--> g71
    g65 --PRECEDES--> g72
    g65 --PRECEDES--> g73
    g65 --PRECEDES--> g74
    g66 --PRECEDES--> g69
    g66 --PRECEDES--> g70
    g66 --PRECEDES--> g71
    g66 --PRECEDES--> g72
    g66 --PRECEDES--> g73
    g66 --PRECEDES--> g74
    g67 --PRECEDES--> g69
    g67 --PRECEDES--> g70
    g67 --PRECEDES--> g71
    g67 --PRECEDES--> g72
    g67 --PRECEDES--> g73
    g67 --PRECEDES--> g74
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g68 --PRECEDES--> g71
    g68 --PRECEDES--> g72
    g68 --PRECEDES--> g73
    g68 --PRECEDES--> g74
    g69 --PRECEDES--> g75
    g69 --PRECEDES--> g76
    g69 --PRECEDES--> g77
    g69 --PRECEDES--> g78
    g70 --PRECEDES--> g75
    g70 --PRECEDES--> g76
    g70 --PRECEDES--> g77
    g70 --PRECEDES--> g78
    g71 --PRECEDES--> g75
    g71 --PRECEDES--> g76
    g71 --PRECEDES--> g77
    g71 --PRECEDES--> g78
    g72 --PRECEDES--> g75
    g72 --PRECEDES--> g76
    g72 --PRECEDES--> g77
    g72 --PRECEDES--> g78
    g73 --PRECEDES--> g75
    g73 --PRECEDES--> g76
    g73 --PRECEDES--> g77
    g73 --PRECEDES--> g78
    g74 --PRECEDES--> g75
    g74 --PRECEDES--> g76
    g74 --PRECEDES--> g77
    g74 --PRECEDES--> g78
    g75 --PRECEDES--> g79
    g75 --PRECEDES--> g80
    g75 --PRECEDES--> g81
    g75 --PRECEDES--> g82
    g76 --PRECEDES--> g79
    g76 --PRECEDES--> g80
    g76 --PRECEDES--> g81
    g76 --PRECEDES--> g82
    g77 --PRECEDES--> g79
    g77 --PRECEDES--> g80
    g77 --PRECEDES--> g81
    g77 --PRECEDES--> g82
    g78 --PRECEDES--> g79
    g78 --PRECEDES--> g80
    g78 --PRECEDES--> g81
    g78 --PRECEDES--> g82
    g79 --PRECEDES--> g83
    g80 --PRECEDES--> g83
    g81 --PRECEDES--> g83
    g82 --PRECEDES--> g83
    g83 --PRECEDES--> g84
    g83 --PRECEDES--> g85
    g83 --PRECEDES--> g86
    g83 --PRECEDES--> g87
    g83 --PRECEDES--> g88
    g84 --PRECEDES--> g89
    g84 --PRECEDES--> g90
    g84 --PRECEDES--> g91
    g84 --PRECEDES--> g92
    g84 --PRECEDES--> g93
    g85 --PRECEDES--> g89
    g85 --PRECEDES--> g90
    g85 --PRECEDES--> g91
    g85 --PRECEDES--> g92
    g85 --PRECEDES--> g93
    g86 --PRECEDES--> g89
    g86 --PRECEDES--> g90
    g86 --PRECEDES--> g91
    g86 --PRECEDES--> g92
    g86 --PRECEDES--> g93
    g87 --PRECEDES--> g89
    g87 --PRECEDES--> g90
    g87 --PRECEDES--> g91
    g87 --PRECEDES--> g92
    g87 --PRECEDES--> g93
    g88 --PRECEDES--> g89
    g88 --PRECEDES--> g90
    g88 --PRECEDES--> g91
    g88 --PRECEDES--> g92
    g88 --PRECEDES--> g93
    g89 --PRECEDES--> g94
    g89 --PRECEDES--> g95
    g90 --PRECEDES--> g94
    g90 --PRECEDES--> g95
    g91 --PRECEDES--> g94
    g91 --PRECEDES--> g95
    g92 --PRECEDES--> g94
    g92 --PRECEDES--> g95
    g93 --PRECEDES--> g94
    g93 --PRECEDES--> g95
    g94 --PRECEDES--> g96
    g95 --PRECEDES--> g96
    g96 --PRECEDES--> g97
    g97 --PRECEDES--> g98
    g98 --PRECEDES--> g99
    g05 --SAME_TRACK--> g06
    g05 --SAME_TRACK--> g09
    g05 --SAME_TRACK--> g12
    g05 --SAME_TRACK--> g14
    g05 --SAME_TRACK--> g15
    g05 --SAME_TRACK--> g51
    g05 --SAME_TRACK--> g73
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g10
    g04 --SAME_TRACK--> g11
    g18 --SAME_TRACK--> g24
    g20 --SAME_TRACK--> g25
    g21 --SAME_TRACK--> g26
    g22 --SAME_TRACK--> g27
    g23 --SAME_TRACK--> g28
    g19 --SAME_TRACK--> g37
    g35 --SAME_TRACK--> g38
    g19 --SAME_TRACK--> g39
    g21 --SAME_TRACK--> g44
    g41 --SAME_TRACK--> g45
    g21 --SAME_TRACK--> g46
    g18 --SAME_TRACK--> g49
    g40 --SAME_TRACK--> g50
    g18 --SAME_TRACK--> g52
    g23 --SAME_TRACK--> g56
    g47 --SAME_TRACK--> g57
    g48 --SAME_TRACK--> g58
    g53 --SAME_TRACK--> g59
    g53 --SAME_TRACK--> g60
    g23 --SAME_TRACK--> g61
    g54 --SAME_TRACK--> g62
    g55 --SAME_TRACK--> g63
    g36 --SAME_TRACK--> g64
    g18 --SAME_TRACK--> g65
    g21 --SAME_TRACK--> g66
    g43 --SAME_TRACK--> g68
    g20 --SAME_TRACK--> g69
    g22 --SAME_TRACK--> g70
    g35 --SAME_TRACK--> g71
    g41 --SAME_TRACK--> g72
    g19 --SAME_TRACK--> g74
    g41 --SAME_TRACK--> g75
    g23 --SAME_TRACK--> g76
    g41 --SAME_TRACK--> g77
    g42 --SAME_TRACK--> g78
    g40 --SAME_TRACK--> g79
    g42 --SAME_TRACK--> g80
    g40 --SAME_TRACK--> g81
    g21 --SAME_TRACK--> g82
    g53 --SAME_TRACK--> g83
    g47 --SAME_TRACK--> g84
    g53 --SAME_TRACK--> g85
    g40 --SAME_TRACK--> g86
    g47 --SAME_TRACK--> g87
    g23 --SAME_TRACK--> g88
    g48 --SAME_TRACK--> g89
    g54 --SAME_TRACK--> g90
    g55 --SAME_TRACK--> g91
    g40 --SAME_TRACK--> g96
    g47 --SAME_TRACK--> g97
    g47 --SAME_TRACK--> g98
    g20 --SAME_TRACK--> g99
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.70 | MOVING_START(A); MOVING_START(B) |
| -2.85 | STRONG_THROTTLE_START(B) |
| -2.50 | TRACK_APPEARED_LEFT(B,B:track_001); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,B:track_001) |
| -2.10 | STRONG_THROTTLE_END(B) |
| -2.05 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_001) |
| -0.35 | TRACK_LOST(B,B:track_001) |
| -0.25 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_018); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_018) |
| +0.05 | STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED_LEFT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_006); EGO_PATH_ENTRY(B,B:track_003); CLOSING_START(B,B:track_012) |
| +0.10 | EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_008); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_RIGHT(B,B:track_011); EGO_PATH_ENTRY(B,B:track_005); CLOSING_START(B,B:track_009) |
| +0.15 | EGO_PATH_EXIT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_LEFT(B,B:track_014); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_008) |
| +0.20 | EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_017); EGO_PATH_ENTRY(B,B:track_018); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); CRITICAL_TTC_START(B,B:track_015) |
| +0.25 | EGO_PATH_EXIT(B,B:track_018); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_017); TRACK_LOST(B,B:track_006) |
| +0.30 | CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_LOST(B,B:track_011) |
| +0.35 | CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_012); EGO_PATH_ENTRY(B,B:track_009); TRACK_LOST(A,B); TRACK_LOST(B,B:track_003) |
| +0.40 | CLOSING_END(B,B:track_009); CLOSING_END(B,B:track_018); EGO_PATH_EXIT(B,B:track_009); EGO_PATH_ENTRY(B,B:track_010) |
| +0.45 | CLOSING_END(B,B:track_008); EGO_PATH_EXIT(B,B:track_010); EGO_PATH_ENTRY(B,B:track_008); TRACK_LOST(B,B:track_005) |
| +0.50 | CRITICAL_TTC_END(B,B:track_015) |
| +0.55 | CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_015); EGO_PATH_EXIT(B,B:track_008); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_018) |
| +0.60 | CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_016); CLOSING_END(B,B:track_017); MOVING_END(B); STOP_START(B) |
| +0.85 | MOVING_END(A); STOP_START(A) |
| +1.25 | EGO_PATH_ENTRY(B,B:track_008) |
| +1.40 | EGO_PATH_EXIT(B,B:track_013) |
| +3.75 | EGO_PATH_ENTRY(B,B:track_013) |
| +10.70 | TRACK_LOST(B,B:track_004) |

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.70 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -3.70 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -2.85 | B | g03 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| -2.50 | B | g04 TRACK_APPEARED_LEFT(B,B:track_001) (B:e03)<br>g07 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| -2.50 | A | g05 TRACK_APPEARED_RIGHT(A,B) (A:e02)<br>g06 CLOSING_START(A,B) (A:e03) | ego: MOVING |
| -2.10 | B | g08 STRONG_THROTTLE_END(B) (B:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING |
| -2.05 | A | g09 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.05 | B | g10 CRITICAL_TTC_START(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: CLOSING |
| -0.35 | B | g11 TRACK_LOST(B,B:track_001) (B:e07) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -0.25 | A | g12 EGO_PATH_ENTRY(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g13 COLLISION(A,B) (A:e06)<br>g14 CRITICAL_TTC_END(A,B) (A:e07)<br>g15 CLOSING_END(A,B) (A:e08)<br>g16 STRONG_THROTTLE_START(A) (A:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g13 COLLISION(A,B) (B:e08)<br>g17 STRONG_THROTTLE_START(B) (B:e09)<br>g18 TRACK_APPEARED_LEFT(B,B:track_002) (B:e10)<br>g19 TRACK_APPEARED_LEFT(B,B:track_003) (B:e11)<br>g20 TRACK_APPEARED_LEFT(B,B:track_004) (B:e12)<br>g21 TRACK_APPEARED_LEFT(B,B:track_005) (B:e13)<br>g22 TRACK_APPEARED_LEFT(B,B:track_007) (B:e14)<br>g23 TRACK_APPEARED_LEFT(B,B:track_018) (B:e15)<br>g24 CLOSING_START(B,B:track_002) (B:e16)<br>g25 CLOSING_START(B,B:track_004) (B:e17)<br>g26 CLOSING_START(B,B:track_005) (B:e18)<br>g27 CLOSING_START(B,B:track_007) (B:e19)<br>g28 CLOSING_START(B,B:track_018) (B:e20) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.05 | A | g29 STRONG_THROTTLE_END(A) (A:e10)<br>g31 BRAKE_START(A) (A:e11)<br>g33 HARD_BRAKE_START(A) (A:e12) | ego: MOVING, STRONG_THROTTLE<br>track_001: IN_EGO_PATH |
| +0.05 | B | g30 STRONG_THROTTLE_END(B) (B:e21)<br>g32 BRAKE_START(B) (B:e22)<br>g34 HARD_BRAKE_START(B) (B:e23)<br>g35 TRACK_APPEARED_LEFT(B,B:track_012) (B:e24)<br>g36 TRACK_APPEARED_RIGHT(B,B:track_006) (B:e25)<br>g37 EGO_PATH_ENTRY(B,B:track_003) (B:e26)<br>g38 CLOSING_START(B,B:track_012) (B:e27) | ego: MOVING, STRONG_THROTTLE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.10 | B | g39 EGO_PATH_EXIT(B,B:track_003) (B:e28)<br>g40 TRACK_APPEARED_LEFT(B,B:track_008) (B:e29)<br>g41 TRACK_APPEARED_LEFT(B,B:track_009) (B:e30)<br>g42 TRACK_APPEARED_LEFT(B,B:track_010) (B:e31)<br>g43 TRACK_APPEARED_RIGHT(B,B:track_011) (B:e32)<br>g44 EGO_PATH_ENTRY(B,B:track_005) (B:e33)<br>g45 CLOSING_START(B,B:track_009) (B:e34) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: IN_EGO_PATH, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_012: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.15 | B | g46 EGO_PATH_EXIT(B,B:track_005) (B:e35)<br>g47 TRACK_APPEARED_LEFT(B,B:track_013) (B:e36)<br>g48 TRACK_APPEARED_LEFT(B,B:track_014) (B:e37)<br>g49 EGO_PATH_ENTRY(B,B:track_002) (B:e38)<br>g50 CLOSING_START(B,B:track_008) (B:e39) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: no active state<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.20 | A | g51 EGO_PATH_EXIT(A,B) (A:e13) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH |
| +0.20 | B | g52 EGO_PATH_EXIT(B,B:track_002) (B:e40)<br>g53 TRACK_APPEARED_LEFT(B,B:track_015) (B:e41)<br>g54 TRACK_APPEARED_LEFT(B,B:track_016) (B:e42)<br>g55 TRACK_APPEARED_LEFT(B,B:track_017) (B:e43)<br>g56 EGO_PATH_ENTRY(B,B:track_018) (B:e44)<br>g57 CLOSING_START(B,B:track_013) (B:e45)<br>g58 CLOSING_START(B,B:track_014) (B:e46)<br>g59 CLOSING_START(B,B:track_015) (B:e47)<br>g60 CRITICAL_TTC_START(B,B:track_015) (B:e48) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: no active state<br>track_014: no active state<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.25 | B | g61 EGO_PATH_EXIT(B,B:track_018) (B:e49)<br>g62 CLOSING_START(B,B:track_016) (B:e50)<br>g63 CLOSING_START(B,B:track_017) (B:e51)<br>g64 TRACK_LOST(B,B:track_006) (B:e52) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: no active state<br>track_017: no active state<br>track_018: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.30 | B | g65 CLOSING_END(B,B:track_002) (B:e53)<br>g66 CLOSING_END(B,B:track_005) (B:e54)<br>g67 TRACK_APPEARED_LEFT(B,B:track_019) (B:e55)<br>g68 TRACK_LOST(B,B:track_011) (B:e56) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001, track_006 |
| +0.35 | B | g69 CLOSING_END(B,B:track_004) (B:e57)<br>g70 CLOSING_END(B,B:track_007) (B:e58)<br>g71 CLOSING_END(B,B:track_012) (B:e59)<br>g72 EGO_PATH_ENTRY(B,B:track_009) (B:e60)<br>g74 TRACK_LOST(B,B:track_003) (B:e61) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: no active state<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_006, track_011 |
| +0.35 | A | g73 TRACK_LOST(A,B) (A:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: no active state |
| +0.40 | B | g75 CLOSING_END(B,B:track_009) (B:e62)<br>g76 CLOSING_END(B,B:track_018) (B:e63)<br>g77 EGO_PATH_EXIT(B,B:track_009) (B:e64)<br>g78 EGO_PATH_ENTRY(B,B:track_010) (B:e65) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track_009: CLOSING, IN_EGO_PATH<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_006, track_011 |
| +0.45 | B | g79 CLOSING_END(B,B:track_008) (B:e66)<br>g80 EGO_PATH_EXIT(B,B:track_010) (B:e67)<br>g81 EGO_PATH_ENTRY(B,B:track_008) (B:e68)<br>g82 TRACK_LOST(B,B:track_005) (B:e69) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track_009: no active state<br>track_010: IN_EGO_PATH<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_006, track_011 |
| +0.50 | B | g83 CRITICAL_TTC_END(B,B:track_015) (B:e70) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011 |
| +0.55 | B | g84 CLOSING_END(B,B:track_013) (B:e71)<br>g85 CLOSING_END(B,B:track_015) (B:e72)<br>g86 EGO_PATH_EXIT(B,B:track_008) (B:e73)<br>g87 EGO_PATH_ENTRY(B,B:track_013) (B:e74)<br>g88 TRACK_LOST(B,B:track_018) (B:e75) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011 |
| +0.60 | B | g89 CLOSING_END(B,B:track_014) (B:e76)<br>g90 CLOSING_END(B,B:track_016) (B:e77)<br>g91 CLOSING_END(B,B:track_017) (B:e78)<br>g92 MOVING_END(B) (B:e79)<br>g93 STOP_START(B) (B:e80) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +0.85 | A | g94 MOVING_END(A) (A:e15)<br>g95 STOP_START(A) (A:e16) | ego: MOVING, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001 |
| +1.25 | B | g96 EGO_PATH_ENTRY(B,B:track_008) (B:e81) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +1.40 | B | g97 EGO_PATH_EXIT(B,B:track_013) (B:e82) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +3.75 | B | g98 EGO_PATH_ENTRY(B,B:track_013) (B:e83) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +10.70 | B | g99 TRACK_LOST(B,B:track_004) (B:e84) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |

## Plain-language reading

- 3.70 s before the matched collision, A started moving (already the case when first observed).
- 3.70 s before the matched collision, B started moving (already the case when first observed).
- 2.85 s before the matched collision, B started applying strong throttle.
- 2.50 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared on its left.
- 2.50 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 2.50 s before the matched collision, A observed B start closing in (already the case when first observed).
- 2.50 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.10 s before the matched collision, B stopped applying strong throttle.
- 2.05 s before the matched collision, A's time-to-contact with B became critical.
- 2.05 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 0.35 s before the matched collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- 0.25 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6116, B: 6116 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- At the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- At the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- At the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its left.
- At the matched collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- At the matched collision, B's radar started tracking unidentified object B:track_018, which appeared on its left.
- At the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- At the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- At the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- At the matched collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- At the matched collision, B observed unidentified object B:track_018 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_012, which appeared on its left.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_006, which appeared on its right.
- 0.05 s after the matched collision, B observed unidentified object B:track_003 enter its forward path corridor.
- 0.05 s after the matched collision, B observed unidentified object B:track_012 start closing in (already the case when first observed).
- 0.10 s after the matched collision, B observed unidentified object B:track_003 leave its forward path corridor.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_008, which appeared on its left.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_009, which appeared on its left.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_010, which appeared on its left.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_011, which appeared on its right.
- 0.10 s after the matched collision, B observed unidentified object B:track_005 enter its forward path corridor.
- 0.10 s after the matched collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 0.15 s after the matched collision, B observed unidentified object B:track_005 leave its forward path corridor.
- 0.15 s after the matched collision, B's radar started tracking unidentified object B:track_013, which appeared on its left.
- 0.15 s after the matched collision, B's radar started tracking unidentified object B:track_014, which appeared on its left.
- 0.15 s after the matched collision, B observed unidentified object B:track_002 enter its forward path corridor.
- 0.15 s after the matched collision, B observed unidentified object B:track_008 start closing in.
- 0.20 s after the matched collision, A observed B leave its forward path corridor.
- 0.20 s after the matched collision, B observed unidentified object B:track_002 leave its forward path corridor.
- 0.20 s after the matched collision, B's radar started tracking unidentified object B:track_015, which appeared on its left.
- 0.20 s after the matched collision, B's radar started tracking unidentified object B:track_016, which appeared on its left.
- 0.20 s after the matched collision, B's radar started tracking unidentified object B:track_017, which appeared on its left.
- 0.20 s after the matched collision, B observed unidentified object B:track_018 enter its forward path corridor.
- 0.20 s after the matched collision, B observed unidentified object B:track_013 start closing in.
- 0.20 s after the matched collision, B observed unidentified object B:track_014 start closing in.
- 0.20 s after the matched collision, B observed unidentified object B:track_015 start closing in (already the case when first observed).
- 0.20 s after the matched collision, B's time-to-contact with unidentified object B:track_015 became critical (already the case when first observed).
- 0.25 s after the matched collision, B observed unidentified object B:track_018 leave its forward path corridor.
- 0.25 s after the matched collision, B observed unidentified object B:track_016 start closing in.
- 0.25 s after the matched collision, B observed unidentified object B:track_017 start closing in.
- 0.25 s after the matched collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- 0.30 s after the matched collision, B observed unidentified object B:track_002 stop closing in.
- 0.30 s after the matched collision, B observed unidentified object B:track_005 stop closing in.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_019, which appeared on its left.
- 0.30 s after the matched collision, B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the matched collision, B observed unidentified object B:track_004 stop closing in.
- 0.35 s after the matched collision, B observed unidentified object B:track_007 stop closing in.
- 0.35 s after the matched collision, B observed unidentified object B:track_012 stop closing in.
- 0.35 s after the matched collision, B observed unidentified object B:track_009 enter its forward path corridor.
- 0.35 s after the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.35 s after the matched collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.40 s after the matched collision, B observed unidentified object B:track_009 stop closing in.
- 0.40 s after the matched collision, B observed unidentified object B:track_018 stop closing in.
- 0.40 s after the matched collision, B observed unidentified object B:track_009 leave its forward path corridor.
- 0.40 s after the matched collision, B observed unidentified object B:track_010 enter its forward path corridor.
- 0.45 s after the matched collision, B observed unidentified object B:track_008 stop closing in.
- 0.45 s after the matched collision, B observed unidentified object B:track_010 leave its forward path corridor.
- 0.45 s after the matched collision, B observed unidentified object B:track_008 enter its forward path corridor.
- 0.45 s after the matched collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.50 s after the matched collision, B's time-to-contact with unidentified object B:track_015 stopped being critical.
- 0.55 s after the matched collision, B observed unidentified object B:track_013 stop closing in.
- 0.55 s after the matched collision, B observed unidentified object B:track_015 stop closing in.
- 0.55 s after the matched collision, B observed unidentified object B:track_008 leave its forward path corridor.
- 0.55 s after the matched collision, B observed unidentified object B:track_013 enter its forward path corridor.
- 0.55 s after the matched collision, B's radar lost unidentified object B:track_018 (its states are UNKNOWN from then on, not ended).
- 0.60 s after the matched collision, B observed unidentified object B:track_014 stop closing in.
- 0.60 s after the matched collision, B observed unidentified object B:track_016 stop closing in.
- 0.60 s after the matched collision, B observed unidentified object B:track_017 stop closing in.
- 0.60 s after the matched collision, B stopped moving.
- 0.60 s after the matched collision, B came to a stop.
- 0.85 s after the matched collision, A stopped moving.
- 0.85 s after the matched collision, A came to a stop.
- 1.25 s after the matched collision, B observed unidentified object B:track_008 enter its forward path corridor.
- 1.40 s after the matched collision, B observed unidentified object B:track_013 leave its forward path corridor.
- 3.75 s after the matched collision, B observed unidentified object B:track_013 enter its forward path corridor.
- 10.70 s after the matched collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
