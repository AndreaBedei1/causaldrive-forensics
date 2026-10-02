# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 144.63758319616318 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 40 (PRECEDES 32, SAME_TRACK 8)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 2.10 | TRACK_APPEARED_LEFT | B | track_002 | radar |  |
| B:e04 | 2.10 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e05 | 2.10 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 2.10 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e07 | 2.60 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e08 | 4.10 | COLLISION | B | - | collision_sensor | peak_impulse=12137.11; merged_bursts=[[4.35, 2340.56]] |
| B:e09 | 4.10 | CLOSING_END | B | track_002 | radar |  |
| B:e10 | 4.10 | TURN_RIGHT_START | B | - | ego |  |
| B:e11 | 4.15 | THROTTLE_END | B | - | controls |  |
| B:e12 | 4.15 | BRAKE_START | B | - | controls |  |
| B:e13 | 4.25 | CLOSING_START | B | track_002 | radar |  |
| B:e14 | 4.60 | CLOSING_END | B | track_001 | radar |  |
| B:e15 | 4.60 | TURN_RIGHT_END | B | - | ego |  |
| B:e16 | 4.60 | MOVING_END | B | - | ego |  |
| B:e17 | 4.60 | STOP_START | B | - | ego |  |
| B:e18 | 4.65 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e19 | 4.75 | CLOSING_END | B | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e01 --PRECEDES--> B:e04
    B:e01 --PRECEDES--> B:e05
    B:e01 --PRECEDES--> B:e06
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e05
    B:e02 --PRECEDES--> B:e06
    B:e03 --PRECEDES--> B:e07
    B:e04 --PRECEDES--> B:e07
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e04 --SAME_TRACK--> B:e05
    B:e03 --SAME_TRACK--> B:e06
    B:e03 --SAME_TRACK--> B:e07
    B:e03 --SAME_TRACK--> B:e09
    B:e03 --SAME_TRACK--> B:e13
    B:e04 --SAME_TRACK--> B:e14
    B:e03 --SAME_TRACK--> B:e18
    B:e03 --SAME_TRACK--> B:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START | ego: not yet observed | - |
| 2.10 | B:e03 TRACK_APPEARED_LEFT track_002<br>B:e04 TRACK_APPEARED_RIGHT track_001<br>B:e05 CLOSING_START track_001<br>B:e06 CLOSING_START track_002 | ego: MOVING, THROTTLE | 2.00 |
| 2.60 | B:e07 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?<br>track_002: CLOSING, CRITICAL_TTC? | 2.50 |
| 4.10 | B:e08 COLLISION<br>B:e09 CLOSING_END track_002<br>B:e10 TURN_RIGHT_START | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 4.00 |
| 4.15 | B:e11 THROTTLE_END<br>B:e12 BRAKE_START | ego: MOVING, THROTTLE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CRITICAL_TTC | 4.10 |
| 4.25 | B:e13 CLOSING_START track_002 | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CRITICAL_TTC | 4.20 |
| 4.60 | B:e14 CLOSING_END track_001<br>B:e15 TURN_RIGHT_END<br>B:e16 MOVING_END<br>B:e17 STOP_START | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 4.50 |
| 4.65 | B:e18 CRITICAL_TTC_END track_002 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC | 4.60 |
| 4.75 | B:e19 CLOSING_END track_002 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: CLOSING | 4.70 |

## States still active when observation ended

- BRAKE, since B:e12 (t = 4.15 s)
- STOP, since B:e17 (t = 4.60 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 2.60, COLLISION 4.10 (+1.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.10 | 15.15 | 262 | 33.3 m / +28 deg | 9.22 m (11.65) | 10.3 m / +37 deg | 6.4 m/s |
| track_002 | 2.10 | 15.15 | 262 | 32.5 m / -39 deg | 0.64 m (4.60) | 0.7 m / -72 deg | 10.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 2.10 s: B's radar started tracking track_002, which appeared on its left.
- t = 2.10 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.10 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.10 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.60 s: B's time-to-contact with track_002 became critical.
- t = 4.10 s: B's collision sensor recorded a contact (peak impulse 12137 N*s).
- t = 4.10 s: B observed track_002 stop closing in.
- t = 4.10 s: B started turning right.
- t = 4.15 s: B released the accelerator.
- t = 4.15 s: B started braking.
- t = 4.25 s: B observed track_002 start closing in.
- t = 4.60 s: B observed track_001 stop closing in.
- t = 4.60 s: B stopped turning right.
- t = 4.60 s: B stopped moving.
- t = 4.60 s: B came to a stop.
- t = 4.65 s: B's time-to-contact with track_002 stopped being critical.
- t = 4.75 s: B observed track_002 stop closing in.
