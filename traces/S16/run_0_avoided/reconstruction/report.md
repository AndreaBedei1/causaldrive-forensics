# Reconstruction report - S16/run_0_avoided

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 9.95 s | 101 | 8 | 7 | 0 | A:e05 @ 5.15 s |
| B | 9.95 s | 101 | 17 | 29 | 1 | B:e12 @ 5.15 s |
| C | 9.95 s | 101 | 3 | 2 | 0 | none |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e05 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e12 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| B:track_001 | A | ASSOCIATED | 0.95 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>at the contact: minimum range 0.52 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.47 m/s over 3.0 s |

## Global graph

27 nodes, 43 edges; 1 merged node(s): g16 COLLISION(A,B) from A:e05 + B:e12.

### Event sequence (global time)

- `-5.15` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(B,A)
- `-4.45` STRONG_THROTTLE_START(A); CLOSING_START(B,A)
- `-4.40` CRITICAL_TTC_START(B,A)
- `-3.80` STRONG_THROTTLE_START(B)
- `-3.75` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `-3.35` STRONG_THROTTLE_END(A)
- `-2.65` STRONG_THROTTLE_END(B)
- `-1.20` BRAKE_START(A)
- `-0.90` CLOSING_START(B,A)
- `-0.80` CRITICAL_TTC_START(B,A)
- `-0.40` BRAKE_START(B)
- `+0.00` COLLISION(A,B)
- `+0.05` CRITICAL_TTC_END(B,A); CLOSING_END(B,A); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- `+0.45` MOVING_END(B); STOP_START(B)
- `+0.60` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 5.15 s before the matched collision, A started moving (already the case when first observed).
- 5.15 s before the matched collision, B started moving (already the case when first observed).
- 5.15 s before the matched collision, B's radar started tracking A.
- 4.45 s before the matched collision, A started applying strong throttle.
- 4.45 s before the matched collision, B observed A start closing in.
- 4.40 s before the matched collision, B's time-to-contact with A became critical.
- 3.80 s before the matched collision, B started applying strong throttle.
- 3.75 s before the matched collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the matched collision, B observed A stop closing in.
- 3.35 s before the matched collision, A stopped applying strong throttle.
- 2.65 s before the matched collision, B stopped applying strong throttle.
- 1.20 s before the matched collision, A started braking.
- 0.90 s before the matched collision, B observed A start closing in.
- 0.80 s before the matched collision, B's time-to-contact with A became critical.
- 0.40 s before the matched collision, B started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.60 s after the matched collision, A stopped moving.
- 0.60 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.30 s) C stopped moving.
- (unaligned, C local time 0.30 s) C came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(B,A)
- STRONG_THROTTLE_START(A); CLOSING_START(B,A)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A); HARD_BRAKE_START(A); HARD_BRAKE_START(B)
- MOVING_END(B); STOP_START(B)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- BRAKE, since A:e04 (t = 3.95 s)
- HARD_BRAKE, since A:e06 (t = 5.20 s)
- STOP, since A:e08 (t = 5.75 s)
B:
- BRAKE, since B:e11 (t = 4.75 s)
- HARD_BRAKE, since B:e15 (t = 5.20 s)
- STOP, since B:e17 (t = 5.60 s)
C:
- STOP, since C:e03 (t = 0.30 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

## Uncertainty and limitations

- A built no radar track: nothing moving stayed in its forward radar view long enough, so A has no perception of the others.
- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
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
