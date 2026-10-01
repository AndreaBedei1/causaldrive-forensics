# Privileged evaluation - S15/run_0_single_impact

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 8; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 166.000 | 9797.5 | g33 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| B | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| C | UNALIGNED | - | - | 3.8 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

52 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1265/1265 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 112 | 0.566 / 0.796 m | 1.294 m | 7.15 / 0.061 m/s |
| A:track_002 | B | B | correct | 18 | 0.563 / 0.542 m | 0.923 m | 3.759 / 0.845 m/s |
| B:track_001 | A | A | correct | 120 | 0.267 / 0.341 m | 1.974 m | 2.351 / 0.708 m/s |
| B:track_002 | B:track_002 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_003 | B:track_003 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_004 | B:track_004 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_005 | B:track_005 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_006 | B:track_006 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 121 | 0.678 / 0.778 m | 1.238 m | 5.487 / 0.103 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 110 | 0.273 / 0.245 m | 0.84 m | 10.476 / 0.554 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
