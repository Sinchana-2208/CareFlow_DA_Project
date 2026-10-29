from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "outputs"
DASHBOARD_FILE = OUTPUT_DIR / "careflow_interactive_dashboard.html"


def load_csv(filename):
    path = OUTPUT_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Report not found: {path}\n"
            "Run the workflow report first."
        )
    return pd.read_csv(path)


def get_metric(overview, name, default=0):
    rows = overview.loc[
        overview["metric"].astype(str).str.lower() == name.lower(),
        "value",
    ]
    if rows.empty:
        return default
    return float(rows.iloc[0])


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    overview = load_csv("workflow_overview.csv")
    pathways = load_csv("pathway_variants.csv")
    transitions = load_csv("activity_transition_summary.csv")
    timing = load_csv("transition_time_summary.csv")

    long_file = OUTPUT_DIR / "long_interval_investigation.csv"
    long_count = len(pd.read_csv(long_file)) if long_file.exists() else 0

    total_events = int(get_metric(overview, "valid_event_records"))
    total_cases = int(get_metric(overview, "patient_cases"))
    activities = int(get_metric(overview, "unique_activities"))
    variants = len(pathways)
    transition_count = len(transitions)

    fig = make_subplots(
        rows=4,
        cols=2,
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"type": "xy"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "xy"}],
        ],
        subplot_titles=(
            "Patient Cases",
            "Event Records",
            "Pathway Variants",
            "Activity Transitions",
            "Top Patient Pathways",
            "Most Frequent Activity Transitions",
            "Workflow Overview",
            "Transition Timing Comparison",
        ),
        vertical_spacing=0.12,
        horizontal_spacing=0.12,
    )

    kpis = [
        (1, 1, total_cases),
        (1, 2, total_events),
        (2, 1, variants),
        (2, 2, transition_count),
    ]

    for row, col, value in kpis:
        fig.add_trace(
            go.Indicator(
                mode="number",
                value=value,
                number={"valueformat": ",.0f"},
            ),
            row=row,
            col=col,
        )

    # Top patient pathways.
    top_pathways = pathways.nlargest(10, "case_count")
    top_pathways = top_pathways.sort_values("case_count")

    fig.add_trace(
        go.Bar(
            x=top_pathways["case_count"],
            y=top_pathways["variant_id"].astype(str),
            orientation="h",
            customdata=top_pathways[
                ["pathway_variant", "percentage_of_cases"]
            ].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Cases: %{x}<br>"
                "Pathway: %{customdata[0]}<br>"
                "Share of cases: %{customdata[1]:.2f}%"
                "<extra></extra>"
            ),
            name="Patient cases",
        ),
        row=3,
        col=1,
    )

    # Most frequent activity transitions.
    top_transitions = transitions.nlargest(10, "transition_count").copy()
    top_transitions["transition"] = (
        top_transitions["from_activity"].astype(str)
        + " → "
        + top_transitions["to_activity"].astype(str)
    )
    top_transitions = top_transitions.sort_values("transition_count")

    fig.add_trace(
        go.Bar(
            x=top_transitions["transition_count"],
            y=top_transitions["transition"],
            orientation="h",
            customdata=top_transitions[
                ["average_elapsed_minutes", "median_elapsed_minutes"]
            ].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Occurrences: %{x}<br>"
                "Average elapsed: %{customdata[0]:,.2f} minutes<br>"
                "Median elapsed: %{customdata[1]:,.2f} minutes"
                "<extra></extra>"
            ),
            name="Transition count",
        ),
        row=3,
        col=2,
    )

    # Workflow overview metrics.
    overview_plot = overview.copy()
    overview_plot["value"] = pd.to_numeric(
        overview_plot["value"], errors="coerce"
    )
    overview_plot = overview_plot.dropna(subset=["value"])

    fig.add_trace(
        go.Bar(
            x=overview_plot["metric"],
            y=overview_plot["value"],
            name="Workflow metrics",
            hovertemplate="%{x}<br>Value: %{y:,.0f}<extra></extra>",
        ),
        row=4,
        col=1,
    )

    # Compare mean and median transition timing.
    timing_plot = timing.copy()
    for column in ("mean_minutes", "median_minutes", "observations"):
        timing_plot[column] = pd.to_numeric(
            timing_plot[column], errors="coerce"
        )

    timing_plot = timing_plot.dropna(
        subset=["mean_minutes", "median_minutes"]
    )
    timing_plot["transition"] = (
        timing_plot["previous_activity"].astype(str)
        + " → "
        + timing_plot["activity"].astype(str)
    )
    timing_plot = timing_plot.nlargest(10, "observations")

    if not timing_plot.empty:
        fig.add_trace(
            go.Bar(
                x=timing_plot["transition"],
                y=timing_plot["mean_minutes"],
                name="Mean minutes",
                hovertemplate="%{x}<br>Mean: %{y:,.2f} min<extra></extra>",
            ),
            row=4,
            col=2,
        )

        fig.add_trace(
            go.Bar(
                x=timing_plot["transition"],
                y=timing_plot["median_minutes"],
                name="Median minutes",
                hovertemplate="%{x}<br>Median: %{y:,.2f} min<extra></extra>",
            ),
            row=4,
            col=2,
        )

    fig.update_layout(
        title={
            "text": (
                "CareFlow Intelligence"
                "<br><sup>Interactive Healthcare Workflow Overview</sup>"
            ),
            "x": 0.5,
            "xanchor": "center",
        },
        template="plotly_white",
        height=1600,
        barmode="group",
        showlegend=True,
        margin={"t": 130, "l": 80, "r": 50, "b": 180},
    )

    fig.update_xaxes(tickangle=-30, automargin=True)
    fig.update_yaxes(automargin=True)

    fig.add_annotation(
        text=(
            f"Unique activities: {activities:,} | "
            f"Intervals of 24+ hours: {long_count:,}<br>"
            "Long intervals are investigation signals, not proof of bottlenecks. "
            "Transition times may include release and return-to-ER events."
        ),
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.12,
        showarrow=False,
        align="center",
    )

    fig.write_html(
        DASHBOARD_FILE,
        include_plotlyjs=True,
        full_html=True,
    )

    print("\nInteractive dashboard generated successfully!")
    print(f"Patient cases: {total_cases:,}")
    print(f"Event records: {total_events:,}")
    print(f"Pathway variants: {variants:,}")
    print(f"Activity transitions: {transition_count:,}")
    print(f"Long intervals for investigation: {long_count:,}")
    print(f"Dashboard saved to: {DASHBOARD_FILE}")


if __name__ == "__main__":
    main()

