CareFlow Process Mining — Power BI Report Exports

1. Overview

The "exports/" directory stores report files exported from the Power BI dashboard developed for the CareFlow Process Mining project.

This directory is intended to contain static reports and presentation-ready deliverables generated from the implemented dashboard.

The exports will help communicate analytical findings about the sepsis event-log dataset, including recorded patient activities, patient journey patterns, case durations, laboratory measurements, and data-quality results.

Project: CareFlow Process Mining
Component: Power BI Dashboard
Directory: "powerbi/exports/"
Primary Export Format: PDF
Status: Export documentation prepared; actual exports will be added when available.

---

2. Purpose

The purpose of this directory is to maintain an organised collection of dashboard reports and other approved deliverables.

The exported files can be used for:

- Project demonstrations.
- Progress reports.
- Academic or organisational presentations.
- Dashboard review meetings.
- Sharing analytical findings with authorised stakeholders.
- Maintaining snapshots of completed report versions.
- Documenting project milestones.

Exported files provide a static view of the dashboard at the time of export. They do not replace the interactive Power BI report.

---

3. Directory Structure

The following structure is recommended for organising exported reports.

exports/
│
├── README.md
│
├── pdf/
│   ├── careflow_executive_overview.pdf
│   ├── careflow_patient_journey.pdf
│   ├── careflow_case_duration.pdf
│   ├── careflow_laboratory_analysis.pdf
│   └── careflow_data_quality.pdf
│
├── full_reports/
│   └── careflow_dashboard_full_report.pdf
│
└── archive/
    └── previous_report_versions/

Note: This is a proposed structure. Create the additional folders when they are useful, and add files only after generating the corresponding exports.

The "archive/" directory is optional and should be used only when previous report versions need to be retained.

---

4. Export Types

4.1 PDF Reports

PDF files are suitable for documenting completed dashboard pages and sharing static reports.

Potential exports include:

File| Description
"careflow_executive_overview.pdf"| Executive summary of the dashboard metrics and activity trends
"careflow_patient_journey.pdf"| Visual summary of recorded patient activity sequences
"careflow_case_duration.pdf"| Summary of recorded case-duration analysis
"careflow_laboratory_analysis.pdf"| Summary of available clinical measurement analysis
"careflow_data_quality.pdf"| Summary of data-quality checks and validation results
"careflow_dashboard_full_report.pdf"| Combined report containing the selected dashboard pages

These filenames describe the planned deliverables. They do not indicate that the PDF files have already been generated.

4.2 Full Dashboard Export

A combined PDF may be generated to present several or all report pages in one document.

Depending on the Power BI export options available to your account, the combined report may include:

1. Executive Overview.
2. Patient Journey.
3. Case Duration.
4. Laboratory Analysis.
5. Data Quality.

The exported pages should be reviewed to ensure that important charts, titles, tables, and values are visible.

4.3 Other Export Formats

Other formats may be included when useful and supported by the reporting workflow.

Examples include:

- CSV files containing approved tabular results.
- PNG images of selected report visuals.
- Excel files containing approved analytical summaries.

These formats should be included only when they serve a clear project purpose and comply with applicable data-sharing restrictions.

---

5. Dashboard Pages Available for Export

The project plans to develop five Power BI report pages.

5.1 Executive Overview

Purpose: Present a high-level summary of the event-log data.

Potential contents:

- Total distinct cases.
- Total recorded events.
- Total measurement records.
- Average recorded case duration.
- Activity trends.
- Most frequent activities.
- Summary tables.

5.2 Patient Journey

Purpose: Summarise recorded activity sequences and transitions.

Potential contents:

- Process-flow visualisations.
- Activity frequency charts.
- Case activity tables.
- Selected journey metrics.

5.3 Case Duration

Purpose: Present analysis of elapsed time between the first and last recorded events for each case.

Potential contents:

- Average and median recorded duration.
- Duration distribution.
- Case-duration comparisons.
- Case-level duration tables.

5.4 Laboratory Analysis

Purpose: Present analysis of the clinical measurement records available in the dataset.

Potential contents:

- Measurement trends.
- Measurement counts by type.
- Measurement detail tables.
- Relevant measurement summaries.

Clinical measurements should retain their correct units and timestamps. Clinical interpretations should not be made without suitable domain context.

5.5 Data Quality

Purpose: Communicate the results of dataset validation.

Potential contents:

- Missing-value summaries.
- Duplicate-record checks.
- Validation results.
- Data-quality tables.

All reported values must come from actual validation results.

---

6. Exporting Reports from Power BI

The exact export options depend on the Power BI environment, account permissions, report configuration, and available licensing.

A general workflow is:

Step 1: Open the Report

Open the completed CareFlow Process Mining report in Power BI.

Step 2: Validate the Dashboard

Before exporting, verify that:

- KPI calculations are correct.
- Charts display the expected results.
- Tables show the appropriate fields.
- Filters are applied as intended.
- Titles and labels are readable.
- No unintended confidential information is visible.

Step 3: Select the Export Option

Use the export functionality available in your Power BI environment.

If PDF export is available, select the appropriate report export option and review the available page and formatting settings.

Step 4: Generate the Report

Generate the export using the intended report pages and settings.

Wait for the export process to finish before saving or downloading the file.

Step 5: Save the Export

Save the exported report in the appropriate project directory.

For example:

"powerbi/exports/pdf/careflow_dashboard_full_report.pdf"

Step 6: Review the Exported File

Open the PDF and verify that:

- All intended pages are included.
- Charts and tables are readable.
- Text is not clipped.
- Page orientation is appropriate.
- Values match the source report.
- The document does not contain unintended sensitive information.

Step 7: Commit the File to GitHub

Add the approved export to the repository if it is appropriate to store and share there.

Example commit message:

"docs: add executive overview PDF export"

---

7. File Naming Convention

Use descriptive filenames that identify the report content.

Recommended conventions:

- Use lowercase letters.
- Separate words with underscores.
- Include the report page name.
- Use the ".pdf" extension for PDF reports.
- Include a version or date only when needed.

Examples:

careflow_executive_overview.pdf
careflow_patient_journey.pdf
careflow_case_duration.pdf
careflow_laboratory_analysis.pdf
careflow_data_quality.pdf
careflow_dashboard_full_report.pdf

For versioned reports, a date-based filename may be used:

"careflow_executive_overview_2026-10-28.pdf"

Use the actual export date rather than a planned or assumed date.

---

8. Export Quality Standards

All exported reports should meet the following standards.

Accuracy

The exported values must match the validated dashboard.

Readability

Charts, tables, labels, and KPI cards must be readable at the intended viewing size.

Completeness

The export must contain the intended pages and visual components.

Consistency

Formatting should remain consistent with the dashboard design.

Traceability

The report should be identifiable by its filename and, where appropriate, its export date or version.

Privacy

Only approved information should be included in exported files.

Authenticity

Exports must be generated from the actual Power BI report. Planned or illustrative reports must not be presented as completed outputs.

---

9. Report Validation Checklist

Before accepting an export, verify the following:

- [ ] The correct report was exported.
- [ ] The intended report pages are included.
- [ ] KPI values match the Power BI report.
- [ ] Chart titles and axis labels are readable.
- [ ] Tables are not unintentionally truncated.
- [ ] Applied filters are appropriate for the report's purpose.
- [ ] Dates and measurement units are displayed correctly.
- [ ] Data-quality metrics match the validation results.
- [ ] The PDF opens successfully.
- [ ] No unauthorised confidential information is exposed.
- [ ] The file uses the correct filename and location.

---

10. Version Management

When a dashboard is updated, a new export may be generated to reflect the latest validated implementation.

Recommended practices:

- Replace outdated exports when only the latest version is required.
- Retain previous versions only when there is a clear reporting or audit need.
- Use meaningful version labels or dates when necessary.
- Ensure that archived reports are clearly identified.
- Avoid keeping unnecessary duplicate exports.
- Document significant changes to exported reports.

If previous reports must be retained, use the optional "archive/" directory.

---

11. GitHub and File Management

The "exports/" directory is part of the Power BI reporting component of the project.

Recommended practices:

- Keep exported files organised by format or report type.
- Use descriptive commit messages.
- Avoid committing duplicate or obsolete files unnecessarily.
- Review repository file-size limitations before uploading large reports.
- Store sensitive exports only in approved locations.
- Follow organisational policies for handling healthcare-related information.

A PDF export may contain information imported from the source dataset. Review its contents and sharing permissions before publishing it in a public repository.

If an export contains confidential or identifiable patient information, do not upload it to a public GitHub repository.

---

12. Relationship with Other Directories

Directory| Purpose
"powerbi/dashboard/"| Dashboard-related supporting documentation and files
"powerbi/report_design/"| Dashboard layouts and visual specifications
"powerbi/screenshots/"| Screenshots of actual dashboard pages
"powerbi/data_model/"| Documentation of tables and relationships
"powerbi/dax_measures/"| DAX formulas used for dashboard calculations
"powerbi/exports/"| PDF reports and other approved exported deliverables
"powerbi/"| May contain the completed ".pbix" report when available

Screenshots and PDF exports should reflect the actual report implementation and should be kept consistent with the dashboard documentation.

---

13. Current Development Status

Status: Export documentation prepared; report exports pending.

The export directory will be populated as dashboard pages are implemented, validated, and approved for reporting.

A report should be described as exported only after the corresponding file has been generated and saved.

---

14. Expected Outcome

The completed export collection will provide a structured set of static reports derived from the CareFlow Process Mining Power BI dashboard.

These reports will support project demonstrations, progress reporting, review meetings, and communication of validated analytical findings.

The exports will complement the interactive Power BI report, its screenshots, and its technical documentation.

---

Project: CareFlow Process Mining
Component: Power BI Dashboard
Directory: "powerbi/exports/"
Document: "README.md"
