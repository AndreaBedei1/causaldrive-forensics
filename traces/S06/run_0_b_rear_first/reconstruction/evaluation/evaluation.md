# Privileged evaluation - S06/run_0_b_rear_first

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: NO; associations correct: 0/0; anonymous: 3; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| B + C | 175.058 | 21812.2 | - | NO | - s |
| A + B | 176.458 | 31488.3 | g27 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 6.0 | 6.0 | 0.0 s |
| B | ALIGNED | 6.0 | 6.0 | 0.0 s |
| C | UNALIGNED | - | 6.0 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

33 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 505/505 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | B | left anonymous (true identity B) | 46 | 0.543 / 0.528 m | 1.583 m | 2.747 / 0.1 m/s |
| A:track_002 | A:track_002 | C | left anonymous (true identity C) | 2 | 0.533 / 0.864 m | 1.439 m | - / 0.089 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 141 | 0.27 / 0.256 m | 2.048 m | 1.0 / 0.094 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.33 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
