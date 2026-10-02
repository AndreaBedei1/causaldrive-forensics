# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 93.72970312461257 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 13 (PRECEDES 11, SAME_TRACK 2)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e03 | 0.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 1.50 | BRAKE_START | B | - | controls |  |
| B:e05 | 1.65 | BRAKE_END | B | - | controls |  |
| B:e06 | 3.90 | COLLISION | B | - | collision_sensor | peak_impulse=406.35 |
| B:e07 | 3.95 | CLOSING_END | B | track_001 | radar |  |
| B:e08 | 3.95 | BRAKE_START | B | - | controls |  |
| B:e09 | 4.40 | MOVING_END | B | - | ego |  |
| B:e10 | 4.40 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e02 --SAME_TRACK--> B:e03
    B:e02 --SAME_TRACK--> B:e07
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED_RIGHT track_001<br>B:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 1.50 | B:e04 BRAKE_START | ego: MOVING<br>track_001: CLOSING | 1.40 |
| 1.65 | B:e05 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING | 1.60 |
| 3.90 | B:e06 COLLISION | ego: MOVING<br>track_001: CLOSING | 3.80 |
| 3.95 | B:e07 CLOSING_END track_001<br>B:e08 BRAKE_START | ego: MOVING<br>track_001: CLOSING | 3.90 |
| 4.40 | B:e09 MOVING_END<br>B:e10 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 4.30 |

## States still active when observation ended

- BRAKE, since B:e08 (t = 3.95 s)
- STOP, since B:e10 (t = 4.40 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.45 | 229 | 26.8 m / +173 deg | 1.56 m (4.50) | 1.8 m / +130 deg | 13.5 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.50 s: B started braking.
- t = 1.65 s: B released the brake.
- t = 3.90 s: B's collision sensor recorded a contact (peak impulse 406 N*s).
- t = 3.95 s: B observed track_001 stop closing in.
- t = 3.95 s: B started braking.
- t = 4.40 s: B stopped moving.
- t = 4.40 s: B came to a stop.
