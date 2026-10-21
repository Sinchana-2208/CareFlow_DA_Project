import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def generate_eda_charts(variants_df: pd.DataFrame, bottlenecks_df: pd.DataFrame, output_dir: str = "outputs"):
    """Generate and save summary visual charts for process analytics."""
    out_path = Path(output_dir)
    out_path.mkdir(exist_ok=True, parents=True)
    
    # Set plotting style
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Top Process Variants
    plt.figure(figsize=(10, 6))
    top_variants = variants_df.head(5)
    sns.barplot(data=top_variants, x='Case_Count', y='Process_Variant', palette='Blues_r')
    plt.title('Top 5 Clinical Process Variants by Case Volume')
    plt.xlabel('Number of Cases')
    plt.ylabel('Process Sequence')
    plt.tight_layout()
    chart1_path = out_path / 'top_variants.png'
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    
    # Plot 2: Top Bottlenecks (Longest Mean Durations)
    plt.figure(figsize=(10, 6))
    top_bottlenecks = bottlenecks_df.head(5).copy()
    top_bottlenecks['Transition'] = top_bottlenecks['From_Activity'] + " -> " + top_bottlenecks['To_Activity']
    sns.barplot(data=top_bottlenecks, x='Mean_Duration_Hours', y='Transition', palette='Reds_r')
    plt.title('Top 5 Transition Bottlenecks (Mean Duration in Hours)')
    plt.xlabel('Mean Duration (Hours)')
    plt.ylabel('Clinical Transition Step')
    plt.tight_layout()
    chart2_path = out_path / 'top_bottlenecks.png'
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    
    print(f"EDA charts successfully generated and saved to {out_path.resolve()}")

if __name__ == "__main__":
    from src.loader import load_event_log
    from src.cleaner import clean_event_log
    from src.analyzer import extract_process_variants, calculate_transition_bottlenecks
    
    raw = load_event_log()
    cleaned = clean_event_log(raw)
    variants = extract_process_variants(cleaned)
    bottlenecks = calculate_transition_bottlenecks(cleaned)
    
    generate_eda_charts(variants, bottlenecks)
