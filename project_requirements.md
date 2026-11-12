CareFlow Intelligence — Project Requirements

1. Project Information

Project: CareFlow: Clinical Pathway Process Mining

Proposed implementation name: CareFlow Intelligence

Domain: Healthcare Process Analytics

Project period: 10 October 2026 – 10 November 2026

2. Objective

Develop a reproducible analytics solution that uses event-log data to reconstruct process journeys, discover pathway patterns, analyze elapsed time, and present evidence-based operational findings.

3. Business Questions

- BQ01: What are the most common observed process pathways?
- BQ02: What is the elapsed time between consecutive activities?
- BQ03: Which transitions or pathways have comparatively long durations?
- BQ04: How do observed pathways differ from an approved reference workflow, if available?
- BQ05: Which potential improvement opportunities should be prioritized for further investigation?

4. Functional Requirements

- FR01: Inspect and profile the available dataset.
- FR02: Identify data quality issues.
- FR03: Clean and validate the event data.
- FR04: Reconstruct process instances from case identifiers.
- FR05: Discover and compare pathway variants.
- FR06: Calculate case durations and transition elapsed times.
- FR07: Investigate process deviations when a valid reference model exists.
- FR08: Create transparent analytical measures for prioritizing investigation opportunities.
- FR09: Present relevant findings through a Power BI dashboard.
- FR10: Document the methods, findings, assumptions, and limitations.

5. Non-Functional Requirements

- Reproducible data-processing workflow.
- Clear and maintainable code.
- Documented data-cleaning decisions.
- Validation of important calculations.
- Appropriate handling of sensitive data.
- Clear presentation of metrics and limitations.
- Version-controlled source code and documentation.

6. Assumptions Requiring Confirmation

- The source dataset is available and approved for the project.
- The dataset contains a valid process-instance identifier, activity, and event timestamp.
- The intended analysis can be supported by the available event data.
- A reference workflow may or may not be available.
- Dashboard development will use an appropriate Power BI environment.
- Data-sharing and repository-publication permissions will be confirmed.

7. Out of Scope Unless Specifically Approved

- Clinical diagnosis or treatment recommendations.
- Claims about patient outcomes without appropriate data and validation.
- Claims of financial savings without supporting calculations.
- Claims that a long elapsed time proves operational negligence or inefficiency.
- Publishing confidential or identifiable patient information.

8. Expected Deliverables

- Data quality assessment
- Data-cleaning and validation workflow
- Prepared event log
- Exploratory analysis
- Process discovery and pathway analysis
- Duration analysis
- Process deviation analysis, if supported
- Power BI dashboard
- Project report
- Final presentation
- Documented GitHub repository

9. Open Questions for the Internship Mentor

- Which dataset should be used?
- What is the definition of a process case?
- What do the event timestamps represent?
- Is an approved reference workflow available?
- Which business questions are highest priority?
- Are there required tools or reporting formats?
- What data can be stored locally or shared through GitHub?
- Which dashboard and presentation deliverables are mandatory?
