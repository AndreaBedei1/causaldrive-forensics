# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 188.47773114964366 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 35 (PRECEDES 29, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.45 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.15 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e05 | 1.35 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e06 | 1.60 | CLOSING_END | A | track_001 | radar |  |
| A:e07 | 3.90 | CLOSING_START | A | track_001 | radar |  |
| A:e08 | 4.60 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e09 | 5.70 | COLLISION | A | - | collision_sensor | peak_impulse=31406.82 |
| A:e10 | 5.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e11 | 5.70 | CLOSING_END | A | track_001 | radar |  |
| A:e12 | 5.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e13 | 5.75 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e14 | 5.75 | BRAKE_START | A | - | controls |  |
| A:e15 | 5.75 | HARD_BRAKE_START | A | - | controls |  |
| A:e16 | 5.85 | MOVING_END | A | - | ego |  |
| A:e17 | 5.85 | STOP_START | A | - | ego |  |

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
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e13
    A:e09 --PRECEDES--> A:e14
    A:e09 --PRECEDES--> A:e15
    A:e10 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e14
    A:e10 --PRECEDES--> A:e15
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
```

## States still active when observation ended

- BRAKE, since A:e14 (t = 5.75 s)
- HARD_BRAKE, since A:e15 (t = 5.75 s)
- STOP, since A:e17 (t = 5.85 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.15 | 284 | 19.6 m / -1 deg | 0.72 m (5.70) | 1.0 m / +1 deg | 14.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.45 s: A observed track_001 start closing in.
- t = 1.15 s: A started applying strong throttle.
- t = 1.35 s: A stopped applying strong throttle.
- t = 1.60 s: A observed track_001 stop closing in.
- t = 3.90 s: A observed track_001 start closing in.
- t = 4.60 s: A's time-to-contact with track_001 became critical.
- t = 5.70 s: A's collision sensor recorded a contact (peak impulse 31407 N*s).
- t = 5.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.70 s: A observed track_001 stop closing in.
- t = 5.70 s: A started applying strong throttle.
- t = 5.75 s: A stopped applying strong throttle.
- t = 5.75 s: A started braking.
- t = 5.75 s: A started braking hard.
- t = 5.85 s: A stopped moving.
- t = 5.85 s: A came to a stop.
