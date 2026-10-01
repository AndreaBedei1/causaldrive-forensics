# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 493.54037738218904 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 25; edges: 47 (PRECEDES 38, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.20 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.45 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e04 | 1.45 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 1.80 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e06 | 1.80 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e07 | 1.95 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e08 | 1.95 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e09 | 2.00 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e10 | 2.10 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e11 | 2.35 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e12 | 2.75 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e13 | 2.80 | TRACK_LOST | B | track_001 | radar |  |
| B:e14 | 2.95 | BRAKE_START | B | - | controls |  |
| B:e15 | 3.50 | BRAKE_END | B | - | controls |  |
| B:e16 | 3.60 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e17 | 3.80 | COLLISION | B | - | collision_sensor | peak_impulse=9797.50 |
| B:e18 | 3.80 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e19 | 3.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e20 | 3.85 | BRAKE_START | B | - | controls |  |
| B:e21 | 3.85 | HARD_BRAKE_START | B | - | controls |  |
| B:e22 | 4.00 | MOVING_END | B | - | ego |  |
| B:e23 | 4.00 | STOP_START | B | - | ego |  |
| B:e24 | 4.05 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e25 | 4.05 | CLOSING_END | B | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

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
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
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
    B:e03 --SAME_TRACK--> B:e04
    B:e07 --SAME_TRACK--> B:e08
    B:e07 --SAME_TRACK--> B:e09
    B:e03 --SAME_TRACK--> B:e11
    B:e03 --SAME_TRACK--> B:e12
    B:e03 --SAME_TRACK--> B:e13
    B:e07 --SAME_TRACK--> B:e16
    B:e07 --SAME_TRACK--> B:e24
    B:e07 --SAME_TRACK--> B:e25
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.20 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.10 |
| 1.45 | B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, STRONG_THROTTLE | 1.40 |
| 1.80 | B:e05 STRONG_THROTTLE_END<br>B:e06 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING | 1.70 |
| 1.95 | B:e07 TRACK_APPEARED_LEFT track_002<br>B:e08 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 1.90 |
| 2.00 | B:e09 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known | 1.90 |
| 2.10 | B:e10 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.00 |
| 2.35 | B:e11 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.30 |
| 2.75 | B:e12 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.70 |
| 2.80 | B:e13 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.70 |
| 2.95 | B:e14 BRAKE_START | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 2.90 |
| 3.50 | B:e15 BRAKE_END | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.40 |
| 3.60 | B:e16 EGO_PATH_ENTRY track_002 | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.50 |
| 3.80 | B:e17 COLLISION<br>B:e18 STRONG_THROTTLE_START | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.70 |
| 3.85 | B:e19 STRONG_THROTTLE_END<br>B:e20 BRAKE_START<br>B:e21 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.80 |
| 4.00 | B:e22 MOVING_END<br>B:e23 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.90 |
| 4.05 | B:e24 CRITICAL_TTC_END track_002<br>B:e25 CLOSING_END track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 4.00 |

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 1.45 s); the track was lost at 2.80 s
- EGO_PATH of track_002, since B:e16 (t = 3.60 s)
- BRAKE, since B:e20 (t = 3.85 s)
- HARD_BRAKE, since B:e21 (t = 3.85 s)
- STOP, since B:e23 (t = 4.00 s)

## Tracks lost

- track_001 at 2.80 s (B:e13): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.45 | 2.80 | 26 | 28.7 m / +37 deg | 16.09 m (2.80) | 16.1 m / +61 deg | 6.0 m/s |
| track_002 | 1.95 | 13.95 | 241 | 29.3 m / -57 deg | 0.16 m (4.05) | 2.4 m / +50 deg | 11.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.20 s: B started applying strong throttle.
- t = 1.45 s: B's radar started tracking track_001, which appeared on its right.
- t = 1.45 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.80 s: B stopped applying strong throttle.
- t = 1.80 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: B's radar started tracking track_002, which appeared on its left.
- t = 1.95 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.00 s: B's time-to-contact with track_002 became critical.
- t = 2.10 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.35 s: B's time-to-contact with track_001 became critical.
- t = 2.75 s: B's time-to-contact with track_001 stopped being critical.
- t = 2.80 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 2.95 s: B started braking.
- t = 3.50 s: B released the brake.
- t = 3.60 s: B observed track_002 enter its forward path corridor.
- t = 3.80 s: B's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: B started applying strong throttle.
- t = 3.85 s: B stopped applying strong throttle.
- t = 3.85 s: B started braking.
- t = 3.85 s: B started braking hard.
- t = 4.00 s: B stopped moving.
- t = 4.00 s: B came to a stop.
- t = 4.05 s: B's time-to-contact with track_002 stopped being critical.
- t = 4.05 s: B observed track_002 stop closing in.
