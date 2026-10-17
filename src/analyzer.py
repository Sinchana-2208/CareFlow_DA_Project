# src/analyzer.py
import pandas as pd
import numpy as np

def extract_trace_variants(df_event):
    """
    Groups event logs by patient case to discover unique clinical pathways (trace variants).
    """
    # Ensure sorted by case and timestamp
    df_sorted = df_event.sort_values(by=['case:concept:name', 'time:timestamp'])
    
    # Group activities into a single ordered pathway string per case
    traces = df_sorted.groupby('case:concept:name')['concept:name'].apply(lambda x: ' -> '.join(x)).reset_index()
    traces.columns = ['Case_ID', 'Pathway_Trace']
    
    # Count frequency of each unique pathway trace
    variant_summary = traces['Pathway_Trace'].value_counts().reset_index()
    variant_summary.columns = ['Pathway_Trace', 'Case_Count']
    variant_summary['Percentage'] = (variant_summary['Case_Count'] / len(traces)) * 100
    
    return traces, variant_summary

def calculate_bottlenecks(df_event):
    """
    Calculates transition times between consecutive clinical activities to identify process bottlenecks.
    """
    df_sorted = df_event.sort_values(by=['case:concept:name', 'time:timestamp']).copy()
    
    # Shift to get the next activity and its timestamp within the same case
    df_sorted['next_activity'] = df_sorted.groupby('case:concept:name')['concept:name'].shift(-1)
    df_sorted['next_timestamp'] = df_sorted.groupby('case:concept:name')['time:timestamp'].shift(-1)
    
    # Filter out last events (where next_activity is NaN)
    transitions = df_sorted.dropna(subset=['next_activity', 'next_timestamp']).copy()
    
    # Calculate transition duration in hours
    transitions['transition_time_hours'] = (
        transitions['next_timestamp'] - transitions['time:timestamp']
    ).dt.total_seconds() / 3600.0
    
    # Group by activity pair (Source -> Target)
    bottleneck_summary = transitions.groupby(['concept:name', 'next_activity']).agg(
        Transition_Count=('transition_time_hours', 'count'),
        Avg_Duration_Hours=('transition_time_hours', 'mean'),
        Median_Duration_Hours=('transition_time_hours', 'median'),
        Max_Duration_Hours=('transition_time_hours', 'max')
    ).reset_index()
    
    bottleneck_summary.rename(
        columns={'concept:name': 'From_Activity', 'next_activity': 'To_Activity'}, 
        inplace=True
    )
    
    # Sort by longest average duration to highlight biggest bottlenecks
    bottleneck_summary = bottleneck_summary.sort_values(by='Avg_Duration_Hours', ascending=False)
    
    return bottleneck_summary
