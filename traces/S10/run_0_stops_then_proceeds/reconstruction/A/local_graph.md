# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 278.8234966881573 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 135 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.35 s)
- Anonymous radar tracks: 8 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 41; edges: 87 (PRECEDES 67, SAME_TRACK 20)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.75 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=False |
| A:e03 | 2.15 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e04 | 2.55 | BRAKE_START | A | - | controls |  |
| A:e05 | 2.55 | HARD_BRAKE_START | A | - | controls |  |
| A:e06 | 3.35 | MOVING_END | A | - | ego |  |
| A:e07 | 3.35 | STOP_START | A | - | ego |  |
| A:e08 | 3.70 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e09 | 3.70 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e10 | 4.25 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e11 | 5.80 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 5.95 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e13 | 6.10 | CLOSING_END | A | track_001 | radar |  |
| A:e14 | 6.25 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e15 | 6.75 | HARD_BRAKE_END | A | - | controls |  |
| A:e16 | 6.75 | BRAKE_END | A | - | controls |  |
| A:e17 | 6.75 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e18 | 7.00 | TRACK_LOST | A | track_001 | radar |  |
| A:e19 | 7.10 | STOP_END | A | - | ego |  |
| A:e20 | 7.10 | MOVING_START | A | - | ego |  |
| A:e21 | 8.20 | TRACK_APPEARED_RIGHT | A | track_002 | radar |  |
| A:e22 | 8.20 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e23 | 8.25 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e24 | 8.25 | TRACK_APPEARED_RIGHT | A | track_003 | radar |  |
| A:e25 | 8.25 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e26 | 8.30 | TRACK_APPEARED_LEFT | A | track_004 | radar |  |
| A:e27 | 8.30 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e28 | 8.35 | TRACK_APPEARED_LEFT | A | track_005 | radar |  |
| A:e29 | 8.35 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e30 | 8.40 | TRACK_APPEARED_LEFT | A | track_006 | radar |  |
| A:e31 | 8.40 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e32 | 8.45 | TRACK_APPEARED_LEFT | A | track_007 | radar |  |
| A:e33 | 8.45 | TRACK_APPEARED_LEFT | A | track_008 | radar |  |
| A:e34 | 8.45 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e35 | 8.45 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e36 | 9.00 | CRITICAL_TTC_START | A | track_003 | radar |  |
| A:e37 | 9.25 | TRACK_LOST | A | track_003 | radar |  |
| A:e38 | 9.50 | TRACK_LOST | A | track_002 | radar |  |
| A:e39 | 10.75 | TRACK_LOST | A | track_006 | radar |  |
| A:e40 | 11.60 | TRACK_LOST | A | track_007 | radar |  |
| A:e41 | 12.45 | TRACK_LOST | A | track_005 | radar |  |

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
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e22
    A:e20 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e23 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e28
    A:e26 --PRECEDES--> A:e29
    A:e27 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e28 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e36
    A:e36 --PRECEDES--> A:e37
    A:e37 --PRECEDES--> A:e38
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e40 --PRECEDES--> A:e41
    A:e08 --SAME_TRACK--> A:e09
    A:e08 --SAME_TRACK--> A:e10
    A:e08 --SAME_TRACK--> A:e11
    A:e08 --SAME_TRACK--> A:e12
    A:e08 --SAME_TRACK--> A:e13
    A:e08 --SAME_TRACK--> A:e14
    A:e08 --SAME_TRACK--> A:e18
    A:e21 --SAME_TRACK--> A:e22
    A:e24 --SAME_TRACK--> A:e25
    A:e26 --SAME_TRACK--> A:e27
    A:e28 --SAME_TRACK--> A:e29
    A:e30 --SAME_TRACK--> A:e31
    A:e32 --SAME_TRACK--> A:e34
    A:e33 --SAME_TRACK--> A:e35
    A:e24 --SAME_TRACK--> A:e36
    A:e24 --SAME_TRACK--> A:e37
    A:e21 --SAME_TRACK--> A:e38
    A:e30 --SAME_TRACK--> A:e39
    A:e32 --SAME_TRACK--> A:e40
    A:e28 --SAME_TRACK--> A:e41
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 1.75 | A:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.70 |
| 2.15 | A:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known | 2.10 |
| 2.55 | A:e04 BRAKE_START<br>A:e05 HARD_BRAKE_START | ego: MOVING<br>sign-0: STOP sign known | 2.50 |
| 3.35 | A:e06 MOVING_END<br>A:e07 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-0: STOP sign known | 3.30 |
| 3.70 | A:e08 TRACK_APPEARED_LEFT track_001<br>A:e09 CLOSING_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>sign-0: STOP sign known | 3.60 |
| 4.25 | A:e10 CRITICAL_TTC_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known | 4.20 |
| 5.80 | A:e11 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 5.70 |
| 5.95 | A:e12 CRITICAL_TTC_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known | 5.90 |
| 6.10 | A:e13 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known | 6.00 |
| 6.25 | A:e14 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known | 6.20 |
| 6.75 | A:e15 HARD_BRAKE_END<br>A:e16 BRAKE_END<br>A:e17 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-0: STOP sign known | 6.70 |
| 7.00 | A:e18 TRACK_LOST track_001 | ego: STOP, STRONG_THROTTLE<br>track_001: no active state<br>sign-0: STOP sign known | 6.90 |
| 7.10 | A:e19 STOP_END<br>A:e20 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 7.00 |
| 8.20 | A:e21 TRACK_APPEARED_RIGHT track_002<br>A:e22 CLOSING_START track_002 | ego: MOVING, STRONG_THROTTLE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.10 |
| 8.25 | A:e23 STRONG_THROTTLE_END<br>A:e24 TRACK_APPEARED_RIGHT track_003<br>A:e25 CLOSING_START track_003 | ego: MOVING, STRONG_THROTTLE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.20 |
| 8.30 | A:e26 TRACK_APPEARED_LEFT track_004<br>A:e27 CLOSING_START track_004 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.20 |
| 8.35 | A:e28 TRACK_APPEARED_LEFT track_005<br>A:e29 CLOSING_START track_005 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.30 |
| 8.40 | A:e30 TRACK_APPEARED_LEFT track_006<br>A:e31 CLOSING_START track_006 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.30 |
| 8.45 | A:e32 TRACK_APPEARED_LEFT track_007<br>A:e33 TRACK_APPEARED_LEFT track_008<br>A:e34 CLOSING_START track_007<br>A:e35 CLOSING_START track_008 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.40 |
| 9.00 | A:e36 CRITICAL_TTC_START track_003 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 8.90 |
| 9.25 | A:e37 TRACK_LOST track_003 | ego: MOVING<br>track_002: CLOSING<br>track_003: CLOSING, CRITICAL_TTC<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 9.20 |
| 9.50 | A:e38 TRACK_LOST track_002 | ego: MOVING<br>track_002: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_003<br>sign-0: STOP sign known | 9.40 |
| 10.75 | A:e39 TRACK_LOST track_006 | ego: MOVING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003<br>sign-0: STOP sign known | 10.70 |
| 11.60 | A:e40 TRACK_LOST track_007 | ego: MOVING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_006<br>sign-0: STOP sign known | 11.50 |
| 12.45 | A:e41 TRACK_LOST track_005 | ego: MOVING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_006, track_007<br>sign-0: STOP sign known | 12.40 |

## States still active when observation ended

- MOVING, since A:e20 (t = 7.10 s)
- CLOSING of track_002, since A:e22 (t = 8.20 s); the track was lost at 9.50 s
- CLOSING of track_003, since A:e25 (t = 8.25 s); the track was lost at 9.25 s
- CLOSING of track_004, since A:e27 (t = 8.30 s)
- CLOSING of track_005, since A:e29 (t = 8.35 s); the track was lost at 12.45 s
- CLOSING of track_006, since A:e31 (t = 8.40 s); the track was lost at 10.75 s
- CLOSING of track_007, since A:e34 (t = 8.45 s); the track was lost at 11.60 s
- CLOSING of track_008, since A:e35 (t = 8.45 s)
- CRITICAL_TTC of track_003, since A:e36 (t = 9.00 s); the track was lost at 9.25 s

## Tracks lost

- track_003 at 9.25 s (A:e37): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 9.50 s (A:e38): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 10.75 s (A:e39): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 11.60 s (A:e40): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 12.45 s (A:e41): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001

## Sign detection windows

- STOP sign sign-0: detected 1.75 s -> 2.15 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.70 | 7.00 | 64 | 23.3 m / -60 deg | 5.33 m (6.10) | 9.4 m / +61 deg | 9.6 m/s |
| track_002 | 8.20 | 9.50 | 27 | 14.9 m / +54 deg | 10.74 m (9.50) | 10.7 m / +42 deg | 21.7 m/s |
| track_003 | 8.25 | 9.25 | 20 | 14.8 m / +43 deg | 10.83 m (9.25) | 10.8 m / +35 deg | 19.2 m/s |
| track_004 | 8.30 | 13.35 | 80 | 73.8 m / -57 deg | 28.97 m (13.35) | 29.0 m / -23 deg | 2.7 m/s |
| track_005 | 8.35 | 12.45 | 80 | 39.9 m / -59 deg | 10.88 m (12.45) | 10.9 m / -60 deg | 5.8 m/s |
| track_006 | 8.40 | 10.75 | 48 | 27.1 m / -61 deg | 11.11 m (10.75) | 11.1 m / -58 deg | 5.2 m/s |
| track_007 | 8.45 | 11.60 | 61 | 31.9 m / -59 deg | 10.25 m (11.60) | 10.2 m / -57 deg | 6.2 m/s |
| track_008 | 8.45 | 13.35 | 85 | 43.2 m / -56 deg | 8.97 m (13.35) | 9.0 m / -63 deg | 6.6 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.75 s: A's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 2.15 s: A's camera stopped detecting STOP sign sign-0.
- t = 2.55 s: A started braking.
- t = 2.55 s: A started braking hard.
- t = 3.35 s: A stopped moving.
- t = 3.35 s: A came to a stop.
- t = 3.70 s: A's radar started tracking track_001, which appeared on its left.
- t = 3.70 s: A observed track_001 start closing in (already the case when first observed).
- t = 4.25 s: A's time-to-contact with track_001 became critical.
- t = 5.80 s: A observed track_001 enter its forward path corridor.
- t = 5.95 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.10 s: A observed track_001 stop closing in.
- t = 6.25 s: A observed track_001 leave its forward path corridor.
- t = 6.75 s: A stopped braking hard.
- t = 6.75 s: A released the brake.
- t = 6.75 s: A started applying strong throttle.
- t = 7.00 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 7.10 s: A left its stop.
- t = 7.10 s: A started moving.
- t = 8.20 s: A's radar started tracking track_002, which appeared on its right.
- t = 8.20 s: A observed track_002 start closing in (already the case when first observed).
- t = 8.25 s: A stopped applying strong throttle.
- t = 8.25 s: A's radar started tracking track_003, which appeared on its right.
- t = 8.25 s: A observed track_003 start closing in (already the case when first observed).
- t = 8.30 s: A's radar started tracking track_004, which appeared on its left.
- t = 8.30 s: A observed track_004 start closing in (already the case when first observed).
- t = 8.35 s: A's radar started tracking track_005, which appeared on its left.
- t = 8.35 s: A observed track_005 start closing in (already the case when first observed).
- t = 8.40 s: A's radar started tracking track_006, which appeared on its left.
- t = 8.40 s: A observed track_006 start closing in (already the case when first observed).
- t = 8.45 s: A's radar started tracking track_007, which appeared on its left.
- t = 8.45 s: A's radar started tracking track_008, which appeared on its left.
- t = 8.45 s: A observed track_007 start closing in (already the case when first observed).
- t = 8.45 s: A observed track_008 start closing in (already the case when first observed).
- t = 9.00 s: A's time-to-contact with track_003 became critical.
- t = 9.25 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 9.50 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 10.75 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 11.60 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 12.45 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
