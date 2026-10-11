# Privileged evaluation - S18/run_0_passing

This compares the finished reconstruction with `ground_truth/` (simulator state). The reconstruction never read it and was not changed by this evaluation.

**collision reconstructed: yes (1/1 vehicle contacts); associations correct: 2/2; anonymous: 9; max |t_global error| 0.0 s**

Privileged assumption: recorder raw clocks are CARLA simulator time.

## Collisions

| True contact | Sim time | Peak impulse | Reconstructed as | Participants correct | Report timing error |
|--------------|---------:|-------------:|------------------|----------------------|--------------------:|
| A + B | 519.118 | 1092.4 | g31 | yes | 0.0 s |

Reconstructed COLLISION nodes that reproduce no true contact: none.

## Graph alignment accuracy

Local time at which each graph reads t_global = 0, against the true local time of the reference contact; the chain lists the matched collisions that aligned the graph.

| Graph | Status | Chain | Estimated (local) | True (local) | Error |
|-------|--------|-------|------------------:|-------------:|------:|
| A | ALIGNED | collision_001 | 6.2 | 6.2 | 0.0 s |
| B | ALIGNED | collision_001 | 6.2 | 6.2 | 0.0 s |

Relative clock offset B - A: estimated +0.000 s, true +0.000 s (error +0.000 s).

## Global event times

49 timed global nodes; max |t_global - true global time| = 0.0 s; event order agrees with the truth for 1108/1108 pairs.

## Anonymous tracks: identity and trajectory

| Track | Decision | True identity | Verdict | Samples | Position RMSE to surface: raw / smoothed | Smoothed RMSE to centre | Speed RMSE: raw differences / smoothed |
|-------|----------|---------------|---------|--------:|------------------------------------------|------------------------:|----------------------------------------|
| A:track_001#segment_1 | U1 | D | correctly left anonymous | 20 | 0.304 / 0.394 m | 1.885 m | 0.957 / 0.131 m/s |
| A:track_001#segment_2 | U3 | D | correctly left anonymous | 23 | 1.489 / 1.335 m | 2.896 m | 4.109 / 0.438 m/s |
| A:track_001#segment_3 | U2 | C | correctly left anonymous | 54 | 0.54 / 0.577 m | 1.819 m | 4.146 / 0.084 m/s |
| A:track_002 | B | B | correct | 115 | 0.244 / 0.244 m | 1.674 m | 0.838 / 0.534 m/s |
| A:track_003 | U2 | C | correctly left anonymous | 34 | 0.268 / 0.277 m | 2.123 m | 0.541 / 0.016 m/s |
| A:track_004 | U1 | D | correctly left anonymous | 49 | 0.505 / 0.569 m | 1.687 m | 4.751 / 0.117 m/s |
| B:track_001 | A | A | correct | 115 | 0.118 / 0.244 m | 1.495 m | 1.599 / 0.372 m/s |
| B:track_002 | U2 | C | correctly left anonymous | 82 | 0.535 / 0.569 m | 1.849 m | 2.571 / 0.057 m/s |
| B:track_003 | U1 | D | correctly left anonymous | 51 | 0.437 / 0.631 m | 1.619 m | 4.701 / 0.113 m/s |
| B:track_004 | U2 | C | correctly left anonymous | 13 | 0.16 / 0.293 m | 1.471 m | 6.06 / 0.112 m/s |
| B:track_005 | U1 | D | correctly left anonymous | 17 | 0.508 / 0.64 m | 1.606 m | 4.818 / 0.145 m/s |

## Clearance at the true contacts

Per recorder, its track lying on the partner at the last 10 Hz sample at or before the contact: clearance (free distance from the recorder's footprint to the track's near surface), the true gap between the two vehicles' boxes at that instant, and the raw range from the radar.

| Contact | Recorder | Partner | Track | Seen before contact | Clearance | True gap | Error | Range |
|---------|----------|---------|-------|--------------------:|----------:|---------:|------:|------:|
| A + B | A | B | A:track_002 | 0.0 s | 0.179 m | 0.0 m | 0.179 m | 0.303 m |
| A + B | B | A | B:track_001 | 0.0 s | 0.529 m | 0.0 m | 0.529 m | 0.606 m |

Surface distance = distance from a track point to the outline of the true vehicle's bounding box, i.e. where radar returns lie. Raw = median radar return of that sweep; smoothed = Kalman + RTS estimate; both on the same measured 10 Hz sweeps. Raw returns lie on the surface by construction, so smoothing cannot be expected to bring the position closer to it; its gain shows in the speed (raw differences of consecutive returns vs smoothed velocity). The distance to the centre includes the surface-to-centre offset. True identity = the vehicle whose box is closest (median <= 1.5 m).

## Clock-shift check (uses no ground truth)

Recorder B was rebuilt with its local clock reading +0.73 s later (its collision is then at local time 6.93 s), and alignment and fusion were rerun. Global graph identical: **yes**. B's offset_to_global changed by -0.73 s (expected -0.73 s).
