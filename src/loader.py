import pandas as pd
from pathlib import Path

def load_event_log(file_path: str = "data/Sepsis_Cases_Event_Log.xlsx") -> pd.DataFrame:
    """Load the raw Sepsis clinical event log dataset from Excel."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Event log file not found at: {path}")
    
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(path)
    print(f"Successfully loaded {len(df)} rows from {path.name}")
    
    return df

if __name__ == "__main__":
    # Quick test execution
    df = load_event_log()
    print(df.head(2))
