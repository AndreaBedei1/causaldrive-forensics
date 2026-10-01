# Reconstruction report - S15/run_0_deflected_into_c

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.95 s | 141 | 26 | 43 | 2 | A:e09 @ 3.80 s, A:e14 @ 4.75 s |
| B | 13.95 s | 141 | 40 | 96 | 8 | B:e29 @ 3.80 s |
| C | 13.95 s | 141 | 14 | 23 | 2 | C:e08 @ 4.75 s |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e29 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | ALIGNED | C:e08 | 4.75 | -3.80 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1637.56 vs 1637.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.94 | A and C both reported collision_002 at 4.75 s (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.6 m -> 1.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.53 m/s over 3.0 s<br>range at the contact 1.13 m<br>the only track of A compatible with the contact<br>collision_001 with B at 3.80 s: not compatible (track speed disagrees with B's own speed: RMSE 3.64 m/s over 3.0 s (> 1.50)) |
| A:track_002 | B | ASSOCIATED | 0.85 | A and B both reported collision_001 at 3.80 s (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.1 m -> 1.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.85 m/s over 1.8 s<br>range at the contact 1.89 m<br>the only track of A compatible with the contact<br>collision_002 with C at 4.75 s: not compatible (lost 1.00 s before the matched collision (window 0.50 s); track speed disagrees with C's own speed: RMSE 3.29 m/s over 1.8 s (> 1.50)) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.35 s before the matched collision<br>lost 0.65 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 22.2 m -> 14.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.69 m/s over 1.7 s (> 1.50) |
| B:track_002 | A | ASSOCIATED | 0.88 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 16.9 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.77 m/s over 1.8 s<br>range at the contact 0.99 m<br>the only track of B compatible with the contact |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 33.3 m -> 30.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.67 m/s over 0.7 s (> 1.50)<br>range at the contact 30.02 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 22.0 m -> 19.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.16 m/s over 0.7 s (> 1.50)<br>range at the contact 19.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 30.4 m -> 27.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 8.37 m/s over 0.7 s (> 1.50)<br>range at the contact 26.97 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 27.3 m -> 24.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.37 m/s over 0.7 s (> 1.50)<br>range at the contact 24.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.3 m -> 15.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.73 m/s over 0.6 s (> 1.50)<br>range at the contact 15.03 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| C:track_001 | C:track_001 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.75 s before the matched collision<br>continuous up to the contact: last observed 0.30 s before it (window 0.50 s)<br>approaching before the contact: range 11.6 m -> 7.6 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.88 m/s over 2.7 s (> 1.50)<br>range at the contact 7.64 m (beyond 3.50 m: confidence factor 0.39) |
| C:track_002 | A | ASSOCIATED | 0.92 | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.5 m -> 1.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.59 m/s over 3.0 s<br>range at the contact 1.89 m<br>the only track of C compatible with the contact |

## Global graph

78 nodes, 195 edges; 2 merged node(s): g43 COLLISION(A,B) from A:e09 + B:e29, g59 COLLISION(A,C) from A:e14 + C:e08.

### Event sequence (global time)

- `-3.80` MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_LEFT(C,C:track_001); CLOSING_START(C,C:track_001)
- `-3.75` TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
- `-2.35` TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
- `-2.30` STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-1.85` TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- `-1.80` TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- `-1.70` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-1.65` CRITICAL_TTC_START(B,A)
- `-1.55` TURN_LEFT_START(B)
- `-1.25` CRITICAL_TTC_START(A,C)
- `-0.90` CRITICAL_TTC_START(C,A)
- `-0.85` BRAKE_START(B)
- `-0.75` TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006)
- `-0.70` TRACK_APPEARED_LEFT(B,B:track_007); CLOSING_START(B,B:track_007)
- `-0.65` TRACK_LOST(B,B:track_001)
- `-0.30` BRAKE_END(B)
- `-0.10` EGO_PATH_ENTRY(B,A)
- `-0.05` TRACK_LOST(A,B); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006); TRACK_LOST(B,B:track_007)
- `+0.00` COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A)
- `+0.05` BRAKE_START(B); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_008); CRITICAL_TTC_START(B,B:track_008)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.30` CRITICAL_TTC_END(B,A)
- `+0.35` TRACK_LOST(B,B:track_008)
- `+0.50` CLOSING_END(B,A)
- `+0.65` TRACK_LOST(C,C:track_001)
- `+0.70` EGO_PATH_ENTRY(A,C)
- `+0.80` STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- `+0.95` COLLISION(A,C)
- `+1.00` CRITICAL_TTC_END(A,C); CLOSING_END(A,C); EGO_PATH_EXIT(B,A); BRAKE_START(C)
- `+1.15` TURN_LEFT_END(A); EGO_PATH_ENTRY(C,A)
- `+1.20` CRITICAL_TTC_END(C,A)
- `+1.25` CLOSING_END(C,A); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
- `+1.50` STOP_SIGN_DETECTED_START(A,A:sign-2)
- `+4.00` STOP_SIGN_DETECTED_END(A,A:sign-2)
- `+4.90` STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2)
- `+5.80` STOP_SIGN_DETECTED_START(A,A:sign-2)
- `+6.10` STOP_SIGN_DETECTED_END(A,A:sign-2)
- `+7.10` STOP_SIGN_DETECTED_START(A,A:sign-2)

### What happened, in plain language

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 3.80 s before the reference collision, C started moving (already the case when first observed).
- 3.80 s before the reference collision, C's radar started tracking unidentified object C:track_001, which appeared on its left.
- 3.80 s before the reference collision, C observed unidentified object C:track_001 start closing in (already the case when first observed).
- 3.75 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 3.75 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 3.75 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.75 s before the reference collision, C observed A start closing in (already the case when first observed).
- 2.35 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.35 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.30 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.85 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.80 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the reference collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.65 s before the reference collision, B's time-to-contact with A became critical.
- 1.55 s before the reference collision, B started turning left.
- 1.25 s before the reference collision, A's time-to-contact with C became critical.
- 0.90 s before the reference collision, C's time-to-contact with A became critical.
- 0.85 s before the reference collision, B started braking.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_005, which appeared on its left.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_006, which appeared on its left.
- 0.75 s before the reference collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.75 s before the reference collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.75 s before the reference collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.75 s before the reference collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.70 s before the reference collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- 0.70 s before the reference collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- 0.65 s before the reference collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- 0.30 s before the reference collision, B released the brake.
- 0.10 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the reference collision, B stopped turning left.
- At the reference collision, A started turning left.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B's radar started tracking unidentified object B:track_008, which appeared on its right.
- 0.05 s after the reference collision, B observed unidentified object B:track_008 start closing in (already the case when first observed).
- 0.05 s after the reference collision, B's time-to-contact with unidentified object B:track_008 became critical (already the case when first observed).
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.30 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.35 s after the reference collision, B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- 0.50 s after the reference collision, B observed A stop closing in.
- 0.65 s after the reference collision, C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A observed C enter its forward path corridor.
- 0.80 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.80 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 0.95 s after the reference collision, A and C both recorded this same collision (peak impulses A: 1638, C: 1638 N*s).
- 1.00 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.00 s after the reference collision, A observed C stop closing in.
- 1.00 s after the reference collision, B observed A leave its forward path corridor.
- 1.00 s after the reference collision, C started braking.
- 1.15 s after the reference collision, A stopped turning left.
- 1.15 s after the reference collision, C observed A enter its forward path corridor.
- 1.20 s after the reference collision, C's time-to-contact with A stopped being critical.
- 1.25 s after the reference collision, C observed A stop closing in.
- 1.25 s after the reference collision, A stopped moving.
- 1.25 s after the reference collision, C stopped moving.
- 1.25 s after the reference collision, A came to a stop.
- 1.25 s after the reference collision, C came to a stop.
- 1.50 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path).
- 4.00 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 4.90 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- 4.90 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 5.80 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- 6.10 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 7.10 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-5).

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (C): CRITICAL_TTC_START 2.55, COLLISION with C 4.75 (+2.20 s); EGO_PATH_ENTRY 4.50 after critical TTC (+1.95 s) [local times; t_global: critical_ttc_start -1.25, ego_path_entry +0.70, collision +0.95]
- A's track_002 (B): CRITICAL_TTC_START 2.00, COLLISION with B 3.80 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.15, COLLISION with A 3.80 (+1.65 s); EGO_PATH_ENTRY 3.70 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.65, ego_path_entry -0.10, collision +0.00]
- B's track_008 (unidentified B:track_008): CRITICAL_TTC_START 3.85 [local times; t_global: critical_ttc_start +0.05]
- C's track_002 (A): CRITICAL_TTC_START 2.90, COLLISION with A 4.75 (+1.85 s); EGO_PATH_ENTRY 4.95 after critical TTC (+2.05 s) [local times; t_global: critical_ttc_start -0.90, ego_path_entry +1.15, collision +0.95]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_LEFT(C,C:track_001); CLOSING_START(C,C:track_001)
- TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A)
- TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001)
- TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006)
- TRACK_APPEARED_LEFT(B,B:track_007); CLOSING_START(B,B:track_007)
- TRACK_LOST(A,B); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006); TRACK_LOST(B,B:track_007)
- COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A)
- BRAKE_START(B); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_008); CRITICAL_TTC_START(B,B:track_008)
- MOVING_END(B); STOP_START(B)
- STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- CRITICAL_TTC_END(A,C); CLOSING_END(A,C); EGO_PATH_EXIT(B,A); BRAKE_START(C)
- TURN_LEFT_END(A); EGO_PATH_ENTRY(C,A)
- CLOSING_END(C,A); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)
- STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2)

### States still active when observation ended

A:
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- EGO_PATH of track_001, since A:e11 (t = 4.50 s)
- STOP, since A:e19 (t = 5.05 s)
- STOP_SIGN_DETECTED of sign-2, since A:e26 (t = 10.90 s)
B:
- CLOSING of track_001, since B:e03 (t = 1.45 s); the track was lost at 3.15 s
- CLOSING of track_003, since B:e15 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_004, since B:e16 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_005, since B:e17 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_006, since B:e18 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_007, since B:e20 (t = 3.10 s); the track was lost at 3.75 s
- BRAKE, since B:e31 (t = 3.85 s)
- CLOSING of track_008, since B:e33 (t = 3.85 s); the track was lost at 4.15 s
- CRITICAL_TTC of track_008, since B:e34 (t = 3.85 s); the track was lost at 4.15 s
- STOP, since B:e36 (t = 4.00 s)
C:
- CLOSING of track_001, since C:e03 (t = 0.00 s); the track was lost at 4.45 s
- BRAKE, since C:e09 (t = 4.80 s)
- EGO_PATH of track_002, since C:e10 (t = 4.95 s)
- STOP, since C:e14 (t = 5.05 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 4.60 s -> 4.60 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-2: detected 5.30 s -> 7.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 8.70 s -> 8.70 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 9.60 s -> 9.90 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 10.90 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened
B:
- STOP sign sign-0: detected 1.50 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
C:
- none

### Perceived state just before each collision report

- A A:e09 at 3.80 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC; track lost, states UNKNOWN: track_002
- A A:e14 at 4.75 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track lost, states UNKNOWN: track_002; sign-0: STOP sign known
- B B:e29 at 3.80 s (local): ego: MOVING, TURN_LEFT; track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007; sign-0: STOP sign known
- C C:e08 at 4.75 s (local): ego: MOVING; track_002: CLOSING, CRITICAL_TTC; track lost, states UNKNOWN: track_001

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 3.75 s (A:e08): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_001 at 3.15 s (B:e21): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 3.75 s (B:e24): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 3.75 s (B:e25): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 3.75 s (B:e26): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.75 s (B:e27): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 3.75 s (B:e28): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 4.15 s (B:e38): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
C:
- track_001 at 4.45 s (C:e07): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Uncertainty and limitations

- B:track_001 stays anonymous: lost 0.65 s before the matched collision (window 0.50 s); track speed disagrees with A's own speed: RMSE 5.69 m/s over 1.7 s (> 1.50).
- B:track_003 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.67 m/s over 0.7 s (> 1.50).
- B:track_004 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.16 m/s over 0.7 s (> 1.50).
- B:track_005 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 8.37 m/s over 0.7 s (> 1.50).
- B:track_006 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.37 m/s over 0.7 s (> 1.50).
- B:track_007 stays anonymous: tracked for 0.70 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.73 m/s over 0.6 s (> 1.50).
- B:track_008 stays anonymous: tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.05 s after the matched collision; range trend before the contact not measurable; speed not comparable with A's own speed before the collision.
- C:track_001 stays anonymous: track speed disagrees with A's own speed: RMSE 3.88 m/s over 2.7 s (> 1.50).
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
