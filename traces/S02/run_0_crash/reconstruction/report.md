# Reconstruction report - S02/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` only (vehicle-local files). `ground_truth/` was not read; the privileged comparison, if run, is in `evaluation/`.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.15 s | 152 | 8 | 10 | 1 | A:e07 @ 4.25 s |
| B | 15.15 s | 152 | 4 | 3 | 0 | B:e03 @ 4.25 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5953.86 vs 5953.86 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 5953.86 vs 5953.86 N*s)<br>tracked for 4.25 s before the matched collision<br>at the contact: minimum range 0.85 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.40 m/s over 3.0 s |

## Global graph

11 nodes, 13 edges; 1 merged node(s): g09 COLLISION(A,B) from A:e07 + B:e03.

### Event sequence (global time)

- `-4.25` TRACK_APPEARED(A,B); CLOSING(A,B)
- `-3.10` THROTTLE_ONSET(A)
- `-1.45` CRITICAL_TTC(A,B)
- `-1.10` BRAKE_EPISODE(B)
- `-1.05` ENTERED_EGO_PATH(A,B)
- `-0.40` BRAKE_EPISODE(A)
- `+0.00` BRAKE_EPISODE(B); COLLISION(A,B)
- `+0.60` FULL_STOP(A)
- `+0.75` FULL_STOP(B)

### What happened, in plain language

- 4.25 s before the matched collision, A's radar started tracking B at 24.6 m, 8 deg to the left, moving at 8.0 m/s.
- 4.25 s before the matched collision, A observed B closing at 5.6 m/s from 24.6 m (peak 7.9 m/s, down to 0.9 m).
- 3.10 s before the matched collision, A applied strong throttle (0.86 at 12.6 m/s).
- 1.45 s before the matched collision, A's time-to-contact with B fell to 2.0 s at 9.6 m (minimum 0.2 s).
- 1.10 s before the matched collision, B braked for 0.45 s (peak 0.73, mean 0.48), from 8.7 to 6.6 m/s, then released the brake.
- 1.05 s before the matched collision, A observed B move into its path from the left (7.5 m ahead, lateral speed 1.2 m/s).
- 0.40 s before the matched collision, A braked for 11.30 s (peak 1.00, mean 0.99), from 13.4 to 0.0 m/s, still braking when its recording ended.
- At the matched collision, B braked for 10.90 s (peak 1.00, mean 1.00), from 9.6 to 0.0 m/s, still braking when its recording ended.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5954, B: 5954 N*s).
- 0.60 s after the matched collision, A came to a full stop and stayed stopped until its recording ended.
- 0.75 s after the matched collision, B came to a full stop and stayed stopped until its recording ended.

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
    "throttle_onset_threshold": 0.8,
    "full_stop_speed_mps": 0.3,
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
