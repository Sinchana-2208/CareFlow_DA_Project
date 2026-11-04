# Patient and case journey findings

The event log records **1,049 cases** with a median of **13 events per case** (mean 14.5; range 3–185). “Case” is used throughout because the workbook provides case identifiers; it does not establish whether one person can have multiple cases.

## Most common complete event sequences

| trace | cases | pct_cases |
| --- | --- | --- |
| ER Registration → ER Triage → ER Sepsis Triage | 35 | 3.34 |
| ER Registration → ER Triage → ER Sepsis Triage → Leucocytes → CRP | 24 | 2.29 |
| ER Registration → ER Triage → ER Sepsis Triage → CRP → Leucocytes | 22 | 2.10 |
| ER Registration → ER Triage → ER Sepsis Triage → CRP → LacticAcid → Leucocytes → IV Liquid → IV Antibiotics | 13 | 1.24 |
| ER Registration → ER Triage → ER Sepsis Triage → Leucocytes → CRP → LacticAcid | 11 | 1.05 |

## Frequent consecutive activity transitions

| activity | next_activity | transition_count |
| --- | --- | --- |
| Leucocytes | CRP | 1774 |
| CRP | Leucocytes | 1443 |
| ER Registration | ER Triage | 970 |
| ER Triage | ER Sepsis Triage | 904 |
| CRP | LacticAcid | 627 |
| LacticAcid | Leucocytes | 564 |
| IV Liquid | IV Antibiotics | 501 |
| IV Antibiotics | Admission NC | 489 |
| Leucocytes | Leucocytes | 454 |
| Leucocytes | LacticAcid | 435 |

Transitions are adjacent activities after sorting each case by `event_index`; they describe recorded sequence only. The full event order may include simultaneous timestamps, so `event_index` is the tie-break/order field used here.

## Journey detail

[`tables/case_journeys.csv`](tables/case_journeys.csv) includes each case's ordered trace, event count, observed timestamp bounds, and a duration recalculated from those bounds. [`tables/trace_frequency.csv`](tables/trace_frequency.csv) lists all observed full traces and their case counts. Long traces are included without clinical interpretation.
