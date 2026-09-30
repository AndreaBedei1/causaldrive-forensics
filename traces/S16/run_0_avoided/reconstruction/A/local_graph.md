# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 531.2718035392463 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 8; edges: 7 (PRECEDES 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e03 | 1.80 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e04 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e05 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e06 | 5.20 | HARD_BRAKE_START | A | - | controls |  |
| A:e07 | 5.75 | MOVING_END | A | - | ego |  |
| A:e08 | 5.75 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
```

## States still active when observation ended

- BRAKE, since A:e04 (t = 3.95 s)
- HARD_BRAKE, since A:e06 (t = 5.20 s)
- STOP, since A:e08 (t = 5.75 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in A's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.70 s: A started applying strong throttle.
- t = 1.80 s: A stopped applying strong throttle.
- t = 3.95 s: A started braking.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.20 s: A started braking hard.
- t = 5.75 s: A stopped moving.
- t = 5.75 s: A came to a stop.
