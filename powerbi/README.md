CareFlow Process Mining — Power BI Dashboard

1. Overview

The "powerbi/" directory contains the resources required to design, develop, document, and maintain the Power BI dashboard for the CareFlow Process Mining project.

The dashboard focuses on analysing sepsis patient event-log data to explore patient journeys, recorded hospital activities, case durations, and operational patterns.

The objective is to transform structured healthcare event data into meaningful visual insights using interactive charts, KPI cards, tables, and filters.

Project: CareFlow Process Mining
Component: Power BI Dashboard
Domain: Healthcare Process Mining and Data Analytics
Status: Dashboard development in progress

2. Objectives

The Power BI dashboard aims to:

- Analyse patient cases and recorded healthcare activities.
- Identify frequently occurring hospital activities.
- Explore activity patterns over time.
- Analyse the duration of recorded patient cases.
- Present key metrics through KPI cards.
- Enable interactive exploration using filters and slicers.
- Support data-driven investigation of healthcare process patterns.
- Present analytical results through clear and informative visualisations.

3. Directory Structure

powerbi/
│
├── README.md
│
├── dashboard/
│   └── README.md
│
├── report_design/
│   ├── dashboard_layout.md
│   └── visual_catalog.md
│
├── screenshots/
│   └── README.md
│
├── exports/
│   └── README.md
│
├── data_model/
│   └── data_model.md
│
├── dax_measures/
│   └── measures.dax
│
└── careflow_dashboard.pbix

Note: This is the planned directory structure. Add files as the corresponding development work is completed. The ".pbix" file will be created when the actual Power BI report is built and saved.

4. Dataset

The dashboard will use the cleaned sepsis event-log dataset prepared for the project.

Expected dataset filename: "Sepsis_Cases_Event_Log_Cleaned_for_Visualization.xlsx"

The available data may include:

- Patient case identifiers.
- Recorded activity names.
- Event timestamps.
- Case attributes.
- Clinical measurement records.

The exact columns, data types, relationships, and available metrics must be verified against the source workbook before creating the report.

The dataset should be validated to identify missing values, duplicate records, inconsistent timestamps, and other data-quality issues that could affect the analysis.

5. Planned Dashboard Pages

5.1 Overview Dashboard

Provides a summary of the available event-log data.

Planned visuals:

- Total patient cases.
- Total recorded events.
- Total recorded measurements, where available.
- Average recorded case duration.
- Activity trends over time.
- Summary tables.
- Interactive filters.

5.2 Patient Activity Analysis

Explores the frequency and distribution of recorded healthcare activities.

Planned visuals:

- Bar chart of the most frequent activities.
- Activity distribution chart.
- Activity trends over time.
- Table of activity counts.
- Filters for available activity and date fields.

5.3 Case Duration Analysis

Examines the elapsed time between the first and last recorded events for each patient case.

Planned visuals:

- Average recorded case duration.
- Case-duration distribution.
- Case-duration comparisons.
- Table of case-level duration metrics.

Interpretation: Recorded event-log duration is not necessarily equivalent to total hospital length of stay or the duration of a patient's clinical condition.

6. Data Model

The data model will be designed based on the actual structure of the source dataset.

Potential data entities include:

Data Entity| Purpose
Event Log| Stores case identifiers, activity names, and event timestamps.
Case Attributes| Stores available case-level information.
Event Measurements| Stores available clinical measurements and associated timestamps.

These entities are conceptual until the workbook structure is verified.

Relationships will be established using appropriate keys and validated to prevent duplicated records and incorrect calculations.

The data model documentation will be maintained in "data_model/data_model.md".

7. DAX Measures

DAX (Data Analysis Expressions) will be used to calculate metrics for the dashboard.

Potential measures include:

- Total distinct patient cases.
- Total recorded events.
- Total recorded measurements.
- Average recorded case duration.
- Activity frequency.
- Case counts by selected categories.

Each measure must use the correct table names, column names, data types, and counting logic.

The formulas will be stored in "dax_measures/measures.dax" and validated against the source data before being used in the final dashboard.

8. Report Design and Visualisation

The "report_design/" directory will document the layout and specifications of the dashboard.

The visualisation approach will follow these principles:

- Use KPI cards for important summary metrics.
- Use bar charts to compare activity frequencies.
- Use line charts to explore trends over time.
- Use tables for detailed case and activity information.
- Use slicers to enable interactive filtering.
- Apply consistent formatting and readable labels.
- Avoid misleading chart scales and unsupported conclusions.
- Validate visual results against the underlying data.

The files "dashboard_layout.md" and "visual_catalog.md" will describe the planned report layout and individual visuals.

9. Dashboard Screenshots

The "screenshots/" directory will contain screenshots of the actual Power BI report.

Suggested screenshot filenames:

screenshots/
├── overview_dashboard.png
├── patient_activity_analysis.png
└── case_duration_analysis.png

These images should be added after the corresponding visuals have been created.

Screenshots are intended for project documentation, progress reporting, and presentation purposes.

10. Report Exports

The "exports/" directory will store approved exports generated from the dashboard.

Examples include:

- PDF reports.
- Static report snapshots.
- Other appropriate presentation deliverables.

Only genuine outputs generated during development should be stored here.

Sensitive or confidential patient information must not be published without appropriate authorisation.

11. Technology Stack

Technology| Purpose
Microsoft Power BI| Dashboard creation and data visualisation.
DAX| Calculated measures and analytical expressions.
Microsoft Excel| Source dataset format.
Git| Version control.
GitHub| Repository hosting and project collaboration.
Python| Supporting data processing and validation, where required.

Python-based data processing and automated tests are maintained separately in the project's "src/" and "tests/" directories.

12. Development Workflow

The dashboard development process follows these stages:

1. Inspect and validate the cleaned dataset.
2. Identify the relevant tables, columns, and data types.
3. Import the dataset into a compatible Power BI authoring environment.
4. Design the data model and validate table relationships.
5. Create and verify the required DAX measures.
6. Develop the dashboard pages and visualisations.
7. Test filters, calculations, and displayed values.
8. Capture screenshots of completed dashboard pages.
9. Export reports when required.
10. Document the implementation and commit supporting files to GitHub.

13. Version Control and Data Protection

GitHub will be used to maintain the Power BI documentation and supporting project assets.

Recommended practices:

- Use meaningful commit messages.
- Commit completed work regularly.
- Keep documentation consistent with the implementation.
- Avoid committing credentials or access tokens.
- Do not publish confidential patient information.
- Verify dataset permissions before uploading data.
- Review exported reports and screenshots before committing them.

A ".pbix" file may contain imported data. Check its contents and applicable data-sharing restrictions before adding it to a public repository.

14. Current Status

Current stage: Dashboard planning and setup.

The report structure, data model, DAX measures, and visualisations will be developed and validated incrementally.

The dashboard should only be marked as completed after the report has been created, the calculations have been verified, and the intended functionality has been tested.

15. Expected Outcome

The expected outcome is an interactive dashboard that presents the available sepsis event-log data in a clear and structured format.

It will help users explore recorded patient journeys, activity frequencies, case durations, and other supported process metrics.

The dashboard is intended for process analysis and reporting. Any clinical or operational conclusions must be based on validated data and appropriate domain interpretation.

---

Repository: "Rajeev/careflow-process-mining"
Project: CareFlow Process Mining
Component: Power BI Dashboard
Purpose: Healthcare Process Analysis and Visualisation
