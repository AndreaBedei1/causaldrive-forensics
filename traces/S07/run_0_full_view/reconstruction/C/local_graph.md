# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 68.30776481702924 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 9 (PRECEDES 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 2.40 | SPEED_LIMIT_EXCEEDED_START | C | - | ego |  |
| C:e03 | 2.95 | BRAKE_START | C | - | controls |  |
| C:e04 | 3.10 | SPEED_LIMIT_EXCEEDED_END | C | - | ego |  |
| C:e05 | 4.05 | MOVING_END | C | - | ego |  |
| C:e06 | 4.05 | STOP_START | C | - | ego |  |
| C:e07 | 12.95 | BRAKE_END | C | - | controls |  |
| C:e08 | 13.75 | STOP_END | C | - | ego |  |
| C:e09 | 13.75 | MOVING_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

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
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START | ego: not yet observed | - |
| 2.40 | C:e02 SPEED_LIMIT_EXCEEDED_START | ego: MOVING | 2.30 |
| 2.95 | C:e03 BRAKE_START | ego: MOVING, SPEED_LIMIT_EXCEEDED | 2.90 |
| 3.10 | C:e04 SPEED_LIMIT_EXCEEDED_END | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED | 3.00 |
| 4.05 | C:e05 MOVING_END<br>C:e06 STOP_START | ego: MOVING, BRAKE | 4.00 |
| 12.95 | C:e07 BRAKE_END | ego: STOP, BRAKE | 12.90 |
| 13.75 | C:e08 STOP_END<br>C:e09 MOVING_START | ego: STOP | 13.70 |

## States still active when observation ended

- MOVING, since C:e09 (t = 13.75 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in C's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 2.40 s: C began exceeding the speed limit.
- t = 2.95 s: C started braking.
- t = 3.10 s: C returned within the speed limit.
- t = 4.05 s: C stopped moving.
- t = 4.05 s: C came to a stop.
- t = 12.95 s: C released the brake.
- t = 13.75 s: C left its stop.
- t = 13.75 s: C started moving.
