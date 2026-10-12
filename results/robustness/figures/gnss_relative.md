# Fusion quality vs measured relative pose error

Injected input pose: run-level 2-D RMS error; fusion median per run; measured conditions and seeds only. Refined runs use the same injected input errors.
Conditional sensitivity bound, not a universal GNSS specification. Common translation can preserve identity while degrading absolute fusion accuracy.

Empirical zero-identity-error prefix: 0.05 m RMS (conditions above).

| relative RMS upper [m] | jobs | wrong links + false merges | fully aligned |
|--:|--:|--:|--:|
| 0.05 | 109 | 0 | 1.000 |
| 0.1 | 250 | 165 | 0.992 |
| 0.25 | 257 | 165 | 0.992 |
| 0.5 | 275 | 165 | 0.993 |
| 1.0 | 365 | 246 | 0.986 |
| 2.0 | 530 | 424 | 0.962 |
| 3.0 | 666 | 528 | 0.938 |
| 5.0 | 776 | 694 | 0.921 |
| 10.0 | 935 | 898 | 0.916 |
| 20.0 | 1071 | 1097 | 0.909 |
