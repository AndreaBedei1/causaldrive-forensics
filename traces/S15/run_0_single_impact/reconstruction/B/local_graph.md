# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 162.19994998723269 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 6 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 33; edges: 74 (PRECEDES 58, SAME_TRACK 16)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.80 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e03 | 1.95 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e04 | 1.95 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 2.10 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e06 | 2.15 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 2.25 | TURN_LEFT_START | B | - | ego |  |
| B:e08 | 2.95 | BRAKE_START | B | - | controls |  |
| B:e09 | 3.05 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e10 | 3.05 | TRACK_APPEARED_LEFT | B | track_003 | radar |  |
| B:e11 | 3.05 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e12 | 3.05 | TRACK_APPEARED_LEFT | B | track_005 | radar |  |
| B:e13 | 3.05 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e14 | 3.05 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e15 | 3.05 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e16 | 3.05 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e17 | 3.10 | TRACK_APPEARED_LEFT | B | track_006 | radar |  |
| B:e18 | 3.10 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e19 | 3.50 | BRAKE_END | B | - | controls |  |
| B:e20 | 3.70 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e21 | 3.75 | TRACK_LOST | B | track_002 | radar |  |
| B:e22 | 3.75 | TRACK_LOST | B | track_003 | radar |  |
| B:e23 | 3.75 | TRACK_LOST | B | track_004 | radar |  |
| B:e24 | 3.75 | TRACK_LOST | B | track_005 | radar |  |
| B:e25 | 3.75 | TRACK_LOST | B | track_006 | radar |  |
| B:e26 | 3.80 | COLLISION | B | - | collision_sensor | peak_impulse=9797.50 |
| B:e27 | 3.80 | TURN_LEFT_END | B | - | ego |  |
| B:e28 | 3.85 | BRAKE_START | B | - | controls |  |
| B:e29 | 4.00 | MOVING_END | B | - | ego |  |
| B:e30 | 4.00 | STOP_START | B | - | ego |  |
| B:e31 | 4.10 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e32 | 4.30 | CLOSING_END | B | track_001 | radar |  |
| B:e33 | 4.80 | EGO_PATH_EXIT | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e08 --PRECEDES--> B:e13
    B:e08 --PRECEDES--> B:e14
    B:e08 --PRECEDES--> B:e15
    B:e08 --PRECEDES--> B:e16
    B:e09 --PRECEDES--> B:e17
    B:e09 --PRECEDES--> B:e18
    B:e10 --PRECEDES--> B:e17
    B:e10 --PRECEDES--> B:e18
    B:e11 --PRECEDES--> B:e17
    B:e11 --PRECEDES--> B:e18
    B:e12 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e18
    B:e13 --PRECEDES--> B:e17
    B:e13 --PRECEDES--> B:e18
    B:e14 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e20 --PRECEDES--> B:e24
    B:e20 --PRECEDES--> B:e25
    B:e21 --PRECEDES--> B:e26
    B:e21 --PRECEDES--> B:e27
    B:e22 --PRECEDES--> B:e26
    B:e22 --PRECEDES--> B:e27
    B:e23 --PRECEDES--> B:e26
    B:e23 --PRECEDES--> B:e27
    B:e24 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e31
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e06
    B:e09 --SAME_TRACK--> B:e13
    B:e10 --SAME_TRACK--> B:e14
    B:e11 --SAME_TRACK--> B:e15
    B:e12 --SAME_TRACK--> B:e16
    B:e17 --SAME_TRACK--> B:e18
    B:e03 --SAME_TRACK--> B:e20
    B:e09 --SAME_TRACK--> B:e21
    B:e10 --SAME_TRACK--> B:e22
    B:e11 --SAME_TRACK--> B:e23
    B:e12 --SAME_TRACK--> B:e24
    B:e17 --SAME_TRACK--> B:e25
    B:e03 --SAME_TRACK--> B:e31
    B:e03 --SAME_TRACK--> B:e32
    B:e03 --SAME_TRACK--> B:e33
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.80 | B:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 1.80 |
| 1.95 | B:e03 TRACK_APPEARED_LEFT track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING<br>sign-0: STOP sign known | 1.90 |
| 2.10 | B:e05 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 2.10 |
| 2.15 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 2.10 |
| 2.25 | B:e07 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.20 |
| 2.95 | B:e08 BRAKE_START | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.90 |
| 3.05 | B:e09 TRACK_APPEARED_LEFT track_002<br>B:e10 TRACK_APPEARED_LEFT track_003<br>B:e11 TRACK_APPEARED_LEFT track_004<br>B:e12 TRACK_APPEARED_LEFT track_005<br>B:e13 CLOSING_START track_002<br>B:e14 CLOSING_START track_003<br>B:e15 CLOSING_START track_004<br>B:e16 CLOSING_START track_005 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 3.00 |
| 3.10 | B:e17 TRACK_APPEARED_LEFT track_006<br>B:e18 CLOSING_START track_006 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>sign-0: STOP sign known | 3.00 |
| 3.50 | B:e19 BRAKE_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known | 3.40 |
| 3.70 | B:e20 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known | 3.60 |
| 3.75 | B:e21 TRACK_LOST track_002<br>B:e22 TRACK_LOST track_003<br>B:e23 TRACK_LOST track_004<br>B:e24 TRACK_LOST track_005<br>B:e25 TRACK_LOST track_006 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known | 3.70 |
| 3.80 | B:e26 COLLISION<br>B:e27 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known | 3.70 |
| 3.85 | B:e28 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known | 3.80 |
| 4.00 | B:e29 MOVING_END<br>B:e30 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known | 3.90 |
| 4.10 | B:e31 CRITICAL_TTC_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known | 4.00 |
| 4.30 | B:e32 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known | 4.20 |
| 4.80 | B:e33 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_006<br>sign-0: STOP sign known | 4.70 |

## States still active when observation ended

- CLOSING of track_002, since B:e13 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_003, since B:e14 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_004, since B:e15 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_005, since B:e16 (t = 3.05 s); the track was lost at 3.75 s
- CLOSING of track_006, since B:e18 (t = 3.10 s); the track was lost at 3.75 s
- BRAKE, since B:e28 (t = 3.85 s)
- STOP, since B:e30 (t = 4.00 s)

## Tracks lost

- track_002 at 3.75 s (B:e21): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 3.75 s (B:e22): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_004 at 3.75 s (B:e23): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_005 at 3.75 s (B:e24): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_006 at 3.75 s (B:e25): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.15, COLLISION 3.80 (+1.65 s); EGO_PATH_ENTRY 3.70 after critical TTC (+1.55 s)

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.95 | 13.95 | 241 | 29.7 m / -59 deg | 0.14 m (4.25) | 13.8 m / +76 deg | 11.2 m/s |
| track_002 | 3.05 | 3.75 | 13 | 33.3 m / -75 deg | 30.02 m (3.75) | 30.0 m / -66 deg | 1.1 m/s |
| track_003 | 3.05 | 3.75 | 14 | 22.0 m / -77 deg | 19.12 m (3.75) | 19.1 m / -75 deg | 1.4 m/s |
| track_004 | 3.05 | 3.75 | 14 | 30.4 m / -72 deg | 26.97 m (3.75) | 27.0 m / -65 deg | 2.3 m/s |
| track_005 | 3.05 | 3.75 | 14 | 27.3 m / -76 deg | 24.12 m (3.75) | 24.1 m / -70 deg | 1.3 m/s |
| track_006 | 3.10 | 3.75 | 13 | 17.3 m / -80 deg | 15.03 m (3.75) | 15.0 m / -80 deg | 1.0 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.80 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: B's radar started tracking track_001, which appeared on its left.
- t = 1.95 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.10 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.15 s: B's time-to-contact with track_001 became critical.
- t = 2.25 s: B started turning left.
- t = 2.95 s: B started braking.
- t = 3.05 s: B's radar started tracking track_002, which appeared on its left.
- t = 3.05 s: B's radar started tracking track_003, which appeared on its left.
- t = 3.05 s: B's radar started tracking track_004, which appeared on its left.
- t = 3.05 s: B's radar started tracking track_005, which appeared on its left.
- t = 3.05 s: B observed track_002 start closing in (already the case when first observed).
- t = 3.05 s: B observed track_003 start closing in (already the case when first observed).
- t = 3.05 s: B observed track_004 start closing in (already the case when first observed).
- t = 3.05 s: B observed track_005 start closing in (already the case when first observed).
- t = 3.10 s: B's radar started tracking track_006, which appeared on its left.
- t = 3.10 s: B observed track_006 start closing in (already the case when first observed).
- t = 3.50 s: B released the brake.
- t = 3.70 s: B observed track_001 enter its forward path corridor.
- t = 3.75 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 3.75 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 3.80 s: B's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: B stopped turning left.
- t = 3.85 s: B started braking.
- t = 4.00 s: B stopped moving.
- t = 4.00 s: B came to a stop.
- t = 4.10 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.30 s: B observed track_001 stop closing in.
- t = 4.80 s: B observed track_001 leave its forward path corridor.
