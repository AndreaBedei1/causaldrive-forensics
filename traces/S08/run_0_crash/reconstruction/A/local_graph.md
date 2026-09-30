# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 225.90415861457586 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 29 (PRECEDES 20, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.05 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.05 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.05 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e05 | 2.05 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.10 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 2.35 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e08 | 2.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e09 | 3.35 | TRACK_LOST | A | track_002 | radar |  |
| A:e10 | 3.45 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e11 | 4.25 | COLLISION | A | - | collision_sensor | peak_impulse=12077.22 |
| A:e12 | 4.30 | BRAKE_START | A | - | controls |  |
| A:e13 | 4.30 | HARD_BRAKE_START | A | - | controls |  |
| A:e14 | 4.75 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e15 | 4.90 | CLOSING_END | A | track_001 | radar |  |
| A:e16 | 4.90 | MOVING_END | A | - | ego |  |
| A:e17 | 4.90 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e14
    A:e02 --SAME_TRACK--> A:e15
```

## States still active when observation ended

- CLOSING of track_002, since A:e05 (t = 2.05 s); the track was lost at 3.35 s
- CRITICAL_TTC of track_002, since A:e07 (t = 2.35 s); the track was lost at 3.35 s
- BRAKE, since A:e12 (t = 4.30 s)
- HARD_BRAKE, since A:e13 (t = 4.30 s)
- STOP, since A:e17 (t = 4.90 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.05 | 15.15 | 303 | 74.1 m / -3 deg | 7.62 m (15.15) | 7.6 m / -23 deg | 8.9 m/s |
| track_002 | 2.05 | 3.35 | 26 | 34.2 m / +56 deg | 14.40 m (3.35) | 14.4 m / +59 deg | 13.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_001.
- t = 0.05 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.05 s: A's radar started tracking track_002.
- t = 2.05 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.10 s: A's time-to-contact with track_001 became critical.
- t = 2.35 s: A's time-to-contact with track_002 became critical.
- t = 2.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.35 s: A's radar lost track_002.
- t = 3.45 s: A's time-to-contact with track_001 became critical.
- t = 4.25 s: A's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.30 s: A started braking.
- t = 4.30 s: A started braking hard.
- t = 4.75 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.90 s: A observed track_001 stop closing in.
- t = 4.90 s: A stopped moving.
- t = 4.90 s: A came to a stop.
