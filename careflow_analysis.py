"""Reusable analysis helpers for the CareFlow process-mining prototype.

All calculations are intended for synthetic development data unless an approved,
de-identified hospital event log is supplied through an authorized workflow.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = ["Case_ID", "Activity_Name", "Timestamp"]


def validate_event_log(event_log: pd.DataFrame) -> dict:
    """Return a concise validation summary and raise ValueError for critical issues."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(event_log.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    data = event_log.copy()
    if data[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("Required fields contain missing values.")
    if data["Case_ID"].astype(str).str.strip().eq("").any():
        raise ValueError("Case_ID contains blank values.")
    if data["Activity_Name"].astype(str).str.strip().eq("").any():
        raise ValueError("Activity_Name contains blank values.")

    data["Timestamp"] = pd.to_datetime(data["Timestamp"], errors="coerce")
    if data["Timestamp"].isna().any():
        raise ValueError("Timestamp contains invalid values.")

    duplicate_count = int(data.duplicated(REQUIRED_COLUMNS).sum())
    if duplicate_count:
        raise ValueError(f"Found {duplicate_count} duplicate event keys.")

    chronological = (
        data.assign(_ts=data["Timestamp"])
        .sort_values(["Case_ID", "_ts"])
        .groupby("Case_ID")["_ts"]
        .apply(lambda values: values.is_monotonic_increasing)
        .all()
    )
    if not chronological:
        raise ValueError("Events are not chronological within each case.")

    return {
        "passed": True,
        "case_count": int(data["Case_ID"].nunique()),
        "event_count": int(len(data)),
        "activity_type_count": int(data["Activity_Name"].nunique()),
        "duplicate_event_keys": duplicate_count,
    }


def build_transition_summary(event_log: pd.DataFrame) -> pd.DataFrame:
    """Summarize activity-to-next-activity transitions and elapsed minutes."""
    data = event_log[REQUIRED_COLUMNS].copy()
    data["Timestamp"] = pd.to_datetime(data["Timestamp"], errors="raise")
    data = data.sort_values(["Case_ID", "Timestamp"]).reset_index(drop=True)
    data["Next_Activity"] = data.groupby("Case_ID")["Activity_Name"].shift(-1)
    data["Next_Timestamp"] = data.groupby("Case_ID")["Timestamp"].shift(-1)
    data = data[data["Next_Activity"].notna()].copy()
    data["Elapsed_Minutes"] = (
        data["Next_Timestamp"] - data["Timestamp"]
    ).dt.total_seconds() / 60
    data["Transition"] = data["Activity_Name"].astype(str) + " → " + data["Next_Activity"].astype(str)

    summary = (
        data.groupby(["Activity_Name", "Next_Activity", "Transition"], as_index=False)
        .agg(
            Transition_Count=("Case_ID", "size"),
            Mean_Elapsed_Minutes=("Elapsed_Minutes", "mean"),
            Median_Elapsed_Minutes=("Elapsed_Minutes", "median"),
            P90_Elapsed_Minutes=("Elapsed_Minutes", lambda values: values.quantile(0.90)),
        )
        .sort_values(["Mean_Elapsed_Minutes", "Transition_Count"], ascending=[False, False])
        .reset_index(drop=True)
    )
    return summary


def summarize_loopbacks_by_group(
    event_log: pd.DataFrame,
    group_column: str = "Arrival_Shift",
    source_activity: str = "X-Ray",
    target_activity: str = "Triage",
) -> pd.DataFrame:
    """Calculate patient-case counts and rework rates by a case-level grouping field.

    Each case is counted once, even if its event log contains many rows.
    """
    if group_column not in event_log.columns:
        raise ValueError(f"Grouping column '{group_column}' was not found.")
    required = {"Case_ID", "Activity_Name", group_column}
    missing = sorted(required - set(event_log.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    case_rows = []
    for case_id, group in event_log.groupby("Case_ID", sort=True):
        group = group.sort_values("Timestamp") if "Timestamp" in group.columns else group
        activities = group["Activity_Name"].astype(str).tolist()
        group_values = group[group_column].dropna()
        group_value = group_values.iloc[0] if not group_values.empty else "Unknown"
        has_loopback = any(
            left == source_activity and right == target_activity
            for left, right in zip(activities[:-1], activities[1:])
        )
        case_rows.append({
            "Case_ID": case_id,
            group_column: group_value,
            "Has_XRay_Triage_Loopback": bool(has_loopback),
        })

    cases = pd.DataFrame(case_rows)
    summary = (
        cases.groupby(group_column, dropna=False, as_index=False)
        .agg(
            Patient_Cases=("Case_ID", "nunique"),
            Loopback_Cases=("Has_XRay_Triage_Loopback", "sum"),
        )
    )
    summary["Loopback_Rate_Percent"] = (
        100 * summary["Loopback_Cases"] / summary["Patient_Cases"]
    ).round(2)
    return summary.sort_values("Loopback_Rate_Percent", ascending=False).reset_index(drop=True)


def analyze_csv(input_path: str | Path, output_dir: str | Path) -> dict:
    """Load an event-log CSV, validate it, and write reusable analysis outputs."""
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    event_log = pd.read_csv(input_path)
    validation = validate_event_log(event_log)
    transitions = build_transition_summary(event_log)
    if "Arrival_Shift" in event_log.columns:
        shift_summary = summarize_loopbacks_by_group(event_log, "Arrival_Shift")
    else:
        shift_summary = pd.DataFrame(columns=[
            "Arrival_Shift", "Patient_Cases", "Loopback_Cases", "Loopback_Rate_Percent"
        ])

    transitions.to_csv(output_dir / "python_transition_summary.csv", index=False)
    shift_summary.to_csv(output_dir / "python_loopback_by_shift.csv", index=False)
    pd.DataFrame([validation]).to_csv(output_dir / "python_validation_summary.csv", index=False)

    return {
        "validation": validation,
        "transition_rows": len(transitions),
        "shift_rows": len(shift_summary),
        "transition_output": str(output_dir / "python_transition_summary.csv"),
        "shift_output": str(output_dir / "python_loopback_by_shift.csv"),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate and analyze a CareFlow event-log CSV.")
    parser.add_argument("--input", default="careflow_data/clean_event_log.csv",
                        help="Path to the event-log CSV.")
    parser.add_argument("--output-dir", default="careflow_data",
                        help="Directory for generated summary CSV files.")
    args = parser.parse_args()
    result = analyze_csv(args.input, args.output_dir)
    print("Validation:", result["validation"])
    print("Transition summary rows:", result["transition_rows"])
    print("Arrival-shift summary rows:", result["shift_rows"])
    print("Saved:", result["transition_output"])
    print("Saved:", result["shift_output"])
