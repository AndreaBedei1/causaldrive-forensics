# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 36.92172956466675 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 4 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 25; edges: 54 (PRECEDES 42, SAME_TRACK 12)

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
| B:e08 | 8.65 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e09 | 9.60 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e10 | 9.70 | COLLISION | B | - | collision_sensor | peak_impulse=7339.57 |
| B:e11 | 9.70 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e12 | 9.70 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e13 | 9.75 | BRAKE_START | B | - | controls |  |
| B:e14 | 9.75 | TRACK_APPEARED_LEFT | B | track_003 | radar |  |
| B:e15 | 9.75 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e16 | 9.75 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e17 | 9.75 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e18 | 9.85 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e19 | 9.95 | CLOSING_END | B | track_001 | radar |  |
| B:e20 | 10.05 | MOVING_END | B | - | ego |  |
| B:e21 | 10.05 | STOP_START | B | - | ego |  |
| B:e22 | 10.10 | CLOSING_END | B | track_002 | radar |  |
| B:e23 | 10.10 | CLOSING_END | B | track_004 | radar |  |
| B:e24 | 10.20 | TRACK_LOST | B | track_004 | radar |  |
| B:e25 | 10.25 | CLOSING_END | B | track_003 | radar |  |

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
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e10 --PRECEDES--> B:e15
    B:e10 --PRECEDES--> B:e16
    B:e10 --PRECEDES--> B:e17
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e15
    B:e11 --PRECEDES--> B:e16
    B:e11 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e16
    B:e12 --PRECEDES--> B:e17
    B:e13 --PRECEDES--> B:e18
    B:e14 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e06 --SAME_TRACK--> B:e07
    B:e06 --SAME_TRACK--> B:e08
    B:e06 --SAME_TRACK--> B:e09
    B:e11 --SAME_TRACK--> B:e12
    B:e14 --SAME_TRACK--> B:e16
    B:e15 --SAME_TRACK--> B:e17
    B:e06 --SAME_TRACK--> B:e18
    B:e06 --SAME_TRACK--> B:e19
    B:e11 --SAME_TRACK--> B:e22
    B:e15 --SAME_TRACK--> B:e23
    B:e15 --SAME_TRACK--> B:e24
    B:e14 --SAME_TRACK--> B:e25
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
| 8.65 | B:e08 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 8.60 |
| 9.60 | B:e09 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known, relevant to the path | 9.50 |
| 9.70 | B:e10 COLLISION<br>B:e11 TRACK_APPEARED_LEFT track_002<br>B:e12 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known, relevant to the path | 9.60 |
| 9.75 | B:e13 BRAKE_START<br>B:e14 TRACK_APPEARED_LEFT track_003<br>B:e15 TRACK_APPEARED_LEFT track_004<br>B:e16 CLOSING_START track_003<br>B:e17 CLOSING_START track_004 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-1: STOP sign known, relevant to the path | 9.70 |
| 9.85 | B:e18 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path | 9.80 |
| 9.95 | B:e19 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path | 9.90 |
| 10.05 | B:e20 MOVING_END<br>B:e21 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path | 10.00 |
| 10.10 | B:e22 CLOSING_END track_002<br>B:e23 CLOSING_END track_004 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>sign-1: STOP sign known, relevant to the path | 10.00 |
| 10.20 | B:e24 TRACK_LOST track_004 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track_004: no active state<br>sign-1: STOP sign known, relevant to the path | 10.10 |
| 10.25 | B:e25 CLOSING_END track_003 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004<br>sign-1: STOP sign known, relevant to the path | 10.20 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e09 (t = 9.60 s)
- BRAKE, since B:e13 (t = 9.75 s)
- STOP, since B:e21 (t = 10.05 s)

## Tracks lost

- lost with no state active: track_004

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 8.65, COLLISION 9.70 (+1.05 s); EGO_PATH_ENTRY 9.60 after critical TTC (+0.95 s)

## Sign detection windows

- STOP sign sign-1: detected 3.50 s -> 5.30 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 8.15 | 15.95 | 157 | 13.3 m / +51 deg | 0.56 m (15.95) | 0.6 m / +64 deg | 8.7 m/s |
| track_002 | 9.70 | 15.95 | 126 | 15.2 m / -66 deg | 13.81 m (15.85) | 13.8 m / -72 deg | 9.3 m/s |
| track_003 | 9.75 | 15.95 | 125 | 16.4 m / -42 deg | 14.35 m (15.25) | 14.4 m / -53 deg | 5.6 m/s |
| track_004 | 9.75 | 10.20 | 10 | 14.8 m / -78 deg | 13.69 m (10.15) | 13.7 m / -79 deg | 8.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.95 s: B started braking.
- t = 2.65 s: B released the brake.
- t = 3.50 s: B's camera established a STOP sign detection (sign-1).
- t = 5.30 s: B's camera stopped detecting STOP sign sign-1.
- t = 8.15 s: B's radar started tracking track_001, which appeared on its right.
- t = 8.15 s: B observed track_001 start closing in (already the case when first observed).
- t = 8.65 s: B's time-to-contact with track_001 became critical.
- t = 9.60 s: B observed track_001 enter its forward path corridor.
- t = 9.70 s: B's collision sensor recorded a contact (peak impulse 7340 N*s).
- t = 9.70 s: B's radar started tracking track_002, which appeared on its left.
- t = 9.70 s: B observed track_002 start closing in (already the case when first observed).
- t = 9.75 s: B started braking.
- t = 9.75 s: B's radar started tracking track_003, which appeared on its left.
- t = 9.75 s: B's radar started tracking track_004, which appeared on its left.
- t = 9.75 s: B observed track_003 start closing in (already the case when first observed).
- t = 9.75 s: B observed track_004 start closing in (already the case when first observed).
- t = 9.85 s: B's time-to-contact with track_001 stopped being critical.
- t = 9.95 s: B observed track_001 stop closing in.
- t = 10.05 s: B stopped moving.
- t = 10.05 s: B came to a stop.
- t = 10.10 s: B observed track_002 stop closing in.
- t = 10.10 s: B observed track_004 stop closing in.
- t = 10.20 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 10.25 s: B observed track_003 stop closing in.
