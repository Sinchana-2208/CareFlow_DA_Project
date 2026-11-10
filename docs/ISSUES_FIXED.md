# Review of the `CareFlow_DA_Project-Alok-branch` upload — issues found and fixed

| # | Severity | Issue found | Fix |
|---|---|---|---|
| 1 | High | `README.md` described only the Week 3 update — no project overview, architecture or run instructions | Replaced with the full project README |
| 2 | High | Test suite failed (1 of 19): `test_load_event_log_rejects_invalid_timestamp` expected an old error message | Test aligned with the new validation message; week 3 script now shares the validator with `careflow_analysis.py` |
| 3 | High | `__pycache__/` and `.pyc` files were committed; no `.gitignore` | Removed; added `.gitignore` (also covers `.env`, dbt `target/`, coverage files) |
| 4 | Medium | `pyproject.toml` declared a build backend but no project metadata; `pip install .` would fail on flat-layout auto-discovery. Coverage gate (80%) could not pass: measured 43% | Added `[project]` metadata and `py-modules = []`; added 22 tests → **88% coverage**, gate passes |
| 5 | Medium | Week 3/4 scripts and `careflow_analysis.py` sat in the repo root while other scripts lived in `scripts/` | Moved all scripts to `scripts/` (pytest `pythonpath` already includes it) |
| 6 | Medium | Week 3 output schema (`From_Activity`, `Mean_Wait_Minutes`) differed from `transition_bottlenecks.csv`, notebook and dbt (`Activity_Name`, `Next_Activity`, `Mean_Elapsed_Minutes`); trace separator was ASCII `->` instead of `→` | Week 3 now reuses the shared transition logic and `→`; all outputs use one schema. "Wait" renamed to "elapsed" (gaps between events are not pure waiting time) |
| 7 | Medium | `validate_event_log` was copy-pasted in two files with different return keys and weaker checks (whitespace-padded IDs not treated as duplicates) | One refined implementation in `careflow_analysis.py` |
| 8 | Medium | Notebook had lost all markdown headings (only 14 code cells); its last cell imported `careflow_analysis` from the current directory (fails when run from repo root) and wrote stray files into `careflow_data/` | Restored the 16 documented sections, added `scripts/` to `sys.path`, outputs go to `careflow_data/python_helpers/`; notebook re-executed with 0 errors and data verified byte-identical |
| 9 | Low | `load_synthetic_to_bigquery.py`: typos ("yet no cloud client", "connect ."), a misleading "Bigquery connection successful!" message, stray whitespace | Cleaned; `--dry-run` kept and now covered by tests |
| 10 | Low | `requirements.txt` lacked `pytest` / `pytest-cov` although tests and coverage gate need them | Added |
| 11 | Low | Looker Studio chart issues (bottleneck chart blends transitions, variants axis shows counts, empty pie legend, raw KPI labels) | Added labelled `careflow_data/bi_ready/` tables and a fix table in `docs/POWERBI_LOOKER_GUIDE.md` |
| 12 | Info | Screenshot `Looker Studio report.png` sat in the repo root with a space in the file name | Moved to `docs/images/looker_studio_report.png` |

## Checked and found correct
- All 11 dbt SQL files parse as BigQuery SQL; all YAML files load; schema lists every model.
- The notebook regenerates `raw_event_log.csv`, `clean_event_log.csv`, `case_metrics.csv`, `transition_bottlenecks.csv`, `process_variants.csv` and `conformance_results.csv` byte-for-byte (deterministic seed).
- Branch improvements kept: whitespace trimming in the audit script, duplicate-event removal in PM4Py discovery, `--dry-run` in the loader, restructured dbt intermediate models.

## Not verifiable here
BigQuery load, `dbt run` / `dbt test`, and the live Looker Studio data source need your Google Cloud project and credentials.
