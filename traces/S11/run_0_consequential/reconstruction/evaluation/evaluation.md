# Privileged evaluation - S11/run_0_consequential

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (2/2 vehicle contacts); associations correct: 4/4; anonymous: 3; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 229.826 | 4243.5 | g26 | yes | 0.0 s |
| A + C | 230.876 | 322.1 | g42 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 5.55 | 5.55 | 0.0 s |
| B | ALIGNED | collision_001 | 5.55 | 5.55 | 0.0 s |
| C | ALIGNED | collision_001 -> collision_002 | 5.55 | 5.55 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

Relative clock offset C - B: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

56 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1470/1470 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | C | C | correct | 120 | 0.132 / 0.16 m | 2.788 m | 1.048 / 0.232 m/s |
| B:track_001 | A | A | correct | 72 | 0.158 / 0.251 m | 1.95 m | 1.241 / 0.361 m/s |
| B:track_002#segment_1 | C | C | correct | 56 | 0.227 / 0.268 m | 2.728 m | 2.175 / 0.141 m/s |
| B:track_002#segment_2 | U1 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_002#segment_3 | U3 | - | correctly left anonymous | - | - / - m | - m | - / - m/s |
| B:track_003 | U2 | C | left anonymous (true identity C) | 8 | 0.227 / 0.631 m | 2.351 m | 14.777 / 0.261 m/s |
| C:track_001 | A | A | correct | 34 | 0.164 / 0.177 m | 1.972 m | 0.301 / 0.245 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | - | - s | - m | - m | - m | - m |
| A + B | B | A | B:track_001 | -0.05 s | 0.0 m | 0.0 m | 0.0 m | 0.38 m |
| A + C | A | C | A:track_001 | 0.0 s | 0.035 m | 0.0 m | 0.035 m | 0.208 m |
| A + C | C | A | C:track_001 | 0.2 s | 1.248 m | 0.027 m | 1.221 m | 3.402 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder C was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 7.33 s), and alignment and fusion were rerun. Global graph identical: **yes**. C's offset_to_global changed by -0.73 s (expected -0.73 s).
