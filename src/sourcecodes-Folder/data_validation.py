"""Quality checks for event logs and related tables."""
from __future__ import annotations
import pandas as pd


def validate_event_log(df: pd.DataFrame) -> dict:
    """Return a compact data-quality report; does not modify the input."""
    required = ["case_id", "event_index", "activity", "timestamp", "org_group", "lifecycle_transition"]
    missing_columns = [c for c in required if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required event-log columns: {missing_columns}")

    timestamps = pd.to_datetime(df["timestamp"], errors="coerce")
    ordered = df.assign(_timestamp=timestamps).sort_values(["case_id", "_timestamp", "event_index"], kind="stable")
    per_case_monotonic = ordered.groupby("case_id", dropna=False)["_timestamp"].apply(
        lambda s: s.dropna().is_monotonic_increasing
    )
    report = {
        "row_count": int(len(df)),
        "distinct_cases": int(df["case_id"].nunique(dropna=True)),
        "distinct_activities": int(df["activity"].nunique(dropna=True)),
        "missing_case_id": int(df["case_id"].isna().sum()),
        "missing_activity": int(df["activity"].isna().sum()),
        "missing_timestamp": int(timestamps.isna().sum()),
        "missing_event_index": int(pd.to_numeric(df["event_index"], errors="coerce").isna().sum()),
        "duplicate_full_rows": int(df.duplicated().sum()),
        "duplicate_case_event_index": int(df.duplicated(subset=["case_id", "event_index"]).sum()),
        "timestamp_min": str(timestamps.min()) if timestamps.notna().any() else None,
        "timestamp_max": str(timestamps.max()) if timestamps.notna().any() else None,
        "cases_with_chronological_order": int(per_case_monotonic.sum()),
        "cases_checked_for_order": int(len(per_case_monotonic)),
    }
    return report

 def validate_related_sheets(sheets: dict[str, pd.DataFrame]) -> dict:
    """Check case ID coverage between event, attributes, measures, and summary sheets."""
    event = sheets["Event Log Visual"]
    attrs = sheets["Case Attributes Visual"]
    measures = sheets["Event Measures Visual"]
    summary = sheets["Cases Summary Visual"]
    event_cases = set(event["case_id"].dropna().astype(str))
    result = {}
    for label, frame in [("case_attributes", attrs), ("event_measures", measures), ("case_summary", summary)]:
        if "case_id" not in frame.columns:
            result[label] = {"missing_case_id_column": True}
            continue
        related_cases = set(frame["case_id"].dropna().astype(str))
        result[label] = {
            "distinct_cases": len(related_cases),
            "cases_not_in_event_log": len(related_cases - event_cases),
            "event_log_cases_missing_from_sheet": len(event_cases - related_cases),
        }
    return result
