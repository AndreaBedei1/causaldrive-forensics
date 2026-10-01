# Privileged evaluation - S15/run_0_deflected_into_c

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: NO; associations correct: 2/2; anonymous: 4; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 497.340 | 9797.5 | g25 | yes | 0.0 s |
| A + C | 498.290 | 1637.6 | - | NO | - s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 3.8 | 3.8 | 0.0 s |
| B | ALIGNED | 3.8 | 3.8 | 0.0 s |
| C | UNALIGNED | - | 3.8 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

50 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1195/1195 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 138 | 0.386 / 0.519 m | 1.079 m | 2.572 / 0.379 m/s |
| A:track_002 | B | B | correct | 18 | 0.567 / 0.518 m | 0.944 m | 5.467 / 0.353 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 13 | 0.321 / 0.403 m | 1.217 m | 6.171 / 0.622 m/s |
| B:track_002 | A | A | correct | 120 | 0.274 / 0.333 m | 2.119 m | 2.45 / 0.986 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 139 | 0.418 / 0.554 m | 1.371 m | 3.158 / 0.378 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 43 | 0.311 / 0.358 m | 0.868 m | 6.251 / 0.733 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
