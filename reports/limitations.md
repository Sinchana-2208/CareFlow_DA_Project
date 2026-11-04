# Limitations and unsupported conclusions

- **Observational event log:** timestamps and labels describe recorded events; they do not establish why an event occurred or whether care was appropriate.
- **Case versus person:** `case_id` is the available unit. The workbook does not establish unique patients across cases.
- **Duration meaning:** elapsed first-to-last event span is not validated as admission length, ICU stay, or recovery time.
- **Clinical readings:** measurement units, collection conditions, reference limits, and interpretation guidance are absent. Numeric summaries cannot establish diagnosis, prognosis, treatment response, or whether a value is clinically abnormal.
- **No outcomes endpoint:** no outcome variable is identified in the event log or case attributes, so outcome associations and causal effects are unsupported.
- **Sequence ambiguity:** equal timestamps can occur; `event_index` is used for ordering, but the data dictionary does not explain how ties were assigned.
- **Recorded placeholders:** explicit unknown/not-recorded strings are not nulls and may reflect source coding.
- **Time semantics:** timezone and source-system clock behavior are unspecified.
- **Population/generalization:** the workbook alone does not establish sampling frame, inclusion criteria, or representativeness. Findings should not be generalized beyond these records.

Use this report for operational data exploration and dashboard design only. Any clinical use requires qualified review, validated definitions, and appropriate governance.
