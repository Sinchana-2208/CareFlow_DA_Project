"""Exploratory analysis of elapsed time between consecutive recorded events."""
from __future__ import annotations
import pandas as pd


def calculate_transition_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Return each within-case transition and elapsed hours to next event.

    Delay is elapsed time between timestamps, not guaranteed waiting time.
    """
    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    sort_cols = ["case_id", "timestamp"] + (["event_index"] if "event_index" in data else [])
    data = data.sort_values(sort_cols, kind="stable")
    grouped = data.groupby("case_id", dropna=False)
    data["next_activity"] = grouped["activity"].shift(-1)
    data["next_timestamp"] = grouped["timestamp"].shift(-1)
    data["delay_hours"] = (data["next_timestamp"] - data["timestamp"]).dt.total_seconds() / 3600
    keep = ["case_id", "activity", "next_activity", "timestamp", "next_timestamp", "delay_hours"]
    if "event_index" in data:
        keep.insert(1, "event_index")
    return data.dropna(subset=["case_id", "activity", "next_activity", "timestamp", "next_timestamp"])[keep].rename(
        columns={"activity": "source_activity"}
    ).reset_index(drop=True)


def summarize_transition_delays(transitions: pd.DataFrame, min_observations: int = 5) -> pd.DataFrame:
    """Rank transitions by median and 90th-percentile elapsed time.

    The minimum-observation threshold reduces attention to very rare transitions;
    it does not prove a bottleneck exists.
    """
    if transitions.empty:
        return pd.DataFrame(columns=["source_activity", "next_activity", "observations", "median_delay_hours", "p90_delay_hours", "mean_delay_hours"])
    summary = transitions.groupby(["source_activity", "next_activity"])["delay_hours"].agg(
        observations="count", median_delay_hours="median", p90_delay_hours=lambda x: x.quantile(0.90), mean_delay_hours="mean"
    ).reset_index()
    summary = summary[summary["observations"] >= min_observations]
    return summary.sort_values(["median_delay_hours", "p90_delay_hours"], ascending=False).reset_index(drop=True)

