# Privileged evaluation - S07/run_0_occluded

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 5; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 233.320 | 31406.8 | g28 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 5.7 | 5.7 | 0.0 s |
| B | ALIGNED | collision_001 | 5.7 | 5.7 | 0.0 s |
| C | UNALIGNED | - | - | 5.7 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

35 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 574/574 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 142 | 0.739 / 0.83 m | 1.266 m | 3.69 / 0.109 m/s |
| A:track_002 | A:track_002 | C | left anonymous (true identity C) | 21 | 0.746 / 0.791 m | 1.499 m | 3.903 / 0.109 m/s |
| A:track_003 | A:track_003 | C | left anonymous (true identity C) | 4 | 0.315 / 0.346 m | 1.958 m | 2.696 / 0.194 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 141 | 0.507 / 0.494 m | 1.82 m | 3.875 / 0.1 m/s |
| B:track_002 | A | A | correct | 57 | 0.816 / 1.046 m | 1.144 m | 6.338 / 0.1 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 21 | 0.895 / 1.019 m | 0.641 m | 3.978 / 0.123 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 25 | 0.68 / 0.945 m | 0.844 m | 8.175 / 0.103 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_001 | 0.0 s | 0.2 m | 0.008 m | 0.192 m | 3.083 m |
| A + B | B | A | B:track_002 | 0.1 s | 1.103 m | 0.672 m | 0.431 m | 3.903 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
