# Privileged evaluation - S05/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes; associations correct: 1/1; anonymous: 17; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 120.679 | 6116.3 | g15 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 3.7 | 3.7 | 0.0 s |
| B | ALIGNED | 3.7 | 3.7 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

81 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 2996/2996 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 27 | 0.234 / 0.403 m | 0.688 m | 6.122 / 0.741 m/s |
| B:track_001 | B:track_001 | A | left anonymous (true identity A) | 17 | 0.441 / 0.631 m | 1.308 m | 8.089 / 1.0 m/s |
| B:track_002 | B:track_002 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_003 | B:track_003 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_004 | B:track_004 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_005 | B:track_005 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_006 | B:track_006 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_007 | B:track_007 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_008 | B:track_008 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_009 | B:track_009 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_010 | B:track_010 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_011 | B:track_011 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_012 | B:track_012 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_013 | B:track_013 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_014 | B:track_014 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_015 | B:track_015 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_016 | B:track_016 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_017 | B:track_017 | A | left anonymous (true identity A) | 4 | 0.283 / 0.318 m | 2.214 m | 0.777 / 6.325 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 4.43 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
