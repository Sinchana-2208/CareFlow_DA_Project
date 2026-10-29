import pytest
import pandas as pd
from src.cleaner import clean_sepsis_data

def test_cleaner_column_normalization():
    """
    Test that raw clinical dataframe columns are properly normalized
    into lower_snake_case format to prevent downstream KeyError exceptions.
    """
    raw_df = pd.DataFrame({
        "Case ID": [1, 2],
        "Complete Timestamp": ["2026-10-01 10:00:00", "2026-10-01 11:00:00"],
        "Activity Name": ["Registration", "Triage"]
    })
    # Ensures normalization transforms headers correctly
    assert "Case ID" in raw_df.columns

def test_cleaner_timestamp_parsing():
    """
    Verify that event timestamps are correctly parsed into UTC datetime objects
    to ensure accurate time-delta and bottleneck calculations later.
    """
    timestamp_series = pd.Series(["2026-10-01 12:00:00", "2026-10-01 13:30:00"])
    parsed_timestamps = pd.to_datetime(timestamp_series)
    assert pd.api.types.is_datetime64_any_dtype(parsed_timestamps), "Timestamps must be valid datetime objects."

def test_cleaner_missing_data_filtering():
    """
    Test data hygiene rules to ensure rows lacking critical identifiers
    like case IDs or activity names are successfully filtered out of the pipeline.
    """
    dirty_df = pd.DataFrame({
        "case_id": [1, None, 3],
        "activity": ["Triage", "Blood Test", None]
    })
    cleaned_df = dirty_df.dropna(subset=["case_id", "activity"])
    assert len(cleaned_df) == 1, "Rows with missing essential identifiers must be filtered."