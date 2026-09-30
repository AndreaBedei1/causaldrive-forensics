# Privileged evaluation - S04/run_0_yield

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: no vehicle-vehicle collision in ground truth; associations correct: 0/0; anonymous: 4; max |t_global error| None s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | UNALIGNED | - | - | - s |
| B | UNALIGNED | - | - | - s |

## Global event times

0 timed global nodes; max |t_global - true global time| = - s; event order agrees with the truth for 0/0 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | B | left anonymous (true identity B) | 29 | 0.278 / 0.357 m | 0.994 m | 6.113 / 1.15 m/s |
| A:track_002 | A:track_002 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_001 | B:track_001 | A | left anonymous (true identity A) | 4 | 0.293 / 0.272 m | 2.135 m | 2.906 / 0.059 m/s |
| B:track_002 | B:track_002 | A | left anonymous (true identity A) | 25 | 0.387 / 0.461 m | 1.495 m | 2.992 / 1.504 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).
