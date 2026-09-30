# Reconstruction report - S02/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.15 s | 153 | 14 | 20 | 1 | A:e09 @ 4.25 s |
| B | 15.15 s | 153 | 10 | 13 | 0 | B:e06 @ 4.25 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e06 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5953.86 vs 5953.86 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 5953.86 vs 5953.86 N*s)<br>tracked for 4.25 s before the matched collision<br>at the contact: minimum range 0.85 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.40 m/s over 3.0 s |

## Global graph

23 nodes, 33 edges; 1 merged node(s): g14 COLLISION(A,B) from A:e09 + B:e06.

### Event sequence (global time)

- `-4.25` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B)
- `-3.90` STRONG_THROTTLE_START(B)
- `-3.10` STRONG_THROTTLE_START(A)
- `-2.95` STRONG_THROTTLE_END(B)
- `-2.90` STRONG_THROTTLE_END(A)
- `-1.45` CRITICAL_TTC_START(A,B)
- `-1.10` BRAKE_START(B)
- `-1.05` EGO_PATH_ENTRY(A,B)
- `-0.65` BRAKE_END(B)
- `-0.40` BRAKE_START(A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); BRAKE_START(B); HARD_BRAKE_START(B)
- `+0.05` HARD_BRAKE_START(A)
- `+0.60` MOVING_END(A); STOP_START(A)
- `+0.75` MOVING_END(B); STOP_START(B)

### What happened, in plain language

- 4.25 s before the matched collision, A started moving (already the case when first observed).
- 4.25 s before the matched collision, B started moving (already the case when first observed).
- 4.25 s before the matched collision, A's radar started tracking B.
- 4.25 s before the matched collision, A observed B start closing in (already the case when first observed).
- 3.90 s before the matched collision, B started applying strong throttle.
- 3.10 s before the matched collision, A started applying strong throttle.
- 2.95 s before the matched collision, B stopped applying strong throttle.
- 2.90 s before the matched collision, A stopped applying strong throttle.
- 1.45 s before the matched collision, A's time-to-contact with B became critical.
- 1.10 s before the matched collision, B started braking.
- 1.05 s before the matched collision, A observed B enter its forward path corridor.
- 0.65 s before the matched collision, B released the brake.
- 0.40 s before the matched collision, A started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5954, B: 5954 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- At the matched collision, B started braking.
- At the matched collision, B started braking hard.
- 0.05 s after the matched collision, A started braking hard.
- 0.60 s after the matched collision, A stopped moving.
- 0.60 s after the matched collision, A came to a stop.
- 0.75 s after the matched collision, B stopped moving.
- 0.75 s after the matched collision, B came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B); CLOSING_START(A,B)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B); BRAKE_START(B); HARD_BRAKE_START(B)
- MOVING_END(A); STOP_START(A)
- MOVING_END(B); STOP_START(B)

### States still active when observation ended

A:
- EGO_PATH of track_001, since A:e07 (t = 3.20 s)
- BRAKE, since A:e08 (t = 3.85 s)
- HARD_BRAKE, since A:e12 (t = 4.30 s)
- STOP, since A:e14 (t = 4.85 s)
B:
- BRAKE, since B:e07 (t = 4.25 s)
- HARD_BRAKE, since B:e08 (t = 4.25 s)
- STOP, since B:e10 (t = 5.00 s)

### Sign detection windows

A:
- none
B:
- none

## Uncertainty and limitations

- B built no radar track: nothing moving stayed in its forward radar view long enough, so B has no perception of the others.
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
