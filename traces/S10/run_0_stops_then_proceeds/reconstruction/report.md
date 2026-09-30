# Reconstruction report - S10/run_0_stops_then_proceeds

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.35 s | 135 | 41 | 87 | 8 | none |
| B | 13.35 s | 135 | 9 | 12 | 1 | none |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_003 | A:track_003 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_004 | A:track_004 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_005 | A:track_005 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_006 | A:track_006 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_007 | A:track_007 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_008 | A:track_008 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Global graph

50 nodes, 23 edges; 0 merged node(s): none.

### Event sequence (global time)

- (none)

### What happened, in plain language

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 1.75 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 2.15 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.55 s) A started braking.
- (unaligned, A local time 2.55 s) A started braking hard.
- (unaligned, A local time 3.35 s) A stopped moving.
- (unaligned, A local time 3.35 s) A came to a stop.
- (unaligned, A local time 3.70 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 3.70 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 4.25 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.80 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 5.95 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 6.10 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.25 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 6.75 s) A stopped braking hard.
- (unaligned, A local time 6.75 s) A released the brake.
- (unaligned, A local time 6.75 s) A started applying strong throttle.
- (unaligned, A local time 7.00 s) A's radar lost unidentified object A:track_001.
- (unaligned, A local time 7.10 s) A left its stop.
- (unaligned, A local time 7.10 s) A started moving.
- (unaligned, A local time 8.20 s) A's radar started tracking unidentified object A:track_002.
- (unaligned, A local time 8.20 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 8.25 s) A stopped applying strong throttle.
- (unaligned, A local time 8.25 s) A's radar started tracking unidentified object A:track_003.
- (unaligned, A local time 8.25 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 8.30 s) A's radar started tracking unidentified object A:track_004.
- (unaligned, A local time 8.30 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 8.35 s) A's radar started tracking unidentified object A:track_005.
- (unaligned, A local time 8.35 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 8.40 s) A's radar started tracking unidentified object A:track_006.
- (unaligned, A local time 8.40 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 8.45 s) A's radar started tracking unidentified object A:track_007.
- (unaligned, A local time 8.45 s) A's radar started tracking unidentified object A:track_008.
- (unaligned, A local time 8.45 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 8.45 s) A observed unidentified object A:track_008 start closing in (already the case when first observed).
- (unaligned, A local time 9.00 s) A's time-to-contact with unidentified object A:track_003 became critical.
- (unaligned, A local time 9.25 s) A's radar lost unidentified object A:track_003.
- (unaligned, A local time 9.50 s) A's radar lost unidentified object A:track_002.
- (unaligned, A local time 10.75 s) A's radar lost unidentified object A:track_006.
- (unaligned, A local time 11.60 s) A's radar lost unidentified object A:track_007.
- (unaligned, A local time 12.45 s) A's radar lost unidentified object A:track_005.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.20 s) B started applying strong throttle.
- (unaligned, B local time 1.80 s) B stopped applying strong throttle.
- (unaligned, B local time 2.55 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 2.55 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.30 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.50 s) B's radar lost unidentified object B:track_001.
- (unaligned, B local time 7.60 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 7.70 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.

### Simultaneous events (order unresolved at 0.05 s)

- none

### States still active when observation ended

A:
- MOVING, since A:e20 (t = 7.10 s)
- CLOSING of track_002, since A:e22 (t = 8.20 s); the track was lost at 9.50 s
- CLOSING of track_003, since A:e25 (t = 8.25 s); the track was lost at 9.25 s
- CLOSING of track_004, since A:e27 (t = 8.30 s)
- CLOSING of track_005, since A:e29 (t = 8.35 s); the track was lost at 12.45 s
- CLOSING of track_006, since A:e31 (t = 8.40 s); the track was lost at 10.75 s
- CLOSING of track_007, since A:e34 (t = 8.45 s); the track was lost at 11.60 s
- CLOSING of track_008, since A:e35 (t = 8.45 s)
- CRITICAL_TTC of track_003, since A:e36 (t = 9.00 s); the track was lost at 9.25 s
B:
- MOVING, since B:e01 (t = 0.00 s)
- CLOSING of track_001, since B:e05 (t = 2.55 s); the track was lost at 5.50 s
- CRITICAL_TTC of track_001, since B:e06 (t = 4.30 s); the track was lost at 5.50 s

### Sign detection windows

A:
- STOP sign sign-0: detected 1.75 s -> 2.15 s; relevant to the path: False; STOP_START inside: none
B:
- STOP sign sign-1: detected 7.60 s -> 7.70 s; relevant to the path: False; STOP_START inside: none

## Uncertainty and limitations

- A:track_001 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_002 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_003 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_004 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_005 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_006 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_007 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_008 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- B:track_001 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- A is UNALIGNED: it recorded no collision to anchor on.
- B is UNALIGNED: it recorded no collision to anchor on.
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
