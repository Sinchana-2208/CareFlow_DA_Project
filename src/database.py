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
