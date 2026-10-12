**T10_combined.**  Combined GNSS and 10% impulse noise on all 17 canonical cases.

| condition | seeds | jobs | collision recall | wrong pairings | unmatched true contacts | ambiguous candidate refusals | aligned |
|---|---|---|---|---|---|---|---|
| exact + 10% | 3 | 51 | 1.000 | 0.0 | 0.0 | 0.0 | 1.000 |
| RTK + 10% | 3 | 51 | 1.000 | 0.0 | 0.0 | 0.0 | 1.000 |
| consumer independent + 10% | 8 | 136 | 0.767 | 0.1 | 5.1 | 5.4 | 0.875 |
| consumer common 0.9 + 10% | 8 | 136 | 0.784 | 0.1 | 4.8 | 4.5 | 0.897 |

Recall and alignment are pooled per seed then averaged; counts are totals per draw averaged over seeds. Singleton unpaired callbacks are not wrong pairings.
