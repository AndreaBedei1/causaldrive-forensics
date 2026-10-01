# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 142.30000706017017 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 8 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 40; edges: 96 (PRECEDES 75, SAME_TRACK 21)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.45 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e03 | 1.45 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e04 | 1.50 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e05 | 1.95 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e06 | 1.95 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e07 | 2.10 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e08 | 2.15 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e09 | 2.25 | TURN_LEFT_START | B | - | ego |  |
| B:e10 | 2.95 | BRAKE_START | B | - | controls |  |
| B:e11 | 3.05 | TRACK_APPEARED_LEFT | B | track_003 | radar |  |
| B:e12 | 3.05 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e13 | 3.05 | TRACK_APPEARED_LEFT | B | track_005 | radar |  |
| B:e14 | 3.05 | TRACK_APPEARED_LEFT | B | track_006 | radar |  |
| B:e15 | 3.05 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e16 | 3.05 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e17 | 3.05 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e18 | 3.05 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e19 | 3.10 | TRACK_APPEARED_LEFT | B | track_007 | radar |  |
| B:e20 | 3.10 | CLOSING_START | B | track_007 | radar | active_at_first_observation=True |
| B:e21 | 3.15 | TRACK_LOST | B | track_001 | radar |  |
| B:e22 | 3.50 | BRAKE_END | B | - | controls |  |
| B:e23 | 3.70 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e24 | 3.75 | TRACK_LOST | B | track_003 | radar |  |
| B:e25 | 3.75 | TRACK_LOST | B | track_004 | radar |  |
| B:e26 | 3.75 | TRACK_LOST | B | track_005 | radar |  |
| B:e27 | 3.75 | TRACK_LOST | B | track_006 | radar |  |
| B:e28 | 3.75 | TRACK_LOST | B | track_007 | radar |  |
| B:e29 | 3.80 | COLLISION | B | - | collision_sensor | peak_impulse=9797.50 |
| B:e30 | 3.80 | TURN_LEFT_END | B | - | ego |  |
| B:e31 | 3.85 | BRAKE_START | B | - | controls |  |
| B:e32 | 3.85 | TRACK_APPEARED_RIGHT | B | track_008 | radar |  |
| B:e33 | 3.85 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e34 | 3.85 | CRITICAL_TTC_START | B | track_008 | radar | active_at_first_observation=True |
| B:e35 | 4.00 | MOVING_END | B | - | ego |  |
| B:e36 | 4.00 | STOP_START | B | - | ego |  |
| B:e37 | 4.10 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e38 | 4.15 | TRACK_LOST | B | track_008 | radar |  |
| B:e39 | 4.30 | CLOSING_END | B | track_002 | radar |  |
| B:e40 | 4.80 | EGO_PATH_EXIT | B | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e10 --PRECEDES--> B:e15
    B:e10 --PRECEDES--> B:e16
    B:e10 --PRECEDES--> B:e17
    B:e10 --PRECEDES--> B:e18
    B:e11 --PRECEDES--> B:e19
    B:e11 --PRECEDES--> B:e20
    B:e12 --PRECEDES--> B:e19
    B:e12 --PRECEDES--> B:e20
    B:e13 --PRECEDES--> B:e19
    B:e13 --PRECEDES--> B:e20
    B:e14 --PRECEDES--> B:e19
    B:e14 --PRECEDES--> B:e20
    B:e15 --PRECEDES--> B:e19
    B:e15 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e26
    B:e23 --PRECEDES--> B:e27
    B:e23 --PRECEDES--> B:e28
    B:e24 --PRECEDES--> B:e29
    B:e24 --PRECEDES--> B:e30
    B:e25 --PRECEDES--> B:e29
    B:e25 --PRECEDES--> B:e30
    B:e26 --PRECEDES--> B:e29
    B:e26 --PRECEDES--> B:e30
    B:e27 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e32
    B:e29 --PRECEDES--> B:e33
    B:e29 --PRECEDES--> B:e34
    B:e30 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e30 --PRECEDES--> B:e33
    B:e30 --PRECEDES--> B:e34
    B:e31 --PRECEDES--> B:e35
    B:e31 --PRECEDES--> B:e36
    B:e32 --PRECEDES--> B:e35
    B:e32 --PRECEDES--> B:e36
    B:e33 --PRECEDES--> B:e35
    B:e33 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e35
    B:e34 --PRECEDES--> B:e36
    B:e35 --PRECEDES--> B:e37
    B:e36 --PRECEDES--> B:e37
    B:e37 --PRECEDES--> B:e38
    B:e38 --PRECEDES--> B:e39
    B:e39 --PRECEDES--> B:e40
    B:e02 --SAME_TRACK--> B:e03
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e08
    B:e11 --SAME_TRACK--> B:e15
    B:e12 --SAME_TRACK--> B:e16
    B:e13 --SAME_TRACK--> B:e17
    B:e14 --SAME_TRACK--> B:e18
    B:e19 --SAME_TRACK--> B:e20
    B:e02 --SAME_TRACK--> B:e21
    B:e05 --SAME_TRACK--> B:e23
    B:e11 --SAME_TRACK--> B:e24
    B:e12 --SAME_TRACK--> B:e25
    B:e13 --SAME_TRACK--> B:e26
    B:e14 --SAME_TRACK--> B:e27
    B:e19 --SAME_TRACK--> B:e28
    B:e32 --SAME_TRACK--> B:e33
    B:e32 --SAME_TRACK--> B:e34
    B:e05 --SAME_TRACK--> B:e37
    B:e32 --SAME_TRACK--> B:e38
    B:e05 --SAME_TRACK--> B:e39
    B:e05 --SAME_TRACK--> B:e40
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.45 | B:e02 TRACK_APPEARED_RIGHT track_001<br>B:e03 CLOSING_START track_001 | ego: MOVING | 1.40 |
| 1.50 | B:e04 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING<br>track_001: CLOSING | 1.40 |
| 1.95 | B:e05 TRACK_APPEARED_LEFT track_002<br>B:e06 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 1.90 |
| 2.10 | B:e07 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known | 2.00 |
| 2.15 | B:e08 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known | 2.10 |
| 2.25 | B:e09 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.20 |
| 2.95 | B:e10 BRAKE_START | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.90 |
| 3.05 | B:e11 TRACK_APPEARED_LEFT track_003<br>B:e12 TRACK_APPEARED_LEFT track_004<br>B:e13 TRACK_APPEARED_LEFT track_005<br>B:e14 TRACK_APPEARED_LEFT track_006<br>B:e15 CLOSING_START track_003<br>B:e16 CLOSING_START track_004<br>B:e17 CLOSING_START track_005<br>B:e18 CLOSING_START track_006 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 3.00 |
| 3.10 | B:e19 TRACK_APPEARED_LEFT track_007<br>B:e20 CLOSING_START track_007 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known | 3.00 |
| 3.15 | B:e21 TRACK_LOST track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>sign-0: STOP sign known | 3.10 |
| 3.50 | B:e22 BRAKE_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.40 |
| 3.70 | B:e23 EGO_PATH_ENTRY track_002 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.60 |
| 3.75 | B:e24 TRACK_LOST track_003<br>B:e25 TRACK_LOST track_004<br>B:e26 TRACK_LOST track_005<br>B:e27 TRACK_LOST track_006<br>B:e28 TRACK_LOST track_007 | ego: MOVING, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known | 3.70 |
| 3.80 | B:e29 COLLISION<br>B:e30 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known | 3.70 |
| 3.85 | B:e31 BRAKE_START<br>B:e32 TRACK_APPEARED_RIGHT track_008<br>B:e33 CLOSING_START track_008<br>B:e34 CRITICAL_TTC_START track_008 | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known | 3.80 |
| 4.00 | B:e35 MOVING_END<br>B:e36 STOP_START | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known | 3.90 |
| 4.10 | B:e37 CRITICAL_TTC_END track_002 | ego: STOP, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known | 4.00 |
| 4.15 | B:e38 TRACK_LOST track_008 | ego: STOP, BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known | 4.10 |
| 4.30 | B:e39 CLOSING_END track_002 | ego: STOP, BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008<br>sign-0: STOP sign known | 4.20 |
| 4.80 | B:e40 EGO_PATH_EXIT track_002 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008<br>sign-0: STOP sign known | 4.70 |

## States still active when observation ended

- CLOSING of track_001, since B:e03 (t = 1.45 s); the track was lost at 3.15 s
- CLOSING of track_003, since B:e15 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_004, since B:e16 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_005, since B:e17 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_006, since B:e18 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_007, since B:e20 (t = 3.10 s); the track was lost at 3.75 s
- BRAKE, since B:e31 (t = 3.85 s)
- CLOSING of track_008, since B:e33 (t = 3.85 s); the track was lost at 4.15 s
- CRITICAL_TTC of track_008, since B:e34 (t = 3.85 s); the track was lost at 4.15 s
- STOP, since B:e36 (t = 4.00 s)

## Tracks lost

- track_001 at 3.15 s (B:e21): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 3.75 s (B:e24): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 3.75 s (B:e25): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 3.75 s (B:e26): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.75 s (B:e27): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 3.75 s (B:e28): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 4.15 s (B:e38): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 2.15, COLLISION 3.80 (+1.65 s); EGO_PATH_ENTRY 3.70 after critical TTC (+1.55 s)
- track_008: CRITICAL_TTC_START 3.85

## Sign detection windows

- STOP sign sign-0: detected 1.50 s -> 2.10 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.45 | 3.15 | 33 | 28.9 m / +38 deg | 14.65 m (3.15) | 14.7 m / +81 deg | 5.9 m/s |
| track_002 | 1.95 | 13.95 | 241 | 29.7 m / -59 deg | 0.14 m (4.30) | 2.2 m / +66 deg | 11.2 m/s |
| track_003 | 3.05 | 3.75 | 13 | 33.3 m / -75 deg | 30.02 m (3.75) | 30.0 m / -66 deg | 1.1 m/s |
| track_004 | 3.05 | 3.75 | 14 | 22.0 m / -77 deg | 19.12 m (3.75) | 19.1 m / -75 deg | 1.4 m/s |
| track_005 | 3.05 | 3.75 | 14 | 30.4 m / -72 deg | 26.97 m (3.75) | 27.0 m / -65 deg | 2.3 m/s |
| track_006 | 3.05 | 3.75 | 14 | 27.3 m / -76 deg | 24.12 m (3.75) | 24.1 m / -70 deg | 1.3 m/s |
| track_007 | 3.10 | 3.75 | 13 | 17.3 m / -80 deg | 15.03 m (3.75) | 15.0 m / -80 deg | 1.0 m/s |
| track_008 | 3.85 | 4.15 | 7 | 11.4 m / +80 deg | 9.26 m (4.15) | 9.3 m / +78 deg | 10.0 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.45 s: B's radar started tracking track_001, which appeared on its right.
- t = 1.45 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.50 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: B's radar started tracking track_002, which appeared on its left.
- t = 1.95 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.10 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.15 s: B's time-to-contact with track_002 became critical.
- t = 2.25 s: B started turning left.
- t = 2.95 s: B started braking.
- t = 3.05 s: B's radar started tracking track_003, which appeared on its left.
- t = 3.05 s: B's radar started tracking track_004, which appeared on its left.
- t = 3.05 s: B's radar started tracking track_005, which appeared on its left.
- t = 3.05 s: B's radar started tracking track_006, which appeared on its left.
- t = 3.05 s: B observed track_003 start closing in (already the case when first observed).
- t = 3.05 s: B observed track_004 start closing in (already the case when first observed).
- t = 3.05 s: B observed track_005 start closing in (already the case when first observed).
- t = 3.05 s: B observed track_006 start closing in (already the case when first observed).
- t = 3.10 s: B's radar started tracking track_007, which appeared on its left.
- t = 3.10 s: B observed track_007 start closing in (already the case when first observed).
- t = 3.15 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 3.50 s: B released the brake.
- t = 3.70 s: B observed track_002 enter its forward path corridor.
- t = 3.75 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: B's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: B stopped turning left.
- t = 3.85 s: B started braking.
- t = 3.85 s: B's radar started tracking track_008, which appeared on its right.
- t = 3.85 s: B observed track_008 start closing in (already the case when first observed).
- t = 3.85 s: B's time-to-contact with track_008 became critical (already the case when first observed).
- t = 4.00 s: B stopped moving.
- t = 4.00 s: B came to a stop.
- t = 4.10 s: B's time-to-contact with track_002 stopped being critical.
- t = 4.15 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 4.30 s: B observed track_002 stop closing in.
- t = 4.80 s: B observed track_002 leave its forward path corridor.
