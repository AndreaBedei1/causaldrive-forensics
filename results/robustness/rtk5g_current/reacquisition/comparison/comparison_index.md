# OLD vs NEW CARLA reacquisition comparison

Trajectory overlays: OLD dashed, NEW solid. Physical contacts are listed separately in `collision_events.csv`; actor IDs, absolute frame numbers and absolute timestamp origins are run-local and are not treated as behavior changes.

| Run | Map | Participants / recorders | Duration delta [s] | Physical gate | OLD/NEW contact episodes | Trigger signature/time | Max path error [m] | Sensor gate | Plot |
|---|---|---|---:|---|---|---|---:|---|---|
| S01/crash | Town05 | A,B / A,B | +0.000 | PASS | 1/1 | same/same | 0.004 | PASS | [overlay](trajectories/S01_crash.png) |
| S02/crash | Town05 | A,B / A,B | +0.000 | PASS | 1/1 | same/same | 0.282 | PASS | [overlay](trajectories/S02_crash.png) |
| S03/crash | Town05 | A,B / A,B | +0.000 | PASS | 2/2 | same/same | 0.090 | PASS | [overlay](trajectories/S03_crash.png) |
| S04/a_front_pushed | Town05 | A,B,C / A,B,C | +0.000 | PASS | 3/3 | same/same | 0.003 | PASS | [overlay](trajectories/S04_a_front_pushed.png) |
| S04/b_rear_first | Town05 | A,B,C / A,B,C | +0.000 | PASS | 2/2 | same/same | 0.004 | PASS | [overlay](trajectories/S04_b_rear_first.png) |
| S05/crash | Town05 | A,B,C / A,B,C | +0.000 | PASS | 1/1 | same/same | 0.004 | PASS | [overlay](trajectories/S05_crash.png) |
| S06/crash | Town05 | A,B,C / A,B,C | +0.000 | PASS | 2/2 | same/same | 0.033 | PASS | [overlay](trajectories/S06_crash.png) |
| S07/merge_conflict | Town03_Opt | A,B / A,B | +0.000 | PASS | 1/1 | same/same | 0.008 | PASS | [overlay](trajectories/S07_merge_conflict.png) |
| S08/rolls_through | Town05 | A,B / A,B | +0.000 | PASS | 1/1 | same/same | 0.006 | PASS | [overlay](trajectories/S08_rolls_through.png) |
| S09/near_simultaneous | Town05 | A,B / A,B | +0.000 | PASS | 1/1 | same/same | 0.029 | PASS | [overlay](trajectories/S09_near_simultaneous.png) |
| S10/deflected_into_c | Town05 | A,B,C / A,B,C | +0.000 | FAIL | 2/5 | same/same | 0.301 | PASS | [overlay](trajectories/S10_deflected_into_c.png) |
| S11/consequential | Town05 | A,B,C / A,B,C | +0.000 | PASS | 4/4 | same/same | 0.004 | PASS | [overlay](trajectories/S11_consequential.png) |
| S12/crash | Town05 | A,B,C / A,B | +0.000 | PASS | 1/1 | same/same | 0.021 | PASS | [overlay](trajectories/S12_crash.png) |
| S13/abreast | Town05 | A,B,C,D / A,B | +0.000 | PASS | 1/1 | same/same | 0.020 | PASS | [overlay](trajectories/S13_abreast.png) |
| S13/platoon | Town05 | A,B,C,D / A,B | +0.000 | PASS | 1/1 | same/same | 0.114 | PASS | [overlay](trajectories/S13_platoon.png) |
| S13/passing | Town05 | A,B,C,D / A,B | +0.000 | PASS | 1/1 | same/same | 0.012 | PASS | [overlay](trajectories/S13_passing.png) |
| S14/surrounded | Town05 | A,B,C,D,E,F,G,H,J,P / A,B | +0.000 | PASS | 1/1 | same/same | 0.043 | PASS | [overlay](trajectories/S14_surrounded.png) |
| S15/dense_platoon | Town05 | C,D,A,B,E,F,G,H,I,J / A,B | +0.000 | PASS | 1/1 | same/same | 0.004 | PASS | [overlay](trajectories/S15_dense_platoon.png) |
| S16/overtaking | Town05 | C,D,E,A,F,G,B,H,I / A,B | +0.000 | PASS | 1/1 | same/same | 0.008 | PASS | [overlay](trajectories/S16_overtaking.png) |
| S17/occlusion_reappearance | Town05 | A,B,V,C,D,E / A,B | +0.000 | PASS | 1/1 | same/same | 0.010 | PASS | [overlay](trajectories/S17_occlusion_reappearance.png) |
| S18/collision_ambiguity | Town05 | A,B,C,D,E,F,G,H / A,B | +0.000 | PASS | 1/1 | same/same | 0.003 | PASS | [overlay](trajectories/S18_collision_ambiguity.png) |
| S19/highway_curve | Town04 | A,B,C,D,E,F,G / A,B | +0.000 | PASS | 1/1 | same/same | 0.078 | PASS | [overlay](trajectories/S19_highway_curve.png) |
