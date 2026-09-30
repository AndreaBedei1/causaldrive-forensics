# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 544.6900767125189 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 21; edges: 38 (PRECEDES 29, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e03 | 1.80 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e04 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e05 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e06 | 5.15 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e07 | 5.15 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e08 | 5.15 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e09 | 5.15 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e10 | 5.15 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e11 | 5.20 | BRAKE_END | A | - | controls |  |
| A:e12 | 5.55 | TRACK_APPEARED | A | track_003 | radar |  |
| A:e13 | 5.60 | CLOSING_END | A | track_002 | radar |  |
| A:e14 | 5.65 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e15 | 5.65 | TRACK_LOST | A | track_002 | radar |  |
| A:e16 | 5.90 | COLLISION | A | - | collision_sensor | peak_impulse=2695.68 |
| A:e17 | 6.00 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e18 | 6.00 | CLOSING_END | A | track_001 | radar |  |
| A:e19 | 6.05 | MOVING_END | A | - | ego |  |
| A:e20 | 6.05 | STOP_START | A | - | ego |  |
| A:e21 | 6.20 | TRACK_LOST | A | track_003 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e04 --PRECEDES--> A:e08
    A:e04 --PRECEDES--> A:e09
    A:e04 --PRECEDES--> A:e10
    A:e05 --PRECEDES--> A:e11
    A:e06 --PRECEDES--> A:e11
    A:e07 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e21
    A:e06 --SAME_TRACK--> A:e08
    A:e07 --SAME_TRACK--> A:e09
    A:e06 --SAME_TRACK--> A:e10
    A:e07 --SAME_TRACK--> A:e13
    A:e06 --SAME_TRACK--> A:e14
    A:e07 --SAME_TRACK--> A:e15
    A:e06 --SAME_TRACK--> A:e17
    A:e06 --SAME_TRACK--> A:e18
    A:e12 --SAME_TRACK--> A:e21
```

## States still active when observation ended

- EGO_PATH of track_001, since A:e14 (t = 5.65 s)
- STOP, since A:e20 (t = 6.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 5.15 | 9.95 | 91 | 5.6 m / -39 deg | 0.78 m (6.05) | 1.4 m / -14 deg | 1.9 m/s |
| track_002 | 5.15 | 5.65 | 5 | 15.6 m / +41 deg | 14.36 m (5.50) | 14.6 m / +61 deg | 6.2 m/s |
| track_003 | 5.55 | 6.20 | 8 | 19.5 m / +43 deg | 19.46 m (5.55) | 20.0 m / +60 deg | 4.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.70 s: A started applying strong throttle.
- t = 1.80 s: A stopped applying strong throttle.
- t = 3.95 s: A started braking.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.15 s: A's radar started tracking track_001.
- t = 5.15 s: A's radar started tracking track_002.
- t = 5.15 s: A observed track_001 start closing in (already the case when first observed).
- t = 5.15 s: A observed track_002 start closing in (already the case when first observed).
- t = 5.15 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 5.20 s: A released the brake.
- t = 5.55 s: A's radar started tracking track_003.
- t = 5.60 s: A observed track_002 stop closing in.
- t = 5.65 s: A observed track_001 enter its forward path corridor.
- t = 5.65 s: A's radar lost track_002.
- t = 5.90 s: A's collision sensor recorded a contact (peak impulse 2696 N*s).
- t = 6.00 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.00 s: A observed track_001 stop closing in.
- t = 6.05 s: A stopped moving.
- t = 6.05 s: A came to a stop.
- t = 6.20 s: A's radar lost track_003.
