import pandas as pd

def clean_event_log(df_event):
    """
    Cleans the Sepsis event log by handling missing values, 
    converting timestamps, and removing duplicate rows.
    """
    initial_count = len(df_event)
    print(f"[Cleaner] Initial row count: {initial_count}")

    # Drop rows with missing critical fields
    df_clean = df_event.dropna(subset=['case:concept:name', 'time:timestamp']).copy()

    # Convert timestamp to standard datetime format
    df_clean['time:timestamp'] = pd.to_datetime(df_clean['time:timestamp'])

    # Remove duplicates
    duplicates_count = df_clean.duplicated().sum()
    if duplicates_count > 0:
        df_clean = df_clean.drop_duplicates()
        print(f"[Cleaner] Removed {duplicates_count} duplicate rows.")

    print(f"[Cleaner] Final clean row count: {len(df_clean)}")
    return df_clean

if __name__ == "__main__":
    from loader import load_sepsis_data
    df_event, _ = load_sepsis_data()
    cleaned_df = clean_event_log(df_event)
