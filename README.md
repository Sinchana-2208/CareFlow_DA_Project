#CareFlow: Clinical Pathway Process Mining & Analytics
CareFlow is an end-to-end data engineering and process mining pipeline designed to analyze, map, and optimize clinical pathways for Sepsis emergency cases. By parsing raw event logs, CareFlow uncovers common treatment pathways, identifies severe transition bottlenecks (delays in care), computes patient throughput metrics, and stores structured analytics into a SQLite database for advanced querying.

##Key Features

Automated Event Log Ingestion & Cleaning: Parses raw Excel event logs (Sepsis_Cases_Event_Log.xlsx) using dedicated loader.py and cleaner.py modules, standardizing timestamps (utc=True) and case identifiers.

Pathway Variant Mining: Groups and traces sequential clinical activities per patient case via analyzer.py to discover dominant care pathways.

Transition Bottleneck Identification: Measures duration delays between consecutive clinical events to highlight critical operational bottlenecks.

Relational Database Storage: Automatically creates and populates a structured SQLite database (outputs/careflow.db) with relational schemas for event logs, process variants, transition bottlenecks, and overall case metrics using database.py.

Standalone & Embedded SQL Engine: Houses dedicated standalone queries (sql/queries.sql) and runs automated, targeted SQL queries to yield high-value clinical insights directly within the terminal workflow.

Visual Analytics Generation: Uses eda_plots.py to export summary visual assets in the outputs/ directory for presentation and decision-support reporting.

Comprehensive Test Suite: Includes unit and integration test coverage across data processing, process mining, bottleneck analysis, database logic, and full pipeline execution (tests/).

##Repository Structure

CareFlow_DA_Project/
│
├── config/
│   └── config.yaml                 # Pipeline configuration settings & parameters
│
├── data/
│   ├── .gitkeep                    # Directory tracking file
│   └── Sepsis_Cases_Event_Log.xlsx # Source clinical event log dataset
│
├── docs/
│   ├── architecture.md             # System architecture & workflow documentation
│   ├── data_dictionary.md          # Field definitions & metadata
│   └── dataset_schema.md           # Event log schema specifications
│
├── outputs/
│   └── .gitkeep                    # Directory tracking file for SQLite DB & generated plots
│
├── sql/
│   └── queries.sql                 # Standalone SQL analytics query routines
│
├── src/
│   ├── init.py                 # Package initializer
│   ├── analyzer.py                 # Process mining & metrics computation
│   ├── cleaner.py                  # Data cleaning & transformation routines
│   ├── database.py                 # SQLite database storage & query execution
│   ├── eda_plots.py                # Visual chart & graph generation module
│   └── loader.py                   # Excel event log ingestion module
│
├── tests/
│   ├── init.py                 # Test package discovery initializer
│   ├── test_bottleneck_analysis.py # Unit tests for transition intervals
│   ├── test_data_processing.py     # Unit tests for data cleaning & schema validation
│   ├── test_database.py            # Unit tests for SQLite database interface
│   ├── test_pipeline.py            # Integration test for full end-to-end pipeline
│   └── test_process_mining.py      # Unit tests for variant trace generation
│
├── .gitignore                      # Git ignore rules for cache & local data artifacts
├── main.py                         # End-to-end execution script / orchestrator
├── README.md                       # Project documentation & portfolio summary
└── requirements.txt                # Project dependencies

##Tech Stack

Language: Python 3.9+

Data Engineering & Analysis: pandas, openpyxl, pytest

Database Engine: sqlite3

Data Visualization: matplotlib, seaborn

Environment: GitHub Codespaces / VS Code

##Installation & Setup

####Clone the Repository:

git clone https://github.com/Sinchana-2208/CareFlow_DA_Project.git
cd CareFlow_DA_Project

####Install Dependencies:

pip install -r requirements.txt

(Ensure pandas, openpyxl, matplotlib, and pytest are installed)

##How to Run

Execute the primary orchestrator script from the root directory:

python main.py

Execution Steps Executed by main.py:

Loads and validates the raw event dataset via src/loader.py and src/cleaner.py.

Extracts clinical process variants and ranks them by case frequency via src/analyzer.py.

Computes consecutive event transitions and isolates top delay bottlenecks.

Generates visual summary plots in the outputs/ folder via src/eda_plots.py.

Ingests processed tables into SQLite (outputs/careflow.db) via src/database.py.

Executes advanced SQL analytical queries and prints summary results to the terminal interface.

##Running Tests

To run the complete unit and integration test suite:

pytest tests/

##Clinical Analytics & SQL Query Highlights

Process Variant Analysis: Identifies standard clinical treatment sequences from Emergency Room (ER) triage through laboratory evaluation (CRP, LacticAcid, Leucocytes) to treatment delivery (IV Antibiotics, IV Liquid).

Bottleneck Detection: Computes the exact mean transition times between sequential events. Key bottlenecks uncovered include prolonged durations between patient release phases (Release A-E) and subsequent emergency room returns (Return ER).

SQL Query Insights (outputs/careflow.db): CareFlow embeds clinical queries inside src/database.py (and standalone scripts in sql/queries.sql) to evaluate top executed clinical activities, longest transition delays, and overall patient throughput.
