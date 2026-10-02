# Privileged evaluation - S15/run_0_deflected_into_c

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 4/4; anonymous: 2; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 208.047 | 10358.2 | g31 | yes | 0.0 s |
| A + C | 208.947 | 1880.3 | g46 | yes | 0.0 s |

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

62 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1811/1811 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | C | C | correct | 140 | 0.197 / 0.228 m | 1.845 m | 3.117 / 0.241 m/s |
| A:track_002 | B | B | correct | 119 | 0.15 / 0.271 m | 1.06 m | 2.829 / 0.683 m/s |
| B:track_001 | B:track_001 | A | left anonymous (true identity A) | 121 | 12.894 / 12.772 m | 13.925 m | 2.734 / 2.223 m/s |
| B:track_002 | A | A | correct | 36 | 0.304 / 0.466 m | 1.266 m | 5.18 / 0.956 m/s |
| C:track_001 | A | A | correct | 140 | 0.401 / 0.439 m | 1.908 m | 2.889 / 0.145 m/s |
| C:track_002 | C:track_002 | B | left anonymous (true identity B) | 134 | 0.146 / 0.207 m | 1.738 m | 4.05 / 0.509 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.564 m | 0.0 m | 0.564 m | 2.235 m |
| A + B | B | A | B:track_002 | 0.0 s | 0.336 m | 0.0 m | 0.336 m | 1.145 m |
| A + C | A | C | A:track_001 | 0.0 s | 0.0 m | 0.0 m | 0.0 m | 1.086 m |
| A + C | C | A | C:track_001 | 0.0 s | 0.063 m | 0.0 m | 0.063 m | 1.118 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 5.43 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
