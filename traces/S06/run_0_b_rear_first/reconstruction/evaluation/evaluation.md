# Privileged evaluation - S06/run_0_b_rear_first

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 3/3; anonymous: 4; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| B + C | 193.409 | 21812.2 | g35 | yes | 0.0 s |
| A + B | 194.809 | 31488.3 | g46 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 6.0 | 6.0 | 0.0 s |
| B | ALIGNED | collision_001 | 6.0 | 6.0 | 0.0 s |
| C | ALIGNED | collision_001 -> collision_002 | 6.0 | 6.0 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - B: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

51 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1227/1227 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | B | left anonymous (true identity B) | 45 | 0.499 / 0.561 m | 1.533 m | 3.696 / 0.1 m/s |
| A:track_002 | A:track_002 | C | left anonymous (true identity C) | 122 | 0.625 / 0.639 m | 1.673 m | 2.687 / 0.101 m/s |
| B:track_001 | C | C | correct | 142 | 0.559 / 0.555 m | 1.748 m | 0.88 / 0.075 m/s |
| B:track_002 | A | A | correct | 57 | 0.811 / 1.041 m | 1.141 m | 6.478 / 0.105 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 23 | 0.905 / 0.976 m | 0.866 m | 5.041 / 0.11 m/s |
| C:track_002 | B | B | correct | 34 | 0.631 / 0.902 m | 1.064 m | 5.82 / 0.086 m/s |
| C:track_003 | C:track_003 | A | left anonymous (true identity A) | 8 | 0.645 / 0.869 m | 1.335 m | 7.64 / 0.164 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| B + C | B | C | B:track_001 | 0.0 s | 0.153 m | 0.0 m | 0.153 m | 2.457 m |
| B + C | C | B | C:track_002 | 0.1 s | 1.995 m | 0.879 m | 1.116 m | 4.467 m |
| A + B | A | B | A:track_002 | 0.0 s | 4.753 m | 0.061 m | 4.692 m | 7.304 m |
| A + B | B | A | B:track_002 | 0.1 s | 1.177 m | 0.729 m | 0.448 m | 3.92 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.33 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
