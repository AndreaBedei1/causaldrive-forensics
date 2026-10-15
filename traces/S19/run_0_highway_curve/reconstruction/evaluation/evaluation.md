# Privileged evaluation - S19/run_0_highway_curve

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 16; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 28.146 | 7449.2 | g44 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.5 | 7.5 | 0.0 s |
| B | ALIGNED | collision_001 | 7.5 | 7.5 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

70 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 2271/2271 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | C | correctly left anonymous | 82 | 0.275 / 0.431 m | 1.555 m | 2.141 / 0.107 m/s |
| A:track_002 | B | B | correct | 120 | 0.345 / 0.415 m | 2.035 m | 2.514 / 0.1 m/s |
| A:track_003 | U2 | D | correctly left anonymous | 119 | 0.324 / 0.431 m | 1.625 m | 4.824 / 0.157 m/s |
| A:track_004 | U3 | G | correctly left anonymous | 49 | 0.269 / 0.348 m | 1.94 m | 5.099 / 0.078 m/s |
| A:track_005 | U4 | F | correctly left anonymous | 24 | 0.249 / 0.317 m | 2.157 m | 1.453 / 0.272 m/s |
| A:track_006 | U6 | E | correctly left anonymous | 4 | 0.298 / 0.441 m | 1.71 m | 5.744 / 0.132 m/s |
| A:track_007 | U5 | E | correctly left anonymous | 4 | 0.434 / 0.501 m | 1.0 m | 3.509 / 0.233 m/s |
| A:track_008 | U5 | E | correctly left anonymous | 4 | 0.347 / 0.324 m | 0.825 m | 19.65 / 0.121 m/s |
| A:track_009 | U5 | E | correctly left anonymous | 1 | 0.074 / 0.046 m | 1.053 m | - / 0.566 m/s |
| A:track_010 | U7 | G | correctly left anonymous | 5 | 0.333 / 0.459 m | 1.807 m | 4.755 / 0.067 m/s |
| A:track_011 | U8 | F | correctly left anonymous | 33 | 0.396 / 0.68 m | 0.693 m | 5.154 / 0.521 m/s |
| B:track_001 | U3 | G | correctly left anonymous | 71 | 0.313 / 0.35 m | 1.911 m | 7.916 / 0.058 m/s |
| B:track_002 | U5 | E | correctly left anonymous | 50 | 0.358 / 0.477 m | 1.631 m | 6.324 / 0.077 m/s |
| B:track_003 | U1 | C | correctly left anonymous | 105 | 0.341 / 0.502 m | 1.583 m | 3.953 / 0.368 m/s |
| B:track_004 | U2 | D | correctly left anonymous | 120 | 0.195 / 0.438 m | 1.105 m | 4.819 / 0.309 m/s |
| B:track_005 | A | A | correct | 12 | 0.151 / 0.18 m | 2.011 m | 1.168 / 0.047 m/s |
| B:track_006 | U9 | G | correctly left anonymous | 3 | 0.568 / 0.603 m | 1.657 m | 10.647 / 0.126 m/s |
| B:track_007 | U8 | F | correctly left anonymous | 25 | 0.375 / 0.668 m | 0.588 m | 4.756 / 0.497 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.166 m | 0.0 m | 0.166 m | 0.906 m |
| A + B | B | A | B:track_005 | 0.9 s | 4.821 m | 4.464 m | 0.357 m | 7.069 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.23 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
