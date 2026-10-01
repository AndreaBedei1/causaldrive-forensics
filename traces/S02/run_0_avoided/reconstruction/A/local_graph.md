# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 56.33916341140866 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 13 (PRECEDES 8, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.35 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e05 | 2.85 | BRAKE_START | A | - | controls |  |
| A:e06 | 3.25 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e07 | 4.05 | CLOSING_END | A | track_001 | radar |  |
| A:e08 | 4.10 | BRAKE_END | A | - | controls |  |
| A:e09 | 5.30 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |

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
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_LEFT track_001<br>A:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 2.35 | A:e04 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING<br>track_001: CLOSING | 2.30 |
| 2.85 | A:e05 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT | 2.80 |
| 3.25 | A:e06 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CUT_IN_FROM_LEFT | 3.20 |
| 4.05 | A:e07 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 4.10 | A:e08 BRAKE_END | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 5.30 | A:e09 CUT_IN_FROM_LEFT_END track_001 | ego: MOVING<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 5.20 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- EGO_PATH of track_001, since A:e06 (t = 3.25 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CUT_IN_FROM_LEFT_START 2.35, no critical TTC after it; EGO_PATH_ENTRY 3.25, no critical TTC

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
- t = 2.35 s: A observed track_001 cutting in from the left.
- t = 2.85 s: A started braking.
- t = 3.25 s: A observed track_001 enter its forward path corridor.
- t = 4.05 s: A observed track_001 stop closing in.
- t = 4.10 s: A released the brake.
- t = 5.30 s: A observed track_001's cut-in from the left settle.
