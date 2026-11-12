CareFlow Process Mining — Power BI Report Design

1. Overview

This document defines the design and visualisation specifications for the Power BI dashboard developed as part of the CareFlow Process Mining project.

The dashboard uses sepsis patient event-log data to explore healthcare activities, patient journeys, recorded case durations, laboratory measurements, and data quality.

The report is designed to present analytical results through interactive charts, KPI cards, tables, and filters in a structured and professional format.

Project: CareFlow Process Mining
Component: Power BI Dashboard
Domain: Healthcare Analytics and Process Mining
Report Type: Interactive Business Intelligence Dashboard
Status: Design and development in progress

---

2. Dashboard Objectives

The primary objectives are to:

- Provide an overview of recorded patient cases and healthcare activities.
- Explore patient journeys and activity transitions.
- Analyse the duration of recorded patient cases.
- Examine available laboratory measurements and trends.
- Identify missing values, duplicate records, and data validation issues.
- Present key performance indicators through interactive visuals.
- Support data-driven exploration of healthcare process patterns.

---

3. Report Pages

The dashboard is planned to contain five report pages.

Page No.| Report Page| Main Visualisations
1| Executive Overview| KPI cards, bar charts, trend charts, and summary tables
2| Patient Journey| Process-flow visualisations and activity transitions
3| Case Duration| Duration distribution, KPI cards, and case tables
4| Laboratory Analysis| Measurement charts, trends, and tables
5| Data Quality| Missing values, duplicate records, and validation results

The final implementation will depend on the verified dataset structure and the availability of suitable fields for each visualisation.

---

4. Page 1 — Executive Overview

Purpose

Provide a high-level summary of the available sepsis event-log data.

Planned KPI Cards

- Total Cases
- Total Events
- Total Measurements
- Average Recorded Case Duration

Planned Visualisations

Visual| Chart Type| Purpose
Activity Trends| Line Chart| Explore recorded activity volume over time
Most Frequent Activities| Bar Chart| Rank activities by event frequency
Case Summary| Table| Display selected case-level information
Activity Summary| Table| Summarise recorded activities and their counts

Layout

+---------------------------------------------------------+
|        CAREFLOW PROCESS MINING                          |
|        EXECUTIVE OVERVIEW                               |
+---------------------------------------------------------+
| Date Filter | Activity Filter | Case Filter              |
+---------------------------------------------------------+
| Total Cases | Total Events | Measurements | Avg Duration|
+---------------------------------------------------------+
|                                                         |
| Activity Trends             Most Frequent Activities   |
| Line Chart                  Bar Chart                  |
|                                                         |
+-----------------------------+---------------------------+
| Case Summary                | Activity Summary          |
| Table                       | Table                     |
+-----------------------------+---------------------------+

Expected Outcome

Provide a quick understanding of the dataset size, activity distribution, and recorded process patterns.

---

5. Page 2 — Patient Journey

Purpose

Explore the sequence of recorded activities associated with individual patient cases.

Planned Visualisations

Visual| Chart Type| Purpose
Activity Transitions| Flow or Sankey Diagram| Explore transitions between recorded activities
Activity Frequency| Bar Chart| Compare the frequency of activities
Case Activity Details| Table| Display activities associated with selected cases
Journey Summary| KPI Cards| Summarise selected case and activity metrics

Layout

+---------------------------------------------------------+
|                  PATIENT JOURNEY                        |
+---------------------------------------------------------+
| Case Filter | Date Filter | Activity Filter             |
+---------------------------------------------------------+
| Cases Analysed | Activities Recorded | Transitions       |
+---------------------------------------------------------+
|                                                         |
|          Patient Activity Flow                          |
|          Flow / Sankey Diagram                          |
|                                                         |
+-----------------------------+---------------------------+
| Activity Frequency          | Case Activity Details     |
| Bar Chart                   | Table                     |
+-----------------------------+---------------------------+

Expected Outcome

Help users explore how recorded activities follow one another within the event log.

Note: Activity transitions represent recorded sequences. They do not, by themselves, establish clinical causation or the quality of care.

---

6. Page 3 — Case Duration

Purpose

Analyse elapsed time between the first and last recorded events for each case.

Planned KPI Cards

- Cases Analysed
- Average Recorded Case Duration
- Median Recorded Case Duration
- Longest Recorded Case Duration

Planned Visualisations

Visual| Chart Type| Purpose
Duration Distribution| Histogram| Examine variation in recorded case durations
Case Duration Comparison| Bar Chart| Compare selected cases or appropriate groups
Case Duration Details| Table| Display case identifiers and calculated durations
Duration Summary| KPI Cards| Present summary statistics

Layout

+---------------------------------------------------------+
|                 CASE DURATION ANALYSIS                  |
+---------------------------------------------------------+
| Date Filter | Case Filter                               |
+---------------------------------------------------------+
| Cases Analysed | Average | Median | Maximum Duration    |
+---------------------------------------------------------+
|                                                         |
|          Recorded Case Duration Distribution            |
|          Histogram                                      |
|                                                         |
+-----------------------------+---------------------------+
| Duration Comparison         | Case Duration Details     |
| Bar Chart                   | Table                     |
+-----------------------------+---------------------------+

Duration Calculation

For each case:

"Recorded Case Duration = Last Event Timestamp - First Event Timestamp"

The timestamps must be valid and correctly ordered before calculating the duration.

Expected Outcome

Identify variation in recorded case durations and cases that may require further investigation.

Important: Recorded case duration should not automatically be interpreted as total hospital length of stay, treatment duration, or recovery time.

---

7. Page 4 — Laboratory Analysis

Purpose

Explore the clinical measurements available in the source dataset.

Planned Visualisations

Visual| Chart Type| Purpose
Measurement Trends| Line Chart| Explore measurement values over time
Measurements by Type| Bar Chart| Compare measurement counts by type
Measurement Details| Table| Display recorded measurement information
Measurement Summary| KPI Cards| Summarise available measurement records

Layout

+---------------------------------------------------------+
|                 LABORATORY ANALYSIS                     |
+---------------------------------------------------------+
| Date Filter | Case Filter | Measurement Type Filter     |
+---------------------------------------------------------+
| Total Measurements | Measurement Types | Cases           |
+---------------------------------------------------------+
|                                                         |
|          Measurement Trends Over Time                   |
|          Line Chart                                     |
|                                                         |
+-----------------------------+---------------------------+
| Measurements by Type        | Measurement Details       |
| Bar Chart                   | Table                     |
+-----------------------------+---------------------------+

Expected Outcome

Explore the distribution and recorded trends of available laboratory measurements.

Measurement units, timestamps, and case relationships must be verified before comparisons are made.

Clinical reference ranges must not be invented. Any clinical interpretation requires appropriate medical context.

---

8. Page 5 — Data Quality

Purpose

Present the results of data-quality checks performed during data preparation and validation.

Planned KPI Cards

- Total Records Checked
- Missing Values Identified
- Duplicate Records Identified
- Validation Issues Identified

These metrics must be calculated from actual validation results.

Planned Visualisations

Visual| Chart Type| Purpose
Missing Values| Bar Chart| Compare missing values across relevant fields
Duplicate Records| KPI Card or Table| Summarise identified duplicates
Validation Results| Table| Display validation checks and their results
Data Quality Summary| KPI Cards| Present verified quality metrics

Layout

+---------------------------------------------------------+
|                    DATA QUALITY                         |
+---------------------------------------------------------+
| Dataset Filter | Table Filter                           |
+---------------------------------------------------------+
| Records Checked | Missing Values | Duplicates | Issues  |
+---------------------------------------------------------+
|                                                         |
| Missing Values by Field                                 |
| Bar Chart                                               |
|                                                         |
+-----------------------------+---------------------------+
| Validation Summary          | Data Quality Details      |
| KPI / Table                 | Table                     |
+-----------------------------+---------------------------+

Expected Outcome

Make data-quality issues visible and document the reliability of the data used in the other dashboard pages.

Missing values and duplicates must be defined consistently. For example, a repeated event row should not automatically be considered a duplicate unless the validation rules support that conclusion.

---

9. Interactive Filters

The report may include the following slicers, depending on the available columns.

Filter| Purpose
Event Date| Restrict analysis to a selected period
Case Identifier| Explore an individual patient case
Activity Name| Filter recorded activities
Measurement Type| Select a laboratory measurement
Other Available Categories| Support additional analysis where appropriate

Filters should be configured so that they affect the intended visuals without producing misleading results.

---

10. Visual Design Standards

The following principles will guide dashboard development:

- Maintain a consistent visual theme across all five pages.
- Use KPI cards for important summary metrics.
- Use line charts for time-based trends.
- Use bar charts for comparisons between categories.
- Use tables for detailed records and validation results.
- Use clear titles, labels, legends, and measurement units.
- Keep layouts organised and avoid unnecessary visual clutter.
- Use consistent number and date formats.
- Ensure chart scales support accurate interpretation.
- Validate calculations against the source data.

---

11. Data Model Requirements

The report may use the following logical data entities:

- Event Log
- Case Attributes
- Event Measurements

The actual table names and relationships must be confirmed from the workbook.

Relationships should use appropriate keys and account for the granularity of each table. Calculations must avoid unintended duplication when event records and measurement records are combined.

The detailed data model will be documented in "../data_model/data_model.md".

---

12. DAX Measures

DAX measures will be created for metrics such as:

- Total distinct cases
- Total recorded events
- Total measurement records
- Average recorded case duration
- Median recorded case duration
- Activity frequency
- Missing-value counts
- Validated duplicate counts

Each measure must use the actual imported table and column names.

The formulas will be maintained in "../dax_measures/measures.dax" and validated before being used in the final report.

---

13. Testing and Validation

Before considering the dashboard complete, verify that:

1. KPI values match independently calculated results.
2. Distinct case counts are correct.
3. Event counts are not unintentionally duplicated.
4. Activity frequencies match the source data.
5. Duration calculations use valid timestamps.
6. Measurement values retain their correct units.
7. Missing-value and duplicate counts follow documented rules.
8. Slicers filter the intended visuals correctly.
9. Charts display accurate and readable information.
10. Dashboard screenshots represent the actual completed report.

---

14. Design Deliverables

The "report_design/" directory will contain:

File| Purpose
"README.md"| Overall dashboard design and visualisation specifications
"dashboard_layout.md"| Page layouts and placement of visuals
"visual_catalog.md"| Detailed descriptions of individual dashboard visuals

Additional documentation may be added when required.

---

15. Development Status

Current status: Dashboard design specification prepared; implementation and validation pending.

The design will be updated as the report is developed and tested. Planned visuals must not be presented as completed results.

The dashboard will be considered complete only after its visuals, calculations, filters, and data relationships have been implemented and validated.

---

16. Expected Outcome

The completed Power BI dashboard is intended to provide an interactive view of the sepsis event-log data, supporting exploration of:

- Recorded patient journeys.
- Healthcare activity patterns.
- Recorded case durations.
- Available laboratory measurements.
- Data-quality and validation results.

The dashboard will complement the project's data-processing and process-mining components by presenting validated analytical results in an accessible visual format.

---

Project: CareFlow Process Mining
Component: Power BI Report Design
Directory: "powerbi/report_design/"
Document: "README.md"
