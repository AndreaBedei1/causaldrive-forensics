# Privileged evaluation - S06/run_0_a_front_pushed

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 3/3; anonymous: 4; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 159.043 | 11621.7 | g48 | yes | 0.0 s |
| B + C | 159.193 | 10857.6 | g51 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 5.9 | 5.9 | 0.0 s |
| B | ALIGNED | collision_001 | 5.9 | 5.9 | 0.0 s |
| C | ALIGNED | collision_001 -> collision_002 | 5.9 | 5.9 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - B: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

59 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1650/1650 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 297 | 0.792 / 0.906 m | 1.103 m | 3.734 / 0.129 m/s |
| A:track_002 | A:track_002 | C | left anonymous (true identity C) | 282 | 0.61 / 0.616 m | 1.69 m | 2.187 / 0.08 m/s |
| B:track_001 | C | C | correct | 300 | 0.58 / 0.578 m | 1.726 m | 0.692 / 0.052 m/s |
| B:track_002 | A | A | correct | 57 | 0.79 / 1.046 m | 1.111 m | 6.295 / 0.11 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 25 | 0.837 / 0.987 m | 0.862 m | 7.091 / 0.109 m/s |
| C:track_002 | C:track_002 | A | left anonymous (true identity A) | 279 | 8.364 / 8.272 m | 9.209 m | 6.831 / 2.738 m/s |
| C:track_003 | C:track_003 | A | left anonymous (true identity A) | 11 | 0.753 / 0.96 m | 0.935 m | 6.115 / 0.194 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_001 | 0.0 s | 0.529 m | 0.0 m | 0.529 m | 3.363 m |
| A + B | B | A | B:track_002 | 0.1 s | 0.959 m | 0.735 m | 0.224 m | 3.965 m |
| B + C | B | C | B:track_001 | -0.05 s | 0.248 m | 0.0 m | 0.248 m | 2.467 m |
| B + C | C | B | C:track_002 | -0.05 s | 3.803 m | 0.0 m | 3.803 m | 6.162 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 6.78 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
