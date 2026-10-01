# Privileged evaluation - S08/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 4; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 110.335 | 12077.2 | g20 | yes | 0.0 s |

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

32 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 476/476 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 150 | 0.23 / 0.269 m | 2.067 m | 3.938 / 0.166 m/s |
| A:track_002 | B | B | correct | 21 | 0.421 / 0.504 m | 0.964 m | 4.85 / 0.376 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 130 | 0.206 / 0.27 m | 1.992 m | 4.154 / 0.803 m/s |
| B:track_002 | A | A | correct | 129 | 0.186 / 0.369 m | 1.052 m | 3.397 / 0.531 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 148 | 0.657 / 0.708 m | 1.261 m | 4.342 / 0.154 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 131 | 0.264 / 0.301 m | 0.802 m | 5.645 / 0.55 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by - s (expected -0.73 s).
