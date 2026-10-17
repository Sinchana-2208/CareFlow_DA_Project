"""
CareFlow Intelligence
Patient Transition-Time and Case-Duration Analysis

Purpose:
1. Calculate elapsed time between consecutive activities.
2. Summarize elapsed time for observed activity transitions.
3. Calculate recorded journey durations for each case.
4. Flag long elapsed intervals for further investigation.

Important:
Elapsed time between recorded events is not necessarily waiting time.
Long intervals are diagnostic signals, not proof of a process bottleneck.
"""

import argparse
from pathlib import Path

import pandas as pd


def load_event_log(file_path, sheet_name):
    """Load and validate the required event-log fields."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}\n"
            "Please check the dataset path."
        )

    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Support both raw and processed event-log column names.
    column_options = {
        "case_id": ["case_id", "case:concept:name"],
        "activity": ["activity", "concept:name"],
        "timestamp": ["timestamp", "time:timestamp"],
    }

    rename_columns = {}
    for standard_name, alternatives in column_options.items():
        matching_column = next(
            (column for column in alternatives if column in df.columns),
            None,
        )
        if matching_column is None:
            raise ValueError(
                f"Required field '{standard_name}' was not found. "
                f"Available columns: {list(df.columns)}"
            )
        rename_columns[matching_column] = standard_name

    df = df.rename(columns=rename_columns)

    # Keep only fields needed for this analysis.
    columns_to_keep = ["case_id", "activity", "timestamp"]
    if "event_index" in df.columns:
        columns_to_keep.append("event_index")
    df = df[columns_to_keep].copy()

    # Normalize text fields and parse timestamps.
    df["case_id"] = df["case_id"].astype("string").str.strip()
    df["activity"] = df["activity"].astype("string").str.strip()
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce", utc=True
    )

    # Exclude only rows that cannot support this event-log analysis.
    valid_rows = (
        df["case_id"].notna()
        & df["case_id"].ne("").fillna(False)
        & df["activity"].notna()
        & df["activity"].ne("").fillna(False)
        & df["timestamp"].notna()
    )
    excluded_rows = int((~valid_rows).sum())
    df = df.loc[valid_rows].copy()

    if df.empty:
        raise ValueError(
            "No valid event records remain after validating case IDs, "
            "activities, and timestamps."
        )

    # Sort events chronologically within each case. event_index breaks ties.
    sort_columns = ["case_id", "timestamp"]
    if "event_index" in df.columns:
        df["event_index"] = pd.to_numeric(df["event_index"], errors="coerce")
        sort_columns.append("event_index")

    df = df.sort_values(sort_columns, kind="mergesort").reset_index(drop=True)

    print("\n========== DATASET PROFILE ==========")
    print("Valid event records:", len(df))
    print("Excluded records:", excluded_rows)
    print("Unique patient cases:", df["case_id"].nunique())
    print("Unique activities:", df["activity"].nunique())

    return df


def calculate_transition_times(df):
    """Calculate elapsed minutes between consecutive events in each case."""
    df = df.copy()
    grouped = df.groupby("case_id", sort=False)

    df["previous_activity"] = grouped["activity"].shift(1)
    df["previous_timestamp"] = grouped["timestamp"].shift(1)
    df["elapsed_minutes"] = (
        df["timestamp"] - df["previous_timestamp"]
    ).dt.total_seconds() / 60

    # The first event in each case has no preceding event.
    transitions = df.loc[df["previous_activity"].notna()].copy()
    transitions["transition"] = (
        transitions["previous_activity"] + " -> " + transitions["activity"]
    )
    return transitions


def summarize_transitions(transitions):
    """Summarize elapsed time for each observed activity transition."""
    if transitions.empty:
        print("\nNo consecutive transitions were found.")
        return

    summary = (
        transitions.groupby(
            ["previous_activity", "activity"], as_index=False
        )
        .agg(
            observations=("elapsed_minutes", "count"),
            mean_minutes=("elapsed_minutes", "mean"),
            median_minutes=("elapsed_minutes", "median"),
            p90_minutes=(
                "elapsed_minutes",
                lambda values: values.quantile(0.90),
            ),
        )
        .sort_values(
            ["median_minutes", "observations"],
            ascending=[False, False],
        )
    )

    numeric_columns = ["mean_minutes", "median_minutes", "p90_minutes"]
    summary[numeric_columns] = summary[numeric_columns].round(2)

    print("\n========== TRANSITION-TIME ANALYSIS ==========")
    print("Transitions ranked by median elapsed time:")
    print(summary.head(15).to_string(index=False))


def summarize_case_durations(df):
    """Calculate elapsed time from each case's first to last recorded event."""
    case_summary = (
        df.groupby("case_id")
        .agg(
            first_event=("timestamp", "min"),
            last_event=("timestamp", "max"),
            event_count=("activity", "count"),
        )
    )

    case_summary["duration_hours"] = (
        case_summary["last_event"] - case_summary["first_event"]
    ).dt.total_seconds() / 3600

    print("\n========== CASE-DURATION ANALYSIS ==========")
    print("Number of cases:", len(case_summary))
    print("Total recorded events:", int(case_summary["event_count"].sum()))
    print("\nRecorded journey duration in hours:")
    print(
        case_summary["duration_hours"]
        .describe(percentiles=[0.50, 0.90])
        .round(2)
        .to_string()
    )


def investigate_long_gaps(transitions, threshold_hours=24):
    """Summarize long elapsed intervals for further investigation."""
    if threshold_hours < 0:
        raise ValueError("threshold_hours must be zero or greater.")

    if transitions.empty:
        print("\nNo transitions are available for long-gap analysis.")
        return

    # Use a copy so the input transition data is not changed.
    diagnostic = transitions.copy()
    diagnostic["elapsed_hours"] = diagnostic["elapsed_minutes"] / 60

    # Exclude missing or negative elapsed intervals from this diagnostic.
    valid_intervals = (
        diagnostic["elapsed_hours"].notna()
        & (diagnostic["elapsed_hours"] >= 0)
    )
    diagnostic = diagnostic.loc[valid_intervals].copy()

    if diagnostic.empty:
        print("\nNo valid elapsed intervals are available.")
        return

    long_gaps = diagnostic.loc[
        diagnostic["elapsed_hours"] >= threshold_hours
    ].copy()

    total_transitions = len(diagnostic)
    total_long_gaps = len(long_gaps)
    percentage = total_long_gaps / total_transitions * 100

    print("\n========== LONG-GAP DIAGNOSTICS ==========")
    print("Diagnostic threshold:", threshold_hours, "hours")
    print("Valid transitions:", total_transitions)
    print("Transitions meeting threshold:", total_long_gaps)
    print("Percentage of long gaps:", round(percentage, 2), "%")

    if long_gaps.empty:
        print("\nNo transitions met the selected threshold.")
        return

    # These are exploratory categories, not clinical standards.
    long_gaps["gap_category"] = long_gaps["elapsed_hours"].apply(
        lambda hours: "1 to less than 7 days" if hours < 168 else "7 days or more"
    )

    print("\n========== LONG-GAP DURATION GROUPS ==========")
    gap_distribution = (
        long_gaps["gap_category"]
        .value_counts()
        .rename_axis("gap_category")
        .reset_index(name="transition_count")
    )
    print(gap_distribution.to_string(index=False))

    transition_summary = (
        long_gaps.groupby("transition", as_index=False)
        .agg(
            long_gap_count=("elapsed_hours", "size"),
            median_gap_hours=("elapsed_hours", "median"),
            p90_gap_hours=(
                "elapsed_hours",
                lambda values: values.quantile(0.90),
            ),
            maximum_gap_hours=("elapsed_hours", "max"),
        )
        .sort_values(
            ["long_gap_count", "median_gap_hours"],
            ascending=[False, False],
        )
    )

    numeric_columns = [
        "median_gap_hours",
        "p90_gap_hours",
        "maximum_gap_hours",
    ]
    transition_summary[numeric_columns] = transition_summary[numeric_columns].round(2)

    print("\n========== TRANSITIONS WITH LONG GAPS ==========")
    print(transition_summary.head(15).to_string(index=False))

    # Show timestamps and transition labels, not case identifiers.
    longest_intervals = (
        long_gaps.sort_values("elapsed_hours", ascending=False)[
            ["transition", "previous_timestamp", "timestamp", "elapsed_hours"]
        ]
        .head(10)
        .copy()
    )
    longest_intervals["elapsed_hours"] = longest_intervals["elapsed_hours"].round(2)

    print("\n========== 10 LONGEST OBSERVED INTERVALS ==========")
    print(longest_intervals.to_string(index=False))
    print(
        "\nInterpretation: Long intervals require investigation; "
        "they are not automatically proven bottlenecks."
    )


def main():
    """Run the CareFlow transition and case-duration analysis."""
    parser = argparse.ArgumentParser(
        description="Analyze CareFlow patient event times."
    )
    parser.add_argument(
        "--file",
        default=(
            "data/processed/"
            "Sepsis_Cases_Event_Log_Cleaned_for_Visualization.xlsx"
        ),
        help="Path to the approved event-log workbook.",
    )
    parser.add_argument(
        "--sheet",
        default="Event Log Visual",
        help="Worksheet containing the event log.",
    )

    args = parser.parse_args()

    event_log = load_event_log(args.file, args.sheet)
    transitions = calculate_transition_times(event_log)

    print("\nConsecutive transitions:", len(transitions))

    # New feature: investigate unusually long elapsed intervals.
    investigate_long_gaps(transitions, threshold_hours=24)

    # Existing analyses.
    summarize_transitions(transitions)
    summarize_case_durations(event_log)

    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()
