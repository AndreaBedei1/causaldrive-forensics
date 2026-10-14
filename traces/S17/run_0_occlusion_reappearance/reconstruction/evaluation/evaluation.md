# Privileged evaluation - S17/run_0_occlusion_reappearance

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 15; max |t_global error| 0.0 s**

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

82 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 3222/3222 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | V | correctly left anonymous | 120 | 0.131 / 0.21 m | 2.809 m | 3.194 / 0.059 m/s |
| A:track_002 | U2 | D | correctly left anonymous | 49 | 0.407 / 0.393 m | 2.004 m | 1.39 / 0.039 m/s |
| A:track_003 | U3 | E | correctly left anonymous | 32 | 0.466 / 0.587 m | 1.681 m | 4.939 / 0.079 m/s |
| A:track_004 | U4 | F | correctly left anonymous | 68 | 0.47 / 0.652 m | 1.536 m | 2.588 / 0.212 m/s |
| A:track_005 | U5 | C | correctly left anonymous | 44 | 0.356 / 0.535 m | 1.526 m | 6.556 / 0.127 m/s |
| A:track_006 | B | B | correct | 111 | 2.278 / 1.829 m | 3.247 m | 5.247 / 1.293 m/s |
| A:track_007 | U5 | C | correctly left anonymous | 56 | 0.274 / 0.27 m | 2.15 m | 2.727 / 0.101 m/s |
| A:track_008 | U2 | D | correctly left anonymous | 54 | 0.42 / 0.532 m | 1.872 m | 6.08 / 0.062 m/s |
| A:track_009 | U8 | E | correctly left anonymous | 27 | 0.31 / 0.546 m | 1.628 m | 7.707 / 0.228 m/s |
| B:track_001 | U5 | C | correctly left anonymous | 81 | 0.312 / 0.295 m | 2.106 m | 1.354 / 0.029 m/s |
| B:track_002 | U2 | D | correctly left anonymous | 50 | 0.423 / 0.502 m | 1.941 m | 3.759 / 0.092 m/s |
| B:track_003 | U1 | V | correctly left anonymous | 79 | 0.096 / 0.306 m | 2.137 m | 1.683 / 0.794 m/s |
| B:track_004 | U3 | E | correctly left anonymous | 31 | 0.445 / 0.579 m | 1.69 m | 3.912 / 0.052 m/s |
| B:track_005 | A | A | correct | 90 | 0.102 / 0.161 m | 1.071 m | 2.567 / 0.549 m/s |
| B:track_006 | U6 | G | correctly left anonymous | 23 | 0.698 / 0.768 m | 1.017 m | 4.397 / 0.301 m/s |
| B:track_007 | U2 | D | correctly left anonymous | 8 | 0.541 / 0.567 m | 1.805 m | 5.851 / 0.27 m/s |
| B:track_008 | U7 | G | correctly left anonymous | 37 | 0.084 / 0.206 m | 1.338 m | 2.945 / 0.719 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_006 | 0.0 s | 0.836 m | 0.0 m | 0.836 m | 1.976 m |
| A + B | B | A | B:track_005 | 0.0 s | 0.0 m | 0.0 m | 0.0 m | 0.852 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.03 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
