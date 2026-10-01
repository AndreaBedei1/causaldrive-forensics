# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 13.179586462676525 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 181 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (17.95 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 13; edges: 19 (PRECEDES 19)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.50 | MOVING_END | C | - | ego |  |
| C:e03 | 0.50 | STOP_START | C | - | ego |  |
| C:e04 | 9.10 | YIELD_SIGN_DETECTED_START | C | sign-1 | camera | relevant_to_ego_path=False |
| C:e05 | 9.60 | YIELD_SIGN_DETECTED_END | C | sign-1 | camera |  |
| C:e06 | 11.95 | STOP_END | C | - | ego |  |
| C:e07 | 11.95 | MOVING_START | C | - | ego |  |
| C:e08 | 13.80 | STOP_SIGN_DETECTED_START | C | sign-3 | camera | relevant_to_ego_path=False |
| C:e09 | 13.80 | STOP_SIGN_DETECTED_END | C | sign-3 | camera |  |
| C:e10 | 14.10 | COLLISION | C | - | collision_sensor | peak_impulse=9095.53 |
| C:e11 | 14.10 | BRAKE_START | C | - | controls |  |
| C:e12 | 14.65 | MOVING_END | C | - | ego |  |
| C:e13 | 14.65 | STOP_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e01 --PRECEDES--> C:e03
    C:e02 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e04
    C:e04 --PRECEDES--> C:e05
    C:e05 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e06 --PRECEDES--> C:e09
    C:e07 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e10
    C:e08 --PRECEDES--> C:e11
    C:e09 --PRECEDES--> C:e10
    C:e09 --PRECEDES--> C:e11
    C:e10 --PRECEDES--> C:e12
    C:e10 --PRECEDES--> C:e13
    C:e11 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e13
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START | ego: not yet observed | - |
| 0.50 | C:e02 MOVING_END<br>C:e03 STOP_START | ego: MOVING | 0.40 |
| 9.10 | C:e04 YIELD_SIGN_DETECTED_START sign-1 | ego: STOP | 9.00 |
| 9.60 | C:e05 YIELD_SIGN_DETECTED_END sign-1 | ego: STOP<br>sign-1: YIELD sign known | 9.50 |
| 11.95 | C:e06 STOP_END<br>C:e07 MOVING_START | ego: STOP<br>sign-1: YIELD sign known | 11.90 |
| 13.80 | C:e08 STOP_SIGN_DETECTED_START sign-3<br>C:e09 STOP_SIGN_DETECTED_END sign-3 | ego: MOVING<br>sign-1: YIELD sign known | 13.70 |
| 14.10 | C:e10 COLLISION<br>C:e11 BRAKE_START | ego: MOVING<br>sign-1: YIELD sign known<br>sign-3: STOP sign known | 14.00 |
| 14.65 | C:e12 MOVING_END<br>C:e13 STOP_START | ego: MOVING, BRAKE<br>sign-1: YIELD sign known<br>sign-3: STOP sign known | 14.60 |

## States still active when observation ended

- BRAKE, since C:e11 (t = 14.10 s)
- STOP, since C:e13 (t = 14.65 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- STOP sign sign-3: detected 13.80 s -> 13.80 s; relevant to the path: False; STOP_START inside: none
- YIELD sign sign-1: detected 9.10 s -> 9.60 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in C's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.50 s: C stopped moving.
- t = 0.50 s: C came to a stop.
- t = 9.10 s: C's camera established a YIELD sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 9.60 s: C's camera stopped detecting YIELD sign sign-1.
- t = 11.95 s: C left its stop.
- t = 11.95 s: C started moving.
- t = 13.80 s: C's camera established a STOP sign detection (sign-3) (the detector judged it not relevant to its path).
- t = 13.80 s: C's camera stopped detecting STOP sign sign-3.
- t = 14.10 s: C's collision sensor recorded a contact (peak impulse 9096 N*s).
- t = 14.10 s: C started braking.
- t = 14.65 s: C stopped moving.
- t = 14.65 s: C came to a stop.
