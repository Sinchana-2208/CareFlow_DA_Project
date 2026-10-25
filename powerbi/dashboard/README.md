CareFlow Process Mining — Dashboard Design

1. Overview

This document describes the proposed layout and visualisation design for the Power BI dashboard developed as part of the CareFlow Process Mining project.

The dashboard will analyse the available sepsis patient event-log data to explore recorded patient journeys, healthcare activities, case durations, and clinical measurement patterns.

The design focuses on presenting meaningful information through interactive visualisations, key performance indicators (KPIs), tables, and filters.

Dashboard: CareFlow Process Mining
Platform: Microsoft Power BI
Domain: Healthcare Analytics and Process Mining
Status: Design specification

---

2. Dashboard Objectives

The dashboard is designed to:

- Provide an overview of patient cases and recorded activities.
- Identify frequently occurring healthcare activities.
- Analyse activity trends over time.
- Examine the duration of recorded patient cases.
- Explore available clinical measurements.
- Enable users to filter and investigate the dataset.
- Present analytical findings in a clear and professional format.

---

3. Dashboard Structure

The dashboard is planned to contain four report pages.

Page| Name| Purpose
1| Overview Dashboard| Summarise the dataset using KPI cards and charts.
2| Patient Activity Analysis| Examine activity frequency and distribution.
3| Case Duration Analysis| Analyse elapsed time between recorded case events.
4| Clinical Measurements| Explore available clinical measurement data.

The final page structure will depend on the verified dataset fields and the metrics that can be calculated reliably.

---

4. Page 1 — Overview Dashboard

Purpose

Provide a high-level summary of the available event-log data.

Layout

+-----------------------------------------------------------+
|             CAREFLOW PROCESS MINING                       |
|             Healthcare Analytics Dashboard                |
+-----------------------------------------------------------+
| Date Filter | Activity Filter | Other Available Filters   |
+-----------------------------------------------------------+
| Total Cases | Total Events | Total Measurements | Avg     |
|             |              |                   | Duration |
+-----------------------------------------------------------+
|                                                           |
|       Activity Trends Over Time                           |
|                    Line Chart                             |
|                                                           |
+-------------------------------+---------------------------+
| Most Frequent Activities      | Case Summary              |
| Bar Chart                     | Table                     |
+-------------------------------+---------------------------+

Planned Visuals

KPI cards

- Total distinct patient cases.
- Total recorded events.
- Total recorded measurements.
- Average recorded case duration.

Line chart

- Displays recorded activity volume over time.
- Uses the event timestamp as the time dimension.

Bar chart

- Compares the frequency of recorded activities.
- Helps identify commonly occurring activities.

Table

- Displays relevant case-level summary information.
- Includes only fields available and validated in the dataset.

Expected Insight

Users can quickly understand the size of the dataset, the distribution of recorded activities, and the general patterns visible in the event log.

---

5. Page 2 — Patient Activity Analysis

Purpose

Investigate how frequently healthcare activities occur and how their distribution varies across the recorded data.

Layout

+-----------------------------------------------------------+
|                PATIENT ACTIVITY ANALYSIS                  |
+-----------------------------------------------------------+
| Date Filter | Activity Filter | Case Filter               |
+-----------------------------------------------------------+
| Total Activities | Distinct Activities | Cases Represented |
+-----------------------------------------------------------+
|                                                           |
|           Most Frequent Activities                        |
|                  Horizontal Bar Chart                     |
|                                                           |
+-------------------------------+---------------------------+
| Activity Distribution         | Activity Details          |
| Chart                         | Table                     |
+-------------------------------+---------------------------+

Planned Visuals

- Horizontal bar chart: Ranks activities by event count.
- Activity distribution chart: Shows how recorded events are distributed among activity categories.
- Activity details table: Displays activity names and corresponding counts.
- Date-based chart: Shows activity counts over time.

Expected Insight

This page will help identify frequently recorded activities and explore changes in activity patterns.

Event frequency alone does not establish that an activity is clinically important or that a healthcare process is efficient.

---

6. Page 3 — Case Duration Analysis

Purpose

Examine the elapsed time between the first and last recorded events for each case.

Layout

+-----------------------------------------------------------+
|                 CASE DURATION ANALYSIS                   |
+-----------------------------------------------------------+
| Date Filter | Case Filter | Other Available Filters       |
+-----------------------------------------------------------+
| Cases Analysed | Average Duration | Median Duration       |
+-----------------------------------------------------------+
|                                                           |
|              Case Duration Distribution                  |
|                     Histogram                             |
|                                                           |
+-------------------------------+---------------------------+
| Duration Comparison           | Case Duration Details     |
| Bar Chart                     | Table                     |
+-------------------------------+---------------------------+

Planned Visuals

- KPI cards: Number of cases analysed and average or median recorded duration.
- Histogram: Shows the distribution of recorded case durations.
- Bar chart: Compares durations for selected cases or appropriate categories.
- Table: Lists case identifiers, first recorded event, last recorded event, and calculated duration.

Duration Calculation

For each case:

"Recorded Case Duration = Last Event Timestamp - First Event Timestamp"

Expected Insight

Users can examine variation in recorded case durations and identify cases that may require further investigation.

Important: Recorded case duration is not automatically equivalent to total hospital length of stay, treatment duration, or recovery time.

---

7. Page 4 — Clinical Measurements

Purpose

Explore the clinical measurement data available in the dataset.

The source workbook should be inspected to confirm the measurement names, values, timestamps, units, and relationships with patient cases before the final design is implemented.

Layout

+-----------------------------------------------------------+
|                  CLINICAL MEASUREMENTS                    |
+-----------------------------------------------------------+
| Date Filter | Case Filter | Measurement Type Filter       |
+-----------------------------------------------------------+
| Total Measurements | Measurement Types | Cases Represented|
+-----------------------------------------------------------+
|                                                           |
|          Measurement Trends Over Time                     |
|                    Line Chart                             |
|                                                           |
+-------------------------------+---------------------------+
| Measurements by Type          | Measurement Details       |
| Bar Chart                     | Table                     |
+-------------------------------+---------------------------+

Planned Visuals

- Line chart: Displays measurement values over time when the data supports meaningful comparisons.
- Bar chart: Compares measurement counts by measurement type.
- Table: Displays case identifiers, measurement types, timestamps, and values.
- Filters: Allow users to select available measurement types and date ranges.

Expected Insight

Users can explore recorded measurement patterns and their distribution across cases and time.

Clinical interpretation requires appropriate medical context, validated units, and suitable reference ranges. The dashboard must not invent clinical thresholds or provide unsupported diagnoses.

---

8. Filters and Interactivity

Where supported by the data model, the dashboard will include slicers for:

Filter| Purpose
Event Date| Restricts analysis to a selected time range.
Activity| Displays selected activity categories.
Case Identifier| Focuses on a specific patient case.
Measurement Type| Filters available clinical measurements.

Filters should behave consistently across relevant visuals.

Selecting a category in one chart should filter other visuals when the report's interaction settings and data relationships support that behaviour.

---

9. Visualisation Standards

The following design standards will guide report development:

- Use a consistent colour palette across all report pages.
- Keep KPI cards near the top of each page.
- Use readable titles, labels, and legends.
- Choose chart types appropriate to the underlying data.
- Use line charts for trends over time.
- Use bar charts for category comparisons.
- Use tables for detailed records.
- Avoid unnecessary visual clutter.
- Display suitable date formats and measurement units.
- Avoid misleading scales and unsupported comparisons.
- Validate calculations before publishing the report.

---

10. Data Requirements

Before implementing the dashboard, verify the following:

- Case identifiers are available and consistently formatted.
- Event timestamps are valid and correctly typed.
- Activity names are available for activity analysis.
- Clinical measurement fields are present where required.
- Duplicate records are understood and handled appropriately.
- Missing values are assessed before calculations.
- Relationships between event, case, and measurement data are valid.
- Case durations are calculated using the correct timestamps.

The dashboard must use the actual dataset structure rather than assumed column names.

---

11. Testing and Validation

The completed dashboard should be tested to confirm that:

1. KPI cards display correct values.
2. Case and event counts match independently verified calculations.
3. Date filters return the expected records.
4. Activity counts agree with the source data.
5. Case-duration calculations use the correct timestamps.
6. Measurement charts display appropriate units and values.
7. Table relationships do not cause unintended duplication.
8. Interactive filters work as expected.
9. Visuals remain readable when filters are applied.

---

12. Expected Outcome

The proposed dashboard will provide a structured visual interface for exploring the sepsis event-log dataset.

It is intended to support investigation of:

- Recorded patient activity patterns.
- Frequently occurring healthcare activities.
- Variations in recorded case durations.
- Available clinical measurement patterns.
- Differences across selected cases and time periods.

The dashboard will complement the project's data-processing and process-mining components by making validated analytical results easier to explore and communicate.

---

Project: CareFlow Process Mining
Component: Power BI Dashboard Design
Directory: "powerbi/report_design/"
Document: "dashboard_layout.md"
