# Interrupted held-out campaign (NOT final results)

Stopped on request on 2026-10-13, before the algorithm is complete and before S19-S24 are reviewed manually.  These job lines were produced by the frozen commit `c410bca` (detached worktree `CarlaGraph_heldout`, 14 workers) and are kept for the record only: they are **not** the final results and will be superseded by the definitive campaign.

| batch | planned | completed | failed | running when stopped (estimated) | not started |
|---|--:|--:|--:|--:|--:|
| _heldout_all23 | 2392 | 1784 | 0 | 14 | 594 |
| _heldout_collision | 800 | 26 | 0 | 14 | 760 |
| _heldout_s10_s18_extra | 416 | 0 | 0 | 0 | 416 |
| _s06_seed0_3 | 24 | 0 | 0 | 0 | 24 |

Job commits recorded in provenance: `c410bca` (dirty=False), `None` (dirty=None).  59 job lines record git_commit None: the git query timed out under load; their code_sha256 (dddede30...) is identical to the 1751 lines recorded at c410bca, so they ran the same code.

Running jobs are estimated as the first not-completed jobs in submission order (the pool starts jobs in that order; a stopped worker writes no line).  Their lists, and the partial copies they left (held-out worktree `robustness/retrospective/`, 78 MB, kept, never evaluated) are recorded in `INTERRUPTION_LOG.json`.  The batches `_heldout_s10_s18_extra` and `_s06_seed0_3` never started.
