#!/usr/bin/env python3
"""Load the project's synthetic event log into a BigQuery raw table.

This script deliberately refuses data not explicitly marked synthetic. For real EHR
exports, create a separate reviewed ingestion path with approved security controls.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

import pandas as pd

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "careflow_data" / "raw_event_log.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=os.getenv("GCP_PROJECT_ID"), help="Google Cloud project ID (or GCP_PROJECT_ID env var)")
    parser.add_argument("--dataset", default="careflow_raw", help="Existing/new BigQuery dataset to receive demo data")
    parser.add_argument("--table", default="raw_event_log", help="Destination table (the script replaces this demo table)")
    parser.add_argument("--location", default=os.getenv("BIGQUERY_LOCATION", "US"), help="BigQuery dataset location")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Path to raw_event_log.csv")
    parser.add_argument("--dry-run", action="store_true", help="Validate input without uploading to BigQuery")
    args = parser.parse_args()

    if not args.project and not args.dry_run:
        parser.error("Set GCP_PROJECT_ID or pass --project YOUR_PROJECT_ID (or use --dry-run).")

    csv_path = Path(args.csv)
    if not csv_path.is_file():
        parser.error(f"CSV file not found: {csv_path}")

    preview = pd.read_csv(csv_path)
    required = {"Case_ID", "Activity_Name", "Timestamp"}
    missing = sorted(required - set(preview.columns))
    if missing:
        parser.error(f"Missing required columns: {', '.join(missing)}")
    parsed_timestamps = pd.to_datetime(preview["Timestamp"], errors="coerce")
    if parsed_timestamps.isna().any():
        parser.error(f"Refusing upload: {int(parsed_timestamps.isna().sum())} invalid timestamp(s).")
    if "Is_Synthetic" not in preview.columns:
        parser.error("Refusing upload: Is_Synthetic column is missing.")
    synthetic = preview["Is_Synthetic"].astype(str).str.strip().str.lower()
    if len(preview) == 0 or not synthetic.isin(["true", "1", "yes"]).all():
        parser.error("Refusing upload: every row must be explicitly marked Is_Synthetic=True.")

    print(f"Validated {len(preview):,} synthetic events for {args.dataset}.{args.table}.")
    if args.dry_run:
        print("Dry run complete: no cloud client created and no data uploaded.")
        return 0

    try:
        from google.cloud import bigquery
    except ImportError:
        print("Missing BigQuery client. Install requirements-cloud.txt first.", file=sys.stderr)
        return 2

    client = bigquery.Client(project=args.project)
    dataset_id = f"{args.project}.{args.dataset}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = args.location
    client.create_dataset(dataset, exists_ok=True)

    destination = f"{args.project}.{args.dataset}.{args.table}"
    schema = [
        bigquery.SchemaField("Case_ID", "STRING"),
        bigquery.SchemaField("Activity_Name", "STRING"),
        bigquery.SchemaField("Timestamp", "DATETIME"),
        bigquery.SchemaField("Department", "STRING"),
        bigquery.SchemaField("Resource_ID", "STRING"),
        bigquery.SchemaField("Age_Band", "STRING"),
        bigquery.SchemaField("Arrival_Shift", "STRING"),
        bigquery.SchemaField("Rework_Expected", "BOOL"),
        bigquery.SchemaField("Return_Reason", "STRING"),
        bigquery.SchemaField("Is_Synthetic", "BOOL"),
    ]
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        allow_quoted_newlines=True,
    )

    print(f"Loading {len(preview):,} synthetic events into {destination}")
    print("Write mode: WRITE_TRUNCATE (replaces this destination demo table).")
    with csv_path.open("rb") as source_file:
        job = client.load_table_from_file(source_file, destination, job_config=job_config)
    job.result()
    table = client.get_table(destination)
    print(f"Load complete: {table.num_rows:,} rows in {destination}; location={table.location}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
