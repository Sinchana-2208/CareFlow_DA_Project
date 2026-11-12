Patient Journey Analysis Dashboard

1. Project Overview

The Patient Journey Analysis Dashboard provides a visual representation of patient activities, healthcare events, and treatment processes.

The dashboard helps understand patient journeys by analysing the activities performed during hospital visits. It provides insights into frequently occurring activities, patient records, and healthcare process patterns.

2. Dashboard Objectives

- Analyse patient journey activities.
- Identify the most frequently performed healthcare activities.
- Monitor patient events and activity counts.
- Understand individual patient journeys.
- Provide interactive filtering using Case ID.
- Present important healthcare insights through visualizations.

3. Dashboard KPIs

The dashboard includes the following Key Performance Indicators (KPIs):

KPI| Description| Value
Total Patients| Total number displayed in the dashboard| 1K
Total Events| Count of event index| 185
Average Events Per Case| Average events recorded per case| 14.48
Unique Activities| Number of distinct activities| 16

4. Dashboard Visualizations

A. KPI Cards

Displays important project performance indicators:

- Total Patients
- Total Events
- Average Events Per Case
- Unique Activities

B. Patient Journey Details

Displays detailed patient activity information, including:

- Case ID
- Activity
- Sum of Timestamp
- Sum of Event Index
- Lifecycle Transition

C. Top 10 Most Frequent Activities

A clustered bar chart displaying the most frequently occurring healthcare activities.

Activities include:

- Leucocytes
- CRP
- LacticAcid
- Admission NC
- ER Triage
- ER Registration
- ER Sepsis Triage
- IV Antibiotics
- IV Liquid
- Release A

D. Case ID Slicer

An interactive slicer that allows users to select a particular Case ID and analyse the corresponding patient journey.

5. Tools and Technologies

- Power BI Desktop – Dashboard development and visualization.
- Microsoft Excel – Dataset handling and data preparation.
- GitHub – Project documentation and version control.

6. Key Insights

The dashboard provides the following analytical capabilities:

- Identifies frequently occurring healthcare activities.
- Helps explore individual patient journeys.
- Provides an overview of patient events and activities.
- Supports the identification of patterns in healthcare processes.
- Makes healthcare process information easier to understand through visual analytics.

7. Dashboard Structure

dashboard/
│
├── README.md
│
├── report_design/
│   └── dashboard_design.md
│
├── screenshots/
│   └── patient_journey_dashboard.png
│
├── exports/
│   └── patient_journey_report.pdf
│
├── data_model/
│   └── data_model_documentation.md
│
├── dax_measures/
│   └── measures.md
│
└── powerbi/
    └── patient_journey_dashboard.pbix

8. Expected Outcomes

The Patient Journey Analysis Dashboard aims to provide a clear understanding of healthcare activities and patient movement through different stages of care.

It supports data-driven analysis, improves process visibility, and helps identify areas that may require further investigation.

9. Conclusion

This dashboard transforms patient journey data into meaningful visual insights using Power BI. It provides an interactive platform for exploring healthcare activities, analysing patient events, and understanding healthcare process patterns.
