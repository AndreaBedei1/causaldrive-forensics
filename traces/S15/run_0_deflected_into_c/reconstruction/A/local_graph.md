# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 142.30000706017017 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 26; edges: 43 (PRECEDES 35, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.05 | TRACK_APPEARED_FRONT | A | track_001 | radar |  |
| A:e03 | 0.05 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.00 | TRACK_APPEARED_RIGHT | A | track_002 | radar |  |
| A:e05 | 2.00 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.00 | CRITICAL_TTC_START | A | track_002 | radar | active_at_first_observation=True |
| A:e07 | 2.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 3.75 | TRACK_LOST | A | track_002 | radar |  |
| A:e09 | 3.80 | COLLISION | A | - | collision_sensor | peak_impulse=9797.50 |
| A:e10 | 3.80 | TURN_LEFT_START | A | - | ego |  |
| A:e11 | 4.50 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 4.60 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e13 | 4.60 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e14 | 4.75 | COLLISION | A | - | collision_sensor | peak_impulse=1637.56 |
| A:e15 | 4.80 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e16 | 4.80 | CLOSING_END | A | track_001 | radar |  |
| A:e17 | 4.95 | TURN_LEFT_END | A | - | ego |  |
| A:e18 | 5.05 | MOVING_END | A | - | ego |  |
| A:e19 | 5.05 | STOP_START | A | - | ego |  |
| A:e20 | 5.30 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False |
| A:e21 | 7.80 | STOP_SIGN_DETECTED_END | A | sign-2 | camera |  |
| A:e22 | 8.70 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |
| A:e23 | 8.70 | STOP_SIGN_DETECTED_END | A | sign-2 | camera | sign_track=sign-3 |
| A:e24 | 9.60 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| A:e25 | 9.90 | STOP_SIGN_DETECTED_END | A | sign-2 | camera | sign_track=sign-4 |
| A:e26 | 10.90 | STOP_SIGN_DETECTED_START | A | sign-2 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-5 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

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
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e15
    A:e02 --SAME_TRACK--> A:e16
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.05 | A:e02 TRACK_APPEARED_FRONT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 0.00 |
| 2.00 | A:e04 TRACK_APPEARED_RIGHT track_002<br>A:e05 CLOSING_START track_002<br>A:e06 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING | 1.90 |
| 2.55 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 2.50 |
| 3.75 | A:e08 TRACK_LOST track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 3.70 |
| 3.80 | A:e09 COLLISION<br>A:e10 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 | 3.70 |
| 4.50 | A:e11 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 | 4.40 |
| 4.60 | A:e12 STOP_SIGN_DETECTED_START sign-0<br>A:e13 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 4.50 |
| 4.75 | A:e14 COLLISION | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 4.70 |
| 4.80 | A:e15 CRITICAL_TTC_END track_001<br>A:e16 CLOSING_END track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 4.70 |
| 4.95 | A:e17 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 4.90 |
| 5.05 | A:e18 MOVING_END<br>A:e19 STOP_START | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 5.00 |
| 5.30 | A:e20 STOP_SIGN_DETECTED_START sign-2 | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 5.20 |
| 7.80 | A:e21 STOP_SIGN_DETECTED_END sign-2 | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known | 7.70 |
| 8.70 | A:e22 STOP_SIGN_DETECTED_START sign-2<br>A:e23 STOP_SIGN_DETECTED_END sign-2 | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known | 8.60 |
| 9.60 | A:e24 STOP_SIGN_DETECTED_START sign-2 | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known | 9.50 |
| 9.90 | A:e25 STOP_SIGN_DETECTED_END sign-2 | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known | 9.80 |
| 10.90 | A:e26 STOP_SIGN_DETECTED_START sign-2 | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known | 10.80 |

## States still active when observation ended

- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- EGO_PATH of track_001, since A:e11 (t = 4.50 s)
- STOP, since A:e19 (t = 5.05 s)
- STOP_SIGN_DETECTED of sign-2, since A:e26 (t = 10.90 s)

## Tracks lost

- track_002 at 3.75 s (A:e08): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.55, COLLISION 3.80 (+1.25 s); EGO_PATH_ENTRY 4.50 after critical TTC (+1.95 s)
- track_002: CRITICAL_TTC_START 2.00, COLLISION 3.80 (+1.80 s)

## Sign detection windows

- STOP sign sign-0: detected 4.60 s -> 4.60 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-2: detected 5.30 s -> 7.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 8.70 s -> 8.70 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 9.60 s -> 9.90 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-2: detected 10.90 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.05 | 13.95 | 268 | 70.1 m / -3 deg | 0.98 m (5.50) | 1.1 m / -65 deg | 5.8 m/s |
| track_002 | 2.00 | 3.75 | 36 | 28.2 m / +35 deg | 1.89 m (3.75) | 1.9 m / +78 deg | 9.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.05 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.00 s: A's radar started tracking track_002, which appeared on its right.
- t = 2.00 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.00 s: A's time-to-contact with track_002 became critical (already the case when first observed).
- t = 2.55 s: A's time-to-contact with track_001 became critical.
- t = 3.75 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: A's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: A started turning left.
- t = 4.50 s: A observed track_001 enter its forward path corridor.
- t = 4.60 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 4.60 s: A's camera stopped detecting STOP sign sign-0.
- t = 4.75 s: A's collision sensor recorded a contact (peak impulse 1638 N*s).
- t = 4.80 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.80 s: A observed track_001 stop closing in.
- t = 4.95 s: A stopped turning left.
- t = 5.05 s: A stopped moving.
- t = 5.05 s: A came to a stop.
- t = 5.30 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path).
- t = 7.80 s: A's camera stopped detecting STOP sign sign-2.
- t = 8.70 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- t = 8.70 s: A's camera stopped detecting STOP sign sign-2.
- t = 9.60 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- t = 9.90 s: A's camera stopped detecting STOP sign sign-2.
- t = 10.90 s: A's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-5).
