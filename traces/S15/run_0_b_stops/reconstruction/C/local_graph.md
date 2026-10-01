# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 125.58041938394308 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 17 (PRECEDES 11, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED_LEFT | C | track_001 | radar |  |
| C:e03 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e04 | 0.05 | TRACK_APPEARED_FRONT | C | track_002 | radar |  |
| C:e05 | 0.05 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 2.90 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e07 | 4.50 | CLOSING_END | C | track_002 | radar |  |
| C:e08 | 4.55 | TRACK_LOST | C | track_002 | radar |  |
| C:e09 | 4.75 | TRACK_LOST | C | track_001 | radar |  |

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
    C:e05 --PRECEDES--> C:e06
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e02 --SAME_TRACK--> C:e03
    C:e04 --SAME_TRACK--> C:e05
    C:e04 --SAME_TRACK--> C:e06
    C:e04 --SAME_TRACK--> C:e07
    C:e04 --SAME_TRACK--> C:e08
    C:e02 --SAME_TRACK--> C:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 TRACK_APPEARED_LEFT track_001<br>C:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 0.05 | C:e04 TRACK_APPEARED_FRONT track_002<br>C:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING | 0.00 |
| 2.90 | C:e06 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 2.80 |
| 4.50 | C:e07 CLOSING_END track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 4.40 |
| 4.55 | C:e08 TRACK_LOST track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CRITICAL_TTC | 4.50 |
| 4.75 | C:e09 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 | 4.70 |

## States still active when observation ended

- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_001, since C:e03 (t = 0.00 s); the track was lost at 4.75 s
- CRITICAL_TTC of track_002, since C:e06 (t = 2.90 s); the track was lost at 4.55 s

## Tracks lost

- track_002 at 4.55 s (C:e08): CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 4.75 s (C:e09): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 2.90

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 4.75 | 86 | 45.2 m / -57 deg | 9.41 m (4.75) | 9.4 m / -82 deg | 9.7 m/s |
| track_002 | 0.05 | 4.55 | 83 | 69.9 m / -3 deg | 2.39 m (4.50) | 2.5 m / -115 deg | 10.8 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.05 s: C's radar started tracking track_002, which appeared in front of it.
- t = 0.05 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.90 s: C's time-to-contact with track_002 became critical.
- t = 4.50 s: C observed track_002 stop closing in.
- t = 4.55 s: C's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 4.75 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
