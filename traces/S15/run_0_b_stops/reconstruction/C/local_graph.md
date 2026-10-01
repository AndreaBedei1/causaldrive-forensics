# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 478.86066130176187 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 31 (PRECEDES 18, SAME_TRACK 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED | C | track_001 | radar |  |
| C:e03 | 0.00 | TRACK_APPEARED | C | track_002 | radar |  |
| C:e04 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e05 | 0.00 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 0.45 | PREDICTED_PATH_CONFLICT_START | C | track_002 | radar |  |
| C:e07 | 1.65 | PREDICTED_PATH_CONFLICT_END | C | track_002 | radar |  |
| C:e08 | 1.65 | STRONG_THROTTLE_START | C | - | controls |  |
| C:e09 | 2.10 | STRONG_THROTTLE_END | C | - | controls |  |
| C:e10 | 2.25 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e11 | 2.45 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e12 | 2.95 | CRITICAL_TTC_END | C | track_002 | radar |  |
| C:e13 | 3.00 | PREDICTED_PATH_CONFLICT_START | C | track_002 | radar |  |
| C:e14 | 3.35 | PREDICTED_PATH_CONFLICT_END | C | track_002 | radar |  |
| C:e15 | 4.00 | TRACK_LOST | C | track_002 | radar |  |
| C:e16 | 4.50 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e17 | 4.50 | CLOSING_END | C | track_001 | radar |  |
| C:e18 | 4.50 | TRACK_LOST | C | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e06
    C:e02 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e06
    C:e06 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e12 --PRECEDES--> C:e13
    C:e13 --PRECEDES--> C:e14
    C:e14 --PRECEDES--> C:e15
    C:e15 --PRECEDES--> C:e16
    C:e15 --PRECEDES--> C:e17
    C:e15 --PRECEDES--> C:e18
    C:e02 --SAME_TRACK--> C:e04
    C:e03 --SAME_TRACK--> C:e05
    C:e03 --SAME_TRACK--> C:e06
    C:e03 --SAME_TRACK--> C:e07
    C:e03 --SAME_TRACK--> C:e10
    C:e02 --SAME_TRACK--> C:e11
    C:e03 --SAME_TRACK--> C:e12
    C:e03 --SAME_TRACK--> C:e13
    C:e03 --SAME_TRACK--> C:e14
    C:e03 --SAME_TRACK--> C:e15
    C:e02 --SAME_TRACK--> C:e16
    C:e02 --SAME_TRACK--> C:e17
    C:e02 --SAME_TRACK--> C:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 TRACK_APPEARED track_001<br>C:e03 TRACK_APPEARED track_002<br>C:e04 CLOSING_START track_001<br>C:e05 CLOSING_START track_002 | ego: not yet observed | - |
| 0.45 | C:e06 PREDICTED_PATH_CONFLICT_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 0.40 |
| 1.65 | C:e07 PREDICTED_PATH_CONFLICT_END track_002<br>C:e08 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT | 1.60 |
| 2.10 | C:e09 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 2.00 |
| 2.25 | C:e10 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 2.20 |
| 2.45 | C:e11 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 2.40 |
| 2.95 | C:e12 CRITICAL_TTC_END track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 2.90 |
| 3.00 | C:e13 PREDICTED_PATH_CONFLICT_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING | 2.90 |
| 3.35 | C:e14 PREDICTED_PATH_CONFLICT_END track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT | 3.30 |
| 4.00 | C:e15 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING | 3.90 |
| 4.50 | C:e16 CRITICAL_TTC_END track_001<br>C:e17 CLOSING_END track_001<br>C:e18 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.40 |

## States still active when observation ended

- MOVING, since C:e01 (t = 0.00 s)
- CLOSING of track_002, since C:e05 (t = 0.00 s); the track was lost at 4.00 s

## Tracks lost

- track_002 at 4.00 s (C:e15): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 4.50 s (C:e18): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 4.50 | 90 | 70.7 m / -2 deg | 2.09 m (4.50) | 2.1 m / -98 deg | 10.7 m/s |
| track_002 | 0.00 | 4.00 | 79 | 45.1 m / -57 deg | 10.26 m (4.00) | 10.3 m / -56 deg | 9.9 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001.
- t = 0.00 s: C's radar started tracking track_002.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: C observed track_002 start closing in (already the case when first observed).
- t = 0.45 s: C predicted a path conflict with track_002 (close approach ahead if both keep their motion).
- t = 1.65 s: C stopped predicting a path conflict with track_002.
- t = 1.65 s: C started applying strong throttle.
- t = 2.10 s: C stopped applying strong throttle.
- t = 2.25 s: C's time-to-contact with track_002 became critical.
- t = 2.45 s: C's time-to-contact with track_001 became critical.
- t = 2.95 s: C's time-to-contact with track_002 stopped being critical.
- t = 3.00 s: C predicted a path conflict with track_002 (close approach ahead if both keep their motion).
- t = 3.35 s: C stopped predicting a path conflict with track_002.
- t = 4.00 s: C's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 4.50 s: C's time-to-contact with track_001 stopped being critical.
- t = 4.50 s: C observed track_001 stop closing in.
- t = 4.50 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
