CareFlow Process Mining — Analysis Notebooks

Purpose

This directory contains the Jupyter Notebooks used to investigate, clean, analyze, and discover healthcare workflows from the available event log dataset.

Notebook Workflow

1. "01_dataset_assessment.ipynb" — Examine the dataset structure, columns, data types, missing values, duplicates, and suitability for process mining.
2. "02_data_cleaning.ipynb" — Apply documented data-quality checks and prepare an analysis-ready dataset.
3. "03_exploratory_data_analysis.ipynb" — Explore activity frequencies, case counts, event distributions, and available time information.
4. "04_patient_pathway_analysis.ipynb" — Investigate the sequence of activities within individual cases and identify common pathways.
5. "05_process_discovery.ipynb" — Discover process models using suitable process-mining techniques.
6. "06_bottleneck_analysis.ipynb" — Investigate waiting times, process durations, and potential bottlenecks when the required timestamps are available.

Working Principles

- Preserve the original dataset in "data/raw/".
- Store cleaned outputs in "data/processed/".
- Use relative file paths so the project can run on another computer.
- Document assumptions, data-quality decisions, and limitations.
- Never claim a finding that is not supported by the dataset.
- Keep patient-identifiable or sensitive information out of public reports and visualizations.

Reproducibility

Each notebook should contain its objective, code, outputs, interpretation, and limitations. Run notebooks in a consistent order and record the dependencies required to reproduce the analysis.
