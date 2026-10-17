"""Process discovery using PM4Py, with a simple fallback DFG counter."""
from __future__ import annotations
from collections import Counter
import pandas as pd


def build_dfg_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Build directly-follows transition frequencies from ordered events.

    A transition A -> B means B was the next recorded event in the same case.
    This is an observed event-log relation, not a clinical recommendation.
    """
    required = ["case_id", "activity", "timestamp"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    sort_cols = ["case_id", "timestamp"] + (["event_index"] if "event_index" in data else [])
    data = data.sort_values(sort_cols, kind="stable")
    data["next_activity"] = data.groupby("case_id", dropna=False)["activity"].shift(-1)
    transitions = data.dropna(subset=["case_id", "activity", "next_activity"])
    counts = Counter(zip(transitions["activity"].astype(str), transitions["next_activity"].astype(str)))
    result = pd.DataFrame(
        [(a, b, n) for (a, b), n in counts.items()],
        columns=["source_activity", "target_activity", "frequency"],
    )
    if not result.empty:
        result = result.sort_values("frequency", ascending=False).reset_index(drop=True)
    return result

  def discover_with_pm4py(df: pd.DataFrame) -> dict:
    """Discover a DFG with PM4Py; return DFG, start and end activity counts.

    Requires PM4Py. The simpler build_dfg_counts function works without it.
    """
    try:
        import pm4py
    except ImportError as exc:
        raise ImportError("PM4Py is required. Install dependencies with: python -m pip install -r requirements.txt") from exc
    data = df.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="raise")
    dfg, starts, ends = pm4py.discover_dfg(
        data,
        case_id_key="case_id",
        activity_key="activity",
        timestamp_key="timestamp",
    )
    return {"dfg": dfg, "start_activities": starts, "end_activities": ends}
