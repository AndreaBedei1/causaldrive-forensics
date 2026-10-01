# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 513.3408981114626 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 10; edges: 21 (PRECEDES 16, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.80 | TRACK_APPEARED_FRONT | C | track_001 | radar |  |
| C:e03 | 0.80 | TRACK_APPEARED_LEFT | C | track_002 | radar |  |
| C:e04 | 0.80 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e05 | 0.80 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 2.80 | STOP_SIGN_DETECTED_START | C | sign-0 | camera | relevant_to_ego_path=False |
| C:e07 | 2.80 | STOP_SIGN_DETECTED_END | C | sign-0 | camera |  |
| C:e08 | 2.95 | CLOSING_END | C | track_002 | radar |  |
| C:e09 | 3.85 | CLOSING_START | C | track_002 | radar |  |
| C:e10 | 5.00 | EGO_PATH_ENTRY | C | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e01 --PRECEDES--> C:e03
    C:e01 --PRECEDES--> C:e04
    C:e01 --PRECEDES--> C:e05
    C:e02 --PRECEDES--> C:e06
    C:e02 --PRECEDES--> C:e07
    C:e03 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e07
    C:e04 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e07
    C:e05 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e02 --SAME_TRACK--> C:e04
    C:e03 --SAME_TRACK--> C:e05
    C:e03 --SAME_TRACK--> C:e08
    C:e03 --SAME_TRACK--> C:e09
    C:e02 --SAME_TRACK--> C:e10
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START | ego: not yet observed | - |
| 0.80 | C:e02 TRACK_APPEARED_FRONT track_001<br>C:e03 TRACK_APPEARED_LEFT track_002<br>C:e04 CLOSING_START track_001<br>C:e05 CLOSING_START track_002 | ego: MOVING | 0.70 |
| 2.80 | C:e06 STOP_SIGN_DETECTED_START sign-0<br>C:e07 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 2.70 |
| 2.95 | C:e08 CLOSING_END track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known | 2.90 |
| 3.85 | C:e09 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: no active state<br>sign-0: STOP sign known | 3.80 |
| 5.00 | C:e10 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known | 4.90 |

## States still active when observation ended

- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_001, since C:e04 (t = 0.80 s)
- CLOSING of track_002, since C:e09 (t = 3.85 s)
- EGO_PATH of track_001, since C:e10 (t = 5.00 s)

## Tracks lost

- no track was lost

## Sign detection windows

- STOP sign sign-0: detected 2.80 s -> 2.80 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.80 | 13.95 | 257 | 90.2 m / -2 deg | 17.67 m (13.95) | 17.7 m / +3 deg | 10.7 m/s |
| track_002 | 0.80 | 13.95 | 236 | 60.7 m / -29 deg | 33.42 m (13.95) | 33.4 m / -11 deg | 10.2 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.80 s: C's radar started tracking track_001, which appeared in front of it.
- t = 0.80 s: C's radar started tracking track_002, which appeared on its left.
- t = 0.80 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.80 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.80 s: C's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 2.80 s: C's camera stopped detecting STOP sign sign-0.
- t = 2.95 s: C observed track_002 stop closing in.
- t = 3.85 s: C observed track_002 start closing in.
- t = 5.00 s: C observed track_001 enter its forward path corridor.
