# Identity report of the dense scenarios (evaluation only)

Times t_global [s], 0 = the collision.  `entities (relevant samples)`: how many global entities carry the car's samples while it is inside an observer's relevance envelope (1 = not fragmented where it matters); `non-relevant`: the same outside it.

## S19/run_0

| physical road users seen | recorders | local tracks | global anonymous entities | single-track entities (unresolved) | tracks resolved retrospectively |
|--:|---|--:|--:|--:|--:|
| 7 | A,B | 24 | 17 | 12 | 10 |

Fragmentation inside vs outside the relevance envelope:

| car | entities (relevant samples) | entities (non-relevant samples) | relevant samples | non-relevant samples | wrong samples |
|---|--:|--:|--:|--:|--:|
| A (recorder) | 1 | 0 | 120 | 0 | 0 |
| B (recorder) | 1 | 0 | 120 | 0 | 0 |
| C | 2 | 0 | 239 | 0 | 0 |
| D | 1 | 0 | 236 | 0 | 0 |
| E | 2 | 0 | 238 | 0 | 0 |
| F | 2 | 2 | 24 | 73 | 0 |
| G | 2 | 2 | 72 | 32 | 0 |
| H | 2 | 3 | 8 | 39 | 0 |
| J | 0 | 3 | 0 | 52 | 5 |

Local tracks per car:

**A** (recorder)
- `B:track_002` -7.75 .. +4.15 s, 120 samples, 100% relevant, min range 1 m -> A

**B** (recorder)
- `A:track_003` -7.75 .. +4.15 s, 120 samples, 100% relevant, min range 0 m -> B

**C**
- `A:track_001#segment_1` -7.75 .. -7.05 s, 8 samples, 100% relevant, min range 12 m -> U1
- `B:track_004` -7.65 .. +4.15 s, 119 samples, 100% relevant, min range 10 m -> U6 (resolved from -6.55 s) RETRO
- `A:track_001#segment_2` -6.95 .. +4.15 s, 112 samples, 100% relevant, min range 11 m -> U6 (resolved from -6.55 s) RETRO

**D**
- `B:track_001` -7.75 .. +4.15 s, 120 samples, 100% relevant, min range 9 m -> U3 (resolved from -6.95 s) RETRO
- `A:track_005` -7.35 .. +4.15 s, 116 samples, 100% relevant, min range 10 m -> U3 (resolved from -6.95 s) RETRO

**E**
- `A:track_004#segment_1` -7.65 .. -6.75 s, 10 samples, 100% relevant, min range 11 m -> U5
- `B:track_005` -7.65 .. +4.15 s, 119 samples, 100% relevant, min range 10 m -> U7 (resolved from -6.25 s) RETRO
- `A:track_004#segment_2` -6.65 .. +4.15 s, 109 samples, 100% relevant, min range 10 m -> U7 (resolved from -6.25 s) RETRO

**F**
- `B:track_003` -7.75 .. -4.15 s, 35 samples, 11% relevant, min range 29 m -> U4
- `B:track_008` -1.35 .. +1.45 s, 29 samples, 59% relevant, min range 26 m -> U11 (resolved from +1.35 s) RETRO
- `A:track_009` +0.85 .. +4.15 s, 33 samples, 9% relevant, min range 27 m -> U11 (resolved from +1.35 s) RETRO

**G**
- `B:track_006` -7.55 .. -3.95 s, 37 samples, 19% relevant, min range 28 m -> U8
- `B:track_009` -1.25 .. +0.95 s, 23 samples, 100% relevant, min range 26 m -> U12 (resolved from +0.35 s) RETRO
- `A:track_008` -0.15 .. +4.15 s, 44 samples, 95% relevant, min range 25 m -> U12 (resolved from +0.35 s) RETRO

**H**
- `A:track_002#segment_1` -7.75 .. -5.85 s, 20 samples, 0% relevant, min range 42 m -> U2
- `B:track_007` -7.55 .. -5.55 s, 20 samples, 0% relevant, min range 44 m -> U9
- `A:track_002#segment_2` -5.75 .. -5.35 s, 4 samples, 0% relevant, min range 42 m -> U10
- `B:track_010` -1.15 .. -0.75 s, 5 samples, 100% relevant, min range 43 m -> U13
- `A:track_007` -1.05 .. -0.85 s, 3 samples, 100% relevant, min range 42 m -> U15

**J**
- `A:track_006` -1.05 .. -0.05 s, 11 samples, 0% relevant, min range 42 m -> U14
- `B:track_011` +0.45 .. +4.15 s, 31 samples, 0% relevant, min range 41 m -> U16
- `A:track_010` +2.25 .. +3.25 s, 10 samples, 0% relevant, min range 41 m -> U17

## S20/run_0

| physical road users seen | recorders | local tracks | global anonymous entities | single-track entities (unresolved) | tracks resolved retrospectively |
|--:|---|--:|--:|--:|--:|
| 8 | A,B | 20 | 14 | 9 | 10 |

Fragmentation inside vs outside the relevance envelope:

| car | entities (relevant samples) | entities (non-relevant samples) | relevant samples | non-relevant samples | wrong samples |
|---|--:|--:|--:|--:|--:|
| A (recorder) | 1 | 1 | 84 | 35 | 0 |
| C | 0 | 1 | 0 | 23 | 0 |
| D | 1 | 1 | 68 | 46 | 0 |
| E | 2 | 2 | 75 | 55 | 0 |
| F | 1 | 2 | 144 | 31 | 0 |
| G | 2 | 1 | 151 | 42 | 0 |
| H | 1 | 1 | 64 | 78 | 0 |
| I | 1 | 1 | 139 | 50 | 0 |
| J | 1 | 1 | 152 | 43 | 0 |

Local tracks per car:

**A** (recorder)
- `B:track_006` -7.35 .. +4.45 s, 119 samples, 71% relevant, min range 0 m -> A

**C**
- `A:track_008` +0.45 .. +2.65 s, 23 samples, 0% relevant, min range 34 m -> U10

**D**
- `A:track_002` -7.45 .. +4.35 s, 114 samples, 60% relevant, min range 7 m -> U2

**E**
- `A:track_005` -7.45 .. +1.05 s, 86 samples, 74% relevant, min range 14 m -> U5 (resolved from -6.95 s) RETRO
- `B:track_002` -7.45 .. -3.75 s, 37 samples, 19% relevant, min range 26 m -> U5 (resolved from -6.95 s) RETRO
- `B:track_008` -1.15 .. -0.75 s, 4 samples, 100% relevant, min range 26 m -> U9
- `A:track_009` +3.25 .. +3.45 s, 3 samples, 0% relevant, min range 62 m -> U12

**F**
- `A:track_001` -7.45 .. +1.95 s, 95 samples, 75% relevant, min range 3 m -> U1 (resolved from -7.00 s) RETRO
- `B:track_005` -7.45 .. -0.05 s, 73 samples, 100% relevant, min range 13 m -> U1 (resolved from -7.00 s) RETRO
- `A:track_010` +3.55 .. +4.45 s, 7 samples, 0% relevant, min range 53 m -> U13

**G**
- `A:track_006` -7.45 .. +4.45 s, 120 samples, 65% relevant, min range 1 m -> U6
- `B:track_001#segment_1` -7.45 .. +0.75 s, 83 samples, 100% relevant, min range 3 m -> U8

**H**
- `A:track_004` -7.45 .. +4.45 s, 115 samples, 54% relevant, min range 16 m -> U4 (resolved from -6.70 s) RETRO
- `B:track_007` -7.15 .. -4.25 s, 27 samples, 7% relevant, min range 28 m -> U4 (resolved from -6.70 s) RETRO

**I**
- `A:track_003` -7.45 .. +4.45 s, 120 samples, 58% relevant, min range 5 m -> U3 (resolved from -7.00 s) RETRO
- `B:track_004` -7.45 .. -0.05 s, 69 samples, 100% relevant, min range 16 m -> U3 (resolved from -7.00 s) RETRO

**J**
- `A:track_007` -7.45 .. +4.45 s, 120 samples, 64% relevant, min range 1 m -> U7 (resolved from -7.00 s) RETRO
- `B:track_003` -7.45 .. -0.05 s, 75 samples, 100% relevant, min range 4 m -> U7 (resolved from -7.00 s) RETRO

## S21/run_0

| physical road users seen | recorders | local tracks | global anonymous entities | single-track entities (unresolved) | tracks resolved retrospectively |
|--:|---|--:|--:|--:|--:|
| 7 | A,B | 21 | 14 | 10 | 7 |

Fragmentation inside vs outside the relevance envelope:

| car | entities (relevant samples) | entities (non-relevant samples) | relevant samples | non-relevant samples | wrong samples |
|---|--:|--:|--:|--:|--:|
| A (recorder) | 1 | 0 | 76 | 0 | 0 |
| B (recorder) | 1 | 0 | 116 | 0 | 0 |
| C | 0 | 1 | 0 | 16 | 0 |
| D | 1 | 1 | 71 | 90 | 0 |
| E | 4 | 2 | 84 | 30 | 0 |
| F | 1 | 1 | 150 | 87 | 0 |
| G | 2 | 2 | 34 | 74 | 0 |
| H | 1 | 1 | 149 | 68 | 0 |
| I | 1 | 3 | 5 | 51 | 16 |

Local tracks per car:

**A** (recorder)
- `B:track_001` -6.75 .. +5.15 s, 120 samples, 100% relevant, min range 0 m -> A

**B** (recorder)
- `A:track_006` -6.35 .. +5.15 s, 116 samples, 100% relevant, min range 1 m -> B

**C**
- `A:track_009` +1.35 .. +3.75 s, 16 samples, 0% relevant, min range 37 m -> U10

**D**
- `A:track_004` -6.75 .. -3.15 s, 36 samples, 100% relevant, min range 25 m -> U4 (resolved from -1.15 s) RETRO
- `A:track_007` -1.15 .. +5.15 s, 64 samples, 28% relevant, min range 19 m -> U4 (resolved from -0.60 s) RETRO
- `B:track_006` -1.05 .. +5.15 s, 61 samples, 28% relevant, min range 17 m -> U4 (resolved from -0.60 s) RETRO

**E**
- `A:track_005` -6.75 .. -6.25 s, 6 samples, 100% relevant, min range 8 m -> U5
- `B:track_003` -6.75 .. -1.55 s, 53 samples, 100% relevant, min range 5 m -> U6
- `A:track_010` +1.55 .. +5.15 s, 37 samples, 57% relevant, min range 2 m -> U11
- `B:track_009` +3.45 .. +5.15 s, 18 samples, 22% relevant, min range 4 m -> U14

**F**
- `A:track_003` -6.75 .. +5.05 s, 118 samples, 63% relevant, min range 12 m -> U3 (resolved from -6.30 s) RETRO
- `B:track_002` -6.75 .. +5.15 s, 119 samples, 64% relevant, min range 11 m -> U3 (resolved from -6.30 s) RETRO

**G**
- `B:track_005` -5.95 .. -3.65 s, 22 samples, 100% relevant, min range 33 m -> U7
- `B:track_007` -0.85 .. +4.75 s, 53 samples, 23% relevant, min range 26 m -> U8
- `A:track_008` -0.75 .. +4.95 s, 49 samples, 0% relevant, min range 28 m -> U9

**H**
- `A:track_001` -6.75 .. +4.45 s, 108 samples, 69% relevant, min range 3 m -> U1 (resolved from -6.20 s) RETRO
- `B:track_004` -6.65 .. +4.35 s, 109 samples, 69% relevant, min range 10 m -> U1 (resolved from -6.20 s) RETRO

**I**
- `A:track_002` -6.75 .. -3.15 s, 36 samples, 14% relevant, min range 16 m -> U2
- `A:track_011` +1.85 .. +2.05 s, 3 samples, 0% relevant, min range 46 m -> U12
- `B:track_008` +1.85 .. +2.95 s, 12 samples, 0% relevant, min range 44 m -> U13
- `A:track_012` +2.35 .. +2.85 s, 5 samples, 0% relevant, min range 52 m -> U12

## S22/run_0

| physical road users seen | recorders | local tracks | global anonymous entities | single-track entities (unresolved) | tracks resolved retrospectively |
|--:|---|--:|--:|--:|--:|
| 6 | A,B | 17 | 9 | 6 | 9 |

Fragmentation inside vs outside the relevance envelope:

| car | entities (relevant samples) | entities (non-relevant samples) | relevant samples | non-relevant samples | wrong samples |
|---|--:|--:|--:|--:|--:|
| A (recorder) | 1 | 0 | 90 | 0 | 0 |
| B (recorder) | 1 | 1 | 74 | 1 | 0 |
| C | 1 | 1 | 136 | 45 | 0 |
| D | 1 | 1 | 80 | 81 | 0 |
| E | 0 | 3 | 0 | 90 | 0 |
| F | 1 | 1 | 65 | 3 | 0 |
| G | 2 | 0 | 60 | 0 | 0 |
| V | 1 | 1 | 154 | 45 | 0 |

Local tracks per car:

**A** (recorder)
- `B:track_005` -4.30 .. +4.60 s, 90 samples, 100% relevant, min range 1 m -> A

**B** (recorder)
- `A:track_006` -6.40 .. +4.60 s, 111 samples, 96% relevant, min range 2 m -> B

**C**
- `B:track_001` -7.30 .. +0.70 s, 81 samples, 95% relevant, min range 13 m -> U5 (resolved from -6.70 s) RETRO
- `A:track_005` -7.10 .. -2.80 s, 44 samples, 100% relevant, min range 19 m -> U5 (resolved from -6.70 s) RETRO
- `A:track_007` -0.90 .. +4.60 s, 56 samples, 27% relevant, min range 12 m -> U5 (resolved from -0.50 s) RETRO

**D**
- `A:track_002` -7.30 .. -2.50 s, 49 samples, 100% relevant, min range 20 m -> U2 (resolved from -0.85 s) RETRO
- `B:track_002` -7.30 .. -2.30 s, 50 samples, 44% relevant, min range 12 m -> U2 (resolved from -0.85 s) RETRO
- `A:track_008` -0.80 .. +4.50 s, 54 samples, 17% relevant, min range 21 m -> U2 (resolved from +0.05 s) RETRO
- `B:track_007` -0.40 .. +0.30 s, 8 samples, 0% relevant, min range 23 m -> U2 (resolved from +0.05 s) RETRO

**E**
- `A:track_003` -7.30 .. -4.00 s, 32 samples, 0% relevant, min range 38 m -> U3
- `B:track_004` -7.00 .. -3.90 s, 31 samples, 0% relevant, min range 27 m -> U6
- `A:track_009` +1.20 .. +4.60 s, 27 samples, 0% relevant, min range 46 m -> U9

**F**
- `A:track_004` -7.30 .. -0.60 s, 68 samples, 96% relevant, min range 8 m -> U4

**G**
- `B:track_006` -2.10 .. +0.10 s, 23 samples, 100% relevant, min range 14 m -> U7
- `B:track_008` +1.00 .. +4.60 s, 37 samples, 100% relevant, min range 3 m -> U8

**V**
- `A:track_001` -7.30 .. +4.60 s, 120 samples, 65% relevant, min range 3 m -> U1 (resolved from -6.85 s) RETRO
- `B:track_003` -7.30 .. +0.50 s, 79 samples, 96% relevant, min range 1 m -> U1 (resolved from -6.85 s) RETRO

## S23/run_0

| physical road users seen | recorders | local tracks | global anonymous entities | single-track entities (unresolved) | tracks resolved retrospectively |
|--:|---|--:|--:|--:|--:|
| 5 | A,B | 24 | 11 | 5 | 17 |

Fragmentation inside vs outside the relevance envelope:

| car | entities (relevant samples) | entities (non-relevant samples) | relevant samples | non-relevant samples | wrong samples |
|---|--:|--:|--:|--:|--:|
| A (recorder) | 1 | 0 | 97 | 0 | 0 |
| B (recorder) | 1 | 0 | 120 | 0 | 0 |
| C | 4 | 1 | 108 | 48 | 0 |
| D | 4 | 1 | 81 | 50 | 2 |
| E | 1 | 1 | 170 | 4 | 0 |
| F | 1 | 0 | 87 | 0 | 0 |
| G | 1 | 0 | 35 | 0 | 0 |

Local tracks per car:

**A** (recorder)
- `B:track_002` -8.50 .. +3.40 s, 120 samples, 100% relevant, min range 0 m -> A

**B** (recorder)
- `A:track_002` -8.50 .. +3.40 s, 120 samples, 100% relevant, min range 0 m -> B

**C**
- `A:track_005#segment_1` -7.60 .. -6.30 s, 14 samples, 100% relevant, min range 50 m -> U4
- `B:track_006` -7.50 .. -5.30 s, 22 samples, 100% relevant, min range 43 m -> U5 (resolved from -5.70 s) RETRO
- `A:track_005#segment_2` -6.20 .. -4.70 s, 15 samples, 100% relevant, min range 40 m -> U5 (resolved from -5.70 s) RETRO
- `A:track_007#segment_1` -1.90 .. -1.00 s, 10 samples, 100% relevant, min range 14 m -> U9
- `B:track_010` -1.80 .. +3.40 s, 53 samples, 55% relevant, min range 4 m -> U10 (resolved from -0.50 s) RETRO
- `A:track_007#segment_2` -0.90 .. +3.40 s, 44 samples, 45% relevant, min range 3 m -> U10 (resolved from -0.50 s) RETRO

**D**
- `A:track_006` -6.90 .. -4.90 s, 18 samples, 100% relevant, min range 42 m -> U6
- `B:track_007` -6.30 .. -6.10 s, 3 samples, 100% relevant, min range 49 m -> U7
- `B:track_008` -5.90 .. -5.10 s, 6 samples, 100% relevant, min range 43 m -> U8
- `B:track_011` -1.80 .. +3.40 s, 53 samples, 51% relevant, min range 7 m -> U11 (resolved from -1.20 s) RETRO
- `A:track_008` -1.60 .. +3.40 s, 51 samples, 53% relevant, min range 7 m -> U11 (resolved from -1.20 s) RETRO

**E**
- `B:track_004` -8.00 .. -7.80 s, 3 samples, 100% relevant, min range 34 m -> U3 (resolved from +1.35 s) RETRO
- `A:track_004` -7.60 .. -0.90 s, 67 samples, 100% relevant, min range 1 m -> U3 (resolved from +1.35 s) RETRO
- `B:track_005` -7.60 .. -2.70 s, 50 samples, 100% relevant, min range 5 m -> U3 (resolved from +1.35 s) RETRO
- `B:track_012` -1.50 .. +0.70 s, 19 samples, 79% relevant, min range 8 m -> U3 (resolved from +1.35 s) RETRO
- `B:track_013` +1.40 .. +3.40 s, 21 samples, 100% relevant, min range 7 m -> U3 (resolved from +2.50 s) RETRO
- `A:track_009` +2.10 .. +3.40 s, 14 samples, 100% relevant, min range 5 m -> U3 (resolved from +2.50 s) RETRO

**F**
- `A:track_001` -8.50 .. -4.30 s, 43 samples, 100% relevant, min range 1 m -> U1 (resolved from -8.05 s) RETRO
- `B:track_001` -8.50 .. -6.20 s, 24 samples, 100% relevant, min range 6 m -> U1 (resolved from -8.05 s) RETRO
- `B:track_009` -5.00 .. -3.10 s, 20 samples, 100% relevant, min range 7 m -> U1 (resolved from -4.55 s) RETRO

**G**
- `A:track_003` -8.50 .. -7.30 s, 13 samples, 100% relevant, min range 2 m -> U2 (resolved from -7.65 s) RETRO
- `B:track_003` -8.10 .. -6.00 s, 22 samples, 100% relevant, min range 7 m -> U2 (resolved from -7.65 s) RETRO

## S24/run_0

| physical road users seen | recorders | local tracks | global anonymous entities | single-track entities (unresolved) | tracks resolved retrospectively |
|--:|---|--:|--:|--:|--:|
| 6 | A,B | 21 | 15 | 11 | 8 |

Fragmentation inside vs outside the relevance envelope:

| car | entities (relevant samples) | entities (non-relevant samples) | relevant samples | non-relevant samples | wrong samples |
|---|--:|--:|--:|--:|--:|
| B (recorder) | 3 | 0 | 116 | 0 | 3 |
| C | 1 | 1 | 175 | 32 | 1 |
| D | 3 | 2 | 180 | 32 | 0 |
| E | 3 | 2 | 88 | 16 | 0 |
| F | 3 | 2 | 84 | 15 | 0 |
| G | 1 | 1 | 87 | 41 | 0 |
| H | 2 | 2 | 117 | 23 | 0 |

Local tracks per car:

**B** (recorder)
- `A:track_005#segment_1` -7.65 .. -6.85 s, 9 samples, 100% relevant, min range 14 m -> U8
- `A:track_005#segment_2` -6.75 .. +0.05 s, 69 samples, 100% relevant, min range 0 m -> B
- `A:track_005#segment_3` +0.15 .. +1.45 s, 12 samples, 100% relevant, min range 1 m -> U10
- `A:track_005#segment_4` +1.55 .. +4.15 s, 27 samples, 100% relevant, min range 1 m -> B

**C**
- `B:track_002` -7.75 .. +4.15 s, 120 samples, 76% relevant, min range 1 m -> U6 (resolved from -6.95 s) RETRO
- `A:track_006` -7.35 .. +1.25 s, 87 samples, 97% relevant, min range 3 m -> U6 (resolved from -6.95 s) RETRO

**D**
- `A:track_001#segment_1` -7.75 .. -7.05 s, 8 samples, 100% relevant, min range 14 m -> U1
- `B:track_003` -7.75 .. +4.15 s, 120 samples, 78% relevant, min range 1 m -> U7 (resolved from -6.50 s) RETRO
- `A:track_001#segment_2` -6.95 .. +0.95 s, 80 samples, 100% relevant, min range 2 m -> U7 (resolved from -6.50 s) RETRO
- `A:track_009` +0.85 .. +1.45 s, 7 samples, 29% relevant, min range 4 m -> U11

**E**
- `A:track_002` -7.75 .. -1.95 s, 59 samples, 100% relevant, min range 1 m -> U2
- `A:track_010` +1.25 .. +3.05 s, 19 samples, 74% relevant, min range 1 m -> U12
- `B:track_005` +1.65 .. +4.15 s, 26 samples, 58% relevant, min range 1 m -> U14

**F**
- `A:track_004` -7.75 .. -2.35 s, 55 samples, 100% relevant, min range 1 m -> U4
- `A:track_011` +1.25 .. +3.05 s, 19 samples, 74% relevant, min range 1 m -> U13
- `B:track_006` +1.75 .. +4.15 s, 25 samples, 60% relevant, min range 1 m -> U15

**G**
- `B:track_001` -7.75 .. +4.15 s, 120 samples, 68% relevant, min range 13 m -> U5 (resolved from +0.40 s) RETRO
- `A:track_007` -0.05 .. +0.65 s, 8 samples, 62% relevant, min range 18 m -> U5 (resolved from +0.40 s) RETRO

**H**
- `A:track_003` -7.75 .. -4.45 s, 34 samples, 100% relevant, min range 30 m -> U3 (resolved from -7.20 s) RETRO
- `B:track_004` -7.65 .. +2.45 s, 99 samples, 80% relevant, min range 16 m -> U3 (resolved from -7.20 s) RETRO
- `A:track_008` -0.05 .. +0.55 s, 7 samples, 57% relevant, min range 21 m -> U9

