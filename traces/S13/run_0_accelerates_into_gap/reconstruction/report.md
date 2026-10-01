# Reconstruction report - S13/run_0_accelerates_into_gap

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 9.95 s | 101 | 20 | 35 | 2 | A:e11 @ 5.65 s |
| B | 9.95 s | 101 | 153 | 753 | 42 | B:e03 @ 5.65 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

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

## Global graph

172 nodes, 998 edges; 1 merged node(s): g13 COLLISION(A,B) from A:e11 + B:e03.

### Event sequence (global time)

- `-5.65` MOVING_START(A); MOVING_START(B)
- `-5.50` TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001)
- `-4.90` TRACK_LOST(A,A:track_001)
- `-4.85` BRAKE_START(B)
- `-2.90` SPEED_LIMIT_EXCEEDED_START(A)
- `-2.30` TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-1.80` CUT_IN_FROM_LEFT_START(A,B)
- `-1.65` CRITICAL_TTC_START(A,B)
- `-0.20` EGO_PATH_ENTRY(A,B)
- `+0.00` COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A)
- `+0.05` BRAKE_START(A)
- `+0.10` TURN_RIGHT_START(B)
- `+0.20` CRITICAL_TTC_END(A,B)
- `+0.25` TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_022); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_022)
- `+0.30` TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); TRACK_APPEARED_RIGHT(B,B:track_006); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006)
- `+0.40` TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008); CLOSING_START(B,B:track_009)
- `+0.45` TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_LEFT(B,B:track_011); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_RIGHT(B,B:track_020); TRACK_APPEARED_RIGHT(B,B:track_029); CLOSING_START(B,B:track_010); CLOSING_START(B,B:track_011); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_020); CLOSING_START(B,B:track_029)
- `+0.50` TRACK_APPEARED_LEFT(B,B:track_014); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_021); TRACK_APPEARED_RIGHT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_013); CLOSING_START(B,B:track_012); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_021); CRITICAL_TTC_START(B,B:track_012); CRITICAL_TTC_START(B,B:track_013)
- `+0.55` TRACK_APPEARED_LEFT(B,B:track_017); TRACK_APPEARED_LEFT(B,B:track_018); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_APPEARED_LEFT(B,B:track_026); CLOSING_START(B,B:track_017); CLOSING_START(B,B:track_018); CLOSING_START(B,B:track_019); CLOSING_START(B,B:track_026)
- `+0.60` TRACK_LOST(B,B:track_004)
- `+0.65` TRACK_APPEARED_LEFT(B,B:track_023); TRACK_APPEARED_LEFT(B,B:track_024); TRACK_APPEARED_LEFT(B,B:track_025); TRACK_APPEARED_LEFT(B,B:track_027); TRACK_APPEARED_LEFT(B,B:track_030); TRACK_APPEARED_LEFT(B,B:track_031); CLOSING_START(B,B:track_023); CLOSING_START(B,B:track_024); CLOSING_START(B,B:track_025); CLOSING_START(B,B:track_027); CLOSING_START(B,B:track_030); CLOSING_START(B,B:track_031); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_008); TRACK_LOST(B,B:track_009)
- `+0.70` TRACK_APPEARED_LEFT(B,B:track_028); CLOSING_START(B,B:track_028)
- `+0.75` TRACK_APPEARED_LEFT(B,B:track_032); TRACK_APPEARED_LEFT(B,B:track_033); TRACK_APPEARED_LEFT(B,B:track_034); TRACK_APPEARED_LEFT(B,B:track_036); TRACK_APPEARED_LEFT(B,B:track_037); TRACK_APPEARED_LEFT(B,B:track_040); TRACK_APPEARED_RIGHT(B,B:track_035); CLOSING_START(B,B:track_032); CLOSING_START(B,B:track_033); CLOSING_START(B,B:track_034); CLOSING_START(B,B:track_035); CLOSING_START(B,B:track_036); CLOSING_START(B,B:track_037); CLOSING_START(B,B:track_040); CRITICAL_TTC_START(A,B); TRACK_LOST(B,B:track_010); TRACK_LOST(B,B:track_011)
- `+0.80` TRACK_APPEARED_LEFT(B,B:track_041); CLOSING_START(B,B:track_041); TRACK_LOST(B,B:track_014); TRACK_LOST(B,B:track_015); TRACK_LOST(B,B:track_021)
- `+0.85` TRACK_APPEARED_LEFT(B,B:track_038); TRACK_APPEARED_LEFT(B,B:track_039); TRACK_APPEARED_LEFT(B,B:track_042); CLOSING_START(B,B:track_038); CLOSING_START(B,B:track_039); CLOSING_START(B,B:track_042); TRACK_LOST(B,B:track_016); TRACK_LOST(B,B:track_018)
- `+0.90` TRACK_LOST(B,B:track_019); TRACK_LOST(B,B:track_026)
- `+0.95` TRACK_LOST(B,B:track_017); TRACK_LOST(B,B:track_023); TRACK_LOST(B,B:track_027)
- `+1.00` CRITICAL_TTC_END(B,B:track_013); EGO_PATH_ENTRY(B,B:track_012); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_033)
- `+1.05` CLOSING_END(B,B:track_024); CLOSING_END(B,B:track_031); CLOSING_END(B,B:track_034); TRACK_LOST(B,B:track_024); TRACK_LOST(B,B:track_031); TRACK_LOST(B,B:track_034)
- `+1.10` CRITICAL_TTC_END(B,B:track_012); CLOSING_END(B,B:track_030)
- `+1.15` CUT_IN_FROM_LEFT_END(A,B); CLOSING_END(B,B:track_028); CLOSING_END(B,B:track_032); CLOSING_END(B,B:track_036); CLOSING_END(B,B:track_040); CLOSING_END(B,B:track_041); EGO_PATH_ENTRY(B,B:track_005); TRACK_LOST(B,B:track_028)
- `+1.20` CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_025); CLOSING_END(B,B:track_037); CLOSING_END(B,B:track_038); CLOSING_END(B,B:track_039); CLOSING_END(B,B:track_042); TRACK_LOST(B,B:track_041)
- `+1.25` CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_006); CLOSING_END(B,B:track_012); CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_020); CLOSING_END(B,B:track_029); CLOSING_END(B,B:track_035); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
- `+1.30` MOVING_END(A); STOP_START(A)
- `+1.35` CLOSING_END(B,B:track_022)
- `+1.70` TRACK_LOST(B,B:track_022)
- `+2.00` TRACK_LOST(B,B:track_025)
- `+2.05` EGO_PATH_ENTRY(B,B:track_006)
- `+2.70` EGO_PATH_EXIT(B,B:track_013)
- `+3.00` TRACK_LOST(B,B:track_029)
- `+4.05` TRACK_LOST(B,B:track_037)
- `+4.25` TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_035)

### What happened, in plain language

- 5.65 s before the reference collision, A started moving (already the case when first observed).
- 5.65 s before the reference collision, B started moving (already the case when first observed).
- 5.50 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- 5.50 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 4.90 s before the reference collision, A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- 4.85 s before the reference collision, B started braking.
- 2.90 s before the reference collision, A began exceeding the speed limit.
- 2.30 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 2.30 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the reference collision, A observed B cutting in from the left.
- 1.65 s before the reference collision, A's time-to-contact with B became critical.
- 0.20 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 5216, B: 5216 N*s).
- At the reference collision, A returned within the speed limit.
- 0.05 s after the reference collision, A started braking.
- 0.10 s after the reference collision, B started turning right.
- 0.20 s after the reference collision, A's time-to-contact with B stopped being critical.
- 0.25 s after the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 0.25 s after the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 0.25 s after the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 0.25 s after the reference collision, B's radar started tracking unidentified object B:track_022, which appeared on its right.
- 0.25 s after the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 0.25 s after the reference collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.25 s after the reference collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.25 s after the reference collision, B observed unidentified object B:track_022 start closing in (already the case when first observed).
- 0.30 s after the reference collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 0.30 s after the reference collision, B's radar started tracking unidentified object B:track_005, which appeared on its right.
- 0.30 s after the reference collision, B's radar started tracking unidentified object B:track_006, which appeared on its right.
- 0.30 s after the reference collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.30 s after the reference collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.30 s after the reference collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.40 s after the reference collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- 0.40 s after the reference collision, B's radar started tracking unidentified object B:track_009, which appeared on its left.
- 0.40 s after the reference collision, B's radar started tracking unidentified object B:track_008, which appeared on its right.
- 0.40 s after the reference collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- 0.40 s after the reference collision, B observed unidentified object B:track_008 start closing in (already the case when first observed).
- 0.40 s after the reference collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 0.45 s after the reference collision, B's radar started tracking unidentified object B:track_010, which appeared on its left.
- 0.45 s after the reference collision, B's radar started tracking unidentified object B:track_011, which appeared on its left.
- 0.45 s after the reference collision, B's radar started tracking unidentified object B:track_015, which appeared on its left.
- 0.45 s after the reference collision, B's radar started tracking unidentified object B:track_020, which appeared on its right.
- 0.45 s after the reference collision, B's radar started tracking unidentified object B:track_029, which appeared on its right.
- 0.45 s after the reference collision, B observed unidentified object B:track_010 start closing in (already the case when first observed).
- 0.45 s after the reference collision, B observed unidentified object B:track_011 start closing in (already the case when first observed).
- 0.45 s after the reference collision, B observed unidentified object B:track_015 start closing in (already the case when first observed).
- 0.45 s after the reference collision, B observed unidentified object B:track_020 start closing in (already the case when first observed).
- 0.45 s after the reference collision, B observed unidentified object B:track_029 start closing in (already the case when first observed).
- 0.50 s after the reference collision, B's radar started tracking unidentified object B:track_014, which appeared on its left.
- 0.50 s after the reference collision, B's radar started tracking unidentified object B:track_016, which appeared on its left.
- 0.50 s after the reference collision, B's radar started tracking unidentified object B:track_021, which appeared on its left.
- 0.50 s after the reference collision, B's radar started tracking unidentified object B:track_012, which appeared on its right.
- 0.50 s after the reference collision, B's radar started tracking unidentified object B:track_013, which appeared on its right.
- 0.50 s after the reference collision, B observed unidentified object B:track_012 start closing in (already the case when first observed).
- 0.50 s after the reference collision, B observed unidentified object B:track_013 start closing in (already the case when first observed).
- 0.50 s after the reference collision, B observed unidentified object B:track_014 start closing in (already the case when first observed).
- 0.50 s after the reference collision, B observed unidentified object B:track_016 start closing in (already the case when first observed).
- 0.50 s after the reference collision, B observed unidentified object B:track_021 start closing in (already the case when first observed).
- 0.50 s after the reference collision, B's time-to-contact with unidentified object B:track_012 became critical (already the case when first observed).
- 0.50 s after the reference collision, B's time-to-contact with unidentified object B:track_013 became critical (already the case when first observed).
- 0.55 s after the reference collision, B's radar started tracking unidentified object B:track_017, which appeared on its left.
- 0.55 s after the reference collision, B's radar started tracking unidentified object B:track_018, which appeared on its left.
- 0.55 s after the reference collision, B's radar started tracking unidentified object B:track_019, which appeared on its left.
- 0.55 s after the reference collision, B's radar started tracking unidentified object B:track_026, which appeared on its left.
- 0.55 s after the reference collision, B observed unidentified object B:track_017 start closing in (already the case when first observed).
- 0.55 s after the reference collision, B observed unidentified object B:track_018 start closing in (already the case when first observed).
- 0.55 s after the reference collision, B observed unidentified object B:track_019 start closing in (already the case when first observed).
- 0.55 s after the reference collision, B observed unidentified object B:track_026 start closing in (already the case when first observed).
- 0.60 s after the reference collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the reference collision, B's radar started tracking unidentified object B:track_023, which appeared on its left.
- 0.65 s after the reference collision, B's radar started tracking unidentified object B:track_024, which appeared on its left.
- 0.65 s after the reference collision, B's radar started tracking unidentified object B:track_025, which appeared on its left.
- 0.65 s after the reference collision, B's radar started tracking unidentified object B:track_027, which appeared on its left.
- 0.65 s after the reference collision, B's radar started tracking unidentified object B:track_030, which appeared on its left.
- 0.65 s after the reference collision, B's radar started tracking unidentified object B:track_031, which appeared on its left.
- 0.65 s after the reference collision, B observed unidentified object B:track_023 start closing in (already the case when first observed).
- 0.65 s after the reference collision, B observed unidentified object B:track_024 start closing in (already the case when first observed).
- 0.65 s after the reference collision, B observed unidentified object B:track_025 start closing in (already the case when first observed).
- 0.65 s after the reference collision, B observed unidentified object B:track_027 start closing in (already the case when first observed).
- 0.65 s after the reference collision, B observed unidentified object B:track_030 start closing in (already the case when first observed).
- 0.65 s after the reference collision, B observed unidentified object B:track_031 start closing in (already the case when first observed).
- 0.65 s after the reference collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the reference collision, B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the reference collision, B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- 0.65 s after the reference collision, B's radar lost unidentified object B:track_009 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, B's radar started tracking unidentified object B:track_028, which appeared on its left.
- 0.70 s after the reference collision, B observed unidentified object B:track_028 start closing in (already the case when first observed).
- 0.75 s after the reference collision, B's radar started tracking unidentified object B:track_032, which appeared on its left.
- 0.75 s after the reference collision, B's radar started tracking unidentified object B:track_033, which appeared on its left.
- 0.75 s after the reference collision, B's radar started tracking unidentified object B:track_034, which appeared on its left.
- 0.75 s after the reference collision, B's radar started tracking unidentified object B:track_036, which appeared on its left.
- 0.75 s after the reference collision, B's radar started tracking unidentified object B:track_037, which appeared on its left.
- 0.75 s after the reference collision, B's radar started tracking unidentified object B:track_040, which appeared on its left.
- 0.75 s after the reference collision, B's radar started tracking unidentified object B:track_035, which appeared on its right.
- 0.75 s after the reference collision, B observed unidentified object B:track_032 start closing in (already the case when first observed).
- 0.75 s after the reference collision, B observed unidentified object B:track_033 start closing in (already the case when first observed).
- 0.75 s after the reference collision, B observed unidentified object B:track_034 start closing in (already the case when first observed).
- 0.75 s after the reference collision, B observed unidentified object B:track_035 start closing in (already the case when first observed).
- 0.75 s after the reference collision, B observed unidentified object B:track_036 start closing in (already the case when first observed).
- 0.75 s after the reference collision, B observed unidentified object B:track_037 start closing in (already the case when first observed).
- 0.75 s after the reference collision, B observed unidentified object B:track_040 start closing in (already the case when first observed).
- 0.75 s after the reference collision, A's time-to-contact with B became critical.
- 0.75 s after the reference collision, B's radar lost unidentified object B:track_010 (its states are UNKNOWN from then on, not ended).
- 0.75 s after the reference collision, B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, B's radar started tracking unidentified object B:track_041, which appeared on its left.
- 0.80 s after the reference collision, B observed unidentified object B:track_041 start closing in (already the case when first observed).
- 0.80 s after the reference collision, B's radar lost unidentified object B:track_014 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, B's radar lost unidentified object B:track_015 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, B's radar lost unidentified object B:track_021 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the reference collision, B's radar started tracking unidentified object B:track_038, which appeared on its left.
- 0.85 s after the reference collision, B's radar started tracking unidentified object B:track_039, which appeared on its left.
- 0.85 s after the reference collision, B's radar started tracking unidentified object B:track_042, which appeared on its left.
- 0.85 s after the reference collision, B observed unidentified object B:track_038 start closing in (already the case when first observed).
- 0.85 s after the reference collision, B observed unidentified object B:track_039 start closing in (already the case when first observed).
- 0.85 s after the reference collision, B observed unidentified object B:track_042 start closing in (already the case when first observed).
- 0.85 s after the reference collision, B's radar lost unidentified object B:track_016 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the reference collision, B's radar lost unidentified object B:track_018 (its states are UNKNOWN from then on, not ended).
- 0.90 s after the reference collision, B's radar lost unidentified object B:track_019 (its states are UNKNOWN from then on, not ended).
- 0.90 s after the reference collision, B's radar lost unidentified object B:track_026 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the reference collision, B's radar lost unidentified object B:track_017 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the reference collision, B's radar lost unidentified object B:track_023 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the reference collision, B's radar lost unidentified object B:track_027 (its states are UNKNOWN from then on, not ended).
- 1.00 s after the reference collision, B's time-to-contact with unidentified object B:track_013 stopped being critical.
- 1.00 s after the reference collision, B observed unidentified object B:track_012 enter its forward path corridor.
- 1.00 s after the reference collision, B observed unidentified object B:track_013 enter its forward path corridor.
- 1.00 s after the reference collision, B's radar lost unidentified object B:track_033 (its states are UNKNOWN from then on, not ended).
- 1.05 s after the reference collision, B observed unidentified object B:track_024 stop closing in.
- 1.05 s after the reference collision, B observed unidentified object B:track_031 stop closing in.
- 1.05 s after the reference collision, B observed unidentified object B:track_034 stop closing in.
- 1.05 s after the reference collision, B's radar lost unidentified object B:track_024 (its states are UNKNOWN from then on, not ended).
- 1.05 s after the reference collision, B's radar lost unidentified object B:track_031 (its states are UNKNOWN from then on, not ended).
- 1.05 s after the reference collision, B's radar lost unidentified object B:track_034 (its states are UNKNOWN from then on, not ended).
- 1.10 s after the reference collision, B's time-to-contact with unidentified object B:track_012 stopped being critical.
- 1.10 s after the reference collision, B observed unidentified object B:track_030 stop closing in.
- 1.15 s after the reference collision, A observed B's cut-in from the left settle.
- 1.15 s after the reference collision, B observed unidentified object B:track_028 stop closing in.
- 1.15 s after the reference collision, B observed unidentified object B:track_032 stop closing in.
- 1.15 s after the reference collision, B observed unidentified object B:track_036 stop closing in.
- 1.15 s after the reference collision, B observed unidentified object B:track_040 stop closing in.
- 1.15 s after the reference collision, B observed unidentified object B:track_041 stop closing in.
- 1.15 s after the reference collision, B observed unidentified object B:track_005 enter its forward path corridor.
- 1.15 s after the reference collision, B's radar lost unidentified object B:track_028 (its states are UNKNOWN from then on, not ended).
- 1.20 s after the reference collision, A's time-to-contact with B stopped being critical.
- 1.20 s after the reference collision, A observed B stop closing in.
- 1.20 s after the reference collision, B observed unidentified object B:track_025 stop closing in.
- 1.20 s after the reference collision, B observed unidentified object B:track_037 stop closing in.
- 1.20 s after the reference collision, B observed unidentified object B:track_038 stop closing in.
- 1.20 s after the reference collision, B observed unidentified object B:track_039 stop closing in.
- 1.20 s after the reference collision, B observed unidentified object B:track_042 stop closing in.
- 1.20 s after the reference collision, B's radar lost unidentified object B:track_041 (its states are UNKNOWN from then on, not ended).
- 1.25 s after the reference collision, B observed unidentified object B:track_001 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_003 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_005 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_006 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_012 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_013 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_020 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_029 stop closing in.
- 1.25 s after the reference collision, B observed unidentified object B:track_035 stop closing in.
- 1.25 s after the reference collision, B stopped turning right.
- 1.25 s after the reference collision, B stopped moving.
- 1.25 s after the reference collision, B came to a stop.
- 1.30 s after the reference collision, A stopped moving.
- 1.30 s after the reference collision, A came to a stop.
- 1.35 s after the reference collision, B observed unidentified object B:track_022 stop closing in.
- 1.70 s after the reference collision, B's radar lost unidentified object B:track_022 (its states are UNKNOWN from then on, not ended).
- 2.00 s after the reference collision, B's radar lost unidentified object B:track_025 (its states are UNKNOWN from then on, not ended).
- 2.05 s after the reference collision, B observed unidentified object B:track_006 enter its forward path corridor.
- 2.70 s after the reference collision, B observed unidentified object B:track_013 leave its forward path corridor.
- 3.00 s after the reference collision, B's radar lost unidentified object B:track_029 (its states are UNKNOWN from then on, not ended).
- 4.05 s after the reference collision, B's radar lost unidentified object B:track_037 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the reference collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 4.25 s after the reference collision, B's radar lost unidentified object B:track_035 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_002 (B): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 3.85 < CRITICAL_TTC_START 4.00 (+0.15 s) < COLLISION with B 5.65 (+1.65 s); EGO_PATH_ENTRY 5.45 after critical TTC (+1.45 s) [local times; t_global: cut_in -1.80, critical_ttc_start -1.65, ego_path_entry -0.20, collision +0.00]
- B's track_005 (unidentified B:track_005): EGO_PATH_ENTRY 6.80, no critical TTC [local times; t_global: ego_path_entry +1.15]
- B's track_006 (unidentified B:track_006): EGO_PATH_ENTRY 7.70, no critical TTC [local times; t_global: ego_path_entry +2.05]
- B's track_012 (unidentified B:track_012): CRITICAL_TTC_START 6.15; EGO_PATH_ENTRY 6.65 after critical TTC (+0.50 s) [local times; t_global: critical_ttc_start +0.50, ego_path_entry +1.00]
- B's track_013 (unidentified B:track_013): CRITICAL_TTC_START 6.15; EGO_PATH_ENTRY 6.65 after critical TTC (+0.50 s) [local times; t_global: critical_ttc_start +0.50, ego_path_entry +1.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED_LEFT(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A)
- TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_022); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_022)
- TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); TRACK_APPEARED_RIGHT(B,B:track_006); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006)
- TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008); CLOSING_START(B,B:track_009)
- TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_LEFT(B,B:track_011); TRACK_APPEARED_LEFT(B,B:track_015); TRACK_APPEARED_RIGHT(B,B:track_020); TRACK_APPEARED_RIGHT(B,B:track_029); CLOSING_START(B,B:track_010); CLOSING_START(B,B:track_011); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_020); CLOSING_START(B,B:track_029)
- TRACK_APPEARED_LEFT(B,B:track_014); TRACK_APPEARED_LEFT(B,B:track_016); TRACK_APPEARED_LEFT(B,B:track_021); TRACK_APPEARED_RIGHT(B,B:track_012); TRACK_APPEARED_RIGHT(B,B:track_013); CLOSING_START(B,B:track_012); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); CLOSING_START(B,B:track_016); CLOSING_START(B,B:track_021); CRITICAL_TTC_START(B,B:track_012); CRITICAL_TTC_START(B,B:track_013)
- TRACK_APPEARED_LEFT(B,B:track_017); TRACK_APPEARED_LEFT(B,B:track_018); TRACK_APPEARED_LEFT(B,B:track_019); TRACK_APPEARED_LEFT(B,B:track_026); CLOSING_START(B,B:track_017); CLOSING_START(B,B:track_018); CLOSING_START(B,B:track_019); CLOSING_START(B,B:track_026)
- TRACK_APPEARED_LEFT(B,B:track_023); TRACK_APPEARED_LEFT(B,B:track_024); TRACK_APPEARED_LEFT(B,B:track_025); TRACK_APPEARED_LEFT(B,B:track_027); TRACK_APPEARED_LEFT(B,B:track_030); TRACK_APPEARED_LEFT(B,B:track_031); CLOSING_START(B,B:track_023); CLOSING_START(B,B:track_024); CLOSING_START(B,B:track_025); CLOSING_START(B,B:track_027); CLOSING_START(B,B:track_030); CLOSING_START(B,B:track_031); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_008); TRACK_LOST(B,B:track_009)
- TRACK_APPEARED_LEFT(B,B:track_028); CLOSING_START(B,B:track_028)
- TRACK_APPEARED_LEFT(B,B:track_032); TRACK_APPEARED_LEFT(B,B:track_033); TRACK_APPEARED_LEFT(B,B:track_034); TRACK_APPEARED_LEFT(B,B:track_036); TRACK_APPEARED_LEFT(B,B:track_037); TRACK_APPEARED_LEFT(B,B:track_040); TRACK_APPEARED_RIGHT(B,B:track_035); CLOSING_START(B,B:track_032); CLOSING_START(B,B:track_033); CLOSING_START(B,B:track_034); CLOSING_START(B,B:track_035); CLOSING_START(B,B:track_036); CLOSING_START(B,B:track_037); CLOSING_START(B,B:track_040); CRITICAL_TTC_START(A,B); TRACK_LOST(B,B:track_010); TRACK_LOST(B,B:track_011)
- TRACK_APPEARED_LEFT(B,B:track_041); CLOSING_START(B,B:track_041); TRACK_LOST(B,B:track_014); TRACK_LOST(B,B:track_015); TRACK_LOST(B,B:track_021)
- TRACK_APPEARED_LEFT(B,B:track_038); TRACK_APPEARED_LEFT(B,B:track_039); TRACK_APPEARED_LEFT(B,B:track_042); CLOSING_START(B,B:track_038); CLOSING_START(B,B:track_039); CLOSING_START(B,B:track_042); TRACK_LOST(B,B:track_016); TRACK_LOST(B,B:track_018)
- TRACK_LOST(B,B:track_019); TRACK_LOST(B,B:track_026)
- TRACK_LOST(B,B:track_017); TRACK_LOST(B,B:track_023); TRACK_LOST(B,B:track_027)
- CRITICAL_TTC_END(B,B:track_013); EGO_PATH_ENTRY(B,B:track_012); EGO_PATH_ENTRY(B,B:track_013); TRACK_LOST(B,B:track_033)
- CLOSING_END(B,B:track_024); CLOSING_END(B,B:track_031); CLOSING_END(B,B:track_034); TRACK_LOST(B,B:track_024); TRACK_LOST(B,B:track_031); TRACK_LOST(B,B:track_034)
- CRITICAL_TTC_END(B,B:track_012); CLOSING_END(B,B:track_030)
- CUT_IN_FROM_LEFT_END(A,B); CLOSING_END(B,B:track_028); CLOSING_END(B,B:track_032); CLOSING_END(B,B:track_036); CLOSING_END(B,B:track_040); CLOSING_END(B,B:track_041); EGO_PATH_ENTRY(B,B:track_005); TRACK_LOST(B,B:track_028)
- CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_025); CLOSING_END(B,B:track_037); CLOSING_END(B,B:track_038); CLOSING_END(B,B:track_039); CLOSING_END(B,B:track_042); TRACK_LOST(B,B:track_041)
- CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_006); CLOSING_END(B,B:track_012); CLOSING_END(B,B:track_013); CLOSING_END(B,B:track_020); CLOSING_END(B,B:track_029); CLOSING_END(B,B:track_035); TURN_RIGHT_END(B); MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)
- TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_035)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 0.15 s); the track was lost at 0.75 s
- EGO_PATH of track_002, since A:e10 (t = 5.45 s)
- BRAKE, since A:e13 (t = 5.70 s)
- STOP, since A:e20 (t = 6.95 s)
B:
- BRAKE, since B:e02 (t = 0.80 s)
- CLOSING of track_002, since B:e10 (t = 5.90 s); the track was lost at 6.30 s
- EGO_PATH of track_012, since B:e109 (t = 6.65 s)
- EGO_PATH of track_005, since B:e125 (t = 6.80 s); the track was lost at 9.90 s
- STOP, since B:e144 (t = 6.90 s)
- EGO_PATH of track_006, since B:e148 (t = 7.70 s)
- CLOSING of track_004, since B:e16 (t = 5.95 s); the track was lost at 6.25 s
- CLOSING of track_005, since B:e17 (t = 5.95 s); the track was lost at 9.90 s
- CLOSING of track_006, since B:e18 (t = 5.95 s)
- CLOSING of track_007, since B:e22 (t = 6.05 s); the track was lost at 6.30 s
- CLOSING of track_008, since B:e23 (t = 6.05 s); the track was lost at 6.30 s
- CLOSING of track_009, since B:e24 (t = 6.05 s); the track was lost at 6.30 s
- CLOSING of track_010, since B:e30 (t = 6.10 s); the track was lost at 6.40 s
- CLOSING of track_011, since B:e31 (t = 6.10 s); the track was lost at 6.40 s
- CLOSING of track_015, since B:e32 (t = 6.10 s); the track was lost at 6.45 s
- CLOSING of track_020, since B:e33 (t = 6.10 s)
- CLOSING of track_029, since B:e34 (t = 6.10 s); the track was lost at 8.65 s
- CLOSING of track_012, since B:e40 (t = 6.15 s)
- CLOSING of track_013, since B:e41 (t = 6.15 s)
- CLOSING of track_014, since B:e42 (t = 6.15 s); the track was lost at 6.45 s
- CLOSING of track_016, since B:e43 (t = 6.15 s); the track was lost at 6.50 s
- CLOSING of track_021, since B:e44 (t = 6.15 s); the track was lost at 6.45 s
- CRITICAL_TTC of track_012, since B:e45 (t = 6.15 s)
- CRITICAL_TTC of track_013, since B:e46 (t = 6.15 s)
- CLOSING of track_017, since B:e51 (t = 6.20 s); the track was lost at 6.60 s
- CLOSING of track_018, since B:e52 (t = 6.20 s); the track was lost at 6.50 s
- CLOSING of track_019, since B:e53 (t = 6.20 s); the track was lost at 6.55 s
- CLOSING of track_026, since B:e54 (t = 6.20 s); the track was lost at 6.55 s
- CLOSING of track_023, since B:e62 (t = 6.30 s); the track was lost at 6.60 s
- CLOSING of track_024, since B:e63 (t = 6.30 s); the track was lost at 6.70 s
- CLOSING of track_025, since B:e64 (t = 6.30 s); the track was lost at 7.65 s
- CLOSING of track_027, since B:e65 (t = 6.30 s); the track was lost at 6.60 s
- CLOSING of track_030, since B:e66 (t = 6.30 s)
- CLOSING of track_031, since B:e67 (t = 6.30 s); the track was lost at 6.70 s
- CLOSING of track_028, since B:e73 (t = 6.35 s); the track was lost at 6.80 s
- CLOSING of track_032, since B:e81 (t = 6.40 s)
- CLOSING of track_033, since B:e82 (t = 6.40 s); the track was lost at 6.65 s
- CLOSING of track_034, since B:e83 (t = 6.40 s); the track was lost at 6.70 s
- CLOSING of track_035, since B:e84 (t = 6.40 s); the track was lost at 9.90 s
- CLOSING of track_036, since B:e85 (t = 6.40 s)
- CLOSING of track_037, since B:e86 (t = 6.40 s); the track was lost at 9.70 s
- CLOSING of track_040, since B:e87 (t = 6.40 s)
- CLOSING of track_041, since B:e91 (t = 6.45 s); the track was lost at 6.85 s
- CLOSING of track_038, since B:e98 (t = 6.50 s)
- CLOSING of track_039, since B:e99 (t = 6.50 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e11 at 5.65 s (local): ego: MOVING, SPEED_LIMIT_EXCEEDED; track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT; track lost, states UNKNOWN: track_001
- B B:e03 at 5.65 s (local): ego: MOVING, BRAKE

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 0.75 s (A:e04): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_016 at 6.50 s (B:e101): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_018 at 6.50 s (B:e102): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_019 at 6.55 s (B:e103): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_026 at 6.55 s (B:e104): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_017 at 6.60 s (B:e105): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_023 at 6.60 s (B:e106): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_027 at 6.60 s (B:e107): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_033 at 6.65 s (B:e111): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_024 at 6.70 s (B:e115): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_031 at 6.70 s (B:e116): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_034 at 6.70 s (B:e117): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_028 at 6.80 s (B:e126): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 9.90 s (B:e152): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 6.25 s (B:e55): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 6.30 s (B:e68): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 6.30 s (B:e69): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 6.30 s (B:e70): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_009 at 6.30 s (B:e71): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_010 at 6.40 s (B:e88): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_011 at 6.40 s (B:e89): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_014 at 6.45 s (B:e92): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_015 at 6.45 s (B:e93): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_021 at 6.45 s (B:e94): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_041, track_022, track_025, track_029, track_037, track_035

## Uncertainty and limitations

- A:track_001 stays anonymous: lost 4.90 s before the matched collision (window 0.50 s); speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.25 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_002 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.25 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.25 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_004 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.30 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.30 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_006 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.30 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_007 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.40 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_008 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.40 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_009 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.40 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_010 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.45 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_011 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.45 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_012 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.50 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_013 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.50 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_014 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.50 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_015 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.45 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_016 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.50 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_017 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.55 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_018 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.55 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_019 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.55 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_020 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.45 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_021 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.50 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_022 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.25 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_023 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.65 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_024 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.65 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_025 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.65 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_026 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.55 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_027 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.65 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_028 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_029 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.45 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_030 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.65 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_031 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.65 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_032 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_033 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_034 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_035 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_036 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_037 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_038 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.85 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_039 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.85 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_040 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_041 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.80 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_042 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.85 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- Global time rests on matched collisions (t_global = 0 at the reference one) and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from the collisions that align each recorder.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5,
    "new_impact_ratio": 0.5,
    "reversal_impact_ratio": 0.25,
    "impact_acceleration_mps2": 20.0,
    "reversal_angle_deg": 90.0
  },
  "tracking": {
    "min_height_m": 0.3,
    "max_height_m": 2.5,
    "moving_speed_mps": 1.0,
    "cluster_distance_m": 2.0,
    "max_association_distance_m": 2.5,
    "max_velocity_mismatch_mps": 4.0,
    "max_track_gap_s": 0.5,
    "min_track_frames": 5,
    "measurement_std_m": 0.5,
    "radial_speed_std_mps": 0.3,
    "acceleration_std_mps2": 6.0
  },
  "semantics": {
    "brake_onset_threshold": 0.1,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_reaction_time_s": 1.0,
    "critical_deceleration_mps2": 6.0,
    "critical_standstill_margin_m": 1.0,
    "critical_release_ratio": 0.75,
    "turn_yaw_rate_window_s": 0.2,
    "turn_yaw_rate_on_dps": 10.0,
    "turn_yaw_rate_off_dps": 5.0,
    "turn_min_speed_mps": 1.0,
    "turn_release_debounce_s": 0.3,
    "turn_min_duration_s": 0.5,
    "turn_min_heading_change_deg": 15.0,
    "path_half_width_m": 1.5,
    "track_appeared_front_deg": 5.0,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
    "cut_in_max_heading_deg": 25.0,
    "cut_in_min_target_speed_mps": 2.0,
    "cut_in_lateral_speed_mps": 0.3,
    "cut_in_persistence_s": 0.5,
    "cut_in_outside_margin_m": 0.5,
    "cut_in_min_displacement_m": 0.5,
    "cut_in_horizon_s": 3.0,
    "cut_in_settle_speed_mps": 0.2,
    "cut_in_settle_s": 0.3
  },
  "fusion": {
    "impulse_tolerance": 0.1,
    "clock_tolerance_s": 0.1,
    "contact_window_s": 0.5,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
