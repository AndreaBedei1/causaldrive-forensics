# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 559.752460680902 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 181 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (17.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 14 (PRECEDES 14)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.50 | MOVING_END | C | - | ego |  |
| C:e03 | 0.50 | STOP_START | C | - | ego |  |
| C:e04 | 11.95 | STOP_END | C | - | ego |  |
| C:e05 | 11.95 | MOVING_START | C | - | ego |  |
| C:e06 | 14.10 | COLLISION | C | - | collision_sensor | peak_impulse=9089.81 |
| C:e07 | 14.10 | BRAKE_START | C | - | controls |  |
| C:e08 | 14.15 | HARD_BRAKE_START | C | - | controls |  |
| C:e09 | 14.65 | MOVING_END | C | - | ego |  |
| C:e10 | 14.65 | STOP_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e01 --PRECEDES--> C:e03
    C:e02 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e07
    C:e05 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e10
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START | ego: not yet observed | - |
| 0.50 | C:e02 MOVING_END<br>C:e03 STOP_START | ego: MOVING | 0.40 |
| 11.95 | C:e04 STOP_END<br>C:e05 MOVING_START | ego: STOP | 11.90 |
| 14.10 | C:e06 COLLISION<br>C:e07 BRAKE_START | ego: MOVING | 14.00 |
| 14.15 | C:e08 HARD_BRAKE_START | ego: MOVING, BRAKE | 14.10 |
| 14.65 | C:e09 MOVING_END<br>C:e10 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE | 14.60 |

## States still active when observation ended

- BRAKE, since C:e07 (t = 14.10 s)
- HARD_BRAKE, since C:e08 (t = 14.15 s)
- STOP, since C:e10 (t = 14.65 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in C's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.50 s: C stopped moving.
- t = 0.50 s: C came to a stop.
- t = 11.95 s: C left its stop.
- t = 11.95 s: C started moving.
- t = 14.10 s: C's collision sensor recorded a contact (peak impulse 9090 N*s).
- t = 14.10 s: C started braking.
- t = 14.15 s: C started braking hard.
- t = 14.65 s: C stopped moving.
- t = 14.65 s: C came to a stop.
