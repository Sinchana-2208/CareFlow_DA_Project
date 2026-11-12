# Clinical measurement analysis

The workbook's `Event Measures Visual` has **7,922 measurement rows** across 1,011 cases. It includes `measure_name`, `measure_value`, `timestamp`, `activity`, `event_index`, and `case_id`.

## Descriptive distributions

- **CRP:** 3,118 records across 946 cases; median 95.00, IQR 43.00–162.00, range 5.00–573.00. Values retain the workbook's numeric scale; units are not supplied in the table.
- **LacticAcid:** 1,452 records across 856 cases; median 1.60, IQR 1.10–2.30, range 0.20–14.90. Values retain the workbook's numeric scale; units are not supplied in the table.
- **Leucocytes:** 3,352 records across 1,010 cases; median 10.95, IQR 7.70–15.00, range 0.20–381.30. Values retain the workbook's numeric scale; units are not supplied in the table.

## How to use these results

The values and ranges are descriptive summaries of the recorded numeric column. The workbook does not supply units, assay methods, reference intervals, measurement context, or patient-level interpretation rules. Do not treat the distributions or any suggested visualization bins as medical thresholds. Repeated readings mean row-level distributions are not patient-level distributions; compare patients only after defining a clinically appropriate time point and aggregation with domain review.

The complete numeric summary is in [`tables/measurement_summary.csv`](tables/measurement_summary.csv). Per-case measurement record counts are in [`tables/measurements_per_case.csv`](tables/measurements_per_case.csv), and measurement timestamp ranges are in [`tables/measurement_date_ranges.csv`](tables/measurement_date_ranges.csv).
