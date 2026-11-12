# Data quality report

The workbook's Read Me describes the tables as cleaned and null-free, with certain absent labels explicitly encoded as text. This report independently checks the loaded values. Literal values such as `Unknown / not recorded` and `Not recorded` are categories, not blank cells.

## Missingness

In the four analysis tables, numeric/date blanks are recorded in [`tables/missingness.csv`](tables/missingness.csv). **0** blank cells were detected across these analysis tables. No missingness should be confused with a textual unknown label.

## Consistency checks

| check | count | denominator | rate_pct | note |
| --- | --- | --- | --- | --- |
| Duplicate full rows in event log | 0 | 15190 | 0.00 |  |
| Duplicate (case_id,event_index) | 0 | 15190 | 0.00 |  |
| Duplicate case_id in Case Attributes | 0 | 1049 | 0.00 |  |
| Duplicate case_id in Cases Summary | 0 | 1049 | 0.00 |  |
| Event cases absent from case attributes | 0 | 1049 | 0.00 |  |
| Attribute cases absent from event log | 0 | 1049 | 0.00 |  |
| Event cases absent from summary | 0 | 1049 | 0.00 |  |
| Negative case durations | 0 | 1049 | 0.00 |  |
| Event sequence index gaps / non-start-at-1 cases | 0 | 1049 | 0.00 |  |
| Timestamp decreases in event_index order | 0 | 1049 | 0.00 |  |
| Case summary duration mismatches (>1 second) | 0 | 1049 | 0.00 |  |
| Measure activity/name mismatches | 0 | 7922 | 0.00 |  |

`(case_id, event_index)` is the expected event key for this workbook design. Event ordering was checked by sorting on `event_index`; a timestamp decrease means the resulting order does not follow chronological time. The duration mismatch threshold is one second.

## Interpretation

The key and row checks should be re-run after any refresh. A matching row count does not prove that duplicate or missing records are absent. Where categorical labels are explicit placeholders, retain them as distinct categories in dashboards or clearly group them as unknown.

