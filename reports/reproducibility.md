# Reproducibility notes

## Source and scope

Source workbook: `Sepsis_Cases_Event_Log_Cleaned_for_Visualization(3).xlsx`. The analysis reads all five sheets and uses the four named analysis tables. Row counts and field types are in `tables/sheet_profile.csv` and `tables/column_profile.csv`.

## Definitions

- **Rows and missingness:** measured after reading each sheet with pandas; blank cells are null, while textual placeholder categories remain values.
- **Event ordering:** sort by `case_id`, then `event_index`; adjacent transitions use the next activity within that case.
- **Duration:** `(end_timestamp - start_timestamp)` in days from `Cases Summary Visual`; consistency checks compare to duration_days and to event-derived timestamps.
- **Measurement summaries:** distribution statistics are calculated over non-null measure_value rows grouped by measure_name. Records and cases are both reported to expose repeated observations.
- **Indicator counts:** numeric indicator values equal to 1 or 0 are counted directly; no mapping or interpretation is applied.

## Refresh procedure

1. Replace the source workbook with a version whose sheet names and field meanings are confirmed.
2. Run `python reproduce_reports.py /path/to/workbook.xlsx /path/to/output` from this folder (pandas is required). The command creates `output/reports/` and `output/careflow_reports.zip`.
3. Review row counts, missingness, duplicate keys, case coverage, timestamp ordering, and duration discrepancies.
4. Compare output summaries with the refreshed workbook and investigate material changes before sharing.
5. Update the source filename and analysis date in the reports.

All numeric findings are descriptive and should be regenerated rather than manually edited. The CSVs in `tables/` are the supporting outputs. The report-generation code is included as `reproduce_reports.py`.
