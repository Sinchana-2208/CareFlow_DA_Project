import pandas as pd
from src.data_processing import prepare_event_log
from src.data_validation import validate_event_log
from src.process_discovery import build_dfg_counts
from src.performance_metrics import calculate_case_durations
from src.patient_journey import reconstruct_journeys


def sample_events():
    return pd.DataFrame({
        "case_id": ["C1", "C1", "C2"],
        "event_index": [1, 2, 1],
        "activity": ["Registration", "Treatment", "Registration"],
        "timestamp": ["2024-01-01 09:00", "2024-01-01 10:00", "2024-01-02 09:00"],
        "org_group": ["A", "B", "A"],
        "lifecycle_transition": ["complete", "complete", "complete"],
    })


def test_prepare_and_validate():
    events = prepare_event_log(sample_events())
    report = validate_event_log(events)
    assert report["row_count"] == 3
    assert report["distinct_cases"] == 2
    assert report["missing_timestamp"] == 0


def test_dfg_counts():
    events = prepare_event_log(sample_events())
    dfg = build_dfg_counts(events)
    assert len(dfg) == 1
    assert dfg.iloc[0]["source_activity"] == "Registration"
    assert dfg.iloc[0]["target_activity"] == "Treatment"

def test_case_durations_and_journeys():
    events = prepare_event_log(sample_events())
    durations = calculate_case_durations(events)
    c1 = durations.loc[durations.case_id == "C1", "duration_hours"].iloc[0]
    assert c1 == 1.0
    journeys = reconstruct_journeys(events)
    assert journeys["C1"] == ["Registration", "Treatment"]

