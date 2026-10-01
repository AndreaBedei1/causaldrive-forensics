# Reconstruction report - S08/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.15 s | 153 | 18 | 31 | 2 | A:e12 @ 4.25 s |
| B | 15.15 s | 153 | 22 | 51 | 2 | B:e12 @ 4.25 s |
| C | 15.15 s | 153 | 22 | 38 | 2 | none |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 4.25 | -4.25 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 4.20 s before the matched collision<br>not at the contact: minimum range 11.23 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 8.94 m/s (> 1.50) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>not at the contact: last seen 0.90 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.45 m/s over 1.3 s |
| B:track_001 | A | ASSOCIATED | 0.84 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>at the contact: minimum range 0.93 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.89 m/s over 2.1 s |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.05 s before the matched collision<br>not at the contact: minimum range 14.00 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with A's own speed: RMSE 7.21 m/s (> 1.50) |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Global graph

61 nodes, 101 edges; 1 merged node(s): g23 COLLISION(A,B) from A:e12 + B:e12.

### Event sequence (global time)

- `-4.25` MOVING_START(A); MOVING_START(B)
- `-4.20` TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- `-3.10` STRONG_THROTTLE_START(B)
- `-2.20` TRACK_APPEARED(A,A:track_002); CLOSING_START(A,A:track_002)
- `-2.15` CRITICAL_TTC_START(A,A:track_001)
- `-2.10` TRACK_APPEARED(B,A); CLOSING_START(B,A)
- `-2.05` TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_002)
- `-1.90` CRITICAL_TTC_START(A,A:track_002); CRITICAL_TTC_START(B,A)
- `-1.85` STRONG_THROTTLE_END(B)
- `-1.70` PREDICTED_PATH_CONFLICT_START(A,A:track_002)
- `-1.55` CRITICAL_TTC_END(A,A:track_001)
- `-1.40` PREDICTED_PATH_CONFLICT_START(B,A)
- `-0.90` TRACK_LOST(A,A:track_002)
- `-0.80` CRITICAL_TTC_START(A,A:track_001)
- `-0.20` TRACK_LOST(B,B:track_002)
- `-0.15` EGO_PATH_ENTRY(B,A)
- `+0.00` COLLISION(A,B); STRONG_THROTTLE_START(B)
- `+0.05` PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- `+0.30` MOVING_END(B); STOP_START(B)
- `+0.45` EGO_PATH_EXIT(B,A)
- `+0.50` CRITICAL_TTC_END(A,A:track_001)
- `+0.65` CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 4.20 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 4.20 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 3.10 s before the matched collision, B started applying strong throttle.
- 2.20 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 2.20 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 2.15 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 2.10 s before the matched collision, B's radar started tracking A.
- 2.10 s before the matched collision, B observed A start closing in (already the case when first observed).
- 2.05 s before the matched collision, B's radar started tracking unidentified object B:track_002.
- 2.05 s before the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 1.90 s before the matched collision, A's time-to-contact with unidentified object A:track_002 became critical.
- 1.90 s before the matched collision, B's time-to-contact with A became critical.
- 1.85 s before the matched collision, B stopped applying strong throttle.
- 1.70 s before the matched collision, A predicted a path conflict with unidentified object A:track_002 (close approach ahead if both keep their motion).
- 1.55 s before the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 1.40 s before the matched collision, B predicted a path conflict with A (close approach ahead if both keep their motion).
- 0.90 s before the matched collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 0.80 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 0.20 s before the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.15 s before the matched collision, B observed A enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, B stopped predicting a path conflict with A.
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.30 s after the matched collision, B stopped moving.
- 0.30 s after the matched collision, B came to a stop.
- 0.45 s after the matched collision, B observed A leave its forward path corridor.
- 0.50 s after the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.65 s after the matched collision, A observed unidentified object A:track_001 stop closing in.
- 0.65 s after the matched collision, A stopped moving.
- 0.65 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.05 s) C's radar started tracking unidentified object C:track_001.
- (unaligned, C local time 0.05 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 2.15 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.35 s) C started braking.
- (unaligned, C local time 2.35 s) C started braking hard.
- (unaligned, C local time 2.75 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 2.85 s) C stopped moving.
- (unaligned, C local time 2.85 s) C came to a stop.
- (unaligned, C local time 3.00 s) C's radar started tracking unidentified object C:track_002.
- (unaligned, C local time 3.00 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 3.35 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 3.55 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 4.15 s) C predicted a path conflict with unidentified object C:track_001 (close approach ahead if both keep their motion).
- (unaligned, C local time 4.20 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 4.55 s) C observed unidentified object C:track_002 stop closing in.
- (unaligned, C local time 4.70 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 4.85 s) C stopped predicting a path conflict with unidentified object C:track_001.
- (unaligned, C local time 4.90 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 14.35 s) C stopped braking hard.
- (unaligned, C local time 14.35 s) C released the brake.
- (unaligned, C local time 14.35 s) C started applying strong throttle.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED(A,A:track_002); CLOSING_START(A,A:track_002)
- TRACK_APPEARED(B,A); CLOSING_START(B,A)
- TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_002)
- CRITICAL_TTC_START(A,A:track_002); CRITICAL_TTC_START(B,A)
- COLLISION(A,B); STRONG_THROTTLE_START(B)
- PREDICTED_PATH_CONFLICT_END(B,A); CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_002, since A:e05 (t = 2.05 s); the track was lost at 3.35 s
- CRITICAL_TTC of track_002, since A:e07 (t = 2.35 s); the track was lost at 3.35 s
- PREDICTED_PATH_CONFLICT of track_002, since A:e08 (t = 2.55 s); the track was lost at 3.35 s
- BRAKE, since A:e13 (t = 4.30 s)
- HARD_BRAKE, since A:e14 (t = 4.30 s)
- STOP, since A:e18 (t = 4.90 s)
B:
- CLOSING of track_002, since B:e06 (t = 2.20 s); the track was lost at 4.05 s
- BRAKE, since B:e18 (t = 4.30 s)
- HARD_BRAKE, since B:e19 (t = 4.30 s)
- STOP, since B:e21 (t = 4.55 s)
C:
- STOP, since C:e09 (t = 2.85 s)
- STRONG_THROTTLE, since C:e22 (t = 14.35 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

### Perceived state just before each collision report

- A A:e12 at 4.25 s (local): ego: MOVING; track_001: VISIBLE, CLOSING, CRITICAL_TTC; lost (states UNKNOWN): track_002
- B B:e12 at 4.25 s (local): ego: MOVING; track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT; lost (states UNKNOWN): track_002

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_002 at 3.35 s (A:e10): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_002 at 4.05 s (B:e10): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
C:
- no track was lost

## Uncertainty and limitations

- A:track_001 stays anonymous: not at the contact: minimum range 11.23 m in the last 0.50 s (needs <= 3.50 m); track speed disagrees with B's own speed: RMSE 8.94 m/s (> 1.50).
- A:track_002 stays anonymous: not at the contact: last seen 0.90 s before the matched collision (window 0.50 s).
- B:track_002 stays anonymous: not at the contact: minimum range 14.00 m in the last 0.50 s (needs <= 3.50 m); track speed disagrees with A's own speed: RMSE 7.21 m/s (> 1.50).
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
