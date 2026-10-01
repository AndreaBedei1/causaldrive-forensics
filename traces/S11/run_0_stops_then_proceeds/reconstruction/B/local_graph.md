# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 330.7529085315764 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 135 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.35 s)
- Anonymous radar tracks: 5 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 37; edges: 76 (PRECEDES 59, SAME_TRACK 17)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e05 | 2.40 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e06 | 2.55 | BRAKE_START | B | - | controls |  |
| B:e07 | 2.55 | HARD_BRAKE_START | B | - | controls |  |
| B:e08 | 3.25 | MOVING_END | B | - | ego |  |
| B:e09 | 3.25 | STOP_START | B | - | ego |  |
| B:e10 | 3.50 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e11 | 3.50 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e12 | 4.40 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e13 | 5.75 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e14 | 5.80 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e15 | 6.10 | CLOSING_END | B | track_001 | radar |  |
| B:e16 | 6.20 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e17 | 6.75 | HARD_BRAKE_END | B | - | controls |  |
| B:e18 | 6.75 | BRAKE_END | B | - | controls |  |
| B:e19 | 6.75 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e20 | 7.20 | STOP_END | B | - | ego |  |
| B:e21 | 7.20 | MOVING_START | B | - | ego |  |
| B:e22 | 7.30 | TRACK_LOST | B | track_001 | radar |  |
| B:e23 | 8.40 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e24 | 8.40 | TRACK_APPEARED_LEFT | B | track_003 | radar |  |
| B:e25 | 8.40 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e26 | 8.40 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e27 | 8.40 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e28 | 8.40 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e29 | 8.40 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e30 | 8.45 | TRACK_APPEARED_RIGHT | B | track_005 | radar |  |
| B:e31 | 8.45 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e32 | 8.65 | TRACK_LOST | B | track_005 | radar |  |
| B:e33 | 9.60 | EGO_PATH_ENTRY | B | track_004 | radar |  |
| B:e34 | 9.70 | EGO_PATH_ENTRY | B | track_003 | radar |  |
| B:e35 | 9.85 | EGO_PATH_EXIT | B | track_004 | radar |  |
| B:e36 | 9.90 | EGO_PATH_EXIT | B | track_003 | radar |  |
| B:e37 | 9.90 | TRACK_LOST | B | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e25
    B:e22 --PRECEDES--> B:e26
    B:e22 --PRECEDES--> B:e27
    B:e22 --PRECEDES--> B:e28
    B:e22 --PRECEDES--> B:e29
    B:e23 --PRECEDES--> B:e30
    B:e23 --PRECEDES--> B:e31
    B:e24 --PRECEDES--> B:e30
    B:e24 --PRECEDES--> B:e31
    B:e25 --PRECEDES--> B:e30
    B:e25 --PRECEDES--> B:e31
    B:e26 --PRECEDES--> B:e30
    B:e26 --PRECEDES--> B:e31
    B:e27 --PRECEDES--> B:e30
    B:e27 --PRECEDES--> B:e31
    B:e28 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e35 --PRECEDES--> B:e36
    B:e35 --PRECEDES--> B:e37
    B:e10 --SAME_TRACK--> B:e11
    B:e10 --SAME_TRACK--> B:e12
    B:e10 --SAME_TRACK--> B:e13
    B:e10 --SAME_TRACK--> B:e14
    B:e10 --SAME_TRACK--> B:e15
    B:e10 --SAME_TRACK--> B:e16
    B:e10 --SAME_TRACK--> B:e22
    B:e26 --SAME_TRACK--> B:e27
    B:e24 --SAME_TRACK--> B:e28
    B:e25 --SAME_TRACK--> B:e29
    B:e30 --SAME_TRACK--> B:e31
    B:e30 --SAME_TRACK--> B:e32
    B:e25 --SAME_TRACK--> B:e33
    B:e24 --SAME_TRACK--> B:e34
    B:e25 --SAME_TRACK--> B:e35
    B:e24 --SAME_TRACK--> B:e36
    B:e26 --SAME_TRACK--> B:e37
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 2.10 | B:e04 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 2.00 |
| 2.40 | B:e05 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>sign-1: STOP sign known | 2.30 |
| 2.55 | B:e06 BRAKE_START<br>B:e07 HARD_BRAKE_START | ego: MOVING<br>sign-1: STOP sign known | 2.50 |
| 3.25 | B:e08 MOVING_END<br>B:e09 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign known | 3.20 |
| 3.50 | B:e10 TRACK_APPEARED_LEFT track_001<br>B:e11 CLOSING_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>sign-1: STOP sign known | 3.40 |
| 4.40 | B:e12 CRITICAL_TTC_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known | 4.30 |
| 5.75 | B:e13 CRITICAL_TTC_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known | 5.70 |
| 5.80 | B:e14 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known | 5.70 |
| 6.10 | B:e15 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-1: STOP sign known | 6.00 |
| 6.20 | B:e16 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>sign-1: STOP sign known | 6.10 |
| 6.75 | B:e17 HARD_BRAKE_END<br>B:e18 BRAKE_END<br>B:e19 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-1: STOP sign known | 6.70 |
| 7.20 | B:e20 STOP_END<br>B:e21 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known | 7.10 |
| 7.30 | B:e22 TRACK_LOST track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known | 7.20 |
| 8.40 | B:e23 STRONG_THROTTLE_END<br>B:e24 TRACK_APPEARED_LEFT track_003<br>B:e25 TRACK_APPEARED_LEFT track_004<br>B:e26 TRACK_APPEARED_RIGHT track_002<br>B:e27 CLOSING_START track_002<br>B:e28 CLOSING_START track_003<br>B:e29 CLOSING_START track_004 | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 8.30 |
| 8.45 | B:e30 TRACK_APPEARED_RIGHT track_005<br>B:e31 CLOSING_START track_005 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 8.40 |
| 8.65 | B:e32 TRACK_LOST track_005 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 8.60 |
| 9.60 | B:e33 EGO_PATH_ENTRY track_004 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known | 9.50 |
| 9.70 | B:e34 EGO_PATH_ENTRY track_003 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known | 9.60 |
| 9.85 | B:e35 EGO_PATH_EXIT track_004 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING, IN_EGO_PATH<br>track_004: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known | 9.80 |
| 9.90 | B:e36 EGO_PATH_EXIT track_003<br>B:e37 TRACK_LOST track_002 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING, IN_EGO_PATH<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001, track_005<br>sign-1: STOP sign known | 9.80 |

## States still active when observation ended

- MOVING, since B:e21 (t = 7.20 s)
- CLOSING of track_002, since B:e27 (t = 8.40 s); the track was lost at 9.90 s
- CLOSING of track_003, since B:e28 (t = 8.40 s)
- CLOSING of track_004, since B:e29 (t = 8.40 s)
- CLOSING of track_005, since B:e31 (t = 8.45 s); the track was lost at 8.65 s

## Tracks lost

- track_005 at 8.65 s (B:e32): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 9.90 s (B:e37): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001

## Sign detection windows

- STOP sign sign-1: detected 2.10 s -> 2.40 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.50 | 7.30 | 74 | 24.6 m / -60 deg | 6.90 m (6.10) | 12.6 m / +60 deg | 9.2 m/s |
| track_002 | 8.40 | 9.90 | 31 | 16.0 m / +52 deg | 10.93 m (9.90) | 10.9 m / +42 deg | 20.2 m/s |
| track_003 | 8.40 | 13.35 | 100 | 55.5 m / -48 deg | 12.89 m (13.35) | 12.9 m / +50 deg | 1.1 m/s |
| track_004 | 8.40 | 13.35 | 97 | 52.0 m / -47 deg | 11.38 m (13.35) | 11.4 m / +62 deg | 1.2 m/s |
| track_005 | 8.45 | 8.65 | 5 | 20.2 m / +40 deg | 19.63 m (8.65) | 19.6 m / +55 deg | 1.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 2.10 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 2.40 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.55 s: B started braking.
- t = 2.55 s: B started braking hard.
- t = 3.25 s: B stopped moving.
- t = 3.25 s: B came to a stop.
- t = 3.50 s: B's radar started tracking track_001, which appeared on its left.
- t = 3.50 s: B observed track_001 start closing in (already the case when first observed).
- t = 4.40 s: B's time-to-contact with track_001 became critical.
- t = 5.75 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.80 s: B observed track_001 enter its forward path corridor.
- t = 6.10 s: B observed track_001 stop closing in.
- t = 6.20 s: B observed track_001 leave its forward path corridor.
- t = 6.75 s: B stopped braking hard.
- t = 6.75 s: B released the brake.
- t = 6.75 s: B started applying strong throttle.
- t = 7.20 s: B left its stop.
- t = 7.20 s: B started moving.
- t = 7.30 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.40 s: B stopped applying strong throttle.
- t = 8.40 s: B's radar started tracking track_003, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_004, which appeared on its left.
- t = 8.40 s: B's radar started tracking track_002, which appeared on its right.
- t = 8.40 s: B observed track_002 start closing in (already the case when first observed).
- t = 8.40 s: B observed track_003 start closing in (already the case when first observed).
- t = 8.40 s: B observed track_004 start closing in (already the case when first observed).
- t = 8.45 s: B's radar started tracking track_005, which appeared on its right.
- t = 8.45 s: B observed track_005 start closing in (already the case when first observed).
- t = 8.65 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 9.60 s: B observed track_004 enter its forward path corridor.
- t = 9.70 s: B observed track_003 enter its forward path corridor.
- t = 9.85 s: B observed track_004 leave its forward path corridor.
- t = 9.90 s: B observed track_003 leave its forward path corridor.
- t = 9.90 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
