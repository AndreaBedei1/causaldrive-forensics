# Privileged evaluation - S06/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 7/7; anonymous: 0; max |t_global error| 0.05 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 148.738 | 12137.1 | g29 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 4.1 | 4.1 | 0.0 s |
| B | ALIGNED | collision_001 | 4.1 | 4.1 | 0.0 s |
| C | ALIGNED | - | 4.15 | 4.1 | 0.05 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.050 s, true +0.000 s (error +0.050 s).

Relative clock offset C - B: estimated +0.050 s, true +0.000 s (error +0.050 s).

## Global event times

55 timed global nodes; max |t_global - true global time| = 0.05 s; event order agrees with the truth for 1387/1387 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | C | C | correct | 26 | 0.381 / 0.547 m | 1.771 m | 6.457 / 0.146 m/s |
| A:track_002 | B | B | correct | 131 | 0.089 / 0.118 m | 1.411 m | 1.878 / 0.413 m/s |
| B:track_001 | C | C | correct | 131 | 0.317 / 0.382 m | 1.898 m | 2.339 / 0.717 m/s |
| B:track_002 | A | A | correct | 131 | 0.154 / 0.177 m | 1.16 m | 1.696 / 0.527 m/s |
| C:track_001 | A | A | correct | 3 | 0.201 / 0.442 m | 2.011 m | 6.37 / 0.12 m/s |
| C:track_002 | A | A | correct | 43 | 1.069 / 0.97 m | 2.133 m | 8.854 / 0.441 m/s |
| C:track_003 | B | B | correct | 131 | 0.324 / 0.18 m | 2.018 m | 5.864 / 0.677 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.427 m | 0.0 m | 0.427 m | 1.957 m |
| A + B | B | A | B:track_002 | 0.0 s | 0.487 m | 0.0 m | 0.487 m | 2.204 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
