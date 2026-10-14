# Privileged evaluation - S13/run_0_passing

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 5; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 519.118 | 1092.4 | g20 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 6.2 | 6.2 | 0.0 s |
| B | ALIGNED | collision_001 | 6.2 | 6.2 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

40 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 730/730 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | D | correctly left anonymous | 89 | 0.433 / 0.501 m | 1.79 m | 4.883 / 0.073 m/s |
| A:track_002 | B | B | correct | 115 | 0.245 / 0.242 m | 1.666 m | 0.841 / 0.524 m/s |
| A:track_003 | U2 | C | correctly left anonymous | 96 | 0.444 / 0.457 m | 1.955 m | 3.091 / 0.055 m/s |
| B:track_001 | A | A | correct | 115 | 0.115 / 0.255 m | 1.39 m | 3.068 / 0.31 m/s |
| B:track_002 | U1 | D | correctly left anonymous | 51 | 0.425 / 0.568 m | 1.519 m | 6.904 / 0.141 m/s |
| B:track_003 | U2 | C | correctly left anonymous | 81 | 0.538 / 0.619 m | 1.8 m | 2.742 / 0.047 m/s |
| B:track_004 | U1 | D | correctly left anonymous | 15 | 0.489 / 0.675 m | 1.569 m | 4.798 / 0.087 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.166 m | 0.0 m | 0.166 m | 0.306 m |
| A + B | B | A | B:track_001 | 0.0 s | 0.325 m | 0.0 m | 0.325 m | 0.341 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 6.93 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
