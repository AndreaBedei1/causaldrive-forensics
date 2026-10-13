# Privileged evaluation - S19/run_0_collision_ambiguity

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 17; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 576.528 | 1897.7 | g33 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |
| B | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

73 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 2487/2487 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001 | U1 | D | correctly left anonymous | 93 | 0.271 / 0.349 m | 2.031 m | 2.036 / 0.259 m/s |
| A:track_002 | U2 | E | correctly left anonymous | 59 | 0.148 / 0.211 m | 1.774 m | 1.19 / 0.657 m/s |
| A:track_003 | U3 | H | correctly left anonymous | 34 | 0.506 / 0.563 m | 1.544 m | 3.265 / 0.026 m/s |
| A:track_004 | U4 | F | correctly left anonymous | 55 | 0.145 / 0.225 m | 1.691 m | 1.099 / 0.571 m/s |
| A:track_005#segment_1 | U8 | B | left anonymous (true identity B) | 13 | 0.737 / 0.502 m | 2.086 m | 3.081 / 0.578 m/s |
| A:track_005#segment_2 | B | B | correct | 106 | 0.18 / 0.24 m | 2.263 m | 1.416 / 0.352 m/s |
| A:track_006 | U7 | C | correctly left anonymous | 87 | 0.267 / 0.355 m | 2.091 m | 1.363 / 0.18 m/s |
| A:track_007 | U6 | G | correctly left anonymous | 8 | 0.083 / 0.074 m | 2.183 m | 0.497 / 0.032 m/s |
| A:track_008 | B | B | correct | 8 | 0.399 / 0.993 m | 1.403 m | 4.717 / 0.335 m/s |
| A:track_009 | U3 | H | correctly left anonymous | 6 | 0.234 / 0.262 m | 1.693 m | 3.862 / 0.013 m/s |
| A:track_010 | U9 | E | correctly left anonymous | 19 | 0.116 / 0.484 m | 1.445 m | 4.065 / 2.059 m/s |
| A:track_011 | U10 | F | correctly left anonymous | 19 | 0.098 / 0.456 m | 1.334 m | 4.316 / 1.83 m/s |
| B:track_001 | U5 | H | correctly left anonymous | 85 | 0.641 / 0.606 m | 1.206 m | 6.413 / 0.182 m/s |
| B:track_002 | U6 | G | correctly left anonymous | 120 | 0.181 / 0.169 m | 2.1 m | 1.144 / 0.066 m/s |
| B:track_003 | U3 | H | correctly left anonymous | 96 | 0.374 / 0.359 m | 1.758 m | 1.839 / 0.082 m/s |
| B:track_004 | U7 | C | correctly left anonymous | 120 | 0.148 / 0.211 m | 1.483 m | 1.665 / 0.294 m/s |
| B:track_005 | U1 | D | correctly left anonymous | 120 | 0.177 / 0.232 m | 1.442 m | 1.67 / 0.68 m/s |
| B:track_006 | U11 | E | correctly left anonymous | 26 | 0.144 / 0.43 m | 1.638 m | 3.536 / 1.808 m/s |
| B:track_007 | U12 | F | correctly left anonymous | 25 | 0.138 / 0.4 m | 1.514 m | 3.595 / 1.713 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_005#segment_2 | -0.05 s | 0.0 m | 0.0 m | 0.0 m | 0.34 m |
| A + B | B | A | - | - s | - m | - m | - m | - m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
