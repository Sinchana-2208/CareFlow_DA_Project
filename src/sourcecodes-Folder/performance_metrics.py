"""Descriptive performance measures for recorded cases and activities."""
from __future__ import annotations
import pandas as pd


def calculate_case_durations(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate elapsed time between first and last recorded event per case."""
    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data = data.dropna(subset=["case_id", "timestamp"])
    result = data.groupby("case_id")["timestamp"].agg(start_timestamp="min", end_timestamp="max").reset_index()
    result["duration_hours"] = (result["end_timestamp"] - result["start_timestamp"]).dt.total_seconds() / 3600
    result["duration_days"] = result["duration_hours"] / 24
    return result


def activity_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """Count recorded events by activity."""
    return (df["activity"].value_counts(dropna=False).rename_axis("activity").reset_index(name="event_count"))


def case_summary_metrics(df: pd.DataFrame) -> dict:
    """Summarize event counts and observed case-duration distribution."""
    durations = calculate_case_durations(df)
    return {
        "events": int(len(df)),
        "cases_with_valid_timestamps": int(durations["case_id"].nunique()),
        "mean_duration_hours": float(durations["duration_hours"].mean()) if len(durations) else None,
        "median_duration_hours": float(durations["duration_hours"].median()) if len(durations) else None,
        "p90_duration_hours": float(durations["duration_hours"].quantile(0.90)) if len(durations) else None,
        "max_duration_hours": float(durations["duration_hours"].max()) if len(durations) else None,
    }
