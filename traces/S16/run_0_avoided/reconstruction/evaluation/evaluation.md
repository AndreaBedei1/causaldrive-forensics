# Privileged evaluation - S16/run_0_avoided

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes; associations correct: 1/1; anonymous: 0; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 536.422 | 6073.8 | g16 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 5.15 | 5.15 | 0.0 s |
| B | ALIGNED | 5.15 | 5.15 | 0.0 s |
| C | UNALIGNED | - | 5.15 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

24 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 263/263 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| B:track_001 | A | A | correct | 100 | 0.532 / 0.51 m | 1.59 m | 0.77 / 0.241 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
