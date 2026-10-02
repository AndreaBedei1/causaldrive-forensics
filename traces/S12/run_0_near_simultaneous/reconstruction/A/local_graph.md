# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 119.71085980534554 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 23; edges: 36 (PRECEDES 30, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.65 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.25 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.60 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e05 | 2.60 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e07 | 3.40 | MOVING_END | A | - | ego |  |
| A:e08 | 3.40 | STOP_START | A | - | ego |  |
| A:e09 | 3.50 | CLOSING_END | A | track_001 | radar |  |
| A:e10 | 6.95 | BRAKE_END | A | - | controls |  |
| A:e11 | 7.30 | STOP_END | A | - | ego |  |
| A:e12 | 7.30 | MOVING_START | A | - | ego |  |
| A:e13 | 7.30 | CLOSING_START | A | track_001 | radar |  |
| A:e14 | 8.25 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e15 | 8.30 | TURN_LEFT_START | A | - | ego |  |
| A:e16 | 9.50 | COLLISION | A | - | collision_sensor | peak_impulse=4032.49 |
| A:e17 | 9.50 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e18 | 9.50 | CLOSING_END | A | track_001 | radar |  |
| A:e19 | 9.55 | BRAKE_START | A | - | controls |  |
| A:e20 | 10.00 | TURN_LEFT_END | A | - | ego |  |
| A:e21 | 10.00 | MOVING_END | A | - | ego |  |
| A:e22 | 10.00 | STOP_START | A | - | ego |  |
| A:e23 | 10.95 | STOP_SIGN_DETECTED_START | A | sign-1 | camera | relevant_to_ego_path=False |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e23
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e13
    A:e04 --SAME_TRACK--> A:e14
    A:e04 --SAME_TRACK--> A:e17
    A:e04 --SAME_TRACK--> A:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.65 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.25 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.60 | A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 CLOSING_START track_001 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.50 |
| 2.65 | A:e06 BRAKE_START | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 2.60 |
| 3.40 | A:e07 MOVING_END<br>A:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 3.50 | A:e09 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.40 |
| 6.95 | A:e10 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.90 |
| 7.30 | A:e11 STOP_END<br>A:e12 MOVING_START<br>A:e13 CLOSING_START track_001 | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 7.20 |
| 8.25 | A:e14 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.20 |
| 8.30 | A:e15 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 8.20 |
| 9.50 | A:e16 COLLISION<br>A:e17 CRITICAL_TTC_END track_001<br>A:e18 CLOSING_END track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 9.40 |
| 9.55 | A:e19 BRAKE_START | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 9.50 |
| 10.00 | A:e20 TURN_LEFT_END<br>A:e21 MOVING_END<br>A:e22 STOP_START | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 9.90 |
| 10.95 | A:e23 STOP_SIGN_DETECTED_START sign-1 | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 10.90 |

## States still active when observation ended

- BRAKE, since A:e19 (t = 9.55 s)
- STOP, since A:e22 (t = 10.00 s)
- STOP_SIGN_DETECTED of sign-1, since A:e23 (t = 10.95 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 8.25, COLLISION 9.50 (+1.25 s)

## Sign detection windows

- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none
- STOP sign sign-1: detected 10.95 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.60 | 14.95 | 247 | 28.6 m / -54 deg | 2.50 m (9.50) | 3.7 m / -124 deg | 9.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.65 s: A's camera established a STOP sign detection (sign-0).
- t = 2.25 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.60 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.60 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.65 s: A started braking.
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 3.50 s: A observed track_001 stop closing in.
- t = 6.95 s: A released the brake.
- t = 7.30 s: A left its stop.
- t = 7.30 s: A started moving.
- t = 7.30 s: A observed track_001 start closing in.
- t = 8.25 s: A's time-to-contact with track_001 became critical.
- t = 8.30 s: A started turning left.
- t = 9.50 s: A's collision sensor recorded a contact (peak impulse 4032 N*s).
- t = 9.50 s: A's time-to-contact with track_001 stopped being critical.
- t = 9.50 s: A observed track_001 stop closing in.
- t = 9.55 s: A started braking.
- t = 10.00 s: A stopped turning left.
- t = 10.00 s: A stopped moving.
- t = 10.00 s: A came to a stop.
- t = 10.95 s: A's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
