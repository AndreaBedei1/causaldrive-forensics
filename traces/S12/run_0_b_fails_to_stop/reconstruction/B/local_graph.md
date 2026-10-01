# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 391.65678068995476 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 34; edges: 77 (PRECEDES 64, SAME_TRACK 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 1.95 | BRAKE_START | B | - | controls |  |
| B:e05 | 1.95 | HARD_BRAKE_START | B | - | controls |  |
| B:e06 | 2.30 | HARD_BRAKE_END | B | - | controls |  |
| B:e07 | 2.65 | BRAKE_END | B | - | controls |  |
| B:e08 | 3.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e09 | 3.30 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e10 | 3.50 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e11 | 5.30 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e12 | 8.15 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e13 | 8.15 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e14 | 8.15 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar | active_at_first_observation=True |
| B:e15 | 8.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e16 | 9.60 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e17 | 9.70 | COLLISION | B | - | collision_sensor | peak_impulse=7339.57 |
| B:e18 | 9.70 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e19 | 9.70 | TRACK_APPEARED | B | track_002 | radar |  |
| B:e20 | 9.70 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e21 | 9.75 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e22 | 9.75 | BRAKE_START | B | - | controls |  |
| B:e23 | 9.75 | HARD_BRAKE_START | B | - | controls |  |
| B:e24 | 9.75 | TRACK_APPEARED | B | track_003 | radar |  |
| B:e25 | 9.75 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e26 | 10.05 | MOVING_END | B | - | ego |  |
| B:e27 | 10.05 | STOP_START | B | - | ego |  |
| B:e28 | 10.10 | CLOSING_END | B | track_002 | radar |  |
| B:e29 | 10.10 | CLOSING_END | B | track_003 | radar |  |
| B:e30 | 10.15 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e31 | 10.15 | CLOSING_END | B | track_001 | radar |  |
| B:e32 | 10.25 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |
| B:e33 | 10.65 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e34 | 10.95 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
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
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e22
    B:e17 --PRECEDES--> B:e23
    B:e17 --PRECEDES--> B:e24
    B:e17 --PRECEDES--> B:e25
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e23
    B:e18 --PRECEDES--> B:e24
    B:e18 --PRECEDES--> B:e25
    B:e19 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e23
    B:e19 --PRECEDES--> B:e24
    B:e19 --PRECEDES--> B:e25
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e20 --PRECEDES--> B:e24
    B:e20 --PRECEDES--> B:e25
    B:e21 --PRECEDES--> B:e26
    B:e21 --PRECEDES--> B:e27
    B:e22 --PRECEDES--> B:e26
    B:e22 --PRECEDES--> B:e27
    B:e23 --PRECEDES--> B:e26
    B:e23 --PRECEDES--> B:e27
    B:e24 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e12 --SAME_TRACK--> B:e13
    B:e12 --SAME_TRACK--> B:e14
    B:e12 --SAME_TRACK--> B:e15
    B:e12 --SAME_TRACK--> B:e16
    B:e19 --SAME_TRACK--> B:e20
    B:e24 --SAME_TRACK--> B:e25
    B:e19 --SAME_TRACK--> B:e28
    B:e24 --SAME_TRACK--> B:e29
    B:e12 --SAME_TRACK--> B:e30
    B:e12 --SAME_TRACK--> B:e31
    B:e12 --SAME_TRACK--> B:e32
    B:e12 --SAME_TRACK--> B:e33
    B:e12 --SAME_TRACK--> B:e34
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 1.95 | B:e04 BRAKE_START<br>B:e05 HARD_BRAKE_START | ego: MOVING | 1.90 |
| 2.30 | B:e06 HARD_BRAKE_END | ego: MOVING, BRAKE, HARD_BRAKE | 2.20 |
| 2.65 | B:e07 BRAKE_END | ego: MOVING, BRAKE | 2.60 |
| 3.25 | B:e08 STRONG_THROTTLE_START | ego: MOVING | 3.20 |
| 3.30 | B:e09 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 3.20 |
| 3.50 | B:e10 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 3.40 |
| 5.30 | B:e11 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>sign-1: STOP sign VISIBLE, known | 5.20 |
| 8.15 | B:e12 TRACK_APPEARED track_001<br>B:e13 CLOSING_START track_001<br>B:e14 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>sign-1: STOP sign not visible, known | 8.10 |
| 8.50 | B:e15 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 8.40 |
| 9.60 | B:e16 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 9.50 |
| 9.70 | B:e17 COLLISION<br>B:e18 STRONG_THROTTLE_START<br>B:e19 TRACK_APPEARED track_002<br>B:e20 CLOSING_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 9.60 |
| 9.75 | B:e21 STRONG_THROTTLE_END<br>B:e22 BRAKE_START<br>B:e23 HARD_BRAKE_START<br>B:e24 TRACK_APPEARED track_003<br>B:e25 CLOSING_START track_003 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known | 9.70 |
| 10.05 | B:e26 MOVING_END<br>B:e27 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known | 10.00 |
| 10.10 | B:e28 CLOSING_END track_002<br>B:e29 CLOSING_END track_003 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known | 10.00 |
| 10.15 | B:e30 CRITICAL_TTC_END track_001<br>B:e31 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE<br>track_003: VISIBLE<br>sign-1: STOP sign not visible, known | 10.10 |
| 10.25 | B:e32 PREDICTED_PATH_CONFLICT_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE<br>track_003: VISIBLE<br>sign-1: STOP sign not visible, known | 10.20 |
| 10.65 | B:e33 PREDICTED_PATH_CONFLICT_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>track_002: VISIBLE<br>track_003: VISIBLE<br>sign-1: STOP sign not visible, known | 10.60 |
| 10.95 | B:e34 PREDICTED_PATH_CONFLICT_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE<br>track_003: VISIBLE<br>sign-1: STOP sign not visible, known | 10.90 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e16 (t = 9.60 s)
- BRAKE, since B:e22 (t = 9.75 s)
- HARD_BRAKE, since B:e23 (t = 9.75 s)
- STOP, since B:e27 (t = 10.05 s)

## Tracks lost

- no track was lost

## Sign detection windows

- STOP sign sign-1: detected 3.50 s -> 5.30 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 8.15 | 15.95 | 157 | 13.3 m / +51 deg | 0.67 m (15.95) | 0.7 m / +40 deg | 8.4 m/s |
| track_002 | 9.70 | 15.95 | 126 | 19.0 m / -42 deg | 17.28 m (15.95) | 17.3 m / -36 deg | 3.5 m/s |
| track_003 | 9.75 | 15.95 | 125 | 16.1 m / -52 deg | 14.84 m (15.95) | 14.8 m / -48 deg | 3.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 1.95 s: B started braking.
- t = 1.95 s: B started braking hard.
- t = 2.30 s: B stopped braking hard.
- t = 2.65 s: B released the brake.
- t = 3.25 s: B started applying strong throttle.
- t = 3.30 s: B stopped applying strong throttle.
- t = 3.50 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 5.30 s: B's camera stopped detecting STOP sign sign-1.
- t = 8.15 s: B's radar started tracking track_001.
- t = 8.15 s: B observed track_001 start closing in (already the case when first observed).
- t = 8.15 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion) (already the case when first observed).
- t = 8.50 s: B's time-to-contact with track_001 became critical.
- t = 9.60 s: B observed track_001 enter its forward path corridor.
- t = 9.70 s: B's collision sensor recorded a contact (peak impulse 7340 N*s).
- t = 9.70 s: B started applying strong throttle.
- t = 9.70 s: B's radar started tracking track_002.
- t = 9.70 s: B observed track_002 start closing in (already the case when first observed).
- t = 9.75 s: B stopped applying strong throttle.
- t = 9.75 s: B started braking.
- t = 9.75 s: B started braking hard.
- t = 9.75 s: B's radar started tracking track_003.
- t = 9.75 s: B observed track_003 start closing in (already the case when first observed).
- t = 10.05 s: B stopped moving.
- t = 10.05 s: B came to a stop.
- t = 10.10 s: B observed track_002 stop closing in.
- t = 10.10 s: B observed track_003 stop closing in.
- t = 10.15 s: B's time-to-contact with track_001 stopped being critical.
- t = 10.15 s: B observed track_001 stop closing in.
- t = 10.25 s: B stopped predicting a path conflict with track_001.
- t = 10.65 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 10.95 s: B stopped predicting a path conflict with track_001.
