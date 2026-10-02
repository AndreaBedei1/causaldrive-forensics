# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 239.17912420257926 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 17 (PRECEDES 13, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED_REAR | C | track_001 | radar |  |
| C:e03 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e04 | 0.15 | TRACK_APPEARED_REAR | C | track_002 | radar |  |
| C:e05 | 0.15 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 0.30 | MOVING_END | C | - | ego |  |
| C:e07 | 0.30 | STOP_START | C | - | ego |  |
| C:e08 | 5.15 | TRACK_LOST | C | track_001 | radar |  |
| C:e09 | 5.60 | CLOSING_END | C | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e04
    C:e01 --PRECEDES--> C:e05
    C:e02 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e07
    C:e05 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e02 --SAME_TRACK--> C:e03
    C:e04 --SAME_TRACK--> C:e05
    C:e02 --SAME_TRACK--> C:e08
    C:e04 --SAME_TRACK--> C:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 TRACK_APPEARED_REAR track_001<br>C:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 0.15 | C:e04 TRACK_APPEARED_REAR track_002<br>C:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING | 0.10 |
| 0.30 | C:e06 MOVING_END<br>C:e07 STOP_START | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 0.20 |
| 5.15 | C:e08 TRACK_LOST track_001 | ego: STOP<br>track_001: CLOSING<br>track_002: CLOSING | 5.10 |
| 5.60 | C:e09 CLOSING_END track_002 | ego: STOP<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 | 5.50 |

## States still active when observation ended

- CLOSING of track_001, since C:e03 (t = 0.00 s); the track was lost at 5.15 s
- STOP, since C:e07 (t = 0.30 s)

## Tracks lost

- track_001 at 5.15 s (C:e08): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 5.15 | 60 | 62.2 m / +177 deg | 7.00 m (5.15) | 7.0 m / +151 deg | 13.1 m/s |
| track_002 | 0.15 | 9.95 | 155 | 67.9 m / +177 deg | 9.20 m (5.60) | 12.8 m / +163 deg | 13.3 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001, which appeared behind it.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.15 s: C's radar started tracking track_002, which appeared behind it.
- t = 0.15 s: C observed track_002 start closing in (already the case when first observed).
- t = 0.30 s: C stopped moving.
- t = 0.30 s: C came to a stop.
- t = 5.15 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 5.60 s: C observed track_002 stop closing in.
