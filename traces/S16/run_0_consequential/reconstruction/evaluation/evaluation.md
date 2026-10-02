# Privileged evaluation - S16/run_0_consequential

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 3/3; anonymous: 1; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 258.666 | 6073.8 | g23 | yes | 0.0 s |
| A + C | 259.416 | 2695.7 | g33 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 5.15 | 5.15 | 0.0 s |
| B | ALIGNED | collision_001 | 5.15 | 5.15 | 0.0 s |
| C | ALIGNED | collision_001 -> collision_002 | 5.15 | 5.15 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - B: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

41 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 776/776 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 100 | 0.852 / 0.925 m | 0.747 m | 4.975 / 0.123 m/s |
| B:track_001 | A | A | correct | 98 | 0.724 / 0.865 m | 1.071 m | 5.266 / 0.178 m/s |
| C:track_001 | A | A | correct | 30 | 0.597 / 0.916 m | 0.936 m | 8.66 / 0.105 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 78 | 0.736 / 0.85 m | 0.581 m | 6.032 / 0.268 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_001 | -0.05 s | 0.256 m | 0.0 m | 0.256 m | 3.614 m |
| A + B | B | A | B:track_001 | -0.05 s | 0.613 m | 0.0 m | 0.613 m | 3.041 m |
| A + C | A | C | - | - s | - m | - m | - m | - m |
| A + C | C | A | C:track_001 | 0.8 s | 5.231 m | 2.825 m | 2.406 m | 7.369 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 6.63 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
