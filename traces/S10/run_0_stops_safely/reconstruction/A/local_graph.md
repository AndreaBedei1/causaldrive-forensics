# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 265.36246832087636 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 97 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.55 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 27 (PRECEDES 20, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.90 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e03 | 2.15 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.55 | BRAKE_START | A | - | controls |  |
| A:e05 | 2.55 | HARD_BRAKE_START | A | - | controls |  |
| A:e06 | 3.35 | MOVING_END | A | - | ego |  |
| A:e07 | 3.35 | STOP_START | A | - | ego |  |
| A:e08 | 3.70 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e09 | 3.70 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e10 | 4.25 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e11 | 5.80 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 5.95 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e13 | 6.10 | CLOSING_END | A | track_001 | radar |  |
| A:e14 | 6.25 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e15 | 7.00 | TRACK_LOST | A | track_001 | radar |  |
| A:e16 | 9.55 | STRONG_THROTTLE_START | A | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e08 --SAME_TRACK--> A:e09
    A:e08 --SAME_TRACK--> A:e10
    A:e08 --SAME_TRACK--> A:e11
    A:e08 --SAME_TRACK--> A:e12
    A:e08 --SAME_TRACK--> A:e13
    A:e08 --SAME_TRACK--> A:e14
    A:e08 --SAME_TRACK--> A:e15
```

## States still active when observation ended

- BRAKE, since A:e04 (t = 2.55 s)
- HARD_BRAKE, since A:e05 (t = 2.55 s)
- STOP, since A:e07 (t = 3.35 s)
- STRONG_THROTTLE, since A:e16 (t = 9.55 s)

## Sign detection windows

- STOP sign sign-0: detected 1.90 s -> 2.15 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.70 | 7.00 | 64 | 23.3 m / -60 deg | 5.33 m (6.10) | 9.4 m / +60 deg | 9.6 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.90 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 2.15 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.55 s: A started braking.
- t = 2.55 s: A started braking hard.
- t = 3.35 s: A stopped moving.
- t = 3.35 s: A came to a stop.
- t = 3.70 s: A's radar started tracking track_001.
- t = 3.70 s: A observed track_001 start closing in (already the case when first observed).
- t = 4.25 s: A's time-to-contact with track_001 became critical.
- t = 5.80 s: A observed track_001 enter its forward path corridor.
- t = 5.95 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.10 s: A observed track_001 stop closing in.
- t = 6.25 s: A observed track_001 leave its forward path corridor.
- t = 7.00 s: A's radar lost track_001.
- t = 9.55 s: A started applying strong throttle.
