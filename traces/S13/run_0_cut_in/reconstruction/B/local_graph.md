# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 93.77468854188919 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 5 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 22; edges: 95 (PRECEDES 85, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.80 | BRAKE_START | B | - | controls |  |
| B:e03 | 5.25 | COLLISION | B | - | collision_sensor | peak_impulse=3184.37 |
| B:e04 | 5.45 | TURN_RIGHT_START | B | - | ego |  |
| B:e05 | 5.95 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e06 | 5.95 | TRACK_APPEARED_RIGHT | B | track_002 | radar |  |
| B:e07 | 5.95 | TRACK_APPEARED_RIGHT | B | track_003 | radar |  |
| B:e08 | 5.95 | TRACK_APPEARED_RIGHT | B | track_004 | radar |  |
| B:e09 | 5.95 | TRACK_APPEARED_RIGHT | B | track_005 | radar |  |
| B:e10 | 5.95 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e11 | 5.95 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e12 | 5.95 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e13 | 5.95 | CLOSING_START | B | track_004 | radar | active_at_first_observation=True |
| B:e14 | 5.95 | CLOSING_START | B | track_005 | radar | active_at_first_observation=True |
| B:e15 | 6.40 | CLOSING_END | B | track_001 | radar |  |
| B:e16 | 6.40 | CLOSING_END | B | track_002 | radar |  |
| B:e17 | 6.40 | CLOSING_END | B | track_003 | radar |  |
| B:e18 | 6.40 | CLOSING_END | B | track_004 | radar |  |
| B:e19 | 6.40 | CLOSING_END | B | track_005 | radar |  |
| B:e20 | 6.40 | TURN_RIGHT_END | B | - | ego |  |
| B:e21 | 6.45 | MOVING_END | B | - | ego |  |
| B:e22 | 6.45 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e08
    B:e04 --PRECEDES--> B:e09
    B:e04 --PRECEDES--> B:e10
    B:e04 --PRECEDES--> B:e11
    B:e04 --PRECEDES--> B:e12
    B:e04 --PRECEDES--> B:e13
    B:e04 --PRECEDES--> B:e14
    B:e05 --PRECEDES--> B:e15
    B:e05 --PRECEDES--> B:e16
    B:e05 --PRECEDES--> B:e17
    B:e05 --PRECEDES--> B:e18
    B:e05 --PRECEDES--> B:e19
    B:e05 --PRECEDES--> B:e20
    B:e06 --PRECEDES--> B:e15
    B:e06 --PRECEDES--> B:e16
    B:e06 --PRECEDES--> B:e17
    B:e06 --PRECEDES--> B:e18
    B:e06 --PRECEDES--> B:e19
    B:e06 --PRECEDES--> B:e20
    B:e07 --PRECEDES--> B:e15
    B:e07 --PRECEDES--> B:e16
    B:e07 --PRECEDES--> B:e17
    B:e07 --PRECEDES--> B:e18
    B:e07 --PRECEDES--> B:e19
    B:e07 --PRECEDES--> B:e20
    B:e08 --PRECEDES--> B:e15
    B:e08 --PRECEDES--> B:e16
    B:e08 --PRECEDES--> B:e17
    B:e08 --PRECEDES--> B:e18
    B:e08 --PRECEDES--> B:e19
    B:e08 --PRECEDES--> B:e20
    B:e09 --PRECEDES--> B:e15
    B:e09 --PRECEDES--> B:e16
    B:e09 --PRECEDES--> B:e17
    B:e09 --PRECEDES--> B:e18
    B:e09 --PRECEDES--> B:e19
    B:e09 --PRECEDES--> B:e20
    B:e10 --PRECEDES--> B:e15
    B:e10 --PRECEDES--> B:e16
    B:e10 --PRECEDES--> B:e17
    B:e10 --PRECEDES--> B:e18
    B:e10 --PRECEDES--> B:e19
    B:e10 --PRECEDES--> B:e20
    B:e11 --PRECEDES--> B:e15
    B:e11 --PRECEDES--> B:e16
    B:e11 --PRECEDES--> B:e17
    B:e11 --PRECEDES--> B:e18
    B:e11 --PRECEDES--> B:e19
    B:e11 --PRECEDES--> B:e20
    B:e12 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e16
    B:e12 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e18
    B:e12 --PRECEDES--> B:e19
    B:e12 --PRECEDES--> B:e20
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e13 --PRECEDES--> B:e18
    B:e13 --PRECEDES--> B:e19
    B:e13 --PRECEDES--> B:e20
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e18
    B:e14 --PRECEDES--> B:e19
    B:e14 --PRECEDES--> B:e20
    B:e15 --PRECEDES--> B:e21
    B:e15 --PRECEDES--> B:e22
    B:e16 --PRECEDES--> B:e21
    B:e16 --PRECEDES--> B:e22
    B:e17 --PRECEDES--> B:e21
    B:e17 --PRECEDES--> B:e22
    B:e18 --PRECEDES--> B:e21
    B:e18 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e05 --SAME_TRACK--> B:e10
    B:e06 --SAME_TRACK--> B:e11
    B:e07 --SAME_TRACK--> B:e12
    B:e08 --SAME_TRACK--> B:e13
    B:e09 --SAME_TRACK--> B:e14
    B:e05 --SAME_TRACK--> B:e15
    B:e06 --SAME_TRACK--> B:e16
    B:e07 --SAME_TRACK--> B:e17
    B:e08 --SAME_TRACK--> B:e18
    B:e09 --SAME_TRACK--> B:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.80 | B:e02 BRAKE_START | ego: MOVING | 0.70 |
| 5.25 | B:e03 COLLISION | ego: MOVING, BRAKE | 5.20 |
| 5.45 | B:e04 TURN_RIGHT_START | ego: MOVING, BRAKE | 5.40 |
| 5.95 | B:e05 TRACK_APPEARED_RIGHT track_001<br>B:e06 TRACK_APPEARED_RIGHT track_002<br>B:e07 TRACK_APPEARED_RIGHT track_003<br>B:e08 TRACK_APPEARED_RIGHT track_004<br>B:e09 TRACK_APPEARED_RIGHT track_005<br>B:e10 CLOSING_START track_001<br>B:e11 CLOSING_START track_002<br>B:e12 CLOSING_START track_003<br>B:e13 CLOSING_START track_004<br>B:e14 CLOSING_START track_005 | ego: MOVING, BRAKE, TURN_RIGHT | 5.90 |
| 6.40 | B:e15 CLOSING_END track_001<br>B:e16 CLOSING_END track_002<br>B:e17 CLOSING_END track_003<br>B:e18 CLOSING_END track_004<br>B:e19 CLOSING_END track_005<br>B:e20 TURN_RIGHT_END | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING | 6.30 |
| 6.45 | B:e21 MOVING_END<br>B:e22 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state | 6.40 |

## States still active when observation ended

- BRAKE, since B:e02 (t = 0.80 s)
- STOP, since B:e22 (t = 6.45 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 5.95 | 9.95 | 81 | 9.0 m / +72 deg | 7.88 m (6.60) | 7.9 m / +69 deg | 1.7 m/s |
| track_002 | 5.95 | 9.95 | 81 | 14.1 m / +76 deg | 11.97 m (9.95) | 12.0 m / +73 deg | 1.6 m/s |
| track_003 | 5.95 | 9.95 | 81 | 12.0 m / +75 deg | 10.67 m (9.95) | 10.7 m / +54 deg | 1.7 m/s |
| track_004 | 5.95 | 9.95 | 54 | 22.3 m / +60 deg | 20.67 m (6.60) | 20.8 m / +53 deg | 1.1 m/s |
| track_005 | 5.95 | 9.95 | 75 | 34.2 m / +73 deg | 32.91 m (6.50) | 33.0 m / +65 deg | 1.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.80 s: B started braking.
- t = 5.25 s: B's collision sensor recorded a contact (peak impulse 3184 N*s).
- t = 5.45 s: B started turning right.
- t = 5.95 s: B's radar started tracking track_001, which appeared on its right.
- t = 5.95 s: B's radar started tracking track_002, which appeared on its right.
- t = 5.95 s: B's radar started tracking track_003, which appeared on its right.
- t = 5.95 s: B's radar started tracking track_004, which appeared on its right.
- t = 5.95 s: B's radar started tracking track_005, which appeared on its right.
- t = 5.95 s: B observed track_001 start closing in (already the case when first observed).
- t = 5.95 s: B observed track_002 start closing in (already the case when first observed).
- t = 5.95 s: B observed track_003 start closing in (already the case when first observed).
- t = 5.95 s: B observed track_004 start closing in (already the case when first observed).
- t = 5.95 s: B observed track_005 start closing in (already the case when first observed).
- t = 6.40 s: B observed track_001 stop closing in.
- t = 6.40 s: B observed track_002 stop closing in.
- t = 6.40 s: B observed track_003 stop closing in.
- t = 6.40 s: B observed track_004 stop closing in.
- t = 6.40 s: B observed track_005 stop closing in.
- t = 6.40 s: B stopped turning right.
- t = 6.45 s: B stopped moving.
- t = 6.45 s: B came to a stop.
