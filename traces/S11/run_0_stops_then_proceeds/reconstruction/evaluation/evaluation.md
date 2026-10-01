# Privileged evaluation - S11/run_0_stops_then_proceeds

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: no vehicle-vehicle collision in ground truth; associations correct: 0/0; anonymous: 14; max |t_global error| None s**

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
| A:track_001 | A:track_001 | B | left anonymous (true identity B) | 30 | 0.496 / 0.516 m | 0.885 m | 6.299 / 1.241 m/s |
| B:track_001 | B:track_001 | A | left anonymous (true identity A) | 55 | 0.457 / 0.551 m | 1.278 m | 4.934 / 0.703 m/s |
| B:track_002 | B:track_002 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_003 | B:track_003 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_004 | B:track_004 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_005 | B:track_005 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_006 | B:track_006 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_007 | B:track_007 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_008 | B:track_008 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_009 | B:track_009 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_010 | B:track_010 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_011 | B:track_011 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_012 | B:track_012 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_013 | B:track_013 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).
