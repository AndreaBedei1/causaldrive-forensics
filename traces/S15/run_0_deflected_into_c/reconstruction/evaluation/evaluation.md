# Privileged evaluation - S15/run_0_deflected_into_c

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 4/4; anonymous: 8; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 146.100 | 9797.5 | g43 | yes | 0.0 s |
| A + C | 147.050 | 1637.6 | g59 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| B | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| C | ALIGNED | collision_001 -> collision_002 | 3.8 | 3.8 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - B: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

78 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 2909/2909 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | C | C | correct | 135 | 0.41 / 0.548 m | 0.904 m | 2.799 / 0.356 m/s |
| A:track_002 | B | B | correct | 18 | 0.563 / 0.542 m | 0.923 m | 3.759 / 0.845 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 16 | 0.346 / 0.407 m | 0.925 m | 8.615 / 0.642 m/s |
| B:track_002 | A | A | correct | 120 | 0.254 / 0.334 m | 2.006 m | 2.035 / 0.716 m/s |
| B:track_003 | B:track_003 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_004 | B:track_004 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_005 | B:track_005 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_006 | B:track_006 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_007 | B:track_007 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_008 | B:track_008 | C | left anonymous (true identity C) | 3 | 0.371 / 0.492 m | 1.175 m | 1.835 / 3.375 m/s |
| C:track_001 | C:track_001 | B | left anonymous (true identity B) | 43 | 0.365 / 0.359 m | 0.831 m | 7.472 / 0.691 m/s |
| C:track_002 | A | A | correct | 136 | 0.448 / 0.578 m | 1.111 m | 2.63 / 0.344 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
