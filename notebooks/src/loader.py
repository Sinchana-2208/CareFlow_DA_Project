import os
import pandas as pd

def load_sepsis_data(file_path="Sepsis_Cases_Event_Log.xlsx"):
    """
    Loads Sepsis event log and summary datasets from the specified Excel file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found in root directory.")
    
    df_event = pd.read_excel(file_path, sheet_name='Event Log')
    df_summary = pd.read_excel(file_path, sheet_name='Cases Summary')
    
    print(f"[Loader] Loaded Event Log: {df_event.shape[0]} rows")
    print(f"[Loader] Loaded Cases Summary: {df_summary.shape[0]} cases")
    
    return df_event, df_summary

if __name__ == "__main__":
    df_event, df_summary = load_sepsis_data()
