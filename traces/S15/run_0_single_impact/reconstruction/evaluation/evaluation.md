# Privileged evaluation - S15/run_0_single_impact

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes; associations correct: 2/2; anonymous: 3; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 517.141 | 9797.5 | g19 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 3.8 | 3.8 | 0.0 s |
| B | ALIGNED | 3.8 | 3.8 | 0.0 s |
| C | UNALIGNED | - | 3.8 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

40 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 750/750 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 125 | 0.529 / 0.686 m | 1.411 m | 7.59 / 0.058 m/s |
| A:track_002 | B | B | correct | 18 | 0.567 / 0.518 m | 0.944 m | 5.467 / 0.353 m/s |
| B:track_001 | A | A | correct | 36 | 0.467 / 0.588 m | 1.662 m | 4.177 / 1.753 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 129 | 0.679 / 0.777 m | 1.309 m | 4.548 / 0.102 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 117 | 0.218 / 0.207 m | 0.843 m | 9.926 / 0.489 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
