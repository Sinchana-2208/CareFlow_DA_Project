# CareFlow — Clinical Pathway Process Mining

CareFlow is a healthcare operations analytics prototype that reconstructs patient journeys from timestamped event logs, highlights repeated activity sequences, measures elapsed time between events, and checks conformance against a baseline clinical pathway.

> **Important:** The included dataset is entirely synthetic. It is designed to test the project's process-mining workflow and deliberately injects a triage return after X-Ray into 40% of generated cases. This is not a measured result from a real hospital and must not be treated as clinical evidence.

## Problem being addressed

Traditional healthcare dashboards commonly report averages, such as overall emergency department throughput. Those aggregates do not, by themselves, reveal the sequence of activity events that leads to delay or rework. CareFlow models each visit as a chronological trace and searches for direct activity-to-activity transitions that merit operational review.

## Current prototype capabilities

- Generates synthetic event records using `Case_ID`, `Activity_Name`, and `Timestamp`.
- Validates required fields, duplicate records, timestamp validity, chronological order, and registration/discharge counts.
- Calculates case throughput time, event counts, process variants, and the `X-Ray → Triage` return rate.
- Builds a directly-follows graph and sample patient-journey timelines.
- Ranks activity transitions by mean, median, and 90th-percentile inter-event elapsed time.
- Compares observed traces with a documented baseline pathway.
- Uses PM4Py for optional process discovery when it is installed; the native NetworkX graph and core metrics do not require PM4Py.
- Exports CSV artifacts for subsequent warehouse/BI integration.

## Repository contents

```text
CareFlow_Project/
├── CareFlow_Clinical_Pathway_Process_Mining.ipynb
├── README.md
├── requirements.txt
├── .gitignore
└── careflow_data/                 # generated synthetic demo outputs
    ├── raw_event_log.csv
    ├── clean_event_log.csv
    ├── case_metrics.csv
    ├── transition_bottlenecks.csv
    ├── process_variants.csv
    ├── process_transitions.csv
    ├── conformance_results.csv
    └── data_quality_report.csv
```

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab CareFlow_Clinical_Pathway_Process_Mining.ipynb
```

Run the notebook from the project directory. It generates deterministic sample data using a fixed random seed and writes CSVs into `careflow_data/`.

## Core event-log schema

| Field | Meaning |
|---|---|
| `Case_ID` | Anonymous identifier for one simulated visit |
| `Activity_Name` | Clinical/operational activity recorded for the case |
| `Timestamp` | Timestamp of the event |
| `Department` | Simulated department responsible for the event |
| `Resource_ID` | Synthetic staff/resource identifier |
| `Age_Band` | Synthetic age band for cohort filtering |
| `Arrival_Shift` | Derived arrival-shift category |
| `Return_Reason` | Populated on the injected repeat-triage event |
| `Is_Synthetic` | Marks all records as synthetic |

The three core columns are sufficient to begin many process-mining analyses. Additional fields support prototype investigation and should be reviewed/minimized before any real-data deployment.

## Metric definitions and caveats

- **Case throughput time** = last event timestamp minus first event timestamp in a case.
- **Inter-event elapsed time** = next event timestamp minus current event timestamp. Without explicit queue-entry, activity-start, and activity-end timestamps, this is not pure waiting time or service time.
- **Triage-return rate** = cases with a direct `X-Ray → Triage` transition divided by all cases.
- **Baseline conformance** = exact sequence match against `Registration → Triage → Physician Assessment → X-Ray → Physician Reassessment → Treatment → Discharge`. This transparent first-pass rule flags extra activities as deviations; formal PM4Py alignment-based conformance and clinically approved variants are future improvements.

## Planned next steps

1. Replace synthetic data with authorized, de-identified EHR event logs.
2. Configure BigQuery ingestion and dbt models/tests for standardization and data quality.
3. Use PM4Py process discovery and formal conformance checking on validated data.
4. Build a Power BI/Looker dashboard with process flow, return-loop KPIs, bottlenecks, and controlled drill-downs.
5. Evaluate operational interventions using authorized before/after data and clinically approved definitions.

## Responsible use

Do not commit real patient data, credentials, or secrets to GitHub. Before using real healthcare records, obtain authorization and apply the healthcare organization's privacy, security, access-control, and retention requirements. Prototype outputs are not clinical recommendations.
