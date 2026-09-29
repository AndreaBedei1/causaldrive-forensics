# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 19.181726828217506 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 120 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Nodes: 8; edges: 10 (PRECEDES 7, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | TRACK_APPEARED | A | track_001 | radar | range_m=23.54; bearing_deg=-0.70; speed_mps=13.07; in_ego_path=True |
| A:e02 | 0.45 | CLOSING | A | track_001 | radar | range_m=23.20; closing_speed_mps=1.03; peak_closing_speed_mps=4.18; duration_s=1.10 |
| A:e03 | 1.15 | THROTTLE_ONSET | A | - | controls | throttle=0.86; speed_mps=12.56 |
| A:e04 | 4.25 | CLOSING | A | track_001 | radar | range_m=21.64; closing_speed_mps=1.41; peak_closing_speed_mps=13.69; duration_s=2.20 |
| A:e05 | 5.00 | CRITICAL_TTC | A | track_001 | radar | ttc_s=1.82; range_m=17.95; min_ttc_s=0.10 |
| A:e06 | 5.55 | BRAKE_EPISODE | A | - | controls | start_t_local=5.55; end_t_local=11.95; duration_s=6.40; peak_brake=1.00; mean_brake=0.98; speed_start_mps=13.57; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| A:e07 | 6.50 | COLLISION | A | - | collision_sensor | peak_impulse=17663.06; n_callbacks=1; duration_s=0.00 |
| A:e08 | 6.55 | FULL_STOP | A | - | ego | stopped_for_s=5.40; stopped_until_recording_end=True |

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
| track_001 | 0.00 | 11.95 | 238 | 23.5 m / -1 deg | 0.75 m (11.95) | 0.8 m / +0 deg | 14.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A's radar started tracking track_001 at 23.5 m, ahead, moving at 13.1 m/s, inside its path.
- t = 0.45 s: A observed track_001 closing at 1.0 m/s from 23.2 m (peak 4.2 m/s, down to 20.5 m).
- t = 1.15 s: A applied strong throttle (0.86 at 12.6 m/s).
- t = 4.25 s: A observed track_001 closing at 1.4 m/s from 21.6 m (peak 13.7 m/s, down to 0.8 m).
- t = 5.00 s: A's time-to-contact with track_001 fell to 1.8 s at 17.9 m (minimum 0.1 s).
- t = 5.55 s: A braked for 6.40 s (peak 1.00, mean 0.98), from 13.6 to 0.0 m/s, still braking when its recording ended.
- t = 6.50 s: A's collision sensor recorded a contact (peak impulse 17663 N*s, 1 callback(s) over 0.00 s).
- t = 6.55 s: A came to a full stop and stayed stopped until its recording ended.
