# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 478.86066130176187 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 20 (PRECEDES 14, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.00 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e05 | 2.00 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.00 | CRITICAL_TTC_START | A | track_002 | radar | active_at_first_observation=True |
| A:e07 | 2.45 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 3.80 | TRACK_LOST | A | track_002 | radar |  |
| A:e09 | 4.45 | TRACK_LOST | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e04
    A:e01 --PRECEDES--> A:e05
    A:e01 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
```

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e03 (t = 0.00 s); the track was lost at 4.45 s
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.80 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.80 s
- CRITICAL_TTC of track_001, since A:e07 (t = 2.45 s); the track was lost at 4.45 s

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 4.45 | 87 | 70.9 m / -3 deg | 2.43 m (4.45) | 2.4 m / -83 deg | 5.8 m/s |
| track_002 | 2.00 | 3.80 | 37 | 28.2 m / +36 deg | 6.10 m (3.80) | 6.1 m / +60 deg | 9.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.00 s: A's radar started tracking track_002.
- t = 2.00 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.00 s: A's time-to-contact with track_002 became critical (already the case when first observed).
- t = 2.45 s: A's time-to-contact with track_001 became critical.
- t = 3.80 s: A's radar lost track_002.
- t = 4.45 s: A's radar lost track_001.
