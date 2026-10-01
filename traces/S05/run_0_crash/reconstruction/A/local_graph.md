# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 116.97939620912075 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 146 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 41 (PRECEDES 32, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.25 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 1.25 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.50 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e05 | 1.65 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e06 | 3.50 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e07 | 3.70 | COLLISION | A | - | collision_sensor | peak_impulse=6116.26 |
| A:e08 | 3.70 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e09 | 3.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e10 | 3.70 | CLOSING_END | A | track_001 | radar |  |
| A:e11 | 3.70 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e12 | 3.75 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e13 | 3.75 | BRAKE_START | A | - | controls |  |
| A:e14 | 3.75 | HARD_BRAKE_START | A | - | controls |  |
| A:e15 | 3.90 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e16 | 3.95 | TRACK_LOST | A | track_001 | radar |  |
| A:e17 | 4.55 | MOVING_END | A | - | ego |  |
| A:e18 | 4.55 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e10
    A:e06 --PRECEDES--> A:e11
    A:e07 --PRECEDES--> A:e12
    A:e07 --PRECEDES--> A:e13
    A:e07 --PRECEDES--> A:e14
    A:e08 --PRECEDES--> A:e12
    A:e08 --PRECEDES--> A:e13
    A:e08 --PRECEDES--> A:e14
    A:e09 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e13
    A:e09 --PRECEDES--> A:e14
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e15
    A:e02 --SAME_TRACK--> A:e16
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 1.20 |
| 1.50 | A:e04 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING | 1.40 |
| 1.65 | A:e05 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT | 1.60 |
| 3.50 | A:e06 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT | 3.40 |
| 3.70 | A:e07 COLLISION<br>A:e08 PREDICTED_PATH_CONFLICT_END track_001<br>A:e09 CRITICAL_TTC_END track_001<br>A:e10 CLOSING_END track_001<br>A:e11 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT | 3.60 |
| 3.75 | A:e12 STRONG_THROTTLE_END<br>A:e13 BRAKE_START<br>A:e14 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, IN_EGO_PATH | 3.70 |
| 3.90 | A:e15 EGO_PATH_EXIT track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH | 3.80 |
| 3.95 | A:e16 TRACK_LOST track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE | 3.90 |
| 4.55 | A:e17 MOVING_END<br>A:e18 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 | 4.50 |

## States still active when observation ended

- BRAKE, since A:e13 (t = 3.75 s)
- HARD_BRAKE, since A:e14 (t = 3.75 s)
- STOP, since A:e18 (t = 4.55 s)

## Tracks lost

- lost with no state active: track_001

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.25 | 3.95 | 55 | 36.7 m / +43 deg | 0.85 m (3.70) | 2.4 m / -107 deg | 11.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.25 s: A's radar started tracking track_001.
- t = 1.25 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.50 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 1.65 s: A's time-to-contact with track_001 became critical.
- t = 3.50 s: A observed track_001 enter its forward path corridor.
- t = 3.70 s: A's collision sensor recorded a contact (peak impulse 6116 N*s).
- t = 3.70 s: A stopped predicting a path conflict with track_001.
- t = 3.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.70 s: A observed track_001 stop closing in.
- t = 3.70 s: A started applying strong throttle.
- t = 3.75 s: A stopped applying strong throttle.
- t = 3.75 s: A started braking.
- t = 3.75 s: A started braking hard.
- t = 3.90 s: A observed track_001 leave its forward path corridor.
- t = 3.95 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 4.55 s: A stopped moving.
- t = 4.55 s: A came to a stop.
