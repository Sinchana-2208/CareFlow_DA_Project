from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)


def main():
    overview = pd.read_csv(OUTPUT_DIR / "workflow_overview.csv")
    pathways = pd.read_csv(OUTPUT_DIR / "pathway_variants.csv")
    transitions = pd.read_csv(
        OUTPUT_DIR / "activity_transition_summary.csv"
    )

    # 1. Workflow overview metrics
    plt.figure(figsize=(9, 5))
    plt.bar(
        overview["metric"],
        overview["value"],
    )
    plt.title("CareFlow Workflow Overview")
    plt.ylabel("Count")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "workflow_overview.png", dpi=200)
    plt.close()

    # 2. Five most common patient pathways
    top_pathways = pathways.nlargest(5, "case_count").sort_values(
        "case_count"
    )

    plt.figure(figsize=(12, 6))
    plt.barh(
        top_pathways["variant_id"],
        top_pathways["case_count"],
    )
    plt.title("Top 5 Patient Pathway Variants")
    plt.xlabel("Number of cases")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_pathways.png", dpi=200)
    plt.close()

    # 3. Ten most frequent activity transitions
    top_transitions = transitions.nlargest(
        10, "transition_count"
    ).copy()

    top_transitions["transition"] = (
        top_transitions["from_activity"].astype(str)
        + " → "
        + top_transitions["to_activity"].astype(str)
    )

    top_transitions = top_transitions.sort_values("transition_count")

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

    print(f"Dashboard charts saved to: {CHART_DIR}")
    for chart in sorted(CHART_DIR.glob("*.png")):
        print(chart.name)


if __name__ == "__main__":
    main()