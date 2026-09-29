# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 49.807998076081276 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 152 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Nodes: 9; edges: 11 (PRECEDES 8, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 1.15 | THROTTLE_ONSET | B | - | controls | throttle=1.00; speed_mps=7.39 |
| B:e02 | 2.15 | TRACK_APPEARED | B | track_001 | radar | range_m=32.71; bearing_deg=-37.80; speed_mps=8.19; in_ego_path=False |
| B:e03 | 2.15 | CLOSING | B | track_001 | radar | range_m=32.71; closing_speed_mps=14.23; peak_closing_speed_mps=15.64; duration_s=2.10 |
| B:e04 | 2.35 | CRITICAL_TTC | B | track_001 | radar | ttc_s=2.00; range_m=29.82; min_ttc_s=0.11 |
| B:e05 | 4.10 | ENTERED_EGO_PATH | B | track_001 | radar | from_side=left; longitudinal_m=2.53; lateral_speed_mps=10.70 |
| B:e06 | 4.25 | THROTTLE_ONSET | B | - | controls | throttle=1.00; speed_mps=5.15 |
| B:e07 | 4.25 | COLLISION | B | - | collision_sensor | peak_impulse=12077.22; n_callbacks=1; duration_s=0.00 |
| B:e08 | 4.30 | BRAKE_EPISODE | B | - | controls | start_t_local=4.30; end_t_local=15.15; duration_s=10.85; peak_brake=1.00; mean_brake=1.00; speed_start_mps=4.36; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| B:e09 | 4.55 | FULL_STOP | B | - | ego | stopped_for_s=10.60; stopped_until_recording_end=True |

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e02 --SAME_TRACK--> B:e03
    B:e03 --SAME_TRACK--> B:e04
    B:e04 --SAME_TRACK--> B:e05
```

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.15 | 15.15 | 260 | 32.7 m / -38 deg | 0.87 m (4.30) | 2.9 m / +48 deg | 11.0 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 1.15 s: B applied strong throttle (1.00 at 7.4 m/s).
- t = 2.15 s: B's radar started tracking track_001 at 32.7 m, 38 deg to the left, moving at 8.2 m/s.
- t = 2.15 s: B observed track_001 closing at 14.2 m/s from 32.7 m (peak 15.6 m/s, down to 0.9 m).
- t = 2.35 s: B's time-to-contact with track_001 fell to 2.0 s at 29.8 m (minimum 0.1 s).
- t = 4.10 s: B observed track_001 move into its path from the left (2.5 m ahead, lateral speed 10.7 m/s).
- t = 4.25 s: B applied strong throttle (1.00 at 5.2 m/s).
- t = 4.25 s: B's collision sensor recorded a contact (peak impulse 12077 N*s, 1 callback(s) over 0.00 s).
- t = 4.30 s: B braked for 10.85 s (peak 1.00, mean 1.00), from 4.4 to 0.0 m/s, still braking when its recording ended.
- t = 4.55 s: B came to a full stop and stayed stopped until its recording ended.
