# CareFlow: Clinical Pathway Process Mining & Analytics

CareFlow is an end-to-end data engineering and process mining pipeline designed to analyze, map, and optimize clinical pathways for Sepsis emergency cases. By parsing raw event logs, CareFlow uncovers common treatment pathways, identifies severe transition bottlenecks (delays in care), computes patient throughput metrics, and stores structured analytics into a SQLite database for advanced querying.

Key Features

Automated Event Log Ingestion & Cleaning: Parses raw Excel event logs (Sepsis_Cases_Event_Log.xlsx), standardizing timestamps (utc=True) and case identifiers.

Pathway Variant Mining: Groups and traces sequential clinical activities per patient case to discover dominant care pathways.

Transition Bottleneck Identification: Measures duration delays between consecutive clinical events to highlight critical operational bottlenecks.

Relational Database Storage: Automatically creates and populates a structured SQLite database (careflow.db) with relational schemas for event logs, process variants, transition bottlenecks, and overall case metrics.

Embedded SQL Analytics Engine: Runs automated, targeted SQL queries to yield high-value clinical insights directly within the terminal workflow.

Visual Analytics Generation: Exports summary visual assets (outputs/process_variants_and_bottlenecks.png) for presentation and decision-support reporting.

Repository Structure

CareFlow_DA_Project/
│
├── data/
│   └── Sepsis_Cases_Event_Log.xlsx     # Raw Sepsis event log dataset
│
├── outputs/
│   ├── careflow.db                     # Generated SQLite database
│   ├── process_variants.csv            # Top clinical pathway variants
│   ├── transition_bottlenecks.csv      # Delay durations between clinical activities
│   ├── case_metrics_summary.csv        # Per-case duration and event count metrics
│   └── process_variants_and_bottlenecks.png  # Exported analytics chart
│
├── src/
│   ├── __init__.py                     # Module initialization
│   ├── analyzer.py                     # Core process mining & pipeline functions
│   └── database.py                     # SQLite database loader and SQL query engine
│
├── main.py                             # Pipeline orchestrator script
├── README.md                           # Project documentation
└── requirements.txt                    # Python dependencies


Tech Stack

Language: Python 3.9+

Data Engineering & Analysis: pandas, openpyxl

Database Engine: sqlite3

Data Visualization: matplotlib, seaborn

Environment: GitHub Codespaces / VS Code

Installation & Setup

Clone the Repository:

git clone https://github.com/Sinchana-2208/CareFlow_DA_Project.git
cd CareFlow_DA_Project


Install Dependencies:

pip install -r requirements.txt


(Ensure pandas, openpyxl, and matplotlib are installed)

How to Run

Execute the primary orchestrator script from the root directory:

python main.py


Execution Steps Executed by main.py:

Loads and validates the raw event dataset.

Extracts clinical process variants and ranks them by case frequency.

Computes consecutive event transitions and isolates top delay bottlenecks.

Generates visual summary plots in the outputs/ folder.

Ingests processed tables into SQLite (outputs/careflow.db).

Executes advanced SQL analytical queries and prints summary results to the terminal interface.

Clinical Analytics & SQL Query Highlights

1. Process Variant Analysis

Identifies standard clinical treatment sequences from Emergency Room (ER) triage through laboratory evaluation (CRP, LacticAcid, Leucocytes) to treatment delivery (IV Antibiotics, IV Liquid).

2. Bottleneck Detection

Computes the exact mean transition times between sequential events. Key bottlenecks uncovered include prolonged durations between patient release phases (Release A-E) and subsequent emergency room returns (Return ER).

3. SQL Query Insights (outputs/careflow.db)

CareFlow embeds clinical queries inside src/database.py to evaluate:

Top Executed Clinical Activities: Querying execution counts across all patient encounters.

Top 3 Longest Transition Delays: Sorting average transition hours directly from the transition_bottlenecks database table.

Patient Throughput: Querying average events per patient journey and overall duration days across all tracked Sepsis cases.
