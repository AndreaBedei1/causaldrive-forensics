# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 12.814889293164015 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 7; edges: 6 (PRECEDES 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.40 | BRAKE_START | B | - | controls |  |
| B:e03 | 1.55 | BRAKE_END | B | - | controls |  |
| B:e04 | 3.85 | COLLISION | B | - | collision_sensor | peak_impulse=241.17 |
| B:e05 | 3.90 | BRAKE_START | B | - | controls |  |
| B:e06 | 4.35 | MOVING_END | B | - | ego |  |
| B:e07 | 4.35 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.40 | B:e02 BRAKE_START | ego: MOVING | 1.30 |
| 1.55 | B:e03 BRAKE_END | ego: MOVING, BRAKE | 1.50 |
| 3.85 | B:e04 COLLISION | ego: MOVING | 3.80 |
| 3.90 | B:e05 BRAKE_START | ego: MOVING | 3.80 |
| 4.35 | B:e06 MOVING_END<br>B:e07 STOP_START | ego: MOVING, BRAKE | 4.30 |

## States still active when observation ended

- BRAKE, since B:e05 (t = 3.90 s)
- STOP, since B:e07 (t = 4.35 s)

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
- t = 1.40 s: B started braking.
- t = 1.55 s: B released the brake.
- t = 3.85 s: B's collision sensor recorded a contact (peak impulse 241 N*s).
- t = 3.90 s: B started braking.
- t = 4.35 s: B stopped moving.
- t = 4.35 s: B came to a stop.
