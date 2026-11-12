# CareFlow Process Mining — Reports

This folder contains a descriptive, reproducible report pack built from the workbook `Sepsis_Cases_Event_Log_Cleaned_for_Visualization(3).xlsx`. It is designed to support process exploration and Power BI reporting. It does not provide clinical diagnosis, treatment recommendations, or outcome evaluation.

## Dataset at a glance

- **1,049 cases** and **15,190 event records** in the event log.
- Event timestamps span **2013-11-07 07:18:29** to **2015-06-05 10:25:11**.
- Case attributes cover **1,049 cases**; the clinical measurement table covers **1,011 cases** and 7,922 measurement records.
- Case summary durations: median **5.34 days**, mean **28.48 days**, range **0.00–422.32 days**.

## Contents

- [Dataset profile](01_dataset_profile.md): sheets, fields, inferred types, coverage, and date ranges.
- [Data quality](02_data_quality.md): missingness, key coverage, ordering, and consistency checks.
- [Patient and case journeys](03_case_journeys.md): event sequences, activities, and transitions.
- [Case duration](04_case_duration.md): descriptive duration distribution.
- [Clinical measurements](05_clinical_measurements.md): Leucocytes, CRP, and LacticAcid distributions, with measurement-specific caveats.
- [Process and activity analysis](06_process_activity.md): event volumes and common transitions.
- [Power BI interpretation and template](07_power_bi_dashboard.md): recommended pages, visuals, and interpretation guardrails.
- [Limitations](08_limitations.md): appropriate scope and unsupported conclusions.
- [Reproducibility](09_reproducibility.md): source, calculation definitions, and refresh steps.
- `tables/`: machine-readable profiles and supporting summary tables.
