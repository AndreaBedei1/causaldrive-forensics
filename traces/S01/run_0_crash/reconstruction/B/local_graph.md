# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 19.181726828217506 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 120 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Nodes: 3; edges: 2 (PRECEDES 2)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 3.95 | BRAKE_EPISODE | B | - | controls | start_t_local=3.95; end_t_local=11.95; duration_s=8.00; peak_brake=1.00; mean_brake=1.00; speed_start_mps=13.78; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| B:e02 | 5.15 | FULL_STOP | B | - | ego | stopped_for_s=6.80; stopped_until_recording_end=True |
| B:e03 | 6.50 | COLLISION | B | - | collision_sensor | peak_impulse=17663.06; n_callbacks=1; duration_s=0.00 |

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
```

## Anonymous radar tracks

No radar track: nothing moving stayed in B's forward radar view long enough.

## Plain-language reading

- t = 3.95 s: B braked for 8.00 s (peak 1.00, mean 1.00), from 13.8 to 0.0 m/s, still braking when its recording ended.
- t = 5.15 s: B came to a full stop and stayed stopped until its recording ended.
- t = 6.50 s: B's collision sensor recorded a contact (peak impulse 17663 N*s, 1 callback(s) over 0.00 s).
