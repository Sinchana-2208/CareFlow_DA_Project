"""Run the initial CareFlow event-log analysis pipeline.

From the repository root, run:
    python -m src.main --input "data/raw/Sepsis_Cases_Event_Log_Cleaned_for_Visualization(1).xlsx"
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import pandas as pd

from src.data_processing import load_workbook, prepare_event_log, save_processed_event_log
from src.data_validation import validate_event_log, validate_related_sheets
from src.process_discovery import build_dfg_counts
from src.performance_metrics import calculate_case_durations, activity_frequency, case_summary_metrics
from src.bottleneck_analysis import calculate_transition_delays, summarize_transition_delays
from src.patient_journey import pathway_frequencies
from src.visualization import plot_activity_frequency, plot_case_duration_distribution


def run_pipeline(input_path: str | Path, output_dir: str | Path) -> dict:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    sheets = load_workbook(input_path)
    events = prepare_event_log(sheets["Event Log Visual"])

    quality = validate_event_log(events)
    cross_sheet_quality = validate_related_sheets(sheets)
    save_processed_event_log(events, output_dir / "processed_event_log.csv")

    dfg = build_dfg_counts(events)
    dfg.to_csv(output_dir / "directly_follows_transitions.csv", index=False)
    durations = calculate_case_durations(events)
    durations.to_csv(output_dir / "case_durations.csv", index=False)
    activity_frequency(events).to_csv(output_dir / "activity_frequency.csv", index=False)
    delays = calculate_transition_delays(events)
    delays.to_csv(output_dir / "transition_delays.csv", index=False)
    summarize_transition_delays(delays, min_observations=5).to_csv(output_dir / "transition_delay_summary.csv", index=False)
    pathway_frequencies(events, top_n=50).to_csv(output_dir / "top_pathways.csv", index=False)

    plot_activity_frequency(events, output_dir / "activity_frequency.png")
    plot_case_duration_distribution(durations, output_dir / "case_duration_distribution.png")

    summary = {
        "event_log_quality": quality,
        "related_sheet_case_coverage": cross_sheet_quality,
        "performance_metrics": case_summary_metrics(events),
        "outputs_directory": str(output_dir.resolve()),
        "notes": [
            "Elapsed case duration is first-to-last recorded event, not necessarily hospital length of stay.",
            "Transition delay is elapsed time between recorded events, not necessarily pure waiting time.",
            "Observed pathway frequency does not establish clinical appropriateness or causality.",
        ],
    }
    with open(output_dir / "analysis_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="CareFlow Process Mining starter pipeline")
    parser.add_argument("--input", required=True, help="Path to the Excel workbook")
    parser.add_argument("--output", default="reports/generated", help="Directory for generated outputs")
    args = parser.parse_args()
    summary = run_pipeline(args.input, args.output)
    print(json.dumps(summary, indent=2, default=str))
    print("\nPipeline complete. Review the generated files and quality report before interpreting results.")


if __name__ == "__main__":
    main()

