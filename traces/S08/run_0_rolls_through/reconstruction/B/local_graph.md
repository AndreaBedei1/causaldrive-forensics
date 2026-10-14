# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 165.16541194915771 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 44 (PRECEDES 34, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 2.70 | TRACK_APPEARED_RIGHT | B | track_001 | radar | initial_in_ego_path=False |
| B:e04 | 2.70 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 3.40 | TRACK_APPEARED_RIGHT | B | track_002 | radar | initial_in_ego_path=False |
| B:e06 | 3.40 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e07 | 3.90 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e08 | 3.95 | TRACK_LOST | B | track_001 | radar |  |
| B:e09 | 4.80 | TRACK_APPEARED_RIGHT | B | track_003 | radar | initial_in_ego_path=True |
| B:e10 | 4.80 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e11 | 5.30 | CRITICAL_TTC_START | B | track_003 | radar |  |
| B:e12 | 5.40 | COLLISION | B | - | collision_sensor | peak_impulse=12940.27 |
| B:e13 | 5.40 | CRITICAL_TTC_END | B | track_003 | radar |  |
| B:e14 | 5.40 | CLOSING_END | B | track_002 | radar |  |
| B:e15 | 5.40 | TRACK_LOST | B | track_002 | radar |  |
| B:e16 | 5.40 | TRACK_LOST | B | track_003 | radar |  |
| B:e17 | 5.45 | THROTTLE_END | B | - | controls |  |
| B:e18 | 5.45 | BRAKE_START | B | - | controls |  |
| B:e19 | 5.60 | MOVING_END | B | - | ego |  |
| B:e20 | 5.60 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e01 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e15
    B:e11 --PRECEDES--> B:e16
    B:e12 --PRECEDES--> B:e17
    B:e12 --PRECEDES--> B:e18
    B:e13 --PRECEDES--> B:e17
    B:e13 --PRECEDES--> B:e18
    B:e14 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e03 --SAME_TRACK--> B:e04
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e07
    B:e03 --SAME_TRACK--> B:e08
    B:e09 --SAME_TRACK--> B:e10
    B:e09 --SAME_TRACK--> B:e11
    B:e09 --SAME_TRACK--> B:e13
    B:e05 --SAME_TRACK--> B:e14
    B:e05 --SAME_TRACK--> B:e15
    B:e09 --SAME_TRACK--> B:e16
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START | ego: not yet observed | - |
| 2.70 | B:e03 TRACK_APPEARED_RIGHT track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 2.60 |
| 3.40 | B:e05 TRACK_APPEARED_RIGHT track_002<br>B:e06 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 3.30 |
| 3.90 | B:e07 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? | 3.80 |
| 3.95 | B:e08 TRACK_LOST track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 3.90 |
| 4.80 | B:e09 TRACK_APPEARED_RIGHT track_003<br>B:e10 CLOSING_START track_003 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 | 4.70 |
| 5.30 | B:e11 CRITICAL_TTC_START track_003 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING, IN_EGO_PATH, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001 | 5.20 |
| 5.40 | B:e12 COLLISION<br>B:e13 CRITICAL_TTC_END track_003<br>B:e14 CLOSING_END track_002<br>B:e15 TRACK_LOST track_002<br>B:e16 TRACK_LOST track_003 | ego: MOVING, THROTTLE<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 5.30 |
| 5.45 | B:e17 THROTTLE_END<br>B:e18 BRAKE_START | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001, track_002, track_003 | 5.40 |
| 5.60 | B:e19 MOVING_END<br>B:e20 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001, track_002, track_003 | 5.50 |

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 2.70 s); the track was lost at 3.95 s
- CRITICAL_TTC of track_002, since B:e07 (t = 3.90 s); the track was lost at 5.40 s
- CLOSING of track_003, since B:e10 (t = 4.80 s); the track was lost at 5.40 s
- BRAKE, since B:e18 (t = 5.45 s)
- STOP, since B:e20 (t = 5.60 s)

## Tracks lost

- track_001 at 3.95 s (B:e08): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 5.40 s (B:e15): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 5.40 s (B:e16): CLOSING, CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 3.90, COLLISION 5.40 (+1.50 s)
- track_003: CRITICAL_TTC_START 5.30, COLLISION 5.40 (+0.10 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.70 | 3.95 | 25 | 34.5 m / +20 deg | 21.57 m (3.95) | 21.6 m / +28 deg | 3.3 m/s |
| track_002 | 3.40 | 5.40 | 40 | 26.2 m / +17 deg | 2.94 m (5.40) | 2.9 m / +49 deg | 4.9 m/s |
| track_003 | 4.80 | 5.40 | 13 | 8.3 m / +13 deg | 0.81 m (5.40) | 0.8 m / -3 deg | 5.6 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 2.70 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.70 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.40 s: B's radar started tracking track_002, which appeared on its right.
- t = 3.40 s: B observed track_002 start closing in (already the case when first observed).
- t = 3.90 s: B's time-to-contact with track_002 became critical.
- t = 3.95 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 4.80 s: B's radar started tracking track_003, which appeared on its right.
- t = 4.80 s: B observed track_003 start closing in (already the case when first observed).
- t = 5.30 s: B's time-to-contact with track_003 became critical.
- t = 5.40 s: B's collision sensor recorded a contact (peak impulse 12940 N*s).
- t = 5.40 s: B's time-to-contact with track_003 stopped being critical.
- t = 5.40 s: B observed track_002 stop closing in.
- t = 5.40 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 5.40 s: B's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 5.45 s: B released the accelerator.
- t = 5.45 s: B started braking.
- t = 5.60 s: B stopped moving.
- t = 5.60 s: B came to a stop.
