# Methodology

## 1. Overview
The proposed workflow moves from validation to process analysis, metrics, visualization, and review. Keep each stage reproducible and record assumptions.

## 2. Stage A — Load and validate
1. Load the relevant workbook sheets.
2. Confirm expected columns and data types.
3. Parse timestamps as datetimes.
4. Check case identifiers and event indices.
5. Check duplicate rows and repeated event identifiers.
6. Check that each event's `case_id` exists in the case-attributes table.
7. Compare event counts with the case summary.
8. Report data-quality checks instead of silently discarding records.

## 3. Stage B — Prepare event log
1. Sort events by `case_id`, timestamp, and event index.
2. Compare timestamp order with `event_index`; flag inconsistencies.
3. Preserve simultaneous events. Several activities may share a timestamp, so do not invent an order unless a documented rule is used.
4. Keep the source workbook unchanged and write derived data to a separate output location.
5. Retain missing/unknown labels as explicit categories where appropriate.

## 4. Stage C — Discover process pathways
Analyze:
- Activity frequency.
- Directly-following activity transitions.
- Common activity sequences.
- Case variants and pathway frequency.
- Differences between event-index order and timestamp order.

A process map should state whether edge labels represent case counts, event counts, or percentages.

## 5. Stage D — Performance metrics
Potential metrics:
- Case duration in days.
- Time between consecutive events.
- Time from ER Registration to ER Triage.
- Time from ER Sepsis Triage to first recorded IV Antibiotics.
- Time from first recorded IV Liquid to first recorded IV Antibiotics.
- Time from admission events to release events, only after validating event semantics.
- Counts and proportions of cases with the required start/end events.

For every metric, document inclusion rules, missing start/end events, units, and the denominator. Do not treat a missing event as a zero-minute interval.

## 6. Stage E — Bottleneck candidates
A long interval or frequent transition may be a candidate for investigation, not proof of a bottleneck. Use robust summaries such as median and interquartile range, inspect outliers, and compare like-for-like case groups where justified. Account for missing events, multiple occurrences, and simultaneous timestamps.

## 7. Stage F — Measurement analysis
Summarize measurement values by name and time. Before clinical interpretation, confirm units, collection context, and reference ranges. A measurement's presence or absence in the log is not proof that a test was clinically indicated or omitted.

## 8. Stage G — Visualization and reporting
Suggested outputs:
- Activity frequency bar chart.
- Case-duration distribution.
- Process-flow map.
- Transition-frequency table.
- Time-interval distribution.
- Measurement trends for cases with multiple observations.
- Case pathway detail view.

Each visual should include a title, units, date range, filters, and denominator where relevant.

## 9. Stage H — Validation and review
- Test calculations on small manually checked cases.
- Compare summary event counts against the event log.
- Check for negative durations and missing timestamps.
- Confirm dashboard totals match the validated tables.
- Record known limitations in every final report.
