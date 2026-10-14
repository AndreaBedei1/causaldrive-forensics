# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 204.24685563519597 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 31; edges: 60 (PRECEDES 46, SAME_TRACK 14)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 1.10 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=True |
| B:e04 | 1.70 | TRACK_APPEARED_RIGHT | B | track_001 | radar | initial_in_ego_path=False |
| B:e05 | 1.70 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 2.00 | TRACK_APPEARED_LEFT | B | track_002 | radar | initial_in_ego_path=False |
| B:e07 | 2.00 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e08 | 2.25 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e09 | 2.30 | TURN_LEFT_START | B | - | ego |  |
| B:e10 | 2.50 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e11 | 2.95 | THROTTLE_END | B | - | controls |  |
| B:e12 | 2.95 | BRAKE_START | B | - | controls |  |
| B:e13 | 3.05 | EGO_PATH_ENTRY | B | track_001 | radar | geometry=estimated_body |
| B:e14 | 3.40 | EGO_PATH_EXIT | B | track_001 | radar | geometry=estimated_body |
| B:e15 | 3.50 | BRAKE_END | B | - | controls |  |
| B:e16 | 3.60 | EGO_PATH_ENTRY | B | track_002 | radar | geometry=estimated_body |
| B:e17 | 3.65 | THROTTLE_START | B | - | controls |  |
| B:e18 | 3.80 | COLLISION | B | - | collision_sensor | peak_impulse=10358.22 |
| B:e19 | 3.80 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e20 | 3.80 | TURN_LEFT_END | B | - | ego |  |
| B:e21 | 3.85 | EGO_PATH_EXIT | B | track_002 | radar | geometry=estimated_body |
| B:e22 | 3.85 | THROTTLE_END | B | - | controls |  |
| B:e23 | 3.85 | BRAKE_START | B | - | controls |  |
| B:e24 | 4.00 | MOVING_END | B | - | ego |  |
| B:e25 | 4.00 | STOP_START | B | - | ego |  |
| B:e26 | 4.05 | EGO_PATH_ENTRY | B | track_002 | radar | geometry=estimated_body |
| B:e27 | 4.15 | CLOSING_END | B | track_002 | radar |  |
| B:e28 | 4.70 | CLOSING_END | B | track_001 | radar |  |
| B:e29 | 4.70 | EGO_PATH_ENTRY | B | track_001 | radar | geometry=estimated_body |
| B:e30 | 5.40 | EGO_PATH_EXIT | B | track_001 | radar | geometry=estimated_body |
| B:e31 | 5.50 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e23
    B:e19 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e23
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e24
    B:e21 --PRECEDES--> B:e25
    B:e22 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e26
    B:e26 --PRECEDES--> B:e27
    B:e27 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e30
    B:e30 --PRECEDES--> B:e31
    B:e04 --SAME_TRACK--> B:e05
    B:e06 --SAME_TRACK--> B:e07
    B:e06 --SAME_TRACK--> B:e10
    B:e04 --SAME_TRACK--> B:e13
    B:e04 --SAME_TRACK--> B:e14
    B:e06 --SAME_TRACK--> B:e16
    B:e06 --SAME_TRACK--> B:e19
    B:e06 --SAME_TRACK--> B:e21
    B:e06 --SAME_TRACK--> B:e26
    B:e06 --SAME_TRACK--> B:e27
    B:e04 --SAME_TRACK--> B:e28
    B:e04 --SAME_TRACK--> B:e29
    B:e04 --SAME_TRACK--> B:e30
    B:e04 --SAME_TRACK--> B:e31
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START | ego: not yet observed | - |
| 1.10 | B:e03 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING, THROTTLE | 1.00 |
| 1.70 | B:e04 TRACK_APPEARED_RIGHT track_001<br>B:e05 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>sign-0: STOP sign known, relevant to the path | 1.60 |
| 2.00 | B:e06 TRACK_APPEARED_LEFT track_002<br>B:e07 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path | 1.90 |
| 2.25 | B:e08 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.30 | B:e09 TURN_LEFT_START | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.50 | B:e10 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC?<br>sign-0: STOP sign known, relevant to the path | 2.40 |
| 2.95 | B:e11 THROTTLE_END<br>B:e12 BRAKE_START | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 2.90 |
| 3.05 | B:e13 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 3.00 |
| 3.40 | B:e14 EGO_PATH_EXIT track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 3.50 | B:e15 BRAKE_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 3.40 |
| 3.60 | B:e16 EGO_PATH_ENTRY track_002 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path | 3.50 |
| 3.65 | B:e17 THROTTLE_START | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 3.60 |
| 3.80 | B:e18 COLLISION<br>B:e19 CRITICAL_TTC_END track_002<br>B:e20 TURN_LEFT_END | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 3.70 |
| 3.85 | B:e21 EGO_PATH_EXIT track_002<br>B:e22 THROTTLE_END<br>B:e23 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 3.80 |
| 4.00 | B:e24 MOVING_END<br>B:e25 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known, relevant to the path | 3.90 |
| 4.05 | B:e26 EGO_PATH_ENTRY track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known, relevant to the path | 4.00 |
| 4.15 | B:e27 CLOSING_END track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 4.10 |
| 4.70 | B:e28 CLOSING_END track_001<br>B:e29 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 4.60 |
| 5.40 | B:e30 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 5.30 |
| 5.50 | B:e31 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path | 5.40 |

## States still active when observation ended

- BRAKE, since B:e23 (t = 3.85 s)
- STOP, since B:e25 (t = 4.00 s)
- EGO_PATH of track_002, since B:e26 (t = 4.05 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: EGO_PATH_ENTRY 3.05, no critical TTC
- track_002: CRITICAL_TTC_START 2.50, COLLISION 3.80 (+1.30 s); EGO_PATH_ENTRY 3.60 after critical TTC (+1.10 s)

## Sign detection windows

- STOP sign sign-0: detected 1.10 s -> 2.25 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.70 | 5.50 | 67 | 27.8 m / +37 deg | 6.06 m (5.00) | 6.5 m / +13 deg | 7.0 m/s |
| track_002 | 2.00 | 13.95 | 240 | 30.1 m / -56 deg | 0.27 m (4.15) | 2.5 m / +38 deg | 10.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 1.10 s: B's camera established a STOP sign detection (sign-0).
- t = 1.70 s: B's radar started tracking track_001, which appeared on its right.
- t = 1.70 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.00 s: B's radar started tracking track_002, which appeared on its left.
- t = 2.00 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.25 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.30 s: B started turning left.
- t = 2.50 s: B's time-to-contact with track_002 became critical.
- t = 2.95 s: B released the accelerator.
- t = 2.95 s: B started braking.
- t = 3.05 s: B observed track_001 enter its forward path corridor.
- t = 3.40 s: B observed track_001 leave its forward path corridor.
- t = 3.50 s: B released the brake.
- t = 3.60 s: B observed track_002 enter its forward path corridor.
- t = 3.65 s: B pressed the accelerator.
- t = 3.80 s: B's collision sensor recorded a contact (peak impulse 10358 N*s).
- t = 3.80 s: B's time-to-contact with track_002 stopped being critical.
- t = 3.80 s: B stopped turning left.
- t = 3.85 s: B observed track_002 leave its forward path corridor.
- t = 3.85 s: B released the accelerator.
- t = 3.85 s: B started braking.
- t = 4.00 s: B stopped moving.
- t = 4.00 s: B came to a stop.
- t = 4.05 s: B observed track_002 enter its forward path corridor.
- t = 4.15 s: B observed track_002 stop closing in.
- t = 4.70 s: B observed track_001 stop closing in.
- t = 4.70 s: B observed track_001 enter its forward path corridor.
- t = 5.40 s: B observed track_001 leave its forward path corridor.
- t = 5.50 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
