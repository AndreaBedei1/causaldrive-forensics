# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 559.752460680902 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 181 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (17.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 28; edges: 49 (PRECEDES 39, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e03 | 1.80 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e04 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e05 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e06 | 5.80 | MOVING_END | A | - | ego |  |
| A:e07 | 5.80 | STOP_START | A | - | ego |  |
| A:e08 | 10.95 | BRAKE_END | A | - | controls |  |
| A:e09 | 10.95 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e10 | 11.15 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e11 | 11.15 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e12 | 11.40 | STOP_END | A | - | ego |  |
| A:e13 | 11.40 | MOVING_START | A | - | ego |  |
| A:e14 | 11.80 | CLOSING_START | A | track_001 | radar |  |
| A:e15 | 11.80 | CLOSING_START | A | track_002 | radar |  |
| A:e16 | 12.00 | EGO_PATH_ENTRY | A | track_002 | radar |  |
| A:e17 | 12.20 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e18 | 12.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e19 | 12.70 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e20 | 12.75 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e21 | 13.50 | TRACK_LOST | A | track_002 | radar |  |
| A:e22 | 14.10 | COLLISION | A | - | collision_sensor | peak_impulse=9089.81 |
| A:e23 | 14.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e24 | 14.10 | CLOSING_END | A | track_001 | radar |  |
| A:e25 | 14.10 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e26 | 14.35 | TRACK_LOST | A | track_001 | radar |  |
| A:e27 | 14.65 | MOVING_END | A | - | ego |  |
| A:e28 | 14.65 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e28
    A:e10 --SAME_TRACK--> A:e14
    A:e11 --SAME_TRACK--> A:e15
    A:e11 --SAME_TRACK--> A:e16
    A:e10 --SAME_TRACK--> A:e17
    A:e10 --SAME_TRACK--> A:e18
    A:e11 --SAME_TRACK--> A:e20
    A:e11 --SAME_TRACK--> A:e21
    A:e10 --SAME_TRACK--> A:e23
    A:e10 --SAME_TRACK--> A:e24
    A:e10 --SAME_TRACK--> A:e26
```

## States still active when observation ended

- CLOSING of track_002, since A:e15 (t = 11.80 s); the track was lost at 13.50 s
- EGO_PATH of track_002, since A:e16 (t = 12.00 s); the track was lost at 13.50 s
- EGO_PATH of track_001, since A:e17 (t = 12.20 s); the track was lost at 14.35 s
- CRITICAL_TTC of track_002, since A:e20 (t = 12.75 s); the track was lost at 13.50 s
- STRONG_THROTTLE, since A:e25 (t = 14.10 s)
- STOP, since A:e28 (t = 14.65 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 11.15 | 14.35 | 59 | 14.8 m / -13 deg | 0.01 m (14.25) | 0.1 m / +174 deg | 3.1 m/s |
| track_002 | 11.15 | 13.50 | 41 | 18.2 m / -8 deg | 8.22 m (13.50) | 8.2 m / +12 deg | 1.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.70 s: A started applying strong throttle.
- t = 1.80 s: A stopped applying strong throttle.
- t = 3.95 s: A started braking.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.80 s: A stopped moving.
- t = 5.80 s: A came to a stop.
- t = 10.95 s: A released the brake.
- t = 10.95 s: A started applying strong throttle.
- t = 11.15 s: A's radar started tracking track_001.
- t = 11.15 s: A's radar started tracking track_002.
- t = 11.40 s: A left its stop.
- t = 11.40 s: A started moving.
- t = 11.80 s: A observed track_001 start closing in.
- t = 11.80 s: A observed track_002 start closing in.
- t = 12.00 s: A observed track_002 enter its forward path corridor.
- t = 12.20 s: A observed track_001 enter its forward path corridor.
- t = 12.55 s: A's time-to-contact with track_001 became critical.
- t = 12.70 s: A stopped applying strong throttle.
- t = 12.75 s: A's time-to-contact with track_002 became critical.
- t = 13.50 s: A's radar lost track_002.
- t = 14.10 s: A's collision sensor recorded a contact (peak impulse 9090 N*s).
- t = 14.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 14.10 s: A observed track_001 stop closing in.
- t = 14.10 s: A started applying strong throttle.
- t = 14.35 s: A's radar lost track_001.
- t = 14.65 s: A stopped moving.
- t = 14.65 s: A came to a stop.
