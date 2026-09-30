# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 116.97939620912075 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 146 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 34 (PRECEDES 27, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.25 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 1.25 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.65 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 3.50 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e06 | 3.70 | COLLISION | A | - | collision_sensor | peak_impulse=6116.26 |
| A:e07 | 3.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e08 | 3.70 | CLOSING_END | A | track_001 | radar |  |
| A:e09 | 3.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e10 | 3.75 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e11 | 3.75 | BRAKE_START | A | - | controls |  |
| A:e12 | 3.75 | HARD_BRAKE_START | A | - | controls |  |
| A:e13 | 3.90 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e14 | 3.95 | TRACK_LOST | A | track_001 | radar |  |
| A:e15 | 4.55 | MOVING_END | A | - | ego |  |
| A:e16 | 4.55 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e05 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e10
    A:e06 --PRECEDES--> A:e11
    A:e06 --PRECEDES--> A:e12
    A:e07 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e11
    A:e07 --PRECEDES--> A:e12
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e14
```

## States still active when observation ended

- BRAKE, since A:e11 (t = 3.75 s)
- HARD_BRAKE, since A:e12 (t = 3.75 s)
- STOP, since A:e16 (t = 4.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.25 | 3.95 | 55 | 36.7 m / +43 deg | 0.85 m (3.70) | 2.4 m / -107 deg | 11.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.25 s: A's radar started tracking track_001.
- t = 1.25 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.65 s: A's time-to-contact with track_001 became critical.
- t = 3.50 s: A observed track_001 enter its forward path corridor.
- t = 3.70 s: A's collision sensor recorded a contact (peak impulse 6116 N*s).
- t = 3.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.70 s: A observed track_001 stop closing in.
- t = 3.70 s: A started applying strong throttle.
- t = 3.75 s: A stopped applying strong throttle.
- t = 3.75 s: A started braking.
- t = 3.75 s: A started braking hard.
- t = 3.90 s: A observed track_001 leave its forward path corridor.
- t = 3.95 s: A's radar lost track_001.
- t = 4.55 s: A stopped moving.
- t = 4.55 s: A came to a stop.
