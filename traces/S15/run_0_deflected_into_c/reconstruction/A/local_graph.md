# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 493.54037738218904 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 29; edges: 53 (PRECEDES 42, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.00 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e05 | 2.00 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.00 | CRITICAL_TTC_START | A | track_002 | radar | active_at_first_observation=True |
| A:e07 | 2.50 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 2.65 | PREDICTED_PATH_CONFLICT_START | A | track_002 | radar |  |
| A:e09 | 3.75 | TRACK_LOST | A | track_002 | radar |  |
| A:e10 | 3.80 | COLLISION | A | - | collision_sensor | peak_impulse=9797.50 |
| A:e11 | 3.80 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e12 | 3.85 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e13 | 4.50 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e14 | 4.55 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e15 | 4.55 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e16 | 4.60 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e17 | 4.75 | COLLISION | A | - | collision_sensor | peak_impulse=1637.56 |
| A:e18 | 4.95 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e19 | 4.95 | CLOSING_END | A | track_001 | radar |  |
| A:e20 | 5.05 | MOVING_END | A | - | ego |  |
| A:e21 | 5.05 | STOP_START | A | - | ego |  |
| A:e22 | 5.30 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e23 | 5.30 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False |
| A:e24 | 7.80 | STOP_SIGN_DETECTED_END | A | sign-2 | camera |  |
| A:e25 | 8.70 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |
| A:e26 | 8.70 | STOP_SIGN_DETECTED_END | A | sign-2 | camera | sign_track=sign-3 |
| A:e27 | 9.75 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| A:e28 | 9.90 | STOP_SIGN_DETECTED_END | A | sign-2 | camera | sign_track=sign-4 |
| A:e29 | 10.90 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-5 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e04
    A:e01 --PRECEDES--> A:e05
    A:e01 --PRECEDES--> A:e06
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
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e28 --PRECEDES--> A:e29
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e16
    A:e02 --SAME_TRACK--> A:e18
    A:e02 --SAME_TRACK--> A:e19
    A:e02 --SAME_TRACK--> A:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 2.00 | A:e04 TRACK_APPEARED track_002<br>A:e05 CLOSING_START track_002<br>A:e06 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 1.90 |
| 2.50 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 2.40 |
| 2.65 | A:e08 PREDICTED_PATH_CONFLICT_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC | 2.60 |
| 3.75 | A:e09 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT | 3.70 |
| 3.80 | A:e10 COLLISION<br>A:e11 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 3.70 |
| 3.85 | A:e12 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 3.80 |
| 4.50 | A:e13 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 | 4.40 |
| 4.55 | A:e14 STOP_SIGN_DETECTED_START sign-0<br>A:e15 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 4.50 |
| 4.60 | A:e16 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known | 4.50 |
| 4.75 | A:e17 COLLISION | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known | 4.70 |
| 4.95 | A:e18 CRITICAL_TTC_END track_001<br>A:e19 CLOSING_END track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known | 4.90 |
| 5.05 | A:e20 MOVING_END<br>A:e21 STOP_START | ego: MOVING<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known | 5.00 |
| 5.30 | A:e22 PREDICTED_PATH_CONFLICT_END track_001<br>A:e23 STOP_SIGN_DETECTED_START sign-2 | ego: STOP<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known | 5.20 |
| 7.80 | A:e24 STOP_SIGN_DETECTED_END sign-2 | ego: STOP<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known<br>sign-2: STOP sign VISIBLE, known | 7.70 |
| 8.70 | A:e25 STOP_SIGN_DETECTED_START sign-2<br>A:e26 STOP_SIGN_DETECTED_END sign-2 | ego: STOP<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known<br>sign-2: STOP sign not visible, known | 8.60 |
| 9.75 | A:e27 STOP_SIGN_DETECTED_START sign-2 | ego: STOP<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known<br>sign-2: STOP sign not visible, known | 9.70 |
| 9.90 | A:e28 STOP_SIGN_DETECTED_END sign-2 | ego: STOP<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known<br>sign-2: STOP sign VISIBLE, known | 9.80 |
| 10.90 | A:e29 STOP_SIGN_DETECTED_START sign-2 | ego: STOP<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002<br>sign-0: STOP sign not visible, known<br>sign-2: STOP sign not visible, known | 10.80 |

## States still active when observation ended

- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- PREDICTED_PATH_CONFLICT of track_002, since A:e08 (t = 2.65 s); the track was lost at 3.75 s
- EGO_PATH of track_001, since A:e16 (t = 4.60 s)
- STOP, since A:e21 (t = 5.05 s)
- STOP_SIGN_DETECTED of sign-2, since A:e29 (t = 10.90 s)

## Tracks lost

- track_002 at 3.75 s (A:e09): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 4.55 s -> 4.55 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-2: detected 5.30 s -> 7.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 8.70 s -> 8.70 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 9.75 s -> 9.90 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 10.90 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 13.95 | 277 | 70.9 m / -3 deg | 0.96 m (5.25) | 1.4 m / -41 deg | 5.8 m/s |
| track_002 | 2.00 | 3.75 | 36 | 28.2 m / +36 deg | 1.67 m (3.75) | 1.7 m / +70 deg | 9.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.00 s: A's radar started tracking track_002.
- t = 2.00 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.00 s: A's time-to-contact with track_002 became critical (already the case when first observed).
- t = 2.50 s: A's time-to-contact with track_001 became critical.
- t = 2.65 s: A predicted a path conflict with track_002 (close approach ahead if both keep their motion).
- t = 3.75 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: A's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: A started applying strong throttle.
- t = 3.85 s: A stopped applying strong throttle.
- t = 4.50 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 4.55 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 4.55 s: A's camera stopped detecting STOP sign sign-0.
- t = 4.60 s: A observed track_001 enter its forward path corridor.
- t = 4.75 s: A's collision sensor recorded a contact (peak impulse 1638 N*s).
- t = 4.95 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.95 s: A observed track_001 stop closing in.
- t = 5.05 s: A stopped moving.
- t = 5.05 s: A came to a stop.
- t = 5.30 s: A stopped predicting a path conflict with track_001.
- t = 5.30 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path).
- t = 7.80 s: A's camera stopped detecting STOP sign sign-2.
- t = 8.70 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- t = 8.70 s: A's camera stopped detecting STOP sign sign-2.
- t = 9.75 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- t = 9.90 s: A's camera stopped detecting STOP sign sign-2.
- t = 10.90 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-5).
