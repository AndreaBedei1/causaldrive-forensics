# Privileged evaluation - S06/run_0_crash

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 6/6; anonymous: 1; max |t_global error| 0.05 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 148.738 | 12137.1 | g27 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 4.1 | 4.1 | 0.0 s |
| B | ALIGNED | collision_001 | 4.1 | 4.1 | 0.0 s |
| C | ALIGNED | - | 4.15 | 4.1 | 0.05 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.050 s, true +0.000 s (error +0.050 s).

Relative clock offset C - B: estimated +0.050 s, true +0.000 s (error +0.050 s).

## Global event times

56 timed global nodes; max |t_global - true global time| = 0.05 s; event order agrees with the truth for 1417/1417 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | C | C | correct | 152 | 0.242 / 0.299 m | 2.047 m | 4.26 / 0.124 m/s |
| A:track_002 | B | B | correct | 131 | 0.089 / 0.132 m | 1.399 m | 1.877 / 0.17 m/s |
| B:track_001 | C | C | correct | 131 | 0.317 / 0.379 m | 1.881 m | 2.333 / 0.447 m/s |
| B:track_002 | A | A | correct | 131 | 0.154 / 0.161 m | 1.151 m | 1.679 / 0.197 m/s |
| C:track_001 | A | A | correct | 48 | 0.464 / 0.538 m | 1.884 m | 8.239 / 0.178 m/s |
| C:track_002#segment_1 | B | B | correct | 31 | 0.719 / 0.34 m | 1.363 m | 12.477 / 0.93 m/s |
| C:track_002#segment_2 | U1 | A | left anonymous (true identity A) | 93 | 0.258 / 0.289 m | 2.228 m | 4.525 / 0.297 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.0 m | 0.0 m | 0.0 m | 2.05 m |
| A + B | B | A | B:track_002 | 0.0 s | 1.12 m | 0.0 m | 1.12 m | 2.138 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time -), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
