# Global graph - S01/run_0_crash

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
| A | ALIGNED | A:e07 | 6.50 | -6.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 6.50 | -6.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 17663.06 vs 17663.06 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.99 | A and B both reported collision_001 (peak impulse 17663.06 vs 17663.06 N*s)<br>tracked for 6.50 s before the matched collision<br>at the contact: minimum range 0.78 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.21 m/s over 3.0 s |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -6.50 | TRACK_APPEARED | A | B | A:e01 @ 0.00 | range_m=23.54; bearing_deg=-0.70; speed_mps=13.07; in_ego_path=True |
| g02 | -6.05 | CLOSING | A | B | A:e02 @ 0.45 | range_m=23.20; closing_speed_mps=1.03; peak_closing_speed_mps=4.18; duration_s=1.10 |
| g03 | -5.35 | THROTTLE_ONSET | A | - | A:e03 @ 1.15 | throttle=0.86; speed_mps=12.56 |
| g04 | -2.55 | BRAKE_EPISODE | B | - | B:e01 @ 3.95 | start_t_local=3.95; end_t_local=11.95; duration_s=8.00; peak_brake=1.00; mean_brake=1.00; speed_start_mps=13.78; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| g05 | -2.25 | CLOSING | A | B | A:e04 @ 4.25 | range_m=21.64; closing_speed_mps=1.41; peak_closing_speed_mps=13.69; duration_s=2.20 |
| g06 | -1.50 | CRITICAL_TTC | A | B | A:e05 @ 5.00 | ttc_s=1.82; range_m=17.95; min_ttc_s=0.10 |
| g07 | -1.35 | FULL_STOP | B | - | B:e02 @ 5.15 | stopped_for_s=6.80; stopped_until_recording_end=True |
| g08 | -0.95 | BRAKE_EPISODE | A | - | A:e06 @ 5.55 | start_t_local=5.55; end_t_local=11.95; duration_s=6.40; peak_brake=1.00; mean_brake=0.98; speed_start_mps=13.57; speed_end_mps=0.00; min_speed_mps=0.00; released=False |
| g09 | 0.00 | COLLISION | - | A, B | A:e07 @ 6.50, B:e03 @ 6.50 | peak_impulse=A 17663.06, B 17663.06 |
| g10 | 0.05 | FULL_STOP | A | - | A:e08 @ 6.55 | stopped_for_s=5.40; stopped_until_recording_end=True |

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
    g01 --SAME_TRACK--> g02
    g02 --SAME_TRACK--> g05
    g05 --SAME_TRACK--> g06
```

## Global trace

| t_global | Events |
|---------:|--------|
| -6.50 | TRACK_APPEARED(A,B) |
| -6.05 | CLOSING(A,B) |
| -5.35 | THROTTLE_ONSET(A) |
| -2.55 | BRAKE_EPISODE(B) |
| -2.25 | CLOSING(A,B) |
| -1.50 | CRITICAL_TTC(A,B) |
| -1.35 | FULL_STOP(B) |
| -0.95 | BRAKE_EPISODE(A) |
| +0.00 | COLLISION(A,B) |
| +0.05 | FULL_STOP(A) |

## Plain-language reading

- 6.50 s before the matched collision, A's radar started tracking B at 23.5 m, ahead, moving at 13.1 m/s, inside its path.
- 6.05 s before the matched collision, A observed B closing at 1.0 m/s from 23.2 m (peak 4.2 m/s, down to 20.5 m).
- 5.35 s before the matched collision, A applied strong throttle (0.86 at 12.6 m/s).
- 2.55 s before the matched collision, B braked for 8.00 s (peak 1.00, mean 1.00), from 13.8 to 0.0 m/s, still braking when its recording ended.
- 2.25 s before the matched collision, A observed B closing at 1.4 m/s from 21.6 m (peak 13.7 m/s, down to 0.8 m).
- 1.50 s before the matched collision, A's time-to-contact with B fell to 1.8 s at 17.9 m (minimum 0.1 s).
- 1.35 s before the matched collision, B came to a full stop and stayed stopped until its recording ended.
- 0.95 s before the matched collision, A braked for 6.40 s (peak 1.00, mean 0.98), from 13.6 to 0.0 m/s, still braking when its recording ended.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 17663, B: 17663 N*s).
- 0.05 s after the matched collision, A came to a full stop and stayed stopped until its recording ended.
