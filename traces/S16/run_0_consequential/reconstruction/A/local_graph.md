# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 253.51562337204814 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 18 (PRECEDES 14, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_REAR | A | track_001 | radar |  |
| A:e03 | 0.70 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.40 | CLOSING_END | A | track_001 | radar |  |
| A:e05 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e06 | 4.20 | CLOSING_START | A | track_001 | radar |  |
| A:e07 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e08 | 5.15 | CLOSING_END | A | track_001 | radar |  |
| A:e09 | 5.20 | BRAKE_END | A | - | controls |  |
| A:e10 | 5.40 | TURN_LEFT_START | A | - | ego |  |
| A:e11 | 5.90 | COLLISION | A | - | collision_sensor | peak_impulse=2695.68 |
| A:e12 | 6.00 | TURN_LEFT_END | A | - | ego |  |
| A:e13 | 6.05 | MOVING_END | A | - | ego |  |
| A:e14 | 6.05 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e08
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_REAR track_001 | ego: not yet observed | - |
| 0.70 | A:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state | 0.60 |
| 1.40 | A:e04 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING | 1.30 |
| 3.95 | A:e05 BRAKE_START | ego: MOVING<br>track_001: no active state | 3.90 |
| 4.20 | A:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>track_001: no active state | 4.10 |
| 5.15 | A:e07 COLLISION<br>A:e08 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING | 5.10 |
| 5.20 | A:e09 BRAKE_END | ego: MOVING, BRAKE<br>track_001: no active state | 5.10 |
| 5.40 | A:e10 TURN_LEFT_START | ego: MOVING<br>track_001: no active state | 5.30 |
| 5.90 | A:e11 COLLISION | ego: MOVING, TURN_LEFT<br>track_001: no active state | 5.80 |
| 6.00 | A:e12 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: no active state | 5.90 |
| 6.05 | A:e13 MOVING_END<br>A:e14 STOP_START | ego: MOVING<br>track_001: no active state | 6.00 |

## States still active when observation ended

- STOP, since A:e14 (t = 6.05 s)

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
| track_001 | 0.00 | 9.95 | 200 | 6.2 m / -180 deg | 3.56 m (5.15) | 5.3 m / -163 deg | 13.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared behind it.
- t = 0.70 s: A observed track_001 start closing in.
- t = 1.40 s: A observed track_001 stop closing in.
- t = 3.95 s: A started braking.
- t = 4.20 s: A observed track_001 start closing in.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.15 s: A observed track_001 stop closing in.
- t = 5.20 s: A released the brake.
- t = 5.40 s: A started turning left.
- t = 5.90 s: A's collision sensor recorded a contact (peak impulse 2696 N*s).
- t = 6.00 s: A stopped turning left.
- t = 6.05 s: A stopped moving.
- t = 6.05 s: A came to a stop.
