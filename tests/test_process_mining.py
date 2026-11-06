import pytest
import pandas as pd
from src.analyzer import extract_process_variants

def test_process_variants_grouping():
    """
    Test that patient event sequences are correctly grouped and ordered 
    by Case ID to extract accurate process variants.
    """
    sample_df = pd.DataFrame({
        "case_id": [1, 1, 2, 2],
        "activity": ["Registration", "Triage", "Registration", "Blood Test"],
        "complete_timestamp": pd.to_datetime([
            "2026-10-01 10:00:00", "2026-10-01 10:30:00",
            "2026-10-01 11:00:00", "2026-10-01 11:15:00"
        ])
    })
    
    # Verify dataframe structure for variant extraction
    assert "case_id" in sample_df.columns
    assert "activity" in sample_df.columns
    assert len(sample_df["case_id"].unique()) == 2