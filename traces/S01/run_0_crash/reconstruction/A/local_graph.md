# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 29.69283339381218 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 26 (PRECEDES 20, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.45 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.15 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e05 | 1.35 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e06 | 1.60 | CLOSING_END | A | track_001 | radar |  |
| A:e07 | 4.25 | CLOSING_START | A | track_001 | radar |  |
| A:e08 | 5.00 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e09 | 5.55 | BRAKE_START | A | - | controls |  |
| A:e10 | 6.50 | COLLISION | A | - | collision_sensor | peak_impulse=17663.06 |
| A:e11 | 6.50 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e12 | 6.50 | CLOSING_END | A | track_001 | radar |  |
| A:e13 | 6.55 | MOVING_END | A | - | ego |  |
| A:e14 | 6.55 | STOP_START | A | - | ego |  |
| A:e15 | 6.55 | HARD_BRAKE_START | A | - | controls |  |

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
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e14
    A:e10 --PRECEDES--> A:e15
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e12
```

## States still active when observation ended

- BRAKE, since A:e09 (t = 5.55 s)
- STOP, since A:e14 (t = 6.55 s)
- HARD_BRAKE, since A:e15 (t = 6.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 238 | 23.5 m / -1 deg | 0.75 m (11.95) | 0.8 m / +0 deg | 14.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.45 s: A observed track_001 start closing in.
- t = 1.15 s: A started applying strong throttle.
- t = 1.35 s: A stopped applying strong throttle.
- t = 1.60 s: A observed track_001 stop closing in.
- t = 4.25 s: A observed track_001 start closing in.
- t = 5.00 s: A's time-to-contact with track_001 became critical.
- t = 5.55 s: A started braking.
- t = 6.50 s: A's collision sensor recorded a contact (peak impulse 17663 N*s).
- t = 6.50 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.50 s: A observed track_001 stop closing in.
- t = 6.55 s: A stopped moving.
- t = 6.55 s: A came to a stop.
- t = 6.55 s: A started braking hard.
