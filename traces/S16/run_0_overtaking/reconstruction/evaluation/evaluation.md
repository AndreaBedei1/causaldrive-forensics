# Privileged evaluation - S16/run_0_overtaking

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 19; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 324.927 | 191.8 | g48 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 6.75 | 6.75 | 0.0 s |
| B | ALIGNED | collision_001 | 6.75 | 6.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

99 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 4711/4711 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | H | correctly left anonymous | 108 | 0.207 / 0.252 m | 2.022 m | 1.982 / 0.141 m/s |
| A:track_002 | U2 | I | correctly left anonymous | 36 | 0.446 / 0.448 m | 1.664 m | 3.17 / 0.068 m/s |
| A:track_003 | U3 | F | correctly left anonymous | 118 | 0.321 / 0.326 m | 1.777 m | 4.687 / 0.056 m/s |
| A:track_004 | U4 | D | correctly left anonymous | 36 | 0.42 / 0.503 m | 1.768 m | 2.408 / 0.089 m/s |
| A:track_005 | U5 | E | correctly left anonymous | 6 | 0.234 / 0.239 m | 2.271 m | 0.658 / 0.037 m/s |
| A:track_006 | B | B | correct | 116 | 0.253 / 0.283 m | 1.642 m | 4.725 / 0.8 m/s |
| A:track_007 | U4 | D | correctly left anonymous | 64 | 0.272 / 0.457 m | 1.835 m | 6.552 / 0.081 m/s |
| A:track_008 | U9 | G | correctly left anonymous | 49 | 1.37 / 1.346 m | 2.184 m | 6.593 / 1.028 m/s |
| A:track_009 | U10 | C | correctly left anonymous | 16 | 0.265 / 0.229 m | 2.247 m | 1.951 / 0.056 m/s |
| A:track_010 | U11 | E | correctly left anonymous | 37 | 0.207 / 0.457 m | 1.716 m | 3.51 / 1.396 m/s |
| A:track_011 | U12 | I | correctly left anonymous | 3 | 0.212 / 0.263 m | 1.37 m | 5.857 / 0.122 m/s |
| A:track_012 | U12 | I | correctly left anonymous | 5 | 0.333 / 0.24 m | 1.883 m | 4.756 / 0.129 m/s |
| B:track_001 | A | A | correct | 120 | 2.373 / 1.914 m | 3.043 m | 4.411 / 1.077 m/s |
| B:track_002 | U3 | F | correctly left anonymous | 119 | 0.41 / 0.491 m | 1.637 m | 4.182 / 0.079 m/s |
| B:track_003 | U6 | E | correctly left anonymous | 53 | 0.284 / 0.471 m | 1.328 m | 2.97 / 0.462 m/s |
| B:track_004 | U1 | H | correctly left anonymous | 109 | 0.211 / 0.232 m | 2.039 m | 3.036 / 0.082 m/s |
| B:track_005 | U7 | G | correctly left anonymous | 22 | 0.451 / 0.55 m | 1.724 m | 1.773 / 0.066 m/s |
| B:track_006 | U4 | D | correctly left anonymous | 61 | 0.269 / 0.413 m | 1.854 m | 4.865 / 0.142 m/s |
| B:track_007 | U8 | G | correctly left anonymous | 53 | 0.352 / 0.423 m | 1.853 m | 5.555 / 0.13 m/s |
| B:track_008 | U12 | I | correctly left anonymous | 12 | 0.582 / 0.64 m | 1.384 m | 6.795 / 0.201 m/s |
| B:track_009 | U11 | E | correctly left anonymous | 18 | 0.201 / 0.531 m | 1.439 m | 3.92 / 1.906 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_006 | -0.05 s | 0.09 m | 0.0 m | 0.09 m | 0.891 m |
| A + B | B | A | B:track_001 | -0.05 s | 0.0 m | 0.0 m | 0.0 m | 0.914 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 7.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
