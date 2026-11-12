# Dataset profile

## Workbook structure

Source: `Sepsis_Cases_Event_Log_Cleaned_for_Visualization(3).xlsx`. The workbook has **5 sheets**. The four analysis tables contain the following records:

| sheet | rows | columns | duplicate_rows |
| --- | --- | --- | --- |
| Read Me | 7 | 2 | 0 |
| Event Log Visual | 15190 | 6 | 0 |
| Case Attributes Visual | 1049 | 25 | 0 |
| Event Measures Visual | 7922 | 6 | 0 |
| Cases Summary Visual | 1049 | 6 | 0 |

`Read Me` is documentation rather than a case or event table. Inferred types below are pandas' read-time types; they are not a guarantee of the original Excel cell formatting.

## Analysis table fields

### Event Log Visual

| column | inferred_type | non_null | distinct |
| --- | --- | --- | --- |
| case_id | object | 15190 | 1049 |
| event_index | int64 | 15190 | 185 |
| activity | object | 15190 | 16 |
| timestamp | datetime64[ns] | 15190 | 9455 |
| org_group | object | 15190 | 26 |
| lifecycle_transition | object | 15190 | 1 |

### Case Attributes Visual

| column | inferred_type | non_null | distinct |
| --- | --- | --- | --- |
| case_id | object | 1049 | 1049 |
| Age | int64 | 1049 | 15 |
| diagnosis | object | 1049 | 143 |
| InfectionSuspected | int64 | 1049 | 2 |
| DisfuncOrg | int64 | 1049 | 2 |
| SIRSCritTachypnea | int64 | 1049 | 2 |
| Hypotensie | int64 | 1049 | 2 |
| SIRSCritHeartRate | int64 | 1049 | 2 |
| SIRSCritTemperature | int64 | 1049 | 2 |
| SIRSCritLeucos | int64 | 1049 | 2 |
| SIRSCriteria2OrMore | int64 | 1049 | 2 |
| Oligurie | int64 | 1049 | 2 |
| Hypoxie | int64 | 1049 | 2 |
| Infusion | int64 | 1049 | 2 |
| DiagnosticBlood | int64 | 1049 | 2 |
| DiagnosticArtAstrup | int64 | 1049 | 2 |
| DiagnosticIC | int64 | 1049 | 2 |
| DiagnosticSputum | int64 | 1049 | 2 |
| DiagnosticLiquor | int64 | 1049 | 2 |
| DiagnosticOther | int64 | 1049 | 2 |
| DiagnosticXthorax | int64 | 1049 | 2 |
| DiagnosticUrinaryCulture | int64 | 1049 | 2 |
| DiagnosticUrinarySediment | int64 | 1049 | 2 |
| DiagnosticLacticAcid | int64 | 1049 | 2 |
| DiagnosticECG | int64 | 1049 | 2 |

### Event Measures Visual

| column | inferred_type | non_null | distinct |
| --- | --- | --- | --- |
| case_id | object | 7922 | 1011 |
| event_index | int64 | 7922 | 184 |
| activity | object | 7922 | 3 |
| timestamp | datetime64[ns] | 7922 | 2509 |
| measure_name | object | 7922 | 3 |
| measure_value | float64 | 7922 | 698 |

### Cases Summary Visual

| column | inferred_type | non_null | distinct |
| --- | --- | --- | --- |
| case_id | object | 1049 | 1049 |
| event_count | int64 | 1049 | 52 |
| start_timestamp | datetime64[ns] | 1049 | 1049 |
| end_timestamp | datetime64[ns] | 1049 | 1033 |
| duration_days | float64 | 1049 | 1045 |

## Time coverage

Event timestamps span **2013-11-07 07:18:29** through **2015-06-05 10:25:11**. See [`tables/date_ranges.csv`](tables/date_ranges.csv) for every date-time field's observed range. The event table does not establish timezone semantics.

## Case attributes

Age: mean **70.42**, median **75**, interquartile range **60–85**, range **20–90**. Diagnosis values are categorical labels; the most frequent are:

| diagnosis | cases | pct_cases |
| --- | --- | --- |
| Unknown / not recorded | 297 | 28.31 |
| C | 143 | 13.63 |
| B | 76 | 7.24 |
| E | 64 | 6.10 |
| H | 50 | 4.77 |
| G | 38 | 3.62 |
| D | 22 | 2.10 |
| R | 21 | 2.00 |
| K | 20 | 1.91 |
| S | 12 | 1.14 |

Indicator counts and proportions appear in [`tables/case_attribute_indicators.csv`](tables/case_attribute_indicators.csv). Indicator names are preserved as provided and their clinical definitions are not inferred here.
