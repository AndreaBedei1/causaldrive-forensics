# Privileged evaluation - S08/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 4; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 253.027 | 12077.2 | g18 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 4.25 | 4.25 | 0.0 s |
| B | ALIGNED | collision_001 | 4.25 | 4.25 | 0.0 s |
| C | UNALIGNED | - | - | 4.25 | - s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

31 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 448/448 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 142 | 0.597 / 0.778 m | 1.455 m | 8.986 / 0.147 m/s |
| A:track_002 | B | B | correct | 24 | 0.531 / 0.548 m | 0.736 m | 9.083 / 0.419 m/s |
| B:track_001 | A | A | correct | 131 | 0.396 / 0.4 m | 0.919 m | 3.692 / 0.376 m/s |
| B:track_002 | B:track_002 | C | left anonymous (true identity C) | 127 | 0.53 / 0.537 m | 0.674 m | 4.16 / 0.528 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 141 | 0.665 / 0.829 m | 1.325 m | 9.355 / 0.233 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 129 | 0.291 / 0.309 m | 0.804 m | 6.783 / 0.601 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.05 s | 1.458 m | 0.234 m | 1.224 m | 3.046 m |
| A + B | B | A | B:track_001 | -0.05 s | 0.0 m | 0.0 m | 0.0 m | 2.485 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
