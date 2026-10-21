-- CareFlow Standalone SQL Analytics Queries

-- 1. Top 5 Longest Mean Transition Bottlenecks
SELECT From_Activity, To_Activity, Mean_Duration_Hours, Transition_Count
FROM transition_bottlenecks
ORDER BY Mean_Duration_Hours DESC
LIMIT 5;

-- 2. Top 5 Most Frequent Clinical Process Variants
SELECT Process_Variant, Case_Count
FROM process_variants
ORDER BY Case_Count DESC
LIMIT 5;

-- 3. Activity Execution Frequency Across All Sepsis Cases
SELECT Activity, COUNT(*) AS Total_Executions
FROM event_logs
GROUP BY Activity
ORDER BY Total_Executions DESC;
