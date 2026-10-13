# Reconstruction report - S14/run_0_surrounded

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 37 | 61 | 11 | A:e20 @ 7.75 s |
| B | 11.95 s | 121 | 50 | 102 | 16 | B:e25 @ 7.75 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e20 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e25 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 254.4 vs 254.4 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 2.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.53 m/s over 3.0 s<br>clearance at the contact 2.02 m<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>anonymous road user U1: A:track_001, B:track_003 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 11.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.55 m/s over 3.0 s<br>clearance at the contact 11.12 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>anonymous road user U2: A:track_002, B:track_008 |
| A:track_003 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.38 m/s over 3.0 s<br>clearance at the contact 0.13 m<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma, over 240 samples; 100% within 3 sigma) at B's own velocity (median difference 0.15 m/s) |
| A:track_004 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 3.30 s before the matched collision<br>continuous up to the contact: last observed 0.50 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.1 m -> 10.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.51 m/s over 2.5 s<br>clearance at the contact 9.81 m (beyond 3.50 m: confidence factor 0.11)<br>anonymous road user U9: A:track_004 |
| A:track_005 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.90 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.2 m -> 10.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.71 m/s over 0.9 s<br>clearance at the contact 9.98 m (beyond 3.50 m: confidence factor 0.10)<br>anonymous road user U3: B:track_001, A:track_005 |
| A:track_006 | U13 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.00 s before the matched collision<br>continuous up to the contact: last observed 0.30 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.9 m -> 18.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.89 m/s over 0.7 s<br>clearance at the contact 18.30 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006)<br>anonymous road user U13: A:track_006 |
| A:track_007 | U14 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.1 m -> 41.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 0.7 s<br>clearance at the contact 41.86 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U14: A:track_007 |
| A:track_008 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.35 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.3 m -> 26.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.60 m/s over 0.3 s<br>clearance at the contact 26.19 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U10: B:track_011, A:track_008 |
| A:track_009 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.15 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.9 m -> 10.9 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 10.86 m (beyond 3.50 m: confidence factor 0.05)<br>anonymous road user U7: B:track_007, A:track_009 |
| A:track_010 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U11: B:track_012, A:track_010 |
| A:track_011 | U15 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U15: A:track_011 |
| B:track_001 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.5 m -> 9.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.03 m/s over 3.0 s<br>clearance at the contact 9.92 m (beyond 3.50 m: confidence factor 0.10)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U3: B:track_001, A:track_005 |
| B:track_002 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.76 m/s over 3.0 s<br>clearance at the contact 0.71 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma, over 240 samples; 94% within 3 sigma) at A's own velocity (median difference 0.22 m/s) |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.2 m -> 2.8 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 2.80 m<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U1: A:track_001, B:track_003 |
| B:track_004 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.7 m -> 28.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U4: B:track_004 |
| B:track_005 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 1.05 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 6.6 m -> 7.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.10 m/s over 2.0 s<br>anonymous road user U5: B:track_005, B:track_014 |
| B:track_006 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.05 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.4 m -> 27.9 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_006, B:track_010 |
| B:track_007 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.6 m -> 11.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 3.0 s<br>clearance at the contact 11.11 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U7: B:track_007, A:track_009 |
| B:track_008 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 10.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.07 m/s over 3.0 s<br>clearance at the contact 10.56 m (beyond 3.50 m: confidence factor 0.06)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U2: A:track_002, B:track_008 |
| B:track_009 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 5.55 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 44.6 m -> 44.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U8: B:track_009 |
| B:track_010 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 3.95 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 30.2 m -> 29.8 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_006, B:track_010 |
| B:track_011 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 1.4 s<br>clearance at the contact 26.19 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U10: B:track_011, A:track_008 |
| B:track_012 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.3 s<br>clearance at the contact 26.70 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U11: B:track_012, A:track_010 |
| B:track_013 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.5 m -> 41.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.2 s<br>clearance at the contact 41.94 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013)<br>anonymous road user U12: B:track_013 |
| B:track_014 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U5: B:track_005, B:track_014 |
| B:track_015 | U16 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.60 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U16: B:track_015 |
| B:track_016 | U17 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 254.4 vs 254.4 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.95 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U17: B:track_016 |

## Road users in the common frame

- A:track_003 is B: its returns lie on B's own footprint (median 0.00 m over 240 samples, 100% within 3 sigma) at B's velocity.
- B:track_002 is A: its returns lie on A's own footprint (median 0.00 m over 240 samples, 94% within 3 sigma) at A's velocity.
- U1 (anonymous, -7.75 to 4.20 s): A:track_001, B:track_003 joined by same box A:track_001-B:track_003 (100% of 240 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit.
- U2 (anonymous, -7.75 to 4.20 s): A:track_002, B:track_008 joined by same box A:track_002-B:track_008 (100% of 239 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit.
- U3 (anonymous, -7.75 to 4.20 s): B:track_001, A:track_005 joined by same box A:track_005-B:track_001 (100% of 103 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U4 (anonymous, -7.75 to -4.10 s): B:track_004; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U5 (anonymous, -7.75 to 0.30 s): B:track_005, B:track_014 joined by stitch B:track_005-B:track_014 (100% of 1 instants); footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U6 (anonymous, -7.75 to -3.95 s): B:track_006, B:track_010 joined by same box B:track_006-B:track_010 (100% of 29 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U7 (anonymous, -7.70 to 4.20 s): B:track_007, A:track_009 joined by same box A:track_009-B:track_007 (99% of 87 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U8 (anonymous, -7.70 to -5.55 s): B:track_009; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U9 (anonymous, -3.30 to -0.50 s): A:track_004; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U10 (anonymous, -1.40 to 4.20 s): B:track_011, A:track_008 joined by same box A:track_008-B:track_011 (100% of 19 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U11 (anonymous, -1.35 to 4.20 s): B:track_012, A:track_010 joined by same box A:track_010-B:track_012 (100% of 12 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U12 (anonymous, -1.15 to 4.20 s): B:track_013; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U13 (anonymous, -1.00 to -0.30 s): A:track_006; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U14 (anonymous, -0.70 to -0.05 s): A:track_007; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U15 (anonymous, 1.75 to 3.40 s): A:track_011; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U16 (anonymous, 3.60 to 3.90 s): B:track_015; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U17 (anonymous, 3.95 to 4.20 s): B:track_016; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.

## Global graph

84 nodes, 181 edges; 23 merged node(s): g09 TRACK_APPEARED_LEFT(B,U4) from B:e04 + B:e16, g10 TRACK_APPEARED_LEFT(B,U5) from B:e05 + B:e22, g13 TRACK_APPEARED_RIGHT(B,U6) from B:e08 + B:e17 + B:e09 + B:e18, g14 TRACK_APPEARED_FRONT(B,U8) from B:e10 + B:e15, g17 CRITICAL_TTC_START(A,U1) from A:e06 + A:e26, g22 TRACK_LOST(B,U6) from B:e17 + B:e18, g23 TRACK_APPEARED_LEFT(A,U9) from A:e07 + A:e13, g24 TRACK_APPEARED_RIGHT(B,U10) from B:e19 + B:e33, g25 CRITICAL_TTC_START(A,B) from A:e08 + A:e21, g26 TRACK_APPEARED_LEFT(B,U11) from B:e20 + B:e36, g29 TRACK_APPEARED_LEFT(A,U13) from A:e09 + A:e16, g31 CLOSING_START(A,B) from A:e11 + A:e24, g32 CRITICAL_TTC_START(B,A) from B:e23 + B:e26, g33 TRACK_APPEARED_FRONT(A,U14) from A:e12 + A:e19, g34 CLOSING_START(B,A) from B:e24 + B:e27, g42 COLLISION(A,B) from A:e20 + B:e25, g48 TRACK_APPEARED_LEFT(B,U5) from B:e29 + B:e32, g50 EGO_PATH_ENTRY(B,U12) from B:e30 + B:e37, g58 EGO_PATH_ENTRY(A,U10) from A:e28 + A:e36, g60 EGO_PATH_ENTRY(B,U2) from B:e34 + B:e41, g61 CRITICAL_TTC_START(B,U2) from B:e35 + B:e40, g63 TRACK_APPEARED_LEFT(A,U15) from A:e30 + A:e35, g78 TRACK_APPEARED_LEFT(B,U16) from B:e46 + B:e47.

### Event sequence (global time)

- `-7.75` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U1); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U4); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); TRACK_APPEARED_RIGHT(B,U6)
- `-7.70` TRACK_APPEARED_FRONT(B,U8); TRACK_APPEARED_LEFT(B,U2); TRACK_APPEARED_RIGHT(B,U7)
- `-7.25` CRITICAL_TTC_START(A,U1); CRITICAL_TTC_START(B,U3)
- `-7.15` CLOSING_START(B,U6)
- `-5.55` TRACK_LOST(B,U8)
- `-4.10` TRACK_LOST(B,U4)
- `-3.95` TRACK_LOST(B,U6)
- `-3.30` TRACK_APPEARED_LEFT(A,U9)
- `-1.40` TRACK_APPEARED_RIGHT(B,U10); CRITICAL_TTC_START(A,B)
- `-1.35` TRACK_APPEARED_LEFT(B,U11)
- `-1.15` TRACK_APPEARED_FRONT(B,U12)
- `-1.05` TRACK_LOST(B,U5)
- `-1.00` TRACK_APPEARED_LEFT(A,U13)
- `-0.90` TRACK_APPEARED_LEFT(A,U3)
- `-0.80` CLOSING_START(A,B)
- `-0.75` CRITICAL_TTC_START(B,A)
- `-0.70` TRACK_APPEARED_FRONT(A,U14); CLOSING_START(B,A)
- `-0.50` TRACK_LOST(A,U9)
- `-0.40` CRITICAL_TTC_START(A,U3)
- `-0.35` TRACK_APPEARED_RIGHT(A,U10)
- `-0.30` TRACK_LOST(A,U13)
- `-0.15` EGO_PATH_EXIT(A,U14); TRACK_APPEARED_RIGHT(A,U7)
- `-0.05` TRACK_LOST(A,U14)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.05` THROTTLE_END(A); THROTTLE_END(B)
- `+0.10` TRACK_APPEARED_LEFT(B,U5); EGO_PATH_ENTRY(A,B); EGO_PATH_ENTRY(B,U12)
- `+0.15` CLOSING_END(A,B)
- `+0.25` EGO_PATH_ENTRY(B,U11)
- `+0.30` TRACK_LOST(B,U5)
- `+0.70` TRACK_APPEARED_LEFT(A,U11)
- `+1.10` TRACK_LOST(B,U10)
- `+1.30` CRITICAL_TTC_END(A,U1); EGO_PATH_EXIT(A,U1)
- `+1.35` EGO_PATH_ENTRY(A,U10)
- `+1.40` EGO_PATH_EXIT(A,U7)
- `+1.45` EGO_PATH_ENTRY(B,U2); CRITICAL_TTC_START(B,U2)
- `+1.60` TRACK_LOST(B,U11)
- `+1.75` TRACK_APPEARED_LEFT(A,U15)
- `+1.85` EGO_PATH_EXIT(B,U12)
- `+2.35` CUT_IN_FROM_RIGHT_START(B,U7)
- `+2.40` CRITICAL_TTC_START(A,U7)
- `+2.50` EGO_PATH_ENTRY(A,U7)
- `+2.70` CUT_IN_FROM_RIGHT_START(B,U1)
- `+2.75` CRITICAL_TTC_START(A,U1)
- `+2.80` CRITICAL_TTC_END(B,U2); EGO_PATH_EXIT(B,U2)
- `+2.95` CRITICAL_TTC_START(B,U7)
- `+3.25` EGO_PATH_ENTRY(A,U1)
- `+3.35` CLOSING_START(B,U1)
- `+3.40` EGO_PATH_ENTRY(B,U7); TRACK_LOST(A,U15)
- `+3.55` CRITICAL_TTC_START(B,U1)
- `+3.60` TRACK_APPEARED_LEFT(B,U16)
- `+3.80` EGO_PATH_EXIT(A,U10)
- `+3.85` EGO_PATH_EXIT(A,U3)
- `+3.90` TRACK_LOST(B,U16)
- `+3.95` TRACK_APPEARED_FRONT(B,U17)
- `+4.05` EGO_PATH_ENTRY(B,U1)
- `+4.20` EGO_PATH_EXIT(B,U17)

### What happened, in plain language

- 7.75 s before the reference collision, A started moving (already the case when first observed).
- 7.75 s before the reference collision, B started moving (already the case when first observed).
- 7.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared in front of it.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.75 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared in front of it.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its left.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 7.25 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U3 became critical.
- 7.15 s before the reference collision, B observed anonymous road user U6 start closing in.
- 5.55 s before the reference collision, B's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 4.10 s before the reference collision, B's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 3.95 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 3.30 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared on its left.
- 1.40 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared on its right.
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B's radar started tracking anonymous road user U11, which appeared on its left.
- 1.15 s before the reference collision, B's radar started tracking anonymous road user U12, which appeared in front of it.
- 1.05 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 1.00 s before the reference collision, A's radar started tracking anonymous road user U13, which appeared on its left.
- 0.90 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- 0.80 s before the reference collision, A observed B start closing in.
- 0.75 s before the reference collision, B's time-to-contact with A became critical.
- 0.70 s before the reference collision, A's radar started tracking anonymous road user U14, which appeared in front of it.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.50 s before the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 0.40 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 0.35 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 0.30 s before the reference collision, A's radar lost anonymous road user U13 (its states are UNKNOWN from then on, not ended).
- 0.15 s before the reference collision, A observed anonymous road user U14 leave its forward path corridor.
- 0.15 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared on its right.
- 0.05 s before the reference collision, A's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 254, B: 254 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.10 s after the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.10 s after the reference collision, B observed anonymous road user U12 enter its forward path corridor.
- 0.15 s after the reference collision, A observed B stop closing in.
- 0.25 s after the reference collision, B observed anonymous road user U11 enter its forward path corridor.
- 0.30 s after the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A's radar started tracking anonymous road user U11, which appeared on its left.
- 1.10 s after the reference collision, B's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 1.30 s after the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 1.30 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 1.35 s after the reference collision, A observed anonymous road user U10 enter its forward path corridor.
- 1.40 s after the reference collision, A observed anonymous road user U7 leave its forward path corridor.
- 1.45 s after the reference collision, B observed anonymous road user U2 enter its forward path corridor.
- 1.45 s after the reference collision, B's time-to-contact with anonymous road user U2 became critical.
- 1.60 s after the reference collision, B's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 1.75 s after the reference collision, A's radar started tracking anonymous road user U15, which appeared on its left.
- 1.85 s after the reference collision, B observed anonymous road user U12 leave its forward path corridor.
- 2.35 s after the reference collision, B observed anonymous road user U7 cutting in from the right.
- 2.40 s after the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 2.50 s after the reference collision, A observed anonymous road user U7 enter its forward path corridor.
- 2.70 s after the reference collision, B observed anonymous road user U1 cutting in from the right.
- 2.75 s after the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 2.80 s after the reference collision, B's time-to-contact with anonymous road user U2 stopped being critical.
- 2.80 s after the reference collision, B observed anonymous road user U2 leave its forward path corridor.
- 2.95 s after the reference collision, B's time-to-contact with anonymous road user U7 became critical.
- 3.25 s after the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 3.35 s after the reference collision, B observed anonymous road user U1 start closing in.
- 3.40 s after the reference collision, B observed anonymous road user U7 enter its forward path corridor.
- 3.40 s after the reference collision, A's radar lost anonymous road user U15 (its states are UNKNOWN from then on, not ended).
- 3.55 s after the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 3.60 s after the reference collision, B's radar started tracking anonymous road user U16, which appeared on its left.
- 3.80 s after the reference collision, A observed anonymous road user U10 leave its forward path corridor.
- 3.85 s after the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 3.90 s after the reference collision, B's radar lost anonymous road user U16 (its states are UNKNOWN from then on, not ended).
- 3.95 s after the reference collision, B's radar started tracking anonymous road user U17, which appeared in front of it.
- 4.05 s after the reference collision, B observed anonymous road user U1 enter its forward path corridor.
- 4.20 s after the reference collision, B observed anonymous road user U17 leave its forward path corridor.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s); EGO_PATH_ENTRY 11.00 after critical TTC (+10.50 s) [local times; t_global: critical_ttc_start -7.25, ego_path_entry +3.25, collision +0.00]
- A's track_003 (B): CRITICAL_TTC_START 6.35, COLLISION with B 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -1.40, ego_path_entry +0.10, collision +0.00]
- A's track_005 (unidentified U3): CRITICAL_TTC_START 7.35, COLLISION 7.75 (+0.40 s) [local times; t_global: critical_ttc_start -0.40, collision +0.00]
- A's track_008 (unidentified U10): EGO_PATH_ENTRY 9.10, no critical TTC [local times; t_global: ego_path_entry +1.35]
- A's track_009 (unidentified U7): CRITICAL_TTC_START 10.15; EGO_PATH_ENTRY 10.25 after critical TTC (+0.10 s) [local times; t_global: critical_ttc_start +2.40, ego_path_entry +2.50]
- B's track_001 (unidentified U3): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.00, COLLISION with A 7.75 (+0.75 s) [local times; t_global: critical_ttc_start -0.75, collision +0.00]
- B's track_003 (unidentified U1): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 10.45 < CRITICAL_TTC_START 11.30 (+0.85 s); EGO_PATH_ENTRY 11.80 after critical TTC (+0.50 s) [local times; t_global: cut_in +2.70, critical_ttc_start +3.55, ego_path_entry +4.05]
- B's track_007 (unidentified U7): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 10.10 < CRITICAL_TTC_START 10.70 (+0.60 s); EGO_PATH_ENTRY 11.15 after critical TTC (+0.45 s) [local times; t_global: cut_in +2.35, critical_ttc_start +2.95, ego_path_entry +3.40]
- B's track_008 (unidentified U2): CRITICAL_TTC_START 9.20; EGO_PATH_ENTRY 9.20 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start +1.45, ego_path_entry +1.45]
- B's track_012 (unidentified U11): EGO_PATH_ENTRY 8.00, no critical TTC [local times; t_global: ego_path_entry +0.25]
- B's track_013 (unidentified U12): EGO_PATH_ENTRY 7.85, no critical TTC [local times; t_global: ego_path_entry +0.10]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U1); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U4); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U1); TRACK_APPEARED_RIGHT(B,U6)
- TRACK_APPEARED_FRONT(B,U8); TRACK_APPEARED_LEFT(B,U2); TRACK_APPEARED_RIGHT(B,U7)
- CRITICAL_TTC_START(A,U1); CRITICAL_TTC_START(B,U3)
- TRACK_APPEARED_RIGHT(B,U10); CRITICAL_TTC_START(A,B)
- TRACK_APPEARED_FRONT(A,U14); CLOSING_START(B,A)
- EGO_PATH_EXIT(A,U14); TRACK_APPEARED_RIGHT(A,U7)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- THROTTLE_END(A); THROTTLE_END(B)
- TRACK_APPEARED_LEFT(B,U5); EGO_PATH_ENTRY(A,B); EGO_PATH_ENTRY(B,U12)
- CRITICAL_TTC_END(A,U1); EGO_PATH_EXIT(A,U1)
- EGO_PATH_ENTRY(B,U2); CRITICAL_TTC_START(B,U2)
- CRITICAL_TTC_END(B,U2); EGO_PATH_EXIT(B,U2)
- EGO_PATH_ENTRY(B,U7); TRACK_LOST(A,U15)

### States still active when observation ended

A:
- MOVING, since A:e01 (t = 0.00 s)
- CRITICAL_TTC of track_005, since A:e14 (t = 7.35 s)
- EGO_PATH of track_003, since A:e23 (t = 7.85 s)
- CRITICAL_TTC of track_009, since A:e31 (t = 10.15 s)
- EGO_PATH of track_009, since A:e32 (t = 10.25 s)
- CRITICAL_TTC of track_001, since A:e33 (t = 10.50 s)
- EGO_PATH of track_001, since A:e34 (t = 11.00 s)
B:
- MOVING, since B:e01 (t = 0.00 s)
- CRITICAL_TTC of track_001, since B:e13 (t = 0.50 s)
- CLOSING of track_010, since B:e14 (t = 0.60 s); the track was lost at 3.80 s
- EGO_PATH of track_012, since B:e31 (t = 8.00 s); the track was lost at 9.35 s
- CUT_IN_FROM_RIGHT of track_007, since B:e38 (t = 10.10 s)
- CUT_IN_FROM_RIGHT of track_003, since B:e39 (t = 10.45 s)
- CRITICAL_TTC of track_007, since B:e42 (t = 10.70 s)
- CLOSING of track_003, since B:e43 (t = 11.10 s)
- EGO_PATH of track_007, since B:e44 (t = 11.15 s)
- CRITICAL_TTC of track_003, since B:e45 (t = 11.30 s)
- EGO_PATH of track_003, since B:e49 (t = 11.80 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e20 at 7.75 s (local): ego: MOVING, THROTTLE; track_001: CRITICAL_TTC, IN_EGO_PATH; track_002: no active state; track_003: CLOSING, CRITICAL_TTC; track_005: CRITICAL_TTC, IN_EGO_PATH; track_008: CRITICAL_TTC?; track_009: IN_EGO_PATH, CRITICAL_TTC?; track lost, states UNKNOWN: track_004, track_006, track_007
- B B:e25 at 7.75 s (local): ego: MOVING, THROTTLE; track_001: CRITICAL_TTC, IN_EGO_PATH; track_002: CLOSING, CRITICAL_TTC; track_003: no active state; track_007: no active state; track_008: no active state; track_011: no active state; track_012: no active state; track_013: no active state; track lost, states UNKNOWN: track_004, track_005, track_006, track_009, track_010

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- lost with no state active: track_004, track_006, track_007, track_011
B:
- track_010 at 3.80 s (B:e18): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 9.35 s (B:e36): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_009, track_004, track_006, track_005, track_014, track_011, track_015

## Uncertainty and limitations

- A:track_001 stays anonymous (U1): ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006).
- A:track_002 stays anonymous (U2): ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006).
- A:track_004 stays anonymous (U9): not approaching before the contact: clearance 10.1 m -> 10.3 m over the last 1.0 s.
- A:track_005 stays anonymous (U3): tracked for 0.90 s before the matched collision (needs 1.00 s); not approaching before the contact: clearance 10.2 m -> 10.2 m over the last 1.0 s.
- A:track_006 stays anonymous (U13): ambiguous: 4 persistent tracks of A are compatible with the contact (track_001, track_002, track_003, track_006).
- A:track_007 stays anonymous (U14): tracked for 0.70 s before the matched collision (needs 1.00 s).
- A:track_008 stays anonymous (U10): tracked for 0.35 s before the matched collision (needs 1.00 s).
- A:track_009 stays anonymous (U7): tracked for 0.15 s before the matched collision (needs 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_010 stays anonymous (U11): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_011 stays anonymous (U15): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous (U3): ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013).
- B:track_003 stays anonymous (U1): ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013).
- B:track_004 stays anonymous (U4): lost 4.10 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous (U5): lost 1.05 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 6.6 m -> 7.2 m over the last 1.0 s.
- B:track_006 stays anonymous (U6): lost 4.05 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_007 stays anonymous (U7): ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013).
- B:track_008 stays anonymous (U2): ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013).
- B:track_009 stays anonymous (U8): lost 5.55 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_010 stays anonymous (U6): lost 3.95 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_011 stays anonymous (U10): ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013).
- B:track_012 stays anonymous (U11): ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013).
- B:track_013 stays anonymous (U12): ambiguous: 8 persistent tracks of B are compatible with the contact (track_001, track_002, track_003, track_007, track_008, track_011, track_012, track_013).
- B:track_014 stays anonymous (U5): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.10 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_015 stays anonymous (U16): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 3.60 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_016 stays anonymous (U17): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 3.95 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
    "max_association_distance_m": 2.5,
    "max_velocity_mismatch_mps": 4.0,
    "max_track_gap_s": 0.5,
    "min_track_frames": 5,
    "measurement_std_m": 0.5,
    "radial_speed_std_mps": 0.3,
    "acceleration_std_mps2": 6.0,
    "smoothing_innovation_sigma": 3.0,
    "min_slowdown_returns": 3,
    "identity_body_width_m": 2.5,
    "gating": "fixed",
    "covariance_components": "position,doppler,ambiguity,survival,confirmation",
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
    "association_method": "current",
    "radar_range_std_m": 0.25,
    "radar_azimuth_std_deg": 0.5,
    "assignment_likelihood_ratio": 20.0,
    "retrospective_new_target_density": 3.57e-05,
    "retrospective_min_posterior": 0.95
  }
}
```
