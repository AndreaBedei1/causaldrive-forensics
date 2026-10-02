# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 267.8788150437176 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 181 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (17.95 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 21; edges: 35 (PRECEDES 28, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.50 | MOVING_END | C | - | ego |  |
| C:e03 | 0.50 | STOP_START | C | - | ego |  |
| C:e04 | 3.45 | TRACK_APPEARED_REAR | C | track_001 | radar |  |
| C:e05 | 3.45 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e06 | 4.20 | TRACK_APPEARED_RIGHT | C | track_002 | radar |  |
| C:e07 | 4.20 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e08 | 5.25 | TRACK_LOST | C | track_002 | radar |  |
| C:e09 | 5.60 | CLOSING_END | C | track_001 | radar |  |
| C:e10 | 11.50 | TRACK_APPEARED_RIGHT | C | track_003 | radar |  |
| C:e11 | 11.75 | CLOSING_START | C | track_003 | radar |  |
| C:e12 | 11.95 | STOP_END | C | - | ego |  |
| C:e13 | 11.95 | MOVING_START | C | - | ego |  |
| C:e14 | 12.25 | TRACK_LOST | C | track_003 | radar |  |
| C:e15 | 13.40 | STOP_SIGN_DETECTED_START | C | sign-3 | camera | relevant_to_ego_path=False |
| C:e16 | 13.60 | STOP_SIGN_DETECTED_END | C | sign-3 | camera |  |
| C:e17 | 14.05 | TRACK_LOST | C | track_001 | radar |  |
| C:e18 | 14.10 | COLLISION | C | - | collision_sensor | peak_impulse=9089.81 |
| C:e19 | 14.10 | BRAKE_START | C | - | controls |  |
| C:e20 | 14.65 | MOVING_END | C | - | ego |  |
| C:e21 | 14.65 | STOP_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e02
    C:e01 --PRECEDES--> C:e03
    C:e02 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e07
    C:e05 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e13
    C:e12 --PRECEDES--> C:e14
    C:e13 --PRECEDES--> C:e14
    C:e14 --PRECEDES--> C:e15
    C:e15 --PRECEDES--> C:e16
    C:e16 --PRECEDES--> C:e17
    C:e17 --PRECEDES--> C:e18
    C:e17 --PRECEDES--> C:e19
    C:e18 --PRECEDES--> C:e20
    C:e18 --PRECEDES--> C:e21
    C:e19 --PRECEDES--> C:e20
    C:e19 --PRECEDES--> C:e21
    C:e04 --SAME_TRACK--> C:e05
    C:e06 --SAME_TRACK--> C:e07
    C:e06 --SAME_TRACK--> C:e08
    C:e04 --SAME_TRACK--> C:e09
    C:e10 --SAME_TRACK--> C:e11
    C:e10 --SAME_TRACK--> C:e14
    C:e04 --SAME_TRACK--> C:e17
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START | ego: not yet observed | - |
| 0.50 | C:e02 MOVING_END<br>C:e03 STOP_START | ego: MOVING | 0.40 |
| 3.45 | C:e04 TRACK_APPEARED_REAR track_001<br>C:e05 CLOSING_START track_001 | ego: STOP | 3.40 |
| 4.20 | C:e06 TRACK_APPEARED_RIGHT track_002<br>C:e07 CLOSING_START track_002 | ego: STOP<br>track_001: CLOSING | 4.10 |
| 5.25 | C:e08 TRACK_LOST track_002 | ego: STOP<br>track_001: CLOSING<br>track_002: CLOSING | 5.20 |
| 5.60 | C:e09 CLOSING_END track_001 | ego: STOP<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 | 5.50 |
| 11.50 | C:e10 TRACK_APPEARED_RIGHT track_003 | ego: STOP<br>track_001: no active state<br>track lost, states UNKNOWN: track_002 | 11.40 |
| 11.75 | C:e11 CLOSING_START track_003 | ego: STOP<br>track_001: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_002 | 11.70 |
| 11.95 | C:e12 STOP_END<br>C:e13 MOVING_START | ego: STOP<br>track_001: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_002 | 11.90 |
| 12.25 | C:e14 TRACK_LOST track_003 | ego: MOVING<br>track_001: no active state<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_002 | 12.20 |
| 13.40 | C:e15 STOP_SIGN_DETECTED_START sign-3 | ego: MOVING<br>track_001: no active state<br>track lost, states UNKNOWN: track_002, track_003 | 13.30 |
| 13.60 | C:e16 STOP_SIGN_DETECTED_END sign-3 | ego: MOVING<br>track_001: no active state<br>track lost, states UNKNOWN: track_002, track_003<br>sign-3: STOP sign known | 13.50 |
| 14.05 | C:e17 TRACK_LOST track_001 | ego: MOVING<br>track_001: no active state<br>track lost, states UNKNOWN: track_002, track_003<br>sign-3: STOP sign known | 14.00 |
| 14.10 | C:e18 COLLISION<br>C:e19 BRAKE_START | ego: MOVING<br>track lost, states UNKNOWN: track_001, track_002, track_003<br>sign-3: STOP sign known | 14.00 |
| 14.65 | C:e20 MOVING_END<br>C:e21 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001, track_002, track_003<br>sign-3: STOP sign known | 14.60 |

## States still active when observation ended

- CLOSING of track_002, since C:e07 (t = 4.20 s); the track was lost at 5.25 s
- CLOSING of track_003, since C:e11 (t = 11.75 s); the track was lost at 12.25 s
- BRAKE, since C:e19 (t = 14.10 s)
- STOP, since C:e21 (t = 14.65 s)

## Tracks lost

- track_002 at 5.25 s (C:e08): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 12.25 s (C:e14): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- STOP sign sign-3: detected 13.40 s -> 13.60 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.45 | 14.05 | 98 | 42.6 m / +176 deg | 20.09 m (5.60) | 28.1 m / +172 deg | 13.3 m/s |
| track_002 | 4.20 | 5.25 | 9 | 26.2 m / +172 deg | 17.19 m (5.25) | 17.2 m / +170 deg | 10.4 m/s |
| track_003 | 11.50 | 12.25 | 5 | 19.7 m / +170 deg | 18.37 m (12.25) | 18.4 m / +169 deg | 4.8 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.50 s: C stopped moving.
- t = 0.50 s: C came to a stop.
- t = 3.45 s: C's radar started tracking track_001, which appeared behind it.
- t = 3.45 s: C observed track_001 start closing in (already the case when first observed).
- t = 4.20 s: C's radar started tracking track_002, which appeared on its right.
- t = 4.20 s: C observed track_002 start closing in (already the case when first observed).
- t = 5.25 s: C's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 5.60 s: C observed track_001 stop closing in.
- t = 11.50 s: C's radar started tracking track_003, which appeared on its right.
- t = 11.75 s: C observed track_003 start closing in.
- t = 11.95 s: C left its stop.
- t = 11.95 s: C started moving.
- t = 12.25 s: C's radar lost track_003 (its states are UNKNOWN from then on, not ended).
- t = 13.40 s: C's camera established a STOP sign detection (sign-3) (the detector judged it not relevant to its path).
- t = 13.60 s: C's camera stopped detecting STOP sign sign-3.
- t = 14.05 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 14.10 s: C's collision sensor recorded a contact (peak impulse 9090 N*s).
- t = 14.10 s: C started braking.
- t = 14.65 s: C stopped moving.
- t = 14.65 s: C came to a stop.
