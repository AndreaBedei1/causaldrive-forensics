# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 109.8685935139656 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 14 (PRECEDES 8, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.50 | CLOSING_END | A | track_001 | radar |  |
| A:e05 | 2.45 | CLOSING_START | A | track_001 | radar |  |
| A:e06 | 2.85 | BRAKE_START | A | - | controls |  |
| A:e07 | 4.00 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e08 | 5.30 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e09 | 8.00 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |

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
    A:e08 --PRECEDES--> A:e09
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_LEFT track_001<br>A:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 1.50 | A:e04 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING | 1.40 |
| 2.45 | A:e05 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state | 2.40 |
| 2.85 | A:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING | 2.80 |
| 4.00 | A:e07 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING | 3.90 |
| 5.30 | A:e08 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CUT_IN_FROM_LEFT | 5.20 |
| 8.00 | A:e09 CUT_IN_FROM_LEFT_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT | 7.90 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e05 (t = 2.45 s)
- BRAKE, since A:e06 (t = 2.85 s)
- EGO_PATH of track_001, since A:e08 (t = 5.30 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CUT_IN_FROM_LEFT_START 4.00, no critical TTC after it; EGO_PATH_ENTRY 5.30, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 9.95 | 169 | 21.4 m / -8 deg | 4.58 m (9.95) | 4.6 m / -0 deg | 10.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.50 s: A observed track_001 stop closing in.
- t = 2.45 s: A observed track_001 start closing in.
- t = 2.85 s: A started braking.
- t = 4.00 s: A observed track_001 cutting in from the left.
- t = 5.30 s: A observed track_001 enter its forward path corridor.
- t = 8.00 s: A observed track_001's cut-in from the left settle.
