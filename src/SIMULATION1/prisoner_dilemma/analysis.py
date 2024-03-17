import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_results(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Score", y="Name", data=df.sort_values("Score", ascending=True), hue="Strategy", dodge=False)
    plt.title("Scores of Agents by Strategy in the Iterative Prisoner's Dilemma")
    plt.xlabel("Score")
    plt.ylabel("Agent")
    plt.legend(title="Strategy", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='x')
    plt.show()


def check_results():

    results_df = pd.read_csv('results.csv')

    results_summary = {
        'Total Rounds': results_df['Round'].nunique(),
        'Total Matches': results_df.shape[0],
        'Unique Agents': results_df['Agent1'].nunique(),  # Assuming Agent1 and Agent2 columns contain the same set of agents
    }
    results_df['Agent1_Win'] = results_df['Payoff1'] > 0
    win_rates = results_df.groupby('Agent1')['Agent1_Win'].mean()
    decision_frequencies = pd.concat([
        results_df['Decision1'].value_counts(normalize=True),
        results_df['Decision2'].value_counts(normalize=True)
    ], axis=1)
    decision_frequencies.columns = ['Decision1_Frequency', 'Decision2_Frequency']
    results_summary, win_rates, decision_frequencies.head()
        