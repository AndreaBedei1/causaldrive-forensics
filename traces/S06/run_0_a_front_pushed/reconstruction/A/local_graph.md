# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 153.14251230284572 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 301 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (29.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 37 (PRECEDES 25, SAME_TRACK 12)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_FRONT | A | track_001 | radar |  |
| A:e03 | 0.45 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.00 | TRACK_APPEARED_FRONT | A | track_002 | radar |  |
| A:e05 | 1.00 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 1.65 | CLOSING_END | A | track_001 | radar |  |
| A:e07 | 1.95 | CLOSING_END | A | track_002 | radar |  |
| A:e08 | 3.25 | CLOSING_START | A | track_002 | radar |  |
| A:e09 | 4.00 | CLOSING_START | A | track_001 | radar |  |
| A:e10 | 4.15 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e11 | 4.70 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e12 | 5.55 | BRAKE_START | A | - | controls |  |
| A:e13 | 5.90 | COLLISION | A | - | collision_sensor | peak_impulse=11621.71 |
| A:e14 | 6.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e15 | 6.10 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e16 | 6.10 | CLOSING_END | A | track_001 | radar |  |
| A:e17 | 6.10 | CLOSING_END | A | track_002 | radar |  |
| A:e18 | 6.15 | MOVING_END | A | - | ego |  |
| A:e19 | 6.15 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e14 --PRECEDES--> A:e19
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e14
    A:e04 --SAME_TRACK--> A:e15
    A:e02 --SAME_TRACK--> A:e16
    A:e04 --SAME_TRACK--> A:e17
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_FRONT track_001 | ego: not yet observed | - |
| 0.45 | A:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 0.40 |
| 1.00 | A:e04 TRACK_APPEARED_FRONT track_002<br>A:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 0.90 |
| 1.65 | A:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH | 1.60 |
| 1.95 | A:e07 CLOSING_END track_002 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH | 1.90 |
| 3.25 | A:e08 CLOSING_START track_002 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH | 3.20 |
| 4.00 | A:e09 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH | 3.90 |
| 4.15 | A:e10 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH | 4.10 |
| 4.70 | A:e11 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.60 |
| 5.55 | A:e12 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.50 |
| 5.90 | A:e13 COLLISION | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.80 |
| 6.10 | A:e14 CRITICAL_TTC_END track_001<br>A:e15 CRITICAL_TTC_END track_002<br>A:e16 CLOSING_END track_001<br>A:e17 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 6.00 |
| 6.15 | A:e18 MOVING_END<br>A:e19 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH | 6.10 |

## States still active when observation ended

- BRAKE, since A:e12 (t = 5.55 s)
- STOP, since A:e19 (t = 6.15 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 4.70, COLLISION 5.90 (+1.20 s)
- track_002: CRITICAL_TTC_START 4.15, COLLISION 5.90 (+1.75 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 29.95 | 596 | 23.9 m / -0 deg | 2.62 m (6.10) | 3.5 m / -0 deg | 14.0 m/s |
| track_002 | 1.00 | 29.95 | 566 | 39.9 m / -1 deg | 6.93 m (12.70) | 7.0 m / -1 deg | 14.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.45 s: A observed track_001 start closing in.
- t = 1.00 s: A's radar started tracking track_002, which appeared in front of it.
- t = 1.00 s: A observed track_002 start closing in (already the case when first observed).
- t = 1.65 s: A observed track_001 stop closing in.
- t = 1.95 s: A observed track_002 stop closing in.
- t = 3.25 s: A observed track_002 start closing in.
- t = 4.00 s: A observed track_001 start closing in.
- t = 4.15 s: A's time-to-contact with track_002 became critical.
- t = 4.70 s: A's time-to-contact with track_001 became critical.
- t = 5.55 s: A started braking.
- t = 5.90 s: A's collision sensor recorded a contact (peak impulse 11622 N*s).
- t = 6.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.10 s: A's time-to-contact with track_002 stopped being critical.
- t = 6.10 s: A observed track_001 stop closing in.
- t = 6.10 s: A observed track_002 stop closing in.
- t = 6.15 s: A stopped moving.
- t = 6.15 s: A came to a stop.
