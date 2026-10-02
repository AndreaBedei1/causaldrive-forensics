# Privileged evaluation - S01/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 0; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 39.596 | 17663.1 | g17 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 6.5 | 6.5 | 0.0 s |
| B | ALIGNED | collision_001 | 6.5 | 6.5 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

21 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 198/198 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 115 | 0.696 / 0.787 m | 1.313 m | 4.177 / 0.125 m/s |
| B:track_001 | A | A | correct | 57 | 0.787 / 1.016 m | 1.07 m | 6.564 / 0.112 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_001 | 0.0 s | 0.327 m | 0.0 m | 0.327 m | 3.074 m |
| A + B | B | A | B:track_001 | 0.1 s | 0.819 m | 0.367 m | 0.452 m | 3.661 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 7.23 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
