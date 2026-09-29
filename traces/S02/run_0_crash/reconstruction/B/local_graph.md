# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 32.949120827019215 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 152 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Nodes: 4; edges: 3 (PRECEDES 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 3.15 | BRAKE_EPISODE | B | - | controls | start_t_local=3.15; end_t_local=3.60; duration_s=0.45; peak_brake=0.73; mean_brake=0.48; speed_start_mps=8.71; speed_end_mps=6.56; min_speed_mps=6.56; released=True |
| B:e02 | 4.25 | BRAKE_EPISODE | B | - | controls | start_t_local=4.25; end_t_local=15.15; duration_s=10.90; peak_brake=1.00; mean_brake=1.00; speed_start_mps=9.59; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| B:e03 | 4.25 | COLLISION | B | - | collision_sensor | peak_impulse=5953.86; n_callbacks=1; duration_s=0.00 |
| B:e04 | 5.00 | FULL_STOP | B | - | ego | stopped_for_s=10.15; stopped_until_recording_end=True |

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
```

## Anonymous radar tracks

No radar track: nothing moving stayed in B's forward radar view long enough.

## Plain-language reading

- t = 3.15 s: B braked for 0.45 s (peak 0.73, mean 0.48), from 8.7 to 6.6 m/s, then released the brake.
- t = 4.25 s: B braked for 10.90 s (peak 1.00, mean 1.00), from 9.6 to 0.0 m/s, still braking when its recording ended.
- t = 4.25 s: B's collision sensor recorded a contact (peak impulse 5954 N*s, 1 callback(s) over 0.00 s).
- t = 5.00 s: B came to a full stop and stayed stopped until its recording ended.
