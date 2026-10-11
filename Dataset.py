import pandas as pd

event_data = {
    "case:concept:name": [
        "CASE_001", "CASE_001", "CASE_001", "CASE_001", "CASE_001",
        "CASE_002", "CASE_002", "CASE_002", "CASE_002", "CASE_002",
        "CASE_003", "CASE_003", "CASE_003", "CASE_003", "CASE_003",
        "CASE_004", "CASE_004", "CASE_004", "CASE_004", "CASE_004",
        "CASE_005", "CASE_005", "CASE_005", "CASE_005", "CASE_005"
    ],
    "concept:name": [
        "Registration", "Triage", "Sepsis Screening", "Blood Test", "Antibiotics Administered",
        "Registration", "Triage", "Blood Test", "Lactate Test", "Discharge",
        "Registration", "Triage", "Sepsis Screening", "ICU Admission", "Antibiotics Administered",
        "Registration", "Triage", "Blood Culture", "Ward Admission", "Discharge",
        "Registration", "Sepsis Screening", "Blood Test", "ICU Admission", "Death Recorded"
    ],
    "time:timestamp": [
        "2026-01-01 08:00:00", "2026-01-01 08:15:00",
        "2026-01-01 08:30:00", "2026-01-01 09:00:00",
        "2026-01-01 09:30:00",
        "2026-01-02 09:00:00", "2026-01-02 09:10:00",
        "2026-01-02 09:40:00", "2026-01-02 10:00:00",
        "2026-01-02 14:00:00",
        "2026-01-03 07:00:00", "2026-01-03 07:15:00",
        "2026-01-03 07:30:00", "2026-01-03 08:30:00",
        "2026-01-03 09:00:00",
        "2026-01-04 10:00:00", "2026-01-04 10:20:00",
        "2026-01-04 11:00:00", "2026-01-04 12:00:00",
        "2026-01-04 16:00:00",
        "2026-01-05 06:00:00", "2026-01-05 06:20:00",
        "2026-01-05 07:00:00", "2026-01-05 08:00:00",
        "2026-01-05 09:00:00"
    ],
    "Age": [
        67, 67, 67, 67, 67,
        54, 54, 54, 54, 54,
        81, 81, 81, 81, 81,
        43, 43, 43, 43, 43,
        72, 72, 72, 72, 72
    ]
}

df_event = pd.DataFrame(event_data)
# Convert timestamps to datetime

df_event["time:timestamp"] = pd.to_datetime(
    df_event["time:timestamp"]
)

print(df_event)
