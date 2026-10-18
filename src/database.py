import sqlite3
import os

def save_to_sqlite(df_event, variant_summary, bottlenecks, case_metrics, db_path="outputs/careflow.db"):
    """Saves analytical DataFrames into a SQLite database."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    # Write tables to SQLite
    df_event.to_sql('event_log', conn, if_exists='replace', index=False)
    variant_summary.to_sql('process_variants', conn, if_exists='replace', index=False)
    bottlenecks.to_sql('transition_bottlenecks', conn, if_exists='replace', index=False)
    case_metrics.to_sql('case_metrics', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"-> Successfully stored all tables into SQLite database at: {db_path}")

def run_sample_queries(db_path="outputs/careflow.db"):
    """Runs sample SQL queries on the clinical database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print(" SQL QUERY RESULT: Top 3 Longest Transition Bottlenecks")
    print("="*50)
    query = """
        SELECT From_Activity, To_Activity, Avg_Duration_Hours 
        FROM transition_bottlenecks 
        ORDER BY Avg_Duration_Hours DESC 
        LIMIT 3;
    """
    for row in cursor.execute(query):
        print(f"From: {row[0]} -> To: {row[1]} | Avg Delay: {row[2]:.2f} hours")
        
    conn.close()

def run_advanced_clinical_queries(db_path="outputs/careflow.db"):
    """Runs advanced SQL analytics on event logs for clinical insights."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n" + "="*60)
    print(" ADVANCED SQL CLINICAL INSIGHTS")
    print("="*60)

    # 1. Check patient volume per main hospital unit / activity
    print("\n[Query 1] Top 5 Most Frequently Executed Clinical Activities:")
    activity_query = """
        SELECT "concept:name" AS Activity, COUNT(*) AS Execution_Count
        FROM event_log
        GROUP BY Activity
        ORDER BY Execution_Count DESC
        LIMIT 5;
    """
    for row in cursor.execute(activity_query):
        print(f"  - {row[0]}: {row[1]:,} occurrences")

    # 2. Average throughput duration from case metrics
    print("\n[Query 2] Overall Case Metrics Summary (from SQL):")
    metrics_query = """
        SELECT 
            COUNT(case:concept:name) AS Total_Cases,
            AVG(Event_Count) AS Avg_Events_Per_Case,
            AVG(Duration_Days) AS Avg_Duration_Days
        FROM case_metrics;
    """
    row = cursor.execute(metrics_query).fetchone()
    if row:
        print(f"  - Total Tracked Cases: {row[0]:,}")
        print(f"  - Avg Events per Patient: {row[1]:.1f}")
        print(f"  - Avg Patient Journey Duration: {row[2]:.1f} days")

    print("="*60)
    conn.close()
