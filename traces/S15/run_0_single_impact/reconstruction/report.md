# Reconstruction report - S15/run_0_single_impact

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.95 s | 141 | 20 | 36 | 2 | A:e08 @ 3.80 s |
| B | 13.95 s | 141 | 20 | 33 | 2 | B:e12 @ 3.80 s |
| C | 13.95 s | 141 | 11 | 19 | 3 | none |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.55 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 65.9 m -> 53.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.99 m/s over 2.5 s (> 1.50)<br>clearance at the contact 53.92 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_002 | B | ASSOCIATED | 0.91 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.8 m -> 0.7 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.64 m/s over 1.6 s<br>clearance at the contact 0.75 m<br>the only track of A compatible with the contact |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>approaching before the contact: clearance 16.0 m -> 0.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.49 m/s over 1.7 s<br>clearance at the contact 0.19 m<br>the only track of B compatible with the contact |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.90 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 1.00 s)<br>not approaching before the contact: clearance 52.4 m -> 53.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 8.54 m/s over 0.9 s (> 1.50)<br>clearance at the contact 52.33 m (beyond 3.50 m: confidence factor 0.00) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_003 | C:track_003 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Global graph

50 nodes, 79 edges; 1 merged node(s): g19 COLLISION(A,B) from A:e08 + B:e12.

### Event sequence (global time)

- `-3.80` MOVING_START(A); MOVING_START(B)
- `-2.55` TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
- `-2.05` STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-1.75` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-1.70` TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-1.55` TURN_LEFT_START(B)
- `-0.90` TRACK_APPEARED_RIGHT(B,B:track_002)
- `-0.85` BRAKE_START(B)
- `-0.30` BRAKE_END(B)
- `-0.15` EGO_PATH_ENTRY(B,A)
- `-0.05` TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001); CLOSING_START(B,B:track_002)
- `+0.05` EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.25` EGO_PATH_ENTRY(A,A:track_001)
- `+0.35` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.50` EGO_PATH_EXIT(A,A:track_001)
- `+0.75` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `+0.85` EGO_PATH_EXIT(B,A)
- `+1.25` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `+1.40` TURN_LEFT_END(A)
- `+6.75` STOP_SIGN_DETECTED_START(A,A:sign-1)
- `+7.75` MOVING_END(A); STOP_START(A)
- `+9.60` CRITICAL_TTC_START(A,A:track_001)

### What happened, in plain language

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 2.55 s before the reference collision, A's radar started tracking unidentified object A:track_001, which appeared in front of it.
- 2.55 s before the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.05 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.75 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.70 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.70 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.70 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.70 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.70 s before the reference collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the reference collision, B's time-to-contact with A became critical (already the case when first observed).
- 1.55 s before the reference collision, B started turning left.
- 0.90 s before the reference collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 0.85 s before the reference collision, B started braking.
- 0.30 s before the reference collision, B released the brake.
- 0.15 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the reference collision, B stopped turning left.
- At the reference collision, A started turning left.
- At the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- At the reference collision, B observed unidentified object B:track_002 start closing in.
- 0.05 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.05 s after the reference collision, B started braking.
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.25 s after the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.35 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.35 s after the reference collision, B observed A stop closing in.
- 0.50 s after the reference collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.75 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.85 s after the reference collision, B observed A leave its forward path corridor.
- 1.25 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 1.40 s after the reference collision, A stopped turning left.
- 6.75 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 7.75 s after the reference collision, A stopped moving.
- 7.75 s after the reference collision, A came to a stop.
- 9.60 s after the reference collision, A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.40 s) C's radar started tracking unidentified object C:track_001, which appeared on its left.
- (unaligned, C local time 0.40 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 1.25 s) C's radar started tracking unidentified object C:track_002, which appeared in front of it.
- (unaligned, C local time 1.25 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.25 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 2.80 s) C's camera established a STOP sign detection (unidentified object C:sign-0) (the detector judged it not relevant to its path).
- (unaligned, C local time 2.80 s) C's camera stopped detecting STOP sign unidentified object C:sign-0.
- (unaligned, C local time 3.15 s) C's radar started tracking unidentified object C:track_003, which appeared on its left.
- (unaligned, C local time 3.90 s) C observed unidentified object C:track_003 start closing in.
- (unaligned, C local time 5.20 s) C observed unidentified object C:track_002 enter its forward path corridor.

### Temporal safety relations

CUT_IN_START < CRITICAL_TTC_START < COLLISION, or CRITICAL_TTC_START <= CUT_IN_START (critical TTC already active), and EGO_PATH_ENTRY before/after the critical TTC. Temporal order only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 13.40; EGO_PATH_ENTRY 3.80 before critical TTC (-9.60 s) [local times; t_global: critical_ttc_start +9.60, ego_path_entry +0.00]
- A's track_002 (B): CRITICAL_TTC_START 2.10, COLLISION with B 3.80 (+1.70 s) [local times; t_global: critical_ttc_start -1.70, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 2.10, COLLISION with A 3.80 (+1.70 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.70, ego_path_entry -0.15, collision +0.00]
- C's track_002 (unidentified C:track_002): EGO_PATH_ENTRY 5.20, no critical TTC [local times]

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED_FRONT(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED_LEFT(B,A); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A); EGO_PATH_ENTRY(A,A:track_001); CLOSING_START(B,B:track_002)
- EGO_PATH_EXIT(A,A:track_001); BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 1.25 s)
- CLOSING of track_002, since A:e05 (t = 2.10 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.10 s); the track was lost at 3.75 s
- STOP_SIGN_DETECTED of sign-1, since A:e17 (t = 10.55 s)
- STOP, since A:e19 (t = 11.55 s)
- CRITICAL_TTC of track_001, since A:e20 (t = 13.40 s)
B:
- CLOSING of track_002, since B:e14 (t = 3.80 s)
- BRAKE, since B:e15 (t = 3.85 s)
- STOP, since B:e17 (t = 4.00 s)
C:
- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_001, since C:e03 (t = 0.40 s); the track was lost at 2.25 s
- CLOSING of track_002, since C:e05 (t = 1.25 s)
- CLOSING of track_003, since C:e10 (t = 3.90 s)
- EGO_PATH of track_002, since C:e11 (t = 5.20 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 4.55 s -> 5.05 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 10.55 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: A:e19
B:
- STOP sign sign-0: detected 1.75 s -> 2.05 s; relevant to the path: False; STOP_START inside: none
C:
- STOP sign sign-0: detected 2.80 s -> 2.80 s; relevant to the path: False; STOP_START inside: none

### Perceived state just before each collision report

- A A:e08 at 3.80 s (local): ego: MOVING; track_001: CLOSING; track lost, states UNKNOWN: track_002
- B B:e12 at 3.80 s (local): ego: MOVING, TURN_LEFT; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; track_002: no active state; sign-0: STOP sign known

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 3.75 s (A:e07): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- no track was lost
C:
- track_001 at 2.25 s (C:e06): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Uncertainty and limitations

- A:track_001 stays anonymous: track speed disagrees with B's own speed: RMSE 6.99 m/s over 2.5 s (> 1.50).
- B:track_002 stays anonymous: tracked for 0.90 s before the matched collision (needs 1.00 s); not approaching before the contact: clearance 52.4 m -> 53.1 m over the last 1.0 s; track speed disagrees with A's own speed: RMSE 8.54 m/s over 0.9 s (> 1.50).
- C:track_001 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C:track_002 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C:track_003 stays anonymous: graph C is not aligned: it recorded no collision to anchor on.
- C is UNALIGNED: it recorded no collision to anchor on.
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
    "new_impact_ratio": 0.75,
    "min_impact_ratio": 0.25,
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
    "track_appeared_rear_deg": 5.0,
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
    "contact_window_s": 1.0,
    "contact_range_m": 3.5,
    "contact_range_scale_m": 3.0,
    "approach_window_s": 1.0,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
