# Reconstruction report - S16/run_0_overtaking

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 55 | 119 | 13 | A:e28 @ 6.75 s |
| B | 11.95 s | 121 | 55 | 117 | 10 | B:e25 @ 6.75 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e28 | 6.75 | -6.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e25 | 6.75 | -6.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 191.84 vs 191.84 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 10.5 m -> 12.4 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.09 m/s over 3.0 s<br>clearance at the contact 10.49 m (beyond 3.50 m: confidence factor 0.07)<br>anonymous road user U1: A:track_001, B:track_001 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 3.15 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 21.4 m -> 23.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U2: A:track_002 |
| A:track_003#segment_1 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 2.00 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 12.1 m -> 11.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.82 m/s over 1.0 s (> 1.50)<br>anonymous road user U3: A:track_003#segment_1, B:track_003, A:track_003#segment_3 |
| A:track_003#segment_2 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.95 s before the matched collision<br>continuous up to the contact: last observed 0.55 s before it (window 1.00 s)<br>not approaching before the contact: clearance 12.2 m -> 12.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 1.94 m/s over 1.4 s (> 1.50)<br>clearance at the contact 12.10 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U8: A:track_003#segment_2 |
| A:track_003#segment_3 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.50 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 12.2 m -> 12.2 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 2.04 m/s over 0.5 s (> 1.50)<br>clearance at the contact 12.16 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U3: A:track_003#segment_1, B:track_003, A:track_003#segment_3 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 3.15 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 26.6 m -> 24.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U4: A:track_004 |
| A:track_005 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 6.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 6.4 m -> 7.4 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U5: A:track_005 |
| A:track_006 | B | ASSOCIATED | 0.73 | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.18 m/s over 3.0 s<br>clearance at the contact 0.16 m<br>the only track of A compatible with the contact |
| A:track_007 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.45 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.6 m -> 19.2 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 4.06 m/s over 1.5 s (> 1.50)<br>clearance at the contact 19.16 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U9: A:track_007, B:track_006 |
| A:track_008 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.85 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 28.0 m -> 29.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.14 m/s over 0.8 s<br>clearance at the contact 27.96 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U10: A:track_008 |
| A:track_009 | U13 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U13: A:track_009 |
| A:track_010 | U15 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.55 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U15: A:track_010, B:track_010 |
| A:track_011 | U14 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.80 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U14: B:track_009, A:track_011 |
| B:track_001 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 10.3 m -> 10.3 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.93 m/s over 3.0 s (> 1.50)<br>clearance at the contact 10.28 m (beyond 3.50 m: confidence factor 0.08)<br>anonymous road user U1: A:track_001, B:track_001 |
| B:track_002 | A | ASSOCIATED | 0.73 | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.1 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.19 m/s over 3.0 s<br>clearance at the contact 0.19 m<br>the only compatible track of B touching it at the contact (clearance 0.19 m; track_003 at 10.50 m) |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 12.4 m -> 10.5 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.12 m/s over 3.0 s<br>clearance at the contact 10.50 m (beyond 3.50 m: confidence factor 0.07)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_002, track_003)<br>anonymous road user U3: A:track_003#segment_1, B:track_003, A:track_003#segment_3 |
| B:track_004 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.75 s before the matched collision<br>lost 1.55 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 12.3 m -> 16.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.70 m/s over 1.5 s (> 1.50)<br>anonymous road user U6: B:track_004 |
| B:track_005 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 6.55 s before the matched collision<br>lost 3.65 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 35.1 m -> 33.1 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_005 |
| B:track_006 | U9 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 1.10 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 21.7 m -> 17.9 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.05 m/s over 1.1 s (> 1.50)<br>clearance at the contact 17.87 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U9: A:track_007, B:track_006 |
| B:track_007 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.85 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 27.9 m -> 26.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.03 m/s over 0.8 s<br>clearance at the contact 26.20 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U11: B:track_007 |
| B:track_008 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.55 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 35.8 m -> 33.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.96 m/s over 0.5 s (> 1.50)<br>clearance at the contact 33.46 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U12: B:track_008 |
| B:track_009 | U14 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.50 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U14: B:track_009, A:track_011 |
| B:track_010 | U15 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 191.84 vs 191.84 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 3.45 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U15: A:track_010, B:track_010 |

## Road users in the common frame

- U1 (anonymous, -6.75 to 4.45 s): A:track_001, B:track_001 joined by same box A:track_001-B:track_001 (100% of 200 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U2 (anonymous, -6.75 to -3.15 s): A:track_002; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U3 (anonymous, -6.75 to 5.20 s): A:track_003#segment_1, B:track_003, A:track_003#segment_3 joined by same box A:track_003#segment_1-B:track_003 (100% of 89 instants); same box A:track_003#segment_3-B:track_003 (99% of 96 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U4 (anonymous, -6.75 to -3.15 s): A:track_004; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U5 (anonymous, -6.75 to -6.25 s): A:track_005; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U6 (anonymous, -6.75 to -1.55 s): B:track_004; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U7 (anonymous, -6.55 to -3.65 s): B:track_005; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U8 (anonymous, -1.95 to -0.55 s): A:track_003#segment_2; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U9 (anonymous, -1.45 to 5.20 s): A:track_007, B:track_006 joined by same box A:track_007-B:track_006 (100% of 108 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U10 (anonymous, -0.85 to 5.10 s): A:track_008; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U11 (anonymous, -0.85 to 4.80 s): B:track_007; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U12 (anonymous, -0.55 to 0.80 s): B:track_008; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U13 (anonymous, 1.15 to 5.20 s): A:track_009; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U14 (anonymous, 1.50 to 3.20 s): B:track_009, A:track_011 joined by same box A:track_011-B:track_009 (100% of 12 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U15 (anonymous, 1.55 to 5.20 s): A:track_010, B:track_010 joined by same box A:track_010-B:track_010 (100% of 36 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.

## Global graph

109 nodes, 274 edges; 38 merged node(s): g05 TRACK_APPEARED_FRONT(A,U3) from A:e03 + A:e16, g06 TRACK_APPEARED_FRONT(B,U1) from B:e03 + B:e53, g07 TRACK_APPEARED_LEFT(A,U1) from A:e04 + A:e53, g08 TRACK_APPEARED_LEFT(A,U2) from A:e05 + A:e13, g09 TRACK_APPEARED_RIGHT(A,U4) from A:e06 + A:e14, g10 TRACK_APPEARED_RIGHT(A,U5) from A:e07 + A:e12, g13 TRACK_APPEARED_RIGHT(B,U6) from B:e06 + B:e16, g15 CLOSING_START(B,A) from B:e07 + B:e14, g16 CLOSING_START(B,U3) from B:e08 + B:e32, g17 TRACK_APPEARED_FRONT(B,U7) from B:e09 + B:e12, g20 CLOSING_START(A,B) from A:e10 + A:e15, g22 CRITICAL_TTC_START(B,U1) from B:e11 + B:e38, g25 CUT_IN_FROM_RIGHT_START(B,A) from B:e13 + B:e15, g32 TRACK_APPEARED_FRONT(A,U8) from A:e17 + A:e25, g33 CRITICAL_TTC_START(A,B) from A:e18 + A:e29, g36 CLOSING_START(A,U9) from A:e20 + A:e36, g37 CRITICAL_TTC_START(B,A) from B:e17 + B:e26, g40 CLOSING_START(B,U9) from B:e19 + B:e34, g41 EGO_PATH_ENTRY(A,U1) from A:e22 + A:e38, g42 TRACK_APPEARED_FRONT(A,U10) from A:e23 + A:e55, g43 TRACK_APPEARED_RIGHT(B,U11) from B:e20 + B:e55, g44 CLOSING_START(B,U11) from B:e21 + B:e31, g45 TRACK_APPEARED_RIGHT(B,U12) from B:e22 + B:e39, g46 CLOSING_START(A,B) from A:e24 + A:e31, g47 CLOSING_START(B,U12) from B:e23 + B:e35, g50 CLOSING_START(B,A) from B:e24 + B:e27, g51 EGO_PATH_ENTRY(A,B) from A:e27 + A:e41, g52 COLLISION(A,B) from A:e28 + B:e25, g62 EGO_PATH_ENTRY(A,U3) from A:e34 + A:e49, g63 CRITICAL_TTC_START(A,U3) from A:e35 + A:e37, g64 EGO_PATH_ENTRY(B,U11) from B:e30 + B:e46, g68 EGO_PATH_ENTRY(B,U3) from B:e33 + B:e51, g72 CRITICAL_TTC_START(B,U3) from B:e37 + B:e44, g86 TRACK_APPEARED_LEFT(B,U14) from B:e43 + B:e49, g88 CLOSING_START(A,U15) from A:e46 + A:e52, g89 EGO_PATH_ENTRY(A,U9) from A:e47 + A:e54, g91 TRACK_APPEARED_LEFT(A,U14) from A:e48 + A:e50, g94 EGO_PATH_ENTRY(B,U9) from B:e47 + B:e54.

### Event sequence (global time)

- `-6.75` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U1); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(A,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U3); TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(A,U4); CLOSING_START(B,A); CLOSING_START(B,U3)
- `-6.55` TRACK_APPEARED_FRONT(B,U7); CLOSING_START(B,U7)
- `-6.35` TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-6.25` CRITICAL_TTC_START(A,U3); CRITICAL_TTC_START(B,U1); TRACK_LOST(A,U5)
- `-3.65` TRACK_LOST(B,U7)
- `-3.25` CUT_IN_FROM_RIGHT_START(B,A)
- `-3.15` TRACK_LOST(A,U2); TRACK_LOST(A,U4)
- `-2.90` CLOSING_END(A,B)
- `-2.60` CLOSING_END(B,A)
- `-2.45` CUT_IN_FROM_RIGHT_END(B,A)
- `-2.00` TRACK_LOST(A,U3)
- `-1.95` TRACK_APPEARED_FRONT(A,U8)
- `-1.65` CRITICAL_TTC_START(A,B)
- `-1.55` TRACK_LOST(B,U6)
- `-1.45` TRACK_APPEARED_RIGHT(A,U9); CLOSING_START(A,U9)
- `-1.20` CRITICAL_TTC_START(B,A)
- `-1.15` CRITICAL_TTC_START(A,U1)
- `-1.10` TRACK_APPEARED_RIGHT(B,U9); CLOSING_START(B,U9)
- `-1.05` EGO_PATH_ENTRY(A,U1)
- `-0.85` TRACK_APPEARED_FRONT(A,U10); TRACK_APPEARED_RIGHT(B,U11); CLOSING_START(B,U11)
- `-0.55` TRACK_APPEARED_RIGHT(B,U12); CLOSING_START(A,B); CLOSING_START(B,U12); TRACK_LOST(A,U8)
- `-0.50` TRACK_APPEARED_RIGHT(A,U3)
- `-0.45` CLOSING_START(B,A)
- `-0.35` EGO_PATH_ENTRY(A,B)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); EGO_PATH_EXIT(A,U3)
- `+0.05` CLOSING_END(A,B); CLOSING_END(B,A); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- `+0.10` EGO_PATH_ENTRY(A,U3); CRITICAL_TTC_START(A,U3)
- `+0.20` EGO_PATH_ENTRY(B,U11)
- `+0.30` CLOSING_END(B,U11)
- `+0.35` CLOSING_END(B,U3)
- `+0.45` CLOSING_END(A,U9)
- `+0.50` EGO_PATH_ENTRY(B,U3)
- `+0.60` CLOSING_END(B,U12); CLOSING_END(B,U9); EGO_PATH_ENTRY(B,U12)
- `+0.65` CRITICAL_TTC_START(B,U3)
- `+0.70` CRITICAL_TTC_END(A,U3)
- `+0.80` CRITICAL_TTC_END(B,U1); EGO_PATH_EXIT(A,U1); EGO_PATH_EXIT(A,U10); TRACK_LOST(B,U12)
- `+1.15` MOVING_END(B); STOP_START(B); TRACK_APPEARED_FRONT(A,U13); EGO_PATH_ENTRY(B,A)
- `+1.20` EGO_PATH_EXIT(A,B); MOVING_END(A); STOP_START(A)
- `+1.30` EGO_PATH_ENTRY(A,B)
- `+1.50` TRACK_APPEARED_LEFT(B,U14)
- `+1.55` TRACK_APPEARED_RIGHT(A,U15); CLOSING_START(A,U15)
- `+1.60` EGO_PATH_ENTRY(A,U9)
- `+1.75` CRITICAL_TTC_END(B,U3)
- `+1.80` TRACK_APPEARED_LEFT(A,U14)
- `+1.90` EGO_PATH_EXIT(B,U1)
- `+2.30` EGO_PATH_EXIT(B,U11)
- `+2.40` EGO_PATH_ENTRY(B,U9)
- `+2.90` CUT_IN_FROM_RIGHT_START(B,U3)
- `+2.95` TRACK_LOST(B,U14)
- `+3.20` EGO_PATH_EXIT(A,U3); TRACK_LOST(A,U14)
- `+3.35` EGO_PATH_EXIT(A,U13)
- `+3.40` CLOSING_END(A,U15)
- `+3.45` TRACK_APPEARED_RIGHT(B,U15)
- `+3.60` EGO_PATH_EXIT(B,U3)
- `+4.15` CUT_IN_FROM_RIGHT_START(B,U9)
- `+4.35` TRACK_LOST(B,U1)
- `+4.45` TRACK_LOST(A,U1)
- `+4.60` EGO_PATH_EXIT(A,U9)
- `+4.80` EGO_PATH_EXIT(B,U9); TRACK_LOST(B,U11)
- `+5.10` TRACK_LOST(A,U10)

### What happened, in plain language

- 6.75 s before the reference collision, A started moving (already the case when first observed).
- 6.75 s before the reference collision, B started moving (already the case when first observed).
- 6.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 6.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 6.75 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared in front of it.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 6.75 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared on its right.
- 6.75 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.75 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 6.75 s before the reference collision, A observed anonymous road user U4 start closing in (already the case when first observed).
- 6.75 s before the reference collision, B observed A start closing in (already the case when first observed).
- 6.75 s before the reference collision, B observed anonymous road user U3 start closing in (already the case when first observed).
- 6.55 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared in front of it.
- 6.55 s before the reference collision, B observed anonymous road user U7 start closing in (already the case when first observed).
- 6.35 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.35 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.25 s before the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 6.25 s before the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 6.25 s before the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 3.65 s before the reference collision, B's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 3.25 s before the reference collision, B observed A cutting in from the right.
- 3.15 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 3.15 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 2.90 s before the reference collision, A observed B stop closing in.
- 2.60 s before the reference collision, B observed A stop closing in.
- 2.45 s before the reference collision, B observed A's cut-in from the right settle.
- 2.00 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 1.95 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared in front of it.
- 1.65 s before the reference collision, A's time-to-contact with B became critical.
- 1.55 s before the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.45 s before the reference collision, A's radar started tracking anonymous road user U9, which appeared on its right.
- 1.45 s before the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 1.20 s before the reference collision, B's time-to-contact with A became critical.
- 1.15 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 1.10 s before the reference collision, B's radar started tracking anonymous road user U9, which appeared on its right.
- 1.10 s before the reference collision, B observed anonymous road user U9 start closing in (already the case when first observed).
- 1.05 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 0.85 s before the reference collision, A's radar started tracking anonymous road user U10, which appeared in front of it.
- 0.85 s before the reference collision, B's radar started tracking anonymous road user U11, which appeared on its right.
- 0.85 s before the reference collision, B observed anonymous road user U11 start closing in (already the case when first observed).
- 0.55 s before the reference collision, B's radar started tracking anonymous road user U12, which appeared on its right.
- 0.55 s before the reference collision, A observed B start closing in.
- 0.55 s before the reference collision, B observed anonymous road user U12 start closing in (already the case when first observed).
- 0.55 s before the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 0.50 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its right.
- 0.45 s before the reference collision, B observed A start closing in.
- 0.35 s before the reference collision, A observed B enter its forward path corridor.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 192, B: 192 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 0.05 s after the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.10 s after the reference collision, A observed anonymous road user U3 enter its forward path corridor.
- 0.10 s after the reference collision, A's time-to-contact with anonymous road user U3 became critical.
- 0.20 s after the reference collision, B observed anonymous road user U11 enter its forward path corridor.
- 0.30 s after the reference collision, B observed anonymous road user U11 stop closing in.
- 0.35 s after the reference collision, B observed anonymous road user U3 stop closing in.
- 0.45 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 0.50 s after the reference collision, B observed anonymous road user U3 enter its forward path corridor.
- 0.60 s after the reference collision, B observed anonymous road user U12 stop closing in.
- 0.60 s after the reference collision, B observed anonymous road user U9 stop closing in.
- 0.60 s after the reference collision, B observed anonymous road user U12 enter its forward path corridor.
- 0.65 s after the reference collision, B's time-to-contact with anonymous road user U3 became critical.
- 0.70 s after the reference collision, A's time-to-contact with anonymous road user U3 stopped being critical.
- 0.80 s after the reference collision, B's time-to-contact with anonymous road user U1 stopped being critical.
- 0.80 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 0.80 s after the reference collision, A observed anonymous road user U10 leave its forward path corridor.
- 0.80 s after the reference collision, B's radar lost anonymous road user U12 (its states are UNKNOWN from then on, not ended).
- 1.15 s after the reference collision, B stopped moving.
- 1.15 s after the reference collision, B came to a stop.
- 1.15 s after the reference collision, A's radar started tracking anonymous road user U13, which appeared in front of it.
- 1.15 s after the reference collision, B observed A enter its forward path corridor.
- 1.20 s after the reference collision, A observed B leave its forward path corridor.
- 1.20 s after the reference collision, A stopped moving.
- 1.20 s after the reference collision, A came to a stop.
- 1.30 s after the reference collision, A observed B enter its forward path corridor.
- 1.50 s after the reference collision, B's radar started tracking anonymous road user U14, which appeared on its left.
- 1.55 s after the reference collision, A's radar started tracking anonymous road user U15, which appeared on its right.
- 1.55 s after the reference collision, A observed anonymous road user U15 start closing in (already the case when first observed).
- 1.60 s after the reference collision, A observed anonymous road user U9 enter its forward path corridor.
- 1.75 s after the reference collision, B's time-to-contact with anonymous road user U3 stopped being critical.
- 1.80 s after the reference collision, A's radar started tracking anonymous road user U14, which appeared on its left.
- 1.90 s after the reference collision, B observed anonymous road user U1 leave its forward path corridor.
- 2.30 s after the reference collision, B observed anonymous road user U11 leave its forward path corridor.
- 2.40 s after the reference collision, B observed anonymous road user U9 enter its forward path corridor.
- 2.90 s after the reference collision, B observed anonymous road user U3 cutting in from the right.
- 2.95 s after the reference collision, B's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- 3.20 s after the reference collision, A observed anonymous road user U3 leave its forward path corridor.
- 3.20 s after the reference collision, A's radar lost anonymous road user U14 (its states are UNKNOWN from then on, not ended).
- 3.35 s after the reference collision, A observed anonymous road user U13 leave its forward path corridor.
- 3.40 s after the reference collision, A observed anonymous road user U15 stop closing in.
- 3.45 s after the reference collision, B's radar started tracking anonymous road user U15, which appeared on its right.
- 3.60 s after the reference collision, B observed anonymous road user U3 leave its forward path corridor.
- 4.15 s after the reference collision, B observed anonymous road user U9 cutting in from the right.
- 4.35 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 4.45 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 4.60 s after the reference collision, A observed anonymous road user U9 leave its forward path corridor.
- 4.80 s after the reference collision, B observed anonymous road user U9 leave its forward path corridor.
- 4.80 s after the reference collision, B's radar lost anonymous road user U11 (its states are UNKNOWN from then on, not ended).
- 5.10 s after the reference collision, A's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 5.60, COLLISION 6.75 (+1.15 s); EGO_PATH_ENTRY 5.70 after critical TTC (+0.10 s) [local times; t_global: critical_ttc_start -1.15, ego_path_entry -1.05, collision +0.00]
- A's track_003#segment_1 (unidentified U3): CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s) [local times; t_global: critical_ttc_start -6.25, collision +0.00]
- A's track_003#segment_3 (unidentified U3): CRITICAL_TTC_START 6.85; EGO_PATH_ENTRY 6.85 together with critical TTC (+0.00 s) [local times; t_global: critical_ttc_start +0.10, ego_path_entry +0.10]
- A's track_006 (B): CRITICAL_TTC_START 5.10, COLLISION with B 6.75 (+1.65 s); EGO_PATH_ENTRY 6.40 after critical TTC (+1.30 s) [local times; t_global: critical_ttc_start -1.65, ego_path_entry -0.35, collision +0.00]
- A's track_007 (unidentified U9): EGO_PATH_ENTRY 8.35, no critical TTC [local times; t_global: ego_path_entry +1.60]
- B's track_001 (unidentified U1): CRITICAL_TTC_START 0.50, COLLISION 6.75 (+6.25 s) [local times; t_global: critical_ttc_start -6.25, collision +0.00]
- B's track_002 (A): cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 3.50 < CRITICAL_TTC_START 5.55 (+2.05 s) < COLLISION with A 6.75 (+1.20 s); EGO_PATH_ENTRY 7.90 after critical TTC (+2.35 s) [local times; t_global: cut_in -3.25, critical_ttc_start -1.20, ego_path_entry +1.15, collision +0.00]
- B's track_003 (unidentified U3): CUT_IN_FROM_RIGHT_START 9.65, no critical TTC after it; EGO_PATH_ENTRY 7.25 before critical TTC (-0.15 s) [local times; t_global: cut_in +2.90, critical_ttc_start +0.65, ego_path_entry +0.50]
- B's track_006 (unidentified U9): CUT_IN_FROM_RIGHT_START 10.90, no critical TTC after it; EGO_PATH_ENTRY 9.15, no critical TTC [local times; t_global: cut_in +4.15, ego_path_entry +2.40]
- B's track_007 (unidentified U11): EGO_PATH_ENTRY 6.95, no critical TTC [local times; t_global: ego_path_entry +0.20]
- B's track_008 (unidentified U12): EGO_PATH_ENTRY 7.35, no critical TTC [local times; t_global: ego_path_entry +0.60]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U1); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(A,U5); TRACK_APPEARED_RIGHT(B,A); TRACK_APPEARED_RIGHT(B,U3); TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(A,U4); CLOSING_START(B,A); CLOSING_START(B,U3)
- TRACK_APPEARED_FRONT(B,U7); CLOSING_START(B,U7)
- TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- CRITICAL_TTC_START(A,U3); CRITICAL_TTC_START(B,U1); TRACK_LOST(A,U5)
- TRACK_LOST(A,U2); TRACK_LOST(A,U4)
- TRACK_APPEARED_RIGHT(A,U9); CLOSING_START(A,U9)
- TRACK_APPEARED_RIGHT(B,U9); CLOSING_START(B,U9)
- TRACK_APPEARED_FRONT(A,U10); TRACK_APPEARED_RIGHT(B,U11); CLOSING_START(B,U11)
- TRACK_APPEARED_RIGHT(B,U12); CLOSING_START(A,B); CLOSING_START(B,U12); TRACK_LOST(A,U8)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); EGO_PATH_EXIT(A,U3)
- CLOSING_END(A,B); CLOSING_END(B,A); THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B)
- EGO_PATH_ENTRY(A,U3); CRITICAL_TTC_START(A,U3)
- CLOSING_END(B,U12); CLOSING_END(B,U9); EGO_PATH_ENTRY(B,U12)
- CRITICAL_TTC_END(B,U1); EGO_PATH_EXIT(A,U1); EGO_PATH_EXIT(A,U10); TRACK_LOST(B,U12)
- MOVING_END(B); STOP_START(B); TRACK_APPEARED_FRONT(A,U13); EGO_PATH_ENTRY(B,A)
- EGO_PATH_EXIT(A,B); MOVING_END(A); STOP_START(A)
- TRACK_APPEARED_RIGHT(A,U15); CLOSING_START(A,U15)
- EGO_PATH_EXIT(A,U3); TRACK_LOST(A,U14)
- EGO_PATH_EXIT(B,U9); TRACK_LOST(B,U11)

### States still active when observation ended

A:
- CLOSING of track_004, since A:e08 (t = 0.00 s); the track was lost at 3.60 s
- CRITICAL_TTC of track_003#segment_1, since A:e11 (t = 0.50 s); the track was lost at 4.75 s
- CRITICAL_TTC of track_001, since A:e21 (t = 5.60 s); the track was lost at 11.20 s
- BRAKE, since A:e33 (t = 6.80 s)
- STOP, since A:e43 (t = 7.95 s)
- EGO_PATH of track_006, since A:e44 (t = 8.05 s)
B:
- CLOSING of track_005, since B:e10 (t = 0.20 s); the track was lost at 3.10 s
- BRAKE, since B:e29 (t = 6.80 s)
- EGO_PATH of track_008, since B:e36 (t = 7.35 s); the track was lost at 7.55 s
- STOP, since B:e41 (t = 7.90 s)
- EGO_PATH of track_002, since B:e42 (t = 7.90 s)
- CUT_IN_FROM_RIGHT of track_003, since B:e48 (t = 9.65 s)
- CUT_IN_FROM_RIGHT of track_006, since B:e52 (t = 10.90 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e28 at 6.75 s (local): ego: MOVING, THROTTLE; track_001: CRITICAL_TTC, IN_EGO_PATH; track_003#segment_3: IN_EGO_PATH, CRITICAL_TTC?; track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_007: CLOSING; track_008: IN_EGO_PATH; track lost, states UNKNOWN: track_002, track_003#segment_1, track_003#segment_2, track_004, track_005
- B B:e25 at 6.75 s (local): ego: MOVING, THROTTLE; track_001: CRITICAL_TTC, IN_EGO_PATH; track_002: CLOSING, CRITICAL_TTC; track_003: CLOSING; track_006: CLOSING; track_007: CLOSING; track_008: CLOSING; track lost, states UNKNOWN: track_004, track_005

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_004 at 3.60 s (A:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003#segment_1 at 4.75 s (A:e16): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 11.20 s (A:e53): CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_005, track_002, track_003#segment_2, track_011, track_008
B:
- track_005 at 3.10 s (B:e12): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 7.55 s (B:e39): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_009, track_001, track_007

## Uncertainty and limitations

- A:track_001 stays anonymous (U1): not approaching before the contact: clearance 10.5 m -> 12.4 m over the last 1.0 s.
- A:track_002 stays anonymous (U2): lost 3.15 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 21.4 m -> 23.5 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_003#segment_1 stays anonymous (U3): lost 2.00 s before the matched collision (window 1.00 s); track speed disagrees with B's own speed: RMSE 1.82 m/s over 1.0 s (> 1.50).
- A:track_003#segment_2 stays anonymous (U8): not approaching before the contact: clearance 12.2 m -> 12.5 m over the last 1.0 s; track speed disagrees with B's own speed: RMSE 1.94 m/s over 1.4 s (> 1.50).
- A:track_003#segment_3 stays anonymous (U3): tracked for 0.50 s before the matched collision (needs 1.00 s); not approaching before the contact: clearance 12.2 m -> 12.2 m over the last 1.0 s; track speed disagrees with B's own speed: RMSE 2.04 m/s over 0.5 s (> 1.50).
- A:track_004 stays anonymous (U4): lost 3.15 s before the matched collision (window 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_005 stays anonymous (U5): lost 6.25 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 6.4 m -> 7.4 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_007 stays anonymous (U9): track speed disagrees with B's own speed: RMSE 4.06 m/s over 1.5 s (> 1.50).
- A:track_008 stays anonymous (U10): tracked for 0.85 s before the matched collision (needs 1.00 s); not approaching before the contact: clearance 28.0 m -> 29.3 m over the last 1.0 s.
- A:track_009 stays anonymous (U13): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.15 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_010 stays anonymous (U15): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.55 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_011 stays anonymous (U14): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.80 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous (U1): track speed disagrees with A's own speed: RMSE 1.93 m/s over 3.0 s (> 1.50).
- B:track_003 stays anonymous (U3): ambiguous: 2 persistent tracks of B are compatible with the contact (track_002, track_003).
- B:track_004 stays anonymous (U6): lost 1.55 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 12.3 m -> 16.2 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 1.70 m/s over 1.5 s (> 1.50).
- B:track_005 stays anonymous (U7): lost 3.65 s before the matched collision (window 1.00 s); speed not comparable with A's own speed before the collision.
- B:track_006 stays anonymous (U9): track speed disagrees with A's own speed: RMSE 2.05 m/s over 1.1 s (> 1.50).
- B:track_007 stays anonymous (U11): tracked for 0.85 s before the matched collision (needs 1.00 s).
- B:track_008 stays anonymous (U12): tracked for 0.55 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 1.96 m/s over 0.5 s (> 1.50).
- B:track_009 stays anonymous (U14): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.50 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_010 stays anonymous (U15): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 3.45 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
