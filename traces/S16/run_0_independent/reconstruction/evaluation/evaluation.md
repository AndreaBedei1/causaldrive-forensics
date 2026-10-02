# Privileged evaluation - S16/run_0_independent

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 2/2; anonymous: 5; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 273.029 | 6073.8 | g23 | yes | 0.0 s |
| A + C | 281.979 | 9089.8 | g50 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_002 | 14.1 | 14.1 | 0.0 s |
| B | ALIGNED | collision_002 -> collision_001 | 14.1 | 14.1 | 0.0 s |
| C | ALIGNED | collision_002 | 14.1 | 14.1 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - B: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

58 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1605/1605 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | B | B | correct | 168 | 0.848 / 0.917 m | 0.576 m | 4.752 / 0.151 m/s |
| A:track_002 | A:track_002 | C | left anonymous (true identity C) | 45 | 0.146 / 0.147 m | 2.812 m | 0.726 / 0.159 m/s |
| B:track_001 | A | A | correct | 136 | 0.74 / 0.923 m | 1.077 m | 5.22 / 0.143 m/s |
| B:track_002 | B:track_002 | C | left anonymous (true identity C) | 45 | 0.39 / 0.568 m | 2.401 m | 7.298 / 0.158 m/s |
| C:track_001 | C:track_001 | B | left anonymous (true identity B) | 46 | 0.657 / 0.793 m | 0.518 m | 13.097 / 0.291 m/s |
| C:track_002 | C:track_002 | A | left anonymous (true identity A) | 4 | 0.608 / 0.828 m | 0.293 m | - / 0.744 m/s |
| C:track_003 | C:track_003 | A | left anonymous (true identity A) | 2 | 0.769 / 0.934 m | 0.182 m | - / 0.46 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_001 | -0.05 s | 0.428 m | 0.0 m | 0.428 m | 3.786 m |
| A + B | B | A | B:track_001 | -0.05 s | 0.651 m | 0.0 m | 0.651 m | 3.051 m |
| A + C | A | C | A:track_002 | 0.0 s | 0.102 m | 0.0 m | 0.102 m | 2.235 m |
| A + C | C | A | - | - s | - m | - m | - m | - m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 14.83 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
