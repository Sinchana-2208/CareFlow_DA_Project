CareFlow Process Mining — Power BI Data Model

1. Overview

This document describes the proposed data model for the CareFlow Process Mining Power BI dashboard.

The data model organises the cleaned sepsis event-log dataset into logical tables so that healthcare activities, patient cases, case durations, and clinical measurements can be analysed consistently.

The model is designed to support five dashboard pages:

1. Executive Overview
2. Patient Journey
3. Case Duration
4. Laboratory Analysis
5. Data Quality

The data model will serve as the foundation for Power BI visualisations, DAX measures, interactive filters, and analytical reporting.

Project: CareFlow Process Mining
Component: Power BI Data Model
Source Format: Microsoft Excel
Visualisation Platform: Microsoft Power BI
Status: Model design documented; implementation and relationship validation pending.

---

2. Source Dataset

The model is based on the cleaned workbook:

"Sepsis_Cases_Event_Log_Cleaned_for_Visualization.xlsx"

The workbook contains the following visualisation-oriented sheets:

Source Sheet| Purpose
"Event Log Visual"| Stores individual recorded healthcare events.
"Case Attributes Visual"| Stores case-level attributes.
"Event Measurements Visual"| Stores available clinical measurement records.
"Cases Summary Visual"| Stores one summary record per case.

The workbook also contains a "Read Me" sheet describing the prepared data.

Each sheet has a different level of detail. These differences must be preserved when building the Power BI model.

Important: The workbook's actual column names should be checked in Power Query before creating relationships or writing final DAX measures.

---

3. Data Model Objectives

The data model aims to:

- Organise event-level and case-level information.
- Connect healthcare activities with their corresponding cases.
- Support accurate distinct case counts.
- Analyse event frequency and activity transitions.
- Calculate recorded case durations.
- Explore laboratory measurements by type and time.
- Support interactive filtering across report pages.
- Reduce unintended duplication in calculated metrics.
- Provide a foundation for reliable data-quality reporting.

---

4. Proposed Data Model Architecture

The model uses four logical tables.

4.1 Logical Model

                 CASE ATTRIBUTES
                 One row per case
                       |
                       | case_id
                       |
                       v
                    EVENT LOG
                 One row per event
                       ^
                       |
                       | case_id
                       |
                  CASES SUMMARY
                 One row per case


                    EVENT LOG
                       ^
                       |
                       | case_id
                       |
                       v
               EVENT MEASUREMENTS
              One row per measurement

This diagram illustrates the logical data entities and their shared case identifier. It is not the final Power BI relationship diagram.

4.2 Recommended Relationship Design

For a more robust Power BI implementation, consider creating a dedicated "DimCase" table containing one unique row per case.

The recommended star-style model is:

                      DimCase
                    One row per case
                    /      |      \
                   /       |       \
                  v        v        v
             EventLog   CaseSummary  EventMeasurements
             Many rows   One row      Many rows
             per case    per case     per case

Recommended relationships:

- "DimCase[case_id]" → "EventLog[case_id]"
- "DimCase[case_id]" → "CaseSummary[case_id]"
- "DimCase[case_id]" → "EventMeasurements[case_id]"

Each relationship should be one-to-many, with "DimCase" on the one side.

The "Case Attributes Visual" sheet can be used to help construct "DimCase" if it contains exactly one row per case and a unique, nonblank "case_id".

The model should not contain multiple competing active filter paths without a deliberate reason.

---

5. Table 1 — Event Log

5.1 Purpose

The "EventLog" table stores individual recorded healthcare activities associated with patient cases.

It is the primary fact table for analysing event frequency, activity sequences, and activity trends over time.

5.2 Source

Excel sheet:

"Event Log Visual"

5.3 Grain

One row represents one recorded event.

A case can contain multiple event records.

5.4 Core Columns

The cleaned event-log schema includes the following core fields:

Column| Suggested Data Type| Description
"case_id"| Text| Identifier linking an event to its case.
"activity"| Text| Name of the recorded healthcare activity.
"timestamp"| Date/Time| Timestamp associated with the event.
"event_index"| Whole Number| Event-order index within a case.
"org_group"| Text| Available organisational group information.
"lifecycle_transition"| Text| Available lifecycle transition information.

These are the known core fields. Additional fields should only be documented if they are present in the imported sheet.

5.5 Primary Identifier

The combination of "case_id" and "event_index" may help identify an event's position within a case.

However, do not assume this combination is globally unique until it has been checked against the dataset.

If duplicate events can share the same case and index, a separate event identifier or a documented composite key may be necessary.

5.6 Analytical Uses

The table supports:

- Total event counts.
- Activity frequency analysis.
- Event trends over time.
- Activity transitions.
- Patient journey exploration.
- Organisational group comparisons, where the field is meaningful.
- Lifecycle transition analysis.

5.7 Data Quality Rules

Validate the following:

- "case_id" is not blank.
- "activity" is available for activity analysis.
- "timestamp" is converted to a valid Date/Time type.
- "event_index" uses a consistent numeric type.
- Events can be ordered consistently within each case.
- Repeated records are reviewed before being classified as duplicates.
- Missing organisational or lifecycle labels are handled according to the documented cleaning rules.

The cleaned workbook uses "Not recorded" for certain missing organisational and lifecycle labels.

This label must be interpreted as unavailable information, not as a real organisational group or lifecycle transition.

---

6. Table 2 — Case Attributes

6.1 Purpose

The "CaseAttributes" table stores information describing individual patient cases.

It provides context for analysing differences between cases.

6.2 Source

Excel sheet:

"Case Attributes Visual"

6.3 Grain

One row represents one case.

The model requires "case_id" to be unique in this table.

6.4 Columns

The exact attribute columns must be confirmed from the workbook.

Potential attributes include:

- "case_id"
- Age
- Diagnosis or diagnostic category
- Other available case-level categories

These are examples of possible attributes, not a guarantee that every column is present.

6.5 Primary Key

"case_id"

This column must contain one unique, nonblank identifier for each case.

6.6 Analytical Uses

The table can support:

- Case segmentation.
- Comparison across available patient attributes.
- Case counts by available categories.
- Filtering the event log by case-level attributes.

6.7 Data Quality Rules

- Confirm that each case appears only once.
- Check that attribute values use consistent formats.
- Identify missing or unknown categories.
- Verify that case identifiers match the identifiers used in the event log.
- Document imputed values separately from originally observed values.

The cleaned workbook documents that missing diagnosis or category values may be labelled "Unknown / not recorded".

If age values were imputed using the median, this must be documented because an imputed value is not an original observation.

---

7. Table 3 — Event Measurements

7.1 Purpose

The "EventMeasurements" table stores available clinical measurement records in long format.

It supports exploration of measurement frequencies and trends.

7.2 Source

Excel sheet:

"Event Measurements Visual"

7.3 Grain

One row represents one recorded measurement.

A case may have multiple measurement records, including multiple measurements of the same type.

7.4 Measurement Types

The prepared dataset documents the following measurement types:

- Leucocytes
- CRP
- LacticAcid

7.5 Core Information

The table should contain the fields available in the actual sheet to identify:

- The associated case.
- The measurement type.
- The recorded measurement value.
- The measurement timestamp, where provided.

The precise column names and units must be confirmed before implementing the model.

Do not invent missing values, measurement timestamps, or units.

7.6 Analytical Uses

The table supports:

- Measurement counts by type.
- Measurement trends over time.
- Measurement comparisons where units and definitions are compatible.
- Case-level measurement exploration.
- Filtering by measurement type.

7.7 Data Quality Rules

- Check that measurement values use an appropriate numeric type.
- Validate timestamps where available.
- Preserve measurement types and units.
- Review implausible or incorrectly formatted values.
- Do not treat an absent measurement record as a measured value of zero.
- Do not fabricate measurements for cases or timestamps where no measurement was recorded.

Important: Clinical measurement analysis must not be interpreted as a diagnosis. Clinical interpretation requires appropriate medical context.

---

8. Table 4 — Cases Summary

8.1 Purpose

The "CasesSummary" table contains precomputed summary information for each case.

It supports case-duration analysis and case-level reporting.

8.2 Source

Excel sheet:

"Cases Summary Visual"

8.3 Grain

One row represents one case.

The "case_id" column must be unique and nonblank.

8.4 Expected Information

The prepared workbook documents that this sheet contains:

- Case identifier.
- Start timestamp.
- End timestamp.
- Event count.
- Calculated duration in days.

Confirm the exact column names before creating DAX measures.

8.5 Duration Definition

Recorded case duration is calculated as:

"Duration = End Timestamp - Start Timestamp"

Where:

- Start timestamp represents the first recorded event timestamp for the case.
- End timestamp represents the last recorded event timestamp for the case.
- Duration is expressed in days when using the workbook's documented duration field.

8.6 Analytical Uses

The table supports:

- Average recorded case duration.
- Median recorded case duration.
- Duration distribution.
- Case-level duration tables.
- Comparison of recorded durations across available categories.

8.7 Validation Rules

- The start timestamp must not occur after the end timestamp.
- Event counts should agree with the event-log aggregation, subject to the documented event inclusion rules.
- Calculated duration should agree with the difference between the start and end timestamps.
- Case identifiers must match the case identifiers in the other tables.
- Cases with invalid timestamps must be investigated rather than silently assigned misleading durations.

Interpretation: The recorded duration measures the span between the first and last recorded events. It does not automatically represent hospital length of stay, treatment duration, or recovery time.

---

9. Primary Keys and Foreign Keys

The following key design is recommended.

Table| Key Column| Key Role
"DimCase"| "case_id"| Primary key for the case dimension.
"EventLog"| "case_id"| Foreign key linking events to cases.
"CaseAttributes"| "case_id"| Case identifier; unique if retained as a separate one-row-per-case table.
"CasesSummary"| "case_id"| Case identifier; unique if one row exists per case.
"EventMeasurements"| "case_id"| Foreign key linking measurements to cases.

If "CaseAttributes" is used to construct "DimCase", it may not need to remain a separate table in the final model.

Do not create a relationship using an attribute such as activity name or measurement type when the intended relationship is based on case identity.

---

10. Relationship Cardinality

10.1 Recommended Relationships

One Side| Many Side| Cardinality| Filter Direction
"DimCase[case_id]"| "EventLog[case_id]"| One-to-many| Single direction
"DimCase[case_id]"| "CasesSummary[case_id]"| One-to-many| Single direction
"DimCase[case_id]"| "EventMeasurements[case_id]"| One-to-many| Single direction

The single-direction filter design allows case selections to filter the associated fact records.

Use "DimCase" as the common case dimension to avoid directly joining event-level and measurement-level tables in ways that can multiply rows.

10.2 Why Direct Fact-to-Fact Joins Should Be Avoided

A case may have many event records and many measurement records.

Joining both tables directly by "case_id" can produce multiple combinations for the same case.

For example, a case with 20 event records and 10 measurement records could generate 200 joined rows in a direct many-to-many-style merge.

This can inflate event counts, measurement counts, and other calculations.

The recommended approach is to keep the tables at their original grain and connect them through the case dimension.

10.3 Referential Integrity

Check whether every case identifier in the event and measurement tables exists in "DimCase".

Investigate unmatched case identifiers before publishing the report.

---

11. Power BI Model Configuration

11.1 Data Types

Use the following general data-type guidelines.

Field| Recommended Type
"case_id"| Text
"activity"| Text
"timestamp"| Date/Time
"event_index"| Whole Number
"org_group"| Text
"lifecycle_transition"| Text
Measurement value| Decimal Number
Duration in days| Decimal Number
Event count| Whole Number

The final types must match the actual imported columns.

11.2 Table Naming

Use consistent table names in Power BI:

- "DimCase"
- "EventLog"
- "CaseAttributes", if retained separately
- "EventMeasurements"
- "CasesSummary"

These are recommended model names. The Excel sheet names may differ from the names used inside Power BI.

11.3 Hide Technical Fields When Appropriate

Fields such as technical event indices or internal keys can be hidden from report users when they are not needed for analysis.

Keep the fields available to the model where they are required for sorting, relationships, or calculations.

---

12. Date and Time Handling

Event timestamps are important for analysing patient activity sequences and temporal patterns.

Requirements

- Convert valid timestamp columns to Date/Time.
- Investigate invalid timestamps.
- Preserve the original timestamp meaning.
- Use a consistent time-zone interpretation.
- Ensure that events are sorted correctly within cases.
- Avoid comparing timestamps with incompatible time-zone assumptions.

Optional Date Dimension

A dedicated "DimDate" table may be introduced for date-based analysis.

It should be related to the relevant date field through a deliberate model design.

If multiple timestamp columns are used, such as event timestamps and case start timestamps, decide which date relationships should be active and how alternative date contexts will be handled.

A date dimension is optional for the initial report and should be added when it improves time-based analysis.

---

13. DAX Measures Supported by the Model

The data model is intended to support the following measures.

Measure| Source Table| Purpose
Total Cases| "DimCase" or "CasesSummary"| Count distinct cases.
Total Events| "EventLog"| Count recorded event rows.
Total Measurements| "EventMeasurements"| Count recorded measurement rows.
Average Recorded Case Duration| "CasesSummary"| Calculate the mean case duration.
Median Recorded Case Duration| "CasesSummary"| Calculate the median case duration.
Activity Frequency| "EventLog"| Count events by activity.
Cases by Category| "DimCase"| Count cases by an available case attribute.
Measurements by Type| "EventMeasurements"| Count measurement records by type.

The exact formulas should be stored in:

"powerbi/dax_measures/measures.dax"

Every measure must be checked against the imported table and column names before implementation.

---

14. Example DAX Measures

The following examples illustrate the intended calculations. They assume that the model uses the table and column names documented above.

14.1 Total Cases

Total Cases =
DISTINCTCOUNT ( DimCase[case_id] )

Counts distinct cases in the current filter context.

14.2 Total Events

Total Events =
COUNTROWS ( EventLog )

Counts recorded event rows.

This measure should be validated against the event-log row count and should not be calculated from a merged table that duplicates events.

14.3 Total Measurements

Total Measurements =
COUNTROWS ( EventMeasurements )

Counts recorded measurement rows.

14.4 Average Recorded Case Duration

Assuming "CasesSummary" contains a numeric "duration_days" column:

Average Recorded Case Duration (Days) =
AVERAGE ( CasesSummary[duration_days] )

Only valid duration values should contribute to the calculation.

14.5 Median Recorded Case Duration

Median Recorded Case Duration (Days) =
MEDIAN ( CasesSummary[duration_days] )

This measure reports the median of the available numeric duration values.

14.6 Distinct Activities

Distinct Activities =
DISTINCTCOUNT ( EventLog[activity] )

Counts distinct recorded activity labels in the current filter context.

These measures are examples, not verified final formulas. Adjust them to the actual Power BI model and validate their results.

---

15. Data Quality and Model Validation

Before the dashboard is published, validate the model using the following checks.

15.1 Key Validation

- Confirm that "DimCase[case_id]" is unique.
- Confirm that case identifiers are not blank.
- Confirm that "CasesSummary" contains no more than one row per case.
- Check for duplicate case identifiers in "CaseAttributes", if retained separately.

15.2 Relationship Validation

- Confirm that all relationships use the intended case identifier.
- Verify one-to-many cardinality where expected.
- Investigate unmatched case identifiers.
- Avoid unintended many-to-many relationships.
- Check for ambiguous filter paths.

15.3 Event Validation

- Compare the Power BI event count with the source event-log row count.
- Confirm that activity frequencies match the source data.
- Check timestamp validity and event ordering.
- Review duplicate event records.

15.4 Measurement Validation

- Compare measurement counts with the source sheet.
- Verify measurement types and numeric values.
- Preserve the original measurement units.
- Avoid converting missing measurements to zero.

15.5 Duration Validation

- Recalculate durations from start and end timestamps.
- Compare the calculated values with "duration_days".
- Investigate negative or implausible durations.
- Confirm the units displayed in KPI cards and charts.

---

16. Data Transformation Rules

The cleaned workbook was prepared specifically for visualisation and documents the following rules:

- The original source workbook was not overwritten.
- Missing organisational and lifecycle labels were replaced with "Not recorded".
- Missing diagnosis or category labels were represented as "Unknown / not recorded".
- The measurement table contains recorded measurements rather than fabricated missing measurement rows.
- Age values may have been median-imputed where an age value was unexpectedly missing.
- Case summary information includes calculated start/end timestamps, event counts, and durations.

These transformations must be understood when interpreting dashboard results.

The labels "Not recorded" and "Unknown / not recorded" are data-quality placeholders, not clinical categories.

---

17. Privacy and Data Governance

The dataset concerns healthcare-related cases.

Follow these practices:

- Do not publish confidential patient information.
- Avoid exposing identifiable case-level details in public screenshots.
- Verify data-sharing permissions before uploading datasets to GitHub.
- Use aggregated visuals for public project demonstrations where appropriate.
- Restrict access to sensitive files.
- Review exported reports before sharing them.
- Follow applicable organisational data-protection requirements.

A case identifier should not automatically be assumed to be anonymous merely because it does not contain a patient's name.

---

18. Implementation Checklist

Use this checklist when implementing the data model in Power BI.

- [ ] Import the four relevant Excel sheets.
- [ ] Verify actual column names and data types.
- [ ] Confirm the grain of every table.
- [ ] Validate "case_id" values.
- [ ] Build "DimCase" with unique case identifiers.
- [ ] Configure the case-to-event relationship.
- [ ] Configure the case-to-summary relationship.
- [ ] Configure the case-to-measurement relationship.
- [ ] Validate relationship cardinality and filter direction.
- [ ] Check for duplicate or unmatched keys.
- [ ] Validate event and measurement counts.
- [ ] Validate recorded case durations.
- [ ] Create and verify DAX measures.
- [ ] Test report slicers and cross-filtering.
- [ ] Document any exceptions or limitations.

---

19. Related Project Files

Path| Purpose
"powerbi/README.md"| Overview of the Power BI dashboard component.
"powerbi/report_design/README.md"| Overall report design and visualisation specifications.
"powerbi/report_design/dashboard_layout.md"| Proposed page layouts.
"powerbi/report_design/visual_catalog.md"| Individual visual specifications.
"powerbi/dax_measures/measures.dax"| DAX measure definitions.
"powerbi/screenshots/README.md"| Screenshot documentation.
"powerbi/exports/README.md"| Exported report documentation.

---

20. Current Status

Status: Data model documentation prepared; Power BI implementation pending.

The final model must be verified against the source workbook before the report is considered complete.

Table names, field names, relationships, and calculations should be updated in this document if the implemented model differs from the proposed design.

---

21. Expected Outcome

The completed data model will provide a reliable foundation for the CareFlow Process Mining Power BI dashboard.

It will enable consistent analysis of:

- Recorded healthcare activities.
- Patient case summaries.
- Activity sequences and transitions.
- Recorded case durations.
- Clinical measurement records.
- Data-quality results.

A correctly designed model will help prevent double-counting, improve the reliability of DAX calculations, and support clear and consistent dashboard reporting.

---

Project: CareFlow Process Mining
Component: Power BI Data Model
Directory: "powerbi/data_model/"
Document: "data_model.md"
