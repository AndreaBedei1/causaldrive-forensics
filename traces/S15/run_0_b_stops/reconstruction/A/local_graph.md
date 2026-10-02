# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 184.48766066133976 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 13; edges: 28 (PRECEDES 18, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.20 | TRACK_APPEARED_FRONT | A | track_001 | radar |  |
| A:e03 | 0.20 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.10 | TRACK_APPEARED_RIGHT | A | track_002 | radar |  |
| A:e05 | 2.10 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.10 | CRITICAL_TTC_START | A | track_002 | radar | active_at_first_observation=True |
| A:e07 | 2.50 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 4.20 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e09 | 4.25 | CLOSING_END | A | track_002 | radar |  |
| A:e10 | 4.65 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e11 | 4.65 | CLOSING_END | A | track_001 | radar |  |
| A:e12 | 9.55 | TRACK_LOST | A | track_001 | radar |  |
| A:e13 | 10.40 | TRACK_LOST | A | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e12
    A:e04 --SAME_TRACK--> A:e13
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.20 | A:e02 TRACK_APPEARED_FRONT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 0.10 |
| 2.10 | A:e04 TRACK_APPEARED_RIGHT track_002<br>A:e05 CLOSING_START track_002<br>A:e06 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING | 2.00 |
| 2.50 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 2.40 |
| 4.20 | A:e08 CRITICAL_TTC_END track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 4.10 |
| 4.25 | A:e09 CLOSING_END track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 4.20 |
| 4.65 | A:e10 CRITICAL_TTC_END track_001<br>A:e11 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state | 4.60 |
| 9.55 | A:e12 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>track_002: no active state | 9.50 |
| 10.40 | A:e13 TRACK_LOST track_002 | ego: MOVING<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 | 10.30 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)

## Tracks lost

- lost with no state active: track_001, track_002

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.50
- track_002: CRITICAL_TTC_START 2.10

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.20 | 9.55 | 136 | 70.0 m / -3 deg | 2.39 m (4.65) | 79.6 m / -177 deg | 5.9 m/s |
| track_002 | 2.10 | 10.40 | 134 | 28.5 m / +32 deg | 5.66 m (4.25) | 65.4 m / +174 deg | 8.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.20 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.20 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.10 s: A's radar started tracking track_002, which appeared on its right.
- t = 2.10 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.10 s: A's time-to-contact with track_002 became critical (already the case when first observed).
- t = 2.50 s: A's time-to-contact with track_001 became critical.
- t = 4.20 s: A's time-to-contact with track_002 stopped being critical.
- t = 4.25 s: A observed track_002 stop closing in.
- t = 4.65 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.65 s: A observed track_001 stop closing in.
- t = 9.55 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 10.40 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
