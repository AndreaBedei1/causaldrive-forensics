# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 21.149357691407204 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 132 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.05 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 7; edges: 7 (PRECEDES 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 3.95 | BRAKE_START | B | - | controls |  |
| B:e03 | 5.15 | MOVING_END | B | - | ego |  |
| B:e04 | 5.15 | STOP_START | B | - | ego |  |
| B:e05 | 11.95 | BRAKE_END | B | - | controls |  |
| B:e06 | 12.35 | STOP_END | B | - | ego |  |
| B:e07 | 12.35 | MOVING_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 3.95 | B:e02 BRAKE_START | ego: MOVING | 3.90 |
| 5.15 | B:e03 MOVING_END<br>B:e04 STOP_START | ego: MOVING, BRAKE | 5.10 |
| 11.95 | B:e05 BRAKE_END | ego: STOP, BRAKE | 11.90 |
| 12.35 | B:e06 STOP_END<br>B:e07 MOVING_START | ego: STOP | 12.30 |

## States still active when observation ended

- MOVING, since B:e07 (t = 12.35 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in B's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 3.95 s: B started braking.
- t = 5.15 s: B stopped moving.
- t = 5.15 s: B came to a stop.
- t = 11.95 s: B released the brake.
- t = 12.35 s: B left its stop.
- t = 12.35 s: B started moving.
