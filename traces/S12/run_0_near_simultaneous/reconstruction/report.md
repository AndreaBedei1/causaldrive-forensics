# Reconstruction report - S12/run_0_near_simultaneous

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.95 s | 151 | 81 | 353 | 19 | A:e44 @ 9.50 s |
| B | 14.95 s | 151 | 23 | 37 | 1 | B:e18 @ 9.50 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e44 | 9.50 | -9.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e18 | 9.50 | -9.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4032.49 vs 4032.49 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.90 | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 7.05 s before the matched collision<br>continuous up to the contact: last observed 0.35 s before it (window 0.50 s)<br>approaching before the contact: range 16.8 m -> 4.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.43 m/s over 2.7 s<br>range at the contact 4.63 m (beyond 3.50 m: confidence factor 0.93)<br>the only track of A compatible with the contact |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 68.5 m -> 64.7 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.09 m/s over 0.7 s (> 1.50)<br>range at the contact 64.74 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 45.3 m -> 41.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.35 m/s over 0.7 s (> 1.50)<br>range at the contact 41.89 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 40.8 m -> 37.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.25 m/s over 0.7 s (> 1.50)<br>range at the contact 37.45 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 96.6 m -> 93.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.61 m/s over 0.7 s (> 1.50)<br>range at the contact 93.37 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 57.8 m -> 54.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.81 m/s over 0.7 s (> 1.50)<br>range at the contact 54.52 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_007 | A:track_007 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 50.0 m -> 46.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.81 m/s over 0.7 s (> 1.50)<br>range at the contact 46.85 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_008 | A:track_008 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 53.6 m -> 50.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.77 m/s over 0.7 s (> 1.50)<br>range at the contact 50.36 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_009 | A:track_009 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.60 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 35.9 m -> 32.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 7.67 m/s over 0.6 s (> 1.50)<br>range at the contact 32.92 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_010 | A:track_010 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 93.2 m -> 88.8 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.58 m/s over 0.7 s (> 1.50)<br>range at the contact 88.83 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_011 | A:track_011 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.20 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 25.8 m -> 24.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.33 m/s over 0.2 s (> 1.50)<br>range at the contact 24.51 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_012 | A:track_012 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.15 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>not approaching before the contact: range 12.9 m -> 13.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>range at the contact 12.91 m (beyond 3.50 m: confidence factor 0.01) |
| A:track_013 | A:track_013 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 87.1 m -> 83.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.61 m/s over 0.7 s (> 1.50)<br>range at the contact 82.97 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_014 | A:track_014 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.10 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 87.4 m -> 86.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>range at the contact 86.50 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_015 | A:track_015 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 9.78 m (beyond 3.50 m: confidence factor 0.11) |
| A:track_016 | A:track_016 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 18.6 m -> 18.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>range at the contact 18.17 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_017 | A:track_017 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 12.72 m (beyond 3.50 m: confidence factor 0.01) |
| A:track_018 | A:track_018 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |
| A:track_019 | A:track_019 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |
| B:track_001 | A | ASSOCIATED | 0.69 | B and A both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 12.5 m -> 1.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.30 m/s over 3.0 s<br>range at the contact 1.09 m<br>the only track of B compatible with the contact |

## Global graph

103 nodes, 439 edges; 1 merged node(s): g61 COLLISION(A,B) from A:e44 + B:e18.

### Event sequence (global time)

- `-9.50` MOVING_START(A); MOVING_START(B)
- `-8.80` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `-7.70` STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-7.20` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `-7.05` TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- `-6.95` TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- `-6.90` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-6.85` BRAKE_START(A)
- `-6.75` BRAKE_START(B)
- `-6.10` MOVING_END(A); STOP_START(A)
- `-6.00` CLOSING_END(A,B); CLOSING_END(B,A); MOVING_END(B); STOP_START(B)
- `-2.55` BRAKE_END(A); BRAKE_END(B)
- `-2.20` STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A)
- `-2.15` STOP_END(B); MOVING_START(B)
- `-1.20` TURN_LEFT_START(A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-0.70` TRACK_APPEARED_LEFT(A,A:track_002); TRACK_APPEARED_LEFT(A,A:track_005); TRACK_APPEARED_LEFT(A,A:track_010); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_010)
- `-0.65` TRACK_APPEARED_LEFT(A,A:track_003); TRACK_APPEARED_LEFT(A,A:track_004); TRACK_APPEARED_LEFT(A,A:track_006); TRACK_APPEARED_LEFT(A,A:track_007); TRACK_APPEARED_LEFT(A,A:track_008); TRACK_APPEARED_LEFT(A,A:track_013); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008); CLOSING_START(A,A:track_013)
- `-0.60` TRACK_APPEARED_LEFT(A,A:track_009); CLOSING_START(A,A:track_009)
- `-0.55` EGO_PATH_ENTRY(B,A)
- `-0.35` TRACK_LOST(A,B)
- `-0.20` TRACK_APPEARED_LEFT(A,A:track_011); CLOSING_START(A,A:track_011)
- `-0.15` TRACK_APPEARED_RIGHT(A,A:track_012)
- `-0.10` TRACK_APPEARED_LEFT(A,A:track_014); CLOSING_START(A,A:track_014)
- `-0.05` CRITICAL_TTC_END(B,A); CLOSING_END(B,A); TRACK_APPEARED_LEFT(A,A:track_016); CLOSING_START(A,A:track_016)
- `+0.00` COLLISION(A,B); TRACK_APPEARED_FRONT(A,A:track_017); TRACK_APPEARED_RIGHT(A,A:track_015); CLOSING_START(A,A:track_017)
- `+0.05` EGO_PATH_EXIT(A,A:track_017); EGO_PATH_EXIT(B,A); BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(A,A:track_018); TRACK_APPEARED_RIGHT(A,A:track_019); CLOSING_START(A,A:track_018); CLOSING_START(A,A:track_019); TRACK_LOST(A,A:track_012)
- `+0.20` CLOSING_START(A,A:track_015)
- `+0.25` TRACK_LOST(B,A)
- `+0.45` MOVING_END(B); STOP_START(B)
- `+0.50` CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_005); CLOSING_END(A,A:track_008); CLOSING_END(A,A:track_015); CLOSING_END(A,A:track_017); CLOSING_END(A,A:track_018); CLOSING_END(A,A:track_019); TURN_LEFT_END(A); MOVING_END(A); STOP_START(A); TRACK_LOST(A,A:track_019)
- `+0.55` CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_009); CLOSING_END(A,A:track_010); CLOSING_END(A,A:track_011); CLOSING_END(A,A:track_013); CLOSING_END(A,A:track_014); CLOSING_END(A,A:track_016)
- `+0.60` CLOSING_END(A,A:track_006)
- `+1.50` STOP_SIGN_DETECTED_START(A,A:sign-1)
- `+3.10` TRACK_LOST(A,A:track_006)
- `+4.85` TRACK_LOST(A,A:track_018)
- `+5.35` TRACK_LOST(A,A:track_005)
- `+5.40` TRACK_LOST(A,A:track_008)

### What happened, in plain language

- 9.50 s before the reference collision, A started moving (already the case when first observed).
- 9.50 s before the reference collision, B started moving (already the case when first observed).
- 8.80 s before the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 7.70 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 7.20 s before the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.05 s before the reference collision, A's radar started tracking B, which appeared on its left.
- 7.05 s before the reference collision, A observed B start closing in (already the case when first observed).
- 6.95 s before the reference collision, B's radar started tracking A, which appeared on its right.
- 6.95 s before the reference collision, B observed A start closing in (already the case when first observed).
- 6.90 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 6.85 s before the reference collision, A started braking.
- 6.75 s before the reference collision, B started braking.
- 6.10 s before the reference collision, A stopped moving.
- 6.10 s before the reference collision, A came to a stop.
- 6.00 s before the reference collision, A observed B stop closing in.
- 6.00 s before the reference collision, B observed A stop closing in.
- 6.00 s before the reference collision, B stopped moving.
- 6.00 s before the reference collision, B came to a stop.
- 2.55 s before the reference collision, A released the brake.
- 2.55 s before the reference collision, B released the brake.
- 2.20 s before the reference collision, A left its stop.
- 2.20 s before the reference collision, A started moving.
- 2.20 s before the reference collision, A observed B start closing in.
- 2.20 s before the reference collision, B observed A start closing in.
- 2.15 s before the reference collision, B left its stop.
- 2.15 s before the reference collision, B started moving.
- 1.20 s before the reference collision, A started turning left.
- 1.20 s before the reference collision, A's time-to-contact with B became critical.
- 1.20 s before the reference collision, B's time-to-contact with A became critical.
- 0.70 s before the reference collision, A's radar started tracking unidentified object A:track_002, which appeared on its left.
- 0.70 s before the reference collision, A's radar started tracking unidentified object A:track_005, which appeared on its left.
- 0.70 s before the reference collision, A's radar started tracking unidentified object A:track_010, which appeared on its left.
- 0.70 s before the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 0.70 s before the reference collision, A observed unidentified object A:track_005 start closing in (already the case when first observed).
- 0.70 s before the reference collision, A observed unidentified object A:track_010 start closing in (already the case when first observed).
- 0.65 s before the reference collision, A's radar started tracking unidentified object A:track_003, which appeared on its left.
- 0.65 s before the reference collision, A's radar started tracking unidentified object A:track_004, which appeared on its left.
- 0.65 s before the reference collision, A's radar started tracking unidentified object A:track_006, which appeared on its left.
- 0.65 s before the reference collision, A's radar started tracking unidentified object A:track_007, which appeared on its left.
- 0.65 s before the reference collision, A's radar started tracking unidentified object A:track_008, which appeared on its left.
- 0.65 s before the reference collision, A's radar started tracking unidentified object A:track_013, which appeared on its left.
- 0.65 s before the reference collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- 0.65 s before the reference collision, A observed unidentified object A:track_004 start closing in (already the case when first observed).
- 0.65 s before the reference collision, A observed unidentified object A:track_006 start closing in (already the case when first observed).
- 0.65 s before the reference collision, A observed unidentified object A:track_007 start closing in (already the case when first observed).
- 0.65 s before the reference collision, A observed unidentified object A:track_008 start closing in (already the case when first observed).
- 0.65 s before the reference collision, A observed unidentified object A:track_013 start closing in (already the case when first observed).
- 0.60 s before the reference collision, A's radar started tracking unidentified object A:track_009, which appeared on its left.
- 0.60 s before the reference collision, A observed unidentified object A:track_009 start closing in (already the case when first observed).
- 0.55 s before the reference collision, B observed A enter its forward path corridor.
- 0.35 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.20 s before the reference collision, A's radar started tracking unidentified object A:track_011, which appeared on its left.
- 0.20 s before the reference collision, A observed unidentified object A:track_011 start closing in (already the case when first observed).
- 0.15 s before the reference collision, A's radar started tracking unidentified object A:track_012, which appeared on its right.
- 0.10 s before the reference collision, A's radar started tracking unidentified object A:track_014, which appeared on its left.
- 0.10 s before the reference collision, A observed unidentified object A:track_014 start closing in (already the case when first observed).
- 0.05 s before the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s before the reference collision, B observed A stop closing in.
- 0.05 s before the reference collision, A's radar started tracking unidentified object A:track_016, which appeared on its left.
- 0.05 s before the reference collision, A observed unidentified object A:track_016 start closing in (already the case when first observed).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 4032, B: 4032 N*s).
- At the reference collision, A's radar started tracking unidentified object A:track_017, which appeared in front of it.
- At the reference collision, A's radar started tracking unidentified object A:track_015, which appeared on its right.
- At the reference collision, A observed unidentified object A:track_017 start closing in (already the case when first observed).
- 0.05 s after the reference collision, A observed unidentified object A:track_017 leave its forward path corridor.
- 0.05 s after the reference collision, B observed A leave its forward path corridor.
- 0.05 s after the reference collision, A started braking.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, A's radar started tracking unidentified object A:track_018, which appeared on its left.
- 0.05 s after the reference collision, A's radar started tracking unidentified object A:track_019, which appeared on its right.
- 0.05 s after the reference collision, A observed unidentified object A:track_018 start closing in (already the case when first observed).
- 0.05 s after the reference collision, A observed unidentified object A:track_019 start closing in (already the case when first observed).
- 0.05 s after the reference collision, A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- 0.20 s after the reference collision, A observed unidentified object A:track_015 start closing in.
- 0.25 s after the reference collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.50 s after the reference collision, A observed unidentified object A:track_002 stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_005 stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_008 stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_015 stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_017 stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_018 stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_019 stop closing in.
- 0.50 s after the reference collision, A stopped turning left.
- 0.50 s after the reference collision, A stopped moving.
- 0.50 s after the reference collision, A came to a stop.
- 0.50 s after the reference collision, A's radar lost unidentified object A:track_019 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the reference collision, A observed unidentified object A:track_003 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_004 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_007 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_009 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_010 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_011 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_013 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_014 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_016 stop closing in.
- 0.60 s after the reference collision, A observed unidentified object A:track_006 stop closing in.
- 1.50 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 3.10 s after the reference collision, A's radar lost unidentified object A:track_006 (its states are UNKNOWN from then on, not ended).
- 4.85 s after the reference collision, A's radar lost unidentified object A:track_018 (its states are UNKNOWN from then on, not ended).
- 5.35 s after the reference collision, A's radar lost unidentified object A:track_005 (its states are UNKNOWN from then on, not ended).
- 5.40 s after the reference collision, A's radar lost unidentified object A:track_008 (its states are UNKNOWN from then on, not ended).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 8.30, COLLISION with B 9.50 (+1.20 s) [local times; t_global: critical_ttc_start -1.20, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 8.30, COLLISION with A 9.50 (+1.20 s); EGO_PATH_ENTRY 8.95 after critical TTC (+0.65 s) [local times; t_global: critical_ttc_start -1.20, ego_path_entry -0.55, collision +0.00]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B)
- TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A)
- MOVING_END(A); STOP_START(A)
- CLOSING_END(A,B); CLOSING_END(B,A); MOVING_END(B); STOP_START(B)
- BRAKE_END(A); BRAKE_END(B)
- STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A)
- STOP_END(B); MOVING_START(B)
- TURN_LEFT_START(A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- TRACK_APPEARED_LEFT(A,A:track_002); TRACK_APPEARED_LEFT(A,A:track_005); TRACK_APPEARED_LEFT(A,A:track_010); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_010)
- TRACK_APPEARED_LEFT(A,A:track_003); TRACK_APPEARED_LEFT(A,A:track_004); TRACK_APPEARED_LEFT(A,A:track_006); TRACK_APPEARED_LEFT(A,A:track_007); TRACK_APPEARED_LEFT(A,A:track_008); TRACK_APPEARED_LEFT(A,A:track_013); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008); CLOSING_START(A,A:track_013)
- TRACK_APPEARED_LEFT(A,A:track_009); CLOSING_START(A,A:track_009)
- TRACK_APPEARED_LEFT(A,A:track_011); CLOSING_START(A,A:track_011)
- TRACK_APPEARED_LEFT(A,A:track_014); CLOSING_START(A,A:track_014)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A); TRACK_APPEARED_LEFT(A,A:track_016); CLOSING_START(A,A:track_016)
- COLLISION(A,B); TRACK_APPEARED_FRONT(A,A:track_017); TRACK_APPEARED_RIGHT(A,A:track_015); CLOSING_START(A,A:track_017)
- EGO_PATH_EXIT(A,A:track_017); EGO_PATH_EXIT(B,A); BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(A,A:track_018); TRACK_APPEARED_RIGHT(A,A:track_019); CLOSING_START(A,A:track_018); CLOSING_START(A,A:track_019); TRACK_LOST(A,A:track_012)
- MOVING_END(B); STOP_START(B)
- CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_005); CLOSING_END(A,A:track_008); CLOSING_END(A,A:track_015); CLOSING_END(A,A:track_017); CLOSING_END(A,A:track_018); CLOSING_END(A,A:track_019); TURN_LEFT_END(A); MOVING_END(A); STOP_START(A); TRACK_LOST(A,A:track_019)
- CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_009); CLOSING_END(A,A:track_010); CLOSING_END(A,A:track_011); CLOSING_END(A,A:track_013); CLOSING_END(A,A:track_014); CLOSING_END(A,A:track_016)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e13 (t = 7.30 s); the track was lost at 9.15 s
- CRITICAL_TTC of track_001, since A:e15 (t = 8.30 s); the track was lost at 9.15 s
- BRAKE, since A:e49 (t = 9.55 s)
- STOP, since A:e65 (t = 10.00 s)
- STOP_SIGN_DETECTED of sign-1, since A:e77 (t = 11.00 s)
B:
- BRAKE, since B:e20 (t = 9.55 s)
- STOP, since B:e23 (t = 9.95 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 0.70 s -> 2.30 s; relevant to the path: True; STOP_START inside: none
- STOP sign sign-1: detected 11.00 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened
B:
- STOP sign sign-0: detected 1.80 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

### Perceived state just before each collision report

- A A:e44 at 9.50 s (local): ego: MOVING, TURN_LEFT; track_002: CLOSING; track_003: CLOSING; track_004: CLOSING; track_005: CLOSING; track_006: CLOSING; track_007: CLOSING; track_008: CLOSING; track_009: CLOSING; track_010: CLOSING; track_011: CLOSING; track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?; track_013: CLOSING; track_014: CLOSING; track_016: CLOSING; track lost, states UNKNOWN: track_001; sign-0: STOP sign known, relevant to the path
- B B:e18 at 9.50 s (local): ego: MOVING; track_001: IN_EGO_PATH; sign-0: STOP sign known, relevant to the path

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 9.15 s (A:e36): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_019 at 10.00 s (A:e66): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_012, track_006, track_018, track_005, track_008
B:
- lost with no state active: track_001

## Uncertainty and limitations

- A:track_002 stays anonymous: tracked for 0.70 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 8.09 m/s over 0.7 s (> 1.50).
- A:track_003 stays anonymous: tracked for 0.65 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 8.35 m/s over 0.7 s (> 1.50).
- A:track_004 stays anonymous: tracked for 0.65 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 8.25 m/s over 0.7 s (> 1.50).
- A:track_005 stays anonymous: tracked for 0.70 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 6.61 m/s over 0.7 s (> 1.50).
- A:track_006 stays anonymous: tracked for 0.65 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 8.81 m/s over 0.7 s (> 1.50).
- A:track_007 stays anonymous: tracked for 0.65 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 8.81 m/s over 0.7 s (> 1.50).
- A:track_008 stays anonymous: tracked for 0.65 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 8.77 m/s over 0.7 s (> 1.50).
- A:track_009 stays anonymous: tracked for 0.60 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 7.67 m/s over 0.6 s (> 1.50).
- A:track_010 stays anonymous: tracked for 0.70 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 5.58 m/s over 0.7 s (> 1.50).
- A:track_011 stays anonymous: tracked for 0.20 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 6.33 m/s over 0.2 s (> 1.50).
- A:track_012 stays anonymous: tracked for 0.15 s before the matched collision (needs 1.00 s); not approaching before the contact: range 12.9 m -> 13.2 m over the last 1.0 s; speed not comparable with B's own speed before the collision.
- A:track_013 stays anonymous: tracked for 0.65 s before the matched collision (needs 1.00 s); track speed disagrees with B's own speed: RMSE 8.61 m/s over 0.7 s (> 1.50).
- A:track_014 stays anonymous: tracked for 0.10 s before the matched collision (needs 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_015 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_016 stays anonymous: tracked for 0.05 s before the matched collision (needs 1.00 s); speed not comparable with B's own speed before the collision.
- A:track_017 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_018 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.05 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
- A:track_019 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.05 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision.
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
