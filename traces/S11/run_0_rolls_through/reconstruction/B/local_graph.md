# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 296.6198318079114 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 28; edges: 49 (PRECEDES 40, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 1.95 | BRAKE_START | B | - | controls |  |
| B:e05 | 1.95 | HARD_BRAKE_START | B | - | controls |  |
| B:e06 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e07 | 2.20 | HARD_BRAKE_END | B | - | controls |  |
| B:e08 | 2.45 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e09 | 2.65 | BRAKE_END | B | - | controls |  |
| B:e10 | 3.00 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e11 | 3.25 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e12 | 3.95 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e13 | 3.95 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e14 | 3.95 | CRITICAL_TTC_START | B | track_001 | radar | active_at_first_observation=True |
| B:e15 | 4.40 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e16 | 5.30 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e17 | 5.50 | COLLISION | B | - | collision_sensor | peak_impulse=8859.58 |
| B:e18 | 5.50 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e19 | 5.55 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e20 | 5.55 | BRAKE_START | B | - | controls |  |
| B:e21 | 5.55 | HARD_BRAKE_START | B | - | controls |  |
| B:e22 | 5.70 | MOVING_END | B | - | ego |  |
| B:e23 | 5.70 | STOP_START | B | - | ego |  |
| B:e24 | 5.75 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e25 | 5.75 | CLOSING_END | B | track_001 | radar |  |
| B:e26 | 5.80 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |
| B:e27 | 6.15 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e28 | 6.75 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |

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
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e23
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e26
    B:e26 --PRECEDES--> B:e27
    B:e27 --PRECEDES--> B:e28
    B:e12 --SAME_TRACK--> B:e13
    B:e12 --SAME_TRACK--> B:e14
    B:e12 --SAME_TRACK--> B:e15
    B:e12 --SAME_TRACK--> B:e16
    B:e12 --SAME_TRACK--> B:e24
    B:e12 --SAME_TRACK--> B:e25
    B:e12 --SAME_TRACK--> B:e26
    B:e12 --SAME_TRACK--> B:e27
    B:e12 --SAME_TRACK--> B:e28
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 1.95 | B:e04 BRAKE_START<br>B:e05 HARD_BRAKE_START | ego: MOVING | 1.90 |
| 2.10 | B:e06 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING, BRAKE, HARD_BRAKE | 2.00 |
| 2.20 | B:e07 HARD_BRAKE_END | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign VISIBLE, known | 2.10 |
| 2.45 | B:e08 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING, BRAKE<br>sign-1: STOP sign VISIBLE, known | 2.40 |
| 2.65 | B:e09 BRAKE_END | ego: MOVING, BRAKE<br>sign-1: STOP sign not visible, known | 2.60 |
| 3.00 | B:e10 STRONG_THROTTLE_START | ego: MOVING<br>sign-1: STOP sign not visible, known | 2.90 |
| 3.25 | B:e11 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>sign-1: STOP sign not visible, known | 3.20 |
| 3.95 | B:e12 TRACK_APPEARED track_001<br>B:e13 CLOSING_START track_001<br>B:e14 CRITICAL_TTC_START track_001 | ego: MOVING<br>sign-1: STOP sign not visible, known | 3.90 |
| 4.40 | B:e15 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-1: STOP sign not visible, known | 4.30 |
| 5.30 | B:e16 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 5.20 |
| 5.50 | B:e17 COLLISION<br>B:e18 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 5.40 |
| 5.55 | B:e19 STRONG_THROTTLE_END<br>B:e20 BRAKE_START<br>B:e21 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 5.50 |
| 5.70 | B:e22 MOVING_END<br>B:e23 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 5.60 |
| 5.75 | B:e24 CRITICAL_TTC_END track_001<br>B:e25 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 5.70 |
| 5.80 | B:e26 PREDICTED_PATH_CONFLICT_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 5.70 |
| 6.15 | B:e27 PREDICTED_PATH_CONFLICT_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>sign-1: STOP sign not visible, known | 6.10 |
| 6.75 | B:e28 PREDICTED_PATH_CONFLICT_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>sign-1: STOP sign not visible, known | 6.70 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e16 (t = 5.30 s)
- BRAKE, since B:e20 (t = 5.55 s)
- HARD_BRAKE, since B:e21 (t = 5.55 s)
- STOP, since B:e23 (t = 5.70 s)

## Tracks lost

- no track was lost

## Sign detection windows

- STOP sign sign-1: detected 2.10 s -> 2.45 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.95 | 15.95 | 241 | 20.6 m / -60 deg | 0.24 m (6.80) | 0.3 m / -0 deg | 9.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 1.95 s: B started braking.
- t = 1.95 s: B started braking hard.
- t = 2.10 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 2.20 s: B stopped braking hard.
- t = 2.45 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.65 s: B released the brake.
- t = 3.00 s: B started applying strong throttle.
- t = 3.25 s: B stopped applying strong throttle.
- t = 3.95 s: B's radar started tracking track_001.
- t = 3.95 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.95 s: B's time-to-contact with track_001 became critical (already the case when first observed).
- t = 4.40 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 5.30 s: B observed track_001 enter its forward path corridor.
- t = 5.50 s: B's collision sensor recorded a contact (peak impulse 8860 N*s).
- t = 5.50 s: B started applying strong throttle.
- t = 5.55 s: B stopped applying strong throttle.
- t = 5.55 s: B started braking.
- t = 5.55 s: B started braking hard.
- t = 5.70 s: B stopped moving.
- t = 5.70 s: B came to a stop.
- t = 5.75 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.75 s: B observed track_001 stop closing in.
- t = 5.80 s: B stopped predicting a path conflict with track_001.
- t = 6.15 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 6.75 s: B stopped predicting a path conflict with track_001.
