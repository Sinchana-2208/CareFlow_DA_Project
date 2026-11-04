# Clinical Measurements Analysis Dashboard

## 1. Project Overview

The Clinical Measurements Analysis Dashboard is developed using Microsoft Power BI to analyse clinical measurement data recorded during patient healthcare processes.

The dashboard focuses on three important clinical measurements: **CRP, Leucocytes, and LacticAcid**. It provides insights into measurement values, measurement frequency, clinical measurement distributions, and case-level measurement details.

The dashboard transforms clinical event data into meaningful visual insights, helping users explore measurement patterns across different patient cases.

## 2. Project Objectives

- Analyse clinical measurements recorded for different patient cases.
- Examine CRP, Leucocytes, and LacticAcid values.
- Understand the distribution of clinical measurement values.
- Identify measurement frequency across patient cases.
- Compare average values across different measurement types.
- Explore clinical measurement details for individual cases.
- Provide interactive filtering for detailed clinical data analysis.

## 3. Key Performance Indicators (KPIs)

The dashboard displays the following key performance indicators:

| KPI | Value | Description |
|---|---:|---|
| Unique Cases | 1K | Number of unique patient cases |
| Total Measurements | 8K | Total clinical measurements displayed |

## 4. Clinical Measurement Types

The dashboard analyses three major clinical measurement types.

### 4.1 CRP (C-Reactive Protein)

CRP is a clinical measurement used to assess inflammation.

The dashboard categorizes CRP values into different ranges:

- 0–50
- 50–100
- 100–150
- 150–200
- Above 200

### 4.2 Leucocytes

Leucocytes represent white blood cell measurements.

The dashboard categorizes Leucocytes values into:

- 0–10
- 10–20
- 20–30
- 30–40
- Above 40

### 4.3 LacticAcid

LacticAcid is another important clinical measurement included in the analysis.

The dashboard displays the measurement range:

- 2–4

## 5. Dashboard Visualizations

### 5.1 Average Value by Measurement Type

Displays the average clinical measurement values for CRP, Leucocytes, and LacticAcid.

**Purpose:**
- Compare measurement values across different clinical parameters.
- Understand variations between measurement types.
- Support clinical measurement analysis.

### 5.2 Clinical Measurement Value Distribution

Displays the distribution of measurement values across different clinical measurement categories.

**Purpose:**
- Understand the frequency of values within different ranges.
- Identify commonly occurring measurement ranges.
- Compare clinical measurement distributions.

### 5.3 Clinical Measurement Type Distribution

A chart displaying the count and percentage distribution of different measurement types.

**Dashboard values:**

| Measurement Type | Count | Percentage |
|---|---:|---:|
| CRP | 360 | 44.44% |
| Leucocytes | 371 | 45.80% |
| LacticAcid | 79 | 9.75% |
| **Total** | **810** | **100%** |

**Purpose:**
- Compare the frequency of different clinical measurements.
- Identify the most frequently recorded measurement type.
- Understand the composition of clinical measurement records.

### 5.4 Measurement Frequency by Case

Displays the number of clinical measurements recorded for different patient cases.

**Purpose:**
- Identify cases with higher measurement frequencies.
- Compare measurement activity across cases.
- Understand differences in clinical monitoring patterns.

### 5.5 Clinical Measurement Details

A detailed table providing case-level clinical measurement information.

**Columns included:**
- Case ID
- Event Index
- Activity
- Timestamp
- Measurement Name
- Measurement Value

**Purpose:**
- Examine individual clinical measurement records.
- Compare measurement values across cases.
- Support detailed case-level investigation.

## 6. Interactive Filters

The dashboard provides the following interactive filters:

| Filter | Function |
|---|---|
| Measure Name | Filter CRP, Leucocytes, or LacticAcid |
| Measure Value | Search or filter specific measurement values |
| Case ID | Select individual patient cases |

These filters allow users to explore clinical measurements based on their analytical requirements.

## 7. Tools and Technologies

| Technology | Purpose |
|---|---|
| Microsoft Power BI | Dashboard development and visualization |
| Microsoft Excel | Dataset storage and data preparation |
| DAX | Measures and analytical calculations |
| Power Query | Data cleaning and transformation |
| GitHub | Project documentation and version control |

## 8. Key Analytical Insights

The dashboard supports the following analysis:

- Leucocytes account for approximately 45.80% of the displayed measurement-type distribution.
- CRP accounts for approximately 44.44%.
- LacticAcid accounts for approximately 9.75%.
- Leucocytes is the most frequently represented measurement type in the displayed distribution.
- Individual patient cases can be examined to understand their recorded clinical measurements.
- Measurement value categories help identify the distribution of clinical observations.

These findings describe the displayed dashboard data and should not be interpreted as independent medical diagnoses.

## 9. Expected Outcomes

The Clinical Measurements Analysis Dashboard aims to:

- Improve visibility into clinical measurement records.
- Understand measurement patterns across patient cases.
- Identify frequently recorded clinical parameters.
- Support patient-level clinical data exploration.
- Present complex measurement information through interactive visualizations.
- Support further healthcare process analysis.

## 10. Dashboard Folder Structure

```text
clinical_measurements_analysis/
│
├── README.md
│
├── report_design/
│   └── clinical_measurements_design.md
│
├── screenshots/
│   └── clinical_measurements_dashboard.png
│
├── exports/
│   └── clinical_measurements_report.pdf
│
├── data_model/
│   └── data_model_documentation.md
│
├── dax_measures/
│   └── clinical_measurement_measures.md
│
└── powerbi/
    └── clinical_measurements_analysis.pbix
```

## 11. Conclusion

The Clinical Measurements Analysis Dashboard provides an interactive approach to analysing clinical measurement data using Microsoft Power BI.

By examining CRP, Leucocytes, and LacticAcid values, their distributions, and their frequency across patient cases, the dashboard helps transform raw healthcare data into understandable analytical insights.

This analysis contributes to better visibility of clinical measurement patterns and supports further investigation of healthcare processes.

---

**Project Domain:** Healthcare Analytics  
**Analysis Type:** Clinical Measurements Analysis  
**Visualization Tool:** Microsoft Power BI  
**Version Control:** GitHub
