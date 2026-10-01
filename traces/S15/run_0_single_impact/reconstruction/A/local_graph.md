# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 513.3408981114626 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 39 (PRECEDES 30, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.80 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.80 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.00 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e05 | 2.00 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.00 | CRITICAL_TTC_START | A | track_002 | radar | active_at_first_observation=True |
| A:e07 | 2.65 | PREDICTED_PATH_CONFLICT_START | A | track_002 | radar |  |
| A:e08 | 3.75 | TRACK_LOST | A | track_002 | radar |  |
| A:e09 | 3.80 | COLLISION | A | - | collision_sensor | peak_impulse=9797.50 |
| A:e10 | 3.80 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e11 | 3.80 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 3.85 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e13 | 3.85 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e14 | 4.10 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e15 | 4.30 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e16 | 4.60 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e17 | 4.60 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e18 | 10.55 | STOP_SIGN_DETECTED_START | A | sign-1 | camera | relevant_to_ego_path=False |
| A:e19 | 11.55 | MOVING_END | A | - | ego |  |
| A:e20 | 11.55 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

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
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e12
    A:e02 --SAME_TRACK--> A:e14
    A:e02 --SAME_TRACK--> A:e15
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.80 | A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 0.70 |
| 2.00 | A:e04 TRACK_APPEARED track_002<br>A:e05 CLOSING_START track_002<br>A:e06 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 1.90 |
| 2.65 | A:e07 PREDICTED_PATH_CONFLICT_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 2.60 |
| 3.75 | A:e08 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT | 3.70 |
| 3.80 | A:e09 COLLISION<br>A:e10 STRONG_THROTTLE_START<br>A:e11 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_002 | 3.70 |
| 3.85 | A:e12 EGO_PATH_EXIT track_001<br>A:e13 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>lost (states UNKNOWN): track_002 | 3.80 |
| 4.10 | A:e14 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_002 | 4.00 |
| 4.30 | A:e15 EGO_PATH_EXIT track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>lost (states UNKNOWN): track_002 | 4.20 |
| 4.60 | A:e16 STOP_SIGN_DETECTED_START sign-0<br>A:e17 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_002 | 4.50 |
| 10.55 | A:e18 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known | 10.50 |
| 11.55 | A:e19 MOVING_END<br>A:e20 STOP_START | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign VISIBLE, known | 11.50 |

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 0.80 s)
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- PREDICTED_PATH_CONFLICT of track_002, since A:e07 (t = 2.65 s); the track was lost at 3.75 s
- STOP_SIGN_DETECTED of sign-1, since A:e18 (t = 10.55 s)
- STOP, since A:e20 (t = 11.55 s)

## Tracks lost

- track_002 at 3.75 s (A:e08): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 4.60 s -> 4.60 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 10.55 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: A:e20

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.80 | 13.95 | 248 | 90.4 m / -2 deg | 17.46 m (13.95) | 17.5 m / +15 deg | 2.4 m/s |
| track_002 | 2.00 | 3.75 | 36 | 28.2 m / +36 deg | 1.67 m (3.75) | 1.7 m / +70 deg | 9.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.80 s: A's radar started tracking track_001.
- t = 0.80 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.00 s: A's radar started tracking track_002.
- t = 2.00 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.00 s: A's time-to-contact with track_002 became critical (already the case when first observed).
- t = 2.65 s: A predicted a path conflict with track_002 (close approach ahead if both keep their motion).
- t = 3.75 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: A's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: A started applying strong throttle.
- t = 3.80 s: A observed track_001 enter its forward path corridor.
- t = 3.85 s: A observed track_001 leave its forward path corridor.
- t = 3.85 s: A stopped applying strong throttle.
- t = 4.10 s: A observed track_001 enter its forward path corridor.
- t = 4.30 s: A observed track_001 leave its forward path corridor.
- t = 4.60 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 4.60 s: A's camera stopped detecting STOP sign sign-0.
- t = 10.55 s: A's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 11.55 s: A stopped moving.
- t = 11.55 s: A came to a stop.
