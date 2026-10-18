# Sepsis Cases Event Log - Schema Documentation

## Dataset Overview
- **File:** `Sepsis_Cases_Event_Log.xlsx`
- **Total Cases:** 1,049
- **Total Clinical Events:** 15,214

## Primary Event Log Fields
- `case:concept:name`: Unique anonymized identifier for each patient trajectory.
- `concept:name`: The specific clinical activity or event (e.g., `ER Triage`, `Leucocytes`, `CRP`, `Admission NC`).
- `time:timestamp`: Exact timestamp when the clinical action occurred.
- `org:group`: The department or clinical unit performing the activity.

## Clinical Attributes
- `Lifecycle`: Event status flag (e.g., `complete`).
- `Age` & `InfectionSuspected`: Case-level clinical diagnostic attributes.
