# Privileged evaluation - S16/run_0_independent

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: NO; associations correct: 1/1; anonymous: 4; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 18.330 | 6073.8 | - | NO | - s |
| A + C | 27.280 | 9095.5 | g25 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 14.1 | 14.1 | 0.0 s |
| B | UNALIGNED | - | 14.1 | - s |
| C | ALIGNED | 14.1 | 14.1 | 0.0 s |

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

32 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 482/482 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 8 | 0.237 / 0.243 m | 2.728 m | 4.224 / 0.263 m/s |
| A:track_002 | C | C | correct | 28 | 0.18 / 0.444 m | 2.453 m | 4.683 / 0.373 m/s |
| B:track_001 | B:track_001 | A | left anonymous (true identity A) | 141 | 0.558 / 0.561 m | 1.543 m | 1.371 / 0.231 m/s |
| B:track_002 | B:track_002 | C | left anonymous (true identity C) | 39 | 0.339 / 0.645 m | 2.166 m | 8.315 / 0.377 m/s |
| B:track_003 | B:track_003 | C | left anonymous (true identity C) | 6 | 0.375 / 0.385 m | 2.574 m | 4.724 / 0.454 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 14.83 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
