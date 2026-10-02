# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 23.313608441501856 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 26 (PRECEDES 20, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TURN_RIGHT_START | B | - | ego | active_at_first_observation=True |
| B:e03 | 0.00 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e04 | 0.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 0.00 | CRITICAL_TTC_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 0.85 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e07 | 1.20 | TURN_RIGHT_END | B | - | ego |  |
| B:e08 | 1.45 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e09 | 1.80 | COLLISION | B | - | collision_sensor | peak_impulse=1247.19 |
| B:e10 | 1.80 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e11 | 1.80 | CLOSING_END | B | track_001 | radar |  |
| B:e12 | 1.85 | BRAKE_START | B | - | controls |  |
| B:e13 | 1.85 | TURN_LEFT_START | B | - | ego |  |
| B:e14 | 2.50 | TURN_LEFT_END | B | - | ego |  |
| B:e15 | 2.55 | MOVING_END | B | - | ego |  |
| B:e16 | 2.55 | STOP_START | B | - | ego |  |

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
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e05
    B:e03 --SAME_TRACK--> B:e06
    B:e03 --SAME_TRACK--> B:e08
    B:e03 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TURN_RIGHT_START<br>B:e03 TRACK_APPEARED_LEFT track_001<br>B:e04 CLOSING_START track_001<br>B:e05 CRITICAL_TTC_START track_001 | ego: not yet observed | - |
| 0.85 | B:e06 CRITICAL_TTC_END track_001 | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC | 0.80 |
| 1.20 | B:e07 TURN_RIGHT_END | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING | 1.10 |
| 1.45 | B:e08 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 1.40 |
| 1.80 | B:e09 COLLISION<br>B:e10 CRITICAL_TTC_END track_001<br>B:e11 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 1.70 |
| 1.85 | B:e12 BRAKE_START<br>B:e13 TURN_LEFT_START | ego: MOVING<br>track_001: no active state | 1.80 |
| 2.50 | B:e14 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state | 2.40 |
| 2.55 | B:e15 MOVING_END<br>B:e16 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 2.50 |

## States still active when observation ended

- BRAKE, since B:e12 (t = 1.85 s)
- STOP, since B:e16 (t = 2.55 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.00, COLLISION 1.80 (+1.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.95 | 300 | 10.3 m / -61 deg | 2.43 m (1.80) | 2.6 m / -125 deg | 8.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B started turning right (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: B's time-to-contact with track_001 became critical (already the case when first observed).
- t = 0.85 s: B's time-to-contact with track_001 stopped being critical.
- t = 1.20 s: B stopped turning right.
- t = 1.45 s: B's time-to-contact with track_001 became critical.
- t = 1.80 s: B's collision sensor recorded a contact (peak impulse 1247 N*s).
- t = 1.80 s: B's time-to-contact with track_001 stopped being critical.
- t = 1.80 s: B observed track_001 stop closing in.
- t = 1.85 s: B started braking.
- t = 1.85 s: B started turning left.
- t = 2.50 s: B stopped turning left.
- t = 2.55 s: B stopped moving.
- t = 2.55 s: B came to a stop.
