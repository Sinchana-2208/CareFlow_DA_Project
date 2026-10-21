from src.loader import load_event_log
from src.cleaner import clean_event_log
from src.analyzer import extract_process_variants, calculate_transition_bottlenecks
from src.eda_plots import generate_eda_charts
from src.database import save_to_sqlite, run_sample_query

def main():
    print("=== Starting CareFlow Pipeline Execution ===")
    
    # 1. Ingest raw data
    raw_df = load_event_log()
    
    # 2. Clean and standardize data
    cleaned_df = clean_event_log(raw_df)
    
    # 3. Perform process mining & bottleneck analysis
    variants_df = extract_process_variants(cleaned_df)
    bottlenecks_df = calculate_transition_bottlenecks(cleaned_df)
    
    # 4. Generate visual summary charts
    generate_eda_charts(variants_df, bottlenecks_df)
    
    # 5. Persist tables into SQLite database
    save_to_sqlite(cleaned_df, variants_df, bottlenecks_df)
    
    # 6. Run validation query against database
    run_sample_query()
    
    print("=== CareFlow Pipeline Completed Successfully! ===")

if __name__ == "__main__":
    main()
