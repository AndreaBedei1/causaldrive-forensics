# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 46.201942194253206 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 27 (PRECEDES 18, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.15 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e05 | 1.35 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e06 | 1.65 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e07 | 2.20 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e08 | 2.75 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e09 | 2.85 | BRAKE_START | A | - | controls |  |
| A:e10 | 2.85 | HARD_BRAKE_START | A | - | controls |  |
| A:e11 | 3.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e12 | 3.15 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e13 | 3.70 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e14 | 3.70 | HARD_BRAKE_END | A | - | controls |  |
| A:e15 | 4.05 | CLOSING_END | A | track_001 | radar |  |
| A:e16 | 4.10 | BRAKE_END | A | - | controls |  |
| A:e17 | 5.25 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e12
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e15
    A:e02 --SAME_TRACK--> A:e17
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 1.15 | A:e04 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING | 1.10 |
| 1.35 | A:e05 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING | 1.30 |
| 1.65 | A:e06 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 1.60 |
| 2.20 | A:e07 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT | 2.10 |
| 2.75 | A:e08 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT, CUT_IN_FROM_LEFT | 2.70 |
| 2.85 | A:e09 BRAKE_START<br>A:e10 HARD_BRAKE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT, CUT_IN_FROM_LEFT | 2.80 |
| 3.10 | A:e11 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT, CUT_IN_FROM_LEFT | 3.00 |
| 3.15 | A:e12 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT, CUT_IN_FROM_LEFT | 3.10 |
| 3.70 | A:e13 PREDICTED_PATH_CONFLICT_END track_001<br>A:e14 HARD_BRAKE_END | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, PATH_CONFLICT, CUT_IN_FROM_LEFT | 3.60 |
| 4.05 | A:e15 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 4.10 | A:e16 BRAKE_END | ego: MOVING, BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 5.25 | A:e17 CUT_IN_FROM_LEFT_END track_001 | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH, CUT_IN_FROM_LEFT | 5.20 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- EGO_PATH of track_001, since A:e12 (t = 3.15 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 15.15 | 302 | 24.6 m / -8 deg | 6.34 m (4.15) | 15.2 m / -0 deg | 9.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.15 s: A started applying strong throttle.
- t = 1.35 s: A stopped applying strong throttle.
- t = 1.65 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 2.20 s: A observed track_001 cutting in from the left.
- t = 2.75 s: A's time-to-contact with track_001 became critical.
- t = 2.85 s: A started braking.
- t = 2.85 s: A started braking hard.
- t = 3.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.15 s: A observed track_001 enter its forward path corridor.
- t = 3.70 s: A stopped predicting a path conflict with track_001.
- t = 3.70 s: A stopped braking hard.
- t = 4.05 s: A observed track_001 stop closing in.
- t = 4.10 s: A released the brake.
- t = 5.25 s: A observed track_001's cut-in from the left settle.
