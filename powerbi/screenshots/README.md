CareFlow Process Mining — Dashboard Screenshots

1. Overview

The "screenshots/" directory stores screenshots of the Power BI dashboard developed for the CareFlow Process Mining project.

These screenshots provide visual evidence of the dashboard implementation, including report pages, KPI cards, charts, tables, filters, and other visual components.

The screenshots will be used for:

- Project documentation.
- GitHub repository presentation.
- Development progress tracking.
- Weekly progress reports.
- Project demonstrations and presentations.
- Verification of implemented dashboard features.

Project: CareFlow Process Mining
Component: Power BI Dashboard
Directory: "powerbi/screenshots/"
Status: Screenshots will be added as dashboard pages are implemented.

---

2. Purpose of This Directory

The purpose of this directory is to maintain an organised collection of screenshots representing the actual Power BI dashboard.

Each screenshot should:

- Represent a genuine dashboard page or visual.
- Have a clear and descriptive filename.
- Be captured after the relevant visual has been implemented.
- Display readable titles, labels, and values.
- Correspond to the documented dashboard design.
- Avoid exposing confidential or sensitive patient information.

Screenshots are supporting documentation. They do not replace the interactive Power BI report.

---

3. Planned Screenshot Structure

The following structure is recommended for organising screenshots.

screenshots/
│
├── README.md
│
├── 01_executive_overview.png
│
├── 02_patient_journey.png
│
├── 03_case_duration.png
│
├── 04_laboratory_analysis.png
│
├── 05_data_quality.png
│
└── additional_visuals/
    ├── kpi_cards.png
    ├── activity_analysis.png
    └── case_duration_distribution.png

Note: These filenames describe the planned screenshots. Create and add the image files only after capturing the corresponding visuals from your actual Power BI report.

The "additional_visuals/" directory can be created if individual charts or components need separate documentation.

---

4. Screenshot Specifications

4.1 Executive Overview

Filename: "01_executive_overview.png"

This screenshot should show the main summary page of the Power BI dashboard.

Expected components:

- Total Cases KPI card.
- Total Events KPI card.
- Total Measurements KPI card.
- Average Recorded Case Duration KPI card.
- Activity Trends line chart.
- Most Frequent Activities bar chart.
- Case Summary table.
- Activity Summary table.
- Relevant filters and slicers.

Purpose: Demonstrate the overall dataset summary and the main analytical metrics.

4.2 Patient Journey

Filename: "02_patient_journey.png"

This screenshot should show the visual analysis of recorded patient activity sequences.

Expected components:

- Patient case selection.
- Activity transition or process-flow visual.
- Activity frequency chart.
- Case activity details table.
- Relevant summary metrics.

Purpose: Demonstrate how users can explore recorded activity sequences within individual cases.

A Sankey diagram or other specialised process-flow visual should be included only after it has been implemented and validated.

4.3 Case Duration Analysis

Filename: "03_case_duration.png"

This screenshot should show the analysis of recorded case durations.

Expected components:

- Number of cases analysed.
- Average recorded case duration.
- Median recorded case duration.
- Case-duration distribution chart.
- Case-duration comparison chart.
- Case-level duration table.

Purpose: Demonstrate variation in the elapsed time between the first and last recorded events for each case.

Recorded case duration must not automatically be interpreted as total hospital length of stay.

4.4 Laboratory Analysis

Filename: "04_laboratory_analysis.png"

This screenshot should show the available clinical measurement analysis.

Expected components:

- Total measurement records.
- Measurement types.
- Measurement trends over time.
- Measurement counts by type.
- Measurement details table.
- Relevant date and case filters.

Purpose: Demonstrate the exploration of recorded clinical measurement data.

Measurement units and data types should be checked before displaying comparisons.

4.5 Data Quality

Filename: "05_data_quality.png"

This screenshot should show the results of data validation.

Expected components:

- Total records checked.
- Missing-value summary.
- Duplicate-record summary.
- Validation results.
- Data-quality details table.

Purpose: Demonstrate the validation checks used to assess the reliability of the data.

All values must come from actual validation results. Do not add example counts as if they were measured results.

---

5. Screenshot Capture Guidelines

Follow these guidelines when capturing Power BI screenshots.

Step 1: Open the Dashboard

Open the relevant report page in your Power BI authoring environment or browser.

Step 2: Prepare the Report Page

Before taking the screenshot:

- Ensure the intended visuals are fully loaded.
- Apply the appropriate filters.
- Check that chart titles are readable.
- Confirm that values are displayed correctly.
- Remove unnecessary interface elements where possible.

Step 3: Capture the Screenshot

Capture the actual report page using your computer's screenshot functionality.

For a Mac, you can use:

- "Command + Shift + 4" to capture a selected area.
- "Command + Shift + 3" to capture the full screen.

Prefer capturing the dashboard area rather than unrelated desktop content.

Step 4: Save the Image

Save the image in the "powerbi/screenshots/" directory using the recommended filename.

For example:

"powerbi/screenshots/01_executive_overview.png"

Step 5: Verify the Image

Check that:

- The screenshot is clear and readable.
- The report page is not cut off.
- The chart labels and KPI values are visible.
- No unintended personal or confidential information appears.
- The screenshot accurately represents the current dashboard.

Step 6: Commit the Screenshot

After saving the image, add it to Git and push the change to GitHub.

Example commit message:

"docs: add executive overview dashboard screenshot"

---

6. Image Naming Convention

Use descriptive, lowercase filenames with underscores.

Screenshot| Filename
Executive Overview| "01_executive_overview.png"
Patient Journey| "02_patient_journey.png"
Case Duration| "03_case_duration.png"
Laboratory Analysis| "04_laboratory_analysis.png"
Data Quality| "05_data_quality.png"
KPI Cards| "kpi_cards.png"
Activity Analysis| "activity_analysis.png"
Duration Distribution| "case_duration_distribution.png"

Numbered filenames keep the five main dashboard pages in the intended order.

Use the PNG format for clear dashboard screenshots. Other formats may be used when appropriate, provided they display correctly on GitHub.

---

7. Screenshot Quality Standards

Screenshots should meet the following standards:

- Clarity: Text, chart labels, and KPI values must be readable.
- Consistency: Use similar capture dimensions for comparable report pages.
- Accuracy: Display actual results from the implemented report.
- Completeness: Include the important visuals on the relevant page.
- Professional presentation: Avoid unnecessary blank space and unrelated interface elements.
- Privacy: Do not expose confidential patient data or unauthorised personal information.
- Authenticity: Do not create mock screenshots and describe them as completed Power BI outputs.

If a dashboard page is redesigned, replace the older screenshot with the latest verified version.

---

8. Documentation of Screenshots

When necessary, include the following information in the filename or accompanying documentation:

Detail| Description
Screenshot name| Descriptive image filename
Dashboard page| Report page represented
Capture date| Date the screenshot was taken
Implementation status| Planned, implemented, or validated
Related design file| Corresponding report design document
Notes| Important filters, calculations, or limitations

This information helps maintain consistency between the screenshots, dashboard implementation, and project documentation.

---

9. GitHub Integration

Screenshots are maintained as supporting assets in the project repository.

Recommended practices:

- Commit screenshots after meaningful dashboard milestones.
- Use descriptive commit messages.
- Replace outdated images when the corresponding report page changes.
- Avoid uploading unnecessary duplicate screenshots.
- Review every image before publishing it.
- Keep large exports and confidential information out of the repository unless their inclusion is appropriate and authorised.

GitHub can display supported image formats directly when the files are committed to the repository.

---

10. Relationship with Other Project Directories

The screenshot directory is part of the Power BI reporting component.

Directory| Relationship
"powerbi/dashboard/"| Contains dashboard-related supporting documentation and files.
"powerbi/report_design/"| Documents the planned page layouts and visual specifications.
"powerbi/data_model/"| Documents the data tables and relationships.
"powerbi/dax_measures/"| Stores the DAX formulas used for dashboard calculations.
"powerbi/exports/"| Stores suitable exported reports, such as PDFs.
"powerbi/"| May contain the completed ".pbix" report when available.

The screenshots should reflect the actual implementation documented in these directories.

---

11. Current Status

Status: Screenshot directory documentation prepared.

The screenshots will be added incrementally as the five dashboard pages are created and validated.

No screenshot should be considered available until the corresponding image has actually been captured and saved in this directory.

---

12. Expected Outcome

The completed screenshot collection will provide a clear visual record of the CareFlow Process Mining Power BI dashboard.

It will support project documentation, GitHub presentation, progress reporting, and demonstrations of the implemented dashboard features.

The screenshots will complement the actual Power BI report and its supporting technical documentation.

---

Project: CareFlow Process Mining
Component: Power BI Dashboard
Directory: "powerbi/screenshots/"
Document: "README.md"
