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
| A | ALIGNED | A:e07 | 3.70 | -3.70 | reported the reference collision collision_001 |
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
| g04 | -2.50 | TRACK_APPEARED | A | B | A:e02 @ 1.20 |  |
| g05 | -2.50 | TRACK_APPEARED | B | B:track_001 | B:e03 @ 1.20 |  |
| g06 | -2.50 | CLOSING_START | A | B | A:e03 @ 1.20 | active_at_first_observation=True |
| g07 | -2.50 | CLOSING_START | B | B:track_001 | B:e04 @ 1.20 | active_at_first_observation=True |
| g08 | -2.20 | PREDICTED_PATH_CONFLICT_START | A | B | A:e04 @ 1.50 |  |
| g09 | -2.10 | STRONG_THROTTLE_END | B | - | B:e05 @ 1.60 |  |
| g10 | -2.05 | CRITICAL_TTC_START | A | B | A:e05 @ 1.65 |  |
| g11 | -2.05 | CRITICAL_TTC_START | B | B:track_001 | B:e06 @ 1.65 |  |
| g12 | -0.35 | TRACK_LOST | B | B:track_001 | B:e07 @ 3.35 |  |
| g13 | -0.25 | EGO_PATH_ENTRY | A | B | A:e06 @ 3.45 |  |
| g14 | 0.00 | COLLISION | - | A, B | A:e07 @ 3.70, B:e08 @ 3.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 6116.26, B 6116.26 |
| g15 | 0.00 | PREDICTED_PATH_CONFLICT_END | A | B | A:e08 @ 3.70 |  |
| g16 | 0.00 | CRITICAL_TTC_END | A | B | A:e09 @ 3.70 |  |
| g17 | 0.00 | CLOSING_END | A | B | A:e10 @ 3.70 |  |
| g18 | 0.00 | STRONG_THROTTLE_START | A | - | A:e11 @ 3.70 |  |
| g19 | 0.00 | STRONG_THROTTLE_START | B | - | B:e09 @ 3.70 |  |
| g20 | 0.00 | TRACK_APPEARED | B | B:track_002 | B:e10 @ 3.70 |  |
| g21 | 0.00 | TRACK_APPEARED | B | B:track_003 | B:e11 @ 3.70 |  |
| g22 | 0.00 | TRACK_APPEARED | B | B:track_004 | B:e12 @ 3.70 |  |
| g23 | 0.00 | TRACK_APPEARED | B | B:track_005 | B:e13 @ 3.70 |  |
| g24 | 0.00 | TRACK_APPEARED | B | B:track_007 | B:e14 @ 3.70 |  |
| g25 | 0.00 | TRACK_APPEARED | B | B:track_018 | B:e15 @ 3.70 |  |
| g26 | 0.00 | CLOSING_START | B | B:track_002 | B:e16 @ 3.70 | active_at_first_observation=True |
| g27 | 0.00 | CLOSING_START | B | B:track_004 | B:e17 @ 3.70 | active_at_first_observation=True |
| g28 | 0.00 | CLOSING_START | B | B:track_005 | B:e18 @ 3.70 | active_at_first_observation=True |
| g29 | 0.00 | CLOSING_START | B | B:track_007 | B:e19 @ 3.70 | active_at_first_observation=True |
| g30 | 0.00 | CLOSING_START | B | B:track_018 | B:e20 @ 3.70 | active_at_first_observation=True |
| g31 | 0.05 | STRONG_THROTTLE_END | A | - | A:e12 @ 3.75 |  |
| g32 | 0.05 | STRONG_THROTTLE_END | B | - | B:e21 @ 3.75 |  |
| g33 | 0.05 | BRAKE_START | A | - | A:e13 @ 3.75 |  |
| g34 | 0.05 | BRAKE_START | B | - | B:e22 @ 3.75 |  |
| g35 | 0.05 | HARD_BRAKE_START | A | - | A:e14 @ 3.75 |  |
| g36 | 0.05 | HARD_BRAKE_START | B | - | B:e23 @ 3.75 |  |
| g37 | 0.05 | TRACK_APPEARED | B | B:track_006 | B:e24 @ 3.75 |  |
| g38 | 0.05 | TRACK_APPEARED | B | B:track_012 | B:e25 @ 3.75 |  |
| g39 | 0.05 | EGO_PATH_ENTRY | B | B:track_003 | B:e26 @ 3.75 |  |
| g40 | 0.05 | CLOSING_START | B | B:track_012 | B:e27 @ 3.75 | active_at_first_observation=True |
| g41 | 0.10 | EGO_PATH_EXIT | B | B:track_003 | B:e28 @ 3.80 |  |
| g42 | 0.10 | TRACK_APPEARED | B | B:track_008 | B:e29 @ 3.80 |  |
| g43 | 0.10 | TRACK_APPEARED | B | B:track_009 | B:e30 @ 3.80 |  |
| g44 | 0.10 | TRACK_APPEARED | B | B:track_010 | B:e31 @ 3.80 |  |
| g45 | 0.10 | TRACK_APPEARED | B | B:track_011 | B:e32 @ 3.80 |  |
| g46 | 0.10 | EGO_PATH_ENTRY | B | B:track_005 | B:e33 @ 3.80 |  |
| g47 | 0.10 | CLOSING_START | B | B:track_009 | B:e34 @ 3.80 | active_at_first_observation=True |
| g48 | 0.15 | EGO_PATH_EXIT | B | B:track_005 | B:e35 @ 3.85 |  |
| g49 | 0.15 | TRACK_APPEARED | B | B:track_013 | B:e36 @ 3.85 |  |
| g50 | 0.15 | TRACK_APPEARED | B | B:track_014 | B:e37 @ 3.85 |  |
| g51 | 0.15 | EGO_PATH_ENTRY | B | B:track_002 | B:e38 @ 3.85 |  |
| g52 | 0.15 | CLOSING_START | B | B:track_008 | B:e39 @ 3.85 |  |
| g53 | 0.20 | EGO_PATH_EXIT | A | B | A:e15 @ 3.90 |  |
| g54 | 0.20 | EGO_PATH_EXIT | B | B:track_002 | B:e40 @ 3.90 |  |
| g55 | 0.20 | TRACK_APPEARED | B | B:track_015 | B:e41 @ 3.90 |  |
| g56 | 0.20 | TRACK_APPEARED | B | B:track_016 | B:e42 @ 3.90 |  |
| g57 | 0.20 | TRACK_APPEARED | B | B:track_017 | B:e43 @ 3.90 |  |
| g58 | 0.20 | EGO_PATH_ENTRY | B | B:track_018 | B:e44 @ 3.90 |  |
| g59 | 0.20 | CLOSING_START | B | B:track_013 | B:e45 @ 3.90 |  |
| g60 | 0.20 | CLOSING_START | B | B:track_014 | B:e46 @ 3.90 |  |
| g61 | 0.20 | CLOSING_START | B | B:track_015 | B:e47 @ 3.90 | active_at_first_observation=True |
| g62 | 0.20 | CRITICAL_TTC_START | B | B:track_015 | B:e48 @ 3.90 | active_at_first_observation=True |
| g63 | 0.25 | EGO_PATH_EXIT | B | B:track_018 | B:e49 @ 3.95 |  |
| g64 | 0.25 | CLOSING_START | B | B:track_016 | B:e50 @ 3.95 |  |
| g65 | 0.25 | CLOSING_START | B | B:track_017 | B:e51 @ 3.95 |  |
| g66 | 0.25 | TRACK_LOST | B | B:track_006 | B:e52 @ 3.95 |  |
| g67 | 0.30 | CLOSING_END | B | B:track_002 | B:e53 @ 4.00 |  |
| g68 | 0.30 | CLOSING_END | B | B:track_005 | B:e54 @ 4.00 |  |
| g69 | 0.30 | TRACK_APPEARED | B | B:track_019 | B:e55 @ 4.00 |  |
| g70 | 0.30 | TRACK_LOST | B | B:track_011 | B:e56 @ 4.00 |  |
| g71 | 0.35 | CLOSING_END | B | B:track_004 | B:e57 @ 4.05 |  |
| g72 | 0.35 | CLOSING_END | B | B:track_007 | B:e58 @ 4.05 |  |
| g73 | 0.35 | CLOSING_END | B | B:track_012 | B:e59 @ 4.05 |  |
| g74 | 0.35 | EGO_PATH_ENTRY | B | B:track_009 | B:e60 @ 4.05 |  |
| g75 | 0.35 | TRACK_LOST | A | B | A:e16 @ 4.05 |  |
| g76 | 0.35 | TRACK_LOST | B | B:track_003 | B:e61 @ 4.05 |  |
| g77 | 0.40 | CLOSING_END | B | B:track_009 | B:e62 @ 4.10 |  |
| g78 | 0.40 | CLOSING_END | B | B:track_018 | B:e63 @ 4.10 |  |
| g79 | 0.40 | EGO_PATH_EXIT | B | B:track_009 | B:e64 @ 4.10 |  |
| g80 | 0.40 | EGO_PATH_ENTRY | B | B:track_010 | B:e65 @ 4.10 |  |
| g81 | 0.45 | CLOSING_END | B | B:track_008 | B:e66 @ 4.15 |  |
| g82 | 0.45 | EGO_PATH_EXIT | B | B:track_010 | B:e67 @ 4.15 |  |
| g83 | 0.45 | EGO_PATH_ENTRY | B | B:track_008 | B:e68 @ 4.15 |  |
| g84 | 0.45 | TRACK_LOST | B | B:track_005 | B:e69 @ 4.15 |  |
| g85 | 0.50 | CRITICAL_TTC_END | B | B:track_015 | B:e70 @ 4.20 |  |
| g86 | 0.55 | CLOSING_END | B | B:track_013 | B:e71 @ 4.25 |  |
| g87 | 0.55 | CLOSING_END | B | B:track_015 | B:e72 @ 4.25 |  |
| g88 | 0.55 | EGO_PATH_EXIT | B | B:track_008 | B:e73 @ 4.25 |  |
| g89 | 0.55 | EGO_PATH_ENTRY | B | B:track_013 | B:e74 @ 4.25 |  |
| g90 | 0.55 | TRACK_LOST | B | B:track_018 | B:e75 @ 4.25 |  |
| g91 | 0.60 | CLOSING_END | B | B:track_014 | B:e76 @ 4.30 |  |
| g92 | 0.60 | CLOSING_END | B | B:track_016 | B:e77 @ 4.30 |  |
| g93 | 0.60 | CLOSING_END | B | B:track_017 | B:e78 @ 4.30 |  |
| g94 | 0.60 | MOVING_END | B | - | B:e79 @ 4.30 |  |
| g95 | 0.60 | STOP_START | B | - | B:e80 @ 4.30 |  |
| g96 | 0.85 | MOVING_END | A | - | A:e17 @ 4.55 |  |
| g97 | 0.85 | STOP_START | A | - | A:e18 @ 4.55 |  |
| g98 | 1.25 | EGO_PATH_ENTRY | B | B:track_008 | B:e81 @ 4.95 |  |
| g99 | 1.40 | EGO_PATH_EXIT | B | B:track_013 | B:e82 @ 5.10 |  |
| g100 | 3.75 | EGO_PATH_ENTRY | B | B:track_013 | B:e83 @ 7.45 |  |
| g101 | 10.70 | TRACK_LOST | B | B:track_004 | B:e84 @ 14.40 |  |

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
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g13 --PRECEDES--> g18
    g13 --PRECEDES--> g19
    g13 --PRECEDES--> g20
    g13 --PRECEDES--> g21
    g13 --PRECEDES--> g22
    g13 --PRECEDES--> g23
    g13 --PRECEDES--> g24
    g13 --PRECEDES--> g25
    g13 --PRECEDES--> g26
    g13 --PRECEDES--> g27
    g13 --PRECEDES--> g28
    g13 --PRECEDES--> g29
    g13 --PRECEDES--> g30
    g14 --PRECEDES--> g31
    g14 --PRECEDES--> g32
    g14 --PRECEDES--> g33
    g14 --PRECEDES--> g34
    g14 --PRECEDES--> g35
    g14 --PRECEDES--> g36
    g14 --PRECEDES--> g37
    g14 --PRECEDES--> g38
    g14 --PRECEDES--> g39
    g14 --PRECEDES--> g40
    g15 --PRECEDES--> g31
    g15 --PRECEDES--> g32
    g15 --PRECEDES--> g33
    g15 --PRECEDES--> g34
    g15 --PRECEDES--> g35
    g15 --PRECEDES--> g36
    g15 --PRECEDES--> g37
    g15 --PRECEDES--> g38
    g15 --PRECEDES--> g39
    g15 --PRECEDES--> g40
    g16 --PRECEDES--> g31
    g16 --PRECEDES--> g32
    g16 --PRECEDES--> g33
    g16 --PRECEDES--> g34
    g16 --PRECEDES--> g35
    g16 --PRECEDES--> g36
    g16 --PRECEDES--> g37
    g16 --PRECEDES--> g38
    g16 --PRECEDES--> g39
    g16 --PRECEDES--> g40
    g17 --PRECEDES--> g31
    g17 --PRECEDES--> g32
    g17 --PRECEDES--> g33
    g17 --PRECEDES--> g34
    g17 --PRECEDES--> g35
    g17 --PRECEDES--> g36
    g17 --PRECEDES--> g37
    g17 --PRECEDES--> g38
    g17 --PRECEDES--> g39
    g17 --PRECEDES--> g40
    g18 --PRECEDES--> g31
    g18 --PRECEDES--> g32
    g18 --PRECEDES--> g33
    g18 --PRECEDES--> g34
    g18 --PRECEDES--> g35
    g18 --PRECEDES--> g36
    g18 --PRECEDES--> g37
    g18 --PRECEDES--> g38
    g18 --PRECEDES--> g39
    g18 --PRECEDES--> g40
    g19 --PRECEDES--> g31
    g19 --PRECEDES--> g32
    g19 --PRECEDES--> g33
    g19 --PRECEDES--> g34
    g19 --PRECEDES--> g35
    g19 --PRECEDES--> g36
    g19 --PRECEDES--> g37
    g19 --PRECEDES--> g38
    g19 --PRECEDES--> g39
    g19 --PRECEDES--> g40
    g20 --PRECEDES--> g31
    g20 --PRECEDES--> g32
    g20 --PRECEDES--> g33
    g20 --PRECEDES--> g34
    g20 --PRECEDES--> g35
    g20 --PRECEDES--> g36
    g20 --PRECEDES--> g37
    g20 --PRECEDES--> g38
    g20 --PRECEDES--> g39
    g20 --PRECEDES--> g40
    g21 --PRECEDES--> g31
    g21 --PRECEDES--> g32
    g21 --PRECEDES--> g33
    g21 --PRECEDES--> g34
    g21 --PRECEDES--> g35
    g21 --PRECEDES--> g36
    g21 --PRECEDES--> g37
    g21 --PRECEDES--> g38
    g21 --PRECEDES--> g39
    g21 --PRECEDES--> g40
    g22 --PRECEDES--> g31
    g22 --PRECEDES--> g32
    g22 --PRECEDES--> g33
    g22 --PRECEDES--> g34
    g22 --PRECEDES--> g35
    g22 --PRECEDES--> g36
    g22 --PRECEDES--> g37
    g22 --PRECEDES--> g38
    g22 --PRECEDES--> g39
    g22 --PRECEDES--> g40
    g23 --PRECEDES--> g31
    g23 --PRECEDES--> g32
    g23 --PRECEDES--> g33
    g23 --PRECEDES--> g34
    g23 --PRECEDES--> g35
    g23 --PRECEDES--> g36
    g23 --PRECEDES--> g37
    g23 --PRECEDES--> g38
    g23 --PRECEDES--> g39
    g23 --PRECEDES--> g40
    g24 --PRECEDES--> g31
    g24 --PRECEDES--> g32
    g24 --PRECEDES--> g33
    g24 --PRECEDES--> g34
    g24 --PRECEDES--> g35
    g24 --PRECEDES--> g36
    g24 --PRECEDES--> g37
    g24 --PRECEDES--> g38
    g24 --PRECEDES--> g39
    g24 --PRECEDES--> g40
    g25 --PRECEDES--> g31
    g25 --PRECEDES--> g32
    g25 --PRECEDES--> g33
    g25 --PRECEDES--> g34
    g25 --PRECEDES--> g35
    g25 --PRECEDES--> g36
    g25 --PRECEDES--> g37
    g25 --PRECEDES--> g38
    g25 --PRECEDES--> g39
    g25 --PRECEDES--> g40
    g26 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g26 --PRECEDES--> g33
    g26 --PRECEDES--> g34
    g26 --PRECEDES--> g35
    g26 --PRECEDES--> g36
    g26 --PRECEDES--> g37
    g26 --PRECEDES--> g38
    g26 --PRECEDES--> g39
    g26 --PRECEDES--> g40
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g27 --PRECEDES--> g35
    g27 --PRECEDES--> g36
    g27 --PRECEDES--> g37
    g27 --PRECEDES--> g38
    g27 --PRECEDES--> g39
    g27 --PRECEDES--> g40
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g28 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g28 --PRECEDES--> g36
    g28 --PRECEDES--> g37
    g28 --PRECEDES--> g38
    g28 --PRECEDES--> g39
    g28 --PRECEDES--> g40
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g29 --PRECEDES--> g35
    g29 --PRECEDES--> g36
    g29 --PRECEDES--> g37
    g29 --PRECEDES--> g38
    g29 --PRECEDES--> g39
    g29 --PRECEDES--> g40
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g30 --PRECEDES--> g35
    g30 --PRECEDES--> g36
    g30 --PRECEDES--> g37
    g30 --PRECEDES--> g38
    g30 --PRECEDES--> g39
    g30 --PRECEDES--> g40
    g31 --PRECEDES--> g41
    g31 --PRECEDES--> g42
    g31 --PRECEDES--> g43
    g31 --PRECEDES--> g44
    g31 --PRECEDES--> g45
    g31 --PRECEDES--> g46
    g31 --PRECEDES--> g47
    g32 --PRECEDES--> g41
    g32 --PRECEDES--> g42
    g32 --PRECEDES--> g43
    g32 --PRECEDES--> g44
    g32 --PRECEDES--> g45
    g32 --PRECEDES--> g46
    g32 --PRECEDES--> g47
    g33 --PRECEDES--> g41
    g33 --PRECEDES--> g42
    g33 --PRECEDES--> g43
    g33 --PRECEDES--> g44
    g33 --PRECEDES--> g45
    g33 --PRECEDES--> g46
    g33 --PRECEDES--> g47
    g34 --PRECEDES--> g41
    g34 --PRECEDES--> g42
    g34 --PRECEDES--> g43
    g34 --PRECEDES--> g44
    g34 --PRECEDES--> g45
    g34 --PRECEDES--> g46
    g34 --PRECEDES--> g47
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g35 --PRECEDES--> g43
    g35 --PRECEDES--> g44
    g35 --PRECEDES--> g45
    g35 --PRECEDES--> g46
    g35 --PRECEDES--> g47
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g36 --PRECEDES--> g43
    g36 --PRECEDES--> g44
    g36 --PRECEDES--> g45
    g36 --PRECEDES--> g46
    g36 --PRECEDES--> g47
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g37 --PRECEDES--> g44
    g37 --PRECEDES--> g45
    g37 --PRECEDES--> g46
    g37 --PRECEDES--> g47
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g38 --PRECEDES--> g44
    g38 --PRECEDES--> g45
    g38 --PRECEDES--> g46
    g38 --PRECEDES--> g47
    g39 --PRECEDES--> g41
    g39 --PRECEDES--> g42
    g39 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g39 --PRECEDES--> g45
    g39 --PRECEDES--> g46
    g39 --PRECEDES--> g47
    g40 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g40 --PRECEDES--> g45
    g40 --PRECEDES--> g46
    g40 --PRECEDES--> g47
    g41 --PRECEDES--> g48
    g41 --PRECEDES--> g49
    g41 --PRECEDES--> g50
    g41 --PRECEDES--> g51
    g41 --PRECEDES--> g52
    g42 --PRECEDES--> g48
    g42 --PRECEDES--> g49
    g42 --PRECEDES--> g50
    g42 --PRECEDES--> g51
    g42 --PRECEDES--> g52
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g43 --PRECEDES--> g50
    g43 --PRECEDES--> g51
    g43 --PRECEDES--> g52
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g44 --PRECEDES--> g50
    g44 --PRECEDES--> g51
    g44 --PRECEDES--> g52
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g45 --PRECEDES--> g50
    g45 --PRECEDES--> g51
    g45 --PRECEDES--> g52
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g46 --PRECEDES--> g51
    g46 --PRECEDES--> g52
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g47 --PRECEDES--> g50
    g47 --PRECEDES--> g51
    g47 --PRECEDES--> g52
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
    g50 --PRECEDES--> g53
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g50 --PRECEDES--> g56
    g50 --PRECEDES--> g57
    g50 --PRECEDES--> g58
    g50 --PRECEDES--> g59
    g50 --PRECEDES--> g60
    g50 --PRECEDES--> g61
    g50 --PRECEDES--> g62
    g51 --PRECEDES--> g53
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g51 --PRECEDES--> g57
    g51 --PRECEDES--> g58
    g51 --PRECEDES--> g59
    g51 --PRECEDES--> g60
    g51 --PRECEDES--> g61
    g51 --PRECEDES--> g62
    g52 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g52 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g52 --PRECEDES--> g58
    g52 --PRECEDES--> g59
    g52 --PRECEDES--> g60
    g52 --PRECEDES--> g61
    g52 --PRECEDES--> g62
    g53 --PRECEDES--> g63
    g53 --PRECEDES--> g64
    g53 --PRECEDES--> g65
    g53 --PRECEDES--> g66
    g54 --PRECEDES--> g63
    g54 --PRECEDES--> g64
    g54 --PRECEDES--> g65
    g54 --PRECEDES--> g66
    g55 --PRECEDES--> g63
    g55 --PRECEDES--> g64
    g55 --PRECEDES--> g65
    g55 --PRECEDES--> g66
    g56 --PRECEDES--> g63
    g56 --PRECEDES--> g64
    g56 --PRECEDES--> g65
    g56 --PRECEDES--> g66
    g57 --PRECEDES--> g63
    g57 --PRECEDES--> g64
    g57 --PRECEDES--> g65
    g57 --PRECEDES--> g66
    g58 --PRECEDES--> g63
    g58 --PRECEDES--> g64
    g58 --PRECEDES--> g65
    g58 --PRECEDES--> g66
    g59 --PRECEDES--> g63
    g59 --PRECEDES--> g64
    g59 --PRECEDES--> g65
    g59 --PRECEDES--> g66
    g60 --PRECEDES--> g63
    g60 --PRECEDES--> g64
    g60 --PRECEDES--> g65
    g60 --PRECEDES--> g66
    g61 --PRECEDES--> g63
    g61 --PRECEDES--> g64
    g61 --PRECEDES--> g65
    g61 --PRECEDES--> g66
    g62 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g62 --PRECEDES--> g65
    g62 --PRECEDES--> g66
    g63 --PRECEDES--> g67
    g63 --PRECEDES--> g68
    g63 --PRECEDES--> g69
    g63 --PRECEDES--> g70
    g64 --PRECEDES--> g67
    g64 --PRECEDES--> g68
    g64 --PRECEDES--> g69
    g64 --PRECEDES--> g70
    g65 --PRECEDES--> g67
    g65 --PRECEDES--> g68
    g65 --PRECEDES--> g69
    g65 --PRECEDES--> g70
    g66 --PRECEDES--> g67
    g66 --PRECEDES--> g68
    g66 --PRECEDES--> g69
    g66 --PRECEDES--> g70
    g67 --PRECEDES--> g71
    g67 --PRECEDES--> g72
    g67 --PRECEDES--> g73
    g67 --PRECEDES--> g74
    g67 --PRECEDES--> g75
    g67 --PRECEDES--> g76
    g68 --PRECEDES--> g71
    g68 --PRECEDES--> g72
    g68 --PRECEDES--> g73
    g68 --PRECEDES--> g74
    g68 --PRECEDES--> g75
    g68 --PRECEDES--> g76
    g69 --PRECEDES--> g71
    g69 --PRECEDES--> g72
    g69 --PRECEDES--> g73
    g69 --PRECEDES--> g74
    g69 --PRECEDES--> g75
    g69 --PRECEDES--> g76
    g70 --PRECEDES--> g71
    g70 --PRECEDES--> g72
    g70 --PRECEDES--> g73
    g70 --PRECEDES--> g74
    g70 --PRECEDES--> g75
    g70 --PRECEDES--> g76
    g71 --PRECEDES--> g77
    g71 --PRECEDES--> g78
    g71 --PRECEDES--> g79
    g71 --PRECEDES--> g80
    g72 --PRECEDES--> g77
    g72 --PRECEDES--> g78
    g72 --PRECEDES--> g79
    g72 --PRECEDES--> g80
    g73 --PRECEDES--> g77
    g73 --PRECEDES--> g78
    g73 --PRECEDES--> g79
    g73 --PRECEDES--> g80
    g74 --PRECEDES--> g77
    g74 --PRECEDES--> g78
    g74 --PRECEDES--> g79
    g74 --PRECEDES--> g80
    g75 --PRECEDES--> g77
    g75 --PRECEDES--> g78
    g75 --PRECEDES--> g79
    g75 --PRECEDES--> g80
    g76 --PRECEDES--> g77
    g76 --PRECEDES--> g78
    g76 --PRECEDES--> g79
    g76 --PRECEDES--> g80
    g77 --PRECEDES--> g81
    g77 --PRECEDES--> g82
    g77 --PRECEDES--> g83
    g77 --PRECEDES--> g84
    g78 --PRECEDES--> g81
    g78 --PRECEDES--> g82
    g78 --PRECEDES--> g83
    g78 --PRECEDES--> g84
    g79 --PRECEDES--> g81
    g79 --PRECEDES--> g82
    g79 --PRECEDES--> g83
    g79 --PRECEDES--> g84
    g80 --PRECEDES--> g81
    g80 --PRECEDES--> g82
    g80 --PRECEDES--> g83
    g80 --PRECEDES--> g84
    g81 --PRECEDES--> g85
    g82 --PRECEDES--> g85
    g83 --PRECEDES--> g85
    g84 --PRECEDES--> g85
    g85 --PRECEDES--> g86
    g85 --PRECEDES--> g87
    g85 --PRECEDES--> g88
    g85 --PRECEDES--> g89
    g85 --PRECEDES--> g90
    g86 --PRECEDES--> g91
    g86 --PRECEDES--> g92
    g86 --PRECEDES--> g93
    g86 --PRECEDES--> g94
    g86 --PRECEDES--> g95
    g87 --PRECEDES--> g91
    g87 --PRECEDES--> g92
    g87 --PRECEDES--> g93
    g87 --PRECEDES--> g94
    g87 --PRECEDES--> g95
    g88 --PRECEDES--> g91
    g88 --PRECEDES--> g92
    g88 --PRECEDES--> g93
    g88 --PRECEDES--> g94
    g88 --PRECEDES--> g95
    g89 --PRECEDES--> g91
    g89 --PRECEDES--> g92
    g89 --PRECEDES--> g93
    g89 --PRECEDES--> g94
    g89 --PRECEDES--> g95
    g90 --PRECEDES--> g91
    g90 --PRECEDES--> g92
    g90 --PRECEDES--> g93
    g90 --PRECEDES--> g94
    g90 --PRECEDES--> g95
    g91 --PRECEDES--> g96
    g91 --PRECEDES--> g97
    g92 --PRECEDES--> g96
    g92 --PRECEDES--> g97
    g93 --PRECEDES--> g96
    g93 --PRECEDES--> g97
    g94 --PRECEDES--> g96
    g94 --PRECEDES--> g97
    g95 --PRECEDES--> g96
    g95 --PRECEDES--> g97
    g96 --PRECEDES--> g98
    g97 --PRECEDES--> g98
    g98 --PRECEDES--> g99
    g99 --PRECEDES--> g100
    g100 --PRECEDES--> g101
    g04 --SAME_TRACK--> g06
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g10
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g15
    g04 --SAME_TRACK--> g16
    g04 --SAME_TRACK--> g17
    g04 --SAME_TRACK--> g53
    g04 --SAME_TRACK--> g75
    g05 --SAME_TRACK--> g07
    g05 --SAME_TRACK--> g11
    g05 --SAME_TRACK--> g12
    g20 --SAME_TRACK--> g26
    g22 --SAME_TRACK--> g27
    g23 --SAME_TRACK--> g28
    g24 --SAME_TRACK--> g29
    g25 --SAME_TRACK--> g30
    g21 --SAME_TRACK--> g39
    g38 --SAME_TRACK--> g40
    g21 --SAME_TRACK--> g41
    g23 --SAME_TRACK--> g46
    g43 --SAME_TRACK--> g47
    g23 --SAME_TRACK--> g48
    g20 --SAME_TRACK--> g51
    g42 --SAME_TRACK--> g52
    g20 --SAME_TRACK--> g54
    g25 --SAME_TRACK--> g58
    g49 --SAME_TRACK--> g59
    g50 --SAME_TRACK--> g60
    g55 --SAME_TRACK--> g61
    g55 --SAME_TRACK--> g62
    g25 --SAME_TRACK--> g63
    g56 --SAME_TRACK--> g64
    g57 --SAME_TRACK--> g65
    g37 --SAME_TRACK--> g66
    g20 --SAME_TRACK--> g67
    g23 --SAME_TRACK--> g68
    g45 --SAME_TRACK--> g70
    g22 --SAME_TRACK--> g71
    g24 --SAME_TRACK--> g72
    g38 --SAME_TRACK--> g73
    g43 --SAME_TRACK--> g74
    g21 --SAME_TRACK--> g76
    g43 --SAME_TRACK--> g77
    g25 --SAME_TRACK--> g78
    g43 --SAME_TRACK--> g79
    g44 --SAME_TRACK--> g80
    g42 --SAME_TRACK--> g81
    g44 --SAME_TRACK--> g82
    g42 --SAME_TRACK--> g83
    g23 --SAME_TRACK--> g84
    g55 --SAME_TRACK--> g85
    g49 --SAME_TRACK--> g86
    g55 --SAME_TRACK--> g87
    g42 --SAME_TRACK--> g88
    g49 --SAME_TRACK--> g89
    g25 --SAME_TRACK--> g90
    g50 --SAME_TRACK--> g91
    g56 --SAME_TRACK--> g92
    g57 --SAME_TRACK--> g93
    g42 --SAME_TRACK--> g98
    g49 --SAME_TRACK--> g99
    g49 --SAME_TRACK--> g100
    g22 --SAME_TRACK--> g101
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.70 | MOVING_START(A); MOVING_START(B) |
| -2.85 | STRONG_THROTTLE_START(B) |
| -2.50 | TRACK_APPEARED(A,B); TRACK_APPEARED(B,B:track_001); CLOSING_START(A,B); CLOSING_START(B,B:track_001) |
| -2.20 | PREDICTED_PATH_CONFLICT_START(A,B) |
| -2.10 | STRONG_THROTTLE_END(B) |
| -2.05 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_001) |
| -0.35 | TRACK_LOST(B,B:track_001) |
| -0.25 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); PREDICTED_PATH_CONFLICT_END(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); TRACK_APPEARED(B,B:track_003); TRACK_APPEARED(B,B:track_004); TRACK_APPEARED(B,B:track_005); TRACK_APPEARED(B,B:track_007); TRACK_APPEARED(B,B:track_018); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_018) |
| +0.05 | STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_006); TRACK_APPEARED(B,B:track_012); EGO_PATH_ENTRY(B,B:track_003); CLOSING_START(B,B:track_012) |
| +0.10 | EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED(B,B:track_008); TRACK_APPEARED(B,B:track_009); TRACK_APPEARED(B,B:track_010); TRACK_APPEARED(B,B:track_011); EGO_PATH_ENTRY(B,B:track_005); CLOSING_START(B,B:track_009) |
| +0.15 | EGO_PATH_EXIT(B,B:track_005); TRACK_APPEARED(B,B:track_013); TRACK_APPEARED(B,B:track_014); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_008) |
| +0.20 | EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED(B,B:track_015); TRACK_APPEARED(B,B:track_016); TRACK_APPEARED(B,B:track_017); EGO_PATH_ENTRY(B,B:track_018); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); CRITICAL_TTC_START(B,B:track_015) |
| +0.25 | EGO_PATH_EXIT(B,B:track_018); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_017); TRACK_LOST(B,B:track_006) |
| +0.30 | CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_005); TRACK_APPEARED(B,B:track_019); TRACK_LOST(B,B:track_011) |
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
| -2.50 | A | g04 TRACK_APPEARED(A,B) (A:e02)<br>g06 CLOSING_START(A,B) (A:e03) | ego: MOVING |
| -2.50 | B | g05 TRACK_APPEARED(B,B:track_001) (B:e03)<br>g07 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| -2.20 | A | g08 PREDICTED_PATH_CONFLICT_START(A,B) (A:e04) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| -2.10 | B | g09 STRONG_THROTTLE_END(B) (B:e05) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING |
| -2.05 | A | g10 CRITICAL_TTC_START(A,B) (A:e05) | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT |
| -2.05 | B | g11 CRITICAL_TTC_START(B,B:track_001) (B:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| -0.35 | B | g12 TRACK_LOST(B,B:track_001) (B:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC |
| -0.25 | A | g13 EGO_PATH_ENTRY(A,B) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT |
| +0.00 | A | g14 COLLISION(A,B) (A:e07)<br>g15 PREDICTED_PATH_CONFLICT_END(A,B) (A:e08)<br>g16 CRITICAL_TTC_END(A,B) (A:e09)<br>g17 CLOSING_END(A,B) (A:e10)<br>g18 STRONG_THROTTLE_START(A) (A:e11) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT |
| +0.00 | B | g14 COLLISION(A,B) (B:e08)<br>g19 STRONG_THROTTLE_START(B) (B:e09)<br>g20 TRACK_APPEARED(B,B:track_002) (B:e10)<br>g21 TRACK_APPEARED(B,B:track_003) (B:e11)<br>g22 TRACK_APPEARED(B,B:track_004) (B:e12)<br>g23 TRACK_APPEARED(B,B:track_005) (B:e13)<br>g24 TRACK_APPEARED(B,B:track_007) (B:e14)<br>g25 TRACK_APPEARED(B,B:track_018) (B:e15)<br>g26 CLOSING_START(B,B:track_002) (B:e16)<br>g27 CLOSING_START(B,B:track_004) (B:e17)<br>g28 CLOSING_START(B,B:track_005) (B:e18)<br>g29 CLOSING_START(B,B:track_007) (B:e19)<br>g30 CLOSING_START(B,B:track_018) (B:e20) | ego: MOVING<br>lost (states UNKNOWN): track_001 |
| +0.05 | A | g31 STRONG_THROTTLE_END(A) (A:e12)<br>g33 BRAKE_START(A) (A:e13)<br>g35 HARD_BRAKE_START(A) (A:e14) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, IN_EGO_PATH |
| +0.05 | B | g32 STRONG_THROTTLE_END(B) (B:e21)<br>g34 BRAKE_START(B) (B:e22)<br>g36 HARD_BRAKE_START(B) (B:e23)<br>g37 TRACK_APPEARED(B,B:track_006) (B:e24)<br>g38 TRACK_APPEARED(B,B:track_012) (B:e25)<br>g39 EGO_PATH_ENTRY(B,B:track_003) (B:e26)<br>g40 CLOSING_START(B,B:track_012) (B:e27) | ego: MOVING, STRONG_THROTTLE<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_018: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001 |
| +0.10 | B | g41 EGO_PATH_EXIT(B,B:track_003) (B:e28)<br>g42 TRACK_APPEARED(B,B:track_008) (B:e29)<br>g43 TRACK_APPEARED(B,B:track_009) (B:e30)<br>g44 TRACK_APPEARED(B,B:track_010) (B:e31)<br>g45 TRACK_APPEARED(B,B:track_011) (B:e32)<br>g46 EGO_PATH_ENTRY(B,B:track_005) (B:e33)<br>g47 CLOSING_START(B,B:track_009) (B:e34) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, IN_EGO_PATH, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_012: VISIBLE, CLOSING<br>track_018: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001 |
| +0.15 | B | g48 EGO_PATH_EXIT(B,B:track_005) (B:e35)<br>g49 TRACK_APPEARED(B,B:track_013) (B:e36)<br>g50 TRACK_APPEARED(B,B:track_014) (B:e37)<br>g51 EGO_PATH_ENTRY(B,B:track_002) (B:e38)<br>g52 CLOSING_START(B,B:track_008) (B:e39) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING, IN_EGO_PATH<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE<br>track_011: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING<br>track_018: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001 |
| +0.20 | A | g53 EGO_PATH_EXIT(A,B) (A:e15) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH |
| +0.20 | B | g54 EGO_PATH_EXIT(B,B:track_002) (B:e40)<br>g55 TRACK_APPEARED(B,B:track_015) (B:e41)<br>g56 TRACK_APPEARED(B,B:track_016) (B:e42)<br>g57 TRACK_APPEARED(B,B:track_017) (B:e43)<br>g58 EGO_PATH_ENTRY(B,B:track_018) (B:e44)<br>g59 CLOSING_START(B,B:track_013) (B:e45)<br>g60 CLOSING_START(B,B:track_014) (B:e46)<br>g61 CLOSING_START(B,B:track_015) (B:e47)<br>g62 CRITICAL_TTC_START(B,B:track_015) (B:e48) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH<br>track_003: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE<br>track_011: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE<br>track_014: VISIBLE<br>track_018: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001 |
| +0.25 | B | g63 EGO_PATH_EXIT(B,B:track_018) (B:e49)<br>g64 CLOSING_START(B,B:track_016) (B:e50)<br>g65 CLOSING_START(B,B:track_017) (B:e51)<br>g66 TRACK_LOST(B,B:track_006) (B:e52) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE<br>track_011: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING, CRITICAL_TTC<br>track_016: VISIBLE<br>track_017: VISIBLE<br>track_018: VISIBLE, CLOSING, IN_EGO_PATH<br>lost (states UNKNOWN): track_001 |
| +0.30 | B | g67 CLOSING_END(B,B:track_002) (B:e53)<br>g68 CLOSING_END(B,B:track_005) (B:e54)<br>g69 TRACK_APPEARED(B,B:track_019) (B:e55)<br>g70 TRACK_LOST(B,B:track_011) (B:e56) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE<br>track_011: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING, CRITICAL_TTC<br>track_016: VISIBLE, CLOSING<br>track_017: VISIBLE, CLOSING<br>track_018: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_006 |
| +0.35 | B | g71 CLOSING_END(B,B:track_004) (B:e57)<br>g72 CLOSING_END(B,B:track_007) (B:e58)<br>g73 CLOSING_END(B,B:track_012) (B:e59)<br>g74 EGO_PATH_ENTRY(B,B:track_009) (B:e60)<br>g76 TRACK_LOST(B,B:track_003) (B:e61) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_003: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE<br>track_012: VISIBLE, CLOSING<br>track_013: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING, CRITICAL_TTC<br>track_016: VISIBLE, CLOSING<br>track_017: VISIBLE, CLOSING<br>track_018: VISIBLE, CLOSING<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_006, track_011 |
| +0.35 | A | g75 TRACK_LOST(A,B) (A:e16) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE |
| +0.40 | B | g77 CLOSING_END(B,B:track_009) (B:e62)<br>g78 CLOSING_END(B,B:track_018) (B:e63)<br>g79 EGO_PATH_EXIT(B,B:track_009) (B:e64)<br>g80 EGO_PATH_ENTRY(B,B:track_010) (B:e65) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_005: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING, IN_EGO_PATH<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING, CRITICAL_TTC<br>track_016: VISIBLE, CLOSING<br>track_017: VISIBLE, CLOSING<br>track_018: VISIBLE, CLOSING<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_006, track_011 |
| +0.45 | B | g81 CLOSING_END(B,B:track_008) (B:e66)<br>g82 EGO_PATH_EXIT(B,B:track_010) (B:e67)<br>g83 EGO_PATH_ENTRY(B,B:track_008) (B:e68)<br>g84 TRACK_LOST(B,B:track_005) (B:e69) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_005: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE, CLOSING<br>track_009: VISIBLE<br>track_010: VISIBLE, IN_EGO_PATH<br>track_012: VISIBLE<br>track_013: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING, CRITICAL_TTC<br>track_016: VISIBLE, CLOSING<br>track_017: VISIBLE, CLOSING<br>track_018: VISIBLE<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_006, track_011 |
| +0.50 | B | g85 CRITICAL_TTC_END(B,B:track_015) (B:e70) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE, IN_EGO_PATH<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING, CRITICAL_TTC<br>track_016: VISIBLE, CLOSING<br>track_017: VISIBLE, CLOSING<br>track_018: VISIBLE<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_005, track_006, track_011 |
| +0.55 | B | g86 CLOSING_END(B,B:track_013) (B:e71)<br>g87 CLOSING_END(B,B:track_015) (B:e72)<br>g88 EGO_PATH_EXIT(B,B:track_008) (B:e73)<br>g89 EGO_PATH_ENTRY(B,B:track_013) (B:e74)<br>g90 TRACK_LOST(B,B:track_018) (B:e75) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE, IN_EGO_PATH<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE, CLOSING<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>track_016: VISIBLE, CLOSING<br>track_017: VISIBLE, CLOSING<br>track_018: VISIBLE<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_005, track_006, track_011 |
| +0.60 | B | g91 CLOSING_END(B,B:track_014) (B:e76)<br>g92 CLOSING_END(B,B:track_016) (B:e77)<br>g93 CLOSING_END(B,B:track_017) (B:e78)<br>g94 MOVING_END(B) (B:e79)<br>g95 STOP_START(B) (B:e80) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE, IN_EGO_PATH<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE<br>track_016: VISIBLE, CLOSING<br>track_017: VISIBLE, CLOSING<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_005, track_006, track_011, track_018 |
| +0.85 | A | g96 MOVING_END(A) (A:e17)<br>g97 STOP_START(A) (A:e18) | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 |
| +1.25 | B | g98 EGO_PATH_ENTRY(B,B:track_008) (B:e81) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE, IN_EGO_PATH<br>track_014: VISIBLE<br>track_015: VISIBLE<br>track_016: VISIBLE<br>track_017: VISIBLE<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_005, track_006, track_011, track_018 |
| +1.40 | B | g99 EGO_PATH_EXIT(B,B:track_013) (B:e82) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE, IN_EGO_PATH<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE, IN_EGO_PATH<br>track_014: VISIBLE<br>track_015: VISIBLE<br>track_016: VISIBLE<br>track_017: VISIBLE<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_005, track_006, track_011, track_018 |
| +3.75 | B | g100 EGO_PATH_ENTRY(B,B:track_013) (B:e83) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE, IN_EGO_PATH<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE<br>track_014: VISIBLE<br>track_015: VISIBLE<br>track_016: VISIBLE<br>track_017: VISIBLE<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_005, track_006, track_011, track_018 |
| +10.70 | B | g101 TRACK_LOST(B,B:track_004) (B:e84) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_004: VISIBLE<br>track_007: VISIBLE<br>track_008: VISIBLE, IN_EGO_PATH<br>track_009: VISIBLE<br>track_010: VISIBLE<br>track_012: VISIBLE<br>track_013: VISIBLE, IN_EGO_PATH<br>track_014: VISIBLE<br>track_015: VISIBLE<br>track_016: VISIBLE<br>track_017: VISIBLE<br>track_019: VISIBLE<br>lost (states UNKNOWN): track_001, track_003, track_005, track_006, track_011, track_018 |

## Plain-language reading

- 3.70 s before the matched collision, A started moving (already the case when first observed).
- 3.70 s before the matched collision, B started moving (already the case when first observed).
- 2.85 s before the matched collision, B started applying strong throttle.
- 2.50 s before the matched collision, A's radar started tracking B.
- 2.50 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 2.50 s before the matched collision, A observed B start closing in (already the case when first observed).
- 2.50 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.20 s before the matched collision, A predicted a path conflict with B (close approach ahead if both keep their motion).
- 2.10 s before the matched collision, B stopped applying strong throttle.
- 2.05 s before the matched collision, A's time-to-contact with B became critical.
- 2.05 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical.
- 0.35 s before the matched collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- 0.25 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6116, B: 6116 N*s).
- At the matched collision, A stopped predicting a path conflict with B.
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, B's radar started tracking unidentified object B:track_002.
- At the matched collision, B's radar started tracking unidentified object B:track_003.
- At the matched collision, B's radar started tracking unidentified object B:track_004.
- At the matched collision, B's radar started tracking unidentified object B:track_005.
- At the matched collision, B's radar started tracking unidentified object B:track_007.
- At the matched collision, B's radar started tracking unidentified object B:track_018.
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
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_006.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_012.
- 0.05 s after the matched collision, B observed unidentified object B:track_003 enter its forward path corridor.
- 0.05 s after the matched collision, B observed unidentified object B:track_012 start closing in (already the case when first observed).
- 0.10 s after the matched collision, B observed unidentified object B:track_003 leave its forward path corridor.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_008.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_009.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_010.
- 0.10 s after the matched collision, B's radar started tracking unidentified object B:track_011.
- 0.10 s after the matched collision, B observed unidentified object B:track_005 enter its forward path corridor.
- 0.10 s after the matched collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 0.15 s after the matched collision, B observed unidentified object B:track_005 leave its forward path corridor.
- 0.15 s after the matched collision, B's radar started tracking unidentified object B:track_013.
- 0.15 s after the matched collision, B's radar started tracking unidentified object B:track_014.
- 0.15 s after the matched collision, B observed unidentified object B:track_002 enter its forward path corridor.
- 0.15 s after the matched collision, B observed unidentified object B:track_008 start closing in.
- 0.20 s after the matched collision, A observed B leave its forward path corridor.
- 0.20 s after the matched collision, B observed unidentified object B:track_002 leave its forward path corridor.
- 0.20 s after the matched collision, B's radar started tracking unidentified object B:track_015.
- 0.20 s after the matched collision, B's radar started tracking unidentified object B:track_016.
- 0.20 s after the matched collision, B's radar started tracking unidentified object B:track_017.
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
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_019.
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
