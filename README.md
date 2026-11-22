CareFlow Intelligence — Clinical Pathway Process Mining

CareFlow Intelligence is a Python-based healthcare process-mining and data analytics project. It analyzes a clinical event log to understand how recorded patient cases move through activities, how pathways vary, and how much time elapses between consecutive recorded events.

The project is intended for process analysis and reporting. It does not assess clinical correctness, provide diagnoses, or support treatment decisions.

Project objectives

- Reconstruct the recorded activity sequence for each patient case.
- Identify and count distinct pathway variants.
- Analyze transitions between consecutive activities.
- Summarize elapsed time between recorded events.
- Flag long intervals for further investigation.
- Present the results through an interactive dashboard.

Dataset

The analysis uses the Sepsis event-log Excel workbook, with the worksheet Event Log Visual.

Place the workbook in the project directory or provide its full path when running the workflow. The source dataset is not included in this repository unless separately provided.

Current dataset summary
Metric	Result

Recorded event records	15,190
Patient cases	1,049
Unique activities	16
Unique pathway variants	845
Activity transitions	115
Long intervals flagged for investigation (24 hours or more)	2,646


The most common complete recorded pathway identified in the current analysis is:

ER Registration → ER Triage → ER Sepsis Triage

It occurs in 35 cases (approximately 3.34% of the 1,049 cases).

These figures describe the available event log only. A recorded pathway is not necessarily a complete representation of a patient's clinical journey, and pathway frequency does not establish whether a pathway is clinically appropriate.

Analysis and outputs
The workflow produces CSV summaries in the outputs/ directory, including:
- workflow_overview.csv — overall dataset and workflow metrics.
- pathway_variants.csv — pathway sequences, case counts, percentages, and activity counts.
- activity_transition_summary.csv — transition counts, percentages, and elapsed-time summaries.
- transition_time_summary.csv — timing summaries for recorded activity transitions.

Long intervals are investigation signals, not confirmed bottlenecks or proof that a patient was waiting for the entire interval. The meaning of each interval depends on the clinical and operational context of the recorded activities.

Interactive dashboard
The interactive Plotly dashboard is generated at:

outputs/careflow_interactive_dashboard.html

It presents key workflow metrics and visual summaries of pathway variants, activity transitions, transition timing, and long intervals. Open the generated HTML file in a web browser. An internet connection may be required for Plotly charts if the dashboard loads Plotly from its CDN.


Requirements
- Python 3.10 or later recommended.
- Python packages listed in requirements.txt.
- The source Sepsis event-log Excel workbook.


Setup
From the repository root, create and activate a virtual environment (recommended).
Windows PowerShell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Run the workflow
From the repository root, run the workflow report generator. Replace the example workbook path with the actual path to your Excel file.
python -m src.run_workflow_report --input "..\Sepsis_Cases_Event_Log_Cleaned_for_Visualization (1).xlsx" --sheet "Event Log Visual" 

--output-dir "outputs"
If the workbook is stored elsewhere, provide its full path after --input.
Generate and open the interactive dashboard

After the workflow CSV outputs have been generated, run:
python .\src\create_interactive_dashboard.py

Then open the dashboard:
Start-Process .\outputs\careflow_interactive_dashboard.html
Run tests

Run the automated test suite from the repository root:
python -m unittest discover -s tests -v
The latest project test run recorded 17 tests. Run the command above on your current checkout to verify its present status.

Technology stack
- Python
- pandas
- openpyxl
- Plotly
- Matplotlib
- HTML/CSS/JavaScript for the dashboard presentation
- Python unittest for automated tests


Project structure

CareFlow_Balaji_local/
├── src/
│   ├── run_workflow_report.py
│   ├── create_interactive_dashboard.py
│   ├── transition_time_analysis.py
│   └── pathway_variant_analysis.py
├── outputs/
│   ├── workflow_overview.csv
│   ├── pathway_variants.csv
│   ├── activity_transition_summary.csv
│   ├── transition_time_summary.csv
│   └── long_interval_investigation.csv
├── tests/
├── README.md
└── requirements.txt

The exact contents of src/, outputs/, and tests/ may vary by branch or project revision.
Limitations and interpretation

- The analysis reflects only the events recorded in the supplied event log.
- Missing or unrecorded events can affect reconstructed pathways and timing.
- Elapsed time between two recorded events does not necessarily represent patient waiting time.
- Long intervals require contextual investigation before any operational conclusion is drawn.
- The project is for data analysis and reporting, not clinical decision-making.


Project status
The core event-log analysis, pathway-variant analysis, transition-time summaries, automated tests, and interactive dashboard have been developed. The repository is intended to provide a reproducible workflow for generating the analysis outputs and dashboard from the source event-log workbook.