# Careflow Process Mining — Documentation

This folder documents the purpose, data, methodology, architecture, limitations, and usage of the Careflow Process Mining project.

## Documentation index
- [Project Overview](project_overview.md): problem, goals, scope, and expected outputs.
- [Dataset Dictionary](dataset_dictionary.md): workbook sheets, columns, and definitions.
- [Methodology](methodology.md): proposed analysis workflow.
- [System Architecture](architecture.md): role of project folders and modules.
- [Data Quality and Limitations](data_quality_and_limitations.md): cleaning decisions and interpretation cautions.
- [User Guide](user_guide.md): how to use the dataset and run the project as implementation develops.

## Dataset currently reviewed
`Sepsis_Cases_Event_Log_Cleaned_for_Visualization(2).xlsx`

The workbook contains five sheets: `Read Me`, `Event Log Visual`, `Case Attributes Visual`, `Event Measures Visual`, and `Cases Summary Visual`.

## Current dataset snapshot
- **1,049 cases**
- **15,190 event records**
- **7,922 recorded measurement rows**
- Event timestamps span **7 November 2013 to 5 June 2015**
- The three recorded measurement types are **Leucocytes, CRP, and LacticAcid**

These are descriptive counts from the supplied workbook, not clinical conclusions. Recalculate them whenever the dataset changes.

## Important
This documentation describes the supplied cleaned workbook and a proposed project design. It does not claim that all source-code modules, process-mining algorithms, dashboards, or tests have already been implemented. Clinical decisions must not be made from this project alone.
