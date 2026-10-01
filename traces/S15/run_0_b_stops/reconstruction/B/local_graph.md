# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 125.58041938394308 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 24; edges: 39 (PRECEDES 28, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.45 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e03 | 1.45 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 1.80 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e05 | 1.95 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e06 | 1.95 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e07 | 2.10 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e08 | 2.10 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e09 | 2.25 | TURN_LEFT_START | B | - | ego |  |
| B:e10 | 2.55 | BRAKE_START | B | - | controls |  |
| B:e11 | 3.35 | TURN_LEFT_END | B | - | ego |  |
| B:e12 | 3.40 | MOVING_END | B | - | ego |  |
| B:e13 | 3.40 | STOP_START | B | - | ego |  |
| B:e14 | 3.55 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e15 | 3.90 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e16 | 4.00 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e17 | 4.25 | CLOSING_END | B | track_002 | radar |  |
| B:e18 | 4.35 | EGO_PATH_EXIT | B | track_002 | radar |  |
| B:e19 | 5.25 | TRACK_LOST | B | track_002 | radar |  |
| B:e20 | 5.35 | CLOSING_END | B | track_001 | radar |  |
| B:e21 | 5.65 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e22 | 6.40 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e23 | 6.90 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e24 | 8.90 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e02 --SAME_TRACK--> B:e03
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e08
    B:e05 --SAME_TRACK--> B:e14
    B:e05 --SAME_TRACK--> B:e15
    B:e05 --SAME_TRACK--> B:e17
    B:e05 --SAME_TRACK--> B:e18
    B:e05 --SAME_TRACK--> B:e19
    B:e02 --SAME_TRACK--> B:e20
    B:e02 --SAME_TRACK--> B:e21
    B:e02 --SAME_TRACK--> B:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.45 | B:e02 TRACK_APPEARED_RIGHT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 1.40 |
| 1.80 | B:e04 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING<br>track_001: CLOSING | 1.70 |
| 1.95 | B:e05 TRACK_APPEARED_LEFT track_002<br>B:e06 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 1.90 |
| 2.10 | B:e07 STOP_SIGN_DETECTED_END sign-0<br>B:e08 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known | 2.00 |
| 2.25 | B:e09 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.20 |
| 2.55 | B:e10 BRAKE_START | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.50 |
| 3.35 | B:e11 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 3.30 |
| 3.40 | B:e12 MOVING_END<br>B:e13 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 3.30 |
| 3.55 | B:e14 CRITICAL_TTC_END track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 3.50 |
| 3.90 | B:e15 EGO_PATH_ENTRY track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known | 3.80 |
| 4.00 | B:e16 STOP_SIGN_DETECTED_START sign-1 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known | 3.90 |
| 4.25 | B:e17 CLOSING_END track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 4.20 |
| 4.35 | B:e18 EGO_PATH_EXIT track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 4.30 |
| 5.25 | B:e19 TRACK_LOST track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 5.20 |
| 5.35 | B:e20 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 5.30 |
| 5.65 | B:e21 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 5.60 |
| 6.40 | B:e22 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 6.30 |
| 6.90 | B:e23 STOP_SIGN_DETECTED_END sign-1 | ego: STOP, BRAKE<br>track_001: no active state<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 6.80 |
| 8.90 | B:e24 STOP_SIGN_DETECTED_START sign-1 | ego: STOP, BRAKE<br>track_001: no active state<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-1: STOP sign known | 8.80 |

## States still active when observation ended

- BRAKE, since B:e10 (t = 2.55 s)
- STOP, since B:e13 (t = 3.40 s)
- STOP_SIGN_DETECTED of sign-1, since B:e24 (t = 8.90 s)

## Tracks lost

- lost with no state active: track_002

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 5.65, no critical TTC
- track_002: CRITICAL_TTC_START 2.10; EGO_PATH_ENTRY 3.90 after critical TTC (+1.80 s)

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 4.00 s -> 6.90 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-1: detected 8.90 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.45 | 10.55 | 176 | 28.9 m / +38 deg | 7.13 m (5.45) | 29.5 m / -55 deg | 5.9 m/s |
| track_002 | 1.95 | 5.25 | 67 | 29.5 m / -59 deg | 3.28 m (4.25) | 10.3 m / +80 deg | 11.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.45 s: B's radar started tracking track_001, which appeared on its right.
- t = 1.45 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.80 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: B's radar started tracking track_002, which appeared on its left.
- t = 1.95 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.10 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.10 s: B's time-to-contact with track_002 became critical.
- t = 2.25 s: B started turning left.
- t = 2.55 s: B started braking.
- t = 3.35 s: B stopped turning left.
- t = 3.40 s: B stopped moving.
- t = 3.40 s: B came to a stop.
- t = 3.55 s: B's time-to-contact with track_002 stopped being critical.
- t = 3.90 s: B observed track_002 enter its forward path corridor.
- t = 4.00 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 4.25 s: B observed track_002 stop closing in.
- t = 4.35 s: B observed track_002 leave its forward path corridor.
- t = 5.25 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 5.35 s: B observed track_001 stop closing in.
- t = 5.65 s: B observed track_001 enter its forward path corridor.
- t = 6.40 s: B observed track_001 leave its forward path corridor.
- t = 6.90 s: B's camera stopped detecting STOP sign sign-1.
- t = 8.90 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
