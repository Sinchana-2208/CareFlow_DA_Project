"""Run a unified CareFlow patient workflow analysis."""

import argparse
from pathlib import Path

import pandas as pd

try:
    from .transition_time_analysis import load_event_log
    from .pathway_variant_analysis import (
        reconstruct_case_sequences,
        summarize_pathway_variants,
    )
    from .activity_transition_analysis import analyze_activity_transitions
except ImportError:
    from transition_time_analysis import load_event_log
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

    overview = pd.DataFrame(
        [
            {
                "metric": "valid_event_records",
                "value": len(events),
            },
            {
                "metric": "patient_cases",
                "value": events["case_id"].nunique(),
            },
            {
                "metric": "unique_activities",
                "value": events["activity"].nunique(),
            },
            {
                "metric": "unique_pathway_variants",
                "value": len(pathway_summary),
            },
            {
                "metric": "unique_activity_transitions",
                "value": len(transition_summary),
            },
        ]
    )

    return overview, pathway_summary, transition_summary


def main():
    parser = argparse.ArgumentParser(
        description="Generate a unified CareFlow workflow analysis report."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the source Excel event-log file.",
    )
    parser.add_argument(
        "--sheet",
        required=True,
        help="Excel worksheet name or zero-based index.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for generated CSV reports.",
    )

    args = parser.parse_args()

    sheet_name = args.sheet
    if isinstance(sheet_name, str) and sheet_name.isdigit():
        sheet_name = int(sheet_name)

    events = load_event_log(args.input, sheet_name=sheet_name)

    overview, pathways, transitions = build_workflow_report(events)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    overview_path = output_dir / "workflow_overview.csv"
    pathways_path = output_dir / "pathway_variants.csv"
    transitions_path = output_dir / "activity_transition_summary.csv"

    overview.to_csv(overview_path, index=False)
    pathways.to_csv(pathways_path, index=False)
    transitions.to_csv(transitions_path, index=False)

    print("\n========== CAREFLOW WORKFLOW REPORT ==========")
    print(overview.to_string(index=False))

    print("\nTop 5 pathway variants:")
    if pathways.empty:
        print("No pathway variants found.")
    else:
        print(pathways.head(5).to_string(index=False))

    print("\nTop 5 activity transitions:")
    if transitions.empty:
        print("No activity transitions found.")
    else:
        print(transitions.head(5).to_string(index=False))

    print("\nGenerated reports:")
    print(overview_path.resolve())
    print(pathways_path.resolve())
    print(transitions_path.resolve())


if __name__ == "__main__":
    main()