# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 23.34804853051901 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 44 (PRECEDES 35, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 0.00 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 0.20 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e06 | 0.20 | TRACK_APPEARED | A | track_003 | radar |  |
| A:e07 | 0.20 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e08 | 0.20 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e09 | 1.45 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e10 | 1.80 | COLLISION | A | - | collision_sensor | peak_impulse=1247.19 |
| A:e11 | 1.85 | BRAKE_START | A | - | controls |  |
| A:e12 | 1.85 | HARD_BRAKE_START | A | - | controls |  |
| A:e13 | 1.90 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e14 | 1.90 | CLOSING_END | A | track_001 | radar |  |
| A:e15 | 2.50 | CLOSING_END | A | track_002 | radar |  |
| A:e16 | 2.50 | CLOSING_END | A | track_003 | radar |  |
| A:e17 | 2.50 | MOVING_END | A | - | ego |  |
| A:e18 | 2.50 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e05
    A:e01 --PRECEDES--> A:e06
    A:e01 --PRECEDES--> A:e07
    A:e01 --PRECEDES--> A:e08
    A:e02 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e07
    A:e02 --PRECEDES--> A:e08
    A:e03 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e07
    A:e03 --PRECEDES--> A:e08
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e04 --PRECEDES--> A:e08
    A:e05 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e13 --PRECEDES--> A:e18
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e05 --SAME_TRACK--> A:e07
    A:e06 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e14
    A:e05 --SAME_TRACK--> A:e15
    A:e06 --SAME_TRACK--> A:e16
```

## States still active when observation ended

- EGO_PATH of track_001, since A:e09 (t = 1.45 s)
- BRAKE, since A:e11 (t = 1.85 s)
- HARD_BRAKE, since A:e12 (t = 1.85 s)
- STOP, since A:e18 (t = 2.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.95 | 291 | 7.8 m / +39 deg | 0.98 m (1.85) | 1.1 m / +51 deg | 8.7 m/s |
| track_002 | 0.20 | 14.95 | 296 | 47.4 m / -57 deg | 31.98 m (8.00) | 32.2 m / -14 deg | 1.9 m/s |
| track_003 | 0.20 | 14.95 | 294 | 49.9 m / -53 deg | 34.13 m (7.25) | 34.5 m / -8 deg | 1.1 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 0.20 s: A's radar started tracking track_002.
- t = 0.20 s: A's radar started tracking track_003.
- t = 0.20 s: A observed track_002 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_003 start closing in (already the case when first observed).
- t = 1.45 s: A observed track_001 enter its forward path corridor.
- t = 1.80 s: A's collision sensor recorded a contact (peak impulse 1247 N*s).
- t = 1.85 s: A started braking.
- t = 1.85 s: A started braking hard.
- t = 1.90 s: A's time-to-contact with track_001 stopped being critical.
- t = 1.90 s: A observed track_001 stop closing in.
- t = 2.50 s: A observed track_002 stop closing in.
- t = 2.50 s: A observed track_003 stop closing in.
- t = 2.50 s: A stopped moving.
- t = 2.50 s: A came to a stop.
