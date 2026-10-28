from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(filename):
    """Load a CSV report and provide a helpful error if it is missing."""
    path = OUTPUT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Required report not found: {path}\n"
            "Run src.run_workflow_report first."
        )

    return pd.read_csv(path)


def find_metric(overview, keywords, default=0):
    """Find a metric in the workflow overview using its name."""
    metric_names = overview["metric"].astype(str).str.lower()

    for keyword in keywords:
        matches = overview.loc[
            metric_names.str.contains(keyword, regex=False),
            "value",
        ]

        if not matches.empty:
            try:
                return int(float(matches.iloc[0]))
            except (ValueError, TypeError):
                continue

    return default


def save_kpi_dashboard(
    total_cases,
    total_events,
    pathway_variants,
    activity_transitions,
    long_intervals,
):
    """Create a dashboard-style image with workflow KPI cards."""
    kpis = [
        ("PATIENT CASES", f"{total_cases:,}"),
        ("EVENT RECORDS", f"{total_events:,}"),
        ("PATHWAY VARIANTS", f"{pathway_variants:,}"),
        ("ACTIVITY TRANSITIONS", f"{activity_transitions:,}"),
        ("LONG INTERVALS (24H+)", f"{long_intervals:,}"),
    ]

    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    fig.suptitle(
        "CareFlow Intelligence",
        fontsize=23,
        fontweight="bold",
        y=0.96,
    )

    ax.text(
        5,
        3.35,
        "Healthcare Workflow Performance Overview",
        ha="center",
        fontsize=13,
    )

    positions = [
        (0.25, 1.65, 1.8, 1.25),
        (2.2, 1.65, 1.8, 1.25),
        (4.15, 1.65, 1.8, 1.25),
        (6.1, 1.65, 1.8, 1.25),
        (8.05, 1.65, 1.7, 1.25),
    ]

    for (label, value), (x, y, width, height) in zip(
        kpis, positions
    ):
        ax.add_patch(
            plt.Rectangle(
                (x, y),
                width,
                height,
                linewidth=1.2,
                edgecolor="gray",
                facecolor="white",
            )
        )

        ax.text(
            x + width / 2,
            y + height * 0.68,
            value,
            ha="center",
            va="center",
            fontsize=19,
            fontweight="bold",
        )

        ax.text(
            x + width / 2,
            y + height * 0.28,
            label,
            ha="center",
            va="center",
            fontsize=8,
            wrap=True,
        )

    ax.text(
        5,
        0.85,
        "Long intervals are investigation signals, not proof of bottlenecks.",
        ha="center",
        fontsize=10,
        style="italic",
    )

    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(
        CHART_DIR / "dashboard_kpis.png",
        dpi=200,
        bbox_inches="tight",
    )
    plt.close(fig)


def main():
    overview = load_csv("workflow_overview.csv")
    pathways = load_csv("pathway_variants.csv")
    transitions = load_csv("activity_transition_summary.csv")

    # Read the long-interval report if it exists.
    long_interval_file = OUTPUT_DIR / "long_interval_investigation.csv"

    if long_interval_file.exists():
        long_intervals_df = pd.read_csv(long_interval_file)
        long_interval_count = len(long_intervals_df)
    else:
        long_interval_count = 0
        print(
            "Note: Long-interval report not found. "
            "Run the workflow report to generate it."
        )

    # Derive metrics from the generated reports.
    total_cases = int(pathways["case_count"].sum())
    pathway_variant_count = len(pathways)
    activity_transition_count = len(transitions)

    total_events = find_metric(
        overview,
        ["event records", "total events", "event count", "records"],
    )

    # 1. KPI dashboard
    save_kpi_dashboard(
        total_cases=total_cases,
        total_events=total_events,
        pathway_variants=pathway_variant_count,
        activity_transitions=activity_transition_count,
        long_intervals=long_interval_count,
    )

    # 2. Workflow overview metrics
    plt.figure(figsize=(10, 5.5))
    plt.bar(
        overview["metric"].astype(str),
        pd.to_numeric(overview["value"], errors="coerce"),
    )
    plt.title("CareFlow Workflow Overview")
    plt.ylabel("Count")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "workflow_overview.png", dpi=200)
    plt.close()

    # 3. Five most common patient pathways
    top_pathways = pathways.nlargest(
        5, "case_count"
    ).sort_values("case_count")

    plt.figure(figsize=(12, 6))
    plt.barh(
        top_pathways["variant_id"].astype(str),
        top_pathways["case_count"],
    )
    plt.title("Top 5 Patient Pathway Variants")
    plt.xlabel("Number of cases")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_pathways.png", dpi=200)
    plt.close()

    # 4. Ten most frequent activity transitions
    top_transitions = transitions.nlargest(
        10, "transition_count"
    ).copy()

    top_transitions["transition"] = (
        top_transitions["from_activity"].astype(str)
        + " → "
        + top_transitions["to_activity"].astype(str)
    )

    top_transitions = top_transitions.sort_values(
        "transition_count"
    )

    plt.figure(figsize=(12, 7))
    plt.barh(
        top_transitions["transition"],
        top_transitions["transition_count"],
    )
    plt.title("Top 10 Activity Transitions")
    plt.xlabel("Transition count")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_transitions.png", dpi=200)
    plt.close()

    print("\nCareFlow Intelligence dashboard generated!")
    print(f"Patient cases: {total_cases:,}")
    print(f"Event records: {total_events:,}")
    print(f"Pathway variants: {pathway_variant_count:,}")
    print(f"Activity transitions: {activity_transition_count:,}")
    print(f"Long intervals for investigation: {long_interval_count:,}")
    print(f"\nCharts saved to: {CHART_DIR}")

    for chart in sorted(CHART_DIR.glob("*.png")):
        print(f" - {chart.name}")


if __name__ == "__main__":
    main()