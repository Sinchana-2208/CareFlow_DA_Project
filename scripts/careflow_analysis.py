"""Reusable analysis helpers for the CareFlow process-mining prototype.

Validates a normalized event log, summarizes activity-to-activity transition
times, and calculates rework (loop-back) rates by cohort.

All calculations are intended for synthetic development data unless an
approved, de-identified hospital event log is supplied through an authorized
workflow.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS: list[str] = ["Case_ID", "Activity_Name", "Timestamp"]
TEXT_COLUMNS: tuple[str, ...] = ("Case_ID", "Activity_Name")

DEFAULT_SOURCE_ACTIVITY = "X-Ray"
DEFAULT_TARGET_ACTIVITY = "Triage"

TRANSITION_FILE = "python_transition_summary.csv"
LOOPBACK_FILE = "python_loopback_by_shift.csv"
VALIDATION_FILE = "python_validation_summary.csv"


# --------------------------------------------------------------------------- #
# Validation / preparation
# --------------------------------------------------------------------------- #
def _prepare_event_log(event_log: pd.DataFrame) -> pd.DataFrame:
    """Validate, clean and chronologically sort an event log.

    Returns a copy with stripped text fields, parsed timestamps and a stable
    (Case_ID, Timestamp) ordering. Raises ValueError with row-level details
    (1-based CSV row numbers, header counted as row 1) if anything is invalid.
    """
    if not isinstance(event_log, pd.DataFrame):
        raise TypeError("Event log must be a pandas DataFrame.")
    if event_log.empty:
        raise ValueError("Event log is empty. Add at least one event row.")

    missing = [c for c in REQUIRED_COLUMNS if c not in event_log.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}. "
            f"Required columns are {', '.join(REQUIRED_COLUMNS)}."
        )

    data = event_log.reset_index(drop=True).copy()
    data["_csv_row"] = data.index + 2  # header = row 1
    issues: list[str] = []

    for column in TEXT_COLUMNS:
        data[column] = data[column].astype("string").str.strip()
        blank = data[column].isna() | data[column].eq("")
        if blank.any():
            issues.append(f"'{column}' is blank or missing at CSV row(s): {_rows(data, blank)}")

    data["Timestamp"] = pd.to_datetime(data["Timestamp"], errors="coerce")
    bad_ts = data["Timestamp"].isna()
    if bad_ts.any():
        issues.append(f"'Timestamp' is missing or invalid at CSV row(s): {_rows(data, bad_ts)}")

    if issues:
        raise ValueError("Event-log validation failed. " + "; ".join(issues) + ".")

    # Duplicates are checked on the cleaned values so " Triage" == "Triage".
    duplicated = data.duplicated(REQUIRED_COLUMNS, keep="first")
    if duplicated.any():
        raise ValueError(
            f"Event log contains {int(duplicated.sum())} duplicate event row(s) with the same "
            f"Case_ID, Activity_Name and Timestamp (CSV rows: {_rows(data, duplicated)}). "
            "Remove duplicates and retry."
        )

    return (
        data.sort_values(["Case_ID", "Timestamp"], kind="stable")
        .drop(columns="_csv_row")
        .reset_index(drop=True)
    )


def _rows(data: pd.DataFrame, mask: pd.Series, limit: int = 10) -> str:
    """Format offending CSV row numbers, truncating long lists."""
    rows = data.loc[mask, "_csv_row"].tolist()
    shown = ", ".join(map(str, rows[:limit]))
    return shown + (f" ... (+{len(rows) - limit} more)" if len(rows) > limit else "")


def validate_event_log(event_log: pd.DataFrame) -> dict:
    """Validate a normalized event log and return summary counts."""
    data = _prepare_event_log(event_log)
    return {
        "passed": True,
        "case_count": int(data["Case_ID"].nunique()),
        "event_count": int(len(data)),
        "activity_type_count": int(data["Activity_Name"].nunique()),
        "duplicate_event_keys": 0,  # duplicates raise an error, so this is always 0 on success
    }


# --------------------------------------------------------------------------- #
# Analysis
# --------------------------------------------------------------------------- #
def build_transition_summary(event_log: pd.DataFrame) -> pd.DataFrame:
    """Summarize activity -> next-activity transitions and elapsed minutes.

    Elapsed time is the gap between consecutive recorded events in a case; it is
    not pure waiting or service time.
    """
    data = _prepare_event_log(event_log)[REQUIRED_COLUMNS].copy()
    by_case = data.groupby("Case_ID", sort=False)

    data["Next_Activity"] = by_case["Activity_Name"].shift(-1)
    data["Next_Timestamp"] = by_case["Timestamp"].shift(-1)
    data = data.dropna(subset=["Next_Activity"]).copy()

    data["Elapsed_Minutes"] = (data["Next_Timestamp"] - data["Timestamp"]).dt.total_seconds() / 60
    data["Transition"] = data["Activity_Name"] + " → " + data["Next_Activity"]

    return (
        data.groupby(["Activity_Name", "Next_Activity", "Transition"], as_index=False)
        .agg(
            Transition_Count=("Case_ID", "size"),
            Mean_Elapsed_Minutes=("Elapsed_Minutes", "mean"),
            Median_Elapsed_Minutes=("Elapsed_Minutes", "median"),
            P90_Elapsed_Minutes=("Elapsed_Minutes", lambda s: s.quantile(0.90)),
        )
        .round({"Mean_Elapsed_Minutes": 2, "Median_Elapsed_Minutes": 2, "P90_Elapsed_Minutes": 2})
        .sort_values(["Mean_Elapsed_Minutes", "Transition_Count"], ascending=False)
        .reset_index(drop=True)
    )


def summarize_loopbacks_by_group(
    event_log: pd.DataFrame,
    group_column: str = "Arrival_Shift",
    source_activity: str = DEFAULT_SOURCE_ACTIVITY,
    target_activity: str = DEFAULT_TARGET_ACTIVITY,
) -> pd.DataFrame:
    """Count cases and loop-back rate (source -> target directly) per cohort.

    Each case is counted once. The cohort value is the first non-null value of
    `group_column` within the case; cases with none are labelled "Unknown".
    """
    if group_column not in event_log.columns:
        raise ValueError(f"Grouping column '{group_column}' was not found.")

    data = _prepare_event_log(event_log)  # keeps extra columns such as the cohort field

    next_activity = data.groupby("Case_ID", sort=False)["Activity_Name"].shift(-1)
    data["_loop"] = (data["Activity_Name"] == source_activity) & (next_activity == target_activity)

    cases = data.groupby("Case_ID", sort=True).agg(
        **{
            group_column: (group_column, lambda s: s.dropna().iloc[0] if s.notna().any() else "Unknown"),
            "Has_Loopback": ("_loop", "any"),
        }
    )

    summary = cases.groupby(group_column, as_index=False).agg(
        Patient_Cases=("Has_Loopback", "size"),
        Loopback_Cases=("Has_Loopback", "sum"),
    )
    summary["Loopback_Rate_Percent"] = (100 * summary["Loopback_Cases"] / summary["Patient_Cases"]).round(2)
    return summary.sort_values("Loopback_Rate_Percent", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# I/O
# --------------------------------------------------------------------------- #
def analyze_csv(input_path: str | Path, output_dir: str | Path) -> dict:
    """Load an event-log CSV, validate it, and write analysis outputs."""
    input_path, output_dir = Path(input_path), Path(output_dir)
    if not input_path.is_file():
        raise FileNotFoundError(f"Event-log CSV not found: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    event_log = pd.read_csv(input_path)
    validation = validate_event_log(event_log)
    transitions = build_transition_summary(event_log)

    if "Arrival_Shift" in event_log.columns:
        shifts = summarize_loopbacks_by_group(event_log, "Arrival_Shift")
    else:
        shifts = pd.DataFrame(columns=["Arrival_Shift", "Patient_Cases", "Loopback_Cases", "Loopback_Rate_Percent"])

    paths = {
        "transition_output": output_dir / TRANSITION_FILE,
        "shift_output": output_dir / LOOPBACK_FILE,
        "validation_output": output_dir / VALIDATION_FILE,
    }
    transitions.to_csv(paths["transition_output"], index=False)
    shifts.to_csv(paths["shift_output"], index=False)
    pd.DataFrame([validation]).to_csv(paths["validation_output"], index=False)

    return {
        "validation": validation,
        "transition_rows": len(transitions),
        "shift_rows": len(shifts),
        **{k: str(v) for k, v in paths.items()},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and analyze a CareFlow event-log CSV.")
    parser.add_argument("--input", default="careflow_data/clean_event_log.csv", help="Path to the event-log CSV.")
    parser.add_argument("--output-dir", default="careflow_data", help="Directory for generated summary CSV files.")
    args = parser.parse_args(argv)

    try:
        result = analyze_csv(args.input, args.output_dir)
    except (FileNotFoundError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Validation:", result["validation"])
    print("Transition summary rows:", result["transition_rows"])
    print("Arrival-shift summary rows:", result["shift_rows"])
    for key in ("transition_output", "shift_output", "validation_output"):
        print("Saved:", result[key])
    return 0


if __name__ == "__main__":
    sys.exit(main())
