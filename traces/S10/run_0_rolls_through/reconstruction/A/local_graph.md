# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 245.13907996192575 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 37 (PRECEDES 32, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.85 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e03 | 1.95 | BRAKE_START | A | - | controls |  |
| A:e04 | 1.95 | HARD_BRAKE_START | A | - | controls |  |
| A:e05 | 2.15 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e06 | 2.20 | HARD_BRAKE_END | A | - | controls |  |
| A:e07 | 3.80 | BRAKE_END | A | - | controls |  |
| A:e08 | 3.80 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e09 | 3.80 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e10 | 3.80 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e11 | 4.70 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e12 | 5.20 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e13 | 5.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e14 | 5.25 | COLLISION | A | - | collision_sensor | peak_impulse=12489.77 |
| A:e15 | 5.25 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e16 | 5.30 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e17 | 5.30 | BRAKE_START | A | - | controls |  |
| A:e18 | 5.30 | HARD_BRAKE_START | A | - | controls |  |
| A:e19 | 5.40 | MOVING_END | A | - | ego |  |
| A:e20 | 5.40 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e20
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e08 --SAME_TRACK--> A:e09
    A:e08 --SAME_TRACK--> A:e10
    A:e08 --SAME_TRACK--> A:e11
    A:e08 --SAME_TRACK--> A:e12
    A:e08 --SAME_TRACK--> A:e13
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 1.85 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.80 |
| 1.95 | A:e03 BRAKE_START<br>A:e04 HARD_BRAKE_START | ego: MOVING<br>sign-0: STOP sign VISIBLE, known | 1.90 |
| 2.15 | A:e05 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign VISIBLE, known | 2.10 |
| 2.20 | A:e06 HARD_BRAKE_END | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign not visible, known | 2.10 |
| 3.80 | A:e07 BRAKE_END<br>A:e08 TRACK_APPEARED track_001<br>A:e09 CLOSING_START track_001<br>A:e10 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE<br>sign-0: STOP sign not visible, known | 3.70 |
| 4.70 | A:e11 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known | 4.60 |
| 5.20 | A:e12 EGO_PATH_ENTRY track_001<br>A:e13 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>sign-0: STOP sign not visible, known | 5.10 |
| 5.25 | A:e14 COLLISION<br>A:e15 STRONG_THROTTLE_START | ego: MOVING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 5.20 |
| 5.30 | A:e16 STRONG_THROTTLE_END<br>A:e17 BRAKE_START<br>A:e18 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 5.20 |
| 5.40 | A:e19 MOVING_END<br>A:e20 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 5.30 |

## States still active when observation ended

- CLOSING of track_001, since A:e09 (t = 3.80 s); the track was lost at 5.20 s
- CRITICAL_TTC of track_001, since A:e10 (t = 3.80 s); the track was lost at 5.20 s
- PREDICTED_PATH_CONFLICT of track_001, since A:e11 (t = 4.70 s); the track was lost at 5.20 s
- EGO_PATH of track_001, since A:e12 (t = 5.20 s); the track was lost at 5.20 s
- BRAKE, since A:e17 (t = 5.30 s)
- HARD_BRAKE, since A:e18 (t = 5.30 s)
- STOP, since A:e20 (t = 5.40 s)

## Tracks lost

- track_001 at 5.20 s (A:e13): CLOSING, CRITICAL_TTC, PREDICTED_PATH_CONFLICT were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 1.85 s -> 2.15 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.80 | 5.20 | 29 | 21.4 m / -60 deg | 1.64 m (5.20) | 1.6 m / -57 deg | 10.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.85 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: A started braking.
- t = 1.95 s: A started braking hard.
- t = 2.15 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.20 s: A stopped braking hard.
- t = 3.80 s: A released the brake.
- t = 3.80 s: A's radar started tracking track_001.
- t = 3.80 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.80 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 4.70 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 5.20 s: A observed track_001 enter its forward path corridor.
- t = 5.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 5.25 s: A's collision sensor recorded a contact (peak impulse 12490 N*s).
- t = 5.25 s: A started applying strong throttle.
- t = 5.30 s: A stopped applying strong throttle.
- t = 5.30 s: A started braking.
- t = 5.30 s: A started braking hard.
- t = 5.40 s: A stopped moving.
- t = 5.40 s: A came to a stop.
