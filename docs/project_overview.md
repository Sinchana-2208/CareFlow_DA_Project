# Project Overview

## 1. Project title
**Careflow Process Mining: Sepsis Care-Pathway Analysis**

## 2. Background
Hospital care consists of events such as emergency registration, triage, laboratory measurements, treatment, admission, and release. Process mining uses timestamped event logs to examine how cases move through a process. This project uses a sepsis-related event log to describe care pathways, timing, variation, and potential process bottlenecks.

## 3. Problem statement
A list of hospital events is difficult to interpret manually at scale. The project organizes events into case-level timelines and analytical tables so that pathways, event frequencies, durations, and variations can be examined consistently.

## 4. Objectives
1. Validate the structure and quality of the event log.
2. Reconstruct each case's sequence of recorded activities.
3. Describe the frequency and ordering of activities.
4. Calculate elapsed time between recorded events and case start/end timestamps.
5. Identify unusually long intervals or pathways for further review.
6. Present results through clear charts, reports, and a dashboard.
7. Keep the analysis reproducible through documented code and tests.

## 5. Scope
The supplied workbook includes 1,049 cases, 15,190 event rows, case-level attributes, recorded laboratory-measurement values, and a case summary. The recorded event types include emergency registration and triage, laboratory measurements, IV fluids, IV antibiotics, admissions, releases, and return-to-emergency events.

## 6. Questions the project can investigate
- Which activities occur most frequently?
- What are the most common recorded activity sequences?
- How much recorded time elapses between selected activities?
- How do case durations vary?
- Which transitions or intervals are associated with longer observed durations?
- How often are laboratory measurement events recorded?
- How do recorded pathways vary across case attributes?

These are analysis questions, not assumptions that a delay occurred or that care was inappropriate.

## 7. Expected deliverables
- Data validation and preparation scripts.
- Process discovery and pathway summaries.
- Performance and interval metrics.
- Bottleneck candidates for investigation.
- Patient/case journey visualizations.
- Dashboard and report outputs.
- Automated tests and documentation.

## 8. Success criteria
- Event records can be traced to a case and timestamp.
- Key calculations are reproducible.
- Invalid timestamps, duplicate records, and ordering issues are checked explicitly.
- Visualizations explain their definitions and denominators.
- Findings are described as observational, with limitations clearly stated.
- Tests run successfully and the project can be set up from documented instructions.
