# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 103.39315643906593 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 11; edges: 17 (PRECEDES 11, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.10 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 2.10 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 3.00 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 3.45 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e06 | 3.75 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e07 | 4.95 | TRACK_LOST | A | track_001 | radar |  |
| A:e08 | 8.15 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e09 | 8.45 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e10 | 9.70 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e11 | 9.70 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |

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
    A:e09 --PRECEDES--> A:e11
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e10 --SAME_TRACK--> A:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 2.10 | A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 2.00 |
| 3.00 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 2.90 |
| 3.45 | A:e05 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 3.40 |
| 3.75 | A:e06 PREDICTED_PATH_CONFLICT_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT | 3.70 |
| 4.95 | A:e07 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 4.90 |
| 8.15 | A:e08 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING<br>lost (states UNKNOWN): track_001 | 8.10 |
| 8.45 | A:e09 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign VISIBLE, known | 8.40 |
| 9.70 | A:e10 TRACK_APPEARED track_002<br>A:e11 CLOSING_START track_002 | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 9.60 |

## States still active when observation ended

- MOVING, since A:e01 (t = 0.00 s)
- CLOSING of track_001, since A:e03 (t = 2.10 s); the track was lost at 4.95 s
- CRITICAL_TTC of track_001, since A:e04 (t = 3.00 s); the track was lost at 4.95 s
- CLOSING of track_002, since A:e11 (t = 9.70 s)

## Tracks lost

- track_001 at 4.95 s (A:e07): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 8.15 s -> 8.45 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.10 | 4.95 | 58 | 36.3 m / +35 deg | 7.56 m (4.95) | 7.6 m / +62 deg | 9.2 m/s |
| track_002 | 9.70 | 9.95 | 5 | 16.4 m / +52 deg | 15.75 m (9.95) | 15.8 m / +60 deg | 13.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.10 s: A's radar started tracking track_001.
- t = 2.10 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.00 s: A's time-to-contact with track_001 became critical.
- t = 3.45 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 3.75 s: A stopped predicting a path conflict with track_001.
- t = 4.95 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.15 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 8.45 s: A's camera stopped detecting STOP sign sign-0.
- t = 9.70 s: A's radar started tracking track_002.
- t = 9.70 s: A observed track_002 start closing in (already the case when first observed).
