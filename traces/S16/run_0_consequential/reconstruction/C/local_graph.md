# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 196.7230779863894 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 13 (PRECEDES 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.30 | MOVING_END | C | - | ego |  |
| C:e03 | 0.30 | STOP_START | C | - | ego |  |
| C:e04 | 5.90 | COLLISION | C | - | collision_sensor | peak_impulse=2695.68 |
| C:e05 | 5.90 | STOP_END | C | - | ego |  |
| C:e06 | 5.90 | MOVING_START | C | - | ego |  |
| C:e07 | 5.95 | BRAKE_START | C | - | controls |  |
| C:e08 | 6.05 | MOVING_END | C | - | ego |  |
| C:e09 | 6.05 | STOP_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e01 --PRECEDES--> C:e03
    C:e02 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e05
    C:e02 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e07
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
| 0.30 | C:e02 MOVING_END<br>C:e03 STOP_START | ego: MOVING | 0.20 |
| 5.90 | C:e04 COLLISION<br>C:e05 STOP_END<br>C:e06 MOVING_START | ego: STOP | 5.80 |
| 5.95 | C:e07 BRAKE_START | ego: MOVING | 5.90 |
| 6.05 | C:e08 MOVING_END<br>C:e09 STOP_START | ego: MOVING, BRAKE | 6.00 |

## States still active when observation ended

- BRAKE, since C:e07 (t = 5.95 s)
- STOP, since C:e09 (t = 6.05 s)

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
- t = 0.30 s: C stopped moving.
- t = 0.30 s: C came to a stop.
- t = 5.90 s: C's collision sensor recorded a contact (peak impulse 2696 N*s).
- t = 5.90 s: C left its stop.
- t = 5.90 s: C started moving.
- t = 5.95 s: C started braking.
- t = 6.05 s: C stopped moving.
- t = 6.05 s: C came to a stop.
