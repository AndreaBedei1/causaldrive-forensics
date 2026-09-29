# Global graph - S02/run_0_crash

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e07 | 4.25 | -4.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 4.25 | -4.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5953.86 vs 5953.86 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.97 | A and B both reported collision_001 (peak impulse 5953.86 vs 5953.86 N*s)<br>tracked for 4.25 s before the matched collision<br>at the contact: minimum range 0.85 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.40 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -4.25 | TRACK_APPEARED | A | B | A:e01 @ 0.00 | range_m=24.57; bearing_deg=-7.80; speed_mps=8.01; in_ego_path=False |
| g02 | -4.25 | CLOSING | A | B | A:e02 @ 0.00 | range_m=24.57; closing_speed_mps=5.56; peak_closing_speed_mps=7.86; duration_s=4.20 |
| g03 | -3.10 | THROTTLE_ONSET | A | - | A:e03 @ 1.15 | throttle=0.86; speed_mps=12.56 |
| g04 | -1.45 | CRITICAL_TTC | A | B | A:e04 @ 2.80 | ttc_s=1.96; range_m=9.56; min_ttc_s=0.17 |
| g05 | -1.10 | BRAKE_EPISODE | B | - | B:e01 @ 3.15 | start_t_local=3.15; end_t_local=3.60; duration_s=0.45; peak_brake=0.73; mean_brake=0.48; speed_start_mps=8.71; speed_end_mps=6.56; min_speed_mps=6.56; released=True |
| g06 | -1.05 | ENTERED_EGO_PATH | A | B | A:e05 @ 3.20 | from_side=left; longitudinal_m=7.46; lateral_speed_mps=1.25 |
| g07 | -0.40 | BRAKE_EPISODE | A | - | A:e06 @ 3.85 | start_t_local=3.85; end_t_local=15.15; duration_s=11.30; peak_brake=1.00; mean_brake=0.99; speed_start_mps=13.41; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| g08 | 0.00 | BRAKE_EPISODE | B | - | B:e02 @ 4.25 | start_t_local=4.25; end_t_local=15.15; duration_s=10.90; peak_brake=1.00; mean_brake=1.00; speed_start_mps=9.59; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| g09 | 0.00 | COLLISION | - | A, B | A:e07 @ 4.25, B:e03 @ 4.25 | peak_impulse=A 5953.86, B 5953.86 |
| g10 | 0.60 | FULL_STOP | A | - | A:e08 @ 4.85 | stopped_for_s=10.30; stopped_until_recording_end=True |
| g11 | 0.75 | FULL_STOP | B | - | B:e04 @ 5.00 | stopped_for_s=10.15; stopped_until_recording_end=True |

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
    g01 --SAME_TRACK--> g02
    g02 --SAME_TRACK--> g04
    g04 --SAME_TRACK--> g06
```

## Global trace

| t_global | Events |
|---------:|--------|
| -4.25 | TRACK_APPEARED(A,B); CLOSING(A,B) |
| -3.10 | THROTTLE_ONSET(A) |
| -1.45 | CRITICAL_TTC(A,B) |
| -1.10 | BRAKE_EPISODE(B) |
| -1.05 | ENTERED_EGO_PATH(A,B) |
| -0.40 | BRAKE_EPISODE(A) |
| +0.00 | BRAKE_EPISODE(B); COLLISION(A,B) |
| +0.60 | FULL_STOP(A) |
| +0.75 | FULL_STOP(B) |

## Plain-language reading

- 4.25 s before the matched collision, A's radar started tracking B at 24.6 m, 8 deg to the left, moving at 8.0 m/s.
- 4.25 s before the matched collision, A observed B closing at 5.6 m/s from 24.6 m (peak 7.9 m/s, down to 0.9 m).
- 3.10 s before the matched collision, A applied strong throttle (0.86 at 12.6 m/s).
- 1.45 s before the matched collision, A's time-to-contact with B fell to 2.0 s at 9.6 m (minimum 0.2 s).
- 1.10 s before the matched collision, B braked for 0.45 s (peak 0.73, mean 0.48), from 8.7 to 6.6 m/s, then released the brake.
- 1.05 s before the matched collision, A observed B move into its path from the left (7.5 m ahead, lateral speed 1.2 m/s).
- 0.40 s before the matched collision, A braked for 11.30 s (peak 1.00, mean 0.99), from 13.4 to 0.0 m/s, still braking when its recording ended.
- At the matched collision, B braked for 10.90 s (peak 1.00, mean 1.00), from 9.6 to 0.0 m/s, still braking when its recording ended.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5954, B: 5954 N*s).
- 0.60 s after the matched collision, A came to a full stop and stayed stopped until its recording ended.
- 0.75 s after the matched collision, B came to a full stop and stayed stopped until its recording ended.
