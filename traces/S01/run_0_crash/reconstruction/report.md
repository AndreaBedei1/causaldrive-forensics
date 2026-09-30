# Reconstruction report - S01/run_0_crash

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 11.95 s | 121 | 15 | 26 | 1 | A:e10 @ 6.50 s |
| B | 11.95 s | 121 | 8 | 10 | 0 | B:e08 @ 6.50 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e10 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e08 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>at the contact: minimum range 0.78 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.21 m/s over 3.0 s |

## Global graph

22 nodes, 35 edges; 1 merged node(s): g17 COLLISION(A,B) from A:e10 + B:e08.

### Event sequence (global time)

- `-6.50` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B)
- `-6.10` STRONG_THROTTLE_START(B)
- `-6.05` CLOSING_START(A,B)
- `-5.35` STRONG_THROTTLE_START(A)
- `-5.15` STRONG_THROTTLE_END(A)
- `-4.90` CLOSING_END(A,B)
- `-4.75` STRONG_THROTTLE_END(B)
- `-2.55` BRAKE_START(B); HARD_BRAKE_START(B)
- `-2.25` CLOSING_START(A,B)
- `-1.50` CRITICAL_TTC_START(A,B)
- `-1.35` MOVING_END(B); STOP_START(B)
- `-0.95` BRAKE_START(A)
- `+0.00` COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- `+0.05` MOVING_END(A); STOP_START(A); HARD_BRAKE_START(A)

### What happened, in plain language

- 6.50 s before the matched collision, A started moving (already the case when first observed).
- 6.50 s before the matched collision, B started moving (already the case when first observed).
- 6.50 s before the matched collision, A's radar started tracking B.
- 6.10 s before the matched collision, B started applying strong throttle.
- 6.05 s before the matched collision, A observed B start closing in.
- 5.35 s before the matched collision, A started applying strong throttle.
- 5.15 s before the matched collision, A stopped applying strong throttle.
- 4.90 s before the matched collision, A observed B stop closing in.
- 4.75 s before the matched collision, B stopped applying strong throttle.
- 2.55 s before the matched collision, B started braking.
- 2.55 s before the matched collision, B started braking hard.
- 2.25 s before the matched collision, A observed B start closing in.
- 1.50 s before the matched collision, A's time-to-contact with B became critical.
- 1.35 s before the matched collision, B stopped moving.
- 1.35 s before the matched collision, B came to a stop.
- 0.95 s before the matched collision, A started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- At the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A observed B stop closing in.
- 0.05 s after the matched collision, A stopped moving.
- 0.05 s after the matched collision, A came to a stop.
- 0.05 s after the matched collision, A started braking hard.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,B)
- BRAKE_START(B); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- COLLISION(A,B); CRITICAL_TTC_END(A,B); CLOSING_END(A,B)
- MOVING_END(A); STOP_START(A); HARD_BRAKE_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e09 (t = 5.55 s)
- STOP, since A:e14 (t = 6.55 s)
- HARD_BRAKE, since A:e15 (t = 6.55 s)
B:
- BRAKE, since B:e04 (t = 3.95 s)
- HARD_BRAKE, since B:e05 (t = 3.95 s)
- STOP, since B:e07 (t = 5.15 s)

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
