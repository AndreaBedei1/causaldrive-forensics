# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 135.76189954578876 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 301 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (29.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 23 (PRECEDES 16, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.45 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.15 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e05 | 1.35 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e06 | 1.55 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e07 | 1.60 | CLOSING_END | A | track_001 | radar |  |
| A:e08 | 2.95 | TRACK_LOST | A | track_002 | radar |  |
| A:e09 | 4.00 | CLOSING_START | A | track_001 | radar |  |
| A:e10 | 4.70 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e11 | 5.55 | BRAKE_START | A | - | controls |  |
| A:e12 | 5.90 | COLLISION | A | - | collision_sensor | peak_impulse=11621.71 |
| A:e13 | 5.95 | HARD_BRAKE_START | A | - | controls |  |
| A:e14 | 6.25 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e15 | 6.25 | CLOSING_END | A | track_001 | radar |  |
| A:e16 | 6.25 | MOVING_END | A | - | ego |  |
| A:e17 | 6.25 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e07
    A:e06 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e14
    A:e02 --SAME_TRACK--> A:e15
```

## States still active when observation ended

- BRAKE, since A:e11 (t = 5.55 s)
- HARD_BRAKE, since A:e13 (t = 5.95 s)
- STOP, since A:e17 (t = 6.25 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 29.95 | 594 | 21.6 m / -1 deg | 0.26 m (6.25) | 0.8 m / -0 deg | 14.0 m/s |
| track_002 | 1.55 | 2.95 | 7 | 35.7 m / -0 deg | 35.44 m (2.10) | 36.0 m / +0 deg | 14.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.45 s: A observed track_001 start closing in.
- t = 1.15 s: A started applying strong throttle.
- t = 1.35 s: A stopped applying strong throttle.
- t = 1.55 s: A's radar started tracking track_002.
- t = 1.60 s: A observed track_001 stop closing in.
- t = 2.95 s: A's radar lost track_002.
- t = 4.00 s: A observed track_001 start closing in.
- t = 4.70 s: A's time-to-contact with track_001 became critical.
- t = 5.55 s: A started braking.
- t = 5.90 s: A's collision sensor recorded a contact (peak impulse 11622 N*s).
- t = 5.95 s: A started braking hard.
- t = 6.25 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.25 s: A observed track_001 stop closing in.
- t = 6.25 s: A stopped moving.
- t = 6.25 s: A came to a stop.
