# Project Documentation — Questions and Answers

## Q1. What is Careflow Process Mining?
It is a project that uses recorded case events and timestamps to describe and analyze hospital care pathways, timing, and variation.

## Q2. What dataset is being used?
The current workbook is `Sepsis_Cases_Event_Log_Cleaned_for_Visualization(2).xlsx`. It contains event-level records, case-level attributes, recorded laboratory measurements, and a per-case summary.

## Q3. How large is the dataset?
The supplied workbook contains 1,049 cases, 15,190 event rows, and 7,922 measurement rows.

## Q4. Why is an event log important?
It records what activity happened, for which case, and when. These fields make it possible to reconstruct event sequences and calculate elapsed times.

## Q5. What is a case?
A case is the unit whose pathway is being studied, identified by `case_id`. In this workbook, the case is a record grouping related events; do not assume it always represents a unique individual unless the dataset documentation confirms that.

## Q6. What is process discovery?
Process discovery summarizes recorded event sequences into a representation of how the process appears to have occurred in the data.

## Q7. What is a bottleneck?
A bottleneck is a potential constraint that slows a process. In this project, unusually long recorded intervals can be flagged for investigation, but the log alone cannot prove the cause or clinical significance.

## Q8. Which activities are recorded?
Examples include ER Registration, ER Triage, ER Sepsis Triage, Leucocytes, CRP, LacticAcid, IV Liquid, IV Antibiotics, Admission NC, Admission IC, and release/return events.

## Q9. Which measurements are included?
The measurement sheet includes recorded Leucocytes, CRP, and LacticAcid values.

## Q10. Why are there separate tables for events, attributes, measurements, and summaries?
They have different levels of detail. The event log has one row per event; attributes and summaries have one row per case; measurements have one row per recorded measurement. Separating them avoids mixing different row granularities and prevents accidental duplication during analysis.

## Q11. Why can a dataset have no nulls and still have limitations?
Blank cells may have been replaced with labels such as `Unknown / not recorded`, or values may have been imputed. These are not the same as original, fully known values.

## Q12. Can this project diagnose sepsis or recommend treatment?
No. The project is intended for descriptive process analysis of recorded data, not diagnosis or treatment recommendations.

## Q13. How will results be validated?
By checking schema and row counts, timestamp validity, event ordering, case links, summary counts, metric calculations, and automated tests. Dashboard totals should be reconciled with validated tables.

## Q14. What makes the project professional?
Reproducible analysis, clear modular code, documented assumptions, automated tests, meaningful visualizations, transparent limitations, and traceable commits—not just a large number of folders.

## Q15. What are the next implementation steps?
Confirm the repository structure, keep the original workbook unchanged, validate data programmatically, implement the source modules, create tests for each module, then build the visualizations and dashboard.
