# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 296.6198318079114 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 13; edges: 26 (PRECEDES 22, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.75 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 2.75 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 3.70 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 5.45 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e06 | 5.45 | TRACK_LOST | A | track_001 | radar |  |
| A:e07 | 5.50 | COLLISION | A | - | collision_sensor | peak_impulse=8859.58 |
| A:e08 | 5.50 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e09 | 5.55 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e10 | 5.55 | BRAKE_START | A | - | controls |  |
| A:e11 | 5.55 | HARD_BRAKE_START | A | - | controls |  |
| A:e12 | 6.05 | MOVING_END | A | - | ego |  |
| A:e13 | 6.05 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
```

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 2.75 s); the track was lost at 5.45 s
- CRITICAL_TTC of track_001, since A:e04 (t = 3.70 s); the track was lost at 5.45 s
- EGO_PATH of track_001, since A:e05 (t = 5.45 s); the track was lost at 5.45 s
- BRAKE, since A:e10 (t = 5.55 s)
- HARD_BRAKE, since A:e11 (t = 5.55 s)
- STOP, since A:e13 (t = 6.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.75 | 5.45 | 54 | 32.7 m / +24 deg | 1.59 m (5.45) | 1.6 m / +70 deg | 5.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.75 s: A's radar started tracking track_001.
- t = 2.75 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.70 s: A's time-to-contact with track_001 became critical.
- t = 5.45 s: A observed track_001 enter its forward path corridor.
- t = 5.45 s: A's radar lost track_001.
- t = 5.50 s: A's collision sensor recorded a contact (peak impulse 8860 N*s).
- t = 5.50 s: A started applying strong throttle.
- t = 5.55 s: A stopped applying strong throttle.
- t = 5.55 s: A started braking.
- t = 5.55 s: A started braking hard.
- t = 6.05 s: A stopped moving.
- t = 6.05 s: A came to a stop.
