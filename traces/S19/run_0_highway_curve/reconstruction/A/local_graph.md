# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 20.645653568208218 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 11 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 90 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 38; edges: 68 (PRECEDES 48, SAME_TRACK 20)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e04 | 0.00 | TRACK_APPEARED_LEFT | A | track_004 | radar | initial_in_ego_path=False |
| A:e05 | 0.00 | TRACK_APPEARED_RIGHT | A | track_002 | radar | initial_in_ego_path=False |
| A:e06 | 0.00 | TRACK_APPEARED_RIGHT | A | track_003 | radar | initial_in_ego_path=False |
| A:e07 | 0.00 | TRACK_APPEARED_RIGHT | A | track_005 | radar | initial_in_ego_path=False |
| A:e08 | 0.00 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e09 | 0.00 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e10 | 0.05 | TRACK_APPEARED_LEFT | A | track_006 | radar | initial_in_ego_path=True |
| A:e11 | 0.60 | TRACK_LOST | A | track_006 | radar |  |
| A:e12 | 1.40 | TRACK_APPEARED_LEFT | A | track_007 | radar | initial_in_ego_path=True |
| A:e13 | 2.05 | TRACK_LOST | A | track_007 | radar |  |
| A:e14 | 2.35 | TRACK_LOST | A | track_005 | radar |  |
| A:e15 | 2.50 | TRACK_APPEARED_LEFT | A | track_008 | radar | initial_in_ego_path=True |
| A:e16 | 3.00 | TRACK_LOST | A | track_008 | radar |  |
| A:e17 | 3.35 | TRACK_APPEARED_LEFT | A | track_009 | radar | initial_in_ego_path=True |
| A:e18 | 3.70 | TRACK_LOST | A | track_009 | radar |  |
| A:e19 | 5.50 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e20 | 5.50 | CUT_IN_FROM_RIGHT_START | A | track_002 | radar | geometry=estimated_body |
| A:e21 | 6.20 | TRACK_LOST | A | track_004 | radar |  |
| A:e22 | 6.30 | EGO_PATH_ENTRY | A | track_002 | radar | occupancy_evidence=box; occupancy_margin_m=0.56; occupancy_sigma_m=0.26; cause=TARGET_LATERAL; geometry=estimated_body |
| A:e23 | 7.40 | CLOSING_END | A | track_003 | radar |  |
| A:e24 | 7.50 | COLLISION | A | - | collision_sensor | peak_impulse=7449.21 |
| A:e25 | 7.50 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e26 | 7.50 | CLOSING_END | A | track_002 | radar |  |
| A:e27 | 7.55 | THROTTLE_END | A | - | controls |  |
| A:e28 | 7.55 | BRAKE_START | A | - | controls |  |
| A:e29 | 7.75 | TRACK_APPEARED_LEFT | A | track_010 | radar | initial_in_ego_path=False |
| A:e30 | 8.35 | CUT_IN_FROM_RIGHT_END | A | track_002 | radar | geometry=estimated_body |
| A:e31 | 8.45 | TRACK_LOST | A | track_001 | radar |  |
| A:e32 | 8.45 | TRACK_LOST | A | track_010 | radar |  |
| A:e33 | 8.70 | TRACK_APPEARED_RIGHT | A | track_011 | radar | initial_in_ego_path=False |
| A:e34 | 8.70 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e35 | 8.95 | MOVING_END | A | - | ego |  |
| A:e36 | 8.95 | STOP_START | A | - | ego |  |
| A:e37 | 10.30 | CLOSING_END | A | track_011 | radar |  |
| A:e38 | 11.90 | TRACK_LOST | A | track_003 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e10
    A:e02 --PRECEDES--> A:e10
    A:e03 --PRECEDES--> A:e10
    A:e04 --PRECEDES--> A:e10
    A:e05 --PRECEDES--> A:e10
    A:e06 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e27
    A:e24 --PRECEDES--> A:e28
    A:e25 --PRECEDES--> A:e27
    A:e25 --PRECEDES--> A:e28
    A:e26 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e28 --PRECEDES--> A:e29
    A:e29 --PRECEDES--> A:e30
    A:e30 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e37
    A:e37 --PRECEDES--> A:e38
    A:e05 --SAME_TRACK--> A:e08
    A:e06 --SAME_TRACK--> A:e09
    A:e10 --SAME_TRACK--> A:e11
    A:e12 --SAME_TRACK--> A:e13
    A:e07 --SAME_TRACK--> A:e14
    A:e15 --SAME_TRACK--> A:e16
    A:e17 --SAME_TRACK--> A:e18
    A:e05 --SAME_TRACK--> A:e19
    A:e05 --SAME_TRACK--> A:e20
    A:e04 --SAME_TRACK--> A:e21
    A:e05 --SAME_TRACK--> A:e22
    A:e06 --SAME_TRACK--> A:e23
    A:e05 --SAME_TRACK--> A:e25
    A:e05 --SAME_TRACK--> A:e26
    A:e05 --SAME_TRACK--> A:e30
    A:e03 --SAME_TRACK--> A:e31
    A:e29 --SAME_TRACK--> A:e32
    A:e33 --SAME_TRACK--> A:e34
    A:e33 --SAME_TRACK--> A:e37
    A:e06 --SAME_TRACK--> A:e38
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_LEFT track_001<br>A:e04 TRACK_APPEARED_LEFT track_004<br>A:e05 TRACK_APPEARED_RIGHT track_002<br>A:e06 TRACK_APPEARED_RIGHT track_003<br>A:e07 TRACK_APPEARED_RIGHT track_005<br>A:e08 CLOSING_START track_002<br>A:e09 CLOSING_START track_003 | ego: not yet observed | - |
| 0.05 | A:e10 TRACK_APPEARED_LEFT track_006 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_003: CLOSING, CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? | 0.00 |
| 0.60 | A:e11 TRACK_LOST track_006 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track_005: no active state<br>track_006: IN_EGO_PATH, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.50 |
| 1.40 | A:e12 TRACK_APPEARED_LEFT track_007 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_006 | 1.30 |
| 2.05 | A:e13 TRACK_LOST track_007 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track_005: no active state<br>track_007: IN_EGO_PATH<br>track lost, states UNKNOWN: track_006 | 2.00 |
| 2.35 | A:e14 TRACK_LOST track_005 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_006, track_007 | 2.30 |
| 2.50 | A:e15 TRACK_APPEARED_LEFT track_008 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005, track_006, track_007 | 2.40 |
| 3.00 | A:e16 TRACK_LOST track_008 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track_008: IN_EGO_PATH, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_005, track_006, track_007 | 2.90 |
| 3.35 | A:e17 TRACK_APPEARED_LEFT track_009 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005, track_006, track_007, track_008 | 3.30 |
| 3.70 | A:e18 TRACK_LOST track_009 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track_009: IN_EGO_PATH, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_005, track_006, track_007, track_008 | 3.60 |
| 5.50 | A:e19 CRITICAL_TTC_START track_002<br>A:e20 CUT_IN_FROM_RIGHT_START track_002 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005, track_006, track_007, track_008, track_009 | 5.40 |
| 6.20 | A:e21 TRACK_LOST track_004 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_005, track_006, track_007, track_008, track_009 | 6.10 |
| 6.30 | A:e22 EGO_PATH_ENTRY track_002 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_007, track_008, track_009 | 6.20 |
| 7.40 | A:e23 CLOSING_END track_003 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_007, track_008, track_009 | 7.30 |
| 7.50 | A:e24 COLLISION<br>A:e25 CRITICAL_TTC_END track_002<br>A:e26 CLOSING_END track_002 | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_007, track_008, track_009 | 7.40 |
| 7.55 | A:e27 THROTTLE_END<br>A:e28 BRAKE_START | ego: MOVING, THROTTLE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_007, track_008, track_009 | 7.50 |
| 7.75 | A:e29 TRACK_APPEARED_LEFT track_010 | ego: MOVING, BRAKE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_007, track_008, track_009 | 7.70 |
| 8.35 | A:e30 CUT_IN_FROM_RIGHT_END track_002 | ego: MOVING, BRAKE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_007, track_008, track_009 | 8.30 |
| 8.45 | A:e31 TRACK_LOST track_001<br>A:e32 TRACK_LOST track_010 | ego: MOVING, BRAKE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_001: no active state<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_010: no active state<br>track lost, states UNKNOWN: track_004, track_005, track_006, track_007, track_008, track_009 | 8.40 |
| 8.70 | A:e33 TRACK_APPEARED_RIGHT track_011<br>A:e34 CLOSING_START track_011 | ego: MOVING, BRAKE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006, track_007, track_008, track_009, track_010 | 8.60 |
| 8.95 | A:e35 MOVING_END<br>A:e36 STOP_START | ego: MOVING, BRAKE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_011: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006, track_007, track_008, track_009, track_010 | 8.90 |
| 10.30 | A:e37 CLOSING_END track_011 | ego: STOP, BRAKE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_011: CLOSING<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006, track_007, track_008, track_009, track_010 | 10.20 |
| 11.90 | A:e38 TRACK_LOST track_003 | ego: STOP, BRAKE, INDICATOR_LEFT?, INDICATOR_RIGHT?<br>track_002: IN_EGO_PATH<br>track_003: no active state<br>track_011: no active state<br>track lost, states UNKNOWN: track_001, track_004, track_005, track_006, track_007, track_008, track_009, track_010 | 11.80 |

## States still active when observation ended

- EGO_PATH of track_002, since A:e22 (t = 6.30 s)
- BRAKE, since A:e28 (t = 7.55 s)
- STOP, since A:e36 (t = 8.95 s)

## Tracks lost

- track_006 at 0.60 s (A:e11): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_007 at 2.05 s (A:e13): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_008 at 3.00 s (A:e16): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_009 at 3.70 s (A:e18): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_005, track_004, track_001, track_010, track_003

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: critical TTC already active before the cut-in: CRITICAL_TTC_START 5.50 <= CUT_IN_FROM_RIGHT_START 5.50 (+0.00 s); EGO_PATH_ENTRY 6.30 after critical TTC (+0.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 8.45 | 165 | 1.5 m / -76 deg | 1.44 m (1.10) | 28.2 m / -23 deg | 23.9 m/s |
| track_002 | 0.00 | 11.95 | 240 | 22.0 m / +5 deg | 0.21 m (8.00) | 1.6 m / -24 deg | 17.9 m/s |
| track_003 | 0.00 | 11.90 | 235 | 22.4 m / +14 deg | 5.98 m (7.45) | 64.0 m / -15 deg | 18.1 m/s |
| track_004 | 0.00 | 6.20 | 95 | 42.9 m / -9 deg | 42.88 m (0.00) | 68.0 m / -12 deg | 23.9 m/s |
| track_005 | 0.00 | 2.35 | 48 | 10.9 m / +149 deg | 10.88 m (0.00) | 17.3 m / +156 deg | 18.3 m/s |
| track_006 | 0.05 | 0.60 | 5 | 84.3 m / -12 deg | 84.25 m (0.45) | 84.2 m / -13 deg | 20.0 m/s |
| track_007 | 1.40 | 2.05 | 8 | 85.0 m / -13 deg | 85.02 m (1.55) | 85.0 m / -14 deg | 20.4 m/s |
| track_008 | 2.50 | 3.00 | 8 | 85.4 m / -13 deg | 85.37 m (2.55) | 85.4 m / -14 deg | 20.2 m/s |
| track_009 | 3.35 | 3.70 | 3 | 85.8 m / -13 deg | 85.82 m (3.35) | 85.9 m / -14 deg | 20.8 m/s |
| track_010 | 7.75 | 8.45 | 13 | 77.9 m / -21 deg | 77.87 m (7.75) | 87.1 m / -26 deg | 23.9 m/s |
| track_011 | 8.70 | 11.95 | 65 | 24.8 m / +158 deg | 4.04 m (10.15) | 29.0 m / -4 deg | 17.6 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_004, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: A's radar started tracking track_005, which appeared on its right.
- t = 0.00 s: A observed track_002 start closing in (already the case when first observed).
- t = 0.00 s: A observed track_003 start closing in (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_006, which appeared on its left.
- t = 0.60 s: A's radar lost track_006 (its states are UNKNOWN from then on, not ended).
- t = 1.40 s: A's radar started tracking track_007, which appeared on its left.
- t = 2.05 s: A's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 2.35 s: A's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 2.50 s: A's radar started tracking track_008, which appeared on its left.
- t = 3.00 s: A's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 3.35 s: A's radar started tracking track_009, which appeared on its left.
- t = 3.70 s: A's radar lost track_009 (its states are UNKNOWN from then on, not ended).
- t = 5.50 s: A's time-to-contact with track_002 became critical.
- t = 5.50 s: A observed track_002 cutting in from the right.
- t = 6.20 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 6.30 s: A observed track_002 enter its forward path corridor.
- t = 7.40 s: A observed track_003 stop closing in.
- t = 7.50 s: A's collision sensor recorded a contact (peak impulse 7449 N*s).
- t = 7.50 s: A's time-to-contact with track_002 stopped being critical.
- t = 7.50 s: A observed track_002 stop closing in.
- t = 7.55 s: A released the accelerator.
- t = 7.55 s: A started braking.
- t = 7.75 s: A's radar started tracking track_010, which appeared on its left.
- t = 8.35 s: A observed track_002's cut-in from the right settle.
- t = 8.45 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 8.45 s: A's radar lost track_010 (its states are UNKNOWN from then on, not ended).
- t = 8.70 s: A's radar started tracking track_011, which appeared on its right.
- t = 8.70 s: A observed track_011 start closing in (already the case when first observed).
- t = 8.95 s: A stopped moving.
- t = 8.95 s: A came to a stop.
- t = 10.30 s: A observed track_011 stop closing in.
- t = 11.90 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
