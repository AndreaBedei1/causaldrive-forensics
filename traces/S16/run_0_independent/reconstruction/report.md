# Reconstruction report - S16/run_0_independent

Inputs: `vehicles/A/`, `vehicles/B/`, `vehicles/C/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 17.95 s | 181 | 28 | 49 | 2 | A:e05 @ 5.15 s, A:e22 @ 14.10 s |
| B | 17.95 s | 181 | 20 | 35 | 2 | B:e12 @ 5.15 s |
| C | 17.95 s | 181 | 10 | 14 | 0 | C:e06 @ 14.10 s |

## Graph alignment

Reference event: `collision_002`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e22 | 14.10 | -14.10 | reported the reference collision collision_002 |
| B | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |
| C | ALIGNED | C:e06 | 14.10 | -14.10 | reported the reference collision collision_002 |

Estimated relative clock offsets: C - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 9089.81 vs 9089.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 1.00 | A and C both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 2.95 s before the matched collision<br>at the contact: minimum range 0.06 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with C's own speed: RMSE 0.08 m/s over 2.9 s |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and C both reported collision_002 (peak impulse 9089.81 vs 9089.81 N*s)<br>tracked for 2.95 s before the matched collision<br>not at the contact: last seen 0.60 s before the matched collision (window 0.50 s)<br>track speed agrees with C's own speed: RMSE 0.07 m/s over 2.3 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented) |

## Global graph

57 nodes, 73 edges; 1 merged node(s): g27 COLLISION(A,C) from A:e22 + C:e06.

### Event sequence (global time)

- `-14.10` MOVING_START(A); MOVING_START(C)
- `-13.60` MOVING_END(C); STOP_START(C)
- `-13.40` STRONG_THROTTLE_START(A)
- `-12.30` STRONG_THROTTLE_END(A)
- `-10.15` BRAKE_START(A)
- `-8.95` COLLISION(A)
- `-8.30` MOVING_END(A); STOP_START(A)
- `-3.15` BRAKE_END(A); STRONG_THROTTLE_START(A)
- `-2.95` TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,C)
- `-2.70` STOP_END(A); MOVING_START(A)
- `-2.30` CLOSING_START(A,A:track_002); CLOSING_START(A,C)
- `-2.15` STOP_END(C); MOVING_START(C)
- `-2.10` EGO_PATH_ENTRY(A,A:track_002)
- `-1.90` EGO_PATH_ENTRY(A,C)
- `-1.55` CRITICAL_TTC_START(A,C)
- `-1.40` STRONG_THROTTLE_END(A)
- `-1.35` CRITICAL_TTC_START(A,A:track_002)
- `-0.60` TRACK_LOST(A,A:track_002)
- `+0.00` COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,C); STRONG_THROTTLE_START(A); BRAKE_START(C)
- `+0.05` HARD_BRAKE_START(C)
- `+0.25` TRACK_LOST(A,C)
- `+0.55` MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### What happened, in plain language

- 14.10 s before the matched collision, A started moving (already the case when first observed).
- 14.10 s before the matched collision, C started moving (already the case when first observed).
- 13.60 s before the matched collision, C stopped moving.
- 13.60 s before the matched collision, C came to a stop.
- 13.40 s before the matched collision, A started applying strong throttle.
- 12.30 s before the matched collision, A stopped applying strong throttle.
- 10.15 s before the matched collision, A started braking.
- 8.95 s before the matched collision, A's collision sensor recorded a contact (peak impulse 6074 N*s).
- 8.30 s before the matched collision, A stopped moving.
- 8.30 s before the matched collision, A came to a stop.
- 3.15 s before the matched collision, A released the brake.
- 3.15 s before the matched collision, A started applying strong throttle.
- 2.95 s before the matched collision, A's radar started tracking unidentified object A:track_002.
- 2.95 s before the matched collision, A's radar started tracking C.
- 2.70 s before the matched collision, A left its stop.
- 2.70 s before the matched collision, A started moving.
- 2.30 s before the matched collision, A observed unidentified object A:track_002 start closing in.
- 2.30 s before the matched collision, A observed C start closing in.
- 2.15 s before the matched collision, C left its stop.
- 2.15 s before the matched collision, C started moving.
- 2.10 s before the matched collision, A observed unidentified object A:track_002 enter its forward path corridor.
- 1.90 s before the matched collision, A observed C enter its forward path corridor.
- 1.55 s before the matched collision, A's time-to-contact with C became critical.
- 1.40 s before the matched collision, A stopped applying strong throttle.
- 1.35 s before the matched collision, A's time-to-contact with unidentified object A:track_002 became critical.
- 0.60 s before the matched collision, A's radar lost unidentified object A:track_002.
- At the matched collision, A and C both recorded this same collision (peak impulses A: 9090, C: 9090 N*s).
- At the matched collision, A's time-to-contact with C stopped being critical.
- At the matched collision, A observed C stop closing in.
- At the matched collision, A started applying strong throttle.
- At the matched collision, C started braking.
- 0.05 s after the matched collision, C started braking hard.
- 0.25 s after the matched collision, A's radar lost C.
- 0.55 s after the matched collision, A stopped moving.
- 0.55 s after the matched collision, C stopped moving.
- 0.55 s after the matched collision, A came to a stop.
- 0.55 s after the matched collision, C came to a stop.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.00 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 0.70 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 0.75 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 1.35 s) B started applying strong throttle.
- (unaligned, B local time 1.40 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 1.40 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 2.50 s) B stopped applying strong throttle.
- (unaligned, B local time 4.25 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 4.35 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 4.75 s) B started braking.
- (unaligned, B local time 5.15 s) B's collision sensor recorded a contact (peak impulse 6074 N*s).
- (unaligned, B local time 5.20 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.20 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 5.20 s) B started braking hard.
- (unaligned, B local time 5.60 s) B stopped moving.
- (unaligned, B local time 5.60 s) B came to a stop.
- (unaligned, B local time 12.55 s) B's radar started tracking unidentified object B:track_002.
- (unaligned, B local time 13.55 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 14.05 s) B's radar lost unidentified object B:track_001.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(C)
- MOVING_END(C); STOP_START(C)
- MOVING_END(A); STOP_START(A)
- BRAKE_END(A); STRONG_THROTTLE_START(A)
- TRACK_APPEARED(A,A:track_002); TRACK_APPEARED(A,C)
- STOP_END(A); MOVING_START(A)
- CLOSING_START(A,A:track_002); CLOSING_START(A,C)
- STOP_END(C); MOVING_START(C)
- COLLISION(A,C); CRITICAL_TTC_END(A,C); CLOSING_END(A,C); STRONG_THROTTLE_START(A); BRAKE_START(C)
- MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C)

### States still active when observation ended

A:
- CLOSING of track_002, since A:e15 (t = 11.80 s); the track was lost at 13.50 s
- EGO_PATH of track_002, since A:e16 (t = 12.00 s); the track was lost at 13.50 s
- EGO_PATH of track_001, since A:e17 (t = 12.20 s); the track was lost at 14.35 s
- CRITICAL_TTC of track_002, since A:e20 (t = 12.75 s); the track was lost at 13.50 s
- STRONG_THROTTLE, since A:e25 (t = 14.10 s)
- STOP, since A:e28 (t = 14.65 s)
B:
- BRAKE, since B:e11 (t = 4.75 s)
- HARD_BRAKE, since B:e15 (t = 5.20 s)
- STOP, since B:e17 (t = 5.60 s)
C:
- BRAKE, since C:e07 (t = 14.10 s)
- HARD_BRAKE, since C:e08 (t = 14.15 s)
- STOP, since C:e10 (t = 14.65 s)

### Sign detection windows

A:
- none
B:
- none
C:
- none

## Uncertainty and limitations

- C built no radar track: nothing moving stayed in its forward radar view long enough, so C has no perception of the others.
- A:track_002 stays anonymous: not at the contact: last seen 0.60 s before the matched collision (window 0.50 s).
- B:track_001 stays anonymous: graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented).
- B:track_002 stays anonymous: graph B is not aligned: shares only a non-reference collision (multi-hop alignment not implemented).
- B is UNALIGNED: shares only a non-reference collision (multi-hop alignment not implemented).
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
