{{ config(description='Creates one row per event with the previous/next activity and time to the next event.') }}

WITH event_transitions AS (
    SELECT
        t.*,
        LAG(t.activity_name) OVER (PARTITION BY t.case_id ORDER BY t.event_order) AS previous_activity,
        LEAD(t.activity_name) OVER (PARTITION BY t.case_id ORDER BY t.event_order) AS next_activity,
        LEAD(t.event_timestamp) OVER (PARTITION BY t.case_id ORDER BY t.event_order) AS next_event_timestamp,
        LEAD(t.return_reason) OVER (PARTITION BY t.case_id ORDER BY t.event_order) AS next_return_reason
    FROM {{ ref('int_careflow__ordered_events') }} t
)

SELECT
    *,
    CASE
        WHEN next_event_timestamp IS NOT NULL
            THEN SAFE_DIVIDE(DATETIME_DIFF(next_event_timestamp, event_timestamp, SECOND), 60.0)
        ELSE NULL
    END AS elapsed_to_next_minutes
FROM event_transitions
