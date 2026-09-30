# Reconstruction report - S03/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.15 s | 153 | 10 | 15 | 1 | A:e06 @ 4.25 s |
| B | 15.15 s | 153 | 17 | 37 | 1 | B:e08 @ 4.25 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e06 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>not at the contact: last seen 0.90 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.45 m/s over 1.3 s |
| B:track_001 | A | ASSOCIATED | 0.84 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>at the contact: minimum range 0.93 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.89 m/s over 2.1 s |

## Global graph

26 nodes, 59 edges; 1 merged node(s): g13 COLLISION(A,B) from A:e06 + B:e08.

### Event sequence (global time)

- `-4.25` MOVING_START(A); MOVING_START(B)
- `-3.10` STRONG_THROTTLE_START(B)
- `-2.20` TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- `-2.10` TRACK_APPEARED(B,A); CLOSING_START(B,A)
- `-1.90` CRITICAL_TTC_START(A,A:track_001); CRITICAL_TTC_START(B,A)
- `-1.85` STRONG_THROTTLE_END(B)
- `-0.90` TRACK_LOST(A,A:track_001)
- `-0.15` EGO_PATH_ENTRY(B,A)
- `+0.00` COLLISION(A,B); STRONG_THROTTLE_START(B)
- `+0.05` CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- `+0.30` MOVING_END(B); STOP_START(B)
- `+0.45` EGO_PATH_EXIT(B,A)
- `+0.65` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 3.10 s before the matched collision, B started applying strong throttle.
- 2.20 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 2.20 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 2.10 s before the matched collision, B's radar started tracking A.
- 2.10 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.90 s before the matched collision, A's time-to-contact with unidentified object A:track_001 became critical.
- 1.90 s before the matched collision, B's time-to-contact with A became critical.
- 1.85 s before the matched collision, B stopped applying strong throttle.
- 0.90 s before the matched collision, A's radar lost unidentified object A:track_001.
- 0.15 s before the matched collision, B observed A enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- At the matched collision, B started applying strong throttle.
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
- 0.65 s after the matched collision, A stopped moving.
- 0.65 s after the matched collision, A came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED(B,A); CLOSING_START(B,A)
- CRITICAL_TTC_START(A,A:track_001); CRITICAL_TTC_START(B,A)
- COLLISION(A,B); STRONG_THROTTLE_START(B)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 2.05 s); the track was lost at 3.35 s
- CRITICAL_TTC of track_001, since A:e04 (t = 2.35 s); the track was lost at 3.35 s
- BRAKE, since A:e07 (t = 4.30 s)
- HARD_BRAKE, since A:e08 (t = 4.30 s)
- STOP, since A:e10 (t = 4.90 s)
B:
- BRAKE, since B:e13 (t = 4.30 s)
- HARD_BRAKE, since B:e14 (t = 4.30 s)
- STOP, since B:e16 (t = 4.55 s)

### Sign detection windows

A:
- none
B:
- none

## Uncertainty and limitations

- A:track_001 stays anonymous: not at the contact: last seen 0.90 s before the matched collision (window 0.50 s).
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
    "path_half_width_m": 1.5
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
