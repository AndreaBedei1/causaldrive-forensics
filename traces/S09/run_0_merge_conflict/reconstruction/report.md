# Reconstruction report - S09/run_0_merge_conflict

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.95 s | 151 | 22 | 54 | 3 | A:e11 @ 1.80 s |
| B | 14.95 s | 151 | 16 | 26 | 2 | B:e11 @ 1.80 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e11 | 1.80 | -1.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e11 | 1.80 | -1.80 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1247.19 vs 1247.19 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.63 | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.80 s before the matched collision<br>at the contact: minimum range 1.01 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 1.45 m/s over 1.8 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>not at the contact: minimum range 36.18 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 6.69 m/s (> 1.50) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>not at the contact: minimum range 38.37 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with B's own speed: RMSE 6.74 m/s (> 1.50) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>at the contact: minimum range 2.22 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed disagrees with A's own speed: RMSE 4.97 m/s (> 1.50) |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>not at the contact: minimum range 14.50 m in the last 0.50 s (needs <= 3.50 m)<br>track speed disagrees with A's own speed: RMSE 6.98 m/s (> 1.50) |

## Global graph

37 nodes, 117 edges; 1 merged node(s): g21 COLLISION(A,B) from A:e11 + B:e11.

### Event sequence (global time)

- `-1.80` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- `-1.60` TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,A:track_003); TRACK_APPEARED(B,B:track_001); TRACK_APPEARED(B,B:track_002); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001)
- `-1.40` PREDICTED_PATH_CONFLICT_START(B,B:track_001)
- `-1.15` PREDICTED_PATH_CONFLICT_START(A,B)
- `-1.00` STRONG_THROTTLE_START(B)
- `-0.35` EGO_PATH_ENTRY(A,B)
- `-0.20` STRONG_THROTTLE_END(B)
- `-0.15` TRACK_LOST(B,B:track_001)
- `+0.00` COLLISION(A,B)
- `+0.05` BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- `+0.10` PREDICTED_PATH_CONFLICT_END(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TRACK_LOST(B,B:track_002)
- `+0.55` PREDICTED_PATH_CONFLICT_START(A,B)
- `+0.70` CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003); MOVING_END(A); STOP_START(A)
- `+0.75` MOVING_END(B); STOP_START(B)
- `+1.15` PREDICTED_PATH_CONFLICT_END(A,B)

### What happened, in plain language

- 1.80 s before the matched collision, A started moving (already the case when first observed).
- 1.80 s before the matched collision, B started moving (already the case when first observed).
- 1.80 s before the matched collision, A's radar started tracking B.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_003.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_001.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_002.
- 1.60 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical (already the case when first observed).
- 1.40 s before the matched collision, B predicted a path conflict with unidentified object B:track_001 (close approach ahead if both keep their motion).
- 1.15 s before the matched collision, A predicted a path conflict with B (close approach ahead if both keep their motion).
- 1.00 s before the matched collision, B started applying strong throttle.
- 0.35 s before the matched collision, A observed B enter its forward path corridor.
- 0.20 s before the matched collision, B stopped applying strong throttle.
- 0.15 s before the matched collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 1247, B: 1247 N*s).
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.10 s after the matched collision, A stopped predicting a path conflict with B.
- 0.10 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.10 s after the matched collision, A observed B stop closing in.
- 0.10 s after the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the matched collision, A predicted a path conflict with B (close approach ahead if both keep their motion).
- 0.70 s after the matched collision, A observed unidentified object A:track_002 stop closing in.
- 0.70 s after the matched collision, A observed unidentified object A:track_003 stop closing in.
- 0.70 s after the matched collision, A stopped moving.
- 0.70 s after the matched collision, A came to a stop.
- 0.75 s after the matched collision, B stopped moving.
- 0.75 s after the matched collision, B came to a stop.
- 1.15 s after the matched collision, A stopped predicting a path conflict with B.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B)
- TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,A:track_003); TRACK_APPEARED(B,B:track_001); TRACK_APPEARED(B,B:track_002); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001)
- BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- PREDICTED_PATH_CONFLICT_END(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); TRACK_LOST(B,B:track_002)
- CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003); MOVING_END(A); STOP_START(A)
- MOVING_END(B); STOP_START(B)

### States still active when observation ended

A:
- EGO_PATH of track_001, since A:e10 (t = 1.45 s)
- BRAKE, since A:e12 (t = 1.85 s)
- HARD_BRAKE, since A:e13 (t = 1.85 s)
- STOP, since A:e21 (t = 2.50 s)
B:
- CLOSING of track_001, since B:e04 (t = 0.20 s); the track was lost at 1.65 s
- CLOSING of track_002, since B:e05 (t = 0.20 s); the track was lost at 1.90 s
- CRITICAL_TTC of track_001, since B:e06 (t = 0.20 s); the track was lost at 1.65 s
- PREDICTED_PATH_CONFLICT of track_001, since B:e07 (t = 0.40 s); the track was lost at 1.65 s
- BRAKE, since B:e12 (t = 1.85 s)
- HARD_BRAKE, since B:e13 (t = 1.85 s)
- STOP, since B:e16 (t = 2.55 s)

### Sign detection windows

A:
- none
B:
- none

### Perceived state just before each collision report

- A A:e11 at 1.80 s (local): ego: MOVING; track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT; track_002: VISIBLE, CLOSING; track_003: VISIBLE, CLOSING
- B B:e11 at 1.80 s (local): ego: MOVING; track_002: VISIBLE, CLOSING; lost (states UNKNOWN): track_001

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- no track was lost
B:
- track_001 at 1.65 s (B:e10): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 1.90 s (B:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Uncertainty and limitations

- A:track_002 stays anonymous: not at the contact: minimum range 36.18 m in the last 0.50 s (needs <= 3.50 m); track speed disagrees with B's own speed: RMSE 6.69 m/s (> 1.50).
- A:track_003 stays anonymous: not at the contact: minimum range 38.37 m in the last 0.50 s (needs <= 3.50 m); track speed disagrees with B's own speed: RMSE 6.74 m/s (> 1.50).
- B:track_001 stays anonymous: track speed disagrees with A's own speed: RMSE 4.97 m/s (> 1.50).
- B:track_002 stays anonymous: not at the contact: minimum range 14.50 m in the last 0.50 s (needs <= 3.50 m); track speed disagrees with A's own speed: RMSE 6.98 m/s (> 1.50).
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
