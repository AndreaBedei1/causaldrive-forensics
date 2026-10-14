# Reconstruction report - S18/run_0_far_to_near

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 55 | 116 | 11 | A:e42 @ 8.50 s |
| B | 11.95 s | 121 | 49 | 101 | 13 | B:e35 @ 8.50 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e42 | 8.50 | -8.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e35 | 8.50 | -8.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 745.29 vs 745.29 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 4.30 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 1.6 m -> 7.0 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_009 |
| A:track_002 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.5 m -> 0.1 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.07 m/s for reference)<br>clearance at the contact 0.09 m<br>the only track of A compatible with the contact |
| A:track_003 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 7.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 1.6 m -> 7.1 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_003, B:track_003 |
| A:track_004 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.65 s before the matched collision<br>continuous up to the contact: last observed 0.90 s before it (window 1.00 s)<br>not approaching before the contact: clearance 1.4 m -> 6.1 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 5.14 m/s for reference)<br>clearance at the contact 5.35 m (beyond 3.50 m: confidence factor 0.83)<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| A:track_005#segment_1 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.60 s before the matched collision<br>lost 6.30 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 57.0 m -> 50.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U4: A:track_005#segment_1 |
| A:track_005#segment_2 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 6.25 s before the matched collision<br>lost 4.70 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 46.4 m -> 39.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U5: B:track_006, A:track_005#segment_2 |
| A:track_006 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 6.90 s before the matched collision<br>lost 4.85 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 47.9 m -> 41.3 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U6: A:track_006, B:track_008 |
| A:track_007#segment_1 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.90 s before the matched collision<br>continuous up to the contact: last observed 1.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.4 m -> 14.4 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 6.78 m/s for reference)<br>clearance at the contact 14.41 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U8: A:track_007#segment_1 |
| A:track_007#segment_2 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.6 m -> 6.9 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 7.05 m/s for reference)<br>clearance at the contact 6.94 m (beyond 3.50 m: confidence factor 0.52)<br>anonymous road user U9: B:track_010, A:track_007#segment_2 |
| A:track_008 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.65 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.7 m -> 8.3 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 6.98 m/s for reference)<br>clearance at the contact 8.33 m (beyond 3.50 m: confidence factor 0.27)<br>anonymous road user U10: B:track_011, A:track_008 |
| A:track_009 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 2.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_001 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>lost 6.20 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 7.3 m -> 4.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_009 |
| B:track_002 | A | ASSOCIATED | 0.99 | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.17 m/s for reference)<br>clearance at the contact 0.03 m<br>the only track of B compatible with the contact |
| B:track_003 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.10 s before the matched collision<br>lost 5.95 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 11.0 m -> 17.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U2: A:track_003, B:track_003 |
| B:track_004 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 8.00 s before the matched collision<br>lost 7.75 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 35.7 m -> 33.7 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_005 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.60 s before the matched collision<br>lost 2.70 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 7.2 m -> 4.4 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 5.89 m/s for reference)<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_006 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 7.55 s before the matched collision<br>lost 5.15 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 48.8 m -> 42.1 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U5: B:track_006, A:track_005#segment_2 |
| B:track_007 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 6.35 s before the matched collision<br>lost 6.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 50.9 m -> 49.0 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_007 |
| B:track_008 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 5.95 s before the matched collision<br>lost 5.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 48.6 m -> 42.9 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: A:track_006, B:track_008 |
| B:track_009 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 5.00 s before the matched collision<br>lost 3.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 16.9 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U1: A:track_001, B:track_001, B:track_009 |
| B:track_010 | U9 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.5 m -> 6.6 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 7.00 m/s for reference)<br>clearance at the contact 6.57 m (beyond 3.50 m: confidence factor 0.59)<br>anonymous road user U9: B:track_010, A:track_007#segment_2 |
| B:track_011 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 8.6 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 6.94 m/s for reference)<br>clearance at the contact 8.61 m (beyond 3.50 m: confidence factor 0.23)<br>anonymous road user U10: B:track_011, A:track_008 |
| B:track_012 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 1.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.8 m -> 14.4 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 5.82 m/s for reference)<br>clearance at the contact 7.77 m (beyond 3.50 m: confidence factor 0.36)<br>retrospective: identity resolved from later evidence at +1.35 s (entity seen by several observers), carried back 0.65 s with the motion model; posterior 0.965 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |
| B:track_013 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 745.29 vs 745.29 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.35 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 |

## Road users in the common frame

- U1 (anonymous, -8.50 to -3.10 s): A:track_001, B:track_001, B:track_009 joined by same box A:track_001-B:track_001 (100% of 47 instants); same box A:track_001-B:track_009 (100% of 15 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U2 (anonymous, -8.50 to -5.95 s): A:track_003, B:track_003 joined by same box A:track_003-B:track_003 (94% of 18 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U3 (anonymous, -8.00 to 3.45 s): B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 joined by same box A:track_004-B:track_005 (100% of 91 instants); same box A:track_009-B:track_013 (100% of 29 instants); stitch B:track_004-B:track_005 (100% of 1 instants); same box A:track_004-B:track_012 (100% of 14 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U4 (anonymous, -7.60 to -6.30 s): A:track_005#segment_1; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U5 (anonymous, -7.55 to -4.70 s): B:track_006, A:track_005#segment_2 joined by same box A:track_005#segment_2-B:track_006 (100% of 16 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U6 (anonymous, -6.90 to -4.85 s): A:track_006, B:track_008 joined by same box A:track_006-B:track_008 (100% of 9 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U7 (anonymous, -6.35 to -6.10 s): B:track_007; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U8 (anonymous, -1.90 to -1.00 s): A:track_007#segment_1; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U9 (anonymous, -1.85 to 3.45 s): B:track_010, A:track_007#segment_2 joined by same box A:track_007#segment_2-B:track_010 (100% of 42 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U10 (anonymous, -1.80 to 3.45 s): B:track_011, A:track_008 joined by same box A:track_008-B:track_011 (100% of 51 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.

## Global graph

103 nodes, 229 edges; 36 merged node(s): g06 TRACK_APPEARED_RIGHT(A,U1) from A:e04 + A:e24, g07 TRACK_APPEARED_RIGHT(A,U2) from A:e05 + A:e11, g09 TRACK_APPEARED_RIGHT(B,U1) from B:e03 + B:e17, g10 CLOSING_START(A,U1) from A:e06 + A:e19, g11 CLOSING_START(B,U1) from B:e05 + B:e16, g12 TRACK_APPEARED_RIGHT(B,U2) from B:e06 + B:e21, g13 TRACK_APPEARED_RIGHT(B,U3) from B:e07 + B:e09, g16 TRACK_APPEARED_RIGHT(A,U3) from A:e07 + A:e38, g17 CLOSING_START(A,U3) from A:e08 + A:e27, g18 TRACK_APPEARED_FRONT(A,U4) from A:e09 + A:e16, g19 TRACK_APPEARED_RIGHT(B,U3) from B:e10 + B:e27, g21 CLOSING_START(B,U3) from B:e11 + B:e26, g22 TRACK_APPEARED_RIGHT(B,U5) from B:e12 + B:e22, g25 TRACK_APPEARED_FRONT(A,U6) from A:e12 + A:e22, g27 CRITICAL_TTC_START(A,U1) from A:e14 + A:e21, g28 CUT_IN_FROM_RIGHT_START(A,U1) from A:e15 + A:e20, g29 TRACK_APPEARED_RIGHT(B,U7) from B:e14 + B:e18, g32 TRACK_APPEARED_FRONT(A,U5) from A:e17 + A:e23, g37 TRACK_APPEARED_RIGHT(B,U6) from B:e19 + B:e23, g45 TRACK_APPEARED_RIGHT(B,U1) from B:e24 + B:e25, g50 CRITICAL_TTC_START(A,U3) from A:e25 + A:e28, g51 CUT_IN_FROM_RIGHT_START(A,U3) from A:e26 + A:e29, g57 TRACK_APPEARED_FRONT(A,U8) from A:e30 + A:e35, g60 CLOSING_START(B,U9) from B:e29 + B:e42, g62 CLOSING_START(B,U10) from B:e31 + B:e43, g64 CLOSING_START(A,U10) from A:e33 + A:e49, g65 TRACK_APPEARED_RIGHT(B,U3) from B:e32 + B:e41, g66 CRITICAL_TTC_START(A,B) from A:e34 + A:e43, g69 CLOSING_START(A,U9) from A:e37 + A:e50, g70 CRITICAL_TTC_START(B,A) from B:e33 + B:e36, g72 CLOSING_START(A,B) from A:e39 + A:e45, g73 CLOSING_START(B,A) from B:e34 + B:e39, g74 CRITICAL_TTC_START(A,U9) from A:e40 + A:e51, g75 CRITICAL_TTC_START(A,U10) from A:e41 + A:e48, g76 COLLISION(A,B) from A:e42 + B:e35, g87 EGO_PATH_ENTRY(B,A) from B:e40 + B:e44.

### Event sequence (global time)

- `-8.50` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U2); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(B,U1)
- `-8.10` TRACK_APPEARED_RIGHT(B,U2)
- `-8.00` TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3)
- `-7.75` TRACK_LOST(B,U3)
- `-7.65` TRACK_APPEARED_RIGHT(A,U3); CLOSING_START(A,U3)
- `-7.60` TRACK_APPEARED_FRONT(A,U4); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(A,U4); CLOSING_START(B,U3)
- `-7.55` TRACK_APPEARED_RIGHT(B,U5); CLOSING_START(B,U5)
- `-7.25` TRACK_LOST(A,U2)
- `-6.90` TRACK_APPEARED_FRONT(A,U6); CLOSING_START(A,U6)
- `-6.70` CRITICAL_TTC_START(A,U1)
- `-6.55` CUT_IN_FROM_RIGHT_START(A,U1)
- `-6.35` TRACK_APPEARED_RIGHT(B,U7); CLOSING_START(B,U7)
- `-6.30` TRACK_LOST(A,U4)
- `-6.25` TRACK_APPEARED_FRONT(A,U5); CLOSING_START(A,U5)
- `-6.20` CLOSING_END(B,U1); TRACK_LOST(B,U1)
- `-6.10` TRACK_LOST(B,U7)
- `-5.95` TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(B,U6); TRACK_LOST(B,U2)
- `-5.90` CLOSING_END(A,U1)
- `-5.85` CUT_IN_FROM_RIGHT_END(A,U1); CRITICAL_TTC_END(A,U1)
- `-5.15` TRACK_LOST(B,U5)
- `-5.10` TRACK_LOST(B,U6)
- `-5.00` TRACK_APPEARED_RIGHT(B,U1)
- `-4.85` TRACK_LOST(A,U6)
- `-4.70` TRACK_LOST(A,U5)
- `-4.30` TRACK_LOST(A,U1)
- `-3.10` TRACK_LOST(B,U1)
- `-3.05` CRITICAL_TTC_START(A,U3)
- `-2.90` CUT_IN_FROM_RIGHT_START(A,U3)
- `-2.70` CLOSING_END(B,U3); TRACK_LOST(B,U3)
- `-2.40` CLOSING_END(A,U3)
- `-2.35` CRITICAL_TTC_END(A,U3)
- `-2.30` CUT_IN_FROM_RIGHT_END(A,U3)
- `-1.90` TRACK_APPEARED_FRONT(A,U8); CLOSING_START(A,U8)
- `-1.85` TRACK_APPEARED_RIGHT(B,U9); CLOSING_START(B,U9)
- `-1.80` TRACK_APPEARED_RIGHT(B,U10); CLOSING_START(B,U10)
- `-1.65` TRACK_APPEARED_RIGHT(A,U10); CLOSING_START(A,U10)
- `-1.55` TRACK_APPEARED_RIGHT(B,U3)
- `-1.35` CRITICAL_TTC_START(A,B)
- `-1.00` TRACK_LOST(A,U8)
- `-0.95` TRACK_APPEARED_FRONT(A,U9); CLOSING_START(A,U9)
- `-0.90` CRITICAL_TTC_START(B,A); TRACK_LOST(A,U3)
- `-0.85` CLOSING_START(A,B)
- `-0.80` CLOSING_START(B,A)
- `-0.45` CRITICAL_TTC_START(A,U9)
- `-0.05` CRITICAL_TTC_START(A,U10)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(A,B)
- `+0.05` CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- `+0.30` CRITICAL_TTC_END(A,U10)
- `+0.60` CLOSING_END(B,A); EGO_PATH_ENTRY(B,A)
- `+0.70` TRACK_LOST(B,U3)
- `+0.80` CLOSING_END(B,U10); CLOSING_END(B,U9)
- `+0.90` CLOSING_END(A,U10)
- `+0.95` CLOSING_END(A,U9)
- `+1.00` EGO_PATH_EXIT(B,A)
- `+1.10` CRITICAL_TTC_END(A,U9); MOVING_END(B); STOP_START(B)
- `+1.20` MOVING_END(A); STOP_START(A)
- `+1.35` TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3)
- `+2.05` TRACK_APPEARED_RIGHT(A,U3); EGO_PATH_ENTRY(B,A); CLOSING_START(A,U3)

### What happened, in plain language

- 8.50 s before the reference collision, A started moving (already the case when first observed).
- 8.50 s before the reference collision, B started moving (already the case when first observed).
- 8.50 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 8.50 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 8.50 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 8.50 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 8.50 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its right.
- 8.50 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 8.50 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 8.50 s before the reference collision, A observed anonymous road user U1 start closing in (already the case when first observed).
- 8.50 s before the reference collision, B observed anonymous road user U1 start closing in (already the case when first observed).
- 8.10 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 8.00 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 8.00 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 7.75 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 7.65 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 7.65 s before the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
- 7.60 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared in front of it.
- 7.60 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 7.60 s before the reference collision, A observed anonymous road user U4 start closing in (already the case when first observed).
- 7.60 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 7.55 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its right.
- 7.55 s before the reference collision, B observed anonymous road user U5 start closing in (already the case when first observed).
- 7.25 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 6.90 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared in front of it.
- 6.90 s before the reference collision, A observed anonymous road user U6 start closing in (already the case when first observed).
- 6.70 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 6.55 s before the reference collision, A observed anonymous road user U1 cutting in from the right.
- 6.35 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 6.35 s before the reference collision, B observed anonymous road user U7 start closing in (already the case when first observed).
- 6.30 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 6.25 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared in front of it.
- 6.25 s before the reference collision, A observed anonymous road user U5 start closing in (already the case when first observed).
- 6.20 s before the reference collision, B observed anonymous road user U1 stop closing in.
- 6.20 s before the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 6.10 s before the reference collision, B's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 5.95 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 5.95 s before the reference collision, B observed anonymous road user U6 start closing in (already the case when first observed).
- 5.95 s before the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 5.90 s before the reference collision, A observed anonymous road user U1 stop closing in.
- 5.85 s before the reference collision, A observed anonymous road user U1's cut-in from the right settle.
- 5.85 s before the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 5.15 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 5.10 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 5.00 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 4.85 s before the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 4.70 s before the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 4.30 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 3.10 s before the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 3.05 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 2.90 s before the reference collision, A observed anonymous road user U3 cutting in from the right.
- 2.70 s before the reference collision, B observed anonymous road user U3 stop closing in.
- 2.70 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.40 s before the reference collision, A observed anonymous road user U3 stop closing in.
- 2.35 s before the reference collision, A's time-to-contact with anonymous road user U3 stopped being critical.
- 2.30 s before the reference collision, A observed anonymous road user U3's cut-in from the right settle.
- 1.90 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared in front of it.
- 1.90 s before the reference collision, A observed anonymous road user U8 start closing in (already the case when first observed).
- 1.85 s before the reference collision, B's radar started tracking anonymous road user U9, which appeared on its right.
- 1.85 s before the reference collision, B observed anonymous road user U9 start closing in (already the case when first observed).
- 1.80 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared on its right.
- 1.80 s before the reference collision, B observed anonymous road user U10 start closing in (already the case when first observed).
- 1.65 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 1.65 s before the reference collision, A observed anonymous road user U10 start closing in (already the case when first observed).
- 1.55 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 1.35 s before the reference collision, A's time-to-contact with B became critical.
- 1.00 s before the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 0.95 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared in front of it.
- 0.95 s before the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 0.90 s before the reference collision, B's time-to-contact with A became critical.
- 0.90 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.85 s before the reference collision, A observed B start closing in.
- 0.80 s before the reference collision, B observed A start closing in.
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U9 became critical.
- 0.05 s before the reference collision, A's time-to-contact with anonymous road user U10 became critical.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 745, B: 745 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B enter its forward path corridor.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.30 s after the reference collision, A's time-to-contact with anonymous road user U10 stopped being critical.
- 0.60 s after the reference collision, B observed A stop closing in.
- 0.60 s after the reference collision, B observed A enter its forward path corridor.
- 0.70 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.80 s after the reference collision, B observed anonymous road user U10 stop closing in.
- 0.80 s after the reference collision, B observed anonymous road user U9 stop closing in.
- 0.90 s after the reference collision, A observed anonymous road user U10 stop closing in.
- 0.95 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 1.00 s after the reference collision, B observed A leave its forward path corridor.
- 1.10 s after the reference collision, A's time-to-contact with anonymous road user U9 stopped being critical.
- 1.10 s after the reference collision, B stopped moving.
- 1.10 s after the reference collision, B came to a stop.
- 1.20 s after the reference collision, A stopped moving.
- 1.20 s after the reference collision, A came to a stop.
- 1.35 s after the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 1.35 s after the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 2.05 s after the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 2.05 s after the reference collision, B observed A enter its forward path corridor.
- 2.05 s after the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified U1): critical TTC already active before the cut-in: CRITICAL_TTC_START 1.80 <= CUT_IN_FROM_RIGHT_START 1.95 (+0.15 s) [local times; t_global: cut_in -6.55, critical_ttc_start -6.70, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 7.15, COLLISION with B 8.50 (+1.35 s); EGO_PATH_ENTRY 8.50 after critical TTC (+1.35 s) [local times; t_global: critical_ttc_start -1.35, ego_path_entry +0.00, collision +0.00]
- A's track_004 (unidentified U3): critical TTC already active before the cut-in: CRITICAL_TTC_START 5.45 <= CUT_IN_FROM_RIGHT_START 5.60 (+0.15 s) [local times; t_global: cut_in -2.90, critical_ttc_start -3.05, collision +0.00]
- A's track_007#segment_2 (unidentified U9): CRITICAL_TTC_START 8.05, COLLISION 8.50 (+0.45 s) [local times; t_global: critical_ttc_start -0.45, collision +0.00]
- A's track_008 (unidentified U10): CRITICAL_TTC_START 8.45, COLLISION 8.50 (+0.05 s) [local times; t_global: critical_ttc_start -0.05, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.60, COLLISION with A 8.50 (+0.90 s); EGO_PATH_ENTRY 9.10 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -0.90, ego_path_entry +0.60, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U2); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(B,U1)
- TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3)
- TRACK_APPEARED_RIGHT(A,U3); CLOSING_START(A,U3)
- TRACK_APPEARED_FRONT(A,U4); TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(A,U4); CLOSING_START(B,U3)
- TRACK_APPEARED_RIGHT(B,U5); CLOSING_START(B,U5)
- TRACK_APPEARED_FRONT(A,U6); CLOSING_START(A,U6)
- TRACK_APPEARED_RIGHT(B,U7); CLOSING_START(B,U7)
- TRACK_APPEARED_FRONT(A,U5); CLOSING_START(A,U5)
- CLOSING_END(B,U1); TRACK_LOST(B,U1)
- TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(B,U6); TRACK_LOST(B,U2)
- CUT_IN_FROM_RIGHT_END(A,U1); CRITICAL_TTC_END(A,U1)
- CLOSING_END(B,U3); TRACK_LOST(B,U3)
- TRACK_APPEARED_FRONT(A,U8); CLOSING_START(A,U8)
- TRACK_APPEARED_RIGHT(B,U9); CLOSING_START(B,U9)
- TRACK_APPEARED_RIGHT(B,U10); CLOSING_START(B,U10)
- TRACK_APPEARED_RIGHT(A,U10); CLOSING_START(A,U10)
- TRACK_APPEARED_FRONT(A,U9); CLOSING_START(A,U9)
- CRITICAL_TTC_START(B,A); TRACK_LOST(A,U3)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(A,B)
- CLOSING_END(A,B); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- CLOSING_END(B,A); EGO_PATH_ENTRY(B,A)
- CLOSING_END(B,U10); CLOSING_END(B,U9)
- CRITICAL_TTC_END(A,U9); MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)
- TRACK_APPEARED_RIGHT(B,U3); CLOSING_START(B,U3)
- TRACK_APPEARED_RIGHT(A,U3); EGO_PATH_ENTRY(B,A); CLOSING_START(A,U3)

### States still active when observation ended

A:
- CLOSING of track_005#segment_1, since A:e10 (t = 0.90 s); the track was lost at 2.20 s
- CLOSING of track_006, since A:e13 (t = 1.60 s); the track was lost at 3.65 s
- CLOSING of track_005#segment_2, since A:e18 (t = 2.25 s); the track was lost at 3.80 s
- CLOSING of track_007#segment_1, since A:e31 (t = 6.60 s); the track was lost at 7.50 s
- EGO_PATH of track_002, since A:e44 (t = 8.50 s)
- BRAKE, since A:e47 (t = 8.55 s)
- STOP, since A:e53 (t = 9.70 s)
- CLOSING of track_009, since A:e55 (t = 10.55 s)
B:
- CLOSING of track_004, since B:e08 (t = 0.50 s); the track was lost at 0.75 s
- CLOSING of track_006, since B:e13 (t = 0.95 s); the track was lost at 3.35 s
- CLOSING of track_007, since B:e15 (t = 2.15 s); the track was lost at 2.40 s
- CLOSING of track_008, since B:e20 (t = 2.55 s); the track was lost at 3.40 s
- BRAKE, since B:e38 (t = 8.55 s)
- STOP, since B:e46 (t = 9.60 s)
- CLOSING of track_013, since B:e48 (t = 9.85 s)
- EGO_PATH of track_002, since B:e49 (t = 10.55 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e42 at 8.50 s (local): ego: MOVING, THROTTLE; track_002: CLOSING, CRITICAL_TTC; track_007#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_008: CLOSING, CRITICAL_TTC; track lost, states UNKNOWN: track_001, track_003, track_004, track_005#segment_1, track_005#segment_2, track_006, track_007#segment_1
- B B:e35 at 8.50 s (local): ego: MOVING, THROTTLE; track_002: CLOSING, CRITICAL_TTC; track_010: CLOSING; track_011: CLOSING; track_012: no active state; track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008, track_009

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_005#segment_1 at 2.20 s (A:e16): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.65 s (A:e22): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005#segment_2 at 3.80 s (A:e23): CLOSING, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_007#segment_1 at 7.50 s (A:e35): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_001, track_004
B:
- track_004 at 0.75 s (B:e09): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 2.30 s (B:e17): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 2.40 s (B:e18): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.35 s (B:e22): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 3.40 s (B:e23): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 5.80 s (B:e27): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_009, track_012

## Uncertainty and limitations

- A:track_001 stays anonymous (U1): lost 4.30 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 1.6 m -> 7.0 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_003 stays anonymous (U2): lost 7.25 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 1.6 m -> 7.1 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_004 stays anonymous (U3): not approaching before the contact: clearance 1.4 m -> 6.1 m over the last 1.0 s; track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 5.14 m/s for reference).
- A:track_005#segment_1 stays anonymous (U4): lost 6.30 s before the matched collision (window 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_005#segment_2 stays anonymous (U5): lost 4.70 s before the matched collision (window 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_006 stays anonymous (U6): lost 4.85 s before the matched collision (window 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_007#segment_1 stays anonymous (U8): track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 6.78 m/s for reference).
- A:track_007#segment_2 stays anonymous (U9): tracked for 0.95 s before the matched collision (needs 1.00 s); track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 7.05 m/s for reference).
- A:track_008 stays anonymous (U10): track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 6.98 m/s for reference).
- A:track_009 stays anonymous (U3): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 2.05 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous (U1): lost 6.20 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous (U2): lost 5.95 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 11.0 m -> 17.5 m over the last 1.0 s; speed not comparable with A's own speed before the collision.
- B:track_004 stays anonymous (U3): lost 7.75 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous (U3): lost 2.70 s before the matched collision (window 1.00 s); track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 5.89 m/s for reference).
- B:track_006 stays anonymous (U5): lost 5.15 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_007 stays anonymous (U7): lost 6.10 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_008 stays anonymous (U6): lost 5.10 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_009 stays anonymous (U1): lost 3.10 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 10.1 m -> 16.9 m over the last 1.0 s; speed not comparable with A's own speed before the collision.
- B:track_010 stays anonymous (U9): track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 7.00 m/s for reference).
- B:track_011 stays anonymous (U10): track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 6.94 m/s for reference).
- B:track_012 stays anonymous (U3): not approaching before the contact: clearance 7.8 m -> 14.4 m over the last 1.0 s; track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 5.82 m/s for reference).
- B:track_013 stays anonymous (U3): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.35 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- Global time rests on matched collisions (t_global = 0 at the reference one) and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from the collisions that align each recorder.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `anonymous_entities.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5,
    "new_impact_ratio": 0.75,
    "min_impact_ratio": 0.25,
    "min_new_impact_impulse": 1000.0,
    "impact_acceleration_mps2": 20.0,
    "reversal_angle_deg": 90.0,
    "undirected_impact_ratio": 0.5
  },
  "tracking": {
    "min_height_m": 0.3,
    "max_height_m": 2.5,
    "moving_speed_mps": 1.0,
    "cluster_distance_m": 2.0,
    "max_track_gap_s": 0.5,
    "min_track_frames": 5,
    "measurement_std_m": 0.5,
    "radial_speed_std_mps": 0.3,
    "acceleration_std_mps2": 6.0,
    "smoothing_innovation_sigma": 3.0,
    "min_slowdown_returns": 3,
    "identity_body_width_m": 2.5,
    "gate_probability": 0.99,
    "body_length_m": 4.6,
    "body_width_m": 1.9,
    "radar_range_std_m": 0.25,
    "radar_azimuth_std_deg": 0.5,
    "min_track_support_s": 0.2,
    "min_track_updates": 3,
    "gap_cap_s": 2.0,
    "nominal_vehicle_mass_kg": 1500.0,
    "position_cap_m": 10.0,
    "doppler_cap_mps": 10.0,
    "return_likelihood_ratio": 20.0,
    "yaw_rate_std_rps": 0.3
  },
  "semantics": {
    "brake_onset_threshold": 0.1,
    "throttle_on_threshold": 0.1,
    "throttle_off_threshold": 0.05,
    "throttle_release_debounce_s": 0.2,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_reaction_time_s": 1.0,
    "critical_deceleration_mps2": 6.0,
    "critical_standstill_margin_m": 1.0,
    "critical_lateral_margin_m": 0.3,
    "critical_release_ratio": 0.75,
    "prediction_horizon_s": 6.0,
    "prediction_time_step_s": 0.05,
    "target_length_m": 4.6,
    "target_width_m": 1.9,
    "target_braking_min_mps2": 1.0,
    "critical_min_track_age_s": 0.5,
    "critical_time_gap_table": [
      [
        7.2,
        1.0
      ],
      [
        10.0,
        1.1
      ],
      [
        20.0,
        1.2
      ],
      [
        30.0,
        1.3
      ],
      [
        40.0,
        1.4
      ],
      [
        50.0,
        1.5
      ],
      [
        60.0,
        1.6
      ]
    ],
    "critical_min_following_distance_m": 2.0,
    "critical_forward_min_speed_mps": 1.0,
    "critical_front_lateral_margin_m": 1.0,
    "critical_front_lateral_speed_mps": 0.3,
    "critical_forward_release_factor": 1.1,
    "occlusion_margin_m": 0.5,
    "turn_yaw_rate_window_s": 0.2,
    "turn_yaw_rate_on_dps": 10.0,
    "turn_yaw_rate_off_dps": 5.0,
    "turn_min_speed_mps": 1.0,
    "turn_release_debounce_s": 0.3,
    "turn_min_duration_s": 0.5,
    "turn_min_heading_change_deg": 15.0,
    "path_half_width_m": 1.5,
    "path_hysteresis_m": 0.5,
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
    "cut_in_preentry_margin_m": 1.0,
    "cut_in_settle_speed_mps": 0.2,
    "cut_in_settle_s": 0.3
  },
  "fusion": {
    "impulse_tolerance": 0.1,
    "impulse_relative_std": 0.1,
    "impulse_sigma_gate": 3.0,
    "contact_consistency_m": 1.0,
    "clock_tolerance_s": 0.1,
    "contact_window_s": 1.0,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5,
    "touching_clearance_m": 1.0,
    "rival_clearance_m": 2.0,
    "observed_alignment_step_s": 0.05,
    "observed_alignment_min_samples": 10,
    "observed_alignment_min_speed_mps": 2.0,
    "observed_alignment_uniqueness_ratio": 3.0,
    "link_min_samples": 10,
    "link_min_fraction": 0.8,
    "anonymous_gate_probability": 0.99,
    "anonymous_min_shared_samples": 10,
    "anonymous_pass_fraction": 0.8,
    "stitch_max_gap_s": 1.5,
    "box_face_std_m": 0.25,
    "box_length_std_m": 0.7,
    "box_width_std_m": 0.2,
    "entity_output_rate_hz": 10.0,
    "mutual_refinement": false,
    "mutual_refinement_iterations": 3,
    "radar_range_std_m": 0.25,
    "radar_azimuth_std_deg": 0.5,
    "assignment_likelihood_ratio": 20.0,
    "retrospective_new_target_density": 3.57e-05,
    "retrospective_min_posterior": 0.95
  }
}
```
