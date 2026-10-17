# ==========================================
# CareFlow: Clinical Pathway Process Mining
# Sepsis Cases Event Log Analysis & EDA
# ==========================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import modular helper from src/
from src.analyzer import extract_trace_variants, calculate_bottlenecks

# --- STEP 1: Load the Sepsis Event Log ---
print("--- Step 1: Loading Sepsis Event Log ---")
file_path = "data/Sepsis_Cases_Event_Log.xlsx"

if os.path.exists(file_path):
    df_event = pd.read_excel(file_path, sheet_name='Event Log')
    df_summary = pd.read_excel(file_path, sheet_name='Cases Summary')
    print("Sepsis Event Log loaded successfully!")
    print(f"Total Event Rows: {df_event.shape[0]}")
    print(f"Total Patient Cases: {df_summary.shape[0]}")
else:
    raise FileNotFoundError(f"File {file_path} not found. Please ensure it is in the data/ folder.")

# --- STEP 2: Data Cleaning & Preprocessing ---
print("\n--- Step 2: Cleaning Event Log Data ---")
df_event = df_event.dropna(subset=['case:concept:name', 'time:timestamp'])
df_event['time:timestamp'] = pd.to_datetime(df_event['time:timestamp'], utc=True)
duplicates_count = df_event.duplicated().sum()
if duplicates_count > 0:
    df_event = df_event.drop_duplicates()
    print(f"Removed {duplicates_count} duplicate rows.")

# --- STEP 3: Process Mining Analytics (Variants & Bottlenecks) ---
print("\n--- Step 3: Running Process Mining Analysis ---")

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

# 1. Trace Variant Discovery
case_traces, variant_summary = extract_trace_variants(df_event)
variants_path = os.path.join(output_dir, "process_variants.csv")
variant_summary.to_csv(variants_path, index=False)
print(f"-> Discovered {len(variant_summary)} unique process variants. Saved to: {variants_path}")

# 2. Transition Bottlenecks
bottlenecks = calculate_bottlenecks(df_event)
bottlenecks_path = os.path.join(output_dir, "transition_bottlenecks.csv")
bottlenecks.to_csv(bottlenecks_path, index=False)
print(f"-> Calculated activity transition metrics. Saved to: {bottlenecks_path}")

# 3. Case Summary Metrics
case_metrics = df_event.groupby('case:concept:name').agg(
    Event_Count=('concept:name', 'count'),
    Start_Time=('time:timestamp', 'min'),
    End_Time=('time:timestamp', 'max')
).reset_index()
case_metrics['Duration_Days'] = (case_metrics['End_Time'] - case_metrics['Start_Time']).dt.total_seconds() / (24 * 3600)
case_metrics_path = os.path.join(output_dir, "case_metrics_summary.csv")
case_metrics.to_csv(case_metrics_path, index=False)
print(f"-> Exported case throughput metrics to: {case_metrics_path}")

# --- STEP 4: Visualizations ---
print("\n--- Step 4: Generating Process Visualizations ---")
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Plot 1: Top 10 Most Common Process Variants
top_variants = variant_summary.head(10).copy()
top_variants['Variant_Label'] = [f"Variant {i+1}" for i in range(len(top_variants))]

sns.barplot(
    data=top_variants,
    x='Case_Count',
    y='Variant_Label',
    palette='Blues_r',
    hue='Variant_Label',
    legend=False,
    ax=axes[0]
)
axes[0].set_title('Top 10 Clinical Trace Variants Frequency', fontsize=14, pad=15)
axes[0].set_xlabel('Number of Patient Cases', fontsize=12)
axes[0].set_ylabel('Pathway Variant', fontsize=12)

# Plot 2: Top 10 Transitions with Longest Average Delay (Bottlenecks)
top_bottlenecks = bottlenecks.head(10).copy()
top_bottlenecks['Transition'] = top_bottlenecks['From_Activity'] + ' -> ' + top_bottlenecks['To_Activity']

sns.barplot(
    data=top_bottlenecks,
    x='Avg_Duration_Hours',
    y='Transition',
    palette='Reds_r',
    hue='Transition',
    legend=False,
    ax=axes[1]
)
axes[1].set_title('Top 10 Clinical Activity Bottlenecks (Avg Hours)', fontsize=14, pad=15)
axes[1].set_xlabel('Average Delay (Hours)', fontsize=12)
axes[1].set_ylabel('Clinical Step Transition', fontsize=12)

plt.tight_layout()
plot_path = os.path.join(output_dir, "process_variants_and_bottlenecks.png")
plt.savefig(plot_path, dpi=300)
print(f"-> Saved process analysis chart to: {plot_path}")

plt.show()

print("\n--- CareFlow Process Analytics Pipeline Completed Successfully! ---")
