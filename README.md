# \# CareFlow Intelligence — Clinical Pathway Process Mining

# 

# \## 1. Project Overview

# 

# CareFlow Intelligence is a data analytics project focused on exploring recorded clinical event logs and reconstructing observed patient pathways.

# 

# The project uses process-mining concepts and descriptive analytics to examine activity sequences, elapsed time between consecutive activities, recorded case durations, and variations in observed pathways.

# 

# The goal is to produce reproducible, evidence-based analysis that can support further investigation of clinical processes.

# 

# > \*\*Important:\*\* This project provides descriptive process analytics. Its results do not independently establish clinical correctness, quality of care, patient outcomes, or operational inefficiency.

# 

# \## 2. Project Objectives

# 

# \- Understand the structure and quality of the available event-log dataset.

# \- Reconstruct chronological activity sequences for individual cases.

# \- Identify common and less-common recorded pathway variants.

# \- Measure elapsed time between consecutive recorded activities.

# \- Summarize the duration of recorded case journeys.

# \- Flag long elapsed intervals for further investigation.

# \- Prepare aggregated analytical outputs for visualization in Power BI.

# \- Document analysis methods, assumptions, and limitations.

# 

# \## 3. Current Features

# 

# \### 3.1 Transition-Time Analysis

# 

# \*\*File:\*\* `src/transition\_time\_analysis.py`

# 

# This module analyzes elapsed time between consecutive recorded activities.

# 

# Current capabilities:

# 

# \- Load and validate event-log fields.

# \- Parse timestamps and order events chronologically.

# \- Calculate elapsed time between consecutive activities within each case.

# \- Summarize elapsed-time distributions for observed activity transitions.

# \- Calculate recorded journey durations for individual cases.

# \- Investigate long elapsed intervals using a configurable threshold.

# 

# Long elapsed intervals are diagnostic signals. They should not automatically be interpreted as waiting time, process bottlenecks, or evidence of inappropriate care.

# 

# \### 3.2 Patient Pathway Variant Analysis

# 

# \*\*File:\*\* `src/pathway\_variant\_analysis.py`

# 

# This module reconstructs recorded activity sequences and groups cases that follow identical sequences.

# 

# Current capabilities:

# 

# \- Reconstruct chronological activity sequences for each case.

# \- Identify unique observed pathway variants.

# \- Count cases associated with each variant.

# \- Calculate the percentage of analyzed cases associated with each variant.

# \- Rank pathway variants by case frequency.

# \- Export aggregated pathway summaries to CSV.

# 

# The generated CSV contains pathway sequences and aggregate counts rather than individual case IDs.

# 

# \## 4. Dataset and Current Results

# 

# The analysis has been run on the following workbook:

# 

# `Sepsis\_Cases\_Event\_Log\_Cleaned\_for\_Visualization.xlsx`

# 

# Worksheet:

# 

# `Event Log Visual`

# 

# The workbook is stored locally and is not included in this repository by these instructions.

# 

# \### Dataset Profile

# 

# | Metric | Observed Result |

# |---|---:|

# | Valid event records | 15,190 |

# | Excluded event records during loading | 0 |

# | Unique cases | 1,049 |

# | Unique activities | 16 |

# | Consecutive transitions | 14,141 |

# 

# \### Pathway Variant Findings

# 

# | Metric | Observed Result |

# |---|---:|

# | Cases analyzed | 1,049 |

# | Unique pathway variants | 845 |

# | Cases following the most common recorded pathway | 35 |

# | Percentage following the most common pathway | 3.34% |

# 

# The most common recorded pathway in this analysis was:

# 

# `ER Registration → ER Triage → ER Sepsis Triage`

# 

# It occurred in 35 cases, representing 3.34% of the 1,049 analyzed cases.

# 

# These figures describe the supplied event log. They are not, by themselves, evidence that a pathway is clinically appropriate or inappropriate.

# 

# Results may change if the dataset, its event ordering, or its case definitions change.

# 

# \## 5. Repository Structure

# 

# ```text

# CareFlow\_DA\_Project/

# ├── src/

# │   ├── transition\_time\_analysis.py

# │   └── pathway\_variant\_analysis.py

# ├── tests/

# │   ├── test\_transition\_time\_analysis.py

# │   └── test\_pathway\_variant\_analysis.py

# ├── outputs/

# │   └── pathway\_variants.csv

# ├── .gitignore

# └── README.md

# ```

# 

# The `outputs/pathway\_variants.csv` file is generated locally and ignored by Git.

# 

# The original dataset should remain outside version control unless the project team has explicitly confirmed that sharing it is permitted.

# 

# \## 6. Requirements

# 

# The project uses Python and pandas for event-log processing and Excel/CSV data handling.

# 

# Install the required packages from a terminal:

# 

# ```powershell

# python -m pip install pandas openpyxl

# ```

# 

# Check that Python is available:

# 

# ```powershell

# python --version

# ```

# 

# Run the commands below from the project root directory.

# 

# \## 7. How to Run the Analysis

# 

# \### 7.1 Transition-Time Analysis

# 

# Run:

# 

# ```powershell

# python .\\src\\transition\_time\_analysis.py --file "C:\\path\\to\\Sepsis\_Cases\_Event\_Log\_Cleaned\_for\_Visualization.xlsx" --sheet "Event Log Visual"

# ```

# 

# Replace `C:\\path\\to\\...` with the actual location of the Excel workbook on your computer.

# 

# This analysis reports dataset-profile information, elapsed times between recorded activities, case-duration summaries, and long-gap diagnostics.

# 

# \### 7.2 Patient Pathway Variant Analysis

# 

# Run:

# 

# ```powershell

# python .\\src\\pathway\_variant\_analysis.py --file "C:\\path\\to\\Sepsis\_Cases\_Event\_Log\_Cleaned\_for\_Visualization.xlsx" --sheet "Event Log Visual"

# ```

# 

# Replace the example file path with the actual location of your workbook.

# 

# The script displays:

# 

# \- Number of cases analyzed.

# \- Number of unique pathway variants.

# \- The ten most common recorded pathways.

# \- Case counts and percentages for the displayed variants.

# 

# By default, the aggregated output is saved to:

# 

# ```text

# outputs/pathway\_variants.csv

# ```

# 

# To specify another output path, use the `--output` argument:

# 

# ```powershell

# python .\\src\\pathway\_variant\_analysis.py --file "C:\\path\\to\\Sepsis\_Cases\_Event\_Log\_Cleaned\_for\_Visualization.xlsx" --sheet "Event Log Visual" --output "outputs/my\_pathway\_results.csv"

# ```

# 

# The custom output path is relative to the current working directory unless an absolute path is supplied.

# 

# \## 8. Automated Tests

# 

# The repository includes tests for transition-time calculations and pathway variant analysis.

# 

# Run the complete test suite from the project root:

# 

# ```powershell

# python -m unittest discover -s tests -v

# ```

# 

# The current test suite contains nine tests:

# 

# \- Five tests for pathway variant analysis.

# \- Four tests for transition-time analysis.

# 

# The tests cover chronological sequence reconstruction, pathway grouping, case counts, percentage calculations, ranking, empty-input behavior, elapsed-time calculations, transition counts, transition labels, and separation between different cases.

# 

# The latest recorded test run completed successfully with all nine tests passing.

# 

# \## 9. Output and Visualization

# 

# The aggregated pathway summary can be used as an input for further analysis and Power BI visualization.

# 

# The pathway CSV includes:

# 

# | Column | Description |

# |---|---|

# | `variant\_id` | Identifier assigned to a pathway variant in the generated summary |

# | `pathway\_variant` | Recorded activity sequence associated with the variant |

# | `case\_count` | Number of cases following the variant |

# | `percentage\_of\_cases` | Percentage of analyzed cases following the variant |

# | `activity\_count` | Number of recorded activities in the sequence |

# 

# The current implementation produces an aggregated pathway table. A Power BI dashboard and additional analytical components can be developed as subsequent project steps.

# 

# \## 10. Analytical Limitations and Data Handling

# 

# \- Event timestamps describe recorded events; elapsed time between

