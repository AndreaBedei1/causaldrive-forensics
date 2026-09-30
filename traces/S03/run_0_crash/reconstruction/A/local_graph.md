# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 84.233761690557 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 15 (PRECEDES 12, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.05 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 2.05 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.35 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 3.35 | TRACK_LOST | A | track_001 | radar |  |
| A:e06 | 4.25 | COLLISION | A | - | collision_sensor | peak_impulse=12077.22 |
| A:e07 | 4.30 | BRAKE_START | A | - | controls |  |
| A:e08 | 4.30 | HARD_BRAKE_START | A | - | controls |  |
| A:e09 | 4.90 | MOVING_END | A | - | ego |  |
| A:e10 | 4.90 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
```

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 2.05 s); the track was lost at 3.35 s
- CRITICAL_TTC of track_001, since A:e04 (t = 2.35 s); the track was lost at 3.35 s
- BRAKE, since A:e07 (t = 4.30 s)
- HARD_BRAKE, since A:e08 (t = 4.30 s)
- STOP, since A:e10 (t = 4.90 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.05 | 3.35 | 26 | 34.2 m / +56 deg | 14.40 m (3.35) | 14.4 m / +59 deg | 13.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.05 s: A's radar started tracking track_001.
- t = 2.05 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.35 s: A's time-to-contact with track_001 became critical.
- t = 3.35 s: A's radar lost track_001.
- t = 4.25 s: A's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.30 s: A started braking.
- t = 4.30 s: A started braking hard.
- t = 4.90 s: A stopped moving.
- t = 4.90 s: A came to a stop.
