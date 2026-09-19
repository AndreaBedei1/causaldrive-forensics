# Generated results

These files are written by `cdf.evaluation.final_results` from the
artifacts of a recorded campaign. They are committed because the
artifacts themselves are not: without them the documentation would
link to tables a fresh clone does not have.

Do not edit them by hand. Regenerate with:

```bash
python -c "import sys; sys.path.insert(0,'src'); \
           from cdf.evaluation.final_results import write_final_results; \
           write_final_results('artifacts_v2')"
```

`supervisor_table.{csv,md}` is one row per run, written by
`cdf.evaluation.supervisor_table`. It is the table to read when an aggregate
looks surprising and you want to see which run produced it. Regenerate with:

```bash
python -c "import sys; sys.path.insert(0,'src'); \
           from cdf.evaluation.supervisor_table import write_supervisor_table; \
           write_supervisor_table('artifacts_v2')"
```

| File | What it holds |
|---|---|
| [`final_results.md`](final_results.md) | the campaign tables, as the documentation quotes them |
| [`final_results.csv`](final_results.csv) | the per-scenario rows, for a spreadsheet |
| [`final_results.json`](final_results.json) | everything, including the blocks the markdown summarises |
| [`supervisor_table.md`](supervisor_table.md) | one row per run, sixteen columns |
| [`supervisor_table.csv`](supervisor_table.csv) | the same, for a spreadsheet |

Campaign: `artifacts_v2`, clock protocol `independent_local_clocks`, 105 runs over 35 scenario/variant combinations.
