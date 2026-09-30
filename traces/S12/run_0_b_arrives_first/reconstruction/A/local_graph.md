# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 370.09269582107663 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 13 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 51; edges: 132 (PRECEDES 107, SAME_TRACK 25)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.05 | STOP_SIGN_DETECTED_START | A | sign-0 | camera | relevant_to_ego_path=True |
| A:e03 | 3.00 | TRACK_APPEARED | A | track_001 | radar |  |
| A:e04 | 3.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 3.55 | STOP_SIGN_DETECTED_END | A | sign-0 | camera |  |
| A:e06 | 4.35 | BRAKE_START | A | - | controls |  |
| A:e07 | 4.35 | HARD_BRAKE_START | A | - | controls |  |
| A:e08 | 4.70 | CLOSING_END | A | track_001 | radar |  |
| A:e09 | 4.75 | MOVING_END | A | - | ego |  |
| A:e10 | 4.75 | STOP_START | A | - | ego |  |
| A:e11 | 7.00 | CLOSING_START | A | track_001 | radar |  |
| A:e12 | 9.70 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e13 | 9.85 | CLOSING_END | A | track_001 | radar |  |
| A:e14 | 10.20 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e15 | 10.45 | HARD_BRAKE_END | A | - | controls |  |
| A:e16 | 10.45 | BRAKE_END | A | - | controls |  |
| A:e17 | 10.45 | STRONG_THROTTLE_START | A | - | controls |  |
| A:e18 | 10.80 | STOP_END | A | - | ego |  |
| A:e19 | 10.80 | MOVING_START | A | - | ego |  |
| A:e20 | 11.65 | TRACK_LOST | A | track_001 | radar |  |
| A:e21 | 11.80 | STRONG_THROTTLE_END | A | - | controls |  |
| A:e22 | 13.10 | TRACK_APPEARED | A | track_002 | radar |  |
| A:e23 | 13.10 | TRACK_APPEARED | A | track_003 | radar |  |
| A:e24 | 13.10 | TRACK_APPEARED | A | track_004 | radar |  |
| A:e25 | 13.10 | TRACK_APPEARED | A | track_006 | radar |  |
| A:e26 | 13.10 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e27 | 13.10 | CLOSING_START | A | track_003 | radar | active_at_first_observation=True |
| A:e28 | 13.10 | CLOSING_START | A | track_004 | radar | active_at_first_observation=True |
| A:e29 | 13.10 | CLOSING_START | A | track_006 | radar | active_at_first_observation=True |
| A:e30 | 13.25 | TRACK_APPEARED | A | track_005 | radar |  |
| A:e31 | 13.25 | CLOSING_START | A | track_005 | radar | active_at_first_observation=True |
| A:e32 | 13.30 | TRACK_APPEARED | A | track_007 | radar |  |
| A:e33 | 13.30 | TRACK_APPEARED | A | track_009 | radar |  |
| A:e34 | 13.30 | CLOSING_START | A | track_007 | radar | active_at_first_observation=True |
| A:e35 | 13.30 | CLOSING_START | A | track_009 | radar | active_at_first_observation=True |
| A:e36 | 13.35 | TRACK_APPEARED | A | track_008 | radar |  |
| A:e37 | 13.35 | TRACK_APPEARED | A | track_010 | radar |  |
| A:e38 | 13.35 | CLOSING_START | A | track_008 | radar | active_at_first_observation=True |
| A:e39 | 13.35 | CLOSING_START | A | track_010 | radar | active_at_first_observation=True |
| A:e40 | 13.45 | TRACK_APPEARED | A | track_011 | radar |  |
| A:e41 | 13.45 | TRACK_APPEARED | A | track_012 | radar |  |
| A:e42 | 13.45 | CLOSING_START | A | track_011 | radar | active_at_first_observation=True |
| A:e43 | 13.45 | CLOSING_START | A | track_012 | radar | active_at_first_observation=True |
| A:e44 | 13.50 | TRACK_APPEARED | A | track_013 | radar |  |
| A:e45 | 13.50 | CLOSING_START | A | track_013 | radar | active_at_first_observation=True |
| A:e46 | 13.80 | CRITICAL_TTC_START | A | track_007 | radar |  |
| A:e47 | 14.00 | TRACK_LOST | A | track_007 | radar |  |
| A:e48 | 14.40 | TRACK_LOST | A | track_003 | radar |  |
| A:e49 | 15.00 | EGO_PATH_ENTRY | A | track_006 | radar |  |
| A:e50 | 15.60 | TRACK_LOST | A | track_013 | radar |  |
| A:e51 | 15.95 | EGO_PATH_EXIT | A | track_006 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e20
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e21 --PRECEDES--> A:e24
    A:e21 --PRECEDES--> A:e25
    A:e21 --PRECEDES--> A:e26
    A:e21 --PRECEDES--> A:e27
    A:e21 --PRECEDES--> A:e28
    A:e21 --PRECEDES--> A:e29
    A:e22 --PRECEDES--> A:e30
    A:e22 --PRECEDES--> A:e31
    A:e23 --PRECEDES--> A:e30
    A:e23 --PRECEDES--> A:e31
    A:e24 --PRECEDES--> A:e30
    A:e24 --PRECEDES--> A:e31
    A:e25 --PRECEDES--> A:e30
    A:e25 --PRECEDES--> A:e31
    A:e26 --PRECEDES--> A:e30
    A:e26 --PRECEDES--> A:e31
    A:e27 --PRECEDES--> A:e30
    A:e27 --PRECEDES--> A:e31
    A:e28 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e30
    A:e29 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e33
    A:e30 --PRECEDES--> A:e34
    A:e30 --PRECEDES--> A:e35
    A:e31 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e31 --PRECEDES--> A:e35
    A:e32 --PRECEDES--> A:e36
    A:e32 --PRECEDES--> A:e37
    A:e32 --PRECEDES--> A:e38
    A:e32 --PRECEDES--> A:e39
    A:e33 --PRECEDES--> A:e36
    A:e33 --PRECEDES--> A:e37
    A:e33 --PRECEDES--> A:e38
    A:e33 --PRECEDES--> A:e39
    A:e34 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e37
    A:e34 --PRECEDES--> A:e38
    A:e34 --PRECEDES--> A:e39
    A:e35 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e38
    A:e35 --PRECEDES--> A:e39
    A:e36 --PRECEDES--> A:e40
    A:e36 --PRECEDES--> A:e41
    A:e36 --PRECEDES--> A:e42
    A:e36 --PRECEDES--> A:e43
    A:e37 --PRECEDES--> A:e40
    A:e37 --PRECEDES--> A:e41
    A:e37 --PRECEDES--> A:e42
    A:e37 --PRECEDES--> A:e43
    A:e38 --PRECEDES--> A:e40
    A:e38 --PRECEDES--> A:e41
    A:e38 --PRECEDES--> A:e42
    A:e38 --PRECEDES--> A:e43
    A:e39 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e39 --PRECEDES--> A:e42
    A:e39 --PRECEDES--> A:e43
    A:e40 --PRECEDES--> A:e44
    A:e40 --PRECEDES--> A:e45
    A:e41 --PRECEDES--> A:e44
    A:e41 --PRECEDES--> A:e45
    A:e42 --PRECEDES--> A:e44
    A:e42 --PRECEDES--> A:e45
    A:e43 --PRECEDES--> A:e44
    A:e43 --PRECEDES--> A:e45
    A:e44 --PRECEDES--> A:e46
    A:e45 --PRECEDES--> A:e46
    A:e46 --PRECEDES--> A:e47
    A:e47 --PRECEDES--> A:e48
    A:e48 --PRECEDES--> A:e49
    A:e49 --PRECEDES--> A:e50
    A:e50 --PRECEDES--> A:e51
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e08
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
    A:e03 --SAME_TRACK--> A:e14
    A:e03 --SAME_TRACK--> A:e20
    A:e22 --SAME_TRACK--> A:e26
    A:e23 --SAME_TRACK--> A:e27
    A:e24 --SAME_TRACK--> A:e28
    A:e25 --SAME_TRACK--> A:e29
    A:e30 --SAME_TRACK--> A:e31
    A:e32 --SAME_TRACK--> A:e34
    A:e33 --SAME_TRACK--> A:e35
    A:e36 --SAME_TRACK--> A:e38
    A:e37 --SAME_TRACK--> A:e39
    A:e40 --SAME_TRACK--> A:e42
    A:e41 --SAME_TRACK--> A:e43
    A:e44 --SAME_TRACK--> A:e45
    A:e32 --SAME_TRACK--> A:e46
    A:e32 --SAME_TRACK--> A:e47
    A:e23 --SAME_TRACK--> A:e48
    A:e25 --SAME_TRACK--> A:e49
    A:e44 --SAME_TRACK--> A:e50
    A:e25 --SAME_TRACK--> A:e51
```

## States still active when observation ended

- MOVING, since A:e19 (t = 10.80 s)
- CLOSING of track_002, since A:e26 (t = 13.10 s)
- CLOSING of track_003, since A:e27 (t = 13.10 s); the track was lost at 14.40 s
- CLOSING of track_004, since A:e28 (t = 13.10 s)
- CLOSING of track_006, since A:e29 (t = 13.10 s)
- CLOSING of track_005, since A:e31 (t = 13.25 s)
- CLOSING of track_007, since A:e34 (t = 13.30 s); the track was lost at 14.00 s
- CLOSING of track_009, since A:e35 (t = 13.30 s)
- CLOSING of track_008, since A:e38 (t = 13.35 s)
- CLOSING of track_010, since A:e39 (t = 13.35 s)
- CLOSING of track_011, since A:e42 (t = 13.45 s)
- CLOSING of track_012, since A:e43 (t = 13.45 s)
- CLOSING of track_013, since A:e45 (t = 13.50 s); the track was lost at 15.60 s
- CRITICAL_TTC of track_007, since A:e46 (t = 13.80 s); the track was lost at 14.00 s

## Sign detection windows

- STOP sign sign-0: detected 1.05 s -> 3.55 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.00 | 11.65 | 169 | 28.3 m / -44 deg | 10.06 m (9.95) | 14.6 m / +61 deg | 8.1 m/s |
| track_002 | 13.10 | 16.45 | 65 | 90.5 m / -60 deg | 63.37 m (16.45) | 63.4 m / -6 deg | 4.7 m/s |
| track_003 | 13.10 | 14.40 | 26 | 11.1 m / +54 deg | 8.18 m (14.40) | 8.2 m / +42 deg | 18.8 m/s |
| track_004 | 13.10 | 16.45 | 61 | 88.2 m / -58 deg | 60.56 m (16.45) | 60.6 m / -2 deg | 4.7 m/s |
| track_005 | 13.25 | 16.45 | 58 | 91.8 m / -57 deg | 65.88 m (16.45) | 65.9 m / -10 deg | 1.4 m/s |
| track_006 | 13.10 | 16.45 | 64 | 81.3 m / -55 deg | 53.68 m (16.45) | 53.7 m / +3 deg | 2.3 m/s |
| track_007 | 13.30 | 14.00 | 15 | 11.2 m / +37 deg | 8.93 m (14.00) | 8.9 m / +38 deg | 15.2 m/s |
| track_008 | 13.35 | 16.45 | 62 | 41.5 m / -60 deg | 18.36 m (16.45) | 18.4 m / -43 deg | 1.6 m/s |
| track_009 | 13.30 | 16.45 | 55 | 93.9 m / -57 deg | 68.70 m (16.45) | 68.7 m / -14 deg | 1.4 m/s |
| track_010 | 13.35 | 16.45 | 60 | 46.0 m / -59 deg | 22.48 m (16.45) | 22.5 m / -32 deg | 1.4 m/s |
| track_011 | 13.45 | 16.45 | 61 | 30.9 m / -58 deg | 12.16 m (16.45) | 12.2 m / -58 deg | 4.4 m/s |
| track_012 | 13.45 | 16.45 | 61 | 35.4 m / -56 deg | 14.68 m (16.45) | 14.7 m / -51 deg | 1.6 m/s |
| track_013 | 13.50 | 15.60 | 42 | 25.6 m / -60 deg | 12.78 m (15.60) | 12.8 m / -61 deg | 2.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.05 s: A's camera established a STOP sign detection (sign-0).
- t = 3.00 s: A's radar started tracking track_001.
- t = 3.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.55 s: A's camera stopped detecting STOP sign sign-0.
- t = 4.35 s: A started braking.
- t = 4.35 s: A started braking hard.
- t = 4.70 s: A observed track_001 stop closing in.
- t = 4.75 s: A stopped moving.
- t = 4.75 s: A came to a stop.
- t = 7.00 s: A observed track_001 start closing in.
- t = 9.70 s: A observed track_001 enter its forward path corridor.
- t = 9.85 s: A observed track_001 stop closing in.
- t = 10.20 s: A observed track_001 leave its forward path corridor.
- t = 10.45 s: A stopped braking hard.
- t = 10.45 s: A released the brake.
- t = 10.45 s: A started applying strong throttle.
- t = 10.80 s: A left its stop.
- t = 10.80 s: A started moving.
- t = 11.65 s: A's radar lost track_001.
- t = 11.80 s: A stopped applying strong throttle.
- t = 13.10 s: A's radar started tracking track_002.
- t = 13.10 s: A's radar started tracking track_003.
- t = 13.10 s: A's radar started tracking track_004.
- t = 13.10 s: A's radar started tracking track_006.
- t = 13.10 s: A observed track_002 start closing in (already the case when first observed).
- t = 13.10 s: A observed track_003 start closing in (already the case when first observed).
- t = 13.10 s: A observed track_004 start closing in (already the case when first observed).
- t = 13.10 s: A observed track_006 start closing in (already the case when first observed).
- t = 13.25 s: A's radar started tracking track_005.
- t = 13.25 s: A observed track_005 start closing in (already the case when first observed).
- t = 13.30 s: A's radar started tracking track_007.
- t = 13.30 s: A's radar started tracking track_009.
- t = 13.30 s: A observed track_007 start closing in (already the case when first observed).
- t = 13.30 s: A observed track_009 start closing in (already the case when first observed).
- t = 13.35 s: A's radar started tracking track_008.
- t = 13.35 s: A's radar started tracking track_010.
- t = 13.35 s: A observed track_008 start closing in (already the case when first observed).
- t = 13.35 s: A observed track_010 start closing in (already the case when first observed).
- t = 13.45 s: A's radar started tracking track_011.
- t = 13.45 s: A's radar started tracking track_012.
- t = 13.45 s: A observed track_011 start closing in (already the case when first observed).
- t = 13.45 s: A observed track_012 start closing in (already the case when first observed).
- t = 13.50 s: A's radar started tracking track_013.
- t = 13.50 s: A observed track_013 start closing in (already the case when first observed).
- t = 13.80 s: A's time-to-contact with track_007 became critical.
- t = 14.00 s: A's radar lost track_007.
- t = 14.40 s: A's radar lost track_003.
- t = 15.00 s: A observed track_006 enter its forward path corridor.
- t = 15.60 s: A's radar lost track_013.
- t = 15.95 s: A observed track_006 leave its forward path corridor.
