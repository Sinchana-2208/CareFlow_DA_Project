-- Find top 5 most frequent patient care pathways (variants)
SELECT Variant, COUNT(*) as Case_Count
FROM process_variants
ORDER BY Case_Count DESC
LIMIT 5;

-- Calculate average duration of high-risk sepsis cases
SELECT AVG(Duration_Days) as Avg_Stay_Days
FROM case_metrics;
