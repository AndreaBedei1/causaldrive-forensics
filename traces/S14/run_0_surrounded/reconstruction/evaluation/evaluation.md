# Privileged evaluation - S14/run_0_surrounded

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 21; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 21.750 | 497.6 | g38 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |
| B | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

61 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1748/1748 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | P | correctly left anonymous | 120 | 0.137 / 0.135 m | 2.145 m | 0.225 / 0.015 m/s |
| A:track_002 | U2 | C | correctly left anonymous | 120 | 0.322 / 0.36 m | 2.102 m | 1.888 / 0.048 m/s |
| A:track_003 | B | B | correct | 120 | 0.092 / 0.094 m | 1.183 m | 1.013 / 0.141 m/s |
| A:track_004 | U3 | D | correctly left anonymous | 119 | 0.158 / 0.16 m | 2.114 m | 0.864 / 0.06 m/s |
| A:track_005 | U9 | J | correctly left anonymous | 8 | 0.213 / 0.238 m | 1.925 m | 1.84 / 0.203 m/s |
| A:track_006 | U7 | G | correctly left anonymous | 46 | 0.21 / 0.315 m | 1.95 m | 4.941 / 0.124 m/s |
| A:track_007 | U5 | E | correctly left anonymous | 42 | 0.253 / 0.305 m | 2.173 m | 3.023 / 0.041 m/s |
| A:track_008 | U4 | F | correctly left anonymous | 33 | 0.308 / 0.367 m | 1.754 m | 3.936 / 0.043 m/s |
| A:track_009 | U11 | J | correctly left anonymous | 13 | 0.434 / 0.442 m | 1.262 m | 7.321 / 0.068 m/s |
| B:track_001 | U3 | D | correctly left anonymous | 120 | 0.175 / 0.173 m | 2.102 m | 0.501 / 0.04 m/s |
| B:track_002 | A | A | correct | 120 | 0.161 / 0.433 m | 1.184 m | 2.822 / 0.149 m/s |
| B:track_003 | U1 | P | correctly left anonymous | 120 | 0.208 / 0.272 m | 2.016 m | 1.057 / 0.038 m/s |
| B:track_004 | U4 | F | correctly left anonymous | 35 | 0.49 / 0.618 m | 1.465 m | 6.004 / 0.031 m/s |
| B:track_005 | U2 | C | correctly left anonymous | 119 | 0.314 / 0.328 m | 2.121 m | 1.709 / 0.037 m/s |
| B:track_006 | U5 | E | correctly left anonymous | 119 | 0.346 / 0.44 m | 1.979 m | 3.498 / 0.05 m/s |
| B:track_007 | U6 | H | correctly left anonymous | 21 | 0.599 / 0.725 m | 1.671 m | 3.682 / 0.05 m/s |
| B:track_008 | U7 | G | correctly left anonymous | 31 | 0.435 / 0.55 m | 1.725 m | 2.754 / 0.064 m/s |
| B:track_009 | U7 | G | correctly left anonymous | 24 | 0.195 / 0.172 m | 2.104 m | 2.214 / 0.12 m/s |
| B:track_010 | U4 | F | correctly left anonymous | 29 | 0.368 / 0.36 m | 1.758 m | 2.811 / 0.052 m/s |
| B:track_011 | U8 | H | correctly left anonymous | 5 | 0.56 / 0.698 m | 1.714 m | 4.023 / 0.053 m/s |
| B:track_012 | U10 | H | correctly left anonymous | 2 | 0.327 / 0.27 m | 2.202 m | 1.582 / 0.001 m/s |
| B:track_013 | U11 | J | correctly left anonymous | 31 | 0.309 / 0.384 m | 1.725 m | 3.491 / 0.137 m/s |
| B:track_014 | U12 | H | correctly left anonymous | 2 | 0.257 / 0.22 m | 1.078 m | 24.228 / 0.322 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_003 | -0.05 s | 0.085 m | 0.0 m | 0.085 m | 0.293 m |
| A + B | B | A | B:track_002 | -0.05 s | 0.785 m | 0.0 m | 0.785 m | 1.182 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
