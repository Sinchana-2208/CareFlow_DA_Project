# CareFlow Data Dictionary

This document outlines the core fields used within the Sepsis clinical event log dataset and generated analytical outputs.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `case:concept:name` | String / ID | Unique identifier for each individual patient hospital visit case. |
| `concept:name` | String | The specific clinical activity or event executed (e.g., ER Triage, Leucocytes, IV Antibiotics). |
| `time:timestamp` | Datetime | Exact timestamp when the clinical activity was logged. |
| `Variant` | String | The ordered sequence of activities representing a patient's care pathway. |
| `Duration_Days` | Float | Total elapsed time from initial patient admission to discharge. |
