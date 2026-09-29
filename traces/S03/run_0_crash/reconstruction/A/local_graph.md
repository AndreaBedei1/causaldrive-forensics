# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 49.807998076081276 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 152 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Nodes: 7; edges: 9 (PRECEDES 6, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 2.05 | TRACK_APPEARED | A | track_001 | radar | range_m=34.18; bearing_deg=55.70; speed_mps=10.87; in_ego_path=False |
| A:e02 | 2.05 | CLOSING | A | track_001 | radar | range_m=34.18; closing_speed_mps=14.32; peak_closing_speed_mps=15.62; duration_s=1.30 |
| A:e03 | 2.35 | CRITICAL_TTC | A | track_001 | radar | ttc_s=1.99; range_m=29.84; min_ttc_s=0.94 |
| A:e04 | 3.35 | TRACK_LOST | A | track_001 | radar | range_m=14.40; bearing_deg=59.10; tracked_for_s=1.30 |
| A:e05 | 4.25 | COLLISION | A | - | collision_sensor | peak_impulse=12077.22; n_callbacks=1; duration_s=0.00 |
| A:e06 | 4.30 | BRAKE_EPISODE | A | - | controls | start_t_local=4.30; end_t_local=15.15; duration_s=10.85; peak_brake=1.00; mean_brake=1.00; speed_start_mps=8.90; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| A:e07 | 4.90 | FULL_STOP | A | - | ego | stopped_for_s=10.25; stopped_until_recording_end=True |

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e01 --SAME_TRACK--> A:e02
    A:e02 --SAME_TRACK--> A:e03
    A:e03 --SAME_TRACK--> A:e04
```

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.05 | 3.35 | 26 | 34.2 m / +56 deg | 14.40 m (3.35) | 14.4 m / +59 deg | 13.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 2.05 s: A's radar started tracking track_001 at 34.2 m, 56 deg to the right, moving at 10.9 m/s.
- t = 2.05 s: A observed track_001 closing at 14.3 m/s from 34.2 m (peak 15.6 m/s, down to 14.4 m).
- t = 2.35 s: A's time-to-contact with track_001 fell to 2.0 s at 29.8 m (minimum 0.9 s).
- t = 3.35 s: A lost track_001 at 14.4 m, 59 deg to the right, after tracking it for 1.3 s.
- t = 4.25 s: A's collision sensor recorded a contact (peak impulse 12077 N*s, 1 callback(s) over 0.00 s).
- t = 4.30 s: A braked for 10.85 s (peak 1.00, mean 1.00), from 8.9 to 0.0 m/s, still braking when its recording ended.
- t = 4.90 s: A came to a full stop and stayed stopped until its recording ended.
