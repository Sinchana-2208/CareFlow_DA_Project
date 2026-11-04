# Process and activity analysis

Across 1,049 cases, the event log contains 15,190 records and 16 distinct activity labels.

## Most frequent activities

| activity | event_count | pct_events | cases_with_activity |
| --- | --- | --- | --- |
| Leucocytes | 3374 | 22.21 | 1011 |
| CRP | 3257 | 21.44 | 1006 |
| LacticAcid | 1464 | 9.64 | 859 |
| Admission NC | 1180 | 7.77 | 799 |
| ER Triage | 1052 | 6.93 | 1049 |
| ER Registration | 1049 | 6.91 | 1049 |
| ER Sepsis Triage | 1048 | 6.90 | 1048 |
| IV Antibiotics | 822 | 5.41 | 822 |

Counts in this table are event records. The `cases_with_activity` column counts distinct cases containing the activity, so it is not additive across activities. The most frequent activity labels are **Leucocytes, CRP, LacticAcid, Admission NC, ER Triage**.

## Process sequence

The most frequent adjacent activity transitions are shown in [case journey findings](03_case_journeys.md). Use transition counts together with distinct-case counts to avoid mistaking repeated measurements within a case for broad case coverage. `org_group` and `lifecycle_transition` are included in the source log; see `tables/column_profile.csv` and `tables/missingness.csv` for their observed completeness.

Recommended exploratory slices include event activity by calendar month, event count by case, and activity presence by case. They should be presented as process-log descriptions, not measures of care quality, appropriateness, or causality.
