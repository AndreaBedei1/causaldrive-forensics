# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 317.08158706873655 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 97 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.55 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 6; edges: 10 (PRECEDES 6, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.60 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 2.60 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 4.65 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 5.25 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e06 | 5.35 | TRACK_LOST | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
```

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e03 (t = 2.60 s); the track was lost at 5.35 s

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.60 | 5.35 | 56 | 33.8 m / +21 deg | 10.29 m (5.35) | 10.3 m / +60 deg | 4.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.60 s: A's radar started tracking track_001.
- t = 2.60 s: A observed track_001 start closing in (already the case when first observed).
- t = 4.65 s: A's time-to-contact with track_001 became critical.
- t = 5.25 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.35 s: A's radar lost track_001.
