#!/usr/bin/env python3
"""Week 3: bottleneck and throughput metrics as BI-ready CSV summaries.

Input must be a normalized event log with Case_ID, Activity_Name and Timestamp.
Validation and transition maths are shared with ``careflow_analysis`` so every
output (notebook, dbt marts, scripts) uses the same column names and values.
All outputs describe the supplied dataset; synthetic results are not clinical evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from careflow_analysis import REQUIRED_COLUMNS, _prepare_event_log, build_transition_summary, validate_event_log

__all__ = ["REQUIRED_COLUMNS", "validate_event_log", "load_event_log", "build_transition_metrics",
           "build_case_metrics", "build_group_metrics", "analyze_csv", "main"]

TRACE_SEPARATOR = " → "  # same separator as the notebook, dbt marts and conformance outputs


def load_event_log(path: str | Path) -> pd.DataFrame:
    """Read, validate, normalize and chronologically sort event records."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Event-log CSV not found: {path}. Check the path and try again.")
    try:
        frame = pd.read_csv(path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Event-log CSV is empty or has no header: {path}") from exc
    except (UnicodeDecodeError, pd.errors.ParserError) as exc:
        raise ValueError(f"Could not read event-log CSV '{path}': {exc}") from exc
    return _prepare_event_log(frame)


def build_transition_metrics(events: pd.DataFrame) -> pd.DataFrame:
    """Mean / median / P90 elapsed minutes between consecutive events (same schema as the dbt mart)."""
    if events.empty or events.groupby("Case_ID").size().max() < 2:
        return pd.DataFrame(columns=["Activity_Name", "Next_Activity", "Transition", "Transition_Count",
                                     "Mean_Elapsed_Minutes", "Median_Elapsed_Minutes", "P90_Elapsed_Minutes"])
    return build_transition_summary(events)


def build_case_metrics(events: pd.DataFrame) -> pd.DataFrame:
    """Case duration and X-Ray → Triage rework flag for every case."""
    records = []
    for case_id, group in events.groupby("Case_ID", sort=True):
        group = group.sort_values("Timestamp", kind="stable")
        activities = group["Activity_Name"].tolist()
        duration = (group["Timestamp"].iloc[-1] - group["Timestamp"].iloc[0]).total_seconds() / 60
        loopback = any(a == "X-Ray" and b == "Triage" for a, b in zip(activities, activities[1:]))
        records.append({
            "Case_ID": str(case_id),
            "First_Activity": activities[0],
            "Last_Activity": activities[-1],
            "Event_Count": len(activities),
            "Case_Duration_Minutes": round(duration, 2),
            "XRay_To_Triage_Loopback": bool(loopback),
            "Case_Trace": TRACE_SEPARATOR.join(activities),
        })
    return pd.DataFrame(records)


def build_group_metrics(events: pd.DataFrame, cases: pd.DataFrame, group_column: str) -> pd.DataFrame:
    """Case count, mean duration and loopback rate by an optional case-level category."""
    columns = [group_column, "Case_Count", "Mean_Duration_Minutes", "Loopback_Cases", "Loopback_Rate_Percent"]
    if group_column not in events.columns:
        return pd.DataFrame(columns=columns)
    mapping = events[["Case_ID", group_column]].drop_duplicates("Case_ID").assign(
        Case_ID=lambda d: d["Case_ID"].astype(str))
    joined = cases.merge(mapping, on="Case_ID", how="left")
    summary = joined.groupby(group_column, dropna=False, as_index=False).agg(
        Case_Count=("Case_ID", "nunique"),
        Mean_Duration_Minutes=("Case_Duration_Minutes", "mean"),
        Loopback_Cases=("XRay_To_Triage_Loopback", "sum"),
        Loopback_Rate_Percent=("XRay_To_Triage_Loopback", lambda x: 100 * x.mean()),
    )
    summary[["Mean_Duration_Minutes", "Loopback_Rate_Percent"]] = summary[
        ["Mean_Duration_Minutes", "Loopback_Rate_Percent"]].round(2)
    return summary.sort_values(group_column).reset_index(drop=True)


def analyze_csv(input_path: str | Path, output_dir: str | Path) -> dict:
    """Run Week 3 metrics; export CSVs and a compact JSON KPI summary."""
    output_dir = Path(output_dir)
    events = load_event_log(input_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    transitions = build_transition_metrics(events)
    cases = build_case_metrics(events)
    shifts = build_group_metrics(events, cases, "Arrival_Shift")
    transitions.to_csv(output_dir / "week3_transition_bottlenecks.csv", index=False)
    cases.to_csv(output_dir / "week3_case_metrics.csv", index=False)
    shifts.to_csv(output_dir / "week3_shift_metrics.csv", index=False)
    loopbacks = int(cases["XRay_To_Triage_Loopback"].sum())
    summary = {
        "case_count": int(cases["Case_ID"].nunique()),
        "event_count": int(len(events)),
        "activity_count": int(events["Activity_Name"].nunique()),
        "transition_type_count": int(len(transitions)),
        "mean_case_duration_minutes": round(float(cases["Case_Duration_Minutes"].mean()), 2),
        "median_case_duration_minutes": round(float(cases["Case_Duration_Minutes"].median()), 2),
        "xray_to_triage_loopback_cases": loopbacks,
        "xray_to_triage_loopback_rate_percent": round(100 * loopbacks / len(cases), 2),
        "data_source_note": "Metrics describe the supplied event log; synthetic data is illustrative only.",
    }
    (output_dir / "week3_kpi_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="careflow_data/clean_event_log.csv", help="Normalized event-log CSV")
    parser.add_argument("--output-dir", default="careflow_data/week3_metrics", help="Directory for Week 3 outputs")
    args = parser.parse_args()
    try:
        summary = analyze_csv(args.input, args.output_dir)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(summary, indent=2))
    print(f"Week 3 metrics exported to: {Path(args.output_dir).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
