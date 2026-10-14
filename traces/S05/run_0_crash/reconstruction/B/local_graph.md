# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 126.25217776373029 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 138 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.65 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 11; edges: 15 (PRECEDES 12, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 0.10 | TRACK_APPEARED_FRONT | B | track_001 | radar | initial_in_ego_path=True |
| B:e04 | 3.20 | CLOSING_START | B | track_001 | radar |  |
| B:e05 | 3.40 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e06 | 3.65 | THROTTLE_END | B | - | controls |  |
| B:e07 | 3.65 | BRAKE_START | B | - | controls |  |
| B:e08 | 4.15 | TRACK_LOST | B | track_001 | radar |  |
| B:e09 | 4.85 | MOVING_END | B | - | ego |  |
| B:e10 | 4.85 | STOP_START | B | - | ego |  |
| B:e11 | 5.90 | COLLISION | B | - | collision_sensor | peak_impulse=22183.35 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e11
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e05
    B:e03 --SAME_TRACK--> B:e08
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START | ego: not yet observed | - |
| 0.10 | B:e03 TRACK_APPEARED_FRONT track_001 | ego: MOVING, THROTTLE | 0.00 |
| 3.20 | B:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH | 3.10 |
| 3.40 | B:e05 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH | 3.30 |
| 3.65 | B:e06 THROTTLE_END<br>B:e07 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 3.60 |
| 4.15 | B:e08 TRACK_LOST track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 4.10 |
| 4.85 | B:e09 MOVING_END<br>B:e10 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 | 4.80 |
| 5.90 | B:e11 COLLISION | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001 | 5.80 |

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 3.20 s); the track was lost at 4.15 s
- CRITICAL_TTC of track_001, since B:e05 (t = 3.40 s); the track was lost at 4.15 s
- BRAKE, since B:e07 (t = 3.65 s)
- STOP, since B:e10 (t = 4.85 s)

## Tracks lost

- track_001 at 4.15 s (B:e08): CLOSING, CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.40, COLLISION 5.90 (+2.50 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.10 | 4.15 | 81 | 21.5 m / -0 deg | 17.86 m (4.15) | 17.9 m / +0 deg | 13.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 0.10 s: B's radar started tracking track_001, which appeared in front of it.
- t = 3.20 s: B observed track_001 start closing in.
- t = 3.40 s: B's time-to-contact with track_001 became critical.
- t = 3.65 s: B released the accelerator.
- t = 3.65 s: B started braking.
- t = 4.15 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 4.85 s: B stopped moving.
- t = 4.85 s: B came to a stop.
- t = 5.90 s: B's collision sensor recorded a contact (peak impulse 22183 N*s).
