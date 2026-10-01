# Privileged evaluation - S13/run_0_cut_in

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes; associations correct: 1/1; anonymous: 0; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 453.195 | 3184.4 | g10 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 5.25 | 5.25 | 0.0 s |
| B | ALIGNED | 5.25 | 5.25 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

19 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 159/159 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 96 | 0.437 / 0.515 m | 1.172 m | 2.667 / 0.317 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.98 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
