# Privileged evaluation - S15/run_0_dense_platoon

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 1/1; anonymous: 18; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 192.117 | 34836.9 | g43 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.45 | 7.45 | 0.0 s |
| B | ALIGNED | collision_001 | 7.45 | 7.45 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

67 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 2056/2056 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | F | correctly left anonymous | 95 | 0.233 / 0.241 m | 2.086 m | 1.887 / 0.069 m/s |
| A:track_002 | U2 | D | correctly left anonymous | 116 | 0.359 / 0.192 m | 2.168 m | 3.278 / 0.107 m/s |
| A:track_003 | U3 | I | correctly left anonymous | 120 | 0.195 / 0.203 m | 1.911 m | 1.554 / 0.071 m/s |
| A:track_004 | U4 | H | correctly left anonymous | 115 | 0.401 / 0.41 m | 2.025 m | 3.167 / 0.078 m/s |
| A:track_005 | U5 | E | correctly left anonymous | 86 | 0.352 / 0.359 m | 2.071 m | 3.319 / 0.052 m/s |
| A:track_006 | U6 | G | correctly left anonymous | 120 | 0.178 / 0.267 m | 1.827 m | 2.267 / 0.836 m/s |
| A:track_007 | U7 | J | correctly left anonymous | 120 | 0.18 / 0.309 m | 1.977 m | 2.595 / 0.901 m/s |
| A:track_008 | U9 | C | correctly left anonymous | 22 | 0.236 / 0.51 m | 1.667 m | 6.774 / 0.27 m/s |
| A:track_009 | U10 | E | correctly left anonymous | 9 | 0.196 / 0.548 m | 1.271 m | 8.517 / 0.338 m/s |
| A:track_010 | U11 | F | correctly left anonymous | 8 | 0.23 / 0.386 m | 1.207 m | 11.457 / 0.261 m/s |
| B:track_001 | U6 | G | correctly left anonymous | 75 | 0.183 / 0.184 m | 2.001 m | 0.227 / 0.044 m/s |
| B:track_002 | U5 | E | correctly left anonymous | 37 | 0.514 / 0.495 m | 1.906 m | 2.746 / 0.045 m/s |
| B:track_003 | U7 | J | correctly left anonymous | 75 | 0.158 / 0.157 m | 2.127 m | 0.286 / 0.054 m/s |
| B:track_004 | U3 | I | correctly left anonymous | 69 | 0.507 / 0.613 m | 1.511 m | 2.934 / 0.071 m/s |
| B:track_005 | U1 | F | correctly left anonymous | 73 | 0.266 / 0.279 m | 2.008 m | 1.529 / 0.058 m/s |
| B:track_006 | A | A | correct | 119 | 0.198 / 0.178 m | 1.918 m | 2.042 / 0.081 m/s |
| B:track_007 | U4 | H | correctly left anonymous | 30 | 0.439 / 0.494 m | 1.903 m | 2.446 / 0.034 m/s |
| B:track_008 | U5 | E | correctly left anonymous | 5 | 0.568 / 0.597 m | 1.812 m | 1.547 / 0.124 m/s |
| B:track_009 | U8 | H | correctly left anonymous | 3 | 0.646 / 0.518 m | 1.895 m | 5.084 / 0.043 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | - | - s | - m | - m | - m | - m |
| A + B | B | A | B:track_006 | -0.05 s | 0.105 m | 0.0 m | 0.105 m | 0.196 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.18 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
