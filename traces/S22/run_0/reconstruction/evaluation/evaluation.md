# Privileged evaluation - S22/run_0

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 18; max |t_global error| 0.1 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 422.430 | 389.3 | g48 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.3 | 7.3 | 0.0 s |
| B | ALIGNED | collision_001 | 7.3 | 7.3 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

83 timed global nodes; max |t_global - true global time| = 0.1 s; event order agrees with the truth for 3252/3254 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | V | correctly left anonymous | 119 | 0.116 / 0.128 m | 2.862 m | 0.799 / 0.093 m/s |
| A:track_002 | U2 | D | correctly left anonymous | 49 | 0.405 / 0.392 m | 2.005 m | 1.38 / 0.037 m/s |
| A:track_003 | U3 | E | correctly left anonymous | 32 | 0.454 / 0.533 m | 1.733 m | 4.491 / 0.071 m/s |
| A:track_004 | U4 | F | correctly left anonymous | 68 | 0.471 / 0.645 m | 1.553 m | 2.595 / 0.226 m/s |
| A:track_005 | U1 | V | correctly left anonymous | 88 | 0.167 / 0.225 m | 0.917 m | 5.013 / 0.097 m/s |
| A:track_006 | U5 | C | correctly left anonymous | 45 | 0.401 / 0.564 m | 1.692 m | 5.673 / 0.164 m/s |
| A:track_007 | B | B | correct | 111 | 0.143 / 0.236 m | 1.964 m | 1.524 / 0.848 m/s |
| A:track_008 | U2 | D | correctly left anonymous | 55 | 0.413 / 0.478 m | 1.943 m | 4.833 / 0.051 m/s |
| A:track_009 | U5 | C | correctly left anonymous | 56 | 0.27 / 0.252 m | 2.163 m | 2.53 / 0.094 m/s |
| A:track_010 | U7 | E | correctly left anonymous | 27 | 0.334 / 0.467 m | 1.76 m | 6.801 / 0.205 m/s |
| B:track_001 | U5 | C | correctly left anonymous | 81 | 0.312 / 0.293 m | 2.107 m | 1.354 / 0.031 m/s |
| B:track_002 | U2 | D | correctly left anonymous | 50 | 0.416 / 0.471 m | 1.966 m | 3.748 / 0.104 m/s |
| B:track_003 | U3 | E | correctly left anonymous | 32 | 0.408 / 0.426 m | 1.835 m | 1.651 / 0.051 m/s |
| B:track_004 | U1 | V | correctly left anonymous | 79 | 0.093 / 0.183 m | 2.319 m | 1.511 / 0.897 m/s |
| B:track_005 | U3 | E | correctly left anonymous | 18 | 0.254 / 0.249 m | 0.9 m | 6.484 / 0.129 m/s |
| B:track_006 | A | A | correct | 90 | 0.05 / 0.148 m | 0.996 m | 2.512 / 0.493 m/s |
| B:track_007 | U1 | V | correctly left anonymous | 39 | 0.574 / 0.497 m | 1.345 m | 7.029 / 1.763 m/s |
| B:track_008 | U6 | G | correctly left anonymous | 26 | 0.661 / 0.726 m | 1.127 m | 4.253 / 0.32 m/s |
| B:track_009 | U2 | D | correctly left anonymous | 9 | 0.53 / 0.547 m | 1.844 m | 5.48 / 0.259 m/s |
| B:track_010 | U6 | G | correctly left anonymous | 37 | 0.081 / 0.197 m | 1.303 m | 2.173 / 0.753 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_007 | 0.0 s | 0.42 m | 0.0 m | 0.42 m | 0.693 m |
| A + B | B | A | B:track_006 | 0.0 s | 0.0 m | 0.0 m | 0.0 m | 0.838 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.03 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
