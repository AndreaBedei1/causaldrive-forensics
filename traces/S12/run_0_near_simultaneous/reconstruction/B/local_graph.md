# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 119.71085980534554 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 22; edges: 39 (PRECEDES 31, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.80 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=True |
| B:e03 | 2.60 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e04 | 2.75 | BRAKE_START | B | - | controls |  |
| B:e05 | 2.80 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e06 | 2.80 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 3.45 | CLOSING_END | B | track_001 | radar |  |
| B:e08 | 3.50 | MOVING_END | B | - | ego |  |
| B:e09 | 3.50 | STOP_START | B | - | ego |  |
| B:e10 | 6.95 | BRAKE_END | B | - | controls |  |
| B:e11 | 7.30 | CLOSING_START | B | track_001 | radar |  |
| B:e12 | 7.35 | STOP_END | B | - | ego |  |
| B:e13 | 7.35 | MOVING_START | B | - | ego |  |
| B:e14 | 8.30 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e15 | 8.95 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e16 | 9.50 | COLLISION | B | - | collision_sensor | peak_impulse=4032.49 |
| B:e17 | 9.50 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e18 | 9.55 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e19 | 9.55 | CLOSING_END | B | track_001 | radar |  |
| B:e20 | 9.55 | BRAKE_START | B | - | controls |  |
| B:e21 | 9.95 | MOVING_END | B | - | ego |  |
| B:e22 | 9.95 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e07
    B:e05 --SAME_TRACK--> B:e11
    B:e05 --SAME_TRACK--> B:e14
    B:e05 --SAME_TRACK--> B:e15
    B:e05 --SAME_TRACK--> B:e17
    B:e05 --SAME_TRACK--> B:e18
    B:e05 --SAME_TRACK--> B:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.80 | B:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.70 |
| 2.60 | B:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.50 |
| 2.75 | B:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.70 |
| 2.80 | B:e05 TRACK_APPEARED_RIGHT track_001<br>B:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>sign-0: STOP sign known, relevant to the path | 2.70 |
| 3.45 | B:e07 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.40 |
| 3.50 | B:e08 MOVING_END<br>B:e09 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 3.40 |
| 6.95 | B:e10 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 6.90 |
| 7.30 | B:e11 CLOSING_START track_001 | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 7.20 |
| 7.35 | B:e12 STOP_END<br>B:e13 MOVING_START | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 7.30 |
| 8.30 | B:e14 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path | 8.20 |
| 8.95 | B:e15 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 8.90 |
| 9.50 | B:e16 COLLISION<br>B:e17 EGO_PATH_EXIT track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 9.40 |
| 9.55 | B:e18 CRITICAL_TTC_END track_001<br>B:e19 CLOSING_END track_001<br>B:e20 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 9.50 |
| 9.95 | B:e21 MOVING_END<br>B:e22 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path | 9.90 |

## States still active when observation ended

- BRAKE, since B:e20 (t = 9.55 s)
- STOP, since B:e22 (t = 9.95 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 8.30, COLLISION 9.50 (+1.20 s); EGO_PATH_ENTRY 8.95 after critical TTC (+0.65 s)

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.80 | 14.95 | 244 | 26.4 m / +32 deg | 2.14 m (9.50) | 3.3 m / -84 deg | 8.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.80 s: B's camera established a STOP sign detection (sign-0).
- t = 2.60 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.75 s: B started braking.
- t = 2.80 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.80 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.45 s: B observed track_001 stop closing in.
- t = 3.50 s: B stopped moving.
- t = 3.50 s: B came to a stop.
- t = 6.95 s: B released the brake.
- t = 7.30 s: B observed track_001 start closing in.
- t = 7.35 s: B left its stop.
- t = 7.35 s: B started moving.
- t = 8.30 s: B's time-to-contact with track_001 became critical.
- t = 8.95 s: B observed track_001 enter its forward path corridor.
- t = 9.50 s: B's collision sensor recorded a contact (peak impulse 4032 N*s).
- t = 9.50 s: B observed track_001 leave its forward path corridor.
- t = 9.55 s: B's time-to-contact with track_001 stopped being critical.
- t = 9.55 s: B observed track_001 stop closing in.
- t = 9.55 s: B started braking.
- t = 9.95 s: B stopped moving.
- t = 9.95 s: B came to a stop.
