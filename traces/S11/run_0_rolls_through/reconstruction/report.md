# Reconstruction report - S11/run_0_rolls_through

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.95 s | 161 | 13 | 26 | 1 | A:e07 @ 5.50 s |
| B | 15.95 s | 161 | 24 | 40 | 1 | B:e16 @ 5.50 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 5.50 | -5.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 5.50 | -5.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 8859.58 vs 8859.58 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.94 | A and B both reported collision_001 (peak impulse 8859.58 vs 8859.58 N*s)<br>tracked for 2.75 s before the matched collision<br>at the contact: minimum range 1.59 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.51 m/s over 2.7 s |
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 8859.58 vs 8859.58 N*s)<br>tracked for 1.55 s before the matched collision<br>at the contact: minimum range 0.62 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.46 m/s over 1.5 s |

## Global graph

36 nodes, 77 edges; 1 merged node(s): g22 COLLISION(A,B) from A:e07 + B:e16.

### Event sequence (global time)

- `-5.50` MOVING_START(A); MOVING_START(B)
- `-4.25` STRONG_THROTTLE_START(B)
- `-3.65` STRONG_THROTTLE_END(B)
- `-3.55` BRAKE_START(B); HARD_BRAKE_START(B)
- `-3.40` STOP_SIGN_DETECTED_START(B,B:sign-1)
- `-3.30` HARD_BRAKE_END(B)
- `-3.05` STOP_SIGN_DETECTED_END(B,B:sign-1)
- `-2.85` BRAKE_END(B)
- `-2.75` TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- `-2.50` STRONG_THROTTLE_START(B)
- `-2.25` STRONG_THROTTLE_END(B)
- `-1.80` CRITICAL_TTC_START(A,B)
- `-1.55` TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A); CRITICAL_TTC_START(B,A)
- `-0.20` EGO_PATH_ENTRY(B,A)
- `-0.05` EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
- `+0.05` STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- `+0.20` MOVING_END(B); STOP_START(B)
- `+0.25` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.55` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 5.50 s before the matched collision, A started moving (already the case when first observed).
- 5.50 s before the matched collision, B started moving (already the case when first observed).
- 4.25 s before the matched collision, B started applying strong throttle.
- 3.65 s before the matched collision, B stopped applying strong throttle.
- 3.55 s before the matched collision, B started braking.
- 3.55 s before the matched collision, B started braking hard.
- 3.40 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- 3.30 s before the matched collision, B stopped braking hard.
- 3.05 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 2.85 s before the matched collision, B released the brake.
- 2.75 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 2.75 s before the matched collision, A observed B start closing in (already the case when first observed).
- 2.50 s before the matched collision, B started applying strong throttle.
- 2.25 s before the matched collision, B stopped applying strong throttle.
- 1.80 s before the matched collision, A's time-to-contact with B became critical.
- 1.55 s before the matched collision, B's radar started tracking A, which appeared on its left.
- 1.55 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.55 s before the matched collision, B's time-to-contact with A became critical (already the case when first observed).
- 0.20 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A observed B enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 8860, B: 8860 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.20 s after the matched collision, B stopped moving.
- 0.20 s after the matched collision, B came to a stop.
- 0.25 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.25 s after the matched collision, B observed A stop closing in.
- 0.55 s after the matched collision, A stopped moving.
- 0.55 s after the matched collision, A came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- BRAKE_START(B); HARD_BRAKE_START(B)
- TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B)
- TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A); CRITICAL_TTC_START(B,A)
- EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B)
- COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
- STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 2.75 s); the track was lost at 5.45 s
- CRITICAL_TTC of track_001, since A:e04 (t = 3.70 s); the track was lost at 5.45 s
- EGO_PATH of track_001, since A:e05 (t = 5.45 s); the track was lost at 5.45 s
- BRAKE, since A:e10 (t = 5.55 s)
- HARD_BRAKE, since A:e11 (t = 5.55 s)
- STOP, since A:e13 (t = 6.05 s)
B:
- EGO_PATH of track_001, since B:e15 (t = 5.30 s)
- BRAKE, since B:e19 (t = 5.55 s)
- HARD_BRAKE, since B:e20 (t = 5.55 s)
- STOP, since B:e22 (t = 5.70 s)

### Sign detection windows

A:
- none
B:
- STOP sign sign-1: detected 2.10 s -> 2.45 s; relevant to the path: False; STOP_START inside: none

### Perceived state just before each collision report

- A A:e07 at 5.50 s (local): ego: MOVING; track lost, states UNKNOWN: track_001
- B B:e16 at 5.50 s (local): ego: MOVING; track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH; sign-1: STOP sign known

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 5.45 s (A:e06): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
B:
- no track was lost

## Uncertainty and limitations

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
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
