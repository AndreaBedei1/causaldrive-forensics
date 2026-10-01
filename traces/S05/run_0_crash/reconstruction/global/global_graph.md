# Global graph - S05/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
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
| B | ALIGNED | B:e06 | 3.70 | -3.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6116.26 vs 6116.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.90 | A and B both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.5 m -> 1.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.70 m/s over 2.5 s<br>range at the contact 0.90 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.73 | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 2.50 s before the matched collision<br>continuous up to the contact: last observed 0.35 s before it (window 0.50 s)<br>approaching before the contact: range 19.9 m -> 5.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.58 m/s over 2.2 s<br>range at the contact 5.59 m (beyond 3.50 m: confidence factor 0.78)<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 18.91 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 32.42 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 37.27 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 22.75 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 29.98 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_015 | B:track_015 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_016 | B:track_016 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_017 | B:track_017 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_018 | B:track_018 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>range at the contact 27.37 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_019 | B:track_019 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 6116.26 vs 6116.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.70 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.70 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -2.50 | TRACK_APPEARED_LEFT | B | A | B:e02 @ 1.20 |  |
| g04 | -2.50 | TRACK_APPEARED_RIGHT | A | B | A:e02 @ 1.20 |  |
| g05 | -2.50 | CLOSING_START | A | B | A:e03 @ 1.20 | active_at_first_observation=True |
| g06 | -2.50 | CLOSING_START | B | A | B:e03 @ 1.20 | active_at_first_observation=True |
| g07 | -2.05 | CRITICAL_TTC_START | A | B | A:e04 @ 1.65 |  |
| g08 | -2.05 | CRITICAL_TTC_START | B | A | B:e04 @ 1.65 |  |
| g09 | -0.35 | TRACK_LOST | B | A | B:e05 @ 3.35 |  |
| g10 | -0.25 | EGO_PATH_ENTRY | A | B | A:e05 @ 3.45 |  |
| g11 | 0.00 | COLLISION | - | A, B | A:e06 @ 3.70, B:e06 @ 3.70 | matched_event=collision_001; reference_event=True; peak_impulse=A 6116.26, B 6116.26 |
| g12 | 0.00 | CRITICAL_TTC_END | A | B | A:e07 @ 3.70 |  |
| g13 | 0.00 | CLOSING_END | A | B | A:e08 @ 3.70 |  |
| g14 | 0.00 | TURN_LEFT_START | B | - | B:e07 @ 3.70 |  |
| g15 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e08 @ 3.70 |  |
| g16 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_003 | B:e09 @ 3.70 |  |
| g17 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_004 | B:e10 @ 3.70 |  |
| g18 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_005 | B:e11 @ 3.70 |  |
| g19 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_007 | B:e12 @ 3.70 |  |
| g20 | 0.00 | TRACK_APPEARED_LEFT | B | B:track_018 | B:e13 @ 3.70 |  |
| g21 | 0.00 | CLOSING_START | B | B:track_002 | B:e14 @ 3.70 | active_at_first_observation=True |
| g22 | 0.00 | CLOSING_START | B | B:track_004 | B:e15 @ 3.70 | active_at_first_observation=True |
| g23 | 0.00 | CLOSING_START | B | B:track_005 | B:e16 @ 3.70 | active_at_first_observation=True |
| g24 | 0.00 | CLOSING_START | B | B:track_007 | B:e17 @ 3.70 | active_at_first_observation=True |
| g25 | 0.00 | CLOSING_START | B | B:track_018 | B:e18 @ 3.70 | active_at_first_observation=True |
| g26 | 0.05 | BRAKE_START | A | - | A:e09 @ 3.75 |  |
| g27 | 0.05 | BRAKE_START | B | - | B:e19 @ 3.75 |  |
| g28 | 0.05 | TRACK_APPEARED_LEFT | B | B:track_012 | B:e20 @ 3.75 |  |
| g29 | 0.05 | TRACK_APPEARED_RIGHT | B | B:track_006 | B:e21 @ 3.75 |  |
| g30 | 0.05 | EGO_PATH_ENTRY | B | B:track_003 | B:e22 @ 3.75 |  |
| g31 | 0.05 | CLOSING_START | B | B:track_012 | B:e23 @ 3.75 | active_at_first_observation=True |
| g32 | 0.10 | EGO_PATH_EXIT | B | B:track_003 | B:e24 @ 3.80 |  |
| g33 | 0.10 | TRACK_APPEARED_LEFT | B | B:track_008 | B:e25 @ 3.80 |  |
| g34 | 0.10 | TRACK_APPEARED_LEFT | B | B:track_009 | B:e26 @ 3.80 |  |
| g35 | 0.10 | TRACK_APPEARED_LEFT | B | B:track_010 | B:e27 @ 3.80 |  |
| g36 | 0.10 | TRACK_APPEARED_RIGHT | B | B:track_011 | B:e28 @ 3.80 |  |
| g37 | 0.10 | EGO_PATH_ENTRY | B | B:track_005 | B:e29 @ 3.80 |  |
| g38 | 0.10 | CLOSING_START | B | B:track_009 | B:e30 @ 3.80 | active_at_first_observation=True |
| g39 | 0.15 | EGO_PATH_EXIT | B | B:track_005 | B:e31 @ 3.85 |  |
| g40 | 0.15 | TRACK_APPEARED_LEFT | B | B:track_013 | B:e32 @ 3.85 |  |
| g41 | 0.15 | TRACK_APPEARED_LEFT | B | B:track_014 | B:e33 @ 3.85 |  |
| g42 | 0.15 | EGO_PATH_ENTRY | B | B:track_002 | B:e34 @ 3.85 |  |
| g43 | 0.15 | CLOSING_START | B | B:track_008 | B:e35 @ 3.85 |  |
| g44 | 0.20 | EGO_PATH_EXIT | A | B | A:e10 @ 3.90 |  |
| g45 | 0.20 | EGO_PATH_EXIT | B | B:track_002 | B:e36 @ 3.90 |  |
| g46 | 0.20 | TRACK_APPEARED_LEFT | B | B:track_015 | B:e37 @ 3.90 |  |
| g47 | 0.20 | TRACK_APPEARED_LEFT | B | B:track_016 | B:e38 @ 3.90 |  |
| g48 | 0.20 | TRACK_APPEARED_LEFT | B | B:track_017 | B:e39 @ 3.90 |  |
| g49 | 0.20 | EGO_PATH_ENTRY | B | B:track_018 | B:e40 @ 3.90 |  |
| g50 | 0.20 | CLOSING_START | B | B:track_013 | B:e41 @ 3.90 |  |
| g51 | 0.20 | CLOSING_START | B | B:track_014 | B:e42 @ 3.90 |  |
| g52 | 0.20 | CLOSING_START | B | B:track_015 | B:e43 @ 3.90 | active_at_first_observation=True |
| g53 | 0.20 | CRITICAL_TTC_START | B | B:track_015 | B:e44 @ 3.90 | active_at_first_observation=True |
| g54 | 0.25 | EGO_PATH_EXIT | B | B:track_018 | B:e45 @ 3.95 |  |
| g55 | 0.25 | CLOSING_START | B | B:track_016 | B:e46 @ 3.95 |  |
| g56 | 0.25 | CLOSING_START | B | B:track_017 | B:e47 @ 3.95 |  |
| g57 | 0.25 | TRACK_LOST | B | B:track_006 | B:e48 @ 3.95 |  |
| g58 | 0.30 | CLOSING_END | B | B:track_002 | B:e49 @ 4.00 |  |
| g59 | 0.30 | CLOSING_END | B | B:track_005 | B:e50 @ 4.00 |  |
| g60 | 0.30 | TRACK_APPEARED_LEFT | B | B:track_019 | B:e51 @ 4.00 |  |
| g61 | 0.30 | TRACK_LOST | B | B:track_011 | B:e52 @ 4.00 |  |
| g62 | 0.35 | CLOSING_END | B | B:track_004 | B:e53 @ 4.05 |  |
| g63 | 0.35 | CLOSING_END | B | B:track_007 | B:e54 @ 4.05 |  |
| g64 | 0.35 | CLOSING_END | B | B:track_012 | B:e55 @ 4.05 |  |
| g65 | 0.35 | EGO_PATH_ENTRY | B | B:track_009 | B:e56 @ 4.05 |  |
| g66 | 0.35 | TRACK_LOST | A | B | A:e11 @ 4.05 |  |
| g67 | 0.35 | TRACK_LOST | B | B:track_003 | B:e57 @ 4.05 |  |
| g68 | 0.40 | CLOSING_END | B | B:track_009 | B:e58 @ 4.10 |  |
| g69 | 0.40 | CLOSING_END | B | B:track_018 | B:e59 @ 4.10 |  |
| g70 | 0.40 | EGO_PATH_EXIT | B | B:track_009 | B:e60 @ 4.10 |  |
| g71 | 0.40 | EGO_PATH_ENTRY | B | B:track_010 | B:e61 @ 4.10 |  |
| g72 | 0.45 | CLOSING_END | B | B:track_008 | B:e62 @ 4.15 |  |
| g73 | 0.45 | EGO_PATH_EXIT | B | B:track_010 | B:e63 @ 4.15 |  |
| g74 | 0.45 | EGO_PATH_ENTRY | B | B:track_008 | B:e64 @ 4.15 |  |
| g75 | 0.45 | TRACK_LOST | B | B:track_005 | B:e65 @ 4.15 |  |
| g76 | 0.50 | CRITICAL_TTC_END | B | B:track_015 | B:e66 @ 4.20 |  |
| g77 | 0.55 | CLOSING_END | B | B:track_013 | B:e67 @ 4.25 |  |
| g78 | 0.55 | CLOSING_END | B | B:track_015 | B:e68 @ 4.25 |  |
| g79 | 0.55 | EGO_PATH_EXIT | B | B:track_008 | B:e69 @ 4.25 |  |
| g80 | 0.55 | TURN_LEFT_END | B | - | B:e70 @ 4.25 |  |
| g81 | 0.55 | EGO_PATH_ENTRY | B | B:track_013 | B:e71 @ 4.25 |  |
| g82 | 0.55 | TRACK_LOST | B | B:track_018 | B:e72 @ 4.25 |  |
| g83 | 0.60 | CLOSING_END | B | B:track_014 | B:e73 @ 4.30 |  |
| g84 | 0.60 | CLOSING_END | B | B:track_016 | B:e74 @ 4.30 |  |
| g85 | 0.60 | CLOSING_END | B | B:track_017 | B:e75 @ 4.30 |  |
| g86 | 0.60 | MOVING_END | B | - | B:e76 @ 4.30 |  |
| g87 | 0.60 | STOP_START | B | - | B:e77 @ 4.30 |  |
| g88 | 0.85 | MOVING_END | A | - | A:e12 @ 4.55 |  |
| g89 | 0.85 | STOP_START | A | - | A:e13 @ 4.55 |  |
| g90 | 1.25 | EGO_PATH_ENTRY | B | B:track_008 | B:e78 @ 4.95 |  |
| g91 | 1.40 | EGO_PATH_EXIT | B | B:track_013 | B:e79 @ 5.10 |  |
| g92 | 3.75 | EGO_PATH_ENTRY | B | B:track_013 | B:e80 @ 7.45 |  |
| g93 | 10.70 | TRACK_LOST | B | B:track_004 | B:e81 @ 14.40 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g01 --PRECEDES--> g04
    g01 --PRECEDES--> g05
    g01 --PRECEDES--> g06
    g02 --PRECEDES--> g03
    g02 --PRECEDES--> g04
    g02 --PRECEDES--> g05
    g02 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g03 --PRECEDES--> g08
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g06 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g10 --PRECEDES--> g16
    g10 --PRECEDES--> g17
    g10 --PRECEDES--> g18
    g10 --PRECEDES--> g19
    g10 --PRECEDES--> g20
    g10 --PRECEDES--> g21
    g10 --PRECEDES--> g22
    g10 --PRECEDES--> g23
    g10 --PRECEDES--> g24
    g10 --PRECEDES--> g25
    g11 --PRECEDES--> g26
    g11 --PRECEDES--> g27
    g11 --PRECEDES--> g28
    g11 --PRECEDES--> g29
    g11 --PRECEDES--> g30
    g11 --PRECEDES--> g31
    g12 --PRECEDES--> g26
    g12 --PRECEDES--> g27
    g12 --PRECEDES--> g28
    g12 --PRECEDES--> g29
    g12 --PRECEDES--> g30
    g12 --PRECEDES--> g31
    g13 --PRECEDES--> g26
    g13 --PRECEDES--> g27
    g13 --PRECEDES--> g28
    g13 --PRECEDES--> g29
    g13 --PRECEDES--> g30
    g13 --PRECEDES--> g31
    g14 --PRECEDES--> g26
    g14 --PRECEDES--> g27
    g14 --PRECEDES--> g28
    g14 --PRECEDES--> g29
    g14 --PRECEDES--> g30
    g14 --PRECEDES--> g31
    g15 --PRECEDES--> g26
    g15 --PRECEDES--> g27
    g15 --PRECEDES--> g28
    g15 --PRECEDES--> g29
    g15 --PRECEDES--> g30
    g15 --PRECEDES--> g31
    g16 --PRECEDES--> g26
    g16 --PRECEDES--> g27
    g16 --PRECEDES--> g28
    g16 --PRECEDES--> g29
    g16 --PRECEDES--> g30
    g16 --PRECEDES--> g31
    g17 --PRECEDES--> g26
    g17 --PRECEDES--> g27
    g17 --PRECEDES--> g28
    g17 --PRECEDES--> g29
    g17 --PRECEDES--> g30
    g17 --PRECEDES--> g31
    g18 --PRECEDES--> g26
    g18 --PRECEDES--> g27
    g18 --PRECEDES--> g28
    g18 --PRECEDES--> g29
    g18 --PRECEDES--> g30
    g18 --PRECEDES--> g31
    g19 --PRECEDES--> g26
    g19 --PRECEDES--> g27
    g19 --PRECEDES--> g28
    g19 --PRECEDES--> g29
    g19 --PRECEDES--> g30
    g19 --PRECEDES--> g31
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g20 --PRECEDES--> g28
    g20 --PRECEDES--> g29
    g20 --PRECEDES--> g30
    g20 --PRECEDES--> g31
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g21 --PRECEDES--> g29
    g21 --PRECEDES--> g30
    g21 --PRECEDES--> g31
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g22 --PRECEDES--> g30
    g22 --PRECEDES--> g31
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g23 --PRECEDES--> g31
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g24 --PRECEDES--> g28
    g24 --PRECEDES--> g29
    g24 --PRECEDES--> g30
    g24 --PRECEDES--> g31
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g25 --PRECEDES--> g30
    g25 --PRECEDES--> g31
    g26 --PRECEDES--> g32
    g26 --PRECEDES--> g33
    g26 --PRECEDES--> g34
    g26 --PRECEDES--> g35
    g26 --PRECEDES--> g36
    g26 --PRECEDES--> g37
    g26 --PRECEDES--> g38
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g27 --PRECEDES--> g35
    g27 --PRECEDES--> g36
    g27 --PRECEDES--> g37
    g27 --PRECEDES--> g38
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g28 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g28 --PRECEDES--> g36
    g28 --PRECEDES--> g37
    g28 --PRECEDES--> g38
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g29 --PRECEDES--> g35
    g29 --PRECEDES--> g36
    g29 --PRECEDES--> g37
    g29 --PRECEDES--> g38
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g30 --PRECEDES--> g35
    g30 --PRECEDES--> g36
    g30 --PRECEDES--> g37
    g30 --PRECEDES--> g38
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g31 --PRECEDES--> g38
    g32 --PRECEDES--> g39
    g32 --PRECEDES--> g40
    g32 --PRECEDES--> g41
    g32 --PRECEDES--> g42
    g32 --PRECEDES--> g43
    g33 --PRECEDES--> g39
    g33 --PRECEDES--> g40
    g33 --PRECEDES--> g41
    g33 --PRECEDES--> g42
    g33 --PRECEDES--> g43
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g34 --PRECEDES--> g41
    g34 --PRECEDES--> g42
    g34 --PRECEDES--> g43
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g35 --PRECEDES--> g43
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g36 --PRECEDES--> g43
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g38 --PRECEDES--> g39
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g38 --PRECEDES--> g42
    g38 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g39 --PRECEDES--> g45
    g39 --PRECEDES--> g46
    g39 --PRECEDES--> g47
    g39 --PRECEDES--> g48
    g39 --PRECEDES--> g49
    g39 --PRECEDES--> g50
    g39 --PRECEDES--> g51
    g39 --PRECEDES--> g52
    g39 --PRECEDES--> g53
    g40 --PRECEDES--> g44
    g40 --PRECEDES--> g45
    g40 --PRECEDES--> g46
    g40 --PRECEDES--> g47
    g40 --PRECEDES--> g48
    g40 --PRECEDES--> g49
    g40 --PRECEDES--> g50
    g40 --PRECEDES--> g51
    g40 --PRECEDES--> g52
    g40 --PRECEDES--> g53
    g41 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g41 --PRECEDES--> g46
    g41 --PRECEDES--> g47
    g41 --PRECEDES--> g48
    g41 --PRECEDES--> g49
    g41 --PRECEDES--> g50
    g41 --PRECEDES--> g51
    g41 --PRECEDES--> g52
    g41 --PRECEDES--> g53
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g42 --PRECEDES--> g48
    g42 --PRECEDES--> g49
    g42 --PRECEDES--> g50
    g42 --PRECEDES--> g51
    g42 --PRECEDES--> g52
    g42 --PRECEDES--> g53
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g43 --PRECEDES--> g50
    g43 --PRECEDES--> g51
    g43 --PRECEDES--> g52
    g43 --PRECEDES--> g53
    g44 --PRECEDES--> g54
    g44 --PRECEDES--> g55
    g44 --PRECEDES--> g56
    g44 --PRECEDES--> g57
    g45 --PRECEDES--> g54
    g45 --PRECEDES--> g55
    g45 --PRECEDES--> g56
    g45 --PRECEDES--> g57
    g46 --PRECEDES--> g54
    g46 --PRECEDES--> g55
    g46 --PRECEDES--> g56
    g46 --PRECEDES--> g57
    g47 --PRECEDES--> g54
    g47 --PRECEDES--> g55
    g47 --PRECEDES--> g56
    g47 --PRECEDES--> g57
    g48 --PRECEDES--> g54
    g48 --PRECEDES--> g55
    g48 --PRECEDES--> g56
    g48 --PRECEDES--> g57
    g49 --PRECEDES--> g54
    g49 --PRECEDES--> g55
    g49 --PRECEDES--> g56
    g49 --PRECEDES--> g57
    g50 --PRECEDES--> g54
    g50 --PRECEDES--> g55
    g50 --PRECEDES--> g56
    g50 --PRECEDES--> g57
    g51 --PRECEDES--> g54
    g51 --PRECEDES--> g55
    g51 --PRECEDES--> g56
    g51 --PRECEDES--> g57
    g52 --PRECEDES--> g54
    g52 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g53 --PRECEDES--> g54
    g53 --PRECEDES--> g55
    g53 --PRECEDES--> g56
    g53 --PRECEDES--> g57
    g54 --PRECEDES--> g58
    g54 --PRECEDES--> g59
    g54 --PRECEDES--> g60
    g54 --PRECEDES--> g61
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g55 --PRECEDES--> g60
    g55 --PRECEDES--> g61
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g56 --PRECEDES--> g60
    g56 --PRECEDES--> g61
    g57 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g57 --PRECEDES--> g60
    g57 --PRECEDES--> g61
    g58 --PRECEDES--> g62
    g58 --PRECEDES--> g63
    g58 --PRECEDES--> g64
    g58 --PRECEDES--> g65
    g58 --PRECEDES--> g66
    g58 --PRECEDES--> g67
    g59 --PRECEDES--> g62
    g59 --PRECEDES--> g63
    g59 --PRECEDES--> g64
    g59 --PRECEDES--> g65
    g59 --PRECEDES--> g66
    g59 --PRECEDES--> g67
    g60 --PRECEDES--> g62
    g60 --PRECEDES--> g63
    g60 --PRECEDES--> g64
    g60 --PRECEDES--> g65
    g60 --PRECEDES--> g66
    g60 --PRECEDES--> g67
    g61 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g61 --PRECEDES--> g64
    g61 --PRECEDES--> g65
    g61 --PRECEDES--> g66
    g61 --PRECEDES--> g67
    g62 --PRECEDES--> g68
    g62 --PRECEDES--> g69
    g62 --PRECEDES--> g70
    g62 --PRECEDES--> g71
    g63 --PRECEDES--> g68
    g63 --PRECEDES--> g69
    g63 --PRECEDES--> g70
    g63 --PRECEDES--> g71
    g64 --PRECEDES--> g68
    g64 --PRECEDES--> g69
    g64 --PRECEDES--> g70
    g64 --PRECEDES--> g71
    g65 --PRECEDES--> g68
    g65 --PRECEDES--> g69
    g65 --PRECEDES--> g70
    g65 --PRECEDES--> g71
    g66 --PRECEDES--> g68
    g66 --PRECEDES--> g69
    g66 --PRECEDES--> g70
    g66 --PRECEDES--> g71
    g67 --PRECEDES--> g68
    g67 --PRECEDES--> g69
    g67 --PRECEDES--> g70
    g67 --PRECEDES--> g71
    g68 --PRECEDES--> g72
    g68 --PRECEDES--> g73
    g68 --PRECEDES--> g74
    g68 --PRECEDES--> g75
    g69 --PRECEDES--> g72
    g69 --PRECEDES--> g73
    g69 --PRECEDES--> g74
    g69 --PRECEDES--> g75
    g70 --PRECEDES--> g72
    g70 --PRECEDES--> g73
    g70 --PRECEDES--> g74
    g70 --PRECEDES--> g75
    g71 --PRECEDES--> g72
    g71 --PRECEDES--> g73
    g71 --PRECEDES--> g74
    g71 --PRECEDES--> g75
    g72 --PRECEDES--> g76
    g73 --PRECEDES--> g76
    g74 --PRECEDES--> g76
    g75 --PRECEDES--> g76
    g76 --PRECEDES--> g77
    g76 --PRECEDES--> g78
    g76 --PRECEDES--> g79
    g76 --PRECEDES--> g80
    g76 --PRECEDES--> g81
    g76 --PRECEDES--> g82
    g77 --PRECEDES--> g83
    g77 --PRECEDES--> g84
    g77 --PRECEDES--> g85
    g77 --PRECEDES--> g86
    g77 --PRECEDES--> g87
    g78 --PRECEDES--> g83
    g78 --PRECEDES--> g84
    g78 --PRECEDES--> g85
    g78 --PRECEDES--> g86
    g78 --PRECEDES--> g87
    g79 --PRECEDES--> g83
    g79 --PRECEDES--> g84
    g79 --PRECEDES--> g85
    g79 --PRECEDES--> g86
    g79 --PRECEDES--> g87
    g80 --PRECEDES--> g83
    g80 --PRECEDES--> g84
    g80 --PRECEDES--> g85
    g80 --PRECEDES--> g86
    g80 --PRECEDES--> g87
    g81 --PRECEDES--> g83
    g81 --PRECEDES--> g84
    g81 --PRECEDES--> g85
    g81 --PRECEDES--> g86
    g81 --PRECEDES--> g87
    g82 --PRECEDES--> g83
    g82 --PRECEDES--> g84
    g82 --PRECEDES--> g85
    g82 --PRECEDES--> g86
    g82 --PRECEDES--> g87
    g83 --PRECEDES--> g88
    g83 --PRECEDES--> g89
    g84 --PRECEDES--> g88
    g84 --PRECEDES--> g89
    g85 --PRECEDES--> g88
    g85 --PRECEDES--> g89
    g86 --PRECEDES--> g88
    g86 --PRECEDES--> g89
    g87 --PRECEDES--> g88
    g87 --PRECEDES--> g89
    g88 --PRECEDES--> g90
    g89 --PRECEDES--> g90
    g90 --PRECEDES--> g91
    g91 --PRECEDES--> g92
    g92 --PRECEDES--> g93
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g10
    g04 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g44
    g04 --SAME_TRACK--> g66
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g15 --SAME_TRACK--> g21
    g17 --SAME_TRACK--> g22
    g18 --SAME_TRACK--> g23
    g19 --SAME_TRACK--> g24
    g20 --SAME_TRACK--> g25
    g16 --SAME_TRACK--> g30
    g28 --SAME_TRACK--> g31
    g16 --SAME_TRACK--> g32
    g18 --SAME_TRACK--> g37
    g34 --SAME_TRACK--> g38
    g18 --SAME_TRACK--> g39
    g15 --SAME_TRACK--> g42
    g33 --SAME_TRACK--> g43
    g15 --SAME_TRACK--> g45
    g20 --SAME_TRACK--> g49
    g40 --SAME_TRACK--> g50
    g41 --SAME_TRACK--> g51
    g46 --SAME_TRACK--> g52
    g46 --SAME_TRACK--> g53
    g20 --SAME_TRACK--> g54
    g47 --SAME_TRACK--> g55
    g48 --SAME_TRACK--> g56
    g29 --SAME_TRACK--> g57
    g15 --SAME_TRACK--> g58
    g18 --SAME_TRACK--> g59
    g36 --SAME_TRACK--> g61
    g17 --SAME_TRACK--> g62
    g19 --SAME_TRACK--> g63
    g28 --SAME_TRACK--> g64
    g34 --SAME_TRACK--> g65
    g16 --SAME_TRACK--> g67
    g34 --SAME_TRACK--> g68
    g20 --SAME_TRACK--> g69
    g34 --SAME_TRACK--> g70
    g35 --SAME_TRACK--> g71
    g33 --SAME_TRACK--> g72
    g35 --SAME_TRACK--> g73
    g33 --SAME_TRACK--> g74
    g18 --SAME_TRACK--> g75
    g46 --SAME_TRACK--> g76
    g40 --SAME_TRACK--> g77
    g46 --SAME_TRACK--> g78
    g33 --SAME_TRACK--> g79
    g40 --SAME_TRACK--> g81
    g20 --SAME_TRACK--> g82
    g41 --SAME_TRACK--> g83
    g47 --SAME_TRACK--> g84
    g48 --SAME_TRACK--> g85
    g33 --SAME_TRACK--> g90
    g40 --SAME_TRACK--> g91
    g40 --SAME_TRACK--> g92
    g17 --SAME_TRACK--> g93
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.70 | MOVING_START(A); MOVING_START(B) |
| -2.50 | TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A) |
| -2.05 | CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -0.35 | TRACK_LOST(B,A) |
| -0.25 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TURN_LEFT_START(B); TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_018); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_018) |
| +0.05 | BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_006); EGO_PATH_ENTRY(B,B:track_003); CLOSING_START(B,B:track_012) |
| +0.10 | EGO_PATH_EXIT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_008); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_RIGHT(B,B:track_011); EGO_PATH_ENTRY(B,B:track_005); CLOSING_START(B,B:track_009) |
| +0.15 | EGO_PATH_EXIT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_LEFT(B,B:track_014); EGO_PATH_ENTRY(B,B:track_002); CLOSING_START(B,B:track_008) |
| +0.20 | EGO_PATH_EXIT(A,B); EGO_PATH_EXIT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_017); EGO_PATH_ENTRY(B,B:track_018); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_015); CRITICAL_TTC_START(B,B:track_015) |
| +0.25 | EGO_PATH_EXIT(B,B:track_018); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_017); TRACK_LOST(B,B:track_006) |
| +0.30 | CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_LOST(B,B:track_011) |
| +0.35 | CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_007); CLOSING_END(B,B:track_012); EGO_PATH_ENTRY(B,B:track_009); TRACK_LOST(A,B); TRACK_LOST(B,B:track_003) |
| +0.40 | CLOSING_END(B,B:track_009); CLOSING_END(B,B:track_018); EGO_PATH_EXIT(B,B:track_009); EGO_PATH_ENTRY(B,B:track_010) |
| +0.45 | CLOSING_END(B,B:track_008); EGO_PATH_EXIT(B,B:track_010); EGO_PATH_ENTRY(B,B:track_008); TRACK_LOST(B,B:track_005) |
| +0.50 | CRITICAL_TTC_END(B,B:track_015) |
| +0.55 | CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_015); EGO_PATH_EXIT(B,B:track_008); TURN_LEFT_END(B); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_018) |
| +0.60 | CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_016); CLOSING_END(B,B:track_017); MOVING_END(B); STOP_START(B) |
| +0.85 | MOVING_END(A); STOP_START(A) |
| +1.25 | EGO_PATH_ENTRY(B,B:track_008) |
| +1.40 | EGO_PATH_EXIT(B,B:track_013) |
| +3.75 | EGO_PATH_ENTRY(B,B:track_013) |
| +10.70 | TRACK_LOST(B,B:track_004) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 1.65, COLLISION 3.70 (+2.05 s); EGO_PATH_ENTRY 3.45 after critical TTC (+1.80 s) [local times; t_global: critical_ttc_start -2.05, ego_path_entry -0.25, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 1.65, COLLISION 3.70 (+2.05 s) [local times; t_global: critical_ttc_start -2.05, collision +0.00]
- B's track_002 (unidentified B:track_002): EGO_PATH_ENTRY 3.85, no critical TTC [local times; t_global: ego_path_entry +0.15, collision +0.00]
- B's track_003 (unidentified B:track_003): EGO_PATH_ENTRY 3.75, no critical TTC [local times; t_global: ego_path_entry +0.05, collision +0.00]
- B's track_005 (unidentified B:track_005): EGO_PATH_ENTRY 3.80, no critical TTC [local times; t_global: ego_path_entry +0.10, collision +0.00]
- B's track_008 (unidentified B:track_008): EGO_PATH_ENTRY 4.15, no critical TTC [local times; t_global: ego_path_entry +0.45, collision +0.00]
- B's track_009 (unidentified B:track_009): EGO_PATH_ENTRY 4.05, no critical TTC [local times; t_global: ego_path_entry +0.35, collision +0.00]
- B's track_010 (unidentified B:track_010): EGO_PATH_ENTRY 4.10, no critical TTC [local times; t_global: ego_path_entry +0.40, collision +0.00]
- B's track_013 (unidentified B:track_013): EGO_PATH_ENTRY 4.25, no critical TTC [local times; t_global: ego_path_entry +0.55, collision +0.00]
- B's track_015 (unidentified B:track_015): CRITICAL_TTC_START 3.90, COLLISION 3.70 (+-0.20 s) [local times; t_global: critical_ttc_start +0.20, collision +0.00]
- B's track_018 (unidentified B:track_018): EGO_PATH_ENTRY 3.90, no critical TTC [local times; t_global: ego_path_entry +0.20, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.70 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -3.70 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -2.50 | B | g03 TRACK_APPEARED_LEFT(B,A) (B:e02)<br>g06 CLOSING_START(B,A) (B:e03) | ego: MOVING |
| -2.50 | A | g04 TRACK_APPEARED_RIGHT(A,B) (A:e02)<br>g05 CLOSING_START(A,B) (A:e03) | ego: MOVING |
| -2.05 | A | g07 CRITICAL_TTC_START(A,B) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -2.05 | B | g08 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -0.35 | B | g09 TRACK_LOST(B,A) (B:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| -0.25 | A | g10 EGO_PATH_ENTRY(A,B) (A:e05) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC |
| +0.00 | A | g11 COLLISION(A,B) (A:e06)<br>g12 CRITICAL_TTC_END(A,B) (A:e07)<br>g13 CLOSING_END(A,B) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | B | g11 COLLISION(A,B) (B:e06)<br>g14 TURN_LEFT_START(B) (B:e07)<br>g15 TRACK_APPEARED_LEFT(B,B:track_002) (B:e08)<br>g16 TRACK_APPEARED_LEFT(B,B:track_003) (B:e09)<br>g17 TRACK_APPEARED_LEFT(B,B:track_004) (B:e10)<br>g18 TRACK_APPEARED_LEFT(B,B:track_005) (B:e11)<br>g19 TRACK_APPEARED_LEFT(B,B:track_007) (B:e12)<br>g20 TRACK_APPEARED_LEFT(B,B:track_018) (B:e13)<br>g21 CLOSING_START(B,B:track_002) (B:e14)<br>g22 CLOSING_START(B,B:track_004) (B:e15)<br>g23 CLOSING_START(B,B:track_005) (B:e16)<br>g24 CLOSING_START(B,B:track_007) (B:e17)<br>g25 CLOSING_START(B,B:track_018) (B:e18) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| +0.05 | A | g26 BRAKE_START(A) (A:e09) | ego: MOVING<br>track_001: IN_EGO_PATH |
| +0.05 | B | g27 BRAKE_START(B) (B:e19)<br>g28 TRACK_APPEARED_LEFT(B,B:track_012) (B:e20)<br>g29 TRACK_APPEARED_RIGHT(B,B:track_006) (B:e21)<br>g30 EGO_PATH_ENTRY(B,B:track_003) (B:e22)<br>g31 CLOSING_START(B,B:track_012) (B:e23) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.10 | B | g32 EGO_PATH_EXIT(B,B:track_003) (B:e24)<br>g33 TRACK_APPEARED_LEFT(B,B:track_008) (B:e25)<br>g34 TRACK_APPEARED_LEFT(B,B:track_009) (B:e26)<br>g35 TRACK_APPEARED_LEFT(B,B:track_010) (B:e27)<br>g36 TRACK_APPEARED_RIGHT(B,B:track_011) (B:e28)<br>g37 EGO_PATH_ENTRY(B,B:track_005) (B:e29)<br>g38 CLOSING_START(B,B:track_009) (B:e30) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: IN_EGO_PATH, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_012: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.15 | B | g39 EGO_PATH_EXIT(B,B:track_005) (B:e31)<br>g40 TRACK_APPEARED_LEFT(B,B:track_013) (B:e32)<br>g41 TRACK_APPEARED_LEFT(B,B:track_014) (B:e33)<br>g42 EGO_PATH_ENTRY(B,B:track_002) (B:e34)<br>g43 CLOSING_START(B,B:track_008) (B:e35) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: no active state<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.20 | A | g44 EGO_PATH_EXIT(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.20 | B | g45 EGO_PATH_EXIT(B,B:track_002) (B:e36)<br>g46 TRACK_APPEARED_LEFT(B,B:track_015) (B:e37)<br>g47 TRACK_APPEARED_LEFT(B,B:track_016) (B:e38)<br>g48 TRACK_APPEARED_LEFT(B,B:track_017) (B:e39)<br>g49 EGO_PATH_ENTRY(B,B:track_018) (B:e40)<br>g50 CLOSING_START(B,B:track_013) (B:e41)<br>g51 CLOSING_START(B,B:track_014) (B:e42)<br>g52 CLOSING_START(B,B:track_015) (B:e43)<br>g53 CRITICAL_TTC_START(B,B:track_015) (B:e44) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING, IN_EGO_PATH<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: no active state<br>track_014: no active state<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001 |
| +0.25 | B | g54 EGO_PATH_EXIT(B,B:track_018) (B:e45)<br>g55 CLOSING_START(B,B:track_016) (B:e46)<br>g56 CLOSING_START(B,B:track_017) (B:e47)<br>g57 TRACK_LOST(B,B:track_006) (B:e48) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: no active state<br>track_017: no active state<br>track_018: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +0.30 | B | g58 CLOSING_END(B,B:track_002) (B:e49)<br>g59 CLOSING_END(B,B:track_005) (B:e50)<br>g60 TRACK_APPEARED_LEFT(B,B:track_019) (B:e51)<br>g61 TRACK_LOST(B,B:track_011) (B:e52) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track lost, states UNKNOWN: track_001, track_006 |
| +0.35 | B | g62 CLOSING_END(B,B:track_004) (B:e53)<br>g63 CLOSING_END(B,B:track_007) (B:e54)<br>g64 CLOSING_END(B,B:track_012) (B:e55)<br>g65 EGO_PATH_ENTRY(B,B:track_009) (B:e56)<br>g67 TRACK_LOST(B,B:track_003) (B:e57) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track_003: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_004: CLOSING<br>track_005: no active state<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_012: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_006, track_011 |
| +0.35 | A | g66 TRACK_LOST(A,B) (A:e11) | ego: MOVING, BRAKE<br>track_001: no active state |
| +0.40 | B | g68 CLOSING_END(B,B:track_009) (B:e58)<br>g69 CLOSING_END(B,B:track_018) (B:e59)<br>g70 EGO_PATH_EXIT(B,B:track_009) (B:e60)<br>g71 EGO_PATH_ENTRY(B,B:track_010) (B:e61) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track_009: CLOSING, IN_EGO_PATH<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_006, track_011 |
| +0.45 | B | g72 CLOSING_END(B,B:track_008) (B:e62)<br>g73 EGO_PATH_EXIT(B,B:track_010) (B:e63)<br>g74 EGO_PATH_ENTRY(B,B:track_008) (B:e64)<br>g75 TRACK_LOST(B,B:track_005) (B:e65) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: CLOSING<br>track_009: no active state<br>track_010: IN_EGO_PATH<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_006, track_011 |
| +0.50 | B | g76 CRITICAL_TTC_END(B,B:track_015) (B:e66) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING, CRITICAL_TTC<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011 |
| +0.55 | B | g77 CLOSING_END(B,B:track_013) (B:e67)<br>g78 CLOSING_END(B,B:track_015) (B:e68)<br>g79 EGO_PATH_EXIT(B,B:track_008) (B:e69)<br>g80 TURN_LEFT_END(B) (B:e70)<br>g81 EGO_PATH_ENTRY(B,B:track_013) (B:e71)<br>g82 TRACK_LOST(B,B:track_018) (B:e72) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011 |
| +0.60 | B | g83 CLOSING_END(B,B:track_014) (B:e73)<br>g84 CLOSING_END(B,B:track_016) (B:e74)<br>g85 CLOSING_END(B,B:track_017) (B:e75)<br>g86 MOVING_END(B) (B:e76)<br>g87 STOP_START(B) (B:e77) | ego: MOVING, BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: CLOSING<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +0.85 | A | g88 MOVING_END(A) (A:e12)<br>g89 STOP_START(A) (A:e13) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 |
| +1.25 | B | g90 EGO_PATH_ENTRY(B,B:track_008) (B:e78) | ego: STOP, BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +1.40 | B | g91 EGO_PATH_EXIT(B,B:track_013) (B:e79) | ego: STOP, BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +3.75 | B | g92 EGO_PATH_ENTRY(B,B:track_013) (B:e80) | ego: STOP, BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |
| +10.70 | B | g93 TRACK_LOST(B,B:track_004) (B:e81) | ego: STOP, BRAKE<br>track_002: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: IN_EGO_PATH<br>track_009: no active state<br>track_010: no active state<br>track_012: no active state<br>track_013: IN_EGO_PATH<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_019: no active state<br>track lost, states UNKNOWN: track_001, track_003, track_005, track_006, track_011, track_018 |

## Plain-language reading

- 3.70 s before the matched collision, A started moving (already the case when first observed).
- 3.70 s before the matched collision, B started moving (already the case when first observed).
- 2.50 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 2.50 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 2.50 s before the matched collision, A observed B start closing in (already the case when first observed).
- 2.50 s before the matched collision, B observed A start closing in (already the case when first observed).
- 2.05 s before the matched collision, A's time-to-contact with B became critical.
- 2.05 s before the matched collision, B's time-to-contact with A became critical.
- 0.35 s before the matched collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.25 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6116, B: 6116 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- At the matched collision, B started turning left.
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
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
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
- 0.55 s after the matched collision, B stopped turning left.
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
