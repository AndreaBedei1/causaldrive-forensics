# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 97.54959324374795 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 25 (PRECEDES 22, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.65 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.25 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e05 | 3.40 | MOVING_END | A | - | ego |  |
| A:e06 | 3.40 | STOP_START | A | - | ego |  |
| A:e07 | 4.25 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e08 | 4.25 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e09 | 7.75 | BRAKE_END | A | - | controls |  |
| A:e10 | 8.10 | STOP_END | A | - | ego |  |
| A:e11 | 8.10 | MOVING_START | A | - | ego |  |
| A:e12 | 8.60 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e13 | 9.10 | TURN_LEFT_START | A | - | ego |  |
| A:e14 | 9.65 | TRACK_LOST | A | track_001 | radar |  |
| A:e15 | 9.70 | COLLISION | A | - | collision_sensor | peak_impulse=7339.57 |
| A:e16 | 9.75 | BRAKE_START | A | - | controls |  |
| A:e17 | 9.80 | TURN_LEFT_END | A | - | ego |  |
| A:e18 | 10.20 | MOVING_END | A | - | ego |  |
| A:e19 | 10.20 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e07 --SAME_TRACK--> A:e08
    A:e07 --SAME_TRACK--> A:e12
    A:e07 --SAME_TRACK--> A:e14
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.65 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.25 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.65 | A:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.60 |
| 3.40 | A:e05 MOVING_END<br>A:e06 STOP_START | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 4.25 | A:e07 TRACK_APPEARED_LEFT track_001<br>A:e08 CLOSING_START track_001 | ego: STOP, BRAKE<br>sign-0: STOP sign known, relevant to the path | 4.20 |
| 7.75 | A:e09 BRAKE_END | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 7.70 |
| 8.10 | A:e10 STOP_END<br>A:e11 MOVING_START | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.00 |
| 8.60 | A:e12 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.50 |
| 9.10 | A:e13 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 9.00 |
| 9.65 | A:e14 TRACK_LOST track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 9.60 |
| 9.70 | A:e15 COLLISION | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.60 |
| 9.75 | A:e16 BRAKE_START | ego: MOVING, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.70 |
| 9.80 | A:e17 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.70 |
| 10.20 | A:e18 MOVING_END<br>A:e19 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 10.10 |

## States still active when observation ended

- CLOSING of track_001, since A:e08 (t = 4.25 s); the track was lost at 9.65 s
- CRITICAL_TTC of track_001, since A:e12 (t = 8.60 s); the track was lost at 9.65 s
- BRAKE, since A:e16 (t = 9.75 s)
- STOP, since A:e19 (t = 10.20 s)

## Tracks lost

- track_001 at 9.65 s (A:e14): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 8.60, COLLISION 9.70 (+1.10 s)

## Sign detection windows

- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 4.25 | 9.65 | 106 | 30.0 m / -67 deg | 3.40 m (9.65) | 3.4 m / -49 deg | 4.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.65 s: A's camera established a STOP sign detection (sign-0).
- t = 2.25 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.65 s: A started braking.
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 4.25 s: A's radar started tracking track_001, which appeared on its left.
- t = 4.25 s: A observed track_001 start closing in (already the case when first observed).
- t = 7.75 s: A released the brake.
- t = 8.10 s: A left its stop.
- t = 8.10 s: A started moving.
- t = 8.60 s: A's time-to-contact with track_001 became critical.
- t = 9.10 s: A started turning left.
- t = 9.65 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 9.70 s: A's collision sensor recorded a contact (peak impulse 7340 N*s).
- t = 9.75 s: A started braking.
- t = 9.80 s: A stopped turning left.
- t = 10.20 s: A stopped moving.
- t = 10.20 s: A came to a stop.
