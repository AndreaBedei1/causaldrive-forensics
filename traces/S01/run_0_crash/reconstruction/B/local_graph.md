# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 29.69283339381218 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 8; edges: 10 (PRECEDES 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.40 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.75 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 3.95 | BRAKE_START | B | - | controls |  |
| B:e05 | 3.95 | HARD_BRAKE_START | B | - | controls |  |
| B:e06 | 5.15 | MOVING_END | B | - | ego |  |
| B:e07 | 5.15 | STOP_START | B | - | ego |  |
| B:e08 | 6.50 | COLLISION | B | - | collision_sensor | peak_impulse=17663.06 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
```

## States still active when observation ended

- BRAKE, since B:e04 (t = 3.95 s)
- HARD_BRAKE, since B:e05 (t = 3.95 s)
- STOP, since B:e07 (t = 5.15 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in B's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.40 s: B started applying strong throttle.
- t = 1.75 s: B stopped applying strong throttle.
- t = 3.95 s: B started braking.
- t = 3.95 s: B started braking hard.
- t = 5.15 s: B stopped moving.
- t = 5.15 s: B came to a stop.
- t = 6.50 s: B's collision sensor recorded a contact (peak impulse 17663 N*s).
