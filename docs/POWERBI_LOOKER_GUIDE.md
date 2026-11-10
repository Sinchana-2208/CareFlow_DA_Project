# Looker Studio / Power BI Build Guide

The repository ships a ready-to-open HTML dashboard (`dashboard/careflow_dashboard.html`). To build the
enterprise version in Power BI or Looker Studio, follow the steps below. A `.pbix` file cannot be generated
outside Power BI Desktop, so this guide gives the exact data model and measures.

## 1. Connect to data
**Power BI Desktop → Get Data → Google BigQuery** (after `dbt run`), choose the mart tables below. For an
offline demo use **Get Data → Text/CSV** with the files in `careflow_data/`.

| Table | BigQuery mart | CSV fallback |
|---|---|---|
| Cases | `fct_patient_cases` | `careflow_data/case_metrics.csv` |
| Transitions | `fct_transition_bottlenecks` | `careflow_data/transition_bottlenecks.csv` |
| Loopbacks | `fct_triage_loopbacks` | `careflow_data/week3_metrics/week3_case_metrics.csv` |
| Variants | `fct_process_variants` | `careflow_data/process_variants.csv` |
| Conformance | `fct_conformance_results` | `careflow_data/week4_outputs/week4_conformance_by_case.csv` |
| Events (for the process visual) | `stg_careflow__events` | `careflow_data/clean_event_log.csv` |

Relate `Cases[Case_ID]` 1-to-many to `Conformance[Case_ID]` and `Events[Case_ID]`.

## 2. Process-map visual
Install a process-mining custom visual from AppSource (for example *Process Mining by Celonis* or the
*Power Automate Process Mining* visual). Map `Case_ID`, `Activity_Name`, `Timestamp` from `Events`.
Alternative: *Dynamic Network Graph* using `Transitions[Activity_Name]` → `Transitions[Next_Activity]`
with `Transition_Count` as edge weight.

## 3. DAX measures
```DAX
Total Cases        = DISTINCTCOUNT ( Cases[Case_ID] )
Avg Case Minutes   = AVERAGE ( Cases[Case_Duration_Minutes] )
Loopback Cases     = CALCULATE ( [Total Cases], Cases[Returned_To_Triage_After_XRay] = TRUE () )
Loopback Rate %    = DIVIDE ( [Loopback Cases], [Total Cases] ) * 100
Conforming Cases   = CALCULATE ( DISTINCTCOUNT ( Conformance[Case_ID] ), Conformance[Conforms_To_Baseline] = TRUE () )
Conformance Rate % = DIVIDE ( [Conforming Cases], [Total Cases] ) * 100
Avg Minutes Looped = CALCULATE ( [Avg Case Minutes], Cases[Returned_To_Triage_After_XRay] = TRUE () )
Avg Minutes Clean  = CALCULATE ( [Avg Case Minutes], Cases[Returned_To_Triage_After_XRay] = FALSE () )
Potential Savings (min) = ( [Avg Minutes Looped] - [Avg Minutes Clean] ) * DIVIDE ( [Loopback Cases], [Total Cases] )
```

## 4. Page layout
1. **KPI cards:** Total Cases, Avg Case Minutes, Loopback Rate %, Conformance Rate %, Potential Savings.
2. **Process map** (centre) filtered by slicers.
3. **Bar chart:** `Mean_Elapsed_Minutes` by `Transition` (sorted descending) — the bottleneck view.
4. **Table:** variants with case count and share.
5. **Slicers (drill-down):** `Age_Band`, `Arrival_Shift`, `Department`, `Resource_ID` (physician).
6. **Drill-through page:** right-click a variant → case list with `Observed_Trace` and `Deviation_Detail`.

## 5. Looker Studio
Use the BigQuery connector on the same marts, create the same scorecards, a bar chart for transitions,
and add filter controls for age band, shift and resource. Looker Studio has no native process-map; embed
the HTML dashboard or use a community visualization.

> All figures come from synthetic data. Cloud/BI steps must be run and validated in your own environment.

## 6. Existing Looker Studio report — review and fixes

The report screenshot is saved at `docs/images/looker_studio_report.png`. It already shows the four headline KPIs
(500 cases, 150.71 min, 40% loopback, 60% conformance) and the right overall story. Four chart issues are fixed
by pointing the data sources at the labelled tables in `careflow_data/bi_ready/` (created by
`python scripts/export_bi_datasets.py`; upload the CSVs or load them into BigQuery).

| # | Issue in the report | Cause | Fix |
|---|---|---|---|
| 1 | "Top Hospital Process Bottlenecks" groups by *Activity_Name* and averages it, so e.g. X-Ray shows ~23 min although its two outgoing transitions are 15.0 and 30.9 min | Two transitions leave X-Ray (→ Triage and → Physician Reassessment) and are blended | Use `bi_transitions.csv`; dimension = **Transition**, metric = **Mean_Elapsed_Minutes**, sort descending. Add `Is_Loop_Related` as a colour dimension |
| 2 | "Patient Process Variants" axis shows 300 / 200 with no variant name | The dimension is a count, not a label | Use `bi_variants.csv`; dimension = **Variant**, metric = **Case_Count** |
| 3 | "X-Ray to Triage Loopback Reasons" pie has an empty legend entry for 60% | Non-loopback cases have a NULL `Return_Reason` | Use `bi_cases.csv`; dimension = **Loopback_Reason** (non-loopback cases read "No loopback") |
| 4 | KPI tiles are labelled `case_id`, `case_throughput_minutes`, "Loopback Rate 40" | Raw field names; no units | Use `bi_kpis.csv`; rename tiles to *Patient Cases*, *Avg Case Duration (min)*, *Loopback Rate (%)*, *Conformance Rate (%)* |

Also add drill-down controls: drop-down filters for `Age_Band`, `Arrival_Shift` and `Assessing_Physician` (all columns
exist in `bi_cases.csv`), and a table of `Observed_Trace` / `Deviation_Detail` from
`careflow_data/week4_outputs/week4_conformance_by_case.csv`.

The repository's self-contained HTML dashboard (`dashboard/careflow_dashboard.html`) already provides the process map
that Looker Studio cannot draw natively.
