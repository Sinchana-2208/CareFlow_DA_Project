# CareFlow Process Mining — `src/` starter package

This package is tailored to the uploaded workbook `Sepsis_Cases_Event_Log_Cleaned_for_Visualization(1).xlsx` and its sheets, especially `Event Log Visual`.

## Included modules

- `data_processing.py`: workbook loading, column normalization, event-log preparation, CSV export.
- `data_validation.py`: event quality checks and case-ID coverage across workbook sheets.
- `process_discovery.py`: directly-follows graph (DFG) transition counts and optional PM4Py DFG discovery.
- `performance_metrics.py`: first-to-last recorded event durations and activity frequencies.
- `bottleneck_analysis.py`: elapsed time between consecutive recorded events and transition summaries.
- `conformance_checking.py`: simple configurable activity-order rule checks; not a validated clinical guideline.
- `patient_journey.py`: reconstruct case journeys and rank observed sequences.
- `visualization.py`: reusable activity-frequency and duration plots.
- `main.py`: runs the starter pipeline and writes outputs.

## Set up on macOS / VS Code

From the repository root, create and activate a virtual environment if you do not already have one:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Put the workbook in `data/raw/` (do not commit sensitive or identifiable healthcare data to a public repository). Then run:

```bash
python -m src.main --input "data/raw/Sepsis_Cases_Event_Log_Cleaned_for_Visualization(1).xlsx" --output reports/generated
```

The script writes processed data, CSV summaries, charts, and `analysis_summary.json` into `reports/generated/`.

## Run tests

From the project root, with dependencies installed:

```bash
python -m pytest -q
```

## Important interpretation notes

- The workbook is described as cleaned for visualization. This code validates and prepares a copy; it does not overwrite the source workbook.
- A case duration means elapsed time from the earliest to latest recorded event. It is not necessarily hospital length of stay.
- A transition delay means elapsed time between two recorded events. It is not necessarily pure waiting time.
- DFG frequencies and pathway counts describe recorded behavior. They do not establish clinical appropriateness, causal effects, or treatment quality.
- Conformance checking needs independently documented and approved reference rules or a process model.
- Review the generated quality report before interpreting results. The code intentionally reports duplicate rows rather than automatically deleting them.
