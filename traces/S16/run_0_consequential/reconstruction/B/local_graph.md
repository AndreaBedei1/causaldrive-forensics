# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 224.2758263722062 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 4 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 21; edges: 33 (PRECEDES 23, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar |  |
| B:e04 | 0.00 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e05 | 0.00 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e06 | 0.50 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 0.85 | TRACK_APPEARED_LEFT | B | track_003 | radar |  |
| B:e08 | 0.85 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e09 | 4.15 | CLOSING_START | B | track_001 | radar |  |
| B:e10 | 4.85 | TRACK_LOST | B | track_003 | radar |  |
| B:e11 | 5.40 | THROTTLE_END | B | - | controls |  |
| B:e12 | 5.40 | BRAKE_START | B | - | controls |  |
| B:e13 | 5.55 | COLLISION | B | - | collision_sensor | peak_impulse=4243.51 |
| B:e14 | 5.60 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e15 | 5.65 | CLOSING_END | B | track_001 | radar |  |
| B:e16 | 5.80 | CLOSING_END | B | track_002 | radar |  |
| B:e17 | 6.20 | MOVING_END | B | - | ego |  |
| B:e18 | 6.20 | STOP_START | B | - | ego |  |
| B:e19 | 6.80 | TRACK_APPEARED_LEFT | B | track_004 | radar |  |
| B:e20 | 7.10 | TRACK_LOST | B | track_004 | radar |  |
| B:e21 | 7.25 | EGO_PATH_EXIT | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e04 --SAME_TRACK--> B:e05
    B:e03 --SAME_TRACK--> B:e06
    B:e07 --SAME_TRACK--> B:e08
    B:e03 --SAME_TRACK--> B:e09
    B:e07 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e14
    B:e03 --SAME_TRACK--> B:e15
    B:e04 --SAME_TRACK--> B:e16
    B:e19 --SAME_TRACK--> B:e20
    B:e03 --SAME_TRACK--> B:e21
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_FRONT track_001<br>B:e04 TRACK_APPEARED_LEFT track_002<br>B:e05 CLOSING_START track_002 | ego: not yet observed | - |
| 0.50 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? | 0.40 |
| 0.85 | B:e07 TRACK_APPEARED_LEFT track_003<br>B:e08 CLOSING_START track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING | 0.80 |
| 4.15 | B:e09 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING | 4.10 |
| 4.85 | B:e10 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track_003: CLOSING | 4.80 |
| 5.40 | B:e11 THROTTLE_END<br>B:e12 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 | 5.30 |
| 5.55 | B:e13 COLLISION | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 | 5.50 |
| 5.60 | B:e14 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 | 5.50 |
| 5.65 | B:e15 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 | 5.60 |
| 5.80 | B:e16 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_003 | 5.70 |
| 6.20 | B:e17 MOVING_END<br>B:e18 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 | 6.10 |
| 6.80 | B:e19 TRACK_APPEARED_LEFT track_004 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003 | 6.70 |
| 7.10 | B:e20 TRACK_LOST track_004 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track_004: CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_003 | 7.00 |
| 7.25 | B:e21 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: no active state<br>track lost, states UNKNOWN: track_003, track_004 | 7.20 |

## States still active when observation ended

- CLOSING of track_003, since B:e08 (t = 0.85 s); the track was lost at 4.85 s
- BRAKE, since B:e12 (t = 5.40 s)
- STOP, since B:e18 (t = 6.20 s)

## Tracks lost

- track_003 at 4.85 s (B:e10): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_004

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.50, COLLISION 5.55 (+5.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 7.5 m / +0 deg | 0.34 m (5.50) | 12.6 m / -8 deg | 11.9 m/s |
| track_002 | 0.00 | 11.95 | 231 | 25.5 m / -8 deg | 6.60 m (5.55) | 16.5 m / -11 deg | 10.2 m/s |
| track_003 | 0.85 | 4.85 | 41 | 26.3 m / -9 deg | 11.57 m (4.85) | 11.6 m / -11 deg | 8.8 m/s |
| track_004 | 6.80 | 7.10 | 6 | 16.5 m / -6 deg | 16.47 m (6.80) | 18.8 m / -6 deg | 8.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: B observed track_002 start closing in (already the case when first observed).
- t = 0.50 s: B's time-to-contact with track_001 became critical.
- t = 0.85 s: B's radar started tracking track_003, which appeared on its left.
- t = 0.85 s: B observed track_003 start closing in (already the case when first observed).
- t = 4.15 s: B observed track_001 start closing in.
- t = 4.85 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 5.40 s: B released the accelerator.
- t = 5.40 s: B started braking.
- t = 5.55 s: B's collision sensor recorded a contact (peak impulse 4244 N*s).
- t = 5.60 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.65 s: B observed track_001 stop closing in.
- t = 5.80 s: B observed track_002 stop closing in.
- t = 6.20 s: B stopped moving.
- t = 6.20 s: B came to a stop.
- t = 6.80 s: B's radar started tracking track_004, which appeared on its left.
- t = 7.10 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
- t = 7.25 s: B observed track_001 leave its forward path corridor.
