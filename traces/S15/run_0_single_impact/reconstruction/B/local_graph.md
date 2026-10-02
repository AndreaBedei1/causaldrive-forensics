# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 220.40668706968427 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 33 (PRECEDES 26, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.75 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e03 | 2.05 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e04 | 2.10 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e05 | 2.10 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 2.10 | CRITICAL_TTC_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 2.25 | TURN_LEFT_START | B | - | ego |  |
| B:e08 | 2.90 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e09 | 2.95 | BRAKE_START | B | - | controls |  |
| B:e10 | 3.50 | BRAKE_END | B | - | controls |  |
| B:e11 | 3.65 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e12 | 3.80 | COLLISION | B | - | collision_sensor | peak_impulse=9797.50 |
| B:e13 | 3.80 | TURN_LEFT_END | B | - | ego |  |
| B:e14 | 3.80 | CLOSING_START | B | track_002 | radar |  |
| B:e15 | 3.85 | BRAKE_START | B | - | controls |  |
| B:e16 | 4.00 | MOVING_END | B | - | ego |  |
| B:e17 | 4.00 | STOP_START | B | - | ego |  |
| B:e18 | 4.15 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e19 | 4.15 | CLOSING_END | B | track_001 | radar |  |
| B:e20 | 4.65 | EGO_PATH_EXIT | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e20
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e06
    B:e04 --SAME_TRACK--> B:e11
    B:e08 --SAME_TRACK--> B:e14
    B:e04 --SAME_TRACK--> B:e18
    B:e04 --SAME_TRACK--> B:e19
    B:e04 --SAME_TRACK--> B:e20
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.75 | B:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.70 |
| 2.05 | B:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known | 2.00 |
| 2.10 | B:e04 TRACK_APPEARED_LEFT track_001<br>B:e05 CLOSING_START track_001<br>B:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>sign-0: STOP sign known | 2.00 |
| 2.25 | B:e07 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.20 |
| 2.90 | B:e08 TRACK_APPEARED_RIGHT track_002 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.80 |
| 2.95 | B:e09 BRAKE_START | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>sign-0: STOP sign known | 2.90 |
| 3.50 | B:e10 BRAKE_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>sign-0: STOP sign known | 3.40 |
| 3.65 | B:e11 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>sign-0: STOP sign known | 3.60 |
| 3.80 | B:e12 COLLISION<br>B:e13 TURN_LEFT_END<br>B:e14 CLOSING_START track_002 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>sign-0: STOP sign known | 3.70 |
| 3.85 | B:e15 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known | 3.80 |
| 4.00 | B:e16 MOVING_END<br>B:e17 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known | 3.90 |
| 4.15 | B:e18 CRITICAL_TTC_END track_001<br>B:e19 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known | 4.10 |
| 4.65 | B:e20 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>sign-0: STOP sign known | 4.60 |

## States still active when observation ended

- CLOSING of track_002, since B:e14 (t = 3.80 s)
- BRAKE, since B:e15 (t = 3.85 s)
- STOP, since B:e17 (t = 4.00 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.10, COLLISION 3.80 (+1.70 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.55 s)

## Sign detection windows

- STOP sign sign-0: detected 1.75 s -> 2.05 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.10 | 13.95 | 237 | 28.2 m / -55 deg | 2.37 m (4.15) | 14.8 m / +67 deg | 10.5 m/s |
| track_002 | 2.90 | 13.95 | 108 | 53.4 m / +92 deg | 34.98 m (13.95) | 35.0 m / +85 deg | 2.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.75 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 2.05 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.10 s: B's radar started tracking track_001, which appeared on its left.
- t = 2.10 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.10 s: B's time-to-contact with track_001 became critical (already the case when first observed).
- t = 2.25 s: B started turning left.
- t = 2.90 s: B's radar started tracking track_002, which appeared on its right.
- t = 2.95 s: B started braking.
- t = 3.50 s: B released the brake.
- t = 3.65 s: B observed track_001 enter its forward path corridor.
- t = 3.80 s: B's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: B stopped turning left.
- t = 3.80 s: B observed track_002 start closing in.
- t = 3.85 s: B started braking.
- t = 4.00 s: B stopped moving.
- t = 4.00 s: B came to a stop.
- t = 4.15 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.15 s: B observed track_001 stop closing in.
- t = 4.65 s: B observed track_001 leave its forward path corridor.
