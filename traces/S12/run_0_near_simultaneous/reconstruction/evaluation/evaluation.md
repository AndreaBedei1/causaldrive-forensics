# Privileged evaluation - S12/run_0_near_simultaneous

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes; associations correct: 1/1; anonymous: 8; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 421.378 | 4032.5 | g45 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 9.5 | 9.5 | 0.0 s |
| B | ALIGNED | 9.5 | 9.5 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

80 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 3007/3007 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | B | left anonymous (true identity B) | 3 | 0.427 / 0.426 m | 1.68 m | 5.148 / 0.174 m/s |
| A:track_002 | A:track_002 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_003 | A:track_003 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_004 | A:track_004 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_005 | A:track_005 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_006 | A:track_006 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_007 | A:track_007 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_008 | A:track_008 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_001 | A | A | correct | 71 | 0.258 / 0.327 m | 0.963 m | 6.168 / 1.022 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 10.23 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
