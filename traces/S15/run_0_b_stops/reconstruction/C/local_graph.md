# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 184.48766066133976 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 20 (PRECEDES 13, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.05 | TRACK_APPEARED_FRONT | C | track_001 | radar |  |
| C:e03 | 0.05 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e04 | 0.35 | TRACK_APPEARED_LEFT | C | track_002 | radar |  |
| C:e05 | 0.35 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 2.85 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e07 | 4.70 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e08 | 4.70 | CLOSING_END | C | track_001 | radar |  |
| C:e09 | 5.20 | CLOSING_END | C | track_002 | radar |  |
| C:e10 | 10.20 | TRACK_LOST | C | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e01 --PRECEDES--> C:e03
    C:e02 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e06
    C:e06 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e02 --SAME_TRACK--> C:e03
    C:e04 --SAME_TRACK--> C:e05
    C:e02 --SAME_TRACK--> C:e06
    C:e02 --SAME_TRACK--> C:e07
    C:e02 --SAME_TRACK--> C:e08
    C:e04 --SAME_TRACK--> C:e09
    C:e02 --SAME_TRACK--> C:e10
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START | ego: not yet observed | - |
| 0.05 | C:e02 TRACK_APPEARED_FRONT track_001<br>C:e03 CLOSING_START track_001 | ego: MOVING | 0.00 |
| 0.35 | C:e04 TRACK_APPEARED_LEFT track_002<br>C:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING | 0.30 |
| 2.85 | C:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 2.80 |
| 4.70 | C:e07 CRITICAL_TTC_END track_001<br>C:e08 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 4.60 |
| 5.20 | C:e09 CLOSING_END track_002 | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING | 5.10 |
| 10.20 | C:e10 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>track_002: no active state | 10.10 |

## States still active when observation ended

- MOVING, since C:e01 (t = 0.00 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.85

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.05 | 10.20 | 147 | 72.6 m / -3 deg | 2.18 m (4.65) | 90.0 m / -178 deg | 10.9 m/s |
| track_002 | 0.35 | 10.55 | 189 | 42.7 m / -52 deg | 9.13 m (5.35) | 31.2 m / -162 deg | 9.8 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.05 s: C's radar started tracking track_001, which appeared in front of it.
- t = 0.05 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.35 s: C's radar started tracking track_002, which appeared on its left.
- t = 0.35 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.85 s: C's time-to-contact with track_001 became critical.
- t = 4.70 s: C's time-to-contact with track_001 stopped being critical.
- t = 4.70 s: C observed track_001 stop closing in.
- t = 5.20 s: C observed track_002 stop closing in.
- t = 10.20 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
