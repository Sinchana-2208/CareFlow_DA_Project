"""Run a unified CareFlow patient workflow analysis."""

import argparse
from pathlib import Path

import pandas as pd

try:
    from .transition_time_analysis import (
        load_event_log,
        calculate_transition_times,
    )
    from .pathway_variant_analysis import (
        reconstruct_case_sequences,
        summarize_pathway_variants,
    )
    from .activity_transition_analysis import analyze_activity_transitions
except ImportError:
    from transition_time_analysis import (
        load_event_log,
        calculate_transition_times,
    )
    from pathway_variant_analysis import (
        reconstruct_case_sequences,
        summarize_pathway_variants,
    )
    from activity_transition_analysis import analyze_activity_transitions


def build_workflow_report(events):
    """Build pathway, transition, and dataset overview summaries."""

    required_columns = {"case_id", "activity", "timestamp"}
    missing_columns = required_columns.difference(events.columns)

    if missing_columns:
        raise ValueError(
            f"Event log is missing required columns: {sorted(missing_columns)}"
        )

    if events.empty:
        raise ValueError("Cannot analyze an empty event log.")

    case_sequences = reconstruct_case_sequences(events)
    pathway_summary = summarize_pathway_variants(case_sequences)
    transition_summary = analyze_activity_transitions(events)

    timed_transitions = calculate_transition_times(events)
    timed_transitions["elapsed_hours"] = (
        timed_transitions["elapsed_minutes"] / 60
    )

    timed_transitions = timed_transitions.loc[
        timed_transitions["elapsed_hours"].notna()
        & (timed_transitions["elapsed_hours"] >= 0)
    ].copy()

    overview = pd.DataFrame(
        [
            {"metric": "valid_event_records", "value": len(events)},
            {"metric": "patient_cases", "value": events["case_id"].nunique()},
            {"metric": "unique_activities", "value": events["activity"].nunique()},
            {"metric": "unique_pathway_variants", "value": len(pathway_summary)},
            {"metric": "unique_activity_transitions", "value": len(transition_summary)},
        ]
    )

    return overview, pathway_summary, transition_summary, timed_transitions


def main():
    parser = argparse.ArgumentParser(
        description="Generate a unified CareFlow workflow analysis report."
    )
    parser.add_argument("--input", required=True, help="Source Excel event log.")
    parser.add_argument(
        "--sheet", required=True, help="Worksheet name or zero-based index."
    )
    parser.add_argument(
        "--output-dir", default="outputs", help="Directory for generated reports."
    )
    parser.add_argument(
        "--long-gap-hours",
        type=float,
        default=24,
        help="Threshold in hours for the long-interval investigation report.",
    )

    args = parser.parse_args()

    if args.long_gap_hours < 0:
        parser.error("--long-gap-hours must be zero or greater.")

    sheet_name = int(args.sheet) if args.sheet.isdigit() else args.sheet
    events = load_event_log(args.input, sheet_name=sheet_name)

    overview, pathways, transitions, timed_transitions = build_workflow_report(
        events
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    overview_path = output_dir / "workflow_overview.csv"
    pathways_path = output_dir / "pathway_variants.csv"
    transitions_path = output_dir / "activity_transition_summary.csv"
    timing_path = output_dir / "transition_time_summary.csv"
    long_gaps_path = output_dir / "long_interval_investigation.csv"

    overview.to_csv(overview_path, index=False)
    pathways.to_csv(pathways_path, index=False)
    transitions.to_csv(transitions_path, index=False)

    if timed_transitions.empty:
        timing_summary = pd.DataFrame(
            columns=[
                "previous_activity",
                "activity",
                "observations",
                "mean_minutes",
                "median_minutes",
                "p90_minutes",
            ]
        )
    else:
        timing_summary = (
            timed_transitions.groupby(
                ["previous_activity", "activity"], as_index=False
            )
            .agg(
                observations=("elapsed_minutes", "count"),
                mean_minutes=("elapsed_minutes", "mean"),
                median_minutes=("elapsed_minutes", "median"),
                p90_minutes=("elapsed_minutes", lambda x: x.quantile(0.90)),
            )
            .sort_values("median_minutes", ascending=False)
        )

    timing_summary[
        ["mean_minutes", "median_minutes", "p90_minutes"]
    ] = timing_summary[
        ["mean_minutes", "median_minutes", "p90_minutes"]
    ].round(2)

    timing_summary.to_csv(timing_path, index=False)

    long_gaps = timed_transitions.loc[
        timed_transitions["elapsed_hours"] >= args.long_gap_hours
    ].copy()

    long_gaps = long_gaps[
        [
            "transition",
            "previous_timestamp",
            "timestamp",
            "elapsed_minutes",
            "elapsed_hours",
        ]
    ].sort_values("elapsed_hours", ascending=False)

    long_gaps.to_csv(long_gaps_path, index=False)

    print("\n========== CAREFLOW WORKFLOW REPORT ==========")
    print(overview.to_string(index=False))

    print("\nTop 5 pathway variants:")
    print(pathways.head(5).to_string(index=False) if not pathways.empty else "None")

    print("\nTop 5 activity transitions:")
    print(
        transitions.head(5).to_string(index=False)
        if not transitions.empty else "None"
    )

    print("\nTop 10 transitions by median elapsed time:")
    print(timing_summary.head(10).to_string(index=False))

    print(
        f"\nIntervals of {args.long_gap_hours:g} hours or more: "
        f"{len(long_gaps)}"
    )
    print(
        "Note: Long recorded intervals are investigation signals, "
        "not proof of operational or clinical bottlenecks."
    )

    print("\nGenerated reports:")
    for path in [
        overview_path,
        pathways_path,
        transitions_path,
        timing_path,
        long_gaps_path,
    ]:
        print(path.resolve())


if __name__ == "__main__":
    main()
