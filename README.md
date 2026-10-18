CareFlow Intelligence - Clinical Pathway Process Mining

About the project

CareFlow is a data analytics project that looks at recorded patient activity data to understand how cases move through different stages of a clinical process.

The main aim is to study the activities in the event log, understand the order in which they happen, and look at the time between recorded events. We are using Python for the analysis, with plans to use Power BI to present the findings.

What I have worked on

1. Transition-time analysis

I created a Python script to calculate the time between consecutive activities for each case. It also summarizes recorded case durations and highlights long gaps between events for further investigation.

File: src/transition_time_analysis.py

2. Patient pathway analysis

I added another script to reconstruct the activity sequence for each case and identify cases with the same sequence. The results include the number of cases following each pathway and its percentage of the dataset.

File: src/pathway_variant_analysis.py

Dataset and findings

The analysis was run using the Sepsis event-log Excel file, on the worksheet named "Event Log Visual".

Some of the results from the current dataset are:

- Total recorded events: 15,190
- Cases analyzed: 1,049
- Different activities: 16
- Unique pathway variants: 845

The most common complete recorded pathway in the current analysis is:

ER Registration -> ER Triage -> ER Sepsis Triage

This pathway appears in 35 cases, which is about 3.34% of all cases analyzed.

These numbers describe the available event log. They do not tell us whether a pathway is clinically correct or incorrect.

Running the scripts

The project uses Python, pandas, and openpyxl.

Install the required packages with:

python -m pip install pandas openpyxl

To run the transition-time analysis:

python .\src\transition_time_analysis.py --file "C:\path\to\Sepsis_Cases_Event_Log_Cleaned_for_Visualization.xlsx" --sheet "Event Log Visual"

To run the pathway analysis:

python .\src\pathway_variant_analysis.py --file "C:\path\to\Sepsis_Cases_Event_Log_Cleaned_for_Visualization.xlsx" --sheet "Event Log Visual"

Replace the example file path with the location of the Excel file on your computer.

The pathway analysis saves its results to:

outputs/pathway_variants.csv

Testing

I added automated tests for both analysis scripts. They check the pathway sequence calculations, pathway counts and percentages, and the transition-time calculations.

To run all tests:

python -m unittest discover -s tests -v

The latest test run passed all nine tests.

Current status and next steps

The transition-time and pathway-variant analyses are working. The next steps are to explore the results further and use suitable outputs to build a Power BI dashboard.

We also need to investigate the meaning of long gaps carefully. Time between two recorded activities does not necessarily mean that a patient was waiting during that entire period.

The project is intended for process analysis and reporting, not for making clinical decisions.