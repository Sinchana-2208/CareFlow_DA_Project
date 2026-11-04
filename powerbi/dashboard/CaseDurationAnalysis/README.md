# Case Duration Analysis Dashboard

## 1. Project Overview

The Case Duration Analysis Dashboard is developed using Microsoft Power BI to analyse the time taken to complete individual patient cases in a healthcare process.

The dashboard focuses on measuring case duration, identifying the longest-running cases, understanding duration distribution, and analysing monthly average case duration.

It transforms healthcare event data into meaningful visual insights to help understand process delays and identify cases that may require further investigation.

## 2. Project Objectives

- Calculate the duration of individual patient cases.
- Analyse average, maximum, minimum, and median case duration.
- Identify the top 10 longest-running cases.
- Understand the distribution of cases across different duration ranges.
- Analyse monthly average case duration trends.
- Provide interactive case-level analysis using Case ID filters.
- Identify potential delays and variations in healthcare processes.

## 3. Key Performance Indicators (KPIs)

The dashboard displays the following key performance indicators:

| KPI | Value | Description |
|---|---:|---|
| Total Cases | 1K | Total number of cases analysed |
| Average Case Duration | 28.48 Days | Average time taken to complete a case |
| Maximum Case Duration | Not displayed | Maximum duration KPI is currently unavailable |
| Minimum Case Duration | 0.00 Days | Minimum recorded case duration |
| Median Case Duration | 5.34 Days | Middle value of the case duration distribution |

## 4. Dashboard Visualizations

### 4.1 Top 10 Longest Cases

Displays the ten cases with the highest recorded duration.

**Purpose:**
- Identify cases taking the longest time.
- Compare duration between individual cases.
- Highlight cases that may require further investigation.

### 4.2 Case Duration Distribution

A column chart representing the number of cases within different duration ranges.

**Duration Categories:**
- 0–2 Days
- 2–4 Days
- 4–6 Days
- 6–8 Days
- Above 8 Days

**Purpose:**
- Understand how case durations are distributed.
- Identify the most common duration range.
- Compare short-duration and long-duration cases.

### 4.3 Monthly Average Case Duration

Displays the average case duration grouped by the month in which each case started.

**Purpose:**
- Analyse monthly variations in case duration.
- Identify months with higher average case duration.
- Understand changes in process performance over time.

### 4.4 Case Duration Details

A detailed table containing individual case information.

**Columns included:**
- Case ID
- Start Timestamp
- End Timestamp
- Duration in Days

**Purpose:**
- Examine individual case records.
- Compare case start and end timestamps.
- Verify calculated case durations.

### 4.5 Case ID Slicer

An interactive filter that allows users to select specific Case IDs.

**Purpose:**
- Filter dashboard visuals by individual cases.
- Explore specific patient journeys.
- Perform detailed case-level analysis.

## 5. Case Duration Calculation

Case duration is calculated using the difference between the case end timestamp and case start timestamp.

**Formula:**

`Case Duration = End Timestamp - Start Timestamp`

To calculate duration in days:

`Duration (Days) = (End Timestamp - Start Timestamp) / 86400`

This assumes timestamps are recorded in seconds.

## 6. Tools and Technologies

| Technology | Purpose |
|---|---|
| Microsoft Power BI | Dashboard development and visualization |
| Microsoft Excel | Dataset storage and data preparation |
| DAX | KPI calculations and analytical measures |
| GitHub | Project documentation and version control |

## 7. Key Analytical Insights

The dashboard supports the following analysis:

- Comparison of average and median case duration.
- Identification of cases with unusually long durations.
- Analysis of case distribution across different time intervals.
- Monitoring monthly changes in average case duration.
- Identification of potential delays in healthcare processes.
- Detailed investigation of individual case records.

## 8. Expected Outcomes

The Case Duration Analysis Dashboard aims to:

- Improve visibility into healthcare case completion times.
- Identify cases with longer processing durations.
- Support the analysis of healthcare process efficiency.
- Provide meaningful insights through interactive visualizations.
- Help identify areas that may require process improvement.

## 9. Dashboard Folder Structure

```text
case_duration_analysis/
│
├── README.md
│
├── report_design/
│   └── case_duration_design.md
│
├── screenshots/
│   └── case_duration_dashboard.png
│
├── exports/
│   └── case_duration_report.pdf
│
├── data_model/
│   └── data_model.md
│
├── dax_measures/
│   └── case_duration_measures.md
│
└── powerbi/
    └── case_duration_analysis.pbix
```

## 10. Conclusion

The Case Duration Analysis Dashboard provides an effective way to understand the time taken to complete healthcare cases.

By analysing case duration KPIs, longest-running cases, duration distribution, and monthly trends, the dashboard helps identify potential process delays and supports data-driven healthcare process improvement.

**Project Area:** Healthcare Process Analysis  
**Dashboard Tool:** Microsoft Power BI  
**Analysis Type:** Case Duration Analysis
