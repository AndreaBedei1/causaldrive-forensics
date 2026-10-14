# Privileged evaluation - S18/run_0_far_to_near

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 22; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 543.381 | 745.3 | g76 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 8.5 | 8.5 | 0.0 s |
| B | ALIGNED | collision_001 | 8.5 | 8.5 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

103 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 5148/5148 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | F | correctly left anonymous | 43 | 0.224 / 0.361 m | 1.641 m | 2.556 / 1.408 m/s |
| A:track_002 | B | B | correct | 120 | 0.108 / 0.119 m | 0.942 m | 4.528 / 0.171 m/s |
| A:track_003 | U2 | G | correctly left anonymous | 13 | 0.131 / 0.206 m | 2.074 m | 2.291 / 1.02 m/s |
| A:track_004 | U3 | E | correctly left anonymous | 67 | 0.28 / 0.408 m | 1.811 m | 2.681 / 1.343 m/s |
| A:track_005#segment_1 | U4 | C | correctly left anonymous | 14 | 1.098 / 0.672 m | 1.732 m | 18.105 / 0.197 m/s |
| A:track_005#segment_2 | U5 | C | correctly left anonymous | 15 | 0.722 / 0.921 m | 1.477 m | 3.004 / 0.061 m/s |
| A:track_006 | U6 | D | correctly left anonymous | 18 | 0.693 / 0.859 m | 1.54 m | 3.973 / 0.047 m/s |
| A:track_007#segment_1 | U8 | C | correctly left anonymous | 10 | 0.812 / 0.539 m | 1.853 m | 11.262 / 0.218 m/s |
| A:track_007#segment_2 | U9 | C | correctly left anonymous | 44 | 0.187 / 0.18 m | 2.256 m | 1.01 / 0.052 m/s |
| A:track_008 | U10 | D | correctly left anonymous | 51 | 0.259 / 0.329 m | 2.109 m | 2.602 / 0.152 m/s |
| A:track_009 | U3 | E | correctly left anonymous | 14 | 0.145 / 0.253 m | 1.976 m | 1.52 / 0.539 m/s |
| B:track_001 | U1 | F | correctly left anonymous | 24 | 0.202 / 0.467 m | 1.357 m | 3.208 / 0.741 m/s |
| B:track_002 | A | A | correct | 120 | 1.552 / 1.024 m | 1.778 m | 5.504 / 0.486 m/s |
| B:track_003 | U2 | G | correctly left anonymous | 22 | 0.192 / 0.61 m | 1.504 m | 4.639 / 1.043 m/s |
| B:track_004 | U3 | E | correctly left anonymous | 3 | 0.452 / 0.637 m | 1.625 m | 12.299 / 0.061 m/s |
| B:track_005 | U3 | E | correctly left anonymous | 50 | 0.29 / 0.57 m | 1.51 m | 6.625 / 0.656 m/s |
| B:track_006 | U5 | C | correctly left anonymous | 22 | 0.917 / 0.83 m | 1.548 m | 7.088 / 0.441 m/s |
| B:track_007 | U7 | D | correctly left anonymous | 3 | 0.811 / 0.767 m | 1.578 m | 6.766 / 0.079 m/s |
| B:track_008 | U6 | D | correctly left anonymous | 6 | 0.692 / 0.814 m | 1.219 m | 4.681 / 0.068 m/s |
| B:track_009 | U1 | F | correctly left anonymous | 20 | 0.24 / 0.572 m | 1.362 m | 3.256 / 0.912 m/s |
| B:track_010 | U9 | C | correctly left anonymous | 53 | 0.281 / 0.347 m | 2.117 m | 2.552 / 0.128 m/s |
| B:track_011 | U10 | D | correctly left anonymous | 53 | 0.337 / 0.412 m | 2.014 m | 2.706 / 0.163 m/s |
| B:track_012 | U3 | E | correctly left anonymous | 19 | 0.18 / 0.397 m | 1.314 m | 3.479 / 0.908 m/s |
| B:track_013 | U3 | E | correctly left anonymous | 21 | 0.232 / 0.432 m | 1.511 m | 1.908 / 0.443 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.094 m | 0.0 m | 0.094 m | 0.42 m |
| A + B | B | A | B:track_002 | 0.0 s | 0.026 m | 0.0 m | 0.026 m | 0.035 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 9.23 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
