# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 115.46773005649447 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 15 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 42; edges: 149 (PRECEDES 125, SAME_TRACK 24)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 2.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.35 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e05 | 2.65 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e06 | 3.00 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 4.95 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e08 | 5.25 | TRACK_LOST | A | track_001 | radar |  |
| A:e09 | 8.20 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e10 | 8.45 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e11 | 9.35 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e12 | 9.35 | TRACK_APPEARED | A | track_003 | radar |  |
| A:e13 | 9.35 | TRACK_APPEARED | A | track_004 | radar |  |
| A:e14 | 9.35 | TRACK_APPEARED | A | track_005 | radar |  |
| A:e15 | 9.35 | TRACK_APPEARED | A | track_006 | radar |  |
| A:e16 | 9.35 | TRACK_APPEARED | A | track_010 | radar |  |
| A:e17 | 9.35 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e18 | 9.35 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e19 | 9.35 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e20 | 9.35 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e21 | 9.35 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e22 | 9.35 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e23 | 9.45 | TRACK_APPEARED | A | track_007 | radar |  |
| A:e24 | 9.45 | TRACK_APPEARED | A | track_011 | radar |  |
| A:e25 | 9.45 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e26 | 9.45 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e27 | 9.50 | TRACK_APPEARED | A | track_008 | radar |  |
| A:e28 | 9.50 | TRACK_APPEARED | A | track_009 | radar |  |
| A:e29 | 9.50 | TRACK_APPEARED | A | track_012 | radar |  |
| A:e30 | 9.50 | TRACK_APPEARED | A | track_014 | radar |  |
| A:e31 | 9.50 | TRACK_APPEARED | A | track_015 | radar |  |
| A:e32 | 9.50 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |
| A:e33 | 9.50 | CLOSING_START | A | track_012 | radar | active_at_first_observation=True |
| A:e34 | 9.50 | CLOSING_START | A | track_014 | radar | active_at_first_observation=True |
| A:e35 | 9.50 | CLOSING_START | A | track_015 | radar | active_at_first_observation=True |
| A:e36 | 9.70 | TRACK_APPEARED | A | track_013 | radar |  |
| A:e37 | 9.75 | TRACK_LOST | A | track_008 | radar |  |
| A:e38 | 9.85 | CLOSING_END | A | track_009 | radar |  |
| A:e39 | 9.85 | TRACK_LOST | A | track_011 | radar |  |
| A:e40 | 9.85 | TRACK_LOST | A | track_012 | radar |  |
| A:e41 | 9.90 | CRITICAL_TTC_START | A | track_006 | radar |  |
| A:e42 | 9.90 | TRACK_LOST | A | track_009 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e14
    A:e10 --PRECEDES--> A:e15
    A:e10 --PRECEDES--> A:e16
    A:e10 --PRECEDES--> A:e17
    A:e10 --PRECEDES--> A:e18
    A:e10 --PRECEDES--> A:e19
    A:e10 --PRECEDES--> A:e20
    A:e10 --PRECEDES--> A:e21
    A:e10 --PRECEDES--> A:e22
    A:e11 --PRECEDES--> A:e23
    A:e11 --PRECEDES--> A:e24
    A:e11 --PRECEDES--> A:e25
    A:e11 --PRECEDES--> A:e26
    A:e12 --PRECEDES--> A:e23
    A:e12 --PRECEDES--> A:e24
    A:e12 --PRECEDES--> A:e25
    A:e12 --PRECEDES--> A:e26
    A:e13 --PRECEDES--> A:e23
    A:e13 --PRECEDES--> A:e24
    A:e13 --PRECEDES--> A:e25
    A:e13 --PRECEDES--> A:e26
    A:e14 --PRECEDES--> A:e23
    A:e14 --PRECEDES--> A:e24
    A:e14 --PRECEDES--> A:e25
    A:e14 --PRECEDES--> A:e26
    A:e15 --PRECEDES--> A:e23
    A:e15 --PRECEDES--> A:e24
    A:e15 --PRECEDES--> A:e25
    A:e15 --PRECEDES--> A:e26
    A:e16 --PRECEDES--> A:e23
    A:e16 --PRECEDES--> A:e24
    A:e16 --PRECEDES--> A:e25
    A:e16 --PRECEDES--> A:e26
    A:e17 --PRECEDES--> A:e23
    A:e17 --PRECEDES--> A:e24
    A:e17 --PRECEDES--> A:e25
    A:e17 --PRECEDES--> A:e26
    A:e18 --PRECEDES--> A:e23
    A:e18 --PRECEDES--> A:e24
    A:e18 --PRECEDES--> A:e25
    A:e18 --PRECEDES--> A:e26
    A:e19 --PRECEDES--> A:e23
    A:e19 --PRECEDES--> A:e24
    A:e19 --PRECEDES--> A:e25
    A:e19 --PRECEDES--> A:e26
    A:e20 --PRECEDES--> A:e23
    A:e20 --PRECEDES--> A:e24
    A:e20 --PRECEDES--> A:e25
    A:e20 --PRECEDES--> A:e26
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e21 --PRECEDES--> A:e26
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e23 --PRECEDES--> A:e28
    A:e23 --PRECEDES--> A:e29
    A:e23 --PRECEDES--> A:e30
    A:e23 --PRECEDES--> A:e31
    A:e23 --PRECEDES--> A:e32
    A:e23 --PRECEDES--> A:e33
    A:e23 --PRECEDES--> A:e34
    A:e23 --PRECEDES--> A:e35
    A:e24 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e28
    A:e24 --PRECEDES--> A:e29
    A:e24 --PRECEDES--> A:e30
    A:e24 --PRECEDES--> A:e31
    A:e24 --PRECEDES--> A:e32
    A:e24 --PRECEDES--> A:e33
    A:e24 --PRECEDES--> A:e34
    A:e24 --PRECEDES--> A:e35
    A:e25 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e28
    A:e25 --PRECEDES--> A:e29
    A:e25 --PRECEDES--> A:e30
    A:e25 --PRECEDES--> A:e31
    A:e25 --PRECEDES--> A:e32
    A:e25 --PRECEDES--> A:e33
    A:e25 --PRECEDES--> A:e34
    A:e25 --PRECEDES--> A:e35
    A:e26 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e28
    A:e26 --PRECEDES--> A:e29
    A:e26 --PRECEDES--> A:e30
    A:e26 --PRECEDES--> A:e31
    A:e26 --PRECEDES--> A:e32
    A:e26 --PRECEDES--> A:e33
    A:e26 --PRECEDES--> A:e34
    A:e26 --PRECEDES--> A:e35
    A:e27 --PRECEDES--> A:e36
    A:e28 --PRECEDES--> A:e36
    A:e29 --PRECEDES--> A:e36
    A:e30 --PRECEDES--> A:e36
    A:e31 --PRECEDES--> A:e36
    A:e32 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e37 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e37 --PRECEDES--> A:e40
    A:e38 --PRECEDES--> A:e41
    A:e38 --PRECEDES--> A:e42
    A:e39 --PRECEDES--> A:e41
    A:e39 --PRECEDES--> A:e42
    A:e40 --PRECEDES--> A:e41
    A:e40 --PRECEDES--> A:e42
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e11 --SAME_TRACK--> A:e17
    A:e12 --SAME_TRACK--> A:e18
    A:e13 --SAME_TRACK--> A:e19
    A:e14 --SAME_TRACK--> A:e20
    A:e15 --SAME_TRACK--> A:e21
    A:e16 --SAME_TRACK--> A:e22
    A:e23 --SAME_TRACK--> A:e25
    A:e24 --SAME_TRACK--> A:e26
    A:e28 --SAME_TRACK--> A:e32
    A:e29 --SAME_TRACK--> A:e33
    A:e30 --SAME_TRACK--> A:e34
    A:e31 --SAME_TRACK--> A:e35
    A:e27 --SAME_TRACK--> A:e37
    A:e28 --SAME_TRACK--> A:e38
    A:e24 --SAME_TRACK--> A:e39
    A:e29 --SAME_TRACK--> A:e40
    A:e15 --SAME_TRACK--> A:e41
    A:e28 --SAME_TRACK--> A:e42
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 2.00 | A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 1.90 |
| 2.35 | A:e04 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 2.30 |
| 2.65 | A:e05 PREDICTED_PATH_CONFLICT_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT | 2.60 |
| 3.00 | A:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 2.90 |
| 4.95 | A:e07 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 4.90 |
| 5.25 | A:e08 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 5.20 |
| 8.20 | A:e09 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING<br>lost (states UNKNOWN): track_001 | 8.10 |
| 8.45 | A:e10 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign VISIBLE, known | 8.40 |
| 9.35 | A:e11 TRACK_APPEARED track_002<br>A:e12 TRACK_APPEARED track_003<br>A:e13 TRACK_APPEARED track_004<br>A:e14 TRACK_APPEARED track_005<br>A:e15 TRACK_APPEARED track_006<br>A:e16 TRACK_APPEARED track_010<br>A:e17 CLOSING_START track_002<br>A:e18 CLOSING_START track_003<br>A:e19 CLOSING_START track_004<br>A:e20 CLOSING_START track_005<br>A:e21 CLOSING_START track_006<br>A:e22 CLOSING_START track_010 | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 9.30 |
| 9.45 | A:e23 TRACK_APPEARED track_007<br>A:e24 TRACK_APPEARED track_011<br>A:e25 CLOSING_START track_007<br>A:e26 CLOSING_START track_011 | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 9.40 |
| 9.50 | A:e27 TRACK_APPEARED track_008<br>A:e28 TRACK_APPEARED track_009<br>A:e29 TRACK_APPEARED track_012<br>A:e30 TRACK_APPEARED track_014<br>A:e31 TRACK_APPEARED track_015<br>A:e32 CLOSING_START track_009<br>A:e33 CLOSING_START track_012<br>A:e34 CLOSING_START track_014<br>A:e35 CLOSING_START track_015 | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 9.40 |
| 9.70 | A:e36 TRACK_APPEARED track_013 | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 9.60 |
| 9.75 | A:e37 TRACK_LOST track_008 | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_008: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 9.70 |
| 9.85 | A:e38 CLOSING_END track_009<br>A:e39 TRACK_LOST track_011<br>A:e40 TRACK_LOST track_012 | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_009: VISIBLE, CLOSING<br>track_010: VISIBLE, CLOSING<br>track_011: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_008<br>sign-0: STOP sign not visible, known | 9.80 |
| 9.90 | A:e41 CRITICAL_TTC_START track_006<br>A:e42 TRACK_LOST track_009 | ego: MOVING<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>track_004: VISIBLE, CLOSING<br>track_005: VISIBLE, CLOSING<br>track_006: VISIBLE, CLOSING<br>track_007: VISIBLE, CLOSING<br>track_009: VISIBLE<br>track_010: VISIBLE, CLOSING<br>track_013: VISIBLE, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: VISIBLE, CLOSING<br>track_015: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_008, track_011, track_012<br>sign-0: STOP sign not visible, known | 9.80 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e03 (t = 2.00 s); the track was lost at 5.25 s
- CLOSING of track_002, since A:e17 (t = 9.35 s)
- CLOSING of track_003, since A:e18 (t = 9.35 s)
- CLOSING of track_004, since A:e19 (t = 9.35 s)
- CLOSING of track_005, since A:e20 (t = 9.35 s)
- CLOSING of track_006, since A:e21 (t = 9.35 s)
- CLOSING of track_010, since A:e22 (t = 9.35 s)
- CLOSING of track_007, since A:e25 (t = 9.45 s)
- CLOSING of track_011, since A:e26 (t = 9.45 s); the track was lost at 9.85 s
- CLOSING of track_012, since A:e33 (t = 9.50 s); the track was lost at 9.85 s
- CLOSING of track_014, since A:e34 (t = 9.50 s)
- CLOSING of track_015, since A:e35 (t = 9.50 s)
- CRITICAL_TTC of track_006, since A:e41 (t = 9.90 s)

## Tracks lost

- track_001 at 5.25 s (A:e08): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_011 at 9.85 s (A:e39): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_012 at 9.85 s (A:e40): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_008, track_009

## Sign detection windows

- STOP sign sign-0: detected 8.20 s -> 8.45 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.00 | 5.25 | 65 | 37.8 m / +33 deg | 7.12 m (5.25) | 7.1 m / +85 deg | 8.9 m/s |
| track_002 | 9.35 | 9.95 | 12 | 29.5 m / -77 deg | 25.74 m (9.95) | 25.7 m / -65 deg | 2.7 m/s |
| track_003 | 9.35 | 9.95 | 11 | 33.7 m / -78 deg | 29.90 m (9.95) | 29.9 m / -62 deg | 1.4 m/s |
| track_004 | 9.35 | 9.95 | 12 | 24.6 m / -79 deg | 21.06 m (9.95) | 21.1 m / -68 deg | 1.5 m/s |
| track_005 | 9.35 | 9.95 | 12 | 42.2 m / -77 deg | 38.21 m (9.95) | 38.2 m / -57 deg | 2.3 m/s |
| track_006 | 9.35 | 9.95 | 11 | 13.8 m / -70 deg | 9.90 m (9.95) | 9.9 m / -69 deg | 1.2 m/s |
| track_007 | 9.45 | 9.95 | 11 | 19.6 m / -79 deg | 16.81 m (9.95) | 16.8 m / -74 deg | 2.2 m/s |
| track_008 | 9.50 | 9.75 | 6 | 25.2 m / +69 deg | 25.23 m (9.55) | 25.4 m / +79 deg | 11.7 m/s |
| track_009 | 9.50 | 9.90 | 9 | 20.5 m / +59 deg | 20.24 m (9.70) | 20.4 m / +80 deg | 6.3 m/s |
| track_010 | 9.35 | 9.95 | 7 | 37.1 m / -77 deg | 33.21 m (9.95) | 33.2 m / -60 deg | 1.2 m/s |
| track_011 | 9.45 | 9.85 | 5 | 46.0 m / -74 deg | 43.28 m (9.85) | 43.3 m / -61 deg | 1.2 m/s |
| track_012 | 9.50 | 9.85 | 5 | 50.7 m / -71 deg | 48.19 m (9.85) | 48.2 m / -56 deg | 9.7 m/s |
| track_013 | 9.70 | 9.95 | 6 | 17.3 m / +54 deg | 17.02 m (9.90) | 17.1 m / +76 deg | 3.4 m/s |
| track_014 | 9.50 | 9.95 | 5 | 127.3 m / -64 deg | 123.66 m (9.95) | 123.7 m / -47 deg | 8.0 m/s |
| track_015 | 9.50 | 9.95 | 5 | 52.1 m / -69 deg | 48.78 m (9.95) | 48.8 m / -53 deg | 1.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.00 s: A's radar started tracking track_001.
- t = 2.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.35 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 2.65 s: A stopped predicting a path conflict with track_001.
- t = 3.00 s: A's time-to-contact with track_001 became critical.
- t = 4.95 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.25 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.20 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 8.45 s: A's camera stopped detecting STOP sign sign-0.
- t = 9.35 s: A's radar started tracking track_002.
- t = 9.35 s: A's radar started tracking track_003.
- t = 9.35 s: A's radar started tracking track_004.
- t = 9.35 s: A's radar started tracking track_005.
- t = 9.35 s: A's radar started tracking track_006.
- t = 9.35 s: A's radar started tracking track_010.
- t = 9.35 s: A observed track_002 start closing in (already the case when first observed).
- t = 9.35 s: A observed track_003 start closing in (already the case when first observed).
- t = 9.35 s: A observed track_004 start closing in (already the case when first observed).
- t = 9.35 s: A observed track_005 start closing in (already the case when first observed).
- t = 9.35 s: A observed track_006 start closing in (already the case when first observed).
- t = 9.35 s: A observed track_010 start closing in (already the case when first observed).
- t = 9.45 s: A's radar started tracking track_007.
- t = 9.45 s: A's radar started tracking track_011.
- t = 9.45 s: A observed track_007 start closing in (already the case when first observed).
- t = 9.45 s: A observed track_011 start closing in (already the case when first observed).
- t = 9.50 s: A's radar started tracking track_008.
- t = 9.50 s: A's radar started tracking track_009.
- t = 9.50 s: A's radar started tracking track_012.
- t = 9.50 s: A's radar started tracking track_014.
- t = 9.50 s: A's radar started tracking track_015.
- t = 9.50 s: A observed track_009 start closing in (already the case when first observed).
- t = 9.50 s: A observed track_012 start closing in (already the case when first observed).
- t = 9.50 s: A observed track_014 start closing in (already the case when first observed).
- t = 9.50 s: A observed track_015 start closing in (already the case when first observed).
- t = 9.70 s: A's radar started tracking track_013.
- t = 9.75 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 9.85 s: A observed track_009 stop closing in.
- t = 9.85 s: A's radar lost track_011 (its states are UNKNOWN from then on, not ended).
- t = 9.85 s: A's radar lost track_012 (its states are UNKNOWN from then on, not ended).
- t = 9.90 s: A's time-to-contact with track_006 became critical.
- t = 9.90 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
