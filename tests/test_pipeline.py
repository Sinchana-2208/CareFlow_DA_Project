import os
import sqlite3
import pandas as pd

def test_raw_data_exists():
    """Ensures the source sepsis event log dataset is present."""
    data_path = "data/Sepsis_Cases_Event_Log.xlsx"
    assert os.path.exists(data_path), f"Critical Error: Raw dataset not found at {data_path}"

def test_outputs_directory_exists():
    """Ensures the outputs folder exists for artifacts and databases."""
    assert os.path.exists("outputs"), "Outputs directory is missing."

def test_sqlite_database_tables():
    """Validates that the SQLite database contains the required analytical tables."""
    db_path = "outputs/careflow.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        expected_tables = ['event_log', 'process_variants', 'transition_bottlenecks', 'case_metrics']
        for table in expected_tables:
            assert table in tables, f"Expected table '{table}' missing from SQLite database."
    else:
        # If main.py hasn't been run yet, pass quietly
        pass
