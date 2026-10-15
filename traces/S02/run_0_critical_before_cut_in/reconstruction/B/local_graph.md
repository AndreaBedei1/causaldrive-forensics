# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 13.522847969084978 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 21 (PRECEDES 17, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.55 | INDICATOR_RIGHT_START | B | - | lights |  |
| B:e04 | 2.20 | TRACK_APPEARED_RIGHT | B | track_001 | radar | initial_in_ego_path=False |
| B:e05 | 2.20 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 2.70 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 3.95 | INDICATOR_RIGHT_END | B | - | lights |  |
| B:e08 | 4.10 | COLLISION | B | - | collision_sensor | peak_impulse=937.49 |
| B:e09 | 4.10 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e10 | 4.10 | CLOSING_END | B | track_001 | radar |  |
| B:e11 | 4.10 | THROTTLE_END | B | - | controls |  |
| B:e12 | 4.15 | BRAKE_START | B | - | controls |  |
| B:e13 | 4.65 | MOVING_END | B | - | ego |  |
| B:e14 | 4.65 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e07 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e06
    B:e04 --SAME_TRACK--> B:e09
    B:e04 --SAME_TRACK--> B:e10
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START | ego: not yet observed | - |
| 0.55 | B:e03 INDICATOR_RIGHT_START | ego: MOVING, THROTTLE | 0.50 |
| 2.20 | B:e04 TRACK_APPEARED_RIGHT track_001<br>B:e05 CLOSING_START track_001 | ego: MOVING, THROTTLE, INDICATOR_RIGHT | 2.10 |
| 2.70 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE, INDICATOR_RIGHT<br>track_001: CLOSING, CRITICAL_TTC? | 2.60 |
| 3.95 | B:e07 INDICATOR_RIGHT_END | ego: MOVING, THROTTLE, INDICATOR_RIGHT<br>track_001: CLOSING, CRITICAL_TTC | 3.90 |
| 4.10 | B:e08 COLLISION<br>B:e09 CRITICAL_TTC_END track_001<br>B:e10 CLOSING_END track_001<br>B:e11 THROTTLE_END | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC | 4.00 |
| 4.15 | B:e12 BRAKE_START | ego: MOVING<br>track_001: no active state | 4.10 |
| 4.65 | B:e13 MOVING_END<br>B:e14 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 4.60 |

## States still active when observation ended

- BRAKE, since B:e12 (t = 4.15 s)
- STOP, since B:e14 (t = 4.65 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.70, COLLISION 4.10 (+1.40 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.20 | 11.45 | 186 | 9.3 m / +156 deg | 0.60 m (11.30) | 0.6 m / +106 deg | 13.5 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.55 s: B switched on its right turn indicator.
- t = 2.20 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.20 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.70 s: B's time-to-contact with track_001 became critical.
- t = 3.95 s: B switched off its right turn indicator.
- t = 4.10 s: B's collision sensor recorded a contact (peak impulse 937 N*s).
- t = 4.10 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.10 s: B observed track_001 stop closing in.
- t = 4.10 s: B released the accelerator.
- t = 4.15 s: B started braking.
- t = 4.65 s: B stopped moving.
- t = 4.65 s: B came to a stop.
