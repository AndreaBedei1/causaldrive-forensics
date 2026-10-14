# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 37.092514757066965 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 6 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 31; edges: 53 (PRECEDES 37, SAME_TRACK 16)

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
| B:e13 | 5.45 | CLOSING_START | B | track_005 | radar |  |
| B:e14 | 5.55 | CRITICAL_TTC_START | B | track_005 | radar |  |
| B:e15 | 6.20 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e16 | 6.40 | EGO_PATH_ENTRY | B | track_003 | radar | geometry=estimated_body |
| B:e17 | 6.40 | CRITICAL_TTC_START | B | track_003 | radar |  |
| B:e18 | 6.90 | TRACK_APPEARED_FRONT | B | track_006 | radar | initial_in_ego_path=False |
| B:e19 | 7.05 | EGO_PATH_ENTRY | B | track_005 | radar | geometry=estimated_body |
| B:e20 | 7.20 | CLOSING_END | B | track_005 | radar |  |
| B:e21 | 7.30 | COLLISION | B | - | collision_sensor | peak_impulse=389.26 |
| B:e22 | 7.30 | CRITICAL_TTC_END | B | track_005 | radar |  |
| B:e23 | 7.35 | THROTTLE_END | B | - | controls |  |
| B:e24 | 7.35 | BRAKE_START | B | - | controls |  |
| B:e25 | 7.35 | TURN_LEFT_START | B | - | ego |  |
| B:e26 | 7.60 | TRACK_LOST | B | track_006 | radar |  |
| B:e27 | 7.80 | TRACK_LOST | B | track_003 | radar |  |
| B:e28 | 8.00 | TRACK_LOST | B | track_001 | radar |  |
| B:e29 | 8.25 | TURN_LEFT_END | B | - | ego |  |
| B:e30 | 8.25 | MOVING_END | B | - | ego |  |
| B:e31 | 8.25 | STOP_START | B | - | ego |  |

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
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e24
    B:e21 --PRECEDES--> B:e25
    B:e22 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e26
    B:e26 --PRECEDES--> B:e27
    B:e27 --PRECEDES--> B:e28
    B:e28 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e03 --SAME_TRACK--> B:e07
    B:e08 --SAME_TRACK--> B:e09
    B:e06 --SAME_TRACK--> B:e10
    B:e08 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e12
    B:e08 --SAME_TRACK--> B:e13
    B:e08 --SAME_TRACK--> B:e14
    B:e03 --SAME_TRACK--> B:e15
    B:e05 --SAME_TRACK--> B:e16
    B:e05 --SAME_TRACK--> B:e17
    B:e08 --SAME_TRACK--> B:e19
    B:e08 --SAME_TRACK--> B:e20
    B:e08 --SAME_TRACK--> B:e22
    B:e18 --SAME_TRACK--> B:e26
    B:e05 --SAME_TRACK--> B:e27
    B:e03 --SAME_TRACK--> B:e28
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
| 5.45 | B:e13 CLOSING_START track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_002, track_004 | 5.40 |
| 5.55 | B:e14 CRITICAL_TTC_START track_005 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: CLOSING<br>track lost, states UNKNOWN: track_002, track_004 | 5.50 |
| 6.20 | B:e15 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_003: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004 | 6.10 |
| 6.40 | B:e16 EGO_PATH_ENTRY track_003<br>B:e17 CRITICAL_TTC_START track_003 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: no active state<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004 | 6.30 |
| 6.90 | B:e18 TRACK_APPEARED_FRONT track_006 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002, track_004 | 6.80 |
| 7.05 | B:e19 EGO_PATH_ENTRY track_005 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.00 |
| 7.20 | B:e20 CLOSING_END track_005 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.10 |
| 7.30 | B:e21 COLLISION<br>B:e22 CRITICAL_TTC_END track_005 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: CRITICAL_TTC, IN_EGO_PATH<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.20 |
| 7.35 | B:e23 THROTTLE_END<br>B:e24 BRAKE_START<br>B:e25 TURN_LEFT_START | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track_006: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_004 | 7.30 |
| 7.60 | B:e26 TRACK_LOST track_006 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track_006: no active state<br>track lost, states UNKNOWN: track_002, track_004 | 7.50 |
| 7.80 | B:e27 TRACK_LOST track_003 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_006 | 7.70 |
| 8.00 | B:e28 TRACK_LOST track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_006 | 7.90 |
| 8.25 | B:e29 TURN_LEFT_END<br>B:e30 MOVING_END<br>B:e31 STOP_START | ego: MOVING, BRAKE, TURN_LEFT<br>track_005: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_006 | 8.20 |

## States still active when observation ended

- EGO_PATH of track_003, since B:e16 (t = 6.40 s); the track was lost at 7.80 s
- CRITICAL_TTC of track_003, since B:e17 (t = 6.40 s); the track was lost at 7.80 s
- EGO_PATH of track_005, since B:e19 (t = 7.05 s)
- BRAKE, since B:e24 (t = 7.35 s)
- STOP, since B:e31 (t = 8.25 s)

## Tracks lost

- track_003 at 7.80 s (B:e27): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 8.00 s (B:e28): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004, track_002, track_006

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 7.30 (+6.80 s)
- track_003: CRITICAL_TTC_START 6.40, COLLISION 7.30 (+0.90 s); EGO_PATH_ENTRY 6.40 together with critical TTC (+0.00 s)
- track_005: CRITICAL_TTC_START 5.55, COLLISION 7.30 (+1.75 s); EGO_PATH_ENTRY 7.05 after critical TTC (+1.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 8.00 | 161 | 13.4 m / +0 deg | 13.37 m (0.00) | 14.9 m / -3 deg | 10.1 m/s |
| track_002 | 0.00 | 5.05 | 98 | 12.3 m / +30 deg | 11.00 m (0.15) | 19.8 m / +17 deg | 12.0 m/s |
| track_003 | 0.00 | 7.80 | 157 | 3.1 m / +129 deg | 1.06 m (2.80) | 15.7 m / +4 deg | 15.2 m/s |
| track_004 | 0.30 | 3.40 | 60 | 26.6 m / +6 deg | 26.65 m (0.30) | 32.5 m / +6 deg | 11.9 m/s |
| track_005 | 3.00 | 11.95 | 180 | 7.6 m / +139 deg | 0.55 m (8.25) | 0.6 m / +6 deg | 12.8 m/s |
| track_006 | 6.90 | 7.60 | 15 | 23.1 m / +3 deg | 23.15 m (6.90) | 24.5 m / +8 deg | 12.4 m/s |

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
- t = 5.45 s: B observed track_005 start closing in.
- t = 5.55 s: B's time-to-contact with track_005 became critical.
- t = 6.20 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.40 s: B observed track_003 enter its forward path corridor.
- t = 6.40 s: B's time-to-contact with track_003 became critical.
- t = 6.90 s: B's radar started tracking track_006, which appeared in front of it.
- t = 7.05 s: B observed track_005 enter its forward path corridor.
- t = 7.20 s: B observed track_005 stop closing in.
- t = 7.30 s: B's collision sensor recorded a contact (peak impulse 389 N*s).
- t = 7.30 s: B's time-to-contact with track_005 stopped being critical.
- t = 7.35 s: B released the accelerator.
- t = 7.35 s: B started braking.
- t = 7.35 s: B started turning left.
- t = 7.60 s: B's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 7.80 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 8.00 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.25 s: B stopped turning left.
- t = 8.25 s: B stopped moving.
- t = 8.25 s: B came to a stop.
