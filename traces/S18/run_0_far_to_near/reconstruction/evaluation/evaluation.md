# Privileged evaluation - S18/run_0_far_to_near

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 18; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 543.381 | 745.3 | g65 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 8.5 | 8.5 | 0.0 s |
| B | ALIGNED | collision_001 | 8.5 | 8.5 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

90 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 3908/3908 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | F | correctly left anonymous | 43 | 0.204 / 0.337 m | 1.651 m | 2.562 / 1.392 m/s |
| A:track_002 | B | B | correct | 120 | 0.117 / 0.149 m | 0.99 m | 1.969 / 0.301 m/s |
| A:track_003 | U2 | G | correctly left anonymous | 13 | 0.131 / 0.204 m | 2.077 m | 2.291 / 1.017 m/s |
| A:track_004 | U6 | C | correctly left anonymous | 27 | 0.769 / 0.81 m | 1.546 m | 4.769 / 0.045 m/s |
| A:track_005 | U3 | E | correctly left anonymous | 65 | 0.252 / 0.359 m | 1.822 m | 2.296 / 1.306 m/s |
| A:track_006 | U7 | C | correctly left anonymous | 4 | 1.623 / 1.282 m | 2.71 m | - / 1.418 m/s |
| A:track_007 | U9 | C | correctly left anonymous | 54 | 0.296 / 0.239 m | 2.183 m | 1.377 / 0.043 m/s |
| A:track_008 | U8 | D | correctly left anonymous | 44 | 0.242 / 0.284 m | 2.171 m | 2.013 / 0.158 m/s |
| A:track_009 | U3 | E | correctly left anonymous | 14 | 0.144 / 0.24 m | 2.0 m | 1.505 / 0.524 m/s |
| B:track_001 | U1 | F | correctly left anonymous | 24 | 0.204 / 0.432 m | 1.418 m | 2.956 / 0.792 m/s |
| B:track_002 | A | A | correct | 120 | 0.135 / 0.292 m | 1.067 m | 2.93 / 0.491 m/s |
| B:track_003 | U3 | E | correctly left anonymous | 55 | 0.296 / 0.507 m | 1.651 m | 3.889 / 0.635 m/s |
| B:track_004 | U4 | G | correctly left anonymous | 22 | 0.192 / 0.605 m | 1.505 m | 5.08 / 1.057 m/s |
| B:track_005 | U5 | D | correctly left anonymous | 18 | 0.656 / 0.87 m | 1.424 m | 6.537 / 0.032 m/s |
| B:track_006 | U6 | C | correctly left anonymous | 18 | 0.67 / 0.895 m | 1.12 m | 3.798 / 0.217 m/s |
| B:track_007 | U1 | F | correctly left anonymous | 20 | 0.24 / 0.567 m | 1.37 m | 3.256 / 0.927 m/s |
| B:track_008 | U8 | D | correctly left anonymous | 54 | 0.346 / 0.408 m | 2.032 m | 2.693 / 0.167 m/s |
| B:track_009 | U9 | C | correctly left anonymous | 52 | 0.238 / 0.264 m | 2.182 m | 2.231 / 0.086 m/s |
| B:track_010 | U3 | E | correctly left anonymous | 19 | 0.18 / 0.401 m | 1.326 m | 3.479 / 0.919 m/s |
| B:track_011 | U3 | E | correctly left anonymous | 21 | 0.234 / 0.404 m | 1.564 m | 1.725 / 0.449 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.336 m | 0.0 m | 0.336 m | 0.354 m |
| A + B | B | A | B:track_002 | 0.0 s | 0.267 m | 0.0 m | 0.267 m | 0.844 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 9.23 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
