# Global graph - S03/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e05 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e07 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 12077.22 vs 12077.22 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.20 s before the matched collision<br>not at the contact: last seen 0.90 s before the matched collision (window 0.50 s)<br>track speed agrees with B's own speed: RMSE 0.45 m/s over 1.3 s |
| B:track_001 | A | ASSOCIATED | 0.84 | B and A both reported collision_001 (peak impulse 12077.22 vs 12077.22 N*s)<br>tracked for 2.10 s before the matched collision<br>at the contact: minimum range 0.93 m in the last 0.50 s before the collision<br>the only track of B at the contact<br>track speed agrees with A's own speed: RMSE 0.89 m/s over 2.1 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.10 | THROTTLE_ONSET | B | - | B:e01 @ 1.15 | throttle=1.00; speed_mps=7.39 |
| g02 | -2.20 | TRACK_APPEARED | A | A:track_001 | A:e01 @ 2.05 | range_m=34.18; bearing_deg=55.70; speed_mps=10.87; in_ego_path=False |
| g03 | -2.20 | CLOSING | A | A:track_001 | A:e02 @ 2.05 | range_m=34.18; closing_speed_mps=14.32; peak_closing_speed_mps=15.62; duration_s=1.30 |
| g04 | -2.10 | TRACK_APPEARED | B | A | B:e02 @ 2.15 | range_m=32.71; bearing_deg=-37.80; speed_mps=8.19; in_ego_path=False |
| g05 | -2.10 | CLOSING | B | A | B:e03 @ 2.15 | range_m=32.71; closing_speed_mps=14.23; peak_closing_speed_mps=15.64; duration_s=2.10 |
| g06 | -1.90 | CRITICAL_TTC | A | A:track_001 | A:e03 @ 2.35 | ttc_s=1.99; range_m=29.84; min_ttc_s=0.94 |
| g07 | -1.90 | CRITICAL_TTC | B | A | B:e04 @ 2.35 | ttc_s=2.00; range_m=29.82; min_ttc_s=0.11 |
| g08 | -0.90 | TRACK_LOST | A | A:track_001 | A:e04 @ 3.35 | range_m=14.40; bearing_deg=59.10; tracked_for_s=1.30 |
| g09 | -0.15 | ENTERED_EGO_PATH | B | A | B:e05 @ 4.10 | from_side=left; longitudinal_m=2.53; lateral_speed_mps=10.70 |
| g10 | 0.00 | THROTTLE_ONSET | B | - | B:e06 @ 4.25 | throttle=1.00; speed_mps=5.15 |
| g11 | 0.00 | COLLISION | - | A, B | A:e05 @ 4.25, B:e07 @ 4.25 | peak_impulse=A 12077.22, B 12077.22 |
| g12 | 0.05 | BRAKE_EPISODE | A | - | A:e06 @ 4.30 | start_t_local=4.30; end_t_local=15.15; duration_s=10.85; peak_brake=1.00; mean_brake=1.00; speed_start_mps=8.90; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| g13 | 0.05 | BRAKE_EPISODE | B | - | B:e08 @ 4.30 | start_t_local=4.30; end_t_local=15.15; duration_s=10.85; peak_brake=1.00; mean_brake=1.00; speed_start_mps=4.36; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| g14 | 0.30 | FULL_STOP | B | - | B:e09 @ 4.55 | stopped_for_s=10.60; stopped_until_recording_end=True |
| g15 | 0.65 | FULL_STOP | A | - | A:e07 @ 4.90 | stopped_for_s=10.25; stopped_until_recording_end=True |

## Edges

```
    g01 --PRECEDES--> g02
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g02 --SAME_TRACK--> g03
    g03 --SAME_TRACK--> g06
    g06 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g05
    g05 --SAME_TRACK--> g07
    g07 --SAME_TRACK--> g09
```

## Global trace

| t_global | Events |
|---------:|--------|
| -3.10 | THROTTLE_ONSET(B) |
| -2.20 | TRACK_APPEARED(A,A:track_001); CLOSING(A,A:track_001) |
| -2.10 | TRACK_APPEARED(B,A); CLOSING(B,A) |
| -1.90 | CRITICAL_TTC(A,A:track_001); CRITICAL_TTC(B,A) |
| -0.90 | TRACK_LOST(A,A:track_001) |
| -0.15 | ENTERED_EGO_PATH(B,A) |
| +0.00 | THROTTLE_ONSET(B); COLLISION(A,B) |
| +0.05 | BRAKE_EPISODE(A); BRAKE_EPISODE(B) |
| +0.30 | FULL_STOP(B) |
| +0.65 | FULL_STOP(A) |

## Plain-language reading

- 3.10 s before the matched collision, B applied strong throttle (1.00 at 7.4 m/s).
- 2.20 s before the matched collision, A's radar started tracking unidentified object A:track_001 at 34.2 m, 56 deg to the right, moving at 10.9 m/s.
- 2.20 s before the matched collision, A observed unidentified object A:track_001 closing at 14.3 m/s from 34.2 m (peak 15.6 m/s, down to 14.4 m).
- 2.10 s before the matched collision, B's radar started tracking A at 32.7 m, 38 deg to the left, moving at 8.2 m/s.
- 2.10 s before the matched collision, B observed A closing at 14.2 m/s from 32.7 m (peak 15.6 m/s, down to 0.9 m).
- 1.90 s before the matched collision, A's time-to-contact with unidentified object A:track_001 fell to 2.0 s at 29.8 m (minimum 0.9 s).
- 1.90 s before the matched collision, B's time-to-contact with A fell to 2.0 s at 29.8 m (minimum 0.1 s).
- 0.90 s before the matched collision, A lost unidentified object A:track_001 at 14.4 m, 59 deg to the right, after tracking it for 1.3 s.
- 0.15 s before the matched collision, B observed A move into its path from the left (2.5 m ahead, lateral speed 10.7 m/s).
- At the matched collision, B applied strong throttle (1.00 at 5.2 m/s).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 12077, B: 12077 N*s).
- 0.05 s after the matched collision, A braked for 10.85 s (peak 1.00, mean 1.00), from 8.9 to 0.0 m/s, still braking when its recording ended.
- 0.05 s after the matched collision, B braked for 10.85 s (peak 1.00, mean 1.00), from 4.4 to 0.0 m/s, still braking when its recording ended.
- 0.30 s after the matched collision, B came to a full stop and stayed stopped until its recording ended.
- 0.65 s after the matched collision, A came to a full stop and stayed stopped until its recording ended.
