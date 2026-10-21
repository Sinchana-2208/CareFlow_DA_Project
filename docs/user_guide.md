# User Guide

## 1. Purpose
This guide explains the intended workflow for the Careflow Process Mining repository. Update the commands below once the project's actual entry point and dependency list are finalized.

## 2. Suggested repository placement
Save the supplied workbook under `data/raw/` and keep its original version unchanged. Use a separate processed-output folder for derived files. Do not commit sensitive patient-level data to a public repository; follow your organization's rules and repository access settings.

## 3. Environment setup
Use a supported Python version chosen for the project and record it in the repository. Create and activate a virtual environment, then install dependencies from `requirements.txt` after that file is populated with the actual packages used.

Example commands on macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Running the project
The intended entry point is `src/main.py`, but the exact command should be documented after the module is implemented. A possible future command is:

```bash
python -m src.main
```

Do not use this command as a promise that the pipeline already runs; confirm it after implementation.

## 5. Testing
Once tests are implemented, run them from the repository root. If using pytest:

```bash
python -m pytest -q
```

Record the number of tests passed and any failures. Do not report tests as passing unless they have actually been executed.

## 6. Expected outputs
Depending on implementation, outputs may include:
- A data-quality report.
- Activity and transition summaries.
- Case-duration and interval tables.
- Process maps and visualizations.
- Dashboard views.
- A report describing findings and limitations.

## 7. Reproducibility checklist
- [ ] Record the input filename and version.
- [ ] Preserve raw data.
- [ ] Record dependency versions.
- [ ] Use relative/configurable paths.
- [ ] Set and document timestamp ordering rules.
- [ ] Save analysis parameters and filters.
- [ ] Test the calculations.
- [ ] Ensure chart totals match the validated data.
- [ ] Document limitations and avoid unsupported clinical conclusions.
