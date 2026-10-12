**T9_pose.**  Injected absolute and pairwise relative pose error vs fusion quality, same frozen analysis.

| family | level | seeds | absolute RMS [m] | relative RMS [m] | fusion median [m] | wrong links | false merges | missed links | aligned |
|---|---|---|---|---|---|---|---|---|---|
| baseline | none | 1 | 0.000 | 0.000 | 0.402 | 0.0 | 0.0 | 1.0 | 1.000 |
| gnss | rtk | 3 | 0.023 | 0.029 | 0.434 | 0.0 | 0.0 | 1.0 | 1.000 |
| gnss | consumer | 8 | 2.265 | 2.703 | 2.835 | 0.6 | 19.9 | 3.5 | 0.890 |
| gnss | degraded | 8 | 7.175 | 9.641 | 6.961 | 2.1 | 22.5 | 5.5 | 0.860 |
| gnss_refined | rtk | 3 | 0.023 | 0.029 | 0.434 | 0.0 | 0.0 | 1.0 | 1.000 |
| gnss_refined | consumer | 8 | 2.265 | 2.703 | 1.944 | 0.6 | 6.0 | 3.4 | 0.890 |
| gnss_refined | degraded | 8 | 7.175 | 9.641 | 5.854 | 1.8 | 23.6 | 5.0 | 0.860 |
| gnss_correlated | consumer common 0.5 | 8 | 2.075 | 1.914 | 2.390 | 0.4 | 18.2 | 4.4 | 0.868 |
| gnss_correlated | consumer common 0.9 | 8 | 1.808 | 0.863 | 2.495 | 0.1 | 20.6 | 3.6 | 0.934 |
| gnss_correlated | consumer common 1.0 | 8 | 1.706 | 0.083 | 2.485 | 0.0 | 20.6 | 2.5 | 0.985 |

Pose and fusion errors: median per run, then mean over seeds. Counts: campaign total per draw, averaged over seeds. Refined conditions share the same injected input error.
