# Sensitivity of METHOD 3 FINAL (development seed 200)

All 23 runs (17 canonical + S19-S24), conditions exact and consumer GNSS, seed 200, code `e2cd1c5` (the algorithm as frozen; later commits change no reconstruction behaviour).  Nominal: K = 20, new-target density 3.57e-5 /m^2, minimum posterior 0.95; one parameter moved at a time.  Evaluation only (ground truth read after the reconstruction).  The nominal values were declared before this study and are NOT changed by it.

| parameter | level | condition | wrong links | missed links | false merges | missed merges | collisions lost | wrong collision pairs | correct | wrong | unresolved |
|---|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| all | nominal | consumer | 0 | 13 | 0 | 111 | 0 | 0 | 0.8001 | 0.0055 | 0.1944 |
| all | nominal | exact | 0 | 4 | 0 | 74 | 0 | 0 | 0.9399 | 0.0055 | 0.0546 |
| K | low 5 | consumer | 0 | 13 | 0 | 111 | 0 | 0 | 0.8001 | 0.0055 | 0.1944 |
| K | low 5 | exact | 0 | 4 | 0 | 74 | 0 | 0 | 0.9399 | 0.0055 | 0.0546 |
| K | high 100 | consumer | 0 | 13 | 0 | 111 | 0 | 0 | 0.8001 | 0.0055 | 0.1944 |
| K | high 100 | exact | 0 | 4 | 0 | 74 | 0 | 0 | 0.9399 | 0.0055 | 0.0546 |
| density | low 3.57e-6 | consumer | 0 | 13 | 0 | 108 | 0 | 0 | 0.8041 | 0.0055 | 0.1903 |
| density | low 3.57e-6 | exact | 0 | 4 | 0 | 62 | 0 | 0 | 0.9541 | 0.0055 | 0.0404 |
| density | high 3.57e-4 | consumer | 0 | 13 | 0 | 120 | 0 | 0 | 0.7926 | 0.0055 | 0.2019 |
| density | high 3.57e-4 | exact | 0 | 4 | 0 | 92 | 0 | 0 | 0.9295 | 0.0055 | 0.0650 |
| posterior | low 0.90 | consumer | 0 | 13 | 0 | 111 | 0 | 0 | 0.8001 | 0.0055 | 0.1944 |
| posterior | low 0.90 | exact | 0 | 4 | 0 | 68 | 0 | 0 | 0.9473 | 0.0055 | 0.0472 |
| posterior | high 0.99 | consumer | 0 | 13 | 0 | 116 | 0 | 0 | 0.7973 | 0.0055 | 0.1972 |
| posterior | high 0.99 | exact | 0 | 4 | 0 | 85 | 0 | 0 | 0.9344 | 0.0055 | 0.0601 |

## Reading

* **K (assignment likelihood ratio) 5-100: no change at all.**  On these runs no competing assignment falls between a ratio of 5 and 100: every decision is either clear or left to the other rules (discriminability, CANNOT_LINK).
* **New-target density and minimum posterior act on missed merges only**, monotonically: a more permissive setting (density 3.57e-6, posterior 0.90) merges more true re-acquisitions, a stricter one fewer.  The wrong-sample rate, wrong links (0), false merges (0) and the collision results (0 lost, 0 wrong pairs) are identical at every level.
* The permissive levels look better on this seed; they are not adopted: the parameters were fixed before the study (posterior 0.95 = the declared decision risk; density from the campaign's road-user density), and one development seed cannot show the false-merge cost of a looser stitch.
