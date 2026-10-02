# Privileged evaluation - S15/run_0_single_impact

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 5; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 224.207 | 9797.5 | g19 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| B | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| C | UNALIGNED | - | - | 3.8 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

39 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 710/710 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 70 | 0.511 / 0.686 m | 1.412 m | 9.331 / 0.042 m/s |
| A:track_002 | B | B | correct | 17 | 0.549 / 0.499 m | 0.945 m | 8.597 / 0.644 m/s |
| B:track_001 | A | A | correct | 118 | 0.51 / 0.578 m | 1.694 m | 5.37 / 0.59 m/s |
| B:track_002 | B:track_002 | C | left anonymous (true identity C) | 47 | 0.47 / 0.801 m | 1.295 m | 9.207 / 0.07 m/s |
| C:track_001 | C:track_001 | B | left anonymous (true identity B) | 6 | 0.283 / 0.465 m | 0.981 m | - / 1.781 m/s |
| C:track_002 | C:track_002 | A | left anonymous (true identity A) | 107 | 0.648 / 0.842 m | 1.121 m | 10.022 / 0.119 m/s |
| C:track_003 | C:track_003 | B | left anonymous (true identity B) | 73 | 0.201 / 0.178 m | 0.877 m | 12.892 / 0.832 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.1 s | 1.284 m | 0.233 m | 1.051 m | 3.744 m |
| A + B | B | A | B:track_001 | 0.0 s | 0.194 m | 0.0 m | 0.194 m | 2.916 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
