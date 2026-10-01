# Reconstruction report - S15/run_0_single_impact

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.95 s | 141 | 20 | 39 | 2 | A:e09 @ 3.80 s |
| B | 13.95 s | 141 | 24 | 47 | 1 | B:e13 @ 3.80 s |
| C | 13.95 s | 141 | 10 | 21 | 2 | none |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e13 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 3.00 s before the matched collision<br>not at the contact: minimum range 54.18 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 7.07 m/s (> 1.50) |
| A:track_002 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>at the contact: minimum range 1.67 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.35 m/s over 1.8 s |
| B:track_001 | A | ASSOCIATED | 0.90 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>at the contact: minimum range 0.41 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.68 m/s over 1.8 s |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Global graph

53 nodes, 105 edges; 1 merged node(s): g21 COLLISION(A,B) from A:e09 + B:e13.

### Event sequence (global time)

- `-3.80` MOVING_START(A); MOVING_START(B)
- `-3.00` TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- `-2.60` STRONG_THROTTLE_START(B)
- `-2.00` STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0)
- `-1.85` TRACK_APPEARED(B,A); CLOSING_START(B,A)
- `-1.80` TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-1.70` STOP_SIGN_DETECTED_END(B,B:sign-0)
- `-1.15` PREDICTED_PATH_CONFLICT_START(A,B)
- `-0.85` BRAKE_START(B)
- `-0.70` PREDICTED_PATH_CONFLICT_START(B,A)
- `-0.30` BRAKE_END(B)
- `-0.20` EGO_PATH_ENTRY(B,A)
- `-0.05` TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); EGO_PATH_ENTRY(A,A:track_001)
- `+0.05` EGO_PATH_EXIT(A,A:track_001); STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.25` PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.30` EGO_PATH_ENTRY(A,A:track_001)
- `+0.50` EGO_PATH_EXIT(A,A:track_001)
- `+0.80` STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- `+1.05` EGO_PATH_EXIT(B,A)
- `+1.70` TRACK_LOST(B,A)
- `+6.75` STOP_SIGN_DETECTED_START(A,A:sign-1)
- `+7.75` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 3.80 s before the matched collision, A started moving (already the case when first observed).
- 3.80 s before the matched collision, B started moving (already the case when first observed).
- 3.00 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 3.00 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.60 s before the matched collision, B started applying strong throttle.
- 2.00 s before the matched collision, B stopped applying strong throttle.
- 2.00 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the matched collision, B's radar started tracking A.
- 1.85 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.80 s before the matched collision, B's time-to-contact with A became critical.
- 1.70 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.15 s before the matched collision, A predicted a path conflict with B (close approach ahead if both keep their motion).
- 0.85 s before the matched collision, B started braking.
- 0.70 s before the matched collision, B predicted a path conflict with A (close approach ahead if both keep their motion).
- 0.30 s before the matched collision, B released the brake.
- 0.20 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.05 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, B started braking hard.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.25 s after the matched collision, B stopped predicting a path conflict with A.
- 0.25 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the matched collision, B observed A stop closing in.
- 0.30 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.50 s after the matched collision, A observed unidentified object A:track_001 leave its forward path corridor.
- 0.80 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.80 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 1.05 s after the matched collision, B observed A leave its forward path corridor.
- 1.70 s after the matched collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 6.75 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 7.75 s after the matched collision, A stopped moving.
- 7.75 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.80 s) C's radar started tracking unidentified object C:track_001.
- (unaligned, C local time 0.80 s) C's radar started tracking unidentified object C:track_002.
- (unaligned, C local time 0.80 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.80 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 2.80 s) C's camera established a STOP sign detection (unidentified object C:sign-0) (the detector judged it not relevant to its path).
- (unaligned, C local time 2.80 s) C's camera stopped detecting STOP sign unidentified object C:sign-0.
- (unaligned, C local time 2.95 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 3.85 s) C observed unidentified object C:track_002 start closing in.
- (unaligned, C local time 5.00 s) C observed unidentified object C:track_001 enter its forward path corridor.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- STRONG_THROTTLE_END(B); STOP_SIGN_DETECTED_START(B,B:sign-0)
- TRACK_APPEARED(B,A); CLOSING_START(B,A)
- TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); EGO_PATH_ENTRY(A,A:track_001)
- EGO_PATH_EXIT(A,A:track_001); STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(B); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 0.80 s)
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- PREDICTED_PATH_CONFLICT of track_002, since A:e07 (t = 2.65 s); the track was lost at 3.75 s
- STOP_SIGN_DETECTED of sign-1, since A:e18 (t = 10.55 s)
- STOP, since A:e20 (t = 11.55 s)
B:
- BRAKE, since B:e16 (t = 3.85 s)
- HARD_BRAKE, since B:e17 (t = 3.85 s)
- STOP, since B:e19 (t = 4.00 s)
C:
- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_001, since C:e04 (t = 0.80 s)
- CLOSING of track_002, since C:e09 (t = 3.85 s)
- EGO_PATH of track_001, since C:e10 (t = 5.00 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 4.60 s -> 4.60 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 10.55 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: A:e20
B:
- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
C:
- STOP sign sign-0: detected 2.80 s -> 2.80 s; relevant to the path: False; STOP_START inside: none

### Perceived state just before each collision report

- A A:e09 at 3.80 s (local): ego: MOVING; track_001: VISIBLE, CLOSING; lost (states UNKNOWN): track_002
- B B:e13 at 3.80 s (local): ego: MOVING; track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT; sign-0: STOP sign not visible, known

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 3.75 s (A:e08): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)
B:
- lost with no state active: track_001
C:
- no track was lost

## Uncertainty and limitations

- A:track_001 stays anonymous: not at the contact: minimum range 54.18 m in the last 0.50 s (needs <= 3.50 m); track speed disagrees with B's own speed: RMSE 7.07 m/s (> 1.50).
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
    "hard_brake_threshold": 0.9,
    "strong_throttle_threshold": 0.8,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_ttc_s": 2.0,
    "path_half_width_m": 1.5,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
    "conflict_horizon_s": 4.0,
    "conflict_distance_m": 1.5,
    "conflict_release_horizon_s": 5.0,
    "conflict_release_distance_m": 2.5,
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
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
