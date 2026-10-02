# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 71.11231157556176 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 15 (PRECEDES 13, SAME_TRACK 2)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e03 | 0.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 3.15 | BRAKE_START | B | - | controls |  |
| B:e05 | 3.60 | BRAKE_END | B | - | controls |  |
| B:e06 | 4.25 | COLLISION | B | - | collision_sensor | peak_impulse=5953.86 |
| B:e07 | 4.25 | CLOSING_END | B | track_001 | radar |  |
| B:e08 | 4.25 | BRAKE_START | B | - | controls |  |
| B:e09 | 5.00 | MOVING_END | B | - | ego |  |
| B:e10 | 5.00 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e10
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
| 3.15 | B:e04 BRAKE_START | ego: MOVING<br>track_001: CLOSING | 3.10 |
| 3.60 | B:e05 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING | 3.50 |
| 4.25 | B:e06 COLLISION<br>B:e07 CLOSING_END track_001<br>B:e08 BRAKE_START | ego: MOVING<br>track_001: CLOSING | 4.20 |
| 5.00 | B:e09 MOVING_END<br>B:e10 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 4.90 |

## States still active when observation ended

- BRAKE, since B:e08 (t = 4.25 s)
- STOP, since B:e10 (t = 5.00 s)

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
| track_001 | 0.00 | 15.15 | 299 | 27.1 m / +173 deg | 3.42 m (4.25) | 4.8 m / +170 deg | 13.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.15 s: B started braking.
- t = 3.60 s: B released the brake.
- t = 4.25 s: B's collision sensor recorded a contact (peak impulse 5954 N*s).
- t = 4.25 s: B observed track_001 stop closing in.
- t = 4.25 s: B started braking.
- t = 5.00 s: B stopped moving.
- t = 5.00 s: B came to a stop.
