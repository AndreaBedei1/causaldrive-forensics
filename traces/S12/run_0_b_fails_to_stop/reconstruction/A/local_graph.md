# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 391.65678068995476 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 26; edges: 51 (PRECEDES 46, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.65 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.25 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e05 | 2.65 | HARD_BRAKE_START | A | - | controls |  |
| A:e06 | 3.40 | MOVING_END | A | - | ego |  |
| A:e07 | 3.40 | STOP_START | A | - | ego |  |
| A:e08 | 6.75 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e09 | 6.75 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e10 | 7.75 | HARD_BRAKE_END | A | - | controls |  |
| A:e11 | 7.75 | BRAKE_END | A | - | controls |  |
| A:e12 | 7.75 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e13 | 8.10 | STOP_END | A | - | ego |  |
| A:e14 | 8.10 | MOVING_START | A | - | ego |  |
| A:e15 | 8.30 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e16 | 8.50 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e17 | 9.10 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e18 | 9.65 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e19 | 9.65 | TRACK_LOST | A | track_001 | radar |  |
| A:e20 | 9.70 | COLLISION | A | - | collision_sensor | peak_impulse=7339.57 |
| A:e21 | 9.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e22 | 9.75 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e23 | 9.75 | BRAKE_START | A | - | controls |  |
| A:e24 | 9.75 | HARD_BRAKE_START | A | - | controls |  |
| A:e25 | 10.20 | MOVING_END | A | - | ego |  |
| A:e26 | 10.20 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e20 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e08 --SAME_TRACK--> A:e09
    A:e08 --SAME_TRACK--> A:e15
    A:e08 --SAME_TRACK--> A:e16
    A:e08 --SAME_TRACK--> A:e18
    A:e08 --SAME_TRACK--> A:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.65 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.25 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign VISIBLE, known, relevant to the path | 2.20 |
| 2.65 | A:e04 BRAKE_START<br>A:e05 HARD_BRAKE_START | ego: MOVING<br>sign-0: STOP sign not visible, known, relevant to the path | 2.60 |
| 3.40 | A:e06 MOVING_END<br>A:e07 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign not visible, known, relevant to the path | 3.30 |
| 6.75 | A:e08 TRACK_APPEARED track_001<br>A:e09 CLOSING_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>sign-0: STOP sign not visible, known, relevant to the path | 6.70 |
| 7.75 | A:e10 HARD_BRAKE_END<br>A:e11 BRAKE_END<br>A:e12 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 7.70 |
| 8.10 | A:e13 STOP_END<br>A:e14 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 8.00 |
| 8.30 | A:e15 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign not visible, known, relevant to the path | 8.20 |
| 8.50 | A:e16 CRITICAL_TTC_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT<br>sign-0: STOP sign not visible, known, relevant to the path | 8.40 |
| 9.10 | A:e17 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>sign-0: STOP sign not visible, known, relevant to the path | 9.00 |
| 9.65 | A:e18 EGO_PATH_ENTRY track_001<br>A:e19 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>sign-0: STOP sign not visible, known, relevant to the path | 9.60 |
| 9.70 | A:e20 COLLISION<br>A:e21 STRONG_THROTTLE_START | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path | 9.60 |
| 9.75 | A:e22 STRONG_THROTTLE_END<br>A:e23 BRAKE_START<br>A:e24 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path | 9.70 |
| 10.20 | A:e25 MOVING_END<br>A:e26 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known, relevant to the path | 10.10 |

## States still active when observation ended

- CLOSING of track_001, since A:e09 (t = 6.75 s); the track was lost at 9.65 s
- PREDICTED_PATH_CONFLICT of track_001, since A:e15 (t = 8.30 s); the track was lost at 9.65 s
- CRITICAL_TTC of track_001, since A:e16 (t = 8.50 s); the track was lost at 9.65 s
- EGO_PATH of track_001, since A:e18 (t = 9.65 s); the track was lost at 9.65 s
- BRAKE, since A:e23 (t = 9.75 s)
- HARD_BRAKE, since A:e24 (t = 9.75 s)
- STOP, since A:e26 (t = 10.20 s)

## Tracks lost

- track_001 at 9.65 s (A:e19): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 6.75 | 9.65 | 56 | 19.1 m / -60 deg | 1.44 m (9.65) | 1.4 m / -62 deg | 6.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.65 s: A's camera established a STOP sign detection (sign-0).
- t = 2.25 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.65 s: A started braking.
- t = 2.65 s: A started braking hard.
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 6.75 s: A's radar started tracking track_001.
- t = 6.75 s: A observed track_001 start closing in (already the case when first observed).
- t = 7.75 s: A stopped braking hard.
- t = 7.75 s: A released the brake.
- t = 7.75 s: A started applying strong throttle.
- t = 8.10 s: A left its stop.
- t = 8.10 s: A started moving.
- t = 8.30 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 8.50 s: A's time-to-contact with track_001 became critical.
- t = 9.10 s: A stopped applying strong throttle.
- t = 9.65 s: A observed track_001 enter its forward path corridor.
- t = 9.65 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 9.70 s: A's collision sensor recorded a contact (peak impulse 7340 N*s).
- t = 9.70 s: A started applying strong throttle.
- t = 9.75 s: A stopped applying strong throttle.
- t = 9.75 s: A started braking.
- t = 9.75 s: A started braking hard.
- t = 10.20 s: A stopped moving.
- t = 10.20 s: A came to a stop.
