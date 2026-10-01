# Reconstruction report - S15/run_0_single_impact

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.95 s | 141 | 20 | 36 | 2 | A:e08 @ 3.80 s |
| B | 13.95 s | 141 | 33 | 74 | 6 | B:e26 @ 3.80 s |
| C | 13.95 s | 141 | 10 | 19 | 2 | none |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e26 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.90 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 66.2 m -> 54.3 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.99 m/s over 2.9 s (> 1.50)<br>range at the contact 54.25 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_002 | B | ASSOCIATED | 0.85 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.1 m -> 1.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.85 m/s over 1.8 s<br>range at the contact 1.89 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.88 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 16.9 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.77 m/s over 1.8 s<br>range at the contact 0.98 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 33.3 m -> 30.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.67 m/s over 0.7 s (> 1.50)<br>range at the contact 30.02 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 22.0 m -> 19.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.16 m/s over 0.7 s (> 1.50)<br>range at the contact 19.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 30.4 m -> 27.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 8.37 m/s over 0.7 s (> 1.50)<br>range at the contact 26.97 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 27.3 m -> 24.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.37 m/s over 0.7 s (> 1.50)<br>range at the contact 24.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.3 m -> 15.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.73 m/s over 0.6 s (> 1.50)<br>range at the contact 15.03 m (beyond 3.50 m: confidence factor 0.00) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Global graph

62 nodes, 137 edges; 1 merged node(s): g33 COLLISION(A,B) from A:e08 + B:e26.

### Event sequence (global time)

- `-3.80` MOVING_START(A); MOVING_START(B)
- `-2.90` TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
- `-2.00` STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-1.85` TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- `-1.80` TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- `-1.70` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-1.65` CRITICAL_TTC_START(B,A)
- `-1.55` TURN_LEFT_START(B)
- `-0.85` BRAKE_START(B)
- `-0.75` TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
- `-0.70` TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_006)
- `-0.30` BRAKE_END(B)
- `-0.10` EGO_PATH_ENTRY(B,A)
- `-0.05` TRACK_LOST(A,B); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006)
- `+0.00` COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001)
- `+0.05` EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.30` CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(A,A:track_001)
- `+0.50` CLOSING_END(B,A); EGO_PATH_EXIT(A,A:track_001)
- `+0.80` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `+1.00` EGO_PATH_EXIT(B,A)
- `+1.30` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `+1.40` TURN_LEFT_END(A)
- `+6.80` STOP_SIGN_DETECTED_START(A,A:sign-1)
- `+7.75` MOVING_END(A); STOP_START(A)
- `+9.65` CRITICAL_TTC_START(A,A:track_001)

### What happened, in plain language

- 3.80 s before the matched collision, A started moving (already the case when first observed).
- 3.80 s before the matched collision, B started moving (already the case when first observed).
- 2.90 s before the matched collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 2.90 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.00 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 1.85 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.65 s before the matched collision, B's time-to-contact with A became critical.
- 1.55 s before the matched collision, B started turning left.
- 0.85 s before the matched collision, B started braking.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 0.75 s before the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its left.
- 0.75 s before the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.75 s before the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.75 s before the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.75 s before the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.70 s before the matched collision, B's radar started tracking unidentified object B:track_006, which appeared on its left.
- 0.70 s before the matched collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.30 s before the matched collision, B released the brake.
- 0.10 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the matched collision, B stopped turning left.
- At the matched collision, A started turning left.
- At the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.05 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.05 s after the matched collision, B started braking.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.30 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.30 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.50 s after the matched collision, B observed A stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.80 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 1.00 s after the matched collision, B observed A leave its forward path corridor.
- 1.30 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 1.40 s after the matched collision, A stopped turning left.
- 6.80 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 7.75 s after the matched collision, A stopped moving.
- 7.75 s after the matched collision, A came to a stop.
- 9.65 s after the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.65 s) C's radar started tracking unidentified object C:track_002, which appeared on its left.
- (unaligned, C local time 0.65 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 0.80 s) C's radar started tracking unidentified object C:track_001, which appeared in front of it.
- (unaligned, C local time 0.80 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.80 s) C's camera established a STOP sign detection (unidentified object C:sign-0) (the detector judged it not relevant to its path).
- (unaligned, C local time 2.80 s) C's camera stopped detecting STOP sign unidentified object C:sign-0.
- (unaligned, C local time 2.95 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 3.85 s) C observed unidentified object C:track_002 start closing in.
- (unaligned, C local time 5.15 s) C observed unidentified object C:track_001 enter its forward path corridor.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 13.45, COLLISION 3.80 (+-9.65 s); EGO_PATH_ENTRY 3.80 before critical TTC (-9.65 s) [local times; t_global: critical_ttc_start +9.65, ego_path_entry +0.00, collision +0.00]
- A's track_002 (B): CRITICAL_TTC_START 2.00, COLLISION 3.80 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.15, COLLISION 3.80 (+1.65 s); EGO_PATH_ENTRY 3.70 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.65, ego_path_entry -0.10, collision +0.00]
- C's track_001 (unidentified C:track_001): EGO_PATH_ENTRY 5.15, no critical TTC [local times]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A)
- TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005)
- TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_006)
- TRACK_LOST(A,B); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006)
- COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001)
- EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- CRITICAL_TTC_END(B,A); EGO_PATH_ENTRY(A,A:track_001)
- CLOSING_END(B,A); EGO_PATH_EXIT(A,A:track_001)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 0.90 s)
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- STOP_SIGN_DETECTED of sign-1, since A:e17 (t = 10.60 s)
- STOP, since A:e19 (t = 11.55 s)
- CRITICAL_TTC of track_001, since A:e20 (t = 13.45 s)
B:
- CLOSING of track_002, since B:e13 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_003, since B:e14 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_004, since B:e15 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_005, since B:e16 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_006, since B:e18 (t = 3.10 s); the track was lost at 3.75 s
- BRAKE, since B:e28 (t = 3.85 s)
- STOP, since B:e30 (t = 4.00 s)
C:
- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_001, since C:e05 (t = 0.80 s)
- CLOSING of track_002, since C:e09 (t = 3.85 s)
- EGO_PATH of track_001, since C:e10 (t = 5.15 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 4.60 s -> 5.10 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 10.60 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: A:e19
B:
- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
C:
- STOP sign sign-0: detected 2.80 s -> 2.80 s; relevant to the path: False; STOP_START inside: none

### Perceived state just before each collision report

- A A:e08 at 3.80 s (local): ego: MOVING; track_001: CLOSING; track lost, states UNKNOWN: track_002
- B B:e26 at 3.80 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006; sign-0: STOP sign known

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 3.75 s (A:e07): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_002 at 3.75 s (B:e21): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 3.75 s (B:e22): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 3.75 s (B:e23): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 3.75 s (B:e24): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.75 s (B:e25): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
C:
- no track was lost

## Uncertainty and limitations

- A:track_001 stays anonymous: track speed disagrees with B's own speed: RMSE 6.99 m/s over 2.9 s (> 1.50).
- B:track_002 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.67 m/s over 0.7 s (> 1.50).
- B:track_003 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.16 m/s over 0.7 s (> 1.50).
- B:track_004 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 8.37 m/s over 0.7 s (> 1.50).
- B:track_005 stays anonymous: tracked for 0.75 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.37 m/s over 0.7 s (> 1.50).
- B:track_006 stays anonymous: tracked for 0.70 s before the matched collision (needs 1.00 s); track speed disagrees with A's own speed: RMSE 9.73 m/s over 0.6 s (> 1.50).
- C:track_001 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C:track_002 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C is UNALIGNED: it recorded no collision to anchor on.
- Global time rests on one collision anchor and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from t_global = 0.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5
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
    "contact_window_s": 0.5,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
