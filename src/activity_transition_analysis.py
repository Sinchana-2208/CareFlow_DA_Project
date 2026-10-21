"""Analyze activity-to-activity transitions in a patient event log."""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"case_id", "activity", "timestamp"}


def analyze_activity_transitions(
    event_log: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize transition frequency and elapsed time between activities.

    Each row in the input represents one recorded event. Events are sorted
    by case ID and timestamp before consecutive activities are paired.

    Returns an empty DataFrame with the expected columns when no transitions
    can be calculated.
    """
    output_columns = [
        "from_activity",
        "to_activity",
        "transition_count",
        "transition_percentage",
        "average_elapsed_minutes",
        "median_elapsed_minutes",
    ]

    missing_columns = REQUIRED_COLUMNS - set(event_log.columns)
    if missing_columns:
        raise ValueError(
            f"Event log is missing required columns: {sorted(missing_columns)}"
        )

    if event_log.empty:
        return pd.DataFrame(columns=output_columns)

    events = event_log.copy()
    events["timestamp"] = pd.to_datetime(events["timestamp"], errors="raise")

    if events[["case_id", "activity", "timestamp"]].isna().any().any():
        raise ValueError(
            "case_id, activity, and timestamp must not contain missing values."
        )

    events = events.sort_values(
        ["case_id", "timestamp"], kind="mergesort"
    ).copy()

    grouped = events.groupby("case_id", sort=False)
    events["to_activity"] = grouped["activity"].shift(-1)
    events["next_timestamp"] = grouped["timestamp"].shift(-1)

    transitions = events.loc[events["to_activity"].notna()].copy()

    if transitions.empty:
        return pd.DataFrame(columns=output_columns)

    transitions["elapsed_minutes"] = (
        transitions["next_timestamp"] - transitions["timestamp"]
    ).dt.total_seconds() / 60

    transitions = transitions.rename(columns={"activity": "from_activity"})

    summary = (
        transitions.groupby(
            ["from_activity", "to_activity"], as_index=False, sort=False
        )
        .agg(
            transition_count=("elapsed_minutes", "size"),
            average_elapsed_minutes=("elapsed_minutes", "mean"),
            median_elapsed_minutes=("elapsed_minutes", "median"),
        )
    )

    total_transitions = int(summary["transition_count"].sum())
    summary["transition_percentage"] = (
        summary["transition_count"] / total_transitions * 100
    )

    summary = summary[output_columns].sort_values(
        ["transition_count", "from_activity", "to_activity"],
        ascending=[False, True, True],
        kind="mergesort",
    ).reset_index(drop=True)

    return summary


def save_transition_summary(
    summary: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """Save a transition summary to a CSV file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(path, index=False)


if __name__ == "__main__":
    print(
        "Import analyze_activity_transitions() and pass it an event-log "
        "DataFrame containing case_id, activity, and timestamp columns."
    )
