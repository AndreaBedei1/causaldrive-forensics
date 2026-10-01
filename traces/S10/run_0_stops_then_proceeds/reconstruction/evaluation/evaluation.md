# Privileged evaluation - S10/run_0_stops_then_proceeds

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: no vehicle-vehicle collision in ground truth; associations correct: 0/0; anonymous: 16; max |t_global error| None s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | UNALIGNED | - | - | - | - s |
| B | UNALIGNED | - | - | - | - s |

## Global event times

0 timed global nodes; max |t_global - true global time| = - s; event order agrees with the truth for 0/0 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | B | left anonymous (true identity B) | 52 | 0.382 / 0.571 m | 1.12 m | 4.199 / 0.672 m/s |
| A:track_002 | A:track_002 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_003 | A:track_003 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_004 | A:track_004 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_005 | A:track_005 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_006 | A:track_006 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_007 | A:track_007 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_008 | A:track_008 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_009 | A:track_009 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_010 | A:track_010 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_011 | A:track_011 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_012 | A:track_012 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_013 | A:track_013 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_014 | A:track_014 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| A:track_015 | A:track_015 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_001 | B:track_001 | A | left anonymous (true identity A) | 33 | 0.491 / 0.529 m | 0.988 m | 6.254 / 1.074 m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).
