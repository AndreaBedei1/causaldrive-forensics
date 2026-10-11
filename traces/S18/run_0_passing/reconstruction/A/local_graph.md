# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 512.9178570024669 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 6 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 27; edges: 44 (PRECEDES 30, SAME_TRACK 14)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e04 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001#segment_1 | radar |  |
| A:e05 | 0.15 | TRACK_APPEARED_FRONT | A | track_003 | radar |  |
| A:e06 | 0.65 | CRITICAL_TTC_START | A | track_003 | radar |  |
| A:e07 | 1.90 | TRACK_LOST | A | track_001#segment_1 | radar |  |
| A:e08 | 1.95 | TRACK_APPEARED_RIGHT | A | track_001#segment_2 | radar |  |
| A:e09 | 3.50 | TRACK_LOST | A | track_003 | radar |  |
| A:e10 | 3.90 | TRACK_APPEARED_RIGHT | A | track_004 | radar |  |
| A:e11 | 4.25 | TRACK_LOST | A | track_001#segment_2 | radar |  |
| A:e12 | 4.30 | TRACK_APPEARED_FRONT | A | track_001#segment_3 | radar |  |
| A:e13 | 4.80 | CRITICAL_TTC_START | A | track_001#segment_3 | radar |  |
| A:e14 | 5.15 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e15 | 5.60 | CLOSING_START | A | track_002 | radar |  |
| A:e16 | 5.65 | EGO_PATH_EXIT | A | track_001#segment_3 | radar |  |
| A:e17 | 5.75 | CRITICAL_TTC_END | A | track_001#segment_3 | radar |  |
| A:e18 | 6.20 | COLLISION | A | - | collision_sensor | peak_impulse=1092.43; merged_bursts=[[6.3, 41.66]] |
| A:e19 | 6.20 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e20 | 6.25 | THROTTLE_END | A | - | controls |  |
| A:e21 | 6.25 | BRAKE_START | A | - | controls |  |
| A:e22 | 6.40 | CLOSING_END | A | track_002 | radar |  |
| A:e23 | 7.35 | MOVING_END | A | - | ego |  |
| A:e24 | 7.35 | STOP_START | A | - | ego |  |
| A:e25 | 9.70 | TRACK_LOST | A | track_004 | radar |  |
| A:e26 | 9.90 | CUT_IN_FROM_RIGHT_START | A | track_001#segment_3 | radar |  |
| A:e27 | 10.20 | TRACK_LOST | A | track_001#segment_3 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e05 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e05 --SAME_TRACK--> A:e09
    A:e08 --SAME_TRACK--> A:e11
    A:e12 --SAME_TRACK--> A:e13
    A:e03 --SAME_TRACK--> A:e14
    A:e03 --SAME_TRACK--> A:e15
    A:e12 --SAME_TRACK--> A:e16
    A:e12 --SAME_TRACK--> A:e17
    A:e03 --SAME_TRACK--> A:e19
    A:e03 --SAME_TRACK--> A:e22
    A:e10 --SAME_TRACK--> A:e25
    A:e12 --SAME_TRACK--> A:e26
    A:e12 --SAME_TRACK--> A:e27
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_LEFT track_002<br>A:e04 TRACK_APPEARED_RIGHT track_001#segment_1 | ego: not yet observed | - |
| 0.15 | A:e05 TRACK_APPEARED_FRONT track_003 | ego: MOVING, THROTTLE<br>track_001#segment_1: CRITICAL_TTC?<br>track_002: CRITICAL_TTC? | 0.10 |
| 0.65 | A:e06 CRITICAL_TTC_START track_003 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH, CRITICAL_TTC? | 0.60 |
| 1.90 | A:e07 TRACK_LOST track_001#segment_1 | ego: MOVING, THROTTLE<br>track_001#segment_1: no active state<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH | 1.80 |
| 1.95 | A:e08 TRACK_APPEARED_RIGHT track_001#segment_2 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 | 1.90 |
| 3.50 | A:e09 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_003: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 | 3.40 |
| 3.90 | A:e10 TRACK_APPEARED_RIGHT track_004 | ego: MOVING, THROTTLE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_003 | 3.80 |
| 4.25 | A:e11 TRACK_LOST track_001#segment_2 | ego: MOVING, THROTTLE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: no active state<br>track_004: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_003 | 4.20 |
| 4.30 | A:e12 TRACK_APPEARED_FRONT track_001#segment_3 | ego: MOVING, THROTTLE<br>track_002: no active state<br>track_004: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 4.20 |
| 4.80 | A:e13 CRITICAL_TTC_START track_001#segment_3 | ego: MOVING, THROTTLE<br>track_001#segment_3: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 4.70 |
| 5.15 | A:e14 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 5.10 |
| 5.60 | A:e15 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 5.50 |
| 5.65 | A:e16 EGO_PATH_EXIT track_001#segment_3 | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 5.60 |
| 5.75 | A:e17 CRITICAL_TTC_END track_001#segment_3 | ego: MOVING, THROTTLE<br>track_001#segment_3: CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 5.70 |
| 6.20 | A:e18 COLLISION<br>A:e19 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_001#segment_3: no active state<br>track_002: CLOSING, CRITICAL_TTC<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 6.10 |
| 6.25 | A:e20 THROTTLE_END<br>A:e21 BRAKE_START | ego: MOVING, THROTTLE<br>track_001#segment_3: no active state<br>track_002: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 6.20 |
| 6.40 | A:e22 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_001#segment_3: no active state<br>track_002: CLOSING<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 6.30 |
| 7.35 | A:e23 MOVING_END<br>A:e24 STOP_START | ego: MOVING, BRAKE<br>track_001#segment_3: no active state<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 7.30 |
| 9.70 | A:e25 TRACK_LOST track_004 | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003 | 9.60 |
| 9.90 | A:e26 CUT_IN_FROM_RIGHT_START track_001#segment_3 | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track_002: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003, track_004 | 9.80 |
| 10.20 | A:e27 TRACK_LOST track_001#segment_3 | ego: STOP, BRAKE<br>track_001#segment_3: CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_003, track_004 | 10.10 |

## States still active when observation ended

- CRITICAL_TTC of track_003, since A:e06 (t = 0.65 s); the track was lost at 3.50 s
- BRAKE, since A:e21 (t = 6.25 s)
- STOP, since A:e24 (t = 7.35 s)
- CUT_IN_FROM_RIGHT of track_001#segment_3, since A:e26 (t = 9.90 s); the track was lost at 10.20 s

## Tracks lost

- track_003 at 3.50 s (A:e09): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001#segment_3 at 10.20 s (A:e27): CUT_IN_FROM_RIGHT were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001#segment_1, track_001#segment_2, track_004

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001#segment_3: CUT_IN_FROM_RIGHT_START 9.90, no critical TTC after it
- track_002: CRITICAL_TTC_START 5.15, COLLISION 6.20 (+1.05 s)
- track_003: CRITICAL_TTC_START 0.65, COLLISION 6.20 (+5.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001#segment_1 | 0.00 | 1.90 | 39 | 13.2 m / +10 deg | 13.15 m (0.00) | 14.5 m / +11 deg | 12.7 m/s |
| track_001#segment_2 | 1.95 | 4.25 | 47 | 14.4 m / +11 deg | 14.39 m (1.95) | 15.4 m / -2 deg | 13.1 m/s |
| track_001#segment_3 | 4.30 | 10.20 | 106 | 15.6 m / +0 deg | 15.56 m (4.30) | 58.4 m / +3 deg | 14.4 m/s |
| track_002 | 0.00 | 11.45 | 230 | 5.5 m / -144 deg | 0.03 m (6.50) | 0.3 m / -90 deg | 12.8 m/s |
| track_003 | 0.15 | 3.50 | 68 | 15.3 m / -1 deg | 15.17 m (3.50) | 15.2 m / -1 deg | 11.8 m/s |
| track_004 | 3.90 | 9.70 | 99 | 16.4 m / +9 deg | 16.40 m (3.90) | 56.3 m / +7 deg | 14.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_001#segment_1, which appeared on its right.
- t = 0.15 s: A's radar started tracking track_003, which appeared in front of it.
- t = 0.65 s: A's time-to-contact with track_003 became critical.
- t = 1.90 s: A's radar lost track_001#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 1.95 s: A's radar started tracking track_001#segment_2, which appeared on its right.
- t = 3.50 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 3.90 s: A's radar started tracking track_004, which appeared on its right.
- t = 4.25 s: A's radar lost track_001#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 4.30 s: A's radar started tracking track_001#segment_3, which appeared in front of it.
- t = 4.80 s: A's time-to-contact with track_001#segment_3 became critical.
- t = 5.15 s: A's time-to-contact with track_002 became critical.
- t = 5.60 s: A observed track_002 start closing in.
- t = 5.65 s: A observed track_001#segment_3 leave its forward path corridor.
- t = 5.75 s: A's time-to-contact with track_001#segment_3 stopped being critical.
- t = 6.20 s: A's collision sensor recorded a contact (peak impulse 1092 N*s).
- t = 6.20 s: A's time-to-contact with track_002 stopped being critical.
- t = 6.25 s: A released the accelerator.
- t = 6.25 s: A started braking.
- t = 6.40 s: A observed track_002 stop closing in.
- t = 7.35 s: A stopped moving.
- t = 7.35 s: A came to a stop.
- t = 9.70 s: A's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 9.90 s: A observed track_001#segment_3 cutting in from the right.
- t = 10.20 s: A's radar lost track_001#segment_3 (its states are UNKNOWN from then on, not ended).
