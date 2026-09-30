# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 245.13907996192575 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 38 (PRECEDES 34, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.85 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e03 | 1.95 | BRAKE_START | A | - | controls |  |
| A:e04 | 1.95 | HARD_BRAKE_START | A | - | controls |  |
| A:e05 | 2.15 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e06 | 2.20 | HARD_BRAKE_END | A | - | controls |  |
| A:e07 | 3.80 | BRAKE_END | A | - | controls |  |
| A:e08 | 3.80 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e09 | 3.80 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e10 | 3.80 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e11 | 5.20 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 5.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e13 | 5.25 | COLLISION | A | - | collision_sensor | peak_impulse=12489.77 |
| A:e14 | 5.25 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e15 | 5.30 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e16 | 5.30 | BRAKE_START | A | - | controls |  |
| A:e17 | 5.30 | HARD_BRAKE_START | A | - | controls |  |
| A:e18 | 5.40 | MOVING_END | A | - | ego |  |
| A:e19 | 5.40 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e11
    A:e07 --PRECEDES--> A:e12
    A:e08 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e08 --SAME_TRACK--> A:e09
    A:e08 --SAME_TRACK--> A:e10
    A:e08 --SAME_TRACK--> A:e11
    A:e08 --SAME_TRACK--> A:e12
```

## States still active when observation ended

- CLOSING of track_001, since A:e09 (t = 3.80 s); the track was lost at 5.20 s
- CRITICAL_TTC of track_001, since A:e10 (t = 3.80 s); the track was lost at 5.20 s
- EGO_PATH of track_001, since A:e11 (t = 5.20 s); the track was lost at 5.20 s
- BRAKE, since A:e16 (t = 5.30 s)
- HARD_BRAKE, since A:e17 (t = 5.30 s)
- STOP, since A:e19 (t = 5.40 s)

## Sign detection windows

- STOP sign sign-0: detected 1.85 s -> 2.15 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.80 | 5.20 | 29 | 21.4 m / -60 deg | 1.64 m (5.20) | 1.6 m / -57 deg | 10.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.85 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: A started braking.
- t = 1.95 s: A started braking hard.
- t = 2.15 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.20 s: A stopped braking hard.
- t = 3.80 s: A released the brake.
- t = 3.80 s: A's radar started tracking track_001.
- t = 3.80 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.80 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 5.20 s: A observed track_001 enter its forward path corridor.
- t = 5.20 s: A's radar lost track_001.
- t = 5.25 s: A's collision sensor recorded a contact (peak impulse 12490 N*s).
- t = 5.25 s: A started applying strong throttle.
- t = 5.30 s: A stopped applying strong throttle.
- t = 5.30 s: A started braking.
- t = 5.30 s: A started braking hard.
- t = 5.40 s: A stopped moving.
- t = 5.40 s: A came to a stop.
