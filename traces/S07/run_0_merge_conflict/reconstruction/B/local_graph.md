# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 15.514892023056746 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 235 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (23.35 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 27 (PRECEDES 22, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | THROTTLE_START | B | - | controls | active_at_first_observation=True |
| B:e03 | 2.55 | TRACK_APPEARED_LEFT | B | track_001 | radar | initial_in_ego_path=False |
| B:e04 | 2.55 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 6.75 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e06 | 8.20 | TURN_RIGHT_START | B | - | ego |  |
| B:e07 | 9.95 | TURN_RIGHT_END | B | - | ego |  |
| B:e08 | 10.10 | EGO_PATH_ENTRY | B | track_001 | radar | occupancy_evidence=returns; occupancy_margin_m=0.41; occupancy_sigma_m=0.25; cause=MUTUAL_LATERAL; geometry=estimated_body |
| B:e09 | 10.25 | COLLISION | B | - | collision_sensor | peak_impulse=1904.84; merged_bursts=[[10.35, 116.28], [10.85, 7.95]] |
| B:e10 | 10.25 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e11 | 10.25 | CLOSING_END | B | track_001 | radar |  |
| B:e12 | 10.30 | THROTTLE_END | B | - | controls |  |
| B:e13 | 10.30 | BRAKE_START | B | - | controls |  |
| B:e14 | 11.00 | MOVING_END | B | - | ego |  |
| B:e15 | 11.00 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e03
    B:e01 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e05
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
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e03 --SAME_TRACK--> B:e04
    B:e03 --SAME_TRACK--> B:e05
    B:e03 --SAME_TRACK--> B:e08
    B:e03 --SAME_TRACK--> B:e10
    B:e03 --SAME_TRACK--> B:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 THROTTLE_START | ego: not yet observed | - |
| 2.55 | B:e03 TRACK_APPEARED_LEFT track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 2.50 |
| 6.75 | B:e05 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 6.70 |
| 8.20 | B:e06 TURN_RIGHT_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC | 8.10 |
| 9.95 | B:e07 TURN_RIGHT_END | ego: MOVING, THROTTLE, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC | 9.90 |
| 10.10 | B:e08 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC | 10.00 |
| 10.25 | B:e09 COLLISION<br>B:e10 CRITICAL_TTC_END track_001<br>B:e11 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 10.20 |
| 10.30 | B:e12 THROTTLE_END<br>B:e13 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH | 10.20 |
| 11.00 | B:e14 MOVING_END<br>B:e15 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH | 10.90 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e08 (t = 10.10 s)
- BRAKE, since B:e13 (t = 10.30 s)
- STOP, since B:e15 (t = 11.00 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 6.75, COLLISION 10.25 (+3.50 s); EGO_PATH_ENTRY 10.10 after critical TTC (+3.35 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.55 | 23.35 | 412 | 89.9 m / -16 deg | 0.22 m (23.35) | 0.2 m / -82 deg | 8.2 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B pressed the accelerator (already the case when first observed).
- t = 2.55 s: B's radar started tracking track_001, which appeared on its left.
- t = 2.55 s: B observed track_001 start closing in (already the case when first observed).
- t = 6.75 s: B's time-to-contact with track_001 became critical.
- t = 8.20 s: B started turning right.
- t = 9.95 s: B stopped turning right.
- t = 10.10 s: B observed track_001 enter its forward path corridor.
- t = 10.25 s: B's collision sensor recorded a contact (peak impulse 1905 N*s).
- t = 10.25 s: B's time-to-contact with track_001 stopped being critical.
- t = 10.25 s: B observed track_001 stop closing in.
- t = 10.30 s: B released the accelerator.
- t = 10.30 s: B started braking.
- t = 11.00 s: B stopped moving.
- t = 11.00 s: B came to a stop.
