# Privileged evaluation - S14/run_0_surrounded

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 25; max |t_global error| 0.1 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 71.377 | 254.4 | g42 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |
| B | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

84 timed global nodes; max |t_global - true global time| = 0.1 s; event order agrees with the truth for 3387/3387 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | P | correctly left anonymous | 120 | 0.134 / 0.139 m | 2.152 m | 0.218 / 0.075 m/s |
| A:track_002 | U2 | C | correctly left anonymous | 120 | 0.294 / 0.301 m | 2.154 m | 1.21 / 0.081 m/s |
| A:track_003 | B | B | correct | 120 | 0.092 / 0.121 m | 1.264 m | 1.081 / 0.207 m/s |
| A:track_004 | U9 | K | correctly left anonymous | 27 | 0.121 / 0.209 m | 1.069 m | 4.266 / 0.25 m/s |
| A:track_005 | U3 | D | correctly left anonymous | 51 | 0.096 / 0.149 m | 2.135 m | 1.226 / 0.085 m/s |
| A:track_006 | U13 | L | correctly left anonymous | 4 | 0.973 / 0.992 m | 0.827 m | 3.841 / 0.192 m/s |
| A:track_007 | U14 | J | correctly left anonymous | 7 | 0.094 / 0.225 m | 1.934 m | 0.679 / 0.237 m/s |
| A:track_008 | U10 | G | correctly left anonymous | 46 | 0.192 / 0.245 m | 2.056 m | 3.229 / 0.091 m/s |
| A:track_009 | U7 | E | correctly left anonymous | 44 | 0.244 / 0.304 m | 2.145 m | 2.446 / 0.094 m/s |
| A:track_010 | U11 | F | correctly left anonymous | 33 | 0.315 / 0.339 m | 1.78 m | 3.029 / 0.048 m/s |
| A:track_011 | U15 | J | correctly left anonymous | 13 | 0.38 / 0.426 m | 1.368 m | 5.985 / 0.143 m/s |
| B:track_001 | U3 | D | correctly left anonymous | 120 | 0.181 / 0.175 m | 2.1 m | 0.466 / 0.043 m/s |
| B:track_002 | A | A | correct | 120 | 0.133 / 0.377 m | 0.863 m | 5.995 / 0.484 m/s |
| B:track_003 | U1 | P | correctly left anonymous | 120 | 0.199 / 0.226 m | 2.043 m | 0.85 / 0.111 m/s |
| B:track_004 | U4 | F | correctly left anonymous | 35 | 0.499 / 0.601 m | 1.516 m | 3.748 / 0.03 m/s |
| B:track_005 | U5 | K | correctly left anonymous | 66 | 0.179 / 0.195 m | 1.956 m | 0.367 / 0.022 m/s |
| B:track_006 | U6 | G | correctly left anonymous | 37 | 0.433 / 0.452 m | 1.816 m | 2.052 / 0.078 m/s |
| B:track_007 | U7 | E | correctly left anonymous | 119 | 0.341 / 0.434 m | 1.985 m | 2.889 / 0.113 m/s |
| B:track_008 | U2 | C | correctly left anonymous | 119 | 0.298 / 0.297 m | 2.142 m | 1.357 / 0.047 m/s |
| B:track_009 | U8 | H | correctly left anonymous | 21 | 0.598 / 0.724 m | 1.669 m | 3.703 / 0.048 m/s |
| B:track_010 | U6 | G | correctly left anonymous | 20 | 0.321 / 0.422 m | 0.962 m | 5.574 / 0.149 m/s |
| B:track_011 | U10 | G | correctly left anonymous | 24 | 0.192 / 0.165 m | 2.109 m | 2.271 / 0.112 m/s |
| B:track_012 | U11 | F | correctly left anonymous | 29 | 0.376 / 0.388 m | 1.729 m | 2.796 / 0.063 m/s |
| B:track_013 | U12 | J | correctly left anonymous | 38 | 0.982 / 1.004 m | 2.195 m | 3.655 / 0.138 m/s |
| B:track_014 | U5 | K | correctly left anonymous | 2 | 0.163 / 0.207 m | 1.995 m | 2.001 / 0.261 m/s |
| B:track_015 | U16 | H | correctly left anonymous | 2 | 0.319 / 0.238 m | 1.298 m | 7.368 / 0.027 m/s |
| B:track_016 | U17 | G | correctly left anonymous | 3 | 0.164 / 0.129 m | 2.189 m | 1.193 / 0.543 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_003 | -0.05 s | 0.085 m | 0.0 m | 0.085 m | 0.049 m |
| A + B | B | A | B:track_002 | -0.05 s | 0.707 m | 0.0 m | 0.707 m | 1.047 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
