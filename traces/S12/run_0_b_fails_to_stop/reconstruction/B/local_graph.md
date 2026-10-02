# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 97.54959324374795 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 24 (PRECEDES 19, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.95 | BRAKE_START | B | - | controls |  |
| B:e03 | 2.65 | BRAKE_END | B | - | controls |  |
| B:e04 | 3.50 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=True |
| B:e05 | 5.30 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e06 | 8.15 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e07 | 8.15 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e08 | 8.60 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e09 | 9.70 | COLLISION | B | - | collision_sensor | peak_impulse=7339.57 |
| B:e10 | 9.75 | BRAKE_START | B | - | controls |  |
| B:e11 | 10.05 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e12 | 10.05 | MOVING_END | B | - | ego |  |
| B:e13 | 10.05 | STOP_START | B | - | ego |  |
| B:e14 | 10.15 | CLOSING_END | B | track_001 | radar |  |
| B:e15 | 10.15 | EGO_PATH_ENTRY | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e06 --SAME_TRACK--> B:e07
    B:e06 --SAME_TRACK--> B:e08
    B:e06 --SAME_TRACK--> B:e11
    B:e06 --SAME_TRACK--> B:e14
    B:e06 --SAME_TRACK--> B:e15
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.95 | B:e02 BRAKE_START | ego: MOVING | 1.90 |
| 2.65 | B:e03 BRAKE_END | ego: MOVING, BRAKE | 2.60 |
| 3.50 | B:e04 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 3.40 |
| 5.30 | B:e05 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>sign-1: STOP sign known, relevant to the path | 5.20 |
| 8.15 | B:e06 TRACK_APPEARED_RIGHT track_001<br>B:e07 CLOSING_START track_001 | ego: MOVING<br>sign-1: STOP sign known, relevant to the path | 8.10 |
| 8.60 | B:e08 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 8.50 |
| 9.70 | B:e09 COLLISION | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known, relevant to the path | 9.60 |
| 9.75 | B:e10 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known, relevant to the path | 9.70 |
| 10.05 | B:e11 CRITICAL_TTC_END track_001<br>B:e12 MOVING_END<br>B:e13 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known, relevant to the path | 10.00 |
| 10.15 | B:e14 CLOSING_END track_001<br>B:e15 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 10.10 |

## States still active when observation ended

- BRAKE, since B:e10 (t = 9.75 s)
- STOP, since B:e13 (t = 10.05 s)
- EGO_PATH of track_001, since B:e15 (t = 10.15 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 8.60, COLLISION 9.70 (+1.10 s); EGO_PATH_ENTRY 10.15 after critical TTC (+1.55 s)

## Sign detection windows

- STOP sign sign-1: detected 3.50 s -> 5.30 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 8.15 | 15.95 | 157 | 15.2 m / +44 deg | 2.65 m (10.20) | 2.9 m / +35 deg | 7.6 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.95 s: B started braking.
- t = 2.65 s: B released the brake.
- t = 3.50 s: B's camera established a STOP sign detection (sign-1).
- t = 5.30 s: B's camera stopped detecting STOP sign sign-1.
- t = 8.15 s: B's radar started tracking track_001, which appeared on its right.
- t = 8.15 s: B observed track_001 start closing in (already the case when first observed).
- t = 8.60 s: B's time-to-contact with track_001 became critical.
- t = 9.70 s: B's collision sensor recorded a contact (peak impulse 7340 N*s).
- t = 9.75 s: B started braking.
- t = 10.05 s: B's time-to-contact with track_001 stopped being critical.
- t = 10.05 s: B stopped moving.
- t = 10.05 s: B came to a stop.
- t = 10.15 s: B observed track_001 stop closing in.
- t = 10.15 s: B observed track_001 enter its forward path corridor.
