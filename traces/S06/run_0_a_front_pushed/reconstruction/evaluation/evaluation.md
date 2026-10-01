# Privileged evaluation - S06/run_0_a_front_pushed

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: NO; associations correct: 1/1; anonymous: 2; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 141.662 | 11621.7 | g32 | yes | 0.0 s |
| B + C | 141.912 | 9832.4 | - | NO | - s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 5.9 | 5.9 | 0.0 s |
| B | ALIGNED | 5.9 | 5.9 | 0.0 s |
| C | UNALIGNED | - | 5.9 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

44 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 907/907 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 297 | 0.592 / 0.599 m | 1.514 m | 1.159 / 0.093 m/s |
| A:track_002 | A:track_002 | C | left anonymous (true identity C) | 2 | 0.533 / 0.864 m | 1.439 m | - / 0.089 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 62 | 0.248 / 0.23 m | 2.104 m | 1.448 / 0.26 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 6.88 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
