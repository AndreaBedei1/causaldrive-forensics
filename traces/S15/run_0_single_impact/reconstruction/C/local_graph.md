# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 220.40668706968427 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 11; edges: 19 (PRECEDES 14, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.40 | TRACK_APPEARED_LEFT | C | track_001 | radar |  |
| C:e03 | 0.40 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e04 | 1.25 | TRACK_APPEARED_FRONT | C | track_002 | radar |  |
| C:e05 | 1.25 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 2.25 | TRACK_LOST | C | track_001 | radar |  |
| C:e07 | 2.80 | STOP_SIGN_DETECTED_START | C | sign-0 | camera | relevant_to_ego_path=False |
| C:e08 | 2.80 | STOP_SIGN_DETECTED_END | C | sign-0 | camera |  |
| C:e09 | 3.15 | TRACK_APPEARED_LEFT | C | track_003 | radar |  |
| C:e10 | 3.90 | CLOSING_START | C | track_003 | radar |  |
| C:e11 | 5.20 | EGO_PATH_ENTRY | C | track_002 | radar |  |

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
    C:e10 --PRECEDES--> C:e11
    C:e02 --SAME_TRACK--> C:e03
    C:e04 --SAME_TRACK--> C:e05
    C:e02 --SAME_TRACK--> C:e06
    C:e09 --SAME_TRACK--> C:e10
    C:e04 --SAME_TRACK--> C:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START | ego: not yet observed | - |
| 0.40 | C:e02 TRACK_APPEARED_LEFT track_001<br>C:e03 CLOSING_START track_001 | ego: MOVING | 0.30 |
| 1.25 | C:e04 TRACK_APPEARED_FRONT track_002<br>C:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING | 1.20 |
| 2.25 | C:e06 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 2.20 |
| 2.80 | C:e07 STOP_SIGN_DETECTED_START sign-0<br>C:e08 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 | 2.70 |
| 3.15 | C:e09 TRACK_APPEARED_LEFT track_003 | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.10 |
| 3.90 | C:e10 CLOSING_START track_003 | ego: MOVING<br>track_002: CLOSING<br>track_003: no active state<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.80 |
| 5.20 | C:e11 EGO_PATH_ENTRY track_002 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 5.10 |

## States still active when observation ended

- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_001, since C:e03 (t = 0.40 s); the track was lost at 2.25 s
- CLOSING of track_002, since C:e05 (t = 1.25 s)
- CLOSING of track_003, since C:e10 (t = 3.90 s)
- EGO_PATH of track_002, since C:e11 (t = 5.20 s)

## Tracks lost

- track_001 at 2.25 s (C:e06): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: EGO_PATH_ENTRY 5.20, no critical TTC

## Sign detection windows

- STOP sign sign-0: detected 2.80 s -> 2.80 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.40 | 2.25 | 14 | 65.0 m / -31 deg | 55.67 m (2.25) | 55.7 m / -20 deg | 7.8 m/s |
| track_002 | 1.25 | 13.95 | 215 | 87.0 m / -2 deg | 20.05 m (13.95) | 20.1 m / +2 deg | 10.7 m/s |
| track_003 | 3.15 | 13.95 | 147 | 53.6 m / -9 deg | 35.55 m (13.95) | 35.5 m / -11 deg | 4.9 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.40 s: C's radar started tracking track_001, which appeared on its left.
- t = 0.40 s: C observed track_001 start closing in (already the case when first observed).
- t = 1.25 s: C's radar started tracking track_002, which appeared in front of it.
- t = 1.25 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.25 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 2.80 s: C's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 2.80 s: C's camera stopped detecting STOP sign sign-0.
- t = 3.15 s: C's radar started tracking track_003, which appeared on its left.
- t = 3.90 s: C observed track_003 start closing in.
- t = 5.20 s: C observed track_002 enter its forward path corridor.
