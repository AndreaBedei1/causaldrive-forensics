# Reconstruction report - S24/run_0

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 48 | 117 | 12 | A:e26 @ 7.75 s |
| B | 11.95 s | 121 | 29 | 53 | 7 | B:e09 @ 7.75 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e26 | 7.75 | -7.75 | reported the reference collision collision_001 |
| B | ALIGNED | B:e09 | 7.75 | -7.75 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1897.7 vs 1897.7 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar trajectory checked against the candidate partner pose stream where observed

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.1 m -> 0.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 3.0 s<br>clearance at the contact 0.61 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006)<br>anonymous road user U1: A:track_001, B:track_005 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 1.80 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.0 m -> 7.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.17 m/s over 1.2 s<br>anonymous road user U2: A:track_002 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 4.10 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 30.7 m -> 28.9 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_003, A:track_009 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>lost 2.10 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 5.1 m -> 7.1 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.08 m/s over 0.9 s<br>anonymous road user U4: A:track_004 |
| A:track_005#segment_1 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.70 s before the matched collision<br>lost 6.45 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 14.8 m -> 12.8 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U8: A:track_005#segment_1 |
| A:track_005#segment_2 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 6.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.3 m -> 0.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.42 m/s over 3.0 s<br>clearance at the contact 0.00 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006)<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma, over 213 samples; 98% within 3 sigma) at B's own velocity (median difference 0.04 m/s) |
| A:track_006 | U7 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.35 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.5 m -> 2.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.21 m/s over 3.0 s<br>clearance at the contact 2.26 m<br>ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006)<br>anonymous road user U7: B:track_004, A:track_006 |
| A:track_007 | U6 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 18.3 m -> 18.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 18.20 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U6: B:track_002, A:track_007 |
| A:track_008 | B | ASSOCIATED | 1.00 | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 3.6 m -> 3.6 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 3.60 m<br>common frame: its returns lie on B's own footprint (median 0.00 m, 0.00 sigma, over 16 samples; 100% within 3 sigma) at B's own velocity (median difference 0.20 m/s) |
| A:track_009 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 20.7 m -> 20.7 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>clearance at the contact 20.66 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: A:track_003, B:track_003, A:track_009 |
| A:track_010 | U9 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U9: A:track_010 |
| A:track_011 | U10 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.20 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U10: A:track_011 |
| B:track_001 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 16.9 m -> 17.3 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.88 m/s over 3.0 s (> 1.50)<br>clearance at the contact 16.46 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U5: B:track_001 |
| B:track_002 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 13.5 m -> 13.5 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.89 m/s over 3.0 s (> 1.50)<br>clearance at the contact 13.47 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U6: B:track_002, A:track_007 |
| B:track_003 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 15.9 m -> 15.8 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.06 m/s over 3.0 s (> 1.50)<br>clearance at the contact 15.82 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U3: A:track_003, B:track_003, A:track_009 |
| B:track_004 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 1.4 m -> 1.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.96 m/s over 3.0 s (> 1.50)<br>clearance at the contact 1.37 m<br>anonymous road user U7: B:track_004, A:track_006 |
| B:track_005 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 7.75 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 1.5 m -> 1.5 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 1.92 m/s over 3.0 s (> 1.50)<br>clearance at the contact 1.46 m<br>anonymous road user U1: A:track_001, B:track_005 |
| B:track_006 | U11 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.65 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U11: B:track_006 |
| B:track_007 | U12 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1897.7 vs 1897.7 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.75 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U12: B:track_007 |

## Road users in the common frame

- A:track_005#segment_2 is B: its returns lie on B's own footprint (median 0.00 m over 213 samples, 98% within 3 sigma) at B's velocity.
- A:track_008 is B: its returns lie on B's own footprint (median 0.00 m over 16 samples, 100% within 3 sigma) at B's velocity.
- U1 (anonymous, -7.75 to 4.20 s): A:track_001, B:track_005 joined by same box A:track_001-B:track_005 (89% of 185 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U2 (anonymous, -7.75 to -1.80 s): A:track_002; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U3 (anonymous, -7.75 to 2.50 s): A:track_003, B:track_003, A:track_009 joined by same box A:track_003-B:track_003 (100% of 63 instants); same box A:track_009-B:track_003 (100% of 12 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U4 (anonymous, -7.75 to -2.10 s): A:track_004; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U5 (anonymous, -7.75 to 3.50 s): B:track_001; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.
- U6 (anonymous, -7.75 to 4.20 s): B:track_002, A:track_007 joined by same box A:track_007-B:track_002 (100% of 16 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U7 (anonymous, -7.75 to 4.20 s): B:track_004, A:track_006 joined by same box A:track_006-B:track_004 (96% of 173 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U8 (anonymous, -7.70 to -6.45 s): A:track_005#segment_1; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U9 (anonymous, 1.20 to 3.10 s): A:track_010; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U10 (anonymous, 1.20 to 3.10 s): A:track_011; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U11 (anonymous, 1.65 to 4.20 s): B:track_006; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U12 (anonymous, 1.75 to 4.20 s): B:track_007; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.

## Global graph

74 nodes, 181 edges; 26 merged node(s): g05 TRACK_APPEARED_FRONT(A,U3) from A:e03 + A:e18, g07 TRACK_APPEARED_LEFT(A,U2) from A:e04 + A:e20, g08 TRACK_APPEARED_LEFT(B,U3) from B:e05 + B:e22, g09 TRACK_APPEARED_LEFT(B,U5) from B:e04 + B:e29, g11 TRACK_APPEARED_RIGHT(A,U1) from A:e05 + A:e44, g12 TRACK_APPEARED_RIGHT(A,U4) from A:e06 + A:e19, g14 CLOSING_START(A,U1) from A:e07 + A:e22, g16 TRACK_APPEARED_LEFT(A,U8) from A:e09 + A:e14, g18 TRACK_APPEARED_LEFT(A,U7) from A:e11 + A:e43, g19 CLOSING_START(A,U7) from A:e12 + A:e29, g20 CRITICAL_TTC_START(B,U6) from B:e08 + B:e12, g23 TRACK_APPEARED_FRONT(A,B) from A:e15 + A:e24 + A:e35, g24 CLOSING_START(A,B) from A:e16 + A:e28, g25 CRITICAL_TTC_START(A,B) from A:e17 + A:e27, g29 CUT_IN_FROM_RIGHT_START(A,U1) from A:e21 + A:e30, g31 TRACK_APPEARED_FRONT(A,U6) from A:e23 + A:e34, g32 TRACK_APPEARED_LEFT(A,U3) from A:e25 + A:e36, g33 COLLISION(A,B) from A:e26 + B:e09, g48 TRACK_APPEARED_LEFT(A,U9) from A:e39 + A:e47, g49 TRACK_APPEARED_RIGHT(A,U10) from A:e40 + A:e48, g50 CLOSING_START(A,U10) from A:e42 + A:e46, g51 CLOSING_START(A,U9) from A:e41 + A:e45, g57 CLOSING_START(B,U11) from B:e16 + B:e24, g59 CLOSING_START(B,U12) from B:e18 + B:e25, g62 CRITICAL_TTC_START(B,U11) from B:e19 + B:e21, g63 CRITICAL_TTC_START(B,U12) from B:e20 + B:e23.

### Event sequence (global time)

- `-7.75` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U6); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U3); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_LEFT(B,U7); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(A,U3)
- `-7.70` TRACK_APPEARED_LEFT(A,U8); CLOSING_START(A,U8)
- `-7.35` TRACK_APPEARED_LEFT(A,U7); CLOSING_START(A,U7)
- `-7.25` CRITICAL_TTC_START(B,U6)
- `-6.90` EGO_PATH_EXIT(A,U7)
- `-6.45` TRACK_LOST(A,U8)
- `-6.40` TRACK_APPEARED_FRONT(A,B); CLOSING_START(A,B)
- `-5.90` CRITICAL_TTC_START(A,B)
- `-4.10` TRACK_LOST(A,U3)
- `-2.10` TRACK_LOST(A,U4)
- `-1.80` TRACK_LOST(A,U2)
- `-0.80` CUT_IN_FROM_RIGHT_START(A,U1)
- `-0.25` CLOSING_END(A,U1)
- `-0.05` TRACK_APPEARED_FRONT(A,U6); TRACK_APPEARED_LEFT(A,U3)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(A,U7); THROTTLE_END(B)
- `+0.05` CUT_IN_FROM_RIGHT_END(A,U1); THROTTLE_END(A); BRAKE_START(A); BRAKE_START(B)
- `+0.45` CRITICAL_TTC_START(A,B)
- `+0.50` CRITICAL_TTC_END(B,U6)
- `+0.70` TRACK_LOST(A,U3); TRACK_LOST(A,U6)
- `+1.15` MOVING_END(A); STOP_START(A)
- `+1.20` TRACK_APPEARED_LEFT(A,U9); TRACK_APPEARED_RIGHT(A,U10); CLOSING_START(A,U10); CLOSING_START(A,U9)
- `+1.25` MOVING_END(B); STOP_START(B)
- `+1.30` TRACK_LOST(A,U7)
- `+1.45` TRACK_LOST(A,U1)
- `+1.65` TRACK_APPEARED_LEFT(B,U11); CLOSING_START(B,U11)
- `+1.75` TRACK_APPEARED_RIGHT(B,U12); CLOSING_START(B,U12)
- `+2.10` CLOSING_END(A,U9)
- `+2.15` CLOSING_END(A,U10); CRITICAL_TTC_START(B,U11)
- `+2.25` CRITICAL_TTC_START(B,U12)
- `+2.50` CRITICAL_TTC_END(B,U11); TRACK_LOST(B,U3)
- `+2.55` CRITICAL_TTC_END(B,U12); CLOSING_END(B,U11)
- `+2.60` CLOSING_END(B,U12)
- `+2.90` EGO_PATH_EXIT(B,U6); CUT_IN_FROM_RIGHT_START(B,U1)
- `+3.10` TRACK_LOST(A,U10); TRACK_LOST(A,U9)
- `+3.25` EGO_PATH_ENTRY(B,U1)
- `+3.50` TRACK_LOST(B,U5)

### What happened, in plain language

- 7.75 s before the reference collision, A started moving (already the case when first observed).
- 7.75 s before the reference collision, B started moving (already the case when first observed).
- 7.75 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared in front of it.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared on its left.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U7, which appeared on its left.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its right.
- 7.75 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its right.
- 7.75 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.75 s before the reference collision, A observed anonymous road user U1 start closing in (already the case when first observed).
- 7.75 s before the reference collision, A observed anonymous road user U3 start closing in (already the case when first observed).
- 7.70 s before the reference collision, A's radar started tracking anonymous road user U8, which appeared on its left.
- 7.70 s before the reference collision, A observed anonymous road user U8 start closing in (already the case when first observed).
- 7.35 s before the reference collision, A's radar started tracking anonymous road user U7, which appeared on its left.
- 7.35 s before the reference collision, A observed anonymous road user U7 start closing in (already the case when first observed).
- 7.25 s before the reference collision, B's time-to-contact with anonymous road user U6 became critical.
- 6.90 s before the reference collision, A observed anonymous road user U7 leave its forward path corridor.
- 6.45 s before the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).
- 6.40 s before the reference collision, A's radar started tracking B, which appeared in front of it.
- 6.40 s before the reference collision, A observed B start closing in (already the case when first observed).
- 5.90 s before the reference collision, A's time-to-contact with B became critical.
- 4.10 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.10 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 1.80 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 0.80 s before the reference collision, A observed anonymous road user U1 cutting in from the right.
- 0.25 s before the reference collision, A observed anonymous road user U1 stop closing in.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U6, which appeared in front of it.
- 0.05 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared on its left.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 1898, B: 1898 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, A observed B stop closing in.
- At the reference collision, A observed anonymous road user U7 stop closing in.
- At the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A observed anonymous road user U1's cut-in from the right settle.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.45 s after the reference collision, A's time-to-contact with B became critical.
- 0.50 s after the reference collision, B's time-to-contact with anonymous road user U6 stopped being critical.
- 0.70 s after the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 1.15 s after the reference collision, A stopped moving.
- 1.15 s after the reference collision, A came to a stop.
- 1.20 s after the reference collision, A's radar started tracking anonymous road user U9, which appeared on its left.
- 1.20 s after the reference collision, A's radar started tracking anonymous road user U10, which appeared on its right.
- 1.20 s after the reference collision, A observed anonymous road user U10 start closing in (already the case when first observed).
- 1.20 s after the reference collision, A observed anonymous road user U9 start closing in (already the case when first observed).
- 1.25 s after the reference collision, B stopped moving.
- 1.25 s after the reference collision, B came to a stop.
- 1.30 s after the reference collision, A's radar lost anonymous road user U7 (its states are UNKNOWN from then on, not ended).
- 1.45 s after the reference collision, A's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 1.65 s after the reference collision, B's radar started tracking anonymous road user U11, which appeared on its left.
- 1.65 s after the reference collision, B observed anonymous road user U11 start closing in (already the case when first observed).
- 1.75 s after the reference collision, B's radar started tracking anonymous road user U12, which appeared on its right.
- 1.75 s after the reference collision, B observed anonymous road user U12 start closing in (already the case when first observed).
- 2.10 s after the reference collision, A observed anonymous road user U9 stop closing in.
- 2.15 s after the reference collision, A observed anonymous road user U10 stop closing in.
- 2.15 s after the reference collision, B's time-to-contact with anonymous road user U11 became critical.
- 2.25 s after the reference collision, B's time-to-contact with anonymous road user U12 became critical.
- 2.50 s after the reference collision, B's time-to-contact with anonymous road user U11 stopped being critical.
- 2.50 s after the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 2.55 s after the reference collision, B's time-to-contact with anonymous road user U12 stopped being critical.
- 2.55 s after the reference collision, B observed anonymous road user U11 stop closing in.
- 2.60 s after the reference collision, B observed anonymous road user U12 stop closing in.
- 2.90 s after the reference collision, B observed anonymous road user U6 leave its forward path corridor.
- 2.90 s after the reference collision, B observed anonymous road user U1 cutting in from the right.
- 3.10 s after the reference collision, A's radar lost anonymous road user U10 (its states are UNKNOWN from then on, not ended).
- 3.10 s after the reference collision, A's radar lost anonymous road user U9 (its states are UNKNOWN from then on, not ended).
- 3.25 s after the reference collision, B observed anonymous road user U1 enter its forward path corridor.
- 3.50 s after the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified U1): CUT_IN_FROM_RIGHT_START 6.95, no critical TTC after it [local times; t_global: cut_in -0.80, collision +0.00]
- A's track_005#segment_2 (B): CRITICAL_TTC_START 1.85, COLLISION with B 7.75 (+5.90 s) [local times; t_global: critical_ttc_start -5.90, collision +0.00]
- A's track_008 (B): CRITICAL_TTC_START 8.20 [local times; t_global: critical_ttc_start +0.45]
- B's track_002 (unidentified U6): CRITICAL_TTC_START 0.50, COLLISION 7.75 (+7.25 s) [local times; t_global: critical_ttc_start -7.25, collision +0.00]
- B's track_005 (unidentified U1): CUT_IN_FROM_RIGHT_START 10.65, no critical TTC after it; EGO_PATH_ENTRY 11.00, no critical TTC [local times; t_global: cut_in +2.90, ego_path_entry +3.25]
- B's track_006 (unidentified U11): CRITICAL_TTC_START 9.90 [local times; t_global: critical_ttc_start +2.15]
- B's track_007 (unidentified U12): CRITICAL_TTC_START 10.00 [local times; t_global: critical_ttc_start +2.25]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U6); TRACK_APPEARED_LEFT(A,U2); TRACK_APPEARED_LEFT(B,U3); TRACK_APPEARED_LEFT(B,U5); TRACK_APPEARED_LEFT(B,U7); TRACK_APPEARED_RIGHT(A,U1); TRACK_APPEARED_RIGHT(A,U4); TRACK_APPEARED_RIGHT(B,U1); CLOSING_START(A,U1); CLOSING_START(A,U3)
- TRACK_APPEARED_LEFT(A,U8); CLOSING_START(A,U8)
- TRACK_APPEARED_LEFT(A,U7); CLOSING_START(A,U7)
- TRACK_APPEARED_FRONT(A,B); CLOSING_START(A,B)
- TRACK_APPEARED_FRONT(A,U6); TRACK_APPEARED_LEFT(A,U3)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(A,U7); THROTTLE_END(B)
- CUT_IN_FROM_RIGHT_END(A,U1); THROTTLE_END(A); BRAKE_START(A); BRAKE_START(B)
- TRACK_LOST(A,U3); TRACK_LOST(A,U6)
- MOVING_END(A); STOP_START(A)
- TRACK_APPEARED_LEFT(A,U9); TRACK_APPEARED_RIGHT(A,U10); CLOSING_START(A,U10); CLOSING_START(A,U9)
- MOVING_END(B); STOP_START(B)
- TRACK_APPEARED_LEFT(B,U11); CLOSING_START(B,U11)
- TRACK_APPEARED_RIGHT(B,U12); CLOSING_START(B,U12)
- CLOSING_END(A,U10); CRITICAL_TTC_START(B,U11)
- CRITICAL_TTC_END(B,U11); TRACK_LOST(B,U3)
- CRITICAL_TTC_END(B,U12); CLOSING_END(B,U11)
- EGO_PATH_EXIT(B,U6); CUT_IN_FROM_RIGHT_START(B,U1)
- TRACK_LOST(A,U10); TRACK_LOST(A,U9)

### States still active when observation ended

A:
- CLOSING of track_003, since A:e08 (t = 0.00 s); the track was lost at 3.65 s
- CLOSING of track_005#segment_1, since A:e10 (t = 0.05 s); the track was lost at 1.30 s
- BRAKE, since A:e32 (t = 7.80 s)
- CRITICAL_TTC of track_008, since A:e33 (t = 8.20 s); the track was lost at 8.45 s
- STOP, since A:e38 (t = 8.90 s)
B:
- BRAKE, since B:e11 (t = 7.80 s)
- STOP, since B:e14 (t = 9.00 s)
- CUT_IN_FROM_RIGHT of track_005, since B:e27 (t = 10.65 s)
- EGO_PATH of track_005, since B:e28 (t = 11.00 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e26 at 7.75 s (local): ego: MOVING, THROTTLE; track_001: CUT_IN_FROM_RIGHT; track_005#segment_2: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_006: CLOSING; track_007: IN_EGO_PATH, CRITICAL_TTC?; track_008: IN_EGO_PATH, CRITICAL_TTC?; track_009: CRITICAL_TTC?; track lost, states UNKNOWN: track_002, track_003, track_004, track_005#segment_1
- B B:e09 at 7.75 s (local): ego: MOVING, THROTTLE; track_001: no active state; track_002: CRITICAL_TTC, IN_EGO_PATH; track_003: no active state; track_004: no active state; track_005: no active state

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_005#segment_1 at 1.30 s (A:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 3.65 s (A:e18): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 8.45 s (A:e34): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 8.45 s (A:e35): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_002, track_009, track_006, track_001, track_010, track_011
B:
- lost with no state active: track_003, track_001

## Uncertainty and limitations

- A:track_001 stays anonymous (U1): ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006).
- A:track_002 stays anonymous (U2): lost 1.80 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 5.0 m -> 7.2 m over the last 1.0 s.
- A:track_003 stays anonymous (U3): lost 4.10 s before the matched collision (window 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_004 stays anonymous (U4): lost 2.10 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 5.1 m -> 7.1 m over the last 1.0 s.
- A:track_005#segment_1 stays anonymous (U8): lost 6.45 s before the matched collision (window 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_006 stays anonymous (U7): ambiguous: 3 persistent tracks of A are compatible with the contact (track_001, track_005#segment_2, track_006).
- A:track_007 stays anonymous (U6): tracked for 0.05 s before the matched collision (needs 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_009 stays anonymous (U3): tracked for 0.05 s before the matched collision (needs 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_010 stays anonymous (U9): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.20 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_011 stays anonymous (U10): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.20 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous (U5): not approaching before the contact: clearance 16.9 m -> 17.3 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 1.88 m/s over 3.0 s (> 1.50).
- B:track_002 stays anonymous (U6): not approaching before the contact: clearance 13.5 m -> 13.5 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 1.89 m/s over 3.0 s (> 1.50).
- B:track_003 stays anonymous (U3): track speed disagrees with A's own speed: RMSE 2.06 m/s over 3.0 s (> 1.50).
- B:track_004 stays anonymous (U7): track speed disagrees with A's own speed: RMSE 1.96 m/s over 3.0 s (> 1.50).
- B:track_005 stays anonymous (U1): not approaching before the contact: clearance 1.5 m -> 1.5 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 1.92 m/s over 3.0 s (> 1.50).
- B:track_006 stays anonymous (U11): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.65 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- B:track_007 stays anonymous (U12): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.75 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
