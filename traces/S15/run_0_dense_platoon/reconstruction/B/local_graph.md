# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 184.6674646884203 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 10 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 26; edges: 44 (PRECEDES 32, SAME_TRACK 12)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_LEFT | B | track_001#segment_1 | radar | initial_in_ego_path=False |
| B:e04 | 0.00 | TRACK_APPEARED_LEFT | B | track_002 | radar | initial_in_ego_path=False |
| B:e05 | 0.00 | TRACK_APPEARED_LEFT | B | track_005 | radar | initial_in_ego_path=False |
| B:e06 | 0.00 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=False |
| B:e07 | 0.00 | TRACK_APPEARED_RIGHT | B | track_004 | radar | initial_in_ego_path=False |
| B:e08 | 0.05 | TRACK_APPEARED_FRONT | B | track_006 | radar | initial_in_ego_path=True |
| B:e09 | 0.30 | TRACK_APPEARED_RIGHT | B | track_007 | radar | initial_in_ego_path=False |
| B:e10 | 0.55 | CRITICAL_TTC_START | B | track_006 | radar |  |
| B:e11 | 3.55 | TRACK_LOST | B | track_007 | radar |  |
| B:e12 | 3.70 | TRACK_LOST | B | track_002 | radar |  |
| B:e13 | 6.20 | CLOSING_START | B | track_006 | radar |  |
| B:e14 | 6.30 | TRACK_APPEARED_LEFT | B | track_008 | radar | initial_in_ego_path=False |
| B:e15 | 6.75 | TRACK_LOST | B | track_008 | radar |  |
| B:e16 | 7.40 | TRACK_LOST | B | track_004 | radar |  |
| B:e17 | 7.40 | TRACK_LOST | B | track_005 | radar |  |
| B:e18 | 7.45 | COLLISION | B | - | collision_sensor | peak_impulse=34836.87 |
| B:e19 | 7.45 | CRITICAL_TTC_END | B | track_006 | radar |  |
| B:e20 | 7.45 | CLOSING_END | B | track_006 | radar |  |
| B:e21 | 7.45 | TRACK_LOST | B | track_003 | radar |  |
| B:e22 | 7.50 | THROTTLE_END | B | - | controls |  |
| B:e23 | 8.25 | TRACK_LOST | B | track_001#segment_1 | radar |  |
| B:e24 | 8.30 | TRACK_APPEARED_LEFT | B | track_001#segment_2 | radar | initial_in_ego_path=False |
| B:e25 | 11.70 | TRACK_LOST | B | track_001#segment_2 | radar |  |
| B:e26 | 11.75 | TRACK_APPEARED_LEFT | B | track_001#segment_3 | radar | initial_in_ego_path=False |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e16 --PRECEDES--> B:e20
    B:e16 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e17 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e08 --SAME_TRACK--> B:e10
    B:e09 --SAME_TRACK--> B:e11
    B:e04 --SAME_TRACK--> B:e12
    B:e08 --SAME_TRACK--> B:e13
    B:e14 --SAME_TRACK--> B:e15
    B:e07 --SAME_TRACK--> B:e16
    B:e05 --SAME_TRACK--> B:e17
    B:e08 --SAME_TRACK--> B:e19
    B:e08 --SAME_TRACK--> B:e20
    B:e06 --SAME_TRACK--> B:e21
    B:e03 --SAME_TRACK--> B:e23
    B:e24 --SAME_TRACK--> B:e25
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_LEFT track_001#segment_1<br>B:e04 TRACK_APPEARED_LEFT track_002<br>B:e05 TRACK_APPEARED_LEFT track_005<br>B:e06 TRACK_APPEARED_RIGHT track_003<br>B:e07 TRACK_APPEARED_RIGHT track_004 | ego: not yet observed | - |
| 0.05 | B:e08 TRACK_APPEARED_FRONT track_006 | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC? | 0.00 |
| 0.30 | B:e09 TRACK_APPEARED_RIGHT track_007 | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?<br>track_002: CRITICAL_TTC?<br>track_003: CRITICAL_TTC?<br>track_004: CRITICAL_TTC?<br>track_005: CRITICAL_TTC?<br>track_006: IN_EGO_PATH, CRITICAL_TTC? | 0.20 |
| 0.55 | B:e10 CRITICAL_TTC_START track_006 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: IN_EGO_PATH, CRITICAL_TTC?<br>track_007: CRITICAL_TTC? | 0.50 |
| 3.55 | B:e11 TRACK_LOST track_007 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track_007: no active state | 3.50 |
| 3.70 | B:e12 TRACK_LOST track_002 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_007 | 3.60 |
| 6.20 | B:e13 CLOSING_START track_006 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_007 | 6.10 |
| 6.30 | B:e14 TRACK_APPEARED_LEFT track_008 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_007 | 6.20 |
| 6.75 | B:e15 TRACK_LOST track_008 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_002, track_007 | 6.70 |
| 7.40 | B:e16 TRACK_LOST track_004<br>B:e17 TRACK_LOST track_005 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_007, track_008 | 7.30 |
| 7.45 | B:e18 COLLISION<br>B:e19 CRITICAL_TTC_END track_006<br>B:e20 CLOSING_END track_006<br>B:e21 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_003: no active state<br>track_006: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_004, track_005, track_007, track_008 | 7.40 |
| 7.50 | B:e22 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_007, track_008 | 7.40 |
| 8.25 | B:e23 TRACK_LOST track_001#segment_1 | ego: MOVING<br>track_001#segment_1: no active state<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002, track_003, track_004, track_005, track_007, track_008 | 8.20 |
| 8.30 | B:e24 TRACK_APPEARED_LEFT track_001#segment_2 | ego: MOVING<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005, track_007, track_008 | 8.20 |
| 11.70 | B:e25 TRACK_LOST track_001#segment_2 | ego: MOVING<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_002, track_003, track_004, track_005, track_007, track_008 | 11.60 |
| 11.75 | B:e26 TRACK_APPEARED_LEFT track_001#segment_3 | ego: MOVING<br>track_006: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002, track_003, track_004, track_005, track_007, track_008 | 11.70 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)

## Tracks lost

- lost with no state active: track_007, track_002, track_008, track_004, track_005, track_003, track_001#segment_1, track_001#segment_2

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_006: CRITICAL_TTC_START 0.55, COLLISION 7.45 (+6.90 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001#segment_1 | 0.00 | 8.25 | 166 | 3.2 m / -33 deg | 3.22 m (0.75) | 5.6 m / -56 deg | 11.9 m/s |
| track_001#segment_2 | 8.30 | 11.70 | 69 | 5.9 m / -60 deg | 5.87 m (8.30) | 8.7 m / -48 deg | 1.5 m/s |
| track_001#segment_3 | 11.75 | 11.95 | 5 | 7.8 m / -48 deg | 7.75 m (11.75) | 8.0 m / -46 deg | 0.0 m/s |
| track_002 | 0.00 | 3.70 | 69 | 25.8 m / -7 deg | 25.69 m (0.75) | 25.9 m / -7 deg | 12.0 m/s |
| track_003 | 0.00 | 7.45 | 150 | 4.6 m / +27 deg | 4.15 m (5.45) | 6.0 m / +30 deg | 12.1 m/s |
| track_004 | 0.00 | 7.40 | 136 | 16.3 m / +10 deg | 16.21 m (0.75) | 17.0 m / +10 deg | 12.2 m/s |
| track_005 | 0.00 | 7.40 | 145 | 14.0 m / -10 deg | 13.41 m (4.15) | 13.6 m / -11 deg | 12.3 m/s |
| track_006 | 0.05 | 11.95 | 239 | 7.7 m / -0 deg | 0.12 m (7.45) | 9.3 m / +1 deg | 12.1 m/s |
| track_007 | 0.30 | 3.55 | 55 | 27.8 m / +7 deg | 27.71 m (0.80) | 27.9 m / +6 deg | 11.9 m/s |
| track_008 | 6.30 | 6.75 | 9 | 26.3 m / -7 deg | 26.32 m (6.75) | 26.3 m / -8 deg | 11.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001#segment_1, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_005, which appeared on its left.
- t = 0.00 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.05 s: B's radar started tracking track_006, which appeared in front of it.
- t = 0.30 s: B's radar started tracking track_007, which appeared on its right.
- t = 0.55 s: B's time-to-contact with track_006 became critical.
- t = 3.55 s: B's radar lost track_007 (its states are UNKNOWN from then on, not ended).
- t = 3.70 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 6.20 s: B observed track_006 start closing in.
- t = 6.30 s: B's radar started tracking track_008, which appeared on its left.
- t = 6.75 s: B's radar lost track_008 (its states are UNKNOWN from then on, not ended).
- t = 7.40 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 7.40 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 7.45 s: B's collision sensor recorded a contact (peak impulse 34837 N*s).
- t = 7.45 s: B's time-to-contact with track_006 stopped being critical.
- t = 7.45 s: B observed track_006 stop closing in.
- t = 7.45 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 7.50 s: B released the accelerator.
- t = 8.25 s: B's radar lost track_001#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 8.30 s: B's radar started tracking track_001#segment_2, which appeared on its left.
- t = 11.70 s: B's radar lost track_001#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 11.75 s: B's radar started tracking track_001#segment_3, which appeared on its left.
