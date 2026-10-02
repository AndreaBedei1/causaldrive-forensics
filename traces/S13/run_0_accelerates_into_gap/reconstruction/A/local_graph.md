# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 138.9119843505323 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 38 (PRECEDES 27, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.75 | SPEED_LIMIT_EXCEEDED_START | A | - | ego |  |
| A:e03 | 3.40 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e04 | 3.40 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 3.95 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e06 | 4.15 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e07 | 5.45 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e08 | 5.65 | COLLISION | A | - | collision_sensor | peak_impulse=5215.85 |
| A:e09 | 5.65 | SPEED_LIMIT_EXCEEDED_END | A | - | ego |  |
| A:e10 | 5.70 | BRAKE_START | A | - | controls |  |
| A:e11 | 5.80 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e12 | 5.80 | CLOSING_END | A | track_001 | radar |  |
| A:e13 | 6.55 | CLOSING_START | A | track_001 | radar |  |
| A:e14 | 6.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e15 | 6.85 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e16 | 6.85 | CLOSING_END | A | track_001 | radar |  |
| A:e17 | 6.95 | MOVING_END | A | - | ego |  |
| A:e18 | 6.95 | STOP_START | A | - | ego |  |
| A:e19 | 7.05 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e19
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e05
    A:e03 --SAME_TRACK--> A:e06
    A:e03 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
    A:e03 --SAME_TRACK--> A:e14
    A:e03 --SAME_TRACK--> A:e15
    A:e03 --SAME_TRACK--> A:e16
    A:e03 --SAME_TRACK--> A:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 2.75 | A:e02 SPEED_LIMIT_EXCEEDED_START | ego: MOVING | 2.70 |
| 3.40 | A:e03 TRACK_APPEARED_LEFT track_001<br>A:e04 CLOSING_START track_001 | ego: MOVING, SPEED_LIMIT_EXCEEDED | 3.30 |
| 3.95 | A:e05 CRITICAL_TTC_START track_001 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING | 3.90 |
| 4.15 | A:e06 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING, CRITICAL_TTC | 4.10 |
| 5.45 | A:e07 EGO_PATH_ENTRY track_001 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 5.40 |
| 5.65 | A:e08 COLLISION<br>A:e09 SPEED_LIMIT_EXCEEDED_END | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 5.60 |
| 5.70 | A:e10 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 5.60 |
| 5.80 | A:e11 CRITICAL_TTC_END track_001<br>A:e12 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 5.70 |
| 6.55 | A:e13 CLOSING_START track_001<br>A:e14 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 6.50 |
| 6.85 | A:e15 CRITICAL_TTC_END track_001<br>A:e16 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 6.80 |
| 6.95 | A:e17 MOVING_END<br>A:e18 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 6.90 |
| 7.05 | A:e19 CUT_IN_FROM_LEFT_END track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 7.00 |

## States still active when observation ended

- EGO_PATH of track_001, since A:e07 (t = 5.45 s)
- BRAKE, since A:e10 (t = 5.70 s)
- STOP, since A:e18 (t = 6.95 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 3.95 <= CUT_IN_FROM_LEFT_START 4.15 (+0.20 s); EGO_PATH_ENTRY 5.45 after critical TTC (+1.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.40 | 9.95 | 126 | 20.0 m / -9 deg | 2.82 m (6.85) | 3.0 m / +4 deg | 11.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.75 s: A began exceeding the speed limit.
- t = 3.40 s: A's radar started tracking track_001, which appeared on its left.
- t = 3.40 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.95 s: A's time-to-contact with track_001 became critical.
- t = 4.15 s: A observed track_001 cutting in from the left.
- t = 5.45 s: A observed track_001 enter its forward path corridor.
- t = 5.65 s: A's collision sensor recorded a contact (peak impulse 5216 N*s).
- t = 5.65 s: A returned within the speed limit.
- t = 5.70 s: A started braking.
- t = 5.80 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.80 s: A observed track_001 stop closing in.
- t = 6.55 s: A observed track_001 start closing in.
- t = 6.55 s: A's time-to-contact with track_001 became critical.
- t = 6.85 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.85 s: A observed track_001 stop closing in.
- t = 6.95 s: A stopped moving.
- t = 6.95 s: A came to a stop.
- t = 7.05 s: A observed track_001's cut-in from the left settle.
