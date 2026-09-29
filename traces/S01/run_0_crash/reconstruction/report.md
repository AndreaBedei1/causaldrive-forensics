# Reconstruction report - S01/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` only (vehicle-local files). `ground_truth/` was not read; the privileged comparison, if run, is in `evaluation/`.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 120 | 8 | 10 | 1 | A:e07 @ 6.50 s |
| B | 11.95 s | 120 | 3 | 2 | 0 | B:e03 @ 6.50 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>at the contact: minimum range 0.78 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.21 m/s over 3.0 s |

## Global graph

10 nodes, 12 edges; 1 merged node(s): g09 COLLISION(A,B) from A:e07 + B:e03.

### Event sequence (global time)

- `-6.50` TRACK_APPEARED(A,B)
- `-6.05` CLOSING(A,B)
- `-5.35` THROTTLE_ONSET(A)
- `-2.55` BRAKE_EPISODE(B)
- `-2.25` CLOSING(A,B)
- `-1.50` CRITICAL_TTC(A,B)
- `-1.35` FULL_STOP(B)
- `-0.95` BRAKE_EPISODE(A)
- `+0.00` COLLISION(A,B)
- `+0.05` FULL_STOP(A)

### What happened, in plain language

- 6.50 s before the matched collision, A's radar started tracking B at 23.5 m, ahead, moving at 13.1 m/s, inside its path.
- 6.05 s before the matched collision, A observed B closing at 1.0 m/s from 23.2 m (peak 4.2 m/s, down to 20.5 m).
- 5.35 s before the matched collision, A applied strong throttle (0.86 at 12.6 m/s).
- 2.55 s before the matched collision, B braked for 8.00 s (peak 1.00, mean 1.00), from 13.8 to 0.0 m/s, still braking when its recording ended.
- 2.25 s before the matched collision, A observed B closing at 1.4 m/s from 21.6 m (peak 13.7 m/s, down to 0.8 m).
- 1.50 s before the matched collision, A's time-to-contact with B fell to 1.8 s at 17.9 m (minimum 0.1 s).
- 1.35 s before the matched collision, B came to a full stop and stayed stopped until its recording ended.
- 0.95 s before the matched collision, A braked for 6.40 s (peak 1.00, mean 0.98), from 13.6 to 0.0 m/s, still braking when its recording ended.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- 0.05 s after the matched collision, A came to a full stop and stayed stopped until its recording ended.

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
