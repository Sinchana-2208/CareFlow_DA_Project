"""
CareFlow Intelligence
Patient Pathway Variant Analysis

Purpose:
1. Reconstruct recorded activity sequences for each case.
2. Identify unique pathway variants.
3. Calculate the case count and percentage for each variant.
4. Export aggregated pathway results for further visualization.

Note:
Observed pathways describe recorded events. They do not, by themselves,
establish clinical correctness, quality of care, or process inefficiency.
"""

import argparse
from pathlib import Path

import pandas as pd

try:
    # Supports importing this module from the project package.
    from .transition_time_analysis import load_event_log
except ImportError:
    # Supports running this file directly from the command line.
    from transition_time_analysis import load_event_log


def reconstruct_case_sequences(events):
    """Reconstruct one chronological activity sequence per case."""
    required_columns = {"case_id", "activity", "timestamp"}
    missing_columns = required_columns.difference(events.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df = events.copy()

    df["case_id"] = df["case_id"].astype("string").str.strip()
    df["activity"] = df["activity"].astype("string").str.strip()
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce", utc=True
    )

    valid_rows = (
        df["case_id"].notna()
        & df["case_id"].ne("").fillna(False)
        & df["activity"].notna()
        & df["activity"].ne("").fillna(False)
        & df["timestamp"].notna()
    )
    df = df.loc[valid_rows].copy()

    result_columns = ["case_id", "pathway_variant", "activity_count"]

    if df.empty:
        return pd.DataFrame(columns=result_columns)

    # Use event_index to break timestamp ties when it is available.
    sort_columns = ["case_id", "timestamp"]

    if "event_index" in df.columns:
        df["event_index"] = pd.to_numeric(
            df["event_index"], errors="coerce"
        )
        sort_columns.append("event_index")

    df = df.sort_values(
        sort_columns, kind="mergesort"
    ).reset_index(drop=True)

    case_sequences = (
        df.groupby("case_id", sort=True)
        .agg(
            pathway_variant=(
                "activity",
                lambda activities: " -> ".join(activities.tolist()),
            ),
            activity_count=("activity", "size"),
        )
        .reset_index()
    )

    return case_sequences[result_columns]


def summarize_pathway_variants(case_sequences):
    """Count pathway variants and calculate their percentage of cases."""
    result_columns = [
        "variant_id",
        "pathway_variant",
        "case_count",
        "percentage_of_cases",
        "activity_count",
    ]

    if case_sequences.empty:
        return pd.DataFrame(columns=result_columns)

    required_columns = {
        "case_id",
        "pathway_variant",
        "activity_count",
    }
    missing_columns = required_columns.difference(case_sequences.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    total_cases = len(case_sequences)

    summary = (
        case_sequences.groupby("pathway_variant", as_index=False)
        .agg(
            case_count=("case_id", "size"),
            activity_count=("activity_count", "first"),
        )
        .sort_values(
            ["case_count", "pathway_variant"],
            ascending=[False, True],
            kind="mergesort",
        )
        .reset_index(drop=True)
    )

    summary["percentage_of_cases"] = (
        summary["case_count"] / total_cases * 100
    ).round(2)

    summary.insert(
        0,
        "variant_id",
        [f"PV{number:03d}" for number in range(1, len(summary) + 1)],
    )

    # Export only aggregated pathway results, not individual case IDs.
    return summary[result_columns]


def main():
    parser = argparse.ArgumentParser(
        description="Analyze observed patient pathway variants."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the Excel event-log file.",
    )
    parser.add_argument(
        "--sheet",
        required=True,
        help="Excel worksheet containing the event log.",
    )
    parser.add_argument(
        "--output",
        default="outputs/pathway_variants.csv",
        help="CSV output path (default: outputs/pathway_variants.csv).",
    )

    args = parser.parse_args()

    events = load_event_log(args.file, args.sheet)

    case_sequences = reconstruct_case_sequences(events)
    variants = summarize_pathway_variants(case_sequences)

    if variants.empty:
        raise ValueError("No valid pathway variants were found.")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    variants.to_csv(output_path, index=False)

    print("\n========== PATHWAY VARIANT ANALYSIS ==========")
    print("Cases analyzed:", len(case_sequences))
    print("Unique pathway variants:", len(variants))
    print("\nTop 10 most common pathway variants:")
    print(variants.head(10).to_string(index=False))
    print("\nAggregated results saved to:", output_path.resolve())


if __name__ == "__main__":
    main()
