# Reconstruction report - S17/run_0_occlusion_reappearance

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> road users in the common frame of the recorders' own pose streams -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 43 | 86 | 9 | A:e25 @ 7.30 s |
| B | 11.95 s | 121 | 40 | 76 | 8 | B:e24 @ 7.30 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e25 | 7.30 | -7.30 | reported the reference collision collision_001 |
| B | ALIGNED | B:e24 | 7.30 | -7.30 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 389.26 vs 389.26 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance; the two bodies touch at their reports (0.00 m apart, tolerance 1.0 m); independent relative impulse std 0.100; combined z 0.000 (gate 3.0); engineering assumption; pre-contact radar view of each recorder checked against the candidate partner's own speed: not contradicted

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | U1 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.2 m -> 10.3 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 4.62 m/s for reference)<br>clearance at the contact 7.17 m (beyond 3.50 m: confidence factor 0.47)<br>anonymous road user U1: A:track_001, B:track_003 |
| A:track_002 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 2.50 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 20.4 m -> 20.5 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 2.02 m/s for reference)<br>retrospective: identity resolved from later evidence at -0.85 s (entity seen by several observers), carried back 1.40 s with the motion model; posterior 0.992 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_007 |
| A:track_003 | U3 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 4.00 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 37.5 m -> 37.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_004 |
| A:track_004 | U4 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.55 s before it (window 1.00 s)<br>not approaching before the contact: clearance 15.9 m -> 18.0 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.33 m/s for reference)<br>clearance at the contact 17.35 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U4: A:track_004 |
| A:track_005 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.15 s before the matched collision<br>lost 2.75 s before the matched collision (window 1.00 s)<br>approaching before the contact: clearance 19.2 m -> 17.9 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.30 m/s for reference)<br>anonymous road user U5: B:track_001, A:track_005, A:track_007 |
| A:track_006 | B | ASSOCIATED | 0.88 | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 6.40 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.9 m -> 0.8 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.76 m/s for reference)<br>clearance at the contact 0.84 m<br>the only track of A compatible with the contact |
| A:track_007 | U5 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.95 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 14.0 m -> 11.8 m over the last 1.0 s<br>track motion compatible with B's own speed in the observed direction (3 sigma; full-speed RMSE 0.27 m/s for reference)<br>clearance at the contact 11.75 m (beyond 3.50 m: confidence factor 0.02)<br>anonymous road user U5: B:track_001, A:track_005, A:track_007 |
| A:track_008 | U2 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.85 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 20.6 m -> 20.9 m over the last 1.0 s<br>track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 1.97 m/s for reference)<br>clearance at the contact 20.60 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_007 |
| A:track_009 | U8 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.15 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>anonymous road user U8: A:track_009 |
| B:track_001 | U5 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 13.5 m -> 13.8 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.90 m/s for reference)<br>clearance at the contact 13.42 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U5: B:track_001, A:track_005, A:track_007 |
| B:track_002 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>lost 2.25 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 17.4 m -> 19.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.15 m/s for reference)<br>retrospective: identity resolved from later evidence at -0.85 s (entity seen by several observers), carried back 1.40 s with the motion model; posterior 0.992 against 1 candidate(s) and a new road user; observation times unchanged<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_007 |
| B:track_003 | U1 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 7.9 m -> 12.8 m over the last 1.0 s<br>track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 2.44 m/s for reference)<br>clearance at the contact 7.85 m (beyond 3.50 m: confidence factor 0.35)<br>anonymous road user U1: A:track_001, B:track_003 |
| B:track_004 | U3 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 7.00 s before the matched collision<br>lost 3.90 s before the matched collision (window 1.00 s)<br>not approaching before the contact: clearance 30.4 m -> 32.4 m over the last 1.0 s<br>speed not comparable with A's own speed before the collision<br>anonymous road user U3: A:track_003, B:track_004 |
| B:track_005 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 4.30 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 2.5 m -> 0.0 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.52 m/s for reference)<br>clearance at the contact 0.00 m<br>the only compatible track of B touching it at the contact (clearance 0.00 m; track_006 at 11.60 m) |
| B:track_006 | U6 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 2.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 13.7 m -> 11.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.28 m/s for reference)<br>clearance at the contact 11.60 m (beyond 3.50 m: confidence factor 0.03)<br>ambiguous: 2 persistent tracks of B are compatible with the contact (track_005, track_006)<br>anonymous road user U6: B:track_006 |
| B:track_007 | U2 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.40 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 23.0 m -> 23.6 m over the last 1.0 s<br>track motion compatible with A's own speed in the observed direction (3 sigma; full-speed RMSE 0.27 m/s for reference)<br>clearance at the contact 22.99 m (beyond 3.50 m: confidence factor 0.00)<br>anonymous road user U2: A:track_002, B:track_002, A:track_008, B:track_007 |
| B:track_008 | U7 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 389.26 vs 389.26 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 1.00 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision<br>anonymous road user U7: B:track_008 |

## Road users in the common frame

- U1 (anonymous, -7.30 to 4.65 s): A:track_001, B:track_003 joined by same box A:track_001-B:track_003 (86% of 157 instants); footprint 4.94 x 1.90 m (fitted/prior); fusion box_fit+covariance_intersection.
- U2 (anonymous, -7.30 to 4.65 s): A:track_002, B:track_002, A:track_008, B:track_007 joined by same box A:track_002-B:track_002 (100% of 91 instants); same box A:track_008-B:track_007 (100% of 10 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U3 (anonymous, -7.30 to -3.90 s): A:track_003, B:track_004 joined by same box A:track_003-B:track_004 (100% of 46 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U4 (anonymous, -7.30 to -0.55 s): A:track_004; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U5 (anonymous, -7.30 to 4.65 s): B:track_001, A:track_005, A:track_007 joined by same box A:track_005-B:track_001 (100% of 80 instants); same box A:track_007-B:track_001 (100% of 31 instants); footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U6 (anonymous, -2.15 to 0.10 s): B:track_006; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U7 (anonymous, 1.00 to 4.65 s): B:track_008; footprint 4.60 x 1.90 m (prior/prior); fusion box_fit+covariance_intersection.
- U8 (anonymous, 1.15 to 4.60 s): A:track_009; footprint 4.60 x 1.90 m (prior/prior); fusion covariance_intersection.

## Global graph

82 nodes, 200 edges; 26 merged node(s): g05 TRACK_APPEARED_FRONT(A,U2) from A:e03 + A:e14, g06 TRACK_APPEARED_FRONT(A,U3) from A:e04 + A:e11, g07 TRACK_APPEARED_FRONT(B,U5) from B:e03 + B:e34, g09 TRACK_APPEARED_LEFT(A,U4) from A:e06 + A:e22, g10 TRACK_APPEARED_RIGHT(B,U1) from B:e05 + B:e33, g11 TRACK_APPEARED_RIGHT(B,U2) from B:e04 + B:e12, g12 TRACK_APPEARED_LEFT(A,U5) from A:e07 + A:e13, g14 TRACK_APPEARED_RIGHT(B,U3) from B:e06 + B:e10, g15 CRITICAL_TTC_START(B,U5) from B:e07 + B:e19, g17 CLOSING_START(A,B) from A:e10 + A:e12, g19 CLOSING_START(B,A) from B:e09 + B:e11, g27 TRACK_APPEARED_RIGHT(B,U6) from B:e13 + B:e29, g29 CRITICAL_TTC_START(A,U1) from A:e15 + A:e33, g30 CLOSING_START(B,A) from B:e15 + B:e23, g31 CLOSING_START(A,B) from A:e16 + A:e27, g32 CRITICAL_TTC_START(A,B) from A:e17 + A:e26, g33 CRITICAL_TTC_START(B,A) from B:e17 + B:e25, g35 EGO_PATH_ENTRY(A,U1) from A:e18 + A:e34, g40 CLOSING_START(A,U5) from A:e20 + A:e32, g43 CRITICAL_TTC_START(A,U5) from A:e23 + A:e35, g44 TRACK_APPEARED_FRONT(B,U2) from B:e21 + B:e31, g45 CUT_IN_FROM_LEFT_START(A,U5) from A:e24 + A:e42, g48 COLLISION(A,B) from A:e25 + B:e24, g58 EGO_PATH_ENTRY(A,U5) from A:e31 + A:e36, g77 CLOSING_START(B,U7) from B:e39 + B:e40, g78 TRACK_APPEARED_RIGHT(A,U8) from A:e40 + A:e43.

### Event sequence (global time)

- `-7.30` MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U5); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U4); TRACK_APPEARED_RIGHT(B,U1); TRACK_APPEARED_RIGHT(B,U2)
- `-7.15` TRACK_APPEARED_LEFT(A,U5); CLOSING_START(A,U5)
- `-7.00` TRACK_APPEARED_RIGHT(B,U3)
- `-6.80` CRITICAL_TTC_START(B,U5)
- `-6.40` TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-4.30` TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- `-4.00` TRACK_LOST(A,U3)
- `-3.90` TRACK_LOST(B,U3)
- `-3.75` CLOSING_END(B,A)
- `-3.15` CLOSING_END(A,B)
- `-2.75` TRACK_LOST(A,U5)
- `-2.50` TRACK_LOST(A,U2)
- `-2.25` TRACK_LOST(B,U2)
- `-2.15` TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(B,U6)
- `-1.95` CRITICAL_TTC_START(A,U1)
- `-1.85` CLOSING_START(B,A)
- `-1.80` CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- `-1.75` CRITICAL_TTC_START(B,A); CRITICAL_TTC_START(B,U1)
- `-1.55` EGO_PATH_ENTRY(A,U1)
- `-1.45` EGO_PATH_ENTRY(B,U1)
- `-1.10` CRITICAL_TTC_END(B,U5); EGO_PATH_EXIT(B,U5)
- `-0.95` TRACK_APPEARED_LEFT(A,U5); CLOSING_START(A,U5)
- `-0.85` TRACK_APPEARED_RIGHT(A,U2)
- `-0.55` TRACK_LOST(A,U4)
- `-0.45` CRITICAL_TTC_START(A,U5)
- `-0.40` TRACK_APPEARED_FRONT(B,U2); CUT_IN_FROM_LEFT_START(A,U5)
- `-0.35` EGO_PATH_ENTRY(B,A)
- `-0.10` CLOSING_END(B,A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B)
- `+0.05` THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B)
- `+0.10` TURN_LEFT_START(A); EGO_PATH_ENTRY(A,U5); TRACK_LOST(B,U6)
- `+0.20` CLOSING_END(A,U5); EGO_PATH_EXIT(B,U2)
- `+0.30` TRACK_LOST(B,U2)
- `+0.35` CRITICAL_TTC_END(A,U1); EGO_PATH_EXIT(A,U1); EGO_PATH_ENTRY(B,U5)
- `+0.50` TRACK_LOST(B,U1)
- `+0.55` CRITICAL_TTC_END(A,U5)
- `+0.65` EGO_PATH_EXIT(A,U5)
- `+0.70` TRACK_LOST(B,U5)
- `+0.95` TURN_LEFT_END(A); TURN_LEFT_END(B); MOVING_END(B); STOP_START(B)
- `+1.00` MOVING_END(A); STOP_START(A); TRACK_APPEARED_RIGHT(B,U7); CLOSING_START(B,U7)
- `+1.15` TRACK_APPEARED_RIGHT(A,U8)
- `+1.40` EGO_PATH_ENTRY(A,B)
- `+1.90` CLOSING_END(B,U7)
- `+3.55` CUT_IN_FROM_LEFT_END(A,U5)
- `+4.60` TRACK_LOST(A,U8)

### What happened, in plain language

- 7.30 s before the reference collision, A started moving (already the case when first observed).
- 7.30 s before the reference collision, B started moving (already the case when first observed).
- 7.30 s before the reference collision, A pressed the accelerator (already the case when first observed).
- 7.30 s before the reference collision, B pressed the accelerator (already the case when first observed).
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared in front of it.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U3, which appeared in front of it.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U5, which appeared in front of it.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U1, which appeared on its left.
- 7.30 s before the reference collision, A's radar started tracking anonymous road user U4, which appeared on its left.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U1, which appeared on its right.
- 7.30 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared on its right.
- 7.15 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared on its left.
- 7.15 s before the reference collision, A observed anonymous road user U5 start closing in (already the case when first observed).
- 7.00 s before the reference collision, B's radar started tracking anonymous road user U3, which appeared on its right.
- 6.80 s before the reference collision, B's time-to-contact with anonymous road user U5 became critical.
- 6.40 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 6.40 s before the reference collision, A observed B start closing in (already the case when first observed).
- 4.30 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 4.30 s before the reference collision, B observed A start closing in (already the case when first observed).
- 4.00 s before the reference collision, A's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.90 s before the reference collision, B's radar lost anonymous road user U3 (its states are UNKNOWN from then on, not ended).
- 3.75 s before the reference collision, B observed A stop closing in.
- 3.15 s before the reference collision, A observed B stop closing in.
- 2.75 s before the reference collision, A's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 2.50 s before the reference collision, A's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.25 s before the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 2.15 s before the reference collision, B's radar started tracking anonymous road user U6, which appeared on its right.
- 2.15 s before the reference collision, B observed anonymous road user U6 start closing in (already the case when first observed).
- 1.95 s before the reference collision, A's time-to-contact with anonymous road user U1 became critical.
- 1.85 s before the reference collision, B observed A start closing in.
- 1.80 s before the reference collision, A observed B start closing in.
- 1.80 s before the reference collision, A's time-to-contact with B became critical.
- 1.75 s before the reference collision, B's time-to-contact with A became critical.
- 1.75 s before the reference collision, B's time-to-contact with anonymous road user U1 became critical.
- 1.55 s before the reference collision, A observed anonymous road user U1 enter its forward path corridor.
- 1.45 s before the reference collision, B observed anonymous road user U1 enter its forward path corridor.
- 1.10 s before the reference collision, B's time-to-contact with anonymous road user U5 stopped being critical.
- 1.10 s before the reference collision, B observed anonymous road user U5 leave its forward path corridor.
- 0.95 s before the reference collision, A's radar started tracking anonymous road user U5, which appeared on its left.
- 0.95 s before the reference collision, A observed anonymous road user U5 start closing in (already the case when first observed).
- 0.85 s before the reference collision, A's radar started tracking anonymous road user U2, which appeared on its right.
- 0.55 s before the reference collision, A's radar lost anonymous road user U4 (its states are UNKNOWN from then on, not ended).
- 0.45 s before the reference collision, A's time-to-contact with anonymous road user U5 became critical.
- 0.40 s before the reference collision, B's radar started tracking anonymous road user U2, which appeared in front of it.
- 0.40 s before the reference collision, A observed anonymous road user U5 cutting in from the left.
- 0.35 s before the reference collision, B observed A enter its forward path corridor.
- 0.10 s before the reference collision, B observed A stop closing in.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 389, B: 389 N*s).
- At the reference collision, A's time-to-contact with B stopped being critical.
- At the reference collision, B's time-to-contact with A stopped being critical.
- At the reference collision, A observed B stop closing in.
- 0.05 s after the reference collision, A released the accelerator.
- 0.05 s after the reference collision, B released the accelerator.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B started turning left.
- 0.10 s after the reference collision, A started turning left.
- 0.10 s after the reference collision, A observed anonymous road user U5 enter its forward path corridor.
- 0.10 s after the reference collision, B's radar lost anonymous road user U6 (its states are UNKNOWN from then on, not ended).
- 0.20 s after the reference collision, A observed anonymous road user U5 stop closing in.
- 0.20 s after the reference collision, B observed anonymous road user U2 leave its forward path corridor.
- 0.30 s after the reference collision, B's radar lost anonymous road user U2 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the reference collision, A's time-to-contact with anonymous road user U1 stopped being critical.
- 0.35 s after the reference collision, A observed anonymous road user U1 leave its forward path corridor.
- 0.35 s after the reference collision, B observed anonymous road user U5 enter its forward path corridor.
- 0.50 s after the reference collision, B's radar lost anonymous road user U1 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the reference collision, A's time-to-contact with anonymous road user U5 stopped being critical.
- 0.65 s after the reference collision, A observed anonymous road user U5 leave its forward path corridor.
- 0.70 s after the reference collision, B's radar lost anonymous road user U5 (its states are UNKNOWN from then on, not ended).
- 0.95 s after the reference collision, A stopped turning left.
- 0.95 s after the reference collision, B stopped turning left.
- 0.95 s after the reference collision, B stopped moving.
- 0.95 s after the reference collision, B came to a stop.
- 1.00 s after the reference collision, A stopped moving.
- 1.00 s after the reference collision, A came to a stop.
- 1.00 s after the reference collision, B's radar started tracking anonymous road user U7, which appeared on its right.
- 1.00 s after the reference collision, B observed anonymous road user U7 start closing in (already the case when first observed).
- 1.15 s after the reference collision, A's radar started tracking anonymous road user U8, which appeared on its right.
- 1.40 s after the reference collision, A observed B enter its forward path corridor.
- 1.90 s after the reference collision, B observed anonymous road user U7 stop closing in.
- 3.55 s after the reference collision, A observed anonymous road user U5's cut-in from the left settle.
- 4.60 s after the reference collision, A's radar lost anonymous road user U8 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified U1): CRITICAL_TTC_START 5.35, COLLISION 7.30 (+1.95 s); EGO_PATH_ENTRY 5.75 after critical TTC (+0.40 s) [local times; t_global: critical_ttc_start -1.95, ego_path_entry -1.55, collision +0.00]
- A's track_006 (B): CRITICAL_TTC_START 5.50, COLLISION with B 7.30 (+1.80 s); EGO_PATH_ENTRY 8.70 after critical TTC (+3.20 s) [local times; t_global: critical_ttc_start -1.80, ego_path_entry +1.40, collision +0.00]
- A's track_007 (unidentified U5): critical TTC already active before the cut-in: CRITICAL_TTC_START 6.85 <= CUT_IN_FROM_LEFT_START 6.90 (+0.05 s); EGO_PATH_ENTRY 7.40 after critical TTC (+0.55 s) [local times; t_global: cut_in -0.40, critical_ttc_start -0.45, ego_path_entry +0.10, collision +0.00]
- B's track_001 (unidentified U5): CRITICAL_TTC_START 0.50, COLLISION 7.30 (+6.80 s); EGO_PATH_ENTRY 7.65 after critical TTC (+7.15 s) [local times; t_global: critical_ttc_start -6.80, ego_path_entry +0.35, collision +0.00]
- B's track_003 (unidentified U1): CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 5.85 after critical TTC (+0.30 s) [local times; t_global: critical_ttc_start -1.75, ego_path_entry -1.45, collision +0.00]
- B's track_005 (A): CRITICAL_TTC_START 5.55, COLLISION with A 7.30 (+1.75 s); EGO_PATH_ENTRY 6.95 after critical TTC (+1.40 s) [local times; t_global: critical_ttc_start -1.75, ego_path_entry -0.35, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); THROTTLE_START(A); THROTTLE_START(B); TRACK_APPEARED_FRONT(A,U2); TRACK_APPEARED_FRONT(A,U3); TRACK_APPEARED_FRONT(B,U5); TRACK_APPEARED_LEFT(A,U1); TRACK_APPEARED_LEFT(A,U4); TRACK_APPEARED_RIGHT(B,U1); TRACK_APPEARED_RIGHT(B,U2)
- TRACK_APPEARED_LEFT(A,U5); CLOSING_START(A,U5)
- TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- TRACK_APPEARED_RIGHT(B,U6); CLOSING_START(B,U6)
- CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- CRITICAL_TTC_START(B,A); CRITICAL_TTC_START(B,U1)
- CRITICAL_TTC_END(B,U5); EGO_PATH_EXIT(B,U5)
- TRACK_APPEARED_LEFT(A,U5); CLOSING_START(A,U5)
- TRACK_APPEARED_FRONT(B,U2); CUT_IN_FROM_LEFT_START(A,U5)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CRITICAL_TTC_END(B,A); CLOSING_END(A,B)
- THROTTLE_END(A); THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B)
- TURN_LEFT_START(A); EGO_PATH_ENTRY(A,U5); TRACK_LOST(B,U6)
- CLOSING_END(A,U5); EGO_PATH_EXIT(B,U2)
- CRITICAL_TTC_END(A,U1); EGO_PATH_EXIT(A,U1); EGO_PATH_ENTRY(B,U5)
- TURN_LEFT_END(A); TURN_LEFT_END(B); MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A); TRACK_APPEARED_RIGHT(B,U7); CLOSING_START(B,U7)

### States still active when observation ended

A:
- CLOSING of track_005, since A:e08 (t = 0.15 s); the track was lost at 4.55 s
- BRAKE, since A:e29 (t = 7.35 s)
- STOP, since A:e39 (t = 8.30 s)
- EGO_PATH of track_006, since A:e41 (t = 8.70 s)
B:
- CLOSING of track_006, since B:e14 (t = 5.15 s); the track was lost at 7.40 s
- CRITICAL_TTC of track_003, since B:e16 (t = 5.55 s); the track was lost at 7.80 s
- EGO_PATH of track_003, since B:e18 (t = 5.85 s); the track was lost at 7.80 s
- EGO_PATH of track_005, since B:e22 (t = 6.95 s)
- BRAKE, since B:e27 (t = 7.35 s)
- EGO_PATH of track_001, since B:e32 (t = 7.65 s); the track was lost at 8.00 s
- STOP, since B:e37 (t = 8.25 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e25 at 7.30 s (local): ego: MOVING, THROTTLE; track_001: CRITICAL_TTC, IN_EGO_PATH; track_006: CLOSING, CRITICAL_TTC; track_007: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT; track_008: no active state; track lost, states UNKNOWN: track_002, track_003, track_004, track_005
- B B:e24 at 7.30 s (local): ego: MOVING, THROTTLE; track_001: no active state; track_003: CRITICAL_TTC, IN_EGO_PATH; track_005: CRITICAL_TTC, IN_EGO_PATH; track_006: CLOSING; track_007: IN_EGO_PATH, CRITICAL_TTC?; track lost, states UNKNOWN: track_002, track_004

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_005 at 4.55 s (A:e13): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 4.80 s (A:e14): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_004, track_009
B:
- track_006 at 7.40 s (B:e29): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 7.80 s (B:e33): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 8.00 s (B:e34): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_002, track_007

## Uncertainty and limitations

- A:track_001 stays anonymous (U1): not approaching before the contact: clearance 7.2 m -> 10.3 m over the last 1.0 s; track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 4.62 m/s for reference).
- A:track_002 stays anonymous (U2): lost 2.50 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 20.4 m -> 20.5 m over the last 1.0 s; track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 2.02 m/s for reference).
- A:track_003 stays anonymous (U3): lost 4.00 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 37.5 m -> 37.5 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_004 stays anonymous (U4): not approaching before the contact: clearance 15.9 m -> 18.0 m over the last 1.0 s.
- A:track_005 stays anonymous (U5): lost 2.75 s before the matched collision (window 1.00 s).
- A:track_007 stays anonymous (U5): tracked for 0.95 s before the matched collision (needs 1.00 s).
- A:track_008 stays anonymous (U2): tracked for 0.85 s before the matched collision (needs 1.00 s); not approaching before the contact: clearance 20.6 m -> 20.9 m over the last 1.0 s; track motion contradicts B's own speed in the observed direction (3 sigma; full-speed RMSE 1.97 m/s for reference).
- A:track_009 stays anonymous (U8): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.15 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous (U5): not approaching before the contact: clearance 13.5 m -> 13.8 m over the last 1.0 s; track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 1.90 m/s for reference).
- B:track_002 stays anonymous (U2): lost 2.25 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 17.4 m -> 19.6 m over the last 1.0 s.
- B:track_003 stays anonymous (U1): not approaching before the contact: clearance 7.9 m -> 12.8 m over the last 1.0 s; track motion contradicts A's own speed in the observed direction (3 sigma; full-speed RMSE 2.44 m/s for reference).
- B:track_004 stays anonymous (U3): lost 3.90 s before the matched collision (window 1.00 s); not approaching before the contact: clearance 30.4 m -> 32.4 m over the last 1.0 s; speed not comparable with A's own speed before the collision.
- B:track_006 stays anonymous (U6): ambiguous: 2 persistent tracks of B are compatible with the contact (track_005, track_006).
- B:track_007 stays anonymous (U2): tracked for 0.40 s before the matched collision (needs 1.00 s); not approaching before the contact: clearance 23.0 m -> 23.6 m over the last 1.0 s.
- B:track_008 stays anonymous (U7): tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 1.00 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
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
