# Reconstruction report - S11/run_0_stops_then_proceeds

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 13.35 s | 135 | 6 | 10 | 1 | none |
| B | 13.35 s | 135 | 37 | 76 | 5 | none |

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
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_004 | B:track_004 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_005 | B:track_005 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Global graph

43 nodes, 21 edges; 0 merged node(s): none.

### Event sequence (global time)

- (none)

### What happened, in plain language

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.60 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 2.60 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 4.65 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.25 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 5.35 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 2.40 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.55 s) B started braking hard.
- (unaligned, B local time 3.25 s) B stopped moving.
- (unaligned, B local time 3.25 s) B came to a stop.
- (unaligned, B local time 3.50 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 3.50 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.40 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.75 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 5.80 s) B observed unidentified object B:track_001 enter its forward path corridor.
- (unaligned, B local time 6.10 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.20 s) B observed unidentified object B:track_001 leave its forward path corridor.
- (unaligned, B local time 6.75 s) B stopped braking hard.
- (unaligned, B local time 6.75 s) B released the brake.
- (unaligned, B local time 6.75 s) B started applying strong throttle.
- (unaligned, B local time 7.20 s) B left its stop.
- (unaligned, B local time 7.20 s) B started moving.
- (unaligned, B local time 7.30 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 8.40 s) B stopped applying strong throttle.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_002.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_003.
- (unaligned, B local time 8.40 s) B's radar started tracking unidentified object B:track_004.
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_003 start closing in (already the case when first observed).
- (unaligned, B local time 8.40 s) B observed unidentified object B:track_004 start closing in (already the case when first observed).
- (unaligned, B local time 8.45 s) B's radar started tracking unidentified object B:track_005.
- (unaligned, B local time 8.45 s) B observed unidentified object B:track_005 start closing in (already the case when first observed).
- (unaligned, B local time 8.65 s) B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 9.60 s) B observed unidentified object B:track_004 enter its forward path corridor.
- (unaligned, B local time 9.70 s) B observed unidentified object B:track_003 enter its forward path corridor.
- (unaligned, B local time 9.85 s) B observed unidentified object B:track_004 leave its forward path corridor.
- (unaligned, B local time 9.90 s) B observed unidentified object B:track_003 leave its forward path corridor.
- (unaligned, B local time 9.90 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).

### Simultaneous events (order unresolved at 0.05 s)

- none

### States still active when observation ended

A:
- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e03 (t = 2.60 s); the track was lost at 5.35 s
B:
- MOVING, since B:e21 (t = 7.20 s)
- CLOSING of track_002, since B:e27 (t = 8.40 s); the track was lost at 9.90 s
- CLOSING of track_003, since B:e28 (t = 8.40 s)
- CLOSING of track_004, since B:e29 (t = 8.40 s)
- CLOSING of track_005, since B:e31 (t = 8.45 s); the track was lost at 8.65 s

### Sign detection windows

A:
- none
B:
- STOP sign sign-1: detected 2.10 s -> 2.40 s; relevant to the path: False; STOP_START inside: none

### Perceived state just before each collision report

- no collision was reported

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_001 at 5.35 s (A:e06): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
B:
- track_005 at 8.65 s (B:e32): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 9.90 s (B:e37): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001

## Uncertainty and limitations

- A:track_001 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- B:track_001 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_002 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_003 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_004 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
- B:track_005 stays anonymous: graph B is not aligned: it recorded no collision to anchor on.
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
    "path_half_width_m": 1.5,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
    "conflict_horizon_s": 4.0,
    "conflict_distance_m": 1.5,
    "conflict_release_horizon_s": 5.0,
    "conflict_release_distance_m": 2.5,
    "cut_in_max_heading_deg": 25.0,
    "cut_in_min_target_speed_mps": 2.0,
    "cut_in_lateral_speed_mps": 0.3,
    "cut_in_persistence_s": 0.5,
    "cut_in_outside_margin_m": 0.5,
    "cut_in_min_displacement_m": 0.5,
    "cut_in_horizon_s": 3.0,
    "cut_in_settle_speed_mps": 0.2,
    "cut_in_settle_s": 0.3
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
