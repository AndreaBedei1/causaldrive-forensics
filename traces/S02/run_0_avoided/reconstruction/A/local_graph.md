# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 56.33916341140866 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 22 (PRECEDES 15, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.15 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e05 | 1.35 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e06 | 2.35 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e07 | 2.80 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 2.85 | BRAKE_START | A | - | controls |  |
| A:e09 | 2.85 | HARD_BRAKE_START | A | - | controls |  |
| A:e10 | 3.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e11 | 3.25 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 3.70 | HARD_BRAKE_END | A | - | controls |  |
| A:e13 | 4.05 | CLOSING_END | A | track_001 | radar |  |
| A:e14 | 4.10 | BRAKE_END | A | - | controls |  |
| A:e15 | 5.30 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e15
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_LEFT track_001<br>A:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 1.15 | A:e04 STRONG_THROTTLE_START | ego: MOVING<br>track_001: CLOSING | 1.10 |
| 1.35 | A:e05 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING | 1.30 |
| 2.35 | A:e06 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING<br>track_001: CLOSING | 2.30 |
| 2.80 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT | 2.70 |
| 2.85 | A:e08 BRAKE_START<br>A:e09 HARD_BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 2.80 |
| 3.10 | A:e10 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.00 |
| 3.25 | A:e11 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CUT_IN_FROM_LEFT | 3.20 |
| 3.70 | A:e12 HARD_BRAKE_END | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT | 3.60 |
| 4.05 | A:e13 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 4.10 | A:e14 BRAKE_END | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 5.30 | A:e15 CUT_IN_FROM_LEFT_END track_001 | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 5.20 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- EGO_PATH of track_001, since A:e11 (t = 3.25 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 15.15 | 277 | 24.6 m / -8 deg | 6.36 m (4.15) | 15.2 m / -1 deg | 8.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.15 s: A started applying strong throttle.
- t = 1.35 s: A stopped applying strong throttle.
- t = 2.35 s: A observed track_001 cutting in from the left.
- t = 2.80 s: A's time-to-contact with track_001 became critical.
- t = 2.85 s: A started braking.
- t = 2.85 s: A started braking hard.
- t = 3.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.25 s: A observed track_001 enter its forward path corridor.
- t = 3.70 s: A stopped braking hard.
- t = 4.05 s: A observed track_001 stop closing in.
- t = 4.10 s: A released the brake.
- t = 5.30 s: A observed track_001's cut-in from the left settle.
