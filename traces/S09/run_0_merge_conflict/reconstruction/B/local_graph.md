# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 23.34804853051901 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 24 (PRECEDES 19, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.20 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e03 | 0.20 | TRACK_APPEARED | B | track_002 | radar |  |
| B:e04 | 0.20 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 0.20 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e06 | 0.20 | CRITICAL_TTC_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 0.80 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e08 | 1.60 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e09 | 1.65 | TRACK_LOST | B | track_001 | radar |  |
| B:e10 | 1.80 | COLLISION | B | - | collision_sensor | peak_impulse=1247.19 |
| B:e11 | 1.85 | BRAKE_START | B | - | controls |  |
| B:e12 | 1.85 | HARD_BRAKE_START | B | - | controls |  |
| B:e13 | 1.90 | TRACK_LOST | B | track_002 | radar |  |
| B:e14 | 2.55 | MOVING_END | B | - | ego |  |
| B:e15 | 2.55 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e01 --PRECEDES--> B:e03
    B:e01 --PRECEDES--> B:e04
    B:e01 --PRECEDES--> B:e05
    B:e01 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e07
    B:e03 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e02 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e05
    B:e02 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e09
    B:e03 --SAME_TRACK--> B:e13
```

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 0.20 s); the track was lost at 1.65 s
- CLOSING of track_002, since B:e05 (t = 0.20 s); the track was lost at 1.90 s
- CRITICAL_TTC of track_001, since B:e06 (t = 0.20 s); the track was lost at 1.65 s
- BRAKE, since B:e11 (t = 1.85 s)
- HARD_BRAKE, since B:e12 (t = 1.85 s)
- STOP, since B:e15 (t = 2.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.20 | 1.65 | 30 | 11.2 m / +54 deg | 2.22 m (1.65) | 2.2 m / +55 deg | 3.8 m/s |
| track_002 | 0.20 | 1.90 | 33 | 23.8 m / +56 deg | 14.05 m (1.90) | 14.1 m / +58 deg | 1.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.20 s: B's radar started tracking track_001.
- t = 0.20 s: B's radar started tracking track_002.
- t = 0.20 s: B observed track_001 start closing in (already the case when first observed).
- t = 0.20 s: B observed track_002 start closing in (already the case when first observed).
- t = 0.20 s: B's time-to-contact with track_001 became critical (already the case when first observed).
- t = 0.80 s: B started applying strong throttle.
- t = 1.60 s: B stopped applying strong throttle.
- t = 1.65 s: B's radar lost track_001.
- t = 1.80 s: B's collision sensor recorded a contact (peak impulse 1247 N*s).
- t = 1.85 s: B started braking.
- t = 1.85 s: B started braking hard.
- t = 1.90 s: B's radar lost track_002.
- t = 2.55 s: B stopped moving.
- t = 2.55 s: B came to a stop.
