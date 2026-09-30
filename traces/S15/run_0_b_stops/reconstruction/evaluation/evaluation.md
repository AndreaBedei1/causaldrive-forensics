# Privileged evaluation - S15/run_0_b_stops

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: no vehicle-vehicle collision in ground truth; associations correct: 0/0; anonymous: 7; max |t_global error| None s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | UNALIGNED | - | - | - s |
| B | UNALIGNED | - | - | - s |
| C | UNALIGNED | - | - | - s |

## Global event times

0 timed global nodes; max |t_global - true global time| = - s; event order agrees with the truth for 0/0 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 43 | 0.562 / 0.755 m | 1.205 m | 4.382 / 0.387 m/s |
| A:track_002 | A:track_002 | B | left anonymous (true identity B) | 19 | 0.532 / 0.51 m | 0.959 m | 6.019 / 1.156 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 13 | 0.324 / 0.403 m | 1.231 m | 5.978 / 0.68 m/s |
| B:track_002 | B:track_002 | A | left anonymous (true identity A) | 29 | 0.42 / 0.61 m | 1.434 m | 4.707 / 1.953 m/s |
| B:track_003 | B:track_003 | C | left anonymous (true identity C) | 65 | 0.318 / 0.416 m | 1.302 m | 4.019 / 0.672 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 45 | 0.628 / 0.824 m | 1.374 m | 5.751 / 0.624 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 39 | 0.367 / 0.402 m | 0.969 m | 6.69 / 1.314 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).
