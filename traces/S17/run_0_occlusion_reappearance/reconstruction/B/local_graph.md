# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 415.1301955282688 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 8 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 40; edges: 76 (PRECEDES 53, SAME_TRACK 23)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e06 | 0.30 | TRACK_APPEARED_RIGHT | B | track_004 | radar | initial_in_ego_path=False |
| B:e07 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e08 | 3.00 | TRACK_APPEARED_RIGHT | B | track_005 | radar | initial_in_ego_path=False |
| B:e09 | 3.00 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e10 | 3.40 | TRACK_LOST | B | track_004 | radar |  |
| B:e11 | 3.55 | CLOSING_END | B | track_005 | radar |  |
| B:e12 | 5.05 | TRACK_LOST | B | track_002 | radar |  |
| B:e13 | 5.15 | TRACK_APPEARED_RIGHT | B | track_006 | radar | initial_in_ego_path=False |
| B:e14 | 5.15 | CLOSING_START | B | track_006 | radar | active_at_first_observation=True |
| B:e15 | 5.45 | CLOSING_START | B | track_005 | radar |  |
| B:e16 | 5.55 | CRITICAL_TTC_START | B | track_003 | radar |  |
| B:e17 | 5.55 | CRITICAL_TTC_START | B | track_005 | radar |  |
| B:e18 | 5.85 | EGO_PATH_ENTRY | B | track_003 | radar | geometry=estimated_body |
| B:e19 | 6.20 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e20 | 6.20 | EGO_PATH_EXIT | B | track_001 | radar | geometry=estimated_body |
| B:e21 | 6.90 | TRACK_APPEARED_FRONT | B | track_007 | radar | initial_in_ego_path=True |
| B:e22 | 6.95 | EGO_PATH_ENTRY | B | track_005 | radar | geometry=estimated_body |
| B:e23 | 7.20 | CLOSING_END | B | track_005 | radar |  |
| B:e24 | 7.30 | COLLISION | B | - | collision_sensor | peak_impulse=389.26 |
| B:e25 | 7.30 | CRITICAL_TTC_END | B | track_005 | radar |  |
| B:e26 | 7.35 | THROTTLE_END | B | - | controls |  |
| B:e27 | 7.35 | BRAKE_START | B | - | controls |  |
| B:e28 | 7.35 | TURN_LEFT_START | B | - | ego |  |
| B:e29 | 7.40 | TRACK_LOST | B | track_006 | radar |  |
| B:e30 | 7.50 | EGO_PATH_EXIT | B | track_007 | radar | geometry=estimated_body |
| B:e31 | 7.60 | TRACK_LOST | B | track_007 | radar |  |
| B:e32 | 7.65 | EGO_PATH_ENTRY | B | track_001 | radar | geometry=estimated_body |
| B:e33 | 7.80 | TRACK_LOST | B | track_003 | radar |  |
| B:e34 | 8.00 | TRACK_LOST | B | track_001 | radar |  |
| B:e35 | 8.25 | TURN_LEFT_END | B | - | ego |  |
| B:e36 | 8.25 | MOVING_END | B | - | ego |  |
| B:e37 | 8.25 | STOP_START | B | - | ego |  |
| B:e38 | 8.30 | TRACK_APPEARED_RIGHT | B | track_008 | radar | initial_in_ego_path=False |
| B:e39 | 8.30 | CLOSING_START | B | track_008 | radar | active_at_first_observation=True |
| B:e40 | 9.20 | CLOSING_END | B | track_008 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e27
    B:e24 --PRECEDES--> B:e28
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e30 --PRECEDES--> B:e31
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e34 --PRECEDES--> B:e36
    B:e34 --PRECEDES--> B:e37
    B:e35 --PRECEDES--> B:e38
    B:e35 --PRECEDES--> B:e39
    B:e36 --PRECEDES--> B:e38
    B:e36 --PRECEDES--> B:e39
    B:e37 --PRECEDES--> B:e38
    B:e37 --PRECEDES--> B:e39
    B:e38 --PRECEDES--> B:e40
    B:e39 --PRECEDES--> B:e40
    B:e03 --SAME_TRACK--> B:e07
    B:e08 --SAME_TRACK--> B:e09
    B:e06 --SAME_TRACK--> B:e10
    B:e08 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e12
    B:e13 --SAME_TRACK--> B:e14
    B:e08 --SAME_TRACK--> B:e15
    B:e05 --SAME_TRACK--> B:e16
    B:e08 --SAME_TRACK--> B:e17
    B:e05 --SAME_TRACK--> B:e18
    B:e03 --SAME_TRACK--> B:e19
    B:e03 --SAME_TRACK--> B:e20
    B:e08 --SAME_TRACK--> B:e22
    B:e08 --SAME_TRACK--> B:e23
    B:e08 --SAME_TRACK--> B:e25
    B:e13 --SAME_TRACK--> B:e29
    B:e21 --SAME_TRACK--> B:e30
    B:e21 --SAME_TRACK--> B:e31
    B:e03 --SAME_TRACK--> B:e32
    B:e05 --SAME_TRACK--> B:e33
    B:e03 --SAME_TRACK--> B:e34
    B:e38 --SAME_TRACK--> B:e39
    B:e38 --SAME_TRACK--> B:e40
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_RIGHT track_002<br>B:e05 TRACK_APPEARED_RIGHT track_003 | ego: not yet observed | - |
| 0.30 | B:e06 TRACK_APPEARED_RIGHT track_004 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC? | 0.20 |
| 0.50 | B:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC? | 0.40 |
| 3.00 | B:e08 TRACK_APPEARED_RIGHT track_005<br>B:e09 CLOSING_START track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state | 2.90 |
| 3.40 | B:e10 TRACK_LOST track_004 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: CLOSING, CRITICAL_TTC? | 3.30 |
| 3.55 | B:e11 CLOSING_END track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_004 | 3.50 |
| 5.05 | B:e12 TRACK_LOST track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_004 | 5.00 |
| 5.15 | B:e13 TRACK_APPEARED_RIGHT track_006<br>B:e14 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_002, track_004 | 5.10 |
| 5.45 | B:e15 CLOSING_START track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 5.40 |
| 5.55 | B:e16 CRITICAL_TTC_START track_003<br>B:e17 CRITICAL_TTC_START track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: CLOSING<br>track_006: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 5.50 |
| 5.85 | B:e18 EGO_PATH_ENTRY track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_004 | 5.80 |
| 6.20 | B:e19 CRITICAL_TTC_END track_001<br>B:e20 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_004 | 6.10 |
| 6.90 | B:e21 TRACK_APPEARED_FRONT track_007 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track lost, states UNKNOWN: track_002, track_004 | 6.80 |
| 6.95 | B:e22 EGO_PATH_ENTRY track_005 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CLOSING<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 6.90 |
| 7.20 | B:e23 CLOSING_END track_005 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.10 |
| 7.30 | B:e24 COLLISION<br>B:e25 CRITICAL_TTC_END track_005 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.20 |
| 7.35 | B:e26 THROTTLE_END<br>B:e27 BRAKE_START<br>B:e28 TURN_LEFT_START | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.30 |
| 7.40 | B:e29 TRACK_LOST track_006 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track_006: CLOSING<br>track_007: IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.30 |
| 7.50 | B:e30 EGO_PATH_EXIT track_007 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_006 | 7.40 |
| 7.60 | B:e31 TRACK_LOST track_007 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track_007: no active state<br>track lost, states UNKNOWN: track_002, track_004, track_006 | 7.50 |
| 7.65 | B:e32 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_006, track_007 | 7.60 |
| 7.80 | B:e33 TRACK_LOST track_003 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_006, track_007 | 7.70 |
| 8.00 | B:e34 TRACK_LOST track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006, track_007 | 7.90 |
| 8.25 | B:e35 TURN_LEFT_END<br>B:e36 MOVING_END<br>B:e37 STOP_START | ego: MOVING, BRAKE, TURN_LEFT<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_006, track_007 | 8.20 |
| 8.30 | B:e38 TRACK_APPEARED_RIGHT track_008<br>B:e39 CLOSING_START track_008 | ego: STOP, BRAKE<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_006, track_007 | 8.20 |
| 9.20 | B:e40 CLOSING_END track_008 | ego: STOP, BRAKE<br>track_005: IN_EGO_PATH<br>track_008: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_006, track_007 | 9.10 |

## States still active when observation ended

- CLOSING of track_006, since B:e14 (t = 5.15 s); the track was lost at 7.40 s
- CRITICAL_TTC of track_003, since B:e16 (t = 5.55 s); the track was lost at 7.80 s
- EGO_PATH of track_003, since B:e18 (t = 5.85 s); the track was lost at 7.80 s
- EGO_PATH of track_005, since B:e22 (t = 6.95 s)
- BRAKE, since B:e27 (t = 7.35 s)
- EGO_PATH of track_001, since B:e32 (t = 7.65 s); the track was lost at 8.00 s
- STOP, since B:e37 (t = 8.25 s)

## Tracks lost

- track_006 at 7.40 s (B:e29): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 7.80 s (B:e33): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 8.00 s (B:e34): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_002, track_007

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.30 (+6.80 s); EGO_PATH_ENTRY 7.65 after critical TTC (+7.15 s)
- track_003: CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 5.85 after critical TTC (+0.30 s)
- track_005: CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 6.95 after critical TTC (+1.40 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 8.00 | 161 | 13.4 m / +0 deg | 13.37 m (0.00) | 14.9 m / -3 deg | 10.1 m/s |
| track_002 | 0.00 | 5.05 | 98 | 12.3 m / +30 deg | 11.00 m (0.15) | 19.8 m / +17 deg | 12.0 m/s |
| track_003 | 0.00 | 7.80 | 157 | 3.1 m / +129 deg | 1.06 m (2.80) | 15.7 m / +4 deg | 15.2 m/s |
| track_004 | 0.30 | 3.40 | 60 | 26.6 m / +6 deg | 26.64 m (0.30) | 32.5 m / +6 deg | 11.9 m/s |
| track_005 | 3.00 | 11.95 | 180 | 7.6 m / +139 deg | 0.53 m (8.25) | 0.7 m / +2 deg | 12.8 m/s |
| track_006 | 5.15 | 7.40 | 46 | 18.9 m / +156 deg | 13.91 m (7.40) | 13.9 m / +156 deg | 12.5 m/s |
| track_007 | 6.90 | 7.60 | 15 | 23.1 m / +3 deg | 23.15 m (6.90) | 24.5 m / +8 deg | 12.4 m/s |
| track_008 | 8.30 | 11.95 | 74 | 9.0 m / +152 deg | 2.95 m (9.55) | 3.0 m / +121 deg | 9.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.30 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 3.00 s: B's radar started tracking track_005, which appeared on its right.
- t = 3.00 s: B observed track_005 start closing in (already the case when first observed).
- t = 3.40 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 3.55 s: B observed track_005 stop closing in.
- t = 5.05 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 5.15 s: B's radar started tracking track_006, which appeared on its right.
- t = 5.15 s: B observed track_006 start closing in (already the case when first observed).
- t = 5.45 s: B observed track_005 start closing in.
- t = 5.55 s: B's time-to-contact with track_003 became critical.
- t = 5.55 s: B's time-to-contact with track_005 became critical.
- t = 5.85 s: B observed track_003 enter its forward path corridor.
- t = 6.20 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.20 s: B observed track_001 leave its forward path corridor.
- t = 6.90 s: B's radar started tracking track_007, which appeared in front of it.
- t = 6.95 s: B observed track_005 enter its forward path corridor.
- t = 7.20 s: B observed track_005 stop closing in.
- t = 7.30 s: B's collision sensor recorded a contact (peak impulse 389 N*s).
- t = 7.30 s: B's time-to-contact with track_005 stopped being critical.
- t = 7.35 s: B released the accelerator.
- t = 7.35 s: B started braking.
- t = 7.35 s: B started turning left.
- t = 7.40 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 7.50 s: B observed track_007 leave its forward path corridor.
- t = 7.60 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 7.65 s: B observed track_001 enter its forward path corridor.
- t = 7.80 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 8.00 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.25 s: B stopped turning left.
- t = 8.25 s: B stopped moving.
- t = 8.25 s: B came to a stop.
- t = 8.30 s: B's radar started tracking track_008, which appeared on its right.
- t = 8.30 s: B observed track_008 start closing in (already the case when first observed).
- t = 9.20 s: B observed track_008 stop closing in.
