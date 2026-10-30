CareFlow Process Mining — Power BI Visual Catalog

1. Overview

This document provides a detailed catalog of the visualisations planned for the CareFlow Process Mining Power BI dashboard.

The dashboard uses the cleaned sepsis event-log dataset to analyse recorded healthcare activities, patient journeys, case durations, clinical measurements, and data quality.

The visual catalog defines the purpose and specifications of each chart, KPI card, table, and interactive filter.

It acts as a reference during Power BI dashboard development and helps maintain consistency across all report pages.

Project: CareFlow Process Mining
Component: Power BI Dashboard
Directory: "powerbi/report_design/"
Document: "visual_catalog.md"
Status: Visualisation design prepared; implementation pending.

---

2. Dashboard Overview

The dashboard is planned to contain five main report pages.

Page No.| Dashboard Page| Main Focus
1| Executive Overview| Overall dataset summary and key metrics
2| Patient Journey| Recorded patient activities and transitions
3| Case Duration| Analysis of recorded case durations
4| Laboratory Analysis| Clinical measurement analysis
5| Data Quality| Missing values, duplicates, and validation

Each page will contain appropriate visualisations to communicate the analytical results clearly.

---

3. Page 1 — Executive Overview

Purpose

The Executive Overview provides a high-level summary of the sepsis event-log dataset.

It allows users to understand the overall size of the dataset, the number of recorded activities, available measurements, and general activity patterns.

3.1 KPI Cards

Visual 1 — Total Cases

Property| Specification
Visual Name| Total Cases
Visual Type| Card
Data Source| DimCase / CasesSummary
Field| case_id
Calculation| Distinct count of case identifiers
Display Format| Whole number
Purpose| Shows the total number of unique cases.

DAX Measure:

Total Cases =
DISTINCTCOUNT(DimCase[case_id])

Expected Outcome: Displays the number of distinct cases represented in the selected data.

Visual 2 — Total Events

Property| Specification
Visual Name| Total Events
Visual Type| Card
Data Source| EventLog
Field| Event records
Calculation| Count of event rows
Display Format| Whole number
Purpose| Shows the total number of recorded healthcare events.

DAX Measure:

Total Events =
COUNTROWS(EventLog)

Expected Outcome: Displays the total number of event records.

Visual 3 — Total Measurements

Property| Specification
Visual Name| Total Measurements
Visual Type| Card
Data Source| EventMeasurements
Field| Measurement records
Calculation| Count of measurement rows
Display Format| Whole number
Purpose| Shows the number of recorded measurement entries.

DAX Measure:

Total Measurements =
COUNTROWS(EventMeasurements)

Expected Outcome: Displays the total number of available measurement records.

Visual 4 — Average Recorded Case Duration

Property| Specification
Visual Name| Average Recorded Case Duration
Visual Type| Card
Data Source| CasesSummary
Field| duration_days
Calculation| Average duration
Display Format| Decimal number with days
Purpose| Shows the average elapsed time between the first and last recorded event per case.

DAX Measure:

Average Recorded Case Duration (Days) =
AVERAGE(CasesSummary[duration_days])

Expected Outcome: Displays the average recorded case duration in days.

This metric must not be interpreted automatically as hospital length of stay.

3.2 Charts and Tables

Visual 5 — Activity Trends Over Time

Property| Specification
Visual Name| Activity Trends
Visual Type| Line Chart
Data Source| EventLog
X-Axis| Event timestamp
Y-Axis| Event count
Legend| Activity, optional
Purpose| Explores changes in recorded activity volume over time.

Recommended Configuration:

- Use event date on the X-axis.
- Use count of event records on the Y-axis.
- Use activity as a legend only if the chart remains readable.
- Allow users to filter the date range.

Expected Outcome: Shows how recorded event activity changes over the selected period.

Visual 6 — Most Frequent Activities

Property| Specification
Visual Name| Most Frequent Activities
Visual Type| Horizontal Bar Chart
Data Source| EventLog
Y-Axis| Activity
X-Axis| Event count
Sorting| Descending
Purpose| Identifies the most frequently recorded activities.

Recommended Configuration:

- Display activity names on the category axis.
- Display event counts on the value axis.
- Sort from highest to lowest.
- Use data labels where appropriate.

Expected Outcome: Highlights activities with the highest recorded frequency.

Visual 7 — Case Summary

Property| Specification
Visual Name| Case Summary
Visual Type| Table
Data Source| CasesSummary
Fields| Case ID, start timestamp, end timestamp, event count, duration
Purpose| Provides case-level summary information.

Expected Outcome: Allows users to inspect individual case summaries.

Visual 8 — Activity Summary

Property| Specification
Visual Name| Activity Summary
Visual Type| Table
Data Source| EventLog
Fields| Activity, event count
Purpose| Provides detailed activity-frequency information.

Expected Outcome: Displays the frequency of each recorded activity.

---

4. Page 2 — Patient Journey

Purpose

The Patient Journey page explores the sequence of recorded activities associated with individual cases.

It helps users understand how activities occur throughout the recorded patient process.

Visual 9 — Patient Activity Flow

Property| Specification
Visual Name| Patient Activity Flow
Visual Type| Sankey Diagram / Process Flow
Data Source| EventLog
Source| Previous activity
Destination| Next activity
Weight| Number of observed transitions
Purpose| Displays transitions between recorded activities.

Recommended Configuration:

- Sort events within each case by timestamp and event index.
- Identify consecutive activity pairs.
- Count the observed transitions.
- Display the transitions using a suitable flow visual.

Expected Outcome: Shows common transitions between recorded activities.

A specialised Sankey visual may require an additional Power BI visual. Use only a visual that is suitable and approved for the project.

Visual 10 — Activity Frequency

Property| Specification
Visual Name| Activity Frequency
Visual Type| Bar Chart
Data Source| EventLog
Category| Activity
Value| Event count
Purpose| Compares the frequency of recorded activities.

Expected Outcome: Identifies activities that occur more frequently in the selected cases.

Visual 11 — Case Activity Details

Property| Specification
Visual Name| Case Activity Details
Visual Type| Table
Data Source| EventLog
Fields| Case ID, activity, timestamp, event index
Purpose| Displays the recorded activity sequence for selected cases.

Expected Outcome: Allows users to examine the event history of an individual case.

Visual 12 — Patient Journey KPI Cards

KPI| Purpose
Selected Cases| Number of cases in the current filter context
Recorded Activities| Number of event records in the selected context
Distinct Activities| Number of unique activity labels
Observed Transitions| Number of consecutive activity transitions

Expected Outcome: Provides a compact summary of the selected patient journey data.

---

5. Page 3 — Case Duration Analysis

Purpose

The Case Duration page examines the elapsed time between the first and last recorded events for each case.

It helps users explore variation in recorded process duration.

Visual 13 — Average Case Duration

Property| Specification
Visual Name| Average Case Duration
Visual Type| Card
Data Source| CasesSummary
Field| duration_days
Calculation| Average
Purpose| Displays average recorded case duration.

Visual 14 — Median Case Duration

Property| Specification
Visual Name| Median Case Duration
Visual Type| Card
Data Source| CasesSummary
Field| duration_days
Calculation| Median
Purpose| Displays the middle recorded duration value.

DAX Measure:

Median Recorded Case Duration (Days) =
MEDIAN(CasesSummary[duration_days])

Visual 15 — Maximum Case Duration

Property| Specification
Visual Name| Maximum Case Duration
Visual Type| Card
Data Source| CasesSummary
Field| duration_days
Calculation| Maximum
Purpose| Displays the longest valid recorded case duration.

DAX Measure:

Maximum Recorded Case Duration (Days) =
MAX(CasesSummary[duration_days])

Visual 16 — Case Duration Distribution

Property| Specification
Visual Name| Case Duration Distribution
Visual Type| Histogram
Data Source| CasesSummary
X-Axis| Duration in days
Y-Axis| Number of cases
Purpose| Shows the distribution of recorded case durations.

Recommended Configuration:

- Create duration bins.
- Display the number of cases in each bin.
- Use meaningful bin intervals.
- Ensure invalid durations are excluded or separately identified.

Expected Outcome: Shows whether recorded case durations are concentrated within particular ranges.

Visual 17 — Case Duration Comparison

Property| Specification
Visual Name| Case Duration Comparison
Visual Type| Bar Chart
Data Source| CasesSummary
Category| Case ID
Value| Duration in days
Purpose| Compares recorded durations between selected cases.

Expected Outcome: Identifies cases with relatively shorter or longer recorded durations.

Visual 18 — Case Duration Details

Property| Specification
Visual Name| Case Duration Details
Visual Type| Table
Data Source| CasesSummary
Fields| Case ID, start timestamp, end timestamp, duration
Purpose| Provides detailed duration information.

Expected Outcome: Allows users to inspect calculated duration values at case level.

---

6. Page 4 — Laboratory Analysis

Purpose

The Laboratory Analysis page explores available clinical measurement records.

The prepared dataset documents three measurement types:

- Leucocytes
- CRP
- LacticAcid

The visualisations should help users examine measurement availability, recorded values, and trends.

Visual 19 — Total Measurements

Property| Specification
Visual Name| Total Measurements
Visual Type| Card
Data Source| EventMeasurements
Calculation| Count of measurement rows
Purpose| Displays the number of recorded measurements.

Visual 20 — Measurement Trends

Property| Specification
Visual Name| Measurement Trends
Visual Type| Line Chart
Data Source| EventMeasurements
X-Axis| Measurement timestamp
Y-Axis| Measurement value
Legend| Measurement type
Purpose| Explores measurement values over time.

Recommended Configuration:

- Use the correct measurement timestamp.
- Display measurement type as the legend.
- Preserve the original measurement units.
- Avoid combining different measurement scales on an inappropriate common axis.

Expected Outcome: Shows how recorded measurement values vary over time.

Visual 21 — Measurements by Type

Property| Specification
Visual Name| Measurements by Type
Visual Type| Column Chart
Data Source| EventMeasurements
X-Axis| Measurement type
Y-Axis| Measurement count
Purpose| Compares the number of recorded measurements by type.

Expected Outcome: Shows the frequency of each available measurement type.

Visual 22 — Measurement Details

Property| Specification
Visual Name| Measurement Details
Visual Type| Table
Data Source| EventMeasurements
Fields| Case ID, measurement type, measurement value, timestamp
Purpose| Displays detailed measurement records.

Expected Outcome: Allows users to inspect the available measurement information.

Visual 23 — Measurement Type Distribution

Property| Specification
Visual Name| Measurement Type Distribution
Visual Type| Donut Chart
Data Source| EventMeasurements
Category| Measurement type
Value| Measurement count
Purpose| Displays the proportion of records belonging to each measurement type.

Expected Outcome: Provides a quick view of the distribution of measurement records.

Use this chart for record counts, not for comparing the clinical magnitude of different measurements.

---

7. Page 5 — Data Quality

Purpose

The Data Quality page communicates the results of data preparation and validation.

It helps users understand the completeness and reliability of the data used in the dashboard.

Visual 24 — Total Records Checked

Property| Specification
Visual Name| Total Records Checked
Visual Type| Card
Data Source| Validation Results
Calculation| Count of records checked
Purpose| Displays the number of records included in the validation process.

Visual 25 — Missing Values Summary

Property| Specification
Visual Name| Missing Values
Visual Type| Bar Chart
Data Source| Validation Results
Category| Field name
Value| Missing-value count
Purpose| Identifies fields with missing values.

Expected Outcome: Highlights fields that require additional data-quality attention.

Visual 26 — Duplicate Records

Property| Specification
Visual Name| Duplicate Records
Visual Type| Card and Table
Data Source| Validation Results
Fields| Table name, duplicate count, validation status
Purpose| Summarises identified duplicate records.

Expected Outcome: Shows the results of duplicate-record checks.

A duplicate must be defined using appropriate keys and business rules. Repeated activity names or repeated measurement types are not automatically duplicates.

Visual 27 — Validation Results

Property| Specification
Visual Name| Validation Results
Visual Type| Table
Data Source| Validation Results
Fields| Check name, table, result, status, notes
Purpose| Documents the results of data-quality checks.

Expected Outcome: Provides a detailed record of the validation process.

Visual 28 — Data Quality Summary

Property| Specification
Visual Name| Data Quality Summary
Visual Type| KPI Cards
Data Source| Validation Results
Metrics| Missing values, duplicate records, validation issues
Purpose| Provides a compact summary of data quality.

Expected Outcome: Gives users a quick understanding of the validation results.

The validation results table may need to be created during data preparation. These metrics should not be presented as available until they have been calculated.

---

8. Interactive Filters and Slicers

Interactive filters allow users to explore specific sections of the dataset.

Filter Name| Field| Purpose
Event Date| Event timestamp| Filter activities by date
Case Identifier| case_id| Select individual cases
Activity Name| activity| Filter selected activities
Measurement Type| Measurement type| Select a laboratory measurement
Case Category| Available case attribute| Explore selected case categories

Filter Design Guidelines

- Use dropdown slicers for long category lists.
- Use date-range slicers for timestamps.
- Keep important filters in consistent positions.
- Ensure filters affect only the intended visuals.
- Test interactions between report pages where applicable.

---

9. Visual Design Standards

All dashboard pages should follow consistent design principles.

9.1 Colour Scheme

Use a professional healthcare-inspired colour palette.

Suggested colours:

Element| Suggested Colour
Dashboard Background| Light Grey
KPI Cards| White
Primary Headings| Dark Blue
Main Charts| Blue
Secondary Charts| Teal
Positive Validation Status| Green
Warning Status| Amber
Error Status| Red

Use colours consistently and ensure that meaning is not communicated by colour alone.

9.2 Typography

- Use clear and readable fonts.
- Keep page titles prominent.
- Use consistent font sizes.
- Avoid excessive text inside charts.
- Use meaningful axis labels and units.

9.3 Chart Formatting

- Display clear chart titles.
- Use appropriate number formats.
- Sort categorical charts meaningfully.
- Avoid unnecessary 3D effects.
- Avoid misleading axis scales.
- Use data labels only where they improve readability.

---

10. Visual-to-Data Mapping

The following table summarises the main relationship between dashboard visuals and their data sources.

Dashboard Page| Visual| Data Source
Executive Overview| Total Cases| DimCase
Executive Overview| Total Events| EventLog
Executive Overview| Total Measurements| EventMeasurements
Executive Overview| Average Duration| CasesSummary
Executive Overview| Activity Trends| EventLog
Executive Overview| Most Frequent Activities| EventLog
Patient Journey| Activity Flow| EventLog
Patient Journey| Activity Frequency| EventLog
Patient Journey| Case Activity Details| EventLog
Case Duration| Average Duration| CasesSummary
Case Duration| Median Duration| CasesSummary
Case Duration| Duration Distribution| CasesSummary
Laboratory Analysis| Measurement Trends| EventMeasurements
Laboratory Analysis| Measurements by Type| EventMeasurements
Laboratory Analysis| Measurement Details| EventMeasurements
Data Quality| Missing Values| Validation Results
Data Quality| Duplicate Records| Validation Results
Data Quality| Validation Summary| Validation Results

---

11. Visual Validation Requirements

Before a visual is considered complete, verify the following:

1. The correct source table is used.
2. The correct fields are assigned to the visual.
3. The aggregation is appropriate.
4. The displayed values match the source data.
5. The visual responds correctly to filters.
6. The title accurately describes the information.
7. The axis labels and units are correct.
8. The visual does not unintentionally double-count records.
9. The visual is readable and properly formatted.
10. Any limitations are documented.

---

12. Performance and Usability

To maintain a responsive dashboard:

- Avoid unnecessary visuals on a single page.
- Use efficient DAX measures.
- Avoid unnecessary calculated columns.
- Keep relationships simple and well-defined.
- Use appropriate data types.
- Avoid excessive cross-filtering.
- Limit the number of categories displayed in complex charts.
- Use drill-through pages where detailed exploration is necessary.

---

13. Implementation Status

The following table tracks the implementation of the planned visuals.

Dashboard Page| Design Status| Implementation Status
Executive Overview| Designed| Pending
Patient Journey| Designed| Pending
Case Duration| Designed| Pending
Laboratory Analysis| Designed| Pending
Data Quality| Designed| Pending

Update the implementation status only after the corresponding visual has been created and tested in Power BI.

---

14. Related Documentation

File| Purpose
"README.md"| Overall dashboard design
"dashboard_layout.md"| Dashboard page layouts
"visual_catalog.md"| Detailed visual specifications
"../data_model/data_model.md"| Data model documentation
"../dax_measures/measures.dax"| DAX calculations
"../screenshots/README.md"| Dashboard screenshot documentation
"../exports/README.md"| Exported report documentation

---

15. Expected Outcome

The completed visual catalog will serve as a technical reference for developing the CareFlow Process Mining Power BI dashboard.

It will ensure that every report page has a clearly defined purpose, suitable visualisation type, appropriate data source, and validated calculation.

The final dashboard will provide an interactive view of healthcare process patterns and support the exploration of recorded patient activities, case durations, laboratory measurements, and data-quality results.

---

Project: CareFlow Process Mining
Component: Power BI Report Design
Directory: "powerbi/report_design/"
Document: "visual_catalog.md"
