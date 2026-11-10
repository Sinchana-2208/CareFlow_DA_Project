#!/usr/bin/env bash
# Reproduce every local artifact end-to-end (synthetic data). Run from the repository root.
set -euo pipefail
python scripts/audit_event_log.py
python scripts/run_pm4py_discovery.py
python scripts/week3_bottleneck_metrics.py
python scripts/week4_conformance.py
python scripts/run_pm4py_conformance.py
python scripts/export_bi_datasets.py
python scripts/build_dashboard.py
python scripts/load_synthetic_to_bigquery.py --dry-run     # validates the BigQuery load without any cloud access
python -m pytest --cov=scripts -q                           # coverage gate (80%) is set in pyproject.toml
