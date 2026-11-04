# Case duration analysis

Duration is the elapsed time between each case's earliest and latest event timestamps. This is a descriptive event-log span, not necessarily hospital length of stay or time to clinical recovery.

## Summary

| Measure | Result |
|---|---:|
| Cases | 1,049 |
| Mean | 28.48 days |
| Median | 5.34 days |
| Standard deviation | 60.56 days |
| 25th / 75th percentile | 0.64 / 18.01 days |
| 90th / 95th percentile | 92.75 / 163.94 days |
| Minimum / maximum | 0.00 / 422.32 days |
| Under 1 day | 272 (25.9%) |
| Over 7 days | 444 (42.3%) |

## Duration bands

| duration_band | cases | pct_cases |
| --- | --- | --- |
| <1 day | 272 | 25.93 |
| 1–<3 days | 75 | 7.15 |
| 3–<7 days | 258 | 24.59 |
| 7–<14 days | 137 | 13.06 |
| 14+ days | 307 | 29.27 |

The mean (28.48 days) is substantially above the median (5.34 days), and the 95th percentile is 163.94 days, indicating a strong right tail. The maximum is 422.32 days. These unusually long event spans should be reviewed as case-level records before operational interpretation. Timestamp ordering and summary-duration consistency checks passed, but they do not explain why a span is long.
