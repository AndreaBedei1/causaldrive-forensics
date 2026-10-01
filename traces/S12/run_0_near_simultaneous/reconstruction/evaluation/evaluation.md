# Privileged evaluation - S12/run_0_near_simultaneous

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 18; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 66.564 | 4032.5 | g61 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 9.5 | 9.5 | 0.0 s |
| B | ALIGNED | collision_001 | 9.5 | 9.5 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

103 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 5008/5008 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 66 | 0.505 / 0.524 m | 1.029 m | 5.049 / 0.401 m/s |
| A:track_002 | A:track_002 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_003 | A:track_003 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_004 | A:track_004 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_005 | A:track_005 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_006 | A:track_006 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_007 | A:track_007 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_008 | A:track_008 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_009 | A:track_009 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_010 | A:track_010 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_011 | A:track_011 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_012 | A:track_012 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_013 | A:track_013 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_014 | A:track_014 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_015 | A:track_015 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_016 | A:track_016 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_017 | A:track_017 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_018 | A:track_018 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_019 | A:track_019 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_001 | A | A | correct | 72 | 0.246 / 0.322 m | 0.911 m | 7.424 / 1.186 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 10.23 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
