# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 13.349094610661268 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 132 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.05 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 11; edges: 16 (PRECEDES 10, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_FRONT | A | track_001 | radar |  |
| A:e03 | 0.45 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.65 | CLOSING_END | A | track_001 | radar |  |
| A:e05 | 4.20 | CLOSING_START | A | track_001 | radar |  |
| A:e06 | 5.00 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 5.05 | BRAKE_START | A | - | controls |  |
| A:e08 | 6.25 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e09 | 6.35 | CLOSING_END | A | track_001 | radar |  |
| A:e10 | 6.35 | MOVING_END | A | - | ego |  |
| A:e11 | 6.35 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_FRONT track_001 | ego: not yet observed | - |
| 0.45 | A:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 0.40 |
| 1.65 | A:e04 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 1.60 |
| 4.20 | A:e05 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 4.10 |
| 5.00 | A:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 4.90 |
| 5.05 | A:e07 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.00 |
| 6.25 | A:e08 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 6.20 |
| 6.35 | A:e09 CLOSING_END track_001<br>A:e10 MOVING_END<br>A:e11 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH | 6.30 |

## States still active when observation ended

- BRAKE, since A:e07 (t = 5.05 s)
- STOP, since A:e11 (t = 6.35 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 5.00

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 13.05 | 256 | 25.8 m / -0 deg | 7.98 m (6.35) | 9.6 m / +1 deg | 13.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.45 s: A observed track_001 start closing in.
- t = 1.65 s: A observed track_001 stop closing in.
- t = 4.20 s: A observed track_001 start closing in.
- t = 5.00 s: A's time-to-contact with track_001 became critical.
- t = 5.05 s: A started braking.
- t = 6.25 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.35 s: A observed track_001 stop closing in.
- t = 6.35 s: A stopped moving.
- t = 6.35 s: A came to a stop.
