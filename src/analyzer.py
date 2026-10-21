import pandas as pd

def extract_process_variants(df: pd.DataFrame) -> pd.DataFrame:
    """Group events per case to identify dominant clinical pathways (variants)."""
    # Sort just to be safe
    df_sorted = df.sort_values(by=['Case_ID', 'Complete_Timestamp'])
    
    # Aggregate activities into a tuple/string sequence per case
    variants = (
        df_sorted.groupby('Case_ID')['Activity']
        .apply(lambda x: ' -> '.join(x))
        .reset_index(name='Process_Variant')
    )
    
    # Count frequency of each variant
    variant_counts = (
        variants['Process_Variant']
        .value_counts()
        .reset_index()
    )
    variant_counts.columns = ['Process_Variant', 'Case_Count']
    
    print(f"Discovered {len(variant_counts)} unique process variants across cases.")
    return variant_counts

def calculate_transition_bottlenecks(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate average time differences between consecutive events to spot bottlenecks."""
    df_sorted = df.sort_values(by=['Case_ID', 'Complete_Timestamp']).copy()
    
    # Shift timestamps and activities to get the 'next' event metrics per case
    df_sorted['Next_Activity'] = df_sorted.groupby('Case_ID')['Activity'].shift(-1)
    df_sorted['Next_Timestamp'] = df_sorted.groupby('Case_ID')['Complete_Timestamp'].shift(-1)
    
    # Calculate duration between current event and next event
    df_sorted['Transition_Duration'] = (df_sorted['Next_Timestamp'] - df_sorted['Complete_Timestamp']).dt.total_seconds() / 3600 # in hours
    
    # Filter out rows where next activity is null (end of case)
    transitions = df_sorted.dropna(subset=['Next_Activity', 'Transition_Duration']).copy()
    
    # Group by transition pair and find average delay
    bottlenecks = (
        transitions.groupby(['Activity', 'Next_Activity'])['Transition_Duration']
        .agg(['mean', 'median', 'count'])
        .reset_index()
    )
    bottlenecks.columns = ['From_Activity', 'To_Activity', 'Mean_Duration_Hours', 'Median_Duration_Hours', 'Transition_Count']
    bottlenecks = bottlenecks.sort_values(by='Mean_Duration_Hours', ascending=False).reset_index(drop=True)
    
    print(f"Analyzed {len(bottlenecks)} unique step transitions for bottlenecks.")
    return bottlenecks

if __name__ == "__main__":
    from src.loader import load_event_log
    from src.cleaner import clean_event_log
    
    raw = load_event_log()
    cleaned = clean_event_log(raw)
    
    variants = extract_process_variants(cleaned)
    print("\nTop 3 Process Variants:")
    print(variants.head(3))
    
    bottlenecks = calculate_transition_bottlenecks(cleaned)
    print("\nTop 3 Slowest Transition Bottlenecks:")
    print(bottlenecks.head(3))
