"""Run activity-transition analysis on a CareFlow event-log Excel file."""

import argparse
from pathlib import Path

try:
    from .transition_time_analysis import load_event_log
    from .activity_transition_analysis import (
        analyze_activity_transitions,
        save_transition_summary,
    )
except ImportError:
    from transition_time_analysis import load_event_log
    from activity_transition_analysis import (
        analyze_activity_transitions,
        save_transition_summary,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Summarize activity transitions in a CareFlow event log."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the source Excel event-log file.",
    )
    parser.add_argument(
        "--sheet",
        default=0,
        help="Excel sheet name or zero-based sheet index (default: 0).",
    )
    parser.add_argument(
        "--output",
        default="outputs/activity_transition_summary.csv",
        help="Destination CSV path.",
    )
    args = parser.parse_args()

    sheet_name = args.sheet
    if isinstance(sheet_name, str) and sheet_name.isdigit():
        sheet_name = int(sheet_name)

    events = load_event_log(args.input, sheet_name=sheet_name)
    summary = analyze_activity_transitions(events)
    save_transition_summary(summary, args.output)

    print("\n========== ACTIVITY TRANSITION SUMMARY ==========")
    print("Valid event records:", len(events))
    print("Unique patient cases:", events["case_id"].nunique())
    print("Unique activities:", events["activity"].nunique())
    print("Unique activity transitions:", len(summary))
    print("Output file:", Path(args.output).resolve())

    if not summary.empty:
        print("\nTop 10 transitions by frequency:")
        print(summary.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
