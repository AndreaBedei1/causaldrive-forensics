# Reconstruction report - S01/run_0_avoided

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.05 s | 132 | 15 | 23 | 1 | none |
| B | 13.05 s | 132 | 12 | 20 | 0 | none |

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

## Global graph

27 nodes, 6 edges; 0 merged node(s): none.

### Event sequence (global time)

- (none)

### What happened, in plain language

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 0.45 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 1.15 s) A started applying strong throttle.
- (unaligned, A local time 1.35 s) A stopped applying strong throttle.
- (unaligned, A local time 1.60 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.25 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 5.00 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.05 s) A started braking.
- (unaligned, A local time 5.05 s) A started braking hard.
- (unaligned, A local time 6.25 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 6.35 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.35 s) A stopped moving.
- (unaligned, A local time 6.35 s) A came to a stop.
- (unaligned, A local time 13.05 s) A started applying strong throttle.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 0.40 s) B started applying strong throttle.
- (unaligned, B local time 1.75 s) B stopped applying strong throttle.
- (unaligned, B local time 3.95 s) B started braking.
- (unaligned, B local time 3.95 s) B started braking hard.
- (unaligned, B local time 5.15 s) B stopped moving.
- (unaligned, B local time 5.15 s) B came to a stop.
- (unaligned, B local time 11.95 s) B stopped braking hard.
- (unaligned, B local time 11.95 s) B released the brake.
- (unaligned, B local time 11.95 s) B started applying strong throttle.
- (unaligned, B local time 12.35 s) B left its stop.
- (unaligned, B local time 12.35 s) B started moving.

### Simultaneous events (order unresolved at 0.05 s)

- none

### States still active when observation ended

A:
- BRAKE, since A:e09 (t = 5.05 s)
- HARD_BRAKE, since A:e10 (t = 5.05 s)
- STOP, since A:e14 (t = 6.35 s)
- STRONG_THROTTLE, since A:e15 (t = 13.05 s)
B:
- STRONG_THROTTLE, since B:e10 (t = 11.95 s)
- MOVING, since B:e12 (t = 12.35 s)

### Sign detection windows

A:
- none
B:
- none

## Uncertainty and limitations

- B built no radar track: nothing moving stayed in its forward radar view long enough, so B has no perception of the others.
- A:track_001 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
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
