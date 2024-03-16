import matplotlib.pyplot as plt
import seaborn as sns


def plot_results(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Score", y="Name", data=df.sort_values("Score", ascending=True), hue="Strategy", dodge=False)
    plt.title("Scores of Agents by Strategy in the Iterative Prisoner's Dilemma")
    plt.xlabel("Score")
    plt.ylabel("Agent")
    plt.legend(title="Strategy", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='x')
    plt.show()