# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 135.76189954578876 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 301 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (29.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 11 (PRECEDES 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.50 | STRONG_THROTTLE_START | C | - | controls |  |
| C:e03 | 2.05 | STRONG_THROTTLE_END | C | - | controls |  |
| C:e04 | 2.40 | SPEED_LIMIT_EXCEEDED_START | C | - | ego |  |
| C:e05 | 2.95 | BRAKE_START | C | - | controls |  |
| C:e06 | 2.95 | HARD_BRAKE_START | C | - | controls |  |
| C:e07 | 3.05 | SPEED_LIMIT_EXCEEDED_END | C | - | ego |  |
| C:e08 | 4.05 | MOVING_END | C | - | ego |  |
| C:e09 | 4.05 | STOP_START | C | - | ego |  |
| C:e10 | 6.15 | COLLISION | C | - | collision_sensor | peak_impulse=9832.40 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e02 --PRECEDES--> C:e03
    C:e03 --PRECEDES--> C:e04
    C:e04 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e10
    C:e09 --PRECEDES--> C:e10
```

## States still active when observation ended

- BRAKE, since C:e05 (t = 2.95 s)
- HARD_BRAKE, since C:e06 (t = 2.95 s)
- STOP, since C:e09 (t = 4.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in C's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.50 s: C started applying strong throttle.
- t = 2.05 s: C stopped applying strong throttle.
- t = 2.40 s: C began exceeding the speed limit.
- t = 2.95 s: C started braking.
- t = 2.95 s: C started braking hard.
- t = 3.05 s: C returned within the speed limit.
- t = 4.05 s: C stopped moving.
- t = 4.05 s: C came to a stop.
- t = 6.15 s: C's collision sensor recorded a contact (peak impulse 9832 N*s).
