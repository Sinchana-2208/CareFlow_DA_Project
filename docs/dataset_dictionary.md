# Dataset Dictionary

## 1. Workbook and sheets
Workbook: `Sepsis_Cases_Event_Log_Cleaned_for_Visualization(2).xlsx`

| Sheet | Rows in supplied workbook | Purpose |
|---|---:|---|
| `Read Me` | 7 | Notes about the cleaned workbook and cleaning choices |
| `Event Log Visual` | 15,190 | One row per recorded event |
| `Case Attributes Visual` | 1,049 | One row per case with patient/case-level attributes |
| `Event Measures Visual` | 7,922 | Long-format table of recorded laboratory measurements |
| `Cases Summary Visual` | 1,049 | One row per case with start/end times, event count, duration, and event sequence |

Counts are based on the supplied file and should be refreshed if the workbook changes.

## 2. Event Log Visual
One row represents one recorded event.

| Column | Meaning | Notes |
|---|---|---|
| `case_id` | Identifier linking an event to a case | Use to group events into case timelines |
| `event_index` | Event order/index within the case | Check against timestamps before relying on it as chronological order |
| `activity` | Recorded activity name | Examples include ER Registration, ER Triage, CRP, IV Antibiotics, Admission NC, and Release A |
| `timestamp` | Date and time of the event | Parse as a datetime before calculating intervals |
| `org_group` | Recorded organizational/resource group label | Treat codes as labels unless a trusted mapping is available |
| `lifecycle_transition` | Lifecycle state recorded for the event | The supplied workbook shows `complete` for all event rows |

## 3. Case Attributes Visual
One row represents one case. The sheet contains 25 columns.

| Column | Meaning |
|---|---|
| `case_id` | Case identifier |
| `Age` | Recorded age; the workbook notes that missing age values, if any, were filled using the median |
| `diagnosis` | Diagnosis/category code or `Unknown / not recorded` |
| `InfectionSuspected` | Recorded indicator for suspected infection |
| `DisfuncOrg` | Recorded indicator for organ dysfunction |
| `SIRSCritTachypnea` | Recorded SIRS-related tachypnea indicator |
| `Hypotensie` | Recorded hypotension indicator |
| `SIRSCritHeartRate` | Recorded SIRS-related heart-rate indicator |
| `SIRSCritTemperature` | Recorded SIRS-related temperature indicator |
| `SIRSCritLeucos` | Recorded SIRS-related leukocyte indicator |
| `SIRSCriteria2OrMore` | Recorded indicator for two or more SIRS criteria |
| `Oligurie` | Recorded oliguria indicator |
| `Hypoxie` | Recorded hypoxia indicator |
| `Infusion` | Recorded infusion indicator |
| `DiagnosticBlood` | Recorded blood-diagnostic indicator |
| `DiagnosticArtAstrup` | Recorded arterial blood-gas diagnostic indicator |
| `DiagnosticIC` | Recorded diagnostic indicator labelled IC in the source |
| `DiagnosticSputum` | Recorded sputum diagnostic indicator |
| `DiagnosticLiquor` | Recorded liquor/CSF diagnostic indicator |
| `DiagnosticOther` | Recorded other-diagnostic indicator |
| `DiagnosticXthorax` | Recorded chest X-ray diagnostic indicator |
| `DiagnosticUrinaryCulture` | Recorded urinary-culture diagnostic indicator |
| `DiagnosticUrinarySediment` | Recorded urinary-sediment diagnostic indicator |
| `DiagnosticLacticAcid` | Recorded lactic-acid diagnostic indicator |
| `DiagnosticECG` | Recorded ECG diagnostic indicator |

**Caution:** Confirm the exact coding scheme and whether indicators use 0/1 before interpreting them. Do not infer the meaning of diagnosis codes such as `A`, `B`, or `C` without a codebook.

## 4. Event Measures Visual
One row represents one recorded measurement.

| Column | Meaning |
|---|---|
| `case_id` | Case identifier |
| `event_index` | Event index corresponding to the event log |
| `activity` | Activity associated with the measurement |
| `timestamp` | Measurement event timestamp |
| `measure_name` | Measurement name: `Leucocytes`, `CRP`, or `LacticAcid` |
| `measure_value` | Recorded numeric measurement value |

The workbook notes that this table includes only recorded measurement values; it does not fabricate rows for measurements that were not recorded. Confirm units and clinical reference ranges from an authoritative data dictionary before clinical interpretation.

## 5. Cases Summary Visual
One row represents one case.

| Column | Meaning |
|---|---|
| `case_id` | Case identifier |
| `event_count` | Number of events represented in the case summary |
| `start_timestamp` | Earliest timestamp used for the case start |
| `end_timestamp` | Latest timestamp used for the case end |
| `duration_days` | Elapsed time between start and end, expressed in days |
| `event_sequence` | Activity names concatenated into a sequence using arrows |

`duration_days` is elapsed time between the summary timestamps. It should not automatically be described as hospital length of stay unless the start/end definitions are confirmed to match admission and discharge.

## 6. Linking tables
- Join `Event Log Visual` to `Case Attributes Visual` using `case_id`.
- Join `Event Log Visual` to `Event Measures Visual` using `case_id` and, where appropriate, `event_index`; validate uniqueness before joining.
- Join `Cases Summary Visual` to case-level attributes using `case_id`.
- Avoid joining only on `case_id` between event-level tables without considering row multiplication.

## 7. Observed dataset snapshot
- Cases: 1,049
- Event rows: 15,190
- Measurement rows: 7,922
- Event timestamp range: 2013-11-07 07:18:29 through 2015-06-05 10:25:11
- Most frequent activities in the event log include Leucocytes, CRP, LacticAcid, Admission NC, and ER Triage.
- Measurement rows contain Leucocytes, CRP, and LacticAcid.
