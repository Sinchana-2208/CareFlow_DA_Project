"""Reusable plots for event-log analysis."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_activity_frequency(df: pd.DataFrame, output_path: str | Path | None = None, top_n: int = 15):
    """Plot the most frequent recorded activities and optionally save the chart."""
    counts = df["activity"].value_counts().head(top_n).sort_values()
    fig, ax = plt.subplots(figsize=(10, max(5, 0.35 * len(counts))))
    counts.plot(kind="barh", ax=ax)
    ax.set_title("Most Frequently Recorded Activities")
    ax.set_xlabel("Recorded event count")
    ax.set_ylabel("Activity")
    fig.tight_layout()
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=160, bbox_inches="tight")
    return fig, ax


def plot_case_duration_distribution(durations: pd.DataFrame, output_path: str | Path | None = None):
    """Plot observed elapsed duration from first to last event per case."""
    fig, ax = plt.subplots(figsize=(9, 5))
    values = durations["duration_hours"].dropna()
    ax.hist(values, bins=30)
    ax.set_title("Observed Case Duration Distribution")
    ax.set_xlabel("Elapsed hours between first and last recorded event")
    ax.set_ylabel("Number of cases")
    fig.tight_layout()
    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=160, bbox_inches="tight")
    return fig, ax
