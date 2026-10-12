# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 497.58820490539074 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 5 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 25; edges: 50 (PRECEDES 37, SAME_TRACK 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e04 | 0.00 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e05 | 0.00 | TRACK_APPEARED_RIGHT | B | track_004 | radar |  |
| B:e06 | 0.00 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e07 | 0.00 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e08 | 0.05 | TRACK_APPEARED_RIGHT | B | track_003 | radar |  |
| B:e09 | 0.05 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e10 | 4.65 | TRACK_LOST | B | track_003 | radar |  |
| B:e11 | 5.55 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e12 | 5.65 | CLOSING_START | B | track_001 | radar |  |
| B:e13 | 6.20 | COLLISION | B | - | collision_sensor | peak_impulse=1097.53; merged_bursts=[[6.3, 199.68]] |
| B:e14 | 6.20 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e15 | 6.25 | THROTTLE_END | B | - | controls |  |
| B:e16 | 6.25 | BRAKE_START | B | - | controls |  |
| B:e17 | 6.35 | CLOSING_END | B | track_002 | radar |  |
| B:e18 | 6.35 | CLOSING_END | B | track_004 | radar |  |
| B:e19 | 6.50 | TRACK_APPEARED_RIGHT | B | track_005 | radar |  |
| B:e20 | 6.60 | CLOSING_END | B | track_001 | radar |  |
| B:e21 | 7.25 | MOVING_END | B | - | ego |  |
| B:e22 | 7.25 | STOP_START | B | - | ego |  |
| B:e23 | 8.55 | TRACK_LOST | B | track_005 | radar |  |
| B:e24 | 8.95 | TRACK_LOST | B | track_002 | radar |  |
| B:e25 | 9.55 | TRACK_LOST | B | track_004 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e08
    B:e01 --PRECEDES--> B:e09
    B:e02 --PRECEDES--> B:e08
    B:e02 --PRECEDES--> B:e09
    B:e03 --PRECEDES--> B:e08
    B:e03 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e09
    B:e05 --PRECEDES--> B:e08
    B:e05 --PRECEDES--> B:e09
    B:e06 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e04 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e07
    B:e08 --SAME_TRACK--> B:e09
    B:e08 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e11
    B:e03 --SAME_TRACK--> B:e12
    B:e03 --SAME_TRACK--> B:e14
    B:e04 --SAME_TRACK--> B:e17
    B:e05 --SAME_TRACK--> B:e18
    B:e03 --SAME_TRACK--> B:e20
    B:e19 --SAME_TRACK--> B:e23
    B:e04 --SAME_TRACK--> B:e24
    B:e05 --SAME_TRACK--> B:e25
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START<br>B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 TRACK_APPEARED_RIGHT track_002<br>B:e05 TRACK_APPEARED_RIGHT track_004<br>B:e06 CLOSING_START track_002<br>B:e07 CLOSING_START track_004 | ego: not yet observed | - |
| 0.05 | B:e08 TRACK_APPEARED_RIGHT track_003<br>B:e09 CLOSING_START track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC?<br>track_004: CLOSING, CRITICAL_TTC? | 0.00 |
| 4.65 | B:e10 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING | 4.60 |
| 5.55 | B:e11 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 | 5.50 |
| 5.65 | B:e12 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 | 5.60 |
| 6.20 | B:e13 COLLISION<br>B:e14 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 | 6.10 |
| 6.25 | B:e15 THROTTLE_END<br>B:e16 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 | 6.20 |
| 6.35 | B:e17 CLOSING_END track_002<br>B:e18 CLOSING_END track_004 | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING<br>track_004: CLOSING<br>track lost, states UNKNOWN: track_003 | 6.30 |
| 6.50 | B:e19 TRACK_APPEARED_RIGHT track_005 | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_003 | 6.40 |
| 6.60 | B:e20 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: no active state<br>track_004: no active state<br>track_005: CRITICAL_TTC?<br>track lost, states UNKNOWN: track_003 | 6.50 |
| 7.25 | B:e21 MOVING_END<br>B:e22 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_003 | 7.20 |
| 8.55 | B:e23 TRACK_LOST track_005 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track_005: no active state<br>track lost, states UNKNOWN: track_003 | 8.50 |
| 8.95 | B:e24 TRACK_LOST track_002 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_003, track_005 | 8.90 |
| 9.55 | B:e25 TRACK_LOST track_004 | ego: STOP, BRAKE<br>track_001: no active state<br>track_004: no active state<br>track lost, states UNKNOWN: track_002, track_003, track_005 | 9.50 |

## States still active when observation ended

- CLOSING of track_003, since B:e09 (t = 0.05 s); the track was lost at 4.65 s
- BRAKE, since B:e16 (t = 6.25 s)
- STOP, since B:e22 (t = 7.25 s)

## Tracks lost

- track_003 at 4.65 s (B:e10): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_005, track_002, track_004

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 5.55, COLLISION 6.20 (+0.65 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.45 | 230 | 4.4 m / +30 deg | 0.06 m (11.45) | 0.1 m / +93 deg | 12.3 m/s |
| track_002 | 0.00 | 8.95 | 174 | 20.8 m / +8 deg | 14.07 m (6.35) | 39.2 m / +9 deg | 13.8 m/s |
| track_003 | 0.05 | 4.65 | 81 | 29.0 m / +5 deg | 24.49 m (4.65) | 24.5 m / +7 deg | 12.0 m/s |
| track_004 | 0.00 | 9.55 | 130 | 23.4 m / +7 deg | 15.76 m (6.35) | 49.0 m / +8 deg | 13.9 m/s |
| track_005 | 6.50 | 8.55 | 26 | 23.0 m / +11 deg | 23.03 m (6.50) | 43.0 m / +8 deg | 14.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_002, which appeared on its right.
- t = 0.00 s: B's radar started tracking track_004, which appeared on its right.
- t = 0.00 s: B observed track_002 start closing in (already the case when first observed).
- t = 0.00 s: B observed track_004 start closing in (already the case when first observed).
- t = 0.05 s: B's radar started tracking track_003, which appeared on its right.
- t = 0.05 s: B observed track_003 start closing in (already the case when first observed).
- t = 4.65 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 5.55 s: B's time-to-contact with track_001 became critical.
- t = 5.65 s: B observed track_001 start closing in.
- t = 6.20 s: B's collision sensor recorded a contact (peak impulse 1098 N*s).
- t = 6.20 s: B's time-to-contact with track_001 stopped being critical.
- t = 6.25 s: B released the accelerator.
- t = 6.25 s: B started braking.
- t = 6.35 s: B observed track_002 stop closing in.
- t = 6.35 s: B observed track_004 stop closing in.
- t = 6.50 s: B's radar started tracking track_005, which appeared on its right.
- t = 6.60 s: B observed track_001 stop closing in.
- t = 7.25 s: B stopped moving.
- t = 7.25 s: B came to a stop.
- t = 8.55 s: B's radar lost track_005 (its states are UNKNOWN from then on, not ended).
- t = 8.95 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 9.55 s: B's radar lost track_004 (its states are UNKNOWN from then on, not ended).
