# Reconstruction report - S19/run_0

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 42 | 69 | 13 | A:e22 @ 7.75 s |
| B | 11.95 s | 121 | 36 | 74 | 11 | B:e19 @ 7.75 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e22 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e19 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 255.03 vs 255.03 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 7.05 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 10.9 m -> 11.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U1: A:track_001#segment_1 |
| A:track_001#segment_2 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.00 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.7 m -> 11.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.54 m/s over 3.0 s<br>clearance at the contact 11.07 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001#segment_2, track_004, track_005#segment_2, track_006)<br>anonymous road user U8: B:track_006, A:track_001#segment_2 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 5.45 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 41.4 m -> 41.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_002 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 5.30 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 41.9 m -> 42.0 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_007 |
| A:track_004 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.3 m -> 0.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.38 m/s over 3.0 s<br>clearance at the contact 0.13 m<br>the only compatible track of A touching it at the contact (clearance 0.13 m; track_001#segment_2, track_005#segment_2, track_006 at 11.07 m, 10.52 m, 41.98 m) |
| A:track_005#segment_1 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 1.50 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 11.0 m -> 10.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.47 m/s over 1.5 s<br>anonymous road user U7: A:track_005#segment_1, B:track_005, A:track_008 |
| A:track_005#segment_2 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.45 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.6 m -> 10.5 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.55 m/s over 1.5 s<br>clearance at the contact 10.17 m (beyond 3.50 m: confidence factor 0.08)<br>anonymous road user U9: A:track_005#segment_2 |
| A:track_005#segment_3 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U4: B:track_001, A:track_005#segment_3 |
| A:track_006 | U12 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.20 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.1 m -> 42.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.62 m/s over 1.2 s<br>clearance at the contact 41.88 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 4 persistent tracks of A are compatible with the contact (track_001#segment_2, track_004, track_005#segment_2, track_006)<br>anonymous road user U12: A:track_006 |
| A:track_007 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.35 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.3 m -> 26.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.60 m/s over 0.3 s<br>clearance at the contact 26.21 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U10: B:track_008, A:track_007 |
| A:track_008 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.10 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U7: A:track_005#segment_1, B:track_005, A:track_008 |
| A:track_009 | U11 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U11: B:track_009, A:track_009 |
| A:track_010 | U14 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U14: A:track_010 |
| B:track_001 | U4 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.5 m -> 9.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.03 m/s over 3.0 s<br>clearance at the contact 9.92 m (beyond 3.50 m: confidence factor 0.10)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U4: B:track_001, A:track_005#segment_3 |
| B:track_002 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.76 m/s over 3.0 s<br>clearance at the contact 0.71 m<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>common frame: its returns lie on A's own footprint (median 0.00 m, 0.00 sigma, over 240 samples; 94% within 3 sigma) at A's own velocity (median difference 0.20 m/s) |
| B:track_003 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.7 m -> 28.5 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U5: B:track_003 |
| B:track_004 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 3.95 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 28.4 m -> 28.0 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U6: B:track_004 |
| B:track_005 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.5 m -> 11.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 3.0 s<br>clearance at the contact 11.10 m (beyond 3.50 m: confidence factor 0.04)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U7: A:track_005#segment_1, B:track_005, A:track_008 |
| B:track_006 | U8 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 11.2 m -> 10.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.07 m/s over 3.0 s<br>clearance at the contact 10.56 m (beyond 3.50 m: confidence factor 0.06)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U8: B:track_006, A:track_001#segment_2 |
| B:track_007 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 5.55 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 44.6 m -> 44.2 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_007 |
| B:track_008 | U10 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.08 m/s over 1.4 s<br>clearance at the contact 26.21 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U10: B:track_008, A:track_007 |
| B:track_009 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 26.8 m -> 26.7 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.3 s<br>clearance at the contact 26.68 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U11: B:track_009, A:track_009 |
| B:track_010 | U13 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 1.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 42.5 m -> 41.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.11 m/s over 1.2 s<br>clearance at the contact 41.94 m (beyond 3.50 m: confidence factor 0.00)<br>ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010)<br>anonymous road user U13: B:track_010 |
| B:track_011 | U15 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 255.03 vs 255.03 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.60 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U15: B:track_011 |

## Road users in the common frame

- B:track_002 is A: its returns lie on A's own footprint (median 0.00 m over 240 samples, 94% within 3 sigma) at A's velocity.
- U1 (anonymous, -7.75 to -7.05 s): A:track_001#segment_1; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit.
- U2 (anonymous, -7.75 to -5.45 s): A:track_002; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U3 (anonymous, -7.75 to -5.30 s): A:track_003, B:track_007 joined by same box A:track_003-B:track_007 (100% of 27 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U4 (anonymous, -7.75 to 4.20 s): B:track_001, A:track_005#segment_3 joined by same box A:track_005#segment_3-B:track_001 (100% of 74 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U5 (anonymous, -7.75 to -4.10 s): B:track_003; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U6 (anonymous, -7.75 to -3.95 s): B:track_004; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U7 (anonymous, -7.70 to 4.20 s): A:track_005#segment_1, B:track_005, A:track_008 joined by same box A:track_005#segment_1-B:track_005 (100% of 125 instants); same box A:track_008-B:track_005 (92% of 83 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U8 (anonymous, -7.70 to 4.20 s): B:track_006, A:track_001#segment_2 joined by same box A:track_001#segment_2-B:track_006 (100% of 225 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U9 (anonymous, -1.45 to 0.50 s): A:track_005#segment_2; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U10 (anonymous, -1.40 to 4.20 s): B:track_008, A:track_007 joined by same box A:track_007-B:track_008 (100% of 19 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U11 (anonymous, -1.35 to 4.20 s): B:track_009, A:track_009 joined by same box A:track_009-B:track_009 (100% of 12 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U12 (anonymous, -1.20 to -0.05 s): A:track_006; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U13 (anonymous, -1.15 to 4.20 s): B:track_010; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U14 (anonymous, 1.75 to 3.40 s): A:track_010; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U15 (anonymous, 3.60 to 3.90 s): B:track_011; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.

## Global graph

77 nodes, 175 edges; 24 merged node(s): g05 TRACK_APPEARED_FRONT(A,U2) from A:e03 + A:e11, g08 TRACK_APPEARED_LEFT(A,U1) from A:e04 + A:e09, g09 TRACK_APPEARED_LEFT(A,U3) from A:e05 + A:e12, g10 TRACK_APPEARED_LEFT(B,U5) from B:e04 + B:e12, g12 TRACK_APPEARED_RIGHT(B,U6) from B:e06 + B:e13, g13 TRACK_APPEARED_FRONT(A,U7) from A:e07 + A:e13, g14 TRACK_APPEARED_FRONT(B,U3) from B:e07 + B:e11, g27 TRACK_APPEARED_FRONT(A,U9) from A:e14 + A:e28, g28 TRACK_APPEARED_RIGHT(B,U10) from B:e14 + B:e25, g29 CRITICAL_TTC_START(A,B) from A:e15 + A:e23, g30 TRACK_APPEARED_LEFT(B,U11) from B:e15 + B:e28, g31 TRACK_APPEARED_FRONT(A,U12) from A:e16 + A:e21, g33 EGO_PATH_ENTRY(A,U12) from A:e17 + A:e20, g34 CLOSING_START(A,B) from A:e18 + A:e27, g35 CRITICAL_TTC_START(B,A) from B:e17 + B:e20, g36 CLOSING_START(B,A) from B:e18 + B:e21, g40 COLLISION(A,B) from A:e22 + B:e19, g48 EGO_PATH_ENTRY(B,U13) from B:e23 + B:e29, g53 CRITICAL_TTC_START(A,U7) from A:e30 + A:e33, g59 EGO_PATH_ENTRY(A,U10) from A:e35 + A:e41, g60 EGO_PATH_ENTRY(B,U8) from B:e26 + B:e32, g61 CRITICAL_TTC_START(B,U8) from B:e27 + B:e31, g63 TRACK_APPEARED_LEFT(A,U14) from A:e36 + A:e40, g74 TRACK_APPEARED_LEFT(B,U15) from B:e35 + B:e36.

### Event sequence (global time)

- `-7.75` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_FRONT(B,U4); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U3); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U6)
- `-7.70` TRACK_APPEARED_FRONT(A,U7); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(B,U8); TRACK_APPEARED_RIGHT(B,U7)
- `-7.25` CRITICAL_TTC_START(B,U4)
- `-7.20` CRITICAL_TTC_START(A,U7)
- `-7.05` TRACK_LOST(A,U1)
- `-7.00` TRACK_APPEARED_LEFT(A,U8)
- `-5.55` TRACK_LOST(B,U3)
- `-5.45` TRACK_LOST(A,U2)
- `-5.30` TRACK_LOST(A,U3)
- `-4.10` TRACK_LOST(B,U5)
- `-3.95` TRACK_LOST(B,U6)
- `-1.50` TRACK_LOST(A,U7)
- `-1.45` TRACK_APPEARED_FRONT(A,U9)
- `-1.40` TRACK_APPEARED_RIGHT(B,U10); CRITICAL_TTC_START(A,B)
- `-1.35` TRACK_APPEARED_LEFT(B,U11)
- `-1.20` TRACK_APPEARED_FRONT(A,U12)
- `-1.15` TRACK_APPEARED_FRONT(B,U13)
- `-1.10` EGO_PATH_ENTRY(A,U12)
- `-0.80` CLOSING_START(A,B)
- `-0.75` CRITICAL_TTC_START(B,A)
- `-0.70` CLOSING_START(B,A)
- `-0.35` TRACK_APPEARED_RIGHT(A,U10)
- `-0.20` EGO_PATH_EXIT(A,U12)
- `-0.05` TRACK_LOST(A,U12)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.05` THROTTLE_END(A); THROTTLE_END(B)
- `+0.10` TRACK_APPEARED_FRONT(A,U7); EGO_PATH_ENTRY(A,B); EGO_PATH_ENTRY(B,U13)
- `+0.15` CLOSING_END(A,B)
- `+0.25` EGO_PATH_ENTRY(B,U11)
- `+0.50` TRACK_LOST(A,U9)
- `+0.55` TRACK_APPEARED_FRONT(A,U4)
- `+0.60` CRITICAL_TTC_START(A,U7)
- `+0.70` TRACK_APPEARED_LEFT(A,U11)
- `+1.05` CRITICAL_TTC_START(A,U4)
- `+1.10` TRACK_LOST(B,U10)
- `+1.20` CRITICAL_TTC_END(A,U7); EGO_PATH_EXIT(A,U7)
- `+1.35` EGO_PATH_ENTRY(A,U10)
- `+1.45` EGO_PATH_ENTRY(B,U8); CRITICAL_TTC_START(B,U8)
- `+1.60` TRACK_LOST(B,U11)
- `+1.75` TRACK_APPEARED_LEFT(A,U14)
- `+1.85` EGO_PATH_EXIT(B,U13); CUT_IN_FROM_RIGHT_START(B,U7)
- `+2.00` CRITICAL_TTC_START(A,U7)
- `+2.50` EGO_PATH_ENTRY(A,U7)
- `+2.70` CUT_IN_FROM_RIGHT_START(A,U7)
- `+2.80` CRITICAL_TTC_END(B,U8); EGO_PATH_EXIT(B,U8)
- `+2.95` CRITICAL_TTC_START(B,U7)
- `+3.40` EGO_PATH_ENTRY(B,U7); TRACK_LOST(A,U14)
- `+3.60` TRACK_APPEARED_LEFT(B,U15)
- `+3.80` EGO_PATH_EXIT(A,U10)
- `+3.85` EGO_PATH_EXIT(A,U4)
- `+3.90` TRACK_LOST(B,U15)

### What happened, in plain language

- 7.75 s before the reference collision, A started moving (already the case when first observed).
- 7.75 s before the reference collision, B started moving (already the case when first observed).
- 7.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U4, which appeared in front of it.
- 7.75 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 7.70 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared in front of it.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U8, which appeared on its left.
- 7.70 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U4 became critical.
- 7.20 s before the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 7.05 s before the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 7.00 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared on its left.
- 5.55 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 5.45 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 5.30 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 4.10 s before the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 3.95 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.50 s before the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 1.45 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared in front of it.
- 1.40 s before the reference collision, B's radar started tracking anonymous road user U10, which appeared on its right.
- 1.40 s before the reference collision, A's time-to-contact with B became critical.
- 1.35 s before the reference collision, B's radar started tracking anonymous road user U11, which appeared on its left.
- 1.20 s before the reference collision, A's radar started tracking anonymous road user U12, which appeared in front of it.
- 1.15 s before the reference collision, B's radar started tracking anonymous road user U13, which appeared in front of it.
- 1.10 s before the reference collision, A observed anonymous road user U12 enter its forward path corridor.
- 0.80 s before the reference collision, A observed B start closing in.
- 0.75 s before the reference collision, B's time-to-contact with A became critical.
- 0.70 s before the reference collision, B observed A start closing in.
- 0.35 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 0.20 s before the reference collision, A observed anonymous road user U12 leave its forward path corridor.
- 0.05 s before the reference collision, A's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 255, B: 255 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.10 s after the reference collision, A's radar started tracking anonymous road user U7, which appeared in front of it.
- 0.10 s after the reference collision, A observed B enter its forward path corridor.
- 0.10 s after the reference collision, B observed anonymous road user U13 enter its forward path corridor.
- 0.15 s after the reference collision, A observed B stop closing in.
- 0.25 s after the reference collision, B observed anonymous road user U11 enter its forward path corridor.
- 0.50 s after the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the reference collision, A's radar started tracking anonymous road user U4, which appeared in front of it.
- 0.60 s after the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 0.70 s after the reference collision, A's radar started tracking anonymous road user U11, which appeared on its left.
- 1.05 s after the reference collision, A's time-to-contact with anonymous road user U4 became critical.
- 1.10 s after the reference collision, B's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 1.20 s after the reference collision, A's time-to-contact with anonymous road user U7 stopped being critical.
- 1.20 s after the reference collision, A observed anonymous road user U7 leave its forward path corridor.
- 1.35 s after the reference collision, A observed anonymous road user U10 enter its forward path corridor.
- 1.45 s after the reference collision, B observed anonymous road user U8 enter its forward path corridor.
- 1.45 s after the reference collision, B's time-to-contact with anonymous road user U8 became critical.
- 1.60 s after the reference collision, B's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 1.75 s after the reference collision, A's radar started tracking anonymous road user U14, which appeared on its left.
- 1.85 s after the reference collision, B observed anonymous road user U13 leave its forward path corridor.
- 1.85 s after the reference collision, B observed anonymous road user U7 cutting in from the right.
- 2.00 s after the reference collision, A's time-to-contact with anonymous road user U7 became critical.
- 2.50 s after the reference collision, A observed anonymous road user U7 enter its forward path corridor.
- 2.70 s after the reference collision, A observed anonymous road user U7 cutting in from the right.
- 2.80 s after the reference collision, B's time-to-contact with anonymous road user U8 stopped being critical.
- 2.80 s after the reference collision, B observed anonymous road user U8 leave its forward path corridor.
- 2.95 s after the reference collision, B's time-to-contact with anonymous road user U7 became critical.
- 3.40 s after the reference collision, B observed anonymous road user U7 enter its forward path corridor.
- 3.40 s after the reference collision, A's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- 3.60 s after the reference collision, B's radar started tracking anonymous road user U15, which appeared on its left.
- 3.80 s after the reference collision, A observed anonymous road user U10 leave its forward path corridor.
- 3.85 s after the reference collision, A observed anonymous road user U4 leave its forward path corridor.
- 3.90 s after the reference collision, B's radar lost anonymous road user U15 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_004 (B): CRITICAL_TTC_START 6.35, COLLISION with B 7.75 (+1.40 s); EGO_PATH_ENTRY 7.85 after critical TTC (+1.50 s) [local times; t_global: critical_ttc_start -1.40, ego_path_entry +0.10, collision +0.00]
- A's track_005#segment_1 (unidentified U7): CRITICAL_TTC_START 0.55, COLLISION 7.75 (+7.20 s) [local times; t_global: critical_ttc_start -7.20, collision +0.00]
- A's track_005#segment_3 (unidentified U4): CRITICAL_TTC_START 8.80 [local times; t_global: critical_ttc_start +1.05]
- A's track_006 (unidentified U12): EGO_PATH_ENTRY 6.65, no critical TTC [local times; t_global: ego_path_entry -1.10, collision +0.00]
- A's track_007 (unidentified U10): EGO_PATH_ENTRY 9.10, no critical TTC [local times; t_global: ego_path_entry +1.35]
- A's track_008 (unidentified U7): critical TTC already active before the cut-in: CRITICAL_TTC_START 9.75 <= CUT_IN_FROM_RIGHT_START 10.45 (+0.70 s); EGO_PATH_ENTRY 10.25 after critical TTC (+0.50 s) [local times; t_global: cut_in +2.70, critical_ttc_start +2.00, ego_path_entry +2.50]
- B's track_001 (unidentified U4): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 7.00, COLLISION with A 7.75 (+0.75 s) [local times; t_global: critical_ttc_start -0.75, collision +0.00]
- B's track_005 (unidentified U7): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 9.60 < CRITICAL_TTC_START 10.70 (+1.10 s); EGO_PATH_ENTRY 11.15 after critical TTC (+0.45 s) [local times; t_global: cut_in +1.85, critical_ttc_start +2.95, ego_path_entry +3.40]
- B's track_006 (unidentified U8): CRITICAL_TTC_START 9.20; EGO_PATH_ENTRY 9.20 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start +1.45, ego_path_entry +1.45]
- B's track_009 (unidentified U11): EGO_PATH_ENTRY 8.00, no critical TTC [local times; t_global: ego_path_entry +0.25]
- B's track_010 (unidentified U13): EGO_PATH_ENTRY 7.85, no critical TTC [local times; t_global: ego_path_entry +0.10]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_FRONT(B,U4); TRACK_APPEARED_LEFT(A,B); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U3); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U6)
- TRACK_APPEARED_FRONT(A,U7); TRACK_APPEARED_FRONT(B,U3); TRACK_APPEARED_LEFT(B,U8); TRACK_APPEARED_RIGHT(B,U7)
- TRACK_APPEARED_RIGHT(B,U10); CRITICAL_TTC_START(A,B)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- THROTTLE_END(A); THROTTLE_END(B)
- TRACK_APPEARED_FRONT(A,U7); EGO_PATH_ENTRY(A,B); EGO_PATH_ENTRY(B,U13)
- CRITICAL_TTC_END(A,U7); EGO_PATH_EXIT(A,U7)
- EGO_PATH_ENTRY(B,U8); CRITICAL_TTC_START(B,U8)
- EGO_PATH_EXIT(B,U13); CUT_IN_FROM_RIGHT_START(B,U7)
- CRITICAL_TTC_END(B,U8); EGO_PATH_EXIT(B,U8)
- EGO_PATH_ENTRY(B,U7); TRACK_LOST(A,U14)

### States still active when observation ended

A:
- MOVING, since A:e01 (t = 0.00 s)
- CRITICAL_TTC of track_005#segment_1, since A:e08 (t = 0.55 s); the track was lost at 6.25 s
- EGO_PATH of track_004, since A:e26 (t = 7.85 s)
- CRITICAL_TTC of track_005#segment_3, since A:e32 (t = 8.80 s)
- CRITICAL_TTC of track_008, since A:e37 (t = 9.75 s)
- EGO_PATH of track_008, since A:e38 (t = 10.25 s)
- CUT_IN_FROM_RIGHT of track_008, since A:e39 (t = 10.45 s)
B:
- MOVING, since B:e01 (t = 0.00 s)
- CRITICAL_TTC of track_001, since B:e10 (t = 0.50 s)
- EGO_PATH of track_009, since B:e24 (t = 8.00 s); the track was lost at 9.35 s
- CUT_IN_FROM_RIGHT of track_005, since B:e30 (t = 9.60 s)
- CRITICAL_TTC of track_005, since B:e33 (t = 10.70 s)
- EGO_PATH of track_005, since B:e34 (t = 11.15 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e22 at 7.75 s (local): ego: MOVING, THROTTLE; track_001#segment_2: no active state; track_004: CLOSING, CRITICAL_TTC; track_005#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?; track_007: CRITICAL_TTC?; track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_005#segment_1, track_006
- B B:e19 at 7.75 s (local): ego: MOVING, THROTTLE; track_001: CRITICAL_TTC, IN_EGO_PATH; track_002: CLOSING, CRITICAL_TTC; track_005: no active state; track_006: no active state; track_008: no active state; track_009: no active state; track_010: no active state; track lost, states UNKNOWN: track_003, track_004, track_007

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_005#segment_1 at 6.25 s (A:e13): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001#segment_1, track_002, track_003, track_006, track_005#segment_2, track_010
B:
- track_009 at 9.35 s (B:e28): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_007, track_003, track_004, track_008, track_011

## Uncertainty and limitations

- A:track_001#segment_1 stays anonymous (U1): lost 7.05 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 10.9 m -> 11.7 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_001#segment_2 stays anonymous (U8): ambiguous: 4 persistent tracks of A are compatible with the contact (track_001#segment_2, track_004, track_005#segment_2, track_006).
- A:track_002 stays anonymous (U2): lost 5.45 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 41.4 m -> 41.5 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_003 stays anonymous (U3): lost 5.30 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 41.9 m -> 42.0 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_005#segment_1 stays anonymous (U7): lost 1.50 s before the matched collision (window 1.00 s).
- A:track_005#segment_2 stays anonymous (U9): insufficient evidence.
- A:track_005#segment_3 stays anonymous (U4): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.55 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_006 stays anonymous (U12): ambiguous: 4 persistent tracks of A are compatible with the contact (track_001#segment_2, track_004, track_005#segment_2, track_006).
- A:track_007 stays anonymous (U10): tracked for 0.35 s before the matched collision (needs 1.00 s).
- A:track_008 stays anonymous (U7): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.10 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_009 stays anonymous (U11): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.70 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_010 stays anonymous (U14): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous (U4): ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010).
- B:track_003 stays anonymous (U5): lost 4.10 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_004 stays anonymous (U6): lost 3.95 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous (U7): ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010).
- B:track_006 stays anonymous (U8): ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010).
- B:track_007 stays anonymous (U3): lost 5.55 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_008 stays anonymous (U10): ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010).
- B:track_009 stays anonymous (U11): ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010).
- B:track_010 stays anonymous (U13): ambiguous: 7 persistent tracks of B are compatible with the contact (track_001, track_002, track_005, track_006, track_008, track_009, track_010).
- B:track_011 stays anonymous (U15): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 3.60 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
