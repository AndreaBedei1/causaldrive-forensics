# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 32.949120827019215 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 152 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Nodes: 8; edges: 10 (PRECEDES 7, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | TRACK_APPEARED | A | track_001 | radar | range_m=24.57; bearing_deg=-7.80; speed_mps=8.01; in_ego_path=False |
| A:e02 | 0.00 | CLOSING | A | track_001 | radar | range_m=24.57; closing_speed_mps=5.56; peak_closing_speed_mps=7.86; duration_s=4.20 |
| A:e03 | 1.15 | THROTTLE_ONSET | A | - | controls | throttle=0.86; speed_mps=12.56 |
| A:e04 | 2.80 | CRITICAL_TTC | A | track_001 | radar | ttc_s=1.96; range_m=9.56; min_ttc_s=0.17 |
| A:e05 | 3.20 | ENTERED_EGO_PATH | A | track_001 | radar | from_side=left; longitudinal_m=7.46; lateral_speed_mps=1.25 |
| A:e06 | 3.85 | BRAKE_EPISODE | A | - | controls | start_t_local=3.85; end_t_local=15.15; duration_s=11.30; peak_brake=1.00; mean_brake=0.99; speed_start_mps=13.41; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| A:e07 | 4.25 | COLLISION | A | - | collision_sensor | peak_impulse=5953.86; n_callbacks=1; duration_s=0.00 |
| A:e08 | 4.85 | FULL_STOP | A | - | ego | stopped_for_s=10.30; stopped_until_recording_end=True |

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e01 --SAME_TRACK--> A:e02
    A:e02 --SAME_TRACK--> A:e04
    A:e04 --SAME_TRACK--> A:e05
```

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 15.15 | 304 | 24.6 m / -8 deg | 0.85 m (4.30) | 2.1 m / -6 deg | 9.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A's radar started tracking track_001 at 24.6 m, 8 deg to the left, moving at 8.0 m/s.
- t = 0.00 s: A observed track_001 closing at 5.6 m/s from 24.6 m (peak 7.9 m/s, down to 0.9 m).
- t = 1.15 s: A applied strong throttle (0.86 at 12.6 m/s).
- t = 2.80 s: A's time-to-contact with track_001 fell to 2.0 s at 9.6 m (minimum 0.2 s).
- t = 3.20 s: A observed track_001 move into its path from the left (7.5 m ahead, lateral speed 1.2 m/s).
- t = 3.85 s: A braked for 11.30 s (peak 1.00, mean 0.99), from 13.4 to 0.0 m/s, still braking when its recording ended.
- t = 4.25 s: A's collision sensor recorded a contact (peak impulse 5954 N*s, 1 callback(s) over 0.00 s).
- t = 4.85 s: A came to a full stop and stayed stopped until its recording ended.
