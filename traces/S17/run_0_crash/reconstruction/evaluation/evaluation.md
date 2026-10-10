# Privileged evaluation - S17/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 3; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 19.257 | 1576.9 | g20 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 4.95 | 4.95 | 0.0 s |
| B | ALIGNED | collision_001 | 4.95 | 4.95 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

40 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 721/721 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | correctly left anonymous | 73 | 0.289 / 0.313 m | 2.132 m | 0.788 / 0.081 m/s |
| A:track_002 | B | B | correct | 110 | 0.174 / 0.194 m | 2.103 m | 0.832 / 0.34 m/s |
| B:track_001 | A | A | correct | 110 | 0.1 / 0.223 m | 1.342 m | 2.283 / 0.461 m/s |
| B:track_002 | B:track_002 | C | correctly left anonymous | 58 | 0.18 / 0.387 m | 1.018 m | 5.152 / 0.558 m/s |
| B:track_003 | B:track_003 | C | correctly left anonymous | 6 | 0.424 / 0.557 m | 1.007 m | 6.697 / 0.427 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | -0.05 s | 0.105 m | 0.0 m | 0.105 m | 0.155 m |
| A + B | B | A | B:track_001 | -0.05 s | 0.242 m | 0.0 m | 0.242 m | 0.855 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.68 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
