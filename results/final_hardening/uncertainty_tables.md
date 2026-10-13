# Effective gates of the uncertainty-normalised tracker (model only, no ground truth)

`scripts/uncertainty_tables.py`.  Radar: range sigma 0.25 m, azimuth sigma 0.5 deg; Doppler sigma 0.3 m/s; process noise 6.0 m/s^2 along the track, plus (v x 0.3 rad/s)^2 across it; 99 % gates (2-D: 3.03 sigma, 1-D: 2.58 sigma).  Steady state after 2 s of 20 Hz sweeps with 8 returns on a 1.6 m face; target speed 10 m/s for the position table.  Values in metres (position) and m/s (Doppler); along / across = along / across the line of sight.

## Position

| geometry | range [m] | radar 1-sigma along / across | track point: innovation 1-sigma along / across | track point: 99 % gate along / across | single return: 99 % gate along / across | after 0.5 s without data: track point gate along / across |
|---|--:|---|---|---|---|---|
| front | 5 | 0.25 / 0.20 | 0.57 / 0.59 | 1.72 / 1.79 | 5.76 / 2.54 | 1.95 / 2.70 |
| front | 10 | 0.25 / 0.25 | 0.57 / 0.61 | 1.72 / 1.84 | 5.76 / 2.58 | 1.95 / 2.74 |
| front | 20 | 0.25 / 0.33 | 0.57 / 0.65 | 1.72 / 1.98 | 5.76 / 2.67 | 1.95 / 2.85 |
| front | 40 | 0.25 / 0.51 | 0.57 / 0.77 | 1.72 / 2.33 | 5.76 / 2.94 | 1.95 / 3.17 |
| front | 60 | 0.25 / 0.68 | 0.57 / 0.91 | 1.72 / 2.75 | 5.76 / 3.28 | 1.95 / 3.56 |
| front | 80 | 0.25 / 0.86 | 0.57 / 1.06 | 1.72 / 3.21 | 5.76 / 3.68 | 1.95 / 4.01 |
| crossing | 5 | 0.25 / 0.04 | 0.58 / 0.54 | 1.75 / 1.65 | 2.51 / 5.74 | 2.02 / 2.42 |
| crossing | 10 | 0.25 / 0.09 | 0.57 / 0.56 | 1.74 / 1.69 | 2.50 / 5.75 | 2.01 / 2.50 |
| crossing | 20 | 0.25 / 0.17 | 0.57 / 0.58 | 1.73 / 1.77 | 2.50 / 5.77 | 2.00 / 2.59 |
| crossing | 40 | 0.25 / 0.35 | 0.57 / 0.67 | 1.73 / 2.03 | 2.49 / 5.85 | 2.00 / 2.84 |
| crossing | 60 | 0.25 / 0.52 | 0.57 / 0.79 | 1.73 / 2.39 | 2.49 / 5.99 | 2.00 / 3.18 |
| crossing | 80 | 0.25 / 0.70 | 0.57 / 0.93 | 1.72 / 2.82 | 2.49 / 6.17 | 2.00 / 3.59 |

## Doppler (radial residual along the return's line of sight)

| geometry | relative speed | radial speed measured | track velocity 1-sigma along LOS | residual 1-sigma | 99 % gate half-width | tangential velocity 1-sigma (not tested by Doppler) |
|---|---|--:|--:|--:|--:|--:|
| front | low (2 m/s) | 2.0 | 0.24 | 0.38 | 0.98 | 0.85 |
| front | medium (10 m/s) | 10.0 | 0.24 | 0.38 | 0.98 | 0.92 |
| front | high (25 m/s) | 25.0 | 0.24 | 0.38 | 0.98 | 1.19 |
| crossing | low (2 m/s) | 0.0 | 0.24 | 0.38 | 0.98 | 0.84 |
| crossing | medium (10 m/s) | 0.0 | 0.24 | 0.39 | 0.99 | 0.84 |
| crossing | high (25 m/s) | 0.0 | 0.26 | 0.40 | 1.03 | 0.83 |

Fixed gates of METHODS 1-3 for comparison: 2.5 m (any range, any direction) and 4.0 m/s.
