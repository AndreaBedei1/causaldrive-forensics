# Privileged evaluation - S15/run_0_b_stops

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: no vehicle-vehicle collision in ground truth; associations correct: 0/0; anonymous: 6; max |t_global error| None s**

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
| C | UNALIGNED | - | - | - | - s |

## Global event times

0 timed global nodes; max |t_global - true global time| = - s; event order agrees with the truth for 0/0 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | A:track_001 | C | left anonymous (true identity C) | 74 | 0.501 / 0.714 m | 1.287 m | 6.794 / 0.679 m/s |
| A:track_002 | A:track_002 | B | left anonymous (true identity B) | 71 | 0.39 / 0.382 m | 0.923 m | 11.125 / 0.744 m/s |
| B:track_001 | B:track_001 | C | left anonymous (true identity C) | 81 | 0.357 / 0.43 m | 1.053 m | 5.118 / 0.364 m/s |
| B:track_002 | B:track_002 | A | left anonymous (true identity A) | 65 | 0.393 / 0.556 m | 1.533 m | 5.787 / 0.789 m/s |
| C:track_001 | C:track_001 | A | left anonymous (true identity A) | 77 | 0.524 / 0.73 m | 1.587 m | 6.439 / 0.917 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 94 | 0.475 / 0.536 m | 0.905 m | 9.065 / 0.54 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).
