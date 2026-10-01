# Global graph - S09/run_0_merge_conflict

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |
| A:track_004 | anonymous_track | seen only by A; candidate: B |
| A:track_005 | anonymous_track | seen only by A; candidate: B |
| A:track_006 | anonymous_track | seen only by A; candidate: B |
| A:track_007 | anonymous_track | seen only by A; candidate: B |
| A:track_008 | anonymous_track | seen only by A; candidate: B |
| A:track_009 | anonymous_track | seen only by A; candidate: B |
| A:track_010 | anonymous_track | seen only by A; candidate: B |
| A:track_011 | anonymous_track | seen only by A; candidate: B |
| A:track_012 | anonymous_track | seen only by A; candidate: B |
| A:track_013 | anonymous_track | seen only by A; candidate: B |
| A:track_014 | anonymous_track | seen only by A; candidate: B |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |
| B:track_004 | anonymous_track | seen only by B; candidate: A |
| B:track_005 | anonymous_track | seen only by B; candidate: A |
| B:track_006 | anonymous_track | seen only by B; candidate: A |
| B:track_007 | anonymous_track | seen only by B; candidate: A |
| B:track_008 | anonymous_track | seen only by B; candidate: A |
| B:track_009 | anonymous_track | seen only by B; candidate: A |
| B:track_010 | anonymous_track | seen only by B; candidate: A |
| B:track_011 | anonymous_track | seen only by B; candidate: A |
| B:track_012 | anonymous_track | seen only by B; candidate: A |
| B:track_013 | anonymous_track | seen only by B; candidate: A |
| B:track_014 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e39 | 1.80 | -1.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e37 | 1.80 | -1.80 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 1247.19 vs 1247.19 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.68 | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 3.3 m -> 1.2 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.31 m/s over 1.8 s<br>range at the contact 1.18 m<br>the only track of A compatible with the contact |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.35 s before it (window 0.50 s)<br>approaching before the contact: range 26.4 m -> 21.2 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.19 m/s over 1.2 s (> 1.50)<br>range at the contact 21.19 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 17.9 m -> 13.8 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.56 m/s over 1.6 s (> 1.50)<br>range at the contact 13.81 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 43.6 m -> 36.3 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 4.72 m/s over 1.6 s (> 1.50)<br>range at the contact 36.33 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.15 s before it (window 0.50 s)<br>approaching before the contact: range 13.7 m -> 10.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.00 m/s over 1.4 s (> 1.50)<br>range at the contact 10.90 m (beyond 3.50 m: confidence factor 0.05) |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 41.6 m -> 35.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 4.86 m/s over 1.6 s (> 1.50)<br>range at the contact 34.95 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_007 | A:track_007 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>lost 1.40 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 69.0 m -> 67.8 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.43 m/s over 0.2 s |
| A:track_008 | A:track_008 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 44.5 m -> 38.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.55 m/s over 1.6 s (> 1.50)<br>range at the contact 38.46 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_009 | A:track_009 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.25 s before it (window 0.50 s)<br>approaching before the contact: range 42.7 m -> 36.1 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.31 m/s over 1.4 s (> 1.50)<br>range at the contact 36.10 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_010 | A:track_010 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 48.6 m -> 43.2 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.58 m/s over 1.6 s (> 1.50)<br>range at the contact 43.21 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_011 | A:track_011 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>lost 1.40 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 32.0 m -> 32.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.23 m/s over 0.2 s (> 1.50) |
| A:track_012 | A:track_012 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 12.3 m -> 8.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.27 m/s over 1.6 s (> 1.50)<br>range at the contact 7.98 m (beyond 3.50 m: confidence factor 0.33) |
| A:track_013 | A:track_013 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>lost 1.35 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 150.9 m -> 151.3 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.89 m/s over 0.2 s (> 1.50) |
| A:track_014 | A:track_014 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.55 s before the matched collision<br>lost 1.20 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 20.7 m -> 21.0 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 1.43 m/s over 0.3 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.80 s before the matched collision<br>lost 1.55 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 8.8 m -> 7.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.83 m/s over 0.2 s (> 1.50) |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>lost 1.40 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 43.7 m -> 44.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 6.05 m/s over 0.2 s (> 1.50) |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 24.4 m -> 22.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 4.22 m/s over 1.6 s (> 1.50)<br>range at the contact 22.43 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 15.3 m -> 11.4 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 6.90 m/s over 1.6 s (> 1.50)<br>range at the contact 11.37 m (beyond 3.50 m: confidence factor 0.03) |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 26.0 m -> 23.2 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.74 m/s over 1.6 s (> 1.50)<br>range at the contact 23.22 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>continuous up to the contact: last observed 0.30 s before it (window 0.50 s)<br>approaching before the contact: range 12.4 m -> 9.3 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 6.66 m/s over 1.3 s (> 1.50)<br>range at the contact 9.27 m (beyond 3.50 m: confidence factor 0.16) |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>lost 1.40 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 68.5 m -> 68.9 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 6.04 m/s over 0.2 s (> 1.50) |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.60 s before the matched collision<br>lost 1.35 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 64.5 m -> 64.8 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.87 m/s over 0.2 s (> 1.50) |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.55 s before the matched collision<br>lost 0.90 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 21.2 m -> 21.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 4.93 m/s over 0.7 s (> 1.50) |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.55 s before the matched collision<br>lost 1.15 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 55.8 m -> 56.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 4.45 m/s over 0.4 s (> 1.50) |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.55 s before the matched collision<br>lost 1.30 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 17.7 m -> 17.8 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.89 m/s over 0.2 s (> 1.50) |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.55 s before the matched collision<br>lost 1.25 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 59.4 m -> 59.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.94 m/s over 0.3 s (> 1.50) |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.55 s before the matched collision<br>lost 1.20 s before the matched collision (window 0.50 s)<br>not approaching before the contact: range 28.9 m -> 29.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.28 m/s over 0.3 s (> 1.50) |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 1247.19 vs 1247.19 N*s)<br>tracked for 1.50 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 14.5 m -> 12.9 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 2.86 m/s over 1.5 s (> 1.50)<br>range at the contact 12.91 m (beyond 3.50 m: confidence factor 0.01) |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -1.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -1.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -1.80 | TURN_LEFT_START | A | - | A:e02 @ 0.00 | active_at_first_observation=True |
| g04 | -1.80 | TURN_RIGHT_START | B | - | B:e02 @ 0.00 | active_at_first_observation=True |
| g05 | -1.80 | TRACK_APPEARED_LEFT | B | B:track_001 | B:e03 @ 0.00 |  |
| g06 | -1.80 | TRACK_APPEARED_RIGHT | A | B | A:e03 @ 0.00 |  |
| g07 | -1.80 | CLOSING_START | A | B | A:e04 @ 0.00 | active_at_first_observation=True |
| g08 | -1.80 | CLOSING_START | B | B:track_001 | B:e04 @ 0.00 | active_at_first_observation=True |
| g09 | -1.80 | CRITICAL_TTC_START | A | B | A:e05 @ 0.00 | active_at_first_observation=True |
| g10 | -1.80 | CRITICAL_TTC_START | B | B:track_001 | B:e05 @ 0.00 | active_at_first_observation=True |
| g11 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_002 | A:e06 @ 0.20 |  |
| g12 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_003 | A:e07 @ 0.20 |  |
| g13 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_004 | A:e08 @ 0.20 |  |
| g14 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_005 | A:e09 @ 0.20 |  |
| g15 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_006 | A:e10 @ 0.20 |  |
| g16 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_007 | A:e11 @ 0.20 |  |
| g17 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_008 | A:e12 @ 0.20 |  |
| g18 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_009 | A:e13 @ 0.20 |  |
| g19 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_010 | A:e14 @ 0.20 |  |
| g20 | -1.60 | TRACK_APPEARED_LEFT | A | A:track_012 | A:e15 @ 0.20 |  |
| g21 | -1.60 | TRACK_APPEARED_LEFT | B | B:track_002 | B:e06 @ 0.20 |  |
| g22 | -1.60 | TRACK_APPEARED_LEFT | B | B:track_007 | B:e07 @ 0.20 |  |
| g23 | -1.60 | TRACK_APPEARED_LEFT | B | B:track_008 | B:e08 @ 0.20 |  |
| g24 | -1.60 | TRACK_APPEARED_RIGHT | A | A:track_011 | A:e16 @ 0.20 |  |
| g25 | -1.60 | TRACK_APPEARED_RIGHT | A | A:track_013 | A:e17 @ 0.20 |  |
| g26 | -1.60 | TRACK_APPEARED_RIGHT | B | B:track_003 | B:e09 @ 0.20 |  |
| g27 | -1.60 | TRACK_APPEARED_RIGHT | B | B:track_004 | B:e10 @ 0.20 |  |
| g28 | -1.60 | TRACK_APPEARED_RIGHT | B | B:track_005 | B:e11 @ 0.20 |  |
| g29 | -1.60 | TRACK_APPEARED_RIGHT | B | B:track_006 | B:e12 @ 0.20 |  |
| g30 | -1.60 | CLOSING_START | A | A:track_002 | A:e18 @ 0.20 | active_at_first_observation=True |
| g31 | -1.60 | CLOSING_START | A | A:track_003 | A:e19 @ 0.20 | active_at_first_observation=True |
| g32 | -1.60 | CLOSING_START | A | A:track_004 | A:e20 @ 0.20 | active_at_first_observation=True |
| g33 | -1.60 | CLOSING_START | A | A:track_005 | A:e21 @ 0.20 | active_at_first_observation=True |
| g34 | -1.60 | CLOSING_START | A | A:track_006 | A:e22 @ 0.20 | active_at_first_observation=True |
| g35 | -1.60 | CLOSING_START | A | A:track_007 | A:e23 @ 0.20 | active_at_first_observation=True |
| g36 | -1.60 | CLOSING_START | A | A:track_008 | A:e24 @ 0.20 | active_at_first_observation=True |
| g37 | -1.60 | CLOSING_START | A | A:track_009 | A:e25 @ 0.20 | active_at_first_observation=True |
| g38 | -1.60 | CLOSING_START | A | A:track_010 | A:e26 @ 0.20 | active_at_first_observation=True |
| g39 | -1.60 | CLOSING_START | A | A:track_012 | A:e27 @ 0.20 | active_at_first_observation=True |
| g40 | -1.60 | CLOSING_START | B | B:track_003 | B:e13 @ 0.20 | active_at_first_observation=True |
| g41 | -1.60 | CLOSING_START | B | B:track_004 | B:e14 @ 0.20 | active_at_first_observation=True |
| g42 | -1.60 | CLOSING_START | B | B:track_005 | B:e15 @ 0.20 | active_at_first_observation=True |
| g43 | -1.60 | CLOSING_START | B | B:track_006 | B:e16 @ 0.20 | active_at_first_observation=True |
| g44 | -1.55 | TRACK_APPEARED_LEFT | B | B:track_009 | B:e17 @ 0.25 |  |
| g45 | -1.55 | TRACK_APPEARED_LEFT | B | B:track_010 | B:e18 @ 0.25 |  |
| g46 | -1.55 | TRACK_APPEARED_LEFT | B | B:track_011 | B:e19 @ 0.25 |  |
| g47 | -1.55 | TRACK_APPEARED_LEFT | B | B:track_012 | B:e20 @ 0.25 |  |
| g48 | -1.55 | TRACK_APPEARED_LEFT | B | B:track_013 | B:e21 @ 0.25 |  |
| g49 | -1.55 | TRACK_APPEARED_RIGHT | A | A:track_014 | A:e28 @ 0.25 |  |
| g50 | -1.55 | CLOSING_START | B | B:track_009 | B:e22 @ 0.25 | active_at_first_observation=True |
| g51 | -1.55 | TRACK_LOST | B | B:track_001 | B:e23 @ 0.25 |  |
| g52 | -1.50 | TRACK_APPEARED_LEFT | B | B:track_014 | B:e24 @ 0.30 |  |
| g53 | -1.50 | CLOSING_START | B | B:track_014 | B:e25 @ 0.30 | active_at_first_observation=True |
| g54 | -1.40 | TRACK_LOST | A | A:track_007 | A:e29 @ 0.40 |  |
| g55 | -1.40 | TRACK_LOST | A | A:track_011 | A:e30 @ 0.40 |  |
| g56 | -1.40 | TRACK_LOST | B | B:track_002 | B:e26 @ 0.40 |  |
| g57 | -1.40 | TRACK_LOST | B | B:track_007 | B:e27 @ 0.40 |  |
| g58 | -1.35 | TRACK_LOST | A | A:track_013 | A:e31 @ 0.45 |  |
| g59 | -1.35 | TRACK_LOST | B | B:track_008 | B:e28 @ 0.45 |  |
| g60 | -1.30 | TRACK_LOST | B | B:track_011 | B:e29 @ 0.50 |  |
| g61 | -1.25 | TRACK_LOST | B | B:track_012 | B:e30 @ 0.55 |  |
| g62 | -1.20 | TRACK_LOST | A | A:track_014 | A:e32 @ 0.60 |  |
| g63 | -1.20 | TRACK_LOST | B | B:track_013 | B:e31 @ 0.60 |  |
| g64 | -1.15 | TRACK_LOST | B | B:track_010 | B:e32 @ 0.65 |  |
| g65 | -1.00 | CLOSING_END | B | B:track_009 | B:e33 @ 0.80 |  |
| g66 | -0.90 | TRACK_LOST | B | B:track_009 | B:e34 @ 0.90 |  |
| g67 | -0.60 | TURN_RIGHT_END | B | - | B:e35 @ 1.20 |  |
| g68 | -0.35 | TRACK_LOST | A | A:track_002 | A:e33 @ 1.45 |  |
| g69 | -0.30 | TRACK_LOST | B | B:track_006 | B:e36 @ 1.50 |  |
| g70 | -0.25 | TRACK_LOST | A | A:track_009 | A:e34 @ 1.55 |  |
| g71 | -0.20 | EGO_PATH_ENTRY | A | B | A:e35 @ 1.60 |  |
| g72 | -0.15 | CUT_IN_FROM_RIGHT_START | A | B | A:e36 @ 1.65 |  |
| g73 | -0.15 | TRACK_LOST | A | A:track_005 | A:e37 @ 1.65 |  |
| g74 | -0.05 | CRITICAL_TTC_END | A | B | A:e38 @ 1.75 |  |
| g75 | 0.00 | COLLISION | - | A, B | A:e39 @ 1.80, B:e37 @ 1.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 1247.19, B 1247.19 |
| g76 | 0.05 | BRAKE_START | A | - | A:e40 @ 1.85 |  |
| g77 | 0.05 | BRAKE_START | B | - | B:e38 @ 1.85 |  |
| g78 | 0.05 | TURN_LEFT_START | B | - | B:e39 @ 1.85 |  |
| g79 | 0.05 | TRACK_LOST | A | A:track_012 | A:e41 @ 1.85 |  |
| g80 | 0.05 | TRACK_LOST | B | B:track_003 | B:e40 @ 1.85 |  |
| g81 | 0.10 | CLOSING_END | A | B | A:e42 @ 1.90 |  |
| g82 | 0.10 | TRACK_LOST | B | B:track_005 | B:e41 @ 1.90 |  |
| g83 | 0.15 | CUT_IN_FROM_RIGHT_END | A | B | A:e43 @ 1.95 |  |
| g84 | 0.15 | TRACK_LOST | B | B:track_004 | B:e42 @ 1.95 |  |
| g85 | 0.35 | CLOSING_END | B | B:track_014 | B:e43 @ 2.15 |  |
| g86 | 0.65 | CLOSING_END | A | A:track_010 | A:e44 @ 2.45 |  |
| g87 | 0.65 | TURN_LEFT_END | A | - | A:e45 @ 2.45 |  |
| g88 | 0.70 | CLOSING_END | A | A:track_003 | A:e46 @ 2.50 |  |
| g89 | 0.70 | CLOSING_END | A | A:track_004 | A:e47 @ 2.50 |  |
| g90 | 0.70 | CLOSING_END | A | A:track_006 | A:e48 @ 2.50 |  |
| g91 | 0.70 | CLOSING_END | A | A:track_008 | A:e49 @ 2.50 |  |
| g92 | 0.70 | TURN_LEFT_END | B | - | B:e44 @ 2.50 |  |
| g93 | 0.70 | MOVING_END | A | - | A:e50 @ 2.50 |  |
| g94 | 0.70 | STOP_START | A | - | A:e51 @ 2.50 |  |
| g95 | 0.75 | MOVING_END | B | - | B:e45 @ 2.55 |  |
| g96 | 0.75 | STOP_START | B | - | B:e46 @ 2.55 |  |

## Edges

```
    g01 --PRECEDES--> g11
    g01 --PRECEDES--> g12
    g01 --PRECEDES--> g13
    g01 --PRECEDES--> g14
    g01 --PRECEDES--> g15
    g01 --PRECEDES--> g16
    g01 --PRECEDES--> g17
    g01 --PRECEDES--> g18
    g01 --PRECEDES--> g19
    g01 --PRECEDES--> g20
    g01 --PRECEDES--> g21
    g01 --PRECEDES--> g22
    g01 --PRECEDES--> g23
    g01 --PRECEDES--> g24
    g01 --PRECEDES--> g25
    g01 --PRECEDES--> g26
    g01 --PRECEDES--> g27
    g01 --PRECEDES--> g28
    g01 --PRECEDES--> g29
    g01 --PRECEDES--> g30
    g01 --PRECEDES--> g31
    g01 --PRECEDES--> g32
    g01 --PRECEDES--> g33
    g01 --PRECEDES--> g34
    g01 --PRECEDES--> g35
    g01 --PRECEDES--> g36
    g01 --PRECEDES--> g37
    g01 --PRECEDES--> g38
    g01 --PRECEDES--> g39
    g01 --PRECEDES--> g40
    g01 --PRECEDES--> g41
    g01 --PRECEDES--> g42
    g01 --PRECEDES--> g43
    g02 --PRECEDES--> g11
    g02 --PRECEDES--> g12
    g02 --PRECEDES--> g13
    g02 --PRECEDES--> g14
    g02 --PRECEDES--> g15
    g02 --PRECEDES--> g16
    g02 --PRECEDES--> g17
    g02 --PRECEDES--> g18
    g02 --PRECEDES--> g19
    g02 --PRECEDES--> g20
    g02 --PRECEDES--> g21
    g02 --PRECEDES--> g22
    g02 --PRECEDES--> g23
    g02 --PRECEDES--> g24
    g02 --PRECEDES--> g25
    g02 --PRECEDES--> g26
    g02 --PRECEDES--> g27
    g02 --PRECEDES--> g28
    g02 --PRECEDES--> g29
    g02 --PRECEDES--> g30
    g02 --PRECEDES--> g31
    g02 --PRECEDES--> g32
    g02 --PRECEDES--> g33
    g02 --PRECEDES--> g34
    g02 --PRECEDES--> g35
    g02 --PRECEDES--> g36
    g02 --PRECEDES--> g37
    g02 --PRECEDES--> g38
    g02 --PRECEDES--> g39
    g02 --PRECEDES--> g40
    g02 --PRECEDES--> g41
    g02 --PRECEDES--> g42
    g02 --PRECEDES--> g43
    g03 --PRECEDES--> g11
    g03 --PRECEDES--> g12
    g03 --PRECEDES--> g13
    g03 --PRECEDES--> g14
    g03 --PRECEDES--> g15
    g03 --PRECEDES--> g16
    g03 --PRECEDES--> g17
    g03 --PRECEDES--> g18
    g03 --PRECEDES--> g19
    g03 --PRECEDES--> g20
    g03 --PRECEDES--> g21
    g03 --PRECEDES--> g22
    g03 --PRECEDES--> g23
    g03 --PRECEDES--> g24
    g03 --PRECEDES--> g25
    g03 --PRECEDES--> g26
    g03 --PRECEDES--> g27
    g03 --PRECEDES--> g28
    g03 --PRECEDES--> g29
    g03 --PRECEDES--> g30
    g03 --PRECEDES--> g31
    g03 --PRECEDES--> g32
    g03 --PRECEDES--> g33
    g03 --PRECEDES--> g34
    g03 --PRECEDES--> g35
    g03 --PRECEDES--> g36
    g03 --PRECEDES--> g37
    g03 --PRECEDES--> g38
    g03 --PRECEDES--> g39
    g03 --PRECEDES--> g40
    g03 --PRECEDES--> g41
    g03 --PRECEDES--> g42
    g03 --PRECEDES--> g43
    g04 --PRECEDES--> g11
    g04 --PRECEDES--> g12
    g04 --PRECEDES--> g13
    g04 --PRECEDES--> g14
    g04 --PRECEDES--> g15
    g04 --PRECEDES--> g16
    g04 --PRECEDES--> g17
    g04 --PRECEDES--> g18
    g04 --PRECEDES--> g19
    g04 --PRECEDES--> g20
    g04 --PRECEDES--> g21
    g04 --PRECEDES--> g22
    g04 --PRECEDES--> g23
    g04 --PRECEDES--> g24
    g04 --PRECEDES--> g25
    g04 --PRECEDES--> g26
    g04 --PRECEDES--> g27
    g04 --PRECEDES--> g28
    g04 --PRECEDES--> g29
    g04 --PRECEDES--> g30
    g04 --PRECEDES--> g31
    g04 --PRECEDES--> g32
    g04 --PRECEDES--> g33
    g04 --PRECEDES--> g34
    g04 --PRECEDES--> g35
    g04 --PRECEDES--> g36
    g04 --PRECEDES--> g37
    g04 --PRECEDES--> g38
    g04 --PRECEDES--> g39
    g04 --PRECEDES--> g40
    g04 --PRECEDES--> g41
    g04 --PRECEDES--> g42
    g04 --PRECEDES--> g43
    g05 --PRECEDES--> g11
    g05 --PRECEDES--> g12
    g05 --PRECEDES--> g13
    g05 --PRECEDES--> g14
    g05 --PRECEDES--> g15
    g05 --PRECEDES--> g16
    g05 --PRECEDES--> g17
    g05 --PRECEDES--> g18
    g05 --PRECEDES--> g19
    g05 --PRECEDES--> g20
    g05 --PRECEDES--> g21
    g05 --PRECEDES--> g22
    g05 --PRECEDES--> g23
    g05 --PRECEDES--> g24
    g05 --PRECEDES--> g25
    g05 --PRECEDES--> g26
    g05 --PRECEDES--> g27
    g05 --PRECEDES--> g28
    g05 --PRECEDES--> g29
    g05 --PRECEDES--> g30
    g05 --PRECEDES--> g31
    g05 --PRECEDES--> g32
    g05 --PRECEDES--> g33
    g05 --PRECEDES--> g34
    g05 --PRECEDES--> g35
    g05 --PRECEDES--> g36
    g05 --PRECEDES--> g37
    g05 --PRECEDES--> g38
    g05 --PRECEDES--> g39
    g05 --PRECEDES--> g40
    g05 --PRECEDES--> g41
    g05 --PRECEDES--> g42
    g05 --PRECEDES--> g43
    g06 --PRECEDES--> g11
    g06 --PRECEDES--> g12
    g06 --PRECEDES--> g13
    g06 --PRECEDES--> g14
    g06 --PRECEDES--> g15
    g06 --PRECEDES--> g16
    g06 --PRECEDES--> g17
    g06 --PRECEDES--> g18
    g06 --PRECEDES--> g19
    g06 --PRECEDES--> g20
    g06 --PRECEDES--> g21
    g06 --PRECEDES--> g22
    g06 --PRECEDES--> g23
    g06 --PRECEDES--> g24
    g06 --PRECEDES--> g25
    g06 --PRECEDES--> g26
    g06 --PRECEDES--> g27
    g06 --PRECEDES--> g28
    g06 --PRECEDES--> g29
    g06 --PRECEDES--> g30
    g06 --PRECEDES--> g31
    g06 --PRECEDES--> g32
    g06 --PRECEDES--> g33
    g06 --PRECEDES--> g34
    g06 --PRECEDES--> g35
    g06 --PRECEDES--> g36
    g06 --PRECEDES--> g37
    g06 --PRECEDES--> g38
    g06 --PRECEDES--> g39
    g06 --PRECEDES--> g40
    g06 --PRECEDES--> g41
    g06 --PRECEDES--> g42
    g06 --PRECEDES--> g43
    g07 --PRECEDES--> g11
    g07 --PRECEDES--> g12
    g07 --PRECEDES--> g13
    g07 --PRECEDES--> g14
    g07 --PRECEDES--> g15
    g07 --PRECEDES--> g16
    g07 --PRECEDES--> g17
    g07 --PRECEDES--> g18
    g07 --PRECEDES--> g19
    g07 --PRECEDES--> g20
    g07 --PRECEDES--> g21
    g07 --PRECEDES--> g22
    g07 --PRECEDES--> g23
    g07 --PRECEDES--> g24
    g07 --PRECEDES--> g25
    g07 --PRECEDES--> g26
    g07 --PRECEDES--> g27
    g07 --PRECEDES--> g28
    g07 --PRECEDES--> g29
    g07 --PRECEDES--> g30
    g07 --PRECEDES--> g31
    g07 --PRECEDES--> g32
    g07 --PRECEDES--> g33
    g07 --PRECEDES--> g34
    g07 --PRECEDES--> g35
    g07 --PRECEDES--> g36
    g07 --PRECEDES--> g37
    g07 --PRECEDES--> g38
    g07 --PRECEDES--> g39
    g07 --PRECEDES--> g40
    g07 --PRECEDES--> g41
    g07 --PRECEDES--> g42
    g07 --PRECEDES--> g43
    g08 --PRECEDES--> g11
    g08 --PRECEDES--> g12
    g08 --PRECEDES--> g13
    g08 --PRECEDES--> g14
    g08 --PRECEDES--> g15
    g08 --PRECEDES--> g16
    g08 --PRECEDES--> g17
    g08 --PRECEDES--> g18
    g08 --PRECEDES--> g19
    g08 --PRECEDES--> g20
    g08 --PRECEDES--> g21
    g08 --PRECEDES--> g22
    g08 --PRECEDES--> g23
    g08 --PRECEDES--> g24
    g08 --PRECEDES--> g25
    g08 --PRECEDES--> g26
    g08 --PRECEDES--> g27
    g08 --PRECEDES--> g28
    g08 --PRECEDES--> g29
    g08 --PRECEDES--> g30
    g08 --PRECEDES--> g31
    g08 --PRECEDES--> g32
    g08 --PRECEDES--> g33
    g08 --PRECEDES--> g34
    g08 --PRECEDES--> g35
    g08 --PRECEDES--> g36
    g08 --PRECEDES--> g37
    g08 --PRECEDES--> g38
    g08 --PRECEDES--> g39
    g08 --PRECEDES--> g40
    g08 --PRECEDES--> g41
    g08 --PRECEDES--> g42
    g08 --PRECEDES--> g43
    g09 --PRECEDES--> g11
    g09 --PRECEDES--> g12
    g09 --PRECEDES--> g13
    g09 --PRECEDES--> g14
    g09 --PRECEDES--> g15
    g09 --PRECEDES--> g16
    g09 --PRECEDES--> g17
    g09 --PRECEDES--> g18
    g09 --PRECEDES--> g19
    g09 --PRECEDES--> g20
    g09 --PRECEDES--> g21
    g09 --PRECEDES--> g22
    g09 --PRECEDES--> g23
    g09 --PRECEDES--> g24
    g09 --PRECEDES--> g25
    g09 --PRECEDES--> g26
    g09 --PRECEDES--> g27
    g09 --PRECEDES--> g28
    g09 --PRECEDES--> g29
    g09 --PRECEDES--> g30
    g09 --PRECEDES--> g31
    g09 --PRECEDES--> g32
    g09 --PRECEDES--> g33
    g09 --PRECEDES--> g34
    g09 --PRECEDES--> g35
    g09 --PRECEDES--> g36
    g09 --PRECEDES--> g37
    g09 --PRECEDES--> g38
    g09 --PRECEDES--> g39
    g09 --PRECEDES--> g40
    g09 --PRECEDES--> g41
    g09 --PRECEDES--> g42
    g09 --PRECEDES--> g43
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g10 --PRECEDES--> g13
    g10 --PRECEDES--> g14
    g10 --PRECEDES--> g15
    g10 --PRECEDES--> g16
    g10 --PRECEDES--> g17
    g10 --PRECEDES--> g18
    g10 --PRECEDES--> g19
    g10 --PRECEDES--> g20
    g10 --PRECEDES--> g21
    g10 --PRECEDES--> g22
    g10 --PRECEDES--> g23
    g10 --PRECEDES--> g24
    g10 --PRECEDES--> g25
    g10 --PRECEDES--> g26
    g10 --PRECEDES--> g27
    g10 --PRECEDES--> g28
    g10 --PRECEDES--> g29
    g10 --PRECEDES--> g30
    g10 --PRECEDES--> g31
    g10 --PRECEDES--> g32
    g10 --PRECEDES--> g33
    g10 --PRECEDES--> g34
    g10 --PRECEDES--> g35
    g10 --PRECEDES--> g36
    g10 --PRECEDES--> g37
    g10 --PRECEDES--> g38
    g10 --PRECEDES--> g39
    g10 --PRECEDES--> g40
    g10 --PRECEDES--> g41
    g10 --PRECEDES--> g42
    g10 --PRECEDES--> g43
    g11 --PRECEDES--> g44
    g11 --PRECEDES--> g45
    g11 --PRECEDES--> g46
    g11 --PRECEDES--> g47
    g11 --PRECEDES--> g48
    g11 --PRECEDES--> g49
    g11 --PRECEDES--> g50
    g11 --PRECEDES--> g51
    g12 --PRECEDES--> g44
    g12 --PRECEDES--> g45
    g12 --PRECEDES--> g46
    g12 --PRECEDES--> g47
    g12 --PRECEDES--> g48
    g12 --PRECEDES--> g49
    g12 --PRECEDES--> g50
    g12 --PRECEDES--> g51
    g13 --PRECEDES--> g44
    g13 --PRECEDES--> g45
    g13 --PRECEDES--> g46
    g13 --PRECEDES--> g47
    g13 --PRECEDES--> g48
    g13 --PRECEDES--> g49
    g13 --PRECEDES--> g50
    g13 --PRECEDES--> g51
    g14 --PRECEDES--> g44
    g14 --PRECEDES--> g45
    g14 --PRECEDES--> g46
    g14 --PRECEDES--> g47
    g14 --PRECEDES--> g48
    g14 --PRECEDES--> g49
    g14 --PRECEDES--> g50
    g14 --PRECEDES--> g51
    g15 --PRECEDES--> g44
    g15 --PRECEDES--> g45
    g15 --PRECEDES--> g46
    g15 --PRECEDES--> g47
    g15 --PRECEDES--> g48
    g15 --PRECEDES--> g49
    g15 --PRECEDES--> g50
    g15 --PRECEDES--> g51
    g16 --PRECEDES--> g44
    g16 --PRECEDES--> g45
    g16 --PRECEDES--> g46
    g16 --PRECEDES--> g47
    g16 --PRECEDES--> g48
    g16 --PRECEDES--> g49
    g16 --PRECEDES--> g50
    g16 --PRECEDES--> g51
    g17 --PRECEDES--> g44
    g17 --PRECEDES--> g45
    g17 --PRECEDES--> g46
    g17 --PRECEDES--> g47
    g17 --PRECEDES--> g48
    g17 --PRECEDES--> g49
    g17 --PRECEDES--> g50
    g17 --PRECEDES--> g51
    g18 --PRECEDES--> g44
    g18 --PRECEDES--> g45
    g18 --PRECEDES--> g46
    g18 --PRECEDES--> g47
    g18 --PRECEDES--> g48
    g18 --PRECEDES--> g49
    g18 --PRECEDES--> g50
    g18 --PRECEDES--> g51
    g19 --PRECEDES--> g44
    g19 --PRECEDES--> g45
    g19 --PRECEDES--> g46
    g19 --PRECEDES--> g47
    g19 --PRECEDES--> g48
    g19 --PRECEDES--> g49
    g19 --PRECEDES--> g50
    g19 --PRECEDES--> g51
    g20 --PRECEDES--> g44
    g20 --PRECEDES--> g45
    g20 --PRECEDES--> g46
    g20 --PRECEDES--> g47
    g20 --PRECEDES--> g48
    g20 --PRECEDES--> g49
    g20 --PRECEDES--> g50
    g20 --PRECEDES--> g51
    g21 --PRECEDES--> g44
    g21 --PRECEDES--> g45
    g21 --PRECEDES--> g46
    g21 --PRECEDES--> g47
    g21 --PRECEDES--> g48
    g21 --PRECEDES--> g49
    g21 --PRECEDES--> g50
    g21 --PRECEDES--> g51
    g22 --PRECEDES--> g44
    g22 --PRECEDES--> g45
    g22 --PRECEDES--> g46
    g22 --PRECEDES--> g47
    g22 --PRECEDES--> g48
    g22 --PRECEDES--> g49
    g22 --PRECEDES--> g50
    g22 --PRECEDES--> g51
    g23 --PRECEDES--> g44
    g23 --PRECEDES--> g45
    g23 --PRECEDES--> g46
    g23 --PRECEDES--> g47
    g23 --PRECEDES--> g48
    g23 --PRECEDES--> g49
    g23 --PRECEDES--> g50
    g23 --PRECEDES--> g51
    g24 --PRECEDES--> g44
    g24 --PRECEDES--> g45
    g24 --PRECEDES--> g46
    g24 --PRECEDES--> g47
    g24 --PRECEDES--> g48
    g24 --PRECEDES--> g49
    g24 --PRECEDES--> g50
    g24 --PRECEDES--> g51
    g25 --PRECEDES--> g44
    g25 --PRECEDES--> g45
    g25 --PRECEDES--> g46
    g25 --PRECEDES--> g47
    g25 --PRECEDES--> g48
    g25 --PRECEDES--> g49
    g25 --PRECEDES--> g50
    g25 --PRECEDES--> g51
    g26 --PRECEDES--> g44
    g26 --PRECEDES--> g45
    g26 --PRECEDES--> g46
    g26 --PRECEDES--> g47
    g26 --PRECEDES--> g48
    g26 --PRECEDES--> g49
    g26 --PRECEDES--> g50
    g26 --PRECEDES--> g51
    g27 --PRECEDES--> g44
    g27 --PRECEDES--> g45
    g27 --PRECEDES--> g46
    g27 --PRECEDES--> g47
    g27 --PRECEDES--> g48
    g27 --PRECEDES--> g49
    g27 --PRECEDES--> g50
    g27 --PRECEDES--> g51
    g28 --PRECEDES--> g44
    g28 --PRECEDES--> g45
    g28 --PRECEDES--> g46
    g28 --PRECEDES--> g47
    g28 --PRECEDES--> g48
    g28 --PRECEDES--> g49
    g28 --PRECEDES--> g50
    g28 --PRECEDES--> g51
    g29 --PRECEDES--> g44
    g29 --PRECEDES--> g45
    g29 --PRECEDES--> g46
    g29 --PRECEDES--> g47
    g29 --PRECEDES--> g48
    g29 --PRECEDES--> g49
    g29 --PRECEDES--> g50
    g29 --PRECEDES--> g51
    g30 --PRECEDES--> g44
    g30 --PRECEDES--> g45
    g30 --PRECEDES--> g46
    g30 --PRECEDES--> g47
    g30 --PRECEDES--> g48
    g30 --PRECEDES--> g49
    g30 --PRECEDES--> g50
    g30 --PRECEDES--> g51
    g31 --PRECEDES--> g44
    g31 --PRECEDES--> g45
    g31 --PRECEDES--> g46
    g31 --PRECEDES--> g47
    g31 --PRECEDES--> g48
    g31 --PRECEDES--> g49
    g31 --PRECEDES--> g50
    g31 --PRECEDES--> g51
    g32 --PRECEDES--> g44
    g32 --PRECEDES--> g45
    g32 --PRECEDES--> g46
    g32 --PRECEDES--> g47
    g32 --PRECEDES--> g48
    g32 --PRECEDES--> g49
    g32 --PRECEDES--> g50
    g32 --PRECEDES--> g51
    g33 --PRECEDES--> g44
    g33 --PRECEDES--> g45
    g33 --PRECEDES--> g46
    g33 --PRECEDES--> g47
    g33 --PRECEDES--> g48
    g33 --PRECEDES--> g49
    g33 --PRECEDES--> g50
    g33 --PRECEDES--> g51
    g34 --PRECEDES--> g44
    g34 --PRECEDES--> g45
    g34 --PRECEDES--> g46
    g34 --PRECEDES--> g47
    g34 --PRECEDES--> g48
    g34 --PRECEDES--> g49
    g34 --PRECEDES--> g50
    g34 --PRECEDES--> g51
    g35 --PRECEDES--> g44
    g35 --PRECEDES--> g45
    g35 --PRECEDES--> g46
    g35 --PRECEDES--> g47
    g35 --PRECEDES--> g48
    g35 --PRECEDES--> g49
    g35 --PRECEDES--> g50
    g35 --PRECEDES--> g51
    g36 --PRECEDES--> g44
    g36 --PRECEDES--> g45
    g36 --PRECEDES--> g46
    g36 --PRECEDES--> g47
    g36 --PRECEDES--> g48
    g36 --PRECEDES--> g49
    g36 --PRECEDES--> g50
    g36 --PRECEDES--> g51
    g37 --PRECEDES--> g44
    g37 --PRECEDES--> g45
    g37 --PRECEDES--> g46
    g37 --PRECEDES--> g47
    g37 --PRECEDES--> g48
    g37 --PRECEDES--> g49
    g37 --PRECEDES--> g50
    g37 --PRECEDES--> g51
    g38 --PRECEDES--> g44
    g38 --PRECEDES--> g45
    g38 --PRECEDES--> g46
    g38 --PRECEDES--> g47
    g38 --PRECEDES--> g48
    g38 --PRECEDES--> g49
    g38 --PRECEDES--> g50
    g38 --PRECEDES--> g51
    g39 --PRECEDES--> g44
    g39 --PRECEDES--> g45
    g39 --PRECEDES--> g46
    g39 --PRECEDES--> g47
    g39 --PRECEDES--> g48
    g39 --PRECEDES--> g49
    g39 --PRECEDES--> g50
    g39 --PRECEDES--> g51
    g40 --PRECEDES--> g44
    g40 --PRECEDES--> g45
    g40 --PRECEDES--> g46
    g40 --PRECEDES--> g47
    g40 --PRECEDES--> g48
    g40 --PRECEDES--> g49
    g40 --PRECEDES--> g50
    g40 --PRECEDES--> g51
    g41 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g41 --PRECEDES--> g46
    g41 --PRECEDES--> g47
    g41 --PRECEDES--> g48
    g41 --PRECEDES--> g49
    g41 --PRECEDES--> g50
    g41 --PRECEDES--> g51
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g42 --PRECEDES--> g48
    g42 --PRECEDES--> g49
    g42 --PRECEDES--> g50
    g42 --PRECEDES--> g51
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g43 --PRECEDES--> g50
    g43 --PRECEDES--> g51
    g44 --PRECEDES--> g52
    g44 --PRECEDES--> g53
    g45 --PRECEDES--> g52
    g45 --PRECEDES--> g53
    g46 --PRECEDES--> g52
    g46 --PRECEDES--> g53
    g47 --PRECEDES--> g52
    g47 --PRECEDES--> g53
    g48 --PRECEDES--> g52
    g48 --PRECEDES--> g53
    g49 --PRECEDES--> g52
    g49 --PRECEDES--> g53
    g50 --PRECEDES--> g52
    g50 --PRECEDES--> g53
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g52 --PRECEDES--> g55
    g52 --PRECEDES--> g56
    g52 --PRECEDES--> g57
    g53 --PRECEDES--> g54
    g53 --PRECEDES--> g55
    g53 --PRECEDES--> g56
    g53 --PRECEDES--> g57
    g54 --PRECEDES--> g58
    g54 --PRECEDES--> g59
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g57 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g58 --PRECEDES--> g60
    g59 --PRECEDES--> g60
    g60 --PRECEDES--> g61
    g61 --PRECEDES--> g62
    g61 --PRECEDES--> g63
    g62 --PRECEDES--> g64
    g63 --PRECEDES--> g64
    g64 --PRECEDES--> g65
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g67 --PRECEDES--> g68
    g68 --PRECEDES--> g69
    g69 --PRECEDES--> g70
    g70 --PRECEDES--> g71
    g71 --PRECEDES--> g72
    g71 --PRECEDES--> g73
    g72 --PRECEDES--> g74
    g73 --PRECEDES--> g74
    g74 --PRECEDES--> g75
    g75 --PRECEDES--> g76
    g75 --PRECEDES--> g77
    g75 --PRECEDES--> g78
    g75 --PRECEDES--> g79
    g75 --PRECEDES--> g80
    g76 --PRECEDES--> g81
    g76 --PRECEDES--> g82
    g77 --PRECEDES--> g81
    g77 --PRECEDES--> g82
    g78 --PRECEDES--> g81
    g78 --PRECEDES--> g82
    g79 --PRECEDES--> g81
    g79 --PRECEDES--> g82
    g80 --PRECEDES--> g81
    g80 --PRECEDES--> g82
    g81 --PRECEDES--> g83
    g81 --PRECEDES--> g84
    g82 --PRECEDES--> g83
    g82 --PRECEDES--> g84
    g83 --PRECEDES--> g85
    g84 --PRECEDES--> g85
    g85 --PRECEDES--> g86
    g85 --PRECEDES--> g87
    g86 --PRECEDES--> g88
    g86 --PRECEDES--> g89
    g86 --PRECEDES--> g90
    g86 --PRECEDES--> g91
    g86 --PRECEDES--> g92
    g86 --PRECEDES--> g93
    g86 --PRECEDES--> g94
    g87 --PRECEDES--> g88
    g87 --PRECEDES--> g89
    g87 --PRECEDES--> g90
    g87 --PRECEDES--> g91
    g87 --PRECEDES--> g92
    g87 --PRECEDES--> g93
    g87 --PRECEDES--> g94
    g88 --PRECEDES--> g95
    g88 --PRECEDES--> g96
    g89 --PRECEDES--> g95
    g89 --PRECEDES--> g96
    g90 --PRECEDES--> g95
    g90 --PRECEDES--> g96
    g91 --PRECEDES--> g95
    g91 --PRECEDES--> g96
    g92 --PRECEDES--> g95
    g92 --PRECEDES--> g96
    g93 --PRECEDES--> g95
    g93 --PRECEDES--> g96
    g94 --PRECEDES--> g95
    g94 --PRECEDES--> g96
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g09
    g11 --SAME_TRACK--> g30
    g12 --SAME_TRACK--> g31
    g13 --SAME_TRACK--> g32
    g14 --SAME_TRACK--> g33
    g15 --SAME_TRACK--> g34
    g16 --SAME_TRACK--> g35
    g17 --SAME_TRACK--> g36
    g18 --SAME_TRACK--> g37
    g19 --SAME_TRACK--> g38
    g20 --SAME_TRACK--> g39
    g16 --SAME_TRACK--> g54
    g24 --SAME_TRACK--> g55
    g25 --SAME_TRACK--> g58
    g49 --SAME_TRACK--> g62
    g11 --SAME_TRACK--> g68
    g18 --SAME_TRACK--> g70
    g06 --SAME_TRACK--> g71
    g06 --SAME_TRACK--> g72
    g14 --SAME_TRACK--> g73
    g06 --SAME_TRACK--> g74
    g20 --SAME_TRACK--> g79
    g06 --SAME_TRACK--> g81
    g06 --SAME_TRACK--> g83
    g19 --SAME_TRACK--> g86
    g12 --SAME_TRACK--> g88
    g13 --SAME_TRACK--> g89
    g15 --SAME_TRACK--> g90
    g17 --SAME_TRACK--> g91
    g05 --SAME_TRACK--> g08
    g05 --SAME_TRACK--> g10
    g26 --SAME_TRACK--> g40
    g27 --SAME_TRACK--> g41
    g28 --SAME_TRACK--> g42
    g29 --SAME_TRACK--> g43
    g44 --SAME_TRACK--> g50
    g05 --SAME_TRACK--> g51
    g52 --SAME_TRACK--> g53
    g21 --SAME_TRACK--> g56
    g22 --SAME_TRACK--> g57
    g23 --SAME_TRACK--> g59
    g46 --SAME_TRACK--> g60
    g47 --SAME_TRACK--> g61
    g48 --SAME_TRACK--> g63
    g45 --SAME_TRACK--> g64
    g44 --SAME_TRACK--> g65
    g44 --SAME_TRACK--> g66
    g29 --SAME_TRACK--> g69
    g26 --SAME_TRACK--> g80
    g28 --SAME_TRACK--> g82
    g27 --SAME_TRACK--> g84
    g52 --SAME_TRACK--> g85
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -1.80 | MOVING_START(A); MOVING_START(B); TURN_LEFT_START(A); TURN_RIGHT_START(B); TRACK_APPEARED_LEFT(B,B:track_001); TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CLOSING_START(B,B:track_001); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,B:track_001) |
| -1.60 | TRACK_APPEARED_LEFT(A,A:track_002); TRACK_APPEARED_LEFT(A,A:track_003); TRACK_APPEARED_LEFT(A,A:track_004); TRACK_APPEARED_LEFT(A,A:track_005); TRACK_APPEARED_LEFT(A,A:track_006); TRACK_APPEARED_LEFT(A,A:track_007); TRACK_APPEARED_LEFT(A,A:track_008); TRACK_APPEARED_LEFT(A,A:track_009); TRACK_APPEARED_LEFT(A,A:track_010); TRACK_APPEARED_LEFT(A,A:track_012); TRACK_APPEARED_LEFT(B,B:track_002); TRACK_APPEARED_LEFT(B,B:track_007); TRACK_APPEARED_LEFT(B,B:track_008); TRACK_APPEARED_RIGHT(A,A:track_011); TRACK_APPEARED_RIGHT(A,A:track_013); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); TRACK_APPEARED_RIGHT(B,B:track_006); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008); CLOSING_START(A,A:track_009); CLOSING_START(A,A:track_010); CLOSING_START(A,A:track_012); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006) |
| -1.55 | TRACK_APPEARED_LEFT(B,B:track_009); TRACK_APPEARED_LEFT(B,B:track_010); TRACK_APPEARED_LEFT(B,B:track_011); TRACK_APPEARED_LEFT(B,B:track_012); TRACK_APPEARED_LEFT(B,B:track_013); TRACK_APPEARED_RIGHT(A,A:track_014); CLOSING_START(B,B:track_009); TRACK_LOST(B,B:track_001) |
| -1.50 | TRACK_APPEARED_LEFT(B,B:track_014); CLOSING_START(B,B:track_014) |
| -1.40 | TRACK_LOST(A,A:track_007); TRACK_LOST(A,A:track_011); TRACK_LOST(B,B:track_002); TRACK_LOST(B,B:track_007) |
| -1.35 | TRACK_LOST(A,A:track_013); TRACK_LOST(B,B:track_008) |
| -1.30 | TRACK_LOST(B,B:track_011) |
| -1.25 | TRACK_LOST(B,B:track_012) |
| -1.20 | TRACK_LOST(A,A:track_014); TRACK_LOST(B,B:track_013) |
| -1.15 | TRACK_LOST(B,B:track_010) |
| -1.00 | CLOSING_END(B,B:track_009) |
| -0.90 | TRACK_LOST(B,B:track_009) |
| -0.60 | TURN_RIGHT_END(B) |
| -0.35 | TRACK_LOST(A,A:track_002) |
| -0.30 | TRACK_LOST(B,B:track_006) |
| -0.25 | TRACK_LOST(A,A:track_009) |
| -0.20 | EGO_PATH_ENTRY(A,B) |
| -0.15 | CUT_IN_FROM_RIGHT_START(A,B); TRACK_LOST(A,A:track_005) |
| -0.05 | CRITICAL_TTC_END(A,B) |
| +0.00 | COLLISION(A,B) |
| +0.05 | BRAKE_START(A); BRAKE_START(B); TURN_LEFT_START(B); TRACK_LOST(A,A:track_012); TRACK_LOST(B,B:track_003) |
| +0.10 | CLOSING_END(A,B); TRACK_LOST(B,B:track_005) |
| +0.15 | CUT_IN_FROM_RIGHT_END(A,B); TRACK_LOST(B,B:track_004) |
| +0.35 | CLOSING_END(B,B:track_014) |
| +0.65 | CLOSING_END(A,A:track_010); TURN_LEFT_END(A) |
| +0.70 | CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_006); CLOSING_END(A,A:track_008); TURN_LEFT_END(B); MOVING_END(A); STOP_START(A) |
| +0.75 | MOVING_END(B); STOP_START(B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): critical TTC already active before the cut-in: CRITICAL_TTC_START 0.00 <= CUT_IN_FROM_RIGHT_START 1.65 (+1.65 s); EGO_PATH_ENTRY 1.60 after critical TTC (+1.60 s) [local times; t_global: cut_in -0.15, critical_ttc_start -1.80, ego_path_entry -0.20, collision +0.00]
- B's track_001 (unidentified B:track_001): CRITICAL_TTC_START 0.00, COLLISION 1.80 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -1.80 | A | g01 MOVING_START(A) (A:e01)<br>g03 TURN_LEFT_START(A) (A:e02)<br>g06 TRACK_APPEARED_RIGHT(A,B) (A:e03)<br>g07 CLOSING_START(A,B) (A:e04)<br>g09 CRITICAL_TTC_START(A,B) (A:e05) | ego: not yet observed |
| -1.80 | B | g02 MOVING_START(B) (B:e01)<br>g04 TURN_RIGHT_START(B) (B:e02)<br>g05 TRACK_APPEARED_LEFT(B,B:track_001) (B:e03)<br>g08 CLOSING_START(B,B:track_001) (B:e04)<br>g10 CRITICAL_TTC_START(B,B:track_001) (B:e05) | ego: not yet observed |
| -1.60 | A | g11 TRACK_APPEARED_LEFT(A,A:track_002) (A:e06)<br>g12 TRACK_APPEARED_LEFT(A,A:track_003) (A:e07)<br>g13 TRACK_APPEARED_LEFT(A,A:track_004) (A:e08)<br>g14 TRACK_APPEARED_LEFT(A,A:track_005) (A:e09)<br>g15 TRACK_APPEARED_LEFT(A,A:track_006) (A:e10)<br>g16 TRACK_APPEARED_LEFT(A,A:track_007) (A:e11)<br>g17 TRACK_APPEARED_LEFT(A,A:track_008) (A:e12)<br>g18 TRACK_APPEARED_LEFT(A,A:track_009) (A:e13)<br>g19 TRACK_APPEARED_LEFT(A,A:track_010) (A:e14)<br>g20 TRACK_APPEARED_LEFT(A,A:track_012) (A:e15)<br>g24 TRACK_APPEARED_RIGHT(A,A:track_011) (A:e16)<br>g25 TRACK_APPEARED_RIGHT(A,A:track_013) (A:e17)<br>g30 CLOSING_START(A,A:track_002) (A:e18)<br>g31 CLOSING_START(A,A:track_003) (A:e19)<br>g32 CLOSING_START(A,A:track_004) (A:e20)<br>g33 CLOSING_START(A,A:track_005) (A:e21)<br>g34 CLOSING_START(A,A:track_006) (A:e22)<br>g35 CLOSING_START(A,A:track_007) (A:e23)<br>g36 CLOSING_START(A,A:track_008) (A:e24)<br>g37 CLOSING_START(A,A:track_009) (A:e25)<br>g38 CLOSING_START(A,A:track_010) (A:e26)<br>g39 CLOSING_START(A,A:track_012) (A:e27) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC |
| -1.60 | B | g21 TRACK_APPEARED_LEFT(B,B:track_002) (B:e06)<br>g22 TRACK_APPEARED_LEFT(B,B:track_007) (B:e07)<br>g23 TRACK_APPEARED_LEFT(B,B:track_008) (B:e08)<br>g26 TRACK_APPEARED_RIGHT(B,B:track_003) (B:e09)<br>g27 TRACK_APPEARED_RIGHT(B,B:track_004) (B:e10)<br>g28 TRACK_APPEARED_RIGHT(B,B:track_005) (B:e11)<br>g29 TRACK_APPEARED_RIGHT(B,B:track_006) (B:e12)<br>g40 CLOSING_START(B,B:track_003) (B:e13)<br>g41 CLOSING_START(B,B:track_004) (B:e14)<br>g42 CLOSING_START(B,B:track_005) (B:e15)<br>g43 CLOSING_START(B,B:track_006) (B:e16) | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -1.55 | B | g44 TRACK_APPEARED_LEFT(B,B:track_009) (B:e17)<br>g45 TRACK_APPEARED_LEFT(B,B:track_010) (B:e18)<br>g46 TRACK_APPEARED_LEFT(B,B:track_011) (B:e19)<br>g47 TRACK_APPEARED_LEFT(B,B:track_012) (B:e20)<br>g48 TRACK_APPEARED_LEFT(B,B:track_013) (B:e21)<br>g50 CLOSING_START(B,B:track_009) (B:e22)<br>g51 TRACK_LOST(B,B:track_001) (B:e23) | ego: MOVING, TURN_RIGHT<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -1.55 | A | g49 TRACK_APPEARED_RIGHT(A,A:track_014) (A:e28) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -1.50 | B | g52 TRACK_APPEARED_LEFT(B,B:track_014) (B:e24)<br>g53 CLOSING_START(B,B:track_014) (B:e25) | ego: MOVING, TURN_RIGHT<br>track_002: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001 |
| -1.40 | A | g54 TRACK_LOST(A,A:track_007) (A:e29)<br>g55 TRACK_LOST(A,A:track_011) (A:e30) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CLOSING<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? |
| -1.40 | B | g56 TRACK_LOST(B,B:track_002) (B:e26)<br>g57 TRACK_LOST(B,B:track_007) (B:e27) | ego: MOVING, TURN_RIGHT<br>track_002: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001 |
| -1.35 | A | g58 TRACK_LOST(A,A:track_013) (A:e31) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_007, track_011 |
| -1.35 | B | g59 TRACK_LOST(B,B:track_008) (B:e28) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007 |
| -1.30 | B | g60 TRACK_LOST(B,B:track_011) (B:e29) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_011: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008 |
| -1.25 | B | g61 TRACK_LOST(B,B:track_012) (B:e30) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_011 |
| -1.20 | A | g62 TRACK_LOST(A,A:track_014) (A:e32) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track_014: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_007, track_011, track_013 |
| -1.20 | B | g63 TRACK_LOST(B,B:track_013) (B:e31) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_013: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_011, track_012 |
| -1.15 | B | g64 TRACK_LOST(B,B:track_010) (B:e32) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_010: no active state<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_011, track_012, track_013 |
| -1.00 | B | g65 CLOSING_END(B,B:track_009) (B:e33) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_010, track_011, track_012, track_013 |
| -0.90 | B | g66 TRACK_LOST(B,B:track_009) (B:e34) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_009: no active state<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_010, track_011, track_012, track_013 |
| -0.60 | B | g67 TURN_RIGHT_END(B) (B:e35) | ego: MOVING, TURN_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| -0.35 | A | g68 TRACK_LOST(A,A:track_002) (A:e33) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_007, track_011, track_013, track_014 |
| -0.30 | B | g69 TRACK_LOST(B,B:track_006) (B:e36) | ego: MOVING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| -0.25 | A | g70 TRACK_LOST(A,A:track_009) (A:e34) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_007, track_011, track_013, track_014 |
| -0.20 | A | g71 EGO_PATH_ENTRY(A,B) (A:e35) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_007, track_009, track_011, track_013, track_014 |
| -0.15 | A | g72 CUT_IN_FROM_RIGHT_START(A,B) (A:e36)<br>g73 TRACK_LOST(A,A:track_005) (A:e37) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_007, track_009, track_011, track_013, track_014 |
| -0.05 | A | g74 CRITICAL_TTC_END(A,B) (A:e38) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_013, track_014 |
| +0.00 | A | g75 COLLISION(A,B) (A:e39) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_013, track_014 |
| +0.00 | B | g75 COLLISION(A,B) (B:e37) | ego: MOVING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +0.05 | A | g76 BRAKE_START(A) (A:e40)<br>g79 TRACK_LOST(A,A:track_012) (A:e41) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_012: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_013, track_014 |
| +0.05 | B | g77 BRAKE_START(B) (B:e38)<br>g78 TURN_LEFT_START(B) (B:e39)<br>g80 TRACK_LOST(B,B:track_003) (B:e40) | ego: MOVING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +0.10 | A | g81 CLOSING_END(A,B) (A:e42) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 |
| +0.10 | B | g82 TRACK_LOST(B,B:track_005) (B:e41) | ego: MOVING, BRAKE, TURN_LEFT<br>track_004: CLOSING<br>track_005: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +0.15 | A | g83 CUT_IN_FROM_RIGHT_END(A,B) (A:e43) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 |
| +0.15 | B | g84 TRACK_LOST(B,B:track_004) (B:e42) | ego: MOVING, BRAKE, TURN_LEFT<br>track_004: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +0.35 | B | g85 CLOSING_END(B,B:track_014) (B:e43) | ego: MOVING, BRAKE, TURN_LEFT<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +0.65 | A | g86 CLOSING_END(A,A:track_010) (A:e44)<br>g87 TURN_LEFT_END(A) (A:e45) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 |
| +0.70 | A | g88 CLOSING_END(A,A:track_003) (A:e46)<br>g89 CLOSING_END(A,A:track_004) (A:e47)<br>g90 CLOSING_END(A,A:track_006) (A:e48)<br>g91 CLOSING_END(A,A:track_008) (A:e49)<br>g93 MOVING_END(A) (A:e50)<br>g94 STOP_START(A) (A:e51) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_006: CLOSING<br>track_008: CLOSING<br>track_010: no active state<br>track lost, states UNKNOWN: track_002, track_005, track_007, track_009, track_011, track_012, track_013, track_014 |
| +0.70 | B | g92 TURN_LEFT_END(B) (B:e44) | ego: MOVING, BRAKE, TURN_LEFT<br>track_014: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |
| +0.75 | B | g95 MOVING_END(B) (B:e45)<br>g96 STOP_START(B) (B:e46) | ego: MOVING, BRAKE<br>track_014: no active state<br>track lost, states UNKNOWN: track_001, track_002, track_003, track_004, track_005, track_006, track_007, track_008, track_009, track_010, track_011, track_012, track_013 |

## Plain-language reading

- 1.80 s before the matched collision, A started moving (already the case when first observed).
- 1.80 s before the matched collision, B started moving (already the case when first observed).
- 1.80 s before the matched collision, A started turning left (already the case when first observed).
- 1.80 s before the matched collision, B started turning right (already the case when first observed).
- 1.80 s before the matched collision, B's radar started tracking unidentified object B:track_001, which appeared on its left.
- 1.80 s before the matched collision, A's radar started tracking B, which appeared on its right.
- 1.80 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 1.80 s before the matched collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.80 s before the matched collision, B's time-to-contact with unidentified object B:track_001 became critical (already the case when first observed).
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_002, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_003, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_004, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_005, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_006, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_007, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_008, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_009, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_010, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_012, which appeared on its left.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its left.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_008, which appeared on its left.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_011, which appeared on its right.
- 1.60 s before the matched collision, A's radar started tracking unidentified object A:track_013, which appeared on its right.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its right.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its right.
- 1.60 s before the matched collision, B's radar started tracking unidentified object B:track_006, which appeared on its right.
- 1.60 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_004 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_005 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_006 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_007 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_008 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_009 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_010 start closing in (already the case when first observed).
- 1.60 s before the matched collision, A observed unidentified object A:track_012 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 1.60 s before the matched collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 1.55 s before the matched collision, B's radar started tracking unidentified object B:track_009, which appeared on its left.
- 1.55 s before the matched collision, B's radar started tracking unidentified object B:track_010, which appeared on its left.
- 1.55 s before the matched collision, B's radar started tracking unidentified object B:track_011, which appeared on its left.
- 1.55 s before the matched collision, B's radar started tracking unidentified object B:track_012, which appeared on its left.
- 1.55 s before the matched collision, B's radar started tracking unidentified object B:track_013, which appeared on its left.
- 1.55 s before the matched collision, A's radar started tracking unidentified object A:track_014, which appeared on its right.
- 1.55 s before the matched collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 1.55 s before the matched collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- 1.50 s before the matched collision, B's radar started tracking unidentified object B:track_014, which appeared on its left.
- 1.50 s before the matched collision, B observed unidentified object B:track_014 start closing in (already the case when first observed).
- 1.40 s before the matched collision, A's radar lost unidentified object A:track_007 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the matched collision, A's radar lost unidentified object A:track_011 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the matched collision, B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- 1.40 s before the matched collision, B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- 1.35 s before the matched collision, A's radar lost unidentified object A:track_013 (its states are UNKNOWN from then on, not ended).
- 1.35 s before the matched collision, B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- 1.30 s before the matched collision, B's radar lost unidentified object B:track_011 (its states are UNKNOWN from then on, not ended).
- 1.25 s before the matched collision, B's radar lost unidentified object B:track_012 (its states are UNKNOWN from then on, not ended).
- 1.20 s before the matched collision, A's radar lost unidentified object A:track_014 (its states are UNKNOWN from then on, not ended).
- 1.20 s before the matched collision, B's radar lost unidentified object B:track_013 (its states are UNKNOWN from then on, not ended).
- 1.15 s before the matched collision, B's radar lost unidentified object B:track_010 (its states are UNKNOWN from then on, not ended).
- 1.00 s before the matched collision, B observed unidentified object B:track_009 stop closing in.
- 0.90 s before the matched collision, B's radar lost unidentified object B:track_009 (its states are UNKNOWN from then on, not ended).
- 0.60 s before the matched collision, B stopped turning right.
- 0.35 s before the matched collision, A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- 0.30 s before the matched collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- 0.25 s before the matched collision, A's radar lost unidentified object A:track_009 (its states are UNKNOWN from then on, not ended).
- 0.20 s before the matched collision, A observed B enter its forward path corridor.
- 0.15 s before the matched collision, A observed B cutting in from the right.
- 0.15 s before the matched collision, A's radar lost unidentified object A:track_005 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the matched collision, A's time-to-contact with B stopped being critical.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 1247, B: 1247 N*s).
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, B started turning left.
- 0.05 s after the matched collision, A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- 0.05 s after the matched collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.10 s after the matched collision, A observed B stop closing in.
- 0.10 s after the matched collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.15 s after the matched collision, A observed B's cut-in from the right settle.
- 0.15 s after the matched collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.35 s after the matched collision, B observed unidentified object B:track_014 stop closing in.
- 0.65 s after the matched collision, A observed unidentified object A:track_010 stop closing in.
- 0.65 s after the matched collision, A stopped turning left.
- 0.70 s after the matched collision, A observed unidentified object A:track_003 stop closing in.
- 0.70 s after the matched collision, A observed unidentified object A:track_004 stop closing in.
- 0.70 s after the matched collision, A observed unidentified object A:track_006 stop closing in.
- 0.70 s after the matched collision, A observed unidentified object A:track_008 stop closing in.
- 0.70 s after the matched collision, B stopped turning left.
- 0.70 s after the matched collision, A stopped moving.
- 0.70 s after the matched collision, A came to a stop.
- 0.75 s after the matched collision, B stopped moving.
- 0.75 s after the matched collision, B came to a stop.
