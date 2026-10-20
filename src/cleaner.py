import pandas as pd

def clean_event_log(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the raw clinical event log."""
    cleaned_df = df.copy()
    
    # Standardize column names (strip whitespace, replace spaces with underscores)
    cleaned_df.columns = [col.strip().replace(" ", "_") for col in cleaned_df.columns]
    
    # Map common expected columns if necessary (adjusting based on standard Sepsis dataset schemas)
    # Typically: 'Case ID', 'Activity', 'Complete Timestamp'
    expected_cols = ['Case_ID', 'Activity', 'Complete_Timestamp']
    
    # Ensure timestamps are parsed properly in UTC
    if 'Complete_Timestamp' in cleaned_df.columns:
        cleaned_df['Complete_Timestamp'] = pd.to_datetime(cleaned_df['Complete_Timestamp'], utc=True)
    elif 'timestamp' in cleaned_df.columns:
        cleaned_df['Complete_Timestamp'] = pd.to_datetime(cleaned_df['timestamp'], utc=True)

    # Sort data by case and timestamp to maintain chronological event ordering
    if 'Case_ID' in cleaned_df.columns and 'Complete_Timestamp' in cleaned_df.columns:
        cleaned_df = cleaned_df.sort_values(by=['Case_ID', 'Complete_Timestamp']).reset_index(drop=True)
        
    # Drop rows with missing critical values
    cleaned_df = cleaned_df.dropna(subset=['Case_ID', 'Activity'])
    
    print(f"Data cleaned. Active records remaining: {len(cleaned_df)}")
    return cleaned_df

if __name__ == "__main__":
    from src.loader import load_event_log
    raw_df = load_event_log()
    clean_df = clean_event_log(raw_df)
    print(clean_df.head(2))
