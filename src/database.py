import sqlite3
import pandas as pd
from pathlib import Path

def save_to_sqlite(cleaned_df: pd.DataFrame, variants_df: pd.DataFrame, bottlenecks_df: pd.DataFrame, db_path: str = "outputs/careflow.db"):
    """Save processed dataframes into a structured SQLite database."""
    path = Path(db_path)
    path.parent.mkdir(exist_ok=True, parents=True)
    
    conn = sqlite3.connect(path)
    
    # Write tables to SQLite
    cleaned_df.to_sql('event_logs', conn, if_exists='replace', index=False)
    variants_df.to_sql('process_variants', conn, if_exists='replace', index=False)
    bottlenecks_df.to_sql('transition_bottlenecks', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"Database successfully created and populated at: {path.resolve()}")

def run_sample_query(db_path: str = "outputs/careflow.db"):
    """Execute a sample query to demonstrate SQL capability."""
    conn = sqlite3.connect(db_path)
    query = """
        SELECT From_Activity, To_Activity, Mean_Duration_Hours, Transition_Count 
        FROM transition_bottlenecks 
        ORDER BY Mean_Duration_Hours DESC 
        LIMIT 3;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    print("\nSample SQL Query Result (Top Bottlenecks):")
    print(df)

if __name__ == "__main__":
    from src.loader import load_event_log
    from src.cleaner import clean_event_log
    from src.analyzer import extract_process_variants, calculate_transition_bottlenecks
    
    raw = load_event_log()
    cleaned = clean_event_log(raw)
    variants = extract_process_variants(cleaned)
    bottlenecks = calculate_transition_bottlenecks(cleaned)
    
    save_to_sqlite(cleaned, variants, bottlenecks)
    run_sample_query()
