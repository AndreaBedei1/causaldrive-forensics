# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 493.54037738218904 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 21; edges: 34 (PRECEDES 25, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED | C | track_001 | radar |  |
| C:e03 | 0.00 | TRACK_APPEARED | C | track_002 | radar |  |
| C:e04 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e05 | 0.00 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 1.65 | STRONG_THROTTLE_START | C | - | controls |  |
| C:e07 | 2.10 | STRONG_THROTTLE_END | C | - | controls |  |
| C:e08 | 2.25 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e09 | 2.50 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e10 | 3.15 | CRITICAL_TTC_END | C | track_002 | radar |  |
| C:e11 | 4.45 | TRACK_LOST | C | track_002 | radar |  |
| C:e12 | 4.75 | COLLISION | C | - | collision_sensor | peak_impulse=1637.56 |
| C:e13 | 4.75 | STRONG_THROTTLE_START | C | - | controls |  |
| C:e14 | 4.80 | STRONG_THROTTLE_END | C | - | controls |  |
| C:e15 | 4.80 | BRAKE_START | C | - | controls |  |
| C:e16 | 4.80 | HARD_BRAKE_START | C | - | controls |  |
| C:e17 | 5.00 | EGO_PATH_ENTRY | C | track_001 | radar |  |
| C:e18 | 5.05 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e19 | 5.05 | CLOSING_END | C | track_001 | radar |  |
| C:e20 | 5.05 | MOVING_END | C | - | ego |  |
| C:e21 | 5.05 | STOP_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    C:e01 --PRECEDES--> C:e06
    C:e02 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e06
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e13
    C:e12 --PRECEDES--> C:e14
    C:e12 --PRECEDES--> C:e15
    C:e12 --PRECEDES--> C:e16
    C:e13 --PRECEDES--> C:e14
    C:e13 --PRECEDES--> C:e15
    C:e13 --PRECEDES--> C:e16
    C:e14 --PRECEDES--> C:e17
    C:e15 --PRECEDES--> C:e17
    C:e16 --PRECEDES--> C:e17
    C:e17 --PRECEDES--> C:e18
    C:e17 --PRECEDES--> C:e19
    C:e17 --PRECEDES--> C:e20
    C:e17 --PRECEDES--> C:e21
    C:e02 --SAME_TRACK--> C:e04
    C:e03 --SAME_TRACK--> C:e05
    C:e03 --SAME_TRACK--> C:e08
    C:e02 --SAME_TRACK--> C:e09
    C:e03 --SAME_TRACK--> C:e10
    C:e03 --SAME_TRACK--> C:e11
    C:e02 --SAME_TRACK--> C:e17
    C:e02 --SAME_TRACK--> C:e18
    C:e02 --SAME_TRACK--> C:e19
```

## States still active when observation ended

- CLOSING of track_002, since C:e05 (t = 0.00 s); the track was lost at 4.45 s
- BRAKE, since C:e15 (t = 4.80 s)
- HARD_BRAKE, since C:e16 (t = 4.80 s)
- EGO_PATH of track_001, since C:e17 (t = 5.00 s)
- STOP, since C:e21 (t = 5.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 13.95 | 279 | 70.8 m / -2 deg | 1.46 m (5.20) | 2.1 m / -49 deg | 10.7 m/s |
| track_002 | 0.00 | 4.45 | 88 | 45.2 m / -57 deg | 7.51 m (4.45) | 7.5 m / -52 deg | 9.8 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001.
- t = 0.00 s: C's radar started tracking track_002.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: C observed track_002 start closing in (already the case when first observed).
- t = 1.65 s: C started applying strong throttle.
- t = 2.10 s: C stopped applying strong throttle.
- t = 2.25 s: C's time-to-contact with track_002 became critical.
- t = 2.50 s: C's time-to-contact with track_001 became critical.
- t = 3.15 s: C's time-to-contact with track_002 stopped being critical.
- t = 4.45 s: C's radar lost track_002.
- t = 4.75 s: C's collision sensor recorded a contact (peak impulse 1638 N*s).
- t = 4.75 s: C started applying strong throttle.
- t = 4.80 s: C stopped applying strong throttle.
- t = 4.80 s: C started braking.
- t = 4.80 s: C started braking hard.
- t = 5.00 s: C observed track_001 enter its forward path corridor.
- t = 5.05 s: C's time-to-contact with track_001 stopped being critical.
- t = 5.05 s: C observed track_001 stop closing in.
- t = 5.05 s: C stopped moving.
- t = 5.05 s: C came to a stop.
