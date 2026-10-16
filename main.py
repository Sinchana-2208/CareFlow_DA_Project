# ==========================================
# CareFlow: Clinical Pathway Process Mining
# Sepsis Cases Event Log Analysis & EDA
# ==========================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- STEP 1: Load the Sepsis Event Log ---
print("--- Step 1: Loading Sepsis Event Log ---")
file_path = "data/Sepsis_Cases_Event_Log.xlsx" # Updated to point to the data/ folder

if os.path.exists(file_path):
    df_event = pd.read_excel(file_path, sheet_name='Event Log')
    df_summary = pd.read_excel(file_path, sheet_name='Cases Summary')
    print("Sepsis Event Log loaded successfully!")
    print(f"Total Event Rows: {df_event.shape[0]}")
    print(f"Total Patient Cases: {df_summary.shape[0]}")
else:
    print(f"File {file_path} not found. Please ensure the Excel file is in the data/ folder.")

# --- STEP 2: Data Cleaning & Preprocessing ---
print("\n--- Step 2: Cleaning Event Log Data ---")
# Drop rows where case name or timestamp is missing
df_event = df_event.dropna(subset=['case:concept:name', 'time:timestamp'])

# Convert timestamp to datetime
df_event['time:timestamp'] = pd.to_datetime(df_event['time:timestamp'])

# Check for duplicate events
duplicates_count = df_event.duplicated().sum()
print(f"Number of duplicate rows: {duplicates_count}")
if duplicates_count > 0:
    df_event = df_event.drop_duplicates()
    print("Duplicates removed!")

print("\n=== Event Log Info After Cleaning ===")
print(df_event.info())

# --- STEP 3: Exploratory Data Analysis & Visualizations ---
print("\n--- Step 3: Generating Process Mining Visualizations ---")
sns.set_theme(style="whitegrid")

# Create a figure with subplots for process insights
fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# Plot 1: Top 10 Most Frequent Clinical Activities
top_activities = df_event['concept:name'].value_counts().head(10).reset_index()
top_activities.columns = ['Activity', 'Count']

sns.barplot(
    data=top_activities,
    x='Count',
    y='Activity',
    palette='Blues_r',
    hue='Activity',
    legend=False,
    ax=axes[0]
)
axes[0].set_title('Top 10 Most Frequent Clinical Activities', fontsize=14, pad=15)
axes[0].set_xlabel('Event Frequency', fontsize=12)
axes[0].set_ylabel('Clinical Activity', fontsize=12)

# Plot 2: Patient Age Distribution (from Summary/Event Data)
if 'Age' in df_event.columns:
    age_data = df_event['Age'].dropna()
    sns.histplot(
        age_data, 
        bins=20, 
        kde=True, 
        color='teal', 
        ax=axes[1]
    )
    axes[1].set_title('Patient Age Distribution in Sepsis Cases', fontsize=14, pad=15)
    axes[1].set_xlabel('Age', fontsize=12)
    axes[1].set_ylabel('Patient Count', fontsize=12)

plt.tight_layout()
plt.show()

print("\n--- Sepsis Process Analysis Script Executed Successfully! ---")
