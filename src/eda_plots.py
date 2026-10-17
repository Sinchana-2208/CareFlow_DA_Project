import matplotlib.pyplot as plt
import seaborn as sns

def plot_top_activities(df_event, top_n=10):
    """
    Plots the top N most frequent clinical activities in the Sepsis event log.
    """
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 5))

    top_activities = df_event['concept:name'].value_counts().head(top_n).reset_index()
    top_activities.columns = ['Activity', 'Count']

    sns.barplot(
        data=top_activities,
        x='Count',
        y='Activity',
        palette='Blues_r',
        hue='Activity',
        legend=False,
        ax=ax
    )

    ax.set_title(f'Top {top_n} Most Frequent Clinical Activities', fontsize=14, pad=15)
    ax.set_xlabel('Event Frequency', fontsize=12)
    ax.set_ylabel('Clinical Activity', fontsize=12)

    plt.tight_layout()
    return fig

if __name__ == "__main__":
    from loader import load_sepsis_data
    from cleaner import clean_event_log

    df_event, _ = load_sepsis_data()
    df_clean = clean_event_log(df_event)
    fig = plot_top_activities(df_clean)
    plt.show()
