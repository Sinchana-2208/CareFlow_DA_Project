# CareFlow Source Modules

This directory contains the modularized Python pipeline for the CareFlow Sepsis process mining project.

## Modules
- **`loader.py`**: Handles loading the raw Sepsis event log and cases summary sheets from Excel.
- **`cleaner.py`**: Performs data cleaning, handles missing values, converts timestamps, and removes duplicate events.
- **`eda_plots.py`**: Generates process visualization charts (e.g., top frequent clinical activities).
- **`analyzer.py`**: Computes core process analytics including patient case durations and activity frequency summaries.
