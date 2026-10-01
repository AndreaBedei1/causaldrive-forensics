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
| B:track_017 | anonymous_track | seen only by B; candidate: A |
| B:track_018 | anonymous_track | seen only by B; candidate: A |
| B:track_019 | anonymous_track | seen only by B; candidate: A |
| B:track_020 | anonymous_track | seen only by B; candidate: A |
| B:track_021 | anonymous_track | seen only by B; candidate: A |
| B:track_022 | anonymous_track | seen only by B; candidate: A |
| B:track_023 | anonymous_track | seen only by B; candidate: A |
| B:track_024 | anonymous_track | seen only by B; candidate: A |
| B:track_025 | anonymous_track | seen only by B; candidate: A |
| B:track_026 | anonymous_track | seen only by B; candidate: A |
| B:track_027 | anonymous_track | seen only by B; candidate: A |
| B:track_028 | anonymous_track | seen only by B; candidate: A |
| B:track_029 | anonymous_track | seen only by B; candidate: A |
| B:track_030 | anonymous_track | seen only by B; candidate: A |
| B:track_031 | anonymous_track | seen only by B; candidate: A |
| B:track_032 | anonymous_track | seen only by B; candidate: A |
| B:track_033 | anonymous_track | seen only by B; candidate: A |
| B:track_034 | anonymous_track | seen only by B; candidate: A |
| B:track_035 | anonymous_track | seen only by B; candidate: A |
| B:track_036 | anonymous_track | seen only by B; candidate: A |
| B:track_037 | anonymous_track | seen only by B; candidate: A |
| B:track_038 | anonymous_track | seen only by B; candidate: A |
| B:track_039 | anonymous_track | seen only by B; candidate: A |
| B:track_040 | anonymous_track | seen only by B; candidate: A |
| B:track_041 | anonymous_track | seen only by B; candidate: A |
| B:track_042 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 5.65 | -5.65 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 5.65 | -5.65 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5215.85 vs 5215.85 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 5.50 s before the matched collision<br>lost 4.90 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 32.7 m -> 30.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision |
| A:track_002 | B | ASSOCIATED | 0.93 | A and B both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 2.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 8.4 m -> 1.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.55 m/s over 2.3 s<br>range at the contact 1.45 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.25 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.25 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.25 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.30 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.40 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.50 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.50 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.50 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_015 | B:track_015 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_016 | B:track_016 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.50 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_017 | B:track_017 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_018 | B:track_018 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_019 | B:track_019 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_020 | B:track_020 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_021 | B:track_021 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.50 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_022 | B:track_022 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.25 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_023 | B:track_023 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_024 | B:track_024 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_025 | B:track_025 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_026 | B:track_026 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_027 | B:track_027 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_028 | B:track_028 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_029 | B:track_029 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_030 | B:track_030 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_031 | B:track_031 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_032 | B:track_032 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_033 | B:track_033 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_034 | B:track_034 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_035 | B:track_035 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_036 | B:track_036 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_037 | B:track_037 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_038 | B:track_038 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.85 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_039 | B:track_039 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.85 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_040 | B:track_040 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_041 | B:track_041 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_042 | B:track_042 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.85 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.65 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.65 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.50 | TRACK_APPEARED_LEFT | A | A:track_001 | A:e02 @ 0.15 |  |
| g04 | -5.50 | CLOSING_START | A | A:track_001 | A:e03 @ 0.15 | active_at_first_observation=True |
| g05 | -4.90 | TRACK_LOST | A | A:track_001 | A:e04 @ 0.75 |  |
| g06 | -4.85 | BRAKE_START | B | - | B:e02 @ 0.80 |  |
| g07 | -2.90 | SPEED_LIMIT_EXCEEDED_START | A | - | A:e05 @ 2.75 |  |
| g08 | -2.30 | TRACK_APPEARED_LEFT | A | B | A:e06 @ 3.35 |  |
| g09 | -2.30 | CLOSING_START | A | B | A:e07 @ 3.35 | active_at_first_observation=True |
| g10 | -1.80 | CUT_IN_FROM_LEFT_START | A | B | A:e08 @ 3.85 |  |
| g11 | -1.65 | CRITICAL_TTC_START | A | B | A:e09 @ 4.00 |  |
| g12 | -0.20 | EGO_PATH_ENTRY | A | B | A:e10 @ 5.45 |  |
| g13 | 0.00 | COLLISION | - | A, B | A:e11 @ 5.65, B:e03 @ 5.65 | matched_event=collision_001; reference_event=True; peak_impulse=A 5215.85, B 5215.85 |
| g14 | 0.00 | SPEED_LIMIT_EXCEEDED_END | A | - | A:e12 @ 5.65 |  |
| g15 | 0.05 | BRAKE_START | A | - | A:e13 @ 5.70 |  |
| g16 | 0.10 | TURN_RIGHT_START | B | - | B:e04 @ 5.75 |  |
| g17 | 0.20 | CRITICAL_TTC_END | A | B | A:e14 @ 5.85 |  |
| g18 | 0.25 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e05 @ 5.90 |  |
| g19 | 0.25 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e06 @ 5.90 |  |
| g20 | 0.25 | TRACK_APPEARED_RIGHT | B | B:track_003 | B:e07 @ 5.90 |  |
| g21 | 0.25 | TRACK_APPEARED_RIGHT | B | B:track_022 | B:e08 @ 5.90 |  |
| g22 | 0.25 | CLOSING_START | B | B:track_001 | B:e09 @ 5.90 | active_at_first_observation=True |
| g23 | 0.25 | CLOSING_START | B | B:track_002 | B:e10 @ 5.90 | active_at_first_observation=True |
| g24 | 0.25 | CLOSING_START | B | B:track_003 | B:e11 @ 5.90 | active_at_first_observation=True |
| g25 | 0.25 | CLOSING_START | B | B:track_022 | B:e12 @ 5.90 | active_at_first_observation=True |
| g26 | 0.30 | TRACK_APPEARED_LEFT | B | B:track_004 | B:e13 @ 5.95 |  |
| g27 | 0.30 | TRACK_APPEARED_RIGHT | B | B:track_005 | B:e14 @ 5.95 |  |
| g28 | 0.30 | TRACK_APPEARED_RIGHT | B | B:track_006 | B:e15 @ 5.95 |  |
| g29 | 0.30 | CLOSING_START | B | B:track_004 | B:e16 @ 5.95 | active_at_first_observation=True |
| g30 | 0.30 | CLOSING_START | B | B:track_005 | B:e17 @ 5.95 | active_at_first_observation=True |
| g31 | 0.30 | CLOSING_START | B | B:track_006 | B:e18 @ 5.95 | active_at_first_observation=True |
| g32 | 0.40 | TRACK_APPEARED_LEFT | B | B:track_007 | B:e19 @ 6.05 |  |
| g33 | 0.40 | TRACK_APPEARED_LEFT | B | B:track_009 | B:e20 @ 6.05 |  |
| g34 | 0.40 | TRACK_APPEARED_RIGHT | B | B:track_008 | B:e21 @ 6.05 |  |
| g35 | 0.40 | CLOSING_START | B | B:track_007 | B:e22 @ 6.05 | active_at_first_observation=True |
| g36 | 0.40 | CLOSING_START | B | B:track_008 | B:e23 @ 6.05 | active_at_first_observation=True |
| g37 | 0.40 | CLOSING_START | B | B:track_009 | B:e24 @ 6.05 | active_at_first_observation=True |
| g38 | 0.45 | TRACK_APPEARED_LEFT | B | B:track_010 | B:e25 @ 6.10 |  |
| g39 | 0.45 | TRACK_APPEARED_LEFT | B | B:track_011 | B:e26 @ 6.10 |  |
| g40 | 0.45 | TRACK_APPEARED_LEFT | B | B:track_015 | B:e27 @ 6.10 |  |
| g41 | 0.45 | TRACK_APPEARED_RIGHT | B | B:track_020 | B:e28 @ 6.10 |  |
| g42 | 0.45 | TRACK_APPEARED_RIGHT | B | B:track_029 | B:e29 @ 6.10 |  |
| g43 | 0.45 | CLOSING_START | B | B:track_010 | B:e30 @ 6.10 | active_at_first_observation=True |
| g44 | 0.45 | CLOSING_START | B | B:track_011 | B:e31 @ 6.10 | active_at_first_observation=True |
| g45 | 0.45 | CLOSING_START | B | B:track_015 | B:e32 @ 6.10 | active_at_first_observation=True |
| g46 | 0.45 | CLOSING_START | B | B:track_020 | B:e33 @ 6.10 | active_at_first_observation=True |
| g47 | 0.45 | CLOSING_START | B | B:track_029 | B:e34 @ 6.10 | active_at_first_observation=True |
| g48 | 0.50 | TRACK_APPEARED_LEFT | B | B:track_014 | B:e35 @ 6.15 |  |
| g49 | 0.50 | TRACK_APPEARED_LEFT | B | B:track_016 | B:e36 @ 6.15 |  |
| g50 | 0.50 | TRACK_APPEARED_LEFT | B | B:track_021 | B:e37 @ 6.15 |  |
| g51 | 0.50 | TRACK_APPEARED_RIGHT | B | B:track_012 | B:e38 @ 6.15 |  |
| g52 | 0.50 | TRACK_APPEARED_RIGHT | B | B:track_013 | B:e39 @ 6.15 |  |
| g53 | 0.50 | CLOSING_START | B | B:track_012 | B:e40 @ 6.15 | active_at_first_observation=True |
| g54 | 0.50 | CLOSING_START | B | B:track_013 | B:e41 @ 6.15 | active_at_first_observation=True |
| g55 | 0.50 | CLOSING_START | B | B:track_014 | B:e42 @ 6.15 | active_at_first_observation=True |
| g56 | 0.50 | CLOSING_START | B | B:track_016 | B:e43 @ 6.15 | active_at_first_observation=True |
| g57 | 0.50 | CLOSING_START | B | B:track_021 | B:e44 @ 6.15 | active_at_first_observation=True |
| g58 | 0.50 | CRITICAL_TTC_START | B | B:track_012 | B:e45 @ 6.15 | active_at_first_observation=True |
| g59 | 0.50 | CRITICAL_TTC_START | B | B:track_013 | B:e46 @ 6.15 | active_at_first_observation=True |
| g60 | 0.55 | TRACK_APPEARED_LEFT | B | B:track_017 | B:e47 @ 6.20 |  |
| g61 | 0.55 | TRACK_APPEARED_LEFT | B | B:track_018 | B:e48 @ 6.20 |  |
| g62 | 0.55 | TRACK_APPEARED_LEFT | B | B:track_019 | B:e49 @ 6.20 |  |
| g63 | 0.55 | TRACK_APPEARED_LEFT | B | B:track_026 | B:e50 @ 6.20 |  |
| g64 | 0.55 | CLOSING_START | B | B:track_017 | B:e51 @ 6.20 | active_at_first_observation=True |
| g65 | 0.55 | CLOSING_START | B | B:track_018 | B:e52 @ 6.20 | active_at_first_observation=True |
| g66 | 0.55 | CLOSING_START | B | B:track_019 | B:e53 @ 6.20 | active_at_first_observation=True |
| g67 | 0.55 | CLOSING_START | B | B:track_026 | B:e54 @ 6.20 | active_at_first_observation=True |
| g68 | 0.60 | TRACK_LOST | B | B:track_004 | B:e55 @ 6.25 |  |
| g69 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_023 | B:e56 @ 6.30 |  |
| g70 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_024 | B:e57 @ 6.30 |  |
| g71 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_025 | B:e58 @ 6.30 |  |
| g72 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_027 | B:e59 @ 6.30 |  |
| g73 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_030 | B:e60 @ 6.30 |  |
| g74 | 0.65 | TRACK_APPEARED_LEFT | B | B:track_031 | B:e61 @ 6.30 |  |
| g75 | 0.65 | CLOSING_START | B | B:track_023 | B:e62 @ 6.30 | active_at_first_observation=True |
| g76 | 0.65 | CLOSING_START | B | B:track_024 | B:e63 @ 6.30 | active_at_first_observation=True |
| g77 | 0.65 | CLOSING_START | B | B:track_025 | B:e64 @ 6.30 | active_at_first_observation=True |
| g78 | 0.65 | CLOSING_START | B | B:track_027 | B:e65 @ 6.30 | active_at_first_observation=True |
| g79 | 0.65 | CLOSING_START | B | B:track_030 | B:e66 @ 6.30 | active_at_first_observation=True |
| g80 | 0.65 | CLOSING_START | B | B:track_031 | B:e67 @ 6.30 | active_at_first_observation=True |
| g81 | 0.65 | TRACK_LOST | B | B:track_002 | B:e68 @ 6.30 |  |
| g82 | 0.65 | TRACK_LOST | B | B:track_007 | B:e69 @ 6.30 |  |
| g83 | 0.65 | TRACK_LOST | B | B:track_008 | B:e70 @ 6.30 |  |
| g84 | 0.65 | TRACK_LOST | B | B:track_009 | B:e71 @ 6.30 |  |
| g85 | 0.70 | TRACK_APPEARED_LEFT | B | B:track_028 | B:e72 @ 6.35 |  |
| g86 | 0.70 | CLOSING_START | B | B:track_028 | B:e73 @ 6.35 | active_at_first_observation=True |
| g87 | 0.75 | TRACK_APPEARED_LEFT | B | B:track_032 | B:e74 @ 6.40 |  |
| g88 | 0.75 | TRACK_APPEARED_LEFT | B | B:track_033 | B:e75 @ 6.40 |  |
| g89 | 0.75 | TRACK_APPEARED_LEFT | B | B:track_034 | B:e76 @ 6.40 |  |
| g90 | 0.75 | TRACK_APPEARED_LEFT | B | B:track_036 | B:e77 @ 6.40 |  |
| g91 | 0.75 | TRACK_APPEARED_LEFT | B | B:track_037 | B:e78 @ 6.40 |  |
| g92 | 0.75 | TRACK_APPEARED_LEFT | B | B:track_040 | B:e79 @ 6.40 |  |
| g93 | 0.75 | TRACK_APPEARED_RIGHT | B | B:track_035 | B:e80 @ 6.40 |  |
| g94 | 0.75 | CLOSING_START | B | B:track_032 | B:e81 @ 6.40 | active_at_first_observation=True |
| g95 | 0.75 | CLOSING_START | B | B:track_033 | B:e82 @ 6.40 | active_at_first_observation=True |
| g96 | 0.75 | CLOSING_START | B | B:track_034 | B:e83 @ 6.40 | active_at_first_observation=True |
| g97 | 0.75 | CLOSING_START | B | B:track_035 | B:e84 @ 6.40 | active_at_first_observation=True |
| g98 | 0.75 | CLOSING_START | B | B:track_036 | B:e85 @ 6.40 | active_at_first_observation=True |
| g99 | 0.75 | CLOSING_START | B | B:track_037 | B:e86 @ 6.40 | active_at_first_observation=True |
| g100 | 0.75 | CLOSING_START | B | B:track_040 | B:e87 @ 6.40 | active_at_first_observation=True |
| g101 | 0.75 | CRITICAL_TTC_START | A | B | A:e15 @ 6.40 |  |
| g102 | 0.75 | TRACK_LOST | B | B:track_010 | B:e88 @ 6.40 |  |
| g103 | 0.75 | TRACK_LOST | B | B:track_011 | B:e89 @ 6.40 |  |
| g104 | 0.80 | TRACK_APPEARED_LEFT | B | B:track_041 | B:e90 @ 6.45 |  |
| g105 | 0.80 | CLOSING_START | B | B:track_041 | B:e91 @ 6.45 | active_at_first_observation=True |
| g106 | 0.80 | TRACK_LOST | B | B:track_014 | B:e92 @ 6.45 |  |
| g107 | 0.80 | TRACK_LOST | B | B:track_015 | B:e93 @ 6.45 |  |
| g108 | 0.80 | TRACK_LOST | B | B:track_021 | B:e94 @ 6.45 |  |
| g109 | 0.85 | TRACK_APPEARED_LEFT | B | B:track_038 | B:e95 @ 6.50 |  |
| g110 | 0.85 | TRACK_APPEARED_LEFT | B | B:track_039 | B:e96 @ 6.50 |  |
| g111 | 0.85 | TRACK_APPEARED_LEFT | B | B:track_042 | B:e97 @ 6.50 |  |
| g112 | 0.85 | CLOSING_START | B | B:track_038 | B:e98 @ 6.50 | active_at_first_observation=True |
| g113 | 0.85 | CLOSING_START | B | B:track_039 | B:e99 @ 6.50 | active_at_first_observation=True |
| g114 | 0.85 | CLOSING_START | B | B:track_042 | B:e100 @ 6.50 | active_at_first_observation=True |
| g115 | 0.85 | TRACK_LOST | B | B:track_016 | B:e101 @ 6.50 |  |
| g116 | 0.85 | TRACK_LOST | B | B:track_018 | B:e102 @ 6.50 |  |
| g117 | 0.90 | TRACK_LOST | B | B:track_019 | B:e103 @ 6.55 |  |
| g118 | 0.90 | TRACK_LOST | B | B:track_026 | B:e104 @ 6.55 |  |
| g119 | 0.95 | TRACK_LOST | B | B:track_017 | B:e105 @ 6.60 |  |
| g120 | 0.95 | TRACK_LOST | B | B:track_023 | B:e106 @ 6.60 |  |
| g121 | 0.95 | TRACK_LOST | B | B:track_027 | B:e107 @ 6.60 |  |
| g122 | 1.00 | CRITICAL_TTC_END | B | B:track_013 | B:e108 @ 6.65 |  |
| g123 | 1.00 | EGO_PATH_ENTRY | B | B:track_012 | B:e109 @ 6.65 |  |
| g124 | 1.00 | EGO_PATH_ENTRY | B | B:track_013 | B:e110 @ 6.65 |  |
| g125 | 1.00 | TRACK_LOST | B | B:track_033 | B:e111 @ 6.65 |  |
| g126 | 1.05 | CLOSING_END | B | B:track_024 | B:e112 @ 6.70 |  |
| g127 | 1.05 | CLOSING_END | B | B:track_031 | B:e113 @ 6.70 |  |
| g128 | 1.05 | CLOSING_END | B | B:track_034 | B:e114 @ 6.70 |  |
| g129 | 1.05 | TRACK_LOST | B | B:track_024 | B:e115 @ 6.70 |  |
| g130 | 1.05 | TRACK_LOST | B | B:track_031 | B:e116 @ 6.70 |  |
| g131 | 1.05 | TRACK_LOST | B | B:track_034 | B:e117 @ 6.70 |  |
| g132 | 1.10 | CRITICAL_TTC_END | B | B:track_012 | B:e118 @ 6.75 |  |
| g133 | 1.10 | CLOSING_END | B | B:track_030 | B:e119 @ 6.75 |  |
| g134 | 1.15 | CUT_IN_FROM_LEFT_END | A | B | A:e16 @ 6.80 |  |
| g135 | 1.15 | CLOSING_END | B | B:track_028 | B:e120 @ 6.80 |  |
| g136 | 1.15 | CLOSING_END | B | B:track_032 | B:e121 @ 6.80 |  |
| g137 | 1.15 | CLOSING_END | B | B:track_036 | B:e122 @ 6.80 |  |
| g138 | 1.15 | CLOSING_END | B | B:track_040 | B:e123 @ 6.80 |  |
| g139 | 1.15 | CLOSING_END | B | B:track_041 | B:e124 @ 6.80 |  |
| g140 | 1.15 | EGO_PATH_ENTRY | B | B:track_005 | B:e125 @ 6.80 |  |
| g141 | 1.15 | TRACK_LOST | B | B:track_028 | B:e126 @ 6.80 |  |
| g142 | 1.20 | CRITICAL_TTC_END | A | B | A:e17 @ 6.85 |  |
| g143 | 1.20 | CLOSING_END | A | B | A:e18 @ 6.85 |  |
| g144 | 1.20 | CLOSING_END | B | B:track_025 | B:e127 @ 6.85 |  |
| g145 | 1.20 | CLOSING_END | B | B:track_037 | B:e128 @ 6.85 |  |
| g146 | 1.20 | CLOSING_END | B | B:track_038 | B:e129 @ 6.85 |  |
| g147 | 1.20 | CLOSING_END | B | B:track_039 | B:e130 @ 6.85 |  |
| g148 | 1.20 | CLOSING_END | B | B:track_042 | B:e131 @ 6.85 |  |
| g149 | 1.20 | TRACK_LOST | B | B:track_041 | B:e132 @ 6.85 |  |
| g150 | 1.25 | CLOSING_END | B | B:track_001 | B:e133 @ 6.90 |  |
| g151 | 1.25 | CLOSING_END | B | B:track_003 | B:e134 @ 6.90 |  |
| g152 | 1.25 | CLOSING_END | B | B:track_005 | B:e135 @ 6.90 |  |
| g153 | 1.25 | CLOSING_END | B | B:track_006 | B:e136 @ 6.90 |  |
| g154 | 1.25 | CLOSING_END | B | B:track_012 | B:e137 @ 6.90 |  |
| g155 | 1.25 | CLOSING_END | B | B:track_013 | B:e138 @ 6.90 |  |
| g156 | 1.25 | CLOSING_END | B | B:track_020 | B:e139 @ 6.90 |  |
| g157 | 1.25 | CLOSING_END | B | B:track_029 | B:e140 @ 6.90 |  |
| g158 | 1.25 | CLOSING_END | B | B:track_035 | B:e141 @ 6.90 |  |
| g159 | 1.25 | TURN_RIGHT_END | B | - | B:e142 @ 6.90 |  |
| g160 | 1.25 | MOVING_END | B | - | B:e143 @ 6.90 |  |
| g161 | 1.25 | STOP_START | B | - | B:e144 @ 6.90 |  |
| g162 | 1.30 | MOVING_END | A | - | A:e19 @ 6.95 |  |
| g163 | 1.30 | STOP_START | A | - | A:e20 @ 6.95 |  |
| g164 | 1.35 | CLOSING_END | B | B:track_022 | B:e145 @ 7.00 |  |
| g165 | 1.70 | TRACK_LOST | B | B:track_022 | B:e146 @ 7.35 |  |
| g166 | 2.00 | TRACK_LOST | B | B:track_025 | B:e147 @ 7.65 |  |
| g167 | 2.05 | EGO_PATH_ENTRY | B | B:track_006 | B:e148 @ 7.70 |  |
| g168 | 2.70 | EGO_PATH_EXIT | B | B:track_013 | B:e149 @ 8.35 |  |
| g169 | 3.00 | TRACK_LOST | B | B:track_029 | B:e150 @ 8.65 |  |
| g170 | 4.05 | TRACK_LOST | B | B:track_037 | B:e151 @ 9.70 |  |
| g171 | 4.25 | TRACK_LOST | B | B:track_005 | B:e152 @ 9.90 |  |
| g172 | 4.25 | TRACK_LOST | B | B:track_035 | B:e153 @ 9.90 |  |

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
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g14 --PRECEDES--> g15
    g15 --PRECEDES--> g16
    g16 --PRECEDES--> g17
    g17 --PRECEDES--> g18
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g17 --PRECEDES--> g21
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g17 --PRECEDES--> g25
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
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g27 --PRECEDES--> g35
    g27 --PRECEDES--> g36
    g27 --PRECEDES--> g37
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g28 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g28 --PRECEDES--> g36
    g28 --PRECEDES--> g37
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g29 --PRECEDES--> g35
    g29 --PRECEDES--> g36
    g29 --PRECEDES--> g37
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g30 --PRECEDES--> g34
    g30 --PRECEDES--> g35
    g30 --PRECEDES--> g36
    g30 --PRECEDES--> g37
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g31 --PRECEDES--> g35
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g32 --PRECEDES--> g38
    g32 --PRECEDES--> g39
    g32 --PRECEDES--> g40
    g32 --PRECEDES--> g41
    g32 --PRECEDES--> g42
    g32 --PRECEDES--> g43
    g32 --PRECEDES--> g44
    g32 --PRECEDES--> g45
    g32 --PRECEDES--> g46
    g32 --PRECEDES--> g47
    g33 --PRECEDES--> g38
    g33 --PRECEDES--> g39
    g33 --PRECEDES--> g40
    g33 --PRECEDES--> g41
    g33 --PRECEDES--> g42
    g33 --PRECEDES--> g43
    g33 --PRECEDES--> g44
    g33 --PRECEDES--> g45
    g33 --PRECEDES--> g46
    g33 --PRECEDES--> g47
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g34 --PRECEDES--> g41
    g34 --PRECEDES--> g42
    g34 --PRECEDES--> g43
    g34 --PRECEDES--> g44
    g34 --PRECEDES--> g45
    g34 --PRECEDES--> g46
    g34 --PRECEDES--> g47
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g35 --PRECEDES--> g43
    g35 --PRECEDES--> g44
    g35 --PRECEDES--> g45
    g35 --PRECEDES--> g46
    g35 --PRECEDES--> g47
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g36 --PRECEDES--> g43
    g36 --PRECEDES--> g44
    g36 --PRECEDES--> g45
    g36 --PRECEDES--> g46
    g36 --PRECEDES--> g47
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g37 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g37 --PRECEDES--> g44
    g37 --PRECEDES--> g45
    g37 --PRECEDES--> g46
    g37 --PRECEDES--> g47
    g38 --PRECEDES--> g48
    g38 --PRECEDES--> g49
    g38 --PRECEDES--> g50
    g38 --PRECEDES--> g51
    g38 --PRECEDES--> g52
    g38 --PRECEDES--> g53
    g38 --PRECEDES--> g54
    g38 --PRECEDES--> g55
    g38 --PRECEDES--> g56
    g38 --PRECEDES--> g57
    g38 --PRECEDES--> g58
    g38 --PRECEDES--> g59
    g39 --PRECEDES--> g48
    g39 --PRECEDES--> g49
    g39 --PRECEDES--> g50
    g39 --PRECEDES--> g51
    g39 --PRECEDES--> g52
    g39 --PRECEDES--> g53
    g39 --PRECEDES--> g54
    g39 --PRECEDES--> g55
    g39 --PRECEDES--> g56
    g39 --PRECEDES--> g57
    g39 --PRECEDES--> g58
    g39 --PRECEDES--> g59
    g40 --PRECEDES--> g48
    g40 --PRECEDES--> g49
    g40 --PRECEDES--> g50
    g40 --PRECEDES--> g51
    g40 --PRECEDES--> g52
    g40 --PRECEDES--> g53
    g40 --PRECEDES--> g54
    g40 --PRECEDES--> g55
    g40 --PRECEDES--> g56
    g40 --PRECEDES--> g57
    g40 --PRECEDES--> g58
    g40 --PRECEDES--> g59
    g41 --PRECEDES--> g48
    g41 --PRECEDES--> g49
    g41 --PRECEDES--> g50
    g41 --PRECEDES--> g51
    g41 --PRECEDES--> g52
    g41 --PRECEDES--> g53
    g41 --PRECEDES--> g54
    g41 --PRECEDES--> g55
    g41 --PRECEDES--> g56
    g41 --PRECEDES--> g57
    g41 --PRECEDES--> g58
    g41 --PRECEDES--> g59
    g42 --PRECEDES--> g48
    g42 --PRECEDES--> g49
    g42 --PRECEDES--> g50
    g42 --PRECEDES--> g51
    g42 --PRECEDES--> g52
    g42 --PRECEDES--> g53
    g42 --PRECEDES--> g54
    g42 --PRECEDES--> g55
    g42 --PRECEDES--> g56
    g42 --PRECEDES--> g57
    g42 --PRECEDES--> g58
    g42 --PRECEDES--> g59
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g43 --PRECEDES--> g50
    g43 --PRECEDES--> g51
    g43 --PRECEDES--> g52
    g43 --PRECEDES--> g53
    g43 --PRECEDES--> g54
    g43 --PRECEDES--> g55
    g43 --PRECEDES--> g56
    g43 --PRECEDES--> g57
    g43 --PRECEDES--> g58
    g43 --PRECEDES--> g59
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g44 --PRECEDES--> g50
    g44 --PRECEDES--> g51
    g44 --PRECEDES--> g52
    g44 --PRECEDES--> g53
    g44 --PRECEDES--> g54
    g44 --PRECEDES--> g55
    g44 --PRECEDES--> g56
    g44 --PRECEDES--> g57
    g44 --PRECEDES--> g58
    g44 --PRECEDES--> g59
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
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
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
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
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
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
    g48 --PRECEDES--> g60
    g48 --PRECEDES--> g61
    g48 --PRECEDES--> g62
    g48 --PRECEDES--> g63
    g48 --PRECEDES--> g64
    g48 --PRECEDES--> g65
    g48 --PRECEDES--> g66
    g48 --PRECEDES--> g67
    g49 --PRECEDES--> g60
    g49 --PRECEDES--> g61
    g49 --PRECEDES--> g62
    g49 --PRECEDES--> g63
    g49 --PRECEDES--> g64
    g49 --PRECEDES--> g65
    g49 --PRECEDES--> g66
    g49 --PRECEDES--> g67
    g50 --PRECEDES--> g60
    g50 --PRECEDES--> g61
    g50 --PRECEDES--> g62
    g50 --PRECEDES--> g63
    g50 --PRECEDES--> g64
    g50 --PRECEDES--> g65
    g50 --PRECEDES--> g66
    g50 --PRECEDES--> g67
    g51 --PRECEDES--> g60
    g51 --PRECEDES--> g61
    g51 --PRECEDES--> g62
    g51 --PRECEDES--> g63
    g51 --PRECEDES--> g64
    g51 --PRECEDES--> g65
    g51 --PRECEDES--> g66
    g51 --PRECEDES--> g67
    g52 --PRECEDES--> g60
    g52 --PRECEDES--> g61
    g52 --PRECEDES--> g62
    g52 --PRECEDES--> g63
    g52 --PRECEDES--> g64
    g52 --PRECEDES--> g65
    g52 --PRECEDES--> g66
    g52 --PRECEDES--> g67
    g53 --PRECEDES--> g60
    g53 --PRECEDES--> g61
    g53 --PRECEDES--> g62
    g53 --PRECEDES--> g63
    g53 --PRECEDES--> g64
    g53 --PRECEDES--> g65
    g53 --PRECEDES--> g66
    g53 --PRECEDES--> g67
    g54 --PRECEDES--> g60
    g54 --PRECEDES--> g61
    g54 --PRECEDES--> g62
    g54 --PRECEDES--> g63
    g54 --PRECEDES--> g64
    g54 --PRECEDES--> g65
    g54 --PRECEDES--> g66
    g54 --PRECEDES--> g67
    g55 --PRECEDES--> g60
    g55 --PRECEDES--> g61
    g55 --PRECEDES--> g62
    g55 --PRECEDES--> g63
    g55 --PRECEDES--> g64
    g55 --PRECEDES--> g65
    g55 --PRECEDES--> g66
    g55 --PRECEDES--> g67
    g56 --PRECEDES--> g60
    g56 --PRECEDES--> g61
    g56 --PRECEDES--> g62
    g56 --PRECEDES--> g63
    g56 --PRECEDES--> g64
    g56 --PRECEDES--> g65
    g56 --PRECEDES--> g66
    g56 --PRECEDES--> g67
    g57 --PRECEDES--> g60
    g57 --PRECEDES--> g61
    g57 --PRECEDES--> g62
    g57 --PRECEDES--> g63
    g57 --PRECEDES--> g64
    g57 --PRECEDES--> g65
    g57 --PRECEDES--> g66
    g57 --PRECEDES--> g67
    g58 --PRECEDES--> g60
    g58 --PRECEDES--> g61
    g58 --PRECEDES--> g62
    g58 --PRECEDES--> g63
    g58 --PRECEDES--> g64
    g58 --PRECEDES--> g65
    g58 --PRECEDES--> g66
    g58 --PRECEDES--> g67
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g59 --PRECEDES--> g62
    g59 --PRECEDES--> g63
    g59 --PRECEDES--> g64
    g59 --PRECEDES--> g65
    g59 --PRECEDES--> g66
    g59 --PRECEDES--> g67
    g60 --PRECEDES--> g68
    g61 --PRECEDES--> g68
    g62 --PRECEDES--> g68
    g63 --PRECEDES--> g68
    g64 --PRECEDES--> g68
    g65 --PRECEDES--> g68
    g66 --PRECEDES--> g68
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g68 --PRECEDES--> g70
    g68 --PRECEDES--> g71
    g68 --PRECEDES--> g72
    g68 --PRECEDES--> g73
    g68 --PRECEDES--> g74
    g68 --PRECEDES--> g75
    g68 --PRECEDES--> g76
    g68 --PRECEDES--> g77
    g68 --PRECEDES--> g78
    g68 --PRECEDES--> g79
    g68 --PRECEDES--> g80
    g68 --PRECEDES--> g81
    g68 --PRECEDES--> g82
    g68 --PRECEDES--> g83
    g68 --PRECEDES--> g84
    g69 --PRECEDES--> g85
    g69 --PRECEDES--> g86
    g70 --PRECEDES--> g85
    g70 --PRECEDES--> g86
    g71 --PRECEDES--> g85
    g71 --PRECEDES--> g86
    g72 --PRECEDES--> g85
    g72 --PRECEDES--> g86
    g73 --PRECEDES--> g85
    g73 --PRECEDES--> g86
    g74 --PRECEDES--> g85
    g74 --PRECEDES--> g86
    g75 --PRECEDES--> g85
    g75 --PRECEDES--> g86
    g76 --PRECEDES--> g85
    g76 --PRECEDES--> g86
    g77 --PRECEDES--> g85
    g77 --PRECEDES--> g86
    g78 --PRECEDES--> g85
    g78 --PRECEDES--> g86
    g79 --PRECEDES--> g85
    g79 --PRECEDES--> g86
    g80 --PRECEDES--> g85
    g80 --PRECEDES--> g86
    g81 --PRECEDES--> g85
    g81 --PRECEDES--> g86
    g82 --PRECEDES--> g85
    g82 --PRECEDES--> g86
    g83 --PRECEDES--> g85
    g83 --PRECEDES--> g86
    g84 --PRECEDES--> g85
    g84 --PRECEDES--> g86
    g85 --PRECEDES--> g87
    g85 --PRECEDES--> g88
    g85 --PRECEDES--> g89
    g85 --PRECEDES--> g90
    g85 --PRECEDES--> g91
    g85 --PRECEDES--> g92
    g85 --PRECEDES--> g93
    g85 --PRECEDES--> g94
    g85 --PRECEDES--> g95
    g85 --PRECEDES--> g96
    g85 --PRECEDES--> g97
    g85 --PRECEDES--> g98
    g85 --PRECEDES--> g99
    g85 --PRECEDES--> g100
    g85 --PRECEDES--> g101
    g85 --PRECEDES--> g102
    g85 --PRECEDES--> g103
    g86 --PRECEDES--> g87
    g86 --PRECEDES--> g88
    g86 --PRECEDES--> g89
    g86 --PRECEDES--> g90
    g86 --PRECEDES--> g91
    g86 --PRECEDES--> g92
    g86 --PRECEDES--> g93
    g86 --PRECEDES--> g94
    g86 --PRECEDES--> g95
    g86 --PRECEDES--> g96
    g86 --PRECEDES--> g97
    g86 --PRECEDES--> g98
    g86 --PRECEDES--> g99
    g86 --PRECEDES--> g100
    g86 --PRECEDES--> g101
    g86 --PRECEDES--> g102
    g86 --PRECEDES--> g103
    g87 --PRECEDES--> g104
    g87 --PRECEDES--> g105
    g87 --PRECEDES--> g106
    g87 --PRECEDES--> g107
    g87 --PRECEDES--> g108
    g88 --PRECEDES--> g104
    g88 --PRECEDES--> g105
    g88 --PRECEDES--> g106
    g88 --PRECEDES--> g107
    g88 --PRECEDES--> g108
    g89 --PRECEDES--> g104
    g89 --PRECEDES--> g105
    g89 --PRECEDES--> g106
    g89 --PRECEDES--> g107
    g89 --PRECEDES--> g108
    g90 --PRECEDES--> g104
    g90 --PRECEDES--> g105
    g90 --PRECEDES--> g106
    g90 --PRECEDES--> g107
    g90 --PRECEDES--> g108
    g91 --PRECEDES--> g104
    g91 --PRECEDES--> g105
    g91 --PRECEDES--> g106
    g91 --PRECEDES--> g107
    g91 --PRECEDES--> g108
    g92 --PRECEDES--> g104
    g92 --PRECEDES--> g105
    g92 --PRECEDES--> g106
    g92 --PRECEDES--> g107
    g92 --PRECEDES--> g108
    g93 --PRECEDES--> g104
    g93 --PRECEDES--> g105
    g93 --PRECEDES--> g106
    g93 --PRECEDES--> g107
    g93 --PRECEDES--> g108
    g94 --PRECEDES--> g104
    g94 --PRECEDES--> g105
    g94 --PRECEDES--> g106
    g94 --PRECEDES--> g107
    g94 --PRECEDES--> g108
    g95 --PRECEDES--> g104
    g95 --PRECEDES--> g105
    g95 --PRECEDES--> g106
    g95 --PRECEDES--> g107
    g95 --PRECEDES--> g108
    g96 --PRECEDES--> g104
    g96 --PRECEDES--> g105
    g96 --PRECEDES--> g106
    g96 --PRECEDES--> g107
    g96 --PRECEDES--> g108
    g97 --PRECEDES--> g104
    g97 --PRECEDES--> g105
    g97 --PRECEDES--> g106
    g97 --PRECEDES--> g107
    g97 --PRECEDES--> g108
    g98 --PRECEDES--> g104
    g98 --PRECEDES--> g105
    g98 --PRECEDES--> g106
    g98 --PRECEDES--> g107
    g98 --PRECEDES--> g108
    g99 --PRECEDES--> g104
    g99 --PRECEDES--> g105
    g99 --PRECEDES--> g106
    g99 --PRECEDES--> g107
    g99 --PRECEDES--> g108
    g100 --PRECEDES--> g104
    g100 --PRECEDES--> g105
    g100 --PRECEDES--> g106
    g100 --PRECEDES--> g107
    g100 --PRECEDES--> g108
    g101 --PRECEDES--> g104
    g101 --PRECEDES--> g105
    g101 --PRECEDES--> g106
    g101 --PRECEDES--> g107
    g101 --PRECEDES--> g108
    g102 --PRECEDES--> g104
    g102 --PRECEDES--> g105
    g102 --PRECEDES--> g106
    g102 --PRECEDES--> g107
    g102 --PRECEDES--> g108
    g103 --PRECEDES--> g104
    g103 --PRECEDES--> g105
    g103 --PRECEDES--> g106
    g103 --PRECEDES--> g107
    g103 --PRECEDES--> g108
    g104 --PRECEDES--> g109
    g104 --PRECEDES--> g110
    g104 --PRECEDES--> g111
    g104 --PRECEDES--> g112
    g104 --PRECEDES--> g113
    g104 --PRECEDES--> g114
    g104 --PRECEDES--> g115
    g104 --PRECEDES--> g116
    g105 --PRECEDES--> g109
    g105 --PRECEDES--> g110
    g105 --PRECEDES--> g111
    g105 --PRECEDES--> g112
    g105 --PRECEDES--> g113
    g105 --PRECEDES--> g114
    g105 --PRECEDES--> g115
    g105 --PRECEDES--> g116
    g106 --PRECEDES--> g109
    g106 --PRECEDES--> g110
    g106 --PRECEDES--> g111
    g106 --PRECEDES--> g112
    g106 --PRECEDES--> g113
    g106 --PRECEDES--> g114
    g106 --PRECEDES--> g115
    g106 --PRECEDES--> g116
    g107 --PRECEDES--> g109
    g107 --PRECEDES--> g110
    g107 --PRECEDES--> g111
    g107 --PRECEDES--> g112
    g107 --PRECEDES--> g113
    g107 --PRECEDES--> g114
    g107 --PRECEDES--> g115
    g107 --PRECEDES--> g116
    g108 --PRECEDES--> g109
    g108 --PRECEDES--> g110
    g108 --PRECEDES--> g111
    g108 --PRECEDES--> g112
    g108 --PRECEDES--> g113
    g108 --PRECEDES--> g114
    g108 --PRECEDES--> g115
    g108 --PRECEDES--> g116
    g109 --PRECEDES--> g117
    g109 --PRECEDES--> g118
    g110 --PRECEDES--> g117
    g110 --PRECEDES--> g118
    g111 --PRECEDES--> g117
    g111 --PRECEDES--> g118
    g112 --PRECEDES--> g117
    g112 --PRECEDES--> g118
    g113 --PRECEDES--> g117
    g113 --PRECEDES--> g118
    g114 --PRECEDES--> g117
    g114 --PRECEDES--> g118
    g115 --PRECEDES--> g117
    g115 --PRECEDES--> g118
    g116 --PRECEDES--> g117
    g116 --PRECEDES--> g118
    g117 --PRECEDES--> g119
    g117 --PRECEDES--> g120
    g117 --PRECEDES--> g121
    g118 --PRECEDES--> g119
    g118 --PRECEDES--> g120
    g118 --PRECEDES--> g121
    g119 --PRECEDES--> g122
    g119 --PRECEDES--> g123
    g119 --PRECEDES--> g124
    g119 --PRECEDES--> g125
    g120 --PRECEDES--> g122
    g120 --PRECEDES--> g123
    g120 --PRECEDES--> g124
    g120 --PRECEDES--> g125
    g121 --PRECEDES--> g122
    g121 --PRECEDES--> g123
    g121 --PRECEDES--> g124
    g121 --PRECEDES--> g125
    g122 --PRECEDES--> g126
    g122 --PRECEDES--> g127
    g122 --PRECEDES--> g128
    g122 --PRECEDES--> g129
    g122 --PRECEDES--> g130
    g122 --PRECEDES--> g131
    g123 --PRECEDES--> g126
    g123 --PRECEDES--> g127
    g123 --PRECEDES--> g128
    g123 --PRECEDES--> g129
    g123 --PRECEDES--> g130
    g123 --PRECEDES--> g131
    g124 --PRECEDES--> g126
    g124 --PRECEDES--> g127
    g124 --PRECEDES--> g128
    g124 --PRECEDES--> g129
    g124 --PRECEDES--> g130
    g124 --PRECEDES--> g131
    g125 --PRECEDES--> g126
    g125 --PRECEDES--> g127
    g125 --PRECEDES--> g128
    g125 --PRECEDES--> g129
    g125 --PRECEDES--> g130
    g125 --PRECEDES--> g131
    g126 --PRECEDES--> g132
    g126 --PRECEDES--> g133
    g127 --PRECEDES--> g132
    g127 --PRECEDES--> g133
    g128 --PRECEDES--> g132
    g128 --PRECEDES--> g133
    g129 --PRECEDES--> g132
    g129 --PRECEDES--> g133
    g130 --PRECEDES--> g132
    g130 --PRECEDES--> g133
    g131 --PRECEDES--> g132
    g131 --PRECEDES--> g133
    g132 --PRECEDES--> g134
    g132 --PRECEDES--> g135
    g132 --PRECEDES--> g136
    g132 --PRECEDES--> g137
    g132 --PRECEDES--> g138
    g132 --PRECEDES--> g139
    g132 --PRECEDES--> g140
    g132 --PRECEDES--> g141
    g133 --PRECEDES--> g134
    g133 --PRECEDES--> g135
    g133 --PRECEDES--> g136
    g133 --PRECEDES--> g137
    g133 --PRECEDES--> g138
    g133 --PRECEDES--> g139
    g133 --PRECEDES--> g140
    g133 --PRECEDES--> g141
    g134 --PRECEDES--> g142
    g134 --PRECEDES--> g143
    g134 --PRECEDES--> g144
    g134 --PRECEDES--> g145
    g134 --PRECEDES--> g146
    g134 --PRECEDES--> g147
    g134 --PRECEDES--> g148
    g134 --PRECEDES--> g149
    g135 --PRECEDES--> g142
    g135 --PRECEDES--> g143
    g135 --PRECEDES--> g144
    g135 --PRECEDES--> g145
    g135 --PRECEDES--> g146
    g135 --PRECEDES--> g147
    g135 --PRECEDES--> g148
    g135 --PRECEDES--> g149
    g136 --PRECEDES--> g142
    g136 --PRECEDES--> g143
    g136 --PRECEDES--> g144
    g136 --PRECEDES--> g145
    g136 --PRECEDES--> g146
    g136 --PRECEDES--> g147
    g136 --PRECEDES--> g148
    g136 --PRECEDES--> g149
    g137 --PRECEDES--> g142
    g137 --PRECEDES--> g143
    g137 --PRECEDES--> g144
    g137 --PRECEDES--> g145
    g137 --PRECEDES--> g146
    g137 --PRECEDES--> g147
    g137 --PRECEDES--> g148
    g137 --PRECEDES--> g149
    g138 --PRECEDES--> g142
    g138 --PRECEDES--> g143
    g138 --PRECEDES--> g144
    g138 --PRECEDES--> g145
    g138 --PRECEDES--> g146
    g138 --PRECEDES--> g147
    g138 --PRECEDES--> g148
    g138 --PRECEDES--> g149
    g139 --PRECEDES--> g142
    g139 --PRECEDES--> g143
    g139 --PRECEDES--> g144
    g139 --PRECEDES--> g145
    g139 --PRECEDES--> g146
    g139 --PRECEDES--> g147
    g139 --PRECEDES--> g148
    g139 --PRECEDES--> g149
    g140 --PRECEDES--> g142
    g140 --PRECEDES--> g143
    g140 --PRECEDES--> g144
    g140 --PRECEDES--> g145
    g140 --PRECEDES--> g146
    g140 --PRECEDES--> g147
    g140 --PRECEDES--> g148
    g140 --PRECEDES--> g149
    g141 --PRECEDES--> g142
    g141 --PRECEDES--> g143
    g141 --PRECEDES--> g144
    g141 --PRECEDES--> g145
    g141 --PRECEDES--> g146
    g141 --PRECEDES--> g147
    g141 --PRECEDES--> g148
    g141 --PRECEDES--> g149
    g142 --PRECEDES--> g150
    g142 --PRECEDES--> g151
    g142 --PRECEDES--> g152
    g142 --PRECEDES--> g153
    g142 --PRECEDES--> g154
    g142 --PRECEDES--> g155
    g142 --PRECEDES--> g156
    g142 --PRECEDES--> g157
    g142 --PRECEDES--> g158
    g142 --PRECEDES--> g159
    g142 --PRECEDES--> g160
    g142 --PRECEDES--> g161
    g143 --PRECEDES--> g150
    g143 --PRECEDES--> g151
    g143 --PRECEDES--> g152
    g143 --PRECEDES--> g153
    g143 --PRECEDES--> g154
    g143 --PRECEDES--> g155
    g143 --PRECEDES--> g156
    g143 --PRECEDES--> g157
    g143 --PRECEDES--> g158
    g143 --PRECEDES--> g159
    g143 --PRECEDES--> g160
    g143 --PRECEDES--> g161
    g144 --PRECEDES--> g150
    g144 --PRECEDES--> g151
    g144 --PRECEDES--> g152
    g144 --PRECEDES--> g153
    g144 --PRECEDES--> g154
    g144 --PRECEDES--> g155
    g144 --PRECEDES--> g156
    g144 --PRECEDES--> g157
    g144 --PRECEDES--> g158
    g144 --PRECEDES--> g159
    g144 --PRECEDES--> g160
    g144 --PRECEDES--> g161
    g145 --PRECEDES--> g150
    g145 --PRECEDES--> g151
    g145 --PRECEDES--> g152
    g145 --PRECEDES--> g153
    g145 --PRECEDES--> g154
    g145 --PRECEDES--> g155
    g145 --PRECEDES--> g156
    g145 --PRECEDES--> g157
    g145 --PRECEDES--> g158
    g145 --PRECEDES--> g159
    g145 --PRECEDES--> g160
    g145 --PRECEDES--> g161
    g146 --PRECEDES--> g150
    g146 --PRECEDES--> g151
    g146 --PRECEDES--> g152
    g146 --PRECEDES--> g153
    g146 --PRECEDES--> g154
    g146 --PRECEDES--> g155
    g146 --PRECEDES--> g156
    g146 --PRECEDES--> g157
    g146 --PRECEDES--> g158
    g146 --PRECEDES--> g159
    g146 --PRECEDES--> g160
    g146 --PRECEDES--> g161
    g147 --PRECEDES--> g150
    g147 --PRECEDES--> g151
    g147 --PRECEDES--> g152
    g147 --PRECEDES--> g153
    g147 --PRECEDES--> g154
    g147 --PRECEDES--> g155
    g147 --PRECEDES--> g156
    g147 --PRECEDES--> g157
    g147 --PRECEDES--> g158
    g147 --PRECEDES--> g159
    g147 --PRECEDES--> g160
    g147 --PRECEDES--> g161
    g148 --PRECEDES--> g150
    g148 --PRECEDES--> g151
    g148 --PRECEDES--> g152
    g148 --PRECEDES--> g153
    g148 --PRECEDES--> g154
    g148 --PRECEDES--> g155
    g148 --PRECEDES--> g156
    g148 --PRECEDES--> g157
    g148 --PRECEDES--> g158
    g148 --PRECEDES--> g159
    g148 --PRECEDES--> g160
    g148 --PRECEDES--> g161
    g149 --PRECEDES--> g150
    g149 --PRECEDES--> g151
    g149 --PRECEDES--> g152
    g149 --PRECEDES--> g153
    g149 --PRECEDES--> g154
    g149 --PRECEDES--> g155
    g149 --PRECEDES--> g156
    g149 --PRECEDES--> g157
    g149 --PRECEDES--> g158
    g149 --PRECEDES--> g159
    g149 --PRECEDES--> g160
    g149 --PRECEDES--> g161
    g150 --PRECEDES--> g162
    g150 --PRECEDES--> g163
    g151 --PRECEDES--> g162
    g151 --PRECEDES--> g163
    g152 --PRECEDES--> g162
    g152 --PRECEDES--> g163
    g153 --PRECEDES--> g162
    g153 --PRECEDES--> g163
    g154 --PRECEDES--> g162
    g154 --PRECEDES--> g163
    g155 --PRECEDES--> g162
    g155 --PRECEDES--> g163
    g156 --PRECEDES--> g162
    g156 --PRECEDES--> g163
    g157 --PRECEDES--> g162
    g157 --PRECEDES--> g163
    g158 --PRECEDES--> g162
    g158 --PRECEDES--> g163
    g159 --PRECEDES--> g162
    g159 --PRECEDES--> g163
    g160 --PRECEDES--> g162
    g160 --PRECEDES--> g163
    g161 --PRECEDES--> g162
    g161 --PRECEDES--> g163
    g162 --PRECEDES--> g164
    g163 --PRECEDES--> g164
    g164 --PRECEDES--> g165
    g165 --PRECEDES--> g166
    g166 --PRECEDES--> g167
    g167 --PRECEDES--> g168
    g168 --PRECEDES--> g169
    g169 --PRECEDES--> g170
    g170 --PRECEDES--> g171
    g170 --PRECEDES--> g172
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g05
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g10
    g08 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g12
    g08 --SAME_TRACK--> g17
    g08 --SAME_TRACK--> g101
    g08 --SAME_TRACK--> g134
    g08 --SAME_TRACK--> g142
    g08 --SAME_TRACK--> g143
    g18 --SAME_TRACK--> g22
    g19 --SAME_TRACK--> g23
    g111 --SAME_TRACK--> g114
    g49 --SAME_TRACK--> g115
    g61 --SAME_TRACK--> g116
    g62 --SAME_TRACK--> g117
    g63 --SAME_TRACK--> g118
    g60 --SAME_TRACK--> g119
    g69 --SAME_TRACK--> g120
    g72 --SAME_TRACK--> g121
    g52 --SAME_TRACK--> g122
    g51 --SAME_TRACK--> g123
    g20 --SAME_TRACK--> g24
    g52 --SAME_TRACK--> g124
    g88 --SAME_TRACK--> g125
    g70 --SAME_TRACK--> g126
    g74 --SAME_TRACK--> g127
    g89 --SAME_TRACK--> g128
    g70 --SAME_TRACK--> g129
    g74 --SAME_TRACK--> g130
    g89 --SAME_TRACK--> g131
    g51 --SAME_TRACK--> g132
    g73 --SAME_TRACK--> g133
    g21 --SAME_TRACK--> g25
    g85 --SAME_TRACK--> g135
    g87 --SAME_TRACK--> g136
    g90 --SAME_TRACK--> g137
    g92 --SAME_TRACK--> g138
    g104 --SAME_TRACK--> g139
    g27 --SAME_TRACK--> g140
    g85 --SAME_TRACK--> g141
    g71 --SAME_TRACK--> g144
    g91 --SAME_TRACK--> g145
    g109 --SAME_TRACK--> g146
    g110 --SAME_TRACK--> g147
    g111 --SAME_TRACK--> g148
    g104 --SAME_TRACK--> g149
    g18 --SAME_TRACK--> g150
    g20 --SAME_TRACK--> g151
    g27 --SAME_TRACK--> g152
    g28 --SAME_TRACK--> g153
    g51 --SAME_TRACK--> g154
    g52 --SAME_TRACK--> g155
    g41 --SAME_TRACK--> g156
    g42 --SAME_TRACK--> g157
    g93 --SAME_TRACK--> g158
    g21 --SAME_TRACK--> g164
    g21 --SAME_TRACK--> g165
    g71 --SAME_TRACK--> g166
    g28 --SAME_TRACK--> g167
    g52 --SAME_TRACK--> g168
    g42 --SAME_TRACK--> g169
    g91 --SAME_TRACK--> g170
    g27 --SAME_TRACK--> g171
    g93 --SAME_TRACK--> g172
    g26 --SAME_TRACK--> g29
    g27 --SAME_TRACK--> g30
    g28 --SAME_TRACK--> g31
    g32 --SAME_TRACK--> g35
    g34 --SAME_TRACK--> g36
    g33 --SAME_TRACK--> g37
    g38 --SAME_TRACK--> g43
    g39 --SAME_TRACK--> g44
    g40 --SAME_TRACK--> g45
    g41 --SAME_TRACK--> g46
    g42 --SAME_TRACK--> g47
    g51 --SAME_TRACK--> g53
    g52 --SAME_TRACK--> g54
    g48 --SAME_TRACK--> g55
    g49 --SAME_TRACK--> g56
    g50 --SAME_TRACK--> g57
    g51 --SAME_TRACK--> g58
    g52 --SAME_TRACK--> g59
    g60 --SAME_TRACK--> g64
    g61 --SAME_TRACK--> g65
    g62 --SAME_TRACK--> g66
    g63 --SAME_TRACK--> g67
    g26 --SAME_TRACK--> g68
    g69 --SAME_TRACK--> g75
    g70 --SAME_TRACK--> g76
    g71 --SAME_TRACK--> g77
    g72 --SAME_TRACK--> g78
    g73 --SAME_TRACK--> g79
    g74 --SAME_TRACK--> g80
    g19 --SAME_TRACK--> g81
    g32 --SAME_TRACK--> g82
    g34 --SAME_TRACK--> g83
    g33 --SAME_TRACK--> g84
    g85 --SAME_TRACK--> g86
    g87 --SAME_TRACK--> g94
    g88 --SAME_TRACK--> g95
    g89 --SAME_TRACK--> g96
    g93 --SAME_TRACK--> g97
    g90 --SAME_TRACK--> g98
    g91 --SAME_TRACK--> g99
    g92 --SAME_TRACK--> g100
    g38 --SAME_TRACK--> g102
    g39 --SAME_TRACK--> g103
    g104 --SAME_TRACK--> g105
    g48 --SAME_TRACK--> g106
    g40 --SAME_TRACK--> g107
    g50 --SAME_TRACK--> g108
    g109 --SAME_TRACK--> g112
    g110 --SAME_TRACK--> g113
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.65 | MOVING_START(A); MOVING_START(B) |
| -5.50 | TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001) |
| -4.90 | TRACK_LOST(A,A:track_001) |
| -4.85 | BRAKE_START(B) |
| -2.90 | SPEED_LIMIT_EXCEEDED_START(A) |
| -2.30 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -1.80 | CUT_IN_FROM_LEFT_START(A,B) |
| -1.65 | CRITICAL_TTC_START(A,B) |
| -0.20 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A) |
| +0.05 | BRAKE_START(A) |
| +0.10 | TURN_RIGHT_START(B) |
| +0.20 | CRITICAL_TTC_END(A,B) |
| +0.25 | TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_022); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_022) |
| +0.30 | TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); TRACK_APPEARED_RIGHT(B,B:track_006); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006) |
| +0.40 | TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008); CLOSING_START(B,B:track_009) |
| +0.45 | TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_LEFT(B,B:track_011); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_RIGHT(B,B:track_020); TRACK_APPEARED_RIGHT(B,B:track_029); CLOSING_START(B,B:track_010); CLOSING_START(B,B:track_011); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_020); CLOSING_START(B,B:track_029) |
| +0.50 | TRACK_APPEARED_LEFT(B,B:track_014); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_021); TRACK_APPEARED_RIGHT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_013); CLOSING_START(B,B:track_012); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_021); CRITICAL_TTC_START(B,B:track_012); CRITICAL_TTC_START(B,B:track_013) |
| +0.55 | TRACK_APPEARED_LEFT(B,B:track_017); TRACK_APPEARED_LEFT(B,B:track_018); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_APPEARED_LEFT(B,B:track_026); CLOSING_START(B,B:track_017); CLOSING_START(B,B:track_018); CLOSING_START(B,B:track_019); CLOSING_START(B,B:track_026) |
| +0.60 | TRACK_LOST(B,B:track_004) |
| +0.65 | TRACK_APPEARED_LEFT(B,B:track_023); TRACK_APPEARED_LEFT(B,B:track_024); TRACK_APPEARED_LEFT(B,B:track_025); TRACK_APPEARED_LEFT(B,B:track_027); TRACK_APPEARED_LEFT(B,B:track_030); TRACK_APPEARED_LEFT(B,B:track_031); CLOSING_START(B,B:track_023); CLOSING_START(B,B:track_024); CLOSING_START(B,B:track_025); CLOSING_START(B,B:track_027); CLOSING_START(B,B:track_030); CLOSING_START(B,B:track_031); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_008); TRACK_LOST(B,B:track_009) |
| +0.70 | TRACK_APPEARED_LEFT(B,B:track_028); CLOSING_START(B,B:track_028) |
| +0.75 | TRACK_APPEARED_LEFT(B,B:track_032); TRACK_APPEARED_LEFT(B,B:track_033); TRACK_APPEARED_LEFT(B,B:track_034); TRACK_APPEARED_LEFT(B,B:track_036); TRACK_APPEARED_LEFT(B,B:track_037); TRACK_APPEARED_LEFT(B,B:track_040); TRACK_APPEARED_RIGHT(B,B:track_035); CLOSING_START(B,B:track_032); CLOSING_START(B,B:track_033); CLOSING_START(B,B:track_034); CLOSING_START(B,B:track_035); CLOSING_START(B,B:track_036); CLOSING_START(B,B:track_037); CLOSING_START(B,B:track_040); CRITICAL_TTC_START(A,B); TRACK_LOST(B,B:track_010); TRACK_LOST(B,B:track_011) |
| +0.80 | TRACK_APPEARED_LEFT(B,B:track_041); CLOSING_START(B,B:track_041); TRACK_LOST(B,B:track_014); TRACK_LOST(B,B:track_015); TRACK_LOST(B,B:track_021) |
| +0.85 | TRACK_APPEARED_LEFT(B,B:track_038); TRACK_APPEARED_LEFT(B,B:track_039); TRACK_APPEARED_LEFT(B,B:track_042); CLOSING_START(B,B:track_038); CLOSING_START(B,B:track_039); CLOSING_START(B,B:track_042); TRACK_LOST(B,B:track_016); TRACK_LOST(B,B:track_018) |
| +0.90 | TRACK_LOST(B,B:track_019); TRACK_LOST(B,B:track_026) |
| +0.95 | TRACK_LOST(B,B:track_017); TRACK_LOST(B,B:track_023); TRACK_LOST(B,B:track_027) |
| +1.00 | CRITICAL_TTC_END(B,B:track_013); EGO_PATH_ENTRY(B,B:track_012); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_033) |
| +1.05 | CLOSING_END(B,B:track_024); CLOSING_END(B,B:track_031); CLOSING_END(B,B:track_034); TRACK_LOST(B,B:track_024); TRACK_LOST(B,B:track_031); TRACK_LOST(B,B:track_034) |
| +1.10 | CRITICAL_TTC_END(B,B:track_012); CLOSING_END(B,B:track_030) |
| +1.15 | CUT_IN_FROM_LEFT_END(A,B); CLOSING_END(B,B:track_028); CLOSING_END(B,B:track_032); CLOSING_END(B,B:track_036); CLOSING_END(B,B:track_040); CLOSING_END(B,B:track_041); EGO_PATH_ENTRY(B,B:track_005); TRACK_LOST(B,B:track_028) |
| +1.20 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_025); CLOSING_END(B,B:track_037); CLOSING_END(B,B:track_038); CLOSING_END(B,B:track_039); CLOSING_END(B,B:track_042); TRACK_LOST(B,B:track_041) |
| +1.25 | CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_006); CLOSING_END(B,B:track_012); CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_020); CLOSING_END(B,B:track_029); CLOSING_END(B,B:track_035); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B) |
| +1.30 | MOVING_END(A); STOP_START(A) |
| +1.35 | CLOSING_END(B,B:track_022) |
| +1.70 | TRACK_LOST(B,B:track_022) |
| +2.00 | TRACK_LOST(B,B:track_025) |
| +2.05 | EGO_PATH_ENTRY(B,B:track_006) |
| +2.70 | EGO_PATH_EXIT(B,B:track_013) |
| +3.00 | TRACK_LOST(B,B:track_029) |
| +4.05 | TRACK_LOST(B,B:track_037) |
| +4.25 | TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_035) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_002 (B): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 3.85 < CRITICAL_TTC_START 4.00 (+0.15 s) < COLLISION 5.65 (+1.65 s); EGO_PATH_ENTRY 5.45 after critical TTC (+1.45 s) [local times; t_global: cut_in -1.80, critical_ttc_start -1.65, ego_path_entry -0.20, collision +0.00]
- B's track_005 (unidentified B:track_005): EGO_PATH_ENTRY 6.80, no critical TTC [local times; t_global: ego_path_entry +1.15, collision +0.00]
- B's track_006 (unidentified B:track_006): EGO_PATH_ENTRY 7.70, no critical TTC [local times; t_global: ego_path_entry +2.05, collision +0.00]
- B's track_012 (unidentified B:track_012): CRITICAL_TTC_START 6.15, COLLISION 5.65 (+-0.50 s); EGO_PATH_ENTRY 6.65 after critical TTC (+0.50 s) [local times; t_global: critical_ttc_start +0.50, ego_path_entry +1.00, collision +0.00]
- B's track_013 (unidentified B:track_013): CRITICAL_TTC_START 6.15, COLLISION 5.65 (+-0.50 s); EGO_PATH_ENTRY 6.65 after critical TTC (+0.50 s) [local times; t_global: critical_ttc_start +0.50, ego_path_entry +1.00, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.65 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.65 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -5.50 | A | g03 TRACK_APPEARED_LEFT(A,A:track_001) (A:e02)<br>g04 CLOSING_START(A,A:track_001) (A:e03) | ego: MOVING |
| -4.90 | A | g05 TRACK_LOST(A,A:track_001) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -4.85 | B | g06 BRAKE_START(B) (B:e02) | ego: MOVING |
| -2.90 | A | g07 SPEED_LIMIT_EXCEEDED_START(A) (A:e05) | ego: MOVING<br>track lost, states UNKNOWN: track_001 |
| -2.30 | A | g08 TRACK_APPEARED_LEFT(A,B) (A:e06)<br>g09 CLOSING_START(A,B) (A:e07) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track lost, states UNKNOWN: track_001 |
| -1.80 | A | g10 CUT_IN_FROM_LEFT_START(A,B) (A:e08) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.65 | A | g11 CRITICAL_TTC_START(A,B) (A:e09) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| -0.20 | A | g12 EGO_PATH_ENTRY(A,B) (A:e10) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.00 | A | g13 COLLISION(A,B) (A:e11)<br>g14 SPEED_LIMIT_EXCEEDED_END(A) (A:e12) | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.00 | B | g13 COLLISION(A,B) (B:e03) | ego: MOVING, BRAKE |
| +0.05 | A | g15 BRAKE_START(A) (A:e13) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.10 | B | g16 TURN_RIGHT_START(B) (B:e04) | ego: MOVING, BRAKE |
| +0.20 | A | g17 CRITICAL_TTC_END(A,B) (A:e14) | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.25 | B | g18 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e05)<br>g19 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e06)<br>g20 TRACK_APPEARED_RIGHT(B,B:track_003) (B:e07)<br>g21 TRACK_APPEARED_RIGHT(B,B:track_022) (B:e08)<br>g22 CLOSING_START(B,B:track_001) (B:e09)<br>g23 CLOSING_START(B,B:track_002) (B:e10)<br>g24 CLOSING_START(B,B:track_003) (B:e11)<br>g25 CLOSING_START(B,B:track_022) (B:e12) | ego: MOVING, BRAKE, TURN_RIGHT |
| +0.30 | B | g26 TRACK_APPEARED_LEFT(B,B:track_004) (B:e13)<br>g27 TRACK_APPEARED_RIGHT(B,B:track_005) (B:e14)<br>g28 TRACK_APPEARED_RIGHT(B,B:track_006) (B:e15)<br>g29 CLOSING_START(B,B:track_004) (B:e16)<br>g30 CLOSING_START(B,B:track_005) (B:e17)<br>g31 CLOSING_START(B,B:track_006) (B:e18) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_022: CLOSING |
| +0.40 | B | g32 TRACK_APPEARED_LEFT(B,B:track_007) (B:e19)<br>g33 TRACK_APPEARED_LEFT(B,B:track_009) (B:e20)<br>g34 TRACK_APPEARED_RIGHT(B,B:track_008) (B:e21)<br>g35 CLOSING_START(B,B:track_007) (B:e22)<br>g36 CLOSING_START(B,B:track_008) (B:e23)<br>g37 CLOSING_START(B,B:track_009) (B:e24) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_022: CLOSING |
| +0.45 | B | g38 TRACK_APPEARED_LEFT(B,B:track_010) (B:e25)<br>g39 TRACK_APPEARED_LEFT(B,B:track_011) (B:e26)<br>g40 TRACK_APPEARED_LEFT(B,B:track_015) (B:e27)<br>g41 TRACK_APPEARED_RIGHT(B,B:track_020) (B:e28)<br>g42 TRACK_APPEARED_RIGHT(B,B:track_029) (B:e29)<br>g43 CLOSING_START(B,B:track_010) (B:e30)<br>g44 CLOSING_START(B,B:track_011) (B:e31)<br>g45 CLOSING_START(B,B:track_015) (B:e32)<br>g46 CLOSING_START(B,B:track_020) (B:e33)<br>g47 CLOSING_START(B,B:track_029) (B:e34) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING |
| +0.50 | B | g48 TRACK_APPEARED_LEFT(B,B:track_014) (B:e35)<br>g49 TRACK_APPEARED_LEFT(B,B:track_016) (B:e36)<br>g50 TRACK_APPEARED_LEFT(B,B:track_021) (B:e37)<br>g51 TRACK_APPEARED_RIGHT(B,B:track_012) (B:e38)<br>g52 TRACK_APPEARED_RIGHT(B,B:track_013) (B:e39)<br>g53 CLOSING_START(B,B:track_012) (B:e40)<br>g54 CLOSING_START(B,B:track_013) (B:e41)<br>g55 CLOSING_START(B,B:track_014) (B:e42)<br>g56 CLOSING_START(B,B:track_016) (B:e43)<br>g57 CLOSING_START(B,B:track_021) (B:e44)<br>g58 CRITICAL_TTC_START(B,B:track_012) (B:e45)<br>g59 CRITICAL_TTC_START(B,B:track_013) (B:e46) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_022: CLOSING<br>track_029: CLOSING |
| +0.55 | B | g60 TRACK_APPEARED_LEFT(B,B:track_017) (B:e47)<br>g61 TRACK_APPEARED_LEFT(B,B:track_018) (B:e48)<br>g62 TRACK_APPEARED_LEFT(B,B:track_019) (B:e49)<br>g63 TRACK_APPEARED_LEFT(B,B:track_026) (B:e50)<br>g64 CLOSING_START(B,B:track_017) (B:e51)<br>g65 CLOSING_START(B,B:track_018) (B:e52)<br>g66 CLOSING_START(B,B:track_019) (B:e53)<br>g67 CLOSING_START(B,B:track_026) (B:e54) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_029: CLOSING |
| +0.60 | B | g68 TRACK_LOST(B,B:track_004) (B:e55) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_029: CLOSING |
| +0.65 | B | g69 TRACK_APPEARED_LEFT(B,B:track_023) (B:e56)<br>g70 TRACK_APPEARED_LEFT(B,B:track_024) (B:e57)<br>g71 TRACK_APPEARED_LEFT(B,B:track_025) (B:e58)<br>g72 TRACK_APPEARED_LEFT(B,B:track_027) (B:e59)<br>g73 TRACK_APPEARED_LEFT(B,B:track_030) (B:e60)<br>g74 TRACK_APPEARED_LEFT(B,B:track_031) (B:e61)<br>g75 CLOSING_START(B,B:track_023) (B:e62)<br>g76 CLOSING_START(B,B:track_024) (B:e63)<br>g77 CLOSING_START(B,B:track_025) (B:e64)<br>g78 CLOSING_START(B,B:track_027) (B:e65)<br>g79 CLOSING_START(B,B:track_030) (B:e66)<br>g80 CLOSING_START(B,B:track_031) (B:e67)<br>g81 TRACK_LOST(B,B:track_002) (B:e68)<br>g82 TRACK_LOST(B,B:track_007) (B:e69)<br>g83 TRACK_LOST(B,B:track_008) (B:e70)<br>g84 TRACK_LOST(B,B:track_009) (B:e71) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_029: CLOSING<br>track lost, states UNKNOWN: track_004 |
| +0.70 | B | g85 TRACK_APPEARED_LEFT(B,B:track_028) (B:e72)<br>g86 CLOSING_START(B,B:track_028) (B:e73) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009 |
| +0.75 | B | g87 TRACK_APPEARED_LEFT(B,B:track_032) (B:e74)<br>g88 TRACK_APPEARED_LEFT(B,B:track_033) (B:e75)<br>g89 TRACK_APPEARED_LEFT(B,B:track_034) (B:e76)<br>g90 TRACK_APPEARED_LEFT(B,B:track_036) (B:e77)<br>g91 TRACK_APPEARED_LEFT(B,B:track_037) (B:e78)<br>g92 TRACK_APPEARED_LEFT(B,B:track_040) (B:e79)<br>g93 TRACK_APPEARED_RIGHT(B,B:track_035) (B:e80)<br>g94 CLOSING_START(B,B:track_032) (B:e81)<br>g95 CLOSING_START(B,B:track_033) (B:e82)<br>g96 CLOSING_START(B,B:track_034) (B:e83)<br>g97 CLOSING_START(B,B:track_035) (B:e84)<br>g98 CLOSING_START(B,B:track_036) (B:e85)<br>g99 CLOSING_START(B,B:track_037) (B:e86)<br>g100 CLOSING_START(B,B:track_040) (B:e87)<br>g102 TRACK_LOST(B,B:track_010) (B:e88)<br>g103 TRACK_LOST(B,B:track_011) (B:e89) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_010: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009 |
| +0.75 | A | g101 CRITICAL_TTC_START(A,B) (A:e15) | ego: MOVING, BRAKE<br>track_002: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +0.80 | B | g104 TRACK_APPEARED_LEFT(B,B:track_041) (B:e90)<br>g105 CLOSING_START(B,B:track_041) (B:e91)<br>g106 TRACK_LOST(B,B:track_014) (B:e92)<br>g107 TRACK_LOST(B,B:track_015) (B:e93)<br>g108 TRACK_LOST(B,B:track_021) (B:e94) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_014: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_015: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_021: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_040: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011 |
| +0.85 | B | g109 TRACK_APPEARED_LEFT(B,B:track_038) (B:e95)<br>g110 TRACK_APPEARED_LEFT(B,B:track_039) (B:e96)<br>g111 TRACK_APPEARED_LEFT(B,B:track_042) (B:e97)<br>g112 CLOSING_START(B,B:track_038) (B:e98)<br>g113 CLOSING_START(B,B:track_039) (B:e99)<br>g114 CLOSING_START(B,B:track_042) (B:e100)<br>g115 TRACK_LOST(B,B:track_016) (B:e101)<br>g116 TRACK_LOST(B,B:track_018) (B:e102) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_016: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_017: CLOSING<br>track_018: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_021 |
| +0.90 | B | g117 TRACK_LOST(B,B:track_019) (B:e103)<br>g118 TRACK_LOST(B,B:track_026) (B:e104) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_017: CLOSING<br>track_019: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_020: CLOSING<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_026: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_018, track_021 |
| +0.95 | B | g119 TRACK_LOST(B,B:track_017) (B:e105)<br>g120 TRACK_LOST(B,B:track_023) (B:e106)<br>g121 TRACK_LOST(B,B:track_027) (B:e107) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_017: CLOSING<br>track_020: CLOSING<br>track_022: CLOSING<br>track_023: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_024: CLOSING<br>track_025: CLOSING<br>track_027: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_018, track_019, track_021, track_026 |
| +1.00 | B | g122 CRITICAL_TTC_END(B,B:track_013) (B:e108)<br>g123 EGO_PATH_ENTRY(B,B:track_012) (B:e109)<br>g124 EGO_PATH_ENTRY(B,B:track_013) (B:e110)<br>g125 TRACK_LOST(B,B:track_033) (B:e111) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC<br>track_013: CLOSING, CRITICAL_TTC<br>track_020: CLOSING<br>track_022: CLOSING<br>track_024: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_033: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_026, track_027 |
| +1.05 | B | g126 CLOSING_END(B,B:track_024) (B:e112)<br>g127 CLOSING_END(B,B:track_031) (B:e113)<br>g128 CLOSING_END(B,B:track_034) (B:e114)<br>g129 TRACK_LOST(B,B:track_024) (B:e115)<br>g130 TRACK_LOST(B,B:track_031) (B:e116)<br>g131 TRACK_LOST(B,B:track_034) (B:e117) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_024: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_031: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_032: CLOSING<br>track_034: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_026, track_027, track_033 |
| +1.10 | B | g132 CRITICAL_TTC_END(B,B:track_012) (B:e118)<br>g133 CLOSING_END(B,B:track_030) (B:e119) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: CLOSING<br>track_032: CLOSING<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_031, track_033, track_034 |
| +1.15 | A | g134 CUT_IN_FROM_LEFT_END(A,B) (A:e16) | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 |
| +1.15 | B | g135 CLOSING_END(B,B:track_028) (B:e120)<br>g136 CLOSING_END(B,B:track_032) (B:e121)<br>g137 CLOSING_END(B,B:track_036) (B:e122)<br>g138 CLOSING_END(B,B:track_040) (B:e123)<br>g139 CLOSING_END(B,B:track_041) (B:e124)<br>g140 EGO_PATH_ENTRY(B,B:track_005) (B:e125)<br>g141 TRACK_LOST(B,B:track_028) (B:e126) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: CLOSING<br>track_028: CLOSING<br>track_029: CLOSING<br>track_030: no active state<br>track_032: CLOSING<br>track_035: CLOSING<br>track_036: CLOSING<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: CLOSING<br>track_041: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_031, track_033, track_034 |
| +1.20 | A | g142 CRITICAL_TTC_END(A,B) (A:e17)<br>g143 CLOSING_END(A,B) (A:e18) | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +1.20 | B | g144 CLOSING_END(B,B:track_025) (B:e127)<br>g145 CLOSING_END(B,B:track_037) (B:e128)<br>g146 CLOSING_END(B,B:track_038) (B:e129)<br>g147 CLOSING_END(B,B:track_039) (B:e130)<br>g148 CLOSING_END(B,B:track_042) (B:e131)<br>g149 TRACK_LOST(B,B:track_041) (B:e132) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: CLOSING<br>track_029: CLOSING<br>track_030: no active state<br>track_032: no active state<br>track_035: CLOSING<br>track_036: no active state<br>track_037: CLOSING<br>track_038: CLOSING<br>track_039: CLOSING<br>track_040: no active state<br>track_041: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_042: CLOSING<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034 |
| +1.25 | B | g150 CLOSING_END(B,B:track_001) (B:e133)<br>g151 CLOSING_END(B,B:track_003) (B:e134)<br>g152 CLOSING_END(B,B:track_005) (B:e135)<br>g153 CLOSING_END(B,B:track_006) (B:e136)<br>g154 CLOSING_END(B,B:track_012) (B:e137)<br>g155 CLOSING_END(B,B:track_013) (B:e138)<br>g156 CLOSING_END(B,B:track_020) (B:e139)<br>g157 CLOSING_END(B,B:track_029) (B:e140)<br>g158 CLOSING_END(B,B:track_035) (B:e141)<br>g159 TURN_RIGHT_END(B) (B:e142)<br>g160 MOVING_END(B) (B:e143)<br>g161 STOP_START(B) (B:e144) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_003: CLOSING<br>track_005: CLOSING, IN_EGO_PATH<br>track_006: CLOSING<br>track_012: CLOSING, IN_EGO_PATH<br>track_013: CLOSING, IN_EGO_PATH<br>track_020: CLOSING<br>track_022: CLOSING<br>track_025: no active state<br>track_029: CLOSING<br>track_030: no active state<br>track_032: no active state<br>track_035: CLOSING<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 |
| +1.30 | A | g162 MOVING_END(A) (A:e19)<br>g163 STOP_START(A) (A:e20) | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +1.35 | B | g164 CLOSING_END(B,B:track_022) (B:e145) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_022: CLOSING<br>track_025: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 |
| +1.70 | B | g165 TRACK_LOST(B,B:track_022) (B:e146) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_022: no active state<br>track_025: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 |
| +2.00 | B | g166 TRACK_LOST(B,B:track_025) (B:e147) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_025: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_026, track_027, track_028, track_031, track_033, track_034, track_041 |
| +2.05 | B | g167 EGO_PATH_ENTRY(B,B:track_006) (B:e148) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_031, track_033, track_034, track_041 |
| +2.70 | B | g168 EGO_PATH_EXIT(B,B:track_013) (B:e149) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: IN_EGO_PATH<br>track_020: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_031, track_033, track_034, track_041 |
| +3.00 | B | g169 TRACK_LOST(B,B:track_029) (B:e150) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: no active state<br>track_020: no active state<br>track_029: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_031, track_033, track_034, track_041 |
| +4.05 | B | g170 TRACK_LOST(B,B:track_037) (B:e151) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: no active state<br>track_020: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_037: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_029, track_031, track_033, track_034, track_041 |
| +4.25 | B | g171 TRACK_LOST(B,B:track_005) (B:e152)<br>g172 TRACK_LOST(B,B:track_035) (B:e153) | ego: STOP, BRAKE<br>track_001: no active state<br>track_003: no active state<br>track_005: IN_EGO_PATH<br>track_006: IN_EGO_PATH<br>track_012: IN_EGO_PATH<br>track_013: no active state<br>track_020: no active state<br>track_030: no active state<br>track_032: no active state<br>track_035: no active state<br>track_036: no active state<br>track_038: no active state<br>track_039: no active state<br>track_040: no active state<br>track_042: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_007, track_008, track_009, track_010, track_011, track_014, track_015, track_016, track_017, track_018, track_019, track_021, track_022, track_023, track_024, track_025, track_026, track_027, track_028, track_029, track_031, track_033, track_034, track_037, track_041 |

## Plain-language reading

- 5.65 s before the matched collision, A started moving (already the case when first observed).
- 5.65 s before the matched collision, B started moving (already the case when first observed).
- 5.50 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 5.50 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 4.90 s before the matched collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 4.85 s before the matched collision, B started braking.
- 2.90 s before the matched collision, A began exceeding the speed limit.
- 2.30 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 2.30 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A observed B cutting in from the left.
- 1.65 s before the matched collision, A's time-to-contact with B became critical.
- 0.20 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5216, B: 5216 N*s).
- At the matched collision, A returned within the speed limit.
- 0.05 s after the matched collision, A started braking.
- 0.10 s after the matched collision, B started turning right.
- 0.20 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.25 s after the matched collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 0.25 s after the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 0.25 s after the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 0.25 s after the matched collision, B's radar started tracking unidentified object B:track_022, which appeared on its right.
- 0.25 s after the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 0.25 s after the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.25 s after the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.25 s after the matched collision, B observed unidentified object B:track_022 start closing in (already the case when first observed).
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its right.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_006, which appeared on its right.
- 0.30 s after the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.30 s after the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.30 s after the matched collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.40 s after the matched collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- 0.40 s after the matched collision, B's radar started tracking unidentified object B:track_009, which appeared on its left.
- 0.40 s after the matched collision, B's radar started tracking unidentified object B:track_008, which appeared on its right.
- 0.40 s after the matched collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- 0.40 s after the matched collision, B observed unidentified object B:track_008 start closing in (already the case when first observed).
- 0.40 s after the matched collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 0.45 s after the matched collision, B's radar started tracking unidentified object B:track_010, which appeared on its left.
- 0.45 s after the matched collision, B's radar started tracking unidentified object B:track_011, which appeared on its left.
- 0.45 s after the matched collision, B's radar started tracking unidentified object B:track_015, which appeared on its left.
- 0.45 s after the matched collision, B's radar started tracking unidentified object B:track_020, which appeared on its right.
- 0.45 s after the matched collision, B's radar started tracking unidentified object B:track_029, which appeared on its right.
- 0.45 s after the matched collision, B observed unidentified object B:track_010 start closing in (already the case when first observed).
- 0.45 s after the matched collision, B observed unidentified object B:track_011 start closing in (already the case when first observed).
- 0.45 s after the matched collision, B observed unidentified object B:track_015 start closing in (already the case when first observed).
- 0.45 s after the matched collision, B observed unidentified object B:track_020 start closing in (already the case when first observed).
- 0.45 s after the matched collision, B observed unidentified object B:track_029 start closing in (already the case when first observed).
- 0.50 s after the matched collision, B's radar started tracking unidentified object B:track_014, which appeared on its left.
- 0.50 s after the matched collision, B's radar started tracking unidentified object B:track_016, which appeared on its left.
- 0.50 s after the matched collision, B's radar started tracking unidentified object B:track_021, which appeared on its left.
- 0.50 s after the matched collision, B's radar started tracking unidentified object B:track_012, which appeared on its right.
- 0.50 s after the matched collision, B's radar started tracking unidentified object B:track_013, which appeared on its right.
- 0.50 s after the matched collision, B observed unidentified object B:track_012 start closing in (already the case when first observed).
- 0.50 s after the matched collision, B observed unidentified object B:track_013 start closing in (already the case when first observed).
- 0.50 s after the matched collision, B observed unidentified object B:track_014 start closing in (already the case when first observed).
- 0.50 s after the matched collision, B observed unidentified object B:track_016 start closing in (already the case when first observed).
- 0.50 s after the matched collision, B observed unidentified object B:track_021 start closing in (already the case when first observed).
- 0.50 s after the matched collision, B's time-to-contact with unidentified object B:track_012 became critical (already the case when first observed).
- 0.50 s after the matched collision, B's time-to-contact with unidentified object B:track_013 became critical (already the case when first observed).
- 0.55 s after the matched collision, B's radar started tracking unidentified object B:track_017, which appeared on its left.
- 0.55 s after the matched collision, B's radar started tracking unidentified object B:track_018, which appeared on its left.
- 0.55 s after the matched collision, B's radar started tracking unidentified object B:track_019, which appeared on its left.
- 0.55 s after the matched collision, B's radar started tracking unidentified object B:track_026, which appeared on its left.
- 0.55 s after the matched collision, B observed unidentified object B:track_017 start closing in (already the case when first observed).
- 0.55 s after the matched collision, B observed unidentified object B:track_018 start closing in (already the case when first observed).
- 0.55 s after the matched collision, B observed unidentified object B:track_019 start closing in (already the case when first observed).
- 0.55 s after the matched collision, B observed unidentified object B:track_026 start closing in (already the case when first observed).
- 0.60 s after the matched collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_023, which appeared on its left.
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_024, which appeared on its left.
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_025, which appeared on its left.
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_027, which appeared on its left.
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_030, which appeared on its left.
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_031, which appeared on its left.
- 0.65 s after the matched collision, B observed unidentified object B:track_023 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B observed unidentified object B:track_024 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B observed unidentified object B:track_025 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B observed unidentified object B:track_027 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B observed unidentified object B:track_030 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B observed unidentified object B:track_031 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the matched collision, B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the matched collision, B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the matched collision, B's radar lost unidentified object B:track_009 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_028, which appeared on its left.
- 0.70 s after the matched collision, B observed unidentified object B:track_028 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_032, which appeared on its left.
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_033, which appeared on its left.
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_034, which appeared on its left.
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_036, which appeared on its left.
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_037, which appeared on its left.
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_040, which appeared on its left.
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_035, which appeared on its right.
- 0.75 s after the matched collision, B observed unidentified object B:track_032 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B observed unidentified object B:track_033 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B observed unidentified object B:track_034 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B observed unidentified object B:track_035 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B observed unidentified object B:track_036 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B observed unidentified object B:track_037 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B observed unidentified object B:track_040 start closing in (already the case when first observed).
- 0.75 s after the matched collision, A's time-to-contact with B became critical.
- 0.75 s after the matched collision, B's radar lost unidentified object B:track_010 (its states are UNKNOWN from then on, not ended).
- 0.75 s after the matched collision, B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the matched collision, B's radar started tracking unidentified object B:track_041, which appeared on its left.
- 0.80 s after the matched collision, B observed unidentified object B:track_041 start closing in (already the case when first observed).
- 0.80 s after the matched collision, B's radar lost unidentified object B:track_014 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the matched collision, B's radar lost unidentified object B:track_015 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the matched collision, B's radar lost unidentified object B:track_021 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the matched collision, B's radar started tracking unidentified object B:track_038, which appeared on its left.
- 0.85 s after the matched collision, B's radar started tracking unidentified object B:track_039, which appeared on its left.
- 0.85 s after the matched collision, B's radar started tracking unidentified object B:track_042, which appeared on its left.
- 0.85 s after the matched collision, B observed unidentified object B:track_038 start closing in (already the case when first observed).
- 0.85 s after the matched collision, B observed unidentified object B:track_039 start closing in (already the case when first observed).
- 0.85 s after the matched collision, B observed unidentified object B:track_042 start closing in (already the case when first observed).
- 0.85 s after the matched collision, B's radar lost unidentified object B:track_016 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the matched collision, B's radar lost unidentified object B:track_018 (its states are UNKNOWN from then on, not ended).
- 0.90 s after the matched collision, B's radar lost unidentified object B:track_019 (its states are UNKNOWN from then on, not ended).
- 0.90 s after the matched collision, B's radar lost unidentified object B:track_026 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the matched collision, B's radar lost unidentified object B:track_017 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the matched collision, B's radar lost unidentified object B:track_023 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the matched collision, B's radar lost unidentified object B:track_027 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the matched collision, B's time-to-contact with unidentified object B:track_013 stopped being critical.
- 1.00 s after the matched collision, B observed unidentified object B:track_012 enter its forward path corridor.
- 1.00 s after the matched collision, B observed unidentified object B:track_013 enter its forward path corridor.
- 1.00 s after the matched collision, B's radar lost unidentified object B:track_033 (its states are UNKNOWN from then on, not ended).
- 1.05 s after the matched collision, B observed unidentified object B:track_024 stop closing in.
- 1.05 s after the matched collision, B observed unidentified object B:track_031 stop closing in.
- 1.05 s after the matched collision, B observed unidentified object B:track_034 stop closing in.
- 1.05 s after the matched collision, B's radar lost unidentified object B:track_024 (its states are UNKNOWN from then on, not ended).
- 1.05 s after the matched collision, B's radar lost unidentified object B:track_031 (its states are UNKNOWN from then on, not ended).
- 1.05 s after the matched collision, B's radar lost unidentified object B:track_034 (its states are UNKNOWN from then on, not ended).
- 1.10 s after the matched collision, B's time-to-contact with unidentified object B:track_012 stopped being critical.
- 1.10 s after the matched collision, B observed unidentified object B:track_030 stop closing in.
- 1.15 s after the matched collision, A observed B's cut-in from the left settle.
- 1.15 s after the matched collision, B observed unidentified object B:track_028 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_032 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_036 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_040 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_041 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_005 enter its forward path corridor.
- 1.15 s after the matched collision, B's radar lost unidentified object B:track_028 (its states are UNKNOWN from then on, not ended).
- 1.20 s after the matched collision, A's time-to-contact with B stopped being critical.
- 1.20 s after the matched collision, A observed B stop closing in.
- 1.20 s after the matched collision, B observed unidentified object B:track_025 stop closing in.
- 1.20 s after the matched collision, B observed unidentified object B:track_037 stop closing in.
- 1.20 s after the matched collision, B observed unidentified object B:track_038 stop closing in.
- 1.20 s after the matched collision, B observed unidentified object B:track_039 stop closing in.
- 1.20 s after the matched collision, B observed unidentified object B:track_042 stop closing in.
- 1.20 s after the matched collision, B's radar lost unidentified object B:track_041 (its states are UNKNOWN from then on, not ended).
- 1.25 s after the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_005 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_006 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_012 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_013 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_020 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_029 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_035 stop closing in.
- 1.25 s after the matched collision, B stopped turning right.
- 1.25 s after the matched collision, B stopped moving.
- 1.25 s after the matched collision, B came to a stop.
- 1.30 s after the matched collision, A stopped moving.
- 1.30 s after the matched collision, A came to a stop.
- 1.35 s after the matched collision, B observed unidentified object B:track_022 stop closing in.
- 1.70 s after the matched collision, B's radar lost unidentified object B:track_022 (its states are UNKNOWN from then on, not ended).
- 2.00 s after the matched collision, B's radar lost unidentified object B:track_025 (its states are UNKNOWN from then on, not ended).
- 2.05 s after the matched collision, B observed unidentified object B:track_006 enter its forward path corridor.
- 2.70 s after the matched collision, B observed unidentified object B:track_013 leave its forward path corridor.
- 3.00 s after the matched collision, B's radar lost unidentified object B:track_029 (its states are UNKNOWN from then on, not ended).
- 4.05 s after the matched collision, B's radar lost unidentified object B:track_037 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the matched collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the matched collision, B's radar lost unidentified object B:track_035 (its states are UNKNOWN from then on, not ended).
