# Power BI dashboard interpretation and template

This template builds on the workbook's four visual-ready tables. Link tables on `case_id`; for event-level detail, retain `event_index` and `timestamp` as the ordering fields. Confirm one-to-many relationships and filter direction in the model before publishing.

## Recommended pages

1. **Overview:** distinct cases, event rows, case duration median, event date range. State each measure's denominator and duration definition.
2. **Process:** activity frequency by event count and by distinct cases; a case flow or transition view ordered by `event_index`. Include filters for date and activity.
3. **Case journeys:** case table from `Cases Summary Visual` with case ID, event count, start/end, duration, and sequence. Keep a drill-through to the event log.
4. **Clinical measurements:** use separate panels for Leucocytes, CRP, and LacticAcid. Show record counts, distribution, timestamp, and case filter. Avoid pooling unlike scales.
5. **Case attributes:** age and supplied indicator fields, with unknown labels visible. Avoid implying those indicators establish diagnosis or severity.

## Measure definitions

- **Cases:** distinct count of case_id in the selected table/filter context.
- **Events:** row count of `Event Log Visual`.
- **Case duration:** use supplied `duration_days` for initial replication; validate against min/max timestamps. Prefer median and percentiles alongside mean.
- **Activity cases:** distinct cases with an activity, not sum of activity counts.
- **Measurement value:** default to individual rows or a distribution within one measure type; avoid summing a clinical reading.

## Interpretation cues

Every card or chart should name the time period, unit (when known), and denominator. Highlight that case duration is timestamp span, measurement records repeat, and labels like `Unknown / not recorded` are data categories. Bins can support exploration but are not clinical reference bands.
