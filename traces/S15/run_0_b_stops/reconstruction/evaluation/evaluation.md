# Privileged evaluation - S15/run_0_b_stops

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: no vehicle-vehicle collision in ground truth; associations correct: 0/0; anonymous: 6; max |t_global error| None s**

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
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 41 | 0.605 / 0.843 m | 1.147 m | 5.103 / 0.579 m/s |
| A:track_002 | A:track_002 | B | left anonymous (true identity B) | 21 | 0.541 / 0.539 m | 0.912 m | 4.377 / 1.286 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 87 | 0.349 / 0.402 m | 1.153 m | 5.071 / 0.426 m/s |
| B:track_002 | B:track_002 | A | left anonymous (true identity A) | 33 | 0.327 / 0.427 m | 1.255 m | 4.579 / 1.299 m/s |
| C:track_001 | C:track_001 | B | left anonymous (true identity B) | 44 | 0.392 / 0.417 m | 0.833 m | 7.199 / 0.817 m/s |
| C:track_002 | C:track_002 | A | left anonymous (true identity A) | 42 | 0.684 / 0.896 m | 1.378 m | 4.944 / 0.675 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).
