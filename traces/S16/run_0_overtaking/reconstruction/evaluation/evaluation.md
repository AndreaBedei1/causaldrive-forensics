# Privileged evaluation - S16/run_0_overtaking

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 21; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 324.927 | 191.8 | g52 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 6.75 | 6.75 | 0.0 s |
| B | ALIGNED | collision_001 | 6.75 | 6.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

109 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 5706/5706 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | H | correctly left anonymous | 108 | 0.189 / 0.224 m | 2.042 m | 1.159 / 0.148 m/s |
| A:track_002 | U2 | I | correctly left anonymous | 36 | 0.436 / 0.432 m | 1.676 m | 3.104 / 0.064 m/s |
| A:track_003#segment_1 | U3 | F | correctly left anonymous | 48 | 0.345 / 0.304 m | 1.791 m | 0.573 / 0.027 m/s |
| A:track_003#segment_2 | U8 | F | correctly left anonymous | 15 | 0.565 / 0.558 m | 1.547 m | 1.959 / 0.062 m/s |
| A:track_003#segment_3 | U3 | F | correctly left anonymous | 53 | 0.168 / 0.223 m | 1.887 m | 3.17 / 0.07 m/s |
| A:track_004 | U4 | D | correctly left anonymous | 36 | 0.416 / 0.493 m | 1.775 m | 2.444 / 0.085 m/s |
| A:track_005 | U5 | E | correctly left anonymous | 6 | 0.234 / 0.24 m | 2.269 m | 0.658 / 0.037 m/s |
| A:track_006 | B | B | correct | 116 | 0.235 / 0.251 m | 1.712 m | 2.924 / 0.712 m/s |
| A:track_007 | U9 | D | correctly left anonymous | 65 | 0.267 / 0.378 m | 1.914 m | 5.115 / 0.125 m/s |
| A:track_008 | U10 | G | correctly left anonymous | 44 | 1.376 / 1.294 m | 2.13 m | 5.308 / 1.121 m/s |
| A:track_009 | U13 | C | correctly left anonymous | 20 | 0.279 / 0.282 m | 2.192 m | 1.951 / 0.035 m/s |
| A:track_010 | U15 | E | correctly left anonymous | 37 | 0.209 / 0.421 m | 1.771 m | 3.531 / 1.475 m/s |
| A:track_011 | U14 | I | correctly left anonymous | 8 | 0.292 / 0.421 m | 1.628 m | 6.644 / 0.2 m/s |
| B:track_001 | U1 | H | correctly left anonymous | 110 | 0.198 / 0.206 m | 2.06 m | 2.6 / 0.075 m/s |
| B:track_002 | A | A | correct | 120 | 0.177 / 0.239 m | 1.776 m | 1.131 / 0.662 m/s |
| B:track_003 | U3 | F | correctly left anonymous | 118 | 0.404 / 0.456 m | 1.676 m | 3.005 / 0.094 m/s |
| B:track_004 | U6 | E | correctly left anonymous | 53 | 0.284 / 0.466 m | 1.342 m | 2.983 / 0.481 m/s |
| B:track_005 | U7 | G | correctly left anonymous | 27 | 0.448 / 0.558 m | 1.715 m | 3.21 / 0.069 m/s |
| B:track_006 | U9 | D | correctly left anonymous | 61 | 0.269 / 0.36 m | 1.936 m | 4.481 / 0.112 m/s |
| B:track_007 | U11 | G | correctly left anonymous | 53 | 0.3 / 0.35 m | 1.922 m | 4.93 / 0.133 m/s |
| B:track_008 | U12 | C | correctly left anonymous | 8 | 0.189 / 0.198 m | 1.124 m | 3.75 / 0.13 m/s |
| B:track_009 | U14 | I | correctly left anonymous | 13 | 0.569 / 0.602 m | 1.408 m | 6.795 / 0.202 m/s |
| B:track_010 | U15 | E | correctly left anonymous | 18 | 0.201 / 0.532 m | 1.43 m | 3.707 / 1.84 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_006 | -0.05 s | 0.131 m | 0.0 m | 0.131 m | 0.691 m |
| A + B | B | A | B:track_002 | -0.05 s | 0.164 m | 0.0 m | 0.164 m | 0.189 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 7.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
