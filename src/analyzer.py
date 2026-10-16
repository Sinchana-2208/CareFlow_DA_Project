import pandas as pd

def compute_case_durations(df_event):
    """
    Computes the total duration for each patient case from start to end timestamp.
    """
    print("[Analyzer] Calculating patient case durations...")
    durations = df_event.groupby('case:concept:name')['time:timestamp'].agg(['min', 'max'])
    durations['duration'] = durations['max'] - durations['min']
    
    print(f"[Analyzer] Computed durations for {len(durations)} unique cases.")
    return durations

def get_activity_summary(df_event):
    """
    Generates a frequency table of all clinical activities in the event log.
    """
    print("[Analyzer] Generating activity frequency summary...")
    summary = df_event['concept:name'].value_counts().reset_index()
    summary.columns = ['Activity', 'Frequency']
    return summary

if __name__ == "__main__":
    from loader import load_sepsis_data
    from cleaner import clean_event_log

    df_event, _ = load_sepsis_data()
    df_clean = clean_event_log(df_event)
    
    durations = compute_case_durations(df_clean)
    print(durations.head())
    
    activity_summary = get_activity_summary(df_clean)
    print(activity_summary.head(10))
