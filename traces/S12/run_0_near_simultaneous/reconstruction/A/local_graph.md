# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 411.87760305032134 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 8 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 48; edges: 129 (PRECEDES 113, SAME_TRACK 16)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.65 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 2.25 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.50 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e05 | 2.50 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 2.65 | BRAKE_START | A | - | controls |  |
| A:e07 | 2.65 | HARD_BRAKE_START | A | - | controls |  |
| A:e08 | 2.80 | TRACK_LOST | A | track_001 | radar |  |
| A:e09 | 3.40 | MOVING_END | A | - | ego |  |
| A:e10 | 3.40 | STOP_START | A | - | ego |  |
| A:e11 | 6.95 | HARD_BRAKE_END | A | - | controls |  |
| A:e12 | 6.95 | BRAKE_END | A | - | controls |  |
| A:e13 | 6.95 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e14 | 7.30 | STOP_END | A | - | ego |  |
| A:e15 | 7.30 | MOVING_START | A | - | ego |  |
| A:e16 | 8.30 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e17 | 9.40 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e18 | 9.40 | TRACK_APPEARED_LEFT | A | track_003 | radar |  |
| A:e19 | 9.40 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e20 | 9.40 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e21 | 9.50 | COLLISION | A | - | collision_sensor | peak_impulse=4032.49 |
| A:e22 | 9.50 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e23 | 9.50 | TRACK_APPEARED_RIGHT | A | track_004 | radar |  |
| A:e24 | 9.55 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e25 | 9.55 | BRAKE_START | A | - | controls |  |
| A:e26 | 9.55 | HARD_BRAKE_START | A | - | controls |  |
| A:e27 | 9.55 | TRACK_APPEARED_LEFT | A | track_006 | radar |  |
| A:e28 | 9.55 | TRACK_APPEARED_LEFT | A | track_007 | radar |  |
| A:e29 | 9.55 | TRACK_APPEARED_LEFT | A | track_008 | radar |  |
| A:e30 | 9.55 | TRACK_APPEARED_RIGHT | A | track_005 | radar |  |
| A:e31 | 9.55 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e32 | 9.55 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e33 | 9.55 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e34 | 9.55 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e35 | 9.60 | CLOSING_START | A | track_004 | radar |  |
| A:e36 | 9.80 | TRACK_LOST | A | track_002 | radar |  |
| A:e37 | 10.00 | CLOSING_END | A | track_005 | radar |  |
| A:e38 | 10.00 | MOVING_END | A | - | ego |  |
| A:e39 | 10.00 | STOP_START | A | - | ego |  |
| A:e40 | 10.05 | CLOSING_END | A | track_003 | radar |  |
| A:e41 | 10.05 | CLOSING_END | A | track_004 | radar |  |
| A:e42 | 10.05 | CLOSING_END | A | track_006 | radar |  |
| A:e43 | 10.05 | CLOSING_END | A | track_007 | radar |  |
| A:e44 | 10.05 | CLOSING_END | A | track_008 | radar |  |
| A:e45 | 11.70 | STOP_SIGN_DETECTED_START | A | sign-1 | camera | relevant_to_ego_path=False |
| A:e46 | 11.80 | STOP_SIGN_DETECTED_END | A | sign-1 | camera |  |
| A:e47 | 13.95 | STOP_SIGN_DETECTED_START | A | sign-1 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| A:e48 | 13.95 | STOP_SIGN_DETECTED_END | A | sign-1 | camera | sign_track=sign-4 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

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
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e20
    A:e17 --PRECEDES--> A:e21
    A:e17 --PRECEDES--> A:e22
    A:e17 --PRECEDES--> A:e23
    A:e18 --PRECEDES--> A:e21
    A:e18 --PRECEDES--> A:e22
    A:e18 --PRECEDES--> A:e23
    A:e19 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e22
    A:e19 --PRECEDES--> A:e23
    A:e20 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e21 --PRECEDES--> A:e26
    A:e21 --PRECEDES--> A:e27
    A:e21 --PRECEDES--> A:e28
    A:e21 --PRECEDES--> A:e29
    A:e21 --PRECEDES--> A:e30
    A:e21 --PRECEDES--> A:e31
    A:e21 --PRECEDES--> A:e32
    A:e21 --PRECEDES--> A:e33
    A:e21 --PRECEDES--> A:e34
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e26
    A:e22 --PRECEDES--> A:e27
    A:e22 --PRECEDES--> A:e28
    A:e22 --PRECEDES--> A:e29
    A:e22 --PRECEDES--> A:e30
    A:e22 --PRECEDES--> A:e31
    A:e22 --PRECEDES--> A:e32
    A:e22 --PRECEDES--> A:e33
    A:e22 --PRECEDES--> A:e34
    A:e23 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e23 --PRECEDES--> A:e28
    A:e23 --PRECEDES--> A:e29
    A:e23 --PRECEDES--> A:e30
    A:e23 --PRECEDES--> A:e31
    A:e23 --PRECEDES--> A:e32
    A:e23 --PRECEDES--> A:e33
    A:e23 --PRECEDES--> A:e34
    A:e24 --PRECEDES--> A:e35
    A:e25 --PRECEDES--> A:e35
    A:e26 --PRECEDES--> A:e35
    A:e27 --PRECEDES--> A:e35
    A:e28 --PRECEDES--> A:e35
    A:e29 --PRECEDES--> A:e35
    A:e30 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e35
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e36 --PRECEDES--> A:e39
    A:e37 --PRECEDES--> A:e40
    A:e37 --PRECEDES--> A:e41
    A:e37 --PRECEDES--> A:e42
    A:e37 --PRECEDES--> A:e43
    A:e37 --PRECEDES--> A:e44
    A:e38 --PRECEDES--> A:e40
    A:e38 --PRECEDES--> A:e41
    A:e38 --PRECEDES--> A:e42
    A:e38 --PRECEDES--> A:e43
    A:e38 --PRECEDES--> A:e44
    A:e39 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e39 --PRECEDES--> A:e42
    A:e39 --PRECEDES--> A:e43
    A:e39 --PRECEDES--> A:e44
    A:e40 --PRECEDES--> A:e45
    A:e41 --PRECEDES--> A:e45
    A:e42 --PRECEDES--> A:e45
    A:e43 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e45
    A:e45 --PRECEDES--> A:e46
    A:e46 --PRECEDES--> A:e47
    A:e46 --PRECEDES--> A:e48
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e08
    A:e17 --SAME_TRACK--> A:e19
    A:e18 --SAME_TRACK--> A:e20
    A:e30 --SAME_TRACK--> A:e31
    A:e27 --SAME_TRACK--> A:e32
    A:e28 --SAME_TRACK--> A:e33
    A:e29 --SAME_TRACK--> A:e34
    A:e23 --SAME_TRACK--> A:e35
    A:e17 --SAME_TRACK--> A:e36
    A:e30 --SAME_TRACK--> A:e37
    A:e18 --SAME_TRACK--> A:e40
    A:e23 --SAME_TRACK--> A:e41
    A:e27 --SAME_TRACK--> A:e42
    A:e28 --SAME_TRACK--> A:e43
    A:e29 --SAME_TRACK--> A:e44
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.65 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 0.60 |
| 2.25 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.20 |
| 2.50 | A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 CLOSING_START track_001 | ego: MOVING<br>sign-0: STOP sign known, relevant to the path | 2.40 |
| 2.65 | A:e06 BRAKE_START<br>A:e07 HARD_BRAKE_START | ego: MOVING<br>track_001: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>sign-0: STOP sign known, relevant to the path | 2.60 |
| 2.80 | A:e08 TRACK_LOST track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>sign-0: STOP sign known, relevant to the path | 2.70 |
| 3.40 | A:e09 MOVING_END<br>A:e10 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 3.30 |
| 6.95 | A:e11 HARD_BRAKE_END<br>A:e12 BRAKE_END<br>A:e13 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 6.90 |
| 7.30 | A:e14 STOP_END<br>A:e15 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 7.20 |
| 8.30 | A:e16 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 8.20 |
| 9.40 | A:e17 TRACK_APPEARED_LEFT track_002<br>A:e18 TRACK_APPEARED_LEFT track_003<br>A:e19 CLOSING_START track_002<br>A:e20 CLOSING_START track_003 | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.30 |
| 9.50 | A:e21 COLLISION<br>A:e22 STRONG_THROTTLE_START<br>A:e23 TRACK_APPEARED_RIGHT track_004 | ego: MOVING<br>track_002: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.40 |
| 9.55 | A:e24 STRONG_THROTTLE_END<br>A:e25 BRAKE_START<br>A:e26 HARD_BRAKE_START<br>A:e27 TRACK_APPEARED_LEFT track_006<br>A:e28 TRACK_APPEARED_LEFT track_007<br>A:e29 TRACK_APPEARED_LEFT track_008<br>A:e30 TRACK_APPEARED_RIGHT track_005<br>A:e31 CLOSING_START track_005<br>A:e32 CLOSING_START track_006<br>A:e33 CLOSING_START track_007<br>A:e34 CLOSING_START track_008 | ego: MOVING, STRONG_THROTTLE<br>track_002: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.50 |
| 9.60 | A:e35 CLOSING_START track_004 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: no active state<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.50 |
| 9.80 | A:e36 TRACK_LOST track_002 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path | 9.70 |
| 10.00 | A:e37 CLOSING_END track_005<br>A:e38 MOVING_END<br>A:e39 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path | 9.90 |
| 10.05 | A:e40 CLOSING_END track_003<br>A:e41 CLOSING_END track_004<br>A:e42 CLOSING_END track_006<br>A:e43 CLOSING_END track_007<br>A:e44 CLOSING_END track_008 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: no active state<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path | 10.00 |
| 11.70 | A:e45 STOP_SIGN_DETECTED_START sign-1 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path | 11.60 |
| 11.80 | A:e46 STOP_SIGN_DETECTED_END sign-1 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known | 11.70 |
| 13.95 | A:e47 STOP_SIGN_DETECTED_START sign-1<br>A:e48 STOP_SIGN_DETECTED_END sign-1 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track lost, states UNKNOWN: track_001, track_002<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known | 13.90 |

## States still active when observation ended

- CLOSING of track_001, since A:e05 (t = 2.50 s); the track was lost at 2.80 s
- CLOSING of track_002, since A:e19 (t = 9.40 s); the track was lost at 9.80 s
- BRAKE, since A:e25 (t = 9.55 s)
- HARD_BRAKE, since A:e26 (t = 9.55 s)
- STOP, since A:e39 (t = 10.00 s)

## Tracks lost

- track_001 at 2.80 s (A:e08): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 9.80 s (A:e36): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-0: detected 0.65 s -> 2.25 s; relevant to the path: True; STOP_START inside: none
- STOP sign sign-1: detected 11.70 s -> 11.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-1: detected 13.95 s -> 13.95 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.50 | 2.80 | 5 | 28.3 m / -58 deg | 24.79 m (2.80) | 24.8 m / -59 deg | 8.5 m/s |
| track_002 | 9.40 | 9.80 | 6 | 90.6 m / -57 deg | 87.24 m (9.80) | 87.2 m / -22 deg | 16.5 m/s |
| track_003 | 9.40 | 14.95 | 98 | 88.1 m / -59 deg | 84.06 m (11.55) | 84.4 m / -18 deg | 5.1 m/s |
| track_004 | 9.50 | 14.95 | 110 | 11.5 m / +30 deg | 11.29 m (10.10) | 11.3 m / +48 deg | 9.9 m/s |
| track_005 | 9.55 | 14.95 | 109 | 14.0 m / +23 deg | 13.36 m (10.00) | 13.8 m / +31 deg | 7.6 m/s |
| track_006 | 9.55 | 14.95 | 104 | 35.9 m / -54 deg | 33.62 m (14.95) | 33.6 m / -34 deg | 3.0 m/s |
| track_007 | 9.55 | 14.95 | 109 | 28.0 m / -58 deg | 25.20 m (14.95) | 25.2 m / -40 deg | 3.4 m/s |
| track_008 | 9.55 | 14.95 | 97 | 40.7 m / -53 deg | 38.33 m (12.40) | 38.5 m / -32 deg | 3.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.65 s: A's camera established a STOP sign detection (sign-0).
- t = 2.25 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.50 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.50 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.65 s: A started braking.
- t = 2.65 s: A started braking hard.
- t = 2.80 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 3.40 s: A stopped moving.
- t = 3.40 s: A came to a stop.
- t = 6.95 s: A stopped braking hard.
- t = 6.95 s: A released the brake.
- t = 6.95 s: A started applying strong throttle.
- t = 7.30 s: A left its stop.
- t = 7.30 s: A started moving.
- t = 8.30 s: A stopped applying strong throttle.
- t = 9.40 s: A's radar started tracking track_002, which appeared on its left.
- t = 9.40 s: A's radar started tracking track_003, which appeared on its left.
- t = 9.40 s: A observed track_002 start closing in (already the case when first observed).
- t = 9.40 s: A observed track_003 start closing in (already the case when first observed).
- t = 9.50 s: A's collision sensor recorded a contact (peak impulse 4032 N*s).
- t = 9.50 s: A started applying strong throttle.
- t = 9.50 s: A's radar started tracking track_004, which appeared on its right.
- t = 9.55 s: A stopped applying strong throttle.
- t = 9.55 s: A started braking.
- t = 9.55 s: A started braking hard.
- t = 9.55 s: A's radar started tracking track_006, which appeared on its left.
- t = 9.55 s: A's radar started tracking track_007, which appeared on its left.
- t = 9.55 s: A's radar started tracking track_008, which appeared on its left.
- t = 9.55 s: A's radar started tracking track_005, which appeared on its right.
- t = 9.55 s: A observed track_005 start closing in (already the case when first observed).
- t = 9.55 s: A observed track_006 start closing in (already the case when first observed).
- t = 9.55 s: A observed track_007 start closing in (already the case when first observed).
- t = 9.55 s: A observed track_008 start closing in (already the case when first observed).
- t = 9.60 s: A observed track_004 start closing in.
- t = 9.80 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 10.00 s: A observed track_005 stop closing in.
- t = 10.00 s: A stopped moving.
- t = 10.00 s: A came to a stop.
- t = 10.05 s: A observed track_003 stop closing in.
- t = 10.05 s: A observed track_004 stop closing in.
- t = 10.05 s: A observed track_006 stop closing in.
- t = 10.05 s: A observed track_007 stop closing in.
- t = 10.05 s: A observed track_008 stop closing in.
- t = 11.70 s: A's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 11.80 s: A's camera stopped detecting STOP sign sign-1.
- t = 13.95 s: A's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- t = 13.95 s: A's camera stopped detecting STOP sign sign-1.
