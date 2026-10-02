# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 76.44139377772808 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 25 (PRECEDES 20, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.95 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 3.55 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 4.35 | BRAKE_START | A | - | controls |  |
| A:e05 | 4.75 | MOVING_END | A | - | ego |  |
| A:e06 | 4.75 | STOP_START | A | - | ego |  |
| A:e07 | 6.90 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e08 | 6.90 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e09 | 9.75 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e10 | 9.90 | CLOSING_END | A | track_001 | radar |  |
| A:e11 | 10.20 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e12 | 10.45 | BRAKE_END | A | - | controls |  |
| A:e13 | 10.80 | STOP_END | A | - | ego |  |
| A:e14 | 10.80 | MOVING_START | A | - | ego |  |
| A:e15 | 12.10 | TURN_LEFT_START | A | - | ego |  |
| A:e16 | 15.30 | TURN_LEFT_END | A | - | ego |  |
| A:e17 | 16.20 | TRACK_LOST | A | track_001 | radar |  |

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
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e07 --SAME_TRACK--> A:e08
    A:e07 --SAME_TRACK--> A:e09
    A:e07 --SAME_TRACK--> A:e10
    A:e07 --SAME_TRACK--> A:e11
    A:e07 --SAME_TRACK--> A:e17
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.95 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.90 |
| 3.55 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 3.50 |
| 4.35 | A:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 4.30 |
| 4.75 | A:e05 MOVING_END<br>A:e06 STOP_START | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path | 4.70 |
| 6.90 | A:e07 TRACK_APPEARED_LEFT track_001<br>A:e08 CLOSING_START track_001 | ego: STOP, BRAKE<br>sign-0: STOP sign known, relevant to the path | 6.80 |
| 9.75 | A:e09 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 9.70 |
| 9.90 | A:e10 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 9.80 |
| 10.20 | A:e11 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 10.10 |
| 10.45 | A:e12 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 10.40 |
| 10.80 | A:e13 STOP_END<br>A:e14 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 10.70 |
| 12.10 | A:e15 TURN_LEFT_START | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 12.00 |
| 15.30 | A:e16 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 15.20 |
| 16.20 | A:e17 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 16.10 |

## States still active when observation ended

- MOVING, since A:e14 (t = 10.80 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 9.75, no critical TTC

## Sign detection windows

- STOP sign sign-0: detected 0.95 s -> 3.55 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 6.90 | 16.20 | 166 | 22.9 m / -57 deg | 12.28 m (9.95) | 75.9 m / -176 deg | 8.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.95 s: A's camera established a STOP sign detection (sign-0).
- t = 3.55 s: A's camera stopped detecting STOP sign sign-0.
- t = 4.35 s: A started braking.
- t = 4.75 s: A stopped moving.
- t = 4.75 s: A came to a stop.
- t = 6.90 s: A's radar started tracking track_001, which appeared on its left.
- t = 6.90 s: A observed track_001 start closing in (already the case when first observed).
- t = 9.75 s: A observed track_001 enter its forward path corridor.
- t = 9.90 s: A observed track_001 stop closing in.
- t = 10.20 s: A observed track_001 leave its forward path corridor.
- t = 10.45 s: A released the brake.
- t = 10.80 s: A left its stop.
- t = 10.80 s: A started moving.
- t = 12.10 s: A started turning left.
- t = 15.30 s: A stopped turning left.
- t = 16.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
