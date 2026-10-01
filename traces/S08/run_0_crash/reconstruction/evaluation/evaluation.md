# Privileged evaluation - S08/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes; associations correct: 1/1; anonymous: 5; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 230.154 | 12077.2 | g23 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 4.25 | 4.25 | 0.0 s |
| B | ALIGNED | 4.25 | 4.25 | 0.0 s |
| C | UNALIGNED | - | 4.25 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

39 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 702/702 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 151 | 0.268 / 0.314 m | 2.036 m | 3.961 / 0.114 m/s |
| A:track_002 | A:track_002 | B | left anonymous (true identity B) | 12 | 0.448 / 0.613 m | 1.51 m | 5.321 / 0.405 m/s |
| B:track_001 | A | A | correct | 129 | 0.188 / 0.355 m | 1.077 m | 3.011 / 0.449 m/s |
| B:track_002 | B:track_002 | C | left anonymous (true identity C) | 19 | 0.398 / 0.427 m | 1.3 m | 7.111 / 2.125 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 149 | 0.653 / 0.715 m | 1.3 m | 4.414 / 0.157 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 122 | 0.244 / 0.281 m | 0.855 m | 4.186 / 0.631 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
