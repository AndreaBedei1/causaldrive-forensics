# Reconstruction report - S12/run_0_near_simultaneous

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 14.95 s | 151 | 48 | 129 | 8 | A:e21 @ 9.50 s |
| B | 14.95 s | 151 | 32 | 64 | 1 | B:e24 @ 9.50 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e21 | 9.50 | -9.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e24 | 9.50 | -9.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4032.49 vs 4032.49 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 7.00 s before the matched collision<br>not at the contact: last seen 6.70 s before the matched collision (window 0.50 s)<br>speed not comparable with B's own speed before the collision |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.10 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 89.51 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.10 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 87.16 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: minimum range 11.46 m in the last 0.50 s (needs <= 3.50 m)<br>speed not comparable with B's own speed before the collision |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| A:track_007 | A:track_007 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| A:track_008 | A:track_008 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.05 s after the matched collision<br>speed not comparable with B's own speed before the collision |
| B:track_001 | A | ASSOCIATED | 0.79 | B and A both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.95 s before the matched collision<br>at the contact: minimum range 0.70 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 1.04 m/s over 3.0 s |

## Global graph

79 nodes, 255 edges; 1 merged node(s): g44 COLLISION(A,B) from A:e21 + B:e24.

### Event sequence (global time)

- `-9.50` MOVING_START(A); MOVING_START(B)
- `-8.85` STOP_SIGN_DETECTED_START(A,A:sign-0)
- `-8.25` STRONG_THROTTLE_START(B)
- `-7.65` STRONG_THROTTLE_END(B)
- `-7.40` STOP_SIGN_DETECTED_START(B,B:sign-1)
- `-7.25` STOP_SIGN_DETECTED_END(A,A:sign-0)
- `-7.00` TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- `-6.95` TRACK_APPEARED(B,A); CLOSING_START(B,A)
- `-6.90` STOP_SIGN_DETECTED_END(B,B:sign-1)
- `-6.85` BRAKE_START(A); HARD_BRAKE_START(A)
- `-6.75` BRAKE_START(B); HARD_BRAKE_START(B)
- `-6.70` TRACK_LOST(A,A:track_001)
- `-6.10` MOVING_END(A); STOP_START(A)
- `-6.00` CLOSING_END(B,A); MOVING_END(B); STOP_START(B)
- `-2.55` HARD_BRAKE_END(A); HARD_BRAKE_END(B); BRAKE_END(A); BRAKE_END(B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
- `-2.20` STOP_END(A); MOVING_START(A); CLOSING_START(B,A)
- `-2.15` STOP_END(B); MOVING_START(B)
- `-1.25` CRITICAL_TTC_START(B,A)
- `-1.20` STRONG_THROTTLE_END(A)
- `-0.85` STRONG_THROTTLE_END(B)
- `-0.55` EGO_PATH_ENTRY(B,A)
- `-0.10` TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,A:track_003); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003)
- `-0.05` CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- `+0.00` COLLISION(A,B); EGO_PATH_EXIT(B,A); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(A,A:track_004)
- `+0.05` STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(A,A:track_005); TRACK_APPEARED(A,A:track_006); TRACK_APPEARED(A,A:track_007); TRACK_APPEARED(A,A:track_008); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008)
- `+0.10` CLOSING_START(A,A:track_004); TRACK_LOST(B,A)
- `+0.30` TRACK_LOST(A,A:track_002)
- `+0.45` MOVING_END(B); STOP_START(B)
- `+0.50` CLOSING_END(A,A:track_005); MOVING_END(A); STOP_START(A)
- `+0.55` CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_006); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_008)
- `+2.20` STOP_SIGN_DETECTED_START(A,A:sign-1)
- `+2.30` STOP_SIGN_DETECTED_END(A,A:sign-1)
- `+4.45` STOP_SIGN_DETECTED_START(A,A:sign-4); STOP_SIGN_DETECTED_END(A,A:sign-4)

### What happened, in plain language

- 9.50 s before the matched collision, A started moving (already the case when first observed).
- 9.50 s before the matched collision, B started moving (already the case when first observed).
- 8.85 s before the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 8.25 s before the matched collision, B started applying strong throttle.
- 7.65 s before the matched collision, B stopped applying strong throttle.
- 7.40 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-1).
- 7.25 s before the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.00 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 7.00 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 6.95 s before the matched collision, B's radar started tracking A.
- 6.95 s before the matched collision, B observed A start closing in (already the case when first observed).
- 6.90 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-1.
- 6.85 s before the matched collision, A started braking.
- 6.85 s before the matched collision, A started braking hard.
- 6.75 s before the matched collision, B started braking.
- 6.75 s before the matched collision, B started braking hard.
- 6.70 s before the matched collision, A's radar lost unidentified object A:track_001.
- 6.10 s before the matched collision, A stopped moving.
- 6.10 s before the matched collision, A came to a stop.
- 6.00 s before the matched collision, B observed A stop closing in.
- 6.00 s before the matched collision, B stopped moving.
- 6.00 s before the matched collision, B came to a stop.
- 2.55 s before the matched collision, A stopped braking hard.
- 2.55 s before the matched collision, B stopped braking hard.
- 2.55 s before the matched collision, A released the brake.
- 2.55 s before the matched collision, B released the brake.
- 2.55 s before the matched collision, A started applying strong throttle.
- 2.55 s before the matched collision, B started applying strong throttle.
- 2.20 s before the matched collision, A left its stop.
- 2.20 s before the matched collision, A started moving.
- 2.20 s before the matched collision, B observed A start closing in.
- 2.15 s before the matched collision, B left its stop.
- 2.15 s before the matched collision, B started moving.
- 1.25 s before the matched collision, B's time-to-contact with A became critical.
- 1.20 s before the matched collision, A stopped applying strong throttle.
- 0.85 s before the matched collision, B stopped applying strong throttle.
- 0.55 s before the matched collision, B observed A enter its forward path corridor.
- 0.10 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 0.10 s before the matched collision, A's radar started tracking unidentified object A:track_003.
- 0.10 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 0.10 s before the matched collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- 0.05 s before the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s before the matched collision, B observed A stop closing in.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 4032, B: 4032 N*s).
- At the matched collision, B observed A leave its forward path corridor.
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started applying strong throttle.
- At the matched collision, A's radar started tracking unidentified object A:track_004.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, B stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.05 s after the matched collision, B started braking hard.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_005.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_006.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_007.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_008.
- 0.05 s after the matched collision, A observed unidentified object A:track_005 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_006 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_007 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_008 start closing in (already the case when first observed).
- 0.10 s after the matched collision, A observed unidentified object A:track_004 start closing in.
- 0.10 s after the matched collision, B's radar lost A.
- 0.30 s after the matched collision, A's radar lost unidentified object A:track_002.
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.50 s after the matched collision, A observed unidentified object A:track_005 stop closing in.
- 0.50 s after the matched collision, A stopped moving.
- 0.50 s after the matched collision, A came to a stop.
- 0.55 s after the matched collision, A observed unidentified object A:track_003 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_004 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_006 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_007 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_008 stop closing in.
- 2.20 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 2.30 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-1.
- 4.45 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-4) (the detector judged it not relevant to its path).
- 4.45 s after the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-4.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B)
- TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- TRACK_APPEARED(B,A); CLOSING_START(B,A)
- BRAKE_START(A); HARD_BRAKE_START(A)
- BRAKE_START(B); HARD_BRAKE_START(B)
- MOVING_END(A); STOP_START(A)
- CLOSING_END(B,A); MOVING_END(B); STOP_START(B)
- HARD_BRAKE_END(A); HARD_BRAKE_END(B); BRAKE_END(A); BRAKE_END(B); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B)
- STOP_END(A); MOVING_START(A); CLOSING_START(B,A)
- STOP_END(B); MOVING_START(B)
- TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,A:track_003); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003)
- CRITICAL_TTC_END(B,A); CLOSING_END(B,A)
- COLLISION(A,B); EGO_PATH_EXIT(B,A); STRONG_THROTTLE_START(A); STRONG_THROTTLE_START(B); TRACK_APPEARED(A,A:track_004)
- STRONG_THROTTLE_END(A); STRONG_THROTTLE_END(B); BRAKE_START(A); BRAKE_START(B); HARD_BRAKE_START(A); HARD_BRAKE_START(B); TRACK_APPEARED(A,A:track_005); TRACK_APPEARED(A,A:track_006); TRACK_APPEARED(A,A:track_007); TRACK_APPEARED(A,A:track_008); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008)
- CLOSING_START(A,A:track_004); TRACK_LOST(B,A)
- MOVING_END(B); STOP_START(B)
- CLOSING_END(A,A:track_005); MOVING_END(A); STOP_START(A)
- CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_006); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_008)
- STOP_SIGN_DETECTED_START(A,A:sign-4); STOP_SIGN_DETECTED_END(A,A:sign-4)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e05 (t = 2.50 s); the track was lost at 2.80 s
- CLOSING of track_002, since A:e19 (t = 9.40 s); the track was lost at 9.80 s
- BRAKE, since A:e25 (t = 9.55 s)
- HARD_BRAKE, since A:e26 (t = 9.55 s)
- STOP, since A:e39 (t = 10.00 s)
B:
- BRAKE, since B:e28 (t = 9.55 s)
- HARD_BRAKE, since B:e29 (t = 9.55 s)
- STOP, since B:e32 (t = 9.95 s)

### Sign detection windows

A:
- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none
- STOP sign sign-1: detected 11.70 s -> 11.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-4: detected 13.95 s -> 13.95 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
B:
- STOP sign sign-1: detected 2.10 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

## Uncertainty and limitations

- A:track_001 stays anonymous: not at the contact: last seen 6.70 s before the matched collision (window 0.50 s); speed not comparable with B's own speed before the collision.
- A:track_002 stays anonymous: tracked only 0.10 s before the matched collision (needs 1.00 s); not at the contact: minimum range 89.51 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with B's own speed before the collision.
- A:track_003 stays anonymous: tracked only 0.10 s before the matched collision (needs 1.00 s); not at the contact: minimum range 87.16 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with B's own speed before the collision.
- A:track_004 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: minimum range 11.46 m in the last 0.50 s (needs <= 3.50 m); speed not comparable with B's own speed before the collision.
- A:track_005 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with B's own speed before the collision.
- A:track_006 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with B's own speed before the collision.
- A:track_007 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with B's own speed before the collision.
- A:track_008 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.05 s after the matched collision; speed not comparable with B's own speed before the collision.
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
