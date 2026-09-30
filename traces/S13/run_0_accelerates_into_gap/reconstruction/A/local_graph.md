# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 432.100672993809 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 25; edges: 53 (PRECEDES 42, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.00 | TRACK_LOST | A | track_001 | radar |  |
| A:e05 | 1.95 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e06 | 2.75 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e07 | 2.75 | SPEED_LIMIT_EXCEEDED_START | A | - | ego |  |
| A:e08 | 3.35 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e09 | 3.35 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e10 | 3.80 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e11 | 5.25 | EGO_PATH_ENTRY | A | track_002 | radar |  |
| A:e12 | 5.65 | COLLISION | A | - | collision_sensor | peak_impulse=5215.85 |
| A:e13 | 5.65 | SPEED_LIMIT_EXCEEDED_END | A | - | ego |  |
| A:e14 | 5.65 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e15 | 5.70 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e16 | 5.70 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e17 | 5.70 | BRAKE_START | A | - | controls |  |
| A:e18 | 5.70 | HARD_BRAKE_START | A | - | controls |  |
| A:e19 | 5.80 | CLOSING_END | A | track_002 | radar |  |
| A:e20 | 6.40 | CLOSING_START | A | track_002 | radar |  |
| A:e21 | 6.40 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e22 | 6.90 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e23 | 6.90 | CLOSING_END | A | track_002 | radar |  |
| A:e24 | 6.95 | MOVING_END | A | - | ego |  |
| A:e25 | 6.95 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e16
    A:e12 --PRECEDES--> A:e17
    A:e12 --PRECEDES--> A:e18
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e13 --PRECEDES--> A:e18
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e08 --SAME_TRACK--> A:e09
    A:e08 --SAME_TRACK--> A:e10
    A:e08 --SAME_TRACK--> A:e11
    A:e08 --SAME_TRACK--> A:e15
    A:e08 --SAME_TRACK--> A:e19
    A:e08 --SAME_TRACK--> A:e20
    A:e08 --SAME_TRACK--> A:e21
    A:e08 --SAME_TRACK--> A:e22
    A:e08 --SAME_TRACK--> A:e23
```

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 0.00 s); the track was lost at 1.00 s
- EGO_PATH of track_002, since A:e11 (t = 5.25 s)
- BRAKE, since A:e17 (t = 5.70 s)
- HARD_BRAKE, since A:e18 (t = 5.70 s)
- STOP, since A:e25 (t = 6.95 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 1.00 | 17 | 33.1 m / -6 deg | 29.49 m (1.00) | 29.5 m / -6 deg | 7.4 m/s |
| track_002 | 3.35 | 9.95 | 131 | 18.3 m / -10 deg | 0.23 m (6.90) | 0.4 m / +1 deg | 11.6 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.00 s: A's radar lost track_001.
- t = 1.95 s: A started applying strong throttle.
- t = 2.75 s: A stopped applying strong throttle.
- t = 2.75 s: A began exceeding the speed limit.
- t = 3.35 s: A's radar started tracking track_002.
- t = 3.35 s: A observed track_002 start closing in (already the case when first observed).
- t = 3.80 s: A's time-to-contact with track_002 became critical.
- t = 5.25 s: A observed track_002 enter its forward path corridor.
- t = 5.65 s: A's collision sensor recorded a contact (peak impulse 5216 N*s).
- t = 5.65 s: A returned within the speed limit.
- t = 5.65 s: A started applying strong throttle.
- t = 5.70 s: A's time-to-contact with track_002 stopped being critical.
- t = 5.70 s: A stopped applying strong throttle.
- t = 5.70 s: A started braking.
- t = 5.70 s: A started braking hard.
- t = 5.80 s: A observed track_002 stop closing in.
- t = 6.40 s: A observed track_002 start closing in.
- t = 6.40 s: A's time-to-contact with track_002 became critical.
- t = 6.90 s: A's time-to-contact with track_002 stopped being critical.
- t = 6.90 s: A observed track_002 stop closing in.
- t = 6.95 s: A stopped moving.
- t = 6.95 s: A came to a stop.
