# Per-run OLD vs NEW details

Relative times are measured from each run's first scenario state. Position reports both world-coordinate and displacement-from-start errors. See `trajectory_metrics.csv`, `sensor_comparison.csv`, `collision_events.csv`, `collision_episodes.csv`, `trigger_events.csv`, `minimum_gap_comparison.csv`, and `maneuver_comparison.csv` for row-level values.

## S01/crash

[Trajectory overlay](trajectories/S01_crash.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True} | {'A': True, 'B': True} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 480 | 480 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0060/0.0079 | 0.0025/0.0041 | 0.0052/0.0365 | 0.0764/0.0764 |
| B | 240/240 | 0.0150/0.0150 | 0.0026/0.0026 | 0.0004/0.0393 | 0.0253/0.0255 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 6.80–6.80 | 1 | 28788.2 |
| NEW | A-B | 6.80–6.80 | 1 | 28687.8 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S02/crash

[Trajectory overlay](trajectories/S02_crash.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True} | {'A': True, 'B': True} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 15.200 | 15.200 | delta +0.000s |
| Ground-truth state rows | 608 | 608 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 304/304 | 0.0731/0.0731 | 0.0752/0.0752 | 0.0128/1.4031 | 0.0933/0.0933 |
| B | 304/304 | 0.2898/0.2898 | 0.2816/0.2816 | 0.0145/2.0579 | 0.2557/0.2559 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 5.35–5.35 | 1 | 4921.3 |
| NEW | A-B | 5.30–5.30 | 1 | 5220.9 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S03/crash

[Trajectory overlay](trajectories/S03_crash.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True} | {'A': True, 'B': True} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 15.200 | 15.200 | delta +0.000s |
| Ground-truth state rows | 608 | 608 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 304/304 | 0.0479/0.0479 | 0.0523/0.0523 | 0.0016/0.2268 | 0.5159/0.5176 |
| B | 304/304 | 0.1291/0.1291 | 0.0899/0.0899 | 0.0213/0.4332 | 1.7564/1.7565 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 4.15–4.15 | 1 | 24275.2 |
| OLD | A-B | 4.40–4.65 | 6 | 5163.0 |
| NEW | A-B | 4.15–4.15 | 1 | 23422.6 |
| NEW | A-B | 4.40–4.60 | 5 | 5737.9 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S04/a_front_pushed

[Trajectory overlay](trajectories/S04_a_front_pushed.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': True} | {'A': True, 'B': True, 'C': True} | same |
| Recorders | A, B, C | A, B, C | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 13.750 | 13.750 | delta +0.000s |
| Ground-truth state rows | 825 | 825 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 275/275 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0001 | 0.0001/0.0001 |
| B | 275/275 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0002 | 0.0019/0.0019 |
| C | 275/275 | 0.0050/0.0052 | 0.0026/0.0027 | 0.0015/0.0024 | 0.0060/0.0126 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 4.85–4.85 | 1 | 20562.8 |
| OLD | B-C | 5.35–5.35 | 1 | 17576.1 |
| OLD | A-B | 5.50–5.95 | 10 | 4328.3 |
| NEW | A-B | 4.85–4.85 | 1 | 20562.8 |
| NEW | B-C | 5.35–5.35 | 1 | 17576.5 |
| NEW | A-B | 5.50–5.95 | 10 | 4353.2 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 9 | 9/9 | 9/9 | 0.05 |
| rgb | 3 | 3/3 | 3/3 | 0.1 |
| depth | 3 | 0/3 | 0/3 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S04/b_rear_first

[Trajectory overlay](trajectories/S04_b_rear_first.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': True} | {'A': True, 'B': True, 'C': True} | same |
| Recorders | A, B, C | A, B, C | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 14.200 | 14.200 | delta +0.000s |
| Ground-truth state rows | 852 | 852 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 284/284 | 0.0002/0.0002 | 0.0002/0.0002 | 0.0000/0.0006 | 0.0053/0.0053 |
| B | 284/284 | 0.0006/0.0006 | 0.0006/0.0006 | 0.0000/0.0043 | 0.0054/0.0055 |
| C | 284/284 | 0.0144/0.0145 | 0.0033/0.0035 | 0.0021/0.0029 | 0.0072/0.0154 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | B-C | 4.75–4.75 | 1 | 43684.9 |
| OLD | A-B | 6.30–6.30 | 1 | 63412.5 |
| NEW | B-C | 4.75–4.75 | 1 | 43687.8 |
| NEW | A-B | 6.30–6.30 | 1 | 63412.0 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 9 | 9/9 | 9/9 | 0.05 |
| rgb | 3 | 3/3 | 3/3 | 0.1 |
| depth | 3 | 0/3 | 0/3 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S05/crash

[Trajectory overlay](trajectories/S05_crash.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': True} | {'A': True, 'B': True, 'C': True} | same |
| Recorders | A, B, C | A, B, C | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 13.700 | 13.700 | delta +0.000s |
| Ground-truth state rows | 822 | 822 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 274/274 | 0.0082/0.0086 | 0.0043/0.0043 | 0.0011/0.0402 | 0.1624/0.1633 |
| B | 274/274 | 0.0014/0.0015 | 0.0014/0.0015 | 0.0000/0.0219 | 0.0945/0.0947 |
| C | 274/274 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0001 | 0.0018/0.0018 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 5.95–5.95 | 1 | 44366.7 |
| NEW | A-B | 5.95–5.95 | 1 | 44237.8 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 9 | 9/9 | 9/9 | 0.05 |
| rgb | 3 | 3/3 | 3/3 | 0.1 |
| depth | 3 | 0/3 | 0/3 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S06/crash

[Trajectory overlay](trajectories/S06_crash.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': True} | {'A': True, 'B': True, 'C': True} | same |
| Recorders | A, B, C | A, B, C | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 15.200 | 15.200 | delta +0.000s |
| Ground-truth state rows | 912 | 912 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | B/depth/front_depth, C/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 304/304 | 0.0075/0.0075 | 0.0075/0.0075 | 0.0001/0.0905 | 0.0874/0.0875 |
| B | 304/304 | 0.0345/0.0345 | 0.0328/0.0328 | 0.0030/0.1608 | 0.6871/0.6873 |
| C | 304/304 | 0.0267/0.0357 | 0.0275/0.0275 | 0.0188/0.0352 | 0.1369/0.3583 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 4.15–4.15 | 1 | 24274.2 |
| OLD | A-B | 4.40–4.65 | 6 | 5175.2 |
| NEW | A-B | 4.15–4.15 | 1 | 24275.0 |
| NEW | A-B | 4.40–4.65 | 6 | 5684.5 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 9 | 9/9 | 9/9 | 0.05 |
| rgb | 3 | 3/3 | 3/3 | 0.1 |
| depth | 3 | 0/3 | 1/3 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S07/merge_conflict

[Trajectory overlay](trajectories/S07_merge_conflict.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town03_Opt | Town03_Opt | same |
| Participants | {'A': True, 'B': True} | {'A': True, 'B': True} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 32.400 | 32.400 | delta +0.000s |
| Ground-truth state rows | 1296 | 1296 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 648/648 | 0.0010/0.0010 | 0.0010/0.0010 | 0.0000/0.0061 | 0.0195/0.0206 |
| B | 648/648 | 0.0064/0.0103 | 0.0083/0.0083 | 0.0034/0.0415 | 0.0076/0.0200 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 19.30–20.50 | 24 | 4826.6 |
| NEW | A-B | 19.30–20.50 | 24 | 4787.7 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S08/rolls_through

[Trajectory overlay](trajectories/S08_rolls_through.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True} | {'A': True, 'B': True} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 16.000 | 16.000 | delta +0.000s |
| Ground-truth state rows | 640 | 640 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 320/320 | 0.0003/0.0003 | 0.0003/0.0003 | 0.0000/0.0028 | 0.0155/0.0155 |
| B | 320/320 | 0.0020/0.0046 | 0.0038/0.0064 | 0.0010/0.0411 | 0.0022/0.0026 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 5.45–5.45 | 1 | 25908.2 |
| NEW | A-B | 5.45–5.45 | 1 | 25909.0 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S09/near_simultaneous

[Trajectory overlay](trajectories/S09_near_simultaneous.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True} | {'A': True, 'B': True} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.900 | 12.900 | delta +0.000s |
| Ground-truth state rows | 516 | 516 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 258/258 | 0.0290/0.0290 | 0.0292/0.0293 | 0.0555/0.2205 | 1.5618/1.5618 |
| B | 258/258 | 0.0096/0.0096 | 0.0096/0.0096 | 0.0003/0.1657 | 0.8998/0.9000 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 7.20–7.20 | 1 | 15322.9 |
| NEW | A-B | 7.20–7.20 | 1 | 15344.6 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S10/deflected_into_c

[Trajectory overlay](trajectories/S10_deflected_into_c.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': True} | {'A': True, 'B': True, 'C': True} | same |
| Recorders | A, B, C | A, B, C | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 14.000 | 14.000 | delta +0.000s |
| Ground-truth state rows | 840 | 840 | same |
| Physical behavior gate | FAIL | FAIL | CHECK |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 280/280 | 0.2909/0.3014 | 0.2909/0.3014 | 0.0388/0.8786 | 1.2704/1.3058 |
| B | 280/280 | 0.0200/0.0252 | 0.0200/0.0223 | 0.0125/0.0168 | 0.1669/0.3162 |
| C | 280/280 | 0.4600/0.4605 | 0.2053/0.2060 | 0.1480/0.8153 | 1.7634/1.7639 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 3.85–3.85 | 1 | 20716.4 |
| OLD | A-C | 4.75–14.00 | 186 | 10527.5 |
| NEW | A-B | 3.85–3.85 | 1 | 20689.0 |
| NEW | A-C | 4.75–6.30 | 31 | 8082.2 |
| NEW | A-C | 6.50–6.75 | 6 | 25.7 |
| NEW | A-C | 7.00–7.15 | 4 | 11.6 |
| NEW | A-C | 7.55–7.60 | 2 | 1.0 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 9 | 9/9 | 9/9 | 0.05 |
| rgb | 3 | 3/3 | 3/3 | 0.1 |
| depth | 3 | 0/3 | 0/3 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S11/consequential

[Trajectory overlay](trajectories/S11_consequential.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': True} | {'A': True, 'B': True, 'C': True} | same |
| Recorders | A, B, C | A, B, C | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 720 | 720 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | A/depth/front_depth, B/depth/front_depth, C/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0016/0.0045 | 0.0016/0.0045 | 0.0024/0.0436 | 0.0344/0.0769 |
| B | 240/240 | 0.0001/0.0002 | 0.0002/0.0002 | 0.0001/0.0002 | 0.0011/0.0012 |
| C | 240/240 | 0.0021/0.0027 | 0.0023/0.0027 | 0.0054/0.0198 | 0.0334/0.0382 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 5.60–5.60 | 1 | 8487.0 |
| OLD | A-C | 6.65–6.65 | 1 | 282.2 |
| OLD | A-C | 6.90–7.50 | 13 | 5142.5 |
| OLD | A-C | 7.65–8.65 | 21 | 6067.2 |
| NEW | A-B | 5.60–5.60 | 1 | 8487.0 |
| NEW | A-C | 6.65–6.65 | 1 | 1680.3 |
| NEW | A-C | 6.90–7.50 | 13 | 4796.6 |
| NEW | A-C | 7.65–8.65 | 21 | 5984.4 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 9 | 9/9 | 9/9 | 0.05 |
| rgb | 3 | 3/3 | 3/3 | 0.1 |
| depth | 3 | 0/3 | 0/3 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S12/crash

[Trajectory overlay](trajectories/S12_crash.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': False} | {'A': True, 'B': True, 'C': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 11.000 | 11.000 | delta +0.000s |
| Ground-truth state rows | 660 | 660 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 220/220 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| B | 220/220 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| C | 220/220 | 0.0195/0.0220 | 0.0182/0.0207 | 0.0171/0.1358 | 0.0794/0.3728 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 5.00–5.80 | 15 | 4550.4 |
| NEW | A-B | 5.00–5.80 | 15 | 4550.4 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD | A | A_evasive_swerve_left | 3.300 |
| NEW | A | A_evasive_swerve_left | 3.300 |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S13/abreast

[Trajectory overlay](trajectories/S13_abreast.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': False, 'D': False} | {'A': True, 'B': True, 'C': False, 'D': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 11.500 | 11.500 | delta +0.000s |
| Ground-truth state rows | 920 | 920 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 230/230 | 0.0316/0.0316 | 0.0117/0.0117 | 0.0117/0.0168 | 0.1020/0.1020 |
| B | 230/230 | 0.0081/0.0087 | 0.0050/0.0050 | 0.0061/0.0276 | 0.0272/0.0312 |
| C | 230/230 | 0.0874/0.0884 | 0.0150/0.0198 | 0.0144/0.0522 | 0.0791/0.1643 |
| D | 230/230 | 0.0121/0.0155 | 0.0112/0.0142 | 0.0232/0.0462 | 0.0930/0.1350 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 6.25–6.50 | 5 | 2458.0 |
| NEW | A-B | 6.25–6.50 | 5 | 2439.1 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S13/platoon

[Trajectory overlay](trajectories/S13_platoon.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': False, 'D': False} | {'A': True, 'B': True, 'C': False, 'D': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 11.500 | 11.500 | delta +0.000s |
| Ground-truth state rows | 920 | 920 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 230/230 | 0.0054/0.0054 | 0.0054/0.0054 | 0.0059/0.0079 | 0.0526/0.0533 |
| B | 230/230 | 0.0085/0.0085 | 0.0016/0.0016 | 0.0016/0.0062 | 0.0227/0.0231 |
| C | 230/230 | 0.0850/0.0916 | 0.0801/0.0890 | 0.0546/0.0907 | 0.2286/0.2874 |
| D | 230/230 | 0.1527/0.1545 | 0.1111/0.1137 | 0.0981/0.1482 | 0.2058/0.3017 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 6.25–6.50 | 5 | 2814.0 |
| NEW | A-B | 6.25–6.50 | 5 | 2437.8 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S13/passing

[Trajectory overlay](trajectories/S13_passing.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': False, 'D': False} | {'A': True, 'B': True, 'C': False, 'D': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 11.500 | 11.500 | delta +0.000s |
| Ground-truth state rows | 920 | 920 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 230/230 | 0.0063/0.0064 | 0.0044/0.0044 | 0.0062/0.0353 | 0.0565/0.0565 |
| B | 230/230 | 0.0082/0.0082 | 0.0018/0.0029 | 0.0047/0.0130 | 0.0085/0.0145 |
| C | 230/230 | 0.0444/0.0445 | 0.0097/0.0118 | 0.0045/0.0350 | 0.0222/0.1044 |
| D | 230/230 | 0.0153/0.0158 | 0.0074/0.0081 | 0.0139/0.0529 | 0.0654/0.1243 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 6.25–6.50 | 5 | 2421.6 |
| NEW | A-B | 6.25–6.50 | 5 | 2812.7 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S14/surrounded

[Trajectory overlay](trajectories/S14_surrounded.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False, 'H': False, 'J': False, 'P': False} | {'A': True, 'B': True, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False, 'H': False, 'J': False, 'P': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 2400 | 2400 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0329/0.0426 | 0.0315/0.0412 | 0.0161/0.0758 | 0.0830/0.1870 |
| B | 240/240 | 0.0330/0.0427 | 0.0330/0.0427 | 0.0156/0.0174 | 0.0763/0.0834 |
| C | 240/240 | 0.0065/0.0078 | 0.0018/0.0035 | 0.0047/0.0389 | 0.0129/0.0181 |
| D | 240/240 | 0.0014/0.0014 | 0.0014/0.0014 | 0.0007/0.0028 | 0.0008/0.0009 |
| E | 240/240 | 0.0004/0.0005 | 0.0004/0.0005 | 0.0003/0.0017 | 0.0002/0.0003 |
| F | 240/240 | 0.0029/0.0030 | 0.0029/0.0030 | 0.0023/0.0058 | 0.0016/0.0017 |
| G | 240/240 | 0.0323/0.0325 | 0.0105/0.0142 | 0.0081/0.0446 | 0.0419/0.1070 |
| H | 240/240 | 0.0028/0.0045 | 0.0049/0.0050 | 0.0027/0.0037 | 0.0133/0.0180 |
| J | 240/240 | 0.0124/0.0131 | 0.0091/0.0105 | 0.0057/0.0564 | 0.0477/0.1421 |
| P | 240/240 | 0.0016/0.0017 | 0.0016/0.0017 | 0.0015/0.0046 | 0.0005/0.0007 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 7.80–12.00 | 85 | 4908.8 |
| NEW | A-B | 7.80–12.00 | 85 | 4221.9 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S15/dense_platoon

[Trajectory overlay](trajectories/S15_dense_platoon.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'C': False, 'D': False, 'A': True, 'B': True, 'E': False, 'F': False, 'G': False, 'H': False, 'I': False, 'J': False} | {'C': False, 'D': False, 'A': True, 'B': True, 'E': False, 'F': False, 'G': False, 'H': False, 'I': False, 'J': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 2400 | 2400 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| B | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| C | 240/240 | 0.0000/0.0001 | 0.0000/0.0001 | 0.0000/0.0000 | 0.0001/0.0001 |
| D | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| E | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| F | 240/240 | 0.0009/0.0009 | 0.0009/0.0009 | 0.0013/0.0037 | 0.0020/0.0093 |
| G | 240/240 | 0.0139/0.0139 | 0.0023/0.0024 | 0.0025/0.0032 | 0.0061/0.0097 |
| H | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| I | 240/240 | 0.0032/0.0043 | 0.0032/0.0043 | 0.0039/0.0327 | 0.0198/0.0804 |
| J | 240/240 | 0.0027/0.0031 | 0.0027/0.0031 | 0.0022/0.0174 | 0.0135/0.0434 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 7.50–7.50 | 1 | 69673.7 |
| NEW | A-B | 7.50–7.50 | 1 | 69673.7 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S16/overtaking

[Trajectory overlay](trajectories/S16_overtaking.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'C': False, 'D': False, 'E': False, 'A': True, 'F': False, 'G': False, 'B': True, 'H': False, 'I': False} | {'C': False, 'D': False, 'E': False, 'A': True, 'F': False, 'G': False, 'B': True, 'H': False, 'I': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 2160 | 2160 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0020/0.0020 | 0.0020/0.0020 | 0.0005/0.0149 | 0.0058/0.0059 |
| B | 240/240 | 0.0019/0.0019 | 0.0019/0.0019 | 0.0011/0.0037 | 0.0027/0.0029 |
| C | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| D | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| E | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| F | 240/240 | 0.0001/0.0001 | 0.0001/0.0001 | 0.0000/0.0000 | 0.0001/0.0001 |
| G | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| H | 240/240 | 0.0003/0.0003 | 0.0003/0.0003 | 0.0001/0.0005 | 0.0002/0.0003 |
| I | 240/240 | 0.0088/0.0095 | 0.0072/0.0078 | 0.0097/0.0774 | 0.0381/0.1250 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 6.80–8.80 | 40 | 1672.4 |
| NEW | A-B | 6.80–8.75 | 39 | 1669.0 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S17/occlusion_reappearance

[Trajectory overlay](trajectories/S17_occlusion_reappearance.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'V': False, 'C': False, 'D': False, 'E': False} | {'A': True, 'B': True, 'V': False, 'C': False, 'D': False, 'E': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 1440 | 1440 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0002/0.0002 | 0.0002/0.0002 | 0.0004/0.0028 | 0.0071/0.0072 |
| B | 240/240 | 0.0002/0.0002 | 0.0002/0.0002 | 0.0002/0.0019 | 0.0004/0.0017 |
| C | 240/240 | 0.0008/0.0011 | 0.0008/0.0011 | 0.0008/0.0057 | 0.0030/0.0157 |
| D | 240/240 | 0.0018/0.0028 | 0.0018/0.0028 | 0.0046/0.0169 | 0.0235/0.0461 |
| E | 240/240 | 0.0089/0.0097 | 0.0098/0.0100 | 0.0206/0.0300 | 0.0325/0.0534 |
| V | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0001 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 7.35–8.25 | 19 | 3129.4 |
| NEW | A-B | 7.35–8.25 | 19 | 3125.7 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S18/collision_ambiguity

[Trajectory overlay](trajectories/S18_collision_ambiguity.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town05 | Town05 | same |
| Participants | {'A': True, 'B': True, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False, 'H': False} | {'A': True, 'B': True, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False, 'H': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 1920 | 1920 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| B | 240/240 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 | 0.0000/0.0000 |
| C | 240/240 | 0.0004/0.0006 | 0.0004/0.0006 | 0.0010/0.0020 | 0.0001/0.0003 |
| D | 240/240 | 0.0005/0.0008 | 0.0005/0.0008 | 0.0017/0.0021 | 0.0002/0.0010 |
| E | 240/240 | 0.0021/0.0022 | 0.0028/0.0029 | 0.0020/0.0024 | 0.0010/0.0027 |
| F | 240/240 | 0.0093/0.0096 | 0.0014/0.0017 | 0.0037/0.0051 | 0.0020/0.0031 |
| G | 240/240 | 0.0017/0.0018 | 0.0017/0.0018 | 0.0019/0.0025 | 0.0004/0.0021 |
| H | 240/240 | 0.0021/0.0024 | 0.0021/0.0024 | 0.0044/0.0062 | 0.0014/0.0040 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 7.70–7.95 | 6 | 3011.5 |
| NEW | A-B | 7.70–7.95 | 6 | 3011.5 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.

## S19/highway_curve

[Trajectory overlay](trajectories/S19_highway_curve.png)

| Configuration / coverage | OLD | NEW | Comparison |
|---|---|---|---|
| Map | Town04 | Town04 | same |
| Participants | {'A': True, 'B': True, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False} | {'A': True, 'B': True, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False} | same |
| Recorders | A, B | A, B | same |
| Vehicle metadata | see config CSV | see config CSV | same |
| Duration [s] | 12.000 | 12.000 | delta +0.000s |
| Ground-truth state rows | 1680 | 1680 | same |
| Physical behavior gate | PASS | PASS | same |
| Required incomplete radar/RGB | none | none | same |
| Advisory incomplete depth | A/depth/front_depth, B/depth/front_depth | A/depth/front_depth, B/depth/front_depth | reported; not blocking |

### Trajectory error over relative time

| Participant | OLD/NEW samples | World position error p95/max [m] | From-start motion error p95/max [m] | Velocity 2D p95/max [m/s] | Heading p95/max [deg] |
|---|---|---|---|---|---|
| A | 240/240 | 0.0353/0.0537 | 0.0652/0.0783 | 0.0334/0.0917 | 0.1322/0.5026 |
| B | 240/240 | 0.0363/0.0399 | 0.0410/0.0465 | 0.0295/0.0836 | 0.0992/0.1871 |
| C | 240/240 | 0.0409/0.0414 | 0.0417/0.0429 | 0.0280/0.0365 | 0.1059/0.1204 |
| D | 240/240 | 0.0041/0.0043 | 0.0041/0.0043 | 0.0091/0.0256 | 0.0408/0.0714 |
| E | 240/240 | 0.0042/0.0068 | 0.0100/0.0107 | 0.0114/0.0439 | 0.0446/0.1301 |
| F | 240/240 | 0.0372/0.0373 | 0.0402/0.0409 | 0.0231/0.0410 | 0.0972/0.1290 |
| G | 240/240 | 0.0102/0.0168 | 0.0216/0.0235 | 0.0143/0.0210 | 0.0441/0.0674 |

### Collision episodes and triggers

| Dataset | Pair | Start–end [s] | Contact ticks | Impulse sum [N·s] |
|---|---|---|---|---|
| OLD | A-B | 7.55–7.55 | 1 | 14898.4 |
| NEW | A-B | 7.55–7.55 | 1 | 14958.7 |

Trigger signatures: same; trigger timing: same within 0.10 s.

| Dataset | Participant | Action | t relative [s] |
|---|---|---|---|
| OLD/NEW | — | none | — |

### Sensor channels

| Sensor | Channels | OLD complete | NEW complete | NEW tick [s] |
|---|---|---|---|---|
| radar | 6 | 6/6 | 6/6 | 0.05 |
| rgb | 2 | 2/2 | 2/2 | 0.1 |
| depth | 2 | 0/2 | 0/2 | 0.05 |

Row-level sensor frame counts, measured rates, missing frames, queue drops, duplicate callbacks and static configuration are in `sensor_comparison.csv`.

### Maneuvers and minimum distances

OLD/NEW brake, throttle, steer and acceleration summaries are in `maneuver_comparison.csv`; minimum oriented box gaps and relative times are in `minimum_gap_comparison.csv`.
