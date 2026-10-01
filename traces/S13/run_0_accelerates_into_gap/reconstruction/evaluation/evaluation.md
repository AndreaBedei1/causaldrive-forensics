# Privileged evaluation - S13/run_0_accelerates_into_gap

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes; associations correct: 1/1; anonymous: 43; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 83.299 | 5215.8 | g13 | yes | 0.0 s |

## Graph alignment accuracy

| Graph | Status | Estimated anchor (local) | True contact (local) | Error |
|-------|--------|-------------------------:|---------------------:|------:|
| A | ALIGNED | 5.65 | 5.65 | 0.0 s |
| B | ALIGNED | 5.65 | 5.65 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

172 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 14060/14060 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | B | left anonymous (true identity B) | 3 | 0.718 / 0.917 m | 1.066 m | - / 0.118 m/s |
| A:track_002 | B | B | correct | 62 | 0.357 / 0.426 m | 1.18 m | 1.55 / 0.539 m/s |
| B:track_001 | B:track_001 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
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
| B:track_017 | B:track_017 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_018 | B:track_018 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_019 | B:track_019 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_020 | B:track_020 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_021 | B:track_021 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_022 | B:track_022 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_023 | B:track_023 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_024 | B:track_024 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_025 | B:track_025 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_026 | B:track_026 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_027 | B:track_027 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_028 | B:track_028 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_029 | B:track_029 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_030 | B:track_030 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_031 | B:track_031 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_032 | B:track_032 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_033 | B:track_033 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_034 | B:track_034 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_035 | B:track_035 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_036 | B:track_036 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_037 | B:track_037 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_038 | B:track_038 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_039 | B:track_039 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_040 | B:track_040 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_041 | B:track_041 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_042 | B:track_042 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 6.38 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
