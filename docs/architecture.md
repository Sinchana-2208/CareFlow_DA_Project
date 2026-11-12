# System Architecture

## 1. Proposed architecture
The project is organized into input data, analytical source code, tests, and user-facing outputs.

```text
careflow-process-mining/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_processing.py
│   ├── data_validation.py
│   ├── process_discovery.py
│   ├── performance_metrics.py
│   ├── bottleneck_analysis.py
│   ├── patient_journey.py
│   ├── visualization.py
│   └── main.py
├── tests/
├── dashboard/
├── reports/
├── presentation/
└── docs/
```

## 2. Module responsibilities
- `data_processing.py`: load, normalize, sort, and prepare data.
- `data_validation.py`: schema checks, duplicate checks, timestamp checks, and cross-table consistency checks.
- `process_discovery.py`: activity frequencies, transitions, variants, and process-map inputs.
- `performance_metrics.py`: case durations and event-to-event intervals.
- `bottleneck_analysis.py`: identify and summarize long intervals for investigation.
- `patient_journey.py`: assemble a case-level timeline and readable event sequence.
- `visualization.py`: generate charts from validated analysis outputs.
- `main.py`: orchestrate the pipeline with clear inputs and outputs.
- `tests/`: automated tests for each implemented module.
- `dashboard/`: interactive presentation layer.
- `reports/`: saved analytical outputs.
- `presentation/`: presentation material for project reviews.
- `docs/`: project, dataset, methodology, architecture, and user documentation.

## 3. Data flow
1. Read the original workbook from `data/raw/`.
2. Validate schema and data integrity.
3. Prepare derived tables in `data/processed/`.
4. Run process and performance analyses.
5. Generate charts and report tables.
6. Feed validated outputs to the dashboard.
7. Test and document the results.

## 4. Design principles
- Keep raw data unchanged.
- Separate data preparation from analysis and presentation.
- Avoid hard-coded absolute file paths.
- Use functions with clear inputs and outputs.
- Make transformations reproducible.
- Keep clinical interpretation separate from descriptive process analysis.
- Add automated tests before relying on outputs in a presentation.
