# Privileged evaluation - S19/run_0

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 22; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 150.140 | 255.0 | g40 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |
| B | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

77 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 2838/2838 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001#segment_1 | U1 | C | correctly left anonymous | 8 | 0.74 / 0.244 m | 2.161 m | 4.446 / 0.474 m/s |
| A:track_001#segment_2 | U8 | C | correctly left anonymous | 112 | 0.291 / 0.297 m | 2.156 m | 1.248 / 0.085 m/s |
| A:track_002 | U2 | J | correctly left anonymous | 17 | 0.558 / 0.635 m | 1.458 m | 3.381 / 0.028 m/s |
| A:track_003 | U3 | H | correctly left anonymous | 24 | 0.564 / 0.775 m | 1.623 m | 4.314 / 0.029 m/s |
| A:track_004 | B | B | correct | 120 | 0.092 / 0.121 m | 1.264 m | 1.081 / 0.207 m/s |
| A:track_005#segment_1 | U7 | E | correctly left anonymous | 62 | 0.235 / 0.238 m | 2.16 m | 0.425 / 0.038 m/s |
| A:track_005#segment_2 | U9 | E | correctly left anonymous | 20 | 1.388 / 1.246 m | 3.269 m | 1.77 / 0.109 m/s |
| A:track_005#segment_3 | U4 | D | correctly left anonymous | 37 | 0.086 / 0.09 m | 2.178 m | 0.36 / 0.026 m/s |
| A:track_006 | U12 | J | correctly left anonymous | 11 | 0.297 / 0.287 m | 1.811 m | 2.92 / 0.039 m/s |
| A:track_007 | U10 | G | correctly left anonymous | 46 | 0.19 / 0.246 m | 2.056 m | 3.21 / 0.092 m/s |
| A:track_008 | U7 | E | correctly left anonymous | 41 | 0.212 / 0.389 m | 2.026 m | 2.812 / 0.189 m/s |
| A:track_009 | U11 | F | correctly left anonymous | 33 | 0.315 / 0.34 m | 1.779 m | 3.029 / 0.048 m/s |
| A:track_010 | U14 | J | correctly left anonymous | 13 | 0.383 / 0.429 m | 1.368 m | 5.963 / 0.143 m/s |
| B:track_001 | U4 | D | correctly left anonymous | 120 | 0.177 / 0.175 m | 2.1 m | 0.452 / 0.043 m/s |
| B:track_002 | A | A | correct | 120 | 0.132 / 0.376 m | 0.862 m | 5.851 / 0.479 m/s |
| B:track_003 | U5 | F | correctly left anonymous | 35 | 0.498 / 0.6 m | 1.518 m | 3.698 / 0.03 m/s |
| B:track_004 | U6 | G | correctly left anonymous | 38 | 0.445 / 0.505 m | 1.765 m | 2.346 / 0.051 m/s |
| B:track_005 | U7 | E | correctly left anonymous | 119 | 0.343 / 0.419 m | 2.022 m | 2.753 / 0.086 m/s |
| B:track_006 | U8 | C | correctly left anonymous | 119 | 0.298 / 0.297 m | 2.143 m | 1.356 / 0.047 m/s |
| B:track_007 | U3 | H | correctly left anonymous | 21 | 0.598 / 0.724 m | 1.669 m | 3.704 / 0.048 m/s |
| B:track_008 | U10 | G | correctly left anonymous | 24 | 0.192 / 0.166 m | 2.108 m | 2.281 / 0.112 m/s |
| B:track_009 | U11 | F | correctly left anonymous | 29 | 0.376 / 0.387 m | 1.73 m | 2.793 / 0.063 m/s |
| B:track_010 | U13 | J | correctly left anonymous | 38 | 0.982 / 1.003 m | 2.196 m | 3.667 / 0.138 m/s |
| B:track_011 | U15 | H | correctly left anonymous | 2 | 0.323 / 0.238 m | 1.329 m | 7.346 / 0.025 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_004 | -0.05 s | 0.085 m | 0.0 m | 0.085 m | 0.048 m |
| A + B | B | A | B:track_002 | -0.05 s | 0.706 m | 0.0 m | 0.706 m | 1.047 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
