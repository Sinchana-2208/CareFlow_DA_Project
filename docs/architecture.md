# CareFlow System Architecture

CareFlow is built on a modular pipeline architecture designed to decouple data ingestion, process mining analytics, graphical visualization generation, and database persistence.

## Pipeline Lifecycle
1. **Ingestion & Cleaning (`src/analyzer.py`):** Parses Excel event logs, standardizes ISO timestamp formats, and handles missing case attributes.
2. **Process Variant & Bottleneck Discovery:** Aggregates event traces to map frequent clinical pathways and measures transition durations.
3. **Persistence Layer (`src/database.py`):** Loads analytical DataFrames into a local SQLite database (`outputs/careflow.db`) to enable structured relational querying.
4. **Advanced SQL Layer:** Executes targeted operational queries to extract key clinical indicators (KPIs) like readmission frequencies and throughput delays.
