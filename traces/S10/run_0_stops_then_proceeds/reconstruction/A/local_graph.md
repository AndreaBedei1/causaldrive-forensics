# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 305.1153160445392 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 135 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.35 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 25 (PRECEDES 20, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.85 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e03 | 2.15 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.55 | BRAKE_START | A | - | controls |  |
| A:e05 | 2.65 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e06 | 2.65 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e07 | 3.35 | MOVING_END | A | - | ego |  |
| A:e08 | 3.35 | STOP_START | A | - | ego |  |
| A:e09 | 5.80 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e10 | 6.15 | CLOSING_END | A | track_001 | radar |  |
| A:e11 | 6.25 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e12 | 6.75 | BRAKE_END | A | - | controls |  |
| A:e13 | 7.10 | STOP_END | A | - | ego |  |
| A:e14 | 7.10 | MOVING_START | A | - | ego |  |
| A:e15 | 7.65 | TURN_LEFT_START | A | - | ego |  |
| A:e16 | 10.30 | TURN_LEFT_END | A | - | ego |  |
| A:e17 | 11.60 | TRACK_LOST | A | track_001 | radar |  |

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
    A:e05 --SAME_TRACK--> A:e06
    A:e05 --SAME_TRACK--> A:e09
    A:e05 --SAME_TRACK--> A:e10
    A:e05 --SAME_TRACK--> A:e11
    A:e05 --SAME_TRACK--> A:e17
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 1.85 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.80 |
| 2.15 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known | 2.10 |
| 2.55 | A:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known | 2.50 |
| 2.65 | A:e05 TRACK_APPEARED_LEFT track_001<br>A:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>sign-0: STOP sign known | 2.60 |
| 3.35 | A:e07 MOVING_END<br>A:e08 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known | 3.30 |
| 5.80 | A:e09 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known | 5.70 |
| 6.15 | A:e10 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known | 6.10 |
| 6.25 | A:e11 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known | 6.20 |
| 6.75 | A:e12 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known | 6.70 |
| 7.10 | A:e13 STOP_END<br>A:e14 MOVING_START | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known | 7.00 |
| 7.65 | A:e15 TURN_LEFT_START | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known | 7.60 |
| 10.30 | A:e16 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>sign-0: STOP sign known | 10.20 |
| 11.60 | A:e17 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>sign-0: STOP sign known | 11.50 |

## States still active when observation ended

- MOVING, since A:e14 (t = 7.10 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 5.80, no critical TTC

## Sign detection windows

- STOP sign sign-0: detected 1.85 s -> 2.15 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.65 | 11.60 | 148 | 35.7 m / -67 deg | 7.47 m (6.15) | 83.7 m / -179 deg | 10.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.85 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 2.15 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.55 s: A started braking.
- t = 2.65 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.65 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.35 s: A stopped moving.
- t = 3.35 s: A came to a stop.
- t = 5.80 s: A observed track_001 enter its forward path corridor.
- t = 6.15 s: A observed track_001 stop closing in.
- t = 6.25 s: A observed track_001 leave its forward path corridor.
- t = 6.75 s: A released the brake.
- t = 7.10 s: A left its stop.
- t = 7.10 s: A started moving.
- t = 7.65 s: A started turning left.
- t = 10.30 s: A stopped turning left.
- t = 11.60 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
