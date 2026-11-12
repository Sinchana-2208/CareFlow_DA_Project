# Data Quality and Limitations

## 1. Cleaning information supplied with the workbook
The workbook's `Read Me` sheet states that:
- Visualization sheets were prepared without blank/null cells.
- Missing organization/lifecycle labels are described as being represented with a placeholder.
- Missing diagnosis/categories are labelled `Unknown / not recorded`.
- Age, if unexpectedly missing, was filled with the median and should be treated as an imputation.
- The measurement table contains only recorded Leucocytes, CRP, and LacticAcid values; no measurement rows were fabricated.
- The original source workbook was not overwritten, and sparse event-specific fields were separated rather than deleting valid events.

## 2. Checks observed in the supplied workbook
At the time of inspection:
- The event log contains 15,190 rows and 6 columns.
- The case-attributes sheet contains 1,049 rows and 25 columns.
- The measurement sheet contains 7,922 rows and 6 columns.
- The case-summary sheet contains 1,049 rows and 6 columns.
- No blank/null cells were detected in these four visualization sheets.
- The event timestamps range from 2013-11-07 to 2015-06-05.

A lack of null cells does not mean every value is known or complete. Placeholder categories and imputed values are still important quality considerations.

## 3. Known interpretation cautions
1. **Imputed age:** Median-filled ages are not original observations. If an imputation flag is not available, the exact rows may not be identifiable from this workbook alone.
2. **Unknown diagnosis:** `Unknown / not recorded` is a data category, not a clinical diagnosis.
3. **Coded diagnosis values:** Do not map letter codes to diagnoses without a verified codebook.
4. **Organization codes:** Treat codes such as A, B, or C as identifiers until a trusted mapping explains them.
5. **Measurement units:** Units and reference ranges are not provided in the columns inspected. Do not infer them.
6. **Event timing:** Multiple events can share a timestamp. Event ordering rules must be documented.
7. **Case duration:** Start-to-end elapsed time may not equal inpatient length of stay.
8. **Missing activity:** Absence of an event from the log does not prove that care was not provided.
9. **Observational data:** Associations and long intervals do not establish cause, quality of care, or clinical appropriateness.
10. **Privacy:** Keep patient-level data in approved storage, avoid publishing identifiable records, and follow the organization's data-handling requirements.

## 4. Recommended data-quality report
Before analysis, produce a report with:
- Row counts per sheet.
- Null and placeholder counts.
- Duplicate event checks.
- Missing/extra case IDs across tables.
- Timestamp parsing failures.
- Event-index versus timestamp ordering conflicts.
- Negative or implausible durations.
- Event-count mismatches between the event log and case summary.
- Measurement values outside documented validity rules, if those rules are supplied.

## 5. Limitations statement for reports
“This analysis describes recorded events in the supplied event log. Missing or unrecorded events, coded attributes, imputed values, and timestamp conventions may affect the results. Identified long intervals are candidates for review and do not by themselves establish a clinical bottleneck, treatment delay, or quality-of-care issue.”
