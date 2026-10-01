# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 162.19994998723269 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 36 (PRECEDES 27, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.90 | TRACK_APPEARED_FRONT | A | track_001 | radar |  |
| A:e03 | 0.90 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 2.00 | TRACK_APPEARED_RIGHT | A | track_002 | radar |  |
| A:e05 | 2.00 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.00 | CRITICAL_TTC_START | A | track_002 | radar | active_at_first_observation=True |
| A:e07 | 3.75 | TRACK_LOST | A | track_002 | radar |  |
| A:e08 | 3.80 | COLLISION | A | - | collision_sensor | peak_impulse=9797.50 |
| A:e09 | 3.80 | TURN_LEFT_START | A | - | ego |  |
| A:e10 | 3.80 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e11 | 3.85 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e12 | 4.10 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e13 | 4.30 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e14 | 4.60 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e15 | 5.10 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e16 | 5.20 | TURN_LEFT_END | A | - | ego |  |
| A:e17 | 10.60 | STOP_SIGN_DETECTED_START | A | sign-1 | camera | relevant_to_ego_path=False |
| A:e18 | 11.55 | MOVING_END | A | - | ego |  |
| A:e19 | 11.55 | STOP_START | A | - | ego |  |
| A:e20 | 13.45 | CRITICAL_TTC_START | A | track_001 | radar |  |

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
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e20
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e12
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e20
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.90 | A:e02 TRACK_APPEARED_FRONT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 0.80 |
| 2.00 | A:e04 TRACK_APPEARED_RIGHT track_002<br>A:e05 CLOSING_START track_002<br>A:e06 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING | 1.90 |
| 3.75 | A:e07 TRACK_LOST track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 3.70 |
| 3.80 | A:e08 COLLISION<br>A:e09 TURN_LEFT_START<br>A:e10 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 | 3.70 |
| 3.85 | A:e11 EGO_PATH_EXIT track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 3.80 |
| 4.10 | A:e12 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 | 4.00 |
| 4.30 | A:e13 EGO_PATH_EXIT track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 4.20 |
| 4.60 | A:e14 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 | 4.60 |
| 5.10 | A:e15 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 5.10 |
| 5.20 | A:e16 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 5.10 |
| 10.60 | A:e17 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known | 10.60 |
| 11.55 | A:e18 MOVING_END<br>A:e19 STOP_START | ego: MOVING<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 11.50 |
| 13.45 | A:e20 CRITICAL_TTC_START track_001 | ego: STOP<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 13.40 |

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 0.90 s)
- CLOSING of track_002, since A:e05 (t = 2.00 s); the track was lost at 3.75 s
- CRITICAL_TTC of track_002, since A:e06 (t = 2.00 s); the track was lost at 3.75 s
- STOP_SIGN_DETECTED of sign-1, since A:e17 (t = 10.60 s)
- STOP, since A:e19 (t = 11.55 s)
- CRITICAL_TTC of track_001, since A:e20 (t = 13.45 s)

## Tracks lost

- track_002 at 3.75 s (A:e07): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 13.45; EGO_PATH_ENTRY 3.80 before critical TTC (-9.65 s)
- track_002: CRITICAL_TTC_START 2.00, COLLISION 3.80 (+1.80 s)

## Sign detection windows

- STOP sign sign-0: detected 4.60 s -> 5.10 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 10.60 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: A:e19

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.90 | 13.95 | 216 | 89.2 m / -3 deg | 17.60 m (13.95) | 17.6 m / +13 deg | 2.2 m/s |
| track_002 | 2.00 | 3.75 | 36 | 28.2 m / +35 deg | 1.89 m (3.75) | 1.9 m / +78 deg | 9.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.90 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.90 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.00 s: A's radar started tracking track_002, which appeared on its right.
- t = 2.00 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.00 s: A's time-to-contact with track_002 became critical (already the case when first observed).
- t = 3.75 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: A's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: A started turning left.
- t = 3.80 s: A observed track_001 enter its forward path corridor.
- t = 3.85 s: A observed track_001 leave its forward path corridor.
- t = 4.10 s: A observed track_001 enter its forward path corridor.
- t = 4.30 s: A observed track_001 leave its forward path corridor.
- t = 4.60 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 5.10 s: A's camera stopped detecting STOP sign sign-0.
- t = 5.20 s: A stopped turning left.
- t = 10.60 s: A's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 11.55 s: A stopped moving.
- t = 11.55 s: A came to a stop.
- t = 13.45 s: A's time-to-contact with track_001 became critical.
