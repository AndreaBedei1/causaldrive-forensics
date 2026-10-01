# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 23.34804853051901 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 22; edges: 54 (PRECEDES 41, SAME_TRACK 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 0.00 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 0.20 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e06 | 0.20 | TRACK_APPEARED | A | track_003 | radar |  |
| A:e07 | 0.20 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e08 | 0.20 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e09 | 0.65 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e10 | 1.45 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e11 | 1.80 | COLLISION | A | - | collision_sensor | peak_impulse=1247.19 |
| A:e12 | 1.85 | BRAKE_START | A | - | controls |  |
| A:e13 | 1.85 | HARD_BRAKE_START | A | - | controls |  |
| A:e14 | 1.90 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |
| A:e15 | 1.90 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e16 | 1.90 | CLOSING_END | A | track_001 | radar |  |
| A:e17 | 2.35 | PREDICTED_PATH_CONFLICT_START | A | track_001 | radar |  |
| A:e18 | 2.50 | CLOSING_END | A | track_002 | radar |  |
| A:e19 | 2.50 | CLOSING_END | A | track_003 | radar |  |
| A:e20 | 2.50 | MOVING_END | A | - | ego |  |
| A:e21 | 2.50 | STOP_START | A | - | ego |  |
| A:e22 | 2.95 | PREDICTED_PATH_CONFLICT_END | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e05
    A:e01 --PRECEDES--> A:e06
    A:e01 --PRECEDES--> A:e07
    A:e01 --PRECEDES--> A:e08
    A:e02 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e07
    A:e02 --PRECEDES--> A:e08
    A:e03 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e07
    A:e03 --PRECEDES--> A:e08
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e07
    A:e04 --PRECEDES--> A:e08
    A:e05 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e17 --PRECEDES--> A:e21
    A:e18 --PRECEDES--> A:e22
    A:e19 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e22
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e05 --SAME_TRACK--> A:e07
    A:e06 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e14
    A:e02 --SAME_TRACK--> A:e15
    A:e02 --SAME_TRACK--> A:e16
    A:e02 --SAME_TRACK--> A:e17
    A:e05 --SAME_TRACK--> A:e18
    A:e06 --SAME_TRACK--> A:e19
    A:e02 --SAME_TRACK--> A:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED track_001<br>A:e03 CLOSING_START track_001<br>A:e04 CRITICAL_TTC_START track_001 | ego: not yet observed | - |
| 0.20 | A:e05 TRACK_APPEARED track_002<br>A:e06 TRACK_APPEARED track_003<br>A:e07 CLOSING_START track_002<br>A:e08 CLOSING_START track_003 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC | 0.10 |
| 0.65 | A:e09 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING | 0.60 |
| 1.45 | A:e10 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING | 1.40 |
| 1.80 | A:e11 COLLISION | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING | 1.70 |
| 1.85 | A:e12 BRAKE_START<br>A:e13 HARD_BRAKE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING | 1.80 |
| 1.90 | A:e14 PREDICTED_PATH_CONFLICT_END track_001<br>A:e15 CRITICAL_TTC_END track_001<br>A:e16 CLOSING_END track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING | 1.80 |
| 2.35 | A:e17 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING | 2.30 |
| 2.50 | A:e18 CLOSING_END track_002<br>A:e19 CLOSING_END track_003<br>A:e20 MOVING_END<br>A:e21 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING<br>track_003: VISIBLE, CLOSING | 2.40 |
| 2.95 | A:e22 PREDICTED_PATH_CONFLICT_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH, PATH_CONFLICT<br>track_002: VISIBLE<br>track_003: VISIBLE | 2.90 |

## States still active when observation ended

- EGO_PATH of track_001, since A:e10 (t = 1.45 s)
- BRAKE, since A:e12 (t = 1.85 s)
- HARD_BRAKE, since A:e13 (t = 1.85 s)
- STOP, since A:e21 (t = 2.50 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.95 | 291 | 7.8 m / +39 deg | 0.98 m (1.85) | 1.1 m / +51 deg | 8.7 m/s |
| track_002 | 0.20 | 14.95 | 296 | 47.4 m / -57 deg | 31.98 m (8.00) | 32.2 m / -14 deg | 1.9 m/s |
| track_003 | 0.20 | 14.95 | 294 | 49.9 m / -53 deg | 34.13 m (7.25) | 34.5 m / -8 deg | 1.1 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 0.20 s: A's radar started tracking track_002.
- t = 0.20 s: A's radar started tracking track_003.
- t = 0.20 s: A observed track_002 start closing in (already the case when first observed).
- t = 0.20 s: A observed track_003 start closing in (already the case when first observed).
- t = 0.65 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 1.45 s: A observed track_001 enter its forward path corridor.
- t = 1.80 s: A's collision sensor recorded a contact (peak impulse 1247 N*s).
- t = 1.85 s: A started braking.
- t = 1.85 s: A started braking hard.
- t = 1.90 s: A stopped predicting a path conflict with track_001.
- t = 1.90 s: A's time-to-contact with track_001 stopped being critical.
- t = 1.90 s: A observed track_001 stop closing in.
- t = 2.35 s: A predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 2.50 s: A observed track_002 stop closing in.
- t = 2.50 s: A observed track_003 stop closing in.
- t = 2.50 s: A stopped moving.
- t = 2.50 s: A came to a stop.
- t = 2.95 s: A stopped predicting a path conflict with track_001.
