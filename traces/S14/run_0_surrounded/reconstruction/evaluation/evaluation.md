# Privileged evaluation - S14/run_0_surrounded

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 21; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 21.750 | 497.6 | g35 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |
| B | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

66 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 2073/2073 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | P | correctly left anonymous | 120 | 0.138 / 0.145 m | 2.151 m | 0.223 / 0.083 m/s |
| A:track_002 | U2 | C | correctly left anonymous | 120 | 0.322 / 0.358 m | 2.104 m | 1.888 / 0.098 m/s |
| A:track_003 | B | B | correct | 120 | 0.092 / 0.12 m | 1.24 m | 1.013 / 0.198 m/s |
| A:track_004#segment_1 | U3 | D | correctly left anonymous | 67 | 0.19 / 0.191 m | 2.073 m | 0.493 / 0.063 m/s |
| A:track_004#segment_2 | U11 | D | correctly left anonymous | 18 | 0.163 / 0.169 m | 2.153 m | 2.294 / 0.05 m/s |
| A:track_004#segment_3 | U3 | D | correctly left anonymous | 33 | 0.079 / 0.085 m | 2.179 m | 0.364 / 0.024 m/s |
| A:track_005 | U12 | J | correctly left anonymous | 8 | 0.213 / 0.232 m | 1.937 m | 1.84 / 0.223 m/s |
| A:track_006 | U9 | G | correctly left anonymous | 44 | 0.213 / 0.3 m | 1.991 m | 4.884 / 0.109 m/s |
| A:track_007 | U5 | E | correctly left anonymous | 41 | 0.279 / 0.361 m | 2.114 m | 4.197 / 0.072 m/s |
| A:track_008 | U8 | F | correctly left anonymous | 33 | 0.308 / 0.368 m | 1.751 m | 3.936 / 0.038 m/s |
| A:track_009 | U13 | J | correctly left anonymous | 11 | 0.462 / 0.497 m | 1.371 m | 7.666 / 0.096 m/s |
| B:track_001 | U3 | D | correctly left anonymous | 120 | 0.172 / 0.171 m | 2.106 m | 0.372 / 0.045 m/s |
| B:track_002 | A | A | correct | 120 | 0.163 / 0.409 m | 1.249 m | 1.689 / 0.676 m/s |
| B:track_003 | U1 | P | correctly left anonymous | 120 | 0.211 / 0.243 m | 2.021 m | 1.064 / 0.16 m/s |
| B:track_004 | U4 | F | correctly left anonymous | 35 | 0.49 / 0.618 m | 1.465 m | 6.004 / 0.034 m/s |
| B:track_005 | U2 | C | correctly left anonymous | 119 | 0.315 / 0.323 m | 2.124 m | 1.598 / 0.046 m/s |
| B:track_006 | U5 | E | correctly left anonymous | 119 | 0.346 / 0.445 m | 1.96 m | 3.718 / 0.081 m/s |
| B:track_007 | U6 | G | correctly left anonymous | 37 | 0.431 / 0.552 m | 1.722 m | 2.796 / 0.058 m/s |
| B:track_008 | U7 | H | correctly left anonymous | 20 | 0.606 / 0.732 m | 1.655 m | 3.78 / 0.054 m/s |
| B:track_009 | U8 | F | correctly left anonymous | 29 | 0.368 / 0.36 m | 1.758 m | 2.811 / 0.054 m/s |
| B:track_010 | U9 | G | correctly left anonymous | 23 | 0.193 / 0.17 m | 2.108 m | 2.264 / 0.12 m/s |
| B:track_011 | U10 | H | correctly left anonymous | 5 | 0.56 / 0.698 m | 1.714 m | 4.023 / 0.05 m/s |
| B:track_012 | U13 | J | correctly left anonymous | 31 | 0.309 / 0.358 m | 1.756 m | 3.491 / 0.127 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_003 | -0.05 s | 0.07 m | 0.0 m | 0.07 m | 0.035 m |
| A + B | B | A | B:track_002 | -0.05 s | 0.758 m | 0.0 m | 0.758 m | 1.414 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
