# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 447.9447439610958 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 6; edges: 7 (PRECEDES 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.80 | BRAKE_START | B | - | controls |  |
| B:e03 | 5.25 | COLLISION | B | - | collision_sensor | peak_impulse=3184.37 |
| B:e04 | 5.25 | HARD_BRAKE_START | B | - | controls |  |
| B:e05 | 6.45 | MOVING_END | B | - | ego |  |
| B:e06 | 6.45 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
```

## States still active when observation ended

- BRAKE, since B:e02 (t = 0.80 s)
- HARD_BRAKE, since B:e04 (t = 5.25 s)
- STOP, since B:e06 (t = 6.45 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in B's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.80 s: B started braking.
- t = 5.25 s: B's collision sensor recorded a contact (peak impulse 3184 N*s).
- t = 5.25 s: B started braking hard.
- t = 6.45 s: B stopped moving.
- t = 6.45 s: B came to a stop.
