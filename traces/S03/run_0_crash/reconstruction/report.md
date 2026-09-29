# Reconstruction report - S03/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` only (vehicle-local files). `ground_truth/` was not read; the privileged comparison, if run, is in `evaluation/`.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.15 s | 152 | 7 | 9 | 1 | A:e05 @ 4.25 s |
| B | 15.15 s | 152 | 9 | 11 | 1 | B:e07 @ 4.25 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e05 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e07 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>not at the contact: last seen 0.90 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.45 m/s over 1.3 s |
| B:track_001 | A | ASSOCIATED | 0.84 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>at the contact: minimum range 0.93 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.89 m/s over 2.1 s |

## Global graph

15 nodes, 20 edges; 1 merged node(s): g11 COLLISION(A,B) from A:e05 + B:e07.

### Event sequence (global time)

- `-3.10` THROTTLE_ONSET(B)
- `-2.20` TRACK_APPEARED(A,A:track_001); CLOSING(A,A:track_001)
- `-2.10` TRACK_APPEARED(B,A); CLOSING(B,A)
- `-1.90` CRITICAL_TTC(A,A:track_001); CRITICAL_TTC(B,A)
- `-0.90` TRACK_LOST(A,A:track_001)
- `-0.15` ENTERED_EGO_PATH(B,A)
- `+0.00` THROTTLE_ONSET(B); COLLISION(A,B)
- `+0.05` BRAKE_EPISODE(A); BRAKE_EPISODE(B)
- `+0.30` FULL_STOP(B)
- `+0.65` FULL_STOP(A)

### What happened, in plain language

- 3.10 s before the matched collision, B applied strong throttle (1.00 at 7.4 m/s).
- 2.20 s before the matched collision, A's radar started tracking unidentified object A:track_001 at 34.2 m, 56 deg to the right, moving at 10.9 m/s.
- 2.20 s before the matched collision, A observed unidentified object A:track_001 closing at 14.3 m/s from 34.2 m (peak 15.6 m/s, down to 14.4 m).
- 2.10 s before the matched collision, B's radar started tracking A at 32.7 m, 38 deg to the left, moving at 8.2 m/s.
- 2.10 s before the matched collision, B observed A closing at 14.2 m/s from 32.7 m (peak 15.6 m/s, down to 0.9 m).
- 1.90 s before the matched collision, A's time-to-contact with unidentified object A:track_001 fell to 2.0 s at 29.8 m (minimum 0.9 s).
- 1.90 s before the matched collision, B's time-to-contact with A fell to 2.0 s at 29.8 m (minimum 0.1 s).
- 0.90 s before the matched collision, A lost unidentified object A:track_001 at 14.4 m, 59 deg to the right, after tracking it for 1.3 s.
- 0.15 s before the matched collision, B observed A move into its path from the left (2.5 m ahead, lateral speed 10.7 m/s).
- At the matched collision, B applied strong throttle (1.00 at 5.2 m/s).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- 0.05 s after the matched collision, A braked for 10.85 s (peak 1.00, mean 1.00), from 8.9 to 0.0 m/s, still braking when its recording ended.
- 0.05 s after the matched collision, B braked for 10.85 s (peak 1.00, mean 1.00), from 4.4 to 0.0 m/s, still braking when its recording ended.
- 0.30 s after the matched collision, B came to a full stop and stayed stopped until its recording ended.
- 0.65 s after the matched collision, A came to a full stop and stayed stopped until its recording ended.

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
