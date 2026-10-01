# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 225.90415861457586 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 22; edges: 51 (PRECEDES 41, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.15 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 2.15 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e04 | 2.15 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 2.20 | TRACK_APPEARED | B | track_002 | radar |  |
| B:e06 | 2.20 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e07 | 2.35 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e08 | 2.40 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e09 | 2.85 | PREDICTED_PATH_CONFLICT_START | B | track_001 | radar |  |
| B:e10 | 4.05 | TRACK_LOST | B | track_002 | radar |  |
| B:e11 | 4.10 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e12 | 4.25 | COLLISION | B | - | collision_sensor | peak_impulse=12077.22 |
| B:e13 | 4.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e14 | 4.30 | PREDICTED_PATH_CONFLICT_END | B | track_001 | radar |  |
| B:e15 | 4.30 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e16 | 4.30 | CLOSING_END | B | track_001 | radar |  |
| B:e17 | 4.30 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e18 | 4.30 | BRAKE_START | B | - | controls |  |
| B:e19 | 4.30 | HARD_BRAKE_START | B | - | controls |  |
| B:e20 | 4.55 | MOVING_END | B | - | ego |  |
| B:e21 | 4.55 | STOP_START | B | - | ego |  |
| B:e22 | 4.70 | EGO_PATH_EXIT | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e16
    B:e12 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e18
    B:e12 --PRECEDES--> B:e19
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e13 --PRECEDES--> B:e18
    B:e13 --PRECEDES--> B:e19
    B:e14 --PRECEDES--> B:e20
    B:e14 --PRECEDES--> B:e21
    B:e15 --PRECEDES--> B:e20
    B:e15 --PRECEDES--> B:e21
    B:e16 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e22
    B:e03 --SAME_TRACK--> B:e04
    B:e05 --SAME_TRACK--> B:e06
    B:e03 --SAME_TRACK--> B:e07
    B:e03 --SAME_TRACK--> B:e09
    B:e05 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e11
    B:e03 --SAME_TRACK--> B:e14
    B:e03 --SAME_TRACK--> B:e15
    B:e03 --SAME_TRACK--> B:e16
    B:e03 --SAME_TRACK--> B:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.15 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.10 |
| 2.15 | B:e03 TRACK_APPEARED track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, STRONG_THROTTLE | 2.10 |
| 2.20 | B:e05 TRACK_APPEARED track_002<br>B:e06 CLOSING_START track_002 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING | 2.10 |
| 2.35 | B:e07 CRITICAL_TTC_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING | 2.30 |
| 2.40 | B:e08 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING | 2.30 |
| 2.85 | B:e09 PREDICTED_PATH_CONFLICT_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING | 2.80 |
| 4.05 | B:e10 TRACK_LOST track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>track_002: VISIBLE, CLOSING | 4.00 |
| 4.10 | B:e11 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 4.00 |
| 4.25 | B:e12 COLLISION<br>B:e13 STRONG_THROTTLE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 4.20 |
| 4.30 | B:e14 PREDICTED_PATH_CONFLICT_END track_001<br>B:e15 CRITICAL_TTC_END track_001<br>B:e16 CLOSING_END track_001<br>B:e17 STRONG_THROTTLE_END<br>B:e18 BRAKE_START<br>B:e19 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH, PATH_CONFLICT<br>lost (states UNKNOWN): track_002 | 4.20 |
| 4.55 | B:e20 MOVING_END<br>B:e21 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002 | 4.50 |
| 4.70 | B:e22 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_002 | 4.60 |

## States still active when observation ended

- CLOSING of track_002, since B:e06 (t = 2.20 s); the track was lost at 4.05 s
- BRAKE, since B:e18 (t = 4.30 s)
- HARD_BRAKE, since B:e19 (t = 4.30 s)
- STOP, since B:e21 (t = 4.55 s)

## Tracks lost

- track_002 at 4.05 s (B:e10): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.15 | 15.15 | 260 | 32.7 m / -38 deg | 0.87 m (4.30) | 2.9 m / +48 deg | 11.0 m/s |
| track_002 | 2.20 | 4.05 | 38 | 33.8 m / +28 deg | 14.00 m (4.05) | 14.0 m / +60 deg | 5.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.15 s: B started applying strong throttle.
- t = 2.15 s: B's radar started tracking track_001.
- t = 2.15 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.20 s: B's radar started tracking track_002.
- t = 2.20 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.35 s: B's time-to-contact with track_001 became critical.
- t = 2.40 s: B stopped applying strong throttle.
- t = 2.85 s: B predicted a path conflict with track_001 (close approach ahead if both keep their motion).
- t = 4.05 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 4.10 s: B observed track_001 enter its forward path corridor.
- t = 4.25 s: B's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.25 s: B started applying strong throttle.
- t = 4.30 s: B stopped predicting a path conflict with track_001.
- t = 4.30 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.30 s: B observed track_001 stop closing in.
- t = 4.30 s: B stopped applying strong throttle.
- t = 4.30 s: B started braking.
- t = 4.30 s: B started braking hard.
- t = 4.55 s: B stopped moving.
- t = 4.55 s: B came to a stop.
- t = 4.70 s: B observed track_001 leave its forward path corridor.
