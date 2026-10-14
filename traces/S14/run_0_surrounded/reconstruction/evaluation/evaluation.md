# Privileged evaluation - S14/run_0_surrounded

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 25; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 71.377 | 254.4 | g44 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |
| B | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

84 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 3389/3389 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | P | correctly left anonymous | 120 | 0.137 / 0.144 m | 2.151 m | 0.218 / 0.08 m/s |
| A:track_002 | U2 | C | correctly left anonymous | 120 | 0.32 / 0.357 m | 2.103 m | 1.882 / 0.093 m/s |
| A:track_003 | B | B | correct | 120 | 0.092 / 0.12 m | 1.241 m | 1.025 / 0.198 m/s |
| A:track_004#segment_1 | U3 | D | correctly left anonymous | 68 | 0.192 / 0.193 m | 2.072 m | 0.48 / 0.065 m/s |
| A:track_004#segment_2 | U13 | D | correctly left anonymous | 16 | 0.162 / 0.16 m | 2.16 m | 2.271 / 0.049 m/s |
| A:track_004#segment_3 | U3 | D | correctly left anonymous | 35 | 0.081 / 0.084 m | 2.181 m | 0.367 / 0.027 m/s |
| A:track_005 | U9 | K | correctly left anonymous | 25 | 0.123 / 0.194 m | 1.008 m | 4.222 / 0.204 m/s |
| A:track_006 | U14 | J | correctly left anonymous | 7 | 0.175 / 0.233 m | 1.937 m | 0.807 / 0.29 m/s |
| A:track_007 | U15 | L | correctly left anonymous | 4 | 0.973 / 1.016 m | 0.846 m | 3.841 / 0.095 m/s |
| A:track_008 | U11 | G | correctly left anonymous | 44 | 0.218 / 0.29 m | 2.011 m | 4.001 / 0.104 m/s |
| A:track_009 | U6 | E | correctly left anonymous | 42 | 0.254 / 0.356 m | 2.121 m | 3.438 / 0.067 m/s |
| A:track_010 | U10 | F | correctly left anonymous | 33 | 0.315 / 0.34 m | 1.778 m | 3.029 / 0.04 m/s |
| A:track_011 | U17 | J | correctly left anonymous | 10 | 0.43 / 0.461 m | 1.579 m | 5.933 / 0.08 m/s |
| B:track_001 | U3 | D | correctly left anonymous | 120 | 0.173 / 0.171 m | 2.105 m | 0.368 / 0.044 m/s |
| B:track_002 | A | A | correct | 120 | 0.164 / 0.411 m | 1.247 m | 2.168 / 0.638 m/s |
| B:track_003 | U1 | P | correctly left anonymous | 120 | 0.211 / 0.243 m | 2.018 m | 1.071 / 0.138 m/s |
| B:track_004 | U4 | F | correctly left anonymous | 35 | 0.49 / 0.618 m | 1.465 m | 6.002 / 0.034 m/s |
| B:track_005 | U5 | K | correctly left anonymous | 66 | 0.179 / 0.194 m | 1.956 m | 0.367 / 0.021 m/s |
| B:track_006 | U2 | C | correctly left anonymous | 119 | 0.314 / 0.322 m | 2.125 m | 1.604 / 0.047 m/s |
| B:track_007 | U6 | E | correctly left anonymous | 119 | 0.346 / 0.444 m | 1.959 m | 3.826 / 0.079 m/s |
| B:track_008 | U7 | G | correctly left anonymous | 37 | 0.435 / 0.554 m | 1.72 m | 2.821 / 0.058 m/s |
| B:track_009 | U8 | H | correctly left anonymous | 20 | 0.606 / 0.731 m | 1.655 m | 3.801 / 0.054 m/s |
| B:track_010 | U10 | F | correctly left anonymous | 29 | 0.377 / 0.391 m | 1.725 m | 2.835 / 0.053 m/s |
| B:track_011 | U11 | G | correctly left anonymous | 23 | 0.194 / 0.17 m | 2.108 m | 2.339 / 0.118 m/s |
| B:track_012 | U12 | H | correctly left anonymous | 5 | 0.56 / 0.698 m | 1.714 m | 4.024 / 0.05 m/s |
| B:track_013 | U16 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_014 | U17 | J | correctly left anonymous | 31 | 0.297 / 0.379 m | 1.741 m | 3.575 / 0.136 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_003 | -0.05 s | 0.075 m | 0.0 m | 0.075 m | 0.04 m |
| A + B | B | A | B:track_002 | -0.05 s | 0.765 m | 0.0 m | 0.765 m | 1.407 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
