# Privileged evaluation - S19/run_0_collision_ambiguity

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 19; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 576.528 | 1897.7 | g37 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |
| B | ALIGNED | collision_001 | 7.75 | 7.75 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

83 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 3289/3289 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001#segment_1 | U1 | D | correctly left anonymous | 8 | 0.337 / 0.504 m | 1.844 m | 2.959 / 0.184 m/s |
| A:track_001#segment_2 | U7 | D | correctly left anonymous | 80 | 0.491 / 0.38 m | 2.055 m | 2.706 / 0.465 m/s |
| A:track_002 | U2 | E | correctly left anonymous | 59 | 0.148 / 0.217 m | 1.766 m | 1.174 / 0.646 m/s |
| A:track_003 | U3 | H | correctly left anonymous | 34 | 0.503 / 0.566 m | 1.542 m | 3.258 / 0.032 m/s |
| A:track_004 | U4 | F | correctly left anonymous | 55 | 0.145 / 0.235 m | 1.688 m | 1.088 / 0.598 m/s |
| A:track_005#segment_1 | U8 | B | left anonymous (true identity B) | 9 | 0.806 / 0.534 m | 2.15 m | 2.869 / 0.776 m/s |
| A:track_005#segment_2 | B | B | correct | 69 | 0.191 / 0.238 m | 2.216 m | 1.104 / 0.47 m/s |
| A:track_005#segment_3 | U9 | B | left anonymous (true identity B) | 12 | 0.279 / 0.506 m | 1.923 m | 1.967 / 0.668 m/s |
| A:track_005#segment_4 | B | B | correct | 27 | 0.069 / 0.068 m | 2.331 m | 0.239 / 0.359 m/s |
| A:track_006 | U6 | C | correctly left anonymous | 87 | 0.284 / 0.324 m | 2.141 m | 1.351 / 0.133 m/s |
| A:track_007 | U5 | G | correctly left anonymous | 8 | 0.081 / 0.072 m | 2.186 m | 0.592 / 0.032 m/s |
| A:track_008 | U3 | H | correctly left anonymous | 7 | 0.217 / 0.259 m | 1.496 m | 11.368 / 0.036 m/s |
| A:track_009 | U10 | D | correctly left anonymous | 7 | 0.147 / 0.145 m | 2.268 m | 1.253 / 0.044 m/s |
| A:track_010 | U11 | E | correctly left anonymous | 19 | 0.124 / 0.457 m | 1.417 m | 5.877 / 1.915 m/s |
| A:track_011 | U12 | F | correctly left anonymous | 19 | 0.098 / 0.487 m | 1.246 m | 4.136 / 1.62 m/s |
| B:track_001 | U5 | G | correctly left anonymous | 120 | 0.186 / 0.174 m | 2.094 m | 1.613 / 0.069 m/s |
| B:track_002 | U6 | C | correctly left anonymous | 120 | 0.149 / 0.226 m | 1.462 m | 1.784 / 0.287 m/s |
| B:track_003 | U7 | D | correctly left anonymous | 120 | 0.184 / 0.275 m | 1.408 m | 2.31 / 0.654 m/s |
| B:track_004 | U3 | H | correctly left anonymous | 99 | 0.447 / 0.484 m | 1.645 m | 2.74 / 0.071 m/s |
| B:track_005 | U13 | E | correctly left anonymous | 26 | 0.148 / 0.435 m | 1.628 m | 3.76 / 1.814 m/s |
| B:track_006 | U14 | F | correctly left anonymous | 25 | 0.141 / 0.422 m | 1.476 m | 3.627 / 1.665 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_005#segment_2 | -0.05 s | 0.0 m | 0.0 m | 0.0 m | 1.14 m |
| A + B | B | A | - | - s | - m | - m | - m | - m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 8.48 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
