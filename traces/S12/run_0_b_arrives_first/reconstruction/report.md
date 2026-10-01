# Reconstruction report - S12/run_0_b_arrives_first

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 16.45 s | 166 | 51 | 132 | 13 | none |
| B | 16.45 s | 166 | 20 | 33 | 1 | none |

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
| A:track_009 | A:track_009 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_010 | A:track_010 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_011 | A:track_011 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_012 | A:track_012 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_013 | A:track_013 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Global graph

71 nodes, 29 edges; 0 merged node(s): none.

### Event sequence (global time)

- (none)

### What happened, in plain language

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 1.05 s) A's camera established a STOP sign detection (unidentified object A:sign-0).
- (unaligned, A local time 3.00 s) A's radar started tracking unidentified object A:track_001, which appeared on its left.
- (unaligned, A local time 3.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.55 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 4.35 s) A started braking.
- (unaligned, A local time 4.35 s) A started braking hard.
- (unaligned, A local time 4.70 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 4.75 s) A stopped moving.
- (unaligned, A local time 4.75 s) A came to a stop.
- (unaligned, A local time 7.00 s) A observed unidentified object A:track_001 start closing in.
- (unaligned, A local time 9.70 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 9.85 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 10.20 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 10.45 s) A stopped braking hard.
- (unaligned, A local time 10.45 s) A released the brake.
- (unaligned, A local time 10.45 s) A started applying strong throttle.
- (unaligned, A local time 10.80 s) A left its stop.
- (unaligned, A local time 10.80 s) A started moving.
- (unaligned, A local time 11.65 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 11.80 s) A stopped applying strong throttle.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_002, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_004, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_006, which appeared on its left.
- (unaligned, A local time 13.10 s) A's radar started tracking unidentified object A:track_003, which appeared on its right.
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_003 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_004 start closing in (already the case when first observed).
- (unaligned, A local time 13.10 s) A observed unidentified object A:track_006 start closing in (already the case when first observed).
- (unaligned, A local time 13.25 s) A's radar started tracking unidentified object A:track_005, which appeared on its left.
- (unaligned, A local time 13.25 s) A observed unidentified object A:track_005 start closing in (already the case when first observed).
- (unaligned, A local time 13.30 s) A's radar started tracking unidentified object A:track_009, which appeared on its left.
- (unaligned, A local time 13.30 s) A's radar started tracking unidentified object A:track_007, which appeared on its right.
- (unaligned, A local time 13.30 s) A observed unidentified object A:track_007 start closing in (already the case when first observed).
- (unaligned, A local time 13.30 s) A observed unidentified object A:track_009 start closing in (already the case when first observed).
- (unaligned, A local time 13.35 s) A's radar started tracking unidentified object A:track_008, which appeared on its left.
- (unaligned, A local time 13.35 s) A's radar started tracking unidentified object A:track_010, which appeared on its left.
- (unaligned, A local time 13.35 s) A observed unidentified object A:track_008 start closing in (already the case when first observed).
- (unaligned, A local time 13.35 s) A observed unidentified object A:track_010 start closing in (already the case when first observed).
- (unaligned, A local time 13.45 s) A's radar started tracking unidentified object A:track_011, which appeared on its left.
- (unaligned, A local time 13.45 s) A's radar started tracking unidentified object A:track_012, which appeared on its left.
- (unaligned, A local time 13.45 s) A observed unidentified object A:track_011 start closing in (already the case when first observed).
- (unaligned, A local time 13.45 s) A observed unidentified object A:track_012 start closing in (already the case when first observed).
- (unaligned, A local time 13.50 s) A's radar started tracking unidentified object A:track_013, which appeared on its left.
- (unaligned, A local time 13.50 s) A observed unidentified object A:track_013 start closing in (already the case when first observed).
- (unaligned, A local time 13.80 s) A's time-to-contact with unidentified object A:track_007 became critical.
- (unaligned, A local time 14.00 s) A's radar lost unidentified object A:track_007 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 14.40 s) A's radar lost unidentified object A:track_003 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 15.00 s) A observed unidentified object A:track_006 enter its forward path corridor.
- (unaligned, A local time 15.60 s) A's radar lost unidentified object A:track_013 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 15.95 s) A observed unidentified object A:track_006 leave its forward path corridor.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 2.10 s) B's camera established a STOP sign detection (unidentified object B:sign-1).
- (unaligned, B local time 2.60 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 2.65 s) B started braking.
- (unaligned, B local time 2.65 s) B started braking hard.
- (unaligned, B local time 3.00 s) B's radar started tracking unidentified object B:track_001, which appeared on its right.
- (unaligned, B local time 3.00 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 4.70 s) B observed unidentified object B:track_001 stop closing in.
- (unaligned, B local time 6.45 s) B stopped braking hard.
- (unaligned, B local time 6.45 s) B released the brake.
- (unaligned, B local time 6.45 s) B started applying strong throttle.
- (unaligned, B local time 6.85 s) B left its stop.
- (unaligned, B local time 6.85 s) B started moving.
- (unaligned, B local time 7.00 s) B observed unidentified object B:track_001 start closing in.
- (unaligned, B local time 7.90 s) B stopped applying strong throttle.
- (unaligned, B local time 8.75 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).

### Simultaneous events (order unresolved at 0.05 s)

- none

### States still active when observation ended

A:
- MOVING, since A:e19 (t = 10.80 s)
- CLOSING of track_002, since A:e26 (t = 13.10 s)
- CLOSING of track_003, since A:e27 (t = 13.10 s); the track was lost at 14.40 s
- CLOSING of track_004, since A:e28 (t = 13.10 s)
- CLOSING of track_006, since A:e29 (t = 13.10 s)
- CLOSING of track_005, since A:e31 (t = 13.25 s)
- CLOSING of track_007, since A:e34 (t = 13.30 s); the track was lost at 14.00 s
- CLOSING of track_009, since A:e35 (t = 13.30 s)
- CLOSING of track_008, since A:e38 (t = 13.35 s)
- CLOSING of track_010, since A:e39 (t = 13.35 s)
- CLOSING of track_011, since A:e42 (t = 13.45 s)
- CLOSING of track_012, since A:e43 (t = 13.45 s)
- CLOSING of track_013, since A:e45 (t = 13.50 s); the track was lost at 15.60 s
- CRITICAL_TTC of track_007, since A:e46 (t = 13.80 s); the track was lost at 14.00 s
B:
- MOVING, since B:e17 (t = 6.85 s)
- CLOSING of track_001, since B:e18 (t = 7.00 s); the track was lost at 8.75 s

### Sign detection windows

A:
- STOP sign sign-0: detected 1.05 s -> 3.55 s; relevant to the path: True; STOP_START inside: none
B:
- STOP sign sign-1: detected 2.10 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

### Perceived state just before each collision report

- no collision was reported

### Tracks lost while a state was active

A lost track's states become UNKNOWN: the recorder can no longer tell whether they ended.

A:
- track_007 at 14.00 s (A:e47): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 14.40 s (A:e48): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_013 at 15.60 s (A:e50): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001
B:
- track_001 at 8.75 s (B:e20): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Uncertainty and limitations

- A:track_001 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_002 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_003 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_004 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_005 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_006 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_007 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_008 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_009 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_010 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_011 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_012 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
- A:track_013 stays anonymous: graph A is not aligned: it recorded no collision to anchor on.
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
    "path_half_width_m": 1.5,
    "track_appeared_front_deg": 5.0,
    "max_position_std_m": 1.0,
    "max_velocity_std_mps": 1.0,
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
