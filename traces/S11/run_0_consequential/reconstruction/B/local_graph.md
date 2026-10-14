# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 224.2758263722062 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 5 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 23; edges: 41 (PRECEDES 30, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 0.30 | TRACK_APPEARED_LEFT | B | track_002#segment_1 | radar | initial_in_ego_path=False |
| B:e05 | 0.30 | CLOSING_START | B | track_002#segment_1 | radar | active_at_first_observation=True |
| B:e06 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 3.25 | EGO_PATH_ENTRY | B | track_002#segment_1 | radar | geometry=estimated_body |
| B:e08 | 4.15 | CLOSING_START | B | track_001 | radar |  |
| B:e09 | 5.40 | THROTTLE_END | B | - | controls |  |
| B:e10 | 5.40 | BRAKE_START | B | - | controls |  |
| B:e11 | 5.55 | COLLISION | B | - | collision_sensor | peak_impulse=4243.51 |
| B:e12 | 5.55 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e13 | 5.70 | CLOSING_END | B | track_001 | radar |  |
| B:e14 | 5.80 | CLOSING_END | B | track_002#segment_1 | radar |  |
| B:e15 | 5.80 | TRACK_LOST | B | track_002#segment_1 | radar |  |
| B:e16 | 5.85 | TRACK_APPEARED_LEFT | B | track_002#segment_2 | radar | initial_in_ego_path=False |
| B:e17 | 6.20 | MOVING_END | B | - | ego |  |
| B:e18 | 6.20 | STOP_START | B | - | ego |  |
| B:e19 | 6.40 | TRACK_APPEARED_LEFT | B | track_003 | radar | initial_in_ego_path=False |
| B:e20 | 7.10 | TRACK_LOST | B | track_001 | radar |  |
| B:e21 | 7.15 | TRACK_LOST | B | track_003 | radar |  |
| B:e22 | 7.70 | TRACK_LOST | B | track_002#segment_2 | radar |  |
| B:e23 | 7.75 | TRACK_APPEARED_LEFT | B | track_002#segment_3 | radar | initial_in_ego_path=False |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e04
    B:e01 --PRECEDES--> B:e05
    B:e02 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e04 --SAME_TRACK--> B:e05
    B:e03 --SAME_TRACK--> B:e06
    B:e04 --SAME_TRACK--> B:e07
    B:e03 --SAME_TRACK--> B:e08
    B:e03 --SAME_TRACK--> B:e12
    B:e03 --SAME_TRACK--> B:e13
    B:e04 --SAME_TRACK--> B:e14
    B:e04 --SAME_TRACK--> B:e15
    B:e03 --SAME_TRACK--> B:e20
    B:e19 --SAME_TRACK--> B:e21
    B:e16 --SAME_TRACK--> B:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001 | ego: not yet observed | - |
| 0.30 | B:e04 TRACK_APPEARED_LEFT track_002#segment_1<br>B:e05 CLOSING_START track_002#segment_1 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC? | 0.20 |
| 0.50 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002#segment_1: CLOSING, CRITICAL_TTC? | 0.40 |
| 3.25 | B:e07 EGO_PATH_ENTRY track_002#segment_1 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002#segment_1: CLOSING | 3.20 |
| 4.15 | B:e08 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002#segment_1: CLOSING, IN_EGO_PATH | 4.10 |
| 5.40 | B:e09 THROTTLE_END<br>B:e10 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002#segment_1: CLOSING, IN_EGO_PATH | 5.30 |
| 5.55 | B:e11 COLLISION<br>B:e12 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002#segment_1: CLOSING, IN_EGO_PATH | 5.50 |
| 5.70 | B:e13 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002#segment_1: CLOSING, IN_EGO_PATH | 5.60 |
| 5.80 | B:e14 CLOSING_END track_002#segment_1<br>B:e15 TRACK_LOST track_002#segment_1 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002#segment_1: CLOSING, IN_EGO_PATH | 5.70 |
| 5.85 | B:e16 TRACK_APPEARED_LEFT track_002#segment_2 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002#segment_1 | 5.80 |
| 6.20 | B:e17 MOVING_END<br>B:e18 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002#segment_1 | 6.10 |
| 6.40 | B:e19 TRACK_APPEARED_LEFT track_003 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002#segment_1 | 6.30 |
| 7.10 | B:e20 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: no active state<br>track lost, states UNKNOWN: track_002#segment_1 | 7.00 |
| 7.15 | B:e21 TRACK_LOST track_003 | ego: STOP, BRAKE<br>track_002#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: no active state<br>track lost, states UNKNOWN: track_001, track_002#segment_1 | 7.10 |
| 7.70 | B:e22 TRACK_LOST track_002#segment_2 | ego: STOP, BRAKE<br>track_002#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_002#segment_1, track_003 | 7.60 |
| 7.75 | B:e23 TRACK_APPEARED_LEFT track_002#segment_3 | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001, track_002#segment_1, track_002#segment_2, track_003 | 7.70 |

## States still active when observation ended

- EGO_PATH of track_002#segment_1, since B:e07 (t = 3.25 s); the track was lost at 5.80 s
- BRAKE, since B:e10 (t = 5.40 s)
- STOP, since B:e18 (t = 6.20 s)

## Tracks lost

- track_002#segment_1 at 5.80 s (B:e15): CLOSING, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_001 at 7.10 s (B:e20): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003, track_002#segment_2

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 5.55 (+5.05 s)
- track_002#segment_1: EGO_PATH_ENTRY 3.25, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 7.10 | 142 | 7.5 m / +0 deg | 0.18 m (5.50) | 10.8 m / -7 deg | 11.9 m/s |
| track_002#segment_1 | 0.30 | 5.80 | 109 | 24.4 m / -7 deg | 6.58 m (5.55) | 8.0 m / -28 deg | 8.8 m/s |
| track_002#segment_2 | 5.85 | 7.70 | 38 | 7.8 m / -40 deg | 7.65 m (6.15) | 8.0 m / -57 deg | 8.2 m/s |
| track_002#segment_3 | 7.75 | 11.95 | 85 | 7.7 m / -58 deg | 7.64 m (11.80) | 7.6 m / -60 deg | 0.2 m/s |
| track_003 | 6.40 | 7.15 | 16 | 10.1 m / -16 deg | 10.05 m (6.40) | 16.0 m / -11 deg | 9.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.30 s: B's radar started tracking track_002#segment_1, which appeared on its left.
- t = 0.30 s: B observed track_002#segment_1 start closing in (already the case when first observed).
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 3.25 s: B observed track_002#segment_1 enter its forward path corridor.
- t = 4.15 s: B observed track_001 start closing in.
- t = 5.40 s: B released the accelerator.
- t = 5.40 s: B started braking.
- t = 5.55 s: B's collision sensor recorded a contact (peak impulse 4244 N*s).
- t = 5.55 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.70 s: B observed track_001 stop closing in.
- t = 5.80 s: B observed track_002#segment_1 stop closing in.
- t = 5.80 s: B's radar lost track_002#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 5.85 s: B's radar started tracking track_002#segment_2, which appeared on its left.
- t = 6.20 s: B stopped moving.
- t = 6.20 s: B came to a stop.
- t = 6.40 s: B's radar started tracking track_003, which appeared on its left.
- t = 7.10 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 7.15 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 7.70 s: B's radar lost track_002#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 7.75 s: B's radar started tracking track_002#segment_3, which appeared on its left.
