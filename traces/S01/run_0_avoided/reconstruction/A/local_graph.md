# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 21.149357691407204 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 132 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.05 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 28 (PRECEDES 20, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.10 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.45 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.15 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e05 | 1.35 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e06 | 1.60 | CLOSING_END | A | track_001 | radar |  |
| A:e07 | 4.25 | CLOSING_START | A | track_001 | radar |  |
| A:e08 | 4.70 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e09 | 5.00 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e10 | 5.05 | BRAKE_START | A | - | controls |  |
| A:e11 | 5.05 | HARD_BRAKE_START | A | - | controls |  |
| A:e12 | 6.25 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e13 | 6.35 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e14 | 6.35 | CLOSING_END | A | track_001 | radar |  |
| A:e15 | 6.35 | MOVING_END | A | - | ego |  |
| A:e16 | 6.35 | STOP_START | A | - | ego |  |
| A:e17 | 13.05 | STRONG_THROTTLE_START | A | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e17
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e12
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e14
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.10 | A:e02 TRACK_APPEARED track_001 | ego: MOVING | 0.00 |
| 0.45 | A:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH | 0.40 |
| 1.15 | A:e04 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 1.10 |
| 1.35 | A:e05 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 1.30 |
| 1.60 | A:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 1.50 |
| 4.25 | A:e07 CLOSING_START track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH | 4.20 |
| 4.70 | A:e08 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH | 4.60 |
| 5.00 | A:e09 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT | 4.90 |
| 5.05 | A:e10 BRAKE_START<br>A:e11 HARD_BRAKE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 5.00 |
| 6.25 | A:e12 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 6.20 |
| 6.35 | A:e13 PREDICTED_PATH_CONFLICT_END track_001<br>A:e14 CLOSING_END track_001<br>A:e15 MOVING_END<br>A:e16 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT | 6.30 |
| 13.05 | A:e17 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH | 13.00 |

## States still active when observation ended

- BRAKE, since A:e10 (t = 5.05 s)
- HARD_BRAKE, since A:e11 (t = 5.05 s)
- STOP, since A:e16 (t = 6.35 s)
- STRONG_THROTTLE, since A:e17 (t = 13.05 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.10 | 13.05 | 251 | 23.6 m / -1 deg | 6.16 m (6.45) | 7.8 m / +1 deg | 14.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.10 s: A's radar started tracking track_001.
- t = 0.45 s: A observed track_001 start closing in.
- t = 1.15 s: A started applying strong throttle.
- t = 1.35 s: A stopped applying strong throttle.
- t = 1.60 s: A observed track_001 stop closing in.
- t = 4.25 s: A observed track_001 start closing in.
- t = 4.70 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 5.00 s: A's time-to-contact with track_001 became critical.
- t = 5.05 s: A started braking.
- t = 5.05 s: A started braking hard.
- t = 6.25 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.35 s: A stopped predicting a path conflict with track_001.
- t = 6.35 s: A observed track_001 stop closing in.
- t = 6.35 s: A stopped moving.
- t = 6.35 s: A came to a stop.
- t = 13.05 s: A started applying strong throttle.
