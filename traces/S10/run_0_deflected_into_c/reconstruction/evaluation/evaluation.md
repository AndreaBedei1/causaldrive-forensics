# Privileged evaluation - S10/run_0_deflected_into_c

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 6/6; anonymous: 0; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 208.047 | 10358.2 | g31 | yes | 0.0 s |
| A + C | 208.947 | 1880.3 | g45 | yes | 0.0 s |

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

58 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1567/1567 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | C | C | correct | 140 | 0.207 / 0.268 m | 1.738 m | 3.424 / 0.074 m/s |
| A:track_002 | B | B | correct | 119 | 0.151 / 0.231 m | 0.958 m | 2.882 / 0.281 m/s |
| B:track_001 | C | C | correct | 30 | 0.182 / 0.208 m | 1.228 m | 5.407 / 0.234 m/s |
| B:track_002 | A | A | correct | 120 | 0.26 / 0.424 m | 1.8 m | 2.951 / 0.296 m/s |
| C:track_001 | A | A | correct | 135 | 0.411 / 0.497 m | 1.831 m | 2.94 / 0.075 m/s |
| C:track_002 | B | B | correct | 136 | 0.142 / 0.209 m | 1.732 m | 4.245 / 0.461 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 1.142 m | 0.0 m | 1.142 m | 3.312 m |
| A + B | B | A | B:track_002 | 0.0 s | 1.461 m | 0.0 m | 1.461 m | 2.246 m |
| A + C | A | C | A:track_001 | 0.0 s | 0.0 m | 0.0 m | 0.0 m | 1.32 m |
| A + C | C | A | C:track_001 | 0.0 s | 0.065 m | 0.0 m | 0.065 m | 1.211 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.43 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
