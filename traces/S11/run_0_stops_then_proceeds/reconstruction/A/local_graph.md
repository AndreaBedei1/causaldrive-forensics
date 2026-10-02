# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 35.43246418610215 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 135 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.35 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 7; edges: 12 (PRECEDES 7, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.65 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e03 | 2.65 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 4.40 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 5.65 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e06 | 6.10 | CLOSING_END | A | track_001 | radar |  |
| A:e07 | 12.10 | TRACK_LOST | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 2.65 | A:e02 TRACK_APPEARED_RIGHT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 2.60 |
| 4.40 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 4.30 |
| 5.65 | A:e05 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 5.60 |
| 6.10 | A:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING | 6.00 |
| 12.10 | A:e07 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state | 12.00 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 4.40

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.65 | 12.10 | 161 | 35.3 m / +19 deg | 9.22 m (6.10) | 90.2 m / -178 deg | 9.1 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.65 s: A's radar started tracking track_001, which appeared on its right.
- t = 2.65 s: A observed track_001 start closing in (already the case when first observed).
- t = 4.40 s: A's time-to-contact with track_001 became critical.
- t = 5.65 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.10 s: A observed track_001 stop closing in.
- t = 12.10 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
