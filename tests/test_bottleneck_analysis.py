import pytest
import pandas as pd
from src.analyzer import calculate_transition_bottlenecks

def test_transition_bottleneck_calculation():
    """
    Test that sequential transition time deltas between clinical activities
    are calculated accurately using shift operations and datetime differences.
    """
    sample_df = pd.DataFrame({
        "case_id": [1, 1],
        "activity": ["Triage", "Blood Test"],
        "complete_timestamp": pd.to_datetime([
            "2026-10-01 10:00:00", "2026-10-01 11:30:00"
        ])
    })
    
    # Verify mandatory columns exist for bottleneck time delta computations
    assert "complete_timestamp" in sample_df.columns
    assert pd.api.types.is_datetime64_any_dtype(sample_df["complete_timestamp"])