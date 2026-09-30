# Reconstruction report - S12/run_0_b_fails_to_stop

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 15.95 s | 161 | 25 | 49 | 1 | A:e19 @ 9.70 s |
| B | 15.95 s | 161 | 30 | 67 | 3 | B:e16 @ 9.70 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e19 | 9.70 | -9.70 | reported the reference collision collision_001 |
| B | ALIGNED | B:e16 | 9.70 | -9.70 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 7339.57 vs 7339.57 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.90 | A and B both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 2.95 s before the matched collision<br>at the contact: minimum range 1.44 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.67 m/s over 2.9 s |
| B:track_001 | A | ASSOCIATED | 0.88 | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked for 1.55 s before the matched collision<br>at the contact: minimum range 1.11 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.75 m/s over 1.5 s |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 19.01 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 7339.57 vs 7339.57 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with A's own speed before the collision |

## Global graph

54 nodes, 139 edges; 1 merged node(s): g34 COLLISION(A,B) from A:e19 + B:e16.

### Event sequence (global time)

- `-9.70` MOVING_START(A); MOVING_START(B)
- `-9.05` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `-8.45` STRONG_THROTTLE_START(B)
- `-7.85` STRONG_THROTTLE_END(B)
- `-7.75` BRAKE_START(B); HARD_BRAKE_START(B)
- `-7.45` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `-7.40` HARD_BRAKE_END(B)
- `-7.05` BRAKE_END(B); BRAKE_START(A); HARD_BRAKE_START(A)
- `-6.45` STRONG_THROTTLE_START(B)
- `-6.40` STRONG_THROTTLE_END(B)
- `-6.30` MOVING_END(A); STOP_START(A)
- `-6.20` STOP_SIGN_DETECTED_START(B,B:sign-1)
- `-4.40` STOP_SIGN_DETECTED_END(B,B:sign-1)
- `-2.95` TRACK_APPEARED(A,B); CLOSING_START(A,B)
- `-1.95` HARD_BRAKE_END(A); BRAKE_END(A); STRONG_THROTTLE_START(A)
- `-1.60` STOP_END(A); MOVING_START(A)
- `-1.55` TRACK_APPEARED(B,A); CLOSING_START(B,A)
- `-1.20` CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- `-0.60` STRONG_THROTTLE_END(A)
- `-0.10` EGO_PATH_ENTRY(B,A)
- `-0.05` EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B)
- `+0.00` COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_002)
- `+0.05` STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_003); CLOSING_START(B,B:track_003)
- `+0.35` MOVING_END(B); STOP_START(B)
- `+0.40` CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003)
- `+0.45` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.50` MOVING_END(A); STOP_START(A)

### What happened, in plain language

- 9.70 s before the matched collision, A started moving (already the case when first observed).
- 9.70 s before the matched collision, B started moving (already the case when first observed).
- 9.05 s before the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 8.45 s before the matched collision, B started applying strong throttle.
- 7.85 s before the matched collision, B stopped applying strong throttle.
- 7.75 s before the matched collision, B started braking.
- 7.75 s before the matched collision, B started braking hard.
- 7.45 s before the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.40 s before the matched collision, B stopped braking hard.
- 7.05 s before the matched collision, B released the brake.
- 7.05 s before the matched collision, A started braking.
- 7.05 s before the matched collision, A started braking hard.
- 6.45 s before the matched collision, B started applying strong throttle.
- 6.40 s before the matched collision, B stopped applying strong throttle.
- 6.30 s before the matched collision, A stopped moving.
- 6.30 s before the matched collision, A came to a stop.
- 6.20 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- 4.40 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 2.95 s before the matched collision, A's radar started tracking B.
- 2.95 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.95 s before the matched collision, A stopped braking hard.
- 1.95 s before the matched collision, A released the brake.
- 1.95 s before the matched collision, A started applying strong throttle.
- 1.60 s before the matched collision, A left its stop.
- 1.60 s before the matched collision, A started moving.
- 1.55 s before the matched collision, B's radar started tracking A.
- 1.55 s before the matched collision, B observed A start closing in (already the case when first observed).
- 1.20 s before the matched collision, A's time-to-contact with B became critical.
- 1.20 s before the matched collision, B's time-to-contact with A became critical.
- 0.60 s before the matched collision, A stopped applying strong throttle.
- 0.10 s before the matched collision, B observed A enter its forward path corridor.
- 0.05 s before the matched collision, A observed B enter its forward path corridor.
- 0.05 s before the matched collision, A's radar lost B.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 7340, B: 7340 N*s).
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, B's radar started tracking unidentified object B:track_002.
- At the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.05 s after the matched collision, B's radar started tracking unidentified object B:track_003.
- 0.05 s after the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.35 s after the matched collision, B stopped moving.
- 0.35 s after the matched collision, B came to a stop.
- 0.40 s after the matched collision, B observed unidentified object B:track_002 stop closing in.
- 0.40 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 0.45 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.45 s after the matched collision, B observed A stop closing in.
- 0.50 s after the matched collision, A stopped moving.
- 0.50 s after the matched collision, A came to a stop.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- BRAKE_START(B); HARD_BRAKE_START(B)
- BRAKE_END(B); BRAKE_START(A); HARD_BRAKE_START(A)
- MOVING_END(A); STOP_START(A)
- TRACK_APPEARED(A,B); CLOSING_START(A,B)
- HARD_BRAKE_END(A); BRAKE_END(A); STRONG_THROTTLE_START(A)
- STOP_END(A); MOVING_START(A)
- TRACK_APPEARED(B,A); CLOSING_START(B,A)
- CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A)
- EGO_PATH_ENTRY(A,B); TRACK_LOST(A,B)
- COLLISION(A,B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_002)
- STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(B,B:track_003); CLOSING_START(B,B:track_003)
- MOVING_END(B); STOP_START(B)
- CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e09 (t = 6.75 s); the track was lost at 9.65 s
- CRITICAL_TTC of track_001, since A:e15 (t = 8.50 s); the track was lost at 9.65 s
- EGO_PATH of track_001, since A:e17 (t = 9.65 s); the track was lost at 9.65 s
- BRAKE, since A:e22 (t = 9.75 s)
- HARD_BRAKE, since A:e23 (t = 9.75 s)
- STOP, since A:e25 (t = 10.20 s)
B:
- EGO_PATH of track_001, since B:e15 (t = 9.60 s)
- BRAKE, since B:e21 (t = 9.75 s)
- HARD_BRAKE, since B:e22 (t = 9.75 s)
- STOP, since B:e26 (t = 10.05 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none
B:
- STOP sign sign-1: detected 3.50 s -> 5.30 s; relevant to the path: False; STOP_START inside: none

## Uncertainty and limitations

- B:track_002 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 19.01 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with A's own speed before the collision.
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
