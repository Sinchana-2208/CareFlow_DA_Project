"""Loading and preparing the CareFlow Sepsis event-log workbook.

The uploaded workbook is already described as cleaned for visualization. These
functions validate and standardize a working copy; they do not overwrite raw data.
"""
from __future__ import annotations

from pathlib import Path
import re
import pandas as pd

EVENT_SHEET = "Event Log Visual"
CASE_ATTRIBUTES_SHEET = "Case Attributes Visual"
EVENT_MEASURES_SHEET = "Event Measures Visual"
CASE_SUMMARY_SHEET = "Cases Summary Visual"

REQUIRED_EVENT_COLUMNS = [
    "case_id", "event_index", "activity", "timestamp",
    "org_group", "lifecycle_transition"
]


def load_workbook(path: str | Path) -> dict[str, pd.DataFrame]:
    """Load relevant workbook sheets into a dictionary of DataFrames."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Workbook not found: {path}")
    sheets = pd.read_excel(path, sheet_name=None)
    required_sheets = [EVENT_SHEET, CASE_ATTRIBUTES_SHEET, EVENT_MEASURES_SHEET, CASE_SUMMARY_SHEET]
    missing = [name for name in required_sheets if name not in sheets]
    if missing:
        raise ValueError(f"Workbook is missing expected sheet(s): {missing}. Available: {list(sheets)}")
    return sheets


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column labels without changing the underlying values."""
    out = df.copy()
    out.columns = [
        re.sub(r"_+", "_", re.sub(r"[^0-9a-zA-Z]+", "_", str(c).strip().lower())).strip("_")
        for c in out.columns
    ]
    return out

def prepare_event_log(df: pd.DataFrame) -> pd.DataFrame:
    """Return a prepared event-log copy with validated core fields.

    Does not drop duplicate rows or missing values automatically. It converts
    timestamps safely, normalizes text whitespace, and sorts events by case,
    timestamp, and event_index when available.
    """
    out = standardize_column_names(df)
    missing = [c for c in REQUIRED_EVENT_COLUMNS if c not in out.columns]
    if missing:
        raise ValueError(f"Event log is missing required columns: {missing}")

    for col in ["case_id", "activity", "org_group", "lifecycle_transition"]:
        out[col] = out[col].astype("string").str.strip()

    out["event_index"] = pd.to_numeric(out["event_index"], errors="coerce")
    out["timestamp"] = pd.to_datetime(out["timestamp"], errors="coerce")
    # A stable sort preserves original order when sort keys tie.
    out = out.sort_values(["case_id", "timestamp", "event_index"], kind="stable", na_position="last")
    return out.reset_index(drop=True)


def save_processed_event_log(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Save processed event data as CSV, creating parent directories."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path

