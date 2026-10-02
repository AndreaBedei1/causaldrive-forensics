# Privileged evaluation - S15/run_0_deflected_into_c

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 4/4; anonymous: 2; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 204.119 | 9797.5 | g29 | yes | 0.0 s |
| A + C | 205.069 | 1637.6 | g43 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| B | ALIGNED | collision_001 | 3.8 | 3.8 | 0.0 s |
| C | ALIGNED | collision_001 -> collision_002 | 3.8 | 3.8 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - B: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

61 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1788/1788 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | C | C | correct | 131 | 0.645 / 0.732 m | 0.685 m | 4.883 / 0.263 m/s |
| A:track_002 | B | B | correct | 17 | 0.549 / 0.499 m | 0.945 m | 8.597 / 0.644 m/s |
| B:track_001 | B:track_001 | A | left anonymous (true identity A) | 120 | 10.6 / 10.443 m | 11.485 m | 6.499 / 1.951 m/s |
| B:track_002 | A | A | correct | 48 | 0.522 / 0.591 m | 1.409 m | 4.647 / 0.976 m/s |
| C:track_001 | A | A | correct | 132 | 0.741 / 0.817 m | 0.778 m | 5.014 / 0.227 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 111 | 0.598 / 0.621 m | 0.522 m | 7.057 / 0.496 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.1 s | 1.284 m | 0.233 m | 1.051 m | 3.744 m |
| A + B | B | A | B:track_002 | 0.0 s | 0.178 m | 0.0 m | 0.178 m | 2.899 m |
| A + C | A | C | A:track_001 | -0.05 s | 0.161 m | 0.0 m | 0.161 m | 2.842 m |
| A + C | C | A | C:track_001 | -0.05 s | 1.018 m | 0.0 m | 1.018 m | 2.622 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
