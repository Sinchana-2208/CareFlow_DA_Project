# CareFlow Process Mining tests

This folder is a starter structure for tests of the project's `src/` modules. The test files are intentionally marked as skipped: the source code was not included, so its function names and expected interfaces are not assumed. `pytest` can collect the suite now; replace each skipped example with assertions against your implementation to make it an active check.

## Structure

```text
tests/
├── data_processing/       # cleaning, sorting, and event preparation
├── data_validation/       # required fields and data consistency
├── performance_metrics/   # case duration and process timing
├── bottleneck_analysis/   # long waits and slow activities/transitions
├── patient_journey/       # event sequence and case pathway behavior
└── README.md
```

The workbook inspected for this starter contains these sheets and headers:

- **Event Log Visual:** `case_id`, `event_index`, `activity`, `timestamp`, `org_group`, `lifecycle_transition`
- **Case Attributes Visual:** `case_id`, `Age`, `diagnosis`, and clinical/diagnostic attributes
- **Event Measures Visual:** `case_id`, `event_index`, `activity`, `timestamp`, `measure_name`, `measure_value`
- **Cases Summary Visual:** `case_id`, `event_count`, `start_timestamp`, `end_timestamp`, `duration_days`, `event_sequence`

Use the actual workbook conventions in your tests. For example, missing category values may be represented by labels such as `Unknown / not recorded`; do not treat those labels as nulls unless your project explicitly does so.

## Setup and run

From the project root, install pytest if needed and run:

```bash
python -m pip install pytest
python -m pytest
```

To run one group:

```bash
python -m pytest tests/data_validation
```

When you connect the starter checks to your `src/` code, keep imports consistent with your project layout. If the project uses a `src/` package, add `src/__init__.py` if needed and run pytest from the project root.
