# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 12.805227477103472 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 132 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.05 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 12; edges: 20 (PRECEDES 20)

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
| B:e08 | 11.95 | HARD_BRAKE_END | B | - | controls |  |
| B:e09 | 11.95 | BRAKE_END | B | - | controls |  |
| B:e10 | 11.95 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e11 | 12.35 | STOP_END | B | - | ego |  |
| B:e12 | 12.35 | MOVING_START | B | - | ego |  |

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
    B:e06 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e10
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
```

## States still active when observation ended

- STRONG_THROTTLE, since B:e10 (t = 11.95 s)
- MOVING, since B:e12 (t = 12.35 s)

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
- t = 11.95 s: B stopped braking hard.
- t = 11.95 s: B released the brake.
- t = 11.95 s: B started applying strong throttle.
- t = 12.35 s: B left its stop.
- t = 12.35 s: B started moving.
